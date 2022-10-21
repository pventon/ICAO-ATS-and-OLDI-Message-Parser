import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF18 import ParseF18
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

        self.do_f19_test(True, 1, "E/", ["Expecting data following field 19 keyword 'E/'"])

        self.do_f19_test(True, 1, "N/P/DIDDLY TRASH ", [
            "Expecting data following field 19 keyword 'N/'", ""])

        self.do_f19_test(False, 0, "P/VALID DATA1 X ", [""])

        self.do_f19_test(True, 1, "R/VALID DATA2 X/ ", [
            "Field 19 Keyword 'X/' unrecognised"])

        self.do_f19_test(True, 1, "S/VALID DATA3 X/DATA ", [
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(False, 0, "A/VALID DATA4 X C/VALID DATA ", [""])

        self.do_f19_test(True, 1, "A/VALID DATA5 X/ C/VALID DATA ", [
            "Field 19 Keyword 'X/' unrecognised", ""])

        self.do_f19_test(True, 1, "A/VALID DATA6 X/DATA C/VALID DATA ", [
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(True, 1, "D/VALID DATA7 S Y/DATA C/VALID DATA ", [
            "Field 19 Keyword 'Y/DATA' unrecognised"])

        self.do_f19_test(True, 2, "N/VALID DATA8 Y/ X/DATA A/VALID DATA ", [
            "Field 19 Keyword 'Y/' unrecognised",
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(True, 2, "A/VALID DATA9 Y/DATA X/DATA S/VALID DATA ", [
            "Field 19 Keyword 'Y/DATA' unrecognised",
            "Field 19 Keyword 'X/DATA' unrecognised"])

        self.do_f19_test(False, 0, "S/S 1 S/S 2 S/S 3", [""])

        fpr = self.do_f19_test(False, 0, "S/S 1 S/S 2 S/S 3 "
                                         "A/A 1 A/A 2 A/A 3 "
                                         "N/N DATA P/P DATA R/R DATA", [""])
        self.assertEqual("A 2", fpr.get_all_icao_subfields(
            FieldIdentifiers.F19, SubFieldIdentifiers.F19a)[1].get_field_text())
        self.assertEqual(None, fpr.get_all_icao_subfields(
            FieldIdentifiers.F19, SubFieldIdentifiers.F19c))

        self.do_f19_test(True, 2, "C/H/GARBAGE J/J DATA", [
            "Expecting data following field 19 keyword 'C/'",
            "Field 19 Keyword 'H/GARBAGE' unrecognised"])

        self.do_f19_test(True, 2,
                         "/A/SOMETHING MORE FIELDS J/DIDDLY TRASH HHH/GARBAGE N/REMARK "
                         "R/A DEST FIELD C/SECOND C",
                         ["Expecting field 19 keyword/data instead of '/'",
                          "Field 19 Keyword 'HHH/GARBAGE' unrecognised"])

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
