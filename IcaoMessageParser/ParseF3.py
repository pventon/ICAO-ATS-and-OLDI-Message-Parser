from Configuration.EnumerationConstants import FieldIdentifiers, AdjacentUnits
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils


class ParseF3(ParseFieldsCommon):

    """The adjacent unit identifier extracted from F3b sending unit;
    This may be used to assist in setting the message type and as
    an index into identifying the field content for a given message
    title, type and unit combination."""

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 3.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F3,  # ICAO field identifier
                         " /\n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F3),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F3))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Some horrible processing needed to 'split' the F3 field into the adjacent unit names and sequence numbers
        if len(self.get_tokens().get_token_at(0).get_token_string()) > 3:
            # We have a possible F3b following F3a, have to split F3a from the start of F3b
            self.split_and_insert_token(0, 3)

        # Sort out the F3b receiver and sequence number and the start of F3c
        if self.get_tokens().get_number_of_tokens() > 3:
            # Assume we have some parts of F3b and F3c
            # Search for the sequence number from F3b
            index = Utils.get_first_digit_index(self.get_tokens().get_token_at(3).get_token_string())
            if index > 0:
                # F3b sequence number found, save the receiver of F3b
                self.split_and_insert_token(3, index)
                index = Utils.get_first_alpha_index(self.get_tokens().get_token_at(4).get_token_string())
                if index > -1:
                    self.split_and_insert_token(4, index)
        # Sort out the F3c receiver and sequence number
        if self.get_tokens().get_number_of_tokens() > 7:
            # Assume we have the receiver and sequence number of F3c
            # Search for the sequence number from F3c
            index = Utils.get_first_digit_index(self.get_tokens().get_token_at(7).get_token_string())
            if index > 0:
                # F3c sequence number found, save the receiver of F3b
                self.split_and_insert_token(7, index)

        # Parse the Field
        num_parsed = self.parse_field_base()

        # Parse any extra tokens that may be present
        self.check_if_tokens_left_over()

        # Save any adjacent unit sender and receiver names to the FPR
        if self.get_tokens().get_number_of_tokens() > 2:
            # Save the adjacent unit sender
            self.get_flight_plan_record().set_sender_adjacent_unit_name(
                self.set_adjacent_unit(self.get_tokens().get_token_at(1).get_token_string()))
        if self.get_tokens().get_number_of_tokens() > 4:
            # Save the adjacent unit receiver
            self.get_flight_plan_record().set_receiver_adjacent_unit_name(
                self.set_adjacent_unit(self.get_tokens().get_token_at(3).get_token_string()))

        # Need to check if full 'sets' of optional fields are present, Field 3 is horrible!
        # If one or mor tokens from field 3b are present then they must all be present
        # This bit of code is horrible, but it seems to do the job
        if len(self.get_sub_field_list()) > num_parsed != 1 and num_parsed != 5 and num_parsed != 9:
            # If we have e.g. FPLAA/BB001 (F3a & F3b) or FPLAA/BB002CC/DD003 (F3a, F3b & F3c)
            # The first example will create 5 tokens, the latter example 8 tokens
            # If we have token quantities that are not 5 or 8 then we have partially
            # complete F3b and/or F3c and errors must be reported.
            # We want to concatenate all the tokens from a specific erroneous set of
            # fields to report an accurate error
            start_index = 0
            if 1 < num_parsed < 5:
                start_index = 1
            elif 4 < num_parsed < 10:
                start_index = 5
            concatenated = self.concatenate_token_text(start_index, self.get_tokens().get_number_of_tokens())
            self.add_error(concatenated[0],
                           concatenated[1],
                           concatenated[2],
                           self.get_more_subfields_expected_error())

    @staticmethod
    def set_adjacent_unit(adjacent_unit_name):
        # type: (str) -> AdjacentUnits
        for unit in AdjacentUnits:
            if unit.name == adjacent_unit_name:
                return unit
        return AdjacentUnits.DEFAULT
