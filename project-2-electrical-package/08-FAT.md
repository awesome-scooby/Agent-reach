# STAGE 8 — FACTORY ACCEPTANCE TEST

**Document:** NFD-ELE-FAT-0001 · Rev 0
**Registers:** [`registers/fat-sheet.csv`](registers/fat-sheet.csv) · [`registers/punch-list.csv`](registers/punch-list.csv)

---

## 8.1 What a FAT is for

A FAT exists so that **problems are found in a workshop, where they are cheap, rather than on site, where they are not.**

| | Workshop | Site |
|---|---|---|
| Access to the board | Total — it is on a bench | Bolted to a plinth against a wall |
| Spare parts | On the shelf | Two days away |
| Labour | Already there | Mobilised at site rates |
| Consequence of a delay | A day in the programme | Plant unavailable, possibly a shutdown extension |
| Who is watching | The panel builder and the PE | The client, the operators and everyone's management |

**A defect found at FAT costs roughly a tenth of the same defect found at site, and a hundredth of the same defect found after handover.** That is the entire business case, and it is the answer to "why is FAT worth three days?".

A FAT is also **a contractual milestone.** Passing it usually triggers a payment and transfers a degree of risk. That is why the procedure is agreed with the client in advance, why the results are recorded, and why "we tested it and it was fine" is not an acceptable record.

---

## 8.2 Before the FAT — preparation

This is where FATs are won or lost. A FAT that starts badly rarely recovers, because the client's confidence goes early and every subsequent finding gets read through that lens.

| Item | Why | Done by |
|---|---|---|
| **FAT procedure issued to the client and approved** — at least two weeks ahead | Testing against a procedure the client has not agreed is how you get an argument about the result | PE |
| Drawings at current IFC revision, printed, on the bench | The client will check | PE |
| **Internal pre-FAT run-through completed** | Never let the client witness the first time the board is energised. Find your own defects first. | PE + workshop |
| Test equipment calibrated, with current certificates | An uncalibrated instrument invalidates the result | Workshop |
| Loop calibrator, insulation tester, low-resistance ohmmeter, multimeter, phase rotation tester | | Workshop |
| Test supply arranged, with the right protection | | Workshop |
| PLC program loaded — at the correct revision | Testing against the wrong program version wastes a day | Integrator |
| SCADA simulation or the integrator's test HMI available | Otherwise you cannot close the loop to the operator's screen | Integrator |
| Motor simulation arrangement agreed | You cannot connect 75 kW motors in a workshop. **Agree the method with the client in advance.** | PE + client |
| Attendees confirmed, including a client operations representative | Operations will raise the maintainability findings. Better at FAT than at handover. | PE |
| Punch list template ready | | PE |
| Outstanding items declared **up front** | Never let the client discover an incomplete item. Declare it in the opening. | PE |
| Safety briefing, isolation arrangements, test area controls | Live testing in a workshop with visitors present | Workshop |

> **"Never let the client witness the first energisation" is the single most practical piece of advice in this document.** Run the whole procedure internally first. Fix what you find. Then invite the client. A FAT is a demonstration, not an experiment.

### Declaring incomplete items

Open the FAT by stating what is not ready and why. A client who is told at 8 a.m. that the network switch is still on backorder and section P will be tested at a supplementary FAT will accept it. The same client who discovers it at 3 p.m., after finding it themselves, will question everything else.

---

## 8.3 FAT procedure

### A — Documentation check

| Purpose | Confirm that what is about to be tested is the approved design |
|---|---|

1. Drawing register — every drawing present, at the revision listed, matching the client's approved set.
2. BOM at current revision, reconciled against drawings.
3. Approved FAT procedure, signed.
4. Equipment data sheets and test certificates available for the MDR.
5. **Manufacturer's AS/NZS 61439 design verification evidence** for the enclosure system, busbar and form of separation. *(This is the manufacturer's obligation, not ours — but it must be produced and it belongs in the MDR.)*
6. Calibration certificates for all test equipment, current.
7. PLC program version recorded.
8. Outstanding items and deviations declared and listed.

### B — Visual inspection

