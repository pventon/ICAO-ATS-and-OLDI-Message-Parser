from Configuration.EnumerationConstants import ErrorId, MessageTitles
from Configuration.ErrorMessages import ErrorMessages
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord


class Utils:
    # This method adds an error to the Flight Data Record
    # Arguments
    # ---------
    # flight_plan_record:   Flight Data Record into which an error is written
    # erroneous_field_text: The field that is in error
    # start_index:          Zero based start index of the erroneous fields position
    #                       in the original message
    # end_index:            Zero based end index of the erroneous fields position
    #                       in the original message
    # error_id:             Index into the error message dictionary in ErrorMessageDefinitions
    @staticmethod
    def add_error(flight_plan_record, erroneous_field_text, start_index, end_index, error_messages, error_id):
        # type: (FlightPlanRecord, str, int, int, ErrorMessages, ErrorId) -> None
        error_text = error_messages.get_error_message(error_id).replace("!", erroneous_field_text)
        flight_plan_record.add_erroneous_field(
            erroneous_field_text, error_text, start_index, end_index)

    @staticmethod
    def get_first_digit_index(str_):
        # type: (str) -> int
        for index, char in enumerate(str_):
            if char.isdigit():
                return index
        return -1

    @staticmethod
    def get_first_alpha_index(str_):
        # type: (str) -> int
        for index, char in enumerate(str_):
            if char.isalpha():
                return index
        return -1

    @staticmethod
    def split_on_first_digit(str_):
        # type: (str) -> []
        idx = Utils.get_first_digit_index(str_)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_first_alpha(str_):
        # type: (str) -> []
        idx = Utils.get_first_alpha_index(str_)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_first_character(str_, char):
        # type: (str, str) -> []
        idx = str_.find(char)
        if idx < 0:
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def split_on_index(str_, idx):
        # type: (str, int) -> []
        if idx < 1 or len(str_) < 2 or idx >= len(str_):
            return None
        return [str_[0:idx], str_[idx:]]

    @staticmethod
    def is_dof(dof):
        # type: (str) -> bool
        if len(dof) != 6 or dof.isnumeric() is False:
            return False

        yy = int(dof[0:2])
        mm = int(dof[2:4])
        dd = int(dof[4:])

        day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0):
            day_count_for_month[2] = 29
        return 1 <= mm <= 12 and 1 <= dd <= day_count_for_month[mm]

    # This method checks if a message title is supported by checking if it
    # can be found in an enumeration of EnumerationConstants.MessageTitles class.
    # Arguments
    # ---------
    # f3:       A string containing a message title;
    # return:   An enumeration instance of MessageTitles or
    #           None if the message title is not defined / supported.
    @staticmethod
    def title_defined(f3):
        # type: (str) -> MessageTitles | None
        for title in MessageTitles:
            if title.name == f3:
                return title
        return None
