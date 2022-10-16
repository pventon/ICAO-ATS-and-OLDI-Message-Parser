from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF8(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 8.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F8,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F8),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F8))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Need split field 8a and 8b if the first token is more than 1 character long
        # We assume the field follows its syntactical rules.
        if len(self.get_tokens().get_first_token().get_token_string()) > 1:
            # Slit the rules and type of flight
            self.split_and_insert_token(0, 1)

        # Parse the field
        self.parse_field_base()

        # Check if there are extra unwanted tokens after Field 8b
        self.check_if_tokens_left_over()
