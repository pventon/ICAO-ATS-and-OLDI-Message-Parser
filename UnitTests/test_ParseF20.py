import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF20 import ParseF20


class TestParseF20(unittest.TestCase):

    def test_parse_field20(self):
        # Field empty
        self.do_f20_test(True, 1, "", ["There is no data in field 20"])

        # Field empty with spaces
        self.do_f20_test(True, 1, "    ", ["There is no data in field 20"])

        # 20a
        self.do_f20_test(True, 1, "EGL", [
            "More subfields expected after 'EGL'"])

        # 20a & 20b
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT", [
            "More subfields expected after 'LAST_UNIT'"])

        # 20a & 20b & 20c
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234", [
            "More subfields expected after '1234'"])

        # 20a & 20b & 20c & 20d
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45", [
            "More subfields expected after '132.45'"])

        # 20a & 20b & 20c & 20d & 20e
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 N23W123", [
            "More subfields expected after 'N23W123'"])

        # 20a & 20b & 20c & 20d & 20e & 20f
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 N2334W12343 F20F", [
            "More subfields expected after 'F20F'"])

        # 20a & 20b & 20c & 20d & 20e & 20f & F20g
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 GOLVA F20F F20G", [
            "More subfields expected after 'F20G'"])

        # 20a & 20b & 20c & 20d & 20e & 20f & F20g & F20h
        self.do_f20_test(False, 0, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PNT F20F F20G F20H", [
            "More subfields expected after '23N123W'"])

        # Error in 20a
        self.do_f20_test(True, 1, "BRITISH_*AIRWAYS LAST_UNIT 1234 132.45 PNT F20F F20G F20H", [
            "Invalid characters in field 20a, expecting A to Z, 0 to 9 instead of 'BRITISH_*AIRWAYS'"])

        # Error in 20b
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_*UNIT 1234 132.45 PNT F20F F20G F20H", [
            "Invalid characters in field 20b, expecting A to Z, 0 to 9 instead of 'LAST_*UNIT'"])

        # Error in 20c
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1260 132.45 PNT F20F F20G F20H", [
            "Expecting time in HHMM instead of '1260'"])

        # Error in 20d
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.475 PNT F20F F20G F20H", [
            "Expecting frequency in 2 to 4 digits, decimal point, 1 to 2 digit format instead of '132.475'"])

        # Error in 20e
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PN66T F20F F20G F20H", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes or "
            "point/bearing/distance instead of 'PN66T'"])

        # Error in 20f
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PNT F*20F F20G F20H", [
            "Invalid characters in field 20f, expecting A to Z, 0 to 9 instead of 'F*20F'"])

        # Error in F20g
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PNT F20F F*20G F20H", [
            "Invalid characters in field 20g, expecting A to Z, 0 to 9 instead of 'F*20G'"])

        # Error in F20h
        self.do_f20_test(True, 1, "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PNT F20F F20G F*20H", [
            "Invalid characters in field 20h, expecting A to Z, 0 to 9 instead of 'F*20H'"])

        # What happens with extra fields at the end? The result is not really ideal
        self.do_f20_test(True, 1,
                         "BRITISH_AIRWAYS LAST_UNIT 1234 132.45 PNT F20F F20G F20H SOME MORE FIELDS AT THE END", [
                          "Too many fields in Field 20, remove 'SOME MORE FIELDS AT THE END'"])

    def do_f20_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F20, string_to_parse, 0, len(string_to_parse))
        pf20 = ParseF20(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf20.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
