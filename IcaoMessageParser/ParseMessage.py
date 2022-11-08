import re

from Configuration.EnumerationConstants import MessageTypes, MessageTitles, AdjacentUnits, ErrorId, FieldIdentifiers, \
    SubFieldIdentifiers, FlightRules
from Configuration.ErrorMessages import ErrorMessages
from Configuration.FieldsInMessage import FieldsInMessage
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.MessageDescription import MessageDescription
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseAdditionalAddressee import ParseAdditionalAddressee
from IcaoMessageParser.ParseAddressee import ParseAddressee
from IcaoMessageParser.ParseF3 import ParseF3
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from IcaoMessageParser.ParseFilingTime import ParseFilingTime
from IcaoMessageParser.ParseOriginator import ParseOriginator
from IcaoMessageParser.ParsePriorityIndicator import ParsePriorityIndicator
from IcaoMessageParser.Utils import Utils
from Tokenizer.Tokenize import Tokenize, Tokens


class ParseMessage:
    """This class is the entry point for parsing complete ICAO format messages for both ATS and OLDI
    messages. The parser is able to automatically evaluate if a message contains a header or not. For
    ICAO ATS messages the data definitions are set up as a single data set; for OLDI messages the
    definitions vary depending on an adjacent unit sending identifier.

    The entry point method is 'parse_message()' that takes an instance of FlightPlanRecord and a
    string containing the message to parse. The FlightPlanRecord is populated by the parser and
    includes all extracted fields, an extracted route (if field 15 is present) and any errors. It
    is a callers responsibility to retrieve the errors.

    If this software is used in conjunction with a GUI, all the fields are stored with their zero
    based index into the message so that erroneous fields can be highlighted in the GUI. This makes
    message correction quite simple for end users.

    Note: Eventually this parser will also support ADEXP message parsing; currently an error is reported
    when an ADEXP message is encountered.

    This class is thread safe and can be used simultaneously on multiple threads. This class includes
    the message field list definitions (the configuration data for the parser) by instantiating the
    MessageDescriptions class and assigning this the MCD member of this class.
    """

    MINIMUM_HEADER_LENGTH: int = 20
    """Minimum length of header text, anything less than this is considered junk and added to the message body."""

    MINIMUM_BODY_LENGTH: int = 12
    """Minimum message length under which a message is considered junk, no attempt will be made to parse it 
    further. The shortest message is a LAM, LAML/E012E/L001 -> 15 characters minimum."""

    FIM: FieldsInMessage = FieldsInMessage()
    """Configuration data defining the fields in a message for all message titles"""

    SFIF: SubFieldsInFields = SubFieldsInFields()
    """Configuration data mapping ICAO fields to their respective subfields"""

    SFD: SubFieldDescriptions = SubFieldDescriptions()
    """Configuration data providing subfield syntax definitions & other data"""

    EM: ErrorMessages = ErrorMessages()
    """Configuration data containing all the error messages"""

    def consistency_check(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method performs consistency checking between various fields, that includes:
            - Flight rules between F8a and the flight rules derived by the F15 parsing and route
              extraction process; these must match.
            - If F10a contains the letter 'Z' then one or more of the F18 subfields
              'COM', 'NAV' or 'DAT' must be present;
            - If F10a contains the letter 'R' then the F18 'PBN' subfield must be present and
              contain one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5';
            - If F18 contains the subfield 'PBN', F10a must contain an 'R';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1',
              'D2', 'O1' or 'O2', then F10a must contain the letter 'G';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B3', 'C1', 'C3', 'D1',
              'D3', 'O1' or 'O3', then F10a must contain the letter 'D';
            - If F18 'PBN' contains one or more of the indicators 'B1' or 'B4', then F10a must
              contain either an 'O' or 'S' and a 'D';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1',
              'D4', 'O1' or 'O4', then F10a must contain the letter 'I';
            - If F18 'PBN' contains one or more of the indicators 'C1', 'C4', 'D1', 'D4', 'O1'
              or 'O4', then F10a must contain the letter 'D';

        These consistency checks are only carried out on message titles defined to contain both field 10
        and field 18, and/or field 8 and 15. These messages are:
            - AFP
            - ALR
            - APL
            - CPL
            - FPL

        :param flight_plan_record: Flight plan record used for checking consistency;
        :return: False if errors are detected, True if all is OK;
        """
        if flight_plan_record.get_message_title() is not MessageTitles.AFP and \
                flight_plan_record.get_message_title() is not MessageTitles.ALR and \
                flight_plan_record.get_message_title() is not MessageTitles.APL and \
                flight_plan_record.get_message_title() is not MessageTitles.CPL and \
                flight_plan_record.get_message_title() is not MessageTitles.FPL:
            return True

        # Consistency check the flight rules in F8a and those derived from F15
        result1: bool = self.consistency_check_flight_rules(flight_plan_record)

        # Check if the flight plan contains f10
        if flight_plan_record.get_icao_field(FieldIdentifiers.F10) is None:
            return result1

        # Get field 10a
        if flight_plan_record.get_icao_subfield(FieldIdentifiers.F10, SubFieldIdentifiers.F10a) is None:
            f10a = ""
        else:
            f10a = flight_plan_record.get_icao_subfield(FieldIdentifiers.F10, SubFieldIdentifiers.F10a).get_field_text()

        # Check various field 10 consistency checks
        result2 = self.consistency_check_f10a_r(flight_plan_record, f10a)
        result3 = self.consistency_check_f10a_z(flight_plan_record, f10a)
        result4 = self.consistency_check_pbn(flight_plan_record, f10a)
        result5 = self.consistency_check_f9b_dep(flight_plan_record)
        result6 = self.consistency_check_f13a_dep(flight_plan_record)
        result7 = self.consistency_check_f16a_dep(flight_plan_record)

        return result1 or result2 or result3 or result4 or result5 or result6 or result7

    def consistency_check_pbn(self, flight_plan_record, f10a):
        # type: (FlightPlanRecord, str) -> bool
        """This method consistency checks that one of the following dealing with the field
        18 PBN subfield:
            - If F18 contains the subfield 'PBN', F10a must contain an 'R';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1',
              'D2', 'O1' or 'O2', then F10a must contain the letter 'G';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B3', 'C1', 'C3', 'D1',
              'D3', 'O1' or 'O3', then F10a must contain the letter 'D';
            - If F18 'PBN' contains one or more of the indicators 'B1' or 'B4', then F10a must
              contain either an O' or 'S' and a 'D';
            - If F18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1',
              'D4', 'O1' or 'O4', then F10a must contain the letter 'I';
            - If F18 'PBN' contains one or more of the indicators 'C1', 'C4', 'D1', 'D4', 'O1'
              or 'O4', then F10a must contain the letter 'D';
        Another way to simplify the logic is to use a table to identify the permutations:
             | B1| B2| B3| B4| B5| C1| C2| C3| C4| D1| D2| D3| D4| O1| O2| O3| O4|
          D  | X |   | X | X |   | X |   | X | X | X |   | X | X | X |   | X | X |
          G  | X | X |   |   |   | X | X |   |   | X | X |   |   | X | X |   |   |
          I  | X |   |   |   | X | X |   |   | X | X |   |   | X | X |   |   | X |
         O|S | X |   |   | X |   |   |   |   |   |   |   |   |   |   |   |   |   |
          R  | X | X | X | X | X |   |   |   |   |   |   |   |   |   |   |   |   |

        :param flight_plan_record: Flight plan record used for checking consistency;
        :param f10a: The contents of field 10a;
        :return: False if errors are detected, True if all is OK;
        """
        result = True
        pbn = flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18pbn)
        if pbn is not None:
            if len(re.findall("B1|B3|B4|C1|C3|C4|D1|D3|D4|O1|O3|O4", pbn.get_field_text())) != 0:
                if f10a.find("D") == -1:
                    # Missing 'D' in field 10a, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_PBN_D)
                    result = False
            if len(re.findall("B1|B2|C1|C2|D1|D2|O1|O2", pbn.get_field_text())) != 0:
                if f10a.find("G") == -1:
                    # Missing 'G' in field 10a, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_PBN_G)
                    result = False
            if len(re.findall("B1|B5|C1|C4|D1|D4|O1|O4", pbn.get_field_text())) != 0:
                if f10a.find("I") == -1:
                    # Missing 'I' in field 10a, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_PBN_I)
                    result = False
            if len(re.findall("B1|B4", pbn.get_field_text())) != 0:
                if len(re.findall("[OS]", f10a)) == 0:
                    # Missing 'O' and 'S' in field 10a, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_PBN_OS)
                    result = False
            if len(re.findall("B[1-5]", pbn.get_field_text())) != 0:
                if f10a.find("R") == -1:
                    # Missing 'R' in field 10a, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_PBN_R)
                    result = False

        return result

    def consistency_check_f9b_dep(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method consistency checks that if F9b contains 'ZZZZ' that there is
        a field 18 TYP subfield;

        :param flight_plan_record: Flight plan record used for checking consistency;
        :return: False if errors are detected, True if all is OK;
        """
        # Check if the flight plan contains f9
        if flight_plan_record.get_icao_field(FieldIdentifiers.F9) is None:
            return True

        # Get field 9b
        if flight_plan_record.get_icao_subfield(FieldIdentifiers.F9, SubFieldIdentifiers.F9b) is None:
            f9b = ""
        else:
            f9b = flight_plan_record.get_icao_subfield(FieldIdentifiers.F9, SubFieldIdentifiers.F9b).get_field_text()

        # Check if field 9b contains 'ZZZZ'
        if f9b == "ZZZZ":
            if flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18typ) is None:
                # Missing field 18 subfield TYP, error
                Utils.add_error(flight_plan_record, "", 0, 0, self.EM, ErrorId.CONSISTENCY_F9B_TYP)
                return False

        return True

    def consistency_check_f10a_r(self, flight_plan_record, f10a):
        # type: (FlightPlanRecord, str) -> bool
        """This method consistency checks that if F10a contains the letter 'R' then the F18
        'PBN' subfield must be present and contain one or more of the indicators
        'B1', 'B2', 'B3', 'B4' or 'B5';;

        :param flight_plan_record: Flight plan record used for checking consistency;
        :param f10a: The contents of field 10a;
        :return: False if errors are detected, True if all is OK;
        """
        # Check if field 10a contains an 'Z'
        if f10a.find("Z") > -1:
            if flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18com) is None and \
                    flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18nav) is None and \
                    flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18dat) is None:
                # Missing field 18 subfields, error
                Utils.add_error(flight_plan_record, "'COM', 'NAV' or 'DAT'", 0, 0,
                                self.EM, ErrorId.CONSISTENCY_F10_Z)
                return False

        return True

    def consistency_check_f10a_z(self, flight_plan_record, f10a):
        # type: (FlightPlanRecord, str) -> bool
        """This method consistency checks that if F10a contains the letter 'Z' then one or
        more of the F18 subfields 'COM', 'NAV' or 'DAT' must be present;

        :param flight_plan_record: Flight plan record used for checking consistency;
        :param f10a: The contents of field 10a;
        :return: False if errors are detected, True if all is OK;
        """
        # Check if field 10a contains an 'R'
        if f10a.find("R") > -1:
            pbn = flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18pbn)
            if pbn is None:
                # Missing field 18 PBN subfield, error
                Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_F10_R)
                return False
            else:
                if len(re.findall("B[1-5]", pbn.get_field_text())) == 0:
                    # Missing field 18 PBN B[1-5] indicators, error
                    Utils.add_error(flight_plan_record, "'PBN'", 0, 0, self.EM, ErrorId.CONSISTENCY_F10_R)
                    return False

        return True

    def consistency_check_f13a_dep(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method consistency checks that if F13a contains 'ZZZZ' that there is
        a field 18 DEP subfield;

        :param flight_plan_record: Flight plan record used for checking consistency;
        :return: False if errors are detected, True if all is OK;
        """
        # Check if the flight plan contains f13
        if flight_plan_record.get_icao_field(FieldIdentifiers.F13) is None:
            return True

        # Get field 13a
        if flight_plan_record.get_icao_subfield(FieldIdentifiers.F13, SubFieldIdentifiers.F13a) is None:
            f13a = ""
        else:
            f13a = flight_plan_record.get_icao_subfield(FieldIdentifiers.F13, SubFieldIdentifiers.F13a).get_field_text()

        # Check if field 13a contains an 'ZZZZ'
        if f13a == "ZZZZ":
            if flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18dep) is None:
                # Missing field 18 subfield DEP, error
                Utils.add_error(flight_plan_record, "", 0, 0,
                                self.EM, ErrorId.CONSISTENCY_F13A_DEP)
                return False

        return True

    def consistency_check_f16a_dep(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method consistency checks that if F16a contains 'ZZZZ' that there is
        a field 18 DEST subfield;

        :param flight_plan_record: Flight plan record used for checking consistency;
        :return: False if errors are detected, True if all is OK;
        """
        # Check if the flight plan contains f16
        if flight_plan_record.get_icao_field(FieldIdentifiers.F16) is None:
            return True

        # Get field 16a
        if flight_plan_record.get_icao_subfield(FieldIdentifiers.F16, SubFieldIdentifiers.F16a) is None:
            f16a = ""
        else:
            f16a = flight_plan_record.get_icao_subfield(FieldIdentifiers.F16, SubFieldIdentifiers.F16a).get_field_text()

        # Check if field 16a contains an 'ZZZZ'
        if f16a == "ZZZZ":
            if flight_plan_record.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18dest) is None:
                # Missing field 18 subfield DEST, error
                Utils.add_error(flight_plan_record, "", 0, 0,
                                self.EM, ErrorId.CONSISTENCY_F16A_DEST)
                return False

        return True

    def consistency_check_flight_rules(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method consistency checks the flight rules given in Field 8a and
        the rules derived from parsing and generated the extracted route from F15.

        :param flight_plan_record: Flight plan record used for checking the flight rules consistency;
        :return: False if errors are detected, True if all is OK;
        """
        # If there is no extracted route bail out
        if flight_plan_record.get_extracted_route() is None:
            return True

        # Get the derived flight rules from the extracted route and set the derived rules
        # to the flight plan record
        flight_plan_record.set_derived_flight_rules(
            FlightRules.get_flight_rules(
                flight_plan_record.get_extracted_route().get_derived_flight_rules()))

        # Get the flight rules from field 8
        if flight_plan_record.get_icao_subfield(FieldIdentifiers.F8, SubFieldIdentifiers.F8a) is None:
            f8a = ""
        else:
            f8a = flight_plan_record.get_icao_subfield(FieldIdentifiers.F8, SubFieldIdentifiers.F8a).get_field_text()

        # Get the derived flight rules
        derived_rules = flight_plan_record.get_derived_flight_rules()
        if f8a == "":
            if derived_rules is not FlightRules.UNKNOWN:
                # Error, derived rules exist, nothing in Field 8a
                Utils.add_error(flight_plan_record, derived_rules.name, 0, 0,
                                self.EM, ErrorId.CONSISTENCY_F8_F8A_UNKNOWN)
                return False
        elif derived_rules is FlightRules.UNKNOWN:
            if f8a != "":
                # Error, derived rules unknown but Field 8a has a rule assigned
                Utils.add_error(flight_plan_record, f8a, 0, 0,
                                self.EM, ErrorId.CONSISTENCY_F8_DERIVED_UNKNOWN)
                return False
        elif FlightRules.get_flight_rules(f8a) is not derived_rules:
            # Error, both flight rules available but different
            Utils.add_error(flight_plan_record, derived_rules.name, 0, 0,
                            self.EM, ErrorId.CONSISTENCY_F8_F8_DERIVED_DIFFERENT)
            return False

        return True

    @staticmethod
    def correct_ers_indices(flight_plan_record):
        # type: (FlightPlanRecord) -> None
        """This method corrects the Field 15 extracted route records start and end indices to add the
        start index of Field 15's position in the message as a whole. The ERS records (and any associated
        ERS error records) start and end indices were calculated based on the start of field 15, (any
        field parsing always starts at zero). To correctly index a field 15 token with respect to the
        message as a whole, the field 15 start index must be added to all start and end indices in the
        ERS records.

        :param flight_plan_record: The flight plan having its ERS records modified;
        :return: None
        """

        # Make sure we have the resources needed to resolve the field 15 ERS indices
        if flight_plan_record.get_icao_field(FieldIdentifiers.F15) is None:
            return
        if flight_plan_record.get_extracted_route() is None:
            return

        f15_field_start_index = flight_plan_record.get_icao_field(FieldIdentifiers.F15).get_start_index()

        for ers_record in flight_plan_record.get_extracted_route().get_all_elements():
            ers_record.set_start_index(ers_record.get_start_index() + f15_field_start_index)
            ers_record.set_end_index(ers_record.get_end_index() + f15_field_start_index)

        for ers_error in flight_plan_record.get_extracted_route().get_all_errors():
            ers_error.set_start_index(ers_error.get_start_index() + f15_field_start_index)
            ers_error.set_end_index(ers_error.get_end_index() + f15_field_start_index)

    @staticmethod
    def determine_message_type(f3):
        # type: (str) -> MessageTypes
        """This method determines the message type (ICAO ATS, OLDI or ADEXP) based on a message title.

        :param f3: The message title as a string
        :return: An enumeration from MessageDescriptions.MessageTypes; if the title is undefined / not
                 supported then MessageDescriptions.MessageTypes.UNKNOWN is returned.
        """
        if len(f3) < 3:
            # Cannot be a message title, too short, error
            return MessageTypes.UNKNOWN

        message_title = Utils.title_defined(f3[0:3])
        if message_title is None:
            # Title is not supported, error
            return MessageTypes.UNKNOWN

        if message_title.value > MessageTitles.SPL.value:
            return MessageTypes.OLDI

        return MessageTypes.ATS

    def get_message_description(self, flight_plan_record, message_title):
        # type: (FlightPlanRecord, MessageTitles) -> MessageDescription | None
        """This method gets the field list for a message based on its title, adjacent unit name and message
        type. The field list contains a list of ICAO fields that must be included in a message and is used
        by the field parsers to parse individual subfields. The field list is contained in an instance of the
        MessageDescription class.

        :param flight_plan_record: The Flight Plan Record containing the message to parse and into which all
               the parsed data is written; the name of an adjacent unit or DEFAULT if no name is defined
               for the message title being processed.
        :param message_title: The message title of the message being processed;
        :return: An instance of the MessageDescription class containing a list of all fields expected in a
                 given message or None if a suitable field list could not be found. The latter case should
                 never happen and most likely indicates an error in the configuration data.
        """
        md = self.FIM.get_message_content(flight_plan_record.get_message_type(),
                                          flight_plan_record.get_sender_adjacent_unit_name(), message_title)
        if md is None:
            # If we land here then data configuration is missing
            # for the combination Message Type -> Adjacent Unit -> Message Title
            # It is a data configuration error, we can add an error
            Utils.add_error(
                flight_plan_record,
                "Message Type: " + flight_plan_record.get_message_type().name +
                ", Adjacent Unit Name: " + flight_plan_record.get_sender_adjacent_unit_name().name +
                ", Message Title: " + message_title.name +
                ". Default configuration will be used.",
                0, 0, self.EM, ErrorId.SYSTEM_CONFIG_UNDEFINED)
            # Let's check if we can proceed with the default adjacent unit before we give up
            md = self.FIM.get_message_content(flight_plan_record.get_message_type(),
                                              AdjacentUnits.DEFAULT, message_title)
            if md is None:
                # Shit out of luck, cannot proceed
                Utils.add_error(
                    flight_plan_record,
                    "Message Type: " + flight_plan_record.get_message_type().name +
                    ", Adjacent Unit Name: " + AdjacentUnits.DEFAULT.name +
                    ", Message Title: " + message_title.name +
                    ". No default configuration available, message cannot be processed.",
                    0, 0, self.EM, ErrorId.SYSTEM_CONFIG_UNDEFINED)
            else:
                # We have a default definition, proceed with this
                flight_plan_record.set_sender_adjacent_unit_name(AdjacentUnits.DEFAULT)
                return md
            return None

        return md

    def is_message_valid(self, flight_plan_record, message):
        # type: (FlightPlanRecord, str) -> bool
        """This method carries out some rudimentary checks for:
            - A 'null' message
            - An empty message
            - A short message (less than MINIMUM_HEADER_LENGTH characters is treated as an erroneous case)
        Any of the erroneous cases result in an error being written to the Flight Plan Record.

        :param flight_plan_record: A flight plan record into which errors are written;
        :param message: The message being parsed;
        :return: False if errors are detected, True otherwise;
        """
        # Do some very basic checks to make sure we have a valid message
        if message is None:
            # Null message value
            flight_plan_record.add_erroneous_field(
                "Null Field", self.EM.get_error_message(ErrorId.MSG_EMPTY), 0, 0)
            flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
            return False
        if len(message) < 1:
            # Is an empty string
            Utils.add_error(flight_plan_record, message, 0, 0, self.EM, ErrorId.MSG_EMPTY)
            flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
            return False
        if len(message) < self.MINIMUM_BODY_LENGTH:
            # Is way too short
            Utils.add_error(flight_plan_record, message, 0, len(message), self.EM, ErrorId.MSG_TOO_SHORT)
            flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
            return False

        return True

    # TODO Eventually a separate ADEXP parser will be added, for now this format is not supported
    def parse_adexp(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        # Currently ADEXP messages are not supported, we report an error
        Utils.add_error(flight_plan_record, "ADEXP Not Supported", 0, 0, self.EM, ErrorId.MSG_ADEXP_NOT_SUPPORTED)
        return False

    def parse_ats(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """Parses an ICAO ATS message; when this method is called the following is known:
            - The message type is ICAO ATS (MessageTypes.ATS);
            - The message title is valid but the MessageTitle enumeration must be obtained;
            - As it's an ATS message, there is no adjacent unit identifier needed;
        To obtain the appropriate field list for the message title the following are needed:
            - MessageTypes.ATS enumeration: Recover from the flight plan record;
            - MessageTitles.<Title enumeration>: This method will get this from the message title;
            - AdjacentUnit.DEFAULT: The default adjacent unit definition is used as there is no adjacent
              unit for ATS messages;

        :param flight_plan_record: The Flight Plan Record containing the message to parse;
        :return: True if a supported message title could be identified, False if any errors were detected.
        """
        # Tokenize the message, open & closed brackets will be removed
        tokens = self.tokenize_message(flight_plan_record, "()-\r\n\t")

        # Get the message title enumeration
        message_title = Utils.title_defined(
            tokens.get_first_token().get_token_string().replace(" ", "")[0:3])

        return self.parse_ats_or_oldi(flight_plan_record, tokens, message_title)

    def parse_oldi(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This class parses an OLDI message. The difference between an ATS and OLDI message is that
        the field list, i.e. the content of a given message based on its title, varies depending on the
        adjacent unit that a message is being exchanged on.

        This method calls the F3 parser which establishes the adjacent unit from F3b and sets this in
        the FPR. The 'standard' ATS parser is then called which uses the adjacent unit to obtain the
        correct field content definition.

        :param flight_plan_record: The Flight Plan Record containing the message to parse;
        :return: True if no errors were detected, False otherwise;
        """
        # Tokenize the message, open & closed brackets will be removed
        tokens = self.tokenize_message(flight_plan_record, "()-\r\n\t")

        # Get the message title enumeration
        message_title = Utils.title_defined(
            tokens.get_first_token().get_token_string().replace(" ", "")[0:3])

        # For OLDI messages we need to establish the adjacent unit sender name
        # To do this we must assume that the first token is F3a and at least F3b.
        # F3b contains the sender unit name. If we parse F3 it will set the
        # adjacent unit name into the FPR so that the appropriate field list can be
        # obtained for the OLDI title/unit.
        # Set F3 to the FPR
        flight_plan_record.add_icao_field(FieldIdentifiers.F3,
                                          tokens.get_first_token().get_token_string(),
                                          tokens.get_first_token().get_token_start_index(),
                                          tokens.get_first_token().get_token_end_index())
        # Parse F3, this will assign the adjacent unit name to the FPR
        ParseF3(flight_plan_record, self.SFIF, self.SFD).parse_field()

        return self.parse_ats_or_oldi(flight_plan_record, tokens, message_title)

    def parse_ats_header(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method parses an ATS header and saves the fields to the FPR. The header parsing assumes
        correct message semantics, that is the fields are expected in the following order:
            - <Priority Indicator>
            - <One or more Addressees>
            - <Filing Time> <Originator>
            - <One or more Additional Addressees>
        The header is tokenized and the appropriate parser called on the fields in the expected order.
        If fields are missing and/or extra, an error is reported as are any syntax errors.

        :param flight_plan_record: Flight plan record containing the header field and where successfully
               parsed fields will be written to.
        :return: True if parsing was successful, false if errors are detected.
        """
        # Tokenize the header
        tokenize = Tokenize()
        tokenize.set_string_to_tokenize(flight_plan_record.get_message_header())
        tokenize.set_whitespace(" \n\t\r")
        tokenize.tokenize()
        tokens: Tokens = tokenize.get_tokens()

        # Return if there is nothing in the header
        if tokens.get_number_of_tokens() < 1:
            return True

        # Some kind of header is present and ready for parsing, create empty fields in the FPR
        flight_plan_record.add_icao_field(FieldIdentifiers.PRIORITY_INDICATOR, "", 0, 0)
        flight_plan_record.add_icao_field(FieldIdentifiers.ADDRESS, "", 0, 0)
        flight_plan_record.add_icao_field(FieldIdentifiers.FILING_TIME, "", 0, 0)
        flight_plan_record.add_icao_field(FieldIdentifiers.ORIGINATOR, "", 0, 0)
        flight_plan_record.add_icao_field(FieldIdentifiers.ADADDRESS, "", 0, 0)

        # The following is used to indicate the 'state' of processing:
        # 0 -> Next expected header field is the Priority Indicator
        # 1 -> Next expected header field is an addressee field
        # 2 -> Next expected header field is the Originator
        # 3 -> Next expected header field is an additional addressee
        next_field: int = 0
        additional_addressee_available = False
        # Loop over the header fields
        for token in tokens.get_tokens():
            if next_field == 0:  # Process priority indicator

                # Save the Priority Indicator
                flight_plan_record.add_icao_field(FieldIdentifiers.PRIORITY_INDICATOR,
                                                  token.get_token_string(),
                                                  token.get_token_start_index(),
                                                  token.get_token_end_index())

                # Set up a new token for the addressee field(s)
                flight_plan_record.add_icao_field(
                    FieldIdentifiers.ADDRESS,
                    flight_plan_record.get_icao_field(FieldIdentifiers.ADDRESS).get_field_text(),
                    token.get_token_end_index() + 1,
                    token.get_token_end_index() + 1)

                # Indicates the next field is an addressee
                next_field = 1

            elif next_field == 1:  # Process addressee
                if Utils.get_first_digit_index(token.get_token_string()) == 0:
                    # Have to assume a field starting with a digit is the filing time
                    # Save the Filing Time
                    flight_plan_record.add_icao_field(FieldIdentifiers.FILING_TIME,
                                                      token.get_token_string(),
                                                      token.get_token_start_index(),
                                                      token.get_token_end_index())

                    # Indicate next field to process is the originator
                    next_field = 2

                else:
                    # Concatenate the addressees
                    flight_plan_record.add_icao_field(
                        FieldIdentifiers.ADDRESS,
                        flight_plan_record.get_icao_field(
                            FieldIdentifiers.ADDRESS).get_field_text() + token.get_token_string() + " ",
                        flight_plan_record.get_icao_field(FieldIdentifiers.ADDRESS).get_start_index(),
                        token.get_token_end_index())

            elif next_field == 2:  # Process the originator

                # Save the Originator
                flight_plan_record.add_icao_field(FieldIdentifiers.ORIGINATOR,
                                                  token.get_token_string(),
                                                  token.get_token_start_index(),
                                                  token.get_token_end_index())

                # Set up a new token for the additional addressee field(s)
                flight_plan_record.add_icao_field(
                    FieldIdentifiers.ADADDRESS,
                    flight_plan_record.get_icao_field(FieldIdentifiers.ADADDRESS).get_field_text(),
                    token.get_token_end_index() + 1,
                    token.get_token_end_index() + 1)

                next_field = 3

            elif next_field == 3:  # Process additional addressees

                # Concatenate the additional addressees
                flight_plan_record.add_icao_field(
                    FieldIdentifiers.ADADDRESS,
                    flight_plan_record.get_icao_field(
                        FieldIdentifiers.ADADDRESS).get_field_text() + token.get_token_string() + " ",
                    flight_plan_record.get_icao_field(FieldIdentifiers.ADADDRESS).get_start_index(),
                    token.get_token_end_index())
                additional_addressee_available = True

        ParsePriorityIndicator(flight_plan_record, self.SFIF, self.SFD).parse_field()
        ParseAddressee(flight_plan_record, self.SFIF, self.SFD).parse_field()
        ParseFilingTime(flight_plan_record, self.SFIF, self.SFD).parse_field()
        ParseOriginator(flight_plan_record, self.SFIF, self.SFD).parse_field()
        if additional_addressee_available:
            ParseAdditionalAddressee(flight_plan_record, self.SFIF, self.SFD).parse_field()

        return flight_plan_record.errors_detected()

    def parse_ats_or_oldi(self, flight_plan_record, tokens, message_title):
        # type: (FlightPlanRecord, Tokens, MessageTitles) -> bool
        """This method parses the message fields. The field definition list is obtained based on the
        message type, adjacent unit name and message title. The field definition list contains
        information about all the subfields in each field and is used to parse individual subfields.

        The individual parser methods are implemented as callbacks and stored with the field definition
        list. Each parser callback adds the fields and subfields to the FPR. Once this method completes,
        The FPR is fully populated with the message field and subfield content.

        :param flight_plan_record: The Flight Plan Record containing the message to parse and into
               which all the parsed data is written;
        :param tokens: The tokens containing individual ICAO fields;
        :param message_title: The message title;
        :return: True if the message was parsed without error, False if any errors were detected.
        """
        # Obtain the field list definition for this message title
        md: MessageDescription = self.get_message_description(flight_plan_record, message_title)

        # Check that a valid field list is defined
        if md is None:
            return False

        # Get the list of field parsers defined for this message
        field_parsers: [ParseFieldsCommon] = md.get_field_parsers()

        # Get the list of field identifiers defining fields included in this message
        field_identifiers: [FieldIdentifiers] = md.get_message_fields()

        # Loop over the fields in the list of tokens, (these are the fields to
        # be parsed), by calling a parse method defined for each field.
        # The list of fields to parse and the list of fields defined
        # for this messages should be the same size, but if a field is missing or
        # there are additional fields, then the lists will not match. The 'smallest'
        # list is used to control the loop and avoid accessing invalid list entries;
        # if the lists differ in size an error is reported.
        idx = 0
        if tokens.get_number_of_tokens() < md.get_number_of_fields_in_message():
            # There are fewer fields to parse than fields defined for this message
            for token in tokens.get_tokens():
                # Save the field to be parsed to the flight plan
                flight_plan_record.add_icao_field(
                    field_identifiers[idx],
                    token.get_token_string(),
                    token.get_token_start_index() + len(flight_plan_record.get_message_header()),
                    token.get_token_end_index() + len(flight_plan_record.get_message_header()))
                # Get the appropriate field parser
                fp = field_parsers[idx](flight_plan_record, self.SFIF, self.SFD)
                # Parse the field
                fp.parse_field()
                idx += 1

            # Check if fewer fields to parse is allowed, some messages have optional fields
            difference = md.get_number_of_fields_in_message() - tokens.get_number_of_tokens()
            if message_title == MessageTitles.FPL and difference == 1:
                # This title has an optional field 19, we only report an error if more
                # than one field is missing
                return flight_plan_record.errors_detected()
            Utils.add_error(flight_plan_record, str(md.get_number_of_fields_in_message()),
                            tokens.get_first_token().get_token_start_index() +
                            len(flight_plan_record.get_message_header()),
                            tokens.get_last_token().get_token_end_index() +
                            len(flight_plan_record.get_message_header()), self.EM,
                            ErrorId.MSG_TOO_FEW_FIELDS)
        else:
            # Either the fields to parse are equal to those defined, or we have more
            # fields in the message than defined for the message.
            # One special case exists for the CHG and ACH message, these messages
            # have F22 as the last field that uses hyphens as field separators. For
            # these messages, the F22 fields need to be concatenated into a single field.
            # Check if the last field specified for this message is F22
            f22_index = len(field_identifiers) - 1
            if field_identifiers[f22_index] == FieldIdentifiers.F22 or \
                    field_identifiers[f22_index] == FieldIdentifiers.F22_SPECIFIC:
                # The last field in the list of field_identifiers is F22, so this gives
                # us the index into the token list where F22 starts, all tokens including
                # this one up to the end of the token list are all F22 fields.

                # Get the start index of field 22 in the original message
                f22_start_index = tokens.get_token_at(f22_index).get_token_start_index()

                # Get the end index of field 22 in the original message
                f22_end_index = tokens.get_token_at(len(tokens.get_tokens()) - 1).get_token_end_index()

                # Retrieve the F22 string from the original message
                f22_concatenated = flight_plan_record.get_message_body()[f22_start_index - 1:f22_end_index]

                # Save the field 22 string to the field 22 token along with its start and end index
                tokens.get_token_at(f22_index).set_token_string(f22_concatenated)
                tokens.get_token_at(f22_index).set_token_start_index(f22_start_index)
                tokens.get_token_at(f22_index).set_token_end_index(f22_end_index)

                # Lop off the remainder of the list
                tokens.remove_tokens_from_end_of_list(f22_index)

            for field_parser in field_parsers:
                # Save the field to be parsed to the flight plan
                flight_plan_record.add_icao_field(
                    field_identifiers[idx],
                    tokens.get_token_at(idx).get_token_string(),
                    tokens.get_token_at(idx).get_token_start_index() + len(flight_plan_record.get_message_header()),
                    tokens.get_token_at(idx).get_token_end_index() + len(flight_plan_record.get_message_header()))
                # Get the appropriate field parser
                fp = field_parser(flight_plan_record, self.SFIF, self.SFD)
                # Parse the field
                fp.parse_field()
                idx += 1

            # Check if we have more fields to parse than defined for this message
            if tokens.get_number_of_tokens() > md.get_number_of_fields_in_message():
                Utils.add_error(flight_plan_record, tokens.get_token_at(idx).get_token_string(),
                                tokens.get_token_at(idx).get_token_start_index(),
                                tokens.get_token_at(idx).get_token_end_index(), self.EM,
                                ErrorId.MSG_TOO_MANY_FIELDS)

        return flight_plan_record.errors_detected()

    def parse_message(self, flight_plan_record, message):
        # type: (FlightPlanRecord, str | None) -> bool
        """This method is the entry point for message parsing; the method takes an instance of FlightPlanRecord
        (for output) and a string containing the message to parse. The FlightPlanRecord is populated by the
        parser and includes all extracted fields, (if field 15 was present) is stored along with any route
        extraction any errors. It is a callers responsibility to retrieve the errors.

        :param flight_plan_record: A flight plan record into which all data extracted by the parser
               (including errors) are written;
        :param message: The message with or without header;
        :return: False if errors are detected, True otherwise;
        """
        # Check if the message is worthy of further processing
        if not self.is_message_valid(flight_plan_record, message):
            return False

        # Save the complete message to the FPR
        flight_plan_record.set_message_complete(message)

        # Split and save the message header and body
        self.set_message_body_and_header(flight_plan_record)

        # Go into more detail and establish the message type;
        # (ICAO ATS, OLDI or ADEXP). The message type is stored in the FPR.
        if not self.set_message_type(flight_plan_record):
            return False

        # Call the appropriate parser
        match flight_plan_record.get_message_type():
            case MessageTypes.ADEXP:
                self.parse_ats_header(flight_plan_record)
                return self.parse_adexp(flight_plan_record)
            case MessageTypes.ATS:
                self.parse_ats_header(flight_plan_record)
                self.parse_ats(flight_plan_record)
            case MessageTypes.OLDI:
                self.parse_oldi_header(flight_plan_record)
                self.parse_oldi(flight_plan_record)
            case MessageTypes.UNKNOWN:
                return False

        # Call the consistency checking routines
        self.consistency_check(flight_plan_record)

        # Correct the Extracted route start and end indices to reference them against the message as a whole
        self.correct_ers_indices(flight_plan_record)

        return not (flight_plan_record.errors_detected() or len(flight_plan_record.get_erroneous_fields()))

    # TODO This method may be removed if there are no application level headers, (I don't believe there are)
    @staticmethod
    def parse_oldi_header(flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        if flight_plan_record.get_message_body() == "":
            return True
        return True

    def set_message_body_and_header(self, flight_plan_record):
        # type: (FlightPlanRecord) -> None
        """This method determines if a message contains a header and message body or if it's a message
        without a header. The message header and body are copied to the FPR if they are present.

        Differentiating between the message header and body is achieved by detecting the presence or not
        of the first hyphen or open bracket in a message. The action taken is as per the following truth table:
                   Open     Hyphen '-'
         Hyphen | Bracket |  Before |
        Present | Present | Bracket | Action
        --------+---------+---------+--------------------------------------------
           No   |    No   |    x    | Save to message body + Process, no header
        --------+---------+---------+--------------------------------------------
           No   |   Yes   |    x    | Split on Bracket, save to body and header + Process
        --------+---------+---------+--------------------------------------------
          Yes   |    No   |    x    | Split on Hyphen, save to body and header + Process
        --------+---------+---------+--------------------------------------------
          Yes   |   Yes   |   No    | Split on Bracket, save to body and header + Process
        --------+---------+---------+--------------------------------------------
          Yes   |   Yes   |  Yes    | Split on Hyphen, save to body and header + Process
        --------+---------+---------+--------------------------------------------

        :param flight_plan_record: The Flight Plan Record containing the message to parse;
        :return: True if the message header and body have been identified and stored, False if
                 any errors were detected.
        """
        msg = flight_plan_record.get_message_complete()

        # Get the indices of the two characters that could indicate the start
        # of the message body.
        hyphen_index = msg.find("-", 0, len(msg))
        open_b_index = msg.find("(", 0, len(msg))

        # Take action as described in the table for this methods' documentation.
        if hyphen_index < 0 and open_b_index < 0:
            # Hyphen and Bracket Missing
            # A LAM has no hyphen, and if a message was submitted without a bracket, then...
            # Row 1 of the table in the comments
            flight_plan_record.set_message_header("")
            flight_plan_record.set_message_body(msg)
        elif (hyphen_index < 0 and open_b_index > -1) or \
                ((hyphen_index > -1 and open_b_index > -1) and open_b_index < hyphen_index):
            # (Hyphen missing, open bracket present) or
            # ((Hyphen and bracket present) and Bracket before Hyphen)
            # Rows 2 & 4 of the table in the comments
            # Split on bracket
            if open_b_index < self.MINIMUM_HEADER_LENGTH:
                flight_plan_record.set_message_header("")
                flight_plan_record.set_message_body(msg)
            else:
                flight_plan_record.set_message_header(msg[0:open_b_index])
                flight_plan_record.set_message_body(msg[open_b_index:])
        else:
            # (Hyphen present, open bracket missing) or
            # ((Hyphen and bracket present) and Hyphen before Bracket)
            # Rows 3 & 5 of the table in the comments
            # Split on hyphen
            if hyphen_index < self.MINIMUM_HEADER_LENGTH:
                # Safe to assume there is no header
                flight_plan_record.set_message_header("")
                flight_plan_record.set_message_body(msg)
            else:
                flight_plan_record.set_message_header(msg[0:hyphen_index])
                flight_plan_record.set_message_body(msg[hyphen_index:])

    def set_message_type(self, flight_plan_record):
        # type: (FlightPlanRecord) -> bool
        """This method sets the message type (ICAO ATS, OLDI or ADEXP) to the FPR. When this method
        is called, the FPR contains a message body and maybe a header (if the message included a header).
        This method recovers the message title from the start of the message body, and checks if it is a
        supported message title. Using the title, the message type can be ascertained and set with one
        of the enumeration values from the MessageDescriptions.MessageTypes class.

        :param flight_plan_record: The Flight Plan Record containing the message to parse;
        :return: True if a supported message title could be identified. False if any errors were detected.
        """
        msg_body = flight_plan_record.get_message_body()
        msg_header = flight_plan_record.get_message_header()

        # If we can find the '-TITLE' in some shape or form at the start
        # of the field, we must have an ADEXP message.
        # Regexp is for e.g '   -   TITLE' -> whitespace irrelevant
        if re.match("[ \n\r\t]*-[ \n\r\t]*TITLE", msg_body) is not None:
            # We have an ADEXP message
            Utils.add_error(flight_plan_record, "", 0, 0, self.EM, ErrorId.MSG_ADEXP_NOT_SUPPORTED)
            flight_plan_record.set_message_type(MessageTypes.ADEXP)
            return False

        # Try and locate an ATS message title, first attempt with a bracket
        # Regexp is for e.g '   (   FPL' Bracket is optional, whitespace irrelevant
        f3 = re.match("[ \n\r\t]*[(]?[ \n\r\t]*[A-Z]{3}", msg_body)
        if f3 is None:
            # Message title not recognised, error, grab the first three characters
            m = re.match(".{3}", msg_body)
            Utils.add_error(flight_plan_record, m.group(0),
                            len(msg_header) + m.span()[1] - 3,
                            len(msg_header) + m.span()[1], self.EM, ErrorId.F3_TITLE_SYNTAX)
            flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
            return False

        # Store the indices for future error reporting.
        end_index = len(msg_header) + f3.span()[1]
        start_index = end_index - 3

        # We have a possible ATS message, extract the message title
        f3 = re.findall("[A-Z]{3}", f3.group(0))
        if f3 is not None:
            # Try and figure out the message type
            message_type = self.determine_message_type(f3[0])
            if message_type is MessageTypes.UNKNOWN:
                # Unrecognised message title
                Utils.add_error(flight_plan_record, f3[0], start_index, end_index + 3,
                                self.EM, ErrorId.F3_TITLE_SYNTAX)
                flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
                return False
            else:
                # Title recognized
                # One more check to do, some message titles are the same for
                # OLDI and ATS messages. OLDI messages always include F3b & F3c.
                # Regexp is for e.g '   (   ACPAA/BB001' Bracket is optional, whitespace irrelevant
                mm = re.match("[ \n\r\t]*[(]?[ \n\r\t]*[A-Z]{3,7}/[A-Z]{1,4}[0-9]{1,3}", msg_body)
                message_title = Utils.title_defined(f3[0])
                if (message_title is MessageTitles.ACP or message_title is MessageTitles.CDN or
                        message_title is MessageTitles.CPL) and mm is not None:
                    flight_plan_record.set_message_type(MessageTypes.OLDI)
                else:
                    flight_plan_record.set_message_type(message_type)
                return True
        else:
            # This should never ever happen
            Utils.add_error(flight_plan_record, "Regexp went wrong", 0, 0, self.EM, ErrorId.F3_TITLE_SYNTAX)
            flight_plan_record.set_message_type(MessageTypes.UNKNOWN)
            return False

    @staticmethod
    def tokenize_message(flight_plan_record, whitespace):
        # type: (FlightPlanRecord, str) -> Tokens
        """This method tokenizes a field or message based on the token separators in the parameter
        'whitespace'.

        :param flight_plan_record: The Flight Plan Record containing the message to parse;
        :param whitespace: The whitespace characters used to delimit the tokens, these are all consumed by
               the parser apart from the forward slash character '/' which results in its own token.
        :return: The list of tokens;
        """
        tokenizer = Tokenize()
        tokenizer.set_string_to_tokenize(flight_plan_record.get_message_body())
        tokenizer.set_whitespace(whitespace)
        tokenizer.tokenize()
        return tokenizer.get_tokens()
