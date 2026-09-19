# STAGE 5 — BILL OF MATERIALS

**Document:** NFD-ELE-BOM-0001 · Rev C
**Register:** [`registers/bom.csv`](registers/bom.csv) · [`registers/project-2-registers.xlsx`](registers/project-2-registers.xlsx)

---

## ⚠ Read this before quoting any part number

Catalogue numbers below are **indicative**, selected from current manufacturer product families so the BOM reads like a real one. **Some of them will be wrong.** Catalogue numbers change, accessories get missed, and coil-voltage, curve and pole-count variants are the most commonly botched field in any switchboard BOM.

The correct professional statement — and it is what actually happens — is:

> *"Every part number is verified against the manufacturer's current catalogue and confirmed on the vendor's quotation before a purchase order is raised. That verification is part of the Project Engineer's BOM review, and it catches things every single time."*

Do not present any part number here as verified. See [`00-CLAIM-INTEGRITY.md`](00-CLAIM-INTEGRITY.md).

---

## 5.1 What a BOM is actually for

A BOM is not a shopping list. It is **the point where the drawings become money and time.**

| It answers | For whom |
|---|---|
| What must be bought, and how many | Procurement |
| When must it be ordered so the build is not held up | Project Engineer / planner |
| Does every device on the drawings physically exist in the order | Project Engineer |
| Can the board actually be built from this | Workshop |
| What does this package cost | Commercial |

The BOM is also the first place where a drawing error becomes expensive. A missing auxiliary contact block on a drawing costs nothing. The same omission in the BOM stops a wireman.

---

## 5.2 Bill of materials

**Status key:** `OK` = quoted and verified · `PO` = purchase order placed · `REC` = received · `HOLD` = held pending an open item · `TBC` = not yet verified

> **Note on revision.** The BOM below is shown at **Rev C — the state before the motor uprate.** The CSV and XLSX in `registers/` are at **Rev D**, incorporating CR-001 (see [Stage 9](09-DESIGN-CHANGE.md)) and the DR-002 auxiliary contact addition. Comparing the two is a useful exercise in itself: it shows exactly which BOM lines a single design change touches.

### A — Enclosure and structure

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| A01 | MCC enclosure, floor standing, Form 3b, 5 cubicles, 2300 H × 3000 W × 600 D | Panel builder (custom) | Fabrication drawing NFD-ELE-GA-0020 | 1 | IP42 indoor | GA-0020 | **8 wks fab** | **HOLD** | **Cannot release to fabrication until cable entry direction confirmed — TQ-001.** Design verification evidence (AS/NZS 61439.1) required from manufacturer for the MDR. |
| A02 | Gland plate, removable, undrilled, aluminium, 600 × 400 | Panel builder | Per GA-0020 | 5 | — | GA-0020 | With A01 | HOLD | Non-magnetic. Bonded to cubicle earth. |
| A03 | Plinth, 100 mm, galvanised | Panel builder | Per GA-0020 | 1 set | — | GA-0020 | With A01 | HOLD | Height/fixing to suit civil plinth — confirm with civil |
| A04 | Cubicle internal lighting, LED, with door switch | Rittal | SZ 2500.100 | 5 | 240 V AC | SCH-0030/22 | 3 wks | OK | |
| A05 | GPO, double, 10 A, DIN mount | Clipsal | 56 series equiv., DIN | 2 | 240 V AC | SCH-0030/24 | 2 wks | OK | For laptop at FAT and site |
| A06 | Anti-condensation heater, 50 W, with guard | Rittal | SK 3105.340 | 5 | 240 V AC | SCH-0030/26 | 3 wks | OK | Heat source — include in thermal declaration |
| A07 | Hygrostat, DIN mount | Rittal | SK 3118.000 | 2 | — | SCH-0030/26 | 3 wks | OK | |
| A08 | Door earth bonding strap, flexible, 4 mm², 300 mm | Generic | — | 12 | — | GA-0020 | 1 wk | OK | Every door carrying equipment |
| A09 | Main earth bar, tinned copper, 50 × 6, full board length | Panel builder | — | 1 | — | SLD-0001 | With A01 | HOLD | |
| A10 | Instrument screen earth bar, insulated, 25 × 3 | Panel builder | — | 1 | — | TRM-0401 | With A01 | HOLD | **Single-point bonded to A09** |
| A11 | Busbar system, 800 A, 3P + full N, with supports and shrouding | Panel builder | Per GA-0020 | 1 set | 800 A, Icw TBC | SLD-0001 | With A01 | **HOLD** | **Icw cannot be finalised until fault level confirmed — TQ-002.** Full-size neutral (harmonics). |
| A12 | Escutcheon / blanking panels for spare chassis space | Panel builder | — | 1 set | — | GA-0020 | With A01 | HOLD | |

