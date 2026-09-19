# STAGE 10 — HANDOVER AND MANUFACTURER'S DATA RECORD

**Document:** NFD-ELE-MDR-0001 · Rev 0
**Register:** [`registers/mdr-index.csv`](registers/mdr-index.csv)

---

## 10.1 What the MDR is, and why it is not paperwork

The Manufacturer's Data Record is **the asset's documentation for the rest of its life.** This board will be in service for twenty to thirty years. Everyone who built it will have moved on. The MDR is the only thing that remains.

Three tests of a good MDR:

| Test | Question |
|---|---|
| **Maintenance** | Can a technician who has never seen this board fault-find it at 2 a.m. using only what is in here? |
| **Modification** | Can an engineer in ten years safely add a feeder, knowing the spare capacity, the fault level basis and the protection arrangement? |
| **Accountability** | Can anyone reconstruct *why* a decision was made — why that drive brand, why those provisional settings, why that deviation was accepted? |

If the answer to any is no, the MDR has failed, regardless of how thick it is.

> **A common and expensive failure: the as-built drawings do not match the board.** When that happens, every future maintainer eventually learns not to trust the drawings, and from then on the entire documentation set is worthless — because nobody knows which parts of it are still true.

---

## 10.2 MDR structure

### Section 1 — Introduction and index

1.1 Project description and scope
1.2 Document index (every document, with number, revision, date)
1.3 Equipment register — every major item with tag, manufacturer, model, serial number
1.4 Abbreviations and definitions
1.5 Contact details — manufacturer, designer, key vendors

### Section 2 — Design documentation

2.1 Design basis — NFD-ELE-DBS-0001, final revision
2.2 **Design input register**, showing every input, its source and its status at close-out
2.3 **Assumptions register, with the closed-out status of each assumption**
2.4 Functional description
2.5 Control philosophy
2.6 I/O list, final revision
2.7 Load schedule
2.8 Interface register

> **2.3 is the section most often omitted and most often needed.** In five years, when someone asks "what fault level was this board designed for?", the answer must be findable. If the assumption register is not in the MDR, that answer is lost and the next modification is made blind.

### Section 3 — Approved drawings

3.1 Drawing register with revision history
3.2 Single line diagram
3.3 General arrangement and cubicle layouts
3.4 Schematic diagrams — all sheets
3.5 Termination drawings and schedule
3.6 Cable schedule
3.7 Label schedule
3.8 Field control station drawings
3.9 Remote I/O drawings
3.10 Network architecture drawing

### Section 4 — As-built drawings

4.1 **As-built set, clearly marked AS-BUILT, incorporating every FAT mark-up and every punch-list rectification**
4.2 As-built drawing register
4.3 **Record of what differs between the approved set and the as-built set, and why**

> **4.3 matters.** A reader comparing the approved and as-built sets will spot differences and need to know whether each one was a defect rectification, an approved change, or an error. Without that record they cannot tell, and they will have to assume the worst.

### Section 5 — Bill of materials and equipment data

5.1 Final BOM, as-built, reconciled against the drawings
5.2 Equipment data sheets — every item
5.3 **Drive parameter schedule, as set, with a backup file**
5.4 **Protection settings schedule, as applied** *(marked PROVISIONAL — see §10.4)*
5.5 Spares list, including the recommended spares holding
5.6 Consumables and special tools

> **5.3 is genuinely valuable.** A drive parameter set represents hours of configuration. When a drive fails in service and is replaced, having the parameter file means a technician can restore it in minutes. Not having it means a drive engineer's site visit. Include the file, not just a printout.

### Section 6 — Certificates and compliance

6.1 **Manufacturer's AS/NZS 61439 design verification evidence** for the enclosure system, busbar and form of separation
6.2 Manufacturer's routine verification records for this assembly
6.3 Equipment type test certificates and compliance declarations
6.4 Electrical safety certificates as required
6.5 Calibration certificates for the test equipment used at FAT
6.6 Material certificates where required

> **6.1 and 6.2 are the manufacturer's obligations, not ours.** But if they are not obtained before final payment, they will never be obtained. Chasing them is a PE task and it is much easier before the invoice is paid than after.

### Section 7 — Test records

7.1 Approved FAT procedure
7.2 **Completed FAT sheet, signed, with every actual result recorded**
7.3 Earth continuity test results — individual readings
7.4 Insulation resistance test results — individual readings
7.5 Loop test records
7.6 Functional test records
7.7 Emergency stop test records, including the single-channel fault tests
7.8 Network and communications test records
7.9 Retest records for every punch-list item

> **"All satisfactory" is not a test record.** Individual readings are what allow a future test to be compared against the original and a degradation trend to be identified. A board tested again in ten years is meaningless without a baseline.

### Section 8 — Inspection records

