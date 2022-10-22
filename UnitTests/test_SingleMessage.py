import unittest

from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class MyTestCase(unittest.TestCase):

    def test_ParseMessage_ATS_check_f22_variants(self):

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-EGLL0800-N0450F350 BBB-LOWW0200-"
                              "-RMK/REMARK 1 RMK/REMARK 2 RMK/REMARK 3 "
                              "STS/FFR STS/HAZMAT STS/MARSA "
                              "RVR/200 SRC/RPL DATA TALT/TALT DATA)",
                     ["Too many F18 SRC fields, should only be one field as 'RPL', 'FPL', 'AFIL', 'MFS', 'FNM', "
                      "'RQP', 'AFP', 'DIV' or a 4 character location instead of 'RPL DATA'"])

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
