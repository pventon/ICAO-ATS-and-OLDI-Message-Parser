# ICAO ATS and OLDI Message Parser
<meta name="google-site-verification" content="awWwElk8GXFJIvmNuEuEowc-MlPdyv4D-TgYx4_UHsA" />
<p>This <a href="https://github.com/">GitHub</a> repository contains an <b>ICAO ATS and OLDI Message Parser</b>. The <b>ICAO ATS and OLDI Message Parser</b> is implemented using Python version 3.10.7. A more recent version of Python must be used in order to support <b>switch</b> statements used in the source code.
</p>
<p>An acronym list is provided at the end of this readme for readers unfamiliar with ATC acronyms.
</p>
<p>The open source <a href="https://github.com/">GitHub</a> repository for the <b>ICAO ATS and OLDI Message Parser</b> can be found <a href="https://github.com/pventon/ICAO-ATS-and-OLDI-Message-Parser">here</a>.
</p>
<p>The <b>ICAO ATS and OLDI Message Parser</b> uses a standalone <b>ICAO Field 15 Parser</b> that is also available as an open source <a href="https://github.com/">GitHub</a> project that can be found <a href="https://github.com/pventon/ICAO-F15-Parser">here</a>.
</p>
<p>All software on both the <b>ICAO ATS and OLDI Message Parser</b> and <b>ICAO Field 15 Parser</b> <a href="https://github.com/">GitHub</a> repositories has been written by Peter Venton (user pventon on <a href="https://github.com/">GitHub</a>).</p>

<h1>Overview</h1>
<p>ICAO ATS and OLDI messages conform to the syntax and semantic standards described in ICAO DOC 4444.
</p>
<p>ATS messages contain an application header described in the ICAO Annex 10, Volume II document. OLDI messages do not have an application header. Both types of message have additional header information that is processed by the appropriate protocol handler, this parser does not deal with the protocol handler header.
</p>
<p>The <b>ICAO ATS and OLDI Message Parser</b> is able to process the following:</p>
<ul>
<li>Messages with or without the application header;</li>
<li>Messages with or without an application header, with or without the open and closed brackets;</li>
</ul>
<p>The <b>ICAO ATS and OLDI Message Parser</b> automatically determines if messages have the header and/or brackets.
</p>
<p>All fields are parsed and copied to an FPR for the caller to process further. ICAO field 15 is processed using a dedicated Field 15 Parser (available <a href="https://github.com/pventon/ICAO-F15-Parser">here</a>).
</p>
<p>Message content is defined in configuration data; each message title consists of a finite set of ICAO fields. This is the same for OLDI messages although the OLDI messages have some additional fields defined, however, the principle is the same.
</p>
<p>OLDI messages have one further difference when compared to ATS messages; in addition to the content defined for a given title, the field content varies depending on the adjacent unit OLDI messages are exchanged on. The <b>ICAO ATS and OLDI Message Parser</b> determines the adjacent unit identifier from a message and selects the field content using a combination of the message title and adjacent unit name.
</p>
<p>Route extraction is performed on field 15 and the extracted route stored in the FPR. For details on Field 15 parsing refer to the ICAO Field 15 Parser repository.
</p>
<p>Each field and its subfield(s) are parsed for correct syntax and semantics; should an error be detected, accurate error messages are generated describing an error found in a particular field. The zero based index of a field and subfield are stored with all fields and subfields; these indices can be used for highlighting errors in a GUI.
</p>
<h2>Current Functionality</h2>
<p>The current implementation parses all the 'basic' ICAO fields F3, F5, F7, F8, F9, F10, F13, F14, F15, F16, F17, F20 and F21.
The ICAO fields F18, F19 and F22 are 'compound' fields made up of numerous subfields. This parser fully parses F18, F19 and F22 and all their subfields. The flight plan record stores a complete F22 flight plan that is populated by F22 subfields. Theoretically, F22 is able to specify all the fields for a complete flight plan, hence an F22 flight plan is stored within the flight plan proper. Any errors reported for F22 subfields are copied to the main flight plan record for convenience to the caller. Duplicated F22 subfield errors are also reported.
</p>
<p>Fields F18 and F19 are parsed for correct keyword/data format with all subfields copied to the flight plan. Errors are reported if the keyword/data format is found to be incorrect or text is found outside a keyword/data subfield. All F18 and F19 subfields are fully parsed.
</p>
<p>OLDI define two extra fields 80 and 81, the parser fully supports these two fields with appropriate error messages etc. These fields are an addition to the ICAO F22 suite of subfields.
</p>
<p><b><i>A parsed message can be output as an XML string by calling FlightPlanRecord.as_xml()</i></b>
</p>

