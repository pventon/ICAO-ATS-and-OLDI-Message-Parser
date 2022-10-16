import unittest

from Configuration.EnumerationConstants import MessageTypes, SubFieldIdentifiers, FieldIdentifiers
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord, SubFieldRecord
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence
from F15_Parser.F15Parse import ParseF15
from Tokenizer.Tokenize import Tokenize


class MessageParserTest(unittest.TestCase):

    def test_FlightPlanRecord_01(self):
        fpr = FlightPlanRecord()
        fpr.set_message_complete("COMPLETE")
        fpr.set_message_header("HEADER")
        fpr.set_message_body("BODY")
        self.assertEqual(False, fpr.errors_detected())
        self.assertEqual("COMPLETE", fpr.get_message_complete())
        self.assertEqual("HEADER", fpr.get_message_header())
        self.assertEqual("BODY", fpr.get_message_body())

    def test_FlightPlanRecord_02(self):
        fpr = FlightPlanRecord()
        fpr.set_message_type(MessageTypes.ATS)
        fpr.add_icao_field(FieldIdentifiers.ADDRESS, "ADDRESS", 11, 22)
        fpr.add_icao_field(FieldIdentifiers.F16ab, "ADES1234", 22, 30)
        fpr.add_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16a, "ADES", 22, 26)
        fpr.add_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16b, "1234", 26, 30)
        self.assertEqual(False, fpr.errors_detected())
        self.assertEqual(MessageTypes.ATS, fpr.get_message_type())
        fr1 = fpr.get_icao_field(FieldIdentifiers.ADDRESS)
        fr2 = fpr.get_icao_field(FieldIdentifiers.F16ab)
        fr3 = fpr.get_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16a)
        fr4 = fpr.get_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16b)
        self.assertEqual("ADDRESS", fr1.get_field_text())
        self.assertEqual("ADES1234", fr2.get_field_text())
        self.assertEqual("ADES", fr3.get_field_text())
        self.assertEqual("1234", fr4.get_field_text())
        self.assertEqual(11, fr1.get_start_index())
        self.assertEqual(22, fr2.get_start_index())
        self.assertEqual(22, fr3.get_start_index())
        self.assertEqual(26, fr4.get_start_index())
        self.assertEqual(22, fr1.get_end_index())
        self.assertEqual(30, fr2.get_end_index())
        self.assertEqual(26, fr3.get_end_index())
        self.assertEqual(30, fr4.get_end_index())

    def test_FlightPlanRecord_03(self):
        fpr = FlightPlanRecord()
        fpr.add_erroneous_field("BAD FIELD", "Error", 20, 30)
        error_record = fpr.get_erroneous_fields()
        self.assertEqual(True, fpr.errors_detected())
        self.assertEqual("BAD FIELD", error_record[0].get_field_text())
        self.assertEqual("Error", error_record[0].get_error_message())
        self.assertEqual(20, error_record[0].get_start_index())
        self.assertEqual(30, error_record[0].get_end_index())

    def test_FlightPlanRecord_04(self):
        fpr = FlightPlanRecord()
        fpr.add_erroneous_field("BAD FIELD 1", "Error 1", 20, 30)
        fpr.add_erroneous_field("BAD FIELD 2", "Error 2", 40, 50)
        error_record = fpr.get_erroneous_fields()
        self.assertEqual(True, fpr.errors_detected())
        self.assertEqual("BAD FIELD 1", error_record[0].get_field_text())
        self.assertEqual("Error 1", error_record[0].get_error_message())
        self.assertEqual(20, error_record[0].get_start_index())
        self.assertEqual(30, error_record[0].get_end_index())
        self.assertEqual("BAD FIELD 2", error_record[1].get_field_text())
        self.assertEqual("Error 2", error_record[1].get_error_message())
        self.assertEqual(40, error_record[1].get_start_index())
        self.assertEqual(50, error_record[1].get_end_index())

    def test_FlightPlanRecord_05(self):
        fpr = FlightPlanRecord()
        fpr_f22 = FlightPlanRecord()
        fpr_f22.set_message_type(MessageTypes.ATS)
        fpr_f22.add_icao_field(FieldIdentifiers.ADDRESS, "F22 ADDRESS FIELD", 91, 22)
        fpr_f22.add_icao_field(FieldIdentifiers.F16ab, "ADES1234", 92, 33)
        fpr_f22.add_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16a, "ADES", 97, 44)
        fpr_f22.add_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16b, "1234", 97, 64)
        fpr.set_f22_flight_plan(fpr_f22)
        res_fpr = fpr.get_f22_flight_plan()
        self.assertEqual(MessageTypes.ATS, res_fpr.get_message_type())
        fr1 = res_fpr.get_icao_field(FieldIdentifiers.ADDRESS)
        fr2 = res_fpr.get_icao_field(FieldIdentifiers.F16ab)
        fr3 = res_fpr.get_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16a)
        fr4 = res_fpr.get_icao_subfield(FieldIdentifiers.F16ab, SubFieldIdentifiers.F16b)
        self.assertEqual("F22 ADDRESS FIELD", fr1.get_field_text())
        self.assertEqual("ADES1234", fr2.get_field_text())
        self.assertEqual("ADES", fr3.get_field_text())
        self.assertEqual("1234", fr4.get_field_text())
        self.assertEqual(91, fr1.get_start_index())
        self.assertEqual(92, fr2.get_start_index())
        self.assertEqual(97, fr3.get_start_index())
        self.assertEqual(97, fr4.get_start_index())
        self.assertEqual(22, fr1.get_end_index())
        self.assertEqual(33, fr2.get_end_index())
        self.assertEqual(44, fr3.get_end_index())
        self.assertEqual(64, fr4.get_end_index())

    def test_FlightPlanRecord_06(self):
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F15, "N0450F350 GFG B6 DEA/N0200F100", 2, 4)
        tokenizer = Tokenize()
        tokenizer.set_string_to_tokenize(fpr.get_icao_field(FieldIdentifiers.F15).get_field_text())
        tokenizer.set_whitespace("/ \n\t\r")
        tokenizer.tokenize()
        ers = ExtractedRouteSequence()
        ParseF15().parse_f15(ers, tokenizer.get_tokens())
        fpr.add_extracted_route(ers)
        res_ers = fpr.get_extracted_route()
        self.assertEqual("DEA", res_ers.get_previous_to_last_element().get_name())


if __name__ == '__main__':
    unittest.main()
