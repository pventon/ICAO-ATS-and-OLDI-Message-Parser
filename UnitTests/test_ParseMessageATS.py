import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class ParseMessageTests(unittest.TestCase):

    def test_ParseMessageATS_General(self):

        # Too many fields
        self.do_test(True, 1, "(FPL-TEST01-IS\n"
                              "-B737/M-S/C\n"
                              "-LOWW0800\r"
                              "-N0450F350 AAA B9 BBB\t"
                              "-EDDF0200\n"
                              "-0-F19-EXTRA FIELD)",
                     ["Too many fields in this message, the field 'EXTRA FIELD' "
                      "is superfluous; check placement of hyphens"])

        # Too few fields
        self.do_test(True, 1, "(FPL-TEST02-IS\n"
                              "-B737/M-S/C\n"
                              "-LOWW0800\n"
                              "-N0450F350 AAA B9 BBB\n"
                              "-EDDF0200)",
                     ["Too few fields in this message; expecting at least 10 fields"])

        # One field too short on optional field, field 19 missing but this is optional
        self.do_test(False, 0, "(FPL-TEST03-IS\n"
                               "-B737/M-S/C\n"
                               "-LOWW0800\n"
                               "-N0450F350 AAA B9 BBB\n"
                               "-EDDF0200\n"
                               "-0)", [""])

    def test_ParseMessage_ATS_check_configuration(self):
        # ATS Messages
        self.do_test(False, 0, "(ACH-TEST01-EGLL0800-LOWW0200-221012-16/EGFF0130)", [""])
        self.do_test(False, 0, "(ACP-TEST01-EGLL0800-LOWL0100 LOWZ LOWG)", [""])
        self.do_test(False, 0,
                     "(AFP-TEST01-IS-B737/M-S/C-EGLL0800-PNT/1234F350F200A-N0450F350 "
                     "PNT B9 NMB-LOWL0100 LOWZ LOWG-0-E/1235)",
                     [""])
        self.do_test(False, 0,
                     "(ALR-INCERFA/ABCDEFGH/FREE TEXT-TEST01-IS-B737/M-S/C-EGLL0800-N0450F350 "
                     "PNT B9 NMB-LOWL0100 LOWZ LOWG-0-E/2131-SOME JUNK FOR FIELD 20)",
                     [""])
        self.do_test(False, 0,
                     "(APL-TEST01-IS-B737/M-S/C-EGLL0800-PNT/1234F350F200A-N0450F350 PNT B9 "
                     "NMB-LOWL0100 LOWZ LOWG-0-E/1235)",
                     [""])
        self.do_test(False, 0, "(ARR-TEST01-EGLL0800-LOWW0200-RGRG0200 DEN HELDER-221013)", [""])
        self.do_test(False, 0, "(CDN-TEST01-EGLL0800-LOWL0100 LOWZ LOWG-221013)", [""])
        self.do_test(False, 0, "(CHG-TEST01-EGLL0800-LOWW0200-221012-16/EGFF0130)", [""])
        self.do_test(False, 0, "(CNL-TEST01-EGLL0800-LOWL-221013)", [""])
        self.do_test(False, 0,
                     "(CPL-TEST01-IS-B737/M-S/C-EGLL0800-PNT/1234F350F200A-N0450F350 PNT B9 NMB-LOWL0100 LOWZ LOWG-0)",
                     [""])
        self.do_test(False, 0, "(DEP-TEST01-EGLL0800-LOWL-221013)", [""])
        self.do_test(False, 0, "(DLA-TEST01-EGLL0800-LOWL-221013)", [""])
        self.do_test(False, 0, "(EST-TEST01-EGLL0800-PNT/1234F350F200A-LOWL0100 LOWZ LOWG)", [""])
        self.do_test(False, 0, "(FPL-TEST01-IS-B737/M-S/C-EGLL0800-N0450F350 PNT B9 NMB-LOWL0100 LOWZ LOWG-0-E/1235)",
                     [""])
        self.do_test(False, 0, "(FNM-TEST01-B737/M-PETE-N0450F350 PNT B9 NMB-LOWL-0-E/1235)", [""])
        self.do_test(False, 0, "(MFS-TEST01-B737/M-PETE-PNT/1234F350F200A-LOWL-DFG56TH)", [""])
        self.do_test(False, 0, "(RCF-TEST01-FIELD 21 DATA)", [""])
        self.do_test(False, 0, "(RQP-TEST01-EGLL0800-LOWL-221013)", [""])
        self.do_test(False, 0, "(RQS-TEST01-LOWW0800-EGLL0200-0)", [""])
        self.do_test(False, 0, "(SPL-TEST01-EGLL0800-LOWL0100 LOWZ LOWG-0-E/1235)", [""])

        # DEFAULT Adjacent unit
        self.do_test(False, 0, "(ABI-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/BERT0900)", [""])
        self.do_test(False, 0, "(ACPXX/YY234)", [""])
        self.do_test(False, 0, "(ACT-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(AMA-TEST01-SAGE-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(CDN-TEST01-SAGE0900-LOWL0200-221013)", [""])
        self.do_test(False, 0, "(COD - TEST01 - EGLL0800 - LOWL)", [""])
        self.do_test(False, 0, "(CPLCV/HB001-TEST01-EGLL0800-LOWW0200-221012-13/KATE0900)", [""])
        self.do_test(False, 0, "(INF-TEST01-SAGE-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(LAMZZ/TT654)", [""])
        self.do_test(False, 0, "(MAC-TEST01-SAGE-HELP-LOWL)", [""])
        self.do_test(False, 0, "(OCM-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(PAC-TEST01-LOWL-EGLL-9/B737/M)", [""])
        self.do_test(False, 0, "(RAP-TEST01-SAGE-PNT/1234F350F200A-LOWL-221012-13/KATE0900)", [""])
        self.do_test(False, 0, "(REJ-TEST01-SAGE-LOWL-0)", [""])
        self.do_test(False, 0, "(REV-TEST01-SAGE-PNT/1234F350F200A-LOWL)", [""])
        self.do_test(False, 0, "(RJCVV/MM011GG/KK022)", [""])
        self.do_test(False, 0, "(ROC-TEST01-16/EGFF0130-SAGE-PNT/1234F350F200A-LOWL)", [""])
        self.do_test(False, 0, "(RRV-TEST01-SAGE-PNT/1234F350F200A-LOWL)", [""])
        self.do_test(False, 0, "(SBYNN/MM999SS/AA099)", [""])

        # AA Adjacent unit
        self.do_test(False, 0, "(ABIAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(ACPAA/LL098-TEST01-SAGE-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(ACTAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(AMAAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(CDNAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(INFAA/LL098-TEST01-SAGE-EGLL-LOWL-9/B737/M 15/N0450VFR 18/DOF 220321)", [""])
        self.do_test(False, 0, "(MACAA/LL098-TEST01-SAGE-LOWL-PETE-13/KATE0900)", [""])
        self.do_test(False, 0, "(OCMAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(PACAA/LL098-TEST01-SAGE-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(RAPAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(REJAA/LL098-TEST01-SAGE-LOWL-0)", [""])
        self.do_test(False, 0, "(REVAA/LL098-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(RJCAA/LL098-13/KATE0900)", [""])
        self.do_test(False, 0, "(ROCAA/LL098-TEST01-16/EGFF0130-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])
        self.do_test(True, 1, "(ABIAX/VB001-TEST01-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)",
                     ["Message content undefined for Message Type/Adjacent Unit/Title combination Message Type: "
                      "OLDI, Adjacent Unit Name: AX, Message Title: ABI. Default configuration will be used."])
        self.do_test(True, 1,
                     "(CPLAX/VB001-TEST01-EGLL0800-LOWW0200-220430-0)",
                     ["Message content undefined for Message Type/Adjacent Unit/Title combination Message Type: "
                      "OLDI, Adjacent Unit Name: AX, Message Title: CPL. Default configuration will be used."])

        # BB Adjacent unit
        self.do_test(False, 0, "(CDNBB/XX001-TEST01-SAGE-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(INFBB/XX001-TEST01-SAGE-PNT/1234F350F200A-LOWL-221012-13/KATE0900)", [""])
        self.do_test(False, 0, "(PACBB/XX001-TEST01-EGLL0800-LOWL-13/KATE0900)", [""])
        self.do_test(False, 0, "(ROCBB/XX001-TEST01-16/EGFF0130-SAGE-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])

        # CC Adjacent unit
        self.do_test(False, 0, "(PACCC/XX001-TEST01-PNT/1234F350F200A-LOWL-13/KATE0900)", [""])

    # Ensure fields are written to the FPR and can be read back with correct indices
    def test_field_storage_in_fpr(self):
        fpr = self.do_test(
            False, 0, "(FPL-TEST01-IS-B737/M-S/C-EGLL0800-N0450F350 PNT B9 NMB-LOWL0100 LOWZ LOWG-0-E/1235)", [""])
        self.assertEqual("FPL", fpr.get_icao_field(FieldIdentifiers.F3).get_field_text())
        self.assertEqual(1, fpr.get_icao_field(FieldIdentifiers.F3).get_start_index())
        self.assertEqual(4, fpr.get_icao_field(FieldIdentifiers.F3).get_end_index())
        self.assertEqual("TEST01", fpr.get_icao_field(FieldIdentifiers.F7).get_field_text())
        self.assertEqual(5, fpr.get_icao_field(FieldIdentifiers.F7).get_start_index())
        self.assertEqual(11, fpr.get_icao_field(FieldIdentifiers.F7).get_end_index())
        self.assertEqual("IS", fpr.get_icao_field(FieldIdentifiers.F8).get_field_text())
        self.assertEqual(12, fpr.get_icao_field(FieldIdentifiers.F8).get_start_index())
        self.assertEqual(14, fpr.get_icao_field(FieldIdentifiers.F8).get_end_index())
        self.assertEqual("B737/M", fpr.get_icao_field(FieldIdentifiers.F9).get_field_text())
        self.assertEqual(15, fpr.get_icao_field(FieldIdentifiers.F9).get_start_index())
        self.assertEqual(21, fpr.get_icao_field(FieldIdentifiers.F9).get_end_index())
        self.assertEqual("S/C", fpr.get_icao_field(FieldIdentifiers.F10).get_field_text())
        self.assertEqual(22, fpr.get_icao_field(FieldIdentifiers.F10).get_start_index())
        self.assertEqual(25, fpr.get_icao_field(FieldIdentifiers.F10).get_end_index())
        self.assertEqual("EGLL0800", fpr.get_icao_field(FieldIdentifiers.F13).get_field_text())
        self.assertEqual(26, fpr.get_icao_field(FieldIdentifiers.F13).get_start_index())
        self.assertEqual(34, fpr.get_icao_field(FieldIdentifiers.F13).get_end_index())
        self.assertEqual("N0450F350 PNT B9 NMB", fpr.get_icao_field(FieldIdentifiers.F15).get_field_text())
        self.assertEqual(35, fpr.get_icao_field(FieldIdentifiers.F15).get_start_index())
        self.assertEqual(55, fpr.get_icao_field(FieldIdentifiers.F15).get_end_index())
        self.assertEqual("LOWL0100 LOWZ LOWG", fpr.get_icao_field(FieldIdentifiers.F16).get_field_text())
        self.assertEqual(56, fpr.get_icao_field(FieldIdentifiers.F16).get_start_index())
        self.assertEqual(74, fpr.get_icao_field(FieldIdentifiers.F16).get_end_index())
        self.assertEqual("0", fpr.get_icao_field(FieldIdentifiers.F18).get_field_text())
        self.assertEqual(75, fpr.get_icao_field(FieldIdentifiers.F18).get_start_index())
        self.assertEqual(76, fpr.get_icao_field(FieldIdentifiers.F18).get_end_index())
        self.assertEqual("E/1235", fpr.get_icao_field(FieldIdentifiers.F19).get_field_text())
        self.assertEqual(77, fpr.get_icao_field(FieldIdentifiers.F19).get_start_index())
        self.assertEqual(83, fpr.get_icao_field(FieldIdentifiers.F19).get_end_index())

    # Ensure subfields are written to the FPR and can be read back with correct indices
    def test_subfield_storage_in_fpr(self):
        fpr = self.do_test(
            #                    1         2         3         4         5         6
            #          0123456789012345678901234567890123456789012345678901234567890
            False, 0, "(  FPLAA/BB001CC/DD002-TEST01-IS-B737/M-S/C-EGLL0800-"
                      "N0450F350 PNT B9 NMB-LOWL0100 LOWZ LOWG-0-E/1235)", [""])
        # Check some random subfields
        #                           1         2         3         4         5         6
        #                 0123456789012345678901234567890123456789012345678901234567890
        self.assertEqual("  FPLAA/BB001CC/DD002", fpr.get_icao_field(FieldIdentifiers.F3).get_field_text())
        self.assertEqual(1, fpr.get_icao_field(FieldIdentifiers.F3).get_start_index())
        self.assertEqual(22, fpr.get_icao_field(FieldIdentifiers.F3).get_end_index())
        self.assertEqual("FPL", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3a).get_field_text())
        self.assertEqual(3, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3a).get_start_index())
        self.assertEqual(6, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3a).get_end_index())
        self.assertEqual("AA", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b1).get_field_text())
        self.assertEqual(6, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b1).get_start_index())
        self.assertEqual(8, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b1).get_end_index())
        self.assertEqual("BB", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b3).get_field_text())
        self.assertEqual(9, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b3).get_start_index())
        self.assertEqual(11, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b3).get_end_index())
        self.assertEqual("001", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b4).get_field_text())
        self.assertEqual(11, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b4).get_start_index())
        self.assertEqual(14, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3b4).get_end_index())
        self.assertEqual("CC", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c1).get_field_text())
        self.assertEqual(14, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c1).get_start_index())
        self.assertEqual(16, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c1).get_end_index())
        self.assertEqual("DD", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c3).get_field_text())
        self.assertEqual(17, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c3).get_start_index())
        self.assertEqual(19, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c3).get_end_index())
        self.assertEqual("002", fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c4).get_field_text())
        self.assertEqual(19, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c4).get_start_index())
        self.assertEqual(22, fpr.get_icao_subfield(FieldIdentifiers.F3, SubFieldIdentifiers.F3c4).get_end_index())

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
