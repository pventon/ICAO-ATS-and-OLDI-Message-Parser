from F15_Parser.F15TokenSyntaxDescriptions import TokenBaseType, TokenSubType


class ExtractedRouteRecord:
    """This class is a single item/record stored in the extracted route sequence.
    This record contains altitude, speed, geographic position (if available in field 15 point data),
    azimuth and distance between points.

    Some class members cannot be initialized if the data is unavailable in field 15. For example,
    no AIP lookup is NOT carried out by this software, if a point is given as a Publish Route Point as
    opposed to a geographic coordinates, then there are no coordinates. If there are no coordinates
    the azimuth and distance between points cannot be calculated. If they are available, the azimuth
    and distance between points is calculated and stored in this record.

    The class members store comprehensive information that together represent a comprehensive
    data set for subsequent route processing."""

    string: str = ""
    """A string representing a route element such as a point, route, STAR, SID etc."""

    start_index: int = 0
    """The start index of a route element's location into the original field 15 source text"""

    end_index: int = 0
    """The end index of a route element's location into the original field 15 source text"""

    base_type: TokenBaseType = 0
    """Contains one of the element base type definitions (Point, Connector, Modifier
    etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenBaseType' class."""

    sub_type: TokenSubType = 0
    """Contains one of the element subtype definitions (TASRFL, MACHVFR, Point,
    Aerodrome etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenSubType' class."""

    altitude: str = ""
    """The altitude as extracted from a field 15 altitude element"""

    altitude_si: float = 0.0
    """The altitude converted into SI units in meters"""

    speed: str = ""
    """The speed as extracted from a field 15 altitude element"""

    speed_si: float = 0.0
    """The speed converted into SI units in meters / second"""

    break_text: str = ""
    """Free text as entered after the VFR element or other break elements
    defined by EURO-CONTROL IFPS"""

    flight_rules: str = ""
    """Flight rules at given route elements"""

    error_text: str = ""
    """Error reported for this token / record (if an error is reported)"""

    stay_time: int = 0
    """Stay time in minutes assigned at a point record"""

    altitude_cruise_to: str = ""
    """Target altitude to cruise to for a cruise climb element"""

    altitude_cruise_to_si: float = 0.0
    """Target altitude in SI units to cruise to for a cruise climb element"""

    latitude: float = 0.0
    """Point latitude as a decimal degree"""

    longitude: float = 0.0
    """Point longitude as a decimal degree"""

    bearing: float = 0.0
    """Bearing in decimal degrees between two ERS point records"""

    distance: float = 0.0
    """Distance in meters between two ERS points"""

    lat_long_valid: bool = False
    """Indicates if a latitude and longitude are available for a point"""

    def __init__(self, string="", start_index=0, end_index=0, base_type=0, sub_type=0):
        # type: (str, int, int, TokenBaseType, TokenSubType) -> None
        """Creates a route element with its text, start, end index and both element types.

            :param string: The field 15 element string;
            :param start_index: The start index of a route element's location in the original field 15 source text
            :param end_index: The end index of a route element's location in the original field 15 source text
            :param base_type: Contains one of the element base type definitions (Point, Connector, Modifier
                              etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenBaseType' class.
            :param sub_type: Contains one of the element base type definitions (Point, Connector, Modifier
                             etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenBaseType' class.
            :return: None"""
        self.string = string
        self.start_index = start_index
        self.end_index = end_index
        self.base_type = base_type
        self.sub_type = sub_type

    #
    def append_break_text(self, break_text):
        # type: (str) -> None
        """This method appends a route elements break text; a route break occurs when IFR routing
        stops such as when routing changes to VFR or OAT traffic. Text that appears following the 'break'
        indicator is not part of the routing data and is treated as free text associated with the point at which
        IFR rules where cancelled.

            :param break_text: The text following a break point to be stored at the point where IFR rules
                               were cancelled.
            :return: None"""
        if self.break_text == "":
            self.break_text = break_text
        else:
            self.break_text = self.break_text + " " + break_text

    def append_error_text(self, error_text):
        # type: (str) -> None
        """This method appends a route elements error text

            :param error_text: The error text to append
            :return: None"""
        if self.error_text == "":
            self.error_text = error_text
        else:
            self.error_text = self.error_text + " " + error_text

    def get_altitude(self):
        # type: () -> str
        """Gets a route elements altitude as a string, this is what appears in field 15,
        e.g. F350.

            :return: The altitude as given in field 15;"""
        return self.altitude

    def get_altitude_cruise_to(self):
        # type: () -> str
        """Gets a route elements target cruise climb altitude, this is what appears in field 15,
        e.g. F350.

            :return: The altitude as given in a field 15 cruise/climb element;"""
        return self.altitude_cruise_to

    def get_altitude_cruise_to_si(self):
        # type: () -> float
        """Gets a route elements target cruise climb altitude in SI units (meters); the SI units are calculated
        from the altitude values found in field 15 cruise/climb data.

            :return: The altitude in SI units converted from a field 15 cruise/climb element;"""
        return self.altitude_cruise_to_si

    def get_altitude_si(self):
        # type: () -> float
        """Gets a route elements altitude in SI units (meters); the SI units are calculated
        from the altitude values found in field 15 altitude data.

            :return: The altitude in SI units converted from field 15 altitude data element;"""
        return self.altitude_si

    def get_base_type(self):
        # type: () -> TokenBaseType
        """Gets a route elements base type (TASRFL, MACHVFR, Point,
        Aerodrome etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenSubType' class.

            :return: A base type as an enumeration value defined the 'F15TokenSyntaxDescriptions.TokenSubType' class."""
        return self.base_type

    def get_bearing(self):
        # type: () -> float
        """Gets the bearing from a point record to the next point record; this value is only available where the
        points both have geographic coordinates available.

            :return: The bearing or azimuth from one point to the next"""
        return self.bearing

    def get_break_text(self):
        # type: () -> str
        """This method gets the break text at a rule change point; a route break occurs when IFR routing
        stops such as when routing changes to VFR or OAT traffic. Text that appears following the 'break'
        indicator is not part of the routing data and is treated as free text associated with the point at which
        IFR rules where cancelled.

            :return: The text following a break point where IFR rules were cancelled."""
        return self.break_text

    def get_distance(self):
        # type: () -> float
        """Gets the distance from a point record to the next point record; this value is only available where the
        points both have geographic coordinates available.

            :return: The distance in meters from one point to the next"""
        return self.distance

    def get_end_index(self):
        # type: () -> int
        """Gets the end index of a route element's location into the original field 15 source text.

            :return: The zero based index where an elements last character + 1 is located in the
                     original field 15 source string;"""
        return self.end_index

    def get_error_text(self):
        # type: () -> str
        """Gets the error text for a token representing an erroneous token.

            :return: The error message text"""
        return self.error_text

    def get_flight_rules(self):
        # type: () -> str
        """Gets a route elements flight rules, (one of 'I', 'V', 'Y' or 'Z');

            :return: The flight rules at this extracted route element"""
        return self.flight_rules

    def get_latitude(self):
        # type: () -> float
        """Gets the latitude for a points position in decimal degrees; this value is calculated from the value
        found in field 15 which is given as degrees and minutes.

            :return: The latitude as a decimal degree value"""
        return self.latitude

    def get_longitude(self):
        # type: () -> float
        """Gets the longitude for a points position in decimal degrees; this value is calculated from the value
        found in field 15 which is given as degrees and minutes.

            :return: The longitude as a decimal degree value"""
        return self.longitude

    def get_name(self):
        # type: () -> str
        """Gets a route elements text as found in field 15, could be a point, latitude/longitude, ATS route
        SID, STAR etc.

            :return: The route element as extracted from field 15"""
        return self.string

    def get_speed(self):
        # type: () -> str
        """Gets a route elements speed as a string, this is what appears in field 15,
        e.g. N0450.

            :return: The speed as given in field 15;"""
        return self.speed

    def get_speed_si(self):
        # type: () -> float
        """Gets a route elements speed in SI units (meters/second); the SI units are calculated
        from the speed values found in field 15 speed data.

            :return: The speed in SI units converted from field 15 speed data element;"""
        return self.speed_si

    def get_start_index(self):
        # type: () -> int
        """Gets the start index of a route element's location into the original field 15 source text.

            :return: The zero based index where an elements first character is located in the
                     original field 15 source string;"""
        return self.start_index

    def get_stay_time(self):
        # type: () -> int
        """Gets the STAY time in minutes assigned to a point; in field 15 the time is given in HHMM format, this is
        converted and stored as an integer value in minutes.

            :return: The stay time in minutes"""
        return self.stay_time

    def get_sub_type(self):
        # type: () -> TokenSubType
        """Gets a route elements subtype (TASRFL, MACHVFR, Point,
        Aerodrome etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenSubType' class.

            :return: A base type as an enumeration value defined the 'F15TokenSyntaxDescriptions.TokenSubType' class."""
        return self.sub_type

    def is_lat_long_valid(self):
        # type: () -> bool
        """Gets the flag indicating if a latitude and longitude are available for a point; if two consecutive
        point have this flag set to True, then the azimuth and distance between the points can be calculated.

            :return: A boolean indicating if a point has the latitude and longitude available;"""
        return self.lat_long_valid

    # Sets a route elements altitude
    def set_altitude(self, altitude):
        # type: (str) -> None
        """Sets a route elements altitude as a string, this is what appears in field 15,
        e.g. F350.

            :param altitude: The altitude value as a string to set;
            :return: None"""
        self.altitude = altitude

    # Sets a route elements altitude
    def set_altitude_cruise_to(self, altitude_cruise_to):
        # type: (str) -> None
        """Sets a route elements target cruise climb altitude, this is what appears in field 15,
        e.g. F350.

            :param altitude_cruise_to: The altitude value as a string to set;
            :return: None"""
        self.altitude_cruise_to = altitude_cruise_to

    # Sets a route elements altitude
    def set_altitude_cruise_to_si(self, altitude_cruise_to_si):
        # type: (float) -> None
        """Sets a route elements target cruise climb altitude in SI units (meters); the SI units are calculated
        from the altitude values found in field 15 cruise/climb data.

            :param altitude_cruise_to_si: The altitude to set in SI units converted from a
                                          field 15 cruise/climb element;
            :return: None"""
        self.altitude_cruise_to_si = altitude_cruise_to_si

    def set_altitude_si(self, altitude_si):
        # type: (float) -> None
        """Sets a route elements altitude in SI units (meters); the SI units are calculated
        from the altitude values found in field 15 altitude data.

            :param : The altitude to set in SI units converted from field 15 altitude data element;
            :return: None"""
        self.altitude_si = altitude_si

    def set_base_type(self, base_type):
        # type: (TokenBaseType) -> None
        """Sets a route elements base type (TASRFL, MACHVFR, Point,
        Aerodrome etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenBaseType' class.

            :param base_type: A base type to set as an enumeration value defined in the
                             'F15TokenSyntaxDescriptions.TokenBaseType' class.
            :return: None"""
        self.base_type = base_type

    def set_bearing(self, bearing):
        # type: (float) -> None
        """Sets the bearing from a point record to the next point record; this value can only be set where two
        consecutive points both have geographic coordinates available.

            :param bearing: The bearing or azimuth, in decimal degrees to set from one point to the next
            :return: None"""
        self.bearing = bearing

    def set_break_text(self, break_text):
        # type: (str) -> None
        """This method sets the break text at a rule change point; a route break occurs when IFR routing
        stops such as when routing changes to VFR or OAT traffic. Text that appears following the 'break'
        indicator is not part of the routing data and is treated as free text associated with the point at which
        IFR rules where cancelled.

            :param : The text to set following a break point where IFR rules were cancelled.
            :return: None"""
        self.break_text = break_text

    def set_distance(self, distance):
        # type: (float) -> None
        """Sets the distance from a point record to the next point record; this value can only be set where two
        consecutive points both have geographic coordinates available.

            :param distance: The distance to set in meters, from one point to the next
            :return: None"""
        self.distance = distance

    def set_end_index(self, end_index):
        # type: (int) -> None
        """Sets the end index of a route element's location in the original field 15 source text.

            :param : The zero based index to set where an elements last character + 1 is located in the
                     original field 15 source string;
            :return: None"""
        self.end_index = end_index

    # Sets a route elements error text
    def set_error_text(self, error_text):
        # type: (str) -> None
        """Sets the error text for a token representing an erroneous token.

            :param error_text: The error message text to set;
            :return: None"""
        self.error_text = error_text

    # Sets a route elements flight rules
    def set_flight_rules(self, flight_rules):
        # type: (str) -> None
        """Sets a route elements flight rules, (one of 'I', 'V', 'Y' or 'Z');

            :param flight_rules: The flight rules to set at this extracted route element;
            :return: None"""
        self.flight_rules = flight_rules

    def set_latitude(self, latitude):
        # type: (float) -> None
        """Sets the latitude for a points position in decimal degrees; this value is calculated from the value
        found in field 15 which is given as degrees and minutes.

            :param latitude: The latitude to set as a decimal degree value;
            :return: None"""
        self.latitude = latitude

    def set_lat_long_valid(self, lat_long_valid):
        # type: (bool) -> None
        """Sets the flag indicating if a latitude and longitude are available for a point; if two consecutive
        point have this flag set to True, then the azimuth and distance between the points can be calculated.

            :param lat_long_valid: Set to True if a point has the latitude and longitude available, False otherwise;
            :return: None"""
        self.lat_long_valid = lat_long_valid

    # Sets a longitude for a points position
    def set_longitude(self, longitude):
        # type: (float) -> None
        """Sets the longitude for a points position in decimal degrees; this value is calculated from the value
        found in field 15 which is given as degrees and minutes.

            :param longitude: The longitude to set as a decimal degree value;
            :return: None"""
        self.longitude = longitude

    def set_name(self, string):
        # type: (str) -> None
        """Sets a route elements text as found in field 15, could be a point, latitude/longitude, ATS route
        SID, STAR etc.

            :param string: The route element to set;
            :return: None"""
        self.string = string

    # Sets a route elements speed
    def set_speed(self, speed):
        # type: (str) -> None
        """Sets a route elements speed as a string, this is what appears in field 15,
        e.g. N0450.

            :param speed: The speed to set as given in field 15;
            :return: None"""
        self.speed = speed

    def set_speed_si(self, speed_si):
        # type: (float) -> None
        """Sets a route elements speed in SI units (meters/second); the SI units are calculated
        from the speed values found in field 15 speed data.

            :param speed_si: The speed to set in SI units converted from field 15 speed data element;
            :return: None"""
        self.speed_si = speed_si

    def set_start_index(self, start_index):
        # type: (int) -> None
        """Sets the start index of a route element's location in the original field 15 source text.

            :param start_index: The zero based index to set where an elements first character is located in the
                     original field 15 source string;
            :return: None"""
        self.start_index = start_index

    # Sets the stay time, input argument is a string in HHMM,
    # this method converts and stores this as minutes
    def set_stay_time(self, stay_time):
        # type: (str) -> None
        """Sets the STAY time in minutes assigned to a point; in field 15 the time is given in HHMM format, this is
        converted and stored as an integer value in minutes.

            :param stay_time: The stay time to set in minutes;
            :return: None"""
        self.stay_time = (int(stay_time[0:2]) * 60) + int(stay_time[2:])

    def set_sub_type(self, sub_type):
        # type: (TokenSubType) -> None
        """Sets a route elements subtype (TASRFL, MACHVFR, Point,
         Aerodrome etc.) as defined in the 'F15TokenSyntaxDescriptions.TokenSubType' class.

             :param sub_type: A subtype to set as an enumeration value defined in the
                              'F15TokenSyntaxDescriptions.TokenSubType' class.
             :return: None"""
        self.sub_type = sub_type

    def print_record(self, error):
        # type: (bool) -> None
        """This method prints either an error record or a normal record depending on the boolean parameter.

            :param error: If True, an error record is printed that will output a record with any error messages,
                          if False a record is output with break text instead of error text. In all other
                          respects the output is identical.
            :return: None"""
        print(self.to_string(error))

    def unit_test_only(self):
        # type: () -> str
        #
        """This method is a helper method only used for Unit testing comparison

            :return: None"""
        str_ = self.get_name() + " " + \
            self.get_flight_rules() + " " + \
            self.get_speed() + " " + \
            self.get_altitude() + " " + \
            self.get_break_text() + " " + \
            self.get_error_text()
        return str_.rstrip(" ")

    def to_string(self, error):
        # type: (bool) -> str
        """This method converts an extracted route record to a formatted string, so it can be printed

            :param error: If True, an error record is printed that will output a record with any error messages,
                          if False a record is output with break text instead of error text. In all other
                          respects the output is identical.
            :return: A string containing a formatted string putting each class member into a 'column'."""
        if error:
            error_or_break = self.get_error_text()
        else:
            error_or_break = self.get_break_text()
        str_ = "{0:<17}".format(self.get_name()) + \
               "{0:>6}".format(self.get_start_index()) + \
               "{0:>6}".format(self.get_end_index()) + \
               "{0:>5}".format(self.get_base_type()) + \
               "{0:>5}".format(self.get_sub_type()) + \
               "{0:>6}".format(self.get_speed()) + \
               "{0:>6}".format(self.get_speed_si()) + \
               "{0:>6}".format(self.get_altitude()) + \
               "{0:>6}".format(self.get_altitude_si()) + \
               "{0:>7.2f}".format(self.get_bearing()) + \
               "{0:>11.2f}".format(self.get_distance()) + \
               "{0:>6}".format(self.get_flight_rules()) + \
               "{0:>5}".format(self.get_stay_time()) + \
               "{0:>7}".format(self.get_altitude_cruise_to()) + \
               "{0:>7}".format(self.get_altitude_cruise_to_si()) + \
               "{0:>7.2f}".format(self.get_latitude()) + \
               "{0:>8.2f}".format(self.get_longitude()) + \
               " {0:<91}".format(error_or_break)
        return str_

    def as_xml(self, error):
        # type: (bool) -> str
        """This method converts an ERS record into an XML string; the method is called from the
        ExtractedRouteSequence class to generate an XML document containing a complete extracted
        route sequence as an XML document.

        :param error: If True, an error record is included containing the associated error message,
               if False, a record is output with break text instead of error text. In all other
               respects the output is identical.
        :return: An XML string representing a single ERS record."""
        if error:
            error_or_break = self.get_error_text()
            rec_type = "error_record"
            attr_name = "error_text"
        else:
            error_or_break = self.get_break_text()
            rec_type = "ers_record"
            attr_name = "break_text"
        return "<" + rec_type + \
               " name=\"" + self.get_name() + "\"" + \
               " start_index=\"" + str(self.get_start_index()) + "\"" + \
               " end_index=\"" + str(self.get_end_index()) + "\"" + \
               " base_type=\"" + str(self.get_base_type()) + "\"" + \
               " sub_type=\"" + str(self.get_sub_type()) + "\"" + \
               " speed=\"" + self.get_speed() + "\"" + \
               " speed_si=\"" + "{0:.2f}".format(self.get_speed_si()) + "\"" + \
               " altitude=\"" + self.get_altitude() + "\"" + \
               " altitude_si=\"" + "{0:.2f}".format(self.get_altitude_si()) + "\"" + \
               " bearing=\"" + "{0:>.2f}".format(self.get_bearing()) + "\"" + \
               " distance=\"" + "{0:>.2f}".format(self.get_distance()) + "\"" + \
               " flight_rules=\"" + self.get_flight_rules() + "\"" + \
               " stay_time=\"" + str(self.get_stay_time()) + "\"" + \
               " altitude_cruise_to=\"" + self.get_altitude_cruise_to() + "\"" + \
               " altitude_cruise_to_si=\"" + "{0:.2f}".format(self.get_altitude_cruise_to_si()) + "\"" + \
               " latitude=\"" + "{0:>.2f}".format(self.get_latitude()) + "\"" + \
               " longitude=\"" + "{0:>.2f}".format(self.get_longitude()) + "\"" + \
               " " + attr_name + "=\"" + error_or_break + "\"" + \
               "></" + rec_type + ">"
