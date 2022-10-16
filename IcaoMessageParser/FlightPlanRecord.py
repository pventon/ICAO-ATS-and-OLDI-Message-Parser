# The classes in this file together represent a complete flight plan; the overall
# structure for a flight plan record is made up from all the classes in this file in
# the following manner:
# FlightPlanRecord -+-->  FieldRecord -+--> SubFieldRecord
#                   |                  +--> SubFieldRecord
#                   |                  +--> SubFieldRecord
#                   |                  +--> ...
#                   +-->  FieldRecord -+--> SubFieldRecord
#                   |                  +--> SubFieldRecord
#                   |                  +--> SubFieldRecord
#                   |                  +--> ...
#                   +-->  ...
#                   +--> ErrorRecord
#                   +--> ...
# 1. FieldRecord classes are stored in a FlightPlanRecord dictionary and indexed
#    with enumeration values from FieldIdentifiers; FieldRecord's inherit from
#    the SubFieldRecord class.
# 2. SubFieldRecord classes are stored in a FieldRecord dictionary and indexed
#    with enumeration values from SubFieldIdentifiers;
# 3. ErrorRecord classes are stored in a FlightPlanRecord list; ErrorRecord's
#    inherit from the SubFieldRecord class.
from Configuration.EnumerationConstants import MessageTypes, FieldIdentifiers, SubFieldIdentifiers, AdjacentUnits
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence, ExtractedRouteRecord


# This class stores an ICAO subfield added to a flight plan record during ICAO
# message parsing. There are 'n' subfields contained in a flight plan record
# created by the ICAO message parser.
# A subfield is stored with its zero based start and end index in the original
# message.
# The ICAO message parser creates and adds a FieldRecord to a flight plan record
# for each ICAO field located in a message; the ICAO field is further decomposed
# into its constitute subfields and the subfields are stored as part of their
# parent ICAO fields in a FieldRecord.
# There are no 'setter' methods in this class as the constructor initialises
# all members on class instantiation making this class effectively 'read' only.
# Class members are:
# field_text:   A string that is the subfield, i.e. 'LOWL', '0234' etc.
# start_index:  An integer representing the zero based index for the start of the
#               subfield in the original message string.
# end_index:    An integer representing the zero based index for the end of the
#               subfield in the original message string.
class SubFieldRecord:
    # A string that is the subfield, i.e. 'LOWL', '0234' etc.
    field_text: str = ""

    # An integer representing the zero based index for the start of the
    # subfield in the original message string.
    start_index: int = 0

    # An integer representing the zero based index for the end of the
    # subfield in the original message string.
    end_index: int = 0

    # Constructor that initializes all class members
    def __init__(self, field_text, start_index, end_index):
        # type: (str, int, int) -> None
        self.field_text = field_text
        self.start_index = start_index
        self.end_index = end_index

    # Get the field text
    def get_field_text(self):
        # type: () -> str
        return self.field_text

    # Get the zero based index of the fields start position in the original message
    def get_start_index(self):
        # type: () -> int
        return self.start_index

    # Get the zero based index of the fields end position in the original message
    def get_end_index(self):
        # type: () -> int
        return self.end_index


# This class stores an ICAO field added to a flight plan record during ICAO
# message parsing. There are 'n' ICAO fields contained in a flight plan record
# created by the ICAO message parser.
# A field is stored with its zero based start and end index in the original
# message.
# The ICAO message parser creates and adds a FieldRecord for each ICAO field located
# in a message; the ICAO field is further decomposed into its constitute subfields and
# the subfields are stored in this class in a dictionary using the SubFieldIdentifiers
# enumeration as the dictionary key.
# This class inherits from the SubFieldRecord.
# There is a single 'add' method to add subfields to this class.
# Class members are:
# subfields:   A dictionary containing individual ICAO subfields extracted
#              from a message body. The key to this dictionary are
#              enumeration values from the EnumerationConstants.SubFieldIdentifiers
#              class.
class FieldRecord(SubFieldRecord):
    # A dictionary containing one or more subfields that together make up this
    # ICAO field.
    sub_fields: (SubFieldIdentifiers, SubFieldRecord) = {}

    # Constructor that initializes all class members
    def __init__(self, field_text, start_index, end_index):  # , field_identifier):
        # type: (str, int, int) -> None
        super().__init__(field_text, start_index, end_index)
        self.sub_fields = {}

    # Add an ICAO subfield to this ICAO field record
    def add_subfield(self, icao_sub_field_id, sub_field):
        # type: (SubFieldIdentifiers, SubFieldRecord) -> None
        self.sub_fields[icao_sub_field_id] = sub_field

    def get_subfield(self, icao_sub_field_id):
        # type: (SubFieldIdentifiers) -> SubFieldRecord
        return self.sub_fields[icao_sub_field_id]