9. Enclosure undamaged, paint finish acceptable.
10. Form of separation as specified.
11. Equipment layout matches the approved general arrangement.
12. All devices present and match the BOM — **physically read the part number labels**.
13. Labelling complete, engraved, mechanically fixed, text matching the drawings.
14. Warning labels fitted, including **multiple supplies** where applicable.
15. Asset/rating nameplate fitted and correct.
16. Board internally clean — no swarf, offcuts, packaging or tools.
17. Wiring workmanship: routing, duct fill, ferruling, consistency.
18. Door wiring looms, service loops and strain relief.

### C — Mechanical inspection

19. Doors open, close and latch. Door interlocks operate.
20. Every isolating handle operates and padlocks in the off position.
21. Door interlocks defeat mechanism (where fitted) operates and re-sets.
22. Withdrawable or removable items withdraw and re-insert correctly.
23. Gland plates removable; fixings complete.
24. Gaskets intact and continuous.
25. Lifting provisions secure and marked.
26. Terminal rails secure, end brackets fitted.

### D — Wiring verification

27. **Point-to-point check of every internal wire against the schematics.** Performed by someone other than the person who wired it.
28. Wire numbers verified at both ends against the drawings.
29. Terminal allocation verified against the termination schedule.
30. Terminations tight (sample torque check, with a documented sample size).
31. Conductor sizes per drawing.
32. Colour convention verified, including orange for externally-sourced conductors.
33. Maximum two conductors per terminal confirmed.

### E — Continuity and earth testing

