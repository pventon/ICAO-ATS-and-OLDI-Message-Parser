from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


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
