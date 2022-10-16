import F15_Parser
from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from F15_Parser.F15Parse import ParseF15


class ParseF15x(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 15.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F15,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F15),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F15))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, ErrorId.F15_MISSING)
            return

        # Create an ERS instance to store the extracted route in
        ers = ExtractedRouteSequence()

        # Create a field 15 parser
        f15parser = F15_Parser.F15Parse.ParseF15()

        # Parse field 15
        f15parser.parse_f15(ers, self.get_tokens())

        # Add the ERS to the flight plan
        self.get_flight_plan_record().add_extracted_route(ers)
