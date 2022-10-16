import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF13a import ParseF13a
from Tokenizer.Token import Token


class TestParseF13a(unittest.TestCase):

    def test_parse_field13a(self):
        # Field empty
        self.do_f13a_test(True, 1, "", ["There is no data in field 13"])

        # Field empty with spaces
        self.do_f13a_test(True, 1, "    ", ["There is no data in field 13"])

        # Part of ADEP location indicator
        self.do_f13a_test(True, 1, "EGL", ["Expecting departure aerodrome as an ICAO location indicator, "
                                           "e.g. EGLL instead of 'EGL'"])

        # Correct ADEP, EOBT incorrect
        self.do_f13a_test(True, 1, "EGLL080", ["Expecting departure aerodrome as an ICAO location indicator, "
                                               "e.g. EGLL instead of 'EGLL080'"])

        # All correct
        self.do_f13a_test(False, 0, "EGLL", [])

        # Too many fields
        self.do_f13a_test(True, 1, "EGLL EGSS EGBB EGFF KKJJ", ["Too many fields in Field 13, remove "
                                                                "'EGSS EGBB EGFF KKJJ'"])

        # error in ADEP
        self.do_f13a_test(True, 2, "E@LL EGSS", ["Expecting departure aerodrome as an ICAO location indicator, "
                                                 "e.g. EGLL instead of 'E@LL'",
                                                 "Too many fields in Field 13, remove 'EGSS'"])

        # F13a too long
        self.do_f13a_test(True, 1, "EGLL00320", ["Expecting departure aerodrome as an ICAO location indicator, "
                                                 "e.g. EGLL instead of 'EGLL00320'"])

        # Random faults
        self.do_f13a_test(True, 2, "   EGLL0360 / EGSS EGBB", ["Expecting departure aerodrome as an ICAO "
                                                               "location indicator, e.g. EGLL instead of 'EGLL0360'",
                                                               "Too many fields in Field 13, remove '/EGSS EGBB'"])

        # Random faults
        self.do_f13a_test(True, 1, "   EGLL   EGSS    EGBB           EGFF    ", [
            "Too many fields in Field 13, remove 'EGSS EGBB EGFF'"])

        # Random faults
        self.do_f13a_test(True, 2, "E7LL EGSSF ", ["Expecting departure aerodrome as an ICAO location "
                                                   "indicator, e.g. EGLL instead of 'E7LL'",
                                                   "Too many fields in Field 13, remove 'EGSSF'"])

        # Random faults
        self.do_f13a_test(True, 2, "8GLL EGSSF ", ["Expecting departure aerodrome as an ICAO location "
                                                   "indicator, e.g. EGLL instead of '8GLL'",
                                                   "Too many fields in Field 13, remove 'EGSSF'"])

        # Random faults
        self.do_f13a_test(True, 1, "EGLL EGSSF ", ["Too many fields in Field 13, remove 'EGSSF'"])

    def do_f13a_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F13a, string_to_parse, 0, len(string_to_parse))
        pf13a = ParseF13a(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf13a.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
