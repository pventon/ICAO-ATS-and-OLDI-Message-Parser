import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF8a import ParseF8a
from Tokenizer.Token import Token


class TestParseF8a(unittest.TestCase):

    def test_parse_field8a(self):
        # Missing
        self.do_f8a_test(True, 1, "", ["There is no data in field 8"])

        # Single invalid character
        self.do_f8a_test(True, 1, "*", ["Expecting flight rules 'I', 'V', 'Y' or 'Z' instead of '*'"])

        # Too long
        self.do_f8a_test(True, 1, "IIG", ["Expecting flight rules 'I', 'V', 'Y' or 'Z' instead of 'IIG'"])

        # Extra subfields
        self.do_f8a_test(True, 1, "I IBB", ["Field 8 is correct but there is extra unwanted date, remove "
                                            "'IBB' and / or check the overall syntax"])

        # OK
        self.do_f8a_test(False, 0, "Y", [])

        # OK
        self.do_f8a_test(False, 0, " Y ", [])

        # OK with extra tokens
        self.do_f8a_test(True, 1, " Y EXTRA FIELDS", ["Field 8 is correct but there is extra unwanted date, "
                                                      "remove 'EXTRA FIELDS' and / or check the overall syntax"])

    def do_f8a_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F8a, string_to_parse, 0, len(string_to_parse))
        pf8a = ParseF8a(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf8a.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
