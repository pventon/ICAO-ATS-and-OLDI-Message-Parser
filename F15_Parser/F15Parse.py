import copy

from F15_Parser.ErrorMessageDefinitions import ErrorMessages
from F15_Parser.ExtractedRouteRecord import ExtractedRouteRecord
from F15_Parser.ExtractedRouteSequence import ExtractedRouteSequence
from F15_Parser.F15TokenSyntaxDescriptions import TokenBaseType, TokenSubType, F15TokenSyntaxDefinition
from Tokenizer.Tokens import Tokens
from Tokenizer.Token import Token
from Utilities.Utils import Utils
from Utilities.Constants import Constants


class ParseF15:
    """This class parses an ICAO field 15 for correct syntax and semantics; an ICAO
    field 15 string is tokenized by the Tokenizer class to remove all whitespace,
    (spaces, newlines, carriage return and tabs).

    The Tokenizer produces a list of tokens in the Tokens class; this class uses the
    tokens as input to parse.

    The output is stored in an instance of the ExtractedRouteRecord class that is
    populated by this parser class.

    The parser checks for field 15 grammar and semantics reporting errors AS
    necessary.

    Field 15 comprises three basic types of tokens:
        - Point: A point can be an AIP published route point, a latitude / longitude
          or a point derived from a point / bearing / distance token;
        - Connector: A connector can be an AIP ATS route designator, DCT, SID,
          STAR, rule change tokens VFR/IFR, OAT/GAT or IFPSTART/IFPSTOP.
          Connectors connect points together.
        - Modifier: A modifier is a speed and / or level change. A modifier is applied
          at a point preceding the field 15 modifier token.
    This parser creates a list of points and connectors with modifiers applied at
    their associated point. A complete Extracted Route Sequence always starts and ends
    with the ADEP and ADES respectively, both are 'points'. The ERS contains all
    intermediate points connected with one of the connector types if specified in
    ICAO field 15."""

    DEFAULT_ALTITUDE = "F050"
    """The default speed used to assign a speed when a speed is not given, e.g. such as when a 
    SPEED/VFR element is processed. Default is set to F050, (Flight Level 50)."""

    RULES = {"I": "IFR", "V": "VFR", "O": "OAT", "S": "IFPS"}
    """Constants defining the flight rules applied to extracted route elements:
        - "I": "IFR" - Used for extracted route elements where IFR rules are to be applied;
        - "V": "VFR" - Used for extracted route elements where VFR rules are to be applied;
        - "O": "OAT" - Used to indicated Operational Air Traffic (OAT) section of a flight plan;
        - "S": "IFPS" - Used to indicate a 'break' in the IFR routing as determined by EUROCONTROL"""

    def parse_f15(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> bool
        """Entry point for the field 15 parser. Field 15 must start with one of two
        element types, either SPEED/ALTITUDE or SPEED/VFR, everything else is an error.
        When the ExtractedRouteRecord class is instantiated, record 0 is automatically created
        that represents the ADEP.

        The flight rules are set on the ADEP record based on the first field 15 token, either:
            - 'IFR' for SPEED/ALTITUDE or
            - 'VFR' for SPEED/VFR.
        Once parsing is complete an ADES record is added representing the ADES.

        It is the callers responsibility to populate the ADEP and ADES with pertinent
        information once parsing is complete.

        The records in an instance of ExtractedRouteSequence class contains a complete extracted
        route with all points, routes, flight rules, speed and altitudes etc. along a route.

        :param ers: An instance of ExtractedRouteSequence class being populated by the parser;
        :param tokens: A list of tokens extracted from field 15 used as input to the parser.
               This structure contains a tokenized form of all field 15 tokens used as
               input to this parser.
        :return: True if no errors were detected, False otherwise. If False is returned a
                 caller can recover a complete list of all erroneous tokens by calling
                 ExtractedRouteRecord.get_errors();
        """
        # Loop over all the tokens and assign a tokens base and subtype; this identifies a token and is used
        # by the parser to ensure correct grammar and semantics.
        self.assign_syntax_descriptions(tokens)

        # Get the first field 15 token
        token = tokens.get_first_token()
        if token is None:
            # Add a dummy error record and report an error
            ers.add_error("NULL", 0, 0, TokenBaseType.F15_UNKNOWN,
                          TokenSubType.F15_SB_UNKNOWN, ErrorMessages.error_messages[41])
            # Add a dummy ADES
            ers.add_dummy_ades()
            return False
        base_type = token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_SPEED_VFR:
                self.assign_speed_vfr(ers, tokens, token)
                ers.get_first_element().set_flight_rules(self.RULES["V"])
            case TokenBaseType.F15_SPEED_ALTITUDE:
                self.assign_speed_altitude(ers, tokens, token)
                if tokens.get_number_of_tokens() == 1:
                    # Only one token means field 15 has no further route description
                    self.add_error_and_re_sync(ers, tokens, token, 49)
            case _:
                # Error, field 15 must start with a 'Speed/altitude' or 'Speed VFR' token
                self.add_error_and_re_sync(ers, tokens, token, 1)

        # Add a dummy ADES
        ades = ers.add_dummy_ades()
        # Get the rules from the last but one ERS record and assign it to the ADES
        previous = ers.get_previous_to_last_element()
        if previous is None:
            return ers.get_number_of_errors() == 0
        ades.set_flight_rules(previous.get_flight_rules())

        # Return True if no errors have been reported
        return ers.get_number_of_errors() == 0

    def add_error_and_re_sync(self, ers, tokens, token, error_number):
        # type: (ExtractedRouteSequence, Tokens, Token, int) -> None
        """This method adds an error record to the ERS that contains a field 15 element
        deemed erroneous by the parser. The parser continues to try and parse the
        remainder of field 15 by calling ExtractedRouteRecord.re_sync_after_error().

        :param ers: An instance of ExtractedRouteSequence class into which the erroneous token is being stored;
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The erroneous token;
        :param error_number: An integer value representing an index to an error message
               defined in the ErrorMessageDefinitions class.
        :return: None
        """
        self.add_error_no_re_sync(ers, token, error_number)
        self.re_sync_parser_after_error(ers, tokens)

    @staticmethod
    def add_error_no_re_sync(ers, token, error_number):
        # type: (ExtractedRouteSequence, Token, int) -> None
        """This method adds an error record to the ERS that contains a field 15 element
        deemed erroneous by the parser.

        :param ers: An instance of ExtractedRouteSequence class into which the erroneous token is being stored;
        :param token: The erroneous token;
        :param error_number: An integer value representing an index to an error message
               defined in the ErrorMessageDefinitions class.
        :return: None
        """
        ers.add_error(token.get_token_string(),
                      token.get_token_start_index(),
                      token.get_token_end_index(),
                      token.get_token_base_type(),
                      token.get_token_sub_type(),
                      ErrorMessages.error_messages[error_number])

    def add_record(self, ers, token):
        # type: (ExtractedRouteSequence, Token) -> ExtractedRouteRecord
        """This method appends a successfully parsed field 15 element to the list of
        extracted route records in an instance of the ExtractedRouteRecord class.

        :param ers: An ExtractedRouteSequence class instance that this token is being appended to;
        :param token: The token being saved;
        :return: An instance of the ExtractedRouteRecord class representing the
                 saved extracted route item derived from the token input;
        """
        ex_route_rec = ers.append_element(ExtractedRouteRecord(token.get_token_string(),
                                                               token.get_token_start_index(),
                                                               token.get_token_end_index(),
                                                               token.get_token_base_type(),
                                                               token.get_token_sub_type()))
        self.carry_speed_altitude_rules_forward(ers)
        return ex_route_rec

    def assign_altitude(self, ers, token, ex_route_rec, altitude_string, cruise):
        # type: (ExtractedRouteSequence, Token, ExtractedRouteRecord, str, bool) -> None
        """This method saves the altitude data to both the imperial and SI altitude class members of an
        ERS record. All four altitude types encountered in a field 15 are converted to meters for SI
        storage. The altitude types processed are:
            - 'F' Flight level
            - 'S' Standard metric level in tens of metres
            - 'A' Altitude in hundreds of feet
            - 'M' Altitude in tens of metres
        The altitudes are applied to the point at which an altitude is encountered
        and propagated forward until a subsequent altitude change is encountered.

        :param ers: An ExtractedRouteSequence class instance that an error may
                    be written to if an error is detected;
        :param token: A token containing a token used to report an error if an error is detected in the token;
        :param ex_route_rec: An ExtractedRouteRecord record that the altitude is written to;
        :param altitude_string: An altitude as a string extracted from field 15, e.g. F350;
        :param cruise: A boolean indicating if the altitude_string is part of a cruise / climb token;
        :return: None
        """
        if cruise:
            ex_route_rec.set_altitude_cruise_to(altitude_string)
        else:
            ex_route_rec.set_altitude(altitude_string)
        altitude = int(altitude_string[1:])
        altitude_type = altitude_string[0:1]
        match altitude_type:
            # Types 'F' and 'S' are pressure flight levels in imperial ('F') or SI ('S') units
            # Types 'A' and 'M' are altitudes in imperial ('A') or SI ('M') units
            case "A":
                # A = Altitude in hundreds of feet, e.g. A045 = 4,500 feet (1,372 Meters)
                altitude = (altitude * 100) * Constants.FEET_TO_METERS
            case "F":
                # F = Flight Level in hundreds of feet, e.g. F350 = 35,000 feet (10,668 Meters)
                if altitude % 5 != 0:
                    self.add_error_no_re_sync(ers, token, 40)
                altitude = (altitude * 100) * Constants.FEET_TO_METERS
            case "S" | "M":
                # S = Flight Level in tens of meters, e.g. S1130 = 11,300 meters
                # M = Altitude in tens of meters, e.g. M0840 = 8,400 meters
                altitude = altitude * 10
        if cruise:
            ex_route_rec.set_altitude_cruise_to_si(int(altitude + 0.5))
        else:
            ex_route_rec.set_altitude_si(int(altitude + 0.5))

    def assign_azimuth_distance_between_points(self, ers):
        # type: (ExtractedRouteSequence) -> None
        """This method sets the bearing / distance on a point when two consecutive points are
        found both with valid latitude and longitude values assigned. This method 'looks' backward
        in the ERS to locate a 'previous' point with a valid latitude and longitude assigned.
        Points can follow one another or be separated by a connector (e.g. such as a DCT, ATS Route etc.).

        :param ers: The ERS whose last point has just been assigned a latitude / longitude;
        :return: None
        """
        last_ers = ers.get_last_element()
        if last_ers is None:
            return
        last_but_one_ers = ers.get_previous_to_last_element()
        if last_but_one_ers is None:
            return
        if last_ers.is_lat_long_valid():
            if last_but_one_ers.is_lat_long_valid():
                # We have two consecutive points with valid Latitude / Longitude
                # Set azimuth and distance between the two points at the previous
                # point.
                self.set_azimuth_and_distance(last_but_one_ers, last_ers)
            else:
                # Go back one more ERS element and check if this is a point
                last_minus_two_ers = ers.get_element_at(ers.get_number_of_elements()-3)
                if last_minus_two_ers is None:
                    return
                if last_minus_two_ers.is_lat_long_valid():
                    # We have two points separated by a 'connector' element and
                    # both points have a valid Latitude / Longitude
                    # Set azimuth and distance between the two points
                    self.set_azimuth_and_distance(last_minus_two_ers, last_ers)

    @staticmethod
    def assign_latitude(ex_route_rec, latitude):
        # type: (ExtractedRouteRecord, str) -> None
        """This method assigns the latitude as a decimal value to a points' latitude. The
        method takes the latitude input as a string.

        :param ex_route_rec: An extracted route record containing a point whose latitude
               is being set.
        :param latitude: The latitude as a string; 2 characters for degrees, 4 characters
               for degrees and minutes.
        :return: none
        """
        n_or_s = latitude[-1:]
        if len(latitude) < 4:
            # Degrees
            ex_route_rec.set_latitude(float(latitude[0:2]))
        else:
            # Degrees and minutes
            ex_route_rec.set_latitude(float(latitude[0:2]) + (float(latitude[2:4]) / 60.0))
        if n_or_s == "S":
            ex_route_rec.set_latitude(ex_route_rec.get_latitude() * -1.0)

    def assign_lat_long_bearing_distance(self, ers, token):
        # type: (ExtractedRouteSequence, Token) -> None
        """This method processes a point looking for and checking the semantics for latitude / longitude
        and bearing distance points. Errors are reported as they are detected; the parser does not reset when
        an error is located but continues to detect any and all semantic errors for a given point. Semantic
        checks ensure angles do not exceed those specified as follows:
            - Bearing Distance: Bearing angle checked that it does not exceed 360 degrees;
            - Lat/Long Degrees: Latitude degrees checked for max 90 and longitude degrees max 180 degrees;
            - Lat/Long Degrees & Minutes: Latitude degrees checked for max 90, minutes 59 and longitude
              degrees max 180, minutes 59;

        :param ers: An ExtractedRouteSequence class instance that any erroneous token are saved to;
        :param token: The point token being semantically checked;
        :return: None
        """
        token_string = token.get_token_string()
        sub_type = token.get_token_sub_type()
        ex_route_rec = ers.get_last_element()
        match sub_type:
            case TokenSubType.F15_SB_PRP_BD:
                # Point followed by Bearing Distance
                if not Utils.is_degree_semantics(token_string[-6:-3], 360):
                    self.add_error_no_re_sync(ers, token, 46)
                    # To populate the lat/long properly, the lat/long for the
                    # point is needed, which we currently do not have.
                    # Nothing to do for now.
            case TokenSubType.F15_SB_LL_DEG:
                # Lat/Long in Degrees
                self.assign_ll_deg(ers, token, ex_route_rec, token_string)
            case TokenSubType.F15_SB_LL_MIN:
                # Lat/Long in Degrees and Minutes
                self.assign_ll_deg_min(ers, token, ex_route_rec, token_string)
            case TokenSubType.F15_SB_LLBD_DEG:
                # Lat/Long in Degrees followed Bearing Distance
                self.assign_ll_deg(ers, token, ex_route_rec, token_string)
                # Process the bearing component
                if not Utils.is_degree_semantics(token_string[-6:-3], 360):
                    self.add_error_no_re_sync(ers, token, 46)
                # Calculate the 'real' point from the given lat/long and the
                # bearing / distance.
                self.resolve_real_bd_point(
                     ers, ex_route_rec, float(token_string[-6:-3]), float(token_string[-3:]))
            case TokenSubType.F15_SB_LLBD_MIN:
                # Lat/Long in Degrees and Minutes followed by Bearing Distance
                self.assign_ll_deg_min(ers, token, ex_route_rec, token_string)
                if not Utils.is_degree_semantics(token_string[-6:-3], 360):
                    self.add_error_no_re_sync(ers, token, 46)
                # Calculate the 'real' point from the given lat/long and the
                # bearing / distance.
                self.resolve_real_bd_point(
                     ers, ex_route_rec, float(token_string[-6:-3]), float(token_string[-3:]))

    def assign_ll_deg(self, ers, token, ex_route_rec, token_string):
        # type: (ExtractedRouteSequence, Token, ExtractedRouteRecord, str) -> None
        """This method takes a field 15 element representing a point defined as a latitude / longitude in
        degrees (no minutes) and converts the string representation of the latitude / longitude into decimal
        values and stores them in an ERS record.

        The North / South and East / West indicators determine if the decimal value is negative or positive.

        Errors are reported if the angular values specify incorrect semantics. Valid angles are:
            - 00 to 90 for Latitude, North indicator value is positive, South negative;
            - 000 to 180 for Longitude, East indicator value is positive, West negative;

        :param ers: The complete Extracted Route Sequence (ERS);
        :param token: The field 15 lat/long element being processed;
        :param ex_route_rec: An ERS record into which the decimal lat/long values will
               be written;
        :param token_string: The string representing an ICAO lat/long (e.g.23N123E);
        :return: None
        """
        self.assign_latitude(ex_route_rec, token_string[0:3])
        self.assign_longitude(ex_route_rec, token_string[3:7])
        if not Utils.is_degree_semantics(token_string[0:2], 90):
            self.add_error_no_re_sync(ers, token, 42)
        if not Utils.is_degree_semantics(token_string[3:6], 180):
            self.add_error_no_re_sync(ers, token, 44)
        ex_route_rec.set_lat_long_valid(True)
        self.assign_azimuth_distance_between_points(ers)

    def assign_ll_deg_min(self, ers, token, ex_route_rec, token_string):
        # type: (ExtractedRouteSequence, Token, ExtractedRouteRecord, str) -> None
        """This method takes a field 15 element representing a point defined as a latitude / longitude
        in degrees (with minutes) and converts the string representation of the latitude / longitude into
        decimal values and stores them in an ERS record.

        The North / South and East / West indicators determine if the decimal value is negative or positive.

        Errors are reported if the angular values specify incorrect semantics. Valid angles are:
            - 00 to 90 for Latitude, North indicator value is positive, South negative;
            - 000 to 180 for Longitude, East indicator value is positive, West negative;
            - 00 to 59 for minutes;

        :param ers: The complete Extracted Route Sequence (ERS);
        :param token: The field 15 lat/long element being processed;
        :param ex_route_rec: An ERS record into which the decimal lat/long values will
               be written;
        :param token_string: The string representing an ICAO lat/long (e.g.23N123E);
        :return: None
        """
        self.assign_latitude(ex_route_rec, token_string[0:5])
        self.assign_longitude(ex_route_rec, token_string[5:11])
        if not Utils.is_degree_minute_semantics(token_string[0:4], 90, 2):
            self.add_error_no_re_sync(ers, token, 43)
        if not Utils.is_degree_minute_semantics(token_string[5:10], 180, 3):
            self.add_error_no_re_sync(ers, token, 45)
        ex_route_rec.set_lat_long_valid(True)
        self.assign_azimuth_distance_between_points(ers)

    @staticmethod
    def assign_longitude(ex_route_rec, longitude):
        # type: (ExtractedRouteRecord, str) -> None
        """This method assigns a floating point number to a points' longitude. The method takes the
        longitude input as a string.

        :param ex_route_rec: An extracted route record containing a point whose longitude
               is being set.
        :param longitude: The longitude as a string; 3 characters for degrees, 5 characters
               for degrees and minutes.
        :return: None
        """
        e_or_w = longitude[-1:]
        if len(longitude) < 5:
            # Degrees
            ex_route_rec.set_longitude(float(longitude[0:3]))
        else:
            # Degrees and minutes
            ex_route_rec.set_longitude(float(longitude[0:3]) + (float(longitude[3:5]) / 60.0))
        if e_or_w == "W":
            ex_route_rec.set_longitude(ex_route_rec.get_longitude() * -1.0)

    @staticmethod
    def assign_speed(ex_route_rec, speed_string):
        # type: (ExtractedRouteRecord, str) -> None
        """This method saves the speed data to the imperial and SI speed members of an ERS record.
        All three speed types encountered in a field 15 are converted to meters / second for SI storage.
        The speed types processed are:
            - 'K' Kilometres per hour
            - 'N' Knots
            - 'M' True Mach number
        The speeds are applied to the point at which a speed is encountered and propagated forward until
        a subsequent speed change is encountered.

        Note that the Mach speed requires the altitude, hence the ERS altitude record must always be
        set before determining the speed. Some field 15 elements contain only a speed (e.g. Speed / VFR).
        If a Mach number is given in such elements, the speed is calculated using the speed of sound
        at sea level.

        :param ex_route_rec: An ExtractedRouteRecord record that the altitude is written to;
        :param speed_string: A speed as a string extracted from field 15, e.g. N0450;
        :return: none
        """
        ex_route_rec.set_speed(speed_string)

        # Need the altitude in meters for Mach calculation
        altitude_si = ex_route_rec.get_altitude_si()
        speed = int(speed_string[1:])
        speed_type = speed_string[0:1]
        match speed_type:
            case "K":
                # Kilometers / hour
                speed = speed * Constants.KMH_TO_METERS_SECOND
            case "N":
                # Knots
                speed = speed * Constants.KNOTS_TO_METERS_SECOND
            case "M":
                speed = Utils.mach_to_ms_speed(speed, altitude_si)
        ex_route_rec.set_speed_si(int(speed + 0.5))

    def assign_speed_altitude(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a speed / altitude element, (e.g. N0450F350). A speed / altitude element
        is always preceded by a point, hence the speed and altitude are applied to the preceding point
        which is the last ERS record.

        Note that the altitude must be assigned in meters to the ERS before the speed as the speed given
        as a Mach number uses the altitude to calculate a speed.

        :param ers: An ExtractedRouteSequence class instance containing a point in
               the last ERS record that the speed and altitude will be written to;
        :param tokens: A list of tokens extracted from field 15 used as input to the parser.
               This structure contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The speed / altitude token from which the speed and altitude will
               be extracted from;
        :return: None
        """
        ex_route_rec = ers.get_last_element()
        if ex_route_rec is None:
            return
        token_string = token.get_token_string()
        sub_type = token.get_token_sub_type()
        match sub_type:
            case TokenSubType.F15_SB_SPEED_ALTITUDE_MF | TokenSubType.F15_SB_SPEED_ALTITUDE_MS | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_MA | TokenSubType.F15_SB_SPEED_ALTITUDE_MM:
                self.assign_altitude(ers, token, ex_route_rec, token_string[4:], False)
                self.assign_speed(ex_route_rec, token_string[0:4])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_KS | TokenSubType.F15_SB_SPEED_ALTITUDE_KA | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_KM | TokenSubType.F15_SB_SPEED_ALTITUDE_NS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NA | TokenSubType.F15_SB_SPEED_ALTITUDE_NM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_KF | TokenSubType.F15_SB_SPEED_ALTITUDE_NF:
                self.assign_altitude(ers, token, ex_route_rec, token_string[5:], False)
                self.assign_speed(ex_route_rec, token_string[0:5])
            case _:
                self.assign_altitude(ers, token, ex_route_rec, "X000", False)
                self.assign_speed(ex_route_rec, "X0000")
                return

        # As this is a speed altitude element, the rules must be IFR
        ex_route_rec.set_flight_rules(self.RULES["I"])

        next_token = tokens.get_next_token()
        if next_token is None:
            return

        # If there is only one ERS record it has to be the ADEP record, i.e. the
        # next token is the first element following the first SPEED / LEVEL
        # element. Otherwise, we are processing an element after a SPEED / LEVEL
        # somewhere else in field 15.
        if ers.get_number_of_elements() == 1:
            self.post_adep(ers, tokens, next_token)
        else:
            # Go to post point processing as a rule change to IFR is terminated
            # with a point
            self.post_point(ers, tokens, next_token)

    def assign_speed_altitude_altitude(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes the speed / altitude / altitude part of a cruise climb element.
        A speed / altitude / altitude element is always preceded by a point, hence the speed and altitude
        are applied to the preceding point which is the last ERS record.

        :param ers: An ExtractedRouteSequence class instance containing a point in
               the last ERS record that the speed and altitude will be written to.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser.
               This structure contains a tokenized form of all field 15 tokens used as
               input to this parser.
        :param token: The speed / altitude token from which the speed and altitude will
               be extracted from;
        :return: None
        """
        ex_route_rec = ers.get_last_element()
        if ex_route_rec is None:
            return
        token_string = token.get_token_string()
        sub_type = token.get_token_sub_type()
        match sub_type:
            case TokenSubType.F15_SB_SPEED_ALTITUDE_KFF | TokenSubType.F15_SB_SPEED_ALTITUDE_KFS | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_KFA | TokenSubType.F15_SB_SPEED_ALTITUDE_KFM | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_KAF | TokenSubType.F15_SB_SPEED_ALTITUDE_KAS | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_KAA | TokenSubType.F15_SB_SPEED_ALTITUDE_KAM | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_NFF | TokenSubType.F15_SB_SPEED_ALTITUDE_NFS | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_NFA | TokenSubType.F15_SB_SPEED_ALTITUDE_NFM | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_NAF | TokenSubType.F15_SB_SPEED_ALTITUDE_NAS | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_NAA | TokenSubType.F15_SB_SPEED_ALTITUDE_NAM:
                self.assign_altitude(ers, token, ex_route_rec, token_string[5:9], False)
                self.assign_altitude(ers, token, ex_route_rec, token_string[9:], True)
                self.assign_speed(ex_route_rec, token_string[0:5])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_KSF | TokenSubType.F15_SB_SPEED_ALTITUDE_KSS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_KSA | TokenSubType.F15_SB_SPEED_ALTITUDE_KSM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_KMF | TokenSubType.F15_SB_SPEED_ALTITUDE_KMS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_KMA | TokenSubType.F15_SB_SPEED_ALTITUDE_KMM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NSF | TokenSubType.F15_SB_SPEED_ALTITUDE_NSS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NSA | TokenSubType.F15_SB_SPEED_ALTITUDE_NSM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NMF | TokenSubType.F15_SB_SPEED_ALTITUDE_NMS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NMA | TokenSubType.F15_SB_SPEED_ALTITUDE_NMM:
                self.assign_altitude(ers, token, ex_route_rec, token_string[5:10], False)
                self.assign_altitude(ers, token, ex_route_rec, token_string[11:], True)
                self.assign_speed(ex_route_rec, token_string[0:5])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_MFF | TokenSubType.F15_SB_SPEED_ALTITUDE_MFS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MFA | TokenSubType.F15_SB_SPEED_ALTITUDE_MFM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MAF | TokenSubType.F15_SB_SPEED_ALTITUDE_MAS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MAA | TokenSubType.F15_SB_SPEED_ALTITUDE_MAM:
                self.assign_altitude(ers, token, ex_route_rec, token_string[4:8], False)
                self.assign_altitude(ers, token, ex_route_rec, token_string[9:], True)
                self.assign_speed(ex_route_rec, token_string[0:4])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_MSF | TokenSubType.F15_SB_SPEED_ALTITUDE_MSS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MSA | TokenSubType.F15_SB_SPEED_ALTITUDE_MSM | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MMF | TokenSubType.F15_SB_SPEED_ALTITUDE_MMS | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_MMA | TokenSubType.F15_SB_SPEED_ALTITUDE_MMM:
                self.assign_altitude(ers, token, ex_route_rec, token_string[4:9], False)
                self.assign_altitude(ers, token, ex_route_rec, token_string[10:], True)
                self.assign_speed(ex_route_rec, token_string[0:4])
            case _:
                self.assign_altitude(ers, token, ex_route_rec, "X000", False)
                self.assign_speed(ex_route_rec, "X000")
                return

        # As this is a speed altitude element, the rules must be IFR
        ex_route_rec.set_flight_rules(self.RULES["I"])

        next_token = tokens.get_next_token()
        if next_token is None:
            return

        self.post_point(ers, tokens, next_token)

    def assign_speed_altitude_plus(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes the speed / altitude / plus part of a cruise climb element.
        A speed / altitude / plus element is always preceded by a point, hence the speed and altitude
        are applied to the preceding point which is the last ERS record.

        :param ers: An ExtractedRouteSequence class instance containing a point in
               the last ERS record that the speed and altitude will be written to.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser.
               This structure contains a tokenized form of all field 15 tokens used as
               input to this parser.
        :param token: The speed / altitude token from which the speed and altitude will
               be extracted from;
        :return: None
        """
        ex_route_rec = ers.get_last_element()
        if ex_route_rec is None:
            return
        token_string = token.get_token_string()
        sub_type = token.get_token_sub_type()
        match sub_type:
            case TokenSubType.F15_SB_SPEED_ALTITUDE_KF_P | TokenSubType.F15_SB_SPEED_ALTITUDE_KA_P | \
                 TokenSubType.F15_SB_SPEED_ALTITUDE_NF_P | TokenSubType.F15_SB_SPEED_ALTITUDE_NA_P:
                self.assign_altitude(ers, token, ex_route_rec, token_string[5:9], False)
                ex_route_rec.set_altitude_cruise_to(token_string[9:])
                self.assign_speed(ex_route_rec, token_string[0:5])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_KS_P | TokenSubType.F15_SB_SPEED_ALTITUDE_KM_P | \
                    TokenSubType.F15_SB_SPEED_ALTITUDE_NS_P | TokenSubType.F15_SB_SPEED_ALTITUDE_NM_P:
                self.assign_altitude(ers, token, ex_route_rec, token_string[5:10], False)
                ex_route_rec.set_altitude_cruise_to(token_string[10:])
                self.assign_speed(ex_route_rec, token_string[0:5])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_MF_P | TokenSubType.F15_SB_SPEED_ALTITUDE_MA_P:
                self.assign_altitude(ers, token, ex_route_rec, token_string[4:8], False)
                ex_route_rec.set_altitude_cruise_to(token_string[8:])
                self.assign_speed(ex_route_rec, token_string[0:4])
            case TokenSubType.F15_SB_SPEED_ALTITUDE_MS_P | TokenSubType.F15_SB_SPEED_ALTITUDE_MM_P:
                self.assign_altitude(ers, token, ex_route_rec, token_string[4:9], False)
                ex_route_rec.set_altitude_cruise_to(token_string[9:])
                self.assign_speed(ex_route_rec, token_string[0:4])
            case _:
                self.assign_altitude(ers, token, ex_route_rec, "X000", False)
                self.assign_speed(ex_route_rec, "X000")
                return

        # As this is a speed altitude element, the rules must be IFR
        ex_route_rec.set_flight_rules(self.RULES["I"])

        next_token = tokens.get_next_token()
        if next_token is None:
            return

        self.post_point(ers, tokens, next_token)

    def assign_speed_vfr(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method precess a speed / VFR element. The element preceding a SPEED/VFR token must be
        a point, hence we have to set the speed at the previous point and assign VFR rules at a new
        ERS record to store the rule change VFR record.

        :param ers: An ExtractedRouteSequence class instance containing a point in the last ERS record
               that the speed will be written to and a new VFR record will be appended to.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The speed / VFR token from which the speed will be extracted from;
        :return: None
        """
        # Get the last ERS record which will be a point at which the VFR
        # rule change is taking place.
        point_ex_route_rec = ers.get_last_element()
        if point_ex_route_rec is None:
            return

        # Create a copy of the SPEED/VFR token and change the name to 'VFR'
        vfr_token = copy.deepcopy(token)
        vfr_token.set_token_string("VFR")
        ex_route_rec = self.add_record(ers, vfr_token)

        # Assign a default altitude as none is given in a SPEED/VFR element
        self.assign_altitude(ers, token, ex_route_rec, self.DEFAULT_ALTITUDE, False)

        token_string = token.get_token_string()
        sub_type = token.get_token_sub_type()
        match sub_type:
            case TokenBaseType.F15_SPEED_VFR | TokenSubType.F15_SB_SPEED_ALTITUDE_MV:
                self.assign_speed(ex_route_rec, token_string[0:4])
                ex_route_rec.set_flight_rules(self.RULES[token_string[4:5]])
            case TokenBaseType.F15_SPEED_VFR | TokenSubType.F15_SB_SPEED_ALTITUDE_NV | \
                    TokenBaseType.F15_SPEED_VFR | TokenSubType.F15_SB_SPEED_ALTITUDE_KV:
                self.assign_speed(ex_route_rec, token_string[0:5])
                ex_route_rec.set_flight_rules(self.RULES[token_string[5:6]])
            case _:
                self.assign_altitude(ers, token, ex_route_rec, "X000", False)
                ex_route_rec.set_flight_rules(self.RULES["I"])

        # Copy the speed and altitude from the VFR record to the VFR rule change point
        point_ex_route_rec.set_speed(ex_route_rec.get_speed())
        point_ex_route_rec.set_speed_si(ex_route_rec.get_speed_si())
        point_ex_route_rec.set_altitude(ex_route_rec.get_altitude())
        point_ex_route_rec.set_altitude_si(ex_route_rec.get_altitude_si())

        token = tokens.get_next_token()
        if token is None:
            return
        self.break_text_save(ers, tokens, token)

    def break_end(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method is processing a 'break' end token, one of 'IFR', 'GAT' or 'IFPSTART'. A 'break' is
        considered to be a break in IFR routing, i.e. a change from IFR to VFR and back to IFR has a 'break'
        between two IFR sections. Any tokens appearing between the end of the first IFR section and the
        start of the second IFR section are stored on the intermediate VFR (or OAT, IFPSTOP) section token,
        (referred to as break text).

        If the end of a break section is NOT occurring then control is returned to saving these tokens as
        'break' text. All break text ends must be followed by a point. The IFR end must be further followed
        by a point/speed/altitude or point/speed/vfr element. As a rule change is terminated by a point,
        control is handed to the point node for further processing.

        :param ers: An ExtractedRouteSequence class instance containing a start break token, (one of VFR,
               OAT or IFPSTOP) in the last ERS record that the break text will be written to, or if the
               'break' is determined then the change back to IFR will be appended to the ERS.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The 'break' end token, ('IFR', 'GAT' or 'IFPSTART' token indicating the end of 'break';
        :return: None
        """
        # Get what should be a point following the IFR, GAT or IFPSTART element
        rule_change_point = tokens.peek_next_token(1)
        if rule_change_point is None:
            # Nothing following the rule change token
            return
        if rule_change_point.get_token_base_type() != TokenBaseType.F15_POINT:
            # Element following rule change is not a point
            return

        # Process rule change according to type of rule change
        sub_type = token.get_token_sub_type()
        if sub_type == TokenSubType.F15_SB_IFR:

            # Get the '/' following the point
            slash_token = tokens.peek_next_token(2)
            if slash_token is None:
                # End of field 15, no further processing, rule change incomplete
                self.add_error_and_re_sync(ers, tokens, rule_change_point, 22)
                return
            if slash_token.get_token_base_type() != TokenBaseType.F15_SLASH:
                # Not a slash, we can assume no rule change is taking place.
                # We can bale out of rule change processing
                return

            # Get the SPEED / LEVEL following the '/'
            speed_level_token = tokens.peek_next_token(3)
            if speed_level_token is None:
                # End of field 15, no further processing, rule change incomplete
                self.add_error_and_re_sync(ers, tokens, rule_change_point, 22)
                return
            if speed_level_token.get_token_base_type() != TokenBaseType.F15_SPEED_ALTITUDE and \
                    speed_level_token.get_token_base_type() != TokenBaseType.F15_SPEED_VFR:
                # Not a SPEED / LEVEL, we can assume no rule change is taking place
                # We can bale out of rule change processing, the tokens 'peeked' in
                # this method will be saved as break text by the calling function.
                self.add_error_and_re_sync(ers, tokens, rule_change_point, 22)
                return

            # All tokens indicating a rule change are present and correct,
            # action the rule change.
            if speed_level_token.get_token_base_type() == TokenBaseType.F15_SPEED_ALTITUDE:
                self.v_to_i_rule_change(ers, tokens)
            elif speed_level_token.get_token_base_type() == TokenBaseType.F15_SPEED_VFR:
                self.v_to_i_to_v_rule_change(ers, tokens)

        # If we arrive here we are dealing with a rule change from OAT to GAT or
        # IFPSTOP to IFPSTART, hence we can process the point as any other point.
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        self.point(ers, tokens, next_token)

    def break_end_error(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method reports an error if the end of a 'break' section does not match a 'break' start token.
        A 'break' is considered to be a break in IFR routing, i.e. a change from IFR to VFR and back to IFR
        has a 'break' between two IFR sections. Break sections are indicated by start/end matching pairs VFR/IFR,
        OAT/GAT, IFPSTOP/IFPSTART. Erroneous case are, e.g. a VFR break started and now a GAT 'break' end is
        detected, hence the start and end indicators do not form part of a matching 'break' indicator pair.

        :param ers: An ExtractedRouteSequence class instance containing a point token in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The 'break' end token, ('IFR', 'GAT' or 'IFPSTART') token indicating the start of
               'break' section;
        :return:
        """
        subtype = token.get_token_sub_type()
        if subtype is TokenSubType.F15_SB_IFR:
            self.add_error_and_re_sync(ers, tokens, token, 6)
        elif subtype is TokenSubType.F15_SB_GAT:
            self.add_error_and_re_sync(ers, tokens, token, 7)
        elif subtype is TokenSubType.F15_SB_IFPSTART:
            self.add_error_and_re_sync(ers, tokens, token, 8)

    def break_start(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method is processing the elements 'OAT', IFPSTOP', or 'VFR' all of which indicate the
        start of non-IFR routing, a 'break' section. A 'break' is considered to be a break in IFR routing,
        i.e. a change from IFR to VFR and back to IFR has a 'break' between two IFR sections. The ERS last
        element is a point at which the 'break' section starts. The start 'break' token will be appended
        to the ERS and one of the following flight rules set on the start 'break' token:
            - OAT: Rules set to 'O'
            - VFR: Rules set to 'V'
            - IFPSTOP: Rules set to 'S'
        The rule change token is saved to the ERS and the rules are set on this token.

        :param ers: An ExtractedRouteSequence class instance containing a point token in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The 'break' start token, ('VFR', 'OAT' or 'IFPSTOP' token indicating
               the start of 'break' section;
        :return: None
        """
        self.add_record(ers, token)
        ex_route_rec = ers.get_last_element()
        sub_type = token.get_token_sub_type()
        match sub_type:
            case TokenSubType.F15_SB_OAT:
                ex_route_rec.set_flight_rules(self.RULES["O"])
            case TokenSubType.F15_SB_VFR:
                ex_route_rec.set_flight_rules(self.RULES["V"])
            case TokenSubType.F15_SB_IFPSTOP:
                ex_route_rec.set_flight_rules(self.RULES["S"])

        next_token = tokens.get_next_token()
        if next_token is None:
            return
        base_type = next_token.get_token_base_type()
        if base_type is TokenBaseType.F15_TOO_LONG:
            self.add_error_and_re_sync(ers, tokens, next_token, 4)
        else:
            self.break_text_save(ers, tokens, next_token)

    def break_text_save(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method loops over elements saving them as 'break' text; break text follows the 'break'
        start tokens VFR, OAT or IFPSTOP. A 'break' is considered to be a break in IFR routing, i.e. a
        change from IFR to VFR and back to IFR has a 'break' between two IFR sections.

        Once a 'break' end element is detected, processing takes place to ascertain if a 'break' section
        is being correctly terminated; if not, this method continues to save the tokens as 'text' on the
        'break' start token. If there is a possible 'break' end detected control is passed to self.break_end().

        :param ers: An ExtractedRouteSequence class instance containing a 'break' start token in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The 'break' text token being saved to the 'break' start token;
        :return: None
        """
        base_type = token.get_token_base_type()
        if base_type is TokenBaseType.F15_TOO_LONG:
            self.add_error_and_re_sync(ers, tokens, token, 4)

        # Save the token as break text
        last_ers = ers.get_last_element()
        last_ers.append_break_text(token.get_token_string())

        sub_type = token.get_token_sub_type()
        cur_break_type = ers.get_last_element().get_flight_rules()

        # Break text processing is terminated on a rule change back to IFR. If
        # the token being processed in this method indicates the end of a break
        # section (i.e. for VFR -> IFR, for OAT -> GAT or for IFPSTOP -> IFPSTART)
        # processing is handed off to check if a valid rule change is in fact occurring.
        # Also have to check that the break end matches the break start type before
        # jumping out to try and end the break section
        if sub_type is TokenSubType.F15_SB_IFR and cur_break_type is self.RULES["V"]:
            # Possible change to IFR from VFR
            self.break_end(ers, tokens, token)
        elif sub_type is TokenSubType.F15_SB_GAT and cur_break_type is self.RULES["O"]:
            # Possible change to GAT from OAT
            self.break_end(ers, tokens, token)
        elif sub_type is TokenSubType.F15_SB_IFPSTART and cur_break_type is self.RULES["S"]:
            # Possible change to IFPSTOP from IFPSTART
            self.break_end(ers, tokens, token)

        # Recurse with the next token
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        self.break_text_save(ers, tokens, next_token)

    @staticmethod
    def carry_speed_altitude_rules_forward(ers):
        # type: (ExtractedRouteSequence) -> None
        """This method copies the speed, altitude and flight rules from the 'previous' ERS token to the
        'current' (last) ERS token.

        :param ers: An ExtractedRouteSequence class instance containing the last ERS record that has to have
               its speed, altitude and flight rule attributes copied from the penultimate ERS record to the last
               record.
        :return: None
        """
        current_ex_route_rec = ers.get_last_element()
        previous_ex_route_rec = ers.get_previous_to_last_element()
        current_ex_route_rec.set_altitude(previous_ex_route_rec.get_altitude())
        current_ex_route_rec.set_altitude_si(previous_ex_route_rec.get_altitude_si())
        current_ex_route_rec.set_speed(previous_ex_route_rec.get_speed())
        current_ex_route_rec.set_speed_si(previous_ex_route_rec.get_speed_si())
        current_ex_route_rec.set_flight_rules(previous_ex_route_rec.get_flight_rules())

    def cruise_climb_c(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes the 'C' token that indicates a cruise climb element may be present. If the
        token following the 'C' is a '/' then we assume a cruise climb token has been located, in such a
        case, the 'C' is not stored in the ERS. If the token following 'C' is not a '/' then the 'C' is
        considered to be a single character point and stored in the ERS as a point.

        :param ers: An ExtractedRouteSequence class instance containing a 'break' start token in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure contains
               a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The 'break' text token being saved to the 'break' start token;
        :return: None
        """
        next_token = tokens.get_next_token()
        if next_token is None:
            # Store the 'C' as a point
            self.add_record(ers, token)
            return
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, next_token, 3)
            case TokenBaseType.F15_SLASH:
                # '/' found next, assume cruise climb
                # Next token should be a point
                slash_token = next_token
                next_token = tokens.get_next_token()
                if next_token is None:
                    # No further tokens, Store the 'C' as a point
                    self.add_record(ers, token)
                    # Report error, only have C/, should be more
                    self.add_error_and_re_sync(ers, tokens, slash_token, 52)
                    return
                # Process the cruise climb point
                self.cruise_climb_point(ers, tokens, next_token)
            case TokenBaseType.F15_BREAK_START:
                self.add_record(ers, token)
                self.break_start(ers, tokens, next_token)
            case TokenBaseType.F15_SPEED_VFR | TokenBaseType.F15_SPEED_ALTITUDE:
                self.add_error_and_re_sync(ers, tokens, next_token, 5)
            case TokenBaseType.F15_BREAK_END:
                self.break_end_error(ers, tokens, next_token)
            case TokenBaseType.F15_DCT:
                self.add_record(ers, token)
                self.dct(ers, tokens, next_token)
            case TokenBaseType.F15_STAY:
                self.add_record(ers, token)
                self.stay(ers, tokens, next_token)
            case TokenBaseType.F15_TRUNCATE:
                self.add_record(ers, token)
                self.truncate(ers, tokens)
            case TokenBaseType.F15_C:
                self.add_record(ers, token)
                self.cruise_climb_c(ers, tokens, next_token)
            case TokenBaseType.F15_POINT:
                self.add_record(ers, token)
                self.point(ers, tokens, next_token)
            case TokenBaseType.F15_ROUTE:
                self.add_record(ers, token)
                self.route(ers, tokens, next_token)
            case TokenBaseType.F15_SID_STAR:
                self.add_record(ers, token)
                self.sid_star(ers, tokens, next_token)
            case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE | TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                self.add_error_and_re_sync(ers, tokens, next_token, 9)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, next_token, 4)
            case TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, next_token, 10)
            case TokenBaseType.F15_SID:
                self.add_record(ers, token)
                self.sid(ers, tokens, next_token)
            case TokenBaseType.F15_STAR:
                self.add_record(ers, token)
                self.star(ers, tokens, next_token)
            case _:
                self.add_error_and_re_sync(ers, tokens, token, 0)

    def cruise_climb_point(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes the point in a cruise/climb element.

        :param ers: An ExtractedRouteSequence class instance containing an IFR routing element in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The point in a cruise/climb element;
        :return: None
        """
        # Save the cruise / climb point
        self.add_record(ers, token)

        # Check the point semantics for Lat/Long, bearing distance points
        self.assign_lat_long_bearing_distance(ers, token)

        # Get the next token which should be a forward slash '/'
        next_token = tokens.get_next_token()
        if next_token is None:
            self.add_error_and_re_sync(ers, tokens, token, 27)
            return
        base_type = next_token.get_token_base_type()
        if base_type is not TokenBaseType.F15_SLASH:
            self.add_error_and_re_sync(ers, tokens, next_token, 26)

        # Skip the forward slash and get the SPEED/ALTITUDE/ALTITUDE or
        # SPEED / ALTITUDE / PLUS token
        next_token = tokens.get_next_token()
        if next_token is None:
            self.add_error_and_re_sync(ers, tokens, token, 28)
            return
        base_type = next_token.get_token_base_type()

        # Apply the cruise climb speed and altitude values
        if base_type is TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE:
            self.assign_speed_altitude_altitude(ers, tokens, next_token)
        elif base_type is TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
            self.assign_speed_altitude_plus(ers, tokens, next_token)
        else:
            self.add_error_and_re_sync(ers, tokens, next_token, 29)

        next_token = tokens.get_next_token()
        if next_token is None:
            return
        self.point(ers, tokens, next_token)

    def dct(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a DCT element.

        :param ers: An ExtractedRouteSequence class instance containing an IFR routing point element in the
               last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The DCT element;
        :return: None
        """
        self.add_record(ers, token)
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, next_token)
            case TokenBaseType.F15_C:
                self.cruise_climb_c(ers, tokens, next_token)
            case _:
                self.add_error_and_re_sync(ers, tokens, next_token, 21)

    def forward_slash(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a '/' token; the '/' character is not stored in the ERS. The method looks
        for tokens following the '/' as there are only certain element types allowed to follow a '/', namely
        speed/vfr, speed/altitude, truncate indicator point or route. All other element types are incorrect
        resulting in an error being reported.

        :param ers: An ExtractedRouteSequence class instance containing an IFR point element in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure contains
               a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The '/' token;
        :return: None
        """
        # Don't save the '/' and get next token
        next_token = tokens.get_next_token()
        if next_token is None:
            self.add_error_and_re_sync(ers, tokens, token, 20)
            return
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, next_token, 3)
            case TokenBaseType.F15_SLASH:
                self.add_error_and_re_sync(ers, tokens, next_token, 16)
            case TokenBaseType.F15_SPEED_VFR:
                self.assign_speed_vfr(ers, tokens, next_token)
            case TokenBaseType.F15_SPEED_ALTITUDE:
                self.assign_speed_altitude(ers, tokens, next_token)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, next_token, 4)
            case _:
                # TokenBaseType.F15_BREAK_START | TokenBaseType.F15_BREAK_END |
                # TokenBaseType.F15_DCT | TokenBaseType.F15_STAY |
                # TokenBaseType.F15_TRUNCATE | TokenBaseType.F15_C |
                # TokenBaseType.F15_POINT | TokenBaseType.F15_ROUTE |
                # TokenBaseType.F15_SID_STAR | TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE |
                # TokenBaseType.F15_SPEED_ALTITUDE_PLUS | TokenBaseType.F15_STAY_TIME |
                # TokenBaseType.F15_SID | TokenBaseType.F15_STAR
                self.add_error_and_re_sync(ers, tokens, next_token, 50)

    def post_adep(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method determines the next node to move to after a speed/altitude has been applied to the
        first ERS record, the ADEP element.

        :param ers: An ExtractedRouteSequence class instance containing only the ADEP record element
               in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: The first token in the tokens list.
        :return: None
        """
        base_type = token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, token, 3)
            case TokenBaseType.F15_SLASH | TokenBaseType.F15_BREAK_START | \
                    TokenBaseType.F15_SPEED_VFR | TokenBaseType.F15_SPEED_ALTITUDE | \
                    TokenBaseType.F15_BREAK_END | TokenBaseType.F15_STAY | \
                    TokenBaseType.F15_C:
                self.add_error_and_re_sync(ers, tokens, token, 23)
            case TokenBaseType.F15_DCT:
                self.dct(ers, tokens, token)
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, token)
            case TokenBaseType.F15_ROUTE:
                self.add_error_and_re_sync(ers, tokens, token, 24)
            case TokenBaseType.F15_SID_STAR:
                self.sid_star(ers, tokens, token)
            case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE | TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                self.add_error_and_re_sync(ers, tokens, token, 9)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, token, 4)
            case TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, token, 10)
            case TokenBaseType.F15_SID:
                self.sid(ers, tokens, token)
            case TokenBaseType.F15_STAR:
                self.star(ers, tokens, token)
            case _:
                self.add_error_and_re_sync(ers, tokens, token, 0)

    def post_point(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method determines the next node to move to following a point element.

        :param ers: An ExtractedRouteSequence class instance containing an IFR element record in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: A token being checked if it can follow an IFR point;
        :return: None
        """
        base_type = token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, token, 3)
            case TokenBaseType.F15_SLASH:
                self.forward_slash(ers, tokens, token)
            case TokenBaseType.F15_BREAK_START:
                self.break_start(ers, tokens, token)
            case TokenBaseType.F15_SPEED_VFR | TokenBaseType.F15_SPEED_ALTITUDE:
                self.add_error_and_re_sync(ers, tokens, token, 5)
            case TokenBaseType.F15_BREAK_END:
                self.break_end_error(ers, tokens, token)
            case TokenBaseType.F15_DCT:
                self.dct(ers, tokens, token)
            case TokenBaseType.F15_STAY:
                self.stay(ers, tokens, token)
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_C:
                self.cruise_climb_c(ers, tokens, token)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, token)
            case TokenBaseType.F15_ROUTE:
                last_ers_rec = ers.get_last_element()
                sub_type = last_ers_rec.get_sub_type()
                if sub_type == TokenSubType.F15_SB_PRP_BD or sub_type == TokenSubType.F15_SB_LL_DEG or \
                   sub_type == TokenSubType.F15_SB_LL_MIN or sub_type == TokenSubType.F15_SB_LLBD_DEG or \
                   sub_type == TokenSubType.F15_SB_LLBD_MIN:
                    self.add_error_and_re_sync(ers, tokens, token, 47)
                else:
                    self.route(ers, tokens, token)
            case TokenBaseType.F15_SID_STAR:
                self.sid_star(ers, tokens, token)
            case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE | TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                self.add_error_and_re_sync(ers, tokens, token, 9)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, token, 4)
            case TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, token, 10)
            case TokenBaseType.F15_SID:
                self.sid(ers, tokens, token)
            case TokenBaseType.F15_STAR:
                self.star(ers, tokens, token)
            case _:
                self.add_error_and_re_sync(ers, tokens, token, 0)

    def post_sid(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> None
        """This method determines the next node to move to following an SID element.

        :param ers: An ExtractedRouteSequence class instance containing an SID element record in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure contains
               a tokenized form of all field 15 tokens used as input to this parser.
        :return: A token being checked if it can follow an SID element;
        """
        # Get the next token and determine the next node
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, next_token)
            case TokenBaseType.F15_ROUTE:
                self.route(ers, tokens, next_token)
            case TokenBaseType.F15_SID_STAR:
                self.sid_star(ers, tokens, next_token)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, next_token, 4)
            case TokenBaseType.F15_SID:
                self.add_error_and_re_sync(ers, tokens, next_token, 32)
            case TokenBaseType.F15_STAR:
                self.star(ers, tokens, next_token)
            case _:
                # TokenBaseType.F15_UNKNOWN | TokenBaseType.F15_SLASH |
                # TokenBaseType.F15_BREAK_START | TokenBaseType.F15_SPEED_VFR |
                # TokenBaseType.F15_SPEED_ALTITUDE | TokenBaseType.F15_BREAK_END |
                # TokenBaseType.F15_DCT | TokenBaseType.F15_STAY |
                # TokenBaseType.F15_C | TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE |
                # TokenBaseType.F15_SPEED_ALTITUDE_PLUS | TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, next_token, 31)

    def point(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a point element. Points are always IFR elements, hence the rules are always
        set to IFR on point elements and stored in the ERS. The angle semantics for Latitude / Longitude and
        bearing distance points are checked with appropriate errors reported if semantic errors exist.

        :param ers: An ExtractedRouteSequence class instance containing an IFR element record in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: A point token being appended to the ERS;
        :return: None
        """
        self.add_record(ers, token)
        ers.get_last_element().set_flight_rules(self.RULES["I"])

        # Check lat/long and bearing distance semantics
        if token.get_token_sub_type() != TokenSubType.F15_SB_PRP and \
                token.get_token_sub_type() != TokenSubType.F15_SB_PRP_AERO:
            self.assign_lat_long_bearing_distance(ers, token)

        next_token = tokens.get_next_token()
        if next_token is None:
            return

        self.post_point(ers, tokens, next_token)

    def resolve_real_bd_point(self, ers, ex_route_rec, bearing, distance):
        # type: (ExtractedRouteSequence, ExtractedRouteRecord, float, float) -> None
        """This method calculates the coordinates for a point given by a Lat / Long / Bearing / Distance

        :param ers: The complete extracted route sequence;
        :param ex_route_rec: The extracted route record containing the lat/long of the point to which the
               bearing / distance relate.
        :param bearing: The bearing from the point along which the point to be calculated lies.
        :param distance: The distance along the bearing where the point lies;
        :return: None
        """
        result = Utils().get_bearing_distance_projected_point(
            ex_route_rec.get_latitude(), ex_route_rec.get_longitude(),
            bearing, distance * Constants.NM_TO_METERS)
        ex_route_rec.set_latitude(result[0])
        ex_route_rec.set_longitude(result[1])
        self.assign_azimuth_distance_between_points(ers)

    def re_sync_parser_after_error(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> None
        """This method attempts to re-synchronize the parser after an error is reported. This method is called
        whenever an error is reported / added by the 'self.add_error()' method. The next token is retrieved
        and based on its type, after which parsing continues based on the next tokens element type.

        :param ers: An ExtractedRouteSequence class instance containing an erroneous element record in
               the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :return: None
        """
        token = tokens.get_next_token()
        if token is None:
            return
        base_type = token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, token, 3)
            case TokenBaseType.F15_SLASH:
                # Skip the '/' token, only interested in what follows
                next_token = tokens.get_next_token()
                if next_token is None:
                    # Field 15 cannot end with a '/'
                    self.add_error_and_re_sync(ers, tokens, token, 25)
                    return
                next_base_type = next_token.get_token_base_type()
                match next_base_type:
                    case TokenBaseType.F15_SPEED_VFR:
                        self.assign_speed_vfr(ers, tokens, next_token)
                    case TokenBaseType.F15_POINT:
                        self.point(ers, tokens, next_token)
                    case TokenBaseType.F15_SPEED_ALTITUDE:
                        self.assign_speed_altitude(ers, tokens, next_token)
                    case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE:
                        self.assign_speed_altitude_altitude(ers, tokens, next_token)
                    case TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                        self.assign_speed_altitude_plus(ers, tokens, next_token)
                    case _:
                        self.add_error_and_re_sync(ers, tokens, next_token, 11)
            case TokenBaseType.F15_BREAK_START:
                self.break_start(ers, tokens, token)
            case TokenBaseType.F15_SPEED_VFR:
                self.assign_speed_vfr(ers, tokens, token)
            case TokenBaseType.F15_BREAK_END:
                self.break_end(ers, tokens, token)
            case TokenBaseType.F15_DCT:
                self.dct(ers, tokens, token)
            case TokenBaseType.F15_STAY:
                self.stay(ers, tokens, token)
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_C:
                self.cruise_climb_c(ers, tokens, token)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, token)
            case TokenBaseType.F15_ROUTE:
                self.route(ers, tokens, token)
            case TokenBaseType.F15_SID_STAR:
                self.sid_star(ers, tokens, token)
            case TokenBaseType.F15_SPEED_ALTITUDE:
                self.assign_speed_altitude(ers, tokens, token)
            case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE:
                self.assign_speed_altitude_altitude(ers, tokens, token)
            case TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                self.assign_speed_altitude_plus(ers, tokens, token)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, token, 4)
            case TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, token, 10)
            case TokenBaseType.F15_SID:
                self.sid(ers, tokens, token)
            case TokenBaseType.F15_STAR:
                self.star(ers, tokens, token)
            case _:
                # In theory this should never happen
                self.add_error_and_re_sync(ers, tokens, token, 0)

    def route(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes an ATS route element. Routes are always IFR elements, hence the rules are
        always set to IFR on route elements and stored in the ERS.

        :param ers: An ExtractedRouteSequence class instance containing an IFR element record in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: An ATS route token being appended to the ERS;
        :return: None
        """
        self.add_record(ers, token)
        ers.get_last_element().set_flight_rules(self.RULES["I"])
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, next_token, 3)
            case TokenBaseType.F15_SLASH:
                self.add_error_and_re_sync(ers, tokens, next_token, 12)
            case TokenBaseType.F15_BREAK_START:
                self.add_error_and_re_sync(ers, tokens, next_token, 13)
            case TokenBaseType.F15_SPEED_VFR:
                self.add_error_and_re_sync(ers, tokens, next_token, 13)
            case TokenBaseType.F15_SPEED_ALTITUDE:
                self.add_error_and_re_sync(ers, tokens, next_token, 55)
            case TokenBaseType.F15_BREAK_END:
                self.break_end_error(ers, tokens, next_token)
            case TokenBaseType.F15_DCT:
                self.add_error_and_re_sync(ers, tokens, next_token, 14)
            case TokenBaseType.F15_STAY:
                self.add_error_and_re_sync(ers, tokens, next_token, 15)
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_C:
                self.cruise_climb_c(ers, tokens, next_token)
            case TokenBaseType.F15_POINT:
                # A Lat/Long point cannot follow an ATS route
                sub_type = next_token.get_token_sub_type()
                if sub_type == TokenSubType.F15_SB_PRP_BD or sub_type == TokenSubType.F15_SB_LL_DEG or \
                    sub_type == TokenSubType.F15_SB_LL_MIN or sub_type == TokenSubType.F15_SB_LLBD_DEG or \
                        sub_type == TokenSubType.F15_SB_LLBD_MIN:
                    self.add_error_and_re_sync(ers, tokens, next_token, 48)
                self.point(ers, tokens, next_token)
            case TokenBaseType.F15_ROUTE:
                self.add_error_and_re_sync(ers, tokens, next_token, 53)
            case TokenBaseType.F15_SID_STAR | TokenBaseType.F15_STAR:
                self.add_error_and_re_sync(ers, tokens, next_token, 54)
            case TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE | TokenBaseType.F15_SPEED_ALTITUDE_PLUS:
                self.add_error_and_re_sync(ers, tokens, next_token, 9)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, next_token, 4)
            case TokenBaseType.F15_STAY_TIME:
                self.add_error_and_re_sync(ers, tokens, next_token, 10)
            case TokenBaseType.F15_SID:
                self.add_error_and_re_sync(ers, tokens, next_token, 30)
            case _:
                self.add_error_and_re_sync(ers, tokens, next_token, 0)

    @staticmethod
    def set_azimuth_and_distance(point_1, point_2):
        # type: (ExtractedRouteRecord, ExtractedRouteRecord) -> None
        """This method sets a bearing / azimuth and distance from a point 'point_1' to point 'point_2'.

        :param point_1: The point that will have the bearing / azimuth and distance set that provides the
               azimuth and distance from this point to point_2.
        :param point_2: The second point to calculate the azimuth and distance to.
        :return: None
        """
        azimuth_distance = Utils().get_bearing_distance_between_points(
            point_1.get_latitude(), point_1.get_longitude(),
            point_2.get_latitude(), point_2.get_longitude())
        point_1.set_bearing(azimuth_distance[0])
        point_1.set_distance(azimuth_distance[1])

    def sid(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes an SID token that must be the token following the ADEP. Any other location
        in field 15 will result in an error.

        :param ers: An ExtractedRouteSequence class instance containing only the ADEP (no error case) or any
               other element type (error case) record in the last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: An SID token being appended to the ERS;
        :return: None
        """
        self.add_record(ers, token)

        # The SID must be the second record in the ERS following the ADEP
        if ers.get_number_of_elements() == 2:
            sid_rec = ers.get_element_at(1)
            if sid_rec.get_name() == "SID":
                sid_rec.set_base_type(TokenBaseType.F15_SID)
                sid_rec.set_sub_type(TokenSubType.F15_SB_SID_LITERAL)
            else:
                sid_rec.set_base_type(TokenBaseType.F15_SID)
                sid_rec.set_sub_type(TokenSubType.F15_SB_SID)
            self.post_sid(ers, tokens)
        else:
            self.add_error_and_re_sync(ers, tokens, token, 30)

    def sid_star(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes an element which matches the syntax for both a SID or STAR element; the
        syntax cannot be used to uniquely identify which element type it is. The exact type can only be
        determined by its position in field 15. The SID must be the first token in the list of tokens and
        the STAR the last. If the element appears anywhere else in the token list it is an error.

        :param ers: An ExtractedRouteSequence class instance containing only the ADEP or an IFR element that
               is assumed to be the penultimate element in field 15 as the last ERS record (no error case)
               or the SID/STAR element is in the middle of the field 15 token list (error case).
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: An SID or STAR token being appended to the ERS;
        :return: None
        """
        ex_route_rec = self.add_record(ers, token)

        # The SID must be the second record in the ERS following the ADEP
        if ers.get_number_of_elements() == 2:
            # ERS record after the ADEP, so it must be a SID
            if token.get_token_string() == "SID":
                ex_route_rec.set_base_type(TokenBaseType.F15_SID)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_SID_LITERAL)
            else:
                ex_route_rec.set_base_type(TokenBaseType.F15_SID)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_SID)
            # Figure out which node to go to next
            self.post_sid(ers, tokens)
        elif tokens.peek_next_token(1) is None:
            # No more tokens left so this must be the last token that
            # implies this is a STAR
            if token.get_token_string() == "STAR":
                ex_route_rec.set_base_type(TokenBaseType.F15_STAR)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_STAR_LITERAL)
            else:
                ex_route_rec.set_base_type(TokenBaseType.F15_STAR)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_STAR)
        else:
            self.add_error_and_re_sync(ers, tokens, tokens.peek_next_token(1), 34)

    def star(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a STAR token that must be the last token in the list of tokens. Any other
        location in field 15 will result in an error.

        :param ers: An ExtractedRouteSequence class instance containing an IFR element as its last record
               that is assumed to be the penultimate element in field 15 (no error case) or the STAR element is
               in the middle of the field 15 token list (error case).
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: A STAR token being appended to the ERS;
        :return: None
        """
        ex_route_rec = self.add_record(ers, token)

        # The STAR must be the last record in the ERS
        if tokens.peek_next_token(1) is None:
            # No more tokens left so this must be the last token that
            # implies this is a STAR
            if token.get_token_string() == "STAR":
                ex_route_rec.set_base_type(TokenBaseType.F15_STAR)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_STAR_LITERAL)
            else:
                ex_route_rec.set_base_type(TokenBaseType.F15_STAR)
                ex_route_rec.set_sub_type(TokenSubType.F15_SB_STAR)
        else:
            self.add_error_and_re_sync(ers, tokens, tokens.peek_next_token(1), 34)

    def stay(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a STAY token that indicates a 'stay' time at an IFR point preceding the
        STAY token. The method checks the correct token sequence, i.e. Stay -> '/' -> HHMM. Errors are
        reported if the sequence is incorrect.

        :param ers: An ExtractedRouteSequence class instance containing an IFR point element as its last ERS record.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: A STAY token being appended to the ERS;
        :return: None
        """
        # The STAY token does not have to be stored,
        # skip it and get what should be a forward slash
        next_token = tokens.get_next_token()
        if next_token is None:
            self.add_error_and_re_sync(ers, tokens, token, 35)
            return

        # The next token must be a forward slash
        if next_token.get_token_base_type() is not TokenBaseType.F15_SLASH:
            self.add_error_and_re_sync(ers, tokens, next_token, 36)
            return

        # Skip the forward slash and get the HHMM token
        current_token = next_token
        next_token = tokens.get_next_token()
        if next_token is None:
            self.add_error_and_re_sync(ers, tokens, current_token, 37)
            return

        # The next token must be a HHMM token
        current_token = next_token
        if next_token.get_token_base_type() is not TokenBaseType.F15_STAY_TIME:
            self.add_error_and_re_sync(ers, tokens, current_token, 38)
            return

        # Process the HHMM token
        self.stay_time(ers, tokens, next_token)

    def stay_time(self, ers, tokens, token):
        # type: (ExtractedRouteSequence, Tokens, Token) -> None
        """This method processes a stay HHMM token that provides the duration at a 'stay' point. The method
        saves the HHMM token to the ERS and determines the next processing node after the HHMM TOKEN.

        :param ers: An ExtractedRouteSequence class instance containing an IFR point element as its last ERS
               record on which the stay time will be stored in minutes.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :param token: A stay HHMM token being saved on the last ERS point record;
        :return: None
        """
        # Save the HHMM token to the previous ERS element, which must be a point
        ers.get_last_element().set_stay_time(token.get_token_string())

        # Get the next token
        next_token = tokens.get_next_token()
        if next_token is None:
            return

        # Determine the next node
        base_type = next_token.get_token_base_type()
        match base_type:
            case TokenBaseType.F15_UNKNOWN:
                self.add_error_and_re_sync(ers, tokens, next_token, 3)
            case TokenBaseType.F15_BREAK_START:
                self.break_start(ers, tokens, next_token)
            case TokenBaseType.F15_BREAK_END:
                self.break_end_error(ers, tokens, next_token)
            case TokenBaseType.F15_DCT:
                self.dct(ers, tokens, next_token)
            case TokenBaseType.F15_TRUNCATE:
                self.truncate(ers, tokens)
            case TokenBaseType.F15_C:
                self.cruise_climb_c(ers, tokens, next_token)
            case TokenBaseType.F15_POINT:
                self.point(ers, tokens, next_token)
            case TokenBaseType.F15_ROUTE:
                self.route(ers, tokens, next_token)
            case TokenBaseType.F15_SID_STAR:
                self.sid_star(ers, tokens, next_token)
            case TokenBaseType.F15_TOO_LONG:
                self.add_error_and_re_sync(ers, tokens, next_token, 4)
            case TokenBaseType.F15_SID:
                self.sid(ers, tokens, next_token)
            case TokenBaseType.F15_STAR:
                self.star(ers, tokens, next_token)
            case _:
                # TokenBaseType.F15_SLASH | TokenBaseType.F15_SPEED_VFR |
                # TokenBaseType.F15_SPEED_ALTITUDE | TokenBaseType.F15_STAY |
                # TokenBaseType.F15_SPEED_ALTITUDE_ALTITUDE | TokenBaseType.F15_SPEED_ALTITUDE_PLUS |
                # TokenBaseType.F15_STAY_TIME
                self.add_error_and_re_sync(ers, tokens, next_token, 39)

    def truncate(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> None
        """This method processes the 'T' truncate field 15 token. The 'T' character indicates that the
        field 15 has been truncated. No elements should occur after this element. The 'T' is not saved
        to the ERS. If there are any other tokens following the 'T' an error is reported.

        :param ers: An ExtractedRouteSequence class instance containing the last processed element
               irrespective of its type.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :return: A token being processed to determine if field 15 is being correctly truncated;
        """
        next_token = tokens.get_next_token()
        if next_token is None:
            return
        self.add_error_and_re_sync(ers, tokens, next_token, 19)

    def v_to_i_rule_change(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> None
        """This method executes a rule change from VFR to IFR. To complete this rule change there has to be
        a point, a slash '/' and a SPEED/LEVEL following the IFR rule change element. The method break_end()
        performs a look-ahead from the IFR token to ensure these tokens are present and then calls this method.

        This method assumes all the required tokens are available in the Tokens list to copy the rule
        change elements to the ERS.

        :param ers: An ExtractedRouteSequence class instance with the last record containing the VFR item
               onto which all and any break text are copied.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :return: None
        """
        # Get the point for the rule change
        token = tokens.get_next_token()
        ex_route_rec = self.add_record(ers, token)

        # Check lat/long and bearing distance semantics
        if token.get_token_sub_type() != TokenSubType.F15_SB_PRP and \
                token.get_token_sub_type() != TokenSubType.F15_SB_PRP_AERO:
            self.assign_lat_long_bearing_distance(ers, token)

        # As this rule change is VFR to IFR and this is a speed altitude element,
        # the rules must be IFR
        ex_route_rec.set_flight_rules(self.RULES["I"])

        # Next comes the '/' token, skip this as this is not saved
        tokens.get_next_token()

        # Now comes the SPEED/ALTITUDE token
        token = tokens.get_next_token()
        self.assign_speed_altitude(ers, tokens, token)

    def v_to_i_to_v_rule_change(self, ers, tokens):
        # type: (ExtractedRouteSequence, Tokens) -> None
        """This method processes a rule change from VFR to IFR occurs but the IFR point changes back to VFR,
        i.e. a single point IFR section. This method executes a rule change from VFR to IFR and back to VFR.
        To complete this rule change there has to be a point, a slash '/' and a SPEED/VFR following the IFR
        rule change element. The method break_end() performs a look-ahead from the IFR token to ensure
        these tokens are present and then calls this method.

        This method assumes all the required tokens are available in the Tokens list to copy the rule change
        elements to the ERS.

        :param ers: An ExtractedRouteSequence class instance with the last record containing the VFR item
               onto which all and any break text are copied.
        :param tokens: A list of tokens extracted from field 15 used as input to the parser. This structure
               contains a tokenized form of all field 15 tokens used as input to this parser.
        :return: None
        """
        # Get the point for the rule change
        token = tokens.get_next_token()
        ex_route_rec = self.add_record(ers, token)

        # As this rule change is VFR to IFR and this is a speed altitude element,
        # the rules must be IFR
        ex_route_rec.set_flight_rules(self.RULES["I"])

        # Next comes the '/' token, skip this as this is not saved
        tokens.get_next_token()

        # Now comes the SPEED/VFR token
        token = tokens.get_next_token()
        self.assign_speed_vfr(ers, tokens, token)

    @staticmethod
    def assign_syntax_descriptions(tokens):
        # type: (Tokens) -> None
        """ This method loops over all the tokens produced by the Tokenizer and assigns a token base and
        subtype to each token. The type definitions are obtained from the definitions in the
        'F15TokenSyntaxDescriptions' class.
        :param tokens: The tokens being looped over having their base and subtypes assigned;
        :return: None
        """
        f15tsa = F15TokenSyntaxDefinition()
        for token in tokens.get_tokens():
            token_string = token.get_token_string()
            result = f15tsa.get_token_type(token_string)
            token.set_token_base_type(result[F15TokenSyntaxDefinition.TOKEN_BASE_IDENTIFIER_IDX])
            token.set_token_sub_type(result[F15TokenSyntaxDefinition.TOKEN_SUBTYPE_IDENTIFIER_IDX])
            if len(token_string) > F15TokenSyntaxDefinition.MAX_TOKEN_LENGTH:
                token.set_token_base_type(TokenBaseType.F15_TOO_LONG)
                token.set_token_sub_type(TokenSubType.F15_SB_UNKNOWN)
