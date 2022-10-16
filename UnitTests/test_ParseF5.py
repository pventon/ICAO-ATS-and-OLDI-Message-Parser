import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF5 import ParseF5


class TestParseF3(unittest.TestCase):

    def test_parse_field5(self):

        # Too short
        self.do_f5_test(True, 1, "", ["There is no data in field 5"])

        # Too few fields
        self.do_f5_test(True, 1, "KKK",
                        ["The first item in F5a should be INCERFA, ALERFA or DETRESFA instead of 'KKK'"])

        # Too many fields but F5c is free text so this is OK
        self.do_f5_test(True, 1, "HHH GGG JJJ KKK",
                        ["The first item in F5a should be INCERFA, ALERFA or DETRESFA instead of 'HHH'"])

        # F5a and F5b correct but F5c missing
        self.do_f5_test(True, 1, "  INCERFA /ABCDEFGH ",
                        ["More subfields expected after 'ABCDEFGH'"])

        # F5a and F5b correct and F5c present
        self.do_f5_test(False, 0, "ALERFA   /ABCDEFGH /THIS IS FREE TEXT", [""])

        # F5a incorrect, F5b & F5c correct
        self.do_f5_test(True, 1, "NCERFA     /ABCDEFGH /HELLO",
                        ["The first item in F5a should be INCERFA, ALERFA or DETRESFA "
                            "instead of 'NCERFA'"])

        # F5b incorrect, F5a & F5c correct
        self.do_f5_test(True, 1, "    INCERFA     /ABCDEFGHI /HELLO",
                        ["Expecting 8 character or 7 character / digit ATC "
                            "facility address instead of 'ABCDEFGHI'"])

        # F5b incorrect, F5a & F5c correct
        self.do_f5_test(True, 1, "    DETRESFA     /ABC55GHH /HELLO",
                        ["Expecting 8 character or 7 character / digit ATC "
                            "facility address instead of 'ABC55GHH'"])

        # All correct
        self.do_f5_test(False, 0, "    DETRESFA     /ABC8FGH /HELLO", [""])

        # All correct with illegal extra fields at end
        self.do_f5_test(True, 2, "    DETRESFA     /ABC8FGH /HELLO illegal characterS",
                        ["Field 5c can only contain upper case characters and digits instead of 'illegal'",
                         "Field 5c can only contain upper case characters and digits instead of 'characterS'"])

        # All correct with illegal extra fields at end
        self.do_f5_test(True, 1, "    DETRESFA     /ABC8FGH /HELLO FRED characterS",
                        ["Field 5c can only contain upper case characters and digits instead of 'characterS'"])

        # Last field in valid characters
        self.do_f5_test(True, 2, "    DETRESFA     /ABC8*GH /HELLO FRED characterS",
                        ["Expecting 8 character or 7 character / digit ATC facility address instead of 'ABC8*GH'",
                         "Field 5c can only contain upper case characters and digits instead of 'characterS'"])

    def do_f5_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F5, string_to_parse, 0, len(string_to_parse))
        pf5 = ParseF5(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf5.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
