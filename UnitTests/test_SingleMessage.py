import unittest

from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class MyTestCase(unittest.TestCase):

    def test_ParseMessage_ATS_check_f22_variants(self):
        #                      012345678901
        self.do_test(True, 2, "FF ABCDEFGH\n"       # 11 bytes, 12?
                              # 345678901234567
                              "191916 AAAAAAAA\n"   # 15 bytes, 16?
                              #  3         4         5         6         7         8         9         0
                              # 90123456789012345678901234567890123456789012345678901234567890123456789012345
                              "(ARR-TEST14-LOWW0800-LOWW0200-SOME AIRPORT)",
                     ["Expecting ATA in HHMM instead of 'AIRPORT'",
                      "Too few fields in this message; expecting at least 6 fields"])

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
