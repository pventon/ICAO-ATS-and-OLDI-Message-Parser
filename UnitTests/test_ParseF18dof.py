import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF18dof import ParseF18dof
from IcaoMessageParser.ParsePriorityIndicator import ParsePriorityIndicator
from Tokenizer.Token import Token


class TestParseF18dof(unittest.TestCase):

    def test_parse_f18dof(self):
        # Empty
        self.do_f18dof_test(True, 1, "", ["There is no data in field 18"])

        # A blank string
        self.do_f18dof_test(True, 1, "     ", ["There is no data in field 18"])

        # Incorrect DOF
        self.do_f18dof_test(True, 1, "A", ["Expecting DOF in the format YYMMDD instead of 'A'"])

        # Incorrect DOF
        self.do_f18dof_test(True, 1, "  X6X", ["Expecting DOF in the format YYMMDD instead of 'X6X'"])

        # Correct DOF
        self.do_f18dof_test(False, 0, "221103", [""])

        # Correct DOF with extra fields
        self.do_f18dof_test(True, 1, "221103 DDD GREGG UUUU", [
            "Invalid characters for alternate aerodrome text, should be 'A' to 'Z' and "
            "'0' to '9' only instead of 'DDD GREGG UUUU'"])

        # Incorrect DOF syntax
        self.do_f18dof_test(True, 1, "   220D29   ", ["Expecting DOF in the format YYMMDD instead of '220D29'"])

        # Incorrect DOF syntax, month > 13
        self.do_f18dof_test(True, 1, "   221303   ", ["Expecting DOF in the format YYMMDD instead of '221303'"])

        # Incorrect DOF syntax days > 31
        self.do_f18dof_test(True, 1, "   221232   ", ["Expecting DOF in the format YYMMDD instead of '221232'"])

        # Incorrect DOF syntax, February day > 28
        self.do_f18dof_test(True, 1, "   220229   ", ["Expecting DOF in the format YYMMDD instead of '220229'"])

    def do_f18dof_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F18_DOF, string_to_parse, 0, len(string_to_parse))
        pf18dof = ParseF18dof(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf18dof.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
