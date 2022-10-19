class Constants:
    """This class contains constants used by the ICAO Field 15 Parser"""

    CONSTANT_TEMP_ALTITUDE = 11000
    """Height in meters, above which, where temperature remains constant, (the lapse rate)
    used when calculating a speed in meters/second from a Mach number."""

    KELVIN_ZERO = -273.15
    """Absolute zer in Kelvin, used when calculating a speed in meters/second from a Mach number."""

    ISA_TEMP = 15.0  # 15.565
    """International Standard Atmosphere (ISA) temperature @ 1,013.25 mb, used when calculating
    a speed in meters/second from a Mach number."""

    TEMP_LAPSE_RATE_METER = -0.00645
    """Temperature Lapse rate degrees / 1,000 feet (304.8 meters). The standard adiabatic lapse rate is
    where temperatures decrease at the following rates:
        - 6.5°C per 1,000 meters, or 3.5°F(2°C) per 1,000 ft. – from sea level to 11,000 meters
          (approximately 36,000 ft.)
        - From 11,000 meters (approximately 36,000 ft.) up to 20,000 meters (approximately
          65,600 ft.), constant Drop in temperature for every meter in altitude (6.45C / 1,000 meters)"""

    FEET_TO_METERS = 0.3048
    """Conversion factor feet to meters"""

    KNOTS_TO_METERS_SECOND = 0.514444
    """Conversion factor knots to meters / second"""

    KMH_TO_METERS_SECOND = 0.2777778
    """Conversion factor KMH to meters / second"""

    MACH_TO_METERS_SECOND = 343.0
    """Conversion factor Mach number to meters / second at sea level with temp @ 20C"""

    NM_TO_METERS = 1852
    """Conversion factor for Nautical Miles to Meters"""