### B — Incomer and main protection

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| B01 | Main circuit breaker, MCCB, 4-pole, electronic trip unit | Schneider Electric | ComPacT NSX630N + MicroLogic 2.3 | 1 | 630 A, Icu 50 kA @ 415 V | SLD-0001 | 8–10 wks | **HOLD** | **Icu provisional against 25 kA assumption — TQ-002. Settings from coordination study, not yet available.** |
| B02 | Rotary handle, door-interlocked, lockable off, extended | Schneider Electric | ComPacT rotary handle kit | 1 | — | GA-0020 | With B01 | HOLD | |
| B03 | Auxiliary contact kit — OF (status) + SD (trip indication) | Schneider Electric | ComPacT aux kit | 1 set | — | SCH-0201/01 | With B01 | HOLD | Both signals to PLC — status and trip are different alarms |
| B04 | Current transformer, 600/5 A, metering class | Schneider Electric | METSECT5MB060 | 3 | 600/5, Cl. 0.5 | SLD-0001 | 6 wks | **TBC** | **Class and burden to be verified against meter + lead length. Confirm whether revenue-grade metering is required.** |
| B05 | Power meter, EtherNet/IP | Schneider Electric | PowerLogic PM5560 (METSEPM5560) | 1 | — | SLD-0001 | 6 wks | OK | Energy, PQ logging, harmonic indication |
| B06 | Surge protective device, Type 1+2 | Schneider Electric | Acti9 iPRD1 25r | 1 | 3P+N | SLD-0001 | 4 wks | OK | Status contact to PLC. **Connecting lead length is critical to performance — installation detail.** |
| B07 | SPD protective device, 3P+N | Schneider Electric | Acti9 iC60 (rating per SPD manual) | 1 | Per B06 manual | SLD-0001 | 4 wks | TBC | **Rating must come from the SPD manual, not guessed** |
| B08 | Phase failure / phase sequence relay | Schneider Electric | Zelio RM35TF30 | 1 | 415 V | SCH-0201/06 | 4 wks | OK | Permissive + alarm, not a trip |

### C — VSD feeders (2 off — P-101, P-102)

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| C01 | Feeder MCCB, 3-pole | Schneider Electric | ComPacT NSX250N, TMD trip | 2 | 250 A, Icu 50 kA | SLD-0001 | 8 wks | **HOLD** | **Rating must be confirmed from the drive manual, not from motor FLC.** |
| C02 | Rotary handle, door-interlocked, lockable | Schneider Electric | ComPacT handle kit | 2 | — | GA-0020 | With C01 | HOLD | |
| C03 | Auxiliary contacts, OF + SD | Schneider Electric | ComPacT aux kit | 2 set | — | SCH-0201/01 | With C01 | HOLD | |
| C04 | Variable speed drive, 75 kW, 380–480 V, IP20/IP21 | Danfoss | VLT AQUA Drive FC202, type code to be finalised | 2 | 75 kW, 415 V | SLD-0001, SCH-0101 | **14–16 wks** | **HOLD** | **LONGEST LEAD ITEM.** Type code (enclosure, EMC filter class, control card, coating, keypad) must be confirmed before PO. **See DR-005.** |
| C05 | Line reactor, 3 % impedance | Danfoss | Per drive selection guide | 2 | 75 kW | SLD-0001 | 10 wks | **HOLD** | **Provisional — subject to harmonic assessment TQ-006 and confirmed motor cable length.** May be superseded by an active harmonic filter. |
| C06 | EMC cable gland, 360° screen termination | CMP / Lapp | Size to suit final cable | 4 | — | TRM | 4 wks | TBC | Size depends on confirmed cable — **do not order before cable size is fixed** |
| C07 | PTC thermistor protection relay | Schneider Electric | TeSys LT3SA00M | 2 | 24 V DC | SCH-0101/08 | 6 wks | TBC | Independent of drive thermal model |
| C08 | Interposing relay, run command | Phoenix Contact | PLC-RSC-24DC/21 | 2 | 24 V DC, 6 A | SCH-0101/18 | 2 wks | OK | |

### D — DOL feeders and distribution

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| D01 | Motor protection circuit breaker, P-103 | Schneider Electric | TeSys GV2ME14 | 1 | 6–10 A | SLD-0001 | 4 wks | OK | Set to confirmed motor FLC |
| D02 | Motor protection circuit breaker, C-101 | Schneider Electric | TeSys GV2ME16 | 1 | 9–14 A | SLD-0001 | 4 wks | OK | |
| D03 | Motor protection circuit breaker, MOV-101 | Schneider Electric | TeSys GV2ME08 | 1 | 2.5–4 A | SLD-0001 | 4 wks | OK | |
| D04 | Contactor, AC-3, 24 V DC coil | Schneider Electric | TeSys LC1D09BD | 2 | 9 A AC-3 | SCH-0121 | 4 wks | **TBC** | **AC-3 rating, not AC-1. Type 2 coordination with D01/D02 must be verified against the manufacturer's coordination tables.** |
| D05 | Auxiliary contact block, 1 NO + 1 NC | Schneider Electric | LADN11 | 2 | — | SCH-0121 | 4 wks | **TBC** | **See DR-002 — quantity under review** |
| D06 | MCCB, 3-pole, DB-01 feeder | Schneider Electric | ComPacT NSX100N TMD80 | 1 | 80 A | SLD-0001 | 8 wks | OK | |
| D07 | MCCB, 3-pole, PKG-201 feeder | Schneider Electric | ComPacT NSX100N TMD32 | 1 | 32 A | SLD-0001 | 8 wks | TBC | Confirm skid declared FLC from final vendor data sheet |
| D08 | MCB, 3-pole, C-curve, HVAC-01 | Schneider Electric | Acti9 iC60N 3P C20 | 1 | 20 A | SLD-0001 | 2 wks | OK | |
| D09 | MCCB, 3-pole, **SPARE feeder 1** | Schneider Electric | ComPacT NSX100N TMD63 | 1 | 63 A | SLD-0001 | 8 wks | OK | Fitted and wired to terminals |
| D10 | MCCB, 3-pole, **SPARE feeder 2** | Schneider Electric | ComPacT NSX100N TMD32 | 1 | 32 A | SLD-0001 | 8 wks | OK | Fitted and wired to terminals |

