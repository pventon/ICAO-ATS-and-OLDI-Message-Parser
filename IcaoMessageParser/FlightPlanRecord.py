"""The classes in this file together represent a complete flight plan; the overall
structure for a flight plan record is made up from all the classes in this file in
the following manner:

FlightPlanRecord -+-->  FieldRecord -+--> [SubFieldRecord, ...]
                  |                  +--> [SubFieldRecord, ...]
                  |                  +--> [SubFieldRecord, ...]
                  |                  +--> ...
                  +-->  FieldRecord -+--> [SubFieldRecord, ...]
                  |                  +--> [SubFieldRecord, ...]
                  |                  +--> [SubFieldRecord, ...]
                  |                  +--> ...
                  +-->  ...
                  +--> ErrorRecord
                  +--> ...
1. FieldRecord classes are stored in a FlightPlanRecord dictionary and indexed
   with enumeration values from FieldIdentifiers; FieldRecord's inherit from
   the SubFieldRecord class.
2. SubFieldRecord classes are stored in a FieldRecord dictionary and indexed
   with enumeration values from SubFieldIdentifiers;
3. ErrorRecord classes are stored in a FlightPlanRecord list; ErrorRecord's
   inherit from the SubFieldRecord class.
4. Note that the subfields are in a list; this covers the case for some field 18 subfields
   such as the RMK and STS subfields that can occur more than once in field 18."""
from Configuration.EnumerationConstants import MessageTypes, FieldIdentifiers, SubFieldIdentifiers, AdjacentUnits, \
    MessageTitles, FlightRules
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence, ExtractedRouteRecord


class SubFieldRecord:
    """This class stores an ICAO subfield added to a flight plan record during ICAO message parsing.

    There are 'n' subfields contained in a flight plan record created by the ICAO message parser.

    A subfield is stored with its zero based start and end index into the original message.

    The ICAO message parser creates and adds a FieldRecord to a flight plan record for each ICAO field
    located in a message; the ICAO field is further decomposed into its constitute subfields and the subfields
    are stored as part of their parent ICAO fields in a FieldRecord.

    There are no 'setter' methods in this class as the constructor initialises all members on class
    instantiation making this class effectively 'read' only."""

    field_text: str = ""
    """A string that is the subfield, i.e. 'LOWL', '0234' etc."""

    start_index: int = 0
    """An integer representing the zero based index for the start of the subfield in the original message string."""

    end_index: int = 0
    """An integer representing the zero based index for the end of the subfield in the original message string."""

    def __init__(self, field_text, start_index, end_index):
        # type: (str, int, int) -> None
        """Constructor that initializes all class members

        :param field_text: A string that is the subfield, i.e. 'LOWL', '0234' etc.
        :param start_index: An integer representing the zero based index for the start of the
                            subfield in the original message string.
        :param end_index: An integer representing the zero based index for the end of the
                          subfield in the original message string."""
        self.field_text = field_text
        self.start_index = start_index
        self.end_index = end_index

    def get_field_text(self):
        # type: () -> str
        """Gets the subfield text as it appears in the original message
        :return: The subfield text"""
        return self.field_text

    def get_start_index(self):
        # type: () -> int
        """Gets the zero based index of the subfields start position in the original message
        :return: The zero based index of the subfields start position in the original message"""
        return self.start_index

    def get_end_index(self):
        # type: () -> int
        """Gets the zero based index of the subfields end position in the original message
        :return: The zero based index of the subfields end position in the original message"""
        return self.end_index

    def subfield_as_xml(self, subfield_id):
        # type: (SubFieldIdentifiers) -> str
        """This method returns an XML representation of the contents of this class.

        :return: An XML representation of the contents of this class as a string"""
        return "      <subfield_record id=\"" + subfield_id.name + \
               "\" name=\"" + self.get_field_text() + \
               "\" start_index=\"" + str(self.get_start_index()) + \
               "\" end_index=\"" + str(self.get_end_index()) + "\">" + \
               "</subfield_record>"


