from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils


class ParseF14(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 14.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F14,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F14),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F14))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Need to split field 14b (HHMM) from F14c (altitude) from F14d (altitude) and F14e (crossing mode)
        if self.get_tokens().get_number_of_tokens() > 2:
            # We have three tokens, should be point, '/' and the rest of field 14 in the 3rd token
            index = Utils.get_first_alpha_index(self.get_tokens().get_token_at(2).get_token_string())
            if index > -1 and index != 0:
                # Split off F14b HHMM into a separate token
                self.split_and_insert_token(2, index)

                # Token (3) contains the rest of F14, F14c, d & e, F14c is an altitude that should
                # start with a letter followed by a number of digits.
                # If we skip the letter and then look for the next alpha, we can split of the F14c altitude.
                if len(self.get_tokens().get_token_at(3).get_token_string()) > 1:
                    index = Utils.get_first_alpha_index(
                        self.get_tokens().get_token_at(3).get_token_string()[1:])
                    if index > -1 and index != 0:
                        # Split off F14c altitude into a separate token
                        self.split_and_insert_token(3, index + 1)

                        # Token (4) contains the rest of F14, F14d & e, F14d is an altitude that should
                        # start with a letter followed by a number of digits.
                        # If we skip the letter and then look for the next alpha, we can split of the F14c altitude.
                        if len(self.get_tokens().get_token_at(4).get_token_string()) > 1:
                            index = Utils.get_first_alpha_index(
                                self.get_tokens().get_token_at(4).get_token_string()[1:])
                            if index > -1 and index != 0:
                                # Split off F14d altitude into a separate token
                                self.split_and_insert_token(4, index + 1)

        # Parse the field
        self.parse_field_base()

        # Check if there are extra unwanted tokens after Field 14
        self.check_if_tokens_left_over()