### E — Control power

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| E01 | UPS, online, rack/DIN, with volt-free status contacts | Eaton | 9SX 1000i (or equivalent) | 1 | 1 kVA | SCH-0030/02 | **10 wks** | TBC | Autonomy to be confirmed against actual control load. Status contacts required — confirm they are included. |
| E02 | Power supply, 24 V DC, 20 A, switch-mode | Phoenix Contact | QUINT4-PS/1AC/24DC/20 | 2 | 24 V DC 20 A | SCH-0030/06 | 6 wks | OK | **Each sized for the FULL load, not half** |
| E03 | Redundancy (O-ring) module | Phoenix Contact | QUINT4-ORING/24DC/2X20/1X40 | 1 | 40 A | SCH-0030/08 | 6 wks | OK | Not a direct parallel connection |
| E04 | Electronic circuit protector, DC, adjustable, with status | Phoenix Contact | CBM E4 24DC series | 6 | 24 V DC | SCH-0030/10-20 | 6 wks | OK | **DC-rated — AC MCBs are not acceptable on DC** |
| E05 | MCB, 1-pole, C-curve, 10 A | Schneider Electric | Acti9 iC60N 1P C10 | 2 | 10 A | SCH-0030/04 | 2 wks | OK | Separate MCB per PSU |
| E06 | MCB, 1-pole, C-curve, 16 A | Schneider Electric | Acti9 iC60N 1P C16 | 1 | 16 A | SCH-0030/22 | 2 wks | OK | Cubicle services |
| E07 | 24 V DC distribution terminal block, feed-through | Phoenix Contact | PTFIX series | 4 | 24 V DC | SCH-0030/09 | 2 wks | OK | |

### F — Safety circuit

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| F01 | Safety relay, dual channel, monitored manual reset | Pilz | PNOZ s4 | 1 | 24 V DC | SCH-0040 | 8 wks | **HOLD** | **Selection provisional — required Performance Level not yet determined (TQ-003). May change if PLe is required.** |
| F02 | Emergency stop, 40 mm mushroom, twist release, 2 × NC | Schneider Electric | Harmony XB5AS8445 | 1 | 24 V DC | SCH-0040/02 | 3 wks | OK | MCC door |
| F03 | Emergency stop, IP66, 2 × NC (for LCS) | Schneider Electric | Harmony XB5AS8445 + IP66 mounting | 2 | 24 V DC | SCH-0040/03-04 | 3 wks | OK | In LCS-101 / LCS-102 |
| F04 | Emergency stop, IP66 field station, 2 × NC | Schneider Electric | Harmony XALK178 (enclosed) | 1 | 24 V DC | SCH-0040/06 | 4 wks | OK | Pump hall entry |
| F05 | Reset pushbutton, blue, illuminated | Schneider Electric | Harmony XB5AW36B5 | 1 | 24 V DC | SCH-0040/10 | 3 wks | OK | Monitored reset — acts on release |

### G — PLC and I/O

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| G01 | Controller, CompactLogix 5380 | Rockwell Automation | 5069-L306ER | 1 | — | SCH-0201 | 10–12 wks | **HOLD** | **Platform assumed — TQ-007. If the client standardises on a different platform, every item G01–G10 changes.** |
| G02 | Digital input module, 16 pt, 24 V DC sinking | Rockwell Automation | 5069-IB16 | 3 | 24 V DC | SCH-0201/02 | 10 wks | HOLD | 40 points used, 8 spare (20 %) |
| G03 | Digital output module, 16 pt, 24 V DC sourcing | Rockwell Automation | 5069-OB16 | 2 | 24 V DC | SCH-0202 | 10 wks | HOLD | 14 used, 18 spare — module granularity |
| G04 | Analogue input module, 8 ch, current/voltage | Rockwell Automation | 5069-IF8 | 2 | 4–20 mA | SCH-0203 | 10 wks | HOLD | 6 used, 10 spare |
| G05 | Analogue output module, 4 ch | Rockwell Automation | 5069-OF4 | 1 | 4–20 mA | SCH-0204 | 10 wks | HOLD | 2 used, 2 spare |
| G06 | Field potential distributor | Rockwell Automation | 5069-FPD | 2 | — | SCH-0201 | 10 wks | HOLD | Segments field power between module groups |
| G07 | Address reserve module (spare slot placeholder) | Rockwell Automation | 5069-ARM | 1 | — | SCH-0201 | 10 wks | HOLD | Keeps a slot addressable for future expansion |
| G08 | SD card, industrial | Rockwell Automation | 1784-SD2 | 2 | — | — | 4 wks | OK | One installed, one spare for the client |
| G09 | End cap, DIN rail, mounting accessories | Rockwell Automation | 5069-ECR + accessories | 1 set | — | SCH-0201 | 10 wks | HOLD | **Commonly forgotten — the chassis does not work without the end cap** |
| G10 | EtherNet/IP adapter for RIO-01 | Rockwell Automation | 5069-AEN2TR | 1 | — | RIO drawings | 10 wks | HOLD | Dual-port for ring topology if required later |
| G11 | Digital input module for RIO-01 | Rockwell Automation | 5069-IB16 | 1 | 24 V DC | RIO drawings | 10 wks | HOLD | |
| G12 | Analogue input module for RIO-01 | Rockwell Automation | 5069-IF8 | 1 | 4–20 mA | RIO drawings | 10 wks | HOLD | |

