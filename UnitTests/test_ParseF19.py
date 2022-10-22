import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF19 import ParseF19


class TestParseF19(unittest.TestCase):

    def test_parse_f19(self):
        #     F19a = auto()
        #     F19c = auto()
        #     F19d = auto()
        #     F19e = auto()
        #     F19j = auto()
        #     F19n = auto()
        #     F19p = auto()
        #     F19r = auto()
        #     F19s = auto()
        self.do_f19_test(True, 1, "", ["No data in field 19, expecting field 19 keyword/data"])

        self.do_f19_test(True, 1, "     ", ["No data in field 19, expecting field 19 keyword/data"])

        self.do_f19_test(True, 1, "/", ["Field 19 contains no keywords, must consist of one or more "
                                        "keyword/data occurrences instead of '/'"])

        self.do_f19_test(True, 1, "  XXX  ", ["Field 19 contains no keywords, must consist of one or "
                                              "more keyword/data occurrences instead of 'XXX'"])

        self.do_f19_test(True, 1, "0", ["Field 19 contains no keywords, must consist of one or more "
                                        "keyword/data occurrences instead of '0'"])

        self.do_f19_test(True, 1, "   /   A", [
            "Field 19 contains no keywords, must consist of one or more keyword/data occurrences instead of '/   A'"])

        self.do_f19_test(True, 1, "C", [
            "Field 19 contains no keywords, must consist of one or more keyword/data occurrences instead of 'C'"])

        self.do_f19_test(True, 2, "E/", ["Expecting data following field 19 keyword 'E/'",
                                         "Expecting fuel endurance in HHMM format instead of '' in F19 'E'"])

        self.do_f19_test(True, 2, "N/P/23 ", [
            "Expecting data following field 19 keyword 'N/'",
            "Expecting other survival equipment and useful remarks (A-Z, 1-9 and spaces) instead of '' in F19 'N'"])

        self.do_f19_test(False, 0, "P/123 ", [""])

        self.do_f19_test(True, 1, "R/U X/ ", [
            "Field 19 Keyword 'X/' unrecognised"])

        self.do_f19_test(True, 1, "S/M X/DATA ", [
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(False, 0, "A/VALID DATA4 X C/VALID DATA ", [""])

        self.do_f19_test(True, 1, "A/VALID DATA5 X/ C/VALID DATA ", [
            "Field 19 Keyword 'X/' unrecognised", ""])

        self.do_f19_test(True, 1, "A/VALID DATA6 X/DATA C/VALID DATA ", [
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(True, 1, "D/10 123 C RED Y/DATA C/VALID DATA ", [
            "Field 19 Keyword 'Y/DATA' unrecognised"])

        self.do_f19_test(True, 2, "N/VALID DATA8 Y/ X/DATA A/VALID DATA ", [
            "Field 19 Keyword 'Y/' unrecognised",
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(True, 2, "A/VALID DATA9 Y/DATA X/DATA S/M ", [
            "Field 19 Keyword 'Y/DATA' unrecognised",
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(False, 0, "S/P  S/D S/M", [""])

        fpr = self.do_f19_test(False, 0, "S/D S/J S/M "
                                         "A/RED A/GREEN A/BLUE "
                                         "N/SURVIVAL P/123 R/V", [""])
        self.assertEqual("GREEN", fpr.get_all_icao_subfields(
            FieldIdentifiers.F19, SubFieldIdentifiers.F19a)[1].get_field_text())
        self.assertEqual(None, fpr.get_all_icao_subfields(
            FieldIdentifiers.F19, SubFieldIdentifiers.F19c))

        self.do_f19_test(True, 3, "C/H/GARBAGE J/F", [
            "Expecting data following field 19 keyword 'C/'",
            "Field 19 Keyword 'H/GARBAGE' unrecognised",
            "Expecting pilot name (A-Z, 0-9 and spaces) instead of '' in F19 'C'"])

        self.do_f19_test(True, 2,
                         "/A/GREEN J/U HHH/GARBAGE N/REMARK "
                         "R/E C/FRED BLOGS SECOND C",
                         ["Expecting field 19 keyword/data instead of '/'",
                          "Field 19 Keyword 'HHH/GARBAGE' unrecognised"])

    def test_parse_f19_a(self):
        # OK
        self.do_f19_test(False, 0, "   A   /   THIS AIRPLANE IS WHITE WITH 2 WINGS ", [""])

        # Invalid character in field - error
        self.do_f19_test(True, 1, "   A   /   THIS AIRPLANE IS WHITE, WITH 2 WINGS ", [
            "Expecting other significant markings and / or aircraft color (A-Z, 0-9 and spaces) "
            "instead of '   THIS AIRPLANE IS WHITE, WITH 2 WINGS' in F19 'A'"])

    def test_parse_f19_c(self):
        # OK
        self.do_f19_test(False, 0, "   C   /   PILOTS NAME ", [""])

        # Invalid character in field - error
        self.do_f19_test(True, 1, "   C   /   PILOTS; NAME ", [
            "Expecting pilot name (A-Z, 0-9 and spaces) instead of '   PILOTS; NAME' in F19 'C'"])

    def test_parse_f19_d(self):
        # OK
        self.do_f19_test(False, 0, "   D   / 12 123 C RED", [""])

        # Too few fields - error
        self.do_f19_test(True, 1, "   D   /   ", [
            "Expecting data following field 19 keyword 'D   /'"])

        # Too few fields - error
        self.do_f19_test(True, 1, "D/12   ", [
            "Expecting number of dinghies, dinghy capacity, covered or not and "
            "dinghy color, too few fields in F19 'D', '12'"])

        # Too few fields - error
        self.do_f19_test(True, 1, "D/12 345   ", [
            "Expecting number of dinghies, dinghy capacity, covered or not and "
            "dinghy color, too few fields in F19 'D', '12 345'"])

        # Correct with field 'c' missing which is optional
        self.do_f19_test(False, 0, "D/12 345 RED  ", [""])

        # Correct with field 'c' & 'd'
        self.do_f19_test(False, 0, "D/12 345 C RED  ", [""])

        # Correct with minimum number of digits fields 'a' & 'b'
        self.do_f19_test(False, 0, "D/1 3 C RED  ", [""])

        # Too many fields - error
        self.do_f19_test(True, 1, "D/12 345 C GREEN EXTRA  ", [
            "Too many fields in F19 'D', remove 'EXTRA'"])

        # Field 'a' error
        self.do_f19_test(True, 1, "D/123 345 C GREEN  ", [
            "Expecting number of dinghies as 1 to 2 digits instead of '123' in F19 'D'"])

        # Field 'b' error
        self.do_f19_test(True, 1, "D/12 1345 C GREEN  ", [
            "Expecting number of people that can be carried in total in all dinghies as 1 to 3 "
            "digits instead of '1345' in F19 'D'"])

        # Field 'c' error
        self.do_f19_test(True, 1, "D/12 13 D GREEN  ", [
            "Expecting 'C' to indicate dinghies are covered instead of 'D' in F19 'D'"])

        # Field 'd' error
        self.do_f19_test(True, 1, "D/12 13 C GR%EEN  ", [
            "Expecting the colour of the dinghies instead of 'GR%EEN' in F19 'D'"])

    def test_parse_f19_e(self):
        # OK
        self.do_f19_test(False, 0, "   E   /   1234 ", [""])

        # Invalid time value - error
        self.do_f19_test(True, 1, "   E   /   1260", [
            "Expecting fuel endurance in HHMM format instead of '   1260' in F19 'E'"])

    def test_parse_f19_j(self):
        # OK
        self.do_f19_test(False, 0, "J/F", [""])
        self.do_f19_test(False, 0, "J/L", [""])
        self.do_f19_test(False, 0, "J/U", [""])
        self.do_f19_test(False, 0, "J/V", [""])
        self.do_f19_test(False, 0, "J/FL", [""])
        self.do_f19_test(False, 0, "J/LU", [""])
        self.do_f19_test(False, 0, "J/UV", [""])
        self.do_f19_test(False, 0, "J/VULF", [""])
        self.do_f19_test(False, 0, "J/LFU", [""])
        self.do_f19_test(False, 0, "J/UVFL", [""])

        # Invalid character - error
        self.do_f19_test(True, 1, "J/X", [
            "Expecting life jacket equipment as one or more of 'F', 'L', 'U' or 'V' "
            "indicators instead of 'X' in F19 'J'"])
        # Invalid character - error
        self.do_f19_test(True, 1, "J/FXV", [
            "Expecting life jacket equipment as one or more of 'F', 'L', 'U' or 'V' "
            "indicators instead of 'FXV' in F19 'J'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "J/FF", [
            "Expecting life jacket equipment as one or more of 'F', 'L', 'U' or 'V' "
            "indicators instead of 'FF' in F19 'J'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "J/FLL", [
            "Expecting life jacket equipment as one or more of 'F', 'L', 'U' or 'V' "
            "indicators instead of 'FLL' in F19 'J'"])

    def test_parse_f19_n(self):
        # OK
        self.do_f19_test(False, 0, "   N   /   PLAIN LANGUAGE SURVIVAL AND OTHER REMARKS 123 ", [""])

        # Illegal character - error
        self.do_f19_test(True, 1, "N/PLAIN. LANGUAGE SURVIVAL AND OTHER REMARKS 123 ", [
            "Expecting other survival equipment and useful remarks (A-Z, 1-9 and spaces) instead "
            "of 'PLAIN. LANGUAGE SURVIVAL AND OTHER REMARKS 123' in F19 'N'"])

    def test_parse_f19_p(self):
        # OK
        self.do_f19_test(False, 0, "   P   /   1", [""])
        self.do_f19_test(False, 0, "   P   /   12", [""])
        self.do_f19_test(False, 0, "   P   /   123", [""])

        # Too many digits - error
        self.do_f19_test(True, 1, "P/1234", [
            "Expecting number of passengers on board as 1 to 3 digits instead of '1234' in F19 'P'"])

        # Non digit included - error
        self.do_f19_test(True, 1, "P/12V", [
            "Expecting number of passengers on board as 1 to 3 digits instead of '12V' in F19 'P'"])

        # Too many fields
        self.do_f19_test(True, 1, "P/12 EXTRA", [
            "Only one field expected in F19 'P' as 1 to 3 digits instead of '12 EXTRA'"])

    def test_parse_f19_r(self):
        # OK
        self.do_f19_test(False, 0, "R/E", [""])
        self.do_f19_test(False, 0, "R/U", [""])
        self.do_f19_test(False, 0, "R/V", [""])
        self.do_f19_test(False, 0, "R/EV", [""])
        self.do_f19_test(False, 0, "R/UV", [""])
        self.do_f19_test(False, 0, "R/VUE", [""])
        self.do_f19_test(False, 0, "R/EVU", [""])
        self.do_f19_test(False, 0, "R/UVE", [""])

        # Invalid character - error
        self.do_f19_test(True, 1, "R/X", [
            "Expecting frequency availability on board as one or more of 'E', "
            "'U' or 'V' instead of 'X' in F19 'R'"])
        # Invalid character - error
        self.do_f19_test(True, 1, "R/EXV", [
            "Expecting frequency availability on board as one or more of 'E', "
            "'U' or 'V' instead of 'EXV' in F19 'R'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "R/EE", [
            "Expecting frequency availability on board as one or more of 'E', "
            "'U' or 'V' instead of 'EE' in F19 'R'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "R/EVV", [
            "Expecting frequency availability on board as one or more of 'E', "
            "'U' or 'V' instead of 'EVV' in F19 'R'"])

    def test_parse_f19_s(self):
        # OK
        self.do_f19_test(False, 0, "S/D", [""])
        self.do_f19_test(False, 0, "S/J", [""])
        self.do_f19_test(False, 0, "S/M", [""])
        self.do_f19_test(False, 0, "S/P", [""])
        self.do_f19_test(False, 0, "S/DJ", [""])
        self.do_f19_test(False, 0, "S/JM", [""])
        self.do_f19_test(False, 0, "S/MP", [""])
        self.do_f19_test(False, 0, "S/PMJD", [""])
        self.do_f19_test(False, 0, "S/JDM", [""])
        self.do_f19_test(False, 0, "S/MPDJ", [""])

        # Invalid character - error
        self.do_f19_test(True, 1, "S/X", [
            "Expecting survival equipment on board as one or more of "
            "'D', 'J', 'M' or 'P' instead of 'X' in F19 'S'"])
        # Invalid character - error
        self.do_f19_test(True, 1, "S/DXP", [
            "Expecting survival equipment on board as one or more of "
            "'D', 'J', 'M' or 'P' instead of 'DXP' in F19 'S'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "S/DD", [
            "Expecting survival equipment on board as one or more of "
            "'D', 'J', 'M' or 'P' instead of 'DD' in F19 'S'"])
        # Valid character repeated - error
        self.do_f19_test(True, 1, "S/DJJ", [
            "Expecting survival equipment on board as one or more of "
            "'D', 'J', 'M' or 'P' instead of 'DJJ' in F19 'S'"])

    def do_f19_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F19, string_to_parse, 0, len(string_to_parse))
        pf19 = ParseF19(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf19.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
