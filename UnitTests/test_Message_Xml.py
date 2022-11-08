import os
import unittest

from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage
from AFTN_Terminal.ReadXml import ReadXml


class ParseMessageTests(unittest.TestCase):
    fpr: FlightPlanRecord = None
    pm = None
    file_path = "/home/ls/PycharmProjects/ICAO-Message-Parser/UnitTests/FlightPlanRecord_for_testing.xml"

    def tearDown(self) -> None:
        # self.fpr = None
        self.pm = None

    def setUp(self) -> None:
        self.fpr = FlightPlanRecord()
        self.pm = ParseMessage()

    def test_ParseMessage_01(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "241309 IJKLMNOP" + os.linesep +
                              "(FPL-TEST01" + os.linesep +
                              "-IS-B737/M" + os.linesep +
                              "-S/C-LOWW0800" + os.linesep +
                              "-N0450F350 PNT44444 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-RMK/REMARK 1 STS/STS 1 RMK/REMARK 2)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_02(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST02" + os.linesep +
                              "-VG-C172/L" + os.linesep +
                              "-S/C-EGLL0800" + os.linesep +
                              "-N0450VFR THIS IS SOME BREAK TEXT" + os.linesep +
                              "-EGAA0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_03(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST03" + os.linesep +
                              "-YG-A320/M" + os.linesep +
                              "-S/C-EGAA0800" + os.linesep +
                              "-N0450F350 PNT 23N123W VFR SOME BREAK TEXT IFR BBB/N0100F100 CCC START1A" + os.linesep +
                              "-EDDF0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_04(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST04" + os.linesep +
                              "-ZS-B747/H" + os.linesep +
                              "-S/C-EDDF0800" + os.linesep +
                              "-N0450VFR Z RULE BREAK TEXT BBB/N0200F150 PNT 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-EGLL0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_05(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST05" + os.linesep +
                              "-IS-A380/J" + os.linesep +
                              "-S/C-AAAA1000" + os.linesep +
                              "-N0450F350 LNZ1A LNZ PNT 23N123W 33N160W 35N164W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-BBBB0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_06(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST06" + os.linesep +
                              "-YG-B777/M" + os.linesep +
                              "-S/C-CCCC1200" + os.linesep +
                              "-N0450F350 PNT 23N123W 24N125W Y RULES BREAK TEXT IFR BBB/N0300F230 B9 AAA"
                              + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_07(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST07" + os.linesep +
                              "-IS-B767/M" + os.linesep +
                              "-S/C-CCCC1430" + os.linesep +
                              "-N0450F350 SID AAA B9 DDD A4" + os.linesep +
                              "-DDD0207" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_08(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST08" + os.linesep +
                              "-IS-B727/M" + os.linesep +
                              "-S/C-EEEE0800" + os.linesep +
                              "-N0450F35 PNT 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-FFFF1227" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_09(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST09" + os.linesep +
                              "-IS-B737/M" + os.linesep +
                              "-S/C-GGGG1530" + os.linesep +
                              "-N0450F350 PNT 23N123W BBB INVALID B9 AAA STAY1/ 1234" + os.linesep +
                              "-PETE0200" + os.linesep +
                              "-RMK/THIS IS A REMARK UNK/UNKNOWN SUBFIELD)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_10(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST10" + os.linesep +
                              "-IAS-B737/M" + os.linesep +
                              "-S/C-LOWW0800" + os.linesep +
                              "-N0450F350 PNT 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_11(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST11" + os.linesep +
                              "-ZS-B737/M" + os.linesep +
                              "-S/C-LOWW0800" + os.linesep +
                              "-N0450VFR THIS IS BREAK TEXT IFR NNN/N0450F350 PNT 23N123W BBB B9 AAA STAY1/ 1234"
                              + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_12(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "191916 AAAAAAAA "
                              "(DLA-TEST12-LOWW0800-LOWW0200-DOF/221210)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_13(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "191916 AAAAAAAA "
                              "(CHG-TEST13-LOWW0800-LOWW0200-DOF/221010-9/B737/M-13/AAA0912-15/N0450f350 BBB)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_14(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "191916 AAAAAAAA "
                              "(ARR-TEST14-LOWW0800-LOWW0200-SOME AIRPORT)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_15(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "191916 AAAAAAAA" + os.linesep +
                              "(CPL-TEST15" + os.linesep +
                              "-IS-B737/M" + os.linesep +
                              "-S/C-LOWW0800" + os.linesep +
                              "-PNT/1234F0100F0200B" + os.linesep +
                              "-N0450F350 AAA C54 GGG PNT 23N123W BBB B9 AAA 24N020W 24N030W 24N040W" + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_16(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST16" + os.linesep +
                              "-VS-C172/L" + os.linesep +
                              "-S/C-KSAA0800" + os.linesep +
                              "-N0450VFR GOING TO THE GOLF CLUB" + os.linesep +
                              "-KSBB1332" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_17(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST17" + os.linesep +
                              "-IS-B737/M" + os.linesep +
                              "-S/C-EGCC1635" + os.linesep +
                              "-N0450F350 AAA BBB CCC DDD EEE FFF GGG HHH III JJJ KKK" + os.linesep +
                              "-EGDD0123" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_18(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST18" + os.linesep +
                              "-IS-A330/H" + os.linesep +
                              "-S/C-LOWL1718" + os.linesep +
                              "-N0350F250 PNT 23N123W BBB/N0450f350 B9 AAA CCC DDD/N0100F200 EEE FFF STAR1S"
                              + os.linesep +
                              "-LOWS0200" + os.linesep +
                              "-0)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_19(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST19" + os.linesep +
                              "-IS-A340/H" + os.linesep +
                              "-S/C-LOWZ0800" + os.linesep +
                              "-N0450F350 PNT 23N123W INVALID BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-EGYH2345" + os.linesep +
                              "-STS/THIS IS AN STS DOF/999900)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_20(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST20000" + os.linesep +
                              "-IS-BBBB737/M" + os.linesep +
                              "-S/C-LOWW0800" + os.linesep +
                              "-N0450F350 PNT INVALID 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-LOWW0200" + os.linesep +
                              "-INVALID)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_21(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST21" + os.linesep +
                              "-IS-B727/M" + os.linesep +
                              "-S/C-EEEE0800" + os.linesep +
                              "-N0450F350 PNT 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-FFFF1227" + os.linesep +
                              "-0-E/1234 P/345 J/FU)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_22(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH" + os.linesep +
                              "191916 AAAAAAAA" + os.linesep +
                              "(FPL-TEST22" + os.linesep +
                              "-IS-B727/M" + os.linesep +
                              "-S/C-EEEE0800" + os.linesep +
                              "-N0450F350 PNT 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                              "-FFFF1227" + os.linesep +
                              "-0-E/1234 P/345 S/DMH J/FU)")
        # print(self.fpr.as_xml())

    def test_read_xml_01(self):
        rx = ReadXml(self.file_path)
        # Test modification time
        self.assertEqual("Mon Nov  7 09:55:24 2022", rx.get_modification_time())
        self.assertEqual("1667832924.69", "{0:>.2f}".format(rx.get_modification_time_seconds()))
        # Test creation time
        self.assertEqual("Mon Nov  7 09:55:24 2022", rx.get_creation_time())
        self.assertEqual("1667832924.69", "{0:>.2f}".format(rx.get_creation_time_seconds()))

    def test_read_xml_02(self):
        rx = ReadXml(self.file_path)
        # Test original message 'get'
        self.assertEqual("FF ABCDEFGH" + os.linesep +
                         "241309 IJKLMNOP" + os.linesep +
                         "(FPL-TEST01" + os.linesep +
                         "-IS-B737/M" + os.linesep +
                         "-S/C-LOWW0800" + os.linesep +
                         "-N0450F350 PNT44444 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                         "-LOWW0200" + os.linesep +
                         "-RMK/REMARK 1 STS/STS 1 RMK/REMARK 2)" + os.linesep, rx.get_original_message())

    def test_read_xml_03(self):
        rx = ReadXml(self.file_path)
        # Test get ERS errors
        self.assertEqual("The element 'PNT44444' is an unrecognised Field 15 element", rx.get_ers_errors()[0][0])
        self.assertEqual(76, rx.get_ers_errors()[0][1])
        self.assertEqual(84, rx.get_ers_errors()[0][2])

    def test_read_xml_04(self):
        rx = ReadXml(self.file_path)
        # Test get ICAO field errors
        self.assertEqual("Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', "
                         "'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of 'STS'",
                         rx.get_icao_field_errors()[0][0])
        self.assertEqual(144, rx.get_icao_field_errors()[0][1])
        self.assertEqual(147, rx.get_icao_field_errors()[0][2])
        self.assertEqual("Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', "
                         "'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of '1'",
                         rx.get_icao_field_errors()[1][0])
        self.assertEqual(148, rx.get_icao_field_errors()[1][1])
        self.assertEqual(149, rx.get_icao_field_errors()[1][2])

    def test_read_xml_05(self):
        rx = ReadXml(self.file_path)
        # Test get all errors, ICAO and ERS
        self.assertEqual("Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', "
                         "'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of 'STS'",
                         rx.get_all_errors()[0][0])
        self.assertEqual(144, rx.get_all_errors()[0][1])
        self.assertEqual(147, rx.get_all_errors()[0][2])
        self.assertEqual("Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', "
                         "'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of '1'",
                         rx.get_all_errors()[1][0])
        self.assertEqual(148, rx.get_all_errors()[1][1])
        self.assertEqual(149, rx.get_all_errors()[1][2])
        self.assertEqual("The element 'PNT44444' is an unrecognised Field 15 element", rx.get_all_errors()[2][0])
        self.assertEqual(76, rx.get_all_errors()[2][1])
        self.assertEqual(84, rx.get_all_errors()[2][2])

    def test_read_xml_06(self):
        rx = ReadXml(self.file_path)
        # Test get ERS records
        self.assertEqual("ADEP", rx.get_ers_records()[0][0])
        self.assertEqual("IFR", rx.get_ers_records()[0][1])
        self.assertEqual("N0450", rx.get_ers_records()[0][2])
        self.assertEqual("F350", rx.get_ers_records()[0][3])
        self.assertEqual(66, rx.get_ers_records()[0][4])
        self.assertEqual(66, rx.get_ers_records()[0][5])
        self.assertEqual("", rx.get_ers_records()[0][6])

        self.assertEqual("23N123W", rx.get_ers_records()[1][0])
        self.assertEqual("IFR", rx.get_ers_records()[1][1])
        self.assertEqual("N0450", rx.get_ers_records()[1][2])
        self.assertEqual("F350", rx.get_ers_records()[1][3])
        self.assertEqual(85, rx.get_ers_records()[1][4])
        self.assertEqual(92, rx.get_ers_records()[1][5])
        self.assertEqual("", rx.get_ers_records()[1][6])

        self.assertEqual("BBB", rx.get_ers_records()[2][0])
        self.assertEqual("IFR", rx.get_ers_records()[2][1])
        self.assertEqual("N0450", rx.get_ers_records()[2][2])
        self.assertEqual("F350", rx.get_ers_records()[2][3])
        self.assertEqual(93, rx.get_ers_records()[2][4])
        self.assertEqual(96, rx.get_ers_records()[2][5])
        self.assertEqual("", rx.get_ers_records()[2][6])

        self.assertEqual("B9", rx.get_ers_records()[3][0])
        self.assertEqual("IFR", rx.get_ers_records()[3][1])
        self.assertEqual("N0450", rx.get_ers_records()[3][2])
        self.assertEqual("F350", rx.get_ers_records()[3][3])
        self.assertEqual(97, rx.get_ers_records()[3][4])
        self.assertEqual(99, rx.get_ers_records()[3][5])
        self.assertEqual("", rx.get_ers_records()[3][6])

        self.assertEqual("AAA", rx.get_ers_records()[4][0])
        self.assertEqual("IFR", rx.get_ers_records()[4][1])
        self.assertEqual("N0450", rx.get_ers_records()[4][2])
        self.assertEqual("F350", rx.get_ers_records()[4][3])
        self.assertEqual(100, rx.get_ers_records()[4][4])
        self.assertEqual(103, rx.get_ers_records()[4][5])
        self.assertEqual("", rx.get_ers_records()[4][6])

        self.assertEqual("ADES", rx.get_ers_records()[5][0])
        self.assertEqual("IFR", rx.get_ers_records()[5][1])
        self.assertEqual("", rx.get_ers_records()[5][2])
        self.assertEqual("", rx.get_ers_records()[5][3])
        self.assertEqual(66, rx.get_ers_records()[5][4])
        self.assertEqual(66, rx.get_ers_records()[5][5])
        self.assertEqual("", rx.get_ers_records()[5][6])

    def test_read_xml_07(self):
        rx = ReadXml(self.file_path)
        # Test individual ICAO field 'get'
        self.assertEqual("FPL", rx.get_f3())
        self.assertEqual("TEST01", rx.get_f7())
        self.assertEqual("IS", rx.get_f8())
        self.assertEqual("B737/M", rx.get_f9())
        self.assertEqual("S/C", rx.get_f10())
        self.assertEqual("LOWW0800", rx.get_f13())
        self.assertEqual("N0450F350 PNT44444 23N123W BBB B9 AAA STAY1/ 1234", rx.get_f15())
        self.assertEqual("LOWW0200", rx.get_f16())
        self.assertEqual("RMK/REMARK 1 STS/STS 1 RMK/REMARK 2", rx.get_f18())

    def test_read_xml_08(self):
        rx = ReadXml(self.file_path)
        self.assertEqual("FF ABCDEFGH" + os.linesep +
                         "241309 IJKLMNOP" + os.linesep +
                         "(FPL-TEST01-IS" + os.linesep +
                         "-B737/M-S/C" + os.linesep +
                         "-LOWW0800" + os.linesep +
                         "-N0450F350 PNT44444 23N123W BBB B9 AAA STAY1/ 1234" + os.linesep +
                         "-LOWW0200" + os.linesep +
                         "-RMK/REMARK 1 STS/STS 1 RMK/REMARK 2)",
                         rx.build_message())


if __name__ == '__main__':
    unittest.main()