### H — Network

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| H01 | Managed Ethernet switch, 8 port, 2 × multimode fibre SC | Moxa | EDS-408A-MM-SC | 1 | 24 V DC | SCH-0301 | 8 wks | **TBC** | **See DR-004 — fibre port count under review** |
| H02 | Fibre optic termination enclosure / LIU, DIN mount | Generic | — | 1 | — | SCH-0301 | 4 wks | OK | |
| H03 | Fibre pigtails, OM3, SC, 1 m | Generic | — | 8 | — | SCH-0301 | 4 wks | OK | Splice to incoming field fibre |
| H04 | Patch lead, Cat6 industrial, 1 m | Generic | — | 8 | — | SCH-0301 | 2 wks | OK | PLC, drives, meter, spare |
| H05 | RJ45 bulkhead patch panel, DIN | Generic | — | 1 | — | SCH-0301 | 2 wks | OK | Service port on X6 |

### I — Pilot devices and indication

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| I01 | Selector switch, 3-position stay-put, Local/Off/Remote | Schneider Electric | Harmony XB5AD33 | 3 | 24 V DC | SCH-0101/02 | 3 wks | OK | P-101, P-102, P-103 |
| I02 | Pushbutton, flush, green, Start | Schneider Electric | Harmony XB5AA31 | 4 | 24 V DC | SCH-0101/12 | 3 wks | OK | |
| I03 | Pushbutton, flush, red, Stop | Schneider Electric | Harmony XB5AA42 | 4 | 24 V DC | SCH-0101/13 | 3 wks | OK | |
| I04 | Pilot light, LED, green — Running | Schneider Electric | Harmony XB5AVB3 | 6 | 24 V DC | SCH-0101/22 | 3 wks | OK | |
| I05 | Pilot light, LED, red — Fault | Schneider Electric | Harmony XB5AVB4 | 6 | 24 V DC | SCH-0101/23 | 3 wks | OK | |
| I06 | Pilot light, LED, white — Available | Schneider Electric | Harmony XB5AVB1 | 6 | 24 V DC | SCH-0101/21 | 3 wks | OK | |
| I07 | Pushbutton, flush, blue — Lamp test | Schneider Electric | Harmony XB5AA61 | 1 | 24 V DC | SCH-0030/30 | 3 wks | OK | **Without a lamp test, a failed indicator lamp reads as "not running"** |
| I08 | Beacon and sounder, common alarm | Auer / Werma | 24 V DC combination unit | 1 | 24 V DC | SCH-0202/10 | 4 wks | TBC | Confirm client requires local audible alarm |

### J — Relays and terminals

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| J01 | Interposing relay, 24 V DC coil, 1 CO, with LED and test lever | Phoenix Contact | PLC-RSC-24DC/21 | 20 | 24 V DC | SCH-0202 | 2 wks | OK | Every DO leaving the board |
| J02 | Terminal, feed-through, 2.5 mm², grey | Phoenix Contact | UT 2,5 | 360 | — | TRM-0401 | 2 wks | OK | Includes 20 % spare |
| J03 | Terminal, feed-through, 4 mm², grey | Phoenix Contact | UT 4 | 60 | — | TRM-0402 | 2 wks | OK | 240 V AC control |
| J04 | Terminal, **disconnect (knife)**, 2.5 mm² | Phoenix Contact | UT 2,5-MT | 36 | — | TRM-0403 | 2 wks | OK | Every analogue loop |
| J05 | Terminal, feed-through, 2.5 mm², **yellow** | Phoenix Contact | UT 2,5 YE | 24 | — | TRM-0404 | 3 wks | OK | Safety circuit only |
| J06 | Terminal, earth, 2.5 mm² | Phoenix Contact | UT 2,5-PE | 40 | — | TRM | 2 wks | OK | |
| J07 | Terminal, power, 35 mm² | Phoenix Contact | UK 35 | 24 | — | TRM-0405 | 3 wks | OK | Small feeder outgoings |
| J08 | End covers, partition plates, end brackets, separators | Phoenix Contact | D-UT 2,5 / ATP / E/UK | 1 set | — | TRM | 2 wks | **TBC** | **Routinely under-ordered — quantity derived from rail layout, not guessed. Partition plates required between voltage groups.** |
| J09 | Terminal marker strips, printed | Phoenix Contact | ZB series | 1 set | — | TRM | 2 wks | OK | Printed from the termination schedule, not by hand |

