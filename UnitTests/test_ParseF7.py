import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF7 import ParseF7


class TestParseF7(unittest.TestCase):

    def test_parse_field7(self):

        # Missing
        self.do_f7_test(True, 1, "", ["There is no data in field 7"])

        # Single invalid character
        self.do_f7_test(True, 1, "*",
                        ["Expecting callsign in field 7 instead of '*', (1 to 7 characters and digits)"])

        # Too long
        self.do_f7_test(True, 1, "AB345678",
                        ["Expecting callsign in field 7 instead of 'AB345678', (1 to 7 characters and digits)"])

        # OK
        self.do_f7_test(False, 0, "TEST001", [])

        # Mode and code incorrect
        self.do_f7_test(True, 1, "TEST01/", ["Expecting Mode A or C and octal SSR code at end of field instead of '/'"])

        # OK
        self.do_f7_test(False, 0, "   TEST001   ", [])

        # Mode 3A incorrect
        self.do_f7_test(True, 1, " T1/   ", ["Expecting Mode A or C and octal SSR code at end of field instead of '/'"])

        # Mode 3A incorrect
        self.do_f7_test(True, 2, " T1/77   ",
                        ["Expecting SSR mode A or C instead of '7'",
                         "Expecting Mode A or C and octal SSR code at end of field instead of '7'"])

        # Mode 3A incorrect
        self.do_f7_test(True, 2, " T1/ 77   ",
                        ["Expecting SSR mode A or C instead of '7'",
                         "Expecting Mode A or C and octal SSR code at end of field instead of '7'"])

        # Mode 3A incorrect
        self.do_f7_test(True, 2, " T1/D77   ",
                        ["Expecting SSR mode A or C instead of 'D'",
                         "Expecting Mode A or C and octal SSR code at end of field instead of '77'"])

        # Mode 3A incorrect
        self.do_f7_test(True, 1, " T1/A77   ", ["Expecting SSR code as 4 digit octal value instead of '77'"])

        # Mode 3A incorrect
        self.do_f7_test(True, 1, " T1/A7738", ["Expecting SSR code as 4 digit octal value instead of '7738'"])

        # Mode 3A correct
        self.do_f7_test(False, 0, " T1/A7763", [])

        # Mode 3A incorrect
        self.do_f7_test(True, 1, " T1/A1234D", ["Expecting SSR code as 4 digit octal value instead of '1234D'"])

        # Extra field
        self.do_f7_test(True, 1, " T1/A1234 EXTRA",
                        ["Too many fields in Field 7, remove 'EXTRA' and / or check the overall syntax"])

    def do_f7_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F7, string_to_parse, 0, len(string_to_parse))
        pf7 = ParseF7(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf7.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
