from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils
from Tokenizer.Token import Token


class ParseF17(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 17.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F17,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F17),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F17))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Need split field 17a and 17b into the ADES and ATA
        # We assume the field follows its syntactical rules.
        if len(self.get_tokens().get_first_token().get_token_string()) > 0:
            index = Utils.get_first_digit_index(self.get_tokens().get_first_token().get_token_string())
            if index > -1 and index != 0:
                self.split_and_insert_token(0, index)

        # Parse the field
        num_parsed = self.parse_field_base()

        # Parse any free text
        self.parse_extra_optional_tokens()
