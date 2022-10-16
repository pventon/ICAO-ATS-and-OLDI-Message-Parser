import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF10 import ParseF10
from Tokenizer.Token import Token


class TestParseF10(unittest.TestCase):

    def test_parse_field10(self):
        # TODO - Parsing of this field needs some serious extra work which I'll do later
        # Field empty
        self.do_f10_test(True, 1, "", ["There is no data in field 10"])

        # Empty but spaces
        self.do_f10_test(True, 1, "     ", ["There is no data in field 10"])

        # F10a only and incorrect
        self.do_f10_test(True, 1, "*", ["Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', "
                                        "'F-I', 'J1-7', 'K', 'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of '*'"])

        # F10a only and correct
        self.do_f10_test(True, 1, "N", ["Expecting communications and surveillance capabilities instead of 'N'"])

        # F10a and '/' and incorrect
        self.do_f10_test(True, 1, "( /", ["Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', "
                                          "'F-I', 'J1-7', 'K', 'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of '('"])

        # F10a and '/' and correct
        self.do_f10_test(True, 1, "N/", ["Expecting communications and surveillance capabilities instead of '/'"])

        # F10b incorrect
        self.do_f10_test(True, 1, "S/3", ["Expecting surveillance capabilities as 'N' or one or more of 'A', "
                                          "'B1-2', 'C', 'D1', 'E', 'G1', 'H', 'I', 'L', 'P', 'S', 'U1-2', "
                                          "'V1-2' or 'X' instead of '3'"])

        # F10b correct
        self.do_f10_test(False, 0, "N/S", [])

        # Simplest 'correct' case with extra fields
        self.do_f10_test(True, 1, "N/A EXTRA FIELDS", ["Field 10 is correct, remove the extra fields 'EXTRA FIELDS' "
                                                       "and / or check the overall syntax"])

        # Another incorrect case
        self.do_f10_test(True, 1, "S/C More junk!", ["Field 10 is correct, remove the extra fields "
                                                     "'More junk!' and / or check the overall syntax"])

    def do_f10_test(self, errors_detected, number_of_errors,
                   string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F10, string_to_parse, 0, len(string_to_parse))
        pf10 = ParseF10(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf10.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
