from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseAdditionalAddressee(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for the message header 'additional addressee' field.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.ADADDRESS,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.ADADDRESS),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.ADADDRESS))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Parse the field
        self.parse_field_base()

        # Parse any extra tokens that may be present
        self.check_if_tokens_left_over()