class FieldRecord(SubFieldRecord):
    """This class stores an ICAO field added to a flight plan record during ICAO
    message parsing. There are 'n' ICAO fields contained in a flight plan record
    created by the ICAO message parser.

    This class inherits from the SubFieldRecord.

    A field is stored with its zero based start and end index into the original
    message.

    The ICAO message parser creates and adds a FieldRecord for each ICAO field located
    in a message; the ICAO field is further decomposed into its constitute subfields and
    the subfields are stored in this class in a dictionary using the SubFieldIdentifiers
    enumeration as the dictionary key. Some ICAO fields, such as field 18, may have
    several subfields with the same name, (e.g. the STS and RMK subfields can occur
    more than once in a message). To cater for this, the subfields are stored as
    a list of subfields in the subfield's member.

    There is a single 'add' method to add subfields to this class."""

    subfields: (SubFieldIdentifiers, [SubFieldRecord]) = {}
    """A dictionary containing a list of ICAO subfields extracted from a message. The 
    subfields are stored as a list because some ICAO subfields may occur more than once,
    (e.g. the STS and RMK subfields can occur ore than once in a message). The key to
    this dictionary are enumeration values from the EnumerationConstants.SubFieldIdentifiers
    class."""

    def __init__(self, field_text, start_index, end_index):  # , field_identifier):
        # type: (str, int, int) -> None
        """Constructor that initializes all the sub_fields class member with an
        empty subfield dictionary and a fully populated ICAO field.
            :param field_text: The ICAO field as it appears in a message
            :param start_index: The zero based start index of the ICAO fields position in the original message string
            :param end_index: The zero based end index of the ICAO fields position in the original message string
            :return: None"""
        super().__init__(field_text, start_index, end_index)
        self.subfields = {}

    def add_subfield(self, icao_subfield_id, subfield):
        # type: (SubFieldIdentifiers, SubFieldRecord) -> None
        """Adds an ICAO subfield to this ICAO field record
            :param icao_subfield_id: The ICAO field that this subfield is being added to
            :param subfield: The ICAO subfield being added
            :return: None"""
        list_of_subfield: [SubFieldRecord] = self.get_all_subfields(icao_subfield_id)
        if list_of_subfield is None:
            self.subfields[icao_subfield_id] = [subfield]
        else:
            list_of_subfield.append(subfield)

    def get_subfield(self, icao_subfield_id):
        # type: (SubFieldIdentifiers) -> SubFieldRecord | None
        """Returns a single subfield or None if the subfield does not exist. This method
        always returns the first subfield in the list of subfields; typically there is only
        one subfield. For some fields such as field 18 there may be more than one subfield
        with the same name.
            :param icao_subfield_id: The ICAO subfield identifier
            :return: The ICAO subfield or None if the subfield does not exist; if multiple
            subfields exist, this method always the returns the first subfield in the list
            of subfields"""
        if self.contains_subfield(icao_subfield_id):
            return self.subfields[icao_subfield_id][0]
        else:
            return None

    def get_subfield_dictionary(self):
        # type: () -> (SubFieldIdentifiers, [SubFieldRecord])
        """This method returns the complete subfield dictionary stored in this field record; for
        fields such as F18, F19 or F22 there may be a lot of subfields. This method is used primarily
        to loop over the subfields of compound fields such as F18, F19 and F22 to parse the individual
        subfields.
        :return: A dictionary with SubFieldIdentifiers as key and a list of one or more subfields as the
        value;
        """
        return self.subfields

    def get_all_subfields(self, icao_subfield_id):
        # type: (SubFieldIdentifiers) -> [SubFieldRecord]
        """Returns all subfields with the icao_subfield_id or None if the subfield does not
        exist. For some fields such as field 18 there may be more than one subfield
        with the same name/icao_subfield_id.
            :param icao_subfield_id: The ICAO subfield identifier
            :return: A list of ICAO subfields or None if the subfield does not exist"""
        if self.contains_subfield(icao_subfield_id):
            return self.subfields[icao_subfield_id]
        else:
            return None

    def contains_subfield(self, icao_subfield_id):
        # type: (SubFieldIdentifiers) -> bool
        """Checks if the dictionary of subfields contains an entry with the key
        icao_subfield_id.
            :param icao_subfield_id: The ICAO subfield identifier being checked
            :return: True if the subfield dictionary contains an entry with the key
                     icao_subfield_id, False otherwise"""
        return icao_subfield_id in self.subfields

    def field_as_xml(self, field_id):
        # type: (FieldIdentifiers) -> str
        """This method returns an XML representation of the contents of this class.

        :return: An XML representation of the contents of this class as a string"""

        # Build the subfield elements first if any are present
        subfield_xml = ""
        if len(self.subfields) > 0:
            for subfield_id, subfield in self.subfields.items():
                if len(subfield) > 0:
                    for sf in subfield:
                        subfield_xml = subfield_xml + sf.subfield_as_xml(subfield_id) + "\n"

        return "   <field_record id=\"" + field_id.name + \
               "\" name=\"" + self.get_field_text() + \
               "\" start_index=\"" + str(self.get_start_index()) + \
               "\" end_index=\"" + str(self.get_end_index()) + "\">\n" + \
               subfield_xml + \
               "   </field_record>"


