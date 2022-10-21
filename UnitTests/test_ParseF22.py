import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF18 import ParseF18
from IcaoMessageParser.ParseF19 import ParseF19
from IcaoMessageParser.ParseF22 import ParseF22


class TestParseF22(unittest.TestCase):

    def test_parse_f22(self):
        #     F22_f3 = auto()
        #     F22_f5 = auto()
        #     F22_f7 = auto()
        #     F22_f8 = auto()
        #     F22_f9 = auto()
        #     F22_f10 = auto()
        #     F22_f13 = auto()
        #     F22_f14 = auto()
        #     F22_f15 = auto()
        #     F22_f16 = auto()
        #     F22_f17 = auto()
        #     F22_f18 = auto()
        #     F22_f19 = auto()
        #     F22_f20 = auto()
        #     F22_f21 = auto()
        #     F22_f22 = auto()
        self.do_f22_test(True, 1, "",
                         ["No data in field 22, expecting <field 22 ICAO field number>/<ICAO field>"])

        self.do_f22_test(True, 1, "  -   ",
                         ["No data in field 22, expecting <field 22 ICAO field number>/<ICAO field>"])

        self.do_f22_test(True, 1, "-/",
                         ["Expecting <field 22 ICAO field number>/<ICAO field> instead of '/'"])

        self.do_f22_test(True, 1, "  -/XXX  ",
                         ["Expecting <field 22 ICAO field number>/<ICAO field> instead of '/XXX  '"])

        self.do_f22_test(True, 1, "-0",
                         ["Expecting <field 22 ICAO field number>/<ICAO field> instead of '0'"])

        self.do_f22_test(True, 1, "  - /   3",
                         ["Field 22 ICAO field number ' /   3' unrecognised"])

        self.do_f22_test(True, 1, "5", ["Expecting <field 22 ICAO field number>/<ICAO field> instead of '5'"])

        self.do_f22_test(True, 1, "5/", ["Expecting data following field 22 ICAO field number '5/'"])

        self.do_f22_test(False, 0, "8/9/B737/M ", [""])

        self.do_f22_test(True, 1, "-8/-9/B737/M", ["Expecting data following field 22 ICAO field number '8/'"])

        self.do_f22_test(True, 1, "-7/TEST01-8/-9/B737/M",
                         ["Expecting data following field 22 ICAO field number '8/'"])

        self.do_f22_test(False, 0, "-7/TEST - 8 / IS - 9 / B737/M", [
            "Field 19 Keyword 'X/DATA' unrecognised", ""])

        self.do_f22_test(True, 1, "-7/TEST - 11 / IS - 9 / B737/M",
                         ["Field 22 ICAO field number ' 11 / IS ' unrecognised"])

        self.do_f22_test(True, 1, "-7/TEST - 8 / IS - 9 / B737/M - 11", [
            "Expecting <field 22 ICAO field number>/<ICAO field> instead of ' 11'"])

        self.do_f22_test(True, 1, "-7/TEST - 8 / IS - 9 / B737/M-11/", [
            "Field 22 ICAO field number '11/' unrecognised"])

        self.do_f22_test(True, 1, "-7/TEST - 8 / IS - 9 / B737/M-11/SOMETHING", [
            "Field 22 ICAO field number '11/SOMETHING' unrecognised"])

        fpr = self.do_f22_test(False, 0,
                               "-3/FPL-7/TEST01-8/IS-9/B737/M-10/S/C-13/LOWW0800-15/N0450F350 PNT-16/EGLL0200-18/0",
                               [""])

        self.assertEqual("FPL", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f3).get_field_text())
        self.assertEqual("TEST01", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f7).get_field_text())
        self.assertEqual("IS", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f8).get_field_text())
        self.assertEqual("B737/M", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f9).get_field_text())
        self.assertEqual("S/C", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f10).get_field_text())
        self.assertEqual("LOWW0800", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f13).get_field_text())
        self.assertEqual("N0450F350 PNT", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f15).get_field_text())
        self.assertEqual("EGLL0200", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f16).get_field_text())
        self.assertEqual("0", fpr.get_icao_subfield(
            FieldIdentifiers.F22, SubFieldIdentifiers.F22_f18).get_field_text())

    def do_f22_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F22, string_to_parse, 0, len(string_to_parse))
        pf22 = ParseF22(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf22.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
