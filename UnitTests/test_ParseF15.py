import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from F15_Parser.ExtractedRouteRecord import ExtractedRouteRecord
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF15 import ParseF15x


class TestParseF15(unittest.TestCase):

    def test_parse_f15(self):
        # Empty
        self.do_f15_test("", ["There is no route description in field 15"], [])

        # A blank string
        self.do_f15_test("   ", ["There is no route description in field 15"], [])

        # A good route
        self.do_f15_test("N0450F350 PNT B9 CAR", [""], [""])

        # Incorrect priority indicator
        self.do_f15_test("N0450F350 PNT B9 C^^^R", [""], [
                         "The element 'C^^^R' is an unrecognised Field 15 element"])

        # Incorrect priority indicator
        self.do_f15_test("312400  ", [""], [
                         "The first Field 15 element must be a SPEED/LEVEL and not '312400'"])

        # Incorrect priority indicator but first two characters are correct
        self.do_f15_test("N0450F350 PNT $%^& PNT #$%^&  181245FFX", [""],
                         ["The element '$%^&' is an unrecognised Field 15 element",
                          "The element '#$%^&' is an unrecognised Field 15 element",
                          "The element '181245FFX' is an unrecognised Field 15 element"])

        # Correct priority indicator with extra field
        self.do_f15_test("N0450F350 PNT B765 PNT H76543 FFX", [""], [
                         "The element 'H76543' is an unrecognised Field 15 element"])

    def do_f15_test(self, string_to_parse, expected_error_text, expected_f15_errors):
        # type: (str, [str], [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F15, string_to_parse, 0, len(string_to_parse))
        pf15 = ParseF15x(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf15.parse_field()
        if fpr.errors_detected():
            for i in range(0, len(fpr.get_erroneous_fields())):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
            return fpr
        #  fpr.get_extracted_route_sequence().print_ers()
        if fpr.f15_errors_exist():
            #  print("Number of F15 errors: " + str(fpr.get_extracted_route_sequence().get_number_of_errors()))
            #  print("F15 errors: " + fpr.get_extracted_route_sequence().get_all_errors()[0].get_error_text())
            f15_error_records: [ExtractedRouteRecord] = fpr.get_f15_errors()
            idx = 0
            for error_record in f15_error_records:
                #  print("F15 errors: " + error_record.get_error_text())
                self.assertEqual(expected_f15_errors[idx], error_record.get_error_text())
                idx += 1
        return fpr


if __name__ == '__main__':
    unittest.main()