<h2>Consistency Checking</h2>
<p>The <b>ICAO ATS and OLDI Message Parser</b> performs consistency checking between various fields once a flight plan has been parsed. The consistency checking can only be carried out on messages that contain the required fields, the message titles subject to consistency checking are:
</p>
<ul>
<li>AFP</li>
<li>ALR</li>
<li>APL</li>
<li>CPL</li>
<li>FPL</li>
</ul>
<p>The consistency checks carried out are:</p>
<ul>
<li>Flight rules between F8a and the flight rules derived by the F15 parsing and route extraction process; these must match.</li>
<li>If F10a contains the letter 'Z' then one or more of the F18 subfields 'COM', 'NAV' or 'DAT' must be present;</li>
<li>If F10a contains the letter 'R' then the F18 'PBN' subfield must be present and contain one or more of the indicators 'B1', 'B2', 'B3', 'B4' or 'B5';</li>
<li>If F18 contains the subfield 'PBN', F10a must contain an 'R';</li>
<li>If F18 'PBN' contains one or more of the indicators 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'O1' or 'O2', then F10a must contain the letter 'G';</li>
<li>If F18 'PBN' contains one or more of the indicators 'B1', 'B3', 'C1', 'C3', 'D1', 'D3', 'O1' or 'O3', then F10a must contain the letter 'D';</li>
<li>If F18 'PBN' contains one or more of the indicators 'B1' or 'B4', then F10a must contain either an 'O' or 'S' and a 'D';</li>
<li>If F18 'PBN' contains one or more of the indicators 'B1', 'B5', 'C1', 'C4', 'D1', 'D4', 'O1' or 'O4', then F10a must contain the letter 'I';</li>
<li>If F18 'PBN' contains one or more of the indicators 'C1', 'C4', 'D1', 'D4', 'O1' or 'O4', then F10a must contain the letter 'D';</li>
<li>If F9b contains ZZZZ then field 18 must contain the TYP subfield;</li>
<li>If F13a contains ZZZZ then field 18 must contain the DEP subfield;</li>
<li>If F16a contains ZZZZ then field 18 must contain the DEST subfield;</li>
</ul>
<h2>Current Limitations</h2>
<p>None as 23rd October 2022 that the author is currently aware of;</p>
<h2>Future Upgrades</h2>
<p>No modifications pending as of 23rd October 2022;</p>
<h2>Errata and Faults</h2>
<p>Although every attempt has been made to reduce the number of software coding errors and resulting chaos that can ensue as a result of such errors, it is highly likely that this early release will have a few bugs. The possible combinations of message structure and semantics run into millions of combinations, and it's impossible to test them all. There are a lot of unit tests that check the individual field parsers and messages in their entirety, but even with so many tests, there may still be some bugs in the software.
</p>
<p>Should any use be made of this software and errors found, do not hesitate to contact me at peter.venton@flightatm.com, so I may attempt to fix/correct any issues, or alternatively post any errors on the discussion page or bug tracker that I believe is supplied as part of GitHub.
</p>
<p><b>Good luck!</b>
<h1>ICAO ATS and OLDI Message Parser Usage</h1>
<p>In the root directory of the repository there is a class called <b>IcaoAtsMessageParser</b> that is the calling interface to the ICAO ATS and OLDI Message Parser.
</p>
<p>Example usage of the ICAO ATS and OLDI Message Parser;</p>
<pre><code>
# The following example ATS FPL message will be used for the discussions that follow...
# icao_message: str = "(FPL-TEST01-IS-B737/M-S/C-LOWW0800-N0450f350 PNT B9 LNZ1A-EGLL0200-0)"
</code></pre>
There are two methods provided for parsing a message titled Option 1 and Option 2 below.
<h3>Option 1</h3>
<pre><code>
# Instantiate the parser...
icao_message_parser: IcaoAtsMessageParser = IcaoAtsMessageParser()
<br>
# Parse the message...
flight_plan_record: FlightPlanRecord = icao_message_parser.parse_message_p1(icao_message)
<br>
# Check if any errors were reported in the basic field processing...
if flight_plan_record.errors_detected():
    # For fields other than field 15 call the following method, this returns a list of ErrorRecord's...
    basic_field_errors: [ErrorRecord] = flight_plan_record.get_erroneous_fields()
<br>
# For field 15, get the Extracted Route Sequence and get the errors, returns a list of Tokens...
if flight_plan_record.get_extracted_route_sequence().get_number_of_errors() > 0:
    field_15_errors: [Token] = flight_plan_record.get_extracted_route_sequence().get_all_errors()
<br>
# To extract fields and / or subfields use the methods in the following example code...
self.assertEqual(
    # Get the complete ICAO Field 9
    "B737/M",
    flight_plan_record.get_icao_field(FieldIdentifiers.F9).get_field_text())
<br>
self.assertEqual(
    # Get the ICAO field 9 WTC (Field 9 'c')
    "M",
    flight_plan_record.get_icao_subfield(FieldIdentifiers.F9, SubFieldIdentifiers.F9c).get_field_text())
