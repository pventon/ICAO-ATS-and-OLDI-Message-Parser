import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF17 import ParseF17
from Tokenizer.Token import Token


class TestParseF17(unittest.TestCase):

    def test_parse_field17(self):
        # Field empty
        self.do_f17_test(True, 1, "", ["There is no data in field 17"])

        # Field empty with spaces
        self.do_f17_test(True, 1, "    ", ["There is no data in field 17"])

        # Part of ADES location indicator
        self.do_f17_test(True, 1, "EGL", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGL'"])

        # Correct ADES, ATA incorrect
        self.do_f17_test(True, 1, "EGLL080", ["Expecting ATA in HHMM instead of '080'"])

        # Correct ADES, ATA, incorrect alternate
        self.do_f17_test(False, 0, "EGLL0100 E5SS", [
            "Expecting alternate aerodrome as an ICAO location indicator instead of 'E5SS'"])

        # All correct
        self.do_f17_test(False, 0, "EGLL0100 EGSS", ["Too many fields in Field 16, remove 'EGFF'"])

        # Free text after correct F!&a and b
        self.do_f17_test(False, 0, "EGLL0100 THIS IS FREE TEXT", [
            "Too many fields in Field 16, remove 'EGBB EGFF KKJJ'"])

        # Error in ATA
        self.do_f17_test(True, 1, "EGLL0360 ", [
            "Expecting ATA in HHMM instead of '0360'"])

        # error in ADES
        self.do_f17_test(True, 1, "E@LL2359 EGSS", [
            "Expecting arrival aerodrome as an ICAO location indicator, "
            "e.g. EGLL instead of 'E@LL'"])

        # F16a and b too long
        self.do_f17_test(True, 1, "EGLL00320 EGSS", ["Expecting ATA in HHMM instead of '00320'"])

        # Random faults
        self.do_f17_test(True, 1, "   EGLL0360 / EGSS EGBB", ["Expecting ATA in HHMM instead of '0360'"])

        # Random faults
        self.do_f17_test(True, 1, "   EGLL2400    EGSS    EGBB           EGFF    ",
                         ["Expecting ATA in HHMM instead of '2400'"])

        # Random faults
        self.do_f17_test(True, 1, "EGLL2401 EGSSF ", ["Expecting ATA in HHMM instead of '2401'"])

        # Extra character after ATA before optional fields
        self.do_f17_test(True, 1, "EGLL23591", ["Expecting ATA in HHMM instead of '23591'"])

        # Illegal characters in the free text
        self.do_f17_test(True, 8, "EGLL2359 These tests have been written by Peter Venton", [
            "Invalid characters for alternate aerodrome text, should "
            "be 'A' to 'Z' and '0' to '9' only instead of 'These'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'tests'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'have'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'been'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'written'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'by'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'Peter'",
            "Invalid characters for alternate aerodrome text, should be 'A' to "
            "'Z' and '0' to '9' only instead of 'Venton'"])

        # Correct ADES, ATA
        self.do_f17_test(False, 0, "EGLL0900", [""])

    def do_f17_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F17, string_to_parse, 0, len(string_to_parse))
        pf17 = ParseF17(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf17.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
