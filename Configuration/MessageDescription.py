# This class is used to store all ICAO field identifiers of an ICAO ATS or OLDI message.
# The content is given as a list of ICAO field identifiers; the field lists
# vary depending on the message title. Refer to ICAO DOC 4444 and the OLDI
# specification that specify the fields for a given message title.
# The message content is defined in the MessageDescriptions.MessageContentDescriptions
# class.
# This class stores the following information about a message:
# message_title:        An OLDI or ICAO message title such as 'FPL', 'ACT' etc.
# message_description:  A short textual description of the message
# message_fields:       A list of fields supported / expected in a message using
#                       ICAO field numbers as defined in ICAO DOC 4444.
# specific_field_22:    A list of field 22 subfields allowed in this message. In
#                       ICAO ATS messages, field 22 can contain any of the ICAO fields.
#                       But OLDI messages are only allowed a specific subset; hence
#                       the subset is stored here.
# The class does not implement any 'setter' methods as this class is instantiated
# as a 'read' only class storing message configuration data.
from Configuration.EnumerationConstants import FieldIdentifiers
from IcaoMessageParser.ParseFieldsCommon import ParseFieldsCommon


class MessageDescription:

    # An OLDI or ICAO message title such as 'FPL', 'ACT' etc.
    message_title: str = ""

    # A short textual description of the message
    message_description: str = ""

    # A list of fields supported / expected in a message using ICAO field numbers
    # as defined in ICAO DOC 4444. These are defined using enumeration
    # values defined in EnumerationConstants.FieldIdentifiers
    message_fields: [FieldIdentifiers] = None

    # This list is used where specific message titles only permit a limited
    # number of fields, (occurs only with OLDI messages). These are defined
    # using enumeration values defined in EnumerationConstants.FieldIdentifiers
    specific_field_22: [FieldIdentifiers] = None

    # A list of parser callback classes
    field_parsers: [ParseFieldsCommon] = None

    # This constructor populates all the class members.
    def __init__(self, message_title, message_description, field_parsers, message_fields, specific_field_22):
        # type: (str, str, [ParseFieldsCommon], [FieldIdentifiers], [FieldIdentifiers]) -> None
        self.message_title = message_title
        self.message_description = message_description
        self.field_parsers = field_parsers
        self.message_fields = message_fields
        self.specific_field_22 = specific_field_22

    # Get the message title
    def get_message_title(self):
        # type: () -> str
        return self.message_title

    # Get the message description
    def get_message_description(self):
        # type: () -> str
        return self.message_description

    # Get the list of ICAO fields that define the content for this message
    def get_message_fields(self):
        # type: () -> [FieldIdentifiers]
        return self.message_fields

    # Get the list of ICAO fields that define field 22 content for this message
    def get_specific_field_22(self):
        # type: () -> [FieldIdentifiers]
        return self.specific_field_22

    # Get the number of message fields
    def get_number_of_fields_in_message(self):
        # type: () -> int
        return len(self.message_fields)

    # Get the list of parser callback classes
    def get_field_parsers(self):
        # type: () -> [ParseFieldsCommon]
        return self.field_parsers

    def print(self):
        str_ = "{0:<17}".format(self.get_message_title()) + \
               "{0:<17}".format(self.get_message_description()) + \
               "{0:<17}".format(self.get_message_fields()) + \
               "{0:<17}".format(self.get_specific_field_22())
        print(str_)
