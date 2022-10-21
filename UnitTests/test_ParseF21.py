import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF21 import ParseF21


class TestParseF21(unittest.TestCase):

    def test_parse_field21(self):
        # Field empty
        self.do_f21_test(True, 1, "", ["There is no data in field 21"])

        # Field empty with spaces
        self.do_f21_test(True, 1, "    ", ["There is no data in field 21"])

        # 21a
        self.do_f21_test(True, 1, "1234", [
            "More subfields expected after '1234'"])

        # 21a & 21b
        self.do_f21_test(True, 1, "1234 123.45", [
            "More subfields expected after '123.45'"])

        # 21a & 21b & 21c
        self.do_f21_test(True, 1, "1234 123.45 N34E021", [
            "More subfields expected after 'N34E021'"])

        # 21a & 21b & 21c & 21d
        self.do_f21_test(True, 1, "1234 123.45 N34E021 2001", [
            "More subfields expected after '2001'"])

        # 21a & 21b & 21c & 21d & 21e
        self.do_f21_test(True, 1, "1234 123.45 N34E021 2001 COM", [
            "More subfields expected after 'COM'"])

        # 21a & 21b & 21c & 21d & 21e & 21f
        self.do_f21_test(False, 0, "1234 123.45 N34E021 2001 COM REMARKS", [
            "More subfields expected after 'F21F'"])

        # Error in 21a
        self.do_f21_test(True, 1, "1260 123.45 N34E321 2001 COM REMARKS", [
            "Expecting time in HHMM instead of '1260'"])

        # Error in 21b
        self.do_f21_test(True, 1, "1234 123.465 N34E321 2001 COM REMARKS", [
            "Expecting frequency in 2 to 4 digits, decimal point, 1 to 2 digit format instead of '123.465'"])

        # Error in 21c
        self.do_f21_test(True, 1, "1234 123.45 N91E321 2001 COM REMARKS", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes or "
            "point/bearing/distance instead of 'N91E321'"])

        # Error in 21d
        self.do_f21_test(True, 1, "1234 123.45 N34E021 2501 COM REMARKS", [
            "Expecting time in HHMM instead of '2501'"])

        # Error in 21e
        self.do_f21_test(True, 1, "1234 123.45 N34E121 2001 CO*M REMARKS", [
            "Invalid characters in field 21e, expecting A to Z, 0 to 9 instead of 'CO*M'"])

        # Error in 21f
        self.do_f21_test(True, 1, "1234 123.45 N34E021 2001 COM REMA*RKS", [
            "Invalid characters in field 21f, expecting A to Z, 0 to 9 instead of 'REMA*RKS'"])

        # What happens with extra fields at the end? The result is not really ideal
        self.do_f21_test(True, 1,
                         "1234 123.45 N34E021 2001 COM REMARKS SOME MORE FIELDS AT THE END", [
                          "Too many fields in Field 21, remove 'SOME MORE FIELDS AT THE END'"])

    def do_f21_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F21, string_to_parse, 0, len(string_to_parse))
        pf21 = ParseF21(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf21.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
