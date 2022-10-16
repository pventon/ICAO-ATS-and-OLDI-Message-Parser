import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseFilingTime import ParseFilingTime


class TestFilingTime(unittest.TestCase):

    def test_parse_filing_time(self):
        # Empty
        self.do_filing_time_test(True, 1, "", ["The message filing time is missing, should contain DTG as DDHHMM"])

        # A blank string
        self.do_filing_time_test(True, 1, "   ", ["The message filing time is missing, should contain DTG as DDHHMM"])

        # Incorrect priority indicator
        self.do_filing_time_test(True, 1, " 322359", ["Expecting filing time in DDHHMM format instead of '322359'"])

        # Incorrect priority indicator
        self.do_filing_time_test(True, 1, "  312360", ["Expecting filing time in DDHHMM format instead of '312360'"])

        # Incorrect priority indicator
        self.do_filing_time_test(True, 1, "312400  ", ["Expecting filing time in DDHHMM format instead of '312400'"])

        # Incorrect priority indicator but first two characters are correct
        self.do_filing_time_test(True, 1, "  181245FFX",
                                 ["Expecting filing time in DDHHMM format instead of '181245FFX'"])

        # Correct priority indicator with extra field
        self.do_filing_time_test(True, 1, "181245 X", ["Remove the extra field(s) 'X' in the filing time field"])

        # Correct priority indicator with extra fields
        self.do_filing_time_test(True, 1, "181245 X FFF HHH",
                                 ["Remove the extra field(s) 'X FFF HHH' in the filing time field"])

        # All OK
        self.do_filing_time_test(False, 0, "  062134  ", [""])

    def do_filing_time_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.FILING_TIME, string_to_parse, 0, len(string_to_parse))
        pf_filing_time = ParseFilingTime(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf_filing_time.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
