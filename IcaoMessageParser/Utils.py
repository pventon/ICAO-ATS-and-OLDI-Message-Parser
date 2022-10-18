from Configuration.EnumerationConstants import ErrorId, MessageTitles
from Configuration.ErrorMessages import ErrorMessages
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class Utils:
    """This class provides utility methods for the ICAO and OLDI Message Parser."""

    @staticmethod
    def add_error(flight_plan_record, erroneous_field_text, start_index, end_index, error_messages, error_id):
        # type: (FlightPlanRecord, str, int, int, ErrorMessages, ErrorId) -> None
        """This method adds an error to the Flight Data Record

            :param flight_plan_record: Flight Data Record into which an error is written
            :param erroneous_field_text: The field that is in error
            :param start_index: Zero based start index of the erroneous fields position in the original message
            :param end_index: Zero based end index of the erroneous fields position in the original message
            :param error_id: Index into the error message dictionary in ErrorMessageDefinitions
            :return: None"""
        error_text = error_messages.get_error_message(error_id).replace("!", erroneous_field_text)
        flight_plan_record.add_erroneous_field(
            erroneous_field_text, error_text, start_index, end_index)

    @staticmethod
    def get_first_digit_index(str_):
        # type: (str) -> int
        """This method returns a zero based index of the first digit found in a string.

            :param str_: The string being searched for a digit
            :return: The zero based index of the first digit or -1 if no digit could be found"""
        for index, char in enumerate(str_):
            if char.isdigit():
                return index
        return -1

    @staticmethod
    def get_first_alpha_index(str_):
        # type: (str) -> int
        """This method returns a zero based index of the first alpha found in a string.

            :param str_: The string being searched for an alpha
            :return: The zero based index of the first alpha or -1 if no alpha could be found"""
        for index, char in enumerate(str_):
            if char.isalpha():
                return index
        return -1

    @staticmethod
    def get_first_slash_index(str_):
        # type: (str) -> int
        """This method returns a zero based index of the first forward slash '/' found in a string.

            :param str_: The string being searched for a forward slash '/' character
            :return: The zero based index of the first forward slash or -1 if no forward slash could be found"""
        for index, char in enumerate(str_):
            if char == "/":
                return index
        return -1


    @staticmethod
    def split_on_first_digit(str_):
        # type: (str) -> []
        """This method splits a string into two parts at the index of the first digit in the string.

            :param str_: The string being split into two parts
            :return: A list of two strings or None if no digit was found in the string"""
        idx = Utils.get_first_digit_index(str_)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_first_alpha(str_):
        # type: (str) -> []
        """This method splits a string into two parts at the index of the first alpha in the string.

            :param str_: The string being split into two parts
            :return: A list of two strings or None if no alpha was found in the string"""
        idx = Utils.get_first_alpha_index(str_)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_first_character(str_, char):
        # type: (str, str) -> []
        """This method splits a string into two parts at the index of the first character in the string.

            :param str_: The string being split into two parts
            :return: A list of two strings or None if no character was found in the string"""
        idx = str_.find(char)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_index(str_, idx):
        """This method splits a string into two parts at the index specified in the parameters.

            :param str_: The string being split into two parts
            :param idx: The index at which the string is to be split
            :return: A list of two strings or None if the index is out of range"""
        # type: (str, int) -> []
        if idx < 1 or len(str_) < 2 or idx >= len(str_):
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def is_dof(dof):
        # type: (str) -> bool
        """This method checks if a DOF has the correct syntax; ensures that the leap year and the number of
        days in February is correct for any year.

            :param dof: The DOF being checked for correct syntax and semantics
            :return: True if the DOF syntax and semantics is correct, False otherwise"""
        if len(dof) != 6 or dof.isnumeric() is False:
            return False

        yy = int(dof[0:2])
        mm = int(dof[2:4])
        dd = int(dof[4:])

        day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0):
            day_count_for_month[2] = 29
        return 1 <= mm <= 12 and 1 <= dd <= day_count_for_month[mm]

    @staticmethod
    def title_defined(f3):
        # type: (str) -> MessageTitles | None
        """This method checks if a message title is supported by checking if it can be found in an
        enumeration of EnumerationConstants.MessageTitles class.

            :param f3: A string containing a message title;
            :return: An enumeration instance of MessageTitles or None if the message title is not defined / supported."""
        for title in MessageTitles:
            if title.name == f3:
                return title
        return None
