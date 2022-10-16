import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF14a import ParseF14a
from Tokenizer.Token import Token


class TestParseF14a(unittest.TestCase):

    def test_parse_field14a(self):
        # Field empty
        self.do_f14a_test(True, 1, "", ["There is no data in field 14"])

        # Field empty with spaces
        self.do_f14a_test(True, 1, "    ", ["There is no data in field 14"])

        # OK
        self.do_f14a_test(False, 0, "PPP", [""])

        # Building the field bit by bit, all error cases
        self.do_f14a_test(True, 1, "PPP/", ["Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
                                            "degrees/minutes or point/bearing/distance instead of 'PPP/'"])

        # Point Error
        self.do_f14a_test(True, 1, "P3PP", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes or "
            "point/bearing/distance instead of 'P3PP'"])

        # Point is Lat / Long in degrees, OK
        self.do_f14a_test(False, 0, "N65W156", [""])

        # Latitude degrees error > 90
        self.do_f14a_test(True, 1, "N91W179", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N91W179'"])

        # Longitude degrees error > 180
        self.do_f14a_test(True, 1, "N89W181", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N89W181'"])

        # Latitude minutes error > 59
        self.do_f14a_test(True, 1, "N8960W17900", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N8960W17900'"])

        # Longitude minutes error > 59
        self.do_f14a_test(True, 1, "N9050W18060", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of 'N9050W18060'"])

        # Point/Bearing/Distance OK
        self.do_f14a_test(False, 0, "PPP120333", [])

        # Lat/Long in Degrees/Bearing/Distance OK
        self.do_f14a_test(False, 0, "N12W123222333", [])

        # Lat/Long in Degrees & Minutes/Bearing/Distance OK
        self.do_f14a_test(False, 0, "N1234W12345240456", [])

        # Lat/Long in Degrees & Minutes/Bearing/Distance -> Lat Minutes > 59
        self.do_f14a_test(True, 1, "N1260W12345", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of 'N1260W12345'"])

        # Lat/Long in Degrees & Minutes/Bearing/Distance -> Long Minutes > 59
        self.do_f14a_test(True, 1, "N1259W12360", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of 'N1259W12360'"])

        # Extra fields
        self.do_f14a_test(True, 1, "AAAAA EXTRA FIELD", [
            "Too many field(s) in Field 14, remove 'EXTRA FIELD'"])

    def do_f14a_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F14a, string_to_parse, 0, len(string_to_parse))
        pf14a = ParseF14a(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf14a.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
