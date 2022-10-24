from F15_Parser.F15TokenSyntaxDescriptions import TokenBaseType, TokenSubType


class Token:
    """This class represents a single token along with all its attributes unique
    to a token. Each token is stored with its associated attributes:
        - Token text; a string of characters;
        - Token start index - zero based index into the string where a tokens first
          character was found in the source string;
        - Token end index - zero based index into the string where a tokens last + 1
          character was found in the source string;
    In addition, two further attributes are provided in this class that store
    the following:
        - Token Base Type - Derived from a tokens' syntax as defined in the
          'F15TokenSyntaxDescriptions.TokenBaseType' class.
        - Token Subtype - Derived from a tokens syntax as defined in the
          'F15TokenSyntaxDescriptions.TokenSubType' class."""

    token_string: str = ""
    """# A string representing a token"""

    token_start_index: int = 0
    """The start index of a token into the string from which a token was extracted"""

    token_end_index: int = 0
    """The end index of a token into the string from which a token was extracted"""

    token_base_type: TokenBaseType = 0
    """Contains one of the token base type definitions (Point, Connector, Modifier
    # etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenBaseType' class."""

    token_sub_type: TokenSubType = 0
    """Contains one of the token subtype definitions (TASRFL, MACHVFR, Point,
    # Aerodrome etc.) as defined in the 'F15TokenDescriptions.TokenSubType' class."""

    def __init__(self, token_string="", token_start_index=0, token_end_index=0):
        # type: (str, int, int) -> None
        """Creates a token with its text, start and end index. The base and subtype
        members are initialised as 'unknown'.

            :param token_string: The text that is the token;
            :param token_start_index: The zero based start index of the token text's position in the original string;
            :param token_end_index: The zero based end index of the token text's position in the original string;
            :return: None"""
        self.token_string = token_string
        self.token_start_index = token_start_index
        self.token_end_index = token_end_index
        self.token_base_type = TokenBaseType.F15_UNKNOWN
        self.token_sub_type = TokenSubType.F15_SB_UNKNOWN

    def set_token_string(self, token_string):
        # type: (str) -> None
        """This method sets the token string.

            :param token_string: The text that will be stored in this token instance;
            :return: None"""
        self.token_string = token_string

    def get_token_string(self):
        # type: () -> str
        """This method gets a token's string.

            :return: The text that stored in this token instance;"""
        return self.token_string

    # Sets a tokens start index
    def set_token_start_index(self, token_start_index):
        # type: (int) -> None
        """This method sets a tokens zero based start index of its position in the original
        string it was extracted from.

            :return: None"""
        self.token_start_index = token_start_index

    # Gets a tokens start index
    def get_token_start_index(self):
        # type: () -> int
        """This method gets this tokens zero based start index of its position in the original
        string it was extracted from.

            :return: This tokens zero based start index of its position in
                     the original string it was extracted from."""
        return self.token_start_index

    # Sets a tokens end index
    def set_token_end_index(self, token_end_index):
        # type: (int) -> None
        """This method sets a tokens zero based end index of its position in the original
        string it was extracted from.

            :return: None"""
        self.token_end_index = token_end_index

    # Gets a tokens end index
    def get_token_end_index(self):
        # type: () -> int
        """This method gets this tokens zero based end index of its position in the original
        string it was extracted from.

            :return: This tokens zero based end index of its position in the original string it was extracted from."""
        return self.token_end_index

    def set_token_base_type(self, token_base_type):
        # type: (TokenBaseType) -> None
        """This method sets the tokens base type based on the syntax definitions defined
        in the F15TokenSyntaxDescriptions.TokenBaseType class.

            :return: None"""
        self.token_base_type = token_base_type

    def get_token_base_type(self):
        # type: () -> TokenBaseType
        """This method gets the tokens base type.

            :return: The tokens base type as an enumeration value defined in the
                     F15TokenSyntaxDescriptions.TokenBaseType class."""
        return self.token_base_type

    def set_token_sub_type(self, token_sub_type):
        # type: (TokenSubType) -> None
        """This method sets the tokens subtype based on the syntax definitions defined
        in the F15TokenSyntaxDescriptions.TokenSubType class.

            :return: None"""
        self.token_sub_type = token_sub_type

    def get_token_sub_type(self):
        # type: () -> TokenSubType
        """This method gets the tokens' subtype.

            :return: The tokens subtype as an enumeration value defined in the
                     F15TokenSyntaxDescriptions.TokenSubType class."""
        return self.token_sub_type

    def print_token(self):
        # type: () -> None
        """This method prints the token to the console. This method is available for debugging if needed.

            :return: None"""
        print("{0:>9}".format(self.get_token_string()) +
              "{0:>6}".format(self.get_token_start_index()) +
              "{0:>5}".format(self.get_token_end_index()) +
              "{0:>5}".format(self.get_token_base_type()) +
              "{0:>5}".format(self.get_token_sub_type()))
