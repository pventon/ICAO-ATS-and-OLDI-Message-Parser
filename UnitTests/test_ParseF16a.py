import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF16a import ParseF16a
from Tokenizer.Token import Token


class TestParseF16a(unittest.TestCase):

    def test_parse_field16a(self):
        # Field empty
        self.do_f16a_test(True, 1, "", ["There is no data in field 16"])

        # Field empty with spaces
        self.do_f16a_test(True, 1, "    ", ["There is no data in field 16"])

        # Part of ADEP location indicator
        self.do_f16a_test(True, 1, "EGL", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGL'"])

        # Correct ADES, EET incorrect
        self.do_f16a_test(True, 1, "EGLL080", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLL080'"])

        # Correct ADES
        self.do_f16a_test(False, 0, "EGLL", [""])

        # Too many fields
        self.do_f16a_test(True, 1, "EGLL 0100 EGSS EGBB EGFF KKJJ", [
            "Too many fields in Field 16, remove '0100 EGSS EGBB EGFF KKJJ'"])

        # error in ADES
        self.do_f16a_test(True, 2, "E@LL2359 EGSS", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'E@LL2359'",
            "Too many fields in Field 16, remove 'EGSS'"])

        # F16a too long
        self.do_f16a_test(True, 1, "EGLLV", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLLV'"])

        # Random faults
        self.do_f16a_test(True, 2, "   EGLL0360 / EGSS EGBB", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLL0360'",
            "Too many fields in Field 16, remove '/EGSS EGBB'"])

        # Random faults
        self.do_f16a_test(True, 2, "   EGLL2400    EGSS    EGBB           EGFF    ", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLL2400'",
            "Too many fields in Field 16, remove 'EGSS EGBB EGFF'"])

        # Random faults
        self.do_f16a_test(True, 2, "EGLL2401 EGSSF ", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLL2401'",
            "Too many fields in Field 16, remove 'EGSSF'"])

        # Extra character after EOBT before optional fields
        self.do_f16a_test(True, 2, "EGLL23 591", [
            "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of 'EGLL23'",
            "Too many fields in Field 16, remove '591'"])

        # Extra character after second extra unnecessary  field
        self.do_f16a_test(True, 1, "EGLL 2359 EGSS ABCDF ", [
            "Too many fields in Field 16, remove '2359 EGSS ABCDF'"])

    def do_f16a_test(self, errors_detected, number_of_errors,
                     string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F16a, string_to_parse, 0, len(string_to_parse))
        pf16a = ParseF16a(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf16a.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
