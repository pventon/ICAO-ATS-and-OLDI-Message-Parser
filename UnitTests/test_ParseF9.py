import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF9 import ParseF9
from Tokenizer.Token import Token


class TestParseF9(unittest.TestCase):

    def test_parse_field9(self):
        # Empty string
        self.do_f9_test(True, 1, "", ["There is no data in field 9"])

        # Effectively empty string
        self.do_f9_test(True, 1, "      ", ["There is no data in field 9"])

        # Number of aircraft only
        self.do_f9_test(True, 1, "7 ", ["Expecting <Number of A/C (optional), Aircraft Type / WTC> instead of '7'"])

        # Too many aircraft
        self.do_f9_test(True, 1, "102", ["Expecting the number of aircraft as 1 or 2 digits instead of '102'"])

        # Incorrect aircraft type
        self.do_f9_test(True, 1, "B7777754", ["Expecting aircraft type instead of 'B7777754'"])

        # Correct Aircraft type and no '/'
        self.do_f9_test(True, 1, " B737", ["Expecting <Number of A/C (optional), Aircraft "
                                           "Type / WTC> instead of 'B737'"])

        # Correct Number of Aircraft and Aircraft type and no '/'
        self.do_f9_test(True, 1, " 99B737", ["Expecting <Number of A/C (optional), Aircraft "
                                             "Type / WTC> instead of 'B737'"])

        # Correct Aircraft type and '/' but no WTC
        self.do_f9_test(True, 1, " B737/", ["Expecting <Number of A/C (optional), "
                                            "Aircraft Type / WTC> instead of '/'"])

        # Correct Number of Aircraft and Aircraft type and '/' but no WTC
        self.do_f9_test(True, 1, " 23B737/", ["Expecting <Number of A/C (optional), "
                                              "Aircraft Type / WTC> instead of '/'"])

        # WTC Missing
        self.do_f9_test(True, 1, " B737/", ["Expecting <Number of A/C (optional), "
                                            "Aircraft Type / WTC> instead of '/'"])

        # Incorrect WTC
        self.do_f9_test(True, 1, "B737 / R", ["Expecting WTC 'L', 'M', 'H' or 'J' instead of 'R'"])

        # Correct Aircraft and WTC
        self.do_f9_test(False, 0, "B747/H", [])

        # Extra fields
        self.do_f9_test(True, 1, " B707 /M HH", ["Too many fields in Field 9, remove 'HH' and / "
                                                 "or check the overall syntax"])

        # Extra fields
        self.do_f9_test(True, 1, "A320/MR", ["Expecting WTC 'L', 'M', 'H' or 'J' instead of 'MR'"])

        # Incorrect number of aircraft with correct type amd WTC
        self.do_f9_test(True, 1, "111A330/H", ["Expecting the number of aircraft as 1 or 2 digits instead of '111'"])

        # All 3 subfields correct
        self.do_f9_test(False, 0, "  2A320/M  ", [])

    def do_f9_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F9, string_to_parse, 0, len(string_to_parse))
        pf9 = ParseF9(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf9.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