### K — Wiring and accessories

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| K01 | Panel wire, tri-rated, 1.0 mm², **dark blue** — DC control | Generic BS6231 | — | 500 m | 0.6/1 kV | All | 2 wks | OK | AS 60204.1 colour convention |
| K02 | Panel wire, tri-rated, 1.0 mm², **red** — AC control | Generic BS6231 | — | 200 m | 0.6/1 kV | All | 2 wks | OK | |
| K03 | Panel wire, tri-rated, 1.0 mm², **orange** — external source interlock | Generic BS6231 | — | 50 m | 0.6/1 kV | SCH-0141 | 2 wks | OK | **Wires that stay live when the board is isolated** |
| K04 | Panel wire, 2.5 / 4 / 16 / 35 / 70 mm², black | Generic | — | Lot | 0.6/1 kV | All | 2 wks | OK | Power |
| K05 | Panel wire, green/yellow, 2.5 / 4 / 16 mm² | Generic | — | Lot | — | All | 2 wks | OK | Earth |
| K06 | Wire ferrules, printed, heat-shrink type | Partex / Grafoplast | — | Lot | — | All | 2 wks | OK | Both ends of every wire |
| K07 | Slotted cable duct, 40 × 60 / 60 × 80 / 80 × 80, with lids | Betaduct / Panduit | — | Lot | — | GA-0020 | 3 wks | OK | **Separate ducts for power / AC control / DC digital / analogue** |
| K08 | DIN rail, 35 mm, slotted | Generic | — | Lot | — | GA-0020 | 2 wks | OK | |
| K09 | Bootlace ferrules, insulated, assorted | Generic | — | Lot | — | All | 2 wks | OK | |
| K10 | Crimp lugs, compression, for power terminations | Cabac / Utilux | Size to suit | Lot | — | TRM | 3 wks | **TBC** | **Sizes depend on final cable sizes — do not order until cable schedule is IFC** |
| K11 | Cable ties, spiral wrap, adhesive bases | Generic | — | Lot | — | — | 2 wks | OK | |

### L — Labelling

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| L01 | Traffolyte label, engraved, black on white, device labels | Local engraver | Per label schedule LBL-0001 | ~140 | — | LBL-0001 | 3 wks | **TBC** | **Cannot order until label schedule is approved by client.** Mechanically fixed (rivet or screw), not adhesive. |
| L02 | Traffolyte label, cubicle identification, large | Local engraver | Per LBL-0001 | 5 | — | LBL-0001 | 3 wks | TBC | |
| L03 | Warning labels — danger 415 V, multiple supplies, CT secondary | Generic | Per LBL-0001 | Lot | — | LBL-0001 | 2 wks | OK | **"Do not open-circuit CT secondary" is a genuine safety label, not boilerplate** |
| L04 | Asset / rating nameplate, engraved | Local engraver | Per LBL-0001 | 1 | — | LBL-0001 | 3 wks | TBC | Rated current, voltage, Icw, IP, mfr, date, standard — per AS/NZS 61439 marking requirements |
| L05 | Arc flash warning label | — | — | 1 | — | — | — | **CLIENT SCOPE** | **Content comes from the client's arc flash study. We fit a blank holder. We do not generate the label.** |

### M — Field stations and remote I/O

| Item | Description | Manufacturer | Part Number | Qty | Rating | Drawing Ref | Lead Time | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| M01 | Local control station enclosure, GRP, IP66, 4-hole | Schneider / Fibox | To suit XB5 devices | 2 | IP66 | LCS drawings | 4 wks | OK | Pump hall — wet, washdown |
| M02 | LCS internals — Local/Remote selector, Start, Stop, E-stop, Running lamp, terminals | Schneider Electric | Harmony XB5 range | 2 sets | 24 V DC | LCS drawings | 4 wks | OK | |
| M03 | RIO-01 enclosure, 316 stainless, IP66, 600 × 600 × 250 | Generic | — | 1 | IP66 | RIO drawings | 6 wks | TBC | Outdoor at intake — **confirm solar loading / whether a sunshade or vortex cooler is needed** |
| M04 | RIO-01 internals — MCB, 24 V DC PSU, terminals, fibre LIU | Assorted | — | 1 set | — | RIO drawings | 6 wks | TBC | |

---

## 5.3 Long lead items — the schedule-critical list

| Item | Lead time | Why it is critical | Mitigation |
|---|---|---|---|
| **C04 — VSDs** | **14–16 wks** | Longest item. The build cannot be completed without them and the cubicle dimensions depend on them. | Order early against the design freeze; **this is the item the whole programme hangs on** |
| G01–G12 — PLC and I/O | 10–12 wks | Blocked on TQ-007 (platform confirmation) | Escalate TQ-007 as the highest-priority client action |
| E01 — UPS | 10 wks | Control system cannot be tested without it | Order early; FAT can proceed on a temporary supply if it slips, but that is a FAT deviation |
| A01 — MCC enclosure fabrication | 8 wks | Blocked on TQ-001 (cable entry direction) | Escalate TQ-001 |
| B01, C01, D06–D10 — MCCBs | 8–10 wks | Blocked on TQ-002 (fault level) | Order on the assumed rating with the commercial risk acknowledged, or hold and accept the delay — **this is a decision for the project manager, not the PE alone** |
| H01 — managed switch | 8 wks | Fibre-port variants are frequently not stocked locally | See DR-004 |
| F01 — safety relay | 8 wks | Blocked on TQ-003 (required PL) | Provisional selection; hold PO |

> **The pattern to notice:** almost every long-lead item is blocked on an open technical query, not on the supplier. **The PE's real job on procurement is not chasing suppliers — it is closing out the engineering inputs that are stopping the orders.** That is a genuinely useful thing to say in an interview.