8.1 In-progress inspection records — all four inspection points
8.2 Goods-inward inspection records
8.3 Non-conformance reports and their close-out

### Section 9 — Technical queries and deviations

9.1 **Technical query register, complete, with responses**
9.2 **Deviation register, with the client's written acceptance of each**
9.3 **Change register, with impact assessments and approvals**
9.4 Correspondence on technical matters

> **Section 9 is the institutional memory.** DEV-002 explains why the drives are that brand. CR-001 explains why the motors are 90 kW when the original specification said 75. FD-005 explains why the protection settings are provisional. Without this section, all of those look like errors to whoever reads the package next.

### Section 10 — Equipment manuals

10.1 VSD manuals — installation, programming, maintenance
10.2 PLC and I/O manuals
10.3 Network equipment manuals and configuration backup
10.4 Protective device manuals, including setting instructions
10.5 Power supply and UPS manuals
10.6 Safety relay manual
10.7 Power meter manual
10.8 Pilot device and terminal data

### Section 11 — Punch list and close-out

11.1 Final punch list with close-out evidence
11.2 **Items carried forward to site, with their owners** — see §10.4
11.3 Outstanding items and agreed completion dates
11.4 Close-out certificate signed by both parties

### Section 12 — Commissioning information

12.1 Recommended pre-energisation checks
12.2 Energisation procedure
12.3 **Settings to be applied before energisation** — the protection settings hold point
12.4 Site acceptance test scope, and what it must cover that the FAT could not
12.5 Known limitations of the FAT — **explicitly, what was simulated and what was not**
12.6 Maintenance schedule recommendations
12.7 **Spare capacity record** — spare feeders, spare I/O, spare terminals, spare chassis space

> **12.5 is an integrity item.** The FAT simulated the motors. It did not prove the pumps, the hydraulics, or performance under load. If that is not stated plainly, somebody will eventually read a signed FAT record and believe the pump control was proven. Say what was not tested.
>
> **12.7 is a gift to the next engineer.** A single page saying "there are two spare feeders at 63 A and 32 A, eight spare digital inputs, ten spare analogue inputs, 20 % spare terminals on each rail, and one spare chassis slot" saves someone a day of investigation and probably prevents an unnecessary new board.

---

## 10.3 Handover process

| Step | Activity | Owner |
|---|---|---|
| 1 | Punch list closed to Category A and B; Category C agreed | PE |
| 2 | As-built drawings produced from FAT mark-ups and rectifications | Designer / PE |
| 3 | MDR compiled, indexed and internally reviewed against the index | PE |
| 4 | MDR issued to client for review | PE |
| 5 | Client comments incorporated | PE |
| 6 | **Handover meeting** — walk the client through the board and the MDR | PE |
| 7 | Outstanding items, deviations and hold points formally transferred | PE → Client |
| 8 | Close-out certificate signed | Both |
| 9 | Dispatch and delivery, with transit protection and a delivery inspection | Workshop |
| 10 | Site support during installation and commissioning as contracted | PE |

### The handover meeting

This is not a document transfer. It is a briefing. What must be covered:

1. **What the board does**, walked through physically, cubicle by cubicle.
2. **Where the spare capacity is** and how to use it.
3. **What is provisional** — protection settings, and why.
4. **What was not tested at FAT** and what the SAT must therefore cover.
5. **The hold points before energisation.**
6. **Where the parameter backups and configuration files are.**
7. **The deviation and change history** — why the board differs from the original specification.
8. **Who to call**, for what, and under what warranty terms.

> **Hand over to the people who will operate and maintain it, not only to the project manager.** The project manager will be gone in six months. The maintenance technician will be there in ten years, and is the person who will either trust this documentation or learn to ignore it.

---

## 10.4 Items carried forward to site

Transferred formally and in writing, with named owners. **These do not disappear because the FAT passed.**

| # | Item | Origin | Owner | Required before | Status |
|---|---|---|---|---|---|
| CF-01 | **Protection coordination study, and application/verification of settings** | FD-005 / TQ-004 | **Client** | **Site energisation — HOLD POINT** | Open |
| CF-02 | **Prospective fault level confirmation** | TQ-002 | **Client** | Site energisation | Open |
| CF-03 | **Harmonic assessment against network limits** | TQ-006 | Client | Commissioning | Open |
| CF-04 | **Required Performance Level determination for the E-stop function** | TQ-003 | Client | Commissioning | Open |
| CF-05 | **TX-01 transformer capacity check with revised demand plus existing site loads** | TQ-011 / CR-001 | Client | Site energisation | Open |
| CF-06 | Arc flash study and label content | Design basis exclusion | Client | Site energisation | Open |
| CF-07 | Final IP address configuration | TQ-007 | Client / integrator | Commissioning | Placeholder scheme in place |
| CF-08 | Motor cable size confirmation against final AS/NZS 3008 calculation and actual route | CR-001 | Designer / installer | Installation | Open |
| CF-09 | Field instrument calibration | Interface | Client / installer | Commissioning | Open |
| CF-10 | Motor thermal parameter verification against final nameplates | CR-001 | Commissioning | Commissioning | Provisional values set |

