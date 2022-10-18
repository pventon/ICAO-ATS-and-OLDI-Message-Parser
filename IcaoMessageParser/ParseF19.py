from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


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
