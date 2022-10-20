from Tokenizer.Token import Token


class Tokens:
    """This class contains a list of tokens where each token represents a string of
    # characters tokenized from a string by the Tokenizer class.
    # Refer to the Token class for details about a Token's content.
    # This class provides methods to append and retrieve tokens to / from this class."""

    tokens: [Token] = None
    """A list of tokens as the Token class"""

    current_token: int = 0
    """Keeps track of the current tokens index when calling get_next_token()
    and get_previous_token()"""

    def __init__(self):
        # type: () -> None
        """This constructor creates an 'empty' instance of this class.

            :return: None"""
        self.current_token = 0
        self.tokens = []

    def get_number_of_tokens(self):
        # type: () -> int
        """This method gets and returns the number of Token instances stored in this class.

            :return: The number of tokens in this class instance;"""
        return len(self.tokens)

    def append_token(self, token):
        # type: (Token) -> None
        """This method appends a token to this class instance

            :param token: A Token instance to append to the list of tokens in this class;
            :return: None"""
        self.tokens.append(token)

    def insert_token(self, token, index):
        # type: (Token, int) -> None
        """This method inserts a token before the one identified with the index 'index'

            :param token: The Token instance to insert into the list of tokens in this class;
            :param index: The index before which the new token will be inserted;
            :return: None"""
        self.tokens.insert(index, token)

    def create_append_token(self, token_text, token_start_index, token_end_index):
        # type: (str, int, int) -> None
        """This method creates and appends a token to this class instance with a start and end index.

            :param token_text: The text for this new token;
            :param token_start_index: The tokens zero based start index for its position in the original
                                      string it was extracted from;
            :param token_end_index: The tokens zero based end index for its position in the original
                                    string it was extracted from;
            :return: None"""
        self.append_token(Token(token_text, token_start_index, token_end_index))

    def get_tokens(self):
        # type: () -> [Token]
        """This method gets the list of tokens

            :return: The list of token stored in this class;"""
        return self.tokens

    def get_token_at(self, index):
        # type: (int) -> Token | None
        """This method gets a specific token from the list of tokens at 'index', 'None' if 'index' is out of range.

            :param index: The index for the token to be returned;
            :return: A Token instance located in the list of tokens at the position in the list specified by
                    'index' or None if the index is out of range;"""
        if index < 0 or index >= len(self.tokens):
            return None
        return self.tokens[index]

    def get_first_token(self):
        # type: () -> Token
        """This method gets the first token in the list of tokens; the member 'current_token'
        is updated to zero to keep track of the last token recovered.

            :return: The first Token in the list of tokens stored in this class;"""
        self.current_token = 0
        return self.get_token_at(self.current_token)

    def get_last_token(self):
        # type: () -> Token
        """This method gets the last token in the list of tokens; the member 'current_token'
        is updated to the last token index to keep track of the last token recovered.

            :return: The last Token in the list of tokens stored in this class;"""
        self.current_token = self.get_number_of_tokens() - 1
        return self.get_token_at(self.get_number_of_tokens() - 1)

    def get_next_token(self):
        # type: () -> Token
        """This method gets the next token in the list of tokens from the last one retrieved;
        the member 'current_token' is used to indicated the 'current' token index, one is
        added to this and the 'next' token returned.

            :return: The 'next' Token in the list of tokens stored in this class;"""
        self.current_token = self.current_token + 1
        return self.get_token_at(self.current_token)

    def get_previous_token(self):
        # type: () -> Token
        """This method gets the previous token in the list of tokens from the last one retrieved;
        the member 'current_token' is used to indicated the 'current' token index, one is
        subtracted from this and the 'previous' token returned.

            :return: The 'previous' Token in the list of tokens stored in this class;"""
        self.current_token = self.current_token - 1
        return self.get_token_at(self.current_token)

    def peek_next_token(self, look_ahead=1):
        # type: (int) -> Token
        """This method 'peeks' at the next token in the list of tokens from the last one retrieved;
        the member 'current_token' is NOT updated for a 'peek' operation and the 'current' token
        remains the same.

            :return: The 'next' Token in the list of tokens stored in this class;"""
        return self.get_token_at(self.current_token + look_ahead)

    def peek_previous_token(self, look_behind=1):
        # type: (int) -> Token
        """This method 'peeks' at the previous token in the list of tokens from the last one retrieved;
        the member 'current_token' is NOT updated for a 'peek' operation and the 'current' token
        remains the same.

            :return: The 'previous' Token in the list of tokens stored in this class;"""
        return self.get_token_at(self.current_token - look_behind)

    def get_current_token(self):
        # type: () -> Token
        """This method gets the current token in the list of tokens;
        the member 'current_token' is NOT modified in this operation leaving the 'current' token as is.

            :return: The 'current' Token in the list of tokens stored in this class;"""
        return self.get_token_at(self.current_token)

    def remove_tokens_from_end_of_list(self, split_index):
        # type: (int) -> None
        """This method removes tokens from the list above the split_index

        :param split_index: Index above which all tokens will be removed
        :return: None
        """
        self.tokens = self.tokens[:split_index + 1]

    def print_tokens(self):
        # type: () -> None
        """This method prints the complete list of tokens. The method is provided to assist in debugging.

            :return: None"""
        print("Total Number of Tokens: " + str(len(self.tokens)))
        print("{0:>15}".format("Start") +
              "{0:>5}".format("End") +
              "{0:>6}".format("Base") +
              "{0:>5}".format("Sub-"))
        print("{0:>9}".format("Name") +
              "{0:>6}".format("Index") +
              "{0:>6}".format("Index") +
              "{0:>5}".format("Type") +
              "{0:>5}".format("Type"))
        for item in self.tokens:
            item.print_token()