class ErrorRecord(SubFieldRecord):
    """This class contains information about an error detected during message processing.
    The erroneous field along with its zero based start and end index in the message plus
    the error message is stored in this class.
    Zero or more of these records may be included in a flight plan record.
     This class subclasses the FieldRecord class."""

    error_message: str = ""
    """Contains the error message associated with the erroneous token."""

    def __init__(self, erroneous_field_text, error_message, start_index, end_index):
        # type: (str, str, int, int) -> None
        """Constructor that initializes all the subFieldRecord class members and in
         addition, sets the error message associated with the subfield information in this class.
            :param erroneous_field_text: The ICAO subfield as it appears in a message
            :param error_message: The error message
            :param start_index: The zero based start index of the ICAO subfields position in the original message string
            :param end_index: The zero based end index of the ICAO subfields position in the original message string
            :return: None"""
        super().__init__(erroneous_field_text, start_index, end_index)
        self.error_message = error_message

    def get_error_message(self):
        # type: () -> str
        """Gets the error message reported on this subfield
        :return: The error message"""
        return self.error_message

    def field_error_as_xml(self):
        # type: () -> str
        """This method returns an XML representation of the contents of this class.

        :return: An XML representation of the contents of this class as a string"""

        return "   <error=\"" + self.get_field_text() + \
               "\" start_index=\"" + str(self.get_start_index()) + \
               "\" end_index=\"" + str(self.get_end_index()) + \
               "\" error_message=\"" + self.get_error_message() + "\">" + \
               "</error>"