# This class contains information about an error detected during message processing.
# The erroneous field along with its zero based start and end index in the message plus
# the error message is stored in this class.
# Zero or more of these records may be included in a flight plan record.
# This class subclasses the FieldRecord class.
# error_message: Contains the error message associated with the erroneous token.
class ErrorRecord(SubFieldRecord):
    # Contains the error message associated with the erroneous token.
    error_message: str = ""

    # Constructor that initializes all class members
    def __init__(self, erroneous_field_text, error_message, start_index, end_index):
        # type: (str, str, int, int) -> None
        super().__init__(erroneous_field_text, start_index, end_index)
        self.error_message = error_message

    # Get
    def get_error_message(self):
        # type: () -> str
        return self.error_message


# This class contains data representing a complete flight plan.
# The flight plan data is stored as follows:
# message_complete: A string that is the complete message as input to the ICAO
#                   message parser
# message_header:   A string that is the message header as input to the ICAO
#                   message parser
# message_body:     A string that is the message body; it is this data that
#                   represents a flight plan
# header_fields:    A dictionary containing individual fields extracted from
#                   a message header. The key to this dictionary are enumeration
#                   values from the MessageDescriptions.FieldIdentifiers class.
# icao_fields:      A dictionary containing individual fields extracted from
#                   a message body. The key to this dictionary are enumeration
#                   values from the MessageDescriptions.FieldIdentifiers class.
# erroneous_fields: A list contain zero or more ErrorRecord class instances; each
#                   record contains an erroneous field detected by the ICAO message
#                   parser.
# extracted_route:  An instance of ExtractedRouteSequence that contains the extracted
#                   route as derived from ICAO field 15.
# message_type:     The message type, ICAO ATS, OLDI or ADEXP
# f22_flight_plan:  An instance of a FlightPlanRecord instance that is populated from
#                   ICAO field 22. Field 22 theoretically can contain a complete flight
#                   plan.
class FlightPlanRecord:
    # The complete message as a string that was parsed / processed
    message_complete: str = ""

    # Message header without the message body
    message_header: str = ""

    # Message body without the message header
    message_body: str = ""

    # The sending unit adjacent unit name
    sender_adjacent_unit_name: AdjacentUnits = None

    # The receiving unit adjacent unit name
    receiver_adjacent_unit_name: AdjacentUnits = None

    # ICAO fields extracted from the original message
    icao_fields: (FieldIdentifiers, FieldRecord) = {}

    # Contains a list of error records;
    # If the message parser detects an erroneous field it is stored
    # with its start, end index and an appropriate error message.
    erroneous_fields: list[ErrorRecord] = []

    # Extracted route as generated by the field 15 parser
    extracted_route: ExtractedRouteSequence | None = None

    # Describes the message type
    message_type: MessageTypes = MessageTypes.UNKNOWN

    # The following is a flight plan record populated by field 22 items
    # This member is a data type 'FlightPlanRecord' (recurse on this class).
    # Python does not allow a recursive type definition here, type is set
    # on the getter and setter.
    f22_flight_plan: object = None

    # Constructor that all members in this class, strings are set to empty
    # strings, data structures are set to None or empty lists / dictionaries.
    def __init__(self):
        self.message_complete = ""
        self.message_header = ""
        self.message_body = ""
        self.icao_fields = {}
        self.erroneous_fields = []
        self.extracted_route = None
        self.message_type = MessageTypes.UNKNOWN
        self.f22_flight_plan = None
        self.receiver_adjacent_unit_name = AdjacentUnits.DEFAULT
        self.sender_adjacent_unit_name = AdjacentUnits.DEFAULT

    def add_erroneous_field(self, erroneous_field_text, error_text, start_index, end_index):
        # type: (str, str, int, int) -> None
        self.erroneous_fields.append(ErrorRecord(
            erroneous_field_text, error_text, start_index, end_index))

    def get_erroneous_fields(self):
        # type: () -> [ErrorRecord]
        return self.erroneous_fields

    def errors_detected(self):
        # type: () -> bool
        return len(self.erroneous_fields) > 0

    def set_message_complete(self, message_complete):
        # type: (str) -> None
        self.message_complete = message_complete

    def set_message_header(self, message_header):
        # type: (str) -> None
        self.message_header = message_header

    def set_message_body(self, message_body):
        # type: (str) -> None
        self.message_body = message_body

    def get_message_complete(self):
        # type: () -> str
        return self.message_complete

    def get_message_header(self):
        # type: () -> str
        return self.message_header

    def get_message_body(self):
        # type: () -> str
        return self.message_body

    # This method adds an ICAO field to this flight plan record.
    # All ICAO fields are stored in a dedicated dictionary indexed
    # with enumerations found in MessageDescription.FieldIdentifiers
    # The enumeration values used for the ICAO field dictionary are:
    # F3, F5, F7, F8, F9, F10, F13, F14, F15, F16, F17, F18, F19,
    # F22, F80, F81, MFS_SIG_POINT, RQS_FREE_TEXT
    def add_icao_field(self, field_id, field, start_index, end_index):
        # type: (FieldIdentifiers, str, int, int) -> None
        self.icao_fields[field_id] = FieldRecord(field, start_index, end_index)

    # This method adds an ICAO subfield to this flight plan record
    # All ICAO subfields are stored in a dedicated dictionary indexed
    # with enumerations found in MessageDescription.SubFieldIdentifiers
    # The enumeration values used for the ICAO field dictionary are:
    # F3a, F3b, F3c, F5a, F5b, F5c, F7a, F7b, F7c, F8a, F8b,
    # F9a, F9b, F9c, F10a, F10b, F13a, F13b, F14a, F14b, F14c, F14d, F14e,
    # F16a, F16b, F16c, F16d, F17a, F17b, F17c, F18altn, F18code, F18com,
    # F18dat, F18dep, F18dest, F18dof, F18eet, F18est, F18ifp, F18nav,
    # F18opr, F18per, F18ralt, F18reg, F18rif, F18rfp, F18rmk, F18rvr,
    # F18sel, F18sts, F18src, F18typ, F18orgn, F19a, F19c, F19d, F19e,
    # F19j, F19n, F19p, F19r, F19s, F80a, F80b, F81a, F81b
    # The header fields stored are:
    # PRIORITY_INDICATOR
    # FILING_TIME
    # ORIGINATOR
    # ADDRESS
    # ADADDRESS
    def add_icao_subfield(self, field_id, subfield_id, field, start_index, end_index):
        # type: (FieldIdentifiers, SubFieldIdentifiers, str, int, int) -> None
        self.get_icao_field(field_id).add_subfield(subfield_id, SubFieldRecord(field, start_index, end_index))

    # Gets an ICAO field from this flight plan record
    def get_icao_field(self, field_id):
        # type: (FieldIdentifiers) -> FieldRecord
        return self.icao_fields[field_id]

    def get_icao_subfield(self, field_id, subfield_id):
        # type: (FieldIdentifiers, SubFieldIdentifiers) -> SubFieldRecord
        return self.get_icao_field(field_id).get_subfield(subfield_id)

    # Sets an instance of this class that contains F22 fields
    # extracted from a flight plan field 22.
    def set_f22_flight_plan(self, f22_flight_plan):
        # type: (FlightPlanRecord) -> None
        self.f22_flight_plan = f22_flight_plan

    # Gets an instance of this class that contains F22 fields
    # extracted from a flight plan field 22.
    def get_f22_flight_plan(self):
        # type: () -> FlightPlanRecord
        return self.f22_flight_plan

    # Sets an extracted route derived from a message F15;
    # field 15 is parsed by a dedicated parser that creates
    # an instance of the ExtractedRouteSequence class.
    def add_extracted_route(self, extracted_route):
        # type: (ExtractedRouteSequence) -> None
        self.extracted_route = extracted_route

    # Gets the extracted route for this flight plan;
    # field 15 is parsed by a dedicated parser that creates
    # an instance of the ExtractedRouteSequence class.
    def get_extracted_route(self):
        # type: () -> ExtractedRouteSequence
        return self.extracted_route

    # Set the message type, OLDI, ATS or ADEXP.
    def set_message_type(self, message_type):
        # type: (MessageTypes) -> None
        self.message_type = message_type

    # Get the message type, OLDI, ATS or ADEXP.
    def get_message_type(self):
        # type: () -> MessageTypes
        return self.message_type

    # Get the ERS from the flight plan record
    def get_extracted_route_sequence(self):
        # type: () -> ExtractedRouteSequence | None
        return self.extracted_route

    # Method to check if the ERS has any errors
    def f15_errors_exist(self):
        # type: () -> bool
        if self.get_extracted_route_sequence() is None:
            return False
        return self.get_extracted_route_sequence().get_number_of_errors() > 0

    # Method to return the list of field 15 error tokens (contain errors etc.)
    def get_f15_errors(self):
        # type: () -> [ExtractedRouteRecord]
        return self.get_extracted_route_sequence().get_all_errors()

    # Get receiving unit adjacent unit name
    def get_receiver_adjacent_unit_name(self):
        # type: () -> AdjacentUnits
        return self.receiver_adjacent_unit_name

    # Get sender unit adjacent unit name
    def get_sender_adjacent_unit_name(self):
        # type: () -> AdjacentUnits
        return self.sender_adjacent_unit_name

    # Set receiving unit adjacent unit name
    def set_receiver_adjacent_unit_name(self, receiver_adjacent_unit_name):
        # type: (AdjacentUnits) -> None
        self.receiver_adjacent_unit_name = receiver_adjacent_unit_name

    # Set sender unit adjacent unit name
    def set_sender_adjacent_unit_name(self, sender_adjacent_unit_name):
        # type: (AdjacentUnits) -> None
        self.sender_adjacent_unit_name = sender_adjacent_unit_name
