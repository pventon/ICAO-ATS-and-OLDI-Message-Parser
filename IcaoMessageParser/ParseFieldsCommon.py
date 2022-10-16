import re

from Configuration.ErrorMessages import ErrorMessages
from IcaoMessageParser.Utils import Utils
from Tokenizer.Token import Token
from Tokenizer.Tokenize import Tokenize
from Tokenizer.Tokens import Tokens
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers, ErrorId
from Configuration.SubFieldDescriptions import SubFieldDescriptions


class ParseFieldsCommon:
    # Tokens extracted from the ICAO field being parsed
    tokens: Tokens = None

    # Flight plan record into which the extracted subfields and field will be written
    flight_plan_record: FlightPlanRecord = None

    # List of subfields in the ICAO field being parsed
    sub_field_list: [SubFieldIdentifiers] = None

    # List of errors associated to each subfield being parsed
    error_list: [ErrorId] = None

    # Configuration data containing all the error messages
    error_messages: ErrorMessages = None

    # Configuration data containing the regular expressions and other information
    # describing a subfield
    sfd: SubFieldDescriptions = None

    # ICAO Field number of the field currently being parsed
    field_identifier: FieldIdentifiers = None

    def __init__(self, flight_plan_record, sfd, field_identifier, whitespace, sub_field_list, error_list):
        # type: (FlightPlanRecord, SubFieldDescriptions, FieldIdentifiers, str, [SubFieldIdentifiers], [ErrorId])->None

        # Save the field to the FPR
        self.flight_plan_record = flight_plan_record
        self.sfd = sfd
        self.field_identifier = field_identifier
        self.sub_field_list = sub_field_list
        self.error_list = error_list
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(self.flight_plan_record.get_icao_field(self.field_identifier).get_field_text())
        tokenize.set_whitespace(whitespace)
        tokenize.tokenize()
        self.tokens = tokenize.get_tokens()
        self.error_messages = ErrorMessages()

    def parse_field_base(self):
        # type: () -> int

        idx = 0
        token_to_parse = self.get_token_at_idx(idx)
        for subfield_id in self.sub_field_list:
            if token_to_parse is None:
                # We have run out of subfields to parse, this is OK if
                # the subfield is optional, check this
                if self.sfd.get_subfield_description(subfield_id).get_compulsory():
                    # Subfield missing, error
                    self.add_error(self.get_tokens().get_last_token().get_token_string(),
                                   self.get_tokens().get_last_token().get_token_start_index(),
                                   self.get_tokens().get_last_token().get_token_end_index(),
                                   self.get_more_subfields_expected_error())
                # We can finish parsing as there are no further subfields to process
                # negate the number of fields parsed as we did not parse a token here
                idx -= 1
                break
            else:
                # Get the regular expression for the subfield being parsed
                regexp = self.sfd.get_subfield_description(subfield_id).get_field_syntax()
                if re.fullmatch(regexp, token_to_parse.get_token_string()) is None:
                    # Report an error
                    self.add_error(token_to_parse.get_token_string(),
                                   token_to_parse.get_token_start_index(),
                                   token_to_parse.get_token_end_index(),
                                   self.get_error_message_at_idx(idx))
                    # Abort further parsing
                    break

            # Parsing successful, save the token, only correct tokens are saved
            # When setting the indices, the field indices are added to ensure that
            # the subfield indices are referencing the original field string and
            # not 'local' to the subfield.
            self.add_subfield_to_fpr(subfield_id,
                                     self.get_tokens().get_token_at(idx).get_token_string(),
                                     # Add the header field start index to the individual field start index
                                     self.get_tokens().get_token_at(idx).get_token_start_index() +
                                     self.get_flight_plan_record().get_icao_field(
                                         self.get_field_identifier()).get_start_index(),
                                     # Add the header field start index to the individual field end index
                                     self.get_tokens().get_token_at(idx).get_token_end_index() +
                                     self.get_flight_plan_record().get_icao_field(
                                         self.get_field_identifier()).get_start_index())
            idx += 1
            if idx > self.get_tokens().get_number_of_tokens():
                # Bail out if we have no more tokens left
                break

            # Move onto the next token
            token_to_parse = self.get_token_at_idx(idx)

        # Because the IDX is zero based, we add 1 to make it reflect the number of tokens parsed
        return idx + 1

    # More tokens (subfields) than defined / expected for this field
    def check_if_tokens_left_over(self):
        # type: () -> None
        if self.get_tokens().get_number_of_tokens() > len(self.sub_field_list):
            # Extra unwanted subfields present, error
            concatenated = self.concatenate_token_text(len(self.sub_field_list),
                                                       self.get_tokens().get_number_of_tokens())

            # Report the error
            self.add_error(concatenated[0],
                           concatenated[1],
                           concatenated[2],
                           self.get_too_many_subfields_error())

    # More tokens (subfields) than defined for this field but the extra tokens (subfields) are optional
    # with any number of occurrences possible, so they can be included but must conform to the
    # syntax specified for the last subfield definition.
    def parse_extra_optional_tokens(self):
        # type: () -> None
        # If there are more tokens than defined subfields, it may be that the
        # last subfield definition allows 'n' extras, but they still have to conform
        # to a limited syntax. These 'extra' tokens are checked here using the
        # last sfif definition.
        # Get the regular expression for the last subfield definition and its associated error message
        subfield_id = self.get_sub_field_list()[len(self.get_sub_field_list()) - 1]
        regexp = self.sfd.get_subfield_description(subfield_id).get_field_syntax()
        for idx in range(len(self.sub_field_list), self.get_tokens().get_number_of_tokens()):
            token_to_parse = self.get_tokens().get_token_at(idx)
            if re.fullmatch(regexp, token_to_parse.get_token_string()) is None:
                # Report an error
                self.add_error(token_to_parse.get_token_string(),
                               token_to_parse.get_token_start_index(),
                               token_to_parse.get_token_end_index(),
                               self.get_last_subfield_error())

    def parse_extra_compulsory_tokens(self, num_parsed):
        # type: (int) -> None
        # If there are more subfield definitions than tokens parsed and the 'missing'
        # tokens are needed we need to report an error.
        if len(self.get_sub_field_list()) > num_parsed:
            self.add_error(self.get_tokens().get_last_token().get_token_string(),
                           self.get_tokens().get_last_token().get_token_start_index(),
                           self.get_tokens().get_last_token().get_token_end_index(),
                           self.get_more_subfields_expected_error())

    def concatenate_token_text(self, first_extra_index, num_tokens):
        # type: (int, int) -> [str, int, int]
        extra_string = ""
        start_index = self.get_tokens().get_token_at(first_extra_index).get_token_start_index()
        end_index = self.get_tokens().get_token_at(first_extra_index).get_token_end_index()

        # If the indices are the same then return the data for the single indexed token
        if first_extra_index == num_tokens:
            return [self.get_tokens().get_token_at(first_extra_index).get_token_string(),
                    start_index, end_index]

        for extra_index in range(first_extra_index, num_tokens):
            extra_string = extra_string + self.get_tokens().get_token_at(extra_index).get_token_string() + " "
            end_index = self.get_tokens().get_token_at(extra_index).get_token_end_index()
        return [extra_string.rstrip(" ").replace(" /", "/").replace("/ ", "/"), start_index, end_index]

    def split_and_insert_token(self, insert_index, split_index):
        # type: (int, int) -> None
        tmp_token = Token(self.get_tokens().get_token_at(insert_index).get_token_string()[0:split_index],
                          self.get_tokens().get_token_at(insert_index).get_token_start_index(),
                          self.get_tokens().get_token_at(insert_index).get_token_start_index() + split_index)
        # Insert the new token
        self.get_tokens().insert_token(tmp_token, insert_index)
        # Fix up token following the one we just stripped out some text from
        self.get_tokens().get_token_at(insert_index + 1).set_token_string(
            self.get_tokens().get_token_at(insert_index + 1).get_token_string()[split_index:])
        self.get_tokens().get_token_at(insert_index + 1).set_token_start_index(
            self.get_tokens().get_token_at(insert_index + 1).get_token_start_index() + split_index)

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Parse the field
        num_parsed = self.parse_field_base()

        # If there are more 'unparsed' tokens report an error
        if len(self.get_sub_field_list()) > num_parsed:
            concatenated = self.concatenate_token_text(0, self.get_tokens().get_number_of_tokens())
            self.add_error(concatenated[0],
                           concatenated[1],
                           concatenated[2],
                           self.get_more_subfields_expected_error())

        # Parse any extra tokens that may be present
        self.check_if_tokens_left_over()

    def get_tokens(self):
        # type: () -> Tokens
        return self.tokens

    def get_token_at_idx(self, idx):
        # type(int) -> Token
        return self.tokens.get_token_at(idx)

    def no_tokens(self):
        # type: () -> bool
        return self.get_tokens().get_number_of_tokens() == 0

    def get_flight_plan_record(self):
        # type: () -> FlightPlanRecord
        return self.flight_plan_record

    def get_sub_field_list(self):
        # type: () -> [SubFieldIdentifiers]
        return self.sub_field_list

    def get_error_list(self):
        # type: () -> [ErrorId]
        return self.error_list

    def get_error_message_at_idx(self, idx):
        # type: (int) -> ErrorId
        return self.error_list[idx]

    def get_missing_subfield_error(self):
        # type: () -> ErrorId
        return self.get_error_message_at_idx(len(self.error_list) - 1)

    def get_more_subfields_expected_error(self):
        # type: () -> ErrorId
        return self.get_error_message_at_idx(len(self.error_list) - 2)

    def get_too_many_subfields_error(self):
        # type: () -> ErrorId
        return self.get_error_message_at_idx(len(self.error_list) - 3)

    def get_last_subfield_error(self):
        # type: () -> ErrorId
        return self.get_error_message_at_idx(len(self.error_list) - 4)

    def get_field_identifier(self):
        # type: () -> FieldIdentifiers
        return self.field_identifier

    def add_subfield_to_fpr(self, subfield_id, subfield_text, start_idx, end_idx):
        # type: (SubFieldIdentifiers, str, int, int) -> None
        self.get_flight_plan_record().add_icao_subfield(
            self.get_field_identifier(), subfield_id, subfield_text, start_idx, end_idx)

    def add_error(self, erroneous_field_text, start_index, end_index, error_id):
        # type: (str, int, int, ErrorId) -> None
        Utils.add_error(self.flight_plan_record,
                        erroneous_field_text,
                        start_index + self.get_flight_plan_record().get_icao_field(
                            self.get_field_identifier()).get_start_index(),
                        end_index + self.get_flight_plan_record().get_icao_field(
                            self.get_field_identifier()).get_start_index(),
                        self.error_messages,
                        error_id)