34. **Earth continuity** from the main earth bar to: every cubicle earth bar, every door, every gland plate, every equipment earth. Measured with a low-resistance ohmmeter at a defined test current, results recorded individually. *(Acceptance criterion to be per the client's specification — a value should not be asserted here without it.)*
35. Instrument screen bar confirmed **insulated** from the enclosure and bonded at one point only.
36. Continuity of every control circuit per schematic.
37. Continuity from every field terminal to its destination device.
38. Phase continuity and phase identification through the busbar to every feeder.

### F — Insulation resistance testing

39. **Before testing: disconnect or bypass all electronic equipment.** Drives, PLC modules, power supplies, UPS, surge protective devices, power meter, electronic trip units.

> **This is a real and expensive trap.** Applying a 500 V or 1000 V insulation test to a circuit with a surge protective device connected will operate the SPD. Applying it to PLC I/O or drive control terminals will damage them. The devices to disconnect must be **listed in the FAT procedure before the day**, not remembered on the day. Damaging a drive during the insulation test of its own board is an embarrassing and entirely avoidable way to fail a FAT.

40. Insulation resistance, power circuits: phase-to-phase, phase-to-neutral, phase-to-earth, neutral-to-earth. Test voltage and acceptance criteria per the client's specification.
41. Insulation resistance, control circuits (electronics disconnected), at a test voltage appropriate to the circuit.
42. Record every reading individually — not "all satisfactory".
43. Reconnect all disconnected equipment and **record the reconnection as a signed step.** A device left disconnected after insulation testing is a classic post-FAT defect.

### G — Control power energisation

44. Energise 240 V AC supply. Verify voltage.
45. Verify UPS operation, on-line status, and the status contacts.
46. Energise PSU-1 with PSU-2 isolated. Verify 24 V DC bus.
47. Energise PSU-2 with PSU-1 isolated. Verify 24 V DC bus.
48. Both energised — verify redundancy module operation and load sharing behaviour.
49. **Fail PSU-1 with the load connected — verify no interruption to the 24 V bus and that the PSU-1 fail alarm is raised.** Repeat for PSU-2.
50. Verify each electronic circuit protector group is live and correctly allocated.
51. Trip one ECP group — verify only that group is affected and the status alarm is raised.
52. Verify PLC powers up, no faults, correct program version.
53. Verify network switch and all network devices are reachable.

### H — Functional testing

54. Lamp test — every indicator operates.
55. For each feeder: selector switch positions produce the correct mode, and the PLC reads the correct position combination.
56. Start and stop from the MCC pushbuttons in Local.
57. Start and stop from the local control station in Local.
58. Start and stop from the PLC/SCADA in Remote.
59. Verify Local commands are ignored in Remote and vice versa.
60. Verify Off position prevents all operation and the PLC reports the feeder unavailable.
61. Running, fault and available indication at the MCC and at the LCS.
62. Contactor pull-in and drop-out on each DOL feeder, verified by the **contactor auxiliary contact**, not the PLC output.
63. Discrepancy alarms: commanded-but-not-running, and running-but-not-commanded.
64. Duty rotation logic — verify changeover on run hours.
65. Duty/standby changeover on simulated duty pump fault.

### I — Interlock and permissive testing

66. Each permissive tested individually: remove it, verify the start is blocked, verify the correct reason is reported to SCADA.

| Permissive | Method |
|---|---|
| Drive healthy | Force a drive fault |
| Thermistor relay | Open the thermistor circuit at the terminal |
| Low-low level float | Open the float circuit at the terminal |
| Seal water flow | Open the flow switch circuit at the terminal |
| Discharge valve open | Open the limit switch circuit at the terminal |
| Feeder available | Open Q11 |
| E-stop healthy | Press an E-stop |
| Wet well level | Inject a level below setpoint |

67. **Verify the hardwired dry-run trip operates with the PLC in program-stop mode.** *(This is the whole point of hardwiring it. If it is not tested with the PLC stopped, it has not been tested.)*
68. Verify the seal-water start bypass timer operates and then enforces the permissive.
69. Verify the HVAC-fail interlock ramps the drives to minimum speed and alarms (TQ-005 outcome).

### J — Protection verification

70. Record the settings actually applied to every adjustable protective device, against the coordination study.

> **If the coordination study is not available, this test cannot be completed.** Record it as an outstanding item and as a FAT deviation. Do not invent settings and do not record "as found". **In this package, TQ-004 was still open at FAT — see Defect FD-005.**

71. Verify MPCB thermal settings against confirmed motor full-load current.
72. Verify drive motor thermal parameters against motor nameplate data.
73. Operate the trip mechanism on each protective device (test button where provided) and verify the auxiliary/trip indication reaches the PLC.
74. Verify phase failure relay operates on simulated phase loss and the alarm is raised.
75. Verify SPD status contact reports correctly.
76. Verify CT shorting links present, CT secondary warning label fitted, and the power meter reads correctly on injected or applied current.

### K — PLC I/O simulation

77. **Every digital input**: operate the field device or short the field terminals; verify the bit at the PLC **and** the tag at SCADA. Verify the description matches the I/O list.
78. **Every digital output**: force the output; verify the interposing relay operates, verify the field terminal changes state, verify the status at SCADA.
79. **Every analogue input**: inject 4, 8, 12, 16 and 20 mA at the field terminal. Verify engineering units at the PLC and at SCADA at each point. Verify scaling and units.
80. **Every analogue output**: command 0 %, 25 %, 50 %, 75 %, 100 %. Measure the current at the field terminal. Verify the receiving device responds.
81. **Verify live-zero detection** on each analogue input: open the loop, verify the fault is detected and alarmed.
82. Verify every spare I/O point is terminated, labelled and available.
83. Verify fail-safe wiring on critical inputs: **disconnect the field wire and verify the signal reads as a fault, not as healthy.**

### L — Alarm testing

84. Every alarm generated at source, verified at the PLC and at SCADA, with the correct description, priority and time stamp.
85. Common alarm beacon and sounder operate.
86. Alarm acknowledge and reset behaviour.
87. Latched alarms remain latched until acknowledged.
88. Verify alarms that must survive a power interruption do so.

### M — Emergency stop testing

89. **Each E-stop device individually**: operate it, verify both drives go to STO, verify DOL contactors drop, verify the alarm at SCADA.
90. Verify the plant cannot restart while the E-stop is latched.
91. Verify reset requires the E-stop to be released **and** the reset button to be pressed and released.
92. Verify the reset does not occur on press (monitored reset acts on release).
93. **Single-channel fault simulation**: open channel A only. Verify the safety relay detects the discrepancy, goes to the safe state, and will not reset until the fault is cleared. Repeat for channel B.
94. Verify safety relay auxiliary status reaches the PLC and SCADA.
95. Verify E-stop function with the PLC in program-stop mode — the safety function must not depend on the PLC.

> **Test 93 is the one that gets skipped, and it is the one that matters.** Anyone can press an E-stop and watch the plant stop. Proving that a *single broken wire* is detected is what distinguishes a dual-channel safety circuit from two single-channel circuits in parallel.

### N — Local / remote control

96. Verified under H, and repeated per feeder with the mode logic recorded.
97. Verify **all permissives and trips remain active in Local mode** — §3.5.3.

### O — VSD operation simulation

98. Motor simulation method per the agreed arrangement (small test motor, or drive in a no-motor test mode per the manufacturer's procedure — **agreed with the client in advance**).
99. Drive parameters verified against the parameter schedule, and the full parameter set backed up and recorded.
100. Run command, start, ramp, stop, ramp-down.
101. Speed reference tracking: verify commanded speed against actual speed at 0, 25, 50, 75 and 100 %.
102. Verify minimum and maximum speed clamps.
103. Verify acceleration and deceleration ramp times.
104. Verify STO operation from the safety relay, both channels.
105. Verify drive fault, healthy and running signals reach the PLC via both the hardwired route and the network.
106. Verify live-zero response on loss of the speed reference (configured to hold last speed and alarm).
107. Verify motor thermal protection parameters and the external thermistor trip input.

> **Be honest about what motor simulation can and cannot prove.** Running a drive into a small test motor or in a test mode proves the control circuit, the sequencing, the signalling and the parameters. It does **not** prove performance under load, it does not prove the pump's hydraulic behaviour, and it does not prove the motor. Those are commissioning and SAT activities. Claiming a FAT proved the pump control is wrong.

### P — Network and communications

108. Verify every network device is reachable at its assigned IP address.
109. Verify the address schedule matches the issued IP schedule.
110. Verify fibre links — light levels within specification, and continuity to the far end where practicable.
111. Verify switch configuration: VLANs, port settings, management access.
112. Verify drive data over EtherNet/IP: status, speed, current, fault codes.
113. Verify power meter data.
114. Verify remote I/O node communication and every RIO point.
115. **Verify behaviour on network failure**: disconnect the network and confirm hardwired control still functions, and that a comms-fail alarm is raised.

### Q — Nameplate and label verification

116. Every label checked against the label schedule, character for character.
117. Asset/rating nameplate content verified against AS/NZS 61439 marking requirements.
118. Terminal markers checked against the termination schedule.
119. Warning labels present and correct.
120. Arc flash label holder present (content is client scope).

### R — Drawing mark-ups

121. Every discrepancy found during the FAT marked on the drawings, in red, as it is found — **not reconstructed at the end.**
122. Marked-up drawings signed and dated by the person who marked them.
123. Marked-up set retained as the basis for the as-built drawings.

### S — Punch list

124. Every defect recorded with a category, an owner, an action and a due date.
125. Categories agreed with the client before the FAT starts (see §8.5).
126. Punch list signed by both parties at the close of the FAT.
127. Retest requirements for each item identified and agreed **at the time**, not later.

---

## 8.4 FAT sheet (extract)

Full sheet: [`registers/fat-sheet.csv`](registers/fat-sheet.csv) — 127 tests.

**Board:** MCC-01 · **Drawing revision:** 1 · **Date:** ______ · **Tested by:** ______ · **Witnessed by:** ______

| Test No. | Test Description | Expected Result | Actual Result | Pass/Fail | Comments |
|---|---|---|---|---|---|
| A-01 | Drawing register complete, all drawings at listed revision | All present at Rev 1 | All present at Rev 1 | **Pass** | |
| A-05 | Manufacturer's AS/NZS 61439 design verification evidence available | Documentation provided | Provided | **Pass** | Filed in MDR §7 |
| B-12 | All devices present and match BOM part numbers | Match BOM Rev D | 1 discrepancy | **FAIL** | **FD-002** — see §8.6 |
| C-20 | Every isolating handle operates and padlocks off | All operate and lock | All operate and lock | **Pass** | |
| D-27 | Point-to-point wiring check against schematics | All correct | 1 discrepancy | **FAIL** | **FD-001** |
| E-34 | Earth continuity, MEB to each door | Within specified criterion | All within criterion, recorded individually | **Pass** | See attached results sheet |
| E-35 | Instrument screen bar insulated from enclosure | > 1 MΩ | 0 Ω | **FAIL** | **FD-003** |
| F-39 | All electronic equipment disconnected before IR test | Per disconnection list, signed | Complete, signed | **Pass** | |
| F-40 | IR test, power circuits | Per client criterion | All within criterion, recorded | **Pass** | |
| F-43 | All disconnected equipment reconnected and verified | Signed reconnection check | Complete, signed | **Pass** | |
| G-49 | Fail PSU-1 under load — no interruption, alarm raised | Bus holds, alarm at SCADA | Bus holds, alarm at SCADA | **Pass** | |
| G-51 | Trip one ECP group — only that group affected | Group isolated, alarm raised | Correct | **Pass** | |
| H-59 | Local commands ignored in Remote | Ignored | Ignored | **Pass** | |
| H-62 | DOL contactor verified by auxiliary contact | Aux confirms operation | Correct | **Pass** | |
| I-66a | Remove thermistor permissive — start blocked | Start blocked, correct reason at SCADA | Blocked, **reason incorrect** | **FAIL** | **FD-004** |
| I-67 | Hardwired dry-run trip with PLC in program-stop | Drive trips | Drive trips | **Pass** | Critical test |
| J-70 | Protection settings recorded against coordination study | Settings applied and recorded | **Study not available** | **N/A — DEVIATION** | **FD-005** |
| K-79 | Analogue input injection, LIT-101, 5 points | EU correct at PLC and SCADA at each point | Correct at all 5 | **Pass** | |
| K-83 | Fail-safe check — disconnect critical DI, reads fault | Reads fault | Reads fault | **Pass** | |
| M-89 | Each E-stop individually — STO, contactors drop, alarm | All operate | All operate | **Pass** | |
| M-93 | Single-channel fault — discrepancy detected, safe state | Detected, will not reset | Detected, will not reset | **Pass** | |
| O-101 | Speed reference tracking at 0/25/50/75/100 % | Within tolerance | Within tolerance | **Pass** | Test motor, no load |
| P-115 | Network failure — hardwired control still functions | Control retained, alarm raised | Control retained, alarm raised | **Pass** | Validates the hardwired design decision |
| Q-116 | Labels checked against label schedule | All match | 3 discrepancies | **FAIL** | **FD-006** |

---

## 8.5 Defect categories

Agreed with the client **before** the FAT starts. Arguing about categories after a defect is found is a bad conversation.

| Cat. | Definition | Consequence |
|---|---|---|
| **A** | Safety-related, or prevents the board performing its intended function | **FAT fails.** Rectify and retest before dispatch. |
| **B** | Functional defect not preventing overall operation; or a documentation defect affecting the ability to install, commission or maintain | FAT passes with conditions. Rectify before dispatch, or by agreement before site energisation. |
| **C** | Cosmetic or minor, no functional or safety impact | FAT passes. Rectify before handover. |

---

## 8.6 FAT defects — worked in full

### FD-001 — Wiring error: reversed thermistor relay contact

| | |
|---|---|
| **Test** | D-27 point-to-point wiring check |
| **Category** | **A** |

**What was discovered.** The thermistor relay KT101's output contact was wired into the drive's external fault input using the **normally open** contact instead of the normally closed contact. The schematic correctly shows NC.

**Technical consequence.** This is the serious kind of defect because **it tests as working under normal conditions and fails only when you need it.** With the NO contact wired, the circuit is open in normal operation — so if the drive is configured for a normally-closed external fault input, the pump would simply never start, and the error would be found immediately. But if the drive's external fault input polarity was also set to suit, the pump would run normally and **the motor over-temperature trip would never operate.** A 75 kW motor would run to destruction with no protection from its own thermistors.

More broadly: the entire reason for fitting an independent thermistor relay alongside the drive's thermal model (§2.3.7) would have been silently defeated.

**Immediate action.** Rewired to the NC contact. Verified by re-running test I-66a, and separately by opening the thermistor circuit at terminal X3:013 and confirming the drive trips.

**Engineering approval required?** No. The schematic was correct; the wiring was wrong. This is rectification, not a change.

**Drawings / BOM revision?** No.

**Retest required?** Yes — tests D-27 (that circuit), I-66a, and the full thermistor trip verification.

**Root cause and the real lesson.** The wireman worked from the correct drawing and read the contact designation incorrectly — an easy error on a device where the NO and NC terminals are adjacent and similarly marked.

**Why it was caught:** because test D-27 is a point-to-point check **performed by someone other than the person who wired it.** A self-check would very likely have repeated the same misreading. That independence requirement is not bureaucracy; it is the control that caught this.

---

### FD-002 — Incorrect component supplied: contactor coil voltage

| | |
|---|---|
| **Test** | B-12 device verification against BOM |
| **Category** | **A** |

**What was discovered.** Contactor KM103 (sump pump feeder) was fitted with a **240 V AC coil** (LC1D09**P7**) instead of the specified **24 V DC coil** (LC1D09**BD**). Physically near-identical; the difference is in the coil marking and the suffix of the part number.

**Technical consequence.** The feeder would not operate from the 24 V DC control system — the coil would not pull in reliably at 24 V DC, if at all. Worse, had somebody "solved" the problem by connecting it to the 240 V AC services supply, the result would be a 240 V AC circuit running through ELV terminals, in the ELV duct, alongside 24 V DC wiring, and back to a field control station designed for ELV. **That is a serious safety defect and exactly the kind of well-intentioned improvisation that a proper defect process exists to prevent.**

**Immediate action.** Feeder isolated. Correct contactor sourced — in stock, replaced same day. Every other contactor and relay coil in the board was then **physically verified**, because a picking error of this type is rarely isolated. One further incorrect device was found.

**Engineering approval required?** No.

**Drawings / BOM revision?** No — the BOM was correct.

**Retest required?** Yes — tests D-27 (that feeder), H-56 through H-63 for that feeder, and I-66 permissives for that feeder.

**Root cause.** Supplier picking error, not caught at goods-inward inspection.

**The process lesson, and it is a general one:** goods-inward inspection must check **part numbers, not descriptions**. "Contactor 9 A" on a delivery docket matches both parts. The suffix is the whole difference. This is a control that costs minutes and prevented — in this case, failed to prevent — a day of FAT.

**The second lesson:** when you find one picking error, check the whole class. The second incorrect device would otherwise have been found at site.

---

### FD-003 — Instrument screen bar bonded at multiple points

| | |
|---|---|
| **Test** | E-35 screen bar insulation check |
| **Category** | **B** |

**What was discovered.** The instrument screen earth bar measured 0 Ω to the enclosure. It was designed to be insulated from the enclosure and bonded to the main earth bar at **one point only**. The mounting standoffs were insulating, but one of the mounting screws had been fitted through to the mounting plate.

**Technical consequence.** The single-point screen earthing design was defeated. Every instrument screen was effectively earthed at the MCC via multiple paths. In the workshop this causes no visible problem. On site, with a real earthing system and real potential differences between points, it creates earth loops — and the symptom is noisy, drifting or intermittently wrong analogue readings, which is one of the hardest classes of fault to diagnose after commissioning.

**Immediate action.** Correct insulating hardware fitted, insulation re-verified, single-point bond confirmed to the main earth bar.

**Engineering approval required?** No.

**Drawings / BOM revision?** The general arrangement was annotated to show the screen bar mounting detail explicitly, because the original drawing said "insulated bar" without detailing the mounting. **That is a design clarity defect, not just a workmanship defect** — if the drawing had been clear, the error was less likely.

**Retest required?** Yes — E-35, and a re-check of every screen termination.

**Why this matters more than it looks.** This is a defect with no symptom in a workshop and an expensive, persistent symptom on site. It is only found by **testing for it deliberately.** If the FAT procedure did not include test E-35, this board would have shipped with the defect and the instrument noise would have been blamed on the field cabling, the transmitters, or the installation contractor for months.

---

### FD-004 — Incorrect alarm description at SCADA

| | |
|---|---|
| **Test** | I-66a permissive testing |
| **Category** | **B** |

**What was discovered.** Removing the thermistor permissive correctly blocked the start, but SCADA reported *"P-101 Seal Water Fail"* instead of *"P-101 Motor Over Temperature"*. Two alarm descriptions had been transposed in the PLC program.

**Technical consequence.** The protection worked. The **information** was wrong — and on a remote or unattended station the alarm description is the entire basis of the operator's response. An operator told the seal water has failed will check the seal water supply, find it healthy, reset, and restart a pump with a hot motor. **A misleading alarm is worse than no alarm, because it directs effort in the wrong direction and it erodes trust in every other alarm on the screen.**

**Immediate action.** Raised with the systems integrator. Corrected in the PLC program the same day. **Every alarm description on the board was then re-verified against the I/O list**, not just the two that were found — because a transposition in one place suggests the possibility of others. Two further minor description errors were found.

**Engineering approval required?** No — the I/O list was correct, the program did not match it.

**Drawings / BOM revision?** No.

**Retest required?** Yes — the full alarm test, section L, repeated in its entirety. Not just the corrected points.

**Root cause.** The integrator worked from a slightly earlier I/O list revision in which two descriptions had been adjacent and later changed.

**The lesson, and it is the one from Stage 3:** *the I/O list must be issued to the integrator at the same revision as the board, on a transmittal.* This is exactly the failure mode that document control is there to prevent, and it is exactly how it manifests — not as a dramatic failure, but as two swapped words that would have misled operators for years.

---

### FD-005 — Protection settings cannot be verified (deviation, not a defect)

| | |
|---|---|
| **Test** | J-70 protection settings verification |
| **Category** | **Deviation — carried forward** |

**What was discovered.** The protection coordination study (TQ-004) was still not available at the time of FAT. The adjustable settings on the incomer and feeder breakers could not be verified against any approved basis.

**Technical consequence.** The board is fully functional, but the protective device settings are provisional. **Discrimination between the incomer and the feeders is unverified** — meaning a feeder fault might trip the incomer and black out the entire station instead of just the faulted feeder. The devices will protect against a fault; whether they do so selectively is unknown.

**Immediate action.**
- Recorded as a **FAT deviation**, not a pass and not a defect. The distinction matters: a defect is something we got wrong; a deviation is something that cannot be completed for reasons outside our scope.
- Devices set to conservative provisional settings, and **every setting recorded on a settings sheet** and included in the MDR.
- A warning label fitted inside the board stating the settings are provisional and subject to the coordination study.
- Formal written notification to the client that settings must be applied and verified before energisation on site, and that this is a hold point for site energisation.
- TQ-004 re-escalated.

**Engineering approval required?** Yes — the client must accept the deviation, in writing, to allow dispatch.

**Drawings / BOM revision?** No, but the settings sheet becomes an MDR deliverable that is explicitly marked incomplete.

**Retest required?** Yes, on site, once settings are available. Verification of applied settings becomes a **SAT hold point**.

**Why this is handled as a deviation and not quietly passed.** It would be easy to record "settings applied" and move on. That would transfer an unverified protection arrangement into service with a signed FAT record implying it had been verified. If a feeder fault later blacked out the station, the FAT record would be the document everyone read — and it would be wrong.

> **This is the defect that best demonstrates engineering integrity, and it is worth being able to talk about.** The correct answer to "we can't test this" is never "mark it as passed". It is: record it as a deviation, state the consequence, get written acceptance, and put a hold point where the risk actually lands.

---

### FD-006 — Label discrepancies

| | |
|---|---|
| **Test** | Q-116 label verification |
| **Category** | **C** (two items) and **B** (one item) |

**What was discovered.** Three label errors:

1. `P101` on a door label where the drawing says `P-101` (Category C).
2. A terminal marker strip on rail X3 with two markers transposed (Category **B**).
3. The **"multiple supplies"** warning label was not fitted, despite the board containing externally-sourced conductors at the MOV-101 interface (Category **B**).

**Technical consequence.**
- Item 1 is cosmetic, but label-to-drawing consistency is a real requirement — a maintainer searching drawings for "P101" may not find "P-101", and it is exactly the kind of small inconsistency that accumulates.
- Item 2 is genuinely dangerous to maintainability. A transposed terminal marker means someone lands a wire on the wrong terminal while believing they have followed the schedule correctly. It is a defect that actively causes future errors.
- **Item 3 is a safety defect.** Someone will isolate this board at the main switch, believe it is dead, and open it. The externally-sourced conductors at the MOV interface will still be live. That warning label is the only thing telling them.

**Immediate action.** All three corrected. Full label check re-run.

**Engineering approval required?** No.

**Drawings / BOM revision?** The label schedule was updated to explicitly include the multiple-supplies label — it had been omitted from the schedule, not just from the board. **The root cause was a documentation omission, not a manufacturing one**, so fixing the board alone would have left the next board to repeat it.

**Retest required?** Section Q repeated.

**Reflection on the categorisation.** It is tempting to file everything labelled "label" as cosmetic. Two of these three were not. **Category is determined by consequence, not by the type of item.**

---

## 8.7 Punch list management

Full list: [`registers/punch-list.csv`](registers/punch-list.csv)

| # | Description | Cat. | Raised by | Owner | Action | Retest | Due | Status |
|---|---|---|---|---|---|---|---|---|
| FD-001 | KT101 contact wired NO instead of NC | A | PE | Workshop | Rewire to NC | D-27, I-66a | Day 1 | **Closed** |
| FD-002 | KM103 incorrect coil voltage (240 V AC supplied) | A | PE | Workshop | Replace; verify all coils | D-27, H-56→63 | Day 1 | **Closed** |
| FD-003 | Screen bar bonded at multiple points | B | PE | Workshop | Insulating hardware; annotate GA | E-35 | Day 2 | **Closed** |
| FD-004 | Alarm descriptions transposed at SCADA | B | Client | Integrator | Correct program; re-verify all | Section L | Day 2 | **Closed** |
| FD-005 | Protection settings unverified — no coordination study | **Dev** | PE | **Client** | Provide study; apply and verify on site | J-70 at SAT | **SAT hold point** | **Open — carried** |
| FD-006a | Door label `P101` should read `P-101` | C | Client | Workshop | Re-engrave | Q-116 | Day 3 | **Closed** |
| FD-006b | X3 terminal markers transposed | B | PE | Workshop | Reprint from schedule | Q-118 | Day 2 | **Closed** |
| FD-006c | Multiple-supplies warning label missing | B | PE | Workshop | Fit label; update label schedule | Q-119 | Day 2 | **Closed** |

### Rules for running a punch list

1. **Raise it when it is found, in front of the client.** A defect found by the PE and recorded openly builds confidence. The same defect found by the client after the PE noticed and said nothing destroys it.
2. **Category is agreed at the time**, not renegotiated later.
3. **Every item has one named owner.** "The workshop" is not an owner; a person is.
4. **Retest requirements are agreed at the time.** Deciding later what needs retesting always produces an argument and usually produces under-testing.
5. **Retest the whole section, not just the corrected point**, where the defect suggests a class of error. FD-004 was two transposed descriptions; re-running the full alarm test found two more.
6. **A deviation is not a defect and must not be recorded as closed.** FD-005 stays open and becomes a SAT hold point.
7. **Nothing ships with an open Category A.**
8. **Close-out is signed by both parties**, with evidence — a retest record, a photograph, a revised drawing.

---

## 8.8 What the Project Engineer did at Stage 8

1. Wrote the FAT procedure and had the client approve it two weeks ahead.
2. Ran the whole procedure internally first. Found and fixed several defects before the client arrived.
3. Agreed the motor simulation method with the client in advance, and agreed defect categories in advance.
4. Listed the equipment to disconnect before insulation testing, in the procedure, and made reconnection a signed step.
5. Opened the FAT by declaring the outstanding items, including the missing coordination study.
6. Raised defects openly as they were found, including those the client had not noticed.
7. Insisted on independent point-to-point checking — which is what caught FD-001.
8. Refused to record the protection settings as verified, and converted it into a documented deviation with a SAT hold point.
9. Widened the check when a defect suggested a class of error (FD-002, FD-004, FD-006).
10. Marked up the drawings in red as findings occurred, and had the mark-ups signed — so the as-built is a record, not a reconstruction.

---

**Next:** [Stage 9 — Design Change](09-DESIGN-CHANGE.md)
