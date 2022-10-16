import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF13 import ParseF13
from Tokenizer.Token import Token


class TestParseF13(unittest.TestCase):

    def test_parse_field13(self):
        # Field empty
        self.do_f13_test(True, 1, "", ["There is no data in field 13"])

        # Field empty with spaces
        self.do_f13_test(True, 1, "    ", ["There is no data in field 13"])

        # Part of ADEP location indicator
        self.do_f13_test(True, 1, "EGL", ["Expecting departure aerodrome as an ICAO location indicator, "
                                          "e.g. EGLL instead of 'EGL'"])

        # Correct ADEP, EOBT incorrect
        self.do_f13_test(True, 1, "EGLL080", ["Expecting EOBT in HHMM instead of '080'"])

        # Correct ADEP, EOBT and extra field
        self.do_f13_test(True, 1, "EGLL0900 EGHS", ["Too many fields in Field 13, remove 'EGHS'"])

        # All correct
        self.do_f13_test(True, 1, "EGLL0100 EGSS", ["Too many fields in Field 13, remove 'EGSS'"])

        # Too many fields
        self.do_f13_test(True, 1, "EGLL0100 EGSS EGBB EGFF KKJJ", ["Too many fields in Field 13, "
                                                                   "remove 'EGSS EGBB EGFF KKJJ'"])

        # Error in EOBT
        self.do_f13_test(True, 2, "EGLL0360 EGSS", ["Expecting EOBT in HHMM instead of '0360'",
                                                    "Too many fields in Field 13, remove 'EGSS'"])

        # error in ADEP
        self.do_f13_test(True, 2, "E@LL2359 EGSS", ["Expecting departure aerodrome as an ICAO "
                                                    "location indicator, e.g. EGLL instead of 'E@LL'",
                                                    "Too many fields in Field 13, remove 'EGSS'"])

        # F13a and b too long
        self.do_f13_test(True, 1, "EGLL00331", ["Expecting EOBT in HHMM instead of '00331'"])

        # Random faults
        self.do_f13_test(True, 2, "   EGLL0360 / EGSS EGLL",
                         ["Expecting EOBT in HHMM instead of '0360'",
                          "Too many fields in Field 13, remove '/EGSS EGLL'"])

        # Random faults
        self.do_f13_test(True, 2, "   EGLL2400    EGSS    EGBB           EGFF    ",
                         ["Expecting EOBT in HHMM instead of '2400'",
                          "Too many fields in Field 13, remove 'EGSS EGBB EGFF'"])

        # Random faults
        self.do_f13_test(True, 2, "EGLL2401 EGSSF ", ["Expecting EOBT in HHMM instead of '2401'",
                                                      "Too many fields in Field 13, remove 'EGSSF'"])

        # Random faults
        self.do_f13_test(True, 1, "4GLL2401 EGSSF ", ["Expecting departure aerodrome as an ICAO location "
                                                      "indicator, e.g. EGLL instead of '4GLL2401'"])

        # Random faults
        self.do_f13_test(True, 2, "E6GLL2401 EGSSF ", ["Expecting departure aerodrome as an ICAO location "
                                                       "indicator, e.g. EGLL instead of 'E'",
                                                       "Too many fields in Field 13, remove 'EGSSF'"])

    def do_f13_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F13, string_to_parse, 0, len(string_to_parse))
        pf13 = ParseF13(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf13.parse_field()
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
