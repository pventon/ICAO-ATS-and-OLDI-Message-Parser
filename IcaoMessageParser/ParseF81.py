from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF81(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 81.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F81,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F81),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F81))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        if self.get_tokens().get_number_of_tokens() != 3 and self.get_tokens().get_number_of_tokens() < 5:
            # We need 3 tokens as a minimum for this field, the whole field is incorrect
            self.add_error(self.get_flight_plan_record().get_icao_field(self.get_field_identifier()).get_field_text(),
                           self.get_tokens().get_first_token().get_token_start_index(),
                           self.get_tokens().get_last_token().get_token_end_index(),
                           self.get_more_subfields_expected_error())
            return

        # Parse the field
        self.parse_field_base()

        # Check if there are extra unwanted tokens after Field 81
        self.check_if_tokens_left_over()
