from Configuration.EnumerationConstants import SubFieldIdentifiers
from Configuration.SubFieldDescription import SubFieldDescription


class SubFieldDescriptions:
    """This class contains configuration data describing the individual ICAO subfields.

    The individual subfield descriptions are written into an instance of the SubFieldDescription class
    and describe the following about each subfield:
        - ICAO Field Number / identifier as defined in the SubFieldIdentifiers class
        - Minimum Field Length
        - Maximum Field Length
        - Field Syntax given as a regular expression
        - Boolean indicator specifying if a field is compulsory or not, (True indicates it is)
    The SubFieldDescription class instances are stored in a dictionary and indexed
    by the SubFieldIdentifiers enumeration values."""

    subfield_description = {}
    """A dictionary containing for each ICAO subfield, its syntax description given
    as a regular expression."""

    hhmm = "([01][0-9][0-5][0-9]|2[0-3][0-5][0-9])"
    """Regular expression for time in HHMM 0000 to 2359"""

    ddhhmm = "(([012][0-9]|3[01])" + hhmm + ")"
    """Regular expression for filing time as DDHHMM 0000 to 2359"""

    aerodrome = "[A-Z]{4}"
    """Regular expression for location indicator"""

    ll = "([0-8][0-9]|90)[NS](0[0-9]{2}|1[0-7][0-9]|180)[EW]"
    """Regular expression Latitude/Longitude in degrees 00 to 90 & 000 to 180"""

    llmm = "([0-8][0-9][0-5][0-9]|9000)[NS](0[0-9]{2}[0-5][0-9]|1[0-7][0-9][0-5][0-9]|18000)[EW]"
    """Regular expression Latitude/Longitude in degrees & minutes 0000 to 9000 & 00000 to 18000"""

    prp = "[A-Z]{2,5}"
    """Regular expression published route point"""

    bearing = "([012][0-9]{2}|3[0-5][0-9]|360)"
    """Regular expression for bearing 000 to 360"""

    distance = "[0-9]{3}"
    """Regular expression for distance 000 to 999"""

    fac = "([A-Z]{8}|[A-Z]{3}[A-Z0-9]{4})"
    """# Regular expression for facility address"""

    priority = "FF|GG|DD|KK|SS"
    """Regular expression for priority indicator"""

    altitude = "(F[0-9]{2}[05]|A[0-9]{3}|[SM][0-9]{4})"
    """Regular expression for flight level and altitudes"""

    free = "[A-Z0-9 _:/.\r\n\t]*"
    """# Regular expression for free text"""

    dof = "[0-9]{6}"
    """Regular expression for DOF in the format YYMMDD 
    Further syntax checks done in the parser"""

    type = "[A-Z][A-Z0-9]{1,4}"
    """Regular expression for aircraft type"""

    unit = "[A-Z]{1,4}"
    """# Adjacent unit identifier"""

    seq_num = "[0-9]{3}"
    """Channel sequence number"""

    frequency = "[0-9]{2,4}[.][0-9]{1,2}"
    """A frequency"""

    point = "(" + prp + ")|" \
            "(" + ll + ")|" \
            "(" + llmm + ")|" \
            "(" + prp + bearing + distance + ")|" \
            "(" + ll + bearing + distance + ")|" \
            "(" + llmm + bearing + distance + ")"
    """
    Reporting point defined as one of the following:
        AIP Published Route Point
          "(" + self.prp + ")|"
        Latitude longitude in degrees
          "(" + self.ll + ")|"
        Latitude longitude in degrees and minutes
          "(" + self.llmm + ")|"
        Point Bearing Distance
          "(" + self.prp + self.bear + self.dist + ")|"
        Latitude longitude in degrees bearing distance
          "(" + self.ll + self.bear + self.dist + ")|"
        Latitude longitude in degrees and minutes bearing distance
          "(" + self.llmm + self.bear + self.dist + ")", True),"""

    pbn = "(A1){0,1}(B1){0,1}(B2){0,1}(B3){0,1}(B4){0,1}(B5){0,1}(B6){0,1}(C1){0,1}(C2){0,1}" \
          "(C3){0,1}(C4){0,1}(D1){0,1}(D2){0,1}(D3){0,1}(D4){0,1}(L1){0,1}(O1){0,1}(O2){0,1}" \
          "(O3){0,1}(O4){0,1}(S1){0,1}(S2){0,1}(T1){0,1}(T2){0,1}"
    """
    F18 PBN field, EUROCONTROL Definition:
        1 { "A1" | "B1" | "B2" | "B3" | "B4" | "B5" | "B6" | "C1" | "C2" | "C3" | "C4" | "D1" | "D2" | "D3"
        | "D4" | "L1" | "O1" | "O2" | "O3" | "O4" | "S1" | "S2" | "T1" | "T2" } 8"""

    equipment_code = "N|((A){0,1}(B){0,1}(C){0,1}(D){0,1}(E1){0,1}(E2){0,1}(E3){0,1}" \
                     "(F){0,1}(G){0,1}(H){0,1}(I){0,1}(J1){0,1}(J2){0,1}(J3){0,1}" \
                     "(J4){0,1}(J5){0,1}(J6){0,1}(J7){0,1}(K){0,1}(L){0,1}(M1){0,1}" \
                     "(M2){0,1}(M3){0,1}(O){0,1}(P1){0,1}(P2){0,1}(P3){0,1}(P4){0,1}" \
                     "(P5){0,1}(P6){0,1}(P7){0,1}(P8){0,1}(P9){0,1}(R){0,1}(S){0,1}" \
                     "(T){0,1}(U){0,1}(V){0,1}(W){0,1}(X){0,1}(Y){0,1}(Z){0,1})"
    """
    This is ICAO F10a, EUROCONTROL Definition:
        "N" | 
        ( 1 { "A" | "B" | "C" | "D" | "E1" | "E2" | "E3" | "F" | "G" | "H" | "I" |
        "J1" | "J2"| "J3" | "J4" | "J5" | "J6" | "J7" | "K" | "L" | "M1" | "M2"|
        "M3" | "O" | "P1"| "P2"| "P3"| "P4"| "P5"| "P6"| "P7"| "P8"| "P9" | "R" |
        "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" } )
    """

    equipment_status = "EQ|NO|UN"
    """Equipment status, this is used in the custom F22 OLDI fields 80 and 81;"""

    surveillance_class = "A|S|ADSB|ADSC"
    """Surveillance class, this is used in the custom F22 OLDI fields 80 and 81;"""

    surveillance_equipment_code = "A|B1|B2|C|D1|E|G1|H|I|L|P|S|U1|U2|V1|V2|X"
    """Surveillance equipment code, this is used in the custom F22 OLDI fields 80 and 81;"""

    flight_type = "[SNMGX]"
    """Type of flight, ICAO field 8b and field 80a"""

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
                SubFieldIdentifiers.PRIORITY_INDICATOR, 2, 2, self.priority, True),
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
                SubFieldIdentifiers.F8b, 1, 1, self.flight_type, True),

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
                SubFieldIdentifiers.F10a, 1, 25, self.equipment_code, True),
            SubFieldIdentifiers.F10ab: SubFieldDescription(
                SubFieldIdentifiers.F10ab, 0, 20, "[/]", True),
            SubFieldIdentifiers.F10b: SubFieldDescription(
                # "N" | (1{ ("I" | "P" | "X") | "A" | "C"}3 | (1{ "A" | "C" | "E" | "H" | "L" | "S"}6) )
                #       [1{"B1"| "B2" | "D1" | "G1" | "U1" | "U2" | "V1" | "V2"}8]
                SubFieldIdentifiers.F10b, 0, 20,
                "N|(([IPX]{0,1}(A){0,1}(C){0,1})|((A){0,1}(C){0,1}(E){0,1}(H){0,1}(L){0,1}(S){0,1}))"
                "((B1){0,1}(B2){0,1}(D1){0,1}(G1){0,1}(U1){0,1}(U2){0,1}(V1){0,1}(V2){0,1}){0,1}", True),

            # F13 - ADEP and EOBT
            SubFieldIdentifiers.F13a: SubFieldDescription(
                SubFieldIdentifiers.F13a, 4, 4, self.aerodrome, True),
            SubFieldIdentifiers.F13b: SubFieldDescription(
                SubFieldIdentifiers.F13b, 4, 4, self.hhmm, True),

            # F14 - Estimate data
            SubFieldIdentifiers.F14a: SubFieldDescription(
                SubFieldIdentifiers.F14a, 1, 15, self.point, True),
            SubFieldIdentifiers.F14ab: SubFieldDescription(
                SubFieldIdentifiers.F14ab, 1, 1, "[/]", True),
            SubFieldIdentifiers.F14b: SubFieldDescription(
                SubFieldIdentifiers.F14b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F14c: SubFieldDescription(
                SubFieldIdentifiers.F14c, 4, 5, self.altitude, True),
            SubFieldIdentifiers.F14d: SubFieldDescription(
                SubFieldIdentifiers.F14d, 4, 5, self.altitude, False),
            SubFieldIdentifiers.F14e: SubFieldDescription(
                SubFieldIdentifiers.F14e, 1, 1, "[AB]", False),

            # F15 - Route data
            SubFieldIdentifiers.F15: SubFieldDescription(
                SubFieldIdentifiers.F15, 7, 1000, "[A-Z0-9/ \r\n\t]+", True),

            # F16 - ADES, EET and alternate Aerodromes
            SubFieldIdentifiers.F16a: SubFieldDescription(
                SubFieldIdentifiers.F16a, 4, 4, self.aerodrome, True),
            SubFieldIdentifiers.F16b: SubFieldDescription(
                SubFieldIdentifiers.F16b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F16c: SubFieldDescription(
                SubFieldIdentifiers.F16c, 4, 4, self.aerodrome, False),
            SubFieldIdentifiers.F16d: SubFieldDescription(
                SubFieldIdentifiers.F16d, 4, 4, self.aerodrome, False),

            # F17 - Arrival Aerodrome and time
            SubFieldIdentifiers.F17a: SubFieldDescription(
                SubFieldIdentifiers.F17a, 4, 4, self.aerodrome, True),
            SubFieldIdentifiers.F17b: SubFieldDescription(
                SubFieldIdentifiers.F17b, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F17c: SubFieldDescription(
                SubFieldIdentifiers.F17c, 0, 20, self.free, False),

            # F18 - Other information
            SubFieldIdentifiers.F18altn: SubFieldDescription(
                SubFieldIdentifiers.F18altn, 0, 20, self.free, False),
            SubFieldIdentifiers.F18awr: SubFieldDescription(
                SubFieldIdentifiers.F18awr, 2, 2, "R[1-9]", False),
            SubFieldIdentifiers.F18code: SubFieldDescription(
                SubFieldIdentifiers.F18code, 0, 7, "F[A-F0-9]{6}", False),
            SubFieldIdentifiers.F18com: SubFieldDescription(
                SubFieldIdentifiers.F18com, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dat: SubFieldDescription(
                SubFieldIdentifiers.F18dat, 0, 10, self.free, False),
            SubFieldIdentifiers.F18dep: SubFieldDescription(
                SubFieldIdentifiers.F18dep, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dest: SubFieldDescription(
                SubFieldIdentifiers.F18dest, 0, 15, self.free, False),
            SubFieldIdentifiers.F18dle: SubFieldDescription(
                SubFieldIdentifiers.F18dle, 0, 15, self.free, False),
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
            SubFieldIdentifiers.F18orgn: SubFieldDescription(
                SubFieldIdentifiers.F18orgn, 0, 20, self.free, False),
            SubFieldIdentifiers.F18pbn: SubFieldDescription(
                SubFieldIdentifiers.F18pbn, 0, 10, self.pbn, False),
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
            SubFieldIdentifiers.F18sur: SubFieldDescription(
                SubFieldIdentifiers.F18sur, 0, 20, self.free, False),
            SubFieldIdentifiers.F18talt: SubFieldDescription(
                SubFieldIdentifiers.F18talt, 0, 10, self.type, False),
            SubFieldIdentifiers.F18typ: SubFieldDescription(
                SubFieldIdentifiers.F18typ, 0, 10, self.type, False),

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
                SubFieldIdentifiers.F19j, 0, 4, "[LFUV]{1,4}", False),
            SubFieldIdentifiers.F19n: SubFieldDescription(
                SubFieldIdentifiers.F19n, 0, 20, self.free, False),
            SubFieldIdentifiers.F19p: SubFieldDescription(
                SubFieldIdentifiers.F19p, 0, 3, "[0-9]{1,3}", False),
            SubFieldIdentifiers.F19r: SubFieldDescription(
                SubFieldIdentifiers.F19r, 0, 3, "[UVE]{1,3}", False),
            SubFieldIdentifiers.F19s: SubFieldDescription(
                SubFieldIdentifiers.F19s, 0, 4, "[PDMJ]{1,4}", False),

            SubFieldIdentifiers.F20a: SubFieldDescription(
                SubFieldIdentifiers.F20a, 1, 100, self.free, True),
            SubFieldIdentifiers.F20b: SubFieldDescription(
                SubFieldIdentifiers.F20b, 1, 100, self.free, True),
            SubFieldIdentifiers.F20c: SubFieldDescription(
                SubFieldIdentifiers.F20c, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F20d: SubFieldDescription(
                SubFieldIdentifiers.F20d, 4, 7, self.frequency, True),
            SubFieldIdentifiers.F20e: SubFieldDescription(
                SubFieldIdentifiers.F20e, 1, 15, self.point, True),
            SubFieldIdentifiers.F20f: SubFieldDescription(
                SubFieldIdentifiers.F20f, 1, 100, self.free, True),
            SubFieldIdentifiers.F20g: SubFieldDescription(
                SubFieldIdentifiers.F20g, 1, 100, self.free, True),
            SubFieldIdentifiers.F20h: SubFieldDescription(
                SubFieldIdentifiers.F20h, 1, 100, self.free, True),
            SubFieldIdentifiers.F21a: SubFieldDescription(
                SubFieldIdentifiers.F21a, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F21b: SubFieldDescription(
                SubFieldIdentifiers.F21b, 4, 7, self.frequency, True),
            SubFieldIdentifiers.F21c: SubFieldDescription(
                SubFieldIdentifiers.F21c, 1, 15, self.point, True),
            SubFieldIdentifiers.F21d: SubFieldDescription(
                SubFieldIdentifiers.F21d, 4, 4, self.hhmm, True),
            SubFieldIdentifiers.F21e: SubFieldDescription(
                SubFieldIdentifiers.F21e, 0, 100, self.free, True),
            SubFieldIdentifiers.F21f: SubFieldDescription(
                SubFieldIdentifiers.F21f, 0, 100, self.free, True),

            # Field 80 for OLDI
            # F81a is identical to ICAO field 8b
            SubFieldIdentifiers.F80a: SubFieldDescription(
                SubFieldIdentifiers.F80a, 1, 1, self.flight_type, True),

            # Field 81 for OLDI
            SubFieldIdentifiers.F81a: SubFieldDescription(
                SubFieldIdentifiers.F81a, 1, 25,
                "(" + self.equipment_code + ")|(" + self.surveillance_class + ")", True),
            SubFieldIdentifiers.F81ab: SubFieldDescription(
                SubFieldIdentifiers.F81ab, 1, 1, "/", True),
            SubFieldIdentifiers.F81b: SubFieldDescription(
                SubFieldIdentifiers.F81b, 0, 3, self.equipment_status, True),
            SubFieldIdentifiers.F81bc: SubFieldDescription(
                SubFieldIdentifiers.F81bc, 1, 1, "/", False),
            SubFieldIdentifiers.F81c: SubFieldDescription(
                SubFieldIdentifiers.F81c, 0, 3, self.equipment_code, False),

            # Special for the MFS
            SubFieldIdentifiers.MFS_SIG_POINT: SubFieldDescription(
                SubFieldIdentifiers.MFS_SIG_POINT, 0, 15, "[A-Z][A-Z0-9]{1,14}", True),

            # Special for RQS content
            SubFieldIdentifiers.RQS_FREE_TEXT: SubFieldDescription(
                SubFieldIdentifiers.RQS_FREE_TEXT, 0, 0, self.free, True)
        }

    def get_subfield_description(self, subfield_id):
        # type: (SubFieldIdentifiers) -> SubFieldDescription | None
        """This method gets the subfield description for an ICAO subfield based on its ICAO
        subfield ID, i.e. F13a (Only the ADEP location indicator), F16ab (ADES and EET) etc.
            :param subfield_id: The subfield ID; an enum from the SubFieldIdentifiers class. Based on
                                the ICAO subfields as defined in ICAO DOC 4444.
            :return: An instance of SubFieldDescription containing a complete description
                     of a subfield including its syntax using a regular expression, or
                     None if the subfield 'icao_field_id' could not be found."""
        return self.subfield_description[subfield_id]
