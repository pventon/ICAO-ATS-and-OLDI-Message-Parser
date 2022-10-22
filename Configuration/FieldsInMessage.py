from Configuration.EnumerationConstants import FieldIdentifiers, MessageTitles, AdjacentUnits, MessageTypes
from Configuration.MessageDescription import MessageDescription
from IcaoMessageParser.ParseF10 import ParseF10
from IcaoMessageParser.ParseF13 import ParseF13
from IcaoMessageParser.ParseF13a import ParseF13a
from IcaoMessageParser.ParseF14 import ParseF14
from IcaoMessageParser.ParseF14a import ParseF14a
from IcaoMessageParser.ParseF15 import ParseF15x
from IcaoMessageParser.ParseF16 import ParseF16
from IcaoMessageParser.ParseF16a import ParseF16a
from IcaoMessageParser.ParseF16ab import ParseF16ab
from IcaoMessageParser.ParseF17 import ParseF17
from IcaoMessageParser.ParseF18 import ParseF18
from IcaoMessageParser.ParseF18dof import ParseF18dof
from IcaoMessageParser.ParseF19 import ParseF19
from IcaoMessageParser.ParseF20 import ParseF20
from IcaoMessageParser.ParseF21 import ParseF21
from IcaoMessageParser.ParseF22 import ParseF22
from IcaoMessageParser.ParseF22_Specific import ParseF22Specific
from IcaoMessageParser.ParseF3 import ParseF3
from IcaoMessageParser.ParseF5 import ParseF5
from IcaoMessageParser.ParseF7 import ParseF7
from IcaoMessageParser.ParseF8 import ParseF8
from IcaoMessageParser.ParseF9 import ParseF9
from IcaoMessageParser.ParseMfsPoint import ParseMfsPoint


