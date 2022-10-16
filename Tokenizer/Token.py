# This class represents a single token along with all its attributes unique
# to a token. Each token is stored with its associated attributes:
# - Token text; a string of characters;
# - Token start index - zero based index into the string where a tokens first
#   character was found in the source string;
# - Token end index - zero based index into the string where a tokens last + 1
#   character was found in the source string;
# In addition, two further attributes are provided in this class that store
# the following:
# - Token Base Type - derived from a tokens' syntax
# - Token Subtype - derived from a tokens syntax
class Token:

    # A string representing a token
    token_string = ""

    # The start index of a token into the string from which a token was extracted
    token_start_index = 0

    # The end index of a token into the string from which a token was extracted
    token_end_index = 0

    # Contains one of the token base type definitions (Point, Connector, Modifier
    # etc.) as defined in the 'f15_token_descriptions.TokenBaseType' class.
    token_base_type = 0

    # Contains one of the token subtype definitions (TASRFL, MACHVFR, Point,
    # Aerodrome etc.) as defined in the 'f15_token_descriptions.TokenSubType' class.
    token_sub_type = 0

    # Creates a token with its text, start and end index
    def __init__(self, token_string="", token_start_index=0, token_end_index=0):
        self.token_string = token_string
        self.token_start_index = token_start_index
        self.token_end_index = token_end_index

    # Sets a tokens text
    def set_token_string(self, token_string):
        # type: (str) -> None
        self.token_string = token_string

    # Gets a tokens text
    def get_token_string(self):
        # type: () -> str
        return self.token_string

    # Sets a tokens start index
    def set_token_start_index(self, token_start_index):
        # type: (int) -> None
        self.token_start_index = token_start_index

    # Gets a tokens start index
    def get_token_start_index(self):
        # type: () -> int
        return self.token_start_index

    # Sets a tokens end index
    def set_token_end_index(self, token_end_index):
        # type: (int) -> None
        self.token_end_index = token_end_index

    # Gets a tokens end index
    def get_token_end_index(self):
        # type: () -> int
        return self.token_end_index

    # Sets a tokens base type
    def set_token_base_type(self, token_base_type):
        # type: (int) -> None
        self.token_base_type = token_base_type

    # Gets a tokens base type
    def get_token_base_type(self):
        # type: () -> int
        return self.token_base_type

    # Sets a tokens subtype
    def set_token_sub_type(self, token_sub_type):
        # type: (int) -> None
        self.token_sub_type = token_sub_type

    # Gets a tokens subtype
    def get_token_sub_type(self):
        # type: () -> int
        return self.token_sub_type

    def print_token(self):
        # type: () -> None
        print("{0:>9}".format(self.token_string) +
              "{0:>6}".format(self.token_start_index) +
              "{0:>5}".format(self.token_end_index) +
              "{0:>5}".format(self.token_base_type) +
              "{0:>5}".format(self.token_sub_type))
