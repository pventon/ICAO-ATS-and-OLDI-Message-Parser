from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId, SubFieldIdentifiers
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
                # Error, field number unrecognised
                self.add_error(token.get_token_string(),
                               token.get_token_start_index(),
                               token.get_token_end_index(),
                               ErrorId.F22_NO_F22_KEYWORDS_FOUND)
            else:
                field_number_as_string = token.get_token_string()[0:slash_index].rstrip().lstrip()
                subfield_id = self.is_compound_field_keyword(self.get_field_identifier(), field_number_as_string)
                if subfield_id == SubFieldIdentifiers.ANYTHING:
                    self.add_error(token.get_token_string(),
                                   token.get_token_start_index(),
                                   token.get_token_end_index(),
                                   ErrorId.F22_UNRECOGNISED_KEYWORD)
                else:
                    tmp = token.get_token_string()[slash_index + 1:]
                    if len(token.get_token_string()[slash_index + 1:]) < 1:
                        # No data following the '/'
                        self.add_error(token.get_token_string(),
                                       token.get_token_start_index(),
                                       token.get_token_end_index(),
                                       ErrorId.F22_UNRECOGNISED_DATA)
                    else:
                        # Save the subfield
                        self.get_flight_plan_record().add_icao_subfield(
                            self.get_field_identifier(),
                            subfield_id,
                            token.get_token_string()[slash_index + 1:],
                            token.get_token_start_index(),
                            token.get_token_end_index())

        if not data_found:
            self.add_error("", 0, 0, ErrorId.F22_DATA_MISSING)