# This class describes the content of each ICAO and OLDI message supported by this
# message parser.
# The ICAO field IDs are provided by the enumeration values in
# the FieldIdentifiers class. Many of the ICAO field IDs translate directly to those
# specified in ICAO DOC 4444; however, due to support for OLDI messages as well
# as some IFPS Oceanic message, some field identifiers are what could be called custom.
# The result is the same, all fields for a given message title can be obtained from
# this class.
# This class implements a complex data structure that facilitates the field content
# for a message to be individually defined based on the message title, type and
# adjacent unit (for OLDI messages). For ICAO ATS messages, there is no selection
# based on adjacent unit, a 'dummy' DEFAULT adjacent unit is provided to ensure
# the structure is symmetrical for both ICAO ATS and OLDI messages.
# A message must be selected based on its type, (ATS or OLDI), then by its
# adjacent unit designator (for OLDI) then message title.
# When searching for a message, the get_message_content() method requires three
# arguments:
# Message type - Enumeration specified in the MessageType class;
# Adjacent Unit - Enumeration specified in the AdjacentUnit class;
# Message Title - Enumeration specified in the MessageTitles class;
# The data structures in this class are implemented using dictionaries
# to yield a three-dimensional data structure that can be visualized as follows:
#
# self.message_content = {                                  1st dimension
#    MessageType.ATS {                                      2nd dimension
#       AdjacentUnit.DEFAULT {                              3rd dimension
#           // ICAO ATS messages only use a single adjacent unit dimension
#           MessageTitles.A: MessageDescription instance
#                       ...
#           MessageTitles.Z: MessageDescription instance
#       }
#    }
#    MessageType.OLDI {                                     2nd dimension
#       AdjacentUnit.DEFAULT {                              3rd dimension
#           MessageTitles.A: MessageDescription instance
#                       ...
#           MessageTitles.Z: MessageDescription instance
#       }
#       AdjacentUnit.X {                                    3rd dimension
#           // OLDI messages use many adjacent unit dimensions
#           MessageTitles.A: MessageDescription instance
#                       ...
#           MessageTitles.Z: MessageDescription instance
#       }
#       AdjacentUnit.Y {}                                   3rd dimension
#                   ...
#       AdjacentUnit.Z {}                                   3rd dimension
#    }
# }
class FieldsInMessage:
    # A dictionary containing descriptions for all supported messages
    # based on a message title, message type and adjacent unit.
    # A single message content description is stored in an instance
    # of MessageDescription.
    message_content = {}

    # This constructor builds the complete configuration data structure
    # and populates it with the data shown below.
    def __init__(self):
        self.message_content = {
            MessageTypes.ATS: {
                AdjacentUnits.DEFAULT: {
                    MessageTitles.ACH: MessageDescription(
                        MessageTitles.ACH.name,
                        "ATS ATC Change Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16ab,
                            ParseF18dof,
                            ParseF22], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16ab,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22], []),
                    MessageTitles.ACP: MessageDescription(
                        MessageTitles.ACP.name,
                        "ATS Advanced Coordination Procedure Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16], []),
                    MessageTitles.AFP: MessageDescription(
                        MessageTitles.AFP.name,
                        "ATS ATC Flightplan Proposal Message", [
                            ParseF3,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF14,
                            ParseF15x,
                            ParseF16,
                            ParseF18,
                            ParseF19], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19], []),
                    MessageTitles.ALR: MessageDescription(
                        MessageTitles.ALR.name,
                        "ATS ATC Alerting Message", [
                            ParseF3,
                            ParseF5,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF15x,
                            ParseF16,
                            ParseF18,
                            ParseF19,
                            ParseF20], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F5,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19,
                            FieldIdentifiers.F20], []),
                    MessageTitles.APL: MessageDescription(
                        MessageTitles.APL.name,
                        "ATS ATC Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF14,
                            ParseF15x,
                            ParseF16,
                            ParseF18,
                            ParseF19], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19], []),
                    MessageTitles.ARR: MessageDescription(
                        MessageTitles.ARR.name,
                        "ATS Arrival Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16ab,
                            ParseF17,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16ab,
                            FieldIdentifiers.F17,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.CDN: MessageDescription(
                        MessageTitles.CDN.name,
                        "ATS Coordination Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.CHG: MessageDescription(
                        MessageTitles.CHG.name,
                        "ATS Change Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16ab,
                            ParseF18dof,
                            ParseF22], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16ab,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22], []),
                    MessageTitles.CNL: MessageDescription(
                        MessageTitles.CNL.name,
                        "ATS Cancel Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.CPL: MessageDescription(
                        MessageTitles.CPL.name,
                        "ATS Current Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF14,
                            ParseF15x,
                            ParseF16,
                            ParseF18], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18], []),
                    MessageTitles.DEP: MessageDescription(
                        MessageTitles.DEP.name,
                        "ATS Departure Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.DLA: MessageDescription(
                        MessageTitles.DLA.name,
                        "ATS Delay Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.EST: MessageDescription(
                        MessageTitles.EST.name,
                        "ATS Estimate Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF14,
                            ParseF16], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16], []),
                    MessageTitles.FPL: MessageDescription(
                        MessageTitles.FPL.name,
                        "ATS Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF15x,
                            ParseF16,
                            ParseF18,
                            ParseF19], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19], []),
                    MessageTitles.FNM: MessageDescription(
                        MessageTitles.FNM.name,
                        "Gander Oceanic Message", [
                            ParseF3,
                            ParseF7,
                            ParseF9,
                            ParseF13a,
                            ParseF15x,
                            ParseF16a,
                            ParseF18,
                            ParseF19], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19], []),
                    MessageTitles.MFS: MessageDescription(
                        MessageTitles.MFS.name,
                        "Oceanic Centre Message", [
                            ParseF3,
                            ParseF7,
                            ParseF9,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseMfsPoint], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.MFS_SIG_POINT], []),
                    MessageTitles.RCF: MessageDescription(
                        MessageTitles.RCF.name,
                        "ATS Radio communication failure", [
                            ParseF3,
                            ParseF7,
                            ParseF21], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F21], []),
                    MessageTitles.RQP: MessageDescription(
                        MessageTitles.RQP.name,
                        "ATS Request Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a,
                            ParseF18dof], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF], []),
                    MessageTitles.RQS: MessageDescription(
                        MessageTitles.RQS.name,
                        "ATS Request Supplementary Flight Plan Information Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16,
                            ParseF18], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18], []),
                    MessageTitles.SPL: MessageDescription(
                        MessageTitles.SPL.name,
                        "ATS Supplementary Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16,
                            ParseF18,
                            ParseF19], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16,
                            FieldIdentifiers.F18,
                            FieldIdentifiers.F19], [])
                }
            },
            MessageTypes.OLDI: {
                AdjacentUnits.DEFAULT: {
                    MessageTitles.ABI: MessageDescription(
                        MessageTitles.ABI.name,
                        "OLDI Advanced Boundary Information", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.ACP: MessageDescription(
                        MessageTitles.ACP.name,
                        "OLDI Advanced Coordination Procedure Message",
                        [ParseF3],
                        [FieldIdentifiers.F3], []),
                    MessageTitles.ACT: MessageDescription(
                        MessageTitles.ACT.name,
                        "OLDI Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.AMA: MessageDescription(
                        MessageTitles.AMA.name,
                        "OLDI Arrival Management Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F18]),
                    MessageTitles.CDN: MessageDescription(
                        MessageTitles.CDN.name,
                        "OLDI Coordination Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a], []),
                    MessageTitles.COD: MessageDescription(
                        MessageTitles.COD.name,
                        "OLDI Advanced Coordination Procedure", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a], []),
                    MessageTitles.CPL: MessageDescription(
                        MessageTitles.CPL.name,
                        "OLDI Current Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16ab,
                            ParseF18dof,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16ab,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9]),
                    MessageTitles.INF: MessageDescription(
                        MessageTitles.INF.name,
                        "OLDI Information Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F15, FieldIdentifiers.F18]),
                    MessageTitles.LAM: MessageDescription(
                        MessageTitles.LAM.name,
                        "OLDI Logical Acknowledgement", [
                            ParseF3], [
                            FieldIdentifiers.F3], []),
                    MessageTitles.MAC: MessageDescription(
                        MessageTitles.MAC.name,
                        "OLDI Message for the Abrogation of Coordination", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14a,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14a,
                            FieldIdentifiers.F16a], []),
                    MessageTitles.OCM: MessageDescription(
                        MessageTitles.OCM.name,
                        "OLDI Oceanic Clearance Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9]),
                    MessageTitles.PAC: MessageDescription(
                        MessageTitles.PAC.name,
                        "OLDI Preliminary Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9]),
                    MessageTitles.RAP: MessageDescription(
                        MessageTitles.RAP.name,
                        "OLDI Referred Activate Proposal Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF18dof,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.REJ: MessageDescription(
                        MessageTitles.REJ.name,
                        "OLDI Reject Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF18], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18], []),
                    MessageTitles.REV: MessageDescription(
                        MessageTitles.REV.name,
                        "OLDI Revision Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a], []),
                    MessageTitles.RJC: MessageDescription(
                        MessageTitles.RJC.name,
                        "OLDI Reject Coordination Message", [
                            ParseF3], [
                            FieldIdentifiers.F3], []),
                    MessageTitles.ROC: MessageDescription(
                        MessageTitles.ROC.name,
                        "OLDI Request Oceanic Clearance Message", [
                            ParseF3,
                            ParseF7,
                            ParseF22Specific,
                            ParseF13a,
                            ParseF14,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F22_SPECIFIC,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a], [FieldIdentifiers.F9]),
                    MessageTitles.RRV: MessageDescription(
                        MessageTitles.RRV.name,
                        "OLDI Referred Revision Proposal Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a], []),
                    MessageTitles.SBY: MessageDescription(
                        MessageTitles.SBY.name,
                        "OLDI Standby Message", [
                            ParseF3], [
                            FieldIdentifiers.F3], [])
                },
                AdjacentUnits.AA: {
                    MessageTitles.ABI: MessageDescription(
                        MessageTitles.ABI.name,
                        "OLDI Advanced Boundary Information", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.ACP: MessageDescription(
                        MessageTitles.ACP.name,
                        "OLDI Advanced Coordination Procedure Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F18]),
                    MessageTitles.ACT: MessageDescription(
                        MessageTitles.ACT.name,
                        "OLDI Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.AMA: MessageDescription(
                        MessageTitles.AMA.name,
                        "OLDI Arrival Management Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F18]),
                    MessageTitles.CDN: MessageDescription(
                        MessageTitles.CDN.name,
                        "OLDI Coordination Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F15]),
                    MessageTitles.INF: MessageDescription(
                        MessageTitles.INF.name,
                        "OLDI Information Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F15, FieldIdentifiers.F18]),
                    MessageTitles.MAC: MessageDescription(
                        MessageTitles.MAC.name,
                        "OLDI Message for the Abrogation of Coordination", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F13, FieldIdentifiers.F18, FieldIdentifiers.F80,
                         FieldIdentifiers.F81]),
                    MessageTitles.OCM: MessageDescription(
                        MessageTitles.OCM.name,
                        "OLDI Oceanic Clearance Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9, FieldIdentifiers.F15]),
                    MessageTitles.PAC: MessageDescription(
                        MessageTitles.PAC.name,
                        "OLDI Preliminary Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.RAP: MessageDescription(
                        MessageTitles.RAP.name,
                        "OLDI Referred Activate Proposal Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.REJ: MessageDescription(
                        MessageTitles.REJ.name,
                        "OLDI Reject Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF18], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18], []),
                    MessageTitles.REV: MessageDescription(
                        MessageTitles.REV.name,
                        "OLDI Revision Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F81]),
                    MessageTitles.RJC: MessageDescription(
                        MessageTitles.RJC.name,
                        "OLDI Reject Coordination Message", [
                            ParseF3,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F18]),
                    MessageTitles.ROC: MessageDescription(
                        MessageTitles.ROC.name,
                        "OLDI Request Oceanic Clearance Message", [
                            ParseF3,
                            ParseF7,
                            ParseF22,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F22,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9, FieldIdentifiers.F15]),
                },
                AdjacentUnits.AX: {
                    MessageTitles.ACP: MessageDescription(
                        MessageTitles.ACP.name,
                        "OLDI Advanced Coordination Procedure Message", [ParseF3], [
                            FieldIdentifiers.F3], []),
                },
                AdjacentUnits.L: {
                    MessageTitles.ABI: MessageDescription(
                        MessageTitles.ABI.name,
                        "OLDI Advanced Boundary Information", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF18dof,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F81]),
                    MessageTitles.CPL: MessageDescription(
                        MessageTitles.CPL.name,
                        "OLDI Current Flight Plan Message", [
                            ParseF3,
                            ParseF7,
                            ParseF8,
                            ParseF9,
                            ParseF10,
                            ParseF13,
                            ParseF14,
                            ParseF15x,
                            ParseF16a,
                            ParseF18], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F8,
                            FieldIdentifiers.F9,
                            FieldIdentifiers.F10,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F15,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18], []),
                },
                AdjacentUnits.BB: {
                    MessageTitles.CDN: MessageDescription(
                        MessageTitles.CDN.name,
                        "OLDI Coordination Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F15]),
                    MessageTitles.INF: MessageDescription(
                        MessageTitles.INF.name,
                        "OLDI Information Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF18dof,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F18_DOF,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F9, FieldIdentifiers.F15, FieldIdentifiers.F18]),
                    MessageTitles.PAC: MessageDescription(
                        MessageTitles.PAC.name,
                        "OLDI Preliminary Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF13,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F13,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F80]),
                    MessageTitles.ROC: MessageDescription(
                        MessageTitles.ROC.name,
                        "OLDI Request Oceanic Clearance Message", [
                            ParseF3,
                            ParseF7,
                            ParseF22,
                            ParseF13a,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F22,
                            FieldIdentifiers.F13a,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC], [FieldIdentifiers.F9, FieldIdentifiers.F15]),
                },
                AdjacentUnits.CC: {
                    MessageTitles.PAC: MessageDescription(
                        MessageTitles.PAC.name,
                        "OLDI Preliminary Activation Message", [
                            ParseF3,
                            ParseF7,
                            ParseF14,
                            ParseF16a,
                            ParseF22Specific], [
                            FieldIdentifiers.F3,
                            FieldIdentifiers.F7,
                            FieldIdentifiers.F14,
                            FieldIdentifiers.F16a,
                            FieldIdentifiers.F22_SPECIFIC],
                        [FieldIdentifiers.F8a, FieldIdentifiers.F9, FieldIdentifiers.F15,
                         FieldIdentifiers.F18, FieldIdentifiers.F80, FieldIdentifiers.F80]),
                }
            }
        }

    # Gets the field content description for a message based on its message title,
    # message type and adjacent unit identifier.
    # When searching for a message, the get_message_content() method requires three
    # arguments.
    # Arguments
    # ----------
    # message_type:     Enumeration specified in the MessageType class;
    # adjacent_unit:    Enumeration specified in the AdjacentUnit class;
    # message_title:    Enumeration specified in the MessageTitles class;;
    # return:           An instance of the MessageDescription class or None if the message
    #                   given by 'message_title' is unsupported.
    def get_message_content(self, message_type, adjacent_unit, message_title):
        # type: (MessageTypes, AdjacentUnits, MessageTitles) -> MessageDescription | None
        msg_type = self.message_content.get(message_type)
        if msg_type is None:
            return None
        adj_unit = msg_type.get(adjacent_unit)
        if adj_unit is None:
            return None
        return adj_unit.get(message_title)
