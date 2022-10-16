import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMfsPoint import ParseMfsPoint


class TestParseMfsPoint(unittest.TestCase):

    def test_parse_mfs_point(self):
        # Empty
        self.do_mfs_point_test(True, 1, "", ["There is no data in field MFS Significant point field"])

        # A blank string
        self.do_mfs_point_test(True, 1, "   ", ["There is no data in field MFS Significant point field"])

        # Incorrect MFS Point
        self.do_mfs_point_test(True, 1, " 322359", [
            "Expecting MFS significant point starting with a letter followed by up to 14 "
            "letters and digits instead of '322359'"])

        # Incorrect MFS Point
        self.do_mfs_point_test(True, 1, "  A312*360", [
            "Expecting MFS significant point starting with a letter followed by up to 14 "
            "letters and digits instead of 'A312*360'"])

        # MFS Point too long
        self.do_mfs_point_test(True, 1, "A1B2C3D4E5F6G7H8  ", [
            "Expecting MFS significant point starting with a letter followed by up to 14 "
            "letters and digits instead of 'A1B2C3D4E5F6G7H8'"])

        # All OK
        self.do_mfs_point_test(False, 0, "A1B2C3D4E5F6G7H", [""])

        # OK with one extra field
        self.do_mfs_point_test(True, 1, "A1B2C3D4E5F6G7H X", [
            "Expecting a single point for the MFS point, remove 'X'"])

        # OK with many extra field
        self.do_mfs_point_test(True, 1, "A1B2C3D4E5F6G7H 181245 X FFF HHH", [
            "Expecting a single point for the MFS point, remove '181245 X FFF HHH'"])

        # NOK with many extra field
        self.do_mfs_point_test(True, 2, "A1B2C*D4E5F6G7H 181245 X FFF HHH", [
            "Expecting MFS significant point starting with a letter followed by up to 14 "
            "letters and digits instead of 'A1B2C*D4E5F6G7H'",
            "Expecting a single point for the MFS point, remove '181245 X FFF HHH'"])

        # OK but shorter than 15 characters
        self.do_mfs_point_test(False, 0, "A14E5F6G7H", [""])

    def do_mfs_point_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.MFS_SIG_POINT, string_to_parse, 0, len(string_to_parse))
        pf_significant_point = ParseMfsPoint(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_significant_point.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
