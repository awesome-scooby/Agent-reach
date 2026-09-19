# STAGE 7 — FABRICATION AND WIRING

---

## 7.1 What the Project Engineer is actually doing in the workshop

Not building. Not supervising the wireman — a good wireman does not need supervising and will resent it.

Three things:

1. **Confirming the board being built is the board that was designed** — right revision, right devices, right arrangement.
2. **Catching the things that are cheap now and expensive later** — access, clearance, labelling, segregation, maintainability.
3. **Being available to answer questions fast**, so the workshop does not stop or, worse, improvise.

> **That third one is underrated.** A wireman who cannot get an answer in an hour will make a sensible decision and carry on. It will usually be reasonable. It will not be documented. Six months later nobody knows why that link is there. Being reachable is an engineering control.

---

## 7.2 Inspection points

Inspecting once at the end is inspecting too late. Four points:

| # | When | What it catches | Cost if found later |
|---|---|---|---|
| **1** | **Enclosure received, before fitting out** | Dimensions, construction, IP integrity, form of separation, paint, gland plates, earth bar | Enclosure return or on-site modification |
| **2** | **Equipment mounted, before wiring** | Layout, clearances, access, orientation, segregation, correct devices | Removing and remounting — moderate |
| **3** | **Wiring approximately 50 % complete** | Wiring practice, routing, ferruling, duct fill, terminal discipline | Correcting habits while there is still 50 % to go — **highest value inspection** |
| **4** | **Wiring complete, before FAT** | Completeness, labelling, workmanship, drawing status | Punch list, FAT delay |

**Inspection 3 is the one that pays.** If the wireman's ferruling convention or duct routing is wrong, finding it at 50 % means correcting half a board and getting the other half right. Finding it at 100 % means correcting a whole board, or — more likely in practice — accepting it, which sets a precedent.

---

## 7.3 What to look for, and why

### 7.3.1 Enclosure construction

| Check | Why it matters |
|---|---|
| Dimensions match the approved GA | The plinth, the switchroom door and the cable pit are all already built to it |
| Form of separation as specified | Form 3b means specific barriers between busbar, functional units and terminals. **This is verifiable by eye once you know what to look for** — and it is a contractual requirement, not a nicety. |
| Doors align, close, latch, and stay closed | A door that needs persuading will be left open |
| Hinges take the door weight with equipment mounted | Doors get heavy once the pilot devices and drive keypads are on |
| Gasket continuous, not stretched, corners intact | This is the IP rating. A stretched gasket at a corner is where water gets in. |
| Gland plates removable, undrilled, non-magnetic where required | §2.3.1 |
| Main earth bar full length, accessible, correctly sized | |
| Instrument screen bar **insulated from the enclosure**, single-point bonded | If it is bolted straight to the frame, every screen is earthed at multiple points and the single-point design is gone |
| Paint finish, no damage, colour correct | Cosmetic, but it is what the client sees first, and it sets the tone of the FAT |
| Lifting provisions adequate and marked | This board will be lifted by a rigger who has never seen it |
| Ventilation openings as designed, filters fitted | |

### 7.3.2 Equipment layout and orientation

| Check | Why |
|---|---|
| Devices match the BOM part numbers — **physically read the labels** | Substitutions and picking errors. A drive with the wrong option card looks identical. |
| Manufacturer's minimum clearances respected, especially around drives | The drive manual states them. Ignoring them causes over-temperature trips on hot days, months after handover. |
| **Orientation correct** — contactors, MPCBs and some relays are orientation-sensitive | Mounting a contactor upside down or on its side can affect its magnetic operation and its rating. Check the manual. |
| Heat-generating devices not directly below heat-sensitive ones | Drives, transformers and resistors heat what is above them. A PLC above a drive is a bad idea. |
| Devices requiring adjustment are reachable without removing other equipment | Someone has to set that MPCB after the board is installed against a wall |
| Devices requiring reading (meters, keypads, indicators) are at a sensible height | Between roughly 800 mm and 1800 mm. A drive keypad at ankle height is read by nobody. |
| Replaceable items can actually be replaced in situ | Can the PSU come out without unwiring the terminals? Can the drive be removed without dismantling the cubicle? |
| Test points and disconnect terminals accessible | |
| **Segregation of voltage zones maintained by the layout**, not just by the wiring | |
| Spare chassis space is genuinely usable, not left as an awkward gap | |

