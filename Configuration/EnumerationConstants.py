# This file contains severa; enumeration classes used as system-wide constants
# that define the following:
# MessageTitles ->          Enumerations for all supported ATS and OLDI message titles;
# FieldIdentifiers ->       Enumerations for all ICAO fields as defined in both OLDI
#                           standards and ICAO DOC 4444;
# SubFieldIdentifiers ->    Enumerations for all ICAO and OLDI message subfields; a
#                           subfield is derived as described in the ICAO DOC 4444.
# MessageTypes ->           Enumeration to define the type of message, OLDI, ICAO ATS,
#                           ADEXP or UNKNOWN. Determined by analysing a message during
#                           message parsing;
# AdjacentUnits ->          A list of adjacent unit identifiers used in combination with
#                           a message title and its type to determine the field content
#                           of OLDI messages. Unlike the ICAO ATS messages, the fields
#                           contained in an OLDI message are not fixed but vary depending
#                           on the adjacent unit that they are being exchanged on.
# ErrorId ->                Enumeration used to index error messages.
from enum import IntEnum, auto


# This enumeration class defines a unique identifier for each of the supported
# message titles.
class MessageTitles(IntEnum):
    # ATS Messages
    ACH = 0
    ACP = auto()  # This title is also defined as an OLDI message
    AFP = auto()
    ALR = auto()
    APL = auto()
    ARR = auto()
    CDN = auto()  # This title is also defined as an OLDI message
    CHG = auto()
    CNL = auto()
    CPL = auto()  # This title is also defined as an OLDI message
    DEP = auto()
    DLA = auto()
    EST = auto()
    FPL = auto()
    FNM = auto()
    MFS = auto()
    RCF = auto()
    RQP = auto()
    RQS = auto()
    SPL = auto()
    # OLDI Messages
    ABI = auto()
    # ACP = auto() This title is also defined as an ATS message
    ACT = auto()
    AMA = auto()
    # CDN = auto() This title is also defined as an ATS message
    COD = auto()
    # CPL = auto() This title is also defined as an ATS message
    INF = auto()
    LAM = auto()
    MAC = auto()
    OCM = auto()
    PAC = auto()
    RAP = auto()
    REJ = auto()
    REV = auto()
    RJC = auto()
    ROC = auto()
    RRV = auto()
    SBY = auto()


# This enumeration class defines a unique identifier for each of the ICAO fields;
# i.e. ICAO field 13 (ADEP and EOBT).
class FieldIdentifiers(IntEnum):
    PRIORITY_INDICATOR = 0
    FILING_TIME = auto()
    ORIGINATOR = auto()
    ADDRESS = auto()
    ADADDRESS = auto()
    F3 = auto()
    F5 = auto()
    F7 = auto()
    F8 = auto()
    F8a = auto()
    F9 = auto()
    F10 = auto()
    F13 = auto()
    F13a = auto()
    F14 = auto()
    F14a = auto()
    F15 = auto()
    F16 = auto()
    F16a = auto()
    F16ab = auto()
    F16abc = auto()
    F17 = auto()
    F18 = auto()
    F18_DOF = auto()
    F19 = auto()
    F20 = auto()
    F21 = auto()
    F22 = auto()
    F22_SPECIFIC = auto()
    F80 = auto()
    F81 = auto()
    MFS_SIG_POINT = auto()


