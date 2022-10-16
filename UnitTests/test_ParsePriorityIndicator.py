import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParsePriorityIndicator import ParsePriorityIndicator
from Tokenizer.Token import Token


class TestParsePriorityIndicator(unittest.TestCase):

    def test_parse_priority(self):
        # Empty
        self.do_priority_test(True, 1, "",
                              ["The priority field is missing, should contain 'FF', 'GG', 'DD', 'KK' or 'SS'"])

        self.do_priority_test(True, 1, "",
                              ["The priority field is missing, should contain 'FF', 'GG', 'DD', 'KK' or 'SS'"])

        # A blank string
        self.do_priority_test(True, 1, "   ",
                              ["The priority field is missing, should contain 'FF', 'GG', 'DD', 'KK' or 'SS'"])

        # Incorrect priority indicator
        self.do_priority_test(True, 1, "A",
                              ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'A'",
                               ""])

        # Incorrect priority indicator
        self.do_priority_test(True, 1, "  XX",
                              ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'XX'"])

        # Incorrect priority indicator
        self.do_priority_test(True, 1, "XXX  ",
                              ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'XXX'"])

        # Incorrect priority indicator but first two characters are correct
        self.do_priority_test(True, 1, "  FFX",
                              ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'FFX'"])

        # Correct priority indicator with extra field
        self.do_priority_test(True, 1, "GG X",
                              ["Remove the extra field(s) 'X' in the priority field"])

        # Correct priority indicator with extra fields
        self.do_priority_test(True, 1, "KK X FFF HHH",
                              ["Remove the extra field(s) 'X FFF HHH' in the priority field"])

        # All OK
        self.do_priority_test(False, 0, "   DD   ", [])

    def test_parse_priority_msg_related(self):
        # Invalid syntax
        self.do_priority_test(True, 1, "HEADER1",
                              ["Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of 'HEADER1'",
                               ""])

    def do_priority_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.PRIORITY_INDICATOR, string_to_parse, 0, len(string_to_parse))
        pf_priority_indicator = ParsePriorityIndicator(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_priority_indicator.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
