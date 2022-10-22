import re

from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId, SubFieldIdentifiers
from Configuration.ErrorMessages import ErrorMessages
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from IcaoMessageParser.Utils import Utils
from Tokenizer.Tokenize import Tokenize


class ParseF19(ParseFieldsCommon):
    """This class parses ICAO field 19; this class subclasses ParseFieldsCommon. This class
    initialises the super class with information specific for parsing field 19, namely:

    - A flight plan record, instance of FlightPlanRecord
    - Configuration data defining the subfields contained in this field,
      see configuration data in the SubFieldsInFields class
    - Configuration data defining the subfields that a field comprises,
      see configuration data in the SubFieldDescriptions class"""

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 19.

            :param flight_plan_record: Flight plan to populate
            :param sfif: Configuration data defining the subfields in an ICAO field
            :param sfd: Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F19,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F19),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F19))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        """This method is the program entry point to parse ICAO field 19. Most of the parsing
        is carried out by the super class ParseFieldCommon.parse_compound_field_common().
        This method perform rudimentary checks, sets up a list of errors that are
        general to all keyword/subfields and calls the parser in the super class.
            :return: None"""

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, ErrorId.F19_DATA_MISSING)
            return

        # If there is a single token it has to be an error
        if self.get_tokens().get_number_of_tokens() == 1:
            # Report an error, cant do anything with a single token
            self.add_error(self.get_tokens().get_first_token().get_token_string(),
                           self.get_tokens().get_first_token().get_token_start_index(),
                           self.get_tokens().get_first_token().get_token_end_index(),
                           ErrorId.F19_ZERO_OR_KEYWORDS)
            return

        # Two or more tokens present in field 19 if we get this far
        # Declare the errors to be used
        error_codes = [ErrorId.F19_NO_F19_KEYWORDS_FOUND, ErrorId.F19_UNRECOGNISED_DATA,
                       ErrorId.F19_UNRECOGNISED_KEYWORD, ErrorId.F19_ZERO_OR_KEYWORDS]

        # Call the compound field parser that will initially parse field 19.
        # Note that this parser does not parse the data for each individual field 19 keyword,
        # it saves valid keywords with their respective data and generates errors for unknown keywords
        # and any other junk in field 19 that is not part of a keyword's data.
        self.parse_compound_field_common(error_codes, self.is_compound_field_keyword)

        # Loop over the individual subfields and parse as appropriate;
        self.parse_compound_subfields(SubFieldIdentifiers.F19a, SubFieldIdentifiers.F19s)

    def parse_compound_subfields(self, subfield_start, subfield_end):
        # type: (SubFieldIdentifiers, SubFieldIdentifiers) -> None
        """This method loops over all the F!* subfields and parses the individual subfields.

        :param subfield_start: The lowest F18 subfield enumeration value to limit the range of
               loop when looping over the subfields, only need to loop over the F18 subfields;
        :param subfield_end: The highest F18 subfield enumeration value to limit the range of
               loop when looping over the subfields, only need to loop over the F18 subfields;
        :return: None
        """

        # Get the field 19 FieldRecord that contains zero or more F19 subfields
        field_record = self.get_flight_plan_record().get_icao_field(self.get_field_identifier())

        # Get the dictionary containing all the field 19 subfields stored in the flight plan
        subfield_dictionary = field_record.get_subfield_dictionary()

        # Loop over the dictionary of subfields and parse each individual subfield
        for subfield_key, subfield_list in subfield_dictionary.items():
            # Make sure subfield identifiers are valid F19 subfield enumeration values
            if subfield_start <= subfield_key <= subfield_end:
                # Loop over the list of subfields and parse the field;
                for subfield in subfield_list:
                    # print(subfield_key.name)
                    # print(subfield.get_field_text())
                    match subfield_key:
                        case SubFieldIdentifiers.F19a:
                            Utils.parse_for_regexp(
                                self.get_flight_plan_record(), subfield, ErrorId.F19_A_SYNTAX, "[A-Z0-9 ]+")
                        case SubFieldIdentifiers.F19c:
                            Utils.parse_for_regexp(
                                self.get_flight_plan_record(), subfield, ErrorId.F19_C_SYNTAX, "[A-Z0-9 ]+")
                        case SubFieldIdentifiers.F19d:
                            self.parse_f19_d(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F19e:
                            self.parse_f19_e(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F19j:
                            self.parse_f19_j(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F19n:
                            Utils.parse_for_regexp(
                                self.get_flight_plan_record(), subfield, ErrorId.F19_N_SYNTAX, "[A-Z0-9 ]+")
                        case SubFieldIdentifiers.F19p:
                            self.parse_f19_p(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F19r:
                            self.parse_f19_r(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F19s:
                            self.parse_f19_s(self.get_flight_plan_record(), subfield, self.sfd)
                        case _:
                            # The following F18 require no special parsing other than
                            # checking for valid characters;
                            # [A-Z0-9., \n\r\t:;']
                            pass

    @staticmethod
    def parse_f19_d(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'D' subfields are syntactically and semantically correct.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Tokenize the IFP subfield
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        if tokens.get_number_of_tokens() < 1:
            # This gets picked up by the compound field parser
            return

        # Check if there are too few tokens
        if tokens.get_number_of_tokens() < 3:
            # Too few subfields, error
            end_index = tokens.get_token_at(tokens.get_number_of_tokens() - 1).get_token_end_index()
            Utils.add_error(flight_plan_record, subfield.get_field_text()[0:end_index],
                            0,
                            end_index,
                            ErrorMessages(),
                            ErrorId.F19_D_TOO_FEW)
            return

        # Check if there are more than four tokens
        if tokens.get_number_of_tokens() > 4:
            # Too many subfields, error
            start_index = tokens.get_token_at(4).get_token_start_index()
            end_index = tokens.get_token_at(tokens.get_number_of_tokens() - 1).get_token_end_index()
            Utils.add_error(flight_plan_record, subfield.get_field_text()[start_index:end_index],
                            start_index,
                            end_index,
                            ErrorMessages(),
                            ErrorId.F19_D_TOO_MANY)
            return

        # Loop over the tokens
        idx = 0
        error_id = None
        regexp = ""
        for token in tokens.get_tokens():

            # Validate the subfield against the valid syntax
            match idx:
                case 0:
                    error_id = ErrorId.F19_Da_SYNTAX
                    regexp = "[0-9]{1,2}"
                case 1:
                    error_id = ErrorId.F19_Db_SYNTAX
                    regexp = "[0-9]{1,3}"
                case 2:
                    if tokens.get_number_of_tokens() == 3:
                        error_id = ErrorId.F19_Dd_SYNTAX
                        regexp = "[A-Z]+"
                    else:
                        error_id = ErrorId.F19_Dc_SYNTAX
                        regexp = "C"
                case 3:
                    error_id = ErrorId.F19_Dd_SYNTAX
                    regexp = "[A-Z]+"

            # Validate the 'D' subfield against the valid syntax
            mo = re.fullmatch(regexp, token.get_token_string())
            if mo is None:
                # Did not match, report an error
                Utils.add_error(flight_plan_record,
                                token.get_token_string(),
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index(),
                                ErrorMessages(),
                                error_id)

            idx += 1

    @staticmethod
    def parse_f19_e(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'E' subfield syntax conforms to a time in HHMM
        format.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F19_E_TOO_MANY):
            return

        # Parse the 'E subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F19_E_SYNTAX, "[ ]*" + sfd.hhmm + "[ ]*")

    @staticmethod
    def parse_f19_j(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'J' subfield syntax conforms to one of the frequency
        life jacket capability indicators 'F', 'L', 'U' or 'V'.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F19_J_TOO_MANY):
            return

        # Parse the 'E' subfield
        f_ = subfield.get_field_text().count("F")
        l_ = subfield.get_field_text().count("L")
        u_ = subfield.get_field_text().count("U")
        v_ = subfield.get_field_text().count("V")
        if f_ > 1 or l_ > 1 or u_ > 1 or v_ > 1 or f_ + l_ + u_ + v_ == 0:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F19_J_SYNTAX)
            return

        # Let regexp processing check that the string only consists the correct character set
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F19_J_SYNTAX, "[ ]*[FLUV]{1,4}[ ]*")

    @staticmethod
    def parse_f19_p(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'P' subfield syntax conforms to 1 to 3 digits
        format.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F19_P_TOO_MANY):
            return

        # Parse the 'P' subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F19_P_SYNTAX, "[ ]*[0-9]{1,3}[ ]*")

    @staticmethod
    def parse_f19_r(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'R' subfield syntax conforms to one of the frequency
        available indicators 'U', 'V' or 'E'.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F19_J_TOO_MANY):
            return

        # Parse the 'R' subfield
        e_ = subfield.get_field_text().count("E")
        u_ = subfield.get_field_text().count("U")
        v_ = subfield.get_field_text().count("V")
        if e_ > 1 or u_ > 1 or v_ > 1 or e_ + u_ + v_ == 0:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F19_R_SYNTAX)
            return

        # Parse the 'R' subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F19_R_SYNTAX, "[ ]*[EUV]{1,3}[ ]*")

    @staticmethod
    def parse_f19_s(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F19 'S' subfield syntax conforms to one of the survival
        equipment indicators 'D', 'J', 'M' or 'P'.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F19_S_TOO_MANY):
            return

        # Parse the 'S' subfield
        d_ = subfield.get_field_text().count("D")
        j_ = subfield.get_field_text().count("J")
        m_ = subfield.get_field_text().count("M")
        p_ = subfield.get_field_text().count("P")
        if d_ > 1 or j_ > 1 or m_ > 1 or p_ > 1 or d_ + j_ + m_ + p_ == 0:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F19_S_SYNTAX)
            return

        # Parse the 'S' subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F19_S_SYNTAX, "[ ]*[DJMP]{1,4}[ ]*")