# This enumeration class defines a unique identifier for each of the ICAO subfields;
# i.e. ICAO field 13 (ADEP and EOBT) are separated into two subfields, 13 'a' and 'b'.
class SubFieldIdentifiers(IntEnum):
    PRIORITY_INDICATOR = 0
    FILING_TIME = auto()
    ORIGINATOR = auto()
    ADDRESS1 = auto()
    ADDRESS2 = auto()
    ADDRESS3 = auto()
    ADDRESS4 = auto()
    ADDRESS5 = auto()
    ADDRESS6 = auto()
    ADDRESS7 = auto()
    ADDRESS8 = auto()
    ADADDRESS1 = auto()
    ADADDRESS2 = auto()
    ADADDRESS3 = auto()
    ADADDRESS4 = auto()
    ADADDRESS5 = auto()
    ADADDRESS6 = auto()
    ADADDRESS7 = auto()
    ADADDRESS8 = auto()
    F3a = auto()
    F3b1 = auto()
    F3b2 = auto()
    F3b3 = auto()
    F3b4 = auto()
    F3c1 = auto()
    F3c2 = auto()
    F3c3 = auto()
    F3c4 = auto()
    F5a = auto()
    F5ab = auto()
    F5b = auto()
    F5bc = auto()
    F5c = auto()
    F7a = auto()
    F7ab = auto()
    F7b = auto()
    F7c = auto()
    F8a = auto()
    F8b = auto()
    F9a = auto()
    F9b = auto()
    F9bc = auto()
    F9c = auto()
    F10a = auto()
    F10ab = auto()
    F10b = auto()
    F13a = auto()
    F13b = auto()
    F14a = auto()
    F14ab = auto()
    F14b = auto()
    F14c = auto()
    F14d = auto()
    F14e = auto()
    F15 = auto()
    F16a = auto()
    F16b = auto()
    F16c = auto()
    F16d = auto()
    F17a = auto()
    F17b = auto()
    F17c = auto()
    F18altn = auto()
    F18code = auto()
    F18com = auto()
    F18dat = auto()
    F18dep = auto()
    F18dest = auto()
    F18dof = auto()
    F18eet = auto()
    F18est = auto()
    F18ifp = auto()
    F18nav = auto()
    F18opr = auto()
    F18per = auto()
    F18ralt = auto()
    F18reg = auto()
    F18rif = auto()
    F18rfp = auto()
    F18rmk = auto()
    F18rvr = auto()
    F18sel = auto()
    F18sts = auto()
    F18src = auto()
    F18typ = auto()
    F18orgn = auto()
    F19a = auto()
    F19c = auto()
    F19d = auto()
    F19e = auto()
    F19j = auto()
    F19n = auto()
    F19p = auto()
    F19r = auto()
    F19s = auto()
    F20 = auto()
    F21 = auto()
    F22 = auto()
    F80a = auto()
    F80b = auto()
    F81a = auto()
    F81b = auto()
    MFS_SIG_POINT = auto()
    RQS_FREE_TEXT = auto()
    ANYTHING = auto()


# Enumeration to identify the message type, ICAO ATS, OLDI or ADEXP; for OLDI
# messages the field content for a given title can vary depending on the
# adjacent unit that a given OLDI message is exchange on.
# Using a combination of the message type and adjacent unit a precise
# field list can be obtained for a given message title.
class MessageTypes(IntEnum):
    ATS = 0
    OLDI = auto()
    ADEXP = auto()  # Reserved for future use
    UNKNOWN = auto()


# Enumeration to identify an adjacent unit for OLDI messages.
# The field content for OLDI messages varies depending on the adjacent unit
# that an OLDI message is exchanged over. This enumeration defines the
# supported OLDI adjacent units. Using a combination of the message title,
# message type and adjacent unit a precise field list can be defined for
# a given OLDI message title, type and adjacent unit.
class AdjacentUnits(IntEnum):
    DEFAULT = 0
    AA = auto()
    AX = auto()
    BB = auto()
    CC = auto()
    L = auto()


