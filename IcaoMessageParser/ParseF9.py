from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils
from Tokenizer.Token import Token


class ParseF9(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 9.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F9,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F9),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F9))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Need split field 9a and 9b if the field starts with a digit
        # We assume the field follows its syntactical rules.
        if len(self.get_tokens().get_first_token().get_token_string()) > 1:
            # Split the numer of aircraft from the aircraft type
            index = Utils.get_first_digit_index(self.get_tokens().get_first_token().get_token_string())
            if index == 0:
                index = Utils.get_first_alpha_index(self.get_tokens().get_first_token().get_token_string())
                if index > -1:
                    self.split_and_insert_token(0, index)
            else:
                # Add a dummy token containing '0' to satisfy the subfield definitions
                # this will not be saved to the FPR
                tmp_token = Token("00", 0, 0)
                # Insert token containing the number of aircraft
                self.get_tokens().insert_token(tmp_token, 0)

        # Parse the field
        self.parse_field_base()

        # Check if there are extra unwanted tokens after Field 8b
        self.check_if_tokens_left_over()
