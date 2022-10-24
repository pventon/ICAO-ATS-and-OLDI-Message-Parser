import unittest

from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields
from IcaoMessageParser.FlightPlanRecord import FlightPlanRecord
from IcaoMessageParser.ParseF18 import ParseF18


class TestParseF18(unittest.TestCase):

    def test_parse_f18(self):
        self.do_f18_test(True, 1, "", ["No data in field 18, expecting field 18 keyword/data"])

        self.do_f18_test(True, 1, "     ", ["No data in field 18, expecting field 18 keyword/data"])

        self.do_f18_test(True, 1, "/", ["Field 18 contains no keywords, can be '0' or 'n' "
                                        "keyword/data occurrences instead of '/'"])

        self.do_f18_test(True, 1, "  XXX  ", ["Field 18 contains no keywords, can be '0' or 'n' "
                                              "keyword/data occurrences instead of 'XXX'"])

        self.do_f18_test(False, 0, "0", [""])

        self.do_f18_test(True, 1, "   /   DEP", [
            "Field 18 contains no keywords, can be '0' or 'n' keyword/data occurrences instead of '/   DEP'"])

        self.do_f18_test(True, 1, "DEP", [
            "Field 18 contains no keywords, can be '0' or 'n' keyword/data occurrences instead of 'DEP'"])

        self.do_f18_test(True, 2, "DEP/", ["Expecting data following field 18 keyword 'DEP/'",
                                           "Expecting F18 DEP as name and location of departure aerodrome if "
                                           "ZZZZ inserted in ICAO field 13a, (only A-Z, 0-9 and spaces) "
                                           "instead of ''"])

        self.do_f18_test(True, 2, "DEP/RALT/DIDDLY TRASH ", [
            "Expecting data following field 18 keyword 'DEP/'",
            "Expecting F18 DEP as name and location of departure aerodrome if ZZZZ inserted "
            "in ICAO field 13a, (only A-Z, 0-9 and spaces) instead of ''"])

        self.do_f18_test(False, 0, "DEP/VALID DATA1 XXX ", [""])

        self.do_f18_test(True, 1, "DEP/VALID DATA2 XXX/ ", [
            "Field 18 Keyword 'XXX/' unrecognised"])

        self.do_f18_test(True, 1, "DEP/VALID DATA3 XXX/DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(False, 0, "DEP/VALID DATA4 XXX DEST/VALID DATA ", [""])

        self.do_f18_test(True, 1, "DEP/VALID DATA5 XXX/ DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/' unrecognised", ""])

        self.do_f18_test(True, 1, "DEP/VALID DATA6 XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 1, "DEP/VALID DATA7 YYY XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 2, "DEP/VALID DATA8 YYY/ XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'YYY/' unrecognised",
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(True, 2, "DEP/VALID DATA9 YYY/DATA XXX/DATA DEST/VALID DATA ", [
            "Field 18 Keyword 'YYY/DATA' unrecognised",
            "Field 18 Keyword 'XXX/DATA' unrecognised"])

        self.do_f18_test(False, 0, "RMK/REMARK 1 RMK/REMARK 2 RMK/REMARK 3", [""])

        fpr = self.do_f18_test(False, 0, "RMK/REMARK 1 RMK/REMARK 2 RMK/REMARK 3 "
                                         "STS/FFR STS/HAZMAT STS/MARSA "
                                         "RVR/200 SRC/MFS TALT/TALT DATA", [""])
        self.assertEqual("HAZMAT", fpr.get_all_icao_subfields(
            FieldIdentifiers.F18, SubFieldIdentifiers.F18sts)[1].get_field_text())
        self.assertEqual(None, fpr.get_all_icao_subfields(
            FieldIdentifiers.F18, SubFieldIdentifiers.F18typ))

        self.do_f18_test(True, 3, "DEP/HHH/GARBAGE RMK/REMARK", [
            "Expecting data following field 18 keyword 'DEP/'",
            "Field 18 Keyword 'HHH/GARBAGE' unrecognised",
            "Expecting F18 DEP as name and location of departure aerodrome if ZZZZ inserted "
            "in ICAO field 13a, (only A-Z, 0-9 and spaces) instead of ''"])

        self.do_f18_test(True, 2,
                         "/DEP/SOMETHING MORE FIELDS RALT/DIDDLY TRASH HHH/GARBAGE RMK/REMARK "
                         "DEST/A DEST FIELD RMK/SECOND RMK",
                         ["Expecting field 18 keyword/data instead of '/'",
                          "Field 18 Keyword 'HHH/GARBAGE' unrecognised"])

    def test_altn(self):
        # OK
        self.do_f18_test(False, 0, " ALTN /AN AIRPORT", [""])

        # NOK
        self.do_f18_test(True, 1, "ALTN/AN AI#RPORT",
                         ["The F18 ALTN field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'AN AI#RPORT'"])

    def test_awr(self):
        # OK
        self.do_f18_test(False, 0, " AWR/ R5", [""])
        self.do_f18_test(False, 0, " AWR/R9", [""])

        # NOK
        self.do_f18_test(True, 1, "AWR/R0",
                         ["Expecting F18 AWR as R[1-9] instead of 'R0'"])
        self.do_f18_test(True, 1, "AWR/R1 R9",
                         ["Too many F18 AWR fields, should only be one field as R[1-9] instead of 'R1 R9'"])
        self.do_f18_test(True, 1, "AWR/R3 EXTRA",
                         ["Too many F18 AWR fields, should only be one field as R[1-9] instead of 'R3 EXTRA'"])

    def test_code(self):
        # OK
        self.do_f18_test(False, 0, " CODE /F123ABF", [""])

        # NOK - Too long
        self.do_f18_test(True, 1, "CODE/F1234567",
                         ["Expecting F18 CODE as hexadecimal address with 7 HEX digits "
                          "starting at F000000 instead of 'F1234567'"])

        # NOK - Incorrect value
        self.do_f18_test(True, 1, "CODE/F123ZFF",
                         ["Expecting F18 CODE as hexadecimal address with 7 HEX digits "
                          "starting at F000000 instead of 'F123ZFF'"])

        # NOK - Too short
        self.do_f18_test(True, 1, "CODE/F123FF",
                         ["Expecting F18 CODE as hexadecimal address with 7 HEX digits "
                          "starting at F000000 instead of 'F123FF'"])

        # NOK - Extra fields
        self.do_f18_test(True, 1, "CODE/F123ABC F000000",
                         ["Too many F18 CODE fields, should only be one field  with 7 HEX "
                          "digits instead of 'F123ABC F000000'"])

    def test_com(self):
        # OK
        self.do_f18_test(False, 0, " COM /A1 B1B2", [""])

        # NOK
        self.do_f18_test(True, 1, "COM/A1*2O1",
                         ["Expecting F18 COM as communication capabilities (only A-Z, 0-9 and spaces) "
                          "not specified in ICAO field 10a instead of 'A1*2O1'"])

    def test_dat(self):
        # OK
        self.do_f18_test(False, 0, " DAT /A1 B1B2", [""])

        # NOK
        self.do_f18_test(True, 1, "DAT/A1*2O1",
                         ["Expecting F18 DAT as data application capabilities (only A-Z, 0-9 and spaces) "
                          "not specified in ICAO field 10a instead of 'A1*2O1'"])

    def test_dep(self):
        # OK
        self.do_f18_test(False, 0, " DEP /23N123W AN AIRPORT IN FOREIGN COUNTRY", [""])

        # NOK
        self.do_f18_test(True, 1, "DEP /23N123W AN AI#RPORT IN FOREIGN COUNTRY",
                         ["Expecting F18 DEP as name and location of departure aerodrome if ZZZZ "
                          "inserted in ICAO field 13a, (only A-Z, 0-9 and spaces) instead of "
                          "'23N123W AN AI#RPORT IN FOREIGN COUNTRY'"])

    def test_dest(self):
        # OK
        self.do_f18_test(False, 0, " DEST /23N123W AN AIRPORT IN FOREIGN COUNTRY", [""])

        # NOK
        self.do_f18_test(True, 1, "DEST /23N123W AN AI#RPORT IN FOREIGN COUNTRY",
                         ["Expecting F18 DEST as name and location of destination aerodrome "
                          "if ZZZZ inserted in ICAO field 16a, (only A-Z, 0-9 and spaces) instead "
                          "of '23N123W AN AI#RPORT IN FOREIGN COUNTRY'"])

    def test_dle(self):
        # OK
        self.do_f18_test(False, 0, " DLE /PNT1230", [""])

        # OK
        self.do_f18_test(False, 0, " DLE /23N123W1231", [""])

        # OK
        self.do_f18_test(False, 0, " DLE /2323N12359W1232", [""])

        # OK
        self.do_f18_test(False, 0, " DLE /PNT3001001233", [""])

        # OK
        self.do_f18_test(True, 1, " DLE /T1230", [
            "Expected F18 DLE as 'point HHMM' instead of 'T1230', (can be any kind of point)"])

        # NOK Point incorrect
        self.do_f18_test(True, 1, "DLE /23N181W1234", [
            "Expected F18 DLE point as a PRP, Latitude/Longitude (with or without minutes) "
            "or bearing distance instead of '23N181W'"])

        # NOK Point incorrect
        self.do_f18_test(True, 1, "DLE /GOL#A1234", [
            "Expected F18 DLE point as a PRP, Latitude/Longitude (with or without minutes) "
            "or bearing distance instead of 'GOL#A'"])

        # NOK Time incorrect
        self.do_f18_test(True, 1, "DLE /GOLVA1260", [
            "Expected F18 DLE time in HHMM format instead of '1260'"])

        # NOK Too many fields
        self.do_f18_test(True, 1, "DLE /LNZ1234 EXTRA", [
            "Too many fields in F18 DLE, expecting single field as point & time instead of 'LNZ1234 EXTRA'", "", ""])

    def test_dof(self):
        # OK
        self.do_f18_test(False, 0, " DOF /221225", [""])

        # OK
        self.do_f18_test(False, 0, " DOF /200229", [""])

        # NOK
        self.do_f18_test(True, 1, "DOF /220229",
                         ["Expecting DOF in the format YYMMDD instead of '220229'"])

        self.do_f18_test(True, 1, "DOF /220631",
                         ["Expecting DOF in the format YYMMDD instead of '220631'"])

        self.do_f18_test(True, 1, "DOF /22022#",
                         ["Expecting DOF in the format YYMMDD instead of '22022#'"])

        self.do_f18_test(True, 1, "DOF /220229 220123",
                         ["Expecting DOF in the format YYMMDD instead of '220229 220123'"])

    def test_eet(self):
        # OK
        self.do_f18_test(False, 0, " EET / AAA0100", [""])
        self.do_f18_test(False, 0, " EET / AAA0100 BBB0200", [""])
        self.do_f18_test(False, 0, " EET / AAA0100 BBB0300 CCCCC0400", [""])
        self.do_f18_test(False, 0, " EET / AAA0100 BBB0300 CCCCC0400 DDD0500", [""])
        self.do_f18_test(False, 0, " EET / AAA0100 BBB0300 CCCCC0400 DDD0500 EEE0600", [""])

        # Error in 3rd time field
        self.do_f18_test(True, 1, " EET / AAA0100 BBB0300 CCCCC0460 DDD0500 EEE0600", [
            "Expected F18 EET time in HHMM format instead of '0460'"])

        # Error in 3rd point field
        self.do_f18_test(True, 1, " EET / AAA0100 BBB0300 CC#CC0450 DDD0500 EEE0600", [
            "Expected F18 EET point as a PRP, Latitude/Longitude (with or without minutes) or "
            "bearing distance instead of 'CC#CC'"])

    def test_ifp(self):
        # OK
        self.do_f18_test(False, 0, "IFP/ERROUTRAD", [""])
        self.do_f18_test(False, 0, "IFP/ERROUTWE", [""])
        self.do_f18_test(False, 0, "IFP/ERROUTE", [""])
        self.do_f18_test(False, 0, "IFP/ERRTYPE", [""])
        self.do_f18_test(False, 0, "IFP/ERRLEVEL", [""])
        self.do_f18_test(False, 0, "IFP/ERREOBT", [""])
        self.do_f18_test(False, 0, "IFP/NON833", [""])
        self.do_f18_test(False, 0, "IFP/833UNKNOWN", [""])
        self.do_f18_test(False, 0, "IFP/MODESASP", [""])
        self.do_f18_test(False, 0, "IFP/RVSMVIOLATION", [""])
        self.do_f18_test(False, 0, "IFP/NONRVSM", [""])
        self.do_f18_test(False, 0, "IFP/RVSMUNKNOWN", [""])
        self.do_f18_test(False, 0, "IFP/ERROUTRAD ERROUTWE ERROUTE ERRTYPE ERRLEVEL ERREOBT NON833 "
                                   "833UNKNOWN MODESASP RVSMVIOLATION NONRVSM RVSMUNKNOWN", [""])

        # NOK
        self.do_f18_test(True, 1, "IFP/ERROUTRAD ERROUTWE ERROUTE ERRTYPE ERRLEVEL ERREOBT NON833 "
                                  "833UNKNOWN MODESASP #RVSMVIOLATION NONRVSM RVSMUNKNOWN",
                         ["Expecting F18 IFP as 'ERROUTRAD', 'ERROUTWE', 'ERROUTE', 'ERRTYPE', 'ERRLEVEL', "
                          "'ERREOBT', 'NON833', '833UNKNOWN', 'MODESASP', 'RVSMVIOLATION', 'NONRVSM' or "
                          "'RVSMUNKNOWN' instead of '#RVSMVIOLATION'"])

    def test_nav(self):
        # OK
        self.do_f18_test(False, 0, " NAV /SOME NAV DATA", [""])

        # NOK
        self.do_f18_test(True, 1, "NAV /SOME NAV #DATA",
                         ["Expecting F18 NAV as significant navigation equipment as one or more space "
                          "separated designators, (only A-Z, 0-9 and spaces) instead of 'SOME NAV #DATA'"])

    def test_opr(self):
        # OK
        self.do_f18_test(False, 0, " OPR /AIRLINE AGENCY", [""])

        # NOK
        self.do_f18_test(True, 1, "OPR /AIRLINE #AGENCY",
                         ["Expecting F18 OPR as name of aircraft operating agency, (only A-Z, 0-9 "
                          "and spaces) instead of 'AIRLINE #AGENCY'"])

    def test_orgn(self):
        # OK
        self.do_f18_test(False, 0, " ORGN /ABCDEFGH", [""])
        self.do_f18_test(False, 0, " ORGN /ABCDE3H", [""])

        # NOK
        self.do_f18_test(True, 1, "ORGN /ABCDEF#GH",
                         ["Expected F18 ORGN as an 8 or 7 character facility address instead of 'ABCDEF#GH'"])
        self.do_f18_test(True, 1, "ORGN /ABCDEFGH DEFGRTHJ",
                         ["Too many fields in F18 ORGN, expecting single field as facility address instead "
                          "of 'ABCDEFGH DEFGRTHJ'"])

    def test_pbn(self):
        # OK
        self.do_f18_test(False, 0, " PBN / A1", [""])
        self.do_f18_test(False, 0, " PBN/   A1B1", [""])
        self.do_f18_test(False, 0, " PBN/A1B2C1", [""])
        self.do_f18_test(False, 0, " PBN/A1B3C2D1 ", [""])
        self.do_f18_test(False, 0, " PBN/A1B4C3D2L1", [""])
        self.do_f18_test(False, 0, " PBN/A1B5C4D3L1O1", [""])
        self.do_f18_test(False, 0, " PBN/A1B6C3D4L1O2S1", [""])
        self.do_f18_test(False, 0, " PBN/A1B2C3D4L1O4S2T1", [""])

        # NOK
        self.do_f18_test(True, 1, "PBN / A1 B2",
                         ["The F18 PBN field should be a single field instead of ' A1 B2'"])
        self.do_f18_test(True, 1, "PBN / A2",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A2'"])
        self.do_f18_test(True, 1, "PBN / A1B7",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B7'"])
        self.do_f18_test(True, 1, "PBN / A1B5C5",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B5C5'"])
        self.do_f18_test(True, 1, "PBN / A1B4C4D5",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B4C4D5'"])
        self.do_f18_test(True, 1, "PBN / A1B3C3D4L2",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B3C3D4L2'"])
        self.do_f18_test(True, 1, "PBN / A1B2C2D3L1O5",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B2C2D3L1O5'"])
        self.do_f18_test(True, 1, "PBN / A1B1C1D2L1O4S3",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B1C1D2L1O4S3'"])
        self.do_f18_test(True, 1, "PBN / A1B1C1D1L1O3S2T3",
                         ["F18 PBN syntax incorrect, expecting 1 to 8 of either A1, B1-B6, C1-C4, D1-D4, "
                          "L1, O1-O4, S1, S2, T1 or T2 instead of ' A1B1C1D1L1O3S2T3'"])
        self.do_f18_test(True, 1, "PBN / A1B1C1D1L1O3S2T2 A1",
                         ["The F18 PBN field should be a single field instead of ' A1B1C1D1L1O3S2T2 A1'"])
        self.do_f18_test(True, 1, "PBN / A1B1C1D1 L1O3S2T1",
                         ["The F18 PBN field should be a single field instead of ' A1B1C1D1 L1O3S2T1'"])

    def test_per(self):
        # OK
        self.do_f18_test(False, 0, " PER /A", [""])
        self.do_f18_test(False, 0, " PER /  E ", [""])

        # NOK
        self.do_f18_test(True, 1, "PER / 9",
                         ["F18 PER syntax incorrect, expecting a single character A to Z instead of ' 9'"])
        self.do_f18_test(True, 1, "PER / FG",
                         ["F18 PER syntax incorrect, expecting a single character A to Z instead of ' FG'"])
        self.do_f18_test(True, 1, "PER /G J",
                         ["The F18 PER field should be a single field instead of 'G J'"])

    def test_ralt(self):
        # OK
        self.do_f18_test(False, 0, " RALT/ GOLF COURSE 23N123W", [""])

        # NOK
        self.do_f18_test(True, 1, "RALT/GOLF #COURSE 23N123W",
                         ["Expecting F18 RALT as location indicator, alternate arrival aerodrome name or location as "
                          "a latitude/longitude, (only A-Z, 0-9 and spaces) instead of 'GOLF #COURSE 23N123W'"])

    def test_reg(self):
        # OK
        self.do_f18_test(False, 0, " REG/ BRITISH A234", [""])

        # NOK
        self.do_f18_test(True, 1, "REG/ BRIT#ISH A234",
                         ["Expecting F18 REG as nationality or mark and aircraft registration (only A-Z, "
                          "0-9 and spaces) instead of ' BRIT#ISH A234'"])

    def test_rfp(self):
        # OK
        self.do_f18_test(False, 0, " RFP/ Q5", [""])
        self.do_f18_test(False, 0, " RFP/Q9", [""])

        # NOK
        self.do_f18_test(True, 1, "RFP/Q0",
                         ["Expecting F18 RIF as Q[1-9] instead of 'Q0'"])
        self.do_f18_test(True, 1, "RFP/Q1 Q9",
                         ["Too many F18 RIF fields, should only be one field as Q[1-9] instead of 'Q1 Q9'"])
        self.do_f18_test(True, 1, "RFP/Q3 EXTRA",
                         ["Too many F18 RIF fields, should only be one field as Q[1-9] instead of 'Q3 EXTRA'"])

    def test_rif(self):
        # OK
        self.do_f18_test(False, 0, " RIF/ DTA HEC KLAX", [""])
        self.do_f18_test(False, 0, " RIF/ESP G94 CLA YPPH", [""])

        # NOK
        self.do_f18_test(True, 1, "RIF/ESP G94 CLA #YPPH",
                         ["Expecting F18 RIF revised route to destination aerodrome, (only A-Z, 0-9 and spaces) "
                          "instead of 'ESP G94 CLA #YPPH'"])

    def test_rmk(self):
        # OK
        self.do_f18_test(False, 0, "RMK/   THIS IS A REMARK", [""])
        self.do_f18_test(False, 0, "   RMK/ THIS IS A REMARK, WITH NUMBERS 456 AND PUNCTUATION .:;", [""])

        # NOK
        self.do_f18_test(True, 1, "RMK/ THIS IS A REMARK, WI%TH NUMBERS 456 AND PUNCTUATION .:;",
                         ["The F18 RMK field must only contain characters A-Z, 0-9, '.', ':', ';' and "
                          "',' instead of ' THIS IS A REMARK, WI%TH NUMBERS 456 AND PUNCTUATION .:;'"])

    def test_rvr(self):
        # OK
        self.do_f18_test(False, 0, "RVR/  1", [""])
        self.do_f18_test(False, 0, "  RVR/ 40", [""])
        self.do_f18_test(False, 0, "  RVR/ 999", [""])

        # NOK
        self.do_f18_test(True, 1, "RVR/123 345",
                         ["Too many F18 RVR fields, should only be one field as 1 to 3 digit number "
                          "instead of '123 345'"])

        self.do_f18_test(True, 1, "RVR/1233",
                         ["Expecting F18 RVR as 1 to 3 digit number instead of '1233'"])

    def test_sel(self):
        # OK
        self.do_f18_test(False, 0, "SEL/  ABCD", [""])
        self.do_f18_test(False, 0, "  SEL/ ABCDE", [""])

        # NOK
        self.do_f18_test(True, 1, "SEL/ABCD ABCD",
                         ["Too many F18 SEL fields, should only be one field as 4 to 5 alpha "
                          "characters instead of 'ABCD ABCD'"])

        self.do_f18_test(True, 1, "SEL/ABCDEF",
                         ["Expecting F18 SEL as 4 to 5 alpha characters instead of 'ABCDEF'"])

    def test_stayinfo(self):
        # OK
        self.do_f18_test(False, 0, " STAYINFO1 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO2 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO3 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO4 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO5 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO6 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO7 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO8 /STAY INFORMATION", [""])
        self.do_f18_test(False, 0, " STAYINFO9 /STAY INFORMATION", [""])

        # NOK
        self.do_f18_test(True, 1, "STAYINFO1/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO2/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO3/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO4/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO5/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO6/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO7/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO8/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])
        self.do_f18_test(True, 1, "STAYINFO9/STAY ^INFORMATION",
                         ["The F18 STAYINFO field contains illegal characters, only A-Z, "
                          "0-9 and spaces allowed instead of 'STAY ^INFORMATION'"])

    def test_sts(self):
        # OK
        self.do_f18_test(False, 0, "STS/  ALTRV", [""])
        self.do_f18_test(False, 0, "STS/  ATFMX", [""])
        self.do_f18_test(False, 0, "STS/  FFR", [""])
        self.do_f18_test(False, 0, "STS/  FLTCK", [""])
        self.do_f18_test(False, 0, "STS/  HAZMAT", [""])
        self.do_f18_test(False, 0, "STS/  HEAD", [""])
        self.do_f18_test(False, 0, "STS/  HOSP", [""])
        self.do_f18_test(False, 0, "STS/  HUM", [""])
        self.do_f18_test(False, 0, "STS/  MARSA", [""])
        self.do_f18_test(False, 0, "STS/  MEDEVAC", [""])
        self.do_f18_test(False, 0, "STS/  NONRVSM", [""])
        self.do_f18_test(False, 0, "STS/  SAR", [""])
        self.do_f18_test(False, 0, "STS/  STATE", [""])
        self.do_f18_test(False, 0, "STS/  STATE SAR", [""])
        self.do_f18_test(False, 0, "STS/MEDEVAC HUM HAZMAT MARSA", [""])

        # NOK
        self.do_f18_test(True, 1, "STS/ABCD",
                         ["Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', "
                          "'HOSP', 'HUM', 'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of 'ABCD'"])

        self.do_f18_test(True, 1, "STS/MEDEVAC HUM HAZMAT UNKNOWN MARSA", [
            "Expecting F18 STS as 'ALTRV', 'ATFMX', 'FFR', 'FLTCK', 'HAZMAT', 'HEAD', 'HOSP', 'HUM', "
            "'MARSA', 'MEDEVAC', 'NONRVSM', 'SAR' or 'STATE' instead of 'UNKNOWN'"])

    def test_src(self):
        # OK
        self.do_f18_test(False, 0, "SRC/  RPL", [""])
        self.do_f18_test(False, 0, "SRC/  FPL", [""])
        self.do_f18_test(False, 0, "SRC/  MFS", [""])
        self.do_f18_test(False, 0, "SRC/  FNM", [""])
        self.do_f18_test(False, 0, "SRC/  RQP", [""])
        self.do_f18_test(False, 0, "SRC/  AFP", [""])
        self.do_f18_test(False, 0, "SRC/  DIV", [""])
        self.do_f18_test(False, 0, "SRC/  AFIL", [""])
        self.do_f18_test(False, 0, "SRC/  ZZZZ", [""])
        self.do_f18_test(False, 0, "SRC/  LOWW", [""])

        # NOK
        self.do_f18_test(True, 1, "SRC/ABCDE",
                         ["Expecting F18 SRC as 'RPL', 'FPL', 'AFIL', 'MFS', 'FNM', 'RQP', 'AFP', 'DIV' or a "
                          "4 character location indicator instead of 'ABCDE'"])

        self.do_f18_test(True, 1, "SRC/RQP AFIL",
                         ["Too many F18 SRC fields, should only be one field as 'RPL', 'FPL', 'AFIL', 'MFS', "
                          "'FNM', 'RQP', 'AFP', 'DIV' or a 4 character location instead of 'RQP AFIL'"])

    def test_sur(self):
        # OK
        self.do_f18_test(False, 0, " SUR/ SURVEILLANCE CAPABILITIES", [""])

        # NOK
        self.do_f18_test(True, 1, "SUR/ SURVEILLANCE# CAPABILITIES",
                         ["The F18 SUR field should contain surveillance application capabilities "
                          "using characters A-Z, 0-9 instead of ' SURVEILLANCE# CAPABILITIES'"])

    def test_talt(self):
        # OK
        self.do_f18_test(False, 0, " TALT/ GOLF COURSE 23N123W", [""])

        # NOK
        self.do_f18_test(True, 1, "TALT/GOLF #COURSE 23N123W",
                         ["Expecting F18 TALT as location indicator, alternate departure aerodrome name or "
                          "location as a latitude/longitude, (only A-Z, 0-9 and spaces) instead of "
                          "'GOLF #COURSE 23N123W'"])

    def test_typ(self):
        # OK
        self.do_f18_test(False, 0, " TYP/ B737", [""])
        self.do_f18_test(False, 0, " TYP/ 1B737", [""])
        self.do_f18_test(False, 0, " TYP/ 10B737", [""])
        self.do_f18_test(False, 0, " TYP/ B737 3A320 C172", [""])

        # NOK
        self.do_f18_test(True, 1, "TYP/B737777",
                         ["Expecting number (optional) and type of aircraft instead of 'B737777'"])
        self.do_f18_test(True, 1, "TYP/100B737",
                         ["Expecting number (optional) and type of aircraft instead of '100B737'"])
        self.do_f18_test(True, 1, " TYP/ B737 3A320000 C172",
                         ["Expecting number (optional) and type of aircraft instead of '3A320000'"])

    def do_f18_test(self, errors_detected, number_of_errors, string_to_parse, expected_error_text):
        # type: (bool, int, str, [str]) -> FlightPlanRecord
        fpr = FlightPlanRecord()
        fpr.add_icao_field(FieldIdentifiers.F18, string_to_parse, 0, len(string_to_parse))
        pf18 = ParseF18(fpr, SubFieldsInFields(), SubFieldDescriptions())
        pf18.parse_field()
        # print("In the test: str(errors_detected) + ", " + str(number_of_errors))
        self.assertEqual(errors_detected, fpr.errors_detected())
        self.assertEqual(number_of_errors, len(fpr.get_erroneous_fields()))
        if errors_detected:
            for i in range(0, number_of_errors):
                self.assertEqual(expected_error_text[i], fpr.get_erroneous_fields()[i].get_error_message())
        return fpr


if __name__ == '__main__':
    unittest.main()