> **The maintainability checks are the ones a client's maintenance representative will notice at FAT**, and they are the ones that generate the most heated punch-list arguments — because by then they are expensive to fix and impossible to ignore.

### 7.3.3 Wiring

| Check | Why |
|---|---|
| Wire size and type per drawing and specification | |
| **Colour convention applied consistently** (AS 60204.1: red AC control, dark blue DC control, **orange for externally-sourced live conductors**) | The orange one is a safety control — §3.2 |
| Every wire ferruled **at both ends**, numbers matching the drawing | A wire ferruled at one end only is half a wire as far as fault-finding goes |
| Ferrules readable **in situ** and oriented consistently | A ferrule you must remove a wire to read is useless |
| Duct fill not excessive (leave room for additions and for the lid to close) | Overfilled duct traps heat and cannot take a future circuit |
| **Power, AC control, DC digital and analogue in separate ducts** | §4.3 |
| Wiring to doors in flexible loom with adequate service loop, strain relief both ends | The door will be opened thousands of times. Door looms are a very common failure point. |
| No wiring across hinge lines without proper flexible provision | |
| Terminations tight, to the manufacturer's torque where specified | **Loose terminations are the leading cause of switchboard fires.** Torque screwdrivers exist for a reason. |
| Bootlace ferrules on stranded conductors into screw terminals | Loose strands cause both short circuits and high-resistance joints |
| **Maximum two conductors per terminal**, and only if the terminal is rated for it | Three wires under one screw is the joint that eventually heats up |
| Screens terminated per the design — one end for instruments, 360° both ends for VSD cables | §4.4 |
| Earth conductors present and correct on every device, door and gland plate | |
| No sharp edges in contact with wiring; grommets or edge protection at every penetration | |
| Adequate slack at terminals for re-termination | A wire cut exactly to length can only be terminated once |

### 7.3.4 Terminals

| Check | Why |
|---|---|
| Rails as designed, in the designed order | |
| Terminal numbering matches the schedule exactly | |
| **Partition plates fitted between voltage groups** | Routinely forgotten. It is part of the segregation design, not decoration. |
| End brackets and end covers fitted | A rail without end brackets will spread |
| Marker strips printed **from the schedule**, not hand-written | Hand-written markers drift from the documentation immediately |
| Spare terminals fitted, labelled SPARE, and grouped as designed | |
| **Yellow terminals used for the safety circuit, and for nothing else** | |
| Disconnect terminals on every analogue loop | |
| Field side clearly distinguished from internal side | |
| Adequate access for the installer to land field cables — **can a gloved hand and a screwdriver actually get in there?** | This is judged on site, in the dark, by someone who will complain loudly |

### 7.3.5 Labels

| Check | Why |
|---|---|
| Every device labelled with its drawing tag | |
| Labels **engraved traffolyte, mechanically fixed** | Adhesive labels fall off in heat. In ten years they will be on the floor of the cubicle. |
| Label text matches the drawings and the label schedule exactly — **character for character** | "P101" vs "P-101" is a real finding and it will be raised at FAT |
| Cubicle identification labels fitted | |
| Warning labels fitted: 415 V, **multiple supplies where applicable**, CT secondary | |
| **"Multiple supplies" warning where any part of the board remains live after the main isolator is opened** — the externally-sourced interlock wiring | This is a genuine safety label. Someone will open this board believing it is dead. |
| Asset/rating nameplate fitted with the required marking information | AS/NZS 61439 marking |
| Arc flash label holder fitted (content is client scope) | |
| Terminal markers legible and correctly oriented | |

### 7.3.6 Earthing

