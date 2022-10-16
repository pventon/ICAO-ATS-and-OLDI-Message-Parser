import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF16 import ParseF16
from Tokenizer.Token import Token


class TestParseF16(unittest.TestCase):

    def test_parse_field16(self):
        # Field empty
        self.do_f16_test(True, 1, "", ["There is no data in field 16"])

        # Field empty with spaces
        self.do_f16_test(True, 1, "    ", ["There is no data in field 16"])

        # Part of ADEP location indicator
        self.do_f16_test(True, 1, "EGL", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGL'"])

        # Correct ADES, EET incorrect
        self.do_f16_test(True, 1, "EGLL080", ["Expecting EOBT in HHMM instead of '080'"])

        # Correct ADES, EET, 1st alternate and incorrect 2nd alternate
        self.do_f16_test(True, 1, "EGLL0100 EGSS EGBB EG", ["Too many fields in Field 16, remove 'EG'"])

        # All correct
        self.do_f16_test(True, 1, "EGLL0100 EGSS EGBB EGFF", ["Too many fields in Field 16, remove 'EGFF'"])

        # Too many fields
        self.do_f16_test(True, 1, "EGLL0100 EGSS EGBB EGFF KKJJ", ["Too many fields in Field 16, remove 'EGFF KKJJ'"])

        # Error in 2nd alternate
        self.do_f16_test(True, 2, "EGLL0100 EGSS EG6B EGGF", [
            "Expecting alternate aerodrome as an ICAO location indicator instead of 'EG6B'",
            "Too many fields in Field 16, remove 'EGGF'"])

        # Error in 1st alternate
        self.do_f16_test(True, 2, "EGLL0100 EGSS EG#B EGFF", [
            "Expecting alternate aerodrome as an ICAO location indicator instead of 'EG#B'",
            "Too many fields in Field 16, remove 'EGFF'"])

        # Error in EET
        self.do_f16_test(True, 2, "EGLL0360 EGSS EGBB EGFF", [
            "Expecting EOBT in HHMM instead of '0360'",
            "Too many fields in Field 16, remove 'EGFF'"])

        # error in ADES
        self.do_f16_test(True, 2, "E@LL2359 EGSS EGBB EGFF", [
            "Expecting arrival aerodrome as an ICAO location indicator, "
            "e.g. EGLL instead of 'E@LL'",
            "Too many fields in Field 16, remove 'EGFF'"])

        # F16a and b too long
        self.do_f16_test(True, 1, "EGLL00320 EGSS EGBB", ["Expecting EOBT in HHMM instead of '00320'"])

        # Random faults
        self.do_f16_test(True, 2, "   EGLL0360 / EGSS EGBB", ["Expecting EOBT in HHMM instead of '0360'",
                                                              "Too many fields in Field 16, remove 'EGBB'"])

        # Random faults
        self.do_f16_test(True, 2, "   EGLL2400    EGSS    EGBB           EGFF    ",
                         ["Expecting EOBT in HHMM instead of '2400'",
                          "Too many fields in Field 16, remove 'EGFF'"])

        # Random faults
        self.do_f16_test(True, 1, "EGLL2401 EGSSF ", ["Expecting EOBT in HHMM instead of '2401'"])

        # Extra character after EOBT before optional fields
        self.do_f16_test(True, 1, "EGLL23591", ["Expecting EOBT in HHMM instead of '23591'"])

        # Extra character after first optional field
        self.do_f16_test(True, 1, "EGLL2359 EGSSF ",
                         ["Expecting alternate aerodrome as an ICAO location indicator instead of 'EGSSF'"])

        # Extra character after second optional field
        self.do_f16_test(True, 1, "EGLL2359 EGSS ABCDF ",
                         ["Expecting alternate aerodrome as an ICAO location indicator instead of 'ABCDF'"])

        # Correct ADES, EET
        self.do_f16_test(False, 0, "EGLL0900", [""])

        # Correct ADES, EET and 1st alternate
        self.do_f16_test(False, 0, "EGLL0900 EGSS", [""])

        # Correct ADES, EET and both alternates
        self.do_f16_test(False, 0, "EGLL0900 EGSS EGLL", [""])

    def do_f16_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F16, string_to_parse, 0, len(string_to_parse))
        pf16 = ParseF16(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf16.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
