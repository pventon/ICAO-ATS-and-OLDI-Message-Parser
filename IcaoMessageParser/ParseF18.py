
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId, SubFieldIdentifiers
from IcaoMessageParser.ParseF14 import ParseF14
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from IcaoMessageParser.Utils import Utils


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
        This method perform rudimentary checks, sets up a list of errors that are
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
                            Utils.parse_f18_dle(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18dof:
                            Utils.parse_f18_dof(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_DOF_F18A_SYNTAX)
                        case SubFieldIdentifiers.F18eet:
                            Utils.parse_f18_eet(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18est:
                            # self.parse_f18_est(self.get_flight_plan_record(), subfield, self.sfd)
                            # Parsing for this field is currently not supported, the reason is that this
                            # subfield is a field 14, which contains a slash. The Field 18 compound parser
                            # sees the point before the slash as an unknown field 18 keyword.
                            # If this field is need to be parsed this will have to be revisited.
                            # For now, pass
                            pass
                        case SubFieldIdentifiers.F18ifp:
                            Utils.parse_f18_ifp(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18nav:
                            # TODO F18 NAV May require further work once F10 parsing is done
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_NAV_SYNTAX)
                        case SubFieldIdentifiers.F18opr:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_OPR_SYNTAX)
                        case SubFieldIdentifiers.F18orgn:
                            Utils.parse_f18_orgn(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18pbn:
                            Utils.parse_f18_pbn(self.get_flight_plan_record(), subfield, self.sfd)
                        case SubFieldIdentifiers.F18per:
                            Utils.parse_f18_per(self.get_flight_plan_record(), subfield)
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
                            Utils.parse_f18_rfp(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18rmk:
                            Utils.parse_f18_rmk(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18rvr:
                            Utils.parse_f18_rvr(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sel:
                            Utils.parse_f18_sel(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sts:
                            Utils.parse_f18_sts(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18src:
                            Utils.parse_f18_src(self.get_flight_plan_record(), subfield)
                        case SubFieldIdentifiers.F18sur:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_SUR_SYNTAX)
                        case SubFieldIdentifiers.F18talt:
                            Utils.parse_for_alpha_num(
                                self.get_flight_plan_record(), subfield, ErrorId.F18_TALT_SYNTAX)
                        case SubFieldIdentifiers.F18typ:
                            Utils.parse_f18_typ(self.get_flight_plan_record(), subfield, self.sfd)
                        case _:
                            # The following F18 require no special parsing other than
                            # checking for valid characters;
                            # [A-Z0-9., \n\r\t:;']
                            pass

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
