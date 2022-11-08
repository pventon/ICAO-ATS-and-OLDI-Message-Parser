from Configuration.EnumerationConstants import FieldIdentifiers, ErrorId
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon
from Configuration.SubFieldsInFields import SubFieldsInFields
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.Utils import Utils


class ParseF18dof(ParseFieldsCommon):

    def __init__(self, flight_plan_record, sfif, sfd):
        # type: (FlightPlanRecord, SubFieldsInFields, SubFieldDescriptions) -> None
        """Constructor to set up the field parser for ICAO field 18dof.
        Arguments
        ---------
        flight_plan_record:   Flight plan to populate
        sfif:                 Configuration data defining the subfields in an ICAO field
        sfd:                  Configuration data describing the syntax and other information about all subfields"""
        super().__init__(flight_plan_record,  # Flight plan to populate
                         sfd,  # Configuration data describing individual subfields
                         FieldIdentifiers.F18_DOF,  # ICAO field identifier
                         " \n\t\r",  # Whitespace to tokenize the field
                         # Subfields in this field
                         sfif.get_field_content_description(FieldIdentifiers.F18_DOF),
                         # Errors associated for this field
                         sfif.get_field_errors(FieldIdentifiers.F18_DOF))

    def parse_field(self):
        # type: () -> None

        # Check if the field contains anything at all...
        if self.no_tokens():
            self.add_error("", 0, 0, self.get_missing_subfield_error())
            return

        # Parse the field
        # num_parsed = self.parse_field_base()
        # Don't use the base parser as it's a single field that has very specific syntax
        if not Utils().is_dof(self.get_tokens().get_first_token().get_token_string()[-6:]):
            self.add_error(self.get_tokens().get_first_token().get_token_string(),
                           self.get_tokens().get_first_token().get_token_start_index(),
                           self.get_tokens().get_first_token().get_token_end_index(),
                           ErrorId.F18_DOF_F18A_SYNTAX)

        self.add_subfield_to_fpr(self.get_sub_field_list()[0],
                                 self.get_tokens().get_token_at(0).get_token_string(),
                                 self.get_tokens().get_token_at(0).get_token_start_index() +
                                 self.get_flight_plan_record().get_icao_field(
                                     self.get_field_identifier()).get_start_index(),
                                 self.get_tokens().get_token_at(0).get_token_end_index() +
                                 self.get_flight_plan_record().get_icao_field(
                                     self.get_field_identifier()).get_start_index())

        # Parse any extra tokens that may be present
        self.check_if_tokens_left_over()