</code></pre>
<h3>Option 2</h3>
<pre><code>
# Instantiate a FlightPlanRecord, the output is written into this class instance.
flight_plan_record: FlightPlanRecord = FlightPlanRecord()
<br>
# Instantiate the parser...
icao_message_parser = IcaoAtsMessageParser()
<br>
# Parse the message...
# result = icao_message_parser.parse_message_p2(flight_plan_record, icao_message)
<br>
# If errors were detected, result will be False; to get the error records do the following...
if not result:
    # For fields other than field 15 call the following method, this returns a list of ErrorRecord's...
    basic_field_errors: [ErrorRecord] = flight_plan_record.get_erroneous_fields()
<br>
# For field 15, get the Extracted Route Sequence and get the errors, returns a list of Tokens...
if flight_plan_record.get_extracted_route_sequence().get_number_of_errors() > 0:
    field_15_errors: [Token] = flight_plan_record.get_extracted_route_sequence().get_all_errors()
<br>
# To extract fields and / or subfields use the methods in the following example code...
self.assertEqual(
    # Get the complete ICAO Field 13
    "LOWW0800",
    flight_plan_record.get_icao_field(FieldIdentifiers.F13).get_field_text())
<br>
self.assertEqual(
    # Get the ICAO field 16 EET (Field 16 'b')
    "0200",
    flight_plan_record.get_icao_subfield(FieldIdentifiers.F16, SubFieldIdentifiers.F16b).get_field_text())
</code></pre>
<h1>Acronyms</h1>
<ul>
<li>ABI     OLDI Advanced Boundary Information</li>
<li>ACH     ATS ATC Change Message</li>
<li>ACT     OLDI Activation Message</li>
<li>ACP     ATS Advanced Coordination Procedure Message</li>
<li>ACP     OLDI Advanced Coordination Procedure Message</li>
<li>ADEP    Aerodrome of Departure (Given as an ICAO Location Indicator)</li>
<li>ADES    Aerodrome of Destination (Given as an ICAO Location Indicator)</li>
<li>AFP     ATS ATC Flightplan Proposal Message</li>
<li>AIP     Aeronautical Information Publication</li>
<li>ALR     ATS ATC Alerting Message</li>
<li>AMA     OLDI Arrival Management Message</li>
<li>APL     ATS ATC Flight Plan Message</li>
<li>ARR     ATS Arrival Message</li>
<li>ATC     Air Traffic Control</li>
<li>ATS     Air Traffic Service</li>
<li>CDN     ATS Change Message</li>
<li>CDN     OLDI Coordination Message</li>
<li>CFMU    Central Flow Management Unit</li>
<li>CNL     ATS Cancel Message</li>
<li>COD     OLDI Advanced Coordination Procedure</li>
<li>CPL     OLDI Current Flight Plan Message</li>
<li>CPL     ATS Current Flight Plan Message</li>
<li>DCT     Direct (used to specify direct routing between points)</li>
<li>DEP     ATS Departure Message</li>
<li>DLA     ATS Delay Message</li>
<li>ERS     Extracted Route Sequence</li>
<li>EST     ATS Estimate Message</li>
<li>ETO     Estimated Time Over</li>
<li>FPL     ATS Flight Plan Message</li>
<li>FPR     Flight Plan Record</li>
<li>FNM     Gander Oceanic Message</li>
<li>GAT     General Air Traffic</li>
<li>GUI     Graphical User Interface</li>
<li>ICAO    International Civil Aviation Organisation</li>
<li>IFR     Instrument Flight Rules</li>
<li>IFPS    Initial Flight Planing System</li>
<li>IFPSTOP Indicates end of IFR routing (used by the CFMU IFPS)</li>
<li>IFPSTART Indicates start of IFR routing (used by the CFMU IFPS)</li>
<li>INF     OLDI Information Message</li>
<li>LAM     OLDI Logical Acknowledgement</li>
<li>MAC     OLDI Message for the Abrogation of Coordination</li>
<li>MFS     Oceanic Centre Message</li>
<li>OAT     Operational Air Traffic (typically military)</li>
<li>OCM     OLDI Oceanic Clearance Message</li>
<li>PAC     OLDI Preliminary Activation Message</li>
<li>PRP     Published Route Points</li>
<li>RAP     OLDI Referred Activate Proposal Message</li>
<li>RCF     ATS Radio communication failure</li>
<li>REJ     OLDI Reject Message</li>
<li>REV     OLDI Revision Message</li>
<li>RJC     OLDI Reject Coordination Message</li>
<li>ROC     OLDI Request Oceanic Clearance Message</li>
<li>RRV     OLDI Referred Revision Proposal Message</li>
<li>RQP     ATS Request Flight Plan Message</li>
<li>RQS     ATS Request Supplementary Flight Plan Information Message</li>
<li>SBY     OLDI Standby Message</li>
<li>SI      Metric measurement system</li>
<li>SID     Standard Instrument Departure</li>
<li>SPL     ATS Supplementary Flight Plan Message</li>
<li>STAR    Standard Arrival Route</li>
<li>VFR     Visual Flight Rules</li>
</ul>