| Check | Why |
|---|---|
| Main earth bar continuous, correctly sized, accessible | |
| Every cubicle earth bar bonded to the main bar | |
| **Every door with equipment bonded with a flexible strap** — hinges are not an earth path | |
| Every gland plate bonded | |
| Every device with an exposed conductive part bonded | |
| Instrument screen bar insulated and single-point bonded | |
| Paint removed / serrated washers used at every earth bonding point | **Powder coat is an insulator.** An earth bolted through paint is not an earth. This is a very common and very serious defect. |
| Earth continuity verified by **measurement** at FAT, not by eye | |

### 7.3.7 Drawing revision status — the check nobody remembers

| Check | Why |
|---|---|
| The drawings on the workshop bench are the **current IFC revision** | |
| Superseded drawings physically removed | |
| Any workshop mark-ups captured, not just pencilled and forgotten | **Those mark-ups are the as-built. If they are lost, the as-built is fiction.** |
| Changes made in the workshop have been through change control | |

> **Walk the workshop and look at the drawing in the wireman's hand.** Read the revision number. This takes ten seconds and it is one of the highest-value checks in this entire document. A board being wired from a superseded revision is a board that will fail FAT in ways that take days to unpick.

---

## 7.4 Inspection checklist

Also in [`registers/inspection-checklist.csv`](registers/inspection-checklist.csv).

**Board:** MCC-01 · **Inspection point:** ☐ 1 Enclosure ☐ 2 Pre-wire ☐ 3 50 % wire ☐ 4 Pre-FAT
**Date:** ________ **Inspected by:** ________ **Drawing revision on bench:** ________

| # | Check | ✔ | N/A | Comment |
|---|---|---|---|---|
| **ENCLOSURE** ||||
| 1.1 | Dimensions match approved GA | | | |
| 1.2 | Form of separation as specified (Form 3b) | | | |
| 1.3 | Doors align, close, latch correctly | | | |
| 1.4 | Gaskets continuous and undamaged at corners | | | |
| 1.5 | Gland plates removable, undrilled, non-magnetic | | | |
| 1.6 | Main earth bar full length and accessible | | | |
| 1.7 | Instrument screen bar insulated, single-point bonded | | | |
| 1.8 | Paint finish and colour correct, no damage | | | |
| 1.9 | Lifting provisions adequate and marked | | | |
| 1.10 | Ventilation and filters as designed | | | |
| **LAYOUT** ||||
| 2.1 | Devices match BOM part numbers — labels physically read | | | |
| 2.2 | Manufacturer's clearances respected (esp. drives) | | | |
| 2.3 | Device orientation correct per manufacturer | | | |
| 2.4 | Heat-generating devices not below heat-sensitive devices | | | |
| 2.5 | Adjustable devices reachable | | | |
| 2.6 | Readable devices at sensible height (800–1800 mm) | | | |
| 2.7 | Replaceable items removable in situ | | | |
| 2.8 | Voltage zone segregation maintained by layout | | | |
| 2.9 | Spare chassis space usable | | | |
| **WIRING** ||||
| 3.1 | Wire size and type per drawing | | | |
| 3.2 | Colour convention applied (incl. **orange** for external supplies) | | | |
| 3.3 | Every wire ferruled both ends, numbers match drawings | | | |
| 3.4 | Ferrules readable in situ, consistent orientation | | | |
| 3.5 | Duct fill leaves room for lid and future additions | | | |
| 3.6 | Power / AC control / DC digital / analogue in separate ducts | | | |
| 3.7 | Door wiring in flexible loom, service loop, strain relief | | | |
| 3.8 | Terminations tight, torqued where specified | | | |
| 3.9 | Bootlace ferrules on stranded conductors | | | |
| 3.10 | Max 2 conductors per terminal, terminal rated for it | | | |
| 3.11 | Screens terminated per design (1 end / 360° both ends) | | | |
| 3.12 | No sharp edges against wiring; penetrations protected | | | |
| 3.13 | Adequate slack for re-termination | | | |
| **TERMINALS** ||||
| 4.1 | Rails as designed, correct order | | | |
| 4.2 | Numbering matches termination schedule | | | |
| 4.3 | Partition plates between voltage groups | | | |
| 4.4 | End brackets and end covers fitted | | | |
| 4.5 | Marker strips printed from schedule | | | |
| 4.6 | Spare terminals fitted, labelled, grouped | | | |
| 4.7 | Yellow terminals used for safety circuit only | | | |
| 4.8 | Disconnect terminals on every analogue loop | | | |
| 4.9 | Field access adequate for glove and screwdriver | | | |
| **LABELS** ||||
| 5.1 | Every device labelled with drawing tag | | | |
| 5.2 | Engraved traffolyte, mechanically fixed | | | |
| 5.3 | Text matches drawings character for character | | | |
| 5.4 | Cubicle identification labels fitted | | | |
| 5.5 | Warning labels: 415 V, multiple supplies, CT secondary | | | |
| 5.6 | Asset / rating nameplate fitted and correct | | | |
| 5.7 | Arc flash label holder fitted | | | |
| **EARTHING** ||||
| 6.1 | Main earth bar continuous and correctly sized | | | |
| 6.2 | Cubicle earth bars bonded to main bar | | | |
| 6.3 | Every equipment-bearing door bonded with flexible strap | | | |
| 6.4 | Gland plates bonded | | | |
| 6.5 | All equipment earths present | | | |
| 6.6 | **Paint removed / serrated washers at every bonding point** | | | |
| 6.7 | Screen bar insulated, bonded at one point only | | | |
| **DOCUMENT CONTROL** ||||
| 7.1 | **Drawings on bench are current IFC revision** | | | |
| 7.2 | Superseded drawings removed from workshop | | | |
| 7.3 | Workshop mark-ups captured for as-built | | | |
| 7.4 | Any changes have been through change control | | | |
| **GENERAL** ||||
| 8.1 | Board clean, no swarf, offcuts or tools inside | | | |
| 8.2 | All packing, transit restraints and desiccant identified for removal | | | |
| 8.3 | Spares and loose items bagged, labelled and listed | | | |

