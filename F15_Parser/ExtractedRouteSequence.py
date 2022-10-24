from F15_Parser.ExtractedRouteRecord import ExtractedRouteRecord
from F15_Parser.F15TokenSyntaxDescriptions import TokenBaseType, TokenSubType


class ExtractedRouteSequence:
    """This class represents a complete extracted route sequence as output by the ICAO Field 15 Parser.
    This class stores 'n' ExtractedRouteRecord instances that together describe a complete route.
    """

    extracted_route_records: [ExtractedRouteRecord] = []
    """A list of extracted route records"""

    error_records: [ExtractedRouteRecord] = []
    """A list of extracted route items with errors"""

    derived_flight_rules = ""
    """The flight rules derived from parsing field 15, can be 'I', 'V', 'Y' or 'Z'"""

    def __init__(self):
        # type: () -> None
        """Constructor without any initialized extracted route record;
        clears everything, ensures class can be 're-used'

            :return: None"""
        self.extracted_route_records = []
        self.error_records = []
        # Create a dummy record that will be used for the ADEP
        self.add_dummy_adep_ades("ADEP")

    def add_dummy_adep_ades(self, aero):
        # type: (str) -> ExtractedRouteRecord
        """Creates and adds a dummy record for the ADEP or ADES. The extracted route sequence always starts
        and ends with a point of type aerodrome.

            :param aero: The location indicator as text for an aerodrome (4 capitol letters);
            :return: None"""
        return self.create_append_element(aero, 0, 0, TokenBaseType.F15_POINT, TokenSubType.F15_SB_PRP_AERO)

    def add_dummy_ades(self):
        # type: () -> ExtractedRouteRecord
        """Creates and adds a dummy ADES record. The extracted route sequence always starts
        and ends with a point of type aerodrome.

            :return: None"""
        return self.add_dummy_adep_ades("ADES")

    # Add an error record
    def add_error(self, element_text, element_start_index, element_end_index,
                  element_base_type, element_sub_type, error_message):
        # type: (str, int, int, TokenBaseType, TokenSubType, str) -> None
        """Adds an error record to the extracted route sequence. The error record is identical to a 'normal'
        record, the only difference is that it contains the error associated to it.

        :param element_text: The element text as it appears in field 15;
        :param element_start_index: The start index of the elements position in the original field 15 test string;
        :param element_end_index: The end index of the elements position in the original field 15 test string;
        :param element_base_type: A base type as an enumeration value defined in the
                                  'F15TokenSyntaxDescriptions.TokenBaseType' class.
        :param element_sub_type: A base type as an enumeration value defined in the
                                 'F15TokenSyntaxDescriptions.TokenSubType' class.
        :param error_message: The error message describing the error for this element;
        :return: None"""
        err_record = ExtractedRouteRecord(element_text, element_start_index,
                                          element_end_index, element_base_type,
                                          element_sub_type)
        err_record.append_error_text(error_message.replace("!", element_text))
        self.error_records.append(err_record)

    def append_element(self, record):
        # type: (ExtractedRouteRecord) -> ExtractedRouteRecord
        """Appends a new route record to the extracted route sequence.

        :param record: An instance of ExtractedRouteRecord to add to this extracted route sequence
        :return: An instance of the ExtractedRouteRecord that was appended by this method;"""
        self.extracted_route_records.append(record)
        return self.get_last_element()

    def as_xml(self):
        # type: () -> str
        """This method generates an XML string containing a complete ERS
        :return: A string in XML format;
        """

        # Generate the XML for all ERS records
        xml_string = "   <ers>\n"

        # Add the derived rules
        xml_string = xml_string + "      <derived_flight_rules rules=\"" + \
                                  self.get_derived_flight_rules() + \
                                  "\"></derived_flight_rules rules>\n"
        for item in self.get_all_elements():
            xml_string = xml_string + "   " + item.as_xml(False) + "\n"

        # If there are errors, add these as XML output
        if self.get_number_of_errors() > 0:
            xml_string = xml_string + "   <ers_errors>\n"
            for item in self.get_all_errors():
                xml_string = xml_string + "      " + item.as_xml(True) + "\n"
            xml_string = xml_string + "   </ers_errors>\n"

        xml_string = xml_string + "   </ers>"

        return xml_string

    def create_append_element(self, element_text, element_start_index, element_end_index,
                              element_base_type, element_sub_type):
        # type: (str, int, int, TokenBaseType, TokenSubType) -> ExtractedRouteRecord
        """Creates and appends a route element to this class instance with discreet attributes

        :param element_text: The element text as it appears in field 15;
        :param element_start_index: The start index of the elements position in the original field 15 test string;
        :param element_end_index: The end index of the elements position in the original field 15 test string;
        :param element_base_type: A base type as an enumeration value defined in the
                                  'F15TokenSyntaxDescriptions.TokenBaseType' class.
        :param element_sub_type: A base type as an enumeration value defined in the
                                 'F15TokenSyntaxDescriptions.TokenSubType' class.
        :return: An instance of the ExtractedRouteRecord that was appended by this method;"""
        return self.append_element(ExtractedRouteRecord(element_text, element_start_index,
                                                        element_end_index, element_base_type,
                                                        element_sub_type))

    def get_all_elements(self):
        # type: () -> [ExtractedRouteRecord]
        """Gets the list of extracted route records.

        :return: A list of ExtractedRouteRecord instances;"""
        return self.extracted_route_records

    def get_all_errors(self):
        # type: () -> [ExtractedRouteRecord]
        """Gets the list of extracted route records that contain errors.

        :return: A list of ExtractedRouteRecord instances that contain errors;"""
        return self.error_records

    def get_derived_flight_rules(self):
        # type: () -> str
        """Get the flight rules derived and set from parsing F15;

        :return: The flight rules as derived by parsing F15;
        """
        return self.derived_flight_rules

    def get_element_at(self, index):
        # type: (int) -> ExtractedRouteRecord | None
        """Retrieves an extracted route record at 'index', or returns 'None' if 'index' is out of range.

        :param index: The index of the extracted route record to be retrieved;
        :return: An instance of ExtractedRouteRecord located at index provided or None if index is out of range;"""
        if index < 0 or index > self.get_number_of_elements():
            return None
        return self.extracted_route_records[index]

    # Get the first ERS element
    def get_first_element(self):
        # type: () -> ExtractedRouteRecord
        """Retrieves the first extracted route record in the extracted route sequence.

        :return: An instance of ExtractedRouteRecord located at index 0;"""
        return self.get_element_at(0)

    def get_last_element(self):
        # type: () -> ExtractedRouteRecord | None
        """Retrieves the last extracted route record in the extracted route sequence.

        :return: An instance of ExtractedRouteRecord located at the end of the extracted route sequence
                 or None if there are less than two records in the list;"""
        if self.get_number_of_elements() > 0:
            return self.get_element_at(self.get_number_of_elements() - 1)
        else:
            return None

    def get_number_of_elements(self):
        # type: () -> int
        """Gets the number of extracted route records

        :return: The number of extracted route records in the extracted route sequence;"""
        return len(self.extracted_route_records)

    def get_number_of_errors(self):
        # type: () -> int
        """Gets the number of error records.

        :return: The number of extracted route records with errors;
        """
        return len(self.error_records)

    def get_previous_to_last_element(self):
        # type: () -> ExtractedRouteRecord
        """Gets the previous element to the current element.

        :return: The previous extracted route record to the last one retrieved as an
                 instance of ExtractedRouteRecord;"""
        return self.get_element_at(self.get_number_of_elements() - 2)

    def set_derived_flight_rules(self, derived_flight_rules):
        # type: (str) -> None
        """Set the flight rules derived from F15 parsing;

        :param derived_flight_rules: The flight rules to set as derived by parsing F15;
        :return: None
        """
        self.derived_flight_rules = derived_flight_rules

    def print_ers(self):
        # type: () -> None
        """Prints the complete extracted route sequence to the console, used as ahelper in debugging

        :return: None"""
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
        """Helper method for printing the complete extracted route sequence. The output formats the output
        into columns and is provided with appropriate headers.

        :param error: A boolean that prints the error records when true and the 'normal' records when False.
        :return: None"""
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
