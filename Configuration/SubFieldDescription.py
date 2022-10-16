from Configuration.EnumerationConstants import SubFieldIdentifiers


# This class contains a description of an ICAO subfield. For example, ICAO
# field 13 comprises fields 'a' (ADEP Location indicator) and 'b' (the EOBT).
# This class stores information about one of these subfields and is used by the
# parser to check a fields syntax and semantics.
# The subfield content is described in the MessageDescriptions.SubFieldContentDefinitions
# class for ICAO fields and subfields.
# This class stores the following information about a subfield:
# subfield_id - A subfield enumeration value identifying a subfield MessageDescriptions.IcaoSubFieldIDs;
# field_syntax - A regular expression defining the syntax and semantics of a subfield;
# maximum_field_length - Maximum length of a subfield;
# minimum_field_length - Minimum length of a subfield;
# is_compulsory - Indicates if this subfield is optional or not;
# The class does not implement any 'setter' methods as this class is instantiated
# as a 'read' only class storing subfield configuration data.
class SubFieldDescription:
    # A subfield identifier as defined in MessageDescriptions.IcaoSubFieldIDs,
    # these can be mapped to the ICAO field identifiers as specified in ICAO DOC 4444.
    subfield_id: SubFieldIdentifiers = 0

    # Field syntax definition expressed as a regular expression
    field_syntax: str = ""

    # Maximum field length
    maximum_field_length: int = 0

    # Minimum field length
    minimum_field_length: int = 0

    # Boolean to indicate if the field is compulsory or not
    is_compulsory: bool = False

    # This constructor populates all the class members.
    def __init__(self, subfield_id, minimum_field_length,
                 maximum_field_length, field_syntax, is_compulsory):
        # type: (SubFieldIdentifiers, int, int, str, bool) -> None
        self.subfield_id = subfield_id
        self.minimum_field_length = minimum_field_length
        self.maximum_field_length = maximum_field_length
        self.field_syntax = field_syntax
        self.is_compulsory = is_compulsory

    # Gets the subfields ID as an enumeration value defined
    # in EnumerationConstants.SubFieldIdentifiers
    def get_subfield_id(self):
        # type: () -> SubFieldIdentifiers
        return self.subfield_id

    # Gets a subfields syntax description using a regular expression
    def get_field_syntax(self):
        # type: () -> str
        return self.field_syntax

    # Gets the maximum length of this subfield
    def get_maximum_field_length(self):
        # type: () -> int
        return self.maximum_field_length

    # Gets the minimum length of this subfield
    def get_minimum_field_length(self):
        # type: () -> int
        return self.minimum_field_length

    # Gets a flag indicating if this field is optional or not.
    def get_compulsory(self):
        # type: () -> bool
        return self.is_compulsory
