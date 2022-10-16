import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseOriginator import ParseOriginator


class TestOriginator(unittest.TestCase):

    def test_parse_originator(self):
        # Empty
        self.do_originator_test(True, 1, "",
                                ["The message originator is missing, 8 character or 7 character / "
                                 "digit ATC facility address"])

        # A blank string
        self.do_originator_test(True, 1, "   ",
                                ["The message originator is missing, 8 character or 7 character / "
                                 "digit ATC facility address"])

        # Incorrect originator indicator
        self.do_originator_test(True, 1, " ABCDEF",
                                ["Expecting 8 character or 7 character / digit ATC facility "
                                 "address instead of 'ABCDEF'"])

        # Incorrect originator indicator
        self.do_originator_test(True, 1, "  ABC66DDD",
                                ["Expecting 8 character or 7 character / digit ATC facility "
                                 "address instead of 'ABC66DDD'"])

        # Incorrect originator indicator
        self.do_originator_test(True, 1, "ABCDEFGRT  ",
                                ["Expecting 8 character or 7 character / digit ATC facility "
                                 "address instead of 'ABCDEFGRT'"])

        # Correct originator indicator with extra field
        self.do_originator_test(True, 1, "AABBCCDD X",
                                ["Remove the extra field(s) 'X' in the originator field"])

        # Correct originator indicator with extra fields
        self.do_originator_test(True, 1, "AABBCCDD X FFF HHH",
                                ["Remove the extra field(s) 'X FFF HHH' in the originator field"])

        # All OK
        self.do_originator_test(False, 0, "  AABBCCDD  ", [""])

    def do_originator_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.ORIGINATOR, string_to_parse, 0, len(string_to_parse))
        pf_originator = ParseOriginator(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_originator.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
