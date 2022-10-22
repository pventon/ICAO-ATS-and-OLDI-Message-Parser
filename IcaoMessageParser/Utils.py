import re

from Configuration.ErrorMessages import ErrorMessages
from Configuration.EnumerationConstants import ErrorId, MessageTitles, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from Tokenizer.Tokenize import Tokenize


class Utils:
    """This class provides utility methods for the ICAO and OLDI Message Parser."""

    @staticmethod
    def add_error(flight_plan_record, erroneous_field_text, start_index, end_index, error_messages, error_id):
        # type: (FlightPlanRecord, str, int, int, ErrorMessages, ErrorId) -> None
        """This method adds an error to the Flight Data Record

            :param flight_plan_record: Flight Data Record into which an error is written;
            :param erroneous_field_text: The field that is in error;
            :param start_index: Zero based start index of the erroneous fields position in the original message;
            :param end_index: Zero based end index of the erroneous fields position in the original message;
            :param error_messages: Configuration data containing a dictionary of all error messages;
            :param error_id: Index into the error message dictionary in ErrorMessageDefinitions;
            :return: None"""
        error_text = error_messages.get_error_message(error_id).replace("!", erroneous_field_text)
        flight_plan_record.add_erroneous_field(
            erroneous_field_text, error_text, start_index, end_index)

    @staticmethod
    def add_subfield_error(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> None
        """Helper method to save an error to the flight plan record where the subfield
        is the subfield in error.

        :param flight_plan_record: Flight Data Record into which an error is written;
        :param subfield: The subfield in error;
        :param error_id: An enumeration value identifying the error associated with this subfield
        :return: None
        """
        Utils.add_error(flight_plan_record,
                        subfield.get_field_text(),
                        subfield.get_start_index(),
                        subfield.get_end_index(),
                        ErrorMessages(),
                        error_id)

    @staticmethod
    def check_too_many_fields(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> bool
        """This method checks if there are more than one single token in a field

        :param flight_plan_record: Flight Data Record into which an error is written;
        :param subfield: The subfield in error;
        :param error_id: An enumeration value identifying the error associated with this subfield;
        :return: True if there is only 1 token in this subfield, False if more than 1;
        """
        if len(subfield.get_field_text().split()) > 1:
            Utils.add_subfield_error(flight_plan_record, subfield, error_id)
            return False
        return True

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
    def is_dof(dof):
        # type: (str) -> bool
        """This method checks if a DOF has the correct syntax; ensures that the leap year and the number of
        days in February is correct for any year. DOF format should be YYMMDD;

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
    def parse_for_alpha_num(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> None
        """This method validates that the subfield text string conforms to the regular
        expression [A-Z0-9 ], if not an error is added to the flight plan record.

        :param flight_plan_record: The flight plan into which an error may be written
        :param subfield: The subfield whose field text is being parsed;
        :param error_id: The error message that will be reported if the subfield text does not
               match the regular expression.
        :return: None
        """
        Utils.parse_for_regexp(flight_plan_record, subfield, error_id, "[A-Z0-9 ]+")

    @staticmethod
    def parse_for_hex_address(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> None
        """This method validates that the subfield text string conforms to the regular
        expression F[A-F0-9]{6}, (a 7 digit HEX value), if not an error is added to the flight plan record.
        The HEX address starts at F000000;

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param error_id: The error message that will be reported if the subfield text does not
               match the regular expression;
        :return: None
        """
        Utils.parse_for_regexp(flight_plan_record, subfield, error_id, "F[A-F0-9]{6}")

    @staticmethod
    def parse_for_regexp(flight_plan_record, subfield, error_id, regexp):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId, str) -> None
        """This method validates that the subfield text string conforms to the regular
        expression defined in the parameter regexp, if not an error is added to the flight plan record.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param error_id: The error message that will be reported if the subfield text does not
               match the regular expression;
        :param regexp: The regular expression used to parse the text in the subfield;
        :return: None
        """
        mo = re.fullmatch(regexp, subfield.get_field_text())
        if mo is None:
            Utils.add_subfield_error(flight_plan_record, subfield, error_id)

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

            :param str_: The string being split into two parts;
            :param char: The character at which the string will be split if found in the str_ string;
            :return: A list of two strings or None if no character was found in the string;"""
        idx = str_.find(char)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_index(str_, idx):
        # type: (str, int) -> []
        """This method splits a string into two parts at the index specified in the parameters.

            :param str_: The string being split into two parts
            :param idx: The index at which the string is to be split
            :return: A list of two strings or None if the index is out of range"""
        if idx < 1 or len(str_) < 2 or idx >= len(str_):
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def title_defined(f3):
        # type: (str) -> MessageTitles | None
        """This method checks if a message title is supported by checking if it can be found in an
        enumeration of EnumerationConstants.MessageTitles class.

            :param f3: A string containing a message title;
            :return: An enumeration instance of MessageTitles or None if the message
                     title is not defined / supported."""
        for title in MessageTitles:
            if title.name == f3:
                return title
        return None
