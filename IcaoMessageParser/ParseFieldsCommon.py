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
    """This class is the base class that all individual field parsers inherit from. This class
    provides parsing methods that are common to many fields. In general, ICAO fields fall
    into groups that require different parsing techniques:

    - ICAO Fields 3, 5, 7, 8, 9, 10, 13, 16, 17, 20, and 21, also OLDI field 80 and 81) - These are 'basic' fields
      that all have similar parsing requirements; this splits a field into its constituent subfields
      and parses each subfield before storing the fields and associated subfields in a flight plan record.
      Program entry point for the basic field parser is the method self.parse_field() in this class.
    - Field 15 stands on its own as a field requiring special parsing that is implemented
      in a stand-alone parser. Field 15 describes the route an aircraft will follow, the dedicated
      field 15 parser takes the route information and creates an extracted route sequence that is
      copied as a whole to the flight plan record.
    - Fields 18, 19 and 22 - These are what could be referred to as 'compound' fields as they contain
      'n' occurrences of subfields that require individual parsing.

      All subfields are stored in the flight plan record.
      Program entry point for the compound field parser is self.parse_compound_field_common() in this class.

    This parser copies all the fields into the Flight Plan Record (FPR), an instance of the FlightPlanRecord class.
    This is done by adding instances of the 'FieldRecord' class for each field parsed. The 'FieldRecord' class
    stores one or more individual subfields (instances of SubFiledRecord) that a field is comprised off. For
    compound fields, the subfields are copied as individual subfields of the compound field into a field record.
    The compound fields subfields, are in themselves 'field' with subfields that require dedicated parsing
    for each field.
    """

    tokens: Tokens = None
    """Tokens extracted from the ICAO field being parsed"""

    flight_plan_record: FlightPlanRecord = None
    """Flight plan record into which the extracted subfields and field will be written"""

    sub_field_list: [SubFieldIdentifiers] = None
    """List of subfields in the ICAO field being parsed"""

    error_list: [ErrorId] = None
    """List of errors associated to each subfield being parsed"""

    error_messages: ErrorMessages = None
    """Configuration data containing all the error messages"""

    sfd: SubFieldDescriptions = None
    """Configuration data containing the regular expressions and other information
    describing a subfield"""

    field_identifier: FieldIdentifiers = None
    """ICAO Field number of the field currently being parsed"""

    def __init__(self, flight_plan_record, sfd, field_identifier, whitespace, sub_field_list, error_list):
        # type: (FlightPlanRecord, SubFieldDescriptions, FieldIdentifiers, str, [SubFieldIdentifiers], [ErrorId])->None
        """This constructor sets up an instance of a field parser with all data needed to parse a given field.
        This base class tokenizes a field and stores its field identifier, the subfields that the field
        comprises and a list of errors associated with each subfield should an error be detected.
            :param flight_plan_record: An instance of FlightPlanRecord that this parser write its date to,
                   this includes the fields and subfields parsed along with any associated errors.
            :param sfd: Configuration data that describes individual subfields that includes the regular expression
                   used to parse individual subfields.
            :param field_identifier: An enumeration value from the FieldIdentifiers class that identifies the
                   field being parsed.
            :param whitespace: The whitespace characters used to tokenize a field, these differ depending on the field
                   being parsed and are set by subclasses of this class based on the individual requirements
                   of a given field.
            :param sub_field_list: Configuration data containing a list of subfields that the field being parsed
                   comprises. These are given as a list of enumeration values from the SubFieldDescriptions class.
            :param error_list: A list of errors that may be reported by this parser; there is a dedicated syntax error
                   message for each subfield as well as some generic messages relating to none-syntactical
                   errors such as field / subfields missing etc.
            :return: None"""
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

    def add_error(self, erroneous_field_text, start_index, end_index, error_id):
        # type: (str, int, int, ErrorId) -> None
        """This method adds an error to the flight plan record for basic fields, i.e. 3, 5, 7, 8, 9, 10,
        13, 14, 16, 17, 80 and 81.
            :param erroneous_field_text: The text of the field that is in error
            :param start_index: The start index of the erroneous fields location in the original field string
            :param end_index: The end index of the erroneous fields location in the original field string
            :param error_id: The error number given as an enumeration value from the ErrorID class
            :return: None"""
        Utils.add_error(self.flight_plan_record,
                        erroneous_field_text,
                        start_index + self.get_flight_plan_record().get_icao_field(
                            self.get_field_identifier()).get_start_index(),
                        end_index + self.get_flight_plan_record().get_icao_field(
                            self.get_field_identifier()).get_start_index(),
                        self.error_messages,
                        error_id)

    def add_compound_field_error(self, tokens, field_text, error_id):
        # type: ([Token], str, ErrorId) -> None
        """This method adds an error to the flight plan record for the subfield of a compound field,
        i.e. Fields 18, 19 and 22.
            :param tokens: The token representing a field that is in error
            :param field_text: The text representing the complete compound field
            :param error_id: The error number given as an enumeration value from the ErrorID class
            :return: None"""
        start_idx = tokens[0].get_token_start_index()
        end_idx = tokens[len(tokens) - 1].get_token_end_index()
        self.add_error(field_text[start_idx:end_idx], start_idx, end_idx, error_id)

    def add_subfield_to_fpr(self, subfield_id, subfield_text, start_idx, end_idx):
        # type: (SubFieldIdentifiers, str, int, int) -> None
        """This method adds a subfield to the flight plan record;

            :param subfield_id: The subfield identifier as an enumeration value of the SubFieldIdentifiers class
            :param subfield_text: The text being saved that is the subfield text
            :param start_idx: The start index of the subfields position in the original field
            :param end_idx: The start index of the subfields position in the original field
            :return: None"""
        self.get_flight_plan_record().add_icao_subfield(
            self.get_field_identifier(), subfield_id, subfield_text, start_idx, end_idx)

    def check_if_tokens_left_over(self):
        # type: () -> None
        """This method checks if there are more tokens (subfields) than defined / expected for this field.
        If there are to many tokens/subfields present for the field being parsed an error is added to
        the flight plan record.
            :return: None"""
        if self.get_tokens().get_number_of_tokens() > len(self.sub_field_list):
            # Extra unwanted subfields present, error
            concatenated = self.concatenate_token_text(len(self.sub_field_list),
                                                       self.get_tokens().get_number_of_tokens())

            # Report the error
            self.add_error(concatenated[0],
                           concatenated[1],
                           concatenated[2],
                           self.get_too_many_subfields_error())

    def concatenate_token_text(self, first_extra_index, num_tokens):
        # type: (int, int) -> [str, int, int]
        """This method concatenates the text from several tokens/subfields; this is required
        for situations such as error reporting when there are too many subfields
        present in a field and the error must report all the extra tokens as erroneous.
            :param first_extra_index: An index into the list of tokens for the first 'extra' subfield
            :param num_tokens: The last token index that is to be concatenated
            :return: A list containing the concatenated text of the subfields with their start and end index
                     of their location in the original field text"""
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

    def get_error_list(self):
        # type: () -> [ErrorId]
        """This method returns a list of enumeration values from the ErrorId class; each list entry
        represents an error pertaining to each subfield in a field. The position of the error message
        numbers is set in configuration data to match the subfield definition for a given field.
        This definition is made in the configuration data class SubFieldsInFields.
            :return: A list of ErrorId class enumeration values defining the errors for parsing this field."""
        return self.error_list

    def get_error_message_at_idx(self, idx):
        # type: (int) -> ErrorId
        """This method retrieves a single error message number from the list of
        error numbers stored for this field parsing.
            :return: An enumeration value from the ErrorId class identifying a unique error message."""
        return self.error_list[idx]

    def get_field_identifier(self):
        # type: () -> FieldIdentifiers
        """This method returns the ICAO field identifier as an enumeration value from the FieldIdentifiers
        class; when a dedicated field parser inherits from this class and is instantiated, it sets the
        field identifier for the field it is parsing.
            :return: The ICAO field identifier as an enumeration value from the FieldIdentifiers class."""
        return self.field_identifier

    def get_flight_plan_record(self):
        # type: () -> FlightPlanRecord
        """This method returns the flight plan record that is being used by this parser to
        write all parsed fields, subfields and associated error messages.
            :return: An instance of FlightPlanRecord that is the flight plan record used by this parser."""
        return self.flight_plan_record

    def get_last_subfield_error(self):
        # type: () -> ErrorId
        """This method returns a specific error message from the list of error messages defined for
        parsing this field. A list of errors is defined for each subfield in the SubFieldsInFields class.
        This method returns the error associated with last subfield in a field.
            :return: An enumeration value from the ErrorId class identifying a unique error message."""
        return self.get_error_message_at_idx(len(self.error_list) - 4)

    def get_missing_subfield_error(self):
        # type: () -> ErrorId
        """This method returns a specific error message from the list of error messages defined for
        parsing this field. A list of errors is defined for each subfield in the SubFieldsInFields class.
        This method returns the error reported when a subfield is missing from a field.
            :return: An enumeration value from the ErrorId class identifying a unique error message."""
        return self.get_error_message_at_idx(len(self.error_list) - 1)

    def get_more_subfields_expected_error(self):
        # type: () -> ErrorId
        """This method returns a specific error message from the list of error messages defined for
        parsing this field. A list of errors is defined for each subfield in the SubFieldsInFields class.
        This method returns the error reported when more subfields are present than defined for a field.
            :return: An enumeration value from the ErrorId class identifying a unique error message."""
        return self.get_error_message_at_idx(len(self.error_list) - 2)

    def get_sub_field_list(self):
        # type: () -> [SubFieldIdentifiers]
        """This method returns a list of enumeration values from the SubFieldIdentifiers class; each list
        entry represents a subfield in the field being parsed and in total defines a fields
        subfield content. The position of each entry maps directly to the position of a subfield in a field.
        This definition is made in the configuration data class SubFieldsInFields.
            :return: A list of SubFieldIdentifiers class enumeration values that define the subfield content
                     for a field"""
        return self.sub_field_list

    def get_token_at_idx(self, idx):
        # type(int) -> Token
        """This method returns a token/subfield from the list of tokens generated when this class
        was instantiated. Each token is a subfield of a field; the token list includes the 'forward slash'
        ('/') as a token.
            :param idx: The zero based index into the list of tokens to be retrieved.
            :return: A Token class instance representing a single subfield of a field or None
            if the index provided by the parameter idx is out of range."""
        return self.tokens.get_token_at(idx)

    def get_tokens(self):
        # type: () -> Tokens
        """This method return a list of token/subfields derived from the field being parsed; the token
        list includes the 'forward slash' ('/') as a token.
        :return: A list of Token instances"""
        return self.tokens

    def get_too_many_subfields_error(self):
        # type: () -> ErrorId
        """This method returns a specific error message from the list of error messages defined for
        parsing this field. A list of errors is defined for each subfield in the SubFieldsInFields class.
        This method returns the error reported when to many subfields are present than defined for a field.
            :return: An enumeration value from the ErrorId class identifying a unique error message"""
        return self.get_error_message_at_idx(len(self.error_list) - 3)

    @staticmethod
    def is_compound_field_keyword(field_id, candidate_keyword):
        # type: (FieldIdentifiers, str) -> SubFieldIdentifiers
        """This method returns an enumeration value from the SubFieldIdentifiers class for
        a subfield name/identifier given as a string for a specific field. (e.g. if
        FieldIdentifiers.F18 and 'RALT' are provided for the method parameters, the method locates
        the enumeration value matching RALT or returns SubFieldIdentifiers.ANYTHING if no match is found).
        This method is used when parsing the compound fields 18, 19 and 22; these fields contain
        named subfields. This method is used to check if a named subfield exists, if not
        an error is reported by the parser.
            :param field_id: An enumeration value from FieldIdentifiers identifying a field
            :param candidate_keyword: A string containing the subfield name being searched.
        :return: An enumeration value from the SubFieldIdentifiers class for a subfield name/identifier"""
        if field_id == FieldIdentifiers.F18:
            for keyword in SubFieldIdentifiers:
                if SubFieldIdentifiers.F17c < keyword < SubFieldIdentifiers.F19a:
                    if 2 < len(keyword.name[3:]) < 5:
                        if keyword.name[3:].upper() == candidate_keyword:
                            return keyword
        elif field_id == FieldIdentifiers.F19:
            for keyword in SubFieldIdentifiers:
                if SubFieldIdentifiers.F18typ < keyword < SubFieldIdentifiers.F20a:
                    if 0 < len(keyword.name[3:]) < 2:
                        if keyword.name[3:].upper() == candidate_keyword:
                            return keyword
        elif field_id == FieldIdentifiers.F22:
            for keyword in SubFieldIdentifiers:
                if SubFieldIdentifiers.F21f < keyword < SubFieldIdentifiers.F80a:
                    if len(keyword.name[5:]) < 3:
                        #  print(keyword.name[3:])
                        if keyword.name[5:].upper() == candidate_keyword:
                            return keyword
        return SubFieldIdentifiers.ANYTHING

    def no_tokens(self):
        # type: () -> bool
        """This method returns True if the list of tokens is zero, i.e. there are no tokens to parse.
            :return: True if the token list is empty, False otherwise"""
        return self.get_tokens().get_number_of_tokens() == 0

    def parse_compound_field_common(self, error_codes, keyword_checker):
        # type: ([ErrorId], is_compound_field_keyword) -> None
        """This method is the program entry point for the compound field parser used to parse the compound fields
        18, 19 and 22. These fields all contain named subfields, e.g.Field 18 - DEP/Data, Field 19 A/Data
        or field 22 9/Data. In all cases the text preceding the '/', the 'keyword', identifies the subfield. All
        subfields are stored in the flight plan record once parsed.

        This class implements a small state machine to loop over the subfields and extract valid known
        subfields and their associated data, parse them and write them out to the flight plan record.
        Unrecognised subfields are not written to the flight plan record and an error is reported.
        Anything else found that is not a subfield will cause an error to be reported.
            :param error_codes: A list of enumeration values from the ErrorId class identifying an error for
                   each subfield in the field. The error message definition is made in the
                   SubFieldsInFields class.
            :param keyword_checker: A callback method used to check if a subfield keyword is valid for the
                   field being parsed. Because this method is used by all the compound field
                   parsers, each has its own unique field identifier when calling the
                   method self.is_compound_field_keyword()
            :return: None"""
        # Two or more tokens present in field 18 if we get this far
        idx = 0
        subfield_id = None

        # Get the compound field string, this includes all subfields and is the text as it appears in a message
        fxx_field_text = self.get_flight_plan_record().get_icao_field(self.get_field_identifier()).get_field_text()

        # Looping over a compound field is implemented as a simple state machine that has the following states.
        in_known_field = False  # Processing a known keyword '/' sequence
        in_unknown_field = False  # Processing an unknown keyword '/' sequence
        not_in_field = True  # Not in any sequence, this happens if there is junk at the start of a field
        junk_bin = []  # Stores junk found at the start of the field
        known_bin = []  # Stores the keyword. '/' and data for a known keyword
        unknown_bin = []  # Stores the keyword. '/' and data for an unknown keyword
        # Off we go...
        for token in self.get_tokens().get_tokens():
            # We perform look ahead, so we can only loop of the token list size - 1
            if idx >= self.get_tokens().get_number_of_tokens() - 1:
                break
            if not_in_field:
                # In this state when processing the first token(s) a compound field until a valid
                # keyword (known or unknown) '/' sequence is encountered.
                if self.get_tokens().get_token_at(idx + 1).get_token_string() == "/":
                    # The next token slash indicates a state change is taking place
                    if len(junk_bin) > 0:
                        # If there is any 'junk' at the start of the field report an error
                        self.add_compound_field_error(junk_bin, fxx_field_text, error_codes[0])
                    # Establish if the keyword is known or unknown
                    subfield_id = keyword_checker(self.get_field_identifier(), token.get_token_string())
                    if subfield_id == SubFieldIdentifiers.ANYTHING:
                        # Move to the unknown keyword '/' sequence state
                        not_in_field = False
                        in_unknown_field = True
                        unknown_bin.append(token)
                    else:
                        # Move to the known keyword '/' sequence state
                        not_in_field = False
                        in_known_field = True
                        known_bin.append(token)
                    junk_bin = []
                else:
                    # No state change, save more junk!
                    junk_bin.append(token)

            elif in_known_field:
                # In this state when processing a known keyword '/' sequence
                if self.get_tokens().get_token_at(idx + 1).get_token_string() == "/":
                    # The next token slash indicates a state change is taking place
                    if 0 < len(known_bin) < 3:
                        # The previous state must have been a known keyword sequence, it has to
                        # have at least 3 fields to be valid (e.g. STS/DATA)
                        self.add_compound_field_error(known_bin, fxx_field_text, error_codes[1])
                    elif len(unknown_bin) > 0:
                        # The previous state must have been an unknown sequence, if it exists then report an error
                        self.add_compound_field_error(unknown_bin, fxx_field_text, error_codes[2])
                    # Save the current 'known' sequence
                    self.save_compound_field(known_bin, subfield_id, fxx_field_text)
                    # Figure out what state to move to next
                    subfield_id = keyword_checker(self.get_field_identifier(), token.get_token_string())
                    if subfield_id == SubFieldIdentifiers.ANYTHING:
                        in_known_field = False
                        in_unknown_field = True
                        unknown_bin = [token]
                        known_bin = []
                    else:
                        unknown_bin = []
                        known_bin = [token]
                else:
                    known_bin.append(token)

            elif in_unknown_field:
                # In this state when processing an unknown keyword '/' sequence
                if self.get_tokens().get_token_at(idx + 1).get_token_string() == "/":
                    # The next token slash indicates a state change is taking place
                    if 0 < len(known_bin) < 3:
                        # The previous state must have been a known keyword sequence, it has to
                        # have at least 3 fields to be valid (e.g. STS/DATA)
                        self.add_compound_field_error(known_bin, fxx_field_text, error_codes[1])
                    if len(unknown_bin) > 0:
                        # The previous state must have been an unknown sequence, if it exists then report an error
                        self.add_compound_field_error(unknown_bin, fxx_field_text, error_codes[2])
                    # Save the current 'known' sequence
                    # Figure out what state to move to next
                    self.save_compound_field(known_bin, subfield_id, fxx_field_text)
                    subfield_id = keyword_checker(self.get_field_identifier(), token.get_token_string())
                    if subfield_id == SubFieldIdentifiers.ANYTHING:
                        in_unknown_field = True
                        in_known_field = False
                        known_bin = []
                        unknown_bin = [token]
                    else:
                        in_unknown_field = False
                        in_known_field = True
                        known_bin = [token]
                        unknown_bin = []
                else:
                    unknown_bin.append(token)
            idx += 1

        # Clean up the last token
        if in_known_field:
            known_bin.append(self.get_tokens().get_last_token())
        elif in_unknown_field:
            unknown_bin.append(self.get_tokens().get_last_token())
        elif not_in_field:
            junk_bin.append(self.get_tokens().get_last_token())

        # Check if the last field stored has any errors
        if len(junk_bin) > 0:
            self.add_compound_field_error(junk_bin, fxx_field_text, error_codes[3])
        elif len(unknown_bin) > 0:
            self.add_compound_field_error(unknown_bin, fxx_field_text, error_codes[2])
        elif len(known_bin) > 0:
            self.save_compound_field(known_bin, subfield_id, fxx_field_text)
            if len(known_bin) < 3:
                self.add_compound_field_error(known_bin, fxx_field_text, error_codes[1])

    def parse_extra_compulsory_tokens(self, num_parsed):
        # type: (int) -> None
        """This method checks if there are more subfields defined than present in a field.
        If there are more subfield definitions than tokens parsed and the 'missing' tokens are compulsory
        we need to report an error.
            :param num_parsed: The total number of all subfields already parsed
            :return: None"""
        if len(self.get_sub_field_list()) > num_parsed:
            self.add_error(self.get_tokens().get_last_token().get_token_string(),
                           self.get_tokens().get_last_token().get_token_start_index(),
                           self.get_tokens().get_last_token().get_token_end_index(),
                           self.get_more_subfields_expected_error())

    def parse_extra_optional_tokens(self):
        # type: () -> None
        """This method checks if there are more tokens (subfields) than defined for this field but the
        extra tokens (subfields) are optional with any number of occurrences possible, so they can be included
        but must conform to the syntax specified for the last subfield definition.

        If there are more tokens than defined subfields, it may be that the last subfield definition allows
        'n' extras, but they still have to conform to a defined syntax. These 'extra' tokens are checked
        here using the syntax definition for the last token defined in the SubFieldsInFields configuration.
            :return: None"""
        subfield_id = self.get_sub_field_list()[len(self.get_sub_field_list()) - 1]
        # Get the regular expression for the last subfield definition
        regexp = self.sfd.get_subfield_description(subfield_id).get_field_syntax()
        for idx in range(len(self.sub_field_list), self.get_tokens().get_number_of_tokens()):
            token_to_parse = self.get_tokens().get_token_at(idx)
            if re.fullmatch(regexp, token_to_parse.get_token_string()) is None:
                # Report an error
                self.add_error(token_to_parse.get_token_string(),
                               token_to_parse.get_token_start_index(),
                               token_to_parse.get_token_end_index(),
                               self.get_last_subfield_error())

    def parse_field(self):
        # type: () -> None
        """This method is the program entry point for the basic field parser to parse ICAO fields 3, 5, 7,
        8, 9, 10, 13, 14, 16, 17, 80 and 81.

        This method calls the 'base' parser self.parse_field_base() to do most of the heavy lifting. Once
        the base parse is finished, this method checks that all fields are present, not missing any nor
        any extra fields present.
            :return: None"""

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

    def parse_field_base(self):
        # type: () -> int
        """This method loops over the subfields tokenized from a field and parses each subfield.
        The expected subfields to parse along with the configuration data defining what has to be parsed
        are stored in this class when the individual field parser subclasses this class and instantiates itself.
        The configuration data this method needs are:

        - The field identifier for this field, self.field_identifier: FieldIdentifiers
        - List of subfields describing this fields content, self.sub_field_list: [SubFieldIdentifiers]
        - List of error messages associated with each subfield, self.error_list: [ErrorId]
        - List of subfields to parse, self.tokens: Tokens

        Errors and successfully parsed fields and subfields are written to the flight plan record also stored in
        this class when instantiated (self.flight_plan_record: FlightPlanRecord)
            :return: None"""

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

    def save_compound_field(self, tokens, subfield_id, field_text):
        # type: ([Token], SubFieldIdentifiers, str) -> None
        """This method saves a compound field to the flight plan record. The keyword and '/' are not
        saved. The subfields are stored in a SubFieldRecord in a FieldRecord in the FlightPlanRecord.
        The zero based start and end indices are also stored for the subfield.
            :param tokens: The subfield tokens being parsed and saved to the flight plan record
            :param subfield_id: The subfield ID as an enumeration value from the SubFieldIdentifiers class
            :param field_text: The subfield text as it appears in a message.
            :return: None"""
        if len(tokens) == 0:
            return
        # Don't save the keyword and the '/', hence the + 1
        # Token idx 0 is the keyword, token idx 1 is the '/'
        start_idx = tokens[1].get_token_end_index()
        end_idx = tokens[len(tokens) - 1].get_token_end_index()
        self.get_flight_plan_record().add_icao_subfield(self.get_field_identifier(), subfield_id,
                                                        field_text[start_idx:end_idx], start_idx, end_idx)

    def split_and_insert_token(self, insert_index, split_index):
        # type: (int, int) -> None
        """This method splits data in a token and creates a new token so that the subfields can be parsed
        as defined in the configuration data, where each subfield is defined separately.
        For example, a 'full' F3 comprises F3a, F3b & F3c which looks like FPLAA/BB001CC/DD002.
        When tokenized the following tokens are generated:
            - FPLAA     F3a and F3b '1'
            - /         F3b '2'
            - BB001CC   F3b '3' & '4' & F3c '1'
            - /         F3c '2'
            - DD002     F3c '3' & '4'
        These tokens must be split up, so we have each subfield in its own token to look like:
            - FPL       F3a
            - AA        F3b '1'
            - /         F3b '2'
            - BB        F3b '3'
            - 001       F3b '4'
            - CC        F3c '1'
            - /         F3c '2'
            - DD        F3c '3'
            - 002       F3c '4'
        This method will take a field to split, split it and insert a new token for the newly created subfield.
            :param insert_index: The index in the token list, before which the new token is inserted
            :param split_index: The index in a string where to split a tokens text
            :return: None"""
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