---

## 5.4 SLD ↔ SCHEMATIC ↔ BOM reconciliation

### 5.4.1 The method

This is not a read-through. It is three directional passes, and each pass finds a different class of error.

**Pass 1 — SLD → BOM ("is everything on the power drawing purchased?")**

Walk every device on the SLD, top to bottom. For each, confirm a BOM line exists, with the right quantity, the right rating, and the right accessories (handle, aux contacts, trip unit, terminal shrouds).

*Finds:* missing devices; missing accessories; rating mismatch between drawing and BOM.

**Pass 2 — SCHEMATIC → BOM ("does every control device exist, and does it have enough contacts?")**

Walk every schematic sheet. For each device, tally:
- Does a BOM line exist?
- **How many contacts does the schematic use, and how many does the BOM part actually provide as standard?**
- Does the coil voltage on the drawing match the coil voltage in the part number?
- Is every lamp, selector, pushbutton and relay on the drawing in the BOM?

*Finds:* the auxiliary contact shortfall (the big one); coil voltage mismatch; devices drawn but never purchased.

**Pass 3 — BOM → DRAWINGS ("is anything being bought that nothing needs?")**

Walk every BOM line and find where it appears on a drawing. Anything that cannot be traced to a drawing is either an error, a legitimate consumable, or a leftover from a copied BOM.

*Finds:* duplicate procurement; leftover items from a previous project's BOM; obsolete lines from earlier revisions.

**Pass 4 — cross-check against the I/O list and termination schedule**

Module counts must match points used plus spares. Terminal counts must match the termination schedule plus spares. Relay counts must match the number of outputs leaving the board.

### 5.4.2 Why all three directions are needed

| Pass | Catches | Missed by the others |
|---|---|---|
| SLD → BOM | Missing purchase | A schematic-only device would not appear |
| Schematic → BOM | Contact shortfall, coil mismatch | Power devices with no control function would not appear |
| BOM → Drawings | Duplicates, orphans, leftovers | Neither forward pass can find something that should not be there |

**Doing only one direction is the most common shortcut and it misses the most expensive errors.**

### 5.4.3 When to do it

| Point | What is being checked | Cost of a finding |
|---|---|---|
| Rev B, before IFC | Everything | A drawing revision. Cheap. |
| Before each purchase order | The items on that PO | A re-quote. Cheap. |
| On receipt of goods | What arrived vs. what was ordered vs. what was specified | Return and re-order. Moderate. |
| At the start of wiring | Kit completeness | Workshop stoppage. Expensive. |
| At FAT | — | **Too late.** |

---

## 5.5 Common BOM problems and what causes them

| Problem | Typical cause | How it is caught |
|---|---|---|
| **Quantity mismatch** | Device count taken from one drawing revision, drawings later revised | Pass 1 / Pass 2 recount at Rev B |
| **Missing accessory** | Base device ordered without handle, aux contacts, trip unit, terminal shrouds or end cap | Pass 2 contact tally; checking each device family's accessory list |
| **Obsolete part** | BOM copied from an older project; manufacturer superseded the range | Vendor quotation — the supplier flags it, **if you send them the part numbers early enough** |
| **Incorrect rating** | Motor FLC used to size a VSD feeder breaker; contactor sized on AC-1 not AC-3; MCB used on a DC circuit | Pass 1 rating check against the drive manual and the device's utilisation category |
| **Long lead time discovered late** | Procurement not engaged until the BOM is "finished" | Issue a preliminary BOM at Rev A purely to get lead times back |
| **Drawing revision change** | BOM frozen at Rev B, drawings go to Rev C, nobody re-reconciles | Revision-controlled BOM with a mandatory re-reconciliation on every drawing revision |
| **Incompatible component** | MPCB and contactor from different brands with no published coordination; drive without the network option card | Pass 2, plus checking manufacturer coordination tables |
| **Duplicate procurement** | Same item ordered under two BOM lines with different descriptions | Pass 3 |
| **Substitution without engineering approval** | Procurement accepts a supplier's "equivalent" to save cost or time | **Mandatory engineering review of every substitution — see DR-005** |

---

## 5.6 Worked discrepancies

### DR-001 — Quantity mismatch: pilot light count

**Discovered:** Pass 2, Rev B reconciliation.
**Finding:** BOM listed 4 green Running lamps. Schematics show 6 — P-101, P-102, P-103, C-101, MOV-101 open, and a common "station healthy" indicator.
**Cause:** BOM built at Rev A, when C-101 and MOV-101 indication had not yet been added.
**Consequence:** Two lamps short. Would be found in the workshop, at which point the wireman stops on that door.
**Action:** BOM corrected to 6, plus 2 spares. Cost impact: negligible. Schedule impact: none, because it was found at Rev B.
**Engineering approval required:** No — the schematic is correct, the BOM was wrong.
**Drawing revision required:** No.
**Retest required:** No.

**Lesson:** trivial to fix at Rev B, a workshop stoppage at build. This is why the reconciliation is scheduled rather than done when someone remembers.

---

### DR-002 — Missing accessory: contactor auxiliary contact shortfall

**Discovered:** Pass 2 contact tally.
**Finding:** Contactor KM103 (item D04) is specified as LC1D09BD, which provides **1 NO + 1 NC** integral auxiliary contacts. The schematics use **four** contacts on KM103:

| Use | Type | Sheet |
|---|---|---|
| "Running" feedback to PLC DI | NO | SCH-0201/12 |
| Local running lamp at MCC door | NO | SCH-0121/22 |
| Seal-in / latch for the local start circuit | NO | SCH-0121/14 |
| Interlock preventing simultaneous operation with the standby drainage path | NC | SCH-0121/16 |

Three NO and one NC required; one NO and one NC supplied.

**Cause:** The classic. Contacts are free on a drawing and cost money in a catalogue. The designer used what the logic needed; nobody tallied it against the device.

**Consequence if not caught:** The wireman gets to KM103 with two contacts and four wires. Work stops on that feeder. An add-on auxiliary block is sourced at short notice — and add-on blocks are exactly the kind of small item that is out of stock when you need it. Realistically a two- to five-day stoppage on that cubicle, or a rushed and poorly-documented workaround.

**Options considered:**

| Option | Assessment |
|---|---|
| Add an auxiliary contact block (LADN20, 2 NO) | Simple, cheap, standard. **Selected.** |
| Use an interposing relay driven from the existing NO | Adds a relay and a failure point to do a job a $15 contact block does |
| Re-draw the logic to use fewer contacts | Re-engineering to avoid a $15 part. Poor value and introduces new risk. |

**Action:** Item D05 quantity increased, and one LADN20 (2 NO) added per affected contactor. BOM revised to Rev C.
**Engineering approval:** Not required — no functional change.
**Drawing revision:** SCH-0121 annotated to show the add-on block, for the wireman's benefit.
**Retest:** No.
**Cost impact:** Trivial. **Avoided cost:** a workshop stoppage.

**This exact error is the most common BOM defect in the industry.** The countermeasure is the contact tally in Pass 2, and it is boring, mechanical work that must be done anyway.

---

### DR-003 — Obsolete part

**Discovered:** Vendor quotation review.
**Finding:** A terminal accessory carried over from a previous project's BOM template had been superseded by the manufacturer. The supplier quoted the replacement without drawing attention to the change.
**Consequence:** Superseded terminal accessories are often *not* dimensionally identical to what they replace. A different-width partition plate changes the rail length, which changes the terminal layout drawing, which may not fit the cubicle.
**Action:** Confirmed the replacement's dimensions against the manufacturer's data sheet before accepting. In this case dimensionally identical — accepted, BOM part number updated.
**Lesson, and it is the general one:** **read what the supplier actually quoted, not what you asked for.** Quotations routinely substitute silently. A line-by-line comparison of the quotation against the BOM is a PE task and it takes twenty minutes.

---

### DR-004 — Incompatible component: fibre port shortfall

**Discovered:** Pass 3, cross-checking H01 against the network drawing.
**Finding:** The network design requires **two** multimode fibre links — one to the control room, one to RIO-01. The specified switch provides two fibre ports. That is exactly enough, **with zero spare**, and no capacity for a redundant ring, a future fibre link, or a spare port for fault-finding.
**Also found:** the switch is powered from 24 V DC — which is correct and intended — but the BOM did not identify which ECP group feeds it. If it sits on the same group as the field digital outputs, a field short takes the network down at the same moment as the I/O, and SCADA loses visibility exactly when it is most needed.

**Options:**

| Option | Assessment |
|---|---|
| Accept as-is | Zero spare fibre capacity on a remote site. Poor. |
| Upgrade to a switch with 4 fibre ports | Modest cost increase, longer lead, much better capacity |
| Add a second small switch later | More devices, more failure points, more power draw |

**Action:** Raised as a technical query to the client with a cost comparison, recommending the 4-port variant. Separately, confirmed that the switch is fed from the PLC/network protection group (ECP1) and not the field I/O group, and had SCH-0030 annotated to make that explicit so it cannot be reversed in a later revision.

**Engineering approval:** Client decision on the spare-port question (it is their operational cost, not a technical necessity). The ECP allocation is a technical correction and was made directly.
**Drawing revision:** SCH-0030 and SCH-0301 revised.
**Retest:** Network checks at FAT reflect whichever switch is supplied.

**Lesson:** "exactly enough" is a finding. Spare capacity questions are the client's to decide, but they are the PE's to raise. And the second half of this finding — the power group allocation — is the kind of thing that only surfaces when you cross-check documents against each other rather than reading each one alone.

---

### DR-005 — ★ EQUIPMENT SUBSTITUTED WITHOUT ENGINEERING APPROVAL (worked in full)

**This is the one to be able to talk through in an interview.** It is about decision-making, not design, and it is exactly what a Project Engineer's day actually looks like.

#### What happened

Procurement issued the VSD enquiry. The quoted lead time on the specified Danfoss VLT AQUA FC202 came back at **16 weeks**, four weeks longer than allowed in the programme. A supplier offered an alternative manufacturer's drive of the same kW and voltage rating, **ex-stock**, at approximately 8 % lower cost.

The buyer, under genuine and legitimate schedule pressure, prepared a purchase order for the alternative and sent it for signature. It came to me because the project's procurement procedure requires engineering sign-off on any deviation from a specified item — which is precisely why that gate exists.

#### Technical assessment

"Same kW and voltage" is not equivalence. Six things were checked:

