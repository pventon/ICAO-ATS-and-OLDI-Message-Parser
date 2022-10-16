from F15_Parser.ExtractedRouteRecord import ExtractedRouteRecord
from F15_Parser.F15TokenSyntaxDescriptions import TokenBaseType, TokenSubType


class ExtractedRouteSequence:
    # A list of extracted route records
    extracted_route_records = []

    # A list of extracted route items with errors
    error_records = []

    # Constructor without any initialized token
    def __init__(self):
        # Clear everything, ensures class can be 're-used'
        self.extracted_route_records = []
        self.error_records = []
        # Create a dummy record that will be used for the ADEP
        self.add_dummy_adep_ades("ADEP")

    # Adds a dummy record for the ADEP or ADES
    def add_dummy_adep_ades(self, aero):
        # type: (str) -> ExtractedRouteRecord
        # Create a dummy record that will be used for the ADES
        return self.create_append_element(aero, 0, 0, TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP_AERO)

    # Adds a dummy ADES record
    def add_dummy_ades(self):
        # type: () -> ExtractedRouteRecord
        return self.add_dummy_adep_ades("ADES")

    # Add an error record
    def add_error(self, element_text, element_start_index, element_end_index,
                  element_base_type, element_sub_type, error_message):
        # type: (str, int, int, int, int, str) -> None
        err_record = ExtractedRouteRecord(element_text, element_start_index,
                                          element_end_index, element_base_type,
                                          element_sub_type)
        err_record.append_error_text(error_message.replace("!", element_text))
        self.error_records.append(err_record)

    # Appends a route element to this class instance
    def append_element(self, element):
        # type: (ExtractedRouteRecord) -> ExtractedRouteRecord
        self.extracted_route_records.append(element)
        return self.get_last_element()

    # Creates and appends a route element to this class instance with discreet attributes
    def create_append_element(self, element_text, element_start_index, element_end_index,
                              element_base_type, element_sub_type):
        # type: (str, int, int, int, int) -> ExtractedRouteRecord
        return self.append_element(ExtractedRouteRecord(element_text, element_start_index,
                                                        element_end_index, element_base_type,
                                                        element_sub_type))

    # Returns the list of extracted route records
    def get_all_elements(self):
        # type: () -> []
        return self.extracted_route_records

    # Get the list with all errors
    def get_all_errors(self):
        # type: () -> []
        return self.error_records

    # Retrieves a route element at 'index', or returns 'None' if 'index' is out of range
    def get_element_at(self, index):
        # type: (int) -> ExtractedRouteRecord | None
        if index < 0 or index > self.get_number_of_elements():
            return None
        return self.extracted_route_records[index]

    # Get the first ERS element
    def get_first_element(self):
        # type: () -> ExtractedRouteRecord
        return self.get_element_at(0)

    # Get the last ERS element, returns None if the list is empty
    def get_last_element(self):
        # type: () -> ExtractedRouteRecord | None
        if self.get_number_of_elements() > 0:
            return self.get_element_at(self.get_number_of_elements() - 1)
        else:
            return None

    # Get the number of extracted route records
    def get_number_of_elements(self):
        # type: () -> int
        return len(self.extracted_route_records)

    # Get the number of error records
    def get_number_of_errors(self):
        # type: () -> int
        return len(self.error_records)

    # Get the previous element to the current element
    def get_previous_to_last_element(self):
        # type: () -> ExtractedRouteRecord
        return self.get_element_at(self.get_number_of_elements() - 2)

    def print_ers(self):
        # type: () -> None
        print("Total Number of Extracted Route Records: " + str(self.get_number_of_elements()))
        self.__print_header_lines(False)
        for item in self.get_all_elements():
            item.print_record(False)

        num_err = self.get_number_of_errors()
        print("\nTotal Number of Errors: " + str(num_err))
        if num_err > 0:
            self.__print_header_lines(True)
            for item in self.get_all_errors():
                item.print_record(True)

    @staticmethod
    def __print_header_lines(error):
        # type: (bool) -> None
        if error:
            error_or_break = "Error Text"
        else:
            error_or_break = "Break Text"

        print("{0:>23}".format("Start") +
              "{0:>5}".format("End") +
              "{0:>6}".format("Base") +
              "{0:>5}".format("Sub-") +
              "{0:>11}".format("SI") +
              "{0:>12}".format("SI") +
              "{0:>30}".format("Stay") +
              "{0:>7}".format("Cruise") +
              "{0:>7}".format("Cruise"))
        print("{0:<9}".format("Name") +
              "{0:>14}".format("Index") +
              "{0:>6}".format("Index") +
              "{0:>5}".format("Type") +
              "{0:>5}".format("Type") +
              "{0:>6}".format("Speed") +
              "{0:>6}".format("Speed") +
              "{0:>6}".format("Alt.") +
              "{0:>6}".format("Alt.") +
              "{0:>8}".format("Bearing") +
              "{0:>10}".format("Distance") +
              "{0:>6}".format("Rules") +
              "{0:>6}".format("Time ") +
              "{0:>6}".format("To") +
              "{0:>7}".format("To SI") +
              "{0:>7}".format("Lat.") +
              "{0:>9}".format("Long ") +
              "{0:<15}".format(error_or_break))
