import math

from Utilities.Constants import Constants
from geographiclib.geodesic import Geodesic


class Utils:
    # Define the WGS84 ellipsoid from the geographiclib library
    geode = Geodesic.WGS84

    # Checks semantics of string for degrees
    # Attributes
    # ----------
    # degrees:      A string representing an angle in degrees;
    # max_degrees:  The maximum value the 'degrees' value can take;
    # return:       True if the value in 'degrees' <= max_degrees, False otherwise;
    @staticmethod
    def is_degree_semantics(degrees, max_degrees):
        # type: (str, int) -> bool
        return int(degrees) <= max_degrees

    # Checks semantics of string representing degrees and minutes in either
    # a 'ddmm' or 'dddmm' format.
    # Attributes
    # ----------
    # degrees_minutes:  A 4 or 5 digit string representing an angle in degrees and
    #                   minutes in 'ddmm' or 'dddmm' format;
    # max_degrees:      The maximum value the 'degrees' value can take;
    # return:           True if the value in 'degrees' and 'minutes' <= max_degrees,
    #                   False otherwise;
    @staticmethod
    def is_degree_minute_semantics(degrees_minutes, max_degrees, split):
        # type: (str, int, int) -> bool
        if int(degrees_minutes[0:split]) > max_degrees:
            # Degrees to high
            return False
        if int(degrees_minutes[split:]) > 59:
            # Minutes exceed 59
            return False
        if int(degrees_minutes) > max_degrees * 100:
            # Total integer value exceeds the maximum,
            # i.e. 180 max degrees, means 18000 with degrees and minutes
            return False
        return True

    # This method determines the speed of sound at a given altitude.
    # speed of sound ~= 331.15 m/s * sqrt(T / 273.15K)
    # T = (ISA Temp + (altitude in meters * -lapse temp per meter)) + 273.15K / 273.15K
    # For altitudes above 11,000 meters no further temp drops are calculated with air
    # temperature remaining constant at higher altitudes.
    # Arguments
    # ---------
    # altitude_in_meters: Altitude in meters
    # returns:  Speed of sound at the altitude given by the input argument altitude_in_meters
    @staticmethod
    def speed_of_sound_at_altitude(altitude_in_meters):
        # type: (float) -> float
        if altitude_in_meters > Constants.CONSTANT_TEMP_ALTITUDE:
            altitude_temp = Constants.ISA_TEMP + (Constants.CONSTANT_TEMP_ALTITUDE * Constants.TEMP_LAPSE_RATE_METER)
        else:
            altitude_temp = Constants.ISA_TEMP + (altitude_in_meters * Constants.TEMP_LAPSE_RATE_METER)

        speed_of_sound = (altitude_temp - Constants.KELVIN_ZERO) / abs(Constants.KELVIN_ZERO)
        speed_of_sound = 331.15 * math.sqrt(speed_of_sound)
        return speed_of_sound

    # This method converts a Mach number to meters/second. If the altitude is zero
    # the speed of sound at sea level is used given by the constant
    # MACH_TO_METERS_SECOND.
    # Speed of sound decreases at higher altitudes up to 11,000 meters, after which
    # the speed of sound does not change any more.
    # Arguments
    # ---------
    # mach_number: The Mach number speed given as an integer, e.g. 82 is Mach 0.82
    # altitude_si = Altitude im meters
    # returns:  Speed of sound at the altitude given by the input argument altitude_in_meters
    @staticmethod
    def mach_to_ms_speed(mach_number, altitude_si):
        # type: (float, float) -> float
        # Mach number to the nearest hundredth of unit Mach, e.g. M082 = Mach 0.82
        if altitude_si == 0:
            # Use speed of sound at sea level
            return (mach_number / 100) * Constants.MACH_TO_METERS_SECOND
        else:
            # Use speed of sound at given altitude
            return (mach_number / 100) * Utils.speed_of_sound_at_altitude(altitude_si)

    # This method returns a point latitude/longitude calculated from a
    # point / bearing / distance. The return value is a list with two elements
    # containing the latitude and longitude of the calculated point.
    # Arguments
    # ---------
    # latitude:     Latitude of a point from which a projected point's coordinates will
    #               be calculated using the bearing and distance arguments.
    # longitude:    Longitude of a point from which a projected point's coordinates will
    #               be calculated using the bearing and distance arguments.
    # bearing:      Azimuth from a point specified by the latitude and longitude that
    #               is used to calculate a projected point from the latitude / longitude
    #               point along this bearing at a distance given by the distance argument.
    # distance:     Distance along a bearing given by the bearing argument that
    #               is used to calculate a projected point from the latitude / longitude
    #               point given by the latitude / longitude arguments.
    # returns:      A list containing two items, index 0 the latitude, index 1 the longitude
    #               of the projected point calculated by this method.
    def get_bearing_distance_projected_point(self, latitude, longitude, bearing, distance):
        # type: (float, float, float, float) -> []
        result = self.geode.Direct(latitude, longitude, bearing, distance)
        return [result['lat2'], result['lon2']]

    # This method calculates the bearing and distance between two points given by
    # the arguments' latitude_1, longitude_1 and latitude_2, longitude_2.
    # Arguments
    # ---------
    # latitude_1:   The latitude of the first point.
    # longitude_1:  The longitude of the first point.
    # latitude_2:   The latitude of the second point.
    # longitude_2:  The longitude of the second point.
    # returns:      A list containing two elements:
    #               - Index 1 the azimuth from point 1 to point 2;
    #               - Index 2 the distance between point 1 and point 2;
    def get_bearing_distance_between_points(self, latitude_1, longitude_1, latitude_2, longitude_2):
        # type: (float, float, float, float) -> []
        result = self.geode.Inverse(latitude_1, longitude_1, latitude_2, longitude_2)
        return [result['azi1'], result['s12']]
