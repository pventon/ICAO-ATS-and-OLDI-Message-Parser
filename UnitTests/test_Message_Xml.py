import unittest

from Configuration.EnumerationConstants import MessageTypes
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


class ParseMessageTests(unittest.TestCase):
    fpr: FlightPlanRecord = None
    pm = None

    def tearDown(self) -> None:
        # self.fpr = None
        self.pm = None

    def setUp(self) -> None:
        self.fpr = FlightPlanRecord()
        self.pm = ParseMessage()

    def test_ParseMessage_01(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "241309 IJKLMNOP "
                              "(FPL-TEST01"
                              "-IS-B737/M"
                              "-S/C-LOWW0800"
                              "-N0450F350 PNT44444 23N123W BBB B9 AAA STAY1/ 1234"
                              "-LOWW0200"
                              "-RMK/REMARK 1 STS/STS 1 RMK/REMARK 2)")
        # print(self.fpr.as_xml())

    def test_ParseMessage_02(self):
        self.pm.parse_message(self.fpr,
                              "FF ABCDEFGH "
                              "191916 AAAAAAAA "
                              "(FPL-TEST01"
                              "-IS-B737/M"
                              "-S/C-LOWW0800"
                              "-N0450F350 PNT 23N123W BBB B9 AAA STAY1/ 1234"
                              "-LOWW0200"
                              "-0)")
        # print(self.fpr.as_xml())


if __name__ == '__main__':
    unittest.main()
