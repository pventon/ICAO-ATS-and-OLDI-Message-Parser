import unittest

from Configuration.EnumerationConstants import FieldIdentifiers
from Configuration.MessageDescription import MessageDescription
from IcaoMessageParser.ParseF10 import ParseF10
from IcaoMessageParser.ParseF13 import ParseF13
from IcaoMessageParser.ParseF14 import ParseF14
from IcaoMessageParser.ParseF16 import ParseF16
from IcaoMessageParser.ParseF18 import ParseF18
from IcaoMessageParser.ParseF3 import ParseF3
from IcaoMessageParser.ParseF5 import ParseF5
from IcaoMessageParser.ParseF7 import ParseF7
from IcaoMessageParser.ParseF9 import ParseF9


class MessageDescriptionTest(unittest.TestCase):

    def test_messageDescription(self):
        md = MessageDescription("Msg Title", "Msg Description one",
                                [ParseF5, ParseF7, ParseF9, ParseF10, ParseF14],
                                [FieldIdentifiers.F5, FieldIdentifiers.F7, FieldIdentifiers.F9],
                                [FieldIdentifiers.F10, FieldIdentifiers.F14])
        self.assertEqual("Msg Title", md.get_message_title())
        self.assertEqual("Msg Description one", md.get_message_description())
        self.assertEqual([FieldIdentifiers.F5, FieldIdentifiers.F7, FieldIdentifiers.F9], md.get_message_fields())
        self.assertEqual([FieldIdentifiers.F10, FieldIdentifiers.F14], md.get_specific_field_22())

        md = MessageDescription("Msg Title", "Msg Description two",
                                [ParseF3, ParseF7, ParseF13, ParseF16, ParseF18],
                                [FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F13],
                                [FieldIdentifiers.F16, FieldIdentifiers.F18])
        self.assertEqual("Msg Title", md.get_message_title())
        self.assertEqual("Msg Description two", md.get_message_description())
        self.assertEqual([FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F13], md.get_message_fields())
        self.assertEqual([FieldIdentifiers.F16, FieldIdentifiers.F18], md.get_specific_field_22())


if __name__ == '__main__':
    unittest.main()
