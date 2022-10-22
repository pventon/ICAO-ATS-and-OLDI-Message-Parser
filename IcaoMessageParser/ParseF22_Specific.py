from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF22Specific(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for specific ICAO field 22 subfields.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F22_SPECIFIC,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F22_SPECIFIC),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F22_SPECIFIC))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        pass
        # Call the dedicated specific field 22 fields parser
        # TODO Implement the specific field 22 fields parser in here
        # print("Specific Field 22 Parser to be implemented - no parsing of this field yet!!")