**Findings raised:** ________ **Closed:** ________ **Signature:** ________

> **8.1 is not housekeeping.** Metal swarf from drilling a gland plate, sitting on a busbar shroud, is a phase-to-phase fault waiting for the first vibration. Boards get vacuumed before energisation for a reason.

---

## 7.5 Handling workshop queries

The workshop will find things. Some are errors in the design; some are the wireman being right.

| Query type | The right response |
|---|---|
| "This won't fit" | Go and look. Do not resolve a physical problem from a desk. |
| "The drawing says X but the device has Y" | Usually a real finding — often an auxiliary contact or a terminal count. Verify, then change control. |
| "Can I just…" | **The most dangerous question in the workshop.** Usually a sensible suggestion. Sometimes it changes a safety circuit, a segregation arrangement or a rating. Assess it properly, then either approve it formally or decline it with a reason. |
| "Which revision is right?" | Stop. Find out. Check what has already been built to the wrong one. |
| "This is how we normally do it" | Sometimes better than the drawing, sometimes a habit from a job with different requirements. Ask why, then decide. |

**The rule: every workshop deviation gets documented, no matter how small.** Either it goes on the drawing or it goes in the change register. A board full of undocumented "sensible decisions" cannot be maintained and its as-built is worthless.

---

## 7.6 What the Project Engineer did at Stage 7

1. Inspected at all four points, not just before FAT.
2. At Inspection 2, found the PLC mounted directly above a drive and had it relocated — cheap then, a rewire later.
3. At Inspection 3, found ferrules oriented inconsistently and unreadable on the lower terminals, and had the convention corrected while half the board remained to be wired.
4. At Inspection 3, found two earth bonds made through powder coat without serrated washers. Had every bonding point re-checked — **this is a safety defect, not a workmanship nit.**
5. Checked the drawing revision on the bench at every visit.
6. Captured every workshop mark-up as it happened, rather than trying to reconstruct the as-built afterwards.
7. Answered workshop queries same-day, so the workshop never had to improvise.

---

**Next:** [Stage 8 — Factory Acceptance Test](08-FAT.md)
