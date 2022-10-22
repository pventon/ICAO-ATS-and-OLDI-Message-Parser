from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId, SubFieldIdentifiers
from IcaoMessageParser.ParseF3 import ParseF3
from IcaoMessageParser.ParseF5 import ParseF5
from IcaoMessageParser.ParseF7 import ParseF7
from IcaoMessageParser.ParseF8 import ParseF8
from IcaoMessageParser.ParseF9 import ParseF9
from IcaoMessageParser.ParseF10 import ParseF10
from IcaoMessageParser.ParseF13 import ParseF13
from IcaoMessageParser.ParseF14 import ParseF14
from IcaoMessageParser.ParseF15 import ParseF15x
from IcaoMessageParser.ParseF16 import ParseF16
from IcaoMessageParser.ParseF17 import ParseF17
from IcaoMessageParser.ParseF18 import ParseF18
from IcaoMessageParser.ParseF19 import ParseF19
from IcaoMessageParser.ParseF20 import ParseF20
from IcaoMessageParser.ParseF21 import ParseF21
from IcaoMessageParser.ParseF80 import ParseF80
from IcaoMessageParser.ParseF81 import ParseF81
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils


class ParseF22(ParseFieldsCommon):
    """This class parses ICAO field 22; this class subclasses ParseFieldsCommon. This class
    initialises the base class with information specific for parsing field 22, namely:

    - A flight plan record, instance of FlightPlanRecord
    - Configuration data defining the subfields contained in this field,
      see configuration data in the SubFieldsInFields class
    - Configuration data defining the subfields that a field comprises,
      see configuration data in the SubFieldDescriptions class"""

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 22.

            :param flight_plan_record: Flight plan to populate
            :param sfif: Configuration data defining the subfields in an ICAO field
            :param sfd: Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F22,  # ICAO field identifier
                         "-\n\t\r",  # Whitespace to tokenize the field
                         sfif.get_field_content_description(FieldIdentifiers.F22),  # Subfields in this field
                         sfif.get_field_errors(FieldIdentifiers.F22))  # Errors associated with this field

    def parse_field(self):
        # type: () -> None
        """This method is the program entry point to parse ICAO field 22. This field is a little
        different to the other compound fields as the keywords are numbers and the fields are separated
        in a message by hyphens.

        This method loops over the subfields, identifies them and stores them in the flight plan record.
        If a subfield is not recognised an error is reported.
            :return: None"""

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, ErrorId.F22_DATA_MISSING)
            return

        data_found = False
        for token in self.get_tokens().get_tokens():
            if len(token.get_token_string().replace(" ", "")) == 0:
                continue
            else:
                data_found = True
            slash_index = Utils.get_first_slash_index(token.get_token_string())
            if slash_index < 1:
                # Error, field number cannot be determined as it precedes the field, e.g 9/B737/M,
                # If the '/' is missing, then we cannot determine what the field number is.
                self.add_error(token.get_token_string(),
                               token.get_token_start_index(),
                               token.get_token_end_index(),
                               ErrorId.F22_NO_F22_KEYWORDS_FOUND)
            else:
                # We found a slash, what precedes it must be the field number, the number as a string
                field_number_as_string = token.get_token_string()[0:slash_index].rstrip().lstrip()

                # Check if this is a known field number by comparing it with the enumeration
                # values defining the field numbers.
                subfield_id = self.is_compound_field_keyword(self.get_field_identifier(), field_number_as_string)
                if subfield_id == SubFieldIdentifiers.ANYTHING:
                    # Field number in unrecognised, not one of those defined
                    self.add_error(token.get_token_string(),
                                   token.get_token_start_index(),
                                   token.get_token_end_index(),
                                   ErrorId.F22_UNRECOGNISED_KEYWORD)
                else:
                    # Check if there is any data following the '/'
                    if len(token.get_token_string()[slash_index + 1:]) < 1:
                        # No data following the '/'
                        self.add_error(token.get_token_string(),
                                       token.get_token_start_index(),
                                       token.get_token_end_index(),
                                       ErrorId.F22_UNRECOGNISED_DATA)
                    else:
                        # Success! Save the subfield!
                        self.get_flight_plan_record().add_icao_subfield(
                            self.get_field_identifier(),
                            subfield_id,
                            token.get_token_string()[slash_index + 1:],
                            token.get_token_start_index(),
                            token.get_token_end_index())

        if data_found:
            self.parse_compound_subfields(SubFieldIdentifiers.F22_f3, SubFieldIdentifiers.F22_f81)
        else:
            self.add_error("", 0, 0, ErrorId.F22_DATA_MISSING)

    def parse_compound_subfields(self, subfield_start, subfield_end):
        # type: (SubFieldIdentifiers, SubFieldIdentifiers) -> None
        """This method parses the individual F22 subfields by looping over all the subfields
        stored in the flight plans F22 record. All F22 subfields are fields that already
        have parsers implemented.

        The process to parse the F22 subfields works as follows:
            - Get the F22 field record;
            - Retrieve the list of subfields from the field record that contains a list of
              all the F22 subfields;
            - Create a new flight plan record and copy it into the flight plan record used by
              this parser self.get_flight_plan_record().set_f22_flight_plan(new_fpr)), the
              flight plan record maintains a flight plan record of the F22 subfields;
            - Loop over the subfields and:
                * Check if there is more than one subfield in the list of subfields, this implies
                  a subfield appears twice in field 22, an error is reported if this is the case;
                * Copy the subfield into the new flight plan record;
                * Parse the subfield as is done fo any flight plan field;
            - The 'new' flight plan now contains all the F22 subfields as fields with their respective
              subfields along with any errors;
            - Check if there are any errors, if there are, copy them from the new flight plan
              into the flight plan record this field parser is working on;
        When looping over the F22 subfields, the F22 subfield enumeration values are used as the loop range;
        this ensures when looping over the F22 subfields that only F22 subfields are 'addressed' and reduces
        the processing time by limiting the number of enumerations to the F22 subset;

            :param subfield_start: The first F22 subfield enumeration value;
            :param subfield_end: The last F22 subfield enumeration value;
            :return: None
        """
        # Set up a dictionary of field parser callbacks...
        parse_field_x = {SubFieldIdentifiers.F22_f3: [FieldIdentifiers.F3, ParseF3],
                         SubFieldIdentifiers.F22_f5: [FieldIdentifiers.F5, ParseF5],
                         SubFieldIdentifiers.F22_f7: [FieldIdentifiers.F7, ParseF7],
                         SubFieldIdentifiers.F22_f8: [FieldIdentifiers.F8, ParseF8],
                         SubFieldIdentifiers.F22_f9: [FieldIdentifiers.F9, ParseF9],
                         SubFieldIdentifiers.F22_f10: [FieldIdentifiers.F10, ParseF10],
                         SubFieldIdentifiers.F22_f13: [FieldIdentifiers.F13, ParseF13],
                         SubFieldIdentifiers.F22_f14: [FieldIdentifiers.F14, ParseF14],
                         SubFieldIdentifiers.F22_f15: [FieldIdentifiers.F15, ParseF15x],
                         SubFieldIdentifiers.F22_f16: [FieldIdentifiers.F16, ParseF16],
                         SubFieldIdentifiers.F22_f17: [FieldIdentifiers.F17, ParseF17],
                         SubFieldIdentifiers.F22_f18: [FieldIdentifiers.F18, ParseF18],
                         SubFieldIdentifiers.F22_f19: [FieldIdentifiers.F19, ParseF19],
                         SubFieldIdentifiers.F22_f20: [FieldIdentifiers.F20, ParseF20],
                         SubFieldIdentifiers.F22_f21: [FieldIdentifiers.F21, ParseF21],
                         SubFieldIdentifiers.F22_f22: [FieldIdentifiers.F22, ParseF22],
                         SubFieldIdentifiers.F22_f80: [FieldIdentifiers.F80, ParseF80],
                         SubFieldIdentifiers.F22_f81: [FieldIdentifiers.F81, ParseF81]}

        # Get the field 22 FieldRecord that contains zero or more F22 subfields
        field_record = self.get_flight_plan_record().get_icao_field(self.get_field_identifier())

        # Get the dictionary containing all the field 22 subfields stored in the flight plan
        subfield_dictionary = field_record.get_subfield_dictionary()

        # The field parsers need a flight plan, and we can't use the one in this instance, create
        # a new one, it will be populated by all the fields found in the field 22 being parsed.
        new_fpr = FlightPlanRecord()

        # Add the new flight plan to the flight plan instance in this class;
        self.get_flight_plan_record().set_f22_flight_plan(new_fpr)

        # Loop of the dictionary of subfields and parse each individual subfield
        for subfield_key, subfield_list in subfield_dictionary.items():
            # Make sure subfield identifiers are valid F22 subfield enumeration values
            if subfield_start <= subfield_key <= subfield_end:
                # For field 22 there should only be a single subfield, i.e. a single
                # list entry, if there are more than one it means a field has been repeated
                # and an error will be reported.
                if len(subfield_list) > 1:
                    self.add_error(subfield_key.name[5:] + "/" + subfield_list[1].get_field_text(),
                                   subfield_list[1].get_start_index(),
                                   subfield_list[1].get_end_index(),
                                   ErrorId.F22_FIELD_DUPLICATED)

                # Loop over the list of subfields and parse the field;
                for subfield in subfield_list:
                    new_fpr.add_icao_field(
                        parse_field_x[subfield_key][0],
                        subfield.get_field_text(),
                        subfield.get_start_index(),
                        subfield.get_end_index())
                    pfx = parse_field_x[subfield_key][1](new_fpr, SubFieldsInFields(), self.sfd)
                    pfx.parse_field()

        # Check if the new flight plan contains any errors
        if new_fpr.errors_detected():
            # Errors were detected, copy them into the flight plan record of this
            # instance
            for error_records in new_fpr.get_erroneous_fields():
                self.get_flight_plan_record().add_erroneous_field(
                    error_records.get_field_text(),
                    "F22 - " + error_records.get_error_message(),
                    error_records.get_start_index(),
                    error_records.get_end_index())

        # Check if the extracted route in the new flight plan contains amy errors
        if new_fpr.get_extracted_route_sequence() is not None:
            if new_fpr.get_extracted_route_sequence().get_number_of_errors() > 0:
                # We have field 15 errors, copy them over
                for error_record in new_fpr.get_extracted_route_sequence().get_all_errors():
                    self.get_flight_plan_record().add_erroneous_field(
                        error_record.get_name(),
                        "F22 - " + error_record.get_error_text(),
                        error_record.get_start_index(),
                        error_record.get_end_index())
