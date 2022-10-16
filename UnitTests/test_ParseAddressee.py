import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseAddressee import ParseAddressee
from Tokenizer.Token import Token


class TestAddressee(unittest.TestCase):

    def test_parse_addressee(self):
        # Incorrect addressee indicator
        self.do_addressee_test(True, 1, " A5BBCCF", [
            "Expecting 8 character or 7 character / digit ATC facility address instead of 'A5BBCCF'"])

        # Empty
        self.do_addressee_test(True, 1, "", ["The addressee field is missing, expecting at least one addressee as "
                                             "an 8 character or 7 character / digit ATC facility address"])

        # A blank string
        self.do_addressee_test(True, 1, "    ",
                               ["The addressee field is missing, expecting at least one addressee as "
                                "an 8 character or 7 character / digit ATC facility address"])

        # Incorrect addressee indicator
        self.do_addressee_test(True, 1, "  A5BBCCF", ["Expecting 8 character or 7 character / digit ATC facility "
                                                      "address instead of 'A5BBCCF'"])

        # Incorrect addressee indicator
        self.do_addressee_test(True, 1, "A5BBCCF  ",
                               ["Expecting 8 character or 7 character / digit ATC "
                                "facility address instead of 'A5BBCCF'"])

        # Incorrect addressee indicator but first two characters are correct
        self.do_addressee_test(True, 1, "  AABBCCDDFX", ["Expecting 8 character or 7 character / digit "
                                                         "ATC facility address instead of 'AABBCCDDFX'"])

        # Maximum number of correct addressee indicators
        self.do_addressee_test(False, 0, "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH",
                               [""])

        # Maximum number of addressee indicators with an error in the third one
        self.do_addressee_test(True, 1, "AAAAAAAA BBBBBBBB CCCC*CCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH", [
            "Expecting 8 character or 7 character / digit ATC facility address instead of 'CCCC*CCC'"])

        # Maximum number of correct addressee indicators with an extra field
        self.do_addressee_test(True, 1, "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH "
                                        "IIIIIIIIII",
                               ["Remove the extra field(s) 'IIIIIIIIII' in the addressee field"])

        # Maximum number of correct addressee indicators with several extra fields
        self.do_addressee_test(True, 1, "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH "
                                        "IIIIIIIIII X FFF HHH",
                               ["Remove the extra field(s) 'IIIIIIIIII X FFF HHH' in the addressee field"])

        # All OK
        self.do_addressee_test(False, 0, "  DDFFRRTT  ", [""])

        # All OK
        self.do_addressee_test(False, 0, "  HEADER1  ", [""])

        # One under the maximum number of correct addressee indicators
        self.do_addressee_test(False, 0, "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG",
                               [""])

    def do_addressee_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.ADDRESS, string_to_parse, 0, len(string_to_parse))
        pf_addressee = ParseAddressee(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_addressee.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
