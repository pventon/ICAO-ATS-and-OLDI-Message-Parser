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
    def parse_f18_dle(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the field 18 DLE subfield syntax conforms to a point
        followed by a time in HHMM format. The point can be any type, i.e. PRP, latitude/longitude
        or a bearing distance.

        To parse this field, it is assumed that the last 4 characters are the time, the rest some kind of
        point. The point and hhmm subfield definitions will be used to parse the two parts
        of this field. Errors are reported if this subfield is not a 'point hhmm' string.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 6:
            # The field is too short, minimum is a two letter point followed by HHMM
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_DLE_TOO_SHORT)
            return

        # Check if there are more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_DLE_TOO_MANY):
            return

        # Split the time from the point
        split_field = Utils.split_on_index(subfield.get_field_text(), len(subfield.get_field_text()) - 4)

        # Validate the point
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F14a).get_field_syntax(),
                          split_field[0])
        if mo is None:
            Utils.add_error(flight_plan_record,
                            subfield.get_field_text()[0:len(subfield.get_field_text()) - 4],
                            subfield.get_start_index(),
                            subfield.get_end_index() - 4,
                            ErrorMessages(),
                            ErrorId.F18_DLE_PNT_SYNTAX)

        # Validate the time
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F16b).get_field_syntax(),
                          split_field[1])
        if mo is None:
            Utils.add_error(flight_plan_record,
                            subfield.get_field_text()[len(subfield.get_field_text()) - 4:],
                            subfield.get_start_index() + len(subfield.get_field_text()) - 4,
                            subfield.get_end_index(),
                            ErrorMessages(),
                            ErrorId.F18_DLE_TIME_SYNTAX)

    @staticmethod
    def parse_f18_dof(flight_plan_record, subfield, error_id):
        # type: (FlightPlanRecord, SubFieldRecord, ErrorId) -> None
        """This method validates that the subfield text string conforms to the DOF format
        YYMMDD, if not an error is added to the flight plan record.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param error_id: The error message that will be reported if the subfield text does not
               match the regular expression;
        :return: None
        """
        if not Utils.is_dof(subfield.get_field_text()):
            Utils.add_subfield_error(flight_plan_record, subfield, error_id.F18_DOF_F18A_SYNTAX)

    @staticmethod
    def parse_f18_eet(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates the F18 EET field; this field consists of one or more
        point & time tokens. The field will be tokenized and each token parsed for correct syntax
        and semantics. Each token syntax must conform to a point followed by a time in HHMM format.
        The point can be any type, i.e. PRP, latitude/longitude or a bearing distance.

        To parse this field, it is assumed that the last 4 characters in a token are the time, the
        rest some kind of point. The point and hhmm subfield definitions will be used to parse the
        two parts of this field. Errors are reported if any part of these subfield tokens is not a
        'point hhmm' string.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Tokenize the EET field, there can be a lot of these subfields in a message
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Split the time from the point
            split_field = Utils.split_on_index(token.get_token_string(), len(token.get_token_string()) - 4)

            # Validate the point
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F14a).get_field_syntax(),
                              split_field[0])
            if mo is None:
                # Report an error, point syntax is invalid
                Utils.add_error(flight_plan_record,
                                token.get_token_string()[0:len(token.get_token_string()) - 4],
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index() - 4,
                                ErrorMessages(),
                                ErrorId.F18_EET_PNT_SYNTAX)

            # Validate the time
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F16b).get_field_syntax(),
                              split_field[1])
            if mo is None:
                # Report an error, time syntax is invalid
                Utils.add_error(
                    flight_plan_record,
                    token.get_token_string()[len(token.get_token_string()) - 4:],
                    token.get_token_start_index() + subfield.get_start_index() + len(token.get_token_string()) - 4,
                    token.get_token_end_index() + subfield.get_start_index(),
                    ErrorMessages(),
                    ErrorId.F18_EET_TIME_SYNTAX)

    @staticmethod
    def parse_f18_ifp(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 IFP contains one or more of the following:
        ERROUTRAD, ERROUTWE, ERROUTE, ERRTYPE, ERRLEVEL, ERREOBT, NON833, 833UNKNOWN, MODESASP,
        RVSMVIOLATION, NONRVSM or RVSMUNKNOWN.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Tokenize the IFP subfield
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Regular expression for the subfield tokens
        regexp = "[ ]*(ERROUTRAD|ERROUTWE|ERROUTE|ERRTYPE|ERRLEVEL|ERREOBT|NON833|833UNKNOWN" \
                 "|MODESASP|RVSMVIOLATION|NONRVSM|RVSMUNKNOWN)[ ]*"

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Validate the subfield against the valid syntax
            mo = re.fullmatch(regexp, token.get_token_string())
            if mo is None:
                # Did not match, report an error
                Utils.add_error(flight_plan_record,
                                token.get_token_string(),
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index(),
                                ErrorMessages(),
                                ErrorId.F18_IFP_SYNTAX)

    @staticmethod
    def parse_f18_orgn(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F18 ORGN conforms to a facility address.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 7:
            # The field is too short, minimum is 7 characters
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_ORGN_TOO_SHORT)

        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_ORGN_TOO_MANY):
            return

        # Validate the facility address
        mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.ADDRESS1).get_field_syntax(),
                          subfield.get_field_text())
        if mo is None:
            # Report an error, facility address syntax is incorrect
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_ORGN_SYNTAX)

    @staticmethod
    def parse_f18_pbn(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates that the F18 PBN subfield conforms to one or more of the PBN indicators.
        These indicators are A1, B1-B6, C1-C4, D1-D4, L1, O1-O4, S1, S2, T1 or T2.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        if len(subfield.get_field_text()) < 2:
            # The field is too short, minimum is at least one two letter PBN indicator
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PBN_TOO_SHORT)

        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_PBN_TOO_MANY):
            return

        # Validate the PBN indicator(s)
        mo = re.fullmatch(sfd.pbn, subfield.get_field_text().rstrip().lstrip())
        if mo is None:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PBN_SYNTAX)

    @staticmethod
    def parse_f18_per(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 PER subfield syntax conforms to one of the performance
        indicators, a single letter from the set 'A', 'B', 'C', 'D', 'E' or 'H'.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there are more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_PER_TOO_MANY):
            return

        # Validate the PER indicator
        mo = re.fullmatch("[ABCDEH]", subfield.get_field_text().rstrip().lstrip())
        if mo is None:
            Utils.add_subfield_error(flight_plan_record, subfield, ErrorId.F18_PER_SYNTAX)

    @staticmethod
    def parse_f18_rfp(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 PER subfield syntax conforms to the RFP indicator Q[1 to 9].

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_RFP_TOO_MANY):
            return

        # Parse the RFP for a valid 'Q'n indicator
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RFP_SYNTAX, "[ ]*Q[1-9][ ]*")

    @staticmethod
    def parse_f18_rmk(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 RMK subfield conforms to appropriate syntax;
        it's a free format text field, however the text is limited to a subset of the IAT character set.
        Allowable characters are 'A' to 'Z', '0' to '9', ':', ';', '.' or ','.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Parse the RMK subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RMK_SYNTAX, "[A-Z0-9:;., ]+")

    @staticmethod
    def parse_f18_rvr(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 RVR subfield syntax conforms to 1 to 3 digits;

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_RVR_TOO_MANY):
            return

        # Parse the RVR subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_RVR_SYNTAX, "[ ]*[0-9]{1,3}[ ]*")

    @staticmethod
    def parse_f18_sel(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 SEL subfield syntax conforms to a SELCODE value
        defined as 4 to 5 letters 'A' to 'Z'

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_SEL_TOO_MANY):
            return

        # Parse the SEL subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_SEL_SYNTAX, "[ ]*[A-Z]{4,5}[ ]*")

    @staticmethod
    def parse_f18_sts(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 STS subfield syntax conforms to one of the following text strings:
            - ALTRV | ATFMX | FFR | FLTCK | HAZMAT | HEAD | HOSP | HUM | MARSA | MEDEVAC | NONRVSM | SAR | STATE;

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_STS_TOO_MANY):
            return

        # Parse the STS subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_STS_SYNTAX,
                               "[ ]*(ALTRV|ATFMX|FFR|FLTCK|HAZMAT|HEAD|HOSP|HUM|MARSA|MEDEVAC|NONRVSM|SAR|STATE)[ ]*")

    @staticmethod
    def parse_f18_src(flight_plan_record, subfield):
        # type: (FlightPlanRecord, SubFieldRecord) -> None
        """This method validates that the F18 SRC subfield syntax conforms to one of the following text strings:
            - RPL | FPL | AFIL | MFS | FNM | RQP | AFP | DIV | [A-Z]{4};

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :return: None
        """
        # Check if there is more than a single token
        if not Utils.check_too_many_fields(flight_plan_record, subfield, ErrorId.F18_SRC_TOO_MANY):
            return

        # Parse the SRC subfield
        Utils.parse_for_regexp(flight_plan_record, subfield, ErrorId.F18_SRC_SYNTAX,
                               "[ ]*(RPL|FPL|MFS|FNM|RQP|AFP|DIV|[A-Z]{4})[ ]*")

    @staticmethod
    def parse_f18_typ(flight_plan_record, subfield, sfd):
        # type: (FlightPlanRecord, SubFieldRecord, SubFieldDescriptions) -> None
        """This method validates the F18 TYP subfield; this field consists of one or more
        number and type of aircraft tokens. The subfield will be tokenized and each token parsed for
        correct syntax and semantics.

        :param flight_plan_record: The flight plan into which an error may be written;
        :param subfield: The subfield whose field text is being parsed;
        :param sfd: Configuration data containing the subfield syntax definitions;
        :return: None
        """
        # Tokenize the subfield string
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(subfield.get_field_text())
        tokenize.set_whitespace(" /n/t/r")
        tokenize.tokenize()
        tokens = tokenize.get_tokens()

        # Loop over the tokens
        for token in tokens.get_tokens():

            # Validate the number of (optional) and aircraft type
            mo = re.fullmatch(sfd.get_subfield_description(SubFieldIdentifiers.F9a).get_field_syntax() +
                              sfd.get_subfield_description(SubFieldIdentifiers.F9b).get_field_syntax(),
                              token.get_token_string())
            if mo is None:
                # Report an error, syntax did not match
                Utils.add_error(flight_plan_record,
                                token.get_token_string(),
                                token.get_token_start_index() + subfield.get_start_index(),
                                token.get_token_end_index() + subfield.get_start_index(),
                                ErrorMessages(),
                                ErrorId.F18_TYP_SYNTAX)

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
