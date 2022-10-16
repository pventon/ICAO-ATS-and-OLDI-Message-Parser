from Configuration.EnumerationConstants import SubFieldIdentifiers
from Configuration.SubFieldDescription import SubFieldDescription


# This class contains configuration data describing the individual ICAO subfields.
# The individual subfield descriptions are written into an instance of the
# SubFieldDescription class and describe the following about each subfield:
#   ICAO Field Number / identifier as defined SubFieldIdentifiers
#   Minimum Field Length
#   Maximum Field Length
#   Field Syntax given as a regular expression
#   Indicator specifying if a field is compulsory or not, (True indicates it is)
# The SubFieldDescription class instances are stored in a dictionary and indexed
# by the SubFieldIdentifiers enumeration values.
class SubFieldDescriptions:

    # A dictionary containing for each ICAO subfield, its syntax description given
    # as a regular expression.
    subfield_description = {}

    # Regular expression for time in HHMM 0000 to 2359
    hhmm = "([01][0-9][0-5][0-9]|2[0-3][0-5][0-9])"

    # Regular expression for filing time as DDHHMM 0000 to 2359
    ddhhmm = "(([012][0-9]|3[01])" + hhmm + ")"

    # Regular expression for location indicator
    aero = "[A-Z]{4}"

    # Regular expression Latitude/Longitude in degrees 00 to 90 & 000 to 180
    ll = "[NS]([0-8][0-9]|90)[EW](0[0-9]{2}|1[0-7][0-9]|180)"

    # Regular expression Latitude/Longitude in degrees & minutes 0000 to 9000 & 00000 to 18000
    llmm = "[NS]([0-8][0-9][0-5][0-9]|9000)[EW](0[0-9]{2}[0-5][0-9]|1[0-7][0-9][0-5][0-9]|18000)"

    # Regular expression published route point
    prp = "[A-Z]{2,5}"

    # Regular expression for bearing 000 to 360
    bear = "([012][0-9]{2}|3[0-5][0-9]|360)"

    # Regular expression for distance 000 to 999
    dist = "[0-9]{3}"

    # Regular expression for facility address
    fac = "([A-Z]{8}|[A-Z]{3}[A-Z0-9]{4})"

    # Regular expression for priority indicator
    prio = "FF|GG|DD|KK|SS"

    # Regular expression for flight level and altitudes
    level = "(F[0-9]{2}[05]|A[0-9]{3}|[SM][0-9]{4})"

    # Regular expression for free text
    free = "[A-Z0-9 :/.\r\n\t]*"

    # Regular expression for DOF in the format YYMMDD
    # Jan, Mar, May, Jul, Oct, Dec = 31 days;
    # Apr, Jun, Aug, Sep, Nov = 30 days;
    # Feb 29 days year mod 4, otherwise 28 days
    # Further syntax checks done in the parser
    dof = "[0-9]{6}"

    # Regular expression for aircraft type
    type = "[A-Z][A-Z0-9]{1,4}"

    # Adjacent unit identifier
    unit = "[A-Z]{1,4}"

    # Channel sequence number
    seq_num = "[0-9]{3}"

    # This expression makes sure a string has spaces or a newline at its start / end
    # It's tricky to set up these regular expressions, be careful if changes are made
    # and re-run the unit tests to ensure nothing is broken.
    # "(^|\s)[A-Z]{4}($|\s)"

    def __init__(self):
        # type: () -> None
        # Format when assigning data descriptions to a FieldDescription instance is:
        # SubFieldDescription(
        #   ICAO Field Number / identifier as defined SubFieldIdentifiers,
        #   Minimum Field Length,
        #   Maximum Field Length,
        #   Field Syntax,
        #   Indicates if a field is compulsory, (True indicates it is))
        self.subfield_description = {
            # Message header subfields
            SubFieldIdentifiers.PRIORITY_INDICATOR: SubFieldDescription(
                SubFieldIdentifiers.PRIORITY_INDICATOR, 2, 2, self.prio, True),
            SubFieldIdentifiers.FILING_TIME: SubFieldDescription(
                SubFieldIdentifiers.FILING_TIME, 6, 6, self.ddhhmm, True),
            SubFieldIdentifiers.ORIGINATOR: SubFieldDescription(
                SubFieldIdentifiers.ORIGINATOR, 7, 8, self.fac, True),

            # Message header address fields
            SubFieldIdentifiers.ADDRESS1: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS1, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS2: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS2, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS3: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS3, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS4: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS4, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS5: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS5, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS6: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS6, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS7: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS7, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADDRESS8: SubFieldDescription(
                SubFieldIdentifiers.ADDRESS8, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS1: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS1, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS2: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS2, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS3: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS3, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS4: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS4, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS5: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS5, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS6: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS6, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS7: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS7, 7, 8, self.fac, False),
            SubFieldIdentifiers.ADADDRESS8: SubFieldDescription(
                SubFieldIdentifiers.ADADDRESS8, 7, 8, self.fac, False),

            # F3 - Message Title
            SubFieldIdentifiers.F3a: SubFieldDescription(
                SubFieldIdentifiers.F3a, 3, 3,
                "ABI|ACH|ACP|ACT|AFP|ALR|AMA|APL|ARR|CDN|CHG|CNL|COD|CPL|"
                "DEP|DLA|EST|FPL|FNM|INF|LAM|MAC|MFS|OCM|PAC|RAP|REJ|"
                "REV|RCF|RJC|ROC|RQP|RQS|RRV|SBY|SPL", True),
            SubFieldIdentifiers.F3b1: SubFieldDescription(
                SubFieldIdentifiers.F3b1, 1, 4, self.unit, False),
            SubFieldIdentifiers.F3b2: SubFieldDescription(
                SubFieldIdentifiers.F3b2, 1, 1, "[/]", False),
            SubFieldIdentifiers.F3b3: SubFieldDescription(
                SubFieldIdentifiers.F3b3, 1, 4, self.unit, False),
            SubFieldIdentifiers.F3b4: SubFieldDescription(
                SubFieldIdentifiers.F3b4, 3, 3, self.seq_num, False),
            SubFieldIdentifiers.F3c1: SubFieldDescription(
                SubFieldIdentifiers.F3c1, 1, 4, self.unit, False),
            SubFieldIdentifiers.F3c2: SubFieldDescription(
                SubFieldIdentifiers.F3c2, 1, 1, "[/]", False),
            SubFieldIdentifiers.F3c3: SubFieldDescription(
                SubFieldIdentifiers.F3c3, 4, 4, self.unit, False),
            SubFieldIdentifiers.F3c4: SubFieldDescription(
                SubFieldIdentifiers.F3c4, 1, 3, self.seq_num, False),

            # F5 - Emergency Information
            SubFieldIdentifiers.F5a: SubFieldDescription(
                SubFieldIdentifiers.F5a, 6, 8, "INCERFA|ALERFA|DETRESFA", True),
            SubFieldIdentifiers.F5ab: SubFieldDescription(
                SubFieldIdentifiers.F5ab, 1, 1, "[/]", True),
            SubFieldIdentifiers.F5b: SubFieldDescription(
                SubFieldIdentifiers.F5b, 7, 8, self.fac, True),
            SubFieldIdentifiers.F5bc: SubFieldDescription(
                SubFieldIdentifiers.F5bc, 1, 1, "[/]", True),
            SubFieldIdentifiers.F5c: SubFieldDescription(
                SubFieldIdentifiers.F5c, 0, 30, self.free, True),

            # F7 - Callsign
            SubFieldIdentifiers.F7a: SubFieldDescription(
                SubFieldIdentifiers.F7a, 1, 7, "[A-Z][A-Z0-9]{0,6}", True),
            SubFieldIdentifiers.F7ab: SubFieldDescription(
                SubFieldIdentifiers.F7ab, 1, 1, "[/]", False),
            SubFieldIdentifiers.F7b: SubFieldDescription(
                SubFieldIdentifiers.F7b, 1, 1, "[AC]", False),
            SubFieldIdentifiers.F7c: SubFieldDescription(
                SubFieldIdentifiers.F7c, 4, 4, "[0-7]{4}", False),

            # F8 - Flight rules and type of flight
            SubFieldIdentifiers.F8a: SubFieldDescription(
                SubFieldIdentifiers.F8a, 1, 1, "[IVYZ]", True),
            SubFieldIdentifiers.F8b: SubFieldDescription(
                SubFieldIdentifiers.F8b, 1, 1, "[SNMGX]", True),

            # F9 - Number, type of aircraft and WTC
            SubFieldIdentifiers.F9a: SubFieldDescription(
                SubFieldIdentifiers.F9a, 0, 2, "[0-9]{0,2}", False),
            SubFieldIdentifiers.F9b: SubFieldDescription(
                SubFieldIdentifiers.F9b, 2, 4, self.type, True),
            SubFieldIdentifiers.F9bc: SubFieldDescription(
                SubFieldIdentifiers.F9bc, 1, 1, "[/]", True),
            SubFieldIdentifiers.F9c: SubFieldDescription(
                SubFieldIdentifiers.F9c, 1, 1, "[LHMJ]", True),

            # F10 - Equipment
            SubFieldIdentifiers.F10a: SubFieldDescription(
                SubFieldIdentifiers.F10a, 1, 25, "[N]|([S]|[A-MOPRT-Z1-9]+|[A-MOPRT-Z1-9]+)", True),
            SubFieldIdentifiers.F10ab: SubFieldDescription(
                SubFieldIdentifiers.F10ab, 0, 20, "[/]", True),
            SubFieldIdentifiers.F10b: SubFieldDescription(
                SubFieldIdentifiers.F10b, 0, 20, "[ABCDEGHILPSUVX12]", True),

            # F13 - ADEP and EOBT
            SubFieldIdentifiers.F13a: SubFieldDescription(
                SubFieldIdentifiers.F13a, 4, 4, self.aero, True),
            SubFieldIdentifiers.F13b: SubFieldDescription(
                SubFieldIdentifiers.F13b, 4, 4, self.hhmm, True),

            # F14 - Estimate data
            SubFieldIdentifiers.F14a: SubFieldDescription(
                SubFieldIdentifiers.F14a, 1, 15,
                # Published Route Point
                "(" + self.prp + ")|"
                # Latitude longitude in degrees
                "(" + self.ll + ")|"
                # Latitude longitude in degrees and minutes
                "(" + self.llmm + ")|"
                # Point Bearing Distance
                "(" + self.prp + self.bear + self.dist + ")|"
                # Latitude longitude in degrees bearing distance
                "(" + self.ll + self.bear + self.dist + ")|"
                # Latitude longitude in degrees and minutes bearing distance
                "(" + self.llmm + self.bear + self.dist + ")", True),
            SubFieldIdentifiers.F14ab: SubFieldDescription(
                SubFieldIdentifiers.F14ab, 1, 1, "[/]", True),
            SubFieldIdentifiers.F14b: SubFieldDescription(
                SubFieldIdentifiers.F14b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F14c: SubFieldDescription(
                SubFieldIdentifiers.F14c, 4, 5, self.level, True),
            SubFieldIdentifiers.F14d: SubFieldDescription(
                SubFieldIdentifiers.F14d, 4, 5, self.level, False),
            SubFieldIdentifiers.F14e: SubFieldDescription(
                SubFieldIdentifiers.F14e, 1, 1, "[AB]", False),

            # F15 - Route data
            SubFieldIdentifiers.F15: SubFieldDescription(
                SubFieldIdentifiers.F15, 7, 1000, "[A-Z0-9/ \r\n\t]+", True),

            # F16 - ADES, EET and alternate Aerodromes
            SubFieldIdentifiers.F16a: SubFieldDescription(
                SubFieldIdentifiers.F16a, 4, 4, self.aero, True),
            SubFieldIdentifiers.F16b: SubFieldDescription(
                SubFieldIdentifiers.F16b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F16c: SubFieldDescription(
                SubFieldIdentifiers.F16c, 4, 4, self.aero, False),
            SubFieldIdentifiers.F16d: SubFieldDescription(
                SubFieldIdentifiers.F16d, 4, 4, self.aero, False),

            # F17 - Arrival Aerodrome and time
            SubFieldIdentifiers.F17a: SubFieldDescription(
                SubFieldIdentifiers.F17a, 4, 4, self.aero, True),
            SubFieldIdentifiers.F17b: SubFieldDescription(
                SubFieldIdentifiers.F17b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F17c: SubFieldDescription(
                SubFieldIdentifiers.F17c, 0, 20, self.free, False),

            # F18 - Other information
            SubFieldIdentifiers.F18altn: SubFieldDescription(
                SubFieldIdentifiers.F18altn, 0, 20, self.free, False),
            SubFieldIdentifiers.F18code: SubFieldDescription(
                SubFieldIdentifiers.F18code, 0, 10, self.free, False),
            SubFieldIdentifiers.F18com: SubFieldDescription(
                SubFieldIdentifiers.F18com, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dat: SubFieldDescription(
                SubFieldIdentifiers.F18dat, 0, 10, self.free, False),
            SubFieldIdentifiers.F18dep: SubFieldDescription(
                SubFieldIdentifiers.F18dep, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dest: SubFieldDescription(
                SubFieldIdentifiers.F18dest, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dof: SubFieldDescription(
                SubFieldIdentifiers.F18dof, 6, 6, self.dof, False),
            SubFieldIdentifiers.F18eet: SubFieldDescription(
                SubFieldIdentifiers.F18eet, 0, 200, self.free, False),
            SubFieldIdentifiers.F18est: SubFieldDescription(
                SubFieldIdentifiers.F18est, 0, 200, self.free, False),
            SubFieldIdentifiers.F18ifp: SubFieldDescription(
                SubFieldIdentifiers.F18ifp, 0, 200, self.free, False),
            SubFieldIdentifiers.F18nav: SubFieldDescription(
                SubFieldIdentifiers.F18nav, 0, 10, self.free, False),
            SubFieldIdentifiers.F18opr: SubFieldDescription(
                SubFieldIdentifiers.F18opr, 0, 20, self.free, False),
            SubFieldIdentifiers.F18per: SubFieldDescription(
                SubFieldIdentifiers.F18per, 0, 10, self.free, False),
            SubFieldIdentifiers.F18ralt: SubFieldDescription(
                SubFieldIdentifiers.F18ralt, 0, 20, self.free, False),
            SubFieldIdentifiers.F18reg: SubFieldDescription(
                SubFieldIdentifiers.F18reg, 0, 20, self.free, False),
            SubFieldIdentifiers.F18rif: SubFieldDescription(
                SubFieldIdentifiers.F18rif, 0, 20, self.free, False),
            SubFieldIdentifiers.F18rfp: SubFieldDescription(
                SubFieldIdentifiers.F18rfp, 0, 20, self.free, False),
            SubFieldIdentifiers.F18rmk: SubFieldDescription(
                SubFieldIdentifiers.F18rmk, 0, 40, self.free, False),
            SubFieldIdentifiers.F18rvr: SubFieldDescription(
                SubFieldIdentifiers.F18rvr, 0, 3, "[0-9]{3}", False),
            SubFieldIdentifiers.F18sel: SubFieldDescription(
                SubFieldIdentifiers.F18sel, 0, 20, self.free, False),
            SubFieldIdentifiers.F18sts: SubFieldDescription(
                SubFieldIdentifiers.F18sts, 0, 25, self.free, False),
            SubFieldIdentifiers.F18src: SubFieldDescription(
                SubFieldIdentifiers.F18src, 0, 25, self.free, False),
            SubFieldIdentifiers.F18typ: SubFieldDescription(
                SubFieldIdentifiers.F18typ, 0, 10, self.type, False),
            SubFieldIdentifiers.F18orgn: SubFieldDescription(
                SubFieldIdentifiers.F18orgn, 0, 20, self.free, False),

            # F19 - Supplementary information
            SubFieldIdentifiers.F19a: SubFieldDescription(
                SubFieldIdentifiers.F19a, 0, 20, self.free, False),
            SubFieldIdentifiers.F19c: SubFieldDescription(
                SubFieldIdentifiers.F19c, 0, 20, self.free, False),
            SubFieldIdentifiers.F19d: SubFieldDescription(
                SubFieldIdentifiers.F19d, 0, 20, "[0-9]{2}[ ]+[0-9]{3}[ ]+[C][ ]+[A-Z]+", False),
            SubFieldIdentifiers.F19e: SubFieldDescription(
                SubFieldIdentifiers.F19e, 0, 4, self.hhmm, False),
            SubFieldIdentifiers.F19j: SubFieldDescription(
                SubFieldIdentifiers.F19j, 0, 4, "[JFUV]{0,4}", False),
            SubFieldIdentifiers.F19n: SubFieldDescription(
                SubFieldIdentifiers.F19n, 0, 20, self.free, False),
            SubFieldIdentifiers.F19p: SubFieldDescription(
                SubFieldIdentifiers.F19p, 0, 3, "[0-9]{1,3}", False),
            SubFieldIdentifiers.F19r: SubFieldDescription(
                SubFieldIdentifiers.F19r, 0, 3, "[UVE]{0,3}", False),
            SubFieldIdentifiers.F19s: SubFieldDescription(
                SubFieldIdentifiers.F19s, 0, 4, "[PDMJ]{0,4}", False),

            SubFieldIdentifiers.F20: SubFieldDescription(
                SubFieldIdentifiers.F20, 0, 100, self.free, True),
            SubFieldIdentifiers.F21: SubFieldDescription(
                SubFieldIdentifiers.F21, 0, 100, self.free, True),
            SubFieldIdentifiers.F22: SubFieldDescription(
                SubFieldIdentifiers.F22, 0, 100, self.free, True),

            # Field 80 for OLDI
            # TODO - It appears that F80 is part of a custom F22, these definitions may be removed
            # TODO - For F80 it may be the syntax definitions go in the F22 parser
            SubFieldIdentifiers.F80a: SubFieldDescription(
                SubFieldIdentifiers.F80a, 0, 3, "[ABC]{0,3}", False),
            SubFieldIdentifiers.F80b: SubFieldDescription(
                SubFieldIdentifiers.F80b, 0, 3, "[DEF]{0,3}", False),

            # Field 81 for OLDI
            # TODO - It appears that F81 is part of a custom F22, these definitions may be removed
            # TODO - For F81 it may be the syntax definitions go in the F22 parser
            SubFieldIdentifiers.F81a: SubFieldDescription(
                SubFieldIdentifiers.F81b, 0, 3, "[ABC]{0,3}", False),
            SubFieldIdentifiers.F81b: SubFieldDescription(
                SubFieldIdentifiers.F81b, 0, 3, "[DEF]{0,3}", False),

            # Special for the MFS
            SubFieldIdentifiers.MFS_SIG_POINT: SubFieldDescription(
                SubFieldIdentifiers.MFS_SIG_POINT, 0, 15, "[A-Z][A-Z0-9]{1,14}", True),

            # Special for RQS content
            SubFieldIdentifiers.RQS_FREE_TEXT: SubFieldDescription(
                SubFieldIdentifiers.RQS_FREE_TEXT, 0, 0, self.free, True)
        }

    # This method gets the subfield description for an ICAO subfield based on its ICAO
    # subfield ID, i.e. F13a (Only the ADEP location indicator), F16ab (ADES and EET) etc.
    # Attributes
    # ----------
    # subfield_id:      The subfield ID; an enum from the SubFieldIdentifiers class. Based on
    #                   the ICAO subfields as defined in ICAO DOC 4444.
    # return:           An instance of SubFieldDescription containing a complete description
    #                   of a subfield including its syntax using a regular expression, or
    #                   None if the subfield 'icao_field_id' could not be found.
    def get_subfield_description(self, subfield_id):
        # type: (SubFieldIdentifiers) -> SubFieldDescription | None
        return self.subfield_description[subfield_id]
