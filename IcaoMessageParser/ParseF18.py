import re

from Configuration.ErrorMessages import ErrorMessages
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId, SubFieldIdentifiers
from IcaoMessageParser.ParseF14 import ParseF14
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from IcaoMessageParser.Utils import Utils
from Tokenizer.Tokenize import Tokenize


class ParseF18(ParseFieldsCommon):
    """This class parses ICAO field 18; this class subclasses ParseFieldsCommon. This class
    initialises the super class with information specific for parsing field 18, namely:

    - A flight plan record, instance of FlightPlanRecord
    - Configuration data defining the subfields contained in this field,
      see configuration data in the SubFieldsInFields class
    - Configuration data defining the subfields that a field comprises,
      see configuration data in the SubFieldDescriptions class"""

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 18.

            :param flight_plan_record: Flight plan to populate
            :param sfif: Configuration data defining the subfields in an ICAO field
            :param sfd: Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F18,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F18),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F18))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        """This method is the program entry point to parse ICAO field 18. Most of the parsing
        is carried out by the super class ParseFieldCommon.parse_compound_field_common().
        This method performs rudimentary checks, sets up a list of errors that are
        general to all keyword/subfields and calls the parser in the super class.
            :return: None"""

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, ErrorId.F18_DATA_MISSING)
            return

        # If there is a single token it can only be a '0' (zero), otherwise it's an error
        if self.get_tokens().get_number_of_tokens() == 1:
            if self.get_tokens().get_first_token().get_token_string() != "0":
                # Report an error, cant do anything with a single token
                self.add_error(self.get_tokens().get_first_token().get_token_string(),
                               self.get_tokens().get_first_token().get_token_start_index(),
                               self.get_tokens().get_first_token().get_token_end_index(),
                               ErrorId.F18_ZERO_OR_KEYWORDS)
            return

        # Two or more tokens present in field 18 if we get this far
        # Declare the errors to be used
        error_codes = [ErrorId.F18_NO_F18_KEYWORDS_FOUND, ErrorId.F18_UNRECOGNISED_DATA,
                       ErrorId.F18_UNRECOGNISED_KEYWORD, ErrorId.F18_ZERO_OR_KEYWORDS]

        # Call the compound field parser that will initially parse field 18.
        # Note that this parser does not parse the data for each individual field 18 keyword,
        # it saves valid keywords with their respective data and generates errors for unknown keywords
        # and any other junk in field 18 that is not part of a keyword's data.
        self.parse_compound_field_common(error_codes, self.is_compound_field_keyword)

        # Loop over the individual subfields and parse as appropriate;
        self.parse_compound_subfields(SubFieldIdentifiers.F18altn, SubFieldIdentifiers.F18typ)

    def parse_compound_subfields(self, subfield_start, subfield_end):
        # type: (SubFieldIdentifiers, SubFieldIdentifiers) -> None
        """This method loops over all the F18 subfields and parses the individual subfields.

        :param subfield_start: The lowest F18 subfield enumeration value to limit the range of
               loop when looping over the subfields, only need to loop over the F18 subfields;
        :param subfield_end: The highest F18 subfield enumeration value to limit the range of
               loop when looping over the subfields, only need to loop over the F18 subfields;
        :return: None
        """

        # Get the field 18 FieldRecord that contains zero or more F18 subfields
        field_record = self.get_flight_plan_record().get_icao_field(self.get_field_identifier())

        # Get the dictionary containing all the field 18 subfields stored in the flight plan
        subfield_dictionary = field_record.get_subfield_dictionary()

        # Loop over the dictionary of subfields and parse each individual subfield
        for subfield_key, subfield_list in subfield_dictionary.items():
            # Make sure subfield identifiers are valid F18 subfield enumeration values
            if subfield_start <= subfield_key <= subfield_end:
                # Loop over the list of subfields and parse the field;
                for subfield in subfield_list:
                    # print(subfield_key.name)
                    # print(subfield.get_field_text())
                    match subfield_key:
                        case SubFieldIdentifiers.F18altn:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_ALTN_SYNTAX)
                        case SubFieldIdentifiers.F18code:
                            Utils.parse_for_hex_address(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_CODE_SYNTAX)
                        case SubFieldIdentifiers.F18com:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_COM_SYNTAX)
                        case SubFieldIdentifiers.F18dat:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_DAT_SYNTAX)
                        case SubFieldIdentifiers.F18dep:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_DEP_SYNTAX)
                        case SubFieldIdentifiers.F18dest:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_DEST_SYNTAX)
                        case SubFieldIdentifiers.F18dle:
                            self.parse_f18_dle(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18dof:
                            self.parse_f18_dof(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_DOF_F18A_SYNTAX)
                        case SubFieldIdentifiers.F18eet:
                            self.parse_f18_eet(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18est:
                            # self.parse_f18_est(self.get_flight_plan_record(), subfield, self.sfd)
                            # Parsing for this field is currently not supported, the reason is that this
                            # subfield is a field 14, which contains a slash. The Field 18 compound parser
                            # sees the point before the slash as an unknown field 18 keyword.
                            # If this field is need to be parsed this will have to be revisited.
                            # For now, pass
                            pass
                        case SubFieldIdentifiers.F18ifp:
                            self.parse_f18_ifp(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18nav:
                            # TODO F18 NAV May require further work once F10 parsing is done
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_NAV_SYNTAX)
                        case SubFieldIdentifiers.F18opr:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_OPR_SYNTAX)
                        case SubFieldIdentifiers.F18orgn:
                            self.parse_f18_orgn(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18pbn:
                            self.parse_f18_pbn(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18per:
                            self.parse_f18_per(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18ralt:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_RALT_SYNTAX)
                        case SubFieldIdentifiers.F18reg:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_REG_SYNTAX)
                        case SubFieldIdentifiers.F18rif:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_RIF_SYNTAX)
                        case SubFieldIdentifiers.F18rfp:
                            self.parse_f18_rfp(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18rmk:
                            self.parse_f18_rmk(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18rvr:
                            self.parse_f18_rvr(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sel:
                            self.parse_f18_sel(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sts:
                            self.parse_f18_sts(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18src:
                            self.parse_f18_src(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sur:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_SUR_SYNTAX)
                        case SubFieldIdentifiers.F18talt:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_TALT_SYNTAX)
                        case SubFieldIdentifiers.F18typ:
                            self.parse_f18_typ(self.get_flight_plan_record(), subfield, self.sfd)
                        case _:
                            # The following F18 require no special parsing other than
                            # checking for valid characters;
                            # [A-Z0-9., \n\r\t:;']
                            pass

    @staticmethod
    def parse_f18_dle(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the field 18 DLE subfield syntax conforms to a point
        followed by a time in HHMM format. The point can be any type, i.e. PRP, latitude/longitude
        or a bearing distance.

        To parse this field, it is assumed that the last 4 characters are the time, the rest some kind of
        point. The point and hhmm subfield definitions will be used to parse the two parts
        of this field. Errors are reported if this subfield is not a 'point hhmm' string.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 6:
            # The field is too short, minimum is a two letter point followed by HHMM
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_DLE_TOO_SHORT)
            return

        # Check if there are more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_DLE_TOO_MANY):
            return

        # Split the time from the point
        split_field = Utils.split_on_index(subfield.get_field_text(), len(subfield.get_field_text()) - 4)

        # Validate the point
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F14a).get_field_syntax(),
                          split_field[0])
        if mo is None:
            Utils.add_error(flight_plan_record,
                            subfield.get_field_text()[0:len(subfield.get_field_text()) - 4],
                            subfield.get_start_index(),
                            subfield.get_end_index() - 4,
                            ErrorMessages(),
                            ErrorId.F18_DLE_PNT_SYNTAX)

        # Validate the time
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F16b).get_field_syntax(),
                          split_field[1])
        if mo is None:
            Utils.add_error(flight_plan_record,
                            subfield.get_field_text()[len(subfield.get_field_text()) - 4:],
                            subfield.get_start_index() + len(subfield.get_field_text()) - 4,
                            subfield.get_end_index(),
                            ErrorMessages(),
                            ErrorId.F18_DLE_TIME_SYNTAX)

    @staticmethod
    def parse_f18_dof(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> None
        """This method validates that the subfield text string conforms to the DOF format
        YYMMDD, if not an error is added to the flight plan record.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param error_id: The error message that will be reported if the subfield text does not
               match the regular expression;
        :return: None
        """
        if not Utils.is_dof(subfield.get_field_text()):
            Utils.add_subfield_error(flight_plan_record, subfield, error_id.F18_DOF_F18A_SYNTAX)

    @staticmethod
    def parse_f18_eet(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates the F18 EET field; this field consists of one or more
        point & time tokens. The field will be tokenized and each token parsed for correct syntax
        and semantics. Each token syntax must conform to a point followed by a time in HHMM format.
        The point can be any type, i.e. PRP, latitude/longitude or a bearing distance.

        To parse this field, it is assumed that the last 4 characters in a token are the time, the
        rest some kind of point. The point and hhmm subfield definitions will be used to parse the
        two parts of this field. Errors are reported if any part of these subfield tokens is not a
        'point hhmm' string.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Tokenize the EET field, there can be a lot of these subfields in a message
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Split the time from the point
            split_field = Utils.split_on_index(token.get_token_string(), len(token.get_token_string()) - 4)

            # Validate the point
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F14a).get_field_syntax(),
                              split_field[0])
            if mo is None:
                # Report an error, point syntax is invalid
                Utils.add_error(flight_plan_record,
                                token.get_token_string()[0:len(token.get_token_string()) - 4],
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index() - 4,
                                ErrorMessages(),
                                ErrorId.F18_EET_PNT_SYNTAX)

            # Validate the time
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F16b).get_field_syntax(),
                              split_field[1])
            if mo is None:
                # Report an error, time syntax is invalid
                Utils.add_error(
                    flight_plan_record,
                    token.get_token_string()[len(token.get_token_string()) - 4:],
                    token.get_token_start_index() + subfield.get_start_index() + len(token.get_token_string()) - 4,
                    token.get_token_end_index() + subfield.get_start_index(),
                    ErrorMessages(),
                    ErrorId.F18_EET_TIME_SYNTAX)

    @staticmethod
    def parse_f18_est(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates the F18 EST field; this field is a field 14; the Parse14 field
        parser will be used to parse this field.

        NOTE: This method is currently unused as the field 18 EST field contains a '/'
        after the point. The field 18 compound parser sees the point as an unknown field 18
        keyword. If the Field 18 EST subfield has to be parsed, this will have to be revisited.

        :param flight_plan_record: The flight plan into which an error may be written
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # The field parsers need a flight plan, and we can't use the one in this
        # instance, create a new one, it will be populated by the estimate field 14.
        new_fpr = FlightPlanRecord()
        new_fpr.add_icao_field(
            FieldIdentifiers.F14,
            subfield.get_field_text(),
            subfield.get_start_index(),
            subfield.get_end_index())
        pfx = ParseF14(new_fpr, SubFieldsInFields(), sfd)
        pfx.parse_field()

        # Check if the new flight plan contains any errors
        if new_fpr.errors_detected():
            # Errors were detected, copy them into the flight plan record of this
            # instance
            for error_records in new_fpr.get_erroneous_fields():
                flight_plan_record.add_erroneous_field(
                    error_records.get_field_text(),
                    "F22 - " + error_records.get_error_message(),
                    error_records.get_start_index(),
                    error_records.get_end_index())

    @staticmethod
    def parse_f18_ifp(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 IFP contains one or more of the following:
        ERROUTRAD, ERROUTWE, ERROUTE, ERRTYPE, ERRLEVEL, ERREOBT, NON833, 833UNKNOWN, MODESASP,
        RVSMVIOLATION, NONRVSM or RVSMUNKNOWN.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Tokenize the IFP subfield
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Regular expression for the subfield tokens
        regexp = "[ ]*(ERROUTRAD|ERROUTWE|ERROUTE|ERRTYPE|ERRLEVEL|ERREOBT|NON833|833UNKNOWN" \
                 "|MODESASP|RVSMVIOLATION|NONRVSM|RVSMUNKNOWN)[ ]*"

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Validate the subfield against the valid syntax
            mo = re.fullmatch(regexp, token.get_token_string())
            if mo is None:
                # Did not match, report an error
                Utils.add_error(flight_plan_record,
                                token.get_token_string(),
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index(),
                                ErrorMessages(),
                                ErrorId.F18_IFP_SYNTAX)

    @staticmethod
    def parse_f18_orgn(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F18 ORGN conforms to a facility address.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 7:
            # The field is too short, minimum is 7 characters
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_ORGN_TOO_SHORT)

        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_ORGN_TOO_MANY):
            return

        # Validate the facility address
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.ADDRESS1).get_field_syntax(),
                          subfield.get_field_text())
        if mo is None:
            # Report an error, facility address syntax is incorrect
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_ORGN_SYNTAX)

    @staticmethod
    def parse_f18_pbn(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F18 PBN subfield conforms to one or more of the PBN indicators.
        These indicators are A1, B1-B6, C1-C4, D1-D4, L1, O1-O4, S1, S2, T1 or T2.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 2:
            # The field is too short, minimum is at least one two letter PBN indicator
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PBN_TOO_SHORT)

        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_PBN_TOO_MANY):
            return

        # Validate the PBN indicator(s)
        mo = re.fullmatch(sfd.pbn, subfield.get_field_text().rstrip().lstrip())
        if mo is None:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PBN_SYNTAX)

    @staticmethod
    def parse_f18_per(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 PER subfield syntax conforms to one of the performance
        indicators, a single letter from the set 'A', 'B', 'C', 'D', 'E' or 'H'.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there are more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_PER_TOO_MANY):
            return

        # Validate the PER indicator
        mo = re.fullmatch("[ABCDEH]", subfield.get_field_text().rstrip().lstrip())
        if mo is None:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PER_SYNTAX)

    @staticmethod
    def parse_f18_rfp(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 PER subfield syntax conforms to the RFP indicator Q[1 to 9].

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_RFP_TOO_MANY):
            return

        # Parse the RFP for a valid 'Q'n indicator
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RFP_SYNTAX, "[ ]*Q[1-9][ ]*")

    @staticmethod
    def parse_f18_rmk(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 RMK subfield conforms to appropriate syntax;
        it's a free format text field, however the text is limited to a subset of the IAT character set.
        Allowable characters are 'A' to 'Z', '0' to '9', ':', ';', '.' or ','.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Parse the RMK subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RMK_SYNTAX, "[A-Z0-9:;., ]+")

    @staticmethod
    def parse_f18_rvr(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 RVR subfield syntax conforms to 1 to 3 digits;

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_RVR_TOO_MANY):
            return

        # Parse the RVR subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RVR_SYNTAX, "[ ]*[0-9]{1,3}[ ]*")

    @staticmethod
    def parse_f18_sel(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 SEL subfield syntax conforms to a SELCODE value
        defined as 4 to 5 letters 'A' to 'Z'

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_SEL_TOO_MANY):
            return

        # Parse the SEL subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_SEL_SYNTAX, "[ ]*[A-Z]{4,5}[ ]*")

    @staticmethod
    def parse_f18_sts(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 STS subfield syntax conforms to one of the following text strings:
            - ALTRV | ATFMX | FFR | FLTCK | HAZMAT | HEAD | HOSP | HUM | MARSA | MEDEVAC | NONRVSM | SAR | STATE;

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_STS_TOO_MANY):
            return

        # Parse the STS subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_STS_SYNTAX,
                               "[ ]*(ALTRV|ATFMX|FFR|FLTCK|HAZMAT|HEAD|HOSP|HUM|MARSA|MEDEVAC|NONRVSM|SAR|STATE)[ ]*")

    @staticmethod
    def parse_f18_src(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 SRC subfield syntax conforms to one of the following text strings:
            - RPL | FPL | AFIL | MFS | FNM | RQP | AFP | DIV | [A-Z]{4};

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_SRC_TOO_MANY):
            return

        # Parse the SRC subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_SRC_SYNTAX,
                               "[ ]*(RPL|FPL|MFS|FNM|RQP|AFP|DIV|[A-Z]{4})[ ]*")

    @staticmethod
    def parse_f18_typ(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates the F18 TYP subfield; this field consists of one or more
        number and type of aircraft tokens. The subfield will be tokenized and each token parsed for
        correct syntax and semantics.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Tokenize the subfield string
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Validate the number of (optional) and aircraft type
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F9a).get_field_syntax() +
                              sfd.get_subfield_description(SubFieldIdentifiers.F9b).get_field_syntax(),
                              token.get_token_string())
            if mo is None:
                # Report an error, syntax did not match
                Utils.add_error(flight_plan_record,
                                token.get_token_string(),
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index(),
                                ErrorMessages(),
                                ErrorId.F18_TYP_SYNTAX)
