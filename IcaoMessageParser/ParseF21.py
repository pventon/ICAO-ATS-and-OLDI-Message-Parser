from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF21(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 21.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F21,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F21),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F21))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        pass
        # Call the dedicated field 21 parser
        # TODO Implement the field 21 parser in here
        # print("Field 21 Parser to be implemented - no parsing of this field yet!!")
