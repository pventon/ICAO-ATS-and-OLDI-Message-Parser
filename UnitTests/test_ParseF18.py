import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF18 import ParseF18


class TestParseF18(unittest.TestCase):

    def test_parse_f18(self):
        self.do_f18_test(True, 1, "", ["No data in field 18, expecting field 18 keyword/data"])

        self.do_f18_test(True, 1, "     ", ["No data in field 18, expecting field 18 keyword/data"])

        self.do_f18_test(True, 1, "/", ["Field 18 contains no keywords, can be '0' or 'n' "
                                        "keyword/data occurrences instead of '/'"])

        self.do_f18_test(True, 1, "  XXX  ", ["Field 18 contains no keywords, can be '0' or 'n' "
                                              "keyword/data occurrences instead of 'XXX'"])

        self.do_f18_test(False, 0, "0", [""])

        self.do_f18_test(True, 1, "   /   DEP", [
            "Field 18 contains no keywords, can be '0' or 'n' keyword/data occurrences instead of '/   DEP'"])

        self.do_f18_test(True, 1, "DEP", [
            "Field 18 contains no keywords, can be '0' or 'n' keyword/data occurrences instead of 'DEP'"])

        self.do_f18_test(True, 1, "DEP/", ["Expecting data following field 18 keyword 'DEP/'"])

        self.do_f18_test(True, 1, "DEP/RALT/DIDDLY TRASH ", [
            "Expecting data following field 18 keyword 'DEP/'", ""])

        self.do_f18_test(False, 0, "DEP/VALID DATA1 XXX ", [""])

        self.do_f18_test(True, 1, "DEP/VALID DATA2 XXX/ ", [
            "Field 18 Keyword 'XXX/' unrecognised"])

        self.do_f18_test(True, 1, "DEP/VALID DATA3 XXX/DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(False, 0, "DEP/VALID DATA4 XXX DEST/VALID DATA ", [""])

        self.do_f18_test(True, 1, "DEP/VALID DATA5 XXX/ DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/' unrecognised", ""])

        self.do_f18_test(True, 1, "DEP/VALID DATA6 XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 1, "DEP/VALID DATA7 YYY XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 2, "DEP/VALID DATA8 YYY/ XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'YYY/' unrecognised",
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 2, "DEP/VALID DATA9 YYY/DATA XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'YYY/DATA' unrecognised",
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(False, 0, "RMK/REMARK 1 RMK/REMARK 2 RMK/REMARK 3", [""])

        fpr = self.do_f18_test(False, 0, "RMK/REMARK 1 RMK/REMARK 2 RMK/REMARK 3 "
                                         "STS/STS 1 STS/STS 2 STS/STS 3 "
                                         "RVR/200 SRC/SRC DATA TALT/TALT DATA", [""])
        self.assertEqual("STS 2", fpr.get_all_icao_subfields(
            FieldIdentifiers.F18, SubFieldIdentifiers.F18sts)[1].get_field_text())
        self.assertEqual(None, fpr.get_all_icao_subfields(
            FieldIdentifiers.F18, SubFieldIdentifiers.F18typ))

        self.do_f18_test(True, 2, "DEP/HHH/GARBAGE RMK/REMARK", [
            "Expecting data following field 18 keyword 'DEP/'",
            "Field 18 Keyword 'HHH/GARBAGE' unrecognised"])

        self.do_f18_test(True, 2,
                         "/DEP/SOMETHING MORE FIELDS RALT/DIDDLY TRASH HHH/GARBAGE RMK/REMARK "
                         "DEST/A DEST FIELD RMK/SECOND RMK",
                         ["Expecting field 18 keyword/data instead of '/'",
                          "Field 18 Keyword 'HHH/GARBAGE' unrecognised"])

    def do_f18_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F18, string_to_parse, 0, len(string_to_parse))
        pf18 = ParseF18(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf18.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
