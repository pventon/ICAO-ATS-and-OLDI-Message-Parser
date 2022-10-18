import unittest

from Configuration.EnumerationConstants import MessageTypes, AdjacentUnits, MessageTitles, FieldIdentifiers, \
    SubFieldIdentifiers
from Configuration.FieldsInMessage import FieldsInMessage
from Configuration.SubFieldDescriptions import SubFieldDescriptions
from Configuration.SubFieldsInFields import SubFieldsInFields


class SupportedMessagesTest(unittest.TestCase):

    def test_MessageContentDescriptions_01(self):
        fim = FieldsInMessage()
        md = fim.get_message_content(MessageTypes.ATS, AdjacentUnits.DEFAULT, MessageTitles.FPL)
        self.assertEqual(MessageTitles.FPL.name, md.get_message_title())
        self.assertEqual("ATS Flight Plan Message", md.get_message_description())
        fields = md.get_message_fields()
        expected = [FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F8, FieldIdentifiers.F9,
                    FieldIdentifiers.F10, FieldIdentifiers.F13, FieldIdentifiers.F15, FieldIdentifiers.F16,
                    FieldIdentifiers.F18, FieldIdentifiers.F19]
        self.assertEqual(expected, fields)
        self.assertEqual([], md.get_specific_field_22())

        md = fim.get_message_content(MessageTypes.ATS, AdjacentUnits.DEFAULT, MessageTitles.FNM)
        self.assertEqual(MessageTitles.FNM.name, md.get_message_title())
        self.assertEqual("Gander Oceanic Message", md.get_message_description())
        fields = md.get_message_fields()
        expected = [FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F9,
                    FieldIdentifiers.F13a, FieldIdentifiers.F15, FieldIdentifiers.F16a,
                    FieldIdentifiers.F18, FieldIdentifiers.F19]
        self.assertEqual(expected, fields)
        self.assertEqual([], md.get_specific_field_22())

        md = fim.get_message_content(MessageTypes.ATS, AdjacentUnits.DEFAULT, MessageTitles.ARR)
        self.assertEqual(MessageTitles.ARR.name, md.get_message_title())
        self.assertEqual("ATS Arrival Message", md.get_message_description())
        fields = md.get_message_fields()
        expected = [FieldIdentifiers.F3, FieldIdentifiers.F7,
                    FieldIdentifiers.F13, FieldIdentifiers.F16ab,
                    FieldIdentifiers.F17, FieldIdentifiers.F18_DOF]
        self.assertEqual(expected, fields)
        self.assertEqual([], md.get_specific_field_22())

    def test_MessageContentDescriptions_02(self):
        fim = FieldsInMessage()
        md = fim.get_message_content(MessageTypes.OLDI, AdjacentUnits.DEFAULT, MessageTitles.ACT)
        self.assertEqual(MessageTitles.ACT.name, md.get_message_title())
        self.assertEqual("OLDI Activation Message", md.get_message_description())
        fields = md.get_message_fields()
        expected = [FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F13a, FieldIdentifiers.F14,
                    FieldIdentifiers.F16a, FieldIdentifiers.F22_SPECIFIC]
        self.assertEqual(expected, fields)
        self.assertEqual([FieldIdentifiers.F9, FieldIdentifiers.F80, FieldIdentifiers.F81], md.get_specific_field_22())

        fim = FieldsInMessage()
        md = fim.get_message_content(MessageTypes.OLDI, AdjacentUnits.AA, MessageTitles.ACT)
        self.assertEqual(MessageTitles.ACT.name, md.get_message_title())
        self.assertEqual("OLDI Activation Message", md.get_message_description())
        fields = md.get_message_fields()
        expected = [FieldIdentifiers.F3, FieldIdentifiers.F7, FieldIdentifiers.F13a, FieldIdentifiers.F14,
                    FieldIdentifiers.F16a, FieldIdentifiers.F22_SPECIFIC]
        self.assertEqual(expected, fields)
        self.assertEqual([FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                          FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81], md.get_specific_field_22())

    def test_FieldContentDefinitions_01(self):
        sfif = SubFieldsInFields()
        subfields = sfif.get_field_content_description(FieldIdentifiers.F3)
        expected = [SubFieldIdentifiers.F3a, SubFieldIdentifiers.F3b1, SubFieldIdentifiers.F3b2,
                    SubFieldIdentifiers.F3b3, SubFieldIdentifiers.F3b4, SubFieldIdentifiers.F3c1,
                    SubFieldIdentifiers.F3c2, SubFieldIdentifiers.F3c3, SubFieldIdentifiers.F3c4]
        self.assertEqual(expected, subfields)

    def test_get_subfield_description_01(self):
        sfif = SubFieldsInFields()
        subfields = sfif.get_field_content_description(FieldIdentifiers.F22)
        expected = [SubFieldIdentifiers.F22_f3]
        self.assertEqual(expected, subfields)

        sfd = SubFieldDescriptions()
        field_description = sfd.get_subfield_description(SubFieldIdentifiers.F8a)
        self.assertEqual(SubFieldIdentifiers.F8a, field_description.get_subfield_id())


if __name__ == '__main__':
    unittest.main()
