import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF14 import ParseF14
from Tokenizer.Token import Token


class TestParseF14(unittest.TestCase):

    def test_parse_field14(self):
        # Field empty
        self.do_f14_test(True, 1, "", ["There is no data in field 14"])

        # Field empty with spaces
        self.do_f14_test(True, 1, "    ", ["There is no data in field 14"])

        # OK
        self.do_f14_test(True, 1, "PPP", ["Field 14 is incomplete, whole field should be Point/Time '/' (HHMM), "
                                          "Cleared level, supplementary crossing level, crossing condition "
                                          "(A or B) instead of 'PPP'"])

        # Building the field bit by bit, all error cases
        self.do_f14_test(True, 1, "PPP/", ["Field 14 is incomplete, whole field should be Point/Time '/' (HHMM), "
                                           "Cleared level, supplementary crossing level, crossing condition "
                                           "(A or B) instead of '/'"])

        # Building the field bit by bit, all error cases
        self.do_f14_test(True, 1, "PPP/123", ["Expecting boundary crossing time in '/HHMM' instead of '123'"])

        # Building the field bit by bit, all error cases
        self.do_f14_test(True, 1, "PPP/1234F35", ["Expecting cleared level (F/A 3 digits, or M/S 4 "
                                                  "digits) instead of 'F35'"])

        # Building the field bit by bit, all error cases
        self.do_f14_test(True, 1, "PPP/2359F350S102", ["Expecting supplementary crossing data (F/A 3 "
                                                       "digits, or M/S 4 digits) instead of 'S102'"])

        # All OK
        self.do_f14_test(False, 0, "PPP/0000A120M1122A", [])

        # Point Error
        self.do_f14_test(True, 1, "P3PP/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes or "
            "point/bearing/distance instead of 'P3PP'"])

        # Point is Lat / Long in degrees, OK
        self.do_f14_test(False, 0, "65N156W/2334A105M1203A", [])

        # Latitude degrees error > 90
        self.do_f14_test(True, 1, "N91W179/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N91W179'"])

        # Longitude degrees error > 180
        self.do_f14_test(True, 1, "N89W181/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N89W181'"])

        # Latitude minutes error > 59
        self.do_f14_test(True, 1, "N8960W17900/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in degrees/minutes "
            "or point/bearing/distance instead of 'N8960W17900'"])

        # Longitude minutes error > 59
        self.do_f14_test(True, 1, "N9050W18060/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of 'N9050W18060'"])

        # Point/Bearing/Distance OK
        self.do_f14_test(False, 0, "PPP/0000A120M1122A", [])

        # Lat/Long in Degrees/Bearing/Distance OK
        self.do_f14_test(False, 0, "12N123W/0000A120M1122A", [])

        # Lat/Long in Degrees & Minutes/Bearing/Distance OK
        self.do_f14_test(False, 0, "1234N12345W/0000A120M1122A", [])

        # Lat/Long in Degrees & Minutes/Bearing/Distance -> Lat Minutes > 59
        self.do_f14_test(True, 1, "1260N12345W/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of '1260N12345W'"])

        # Lat/Long in Degrees & Minutes/Bearing/Distance -> Long Minutes > 59
        self.do_f14_test(True, 1, "1259N12360W/0000A120M1122A", [
            "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
            "degrees/minutes or point/bearing/distance instead of '1259N12360W'"])

        # Crossing time incorrect
        self.do_f14_test(True, 1, "1259N12334W/2360A120M1122A", [
            "Expecting boundary crossing time in '/HHMM' instead of '2360'"])

        # Invalid crossing level, 'G' instead of 'F' or 'A'
        self.do_f14_test(True, 1, "PPP/1234G300M1000B", [
            "Expecting cleared level (F/A 3 digits, or M/S 4 digits) instead of 'G300'"])

        # Invalid crossing level, Flight level must be modulus 5
        self.do_f14_test(True, 1, "PPPF/0100F351S3200B", [
            "Expecting cleared level (F/A 3 digits, or M/S 4 digits) instead of 'F351'"])

        # Invalid supplementary crossing data, 'G' instead of 'F' or 'A'
        self.do_f14_test(True, 1, "PPPPP/1657F350G400A", [
            "Expecting supplementary crossing data (F/A 3 digits, or M/S 4 digits) instead of 'G400'"])

        # Invalid supplementary crossing data, Flight level must be modulus 5
        self.do_f14_test(True, 1, "PPP/2034F100F201A", [
            "Expecting supplementary crossing data (F/A 3 digits, or M/S 4 digits) instead of 'F201'"])

        # Invalid crossing condition
        self.do_f14_test(True, 1, "PPP/2034F100F320C", [
            "Expecting crossing condition (A or B) instead of 'C'"])

        # Extra fields
        self.do_f14_test(True, 1, "AAAAA/1234F100F320A EXTRA FIELD", [
            "Too many field(s) in Field 14, remove 'EXTRA FIELD'"])

        # Optional fields omitted
        self.do_f14_test(False, 0, "PPP/2034F100", [
            "Expecting crossing condition (A or B) instead of 'C'"])

        # Optional fields omitted with extra fields
        self.do_f14_test(True, 1, "PPP/2034F100 EXTRA FIELDS", [
            "Expecting supplementary crossing data (F/A 3 digits, or M/S 4 digits) instead of 'EXTRA'"])

    def do_f14_test(self, errors_detected, number_of_errors,
                    string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F14, string_to_parse, 0, len(string_to_parse))
        pf14 = ParseF14(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf14.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