| # | Check | Finding |
|---|---|---|
| 1 | **Physical dimensions and mounting** | Different frame size and different mounting centres. The cubicle general arrangement, the mounting plate and the internal cable routing would all change. **The GA was already released for fabrication.** |
| 2 | **Cooling and airflow** | Different clearance requirements and different airflow direction. The cubicle thermal design would need reassessment — and thermal verification is the manufacturer's responsibility under AS/NZS 61439.1, so this is not a trivial redraw. |
| 3 | **Safe Torque Off implementation** | Different STO terminal designation and different wiring arrangement. **SCH-0040 — the safety circuit — would require revision.** Any change to a safety-related circuit is a change that must be reviewed, not absorbed. |
| 4 | **EtherNet/IP capability** | Native on the specified drive. On the alternative it requires an option card that **was not included in the quoted price and had its own lead time.** The "cheaper" comparison was not comparing the same thing. |
| 5 | **Client brand standard** | **TQ-001 still open.** The client's electrical design standard had not been supplied, and water utilities very commonly mandate drive brands across their network. |
| 6 | **Whole-of-life, not purchase price** | The client's maintenance team's spares holding, their technicians' familiarity, their existing configuration and parameter backup tooling, and their drive fleet commonality. An 8 % saving on two drives is negligible against a maintenance team carrying an orphan brand for twenty years. |

#### The decision process — and who actually decides what

| Party | Their call |
|---|---|
| **Procurement** | Identified the lead time problem and sourced an alternative. **Correct behaviour.** Procurement's job is to surface options, not to assess technical equivalence. |
| **Designer** | Assessed the technical differences against the drawings and confirmed which sheets would change. |
| **Project Engineer (me)** | Stopped the PO. Compiled the comparison. Identified that this was **not my decision to make** — it affects the client's asset for its whole life and touches an open standards question. Raised a formal deviation request. |
| **Client** | Decided. |

**I did not decide this.** That is the point of the example. A Project Engineer who unilaterally approves a brand substitution on a client's long-life asset — while the client's own standard is still an open query — is exceeding their authority, however sound the technical reasoning.

#### Deviation request DEV-002 (issued to client)

> Requested: approval to substitute the specified drive with [alternative], same kW/V rating, on the grounds of a 4-week lead time improvement and an ~8 % cost reduction.
> Technical differences identified: physical envelope and mounting, cooling arrangement, STO terminal arrangement (affects the safety circuit drawing), EtherNet/IP requires a cost option not in the quoted price.
> Drawings affected if approved: GA-0020, SCH-0040, SCH-0101, SCH-0111, BOM.
> Note: the client's electrical design standard has not been supplied (TQ-001). If that standard nominates a drive manufacturer, this request is void.
> **Recommendation: reject.** The net cost saving is largely eliminated by the option card, the drawing rework consumes part of the schedule benefit, and the whole-of-life cost of an orphan brand in the client's fleet is not justified by a 4-week programme gain.

#### Client response

Rejected. The client's maintenance group standardises on the specified drive across their network. They confirmed — verbally first, then in writing — that this is in their electrical design standard, **which they then finally supplied.** That closed TQ-001 and, in doing so, confirmed three other assumptions that had been open for weeks.

#### Outcome and impacts

| Impact | Detail |
|---|---|
| Cost | Nil variation. The substitution was not made. |
| Schedule | 4 weeks of float consumed. **Mitigated** by re-sequencing the build: the enclosure, busbar, terminals, PLC section and all small feeders were wired first, and the drive cubicles were left until last. Net programme impact reduced to approximately 1 week. |
| Drawings | No change. |
| FAT | No change. |
| Documentation | Deviation DEV-002 recorded, closed, and included in the MDR — so in five years there is a written record of why that drive is that brand. |
| **Side benefit** | The deviation request is what finally extracted the client's design standard. Sometimes the fastest way to get a document out of a client is to ask them to approve something that depends on it. |

#### What this demonstrates

1. Technical equivalence is not kW and voltage.
2. Purchase price is not cost.
3. Knowing the limit of your own authority and escalating properly.
4. Schedule recovery through **re-sequencing the build** rather than through compromising the design — this is the genuinely valuable move and it is what a good PE does.
5. Documenting a decision so it survives the people who made it.

> **This is the story to tell when an interviewer asks "tell me about a time you had to make a difficult technical decision."** The answer is not that you made a clever technical call. It is that you recognised which decision was yours and which was the client's, and you made the escalation easy for them to act on.

---

## 5.7 What the Project Engineer did at Stage 5

1. Issued a **preliminary BOM at Rev A** purely to get lead times back early — before the BOM was "finished". This is what exposed the 16-week drive lead time in time to do something about it.
2. Ran all four reconciliation passes at Rev B.
3. Compared every vendor quotation line by line against the BOM, and caught DR-003.
4. Identified the long-lead list and, critically, identified that **most of them were blocked on open technical queries, not on suppliers** — then went and closed the queries.
5. Stopped an unapproved substitution and turned it into a formal deviation (DR-005).
6. Recovered four weeks of schedule by re-sequencing the build rather than by compromising the design.
7. Kept the BOM under revision control, with a rule that **any drawing revision triggers a BOM re-reconciliation**.

---

**Next:** [Stage 6 — Procurement and Engineering Control](06-PROCUREMENT-AND-ENGINEERING-CONTROL.md)
