class Constants:
    # Height in meters where temperature laps remains constant
    CONSTANT_TEMP_ALTITUDE = 11000

    # Absolute zer in Kelvin
    KELVIN_ZERO = -273.15

    # International Standard Atmosphere (ISA) temperature @ 1,013.25 mb
    ISA_TEMP = 15.0  # 15.565

    # Temperature Lapse rate degrees / 1,000 feet (304.8 meters)
    # The standard adiabatic lapse rate is where temperatures decrease at the following
    # rates:
    # - 6.5°C per 1,000 meters, or 3.5°F(2°C) per 1,000 ft. – from sea level to 11,000
    #   meters (approximately 36,000 ft.)
    # - From 11,000 meters (approximately 36,000 ft.) up to 20,000 meters (approximately
    #   65,600 ft.), constant
    # Drop in temperature for every meter in altitude (6.45C / 1,000 meters)
    TEMP_LAPSE_RATE_METER = -0.00645

    # Conversion factor feet to meters
    FEET_TO_METERS = 0.3048

    # Conversion factor knots to meters / second
    KNOTS_TO_METERS_SECOND = 0.514444

    # Conversion factor KMH to meters / second
    KMH_TO_METERS_SECOND = 0.2777778

    # Conversion factor Mach number to meters / second at sea level with temp @ 20C
    MACH_TO_METERS_SECOND = 343.0

    # Conversion factor for Nautical Miles to Meters
    NM_TO_METERS = 1852
