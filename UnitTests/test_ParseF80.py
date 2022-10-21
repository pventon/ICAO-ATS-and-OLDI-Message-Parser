import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF80 import ParseF80


class TestParseF80(unittest.TestCase):

    def test_parse_field80(self):
        # Missing
        self.do_f80_test(True, 1, "", ["There is no data in field 80"])

        # Too long
        self.do_f80_test(True, 1, "IIG",
                          ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'IIG'"])

        # OK
        self.do_f80_test(False, 0, "S ", [])

        # Incorrect
        self.do_f80_test(True, 1, "MGA",
                          ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'MGA'"])

        # OK
        self.do_f80_test(False, 0, "    M   ", [])

        # Type of flight incorrect
        self.do_f80_test(True, 1, " K   ",
                          ["Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of 'K'"])

        # Extra field with incorrect type of flight
        self.do_f80_test(True, 1, " M  DD ",
                          ["Field 80 is correct but there is extra unwanted data, "
                           "remove 'DD' and / or check the overall syntax"])

        # Extra field with correct type of flight
        self.do_f80_test(True, 1, " G  DD ",
                          ["Field 80 is correct but there is extra unwanted data, "
                           "remove 'DD' and / or check the overall syntax"])

    def do_f80_test(self, errors_detected, number_of_errors,
                     string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F80, string_to_parse, 0, len(string_to_parse))
        pf80 = ParseF80(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf80.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
