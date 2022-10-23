import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF10 import ParseF10
from Tokenizer.Token import Token


class TestParseF10(unittest.TestCase):

    def test_parse_field10(self):
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
        self.do_f10_test(True, 1, "S/3", ["Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', "
                                          "'C' or 'A', 'C', 'E', 'H', 'L', 'S' followed optionally by 'B1', B2', "
                                          "'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of '3'"])

        # F10b correct
        self.do_f10_test(False, 0, "N/S", [])

        # Simplest 'correct' case with extra fields
        self.do_f10_test(True, 1, "N/A EXTRA FIELDS", ["Field 10 is correct, remove the extra fields 'EXTRA FIELDS' "
                                                       "and / or check the overall syntax"])

        # Another incorrect case
        self.do_f10_test(True, 1, "S/C More junk!", ["Field 10 is correct, remove the extra fields "
                                                     "'More junk!' and / or check the overall syntax"])

    def test_parse_field10a(self):
        # Definition from EUROCONTROL URD is...
        # "N" | ( 1 { "A" | "B" | "C" | "D" | "E1" | "E2" | "E3" | "F" | "G" | "H" | "I" |
        #       "J1" | "J2"| "J3" | "J4" | "J5" | "J6" | "J7" | "K" | "L" | "M1" | "M2"|
        #       "M3" | "O" | "P1"| "P2"| "P3"| "P4"| "P5"| "P6"| "P7"| "P8"| "P9" | "R" |
        #       "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" } )
        # Valid cases
        self.do_f10_test(False, 0, "ABCE2GHJ2J3M2OP3P4SVZ/C", [""])
        self.do_f10_test(False, 0, "N/C", [""])
        self.do_f10_test(False, 0, "E1E2E3J2J4J7M3P4P5TVZ/C", [""])
        self.do_f10_test(False, 0, "A/C", [""])
        self.do_f10_test(False, 0, "E2/C", [""])

        # Error cases
        self.do_f10_test(True, 1, "E2E2/C", [
            "Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', 'F-I', 'J1-7', 'K', "
            "'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of 'E2E2'"])
        self.do_f10_test(True, 1, "CM1QP4/C", [
            "Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', 'F-I', 'J1-7', 'K', "
            "'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of 'CM1QP4'"])
        self.do_f10_test(True, 1, "CM1QP4A/C", [
            "Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', 'F-I', 'J1-7', 'K', "
            "'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of 'CM1QP4A'"])

    def test_parse_field10b(self):
        # Definition from EUROCONTROL URD is...
        # "N" | (1{ ("I" | "P" | "X") | "A" | "C"}3 | (1{ "A" | "C" | "E" | "H" | "L" | "S"}6) )
        #       [1{"B1"| "B2" | "D1" | "G1" | "U1" | "U2" | "V1" | "V2"}8]
        # Valid cases
        self.do_f10_test(False, 0, "N/IA", [""])
        self.do_f10_test(False, 0, "N/PC", [""])
        self.do_f10_test(False, 0, "N/EHL", [""])
        self.do_f10_test(False, 0, "N/PCB2U2", [""])
        self.do_f10_test(False, 0, "N/AHD1V2", [""])

        # Error cases
        self.do_f10_test(True, 1, "N/IAL", [
            "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or 'A', 'C', 'E',"
            " 'H', 'L', 'S' followed optionally by 'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of 'IAL'"])
        self.do_f10_test(True, 1, "N/PCA", [
            "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or 'A', 'C', 'E',"
            " 'H', 'L', 'S' followed optionally by 'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of 'PCA'"])
        self.do_f10_test(True, 1, "N/EHLP", [
            "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or 'A', 'C', 'E',"
            " 'H', 'L', 'S' followed optionally by 'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of 'EHLP'"])
        self.do_f10_test(True, 1, "N/PCB2B3U2", [
            "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or 'A', 'C', 'E', 'H', 'L', "
            "'S' followed optionally by 'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of 'PCB2B3U2'"])
        self.do_f10_test(True, 1, "N/AHD1V2V3", [
            "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or 'A', 'C', 'E', 'H', 'L', "
            "'S' followed optionally by 'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of 'AHD1V2V3'"])

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
