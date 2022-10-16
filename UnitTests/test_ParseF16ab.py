import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF16ab import ParseF16ab
from Tokenizer.Token import Token


class TestParseF16ab(unittest.TestCase):

    def test_parse_field16ab(self):
        # Field empty
        self.do_f16ab_test(True, 1, "", ["There is no data in field 16"])

        # Field empty with spaces
        self.do_f16ab_test(True, 1, "    ", ["There is no data in field 16"])

        # Part of ADEP location indicator
        self.do_f16ab_test(True, 1, "EGL", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGL'"])

        # Correct ADES, EET incorrect
        self.do_f16ab_test(True, 1, "EGLL080", ["Expecting EOBT in HHMM instead of '080'"])

        # Correct ADES, EET, extra field
        self.do_f16ab_test(True, 1, "EGLL0100 E5SS", [
            "Too many fields in Field 16, remove 'E5SS'"])

        # Too many fields
        self.do_f16ab_test(True, 1, "EGLL0100 EGSS EGBB EGFF KKJJ", [
            "Too many fields in Field 16, remove 'EGSS EGBB EGFF KKJJ'"])

        # Error in EET
        self.do_f16ab_test(True, 1, "EGLL0360 ", [
            "Expecting EOBT in HHMM instead of '0360'"])

        # error in ADES
        self.do_f16ab_test(True, 2, "E@LL2359 EGSS", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'E@LL'",
            "Too many fields in Field 16, remove 'EGSS'"])

        # F16a and b too long
        self.do_f16ab_test(True, 2, "EGLL00320 EGSS", ["Expecting EOBT in HHMM instead of '00320'",
                                                       "Too many fields in Field 16, remove 'EGSS'"])

        # Random faults
        self.do_f16ab_test(True, 2, "   EGLL0360 / EGSS EGBB", ["Expecting EOBT in HHMM instead of '0360'",
                                                                "Too many fields in Field 16, remove '/EGSS EGBB'"])

        # Random faults
        self.do_f16ab_test(True, 2, "   EGLL2400    EGSS    EGBB           EGFF    ",
                           ["Expecting EOBT in HHMM instead of '2400'",
                            "Too many fields in Field 16, remove 'EGSS EGBB EGFF'"])

        # Random faults
        self.do_f16ab_test(True, 2, "EGLL2401 EGSSF ", ["Expecting EOBT in HHMM instead of '2401'",
                                                        "Too many fields in Field 16, remove 'EGSSF'"])

        # Extra character after EOBT before optional fields
        self.do_f16ab_test(True, 1, "EGLL23591", ["Expecting EOBT in HHMM instead of '23591'"])

        # Extra character after second extra unnecessary  field
        self.do_f16ab_test(True, 1, "EGLL2359 EGSS ABCDF ",
                           ["Too many fields in Field 16, remove 'EGSS ABCDF'"])

        # Correct ADES, EET
        self.do_f16ab_test(False, 0, "EGLL0900", [""])

    def do_f16ab_test(self, errors_detected, number_of_errors,
                      string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F16ab, string_to_parse, 0, len(string_to_parse))
        pf16ab = ParseF16ab(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf16ab.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
