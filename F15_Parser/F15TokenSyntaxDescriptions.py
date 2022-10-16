# This file contains various constants used to define the following:
# Token base types
# Token Sub-Types
# Rule change types
# ...
from enum import auto, IntEnum
import re

import Tokenizer.Tokens as Tokens


# Token base type definitions
# <b>Token type identifiers for field 15 tokens</b>
# <p>
# F15_NULL - Token is a null token
# <p>
# F15_SLASH - Token is a forward slash
# <p>
# F15_BREAK_START - Token is a start for a BREAK section in one
# of the following forms:
# <ul>
# <li>VFR</li>
# <li>OAT</li>
# <li>IFPSTOP</li>
# </ul>
# <p>
# F15_SPEED_VFR - Token is a start for a BREAK section with VFR and
# speed given as Mach, Knots or Kilometers in one of the following forms:
# <ul>
# <li>M[0-9],{3}VFR</li>
# <li>[NK],[0-9],{4}VFR</li>
# </ul>
# <p>
# F15_BREAK_END - Token is the end for a BREAK section in one of the following forms:
# <ul>
# <li>IFR</li>
# <li>GAT</li>
# <li>IFPSTART</li>
# </ul>
# <p>
# F15_DCT - Token is a DCT section in the following form:
# <ul>
# <li>DCT</li>
# </ul>
# <p>
# F15_STAY - Token is a STAY section in the following form:
# <ul>
# <li>STAY[0-9],</li>
# </ul>
# <p>
# F15_TRUNCATE - Token is a the route truncation indicator in the form:
# <ul>
# <li>T</li>
# </ul>
# <p>
# F15_C - Token is a the start of a cruise climb token in the form:
# <ul>
# <li>C</li>
# </ul>
# <p>
# F15_POINT - Token is a point in one of the following forms:
# <ul>
# <li>[A-Z],{1,3} - Point with 1 to 3 characters</li>
# <li>[A-Z],{4} - Aerodrome type of point</li>
# <li>[A-Z],{5} - Point with 5 characters</li>
# <li>[A-Z],{1,5}[0-9],{6} - Point followed by Bearing Distance</li>
# <li>[0-9],{2}[NS],[0-9],{3}[EW], - Lat/Long Degrees in degrees</li>
# <li>[0-9],{4}[NS],[0-9],{5}[EW], - Lat/Long in Degrees and Minutes</li>
# <li>[0-9],{2}[NS],[0-9],{3}[EW],[0-9],{6} - Lat/Long in Degrees
# followed Bearing Distance</li>
# <li>[0-9],{4}[NS],[0-9],{5}[EW],[0-9],{6} - Lat/Long in degrees and Minutes
# followed by Bearing Distance</li>
# </ul>
# <p>
# F15_ROUTE - Token is a route in one of the following forms:
# <ul>
# <li>NAT[A-Z], - NAT Route</li>
# <li>NAT[A-Z],[0-9], - NAT Route</li>
# <li>PTS[0-9], - PTS Route</li>
# <li>PTS[A-Z], - PTS Route</li>
# <li>[A-Z],{1,2}[0-9], - ATS Route</li>
# <li>[A-Z],[0-9],{1,3}[A-Z], - ATS Route</li>
# <li>[A-Z],[0-9],{2,3} - ATS Route</li>
# <li>[A-Z],{3}[0-9],{3} - ATS Route, (Turkish)</li>
# <li>[A-Z],{3}[0-9],{1,2} - ATS Route, (Older syntax)</li>
# <li>[A-Z],{2}[0-9],[A-Z], - ATS Route</li>
# <li>[A-Z],{2}[0-9],{2,3} - ATS Route</li>
# <li>[A-Z],{4}[0-9],{1,2} - ATS Route, (Russian air corridor)</li>
# <li>[A-Z],{2}[0-9],{2,3}[A-Z], - ATS Route</li>
# <li>[A-Z],[0-9],{3}[A-Z], - ATS Route, (Turkish)</li>
# </ul>
# <p>
# F15_SID_STAR - Token is a STAR or SID, the subfield types further discriminate to the actual
# type, these are given in one of the following forms:
# <ul>
# <li>SID - Literal SID</li>
# <li>STAR - Literal STAR</li>
# <li>[A-Z],{3}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],</li>
# <li>[A-Z],{4,6}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],{2}[A-Z],</li>
# </ul>
# <p>
# F15_SPEED_ALTITUDE - Token is a speed/ALTITUDE in one of the following forms:
# <ul>
# <li>M[0-9],{3}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}</li>
# <li>[KN],[0-9],{4}[AF],[0-9],{3}</li>
# <li>[KN],[0-9],{4}[MS],[0-9],{4}</li>
# </ul>
# <p>
# F15_SPEED_ALTITUDE_ALTITUDE - Token is a speed/ALTITUDE/ALTITUDE token used in cruise climb elements in one
# of the following forms:
# <ul>
# <li>M[0-9],{3}[AF],[0-9],{3}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[AF],[0-9],{3}[SM],[0-9],{4}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}[SM],[0-9],{4}</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}[AF],[0-9],{3}</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}[AF],[0-9],{3}</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}[SM],[0-9],{4}</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}[SM],[0-9],{4}</li>
# <li>M[0-9],{3}[AF],[0-9],{3}PLUS</li>
# <li>M[0-9],{3}[SM],[0-9],{4}PLUS</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}PLUS</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}PLUS</li>
# </ul>
# <p>
# F15_UNKNOWN - Token is not one of the recognised tokens for this field
# <p>
# F15_TOO_LONG - Token is longer than the maximum allowed for field 15 token, 30 bytes
# <p>
# F15_STAY_TIME - Token is a STAY time value in the following form:
# <ul>
# <li>[0-2],[0-3],[0-5],[0-9],</li>
# </ul>
# <p>
# F15_SID - Used when processing SID tokens to ultimately indicate if a token is a SID
# or STAR. Syntactically these items may be identical. This constant is not
# use directly when assigning token types in the token analysis stage.
# <p>
# F15_STAR - Used when processing STAR tokens to ultimately indicate if a token is a SID
# or STAR. Syntactically these items may be identical. This constant is not
# use directly when assigning token types in the token analysis stage.
# /
# noinspection PyArgumentList
class TokenBaseType(IntEnum):
    F15_UNKNOWN = 0
    F15_SLASH = auto()
    F15_BREAK_START = auto()
    F15_SPEED_VFR = auto()
    F15_BREAK_END = auto()
    F15_DCT = auto()
    F15_STAY = auto()
    F15_TRUNCATE = auto()
    F15_C = auto()
    F15_POINT = auto()
    F15_ROUTE = auto()
    F15_SID_STAR = auto()
    F15_SPEED_ALTITUDE = auto()
    F15_SPEED_ALTITUDE_ALTITUDE = auto()
    F15_SPEED_ALTITUDE_PLUS = auto()
    F15_TOO_LONG = auto()
    F15_STAY_TIME = auto()
    F15_SID = auto()
    F15_STAR = auto()


