import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseAdditionalAddressee import ParseAdditionalAddressee
from IcaoMessageParser.ParseMessage import ParseMessage
from Tokenizer.Token import Token


class TestAddressee(unittest.TestCase):

    fpr: FlightPlanRecord = None
    pf_add_pf_addressee = None

    def tearDown(self) -> None:
        # self.fpr = None
        self.pm = None

    def setUp(self) -> None:
        self.fpr = FlightPlanRecord()

    def test_parse_additional_addressee(self):
        # Empty
        self.do_additional_addressee_test(True, 1, "", [
            "Expecting at least one additional addressee as an 8 character "
            "or 7 character / digit ATC facility address"])

        # A blank string
        self.do_additional_addressee_test(True, 1, "   ", [
            "Expecting at least one additional addressee as an 8 character "
            "or 7 character / digit ATC facility address"])

        # Incorrect additional addressee indicator
        self.do_additional_addressee_test(True, 1, " A5BBCCF", [
            "Expecting 8 character or 7 character / digit ATC facility address instead of 'A5BBCCF'"])

        # Incorrect additional addressee indicator
        self.do_additional_addressee_test(True, 1, "  A5BBCCF",
                                          ["Expecting 8 character or 7 character / digit ATC facility "
                                           "address instead of 'A5BBCCF'"])

        # Incorrect additional addressee indicator
        self.do_additional_addressee_test(True, 1, "A5BBCCF  ", [
            "Expecting 8 character or 7 character / digit ATC facility address instead of 'A5BBCCF'"])

        # Incorrect additional addressee indicator but first two characters are correct
        self.do_additional_addressee_test(True, 1, "  AABBCCDDFX", [
            "Expecting 8 character or 7 character / digit ATC facility address instead of 'AABBCCDDFX'"])

        # Maximum number of correct addressee indicators
        self.do_additional_addressee_test(False, 0,
                                          "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH",
                                          [""])

        # Maximum number of addressee indicators with an error in the third one
        self.do_additional_addressee_test(True, 1,
                                          "AAAAAAAA BBBBBBBB CCCC*CCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH", [
                                              "Expecting 8 character or 7 character / digit ATC facility "
                                              "address instead of 'CCCC*CCC'"])

        # Maximum number of correct addressee indicators with an extra field
        self.do_additional_addressee_test(True, 1,
                                          "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH "
                                          "IIIIIIIIII",
                                          ["Remove the extra field(s) 'IIIIIIIIII' in the additional addressee field"])

        # Maximum number of correct addressee indicators with several extra fields
        self.do_additional_addressee_test(True, 1,
                                          "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG HHHHHHHH "
                                          "IIIIIIIIII X FFF HHH",
                                          ["Remove the extra field(s) 'IIIIIIIIII X FFF HHH' in the "
                                           "additional addressee field"])

        # All OK
        self.do_additional_addressee_test(False, 0, "  DDFFRRTT  ", [""])

        # One under the maximum number of correct addressee indicators
        self.do_additional_addressee_test(False, 0, "AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD EEEEEEEE FFFFFFFF GGGGGGGG",
                                          [""])

    def do_additional_addressee_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.ADADDRESS, string_to_parse, 0, len(string_to_parse))
        pf_add_pf_addressee = ParseAdditionalAddressee(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_add_pf_addressee.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
