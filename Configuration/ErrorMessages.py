from Configuration.EnumerationConstants import ErrorId


# This class contains a dictionary of error messages used by the ICAO Message Parser
# when erroneous fields and / or subfields are detected.
class ErrorMessages:
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
            ErrorId.F8_TOO_MANY_FIELDS: "Field 8 is correct but there is extra unwanted date, "
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
            ErrorId.F10_F10B_SYNTAX: "Expecting surveillance capabilities as 'N' or one or more of 'A', 'B1-2', "
                                     "'C', 'D1', 'E', 'G1', 'H', 'I', 'L', 'P', 'S', 'U1-2', 'V1-2' or 'X' instead of "
                                     "'!'",
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
            ErrorId.MFS_POINT_TOO_MANY_FIELDS: "Expecting a single point for the MFS point, remove '!'"

            # Field 18 is handled by its own parser
            # Field 19 is handled by its own parser
            # Field 20 is handled by its own parser
            # Field 21 is handled by its own parser
            # Field 22 is handled by its own parser

        }

    # This method gets an error message using an enumeration value from the
    # ErrorId class.
    # Attributes
    # ----------
    # error_id:         The error message ID; an enum from the ErrorId class.
    # return:           A text string that is the error message.
    def get_error_message(self, error_id):
        # type: (ErrorId) -> str | None
        return self.error_messages[error_id]
