from Configuration.EnumerationConstants import FieldIdentifiers, SubFieldIdentifiers, ErrorId


class SubFieldsInFields:
    """This class describes the subfield content of each ICAO and OLDI field supported by this
    message parser.

    The description consists of listing the ICAO subfields / ID for each ICAO field defined by this parser.
    The ICAO subfield IDs are provided by the enumeration values in the SubFieldIdentifiers class. Many of
    the ICAO subfield IDs translate directly to those specified in ICAO DOC 4444; however, due to support
    for OLDI messages as well as some IFPS Oceanic message, some field identifiers are what could be called
    custom.

    The result is the same, all subfields for a given ICAO field can be obtained from this class. The data
    is stored in a dictionary; the key is an enumeration from the FieldIdentifiers class with the subfields
    stored in a list of SubFieldIdentifiers enumerations and associated with their respective ICAO fields.

    For each ICAO field declaration, a list of error message identifiers are also stored; these errors will
    be used by the parser when looping over the subfields in a field to parse each individual subfield."""

    field_content_description = {}
    """A dictionary containing a description of an ICAO field's subfields.
    # For example, ICAO F16 comprises an ADES given as a location indicator and a time field."""

    def __init__(self):
        # type: () -> None
        self.field_content_description = {
            # Message Header fields
            FieldIdentifiers.PRIORITY_INDICATOR: [[SubFieldIdentifiers.PRIORITY_INDICATOR],
                                                  [ErrorId.PRIORITY_SYNTAX, ErrorId.PRIORITY_TOO_MANY_FIELDS,
                                                   ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.PRIORITY_MISSING]],
            FieldIdentifiers.FILING_TIME: [[SubFieldIdentifiers.FILING_TIME],
                                           [ErrorId.FILING_TIME_SYNTAX, ErrorId.FILING_TIME_TOO_MANY_FIELDS,
                                            ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.FILING_TIME_MISSING]],
            FieldIdentifiers.ORIGINATOR: [[SubFieldIdentifiers.ORIGINATOR],
                                          [ErrorId.ORIGINATOR_SYNTAX, ErrorId.ORIGINATOR_TOO_MANY_FIELDS,
                                           ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.ORIGINATOR_MISSING]],
            FieldIdentifiers.ADDRESS: [[SubFieldIdentifiers.ADDRESS1, SubFieldIdentifiers.ADDRESS2,
                                        SubFieldIdentifiers.ADDRESS3, SubFieldIdentifiers.ADDRESS4,
                                        SubFieldIdentifiers.ADDRESS5, SubFieldIdentifiers.ADDRESS6,
                                        SubFieldIdentifiers.ADDRESS7, SubFieldIdentifiers.ADDRESS8],
                                       [ErrorId.ADDRESSEE_SYNTAX, ErrorId.ADDRESSEE_SYNTAX,
                                        ErrorId.ADDRESSEE_SYNTAX, ErrorId.ADDRESSEE_SYNTAX,
                                        ErrorId.ADDRESSEE_SYNTAX, ErrorId.ADDRESSEE_SYNTAX,
                                        ErrorId.ADDRESSEE_SYNTAX, ErrorId.ADDRESSEE_SYNTAX,
                                        ErrorId.ADDRESSEE_TOO_MANY_FIELDS,
                                        ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.ADDRESSEE_MISSING]],
            FieldIdentifiers.ADADDRESS: [[SubFieldIdentifiers.ADADDRESS1, SubFieldIdentifiers.ADADDRESS2,
                                          SubFieldIdentifiers.ADADDRESS3, SubFieldIdentifiers.ADADDRESS4,
                                          SubFieldIdentifiers.ADADDRESS5, SubFieldIdentifiers.ADADDRESS6,
                                          SubFieldIdentifiers.ADADDRESS7, SubFieldIdentifiers.ADADDRESS8],
                                         [ErrorId.AD_ADDRESSEE_SYNTAX, ErrorId.AD_ADDRESSEE_SYNTAX,
                                          ErrorId.AD_ADDRESSEE_SYNTAX, ErrorId.AD_ADDRESSEE_SYNTAX,
                                          ErrorId.AD_ADDRESSEE_SYNTAX, ErrorId.AD_ADDRESSEE_SYNTAX,
                                          ErrorId.AD_ADDRESSEE_SYNTAX, ErrorId.AD_ADDRESSEE_SYNTAX,
                                          ErrorId.AD_ADDRESSEE_TOO_MANY_FIELDS,
                                          ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.AD_ADDRESSEE_MISSING]],

            # ICAO fields
            FieldIdentifiers.F3: [[SubFieldIdentifiers.F3a, SubFieldIdentifiers.F3b1, SubFieldIdentifiers.F3b2,
                                   SubFieldIdentifiers.F3b3, SubFieldIdentifiers.F3b4, SubFieldIdentifiers.F3c1,
                                   SubFieldIdentifiers.F3c2, SubFieldIdentifiers.F3c3, SubFieldIdentifiers.F3c4],
                                  [ErrorId.F3_TITLE_SYNTAX, ErrorId.F3_TX_SYNTAX, ErrorId.FLD_SLASH_SYNTAX,
                                   ErrorId.F3_RX_SYNTAX, ErrorId.F3_SEQ_SYNTAX, ErrorId.F3_TX_SYNTAX,
                                   ErrorId.FLD_SLASH_SYNTAX, ErrorId.F3_RX_SYNTAX, ErrorId.F3_SEQ_SYNTAX,
                                   ErrorId.F3_TOO_MANY_FIELDS, ErrorId.F3_RX_TX_EXPECTED, ErrorId.F3_TITLE_MISSING]],
            FieldIdentifiers.F5: [[SubFieldIdentifiers.F5a, SubFieldIdentifiers.F5ab, SubFieldIdentifiers.F5b,
                                   SubFieldIdentifiers.F5bc, SubFieldIdentifiers.F5c],
                                  [ErrorId.F5_F5A_SYNTAX, ErrorId.F5_F5AB_EXPECTING_SLASH, ErrorId.F5_F5B_SYNTAX,
                                   ErrorId.F5_F5BC_EXPECTING_SLASH, ErrorId.F5_F5C_SYNTAX, ErrorId.F5_TOO_MANY_FIELDS,
                                   ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F5_MISSING]],
            FieldIdentifiers.F7: [[SubFieldIdentifiers.F7a, SubFieldIdentifiers.F7ab, SubFieldIdentifiers.F7b,
                                   SubFieldIdentifiers.F7c],
                                  [ErrorId.F7_F7A_SYNTAX, ErrorId.F7_F7AB_SYNTAX, ErrorId.F7_F7B_SYNTAX,
                                   ErrorId.F7_F7C_SYNTAX, ErrorId.F7_TOO_MANY_FIELDS,
                                   ErrorId.F7_MORE_SUBFIELDS_EXPECTED, ErrorId.F7_MISSING]],
            FieldIdentifiers.F8: [[SubFieldIdentifiers.F8a, SubFieldIdentifiers.F8b],
                                  [ErrorId.F8_F8A_SYNTAX, ErrorId.F8_F8B_SYNTAX,
                                   ErrorId.F8_TOO_MANY_FIELDS,
                                   ErrorId.F8_MORE_SUBFIELDS_EXPECTED, ErrorId.F8_MISSING]],
            FieldIdentifiers.F8a: [[SubFieldIdentifiers.F8a],
                                   [ErrorId.F8_F8A_SYNTAX, ErrorId.F8_TOO_MANY_FIELDS,
                                    ErrorId.F8_MORE_SUBFIELDS_EXPECTED, ErrorId.F8_MISSING]],
            FieldIdentifiers.F9: [[SubFieldIdentifiers.F9a, SubFieldIdentifiers.F9b, SubFieldIdentifiers.F9bc,
                                   SubFieldIdentifiers.F9c],
                                  [ErrorId.F9_F9A_SYNTAX, ErrorId.F9_F9B_SYNTAX, ErrorId.F9_F9BC_SYNTAX,
                                   ErrorId.F9_F9C_SYNTAX, ErrorId.F9_TOO_MANY_FIELDS,
                                   ErrorId.F9_MORE_SUBFIELDS_EXPECTED, ErrorId.F9_MISSING]],
            FieldIdentifiers.F10: [[SubFieldIdentifiers.F10a, SubFieldIdentifiers.F10ab, SubFieldIdentifiers.F10b],
                                   [ErrorId.F10_F10A_SYNTAX, ErrorId.F10_F10AB_SYNTAX, ErrorId.F10_F10B_SYNTAX,
                                    ErrorId.F10_TOO_MANY_FIELDS,
                                    ErrorId.F10_MORE_SUBFIELDS_EXPECTED, ErrorId.F10_MISSING]],
            FieldIdentifiers.F13: [[SubFieldIdentifiers.F13a, SubFieldIdentifiers.F13b],
                                   [ErrorId.F13_F13A_SYNTAX, ErrorId.F13_F13B_SYNTAX,
                                    ErrorId.F13_TOO_MANY_FIELDS,
                                    ErrorId.F13_MORE_SUBFIELDS_EXPECTED, ErrorId.F13_MISSING]],
            FieldIdentifiers.F13a: [[SubFieldIdentifiers.F13a],
                                    [ErrorId.F13_F13A_SYNTAX, ErrorId.F13_TOO_MANY_FIELDS,
                                     ErrorId.F13_MORE_SUBFIELDS_EXPECTED, ErrorId.F13_MISSING]],
            FieldIdentifiers.F14: [[SubFieldIdentifiers.F14a, SubFieldIdentifiers.F14ab, SubFieldIdentifiers.F14b,
                                    SubFieldIdentifiers.F14c, SubFieldIdentifiers.F14d, SubFieldIdentifiers.F14e],
                                   [ErrorId.F14_F14A_SYNTAX, ErrorId.F14_F14AB_SYNTAX, ErrorId.F14_F14B_SYNTAX,
                                    ErrorId.F14_F14C_SYNTAX, ErrorId.F14_F14D_SYNTAX, ErrorId.F14_F14E_SYNTAX,
                                    ErrorId.F14_TOO_MANY_FIELDS,
                                    ErrorId.F14_MORE_FIELDS_EXPECTED, ErrorId.F14_MISSING]],
            FieldIdentifiers.F14a: [[SubFieldIdentifiers.F14a],
                                    [ErrorId.F14_F14A_SYNTAX, ErrorId.F14_TOO_MANY_FIELDS,
                                     ErrorId.F14_MORE_FIELDS_EXPECTED, ErrorId.F14_MISSING]],
            # Field 15 has its own dedicated parser
            FieldIdentifiers.F15: [[SubFieldIdentifiers.F15], []],
            FieldIdentifiers.F16: [[SubFieldIdentifiers.F16a, SubFieldIdentifiers.F16b, SubFieldIdentifiers.F16c,
                                    SubFieldIdentifiers.F16d],
                                   [ErrorId.F16_F16A_SYNTAX, ErrorId.F16_F16B_SYNTAX,
                                    ErrorId.F16_F16C_SYNTAX, ErrorId.F16_F16D_SYNTAX,
                                    ErrorId.F16_TOO_MANY_FIELDS,
                                    ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F16_MISSING]],
            FieldIdentifiers.F16a: [[SubFieldIdentifiers.F16a],
                                    [ErrorId.F16_F16A_SYNTAX, ErrorId.F16_TOO_MANY_FIELDS,
                                     ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F16_MISSING]],
            FieldIdentifiers.F16ab: [[SubFieldIdentifiers.F16a, SubFieldIdentifiers.F16b],
                                     [ErrorId.F16_F16A_SYNTAX, ErrorId.F16_F16B_SYNTAX,
                                      ErrorId.F16_TOO_MANY_FIELDS,
                                      ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F16_MISSING]],
            FieldIdentifiers.F16abc: [[SubFieldIdentifiers.F16a, SubFieldIdentifiers.F16b, SubFieldIdentifiers.F16c],
                                      [ErrorId.F16_F16A_SYNTAX, ErrorId.F16_F16B_SYNTAX,
                                       ErrorId.F16_F16C_SYNTAX,
                                       ErrorId.F16_TOO_MANY_FIELDS,
                                       ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F16_MISSING]],
            FieldIdentifiers.F17: [[SubFieldIdentifiers.F17a, SubFieldIdentifiers.F17b, SubFieldIdentifiers.F17c],
                                   [ErrorId.F17_F17A_SYNTAX, ErrorId.F17_F17B_SYNTAX,
                                    ErrorId.F17_F17C_SYNTAX, ErrorId.F17_TOO_MANY_FIELDS,
                                    ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F17_MISSING]],

            # TODO F18 Individual field parsing has to be implemented for this field.
            # TODO F18 The fields are all present in the FPR as of this implementation.
            FieldIdentifiers.F18: [
                [SubFieldIdentifiers.F18altn, SubFieldIdentifiers.F18code, SubFieldIdentifiers.F18com,
                 SubFieldIdentifiers.F18dat, SubFieldIdentifiers.F18dep, SubFieldIdentifiers.F18dest,
                 SubFieldIdentifiers.F18dof, SubFieldIdentifiers.F18dle, SubFieldIdentifiers.F18eet,
                 SubFieldIdentifiers.F18est, SubFieldIdentifiers.F18ifp, SubFieldIdentifiers.F18nav,
                 SubFieldIdentifiers.F18opr, SubFieldIdentifiers.F18orgn, SubFieldIdentifiers.F18pbn,
                 SubFieldIdentifiers.F18per, SubFieldIdentifiers.F18ralt, SubFieldIdentifiers.F18reg,
                 SubFieldIdentifiers.F18rif, SubFieldIdentifiers.F18rfp, SubFieldIdentifiers.F18rmk,
                 SubFieldIdentifiers.F18rvr, SubFieldIdentifiers.F18sel, SubFieldIdentifiers.F18sts,
                 SubFieldIdentifiers.F18sur, SubFieldIdentifiers.F18src, SubFieldIdentifiers.F18talt,
                 SubFieldIdentifiers.F18typ],
                []],

            # F18_DOF - For single DOF used on many messages without a complete F18
            FieldIdentifiers.F18_DOF: [[SubFieldIdentifiers.F18dof],
                                       [ErrorId.F18_DOF_F18A_SYNTAX, ErrorId.F18_DOF_TOO_MANY_FIELDS,
                                        ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F18_DOF_MISSING]],

            # MFS message significant point, has different point syntax to normal ICAO points
            FieldIdentifiers.MFS_SIG_POINT: [[SubFieldIdentifiers.MFS_SIG_POINT],
                                             [ErrorId.MFS_POINT_SYNTAX, ErrorId.MFS_POINT_TOO_MANY_FIELDS,
                                              ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.MFS_POINT_MISSING]],

            # TODO F19 Individual field parsing has to be implemented for this field.
            # TODO F19 The fields are all present in the FPR as of this implementation.
            FieldIdentifiers.F19: [[SubFieldIdentifiers.F19a, SubFieldIdentifiers.F19c, SubFieldIdentifiers.F19d,
                                    SubFieldIdentifiers.F19e, SubFieldIdentifiers.F19j, SubFieldIdentifiers.F19n,
                                    SubFieldIdentifiers.F19p, SubFieldIdentifiers.F19r, SubFieldIdentifiers.F19s],
                                   []],

            # Field 20 parsing rules
            FieldIdentifiers.F20: [[SubFieldIdentifiers.F20a, SubFieldIdentifiers.F20b,
                                    SubFieldIdentifiers.F20c, SubFieldIdentifiers.F20d,
                                    SubFieldIdentifiers.F20e, SubFieldIdentifiers.F20f,
                                    SubFieldIdentifiers.F20g, SubFieldIdentifiers.F20h],
                                   [ErrorId.F20_F20A_SYNTAX, ErrorId.F20_F20B_SYNTAX,
                                    ErrorId.F20_F20C_SYNTAX, ErrorId.F20_F20D_SYNTAX,
                                    ErrorId.F20_F20E_SYNTAX, ErrorId.F20_F20F_SYNTAX,
                                    ErrorId.F20_F20G_SYNTAX, ErrorId.F20_F20H_SYNTAX,
                                    ErrorId.F20_TOO_MANY_FIELDS,
                                    ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F20_MISSING]],

            # Field 21 parsing rules
            FieldIdentifiers.F21: [[SubFieldIdentifiers.F21a, SubFieldIdentifiers.F21b,
                                    SubFieldIdentifiers.F21c, SubFieldIdentifiers.F21d,
                                    SubFieldIdentifiers.F21e, SubFieldIdentifiers.F21f],
                                   [ErrorId.F21_F21A_SYNTAX, ErrorId.F21_F21B_SYNTAX,
                                    ErrorId.F21_F21C_SYNTAX, ErrorId.F21_F21D_SYNTAX,
                                    ErrorId.F21_F21E_SYNTAX, ErrorId.F21_F21F_SYNTAX,
                                    ErrorId. F21_TOO_MANY_FIELDS,
                                    ErrorId.FLD_MORE_SUBFIELDS_EXPECTED, ErrorId.F21_MISSING]],

            # TODO F22 Individual field parsing has to be implemented for this field.
            # TODO F22 The fields are all present in the FPR as of this implementation.
            FieldIdentifiers.F22: [[SubFieldIdentifiers.F22_f3],
                                   []],
            FieldIdentifiers.F22_SPECIFIC: [[SubFieldIdentifiers.F22_f3],
                                            []],

            # TODO Special for OLDI
            # TODO - Have to figure out the exact content for the OLDI F80 & F81
            # TODO it appears that F80 & F81 are custom F22 fields, these definition will
            # TODO will be reviewed once the F22 implementation is done
            FieldIdentifiers.F80: [[SubFieldIdentifiers.F80a, SubFieldIdentifiers.F80b],
                                   []],
            FieldIdentifiers.F81: [[SubFieldIdentifiers.F81a, SubFieldIdentifiers.F81b],
                                   []],
        }

    def get_field_content_description(self, icao_field_id):
        # type: (FieldIdentifiers) -> [SubFieldIdentifiers]
        """Gets the subfield description for an ICAO field based on its ICAO field ID, i.e. F13, F16 etc.

            :param icao_field_id: The field ID; an enumerator from the FieldIdentifiers class. Based on
                                  the ICAO field numbers as defined in ICAO DOC 4444.
            :return:              A list of one or more enumeration values from the SubFieldIdentifiers class
                                  or None if the field 'icao_field_id' could not be found."""
        return self.field_content_description[icao_field_id][0]

    def get_field_errors(self, icao_field_id):
        # type: (FieldIdentifiers) -> [ErrorId]
        """Gets the list of errors defined for a given ICAO field that are used by the subfield
        parser to report errors.

        :param icao_field_id: The field ID; an enumerator from the FieldIdentifiers class. Based on
                              the ICAO field numbers as defined in ICAO DOC 4444.
        :return: A list of one or more enumeration values from the ErrorId class
                 or None if the field 'icao_field_id' could not be found."""
        return self.field_content_description[icao_field_id][1]