> **This table is one of the most professionally important pages in the whole package.** It says, in writing, that a set of engineering questions remain open, who owns each one, and what must not happen until they are closed.
>
> Without it, a board arrives on site with a signed FAT certificate and everyone reasonably assumes it is finished. With it, the hold points are explicit and the risk sits with the party who actually owns it.
>
> **CF-01 and CF-05 are the two that could cause real harm** — one leaves protection unverified, the other could overload a transformer that belongs to someone else. Both are genuinely outside our scope. Both are ours to have raised, and ours to have transferred visibly.

---

## 10.5 As-built drawing production

| Step | Detail |
|---|---|
| 1 | Collect every red-marked drawing from the FAT |
| 2 | Collect every workshop mark-up captured during fabrication |
| 3 | Collect every punch-list rectification |
| 4 | Verify each mark-up against the physical board — **do not transcribe blindly** |
| 5 | Incorporate into the drawings |
| 6 | **Check the as-built against the board, physically**, before issuing |
| 7 | Mark clearly AS-BUILT with a date |
| 8 | Record what changed from the approved set, and why |
| 9 | Issue and archive |

**Step 6 is not optional.** The whole value of an as-built is that it is true. A transcribed as-built that nobody physically verified is a document that *looks* authoritative and *is* fiction — which is worse than having no as-built at all, because people will trust it.

---

## 10.6 MDR index (extract)

Full index: [`registers/mdr-index.csv`](registers/mdr-index.csv)

| Section | Document | Number | Rev | Status |
|---|---|---|---|---|
| 2.1 | Design basis | NFD-ELE-DBS-0001 | 1 | Included |
| 2.2 | Design input register | NFD-ELE-REG-0001 | 1 | Included, closed out |
| 2.3 | Assumptions register | NFD-ELE-REG-0002 | 1 | Included, with status |
| 2.4 | Functional description | NFD-ELE-FDS-0001 | 1 | Included |
| 2.6 | I/O list | NFD-ELE-IOL-0001 | 1 | Included |
| 3.2 | Single line diagram | NFD-ELE-SLD-0001 | 1 | Included |
| 3.4 | Schematics (all sheets) | NFD-ELE-SCH-00xx | 1 | Included |
| 3.5 | Termination drawings and schedule | NFD-ELE-TRM-04xx | 1 | Included |
| 4.1 | As-built drawing set | NFD-ELE-xxx-AB | AB | **Physically verified** |
| 5.1 | Final BOM, as-built | NFD-ELE-BOM-0001 | D | Reconciled |
| 5.3 | Drive parameter schedule + backup files | NFD-ELE-PAR-0001 | 0 | Included with files |
| 5.4 | Protection settings schedule | NFD-ELE-PRS-0001 | 0 | **Marked PROVISIONAL — CF-01** |
| 6.1 | Manufacturer's AS/NZS 61439 design verification evidence | Mfr document | — | Obtained |
| 7.2 | Completed FAT sheet, signed | NFD-ELE-FAT-0001 | 1 | Included with all results |
| 9.1 | Technical query register | NFD-ELE-TQR-0001 | — | Included, with open items flagged |
| 9.2 | Deviation register | NFD-ELE-DEV-0001 | — | Included with written acceptances |
| 9.3 | Change register | NFD-ELE-CHG-0001 | — | CR-001 with full impact assessment |
| 11.2 | **Items carried forward to site** | NFD-ELE-CF-0001 | 0 | **Signed by both parties** |
| 12.5 | Known limitations of the FAT | Within FAT report | 1 | **Explicit** |
| 12.7 | Spare capacity record | NFD-ELE-SPC-0001 | 0 | Included |

---

## 10.7 What the Project Engineer did at Stage 10

1. Compiled the MDR against an index agreed with the client **early** — not assembled at the end from whatever happened to exist.
2. Chased vendor certificates and the manufacturer's design verification evidence **before final payment**, because afterwards nobody answers the phone.
3. Verified the as-built drawings against the physical board rather than transcribing mark-ups.
4. Produced the carried-forward register and got it signed, so the open engineering questions transferred visibly rather than evaporating at the FAT certificate.
5. Stated explicitly, in writing, what the FAT did not prove.
6. Wrote the spare capacity record, unprompted.
7. Ran the handover meeting with the **maintenance team**, not just the project manager.
8. Included the deviation and change registers, so future engineers can understand why the board is the way it is.

---

**Next:** [Stage 11 — Portfolio Summary](11-PORTFOLIO-SUMMARY.md)