class FlightPlanRecord:
    """This class contains data representing a complete flight plan."""

    message_complete: str = ""
    """A string that is the complete message as input to the ICAO message parser"""

    message_header: str = ""
    """A string that is the message header as input to the ICAO message parser"""

    message_body: str = ""
    """A string that is the message body; it is this data that represents a flight plan"""

    sender_adjacent_unit_name: AdjacentUnits = None
    """The adjacent unit senders name extracted from ICAO field 3b for OLDI messages"""

    receiver_adjacent_unit_name: AdjacentUnits = None
    """The adjacent unit receivers name extracted from ICAO field 3b for OLDI messages"""

    icao_fields: (FieldIdentifiers, FieldRecord) = {}
    """A dictionary containing individual ICAO fields extracted from a message body. The key 
    to this dictionary are enumeration values from the EnumerationConstants.FieldIdentifiers class."""

    erroneous_fields: list[ErrorRecord] = []
    """A list contain zero or more ErrorRecord class instances; each record contains an
    erroneous field detected by the ICAO message parser along with its start, end index
    and an appropriate error message."""

    extracted_route: ExtractedRouteSequence | None = None
    """An instance of ExtractedRouteSequence that contains the extracted route as 
    derived from ICAO field 15."""

    # Describes the message type
    message_type: MessageTypes = MessageTypes.UNKNOWN
    """The message type, ICAO ATS, OLDI, ADEXP or UNKNOWN, one of the enumeration values 
    from EnumerationConstants.MessageTypes"""

    f22_flight_plan: object = None
    """An instance of a FlightPlanRecord that is populated from ICAO field 22.
    Field 22 theoretically can contain a complete flight plan.
    This member is a data type 'FlightPlanRecord' (recurse on this class). Python does not allow
    a recursive type definition here, hence the type is set on the getter and setter."""

    message_title: MessageTitles = MessageTitles.UNKNOWN
    """The message title as an enumeration value from the MessageTitles enumeration class."""

    derived_flight_rules: FlightRules = FlightRules.UNKNOWN
    """The flight rules as derived from Field 15 route extraction processing;"""

    def __init__(self):
        """Constructor that initialises all members in this class, strings are set to empty
        strings, data structures are set to None or empty lists / dictionaries."""
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
        self.message_title = MessageTitles.UNKNOWN
        self.derived_flight_rules = FlightRules.UNKNOWN

    def add_erroneous_field(self, erroneous_field_text, error_text, start_index, end_index):
        # type: (str, str, int, int) -> None
        """Adds a field or subfield to this flight plan record that the parser has found to be either
        syntactically or semantically incorrect. The erroneous field is stored with its text, start and
        end index into the original message and an associate error message that describes the problem
        with the field/subfield.
            :param erroneous_field_text: The ICAO subfield as it appears in a message
            :param error_text: The error message
            :param start_index: The zero based start index of the ICAO subfields position in the original message string
            :param end_index: The zero based end index of the ICAO subfields position in the original message string
            :return: None"""
        self.erroneous_fields.append(ErrorRecord(
            erroneous_field_text, error_text, start_index, end_index))

    def add_extracted_route(self, extracted_route):
        # type: (ExtractedRouteSequence) -> None
        """Sets an extracted route derived from ICAO field 15; field 15 is parsed by a dedicated parser
        that creates an extracted route sequence output into an instance of the
        ExtractedRouteSequence class.
            :param extracted_route: An instance of the ExtractedRouteSequence class containing an extracted route
            :return: None"""
        self.extracted_route = extracted_route

    def add_icao_field(self, field_id, field, start_index, end_index):
        # type: (FieldIdentifiers, str, int, int) -> None
        """This method adds an ICAO field to this flight plan record. All ICAO fields are stored
        in a dedicated dictionary indexed with enumeration values found in
        the EnumerationConstants.FieldIdentifiers class.
            :param field_id: ICAO field identifier as defined in the EnumerationConstants.FieldIdentifiers class
            :param field: The text that is the ICAO field
            :param start_index: The zero based start index of the ICAO fields position in the original message string
            :param end_index: The zero based end index of the ICAO fields position in the original message string
            :return: None"""
        self.icao_fields[field_id] = FieldRecord(field, start_index, end_index)

    def add_icao_subfield(self, field_id, subfield_id, field, start_index, end_index):
        # type: (FieldIdentifiers, SubFieldIdentifiers, str, int, int) -> None
        """This method adds an ICAO subfield to this flight plan record. All ICAO subfields are stored
        in a dedicated dictionary indexed with enumeration values found in
        the EnumerationConstants.SubFieldIdentifiers class.
            :param field_id: ICAO field identifier as defined in the EnumerationConstants.FieldIdentifiers class
            :param subfield_id: ICAO subfield identifier as defined in the EnumerationConstants.SubFieldIdentifiers
            class
            :param field: The text that is the ICAO subfield
            :param start_index: The zero based start index of the ICAO subfields position in the original message string
            :param end_index: The zero based end index of the ICAO subfields position in the original message string
            :return: None"""
        self.get_icao_field(field_id).add_subfield(subfield_id, SubFieldRecord(field, start_index, end_index))

    def as_xml(self):
        # type: () -> str
        """This method returns an XML representation of the flight plan record.

        :return: An XML representation of the flight plan record as an XML string"""

        # Build the records as an XML
        field_string = ""
        if len(self.icao_fields) > 0:
            field_string = "<icao_fields>\n"
            for field_id, record in self.icao_fields.items():
                field_string = field_string + record.field_as_xml(field_id) + "\n"
            field_string = field_string + "</icao_fields>\n"

        error_string = ""
        if len(self.erroneous_fields) > 0:
            error_string = "<icao_field_errors>\n"
            for error_record in self.erroneous_fields:
                error_string = error_string + error_record.field_error_as_xml() + "\n"
            error_string = error_string + "</icao_field_errors\n"

        # erroneous_fields: list[ErrorRecord] = []
        return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\" ?>\n" + \
               "<flight_plan_record>\n" + \
               "   <derived_flight_rules>" + self.get_derived_flight_rules().name + "</derived_flight_rules>\n"\
               "   <message_type>" + self.get_message_type().name + "</message_type>\n" + \
               "   <original_message>" + self.get_message_complete() + "</original_message>\n" + \
               "   <message_header>" + self.get_message_header() + "</message_header>\n" + \
               "   <message_body>" + self.get_message_body() + "</message_body>\n" + \
               "   <adjacent_unit sender=\"" + self.get_sender_adjacent_unit_name().name + \
               "\" receiver=\"" + self.get_receiver_adjacent_unit_name().name + "\"></adjacent_unit>\n" + \
               field_string + \
               error_string + \
               self.get_extracted_route_sequence().as_xml() + \
               "\n</flight_plan_record>"

    def errors_detected(self):
        # type: () -> bool
        """Return True if this flight plan record contains any erroneous fields
        :return: true if any erroneous fields are present in this flight plan record"""
        return len(self.erroneous_fields) > 0

    def f15_errors_exist(self):
        # type: () -> bool
        """Check if the Extracted Route Sequence has any errors

            :return: True if errors were detected while parsing ICAO field 15, False otherwise"""
        if self.get_extracted_route_sequence() is None:
            return False
        return self.get_extracted_route_sequence().get_number_of_errors() > 0

    def get_all_icao_subfields(self, field_id, subfield_id):
        # type: (FieldIdentifiers, SubFieldIdentifiers) -> [SubFieldRecord]
        """Gets all subfields associated with an ICAO field that can contains multiple subfields with the
        same subfield identifier, e.g. Field 18 may contain mor ethan one STS or RMK field.
            :param field_id: ICAO field identifier as defined in the EnumerationConstants.FieldIdentifiers class
            :param subfield_id: ICAO subfield identifier as defined in the EnumerationConstants.SubFieldIdentifiers
            class
            :return: A list contain one or more instances of the SubFieldRecord class that contains an ICAO subfield
        """
        return self.get_icao_field(field_id).get_all_subfields(subfield_id)

    def get_derived_flight_rules(self):
        # type: () -> FlightRules
        """Get the flight rules derived and set from parsing F15; this is not the rules from F8,
        this is the rules derived from the route extraction parsing.

        :return: The flight rules as derived by parsing F15 as an enumeration value from the
                 FlightRules enumeration class;
        """
        return self.derived_flight_rules

    def get_erroneous_fields(self):
        # type: () -> [ErrorRecord]
        """Gets the field/subfield text for this erroneous field/subfield
        :return: The erroneous field text as it appears in the original message being parsed"""
        return self.erroneous_fields

    def get_extracted_route(self):
        # type: () -> ExtractedRouteSequence
        """Gets the extracted route for this flight plan; field 15 is parsed by a dedicated parser that creates
        an instance of the ExtractedRouteSequence class.
        :return: The extracted route sequence as an instance of the ExtractedRouteSequence class"""
        return self.extracted_route

    def get_extracted_route_sequence(self):
        # type: () -> ExtractedRouteSequence | None
        """Get the Extracted Route Sequence from the flight plan record

            :return: The extracted route sequence as derived by the field 15 parser from ICAO field 15"""
        return self.extracted_route

    def get_f15_errors(self):
        # type: () -> [ExtractedRouteRecord]
        """Return the list of field 15 error records (contain errors etc.)

            :return: A list of errors reported by the ICAO field 15 parser"""
        return self.get_extracted_route_sequence().get_all_errors()

    def get_f22_flight_plan(self):
        # type: () -> FlightPlanRecord
        """Gets an instance of this class that contains F22 fields extracted from a flight plan field 22.
        :return: An instance of this class that contains F22 fields extracted from a flight plan field 22"""
        return self.f22_flight_plan

    def get_icao_field(self, field_id):
        # type: (FieldIdentifiers) -> FieldRecord | None
        """Gets an ICAO field from this flight plan record

            :param field_id: ICAO field identifier as defined in the EnumerationConstants.FieldIdentifiers class
            :return: An instance of FieldRecord that contains an ICAO field or None if the flight pla
                     record does not contain the field identified by field_id"""
        # Check if the flight plan contains the field 'field_id'
        if field_id not in self.icao_fields:
            return None
        return self.icao_fields[field_id]

    def get_icao_subfield(self, field_id, subfield_id):
        # type: (FieldIdentifiers, SubFieldIdentifiers) -> SubFieldRecord | None
        """Gets an ICAO subfield from this flight plan record

            :param field_id: ICAO field identifier as defined in the EnumerationConstants.FieldIdentifiers class
            :param subfield_id: ICAO subfield identifier as defined in the EnumerationConstants.SubFieldIdentifiers
            class
            :return: An instance of SubFieldRecord that contains an ICAO subfield"""
        if self.get_icao_field(field_id) is None:
            return None
        return self.get_icao_field(field_id).get_subfield(subfield_id)

    def get_message_body(self):
        # type: () -> str
        """Gets the complete ICAO message body
            :return: The ICAO message body as input for parsing"""
        return self.message_body

    def get_message_complete(self):
        # type: () -> str
        """Gets the complete ICAO message including the header (if present)
            :return: The ICAO message as input for parsing"""
        return self.message_complete

    def get_message_header(self):
        # type: () -> str
        """Gets the ICAO message header (if present)
            :return: The ICAO message header as input for parsing"""
        return self.message_header

    def get_message_title(self):
        # type: () -> MessageTitles
        """Get the message title assigned to this flight plan record during F3 parsing.
        Will be assigned 'UNKNOWN' if a message did not contain F3.

        :return: The message title as an enumeration value from the MessageTitles class;
        """
        return self.message_title

    def get_message_type(self):
        # type: () -> MessageTypes
        """Gets the message type, defined in the EnumerationConstants.AdjacentUnits class.

            :return: Message type as one of the enumeration values from the EnumerationConstants.MessageTypes class"""
        return self.message_type

    def get_receiver_adjacent_unit_name(self):
        # type: () -> AdjacentUnits
        """Gets the receiver adjacent unit name as extracted from ICAO field 3b; stored
        as an enumeration value defined in the EnumerationConstants.AdjacentUnits class.
            :return: Adjacent unit name as an enumeration value from EnumerationConstants.AdjacentUnits"""
        return self.receiver_adjacent_unit_name

    def get_sender_adjacent_unit_name(self):
        # type: () -> AdjacentUnits
        """Gets the sender adjacent unit name as extracted from ICAO field 3b; stored
        as an enumeration value defined in the EnumerationConstants.AdjacentUnits class.
            :return: Adjacent unit name as an enumeration value from EnumerationConstants.AdjacentUnits"""
        return self.sender_adjacent_unit_name

    def set_derived_flight_rules(self, derived_flight_rules):
        # type: (FlightRules) -> None
        """Set the flight rules from F15 parsing; this is not the rules from F8, this is the rules
        derived from the route extraction parsing.

        :param derived_flight_rules: The flight rules to set as derived by parsing F15 as an
               enumeration value from the FlightRules enumeration class;
        :return: None
        """
        self.derived_flight_rules = derived_flight_rules

    def set_f22_flight_plan(self, f22_flight_plan):
        # type: (FlightPlanRecord) -> None
        """Sets an instance of this class that contains F22 fields extracted from a flight plan field 22.

            :param f22_flight_plan: An instance of FlightPlanRecord containing fields extracted from ICAO F22
            :return: None"""
        self.f22_flight_plan = f22_flight_plan

    def set_message_body(self, message_body):
        # type: (str) -> None
        """Stores the message body as received in the message being parsed,
        the message body is defined ICAO DOC 4444 and the OLDI 4.2 specification
            :param message_body: The ICAO message body
            :return: None"""
        self.message_body = message_body

    def set_message_complete(self, message_complete):
        # type: (str) -> None
        """Stores the complete message being parsed from the start of its header
        (if present) to the end of the message
            :param message_complete: The ICAO message being stored
            :return: None"""
        self.message_complete = message_complete

    def set_message_header(self, message_header):
        # type: (str) -> None
        """Stores the message header (if present) as received in the message being parsed,
        the message header is defined ICAO Annex 10, Vol II
            :param message_header: The ICAO message header
            :return: None"""
        self.message_header = message_header

    def set_message_title(self, message_title):
        # type: (MessageTitles) -> None
        """Set the message title, assigned during F3 parsing.
        Will be assigned 'UNKNOWN' if a message did not contain F3.

        :param message_title: The message title as an enumeration value from the MessageTitles class;
        :return: None
        """
        self.message_title = message_title

    def set_message_type(self, message_type):
        # type: (MessageTypes) -> None
        """Sets the message type, OLDI, ATS, ADEXP or UNKNOWN as defined in the
        EnumerationConstants.AdjacentUnits class.
            :param message_type: Message type as, enumeration value from EnumerationConstants.MessageTypes
            :return: None"""
        self.message_type = message_type

    def set_receiver_adjacent_unit_name(self, receiver_adjacent_unit_name):
        # type: (AdjacentUnits) -> None
        """Sets the receiver adjacent unit name as extracted from ICAO field 3b; stored
        as an enumeration value defined in the EnumerationConstants.AdjacentUnits class.
            :param receiver_adjacent_unit_name: Adjacent unit name as an enumeration value from
                EnumerationConstants.AdjacentUnits
            :return: None"""
        self.receiver_adjacent_unit_name = receiver_adjacent_unit_name

    def set_sender_adjacent_unit_name(self, sender_adjacent_unit_name):
        # type: (AdjacentUnits) -> None
        """Sets the sending adjacent unit name as extracted from ICAO field 3b; stored
        as an enumeration value defined in the EnumerationConstants.AdjacentUnits class.
            :param sender_adjacent_unit_name: Adjacent unit name as an enumeration value from
                EnumerationConstants.AdjacentUnits
            :return: None"""
        self.sender_adjacent_unit_name = sender_adjacent_unit_name
