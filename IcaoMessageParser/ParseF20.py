from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF20(ParseFieldsCommon):
    """This class parses ICAO field 20; this class subclasses ParseFieldsCommon. This class
    initialises the super class with information specific for parsing field 20, namely:

    - A flight plan record, instance of FlightPlanRecord
    - Configuration data defining the subfields contained in this field,
      see configuration data in the SubFieldsInFields class
    - Configuration data defining the subfields that a field comprises,
      see configuration data in the SubFieldDescriptions class"""

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 20.

            :param flight_plan_record: Flight plan to populate
            :param sfif: Configuration data defining the subfields in an ICAO field
            :param sfd: Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F20,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F20),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F20))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        """This method is the program entry point to parse ICAO field 20, the parsing
        is done by calling the super class parse_field_base() method.
        The sole purpose of this class is to initialise the super class with field 20 specific
        configuration data and to tokenize the field.
            :return: None"""

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Parse the field
        self.parse_field_base()

        # Check if there are extra unwanted tokens after Field 16
        self.check_if_tokens_left_over()
