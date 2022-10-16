import unittest

from Configuration.EnumerationConstants import MessageTypes
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class ParseMessageTests(unittest.TestCase):
    fpr: FlightPlanRecord = None
    pm = None

    def tearDown(self) -> None:
        # self.fpr = None
        self.pm = None

    def setUp(self) -> None:
        self.fpr = FlightPlanRecord()
        self.pm = ParseMessage()

    def test_ParseMessage_01(self):
        # Null message, error
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, None, "", "", ["Message is empty"])

    def test_ParseMessage_02(self):
        # Empty message, error
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "", "", "", ["Message is empty"])

    def test_ParseMessage_03(self):
        # Message too short, error
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "123456789", "", "",
                                 ["Message is too short and cannot be considered for processing"])

    def test_ParseMessage_04(self):
        # Hyphen missing, error
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "1234567890123456789012345", "",
                                 "1234567890123456789012345",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_05(self):
        # Hyphen present, TITLE present, no open bracket -> ADEXP message
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "12345-  TITLE FPL -ADEP LOWL", "",
                                 "12345-  TITLE FPL -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_06(self):
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "12345-  TITLE67890 ARR -ADEP LOWL", "",
                                 "12345-  TITLE67890 ARR -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"]),

    def test_ParseMessage_07(self):
        self.do_header_body_test(True, 1, MessageTypes.ADEXP, "    -  TITLE67890 ARR -ADEP LOWL", "",
                                 "    -  TITLE67890 ARR -ADEP LOWL",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_08(self):
        self.do_header_body_test(True, 1, MessageTypes.ADEXP, "-  TITLE67890 ARR -ADEP LOWL", "",
                                 "-  TITLE67890 ARR -ADEP LOWL",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_09(self):
        self.do_header_body_test(True, 1, MessageTypes.ADEXP, "-TITLE67890 ARR -ADEP LOWL", "",
                                 "-TITLE67890 ARR -ADEP LOWL",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_10(self):
        # Hyphen present, TITLE missing, no open bracket, error
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "12345- ITLE67890 ARR -ADEP LOWL", "",
                                 "12345- ITLE67890 ARR -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_11(self):
        # Hyphen present, open bracket present, hyphen before bracket,
        # TITLE present -> ADEXP
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "12345-TITLE67(890 ARR -ADEP LOWL", "",
                                 "12345-TITLE67(890 ARR -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_12(self):
        self.do_header_body_test(True, 1, MessageTypes.ADEXP,
                                 "THIS HEADER IS LONG ENOUGH FOR A HEADER 12345-TITLE67(890",
                                 "THIS HEADER IS LONG ENOUGH FOR A HEADER 12345",
                                 "-TITLE67(890",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_13(self):
        # Hyphen present, open bracket present, hyphen before bracket,
        # TITLE missing -> UNKNOWN
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "12345-ITLE67(890 ARR -ADEP LOWL", "",
                                 "12345-ITLE67(890 ARR -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_14(self):
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN,
                                 "THIS HEADER IS LONG ENOUGH FOR A HEADER 12345-ITLE67(890",
                                 "THIS HEADER IS LONG ENOUGH FOR A HEADER 12345",
                                 "-ITLE67(890",
                                 ["Message title '-IT' unrecognized, cannot process this message"])

    def test_ParseMessage_15(self):
        # Hyphen present, open bracket present, Bracket before hyphen -> ATS
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN, "1234(5-ITLE67(890 ARR -ADEP LOWL", "",
                                 "1234(5-ITLE67(890 ARR -ADEP LOWL",
                                 ["Message title '123' unrecognized, cannot process this message"])

    def test_ParseMessage_16(self):
        # ADEXP message, check message header and body
        self.do_header_body_test(True, 1, MessageTypes.ADEXP, "HEADER HEADER HEADER VVVV-TITLE MESSAGE BODY",
                                 "HEADER HEADER HEADER VVVV",
                                 "-TITLE MESSAGE BODY",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_17(self):
        # ADEXP message, no header, check message header and body
        self.do_header_body_test(True, 1, MessageTypes.ADEXP, "-TITLE MESSAGE BODY ARR -ADEP LOWL", ""
                                                                                                    "",
                                 "-TITLE MESSAGE BODY ARR -ADEP LOWL",
                                 ["Looks like an ADEXP message, currently not supported"])

    def test_ParseMessage_18(self):
        # ATS message, with header, check message header and body
        self.do_header_body_test(True, 3, MessageTypes.ATS,
                                 "HEADER1 HEADER2 HEADER3 (FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)",
                                 "HEADER1 HEADER2 HEADER3 ",
                                 "(FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)",
                                 ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'HEADER1'",
                                  "The message filing time is missing, should contain DTG as DDHHMM",
                                  "The message originator is missing, 8 character or 7 character / "
                                  "digit ATC facility address",
                                  "More subfields expected after 'HEADER2 HEADER3'"])

    def test_ParseMessage_19(self):
        # ATS message, no header, check message header and body
        self.do_header_body_test(False, 0, MessageTypes.ATS,
                                 "(FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)", "",
                                 "(FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)",
                                 [""])

    def test_ParseMessage_20(self):
        # ATS message, no header, no open bracket, check message header and body
        self.do_header_body_test(False, 0, MessageTypes.ATS,
                                 "FPL - TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0))", "",
                                 "FPL - TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0))", [""])

    def test_ParseMessage_21(self):
        # OLDI message, no header, no open bracket, check message header and body
        self.do_header_body_test(False, 0, MessageTypes.OLDI, "PAC - TEST01-EGLL-LOWL-9/B737/M", "",
                                 "PAC - TEST01-EGLL-LOWL-9/B737/M", [""])

    def test_ParseMessage_22(self):
        self.do_header_body_test(False, 0, MessageTypes.OLDI, "     PAC - TEST01-EGLL-LOWL-9/B737/M", "",
                                 "     PAC - TEST01-EGLL-LOWL-9/B737/M", [""])

    def test_ParseMessage_23(self):
        self.do_header_body_test(True, 1, MessageTypes.UNKNOWN,
                                 "THIS IS A MESSAGE HEADER PAC PAC -TEST01-IS-B737/M-S/C-LOWL1234",
                                 "THIS IS A MESSAGE HEADER PAC PAC ",
                                 "-TEST01-IS-B737/M-S/C-LOWL1234",
                                 ["Message title '-TE' unrecognized, cannot process this message"])

    def test_ParseMessage_24(self):
        # OLDI message, no header, with open bracket, check message header and body
        self.do_header_body_test(False, 0, MessageTypes.OLDI, "(PAC -TEST001-LOWW-EGLL-9/B737", "",
                                 "(PAC -TEST001-LOWW-EGLL-9/B737", [""])

    def test_ParseMessage_25(self):
        self.do_header_body_test(True, 1, MessageTypes.OLDI, "     LAML/E012E/L001", "",
                                 "     LAML/E012E/L001",
                                 ["Message content undefined for Message Type/Adjacent Unit/"
                                  "Title combination Message Type: OLDI, Adjacent Unit Name: L, "
                                  "Message Title: LAM. Default configuration will be used."])

    def test_ParseMessage_26(self):
        self.do_header_body_test(False, 0, MessageTypes.OLDI,
                                 "THIS IS A MESSAGE HEADER (PAC -TEST001-LOWW-EGLL-9/B737",
                                 "THIS IS A MESSAGE HEADER ", "(PAC -TEST001-LOWW-EGLL-9/B737", [""])

    def test_ParseMessage_27(self):
        # These test check message titles that have both an OLDI and ATS definition.
        # The difference is decided on the presence or not of field F3b and F3c.
        self.do_header_body_test(False, 0, MessageTypes.ATS, "(ACP -TEST02-LOWL0100-LOWW0200)", "",
                                 "(ACP -TEST02-LOWL0100-LOWW0200)", [""])

    def test_ParseMessage_28(self):
        self.do_header_body_test(False, 0, MessageTypes.OLDI,
                                 "(ACPAA/L001 -TEST02-LOWL-LOWW-18/DOF/221021", "",
                                 "(ACPAA/L001 -TEST02-LOWL-LOWW-18/DOF/221021", [""])

    def test_ParseMessage_29(self):
        self.do_header_body_test(True, 4, MessageTypes.ATS,
                                 "THIS IS SOME HEADER STUFF (CDN -TEST01-LOWL0100-LOWW0200-121212)",
                                 "THIS IS SOME HEADER STUFF ", "(CDN -TEST01-LOWL0100-LOWW0200-121212)",
                                 ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'THIS'",
                                  "Expecting 8 character or 7 character / digit ATC facility address instead of 'IS'",
                                  "The message filing time is missing, should contain DTG as DDHHMM",
                                  "The message originator is missing, 8 character or 7 character / "
                                  "digit ATC facility address"])

    def test_ParseMessage_30(self):
        self.do_header_body_test(False, 0, MessageTypes.OLDI,
                                 "THIS IS SOME HEADER STUFF (CPLE/L001 -TEST01-LOWL0800-LOWW0200-221212-9/B737/M)",
                                 "THIS IS SOME HEADER STUFF ",
                                 "(CPLE/L001 -TEST01-LOWL0800-LOWW0200-221212-9/B737/M)", [""])

    def test_ParseMessage00(self):
        # ATS message, with header, check message header and body
        self.do_header_body_test(False, 0, MessageTypes.ATS,
                                 "FF ABCDEFGH HEADER1 312015 IJKLMNOP "
                                 "(FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)",
                                 "FF ABCDEFGH HEADER1 312015 IJKLMNOP ",
                                 "(FPL-TEST01-IS-B737/M-S/C-LOWL1234-N0450F350 GGG-LOWW0200-0)",
                                 ["More subfields expected after 'ABCDEFGH HEADER1'"])

    def do_header_body_test(self, errors_detected, number_errors_detected, expected_message_type,
                            message_to_parse, expected_header, expected_body, expected_errors):
        # type: (bool, int, MessageTypes, str | None, str, str, [str]) -> None

        self.pm.parse_message(self.fpr, message_to_parse)
        self.assertEqual(expected_message_type, self.fpr.get_message_type())
        self.assertEqual(expected_header, self.fpr.get_message_header())
        self.assertEqual(expected_body, self.fpr.get_message_body())
        self.assertEqual(errors_detected, self.fpr.errors_detected())
        self.assertEqual(number_errors_detected, len(self.fpr.get_erroneous_fields()))
        if self.fpr.errors_detected():
            errors = self.fpr.get_erroneous_fields()
            for idx in range(0, len(errors)):
                self.assertEqual(expected_errors[idx], self.fpr.get_erroneous_fields()[idx].get_error_message())


if __name__ == '__main__':
    unittest.main()