# Token Sub-TYpe Definitions
# <b>Token Sub-type identifiers for field 15 tokens</b>.
# <p>
# F15_SB_IFR - Token is the end for a BREAK section in the following form:
# <ul>
# <li>IFR</li>
# </ul> 
# <p>
# F15_SB_DCT - Token is a DCT section in the following form:
# <ul>
# <li>DCT</li>
# </ul>
# <p>
# F15_SB_VFR - Token is a start for a BREAK section in the following form:
# <ul>
# <li>VFR</li>
# </ul>
# <p>
# F15_SB_OAT - Token is a start for a BREAK section in the following form:
# <ul>
# <li>OAT</li>
# </ul> 
# <p>
# F15_SB_GAT - Token is the end for a BREAK section in the following form:
# <ul>
# <li>GAT</li>
# </ul> 
# <p>
# F15_SB_IFPSTART - Token is the end for a BREAK section in the following form:
# <ul>
# <li>IFPSTART</li>
# </ul>
# <p>
# F15_SB_IFPSTOP - Token is a start for a BREAK section in the following form:
# <ul>
# <li>IFPSTOP</li>
# </ul>
# <p>
# F15_SB_STAY - Token is a STAY section in the following form:
# <ul>
# <li>STAY[0-9],</li>
# </ul>
# <p>
# F15_SB_TRUNCATE - Token is a the route truncation indicator in the form:
# <ul>
# <li>T</li>
# </ul>
# <p>
# F15_SB_C - Token is a the start of a cruise climb token in the form:
# <ul>
# <li>C</li>
# </ul> 
# <p>
# F15_SB_SID_LITERAL - Token is a SID literal in the following form:
# <ul>
# <li>SID - Literal SID</li>
# </ul>
# <p>
# F15_SB_STAR_LITERAL - Token is a STAR literal in the following form:
# <ul>
# <li>STAR - Literal STAR</li>
# </ul> 
# <p>
# F15_SB_3_VFR - Token is a start for a BREAK section with VFR and speed given as Mach in
# the following form:
# <ul>
# <li>M[0-9],{3}VFR</li>
# </ul> 
# <p>
# F15_SB_4_VFR - Token is a start for a BREAK section with VFR and speed given as Knots or
# Kilometers in the following form:
# <ul>
# <li>[NK],[0-9],{4}VFR</li>
# </ul> 
# <p>
# F15_SB_PRP - Token is a point in one of the following forms:
# <ul>
# <li>[A-Z],{1,3}</li>
# <li>[A-Z],{5}</li>
# </ul> 
# <p>
# F15_SB_PRP_AERO - Token is a point in one the following form:
# <ul>
# <li>[A-Z],{4} - Aerodrome type of point</li>
# </ul> 
# <p>
# F15_SB_PRP_BD - Token is a point in the following form:
# <ul>
# <li>[A-Z],{1,5}[0-9],{6} - Point followed by Bearing Distance</li>
# </ul>
# <p>
# F15_SB_LL_DEG - Token is a point in the following form:
# <ul>
# <li>[0-9],{2}[NS],[0-9],{3}[EW], - Lat/Long Degrees in degrees</li>
# </ul>
# <p>
# F15_SB_LL_MIN - Token is a point in the following form:
# <ul>
# <li>[0-9],{4}[NS],[0-9],{5}[EW], - Lat/Long in Degrees and Minutes</li>
# </ul>
# <p>
# F15_SB_LLBD_DEG - Token is a point in the following form:
# <ul>
# <li>[0-9],{2}[NS],[0-9],{3}[EW],[0-9],{6} - Lat/Long in Degrees followed
# Bearing Distance</li>
# </ul> 
# <p>
# F15_SB_LLBD_MIN - Token is a point in the following form:
# <ul>
# <li>[0-9],{4}[NS],[0-9],{5}[EW],[0-9],{6} - Lat/Long in degrees and Minutes
# followed by Bearing Distance</li>
# </ul> 
# <p>
# F15_SB_ATS - Token is an ATS route in one of the following forms:
# <ul>
# <li>[A-Z],{1,2}[0-9], - ATS Route</li>
# <li>[A-Z],[0-9],{1,3}[A-Z], - ATS Route</li>
# <li>[A-Z],[0-9],{2,3} - ATS Route</li>
# <li>[A-Z],{2}[0-9],[A-Z], - ATS Route</li>
# <li>[A-Z],{2}[0-9],{2,3} - ATS Route</li>
# </ul> 
# <p>
# F15_SB_ATS_OLD - Token is an ATS route with older syntax the following form:
# <ul>
# <li>[A-Z],{3}[0-9],{1,2} - ATS Route, (Older syntax)</li>
# </ul> 
# <p>
# F15_SB_ATS_TURK - Token is an ATS route with syntax used exclusively by Turkey in one of
# the following forms:
# <ul>
# <li>[A-Z],{3}[0-9],{3} - ATS Route, (Turkish)</li>
# <li>[A-Z],[0-9],{3}[A-Z], - ATS Route, (Turkish)</li>
# </ul> 
# <p>
# F15_SB_ATS_RUS - Token is a route with syntax as used by the Russians to define their air
# corridors in the following form:
# <ul>
# <li>[A-Z],{4}[0-9],{1,2} - ATS Route, (Russian air corridor)</li>
# </ul> 
# <p>
# F15_SB_STAR - Token is a STAR in one of the following forms:
# <ul>
# <li>[A-Z],{3}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],</li>
# <li>[A-Z],{4,6}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],{2}[A-Z],</li>
# </ul> 
# <p>
# This syntax is identical to a SID, the exact type is set during processing
# by placement of the token in field 15.
# <p>
# F15_SB_SID - Token is an SID in one of the following forms:
# <ul>
# <li>[A-Z],{3}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],</li>
# <li>[A-Z],{4,6}[0-9],[A-Z],</li>
# <li>[A-Z],{5}[0-9],{2}[A-Z],</li>
# </ul> 
# <p>
# This syntax is identical to a STAR, the exact type is set during processing
# by placement of the token in field 15.
# <p>
# F15_SB_3_3 - Token is a speed/ALTITUDE or speed/ALTITUDE/ALTITUDE token in one of the
# following forms:
# <ul>
# <li>M[0-9],{3}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[AF],[0-9],{3}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[AF],[0-9],{3}[SM],[0-9],{4}</li>
# <li>M[0-9],{3}[AF],[0-9],{3}PLUS</li>
# </ul>
# <p>
# F15_SB_3_4 - Token is a speed/ALTITUDE or speed/ALTITUDE/ALTITUDE token in one of the
# following forms:
# <ul>
# <li>M[0-9],{3}[SM],[0-9],{4}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}[AF],[0-9],{3}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}[SM],[0-9],{4}</li>
# <li>M[0-9],{3}[SM],[0-9],{4}PLUS</li>
# </ul> 
# <p>
# F15_SB_4_3 - Token is a speed/ALTITUDE or speed/ALTITUDE/ALTITUDE token in one of the
# following forms:
# <ul>
# <li>[KN],[0-9],{4}[AF],[0-9],{3}</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}[AF],[0-9],{3}</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}[SM],[0-9],{4}</li>
# <li>[NK],[0-9],{4}[AF],[0-9],{3}PLUS</li>
# </ul>
# <p>
# F15_SB_4_4 - Token is a speed/ALTITUDE or speed/ALTITUDE/ALTITUDE token in one of the
# following forms:
# <ul>
# <li>[KN],[0-9],{4}[MS],[0-9],{4}</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}[AF],[0-9],{3}</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}[SM],[0-9],{4}</li>
# <li>[NK],[0-9],{4}[SM],[0-9],{4}PLUS</li>
# </ul>
# <p>
# F15_SB_STAY_TIME - Token is a STAY time value in the following form:
# <ul>
# <li>[0-2],[0-3],[0-5],[0-9],</li>
# </ul> 
# <p>
# F15_SB_NAT - Token is a NAT Track route in one of the following forms:
# <ul>
# <li>NAT[A-Z], - NAT Route</li>
# <li>NAT[A-Z],[0-9], - NAT Route</li>
# </ul>
# <p>
# F15_SB_PTS - Token is a PTS route in one of the following forms:
# <ul>
# <li>PTS[0-9], - PTS Route</li>
# <li>PTS[A-Z], - PTS Route</li>
# </ul>
# <p>
#  F15_SB_SLASH - Token is a forward slash
# /
# noinspection PyArgumentList
class TokenSubType(IntEnum):
    F15_SB_UNKNOWN = 0
    F15_SB_IFR = auto()
    F15_SB_DCT = auto()
    F15_SB_VFR = auto()
    F15_SB_OAT = auto()
    F15_SB_GAT = auto()
    F15_SB_IFPSTART = auto()
    F15_SB_IFPSTOP = auto()
    F15_SB_STAY = auto()
    F15_SB_TRUNCATE = auto()
    F15_SB_C = auto()
    F15_SB_SID_LITERAL = auto()
    F15_SB_STAR_LITERAL = auto()
    F15_SB_PRP = auto()
    F15_SB_PRP_AERO = auto()
    F15_SB_PRP_BD = auto()
    F15_SB_LL_DEG = auto()
    F15_SB_LL_MIN = auto()
    F15_SB_LLBD_DEG = auto()
    F15_SB_LLBD_MIN = auto()
    F15_SB_ATS = auto()
    F15_SB_ATS_OLD = auto()
    F15_SB_ATS_TURK = auto()
    F15_SB_ATS_RUS = auto()
    F15_SB_STAR = auto()
    F15_SB_SID = auto()
    F15_SB_SPEED_ALTITUDE_KF = auto()
    F15_SB_SPEED_ALTITUDE_KS = auto()
    F15_SB_SPEED_ALTITUDE_KA = auto()
    F15_SB_SPEED_ALTITUDE_KM = auto()
    F15_SB_SPEED_ALTITUDE_KV = auto()
    F15_SB_SPEED_ALTITUDE_NF = auto()
    F15_SB_SPEED_ALTITUDE_NS = auto()
    F15_SB_SPEED_ALTITUDE_NA = auto()
    F15_SB_SPEED_ALTITUDE_NM = auto()
    F15_SB_SPEED_ALTITUDE_NV = auto()
    F15_SB_SPEED_ALTITUDE_MF = auto()
    F15_SB_SPEED_ALTITUDE_MS = auto()
    F15_SB_SPEED_ALTITUDE_MA = auto()
    F15_SB_SPEED_ALTITUDE_MM = auto()
    F15_SB_SPEED_ALTITUDE_MV = auto()
    F15_SB_SPEED_ALTITUDE_KFF = auto()
    F15_SB_SPEED_ALTITUDE_KFS = auto()
    F15_SB_SPEED_ALTITUDE_KFA = auto()
    F15_SB_SPEED_ALTITUDE_KFM = auto()
    F15_SB_SPEED_ALTITUDE_KSF = auto()
    F15_SB_SPEED_ALTITUDE_KSS = auto()
    F15_SB_SPEED_ALTITUDE_KSA = auto()
    F15_SB_SPEED_ALTITUDE_KSM = auto()
    F15_SB_SPEED_ALTITUDE_KAF = auto()
    F15_SB_SPEED_ALTITUDE_KAS = auto()
    F15_SB_SPEED_ALTITUDE_KAA = auto()
    F15_SB_SPEED_ALTITUDE_KAM = auto()
    F15_SB_SPEED_ALTITUDE_KMF = auto()
    F15_SB_SPEED_ALTITUDE_KMS = auto()
    F15_SB_SPEED_ALTITUDE_KMA = auto()
    F15_SB_SPEED_ALTITUDE_KMM = auto()
    F15_SB_SPEED_ALTITUDE_NFF = auto()
    F15_SB_SPEED_ALTITUDE_NFS = auto()
    F15_SB_SPEED_ALTITUDE_NFA = auto()
    F15_SB_SPEED_ALTITUDE_NFM = auto()
    F15_SB_SPEED_ALTITUDE_NSF = auto()
    F15_SB_SPEED_ALTITUDE_NSS = auto()
    F15_SB_SPEED_ALTITUDE_NSA = auto()
    F15_SB_SPEED_ALTITUDE_NSM = auto()
    F15_SB_SPEED_ALTITUDE_NAF = auto()
    F15_SB_SPEED_ALTITUDE_NAS = auto()
    F15_SB_SPEED_ALTITUDE_NAA = auto()
    F15_SB_SPEED_ALTITUDE_NAM = auto()
    F15_SB_SPEED_ALTITUDE_NMF = auto()
    F15_SB_SPEED_ALTITUDE_NMS = auto()
    F15_SB_SPEED_ALTITUDE_NMA = auto()
    F15_SB_SPEED_ALTITUDE_NMM = auto()
    F15_SB_SPEED_ALTITUDE_MFF = auto()
    F15_SB_SPEED_ALTITUDE_MFS = auto()
    F15_SB_SPEED_ALTITUDE_MFA = auto()
    F15_SB_SPEED_ALTITUDE_MFM = auto()
    F15_SB_SPEED_ALTITUDE_MSF = auto()
    F15_SB_SPEED_ALTITUDE_MSS = auto()
    F15_SB_SPEED_ALTITUDE_MSA = auto()
    F15_SB_SPEED_ALTITUDE_MSM = auto()
    F15_SB_SPEED_ALTITUDE_MAF = auto()
    F15_SB_SPEED_ALTITUDE_MAS = auto()
    F15_SB_SPEED_ALTITUDE_MAA = auto()
    F15_SB_SPEED_ALTITUDE_MAM = auto()
    F15_SB_SPEED_ALTITUDE_MMF = auto()
    F15_SB_SPEED_ALTITUDE_MMS = auto()
    F15_SB_SPEED_ALTITUDE_MMA = auto()
    F15_SB_SPEED_ALTITUDE_MMM = auto()
    F15_SB_SPEED_ALTITUDE_KF_P = auto()
    F15_SB_SPEED_ALTITUDE_KS_P = auto()
    F15_SB_SPEED_ALTITUDE_KA_P = auto()
    F15_SB_SPEED_ALTITUDE_KM_P = auto()
    F15_SB_SPEED_ALTITUDE_NF_P = auto()
    F15_SB_SPEED_ALTITUDE_NS_P = auto()
    F15_SB_SPEED_ALTITUDE_NA_P = auto()
    F15_SB_SPEED_ALTITUDE_NM_P = auto()
    F15_SB_SPEED_ALTITUDE_MF_P = auto()
    F15_SB_SPEED_ALTITUDE_MS_P = auto()
    F15_SB_SPEED_ALTITUDE_MA_P = auto()
    F15_SB_SPEED_ALTITUDE_MM_P = auto()
    F15_SB_STAY_TIME = auto()
    F15_SB_NAT = auto()
    F15_SB_PTS = auto()
    F15_SB_SLASH = auto()


