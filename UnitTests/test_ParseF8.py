import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF8 import ParseF8


class TestParseF8(unittest.TestCase):

    def test_parse_field8(self):
        # Missing
        self.do_f8_test(True, 1, "", ["There is no data in field 8"])

        # Single invalid character
        self.do_f8_test(True, 1, "*", ["Expecting flight rules 'I', 'V', 'Y' or 'Z' instead of '*'"])

        # Too long
        self.do_f8_test(True, 1, "IIG", ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'IG'"])

        # OK
        self.do_f8_test(False, 0, "IS ", [])

        #
        self.do_f8_test(True, 1, "VGA", ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'GA'"])

        # OK
        self.do_f8_test(False, 0, "   I M   ", [])

        # Type of flight incorrect
        self.do_f8_test(True, 1, " IK   ", ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'K'"])

        # Extra field with incorrect type of flight
        self.do_f8_test(True, 2, " IK  DD ", ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'K'",
                                              "Field 8 is correct but there is extra unwanted data, remove 'DD' "
                                              "and / or check the overall syntax"])

        # Extra field with correct type of flight
        self.do_f8_test(True, 1, " IX  DD ", ["Field 8 is correct but there is extra unwanted data, "
                                              "remove 'DD' and / or check the overall syntax"])

        # Rules correct but nothing else present
        self.do_f8_test(True, 1, " I ", ["Expecting type of flight after rules 'I'"])

    def do_f8_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F8, string_to_parse, 0, len(string_to_parse))
        pf8 = ParseF8(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf8.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
