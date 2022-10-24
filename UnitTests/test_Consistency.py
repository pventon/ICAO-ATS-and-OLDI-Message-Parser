import unittest

from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class ConsistencyTests(unittest.TestCase):

    def test_consistency_flight_rules_ok(self):

        # Flight rules in F8a match those derived in F15
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-0)", [""])

        self.do_test(False, 0, "(FPL-TEST01-VS-B737/M-S/C-LOWW0800"
                               "-N0450VFR FREE TEXT"
                               "-EDDF0200-0)", [""])

        self.do_test(False, 0, "(FPL-TEST01-ZS-B737/M-S/C-LOWW0800"
                               "-N0450VFR FREE TEXT IFR PNT/N0300F350 AAA B9 BBB"
                               "-EDDF0200-0)", [""])

        self.do_test(False, 0, "(FPL-TEST01-YS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB PNT/N0100VFR FREE TEXT"
                               "-EDDF0200-0)", [""])

    def test_consistency_flight_rules_nok(self):

        # Flight rules in F8a do not match those derived in F15
        self.do_test(True, 1, "(FPL-TEST01-VS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)",
                     ["Flight rules derived from field 15 ('IFR') differ from the rules given in field 8"])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450VFR FREE TEXT"
                              "-EDDF0200-0)",
                     ["Flight rules derived from field 15 ('VFR') differ from the rules given in field 8"])

        self.do_test(True, 1, "(FPL-TEST01-YS-B737/M-S/C-LOWW0800"
                              "-N0450VFR FREE TEXT IFR PNT/N0300F350 AAA B9 BBB"
                              "-EDDF0200-0)",
                     ["Flight rules derived from field 15 ('Z') differ from the rules given in field 8"])

        self.do_test(True, 1, "(FPL-TEST01-ZS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB PNT/N0100VFR FREE TEXT"
                              "-EDDF0200-0)",
                     ["Flight rules derived from field 15 ('Y') differ from the rules given in field 8"])

    def test_consistency_flight_rules_corrupt(self):

        # Flight rules missing in F8a
        self.do_test(True, 2, "(FPL-TEST01-#S-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)",
                     ["Expecting flight rules 'I', 'V', 'Y' or 'Z' instead of '#'",
                      "Field 15 infers flight rule is 'IFR', but rules are missing in Field 8;"])

        # Unable to derive rules from field 15
        self.do_test(True, 1, "(FPL-TEST01-VS-B737/M-S/C-LOWW0800"
                              "-*"
                              "-EDDF0200-0)",
                     ["Flight rules derived from field 15 ('IFR') differ from the rules given in field 8"])

    def test_consistency_flight_rules_pbn_d(self):
        # Field 18 contains a PBN subfield with one or more of the identifiers B1|B3|B4|C1|C3|C4|D1|D3|D4|O1|O3|O4,
        # then field 10a must contain a 'D'
        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1C3",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', 'C4', "
                      "'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'"])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1D3)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', 'C4', "
                      "'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'"])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1O3)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', 'C4', "
                      "'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'"])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-D/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1C3O3)", [""])

    def test_consistency_flight_rules_pbn_g(self):
        # Field 18 contains a PBN subfield with one or more of the identifiers B1|B2|C1|C2|D1|D2|O1|O2,
        # then field 10a must contain a 'G'
        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1C2)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2',"
                      " 'O1' or 'O2', therefore F10a must contain the letter 'G'"])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1D2)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2',"
                      " 'O1' or 'O2', therefore F10a must contain the letter 'G'"])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1O2)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2',"
                      " 'O1' or 'O2', therefore F10a must contain the letter 'G'"])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-GS/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1C2D2O2)", [""])

    def test_consistency_flight_rules_pbn_i(self):
        # Field 18 contains a PBN subfield with one or more of the identifiers B1|B5|C1|C4|D1|D4|O1|O4,
        # then field 10a must contain an 'I'
        self.do_test(True, 2, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1B5)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', "
                      "'D4', 'O1' or 'O4', therefore F10a must contain the letter 'I'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5', "
                      "therefore F10a must contain the letter 'R'"])

        self.do_test(True, 2, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1C4)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', "
                      "'C4', 'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', "
                      "'D4', 'O1' or 'O4', therefore F10a must contain the letter 'I'"])

        self.do_test(True, 2, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1D4)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', "
                      "'C4', 'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', "
                      "'D4', 'O1' or 'O4', therefore F10a must contain the letter 'I'"])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-IRS/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1B5)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', "
                      "'D4', 'O1' or 'O4', therefore F10a must contain the letter 'I'"])

    def test_consistency_flight_rules_pbn_o_s(self):
        # Field 18 contains a PBN subfield with one or more of the identifiers B1|B44,
        # then field 10a must contain an 'O' or 'S'
        self.do_test(True, 3, "(FPL-TEST01-IS-B737/M-RS/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1B1)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', "
                      "'C4', 'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', "
                      "'O1' or 'O2', therefore F10a must contain the letter 'G'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', 'D4', "
                      "'O1' or 'O4', therefore F10a must contain the letter 'I'"])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-DGIRS/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1B1)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B3', 'B4', 'C1', 'C3', "
                      "'C4', 'D1', 'D3', 'D4', 'O1', 'O3' or 'O4', therefore F10a must contain the letter 'D'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', "
                      "'O1' or 'O2', therefore F10a must contain the letter 'G'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', 'D4', "
                      "'O1' or 'O4', therefore F10a must contain the letter 'I'"])

    def test_consistency_flight_rules_pbn_r(self):
        # Field 18 contains a PBN subfield with one or more of the identifiers B[1-5],
        # then field 10a must contain an 'R'
        self.do_test(True, 2, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/A1B2)",
                     ["Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', "
                      "'D2', 'O1' or 'O2', therefore F10a must contain the letter 'G'",
                      "Field 18 'PBN' contains one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5', "
                      "therefore F10a must contain the letter 'R'"])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-GRS/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1B2)", [""])

    def test_consistency_flight_rules_10a_r(self):

        # Field 10a contains an 'R' but F18 PBN subfield is missing
        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-R/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)",
                     ["Field 10a contains an 'R', therefore field 18 must contain the subfield 'PBN' "
                      "with one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5'"])

        # Field 10a contains an 'R' but F18 PBN is missing a B[1-5] indicator
        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-GR/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-PBN/B6C2)",
                     ["Field 10a contains an 'R', therefore field 18 must contain the subfield 'PBN' "
                      "with one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5'",
                      ""])

        # Field 10a contains an 'R' and F18 PBN contains a B[1-5] indicator
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-DGR/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-PBN/A1B3C2)", [""])

    def test_consistency_flight_rules_10a_z(self):

        # Field 10a contains an 'Z' but F18 subfields are missing
        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-Z/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)",
                     ["Field 10a contains a 'Z', therefore field 18 must contain one of the "
                      "subfields 'COM', 'NAV' or 'DAT'"])

        # Field 10a contains an 'Z' and F18 COM
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-Z/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-COM/ABC)", [""])

        # Field 10a contains an 'Z' and F18 NAV
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-Z/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-NAV/ABC)", [""])

        # Field 10a contains an 'Z' and F18 DAT
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-Z/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-DAT/ABC)", [""])

    def test_consistency_9b_typ(self):

        # Field 9b contains 'ZZZZ', F18 TYP subfield must be present
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-TYP/A320)", [""])

        self.do_test(False, 0, "(FPL-TEST01-IS-ZZZZ/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-TYP/A320)", [""])

        self.do_test(True, 1, "(FPL-TEST01-IS-ZZZZ/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)", ["Field 9b contains 'ZZZZ' and the field 18 'TYP' subfield "
                                               "is missing, enter a 'TYP' subfield in field 18."])

    def test_consistency_13a_dep(self):

        # Field 13a contains 'ZZZZ', F18 DEP subfield must be present
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-DEP/DEPARTURE AIRPORT)", [""])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-ZZZZ0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-DEP/DEPARTURE AIRPORT)", [""])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-ZZZZ0800"
                              "-N0450F350 AAA B9 BBB"
                              "-EDDF0200-0)", ["Field 13a contains 'ZZZZ' and the field 18 'DEP' subfield "
                                               "is missing, enter a 'DEP' subfield in field 18."])

    def test_consistency_16a_dest(self):

        # Field 16a contains 'ZZZZ', F18 DEST subfield must be present
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-DEST/DESTINATION AIRPORT)", [""])

        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                               "-N0450F350 AAA B9 BBB"
                               "-EDDF0200-DEST/DESTINATION AIRPORT)", [""])

        self.do_test(True, 1, "(FPL-TEST01-IS-B737/M-S/C-LOWW0800"
                              "-N0450F350 AAA B9 BBB"
                              "-ZZZZ0200-0)", ["Field 16a contains 'ZZZZ' and the field 18 'DEST' subfield "
                                               "is missing, enter a 'DEST' subfield in field 18."])

    def do_test(self, errors_detected, number_of_errors, message_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        pm = ParseMessage()
        pm.parse_message(fpr, message_to_parse)
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
