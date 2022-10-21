import unittest

from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class MyTestCase(unittest.TestCase):

    def test_ParseMessage_ATS_check_f22_variants(self):

        self.do_test(True, 3, "(CHG-TEST01-EGLL0800-LOWW0200-221012"
                              "-9/B737/M-15/N0450f350 F*F-16/EGLL0100-9/F34/L)",
                     ["F22 - Field number '9/F34/L' is duplicated and should be removed",
                      "F22 - The first Field 15 element must be a SPEED/LEVEL and not 'N0450f350'",
                      "F22 - The element 'F*F' is an unrecognised Field 15 element"])

    def do_test(self, errors_detected, number_of_errors, message_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        pm = ParseMessage()
        pm.parse_message(fpr, message_to_parse)
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
