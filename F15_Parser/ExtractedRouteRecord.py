class ExtractedRouteRecord:
    # A string representing a route element
    string = ""

    # The start index of a route element's location into the original field 15 source text
    start_index = 0

    # The end index of a route element's location into the original field 15 source text
    end_index = 0

    # Contains one of the element base type definitions (Point, Connector, Modifier
    # etc.) as defined in the 'f15_descriptions.elementBaseType' class.
    base_type = 0

    # Contains one of the element subtype definitions (TASRFL, MACHVFR, Point,
    # Aerodrome etc.) as defined in the 'f15_descriptions.elementSubType' class.
    sub_type = 0

    # The altitude as extracted from a field 15 altitude element
    altitude = ""

    # The altitude converted into SI units in meters
    altitude_si = 0

    # The speed as extracted from a field 15 altitude element
    speed = ""

    # The speed converted into SI units in meters / second
    speed_si = 0

    # Free text as entered after the VFR element or other break elements
    # defined by EURO-CONTROL IFPS
    break_text = ""

    # Flight rules at given route elements
    flight_rules = ""

    # Error reported for this token / record (if an error is reported)
    error_text = ""

    # Stay time in minutes assigned at a point record
    stay_time = 0

    # Target altitude to cruise to for a cruise climb element
    altitude_cruise_to = ""

    # Target altitude in SI units to cruise to for a cruise climb element
    altitude_cruise_to_si = 0

    # Point latitude as a decimal degree
    latitude = 0.0

    # Point longitude as a decimal degree
    longitude = 0.0
    
    # Bearing in decimal degrees between two ERS point records
    bearing = 0.0
    
    # Distance in meters between two ERS points
    distance = 0.0

    # Indicates if a latitude and longitude are available for a point
    lat_long_valid = False

    # Creates a route element with its text, start, end index and both element types
    def __init__(self, string="", start_index=0, end_index=0,
                 base_type=0, sub_type=0):
        self.string = string
        self.start_index = start_index
        self.end_index = end_index
        self.base_type = base_type
        self.sub_type = sub_type

    # Appends a route elements break text
    def append_break_text(self, break_text):
        # type: (str) -> None
        if self.break_text == "":
            self.break_text = break_text
        else:
            self.break_text = self.break_text + " " + break_text

    # Appends a route elements error text
    def append_error_text(self, error_text):
        # type: (str) -> None
        if self.error_text == "":
            self.error_text = error_text
        else:
            self.error_text = self.error_text + " " + error_text

    # Gets a route elements altitude
    def get_altitude(self):
        # type: () -> str
        return self.altitude

    # Gets a route elements target cruise climb altitude
    def get_altitude_cruise_to(self):
        # type: () -> str
        return self.altitude_cruise_to

    # Gets a route elements target cruise climb altitude in SI units
    def get_altitude_cruise_to_si(self):
        # type: () -> float
        return self.altitude_cruise_to_si

    # Gets a route elements altitude in SI units
    def get_altitude_si(self):
        # type: () -> float
        return self.altitude_si

    # Gets a route elements base type
    def get_base_type(self):
        # type: () -> int
        return self.base_type

    # Gets the bearing from a point record to the next point record
    def get_bearing(self):
        # type: () -> float
        return self.bearing

    # Gets a route elements break text
    def get_break_text(self):
        # type: () -> str
        return self.break_text

    # Gets the distance from a point record to the next point record
    def get_distance(self):
        # type: () -> float
        return self.distance

    # Gets a route elements end index
    def get_end_index(self):
        # type: () -> int
        return self.end_index

    # Gets a route elements error text
    def get_error_text(self):
        # type: () -> str
        return self.error_text

    # Gets a route elements flight rules
    def get_flight_rules(self):
        # type: () -> str
        return self.flight_rules

    # Gets the latitude for a points position
    def get_latitude(self):
        # type: () -> float
        return self.latitude

    # Gets the longitude for a points position
    def get_longitude(self):
        # type: () -> float
        return self.longitude

    # Gets a route elements text
    def get_name(self):
        # type: () -> str
        return self.string

    # Gets a route elements speed
    def get_speed(self):
        # type: () -> str
        return self.speed

    # Gets a route elements speed in SI units
    def get_speed_si(self):
        # type: () -> float
        return self.speed_si

    # Gets a route elements start index
    def get_start_index(self):
        # type: () -> int
        return self.start_index

    # Gets the STAY time in minutes assigned to a point
    def get_stay_time(self):
        # type: () -> int
        return self.stay_time

    # Gets a route elements subtype
    def get_sub_type(self):
        # type: () -> int
        return self.sub_type

    # Gets the flag indicating if a latitude and longitude are available
    # for a point
    def is_lat_long_valid(self):
        # type: () -> bool
        return self.lat_long_valid

    # Sets a route elements altitude
    def set_altitude(self, altitude):
        # type: (str) -> None
        self.altitude = altitude

    # Sets a route elements altitude
    def set_altitude_cruise_to(self, altitude_cruise_to):
        # type: (str) -> None
        self.altitude_cruise_to = altitude_cruise_to

    # Sets a route elements altitude
    def set_altitude_cruise_to_si(self, altitude_cruise_to_si):
        # type: (float) -> None
        self.altitude_cruise_to_si = altitude_cruise_to_si

    # Sets a route elements altitude in SI units
    def set_altitude_si(self, altitude_si):
        # type: (float) -> None
        self.altitude_si = altitude_si

    # Sets a route elements base type
    def set_base_type(self, base_type):
        # type: (int) -> None
        self.base_type = base_type

    # Sets a bearing between two point records
    def set_bearing(self, bearing):
        # type: (float) -> None
        self.bearing = bearing

    # Sets a route elements break text
    def set_break_text(self, break_text):
        # type: (str) -> None
        self.break_text = break_text

    # Sets the distance between two point records on a point record
    def set_distance(self, distance):
        # type: (float) -> None
        self.distance = distance

    # Sets a route elements end index
    def set_end_index(self, end_index):
        # type: (int) -> None
        self.end_index = end_index

    # Sets a route elements error text
    def set_error_text(self, error_text):
        # type: (str) -> None
        self.error_text = error_text

    # Sets a route elements flight rules
    def set_flight_rules(self, flight_rules):
        # type: (str) -> None
        self.flight_rules = flight_rules

    # Sets a latitude for a points position
    def set_latitude(self, latitude):
        # type: (float) -> None
        self.latitude = latitude

    # Sets the flag indicating that both a latitude and longitude are available
    # for a point
    def set_lat_long_valid(self, lat_long_valid):
        # type: (bool) -> None
        self.lat_long_valid = lat_long_valid

    # Sets a longitude for a points position
    def set_longitude(self, longitude):
        # type: (float) -> None
        self.longitude = longitude

    # Sets a route elements text
    def set_name(self, string):
        # type: (str) -> None
        self.string = string

    # Sets a route elements speed
    def set_speed(self, speed):
        # type: (str) -> None
        self.speed = speed

    # Sets a route elements speed in SI units
    def set_speed_si(self, speed_si):
        # type: (float) -> None
        self.speed_si = speed_si

    # Sets a route elements start index
    def set_start_index(self, start_index):
        # type: (int) -> None
        self.start_index = start_index

    # Sets the stay time, input argument is a string in HHMM,
    # this method converts and stores this as minutes
    def set_stay_time(self, stay_time):
        # type: (str) -> None
        self.stay_time = (int(stay_time[0:2]) * 60) + int(stay_time[2:])

    # Sets a route elements subtype
    def set_sub_type(self, sub_type):
        # type: (int) -> None
        self.sub_type = sub_type

    def print_record(self, error):
        # type: (bool) -> None
        print(self.to_string(error))

    def unit_test_only(self):
        # type: () -> str
        # Used only for Unit testing comparison
        str_ = self.get_name() + " " + \
               self.get_flight_rules() + " " + \
               self.get_speed() + " " + \
               self.get_altitude() + " " + \
               self.get_break_text() + " " + \
               self.get_error_text()
        return str_.rstrip(" ")

    def to_string(self, error):
        # type: (bool) -> str
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