# Token descriptions for field 15 tokens in a multidimensional list.
# Each entry is a 3 field list that contains the regular expression
# for a token along with its bas and subtype identifiers.
class F15TokenSyntaxDefinition:

    # The following constants are used to index one of the three items in the
    # multidimensional list.
    # Index to the regular expression describing a token
    TOKEN_REGEXP_IDX = 0

    # Index to the base token type ID
    TOKEN_BASE_IDENTIFIER_IDX = 1

    # Index to the subtype token type ID
    TOKEN_SUBTYPE_IDENTIFIER_IDX = 2

    # Maximum length of a single token
    MAX_TOKEN_LENGTH = 25

    F15_SB_CONFIGURATION = list([
        # Regular expression, base type ID, subtype ID...
        # FIXED Text types
        ["/", TokenBaseType.F15_SLASH, TokenSubType.F15_SB_SLASH],
        # VFR and no Speed
        ["VFR", TokenBaseType.F15_BREAK_START, TokenSubType.F15_SB_VFR],
        # VFR with MACH Speed
        ["M[0-9]{3}VFR", TokenBaseType.F15_SPEED_VFR, TokenSubType.F15_SB_SPEED_ALTITUDE_MV],
        # VFR with Knots Speed
        ["N[0-9]{4}VFR", TokenBaseType.F15_SPEED_VFR, TokenSubType.F15_SB_SPEED_ALTITUDE_NV],
        # VFR with Kilometer Speed
        ["K[0-9]{4}VFR", TokenBaseType.F15_SPEED_VFR, TokenSubType.F15_SB_SPEED_ALTITUDE_KV],
        # IFR Element
        ["IFR", TokenBaseType.F15_BREAK_END, TokenSubType.F15_SB_IFR],
        # DCT Element
        ["DCT", TokenBaseType.F15_DCT, TokenSubType.F15_SB_DCT],
        # OAT Element
        ["OAT", TokenBaseType.F15_BREAK_START, TokenSubType.F15_SB_OAT],
        # GAT Element
        ["GAT", TokenBaseType.F15_BREAK_END, TokenSubType.F15_SB_GAT],
        # STOP IFPS Element
        ["IFPSTOP", TokenBaseType.F15_BREAK_START, TokenSubType.F15_SB_IFPSTOP],
        # START IFPS Element
        ["IFPSTART", TokenBaseType.F15_BREAK_END, TokenSubType.F15_SB_IFPSTART],
        # STAY Element
        ["STAY[0-9]", TokenBaseType.F15_STAY, TokenSubType.F15_SB_STAY],
        # Time field for stay element
        ["([01][0-9][0-5][0-9]|2[0-3][0-5][0-9])", TokenBaseType.F15_STAY_TIME, TokenSubType.F15_SB_STAY_TIME],
        # Truncate Element
        ["T", TokenBaseType.F15_TRUNCATE, TokenSubType.F15_SB_TRUNCATE],
        # Climb Element Indicator
        ["C", TokenBaseType.F15_C, TokenSubType.F15_SB_C],
        # Literal SID
        ["SID", TokenBaseType.F15_SID, TokenSubType.F15_SB_SID_LITERAL],
        # Literal STAR
        ["STAR", TokenBaseType.F15_STAR, TokenSubType.F15_SB_STAR_LITERAL],
        # NAT Routes
        ["NAT[A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_NAT],
        ["NAT[A-Z][0-9]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_NAT],
        # PTS Routes
        ["PTS[0-9]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_PTS],
        ["PTS[A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_PTS],

        # POINT types
        # First is the basic point
        ["[A-Z]{1,3}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP],
        # Aerodrome type of point
        ["[A-Z]{4}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP_AERO],
        # Point with 5 characters
        ["[A-Z]{5}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP],
        # Point followed by Bearing Distance
        ["[A-Z]{1,5}[0-9]{6}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP_BD],
        # Lat/Long Degrees in degrees
        ["[0-9]{2}[NS][0-9]{3}[EW]", TokenBaseType.F15_POINT, TokenSubType.F15_SB_LL_DEG],
        # Lat/Long in Degrees and Minutes
        ["[0-9]{4}[NS][0-9]{5}[EW]", TokenBaseType.F15_POINT, TokenSubType.F15_SB_LL_MIN],
        # Lat/Long in Degrees followed Bearing Distance
        ["[0-9]{2}[NS][0-9]{3}[EW][0-9]{6}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_LLBD_DEG],
        # Lat/Long in degrees and Minutes followed by Bearing Distance
        ["[0-9]{4}[NS][0-9]{5}[EW][0-9]{6}", TokenBaseType.F15_POINT, TokenSubType.F15_SB_LLBD_MIN],

        # ROUTE type
        # x9, xx9
        ["[A-Z]{1,2}[0-9]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # x9x, x99x, x999x
        ["[A-Z][0-9]{1,3}[A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # x99, x999
        ["[A-Z][0-9]{2,3}", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # xxx999 turkish type
        ["[A-Z]{3}[0-9]{3}", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS_TURK],
        # xxx9, xxx99 old style
        ["[A-Z]{3}[0-9]{1,2}", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS_OLD],
        # xx9x
        ["[A-Z]{2}[0-9][A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # xx99, xx999
        ["[A-Z]{2}[0-9]{2,3}", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # xxxx9, xxxx99 Russian air corridor
        ["[A-Z]{4}[0-9]{1,2}", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS_RUS],
        # xx99x, xx999x
        ["[A-Z]{2}[0-9]{2,3}[A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS],
        # x999xx
        ["[A-Z][0-9]{3}[A-Z]", TokenBaseType.F15_ROUTE, TokenSubType.F15_SB_ATS_TURK],

        # SID/STAR type - The SID type is set during processing
        # xxx9x xxx99x
        ["[A-Z]{3}[0-9]{1,2}[A-Z]", TokenBaseType.F15_SID_STAR, TokenSubType.F15_SB_STAR],
        # xxxxx9 xxxxx99
        ["[A-Z]{5}[0-9]{1,2}", TokenBaseType.F15_SID_STAR, TokenSubType.F15_SB_STAR],
        # xxxx9x, xxxxx9x, xxxxxx9x
        ["[A-Z]{4,6}[0-9][A-Z]", TokenBaseType.F15_SID_STAR, TokenSubType.F15_SB_STAR],
        # xxxxx99x
        ["[A-Z]{5}[0-9]{2}[A-Z]", TokenBaseType.F15_SID_STAR, TokenSubType.F15_SB_STAR],

        # Speed ALTITUDE types
        ["M[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_MF],
        ["M[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_MS],
        ["M[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_MA],
        ["M[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_MM],
        ["K[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_KF],
        ["K[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_KS],
        ["K[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_KA],
        ["K[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_KM],
        ["N[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_NF],
        ["N[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_NS],
        ["N[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_NA],
        ["N[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE, TokenSubType.F15_SB_SPEED_ALTITUDE_NM],

        # Cruise Climb element types
        ["M[0-9]{3}F[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MFF],
        ["M[0-9]{3}F[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MFS],
        ["M[0-9]{3}F[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MFA],
        ["M[0-9]{3}F[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MFM],
        ["M[0-9]{3}S[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MSF],
        ["M[0-9]{3}S[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MSS],
        ["M[0-9]{3}S[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MSA],
        ["M[0-9]{3}S[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MSM],
        ["M[0-9]{3}A[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MAF],
        ["M[0-9]{3}A[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MAS],
        ["M[0-9]{3}A[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MAA],
        ["M[0-9]{3}A[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MAM],
        ["M[0-9]{3}M[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MMF],
        ["M[0-9]{3}M[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MMS],
        ["M[0-9]{3}M[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MMA],
        ["M[0-9]{3}M[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_MMM],
        ["N[0-9]{4}F[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NFF],
        ["N[0-9]{4}F[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NFS],
        ["N[0-9]{4}F[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NFA],
        ["N[0-9]{4}F[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NFM],
        ["N[0-9]{4}S[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NSF],
        ["N[0-9]{4}S[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NSS],
        ["N[0-9]{4}S[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NSA],
        ["N[0-9]{4}S[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NSM],
        ["N[0-9]{4}A[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NAF],
        ["N[0-9]{4}A[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NAS],
        ["N[0-9]{4}A[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NAA],
        ["N[0-9]{4}A[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NAM],
        ["N[0-9]{4}M[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NMF],
        ["N[0-9]{4}M[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NMS],
        ["N[0-9]{4}M[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NMA],
        ["N[0-9]{4}M[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_NMM],
        ["K[0-9]{4}F[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KFF],
        ["K[0-9]{4}F[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KFS],
        ["K[0-9]{4}F[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KFS],
        ["K[0-9]{4}F[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KFM],
        ["K[0-9]{4}S[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KSF],
        ["K[0-9]{4}S[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KSS],
        ["K[0-9]{4}S[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KSA],
        ["K[0-9]{4}S[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KSM],
        ["K[0-9]{4}A[0-9]{3}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KAF],
        ["K[0-9]{4}A[0-9]{3}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KAS],
        ["K[0-9]{4}A[0-9]{3}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KAA],
        ["K[0-9]{4}A[0-9]{3}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KAM],
        ["K[0-9]{4}M[0-9]{4}F[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KMF],
        ["K[0-9]{4}M[0-9]{4}S[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KMS],
        ["K[0-9]{4}M[0-9]{4}A[0-9]{3}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KMA],
        ["K[0-9]{4}M[0-9]{4}M[0-9]{4}", TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE,
         TokenSubType.F15_SB_SPEED_ALTITUDE_KMM],
        ["M[0-9]{3}F[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_MF_P],
        ["M[0-9]{3}S[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_MS_P],
        ["M[0-9]{3}A[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_MA_P],
        ["M[0-9]{3}M[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_MM_P],
        ["N[0-9]{4}F[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_NF_P],
        ["N[0-9]{4}S[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_NS_P],
        ["N[0-9]{4}A[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_NA_P],
        ["N[0-9]{4}M[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_NM_P],
        ["K[0-9]{4}F[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_KF_P],
        ["K[0-9]{4}S[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_KS_P],
        ["K[0-9]{4}A[0-9]{3}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_KA_P],
        ["K[0-9]{4}M[0-9]{4}PLUS", TokenBaseType.F15_SPEED_ALTITUDE_PLUS, TokenSubType.F15_SB_SPEED_ALTITUDE_KM_P]
    ])

    # Gets and returns a record from all token descriptions for a given token
    # passed in as the argument 'token_string'.
    # The result is returned as a 3 field list that provides:
    # Index 0 - The regular expression describing the token, null string if
    #           a token is unknown. Constant TOKEN_REGEXP_IDX can be used to
    #           access this field.
    # Index 1 - The base type token identifier, Constant
    #           TOKEN_BASE_IDENTIFIER_IDX can be used to access this field.
    # Index 2 - The subtype token identifier, Constant
    #           TOKEN_SUBTYPE_IDENTIFIER_IDX can be used to access this field.
    def get_token_type(self, token_string=""):
        # type: (str) -> []
        for item in self.F15_SB_CONFIGURATION:
            if re.fullmatch(item[self.TOKEN_REGEXP_IDX], token_string):
                return item
        return ["", TokenBaseType.F15_UNKNOWN, TokenSubType.F15_SB_UNKNOWN]

    # This method loops over all the tokens produced by the Tokenizer and assigns
    # a token base and subtype to each token. The type definitions are obtained
    # from the definitions in the 'f15_token_syntax_descriptions' class.
    @staticmethod
    def assign_syntax_descriptions(tokens):
        # type: (Tokens) -> None
        f15tsa = F15TokenSyntaxDefinition()
        for token in tokens.get_tokens():
            token_string = token.get_token_string()
            result = f15tsa.get_token_type(token_string)
            token.set_token_base_type(result[F15TokenSyntaxDefinition.TOKEN_BASE_IDENTIFIER_IDX])
            token.set_token_sub_type(result[F15TokenSyntaxDefinition.TOKEN_SUBTYPE_IDENTIFIER_IDX])
            if len(token_string) > F15TokenSyntaxDefinition.MAX_TOKEN_LENGTH:
                token.set_token_base_type(TokenBaseType.F15_TOO_LONG)
                token.set_token_sub_type(TokenSubType.F15_SB_UNKNOWN)

    def print_descriptions(self):
        # type: () -> None
        for item in self.F15_SB_CONFIGURATION:
            self.print_description(item)

    def print_description(self, item):
        # type: ([]) -> None
        print("{0:>40}".format(item[self.TOKEN_REGEXP_IDX]),
              "{0:>40}".format(str(item[self.TOKEN_BASE_IDENTIFIER_IDX])) +
              "{0:>4}".format(item[self.TOKEN_BASE_IDENTIFIER_IDX]),
              "{0:>40}".format(str(item[self.TOKEN_SUBTYPE_IDENTIFIER_IDX])) +
              "{0:>4}".format(item[self.TOKEN_SUBTYPE_IDENTIFIER_IDX]))
