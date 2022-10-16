# This class contains a list of tokens where each token represents a string of
# characters tokenized from a string by the Tokenizer class.
# Refer to the Token class for details ona Token's content.
# This class provides methods to append and retrieve tokens to / from this class.
from Tokenizer.Token import Token


class Tokens:
    # A list of tokens
    tokens = []

    # Keeps track of the current tokens index when calling get_next_token()
    # and get_previous_token()
    current_token = 0

    # Constructor without any initialized token
    def __init__(self):
        self.current_token = 0
        self.tokens = []

    # Get the number of tokens
    def get_number_of_tokens(self):
        # type: () -> int
        return len(self.tokens)

    # Appends a token to this class instance
    def append_token(self, token):
        # type: (Token) -> None
        self.tokens.append(token)

    # Inserts a token before the one identified with the index 'index'
    def insert_token(self, token, index):
        # type: (Token, int) -> None
        self.tokens.insert(index, token)

    # Creates and appends a token to this class instance with discreet attributes
    def create_append_token(self, token_text, token_start_index, token_end_index):
        # type: (str, int, int) -> None
        self.append_token(Token(token_text, token_start_index, token_end_index))

    # Returns the list of tokens
    def get_tokens(self):
        # type: () -> []
        return self.tokens

    # Retrieves a token at 'index', or returns 'None' if 'index' is out of range
    def get_token_at(self, index):
        # type: (int) -> Token | None
        if index < 0 or index >= len(self.tokens):
            return None
        return self.tokens[index]

    def get_first_token(self):
        # type: () -> Token
        self.current_token = 0
        return self.get_token_at(self.current_token)

    def get_last_token(self):
        # type: () -> Token
        self.current_token = self.get_number_of_tokens() - 1
        return self.get_token_at(self.get_number_of_tokens() - 1)

    def get_next_token(self):
        # type: () -> Token
        self.current_token = self.current_token + 1
        return self.get_token_at(self.current_token)

    def get_previous_token(self):
        # type: () -> Token
        self.current_token = self.current_token - 1
        return self.get_token_at(self.current_token)

    def peek_next_token(self, look_ahead=1):
        # type: (int) -> Token
        return self.get_token_at(self.current_token + look_ahead)

    def peek_previous_token(self, look_behind=1):
        # type: (int) -> Token
        return self.get_token_at(self.current_token - look_behind)

    def get_current_token(self):
        # type: () -> Token
        return self.get_token_at(self.current_token)

    def print_tokens(self):
        # type: () -> None
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
