import unittest

from Configuration.EnumerationConstants import AdjacentUnits, FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF3 import ParseF3


class TestParseF3(unittest.TestCase):

    def test_parse_field3(self):
        # Empty
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "",
                        ["No ATS message title identified in this message"])

        # Empty string
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "     ",
                        ["No ATS message title identified in this message"])

        # Too short
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FP",
                        ["Message title 'FP' unrecognized, cannot process this message"])

        # OK
        self.do_f3_test(False, 0, AdjacentUnits.DEFAULT, "FPL", [""])

        # Invalid syntax
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FP9",
                        ["Message title 'FP9' unrecognized, cannot process this message"])

        # Only part of F3b present
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLA",
                        ["Expecting sender/receiver adjacent unit name and sequence "
                         "number instead of 'A'"])

        # Only part of F3b present
        self.do_f3_test(True, 1, AdjacentUnits.AA, "FPLAA/",
                        ["Expecting sender/receiver adjacent unit name and sequence "
                         "number instead of 'AA/'"])

        # Only part of F3b present
        self.do_f3_test(True, 1, AdjacentUnits.AA, "FPLAA/B",
                        ["Expecting sender/receiver adjacent unit name and sequence "
                         "number instead of 'AA/B'"])

        # Only part of F3b present
        self.do_f3_test(True, 1, AdjacentUnits.AA, "  FPLAA/BB00",
                        ["Expecting channel sequence number as 3 digits instead '00'"])

        # One Tx / Rx unit is OK
        self.do_f3_test(False, 0, AdjacentUnits.DEFAULT, "  FPLAAA/BBB001", [])

        # 2nd Tx / Rx Too short
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLABC/DEF001HB",
                        ["Expecting sender/receiver adjacent unit name and sequence "
                         "number instead of 'HB'"])

        # 2nd Tx / Rx Too short
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "ARRGH/OP023KL/",
                        ["Expecting sender/receiver adjacent unit name and sequence "
                         "number instead of 'KL/'"])

        # 2nd Tx / Rx Too short
        self.do_f3_test(True, 2, AdjacentUnits.DEFAULT, "FPLPO/JUY123KL/4",
                        ["Expecting adjacent unit receiver name as 1 to 4 letters instead of '4'",
                         "Expecting sender/receiver adjacent unit name and sequence number instead of 'KL/4'"])

        # 2nd Tx / Rx OK
        self.do_f3_test(False, 0, AdjacentUnits.DEFAULT, "FPLRTH/SW999ZZ/D560", [""])

        # Invalid characters in Tx / Rx
        self.do_f3_test(True, 2, AdjacentUnits.DEFAULT, "FPLRTH/SW989Z*/H560",
                        ["Expecting adjacent unit sender name as 1 to 4 letters instead of 'Z*'",
                         "Expecting sender/receiver adjacent unit name and sequence number instead of 'Z*/H 560'"])

        # Invalid characters in Tx / Rx
        self.do_f3_test(True, 2, AdjacentUnits.DEFAULT, "FPLRTH/SW!Y9ZZ/U560",
                        ["Expecting adjacent unit receiver name as 1 to 4 letters instead of 'SW!Y'",
                         "Expecting sender/receiver adjacent unit name and sequence number "
                         "instead of 'RTH/SW!Y 9 ZZ/U 560'"])

        # Last Tx / Rx is too long
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLRTH/SWY900ZZ/L5600",
                        ["Expecting channel sequence number as 3 digits instead '5600'"])

        # Extra field at end
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLRTH/SWY900KK/L560 EXTRA",
                        ["Field 3 is correct, the extra fields 'EXTRA' should be removed"])

        # Extra field at end
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLRTH/SWY900KK/L560 EXTRA MORE EXTRA",
                        ["Field 3 is correct, the extra fields 'EXTRA MORE EXTRA' should be removed"])

        # Extra field at end
        self.do_f3_test(True, 2, AdjacentUnits.DEFAULT, "FPLRTH/SWY900 EXTRA MORE EXTRA",
                        ["Expecting adjacent unit sender name as 1 to 4 letters instead of 'EXTRA'",
                         "Expecting sender/receiver adjacent unit name and sequence number "
                         "instead of 'EXTRA MORE EXTRA'"])

        # Extra field at end
        self.do_f3_test(True, 1, AdjacentUnits.DEFAULT, "FPLRTH/SWY EXTRA MORE EXTRA",
                        ["Expecting channel sequence number as 3 digits instead 'EXTRA'"])

    def do_f3_test(self, errors_detected, number_of_errors, expected_adj_unit,
                   string_to_parse, expected_error_text):
        # type: (bool, int, AdjacentUnits, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F3, string_to_parse, 0, len(string_to_parse))
        pf3 = ParseF3(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf3.parse_field()
        self.assertEqual(expected_adj_unit, fpr.get_sender_adjacent_unit_name())
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
