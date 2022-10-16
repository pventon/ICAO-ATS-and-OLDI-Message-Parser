from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class ParseF7(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 7.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F7,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F7),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F7))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Need to do some magic to separate the mode from the code. To do
        # this we assume the field follows its syntactical rules.
        if self.get_tokens().get_number_of_tokens() > 2:
            # Third entry should be a mode and code, need to split them
            self.split_and_insert_token(2, 1)

        # Parse the field
        num_parsed = self.parse_field_base()

        # If we have more than one token, the remainder also need to be defined
        # i.e. TEST01 is OK, TEST01/ is not and must include the mode and code.
        if self.get_tokens().get_number_of_tokens() > 1:
            self.parse_extra_compulsory_tokens(num_parsed)

        # Parse any free text
        self.check_if_tokens_left_over()
