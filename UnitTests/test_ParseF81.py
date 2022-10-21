import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF81 import ParseF81


class TestParseF81(unittest.TestCase):

    def test_parse_field81(self):
        # Missing
        self.do_f81_test(True, 1, "", ["There is no data in field 81"])

        # Field 81a, rest missing
        self.do_f81_test(True, 1, "N",
                         ["Field 81 is incomplete, field should be (equipment code '/' equipment status) or ("
                          "surveillance class '/' equipment status '/' surveillance equipment code) instead of 'N'"])

        # Field 81a '/', rest missing - Field 'a' syntax [N] | ([S] | [A-MOPRT-Z1-9]+ | [A-MOPRT-Z1-9]+)|ADSB|ADSC
        self.do_f81_test(True, 1, "Z1/ ", ["Field 81 is incomplete, field should be (equipment code '/' "
                                           "equipment status) or (surveillance class '/' equipment status "
                                           "'/' surveillance equipment code) instead of 'Z1/ '"])

        # Field 81a '/' F81b - OK
        self.do_f81_test(False, 0, "A/UN", [""])

        # Field 81a, rest missing
        self.do_f81_test(True, 1, " ADSB   ",
                         ["Field 81 is incomplete, field should be (equipment code '/' equipment status) or "
                          "(surveillance class '/' equipment status '/' surveillance equipment code) "
                          "instead of ' ADSB   '"])

        # Field 81a '/', rest missing
        self.do_f81_test(True, 1, " ADSC/   ",
                         ["Field 81 is incomplete, field should be (equipment code '/' equipment status) or "
                          "(surveillance class '/' equipment status '/' surveillance equipment code) "
                          "instead of ' ADSC/   '"])

        # Field 81a '/' F81b - OK
        self.do_f81_test(False, 0, "ADSC/EQ ", [""])

        # Field 81a '/' F81b '/', F81c missing
        self.do_f81_test(True, 1, "ADSC/EQ/ ",
                         ["Field 81 is incomplete, field should be (equipment code '/' equipment status) or "
                          "(surveillance class '/' equipment status '/' surveillance equipment code) "
                          "instead of 'ADSC/EQ/ '"])

        # Field 81a '/' F81b '/' F81c, OK
        self.do_f81_test(False, 0, "ADSC/EQ/B ", [""])

        # Field 81a '/' F81b present, error in F81a - Error
        self.do_f81_test(True, 1, "Q/UN", ["Expecting equipment code or surveillance class instead of 'Q'"])

        # Field 81a '/' F81b present, error in '/' - Error
        self.do_f81_test(True, 1, "A L UN", ["Expecting a forward slash '/' instead of 'L'"])

        # Field 81a '/' F81b present, error in F81c - Error
        self.do_f81_test(True, 1, "A/ VN", ["Expecting equipment stats as 'EQ'.'UN' or 'NO' instead of 'VN'"])

        # Field 81a '/' F81b '/' F81c present, error in F81a - Error
        self.do_f81_test(True, 1, "Q/UN/B", ["Expecting equipment code or surveillance class instead of 'Q'"])

        # Field 81a '/' F81b '/' F81c present, error in '/' - Error
        self.do_f81_test(True, 1, "N L UN/H", ["Expecting a forward slash '/' instead of 'L'"])

        # Field 81a '/' F81b '/' F81c present, error in F81b - Error
        self.do_f81_test(True, 1, "S/XN/P", ["Expecting equipment stats as 'EQ'.'UN' or 'NO' instead of 'XN'"])

        # Field 81a '/' F81b '/' F81c present, error in '/' - Error
        self.do_f81_test(True, 1, "R/UN ! G", ["Expecting a forward slash '/' instead of '!'"])

        # Field 81a '/' F81b '/' F81c present, error in F81c - Error
        self.do_f81_test(True, 1, "O/UN/M", ["Expecting surveillance equipment code instead of 'M'"])

        # Field 81a '/' F81b '/' F81c, OK but too many fields
        self.do_f81_test(True, 1, "ADSC/EQ/B EXTRA BITS AND PIECES",
                         ["Too many field(s) in Field 81, remove 'EXTRA BITS AND PIECES'"])

        # Field 81a '/' F81b '/' F81c present, but error in F81b with too many fields
        self.do_f81_test(True, 2, "ADSC/ZQ/B EXTRA BITS AND PIECES",
                         ["Expecting equipment stats as 'EQ'.'UN' or 'NO' instead of 'ZQ'",
                          "Too many field(s) in Field 81, remove 'EXTRA BITS AND PIECES'"])

    def do_f81_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F81, string_to_parse, 0, len(string_to_parse))
        pf81 = ParseF81(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf81.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