# Enumeration used to index error messages used by the system. The error text is defined
# in the ErrorMessages class using a dictionary, the enumerations in this class are used
# for the error message dictionary.
class ErrorId(IntEnum):
    # System fatal case that really should never happen
    SYSTEM_FATAL = 0
    SYSTEM_CONFIG_UNDEFINED = auto()

    # Errors related to overall message processing
    MSG_EMPTY = auto()
    MSG_TOO_SHORT = auto()
    MSG_MISSING_HYPHENS = auto()
    MSG_ADEXP_NOT_SUPPORTED = auto()
    MSG_TOO_MANY_FIELDS = auto()
    MSG_TOO_FEW_FIELDS = auto()

    # Error messages relating to field processing in general
    FLD_MORE_SUBFIELDS_EXPECTED = auto()
    FLD_SLASH_SYNTAX = auto()
    FLD_TOO_MANY_FIELDS = auto()

    # Errors relating to the header field Priority Indicator
    PRIORITY_MISSING = auto()
    PRIORITY_SYNTAX = auto()
    PRIORITY_TOO_MANY_FIELDS = auto()

    # Errors relating to the header field Filing Time
    FILING_TIME_MISSING = auto()
    FILING_TIME_SYNTAX = auto()
    FILING_TIME_TOO_MANY_FIELDS = auto()

    # Errors relating to the header field Originator
    ORIGINATOR_MISSING = auto()
    ORIGINATOR_SYNTAX = auto()
    ORIGINATOR_TOO_MANY_FIELDS = auto()

    # Errors relating to the header field Addressee
    ADDRESSEE_MISSING = auto()
    ADDRESSEE_SYNTAX = auto()
    ADDRESSEE_TOO_MANY_FIELDS = auto()

    # Errors relating to the header field Additional Addressee
    AD_ADDRESSEE_MISSING = auto()
    AD_ADDRESSEE_SYNTAX = auto()
    AD_ADDRESSEE_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 3
    F3_TITLE_MISSING = auto()
    F3_TITLE_SYNTAX = auto()
    F3_TX_SYNTAX = auto()
    F3_RX_SYNTAX = auto()
    F3_SEQ_SYNTAX = auto()
    F3_RX_TX_EXPECTED = auto()
    F3_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 5
    F5_MISSING = auto()
    F5_F5A_SYNTAX = auto()
    F5_F5AB_EXPECTING_SLASH = auto()
    F5_F5B_SYNTAX = auto()
    F5_F5BC_EXPECTING_SLASH = auto()
    F5_F5C_SYNTAX = auto()
    F5_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 7
    F7_MISSING = auto()
    F7_F7A_SYNTAX = auto()
    F7_F7AB_SYNTAX = auto()
    F7_F7B_SYNTAX = auto()
    F7_F7C_SYNTAX = auto()
    F7_TOO_MANY_FIELDS = auto()
    F7_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 8
    F8_MISSING = auto()
    F8_F8A_SYNTAX = auto()
    F8_F8B_SYNTAX = auto()
    F8_F8C_SYNTAX = auto()
    F8_TOO_MANY_FIELDS = auto()
    F8_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 9
    F9_MISSING = auto()
    F9_F9A_SYNTAX = auto()
    F9_F9B_SYNTAX = auto()
    F9_F9BC_SYNTAX = auto()
    F9_F9C_SYNTAX = auto()
    F9_TOO_MANY_FIELDS = auto()
    F9_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 9
    F10_MISSING = auto()
    F10_F10A_SYNTAX = auto()
    F10_F10AB_SYNTAX = auto()
    F10_F10B_SYNTAX = auto()
    F10_TOO_MANY_FIELDS = auto()
    F10_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 13
    F13_MISSING = auto()
    F13_F13A_SYNTAX = auto()
    F13_F13B_SYNTAX = auto()
    F13_TOO_MANY_FIELDS = auto()
    F13_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 14
    F14_MISSING = auto()
    F14_F14A_SYNTAX = auto()
    F14_F14AB_SYNTAX = auto()
    F14_F14B_SYNTAX = auto()
    F14_F14C_SYNTAX = auto()
    F14_F14D_SYNTAX = auto()
    F14_F14E_SYNTAX = auto()
    F14_MORE_FIELDS_EXPECTED = auto()
    F14_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 15
    # This field has its own dedicated parser, hence no other errors are needed
    F15_MISSING = auto()

    # Errors relating to Field 16
    F16_MISSING = auto()
    F16_F16A_SYNTAX = auto()
    F16_F16B_SYNTAX = auto()
    F16_F16C_SYNTAX = auto()
    F16_F16D_SYNTAX = auto()
    F16_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 17
    F17_MISSING = auto()
    F17_F17A_SYNTAX = auto()
    F17_F17B_SYNTAX = auto()
    F17_F17C_SYNTAX = auto()
    F17_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 18
    F18_DOF_MISSING = auto()
    F18_DOF_F18A_SYNTAX = auto()
    F18_DOF_TOO_MANY_FIELDS = auto()

    # Errors relating to the MFS significant point
    MFS_POINT_MISSING = auto()
    MFS_POINT_SYNTAX = auto()
    MFS_POINT_TOO_MANY_FIELDS = auto()

