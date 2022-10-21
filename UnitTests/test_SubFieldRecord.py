import unittest

from Configuration.EnumerationConstants import MessageTypes, SubFieldIdentifiers, FieldIdentifiers
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence
from F15_Parser.F15Parse import ParseF15
from Tokenizer.Tokenize import Tokenize


class TestSubFieldRecord(unittest.TestCase):

    def test_add_multiple_subfields_00(self):
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F18, "RML/REMARK 1", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 1", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 2", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 3", 0, 0)
        self.assertEqual(
            "RMK Subfield 1",
            fpr.get_icao_field(FieldIdentifiers.F18).get_subfield(SubFieldIdentifiers.F18rmk).get_field_text())
        self.assertEqual(
            "RMK Subfield 1",
            fpr.get_icao_field(FieldIdentifiers.F18).get_all_subfields(SubFieldIdentifiers.F18rmk)[0].get_field_text())
        self.assertEqual(
            "RMK Subfield 2",
            fpr.get_icao_field(FieldIdentifiers.F18).get_all_subfields(SubFieldIdentifiers.F18rmk)[1].get_field_text())
        self.assertEqual(
            "RMK Subfield 3",
            fpr.get_icao_field(FieldIdentifiers.F18).get_all_subfields(SubFieldIdentifiers.F18rmk)[2].get_field_text())

    def test_add_multiple_subfields_01(self):
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F18, "RML/REMARK 1", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 1", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 2", 0, 0)
        fpr.add_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk, "RMK Subfield 3", 0, 0)
        self.assertEqual(
            "RMK Subfield 1",
            fpr.get_icao_subfield(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk).get_field_text())
        self.assertEqual(
            "RMK Subfield 1",
            fpr.get_all_icao_subfields(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk)[0].get_field_text())
        self.assertEqual(
            "RMK Subfield 2",
            fpr.get_all_icao_subfields(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk)[1].get_field_text())
        self.assertEqual(
            "RMK Subfield 3",
            fpr.get_all_icao_subfields(FieldIdentifiers.F18, SubFieldIdentifiers.F18rmk)[2].get_field_text())


if __name__ == '__main__':
    unittest.main()
