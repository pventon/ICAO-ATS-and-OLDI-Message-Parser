from Configuration.EnumerationConstants import ErrorId


class ErrorMessages:
    """This class contains a dictionary of error messages used by the ICAO Message Parser
    when erroneous fields and / or subfields are detected.

    The error message dictionary keys are defined in EnumerationConstants.ErrorId class."""
    error_messages = {}

    def __init__(self):
        self.error_messages = {
            # System fatal case that really should never happen
            ErrorId.SYSTEM_FATAL: "FATAL - Internal error",
            ErrorId.SYSTEM_CONFIG_UNDEFINED: "Message content undefined for Message Type/Adjacent Unit"
                                             "/Title combination !",

            # Errors related to overall message processing
            ErrorId.MSG_EMPTY: "Message is empty",
            ErrorId.MSG_TOO_SHORT: "Message is too short and cannot be considered for processing",
            ErrorId.MSG_MISSING_HYPHENS: "No hyphens in message, cannot be an ICAO or ADEXP message",
            ErrorId.MSG_ADEXP_NOT_SUPPORTED: "Looks like an ADEXP message, currently not supported",
            ErrorId.MSG_TOO_MANY_FIELDS: "Too many fields in this message, the field '!' is superfluous; check "
                                         "placement of hyphens",
            ErrorId.MSG_TOO_FEW_FIELDS: "Too few fields in this message; expecting at least ! fields",

            # Error messages relating to field processing in general
            ErrorId.FLD_MORE_SUBFIELDS_EXPECTED: "More subfields expected after '!'",
            ErrorId.FLD_SLASH_SYNTAX: "Expecting forward slash '/' instead of '!'",
            ErrorId.FLD_TOO_MANY_FIELDS: "Too many fields found, '!' and / or check the overall syntax",

            # Errors relating to the header field Priority Indicator
            ErrorId.PRIORITY_SYNTAX: "Expecting priority indicator as 'FF', 'GG', 'DD', 'KK' or 'SS' instead of '!'",
            ErrorId.PRIORITY_MISSING: "The priority field is missing, should contain 'FF', 'GG', 'DD', 'KK' or 'SS'",
            ErrorId.PRIORITY_TOO_MANY_FIELDS: "Remove the extra field(s) '!' in the priority field",

            # Errors relating to the header field Filing Time
            ErrorId.FILING_TIME_SYNTAX: "Expecting filing time in DDHHMM format instead of '!'",
            ErrorId.FILING_TIME_MISSING: "The message filing time is missing, should contain DTG as DDHHMM",
            ErrorId.FILING_TIME_TOO_MANY_FIELDS: "Remove the extra field(s) '!' in the filing time field",

            # Errors relating to the header field Originator
            ErrorId.ORIGINATOR_SYNTAX: "Expecting 8 character or 7 character / digit ATC facility address instead of "
                                       "'!'",
            ErrorId.ORIGINATOR_MISSING: "The message originator is missing, 8 character or 7 "
                                        "character / digit ATC facility address",
            ErrorId.ORIGINATOR_TOO_MANY_FIELDS: "Remove the extra field(s) '!' in the originator field",

            # Errors relating to the header field Addressee
            ErrorId.ADDRESSEE_SYNTAX:
                "Expecting 8 character or 7 character / digit ATC facility address instead of '!'",
            ErrorId.ADDRESSEE_MISSING: "The addressee field is missing, expecting at least one addressee as an 8 "
                                       "character or 7 character / digit ATC facility address",
            ErrorId.ADDRESSEE_TOO_MANY_FIELDS: "Remove the extra field(s) '!' in the addressee field",

            # Errors relating to the header field Additional Addressee
            ErrorId.AD_ADDRESSEE_MISSING: "Expecting at least one additional addressee as an 8 character or 7 "
                                          "character / digit ATC facility address",
            ErrorId.AD_ADDRESSEE_SYNTAX: "Expecting 8 character or 7 character / digit ATC facility address instead "
                                         "of '!'",
            ErrorId.AD_ADDRESSEE_TOO_MANY_FIELDS: "Remove the extra field(s) '!' in the additional addressee field",

            # Errors relating to Field 3
            ErrorId.F3_TITLE_MISSING: "No ATS message title identified in this message",
            ErrorId.F3_TITLE_SYNTAX: "Message title '!' unrecognized, cannot process this message",
            ErrorId.F3_TX_SYNTAX: "Expecting adjacent unit sender name as 1 to 4 letters instead of '!'",
            ErrorId.F3_RX_SYNTAX: "Expecting adjacent unit receiver name as 1 to 4 letters instead of '!'",
            ErrorId.F3_SEQ_SYNTAX: "Expecting channel sequence number as 3 digits instead '!'",
            ErrorId.F3_RX_TX_EXPECTED: "Expecting sender/receiver adjacent unit name and sequence "
                                       "number instead of '!'",
            ErrorId.F3_TOO_MANY_FIELDS: "Field 3 is correct, the extra fields '!' should be removed",

            # Errors relating to Field 5
            ErrorId.F5_F5A_SYNTAX: "The first item in F5a should be INCERFA, ALERFA or DETRESFA instead of '!'",
            ErrorId.F5_F5AB_EXPECTING_SLASH: "Expecting '/<Facility Address>' instead of '!'",
            ErrorId.F5_F5B_SYNTAX: "Expecting 8 character or 7 character / digit ATC facility address instead of '!'",
            ErrorId.F5_F5BC_EXPECTING_SLASH: "Expecting '/<Free text>' instead of '!'",
            ErrorId.F5_F5C_SYNTAX: "Field 5c can only contain upper case characters and digits instead of '!'",
            ErrorId.F5_MISSING: "There is no data in field 5",
            ErrorId.F5_TOO_MANY_FIELDS: "Field 5 is correct, the extra field '!' should be removed",

            # Errors relating to Field 7
            ErrorId.F7_MISSING: "There is no data in field 7",
            ErrorId.F7_F7A_SYNTAX: "Expecting callsign in field 7 instead of '!', (1 to 7 characters and digits)",
            ErrorId.F7_F7AB_SYNTAX: "Expecting '/<SSR Mode ('A' or 'B') and Code "
                                    "(4 digits 0 to 7 as octal number>' instead of '!'",
            ErrorId.F7_F7B_SYNTAX: "Expecting SSR mode A or C instead of '!'",
            ErrorId.F7_F7C_SYNTAX: "Expecting SSR code as 4 digit octal value instead of '!'",
            ErrorId.F7_TOO_MANY_FIELDS: "Too many fields in Field 7, remove '!' and / or check the overall syntax",
            ErrorId.F7_MORE_SUBFIELDS_EXPECTED: "Expecting Mode A or C and octal SSR code at "
                                                "end of field instead of '!'",

            # Errors relating to Field 8
            ErrorId.F8_MISSING: "There is no data in field 8",
            ErrorId.F8_F8A_SYNTAX: "Expecting flight rules 'I', 'V', 'Y' or 'Z' instead of '!'",
            ErrorId.F8_F8B_SYNTAX: "Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of '!'",
            ErrorId.F8_TOO_MANY_FIELDS: "Field 8 is correct but there is extra unwanted data, "
                                        "remove '!' and / or check the overall syntax",
            ErrorId.F8_MORE_SUBFIELDS_EXPECTED: "Expecting type of flight after rules '!'",

            # Errors relating to Field 9
            ErrorId.F9_MISSING: "There is no data in field 9",
            ErrorId.F9_F9A_SYNTAX: "Expecting the number of aircraft as 1 or 2 digits instead of '!'",
            ErrorId.F9_F9B_SYNTAX: "Expecting aircraft type instead of '!'",
            ErrorId.F9_F9BC_SYNTAX: "Expecting WTC '/L', '/H', '/M' or '/J' after '!'",
            ErrorId.F9_F9C_SYNTAX: "Expecting WTC 'L', 'M', 'H' or 'J' instead of '!'",
            ErrorId.F9_TOO_MANY_FIELDS: "Too many fields in Field 9, remove '!' and / or check the overall syntax",
            ErrorId.F9_MORE_SUBFIELDS_EXPECTED: "Expecting <Number of A/C (optional), Aircraft Type / WTC> "
                                                "instead of '!'",

            # Errors relating to Field 10
            ErrorId.F10_MISSING: "There is no data in field 10",
            ErrorId.F10_F10A_SYNTAX: "Expecting COMMS/NAV capability as 'N' or 'S' and/or 'A-D', 'E1-3', "
                                     "'F-I', 'J1-7', 'K', 'L', 'M1-3', 'O', 'P1-9', 'R-Z' instead of '!'",
            ErrorId.F10_F10AB_SYNTAX: "Expecting surveillance capabilities as 'N' or one or more of 'A', 'B1-2', "
                                      "'C', 'D1', 'E', 'G1', 'H', 'I', 'L', 'P', 'S', 'U1-2', 'V1-2' or 'X' instead of "
                                      "'!'",
            ErrorId.F10_F10B_SYNTAX: "Expecting surveillance capabilities as 'N' or ('I', 'P', 'X') 'A', 'C' or "
                                     "'A', 'C', 'E', 'H', 'L', 'S' followed optionally by "
                                     "'B1', B2', 'D1', 'G1', 'U1', 'U2', 'V1', 'V2' instead of '!'",
            ErrorId.F10_TOO_MANY_FIELDS:
                "Field 10 is correct, remove the extra fields '!' and / or check the overall syntax",
            ErrorId.F10_MORE_SUBFIELDS_EXPECTED: "Expecting communications and surveillance "
                                                 "capabilities instead of '!'",

            # Errors relating to Field 13
            ErrorId.F13_MISSING: "There is no data in field 13",
            ErrorId.F13_F13A_SYNTAX: "Expecting departure aerodrome as an ICAO location "
                                     "indicator, e.g. EGLL instead of '!'",
            ErrorId.F13_F13B_SYNTAX: "Expecting EOBT in HHMM instead of '!'",
            ErrorId.F13_TOO_MANY_FIELDS: "Too many fields in Field 13, remove '!'",
            ErrorId.F13_MORE_SUBFIELDS_EXPECTED: "Expecting EOBT instead of '!'",

            # Errors relating to Field 14
            ErrorId.F14_MISSING: "There is no data in field 14",
            ErrorId.F14_F14A_SYNTAX: "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
                                     "degrees/minutes or point/bearing/distance instead of '!'",
            ErrorId.F14_F14AB_SYNTAX: "Processing the slash",
            ErrorId.F14_F14B_SYNTAX: "Expecting boundary crossing time in '/HHMM' instead of '!'",
            ErrorId.F14_F14C_SYNTAX: "Expecting cleared level (F/A 3 digits, or M/S 4 digits) instead of '!'",
            ErrorId.F14_F14D_SYNTAX: "Expecting supplementary crossing data (F/A 3 digits, or M/S 4 digits) instead "
                                     "of '!'",
            ErrorId.F14_F14E_SYNTAX: "Expecting crossing condition (A or B) instead of '!'",
            ErrorId.F14_TOO_MANY_FIELDS: "Too many field(s) in Field 14, remove '!'",
            ErrorId.F14_MORE_FIELDS_EXPECTED: "Field 14 is incomplete, whole field should be Point/Time '/' (HHMM), "
                                              "Cleared level, supplementary "
                                              "crossing level, crossing condition (A or B) instead of '!'",

            # Errors relating to Field 15
            # This field has its own dedicated parser, hence no other errors are needed
            ErrorId.F15_MISSING: "There is no route description in field 15",

            # Errors relating to Field 16
            ErrorId.F16_MISSING: "There is no data in field 16",
            ErrorId.F16_F16A_SYNTAX: "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of "
                                     "'!'",
            ErrorId.F16_F16B_SYNTAX: "Expecting EOBT in HHMM instead of '!'",
            ErrorId.F16_F16C_SYNTAX: "Expecting alternate aerodrome as an ICAO location indicator instead of '!'",
            ErrorId.F16_F16D_SYNTAX: "Expecting alternate aerodrome as an ICAO location indicator instead of '!'",
            ErrorId.F16_TOO_MANY_FIELDS: "Too many fields in Field 16, remove '!'",

            # Errors relating to Field 17
            ErrorId.F17_MISSING: "There is no data in field 17",
            ErrorId.F17_F17A_SYNTAX: "Expecting arrival aerodrome as an ICAO location indicator, e.g. EGLL instead of "
                                     "'!'",
            ErrorId.F17_F17B_SYNTAX: "Expecting ATA in HHMM instead of '!'",
            ErrorId.F17_F17C_SYNTAX: "Invalid characters for alternate aerodrome text, should be "
                                     "'A' to 'Z' and '0' to '9' only instead of '!'",
            # Field 'c' is free text, no limit on this, only invalid characters
            ErrorId.F17_TOO_MANY_FIELDS: "Invalid characters for alternate aerodrome text, should be "
                                         "'A' to 'Z' and '0' to '9' only instead of '!'",

            # Field 18 DOF - This is the Field 18 DOF at the end of many messages,
            # it's not a complete Field 18, only the DOF
            ErrorId.F18_DOF_MISSING: "There is no data in field 18",
            ErrorId.F18_DOF_F18A_SYNTAX: "Expecting DOF in the format YYMMDD instead of '!'",
            # Field Junk following the DOF
            ErrorId.F18_DOF_TOO_MANY_FIELDS: "Invalid characters for alternate aerodrome text, should be "
                                             "'A' to 'Z' and '0' to '9' only instead of '!'",

            ErrorId.MFS_POINT_MISSING: "There is no data in field MFS Significant point field",
            ErrorId.MFS_POINT_SYNTAX: "Expecting MFS significant point starting with a letter "
                                      "followed by up to 14 letters and digits instead of '!'",
            ErrorId.MFS_POINT_TOO_MANY_FIELDS: "Expecting a single point for the MFS point, remove '!'",

            # Field 18 is handled by its own parser
            ErrorId.F18_NO_F18_KEYWORDS_FOUND: "Expecting field 18 keyword/data instead of '!'",
            ErrorId.F18_UNRECOGNISED_DATA: "Expecting data following field 18 keyword '!'",
            ErrorId.F18_DATA_MISSING: "No data in field 18, expecting field 18 keyword/data",
            ErrorId.F18_GARBAGE: "Field 18 contains invalid data, expecting field 18 keyword/data instead of '!'",
            ErrorId.F18_ZERO_OR_KEYWORDS: "Field 18 contains no keywords, can be '0' or 'n' "
                                          "keyword/data occurrences instead of '!'",
            ErrorId.F18_UNRECOGNISED_KEYWORD: "Field 18 Keyword '!' unrecognised",
            ErrorId.F18_ALTN_SYNTAX: "The F18 ALTN field contains illegal characters, only A-Z, 0-9 "
                                     "and spaces allowed instead of '!'",
            ErrorId.F18_AWR_SYNTAX: "Expecting F18 AWR as R[1-9] instead of '!'",
            ErrorId.F18_AWR_TOO_MANY: "Too many F18 AWR fields, should only be one field as R[1-9] instead of '!'",
            ErrorId.F18_CODE_SYNTAX: "Expecting F18 CODE as hexadecimal address with 7 HEX digits "
                                     "starting at F000000 instead of '!'",
            ErrorId.F18_CODE_TOO_MANY: "Too many F18 CODE fields, should only be one field  with 7 HEX digits "
                                       "instead of '!'",
            ErrorId.F18_COM_SYNTAX: "Expecting F18 COM as communication capabilities (only A-Z, 0-9 and spaces) "
                                    "not specified in ICAO field 10a instead of '!'",
            ErrorId.F18_DAT_SYNTAX: "Expecting F18 DAT as data application capabilities (only A-Z, 0-9 and spaces) "
                                    "not specified in ICAO field 10a instead of '!'",
            ErrorId.F18_DEP_SYNTAX: "Expecting F18 DEP as name and location of departure aerodrome if ZZZZ inserted "
                                    "in ICAO field 13a, (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_DEST_SYNTAX: "Expecting F18 DEST as name and location of destination aerodrome if ZZZZ "
                                     "inserted in ICAO field 16a, (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_DLE_TOO_SHORT: "Expected F18 DLE as 'point HHMM' instead of '!', (can be any kind of point)",
            ErrorId.F18_DLE_PNT_SYNTAX: "Expected F18 DLE point as a PRP, Latitude/Longitude "
                                        "(with or without minutes) or bearing distance instead of '!'",
            ErrorId.F18_DLE_TIME_SYNTAX: "Expected F18 DLE time in HHMM format instead of '!'",
            ErrorId.F18_DLE_TOO_MANY: "Too many fields in F18 DLE, expecting single field as point & "
                                      "time instead of '!'",
            ErrorId.F18_EET_PNT_SYNTAX: "Expected F18 EET point as a PRP, Latitude/Longitude "
                                        "(with or without minutes) or bearing distance instead of '!'",
            ErrorId.F18_EET_TIME_SYNTAX: "Expected F18 EET time in HHMM format instead of '!'",
            ErrorId.F18_EST_SYNTAX: "Expecting F18 EST as estimate data (not sure of the syntax for this at "
                                    "the moment), (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_IFP_SYNTAX: "Expecting F18 IFP as 'ERROUTRAD', 'ERROUTWE', 'ERROUTE', 'ERRTYPE', "
                                    "'ERRLEVEL', 'ERREOBT', 'NON833', '833UNKNOWN', 'MODESASP', 'RVSMVIOLATION', "
                                    "'NONRVSM' or 'RVSMUNKNOWN' instead of '!'",
            ErrorId.F18_NAV_SYNTAX: "Expecting F18 NAV as significant navigation equipment as one or more "
                                    "space separated designators, (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_OPR_SYNTAX: "Expecting F18 OPR as name of aircraft operating agency, "
                                    "(only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_ORGN_SYNTAX: "Expected F18 ORGN as an 8 or 7 character facility address instead of '!'",
            ErrorId.F18_ORGN_TOO_SHORT: "F18 ORGN is too short, 8 or 7 character facility address expected "
                                        "instead of '!'",
            ErrorId.F18_ORGN_TOO_MANY: "Too many fields in F18 ORGN, expecting single field as facility address "
                                      "instead of '!'",
            ErrorId.F18_PBN_TOO_LONG: "Maximum length of F18 PBN is 16 characters, shorten the field '!'",
            ErrorId.F18_PBN_SYNTAX: "F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, "
                                    "C1-C4, D1-D4, L1, O1-O4, S1, S2, T1 or T2 instead of '!'",
            ErrorId.F18_PBN_TOO_MANY: "The F18 PBN field should be a single field instead of '!'",
            ErrorId.F18_PBN_TOO_SHORT: "F18 PBN must be at least two characters long, expecting 1 to eight of "
                                       "either A1, B1-B6, C1-C4, D1-D4, L1, O1-O4, S1, S2, T1 or T2 instead of '!'",
            ErrorId.F18_PER_SYNTAX: "F18 PER syntax incorrect, expecting a single character A to Z instead of '!'",
            ErrorId.F18_PER_TOO_MANY: "The F18 PER field should be a single field instead of '!'",
            ErrorId.F18_RALT_SYNTAX: "Expecting F18 RALT as location indicator, alternate arrival aerodrome name "
                                     "or location as a latitude/longitude, (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_REG_SYNTAX: "Expecting F18 REG as nationality or mark and aircraft registration "
                                    "(only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_RIF_SYNTAX: "Expecting F18 RIF revised route to destination aerodrome, "
                                    "(only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_RFP_SYNTAX: "Expecting F18 RIF as Q[1-9] instead of '!'",
            ErrorId.F18_RFP_TOO_MANY: "Too many F18 RIF fields, should only be one field as Q[1-9] instead of '!'",
            ErrorId.F18_RMK_SYNTAX: "The F18 RMK field must only contain characters A-Z, 0-9, '.', ':', ';' and ',' "
                                      "instead of '!'",
            ErrorId.F18_RVR_SYNTAX: "Expecting F18 RVR as 1 to 3 digit number instead of '!'",
            ErrorId.F18_RVR_TOO_MANY: "Too many F18 RVR fields, should only be one field as 1 to 3 digit "
                                      "number instead of '!'",
            ErrorId.F18_SEL_SYNTAX: "Expecting F18 SEL as 4 to 5 alpha characters instead of '!'",
            ErrorId.F18_SEL_TOO_MANY: "Too many F18 SEL fields, should only be one field as 4 to 5 alpha characters "
                                      "instead of '!'",
            ErrorId.F18_STAYINFO_SYNTAX: "The F18 STAYINFO field contains illegal characters, only A-Z, 0-9 "
                                     "and spaces allowed instead of '!'",
            ErrorId.F18_STS_SYNTAX: "Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', "
                                    "'HOSP', 'HUM', 'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of '!'",
            ErrorId.F18_STS_TOO_MANY: "Too many F18 STS fields, should only be one field as 'ALTRV', 'ATFMX', "
                                      "'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', 'MARSA', 'MEDEVAC', "
                                      "'NONRVSM', 'SAR' or 'STATE' instead of '!'",
            ErrorId.F18_SRC_SYNTAX: "Expecting F18 SRC as 'RPL', 'FPL', 'AFIL', 'MFS', 'FNM', 'RQP', 'AFP', 'DIV' "
                                    "or a 4 character location indicator instead of '!'",
            ErrorId.F18_SRC_TOO_MANY: "Too many F18 SRC fields, should only be one field as 'RPL', 'FPL', 'AFIL', "
                                      "'MFS', 'FNM', 'RQP', 'AFP', 'DIV' or a 4 character location instead of '!'",
            ErrorId.F18_SUR_SYNTAX: "The F18 SUR field should contain surveillance application capabilities using "
                                    "characters A-Z, 0-9 instead of '!'",
            ErrorId.F18_TALT_SYNTAX: "Expecting F18 TALT as location indicator, alternate departure aerodrome name "
                                     "or location as a latitude/longitude, (only A-Z, 0-9 and spaces) instead of '!'",
            ErrorId.F18_TYP_SYNTAX: "Expecting number (optional) and type of aircraft instead of '!'",

            # Field 19 is handled by its own parser
            ErrorId.F19_NO_F19_KEYWORDS_FOUND: "Expecting field 19 keyword/data instead of '!'",
            ErrorId.F19_DATA_MISSING: "No data in field 19, expecting field 19 keyword/data",
            ErrorId.F19_UNRECOGNISED_DATA: "Expecting data following field 19 keyword '!'",
            ErrorId.F19_UNRECOGNISED_KEYWORD: "Field 19 Keyword '!' unrecognised",
            ErrorId.F19_ZERO_OR_KEYWORDS: "Field 19 contains no keywords, must consist of one or more "
                                          "keyword/data occurrences instead of '!'",
            ErrorId.F19_A_SYNTAX: "Expecting other significant markings and / or aircraft color (A-Z, 0-9 and spaces) "
                                  "instead of '!' in F19 'A'",
            ErrorId.F19_C_SYNTAX: "Expecting pilot name (A-Z, 0-9 and spaces) instead of '!' in F19 'C'",
            ErrorId.F19_Da_SYNTAX: "Expecting number of dinghies as 1 to 2 digits instead of '!' in F19 'D'",
            ErrorId.F19_Db_SYNTAX: "Expecting number of people that can be carried in total in all dinghies "
                                   "as 1 to 3 digits instead of '!' in F19 'D'",
            ErrorId.F19_Dc_SYNTAX: "Expecting 'C' to indicate dinghies are covered instead of '!' in F19 'D'",
            ErrorId.F19_Dd_SYNTAX: "Expecting the colour of the dinghies instead of '!' in F19 'D'",
            ErrorId.F19_D_TOO_MANY: "Too many fields in F19 'D', remove '!'",
            ErrorId.F19_D_TOO_FEW: "Expecting number of dinghies, dinghy capacity, covered or not and dinghy color, "
                                   "too few fields in F19 'D', '!'",
            ErrorId.F19_E_SYNTAX: "Expecting fuel endurance in HHMM format instead of '!' in F19 'E'",
            ErrorId.F19_E_TOO_MANY: "Only one field expected in F19 'E' as fuel endurance in HHMM format "
                                    "instead of '!'",
            ErrorId.F19_J_SYNTAX: "Expecting life jacket equipment as one or more of 'F', 'L', 'U' or 'V' "
                                  "indicators instead of '!' in F19 'J'",
            ErrorId.F19_J_TOO_MANY: "Only one field expected in F19 'J' as life jacket equipment as "
                                    "'F', 'L', 'U' or 'V' instead of '!'",
            ErrorId.F19_N_SYNTAX: "Expecting other survival equipment and useful remarks (A-Z, 1-9 and spaces) "
                                  "instead of '!' in F19 'N'",
            ErrorId.F19_P_SYNTAX: "Expecting number of passengers on board as 1 to 3 digits instead of '!' in F19 'P'",
            ErrorId.F19_P_TOO_MANY: "Only one field expected in F19 'P' as 1 to 3 digits instead of '!'",
            ErrorId.F19_R_SYNTAX: "Expecting frequency availability on board as one or more of 'E', 'U' or 'V' "
                                  "instead of '!' in F19 'R'",
            ErrorId.F19_R_TOO_MANY: "Only one field expected in F19 'R' as 'E', 'U' or 'V' instead of '!'",
            ErrorId.F19_S_SYNTAX: "Expecting survival equipment on board as one or more of 'D', 'J', 'M' or 'P' "
                                  "instead of '!' in F19 'S'",
            ErrorId.F19_S_TOO_MANY: "Only one field expected in F19, one or more of "
                                    "'S' as 'D', 'J', 'M' or 'P' instead of '!'",

            # Errors relating to Field 20
            ErrorId.F20_MISSING: "There is no data in field 20",
            ErrorId.F20_F20A_SYNTAX: "Invalid characters in field 20a, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F20_F20B_SYNTAX: "Invalid characters in field 20b, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F20_F20C_SYNTAX: "Expecting time in HHMM instead of '!'",
            ErrorId.F20_F20D_SYNTAX: "Expecting frequency in 2 to 4 digits, decimal "
                                     "point, 1 to 2 digit format instead of '!'",
            ErrorId.F20_F20E_SYNTAX: "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
                                     "degrees/minutes or point/bearing/distance instead of '!'",
            ErrorId.F20_F20F_SYNTAX: "Invalid characters in field 20f, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F20_F20G_SYNTAX: "Invalid characters in field 20g, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F20_F20H_SYNTAX: "Invalid characters in field 20h, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F20_TOO_MANY_FIELDS: "Too many fields in Field 20, remove '!'",

            # Errors relating to Field 20
            ErrorId.F21_MISSING: "There is no data in field 21",
            ErrorId.F21_F21A_SYNTAX: "Expecting time in HHMM instead of '!'",
            ErrorId.F21_F21B_SYNTAX: "Expecting frequency in 2 to 4 digits, decimal "
                                     "point, 1 to 2 digit format instead of '!'",
            ErrorId.F21_F21C_SYNTAX: "Expecting point as PRP, Lat/Long in degrees, Lat/Long in "
                                     "degrees/minutes or point/bearing/distance instead of '!'",
            ErrorId.F21_F21D_SYNTAX: "Expecting time in HHMM instead of '!'",
            ErrorId.F21_F21E_SYNTAX: "Invalid characters in field 21e, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F21_F21F_SYNTAX: "Invalid characters in field 21f, expecting A to Z, 0 to 9 instead of '!'",
            ErrorId.F21_TOO_MANY_FIELDS: "Too many fields in Field 21, remove '!'",

            # Field 22 is handled by its own parser
            ErrorId.F22_NO_F22_KEYWORDS_FOUND: "Expecting <field 22 ICAO field number>/<ICAO field> instead of '!'",
            ErrorId.F22_DATA_MISSING: "No data in field 22, expecting <field 22 ICAO field number>/<ICAO field>",
            ErrorId.F22_UNRECOGNISED_DATA: "Expecting data following field 22 ICAO field number '!'",
            ErrorId.F22_UNRECOGNISED_KEYWORD: "Field 22 ICAO field number '!' unrecognised",
            ErrorId.F22_ZERO_OR_KEYWORDS: "Field 22 contains no ICAO fields, must consist of one or more "
                                          "<ICAO field number>/<ICAO field> occurrences instead of '!'",
            ErrorId.F22_FIELD_DUPLICATED: "F22 - Field number '!' is duplicated and should be removed",

            # Errors relating to Field 80
            ErrorId.F80_MISSING: "There is no data in field 80",
            ErrorId.F80_F80A_SYNTAX: "Expecting type of flight 'S', 'N', 'G', 'M' or 'X' instead of '!'",
            ErrorId.F80_TOO_MANY_FIELDS: "Field 80 is correct but there is extra unwanted data, "
                                        "remove '!' and / or check the overall syntax",
            ErrorId.F80_MORE_SUBFIELDS_EXPECTED: "Expecting type of flight after rules '!'",

            ErrorId.F81_MISSING: "There is no data in field 81",
            ErrorId.F81_F81A_SYNTAX: "Expecting equipment code or surveillance class instead of '!'",
            ErrorId.F81_F81AB_SYNTAX: "Expecting a forward slash '/' instead of '!'",
            ErrorId.F81_F81B_SYNTAX: "Expecting equipment stats as 'EQ'.'UN' or 'NO' instead of '!'",
            ErrorId.F81_F81BC_SYNTAX: "Expecting a forward slash '/' instead of '!'",
            ErrorId.F81_F81C_SYNTAX: "Expecting surveillance equipment code instead of '!'",
            ErrorId.F81_TOO_MANY_FIELDS: "Too many field(s) in Field 81, remove '!'",
            ErrorId.F81_MORE_FIELDS_EXPECTED: "Field 81 is incomplete, field should be (equipment code '/' "
                                              "equipment status) or (surveillance class '/' equipment status "
                                              "'/' surveillance equipment code) instead of '!'",
            ErrorId.CONSISTENCY_F8_F8A_UNKNOWN: "Field 15 infers flight rule is '!', but rules are missing in Field 8;",
            ErrorId.CONSISTENCY_F8_DERIVED_UNKNOWN: "Field 8 flight rules specified as '!' but unable to confirm"
                                                    "flight rules from field 15 ",
            ErrorId.CONSISTENCY_F8_F8_DERIVED_DIFFERENT: "Flight rules derived from field 15 ('!') differ from "
                                                         "the rules given in field 8",
            ErrorId.CONSISTENCY_F9B_TYP: "Field 9b contains 'ZZZZ' and the field 18 'TYP' subfield is missing, "
                                          "enter a 'TYP' subfield in field 18.",
            ErrorId.CONSISTENCY_F10_R: "Field 10a contains an 'R', therefore field 18 must contain the "
                                       "subfield ! with one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5'",
            ErrorId.CONSISTENCY_F10_Z: "Field 10a contains a 'Z', therefore field 18 must contain one of the "
                                       "subfields !",
            ErrorId.CONSISTENCY_F13A_DEP: "Field 13a contains 'ZZZZ' and the field 18 'DEP' subfield is missing, "
                                          "enter a 'DEP' subfield in field 18.",
            ErrorId.CONSISTENCY_F16A_DEST: "Field 16a contains 'ZZZZ' and the field 18 'DEST' subfield is missing, "
                                          "enter a 'DEST' subfield in field 18.",
            ErrorId.CONSISTENCY_PBN_D: "Field 18 ! contains one or more of the indicators "
                                       "'B1', 'B3', 'B4', 'C1', 'C3', 'C4', 'D1', 'D3', 'D4', 'O1', "
                                       "'O3' or 'O4', therefore F10a must contain the letter 'D'",
            ErrorId.CONSISTENCY_PBN_G: "Field 18 ! contains one or more of the indicators "
                                       "'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'O1' or 'O2', therefore F10a "
                                       "must contain the letter 'G'",
            ErrorId.CONSISTENCY_PBN_I: "Field 18 ! contains one or more of the indicators "
                                       "'B1', 'B5', 'C1', 'C4', 'D1', 'D4', 'O1' or 'O4', therefore F10a "
                                       "must contain the letter 'I'",
            ErrorId.CONSISTENCY_PBN_OS: "Field 18 ! contains one or more of the indicators "
                                         "'B1' or 'B4', therefore F10a must contain one or more of the letters "
                                         "'D' and 'O' or 'S'",
            ErrorId.CONSISTENCY_PBN_R: "Field 18 ! contains one or more of the indicators "
                                       "'B1', 'B2', 'B3', 'B4' or 'B5', therefore F10a must contain the letter 'R'"
        }

    def get_error_message(self, error_id):
        # type: (ErrorId) -> str | None
        """This method gets an error message using an enumeration value from the ErrorId class.

            :param error_id: The error message ID; an enum from the ErrorId class.
            :return: A text string that is the error message."""
        return self.error_messages[error_id]
