"""This file contains several enumeration classes used as system-wide constants
that define the following:

MessageTitles -> Enumerations for all supported ATS and OLDI message titles;

FieldIdentifiers -> Enumerations for all ICAO fields as defined in both the OLDI 4.2 standard and ICAO DOC 4444;

SubFieldIdentifiers -> Enumerations for all ICAO and OLDI message subfields; a subfield is derived as
described in the ICAO DOC 4444.

MessageTypes -> Enumeration to define the type of message, OLDI, ICAO ATS, ADEXP or UNKNOWN.
Determined by analysing a message during message parsing;

AdjacentUnits -> A list of adjacent unit identifiers used in combination with a message title and its
type to determine the field content of OLDI messages. Unlike the ICAO ATS messages, the fields contained
in an OLDI message are not fixed but vary depending on the adjacent unit that they are being exchanged on.

ErrorId -> Enumeration used to index error messages."""
from enum import IntEnum, auto


class FlightRules(IntEnum):
    """This class contains enumeration values for each of the 4 possible flight rules."""
    UNKNOWN = 0
    IFR = auto()
    VFR = auto()
    Y = auto()
    Z = auto()

    @staticmethod
    def get_flight_rules(flight_rules):
        # type: (str) -> FlightRules
        for rules in FlightRules:
            if rules.name[0:1] == flight_rules:
                return rules
        return MessageTitles.UNKNOWN


class MessageTitles(IntEnum):
    """This enumeration class defines a unique identifier for each of the supported ICAO and OLDI
    message titles."""
    # ATS Messages
    UNKNOWN = 0
    ACH = auto()
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

    @staticmethod
    def get_message_title(message_title):
        # type: (str) -> MessageTitles
        for title in MessageTitles:
            if title.name == message_title:
                return title
        return MessageTitles.UNKNOWN


class FieldIdentifiers(IntEnum):
    """This enumeration class defines a unique identifier for each of the ICAO fields;
    i.e. ICAO field 13 (ADEP and EOBT)."""
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


class SubFieldIdentifiers(IntEnum):
    """This enumeration class defines a unique identifier for each of the ICAO subfields;
    i.e. ICAO field 13 (ADEP and EOBT) are separated into two subfields, 13 'a' and 'b'.

    Note: These fields must remain in order, do not mix up fields"""
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
    F18awr = auto()
    F18code = auto()
    F18com = auto()
    F18dat = auto()
    F18dep = auto()
    F18dest = auto()
    F18dle = auto()
    F18dof = auto()
    F18eet = auto()
    F18est = auto()
    F18eur = auto()
    F18ifp = auto()
    F18nav = auto()
    F18opr = auto()
    F18orgn = auto()
    F18pbn = auto()
    F18per = auto()
    F18ralt = auto()
    F18reg = auto()
    F18rif = auto()
    F18rfp = auto()
    F18rmk = auto()
    F18rvr = auto()
    F18sel = auto()
    F18stayinfo1 = auto()
    F18stayinfo2 = auto()
    F18stayinfo3 = auto()
    F18stayinfo4 = auto()
    F18stayinfo5 = auto()
    F18stayinfo6 = auto()
    F18stayinfo7 = auto()
    F18stayinfo8 = auto()
    F18stayinfo9 = auto()
    F18sts = auto()
    F18src = auto()
    F18sur = auto()
    F18talt = auto()
    F18typ = auto()
    F19a = auto()
    F19c = auto()
    F19d = auto()
    F19e = auto()
    F19j = auto()
    F19n = auto()
    F19p = auto()
    F19r = auto()
    F19s = auto()
    F20a = auto()
    F20b = auto()
    F20c = auto()
    F20d = auto()
    F20e = auto()
    F20f = auto()
    F20g = auto()
    F20h = auto()
    F21a = auto()
    F21b = auto()
    F21c = auto()
    F21d = auto()
    F21e = auto()
    F21f = auto()
    F22_f3 = auto()
    F22_f5 = auto()
    F22_f7 = auto()
    F22_f8 = auto()
    F22_f9 = auto()
    F22_f10 = auto()
    F22_f13 = auto()
    F22_f14 = auto()
    F22_f15 = auto()
    F22_f16 = auto()
    F22_f17 = auto()
    F22_f18 = auto()
    F22_f19 = auto()
    F22_f20 = auto()
    F22_f21 = auto()
    F22_f22 = auto()
    F22_f80 = auto()
    F22_f81 = auto()
    F80a = auto()
    F81a = auto()
    F81ab = auto()
    F81b = auto()
    F81bc = auto()
    F81c = auto()
    MFS_SIG_POINT = auto()
    RQS_FREE_TEXT = auto()
    ANYTHING = auto()


