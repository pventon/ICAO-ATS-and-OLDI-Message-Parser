from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseMessage import ParseMessage


# This class is the entry point for the ICAO ATS Message Parser.
# To use this class, instantiate the class and call one of the two methods:
# For both methods...
# icao_message_parser = IcaoAtsMessageParser()
#
# Option one:
# -----------
# # An ICAO or OLDI message of your choice...
# icao_message: str = "(FPL-TEST01-IS-B737/M-S/C-LOWW0800-N0450f350 PNT B9 LNZ1A-EGLL0200-0)"
#
# # Instantiate the parser...
# icao_message_parser: IcaoAtsMessageParser = IcaoAtsMessageParser()
#
# # Parse the message...
# flight_plan_record: FlightPlanRecord = icao_message_parser.parse_message_p1(icao_message)
#
# # Check if any errors were reported in the basic field processing...
# if flight_plan_record.errors_detected():
#     # For fields other than field 15 call the following method, this returns a list of ErrorRecord's...
#     basic_field_errors: [ErrorRecord] = flight_plan_record.get_erroneous_fields()
#
# # For field 15, get the Extracted Route Sequence and get the errors, returns a list of Tokens...
# if flight_plan_record.get_extracted_route_sequence().get_number_of_errors() > 0:
#     field_15_errors: [Token] = flight_plan_record.get_extracted_route_sequence().get_all_errors()
#
# # To extract fields and / or subfields use the methods in the following example code...
# self.assertEqual(
#     # Get the complete ICAO Field 9
#     "B737/M",
#     flight_plan_record.get_icao_field(FieldIdentifiers.F9).get_field_text())
#
# self.assertEqual(
#     # Get the ICAO field 9 WTC (Field 9 'c')
#     "M",
#     flight_plan_record.get_icao_subfield(FieldIdentifiers.F9, SubFieldIdentifiers.F9c).get_field_text())
#
#
# Option two:
# -----------
# # Instantiate a FlightPlanRecord, the output is written into this class instance.
# flight_plan_record: FlightPlanRecord = FlightPlanRecord()
#
# # An ICAO or OLDI message of your choice...
# icao_message: str = "(FPL-TEST01-IS-B737/M-S/C-LOWW0800-N0450f350 PNT B9 LNZ1A-EGLL0200-0)"
#
# # Instantiate the parser...
# icao_message_parser = IcaoAtsMessageParser()
#
# # Parse the message...
# result = icao_message_parser.parse_message_p2(flight_plan_record, icao_message)
#
# # If errors were detected, result will be False; to get the error records do the following...
# if not result:
#     # For fields other than field 15 call the following method, this returns a list of ErrorRecord's...
#     basic_field_errors: [ErrorRecord] = flight_plan_record.get_erroneous_fields()
#
# # For field 15, get the Extracted Route Sequence and get the errors, returns a list of Tokens...
# if flight_plan_record.get_extracted_route_sequence().get_number_of_errors() > 0:
#     field_15_errors: [Token] = flight_plan_record.get_extracted_route_sequence().get_all_errors()
#
# # To extract fields and / or subfields use the methods in the following example code...
# self.assertEqual(
#     # Get the complete ICAO Field 13
#     "LOWW0800",
#     flight_plan_record.get_icao_field(FieldIdentifiers.F13).get_field_text())
#
# self.assertEqual(
#     # Get the ICAO field 16 EET (Field 16 'b')
#     "0200",
#     flight_plan_record.get_icao_subfield(FieldIdentifiers.F16, SubFieldIdentifiers.F16b).get_field_text())
#
class IcaoAtsMessageParser:
    # Handle to the ICAO message parser
    icao_message_parser: ParseMessage = ParseMessage()

    def parse_message_p1(self, icao_message):
        # type: (str) -> FlightPlanRecord
        flight_plan_record = FlightPlanRecord()
        self.get_icao_message_parser().parse_message(flight_plan_record, icao_message)
        return flight_plan_record

    def parse_message_p2(self, flight_plan_record, icao_message):
        # type: (FlightPlanRecord, str) -> bool
        return self.get_icao_message_parser().parse_message(flight_plan_record, icao_message)

    def get_icao_message_parser(self):
        # type: () -> ParseMessage
        return self.icao_message_parser