class MessageTypes(IntEnum):
    """Enumeration to identify the message type, ICAO ATS, OLDI, ADEXP or UNKNOWN; for OLDI
    messages the field content for a given title can vary depending on the adjacent unit that
    a given OLDI message is exchange on. Using a combination of the message type and
    adjacent unit a precise field list can be obtained for a given message title."""
    ATS = 0
    OLDI = auto()
    ADEXP = auto()  # Reserved for future use
    UNKNOWN = auto()


class AdjacentUnits(IntEnum):
    """Enumeration to identify an adjacent unit for OLDI messages. The field content for OLDI
    messages varies depending on the adjacent unit that an OLDI message is exchanged over.
    supported OLDI adjacent units. Using a combination of the message title, message type and
    adjacent unit a precise field list can be defined for a given OLDI message title, type
    and adjacent unit."""
    DEFAULT = 0
    AA = auto()
    AX = auto()
    BB = auto()
    CC = auto()
    L = auto()

    @staticmethod
    def get_adjacent_unit(adjacent_unit_name):
        # type: (str) -> AdjacentUnits
        for unit in AdjacentUnits:
            if unit.name == adjacent_unit_name:
                return unit
        return AdjacentUnits.DEFAULT


class ErrorId(IntEnum):
    """Enumeration used to index error messages used by the system. The error text is defined
    in the ErrorMessages class using a dictionary, the enumerations in this class are used as keys
    for the error message dictionary."""
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
    F18_NO_F18_KEYWORDS_FOUND = auto()
    F18_ZERO_OR_KEYWORDS = auto()
    F18_UNRECOGNISED_DATA = auto()
    F18_DATA_MISSING = auto()
    F18_GARBAGE = auto()
    F18_UNRECOGNISED_KEYWORD = auto()
    F18_ALTN_SYNTAX = auto()
    F18_AWR_SYNTAX = auto()
    F18_AWR_TOO_MANY = auto()
    F18_CODE_SYNTAX = auto()
    F18_CODE_TOO_MANY = auto()
    F18_COM_SYNTAX = auto()
    F18_DAT_SYNTAX = auto()
    F18_DEP_SYNTAX = auto()
    F18_DEST_SYNTAX = auto()
    F18_DLE_TOO_SHORT = auto()
    F18_DLE_PNT_SYNTAX = auto()
    F18_DLE_TIME_SYNTAX = auto()
    F18_DLE_TOO_MANY = auto()
    F18_EET_PNT_SYNTAX = auto()
    F18_EET_TIME_SYNTAX = auto()
    F18_EST_SYNTAX = auto()
    F18_IFP_SYNTAX = auto()
    F18_NAV_SYNTAX = auto()
    F18_OPR_SYNTAX = auto()
    F18_ORGN_SYNTAX = auto()
    F18_ORGN_TOO_MANY = auto()
    F18_ORGN_TOO_SHORT = auto()
    F18_PBN_TOO_LONG = auto()
    F18_PBN_SYNTAX = auto()
    F18_PBN_TOO_MANY = auto()
    F18_PBN_TOO_SHORT = auto()
    F18_PER_SYNTAX = auto()
    F18_PER_TOO_MANY = auto()
    F18_RALT_SYNTAX = auto()
    F18_REG_SYNTAX = auto()
    F18_RIF_SYNTAX = auto()
    F18_RFP_SYNTAX = auto()
    F18_RFP_TOO_MANY = auto()
    F18_RMK_SYNTAX = auto()
    F18_RVR_SYNTAX = auto()
    F18_RVR_TOO_MANY = auto()
    F18_SEL_SYNTAX = auto()
    F18_SEL_TOO_MANY = auto()
    F18_STAYINFO_SYNTAX = auto()
    F18_STS_SYNTAX = auto()
    F18_STS_TOO_MANY = auto()
    F18_SRC_SYNTAX = auto()
    F18_SRC_TOO_MANY = auto()
    F18_SUR_SYNTAX = auto()
    F18_TALT_SYNTAX = auto()
    F18_TYP_SYNTAX = auto()

    # Errors relating to Field 19
    F19_NO_F19_KEYWORDS_FOUND = auto()
    F19_DATA_MISSING = auto()
    F19_UNRECOGNISED_DATA = auto()
    F19_UNRECOGNISED_KEYWORD = auto()
    F19_ZERO_OR_KEYWORDS = auto()
    F19_A_SYNTAX = auto()
    F19_C_SYNTAX = auto()
    F19_Da_SYNTAX = auto()
    F19_Db_SYNTAX = auto()
    F19_Dc_SYNTAX = auto()
    F19_Dd_SYNTAX = auto()
    F19_D_TOO_MANY = auto()
    F19_D_TOO_FEW = auto()
    F19_E_SYNTAX = auto()
    F19_E_TOO_MANY = auto()
    F19_J_SYNTAX = auto()
    F19_J_TOO_MANY = auto()
    F19_N_SYNTAX = auto()
    F19_P_SYNTAX = auto()
    F19_P_TOO_MANY = auto()
    F19_R_SYNTAX = auto()
    F19_R_TOO_MANY = auto()
    F19_S_SYNTAX = auto()
    F19_S_TOO_MANY = auto()

    # Errors relating to Field 20
    F20_MISSING = auto()
    F20_F20A_SYNTAX = auto()
    F20_F20B_SYNTAX = auto()
    F20_F20C_SYNTAX = auto()
    F20_F20D_SYNTAX = auto()
    F20_F20E_SYNTAX = auto()
    F20_F20F_SYNTAX = auto()
    F20_F20G_SYNTAX = auto()
    F20_F20H_SYNTAX = auto()
    F20_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 20
    F21_MISSING = auto()
    F21_F21A_SYNTAX = auto()
    F21_F21B_SYNTAX = auto()
    F21_F21C_SYNTAX = auto()
    F21_F21D_SYNTAX = auto()
    F21_F21E_SYNTAX = auto()
    F21_F21F_SYNTAX = auto()
    F21_TOO_MANY_FIELDS = auto()

    # Errors relating to Field 22
    F22_NO_F22_KEYWORDS_FOUND = auto()
    F22_DATA_MISSING = auto()
    F22_UNRECOGNISED_DATA = auto()
    F22_UNRECOGNISED_KEYWORD = auto()
    F22_ZERO_OR_KEYWORDS = auto()
    F22_FIELD_DUPLICATED = auto()

    # Errors relating to Field 80
    F80_MISSING = auto()
    F80_F80A_SYNTAX = auto()
    F80_TOO_MANY_FIELDS = auto()
    F80_MORE_SUBFIELDS_EXPECTED = auto()

    # Errors relating to Field 81
    F81_MISSING = auto()
    F81_F81A_SYNTAX = auto()
    F81_F81AB_SYNTAX = auto()
    F81_F81B_SYNTAX = auto()
    F81_F81BC_SYNTAX = auto()
    F81_F81C_SYNTAX = auto()
    F81_TOO_MANY_FIELDS = auto()
    F81_MORE_FIELDS_EXPECTED = auto()

    # Errors relating to the MFS significant point
    MFS_POINT_MISSING = auto()
    MFS_POINT_SYNTAX = auto()
    MFS_POINT_TOO_MANY_FIELDS = auto()

    # Errors related to consistency checking
    CONSISTENCY_F8_F8A_UNKNOWN = auto()
    CONSISTENCY_F8_DERIVED_UNKNOWN = auto()
    CONSISTENCY_F8_F8_DERIVED_DIFFERENT = auto()
    CONSISTENCY_F10_R = auto()
    CONSISTENCY_F10_Z = auto()
    CONSISTENCY_F13A_DEP = auto()
    CONSISTENCY_F16A_DEST = auto()
    CONSISTENCY_F9B_TYP = auto()
    CONSISTENCY_PBN_D = auto()
    CONSISTENCY_PBN_G = auto()
    CONSISTENCY_PBN_I = auto()
    CONSISTENCY_PBN_OS = auto()
    CONSISTENCY_PBN_R = auto()
