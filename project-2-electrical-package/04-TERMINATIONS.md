# STAGE 4 — TERMINATION DRAWINGS AND SCHEDULE

**Drawing:** [`NFD-ELE-TRM-0401.svg`](drawings/NFD-ELE-TRM-0401.svg) — terminal rail X3 layout
**Registers:** [`registers/termination-schedule.csv`](registers/termination-schedule.csv) · [`registers/cable-schedule.csv`](registers/cable-schedule.csv)

---

## 4.1 What the termination drawings are for, and who actually uses them

The schematic tells you *what the circuit does*. The termination drawing tells you *where the wire physically goes*, and it is read by different people for different reasons:

| Reader | What they need from it |
|---|---|
| The wireman in the workshop | Which terminal, which side, what number goes on the ferrule |
| The installation electrician on site | Which core of which cable lands on which terminal |
| The commissioning technician | Where to break the loop and inject a signal |
| The maintainer at 3 a.m. in five years | Where the fault is, without a laptop |

**The termination schedule is the single most-used document in the package after handover.** Nobody opens the design basis again. Everybody opens the termination schedule. It is worth getting right.

---

## 4.2 Terminal numbering philosophy

### 4.2.1 Rail allocation by voltage and function

| Rail | Function | Voltage | Terminal type | Colour |
|---|---|---|---|---|
| **X0** | Incoming supply | 415 V AC | Busbar links | — |
| **X1** | Outgoing power feeders | 415 V AC | Heavy-duty feed-through, sized per cable | Grey |
| **X2** | AC control and services | 240 V AC | Feed-through, 4 mm² | Grey |
| **X3** | Digital I/O — inputs and outputs | 24 V DC | Feed-through, 2.5 mm² | Grey |
| **X4** | Analogue signals | 4–20 mA | **Disconnect (knife) type**, 2.5 mm² | Grey with orange lever |
| **X5** | Safety circuit — E-stop | 24 V DC | Feed-through, 2.5 mm² | **Yellow** |
| **X6** | Communications | — | RJ45 patch panel + fibre tray | — |
| **XE** | Protective earth | — | Earth terminal, direct busbar contact | Green/yellow |
| **XS** | Instrument screen earth | — | Isolated screen bar, single-point bonded to XE | — |

**Why rails are split by voltage and not just by cubicle.** Two reasons, and the second is the important one:

1. **Safety.** Someone working on a 24 V DC circuit should not have their hand next to a 415 V terminal. Physical separation plus a barrier is the control.
2. **Error prevention.** If the only 415 V terminals on a rail are the power terminals and the only ELV terminals are on a different rail, it is physically harder to land a control wire in a power terminal. Good layout removes error modes; it does not just document them.

**Why X5 is yellow.** The safety circuit is the one circuit where a well-meaning modification does real harm. A distinct terminal colour makes it obvious — to the wireman, the commissioning tech and the auditor — that this rail is different and is not to be casually reworked. It also makes a visual check at FAT trivial.

**Why X4 uses disconnect terminals.** A knife-disconnect terminal lets you open the loop, inject a calibrated 4–20 mA signal, and verify the whole chain from terminal to PLC to SCADA — without unwiring anything and without disturbing the field cable. On a board with six analogue loops this saves hours at commissioning and it saves them again at every future calibration. It costs a few dollars per terminal.

### 4.2.2 Numbering within a rail

```
X3 : 001    ← rail designator : sequential terminal number
```

- Sequential from 001, **no gaps, no re-use.**
- Grouped by equipment, in the same order as the schematic sheets, so X3:001–X3:030 is P-101, X3:031–X3:060 is P-102, and so on. A maintainer who knows the pump can find the terminals without the index.
- **Spare terminals grouped at the end of each equipment block**, labelled `SPARE`, minimum 20 %.
- Numbers are **never** reused when a circuit is deleted. A deleted circuit's terminal becomes a spare and keeps its number. Re-using a number means an old drawing and a new drawing disagree, and someone will eventually work from the old one.

### 4.2.3 Spare terminal philosophy — and the argument against it

Minimum 20 % spare terminals per rail, grouped at the end of each equipment block, physically fitted and labelled.

**Why grouped and not distributed.** Distributed spares (one spare after every ten) look tidy and are nearly useless: you can never fit a new multi-core cable's worth of cores together, and the numbering becomes impossible to follow. A contiguous block of eight spares at the end of the P-101 group is genuinely usable.

**The honest counter-argument:** spares consume rail length, which consumes cubicle width, which costs money and floor space. A client who specifies 30 % spares on every rail across a large MCC can add a cubicle. That is a real cost, and it is why the requirement should come from the client's standard rather than be assumed — **TQ-001**.

### 4.2.4 Wire numbering

Internal wiring: `SHEET-PATH` — e.g. `0101-14` means sheet NFD-ELE-SCH-0101, current path 14. Ferruled at both ends.

**Why this scheme.** Any wire in the board tells you which drawing to open. The alternative — numbering wires by terminal, source-destination style — means you must already know where the wire goes to look it up, which is the thing you were trying to find out.

**The trade-off, stated honestly:** with sheet-path numbering, a wire that runs between several devices on the same path shares a number, so several wires in the board carry the same ferrule. Some clients find that confusing and specify unique numbers instead. Either is defensible; what matters is that it is consistent and that it matches the drawings. **Client standard governs — TQ-001.**

---

## 4.3 Segregation

| Requirement | How it is achieved | Why |
|---|---|---|
| 415 V power separated from ELV control | Separate cable ducts, separate rails, physical barrier between power and control zones | Insulation failure at 415 V must not energise a 24 V circuit. Also limits capacitive and inductive coupling. |
| Analogue separated from digital | Separate duct from digital and from 240 V AC wiring; crossings at right angles where unavoidable | Switching a 24 V DC inductive load next to a 4–20 mA pair induces noise onto a signal that may be representing a 0–10 m level over 16 mA |
| VSD output cabling separated from everything | Screened VSD cable, 360° EMC glands, routed in its own path, kept clear of control and instrument runs | A VSD output is a high dv/dt source. It is the single worst noise source in the board. |
| Safety circuit identifiable | Yellow terminals, and routed so it is visually traceable | See §4.2.1 |
| Field cable segregation | Instrument cables in separate cable tray or separate ducts from power, per the installation design | Not our scope, but our termination schedule should make the requirement visible to the installer |

> **The right-angle crossing rule is worth knowing why, not just that.** Two cables running parallel for a long distance couple capacitively and inductively along that whole length. Two cables crossing at 90° couple over a few millimetres. Where segregation is impossible, crossing at right angles reduces the coupled length to almost nothing.

---

## 4.4 Screen and earth termination

This is the section people get wrong, so it is set out explicitly.

| Cable | Screen treatment | Earthed where | Reason |
|---|---|---|---|
| **Analogue instrument (4–20 mA)** | Screen taken to a dedicated screen terminal on rail XS | **MCC end only.** Field end cut back, insulated, and **not** connected. | Electrostatic shielding. Earthing both ends creates an earth loop — any potential difference between the two earth points drives current through the screen, which couples noise into the pair. |
| **Control multicore (LCS, field switches)** | Screen to XS | MCC end only | Same reason |
| **VSD motor cable** | Screen terminated **360°** via EMC gland | **Both ends** — drive end and motor end | Low-impedance high-frequency return path for common-mode current. A pigtail instead of a 360° termination largely defeats this: a pigtail is an inductor at high frequency. |
| **Ethernet (copper)** | Shielded connectors if shielded cable is used | Per the network design | Mixing shielded and unshielded components creates unintended earth paths |
| **Protective earth (all cables)** | Earth core to rail XE; armour/gland to the gland plate earth | Both ends, always | This is protective earth, not a screen. It has nothing to do with the screen discussion above. |

> **The distinction to be able to state clearly:** *"The instrument screen is solving a signal-integrity problem and gets earthed at one end. The VSD cable screen is solving an EMC problem and gets earthed at both ends, 360°. They are different jobs. And neither of them is the protective earth conductor, which is always connected at both ends because it is a safety conductor."*
>
> If you can say that unprompted, you will sound like someone who has commissioned a board rather than someone who has read about one.

**Instrument screen earth bar XS.** A separate, insulated bar, bonded to the main earth bar at **one point only**. This guarantees single-point earthing for every screen without relying on every technician remembering to leave the field end disconnected — and if a screen does get earthed at the field end, the fault is at least confined and findable.

---

## 4.5 Digital versus analogue — practical differences at the terminals

| | Digital | Analogue |
|---|---|---|
| Terminal type | Feed-through | **Disconnect (knife)** |
| Cable | Multicore, screened overall | **Individually screened pairs**, overall screen (IS/OS) |
| Screen earthing | MCC end, XS | MCC end, XS |
| Power | 24 V DC from digital field group (ECP2/ECP3) | 24 V DC loop power from **separate** analogue group (ECP4) |
| Failure detection | Fail-safe wiring — critical signals normally closed, so a broken wire reads as a fault | **Live zero** — a healthy loop never reads 0 mA, so 0 mA means broken |
| Testing at FAT | Force the contact, confirm the bit at the PLC and at SCADA | Inject 4, 8, 12, 16, 20 mA at the terminal; confirm engineering units at the PLC and at SCADA |
| Typical fault | Wrong terminal, reversed contact sense | Reversed polarity, screen earthed both ends, wrong range scaling |

**Why individually screened pairs for analogue and not just an overall screen.** With an overall screen only, the pairs inside are screened from the outside world but not from each other. A 4–20 mA pair running alongside another pair in the same bundle can pick up crosstalk. Individually screened pairs cost more and are worth it on analogue.

**Why the analogue group has its own protector.** If a digital field output shorts and trips its protector, every analogue loop on the same protector would go dark at the same moment — and the operator would lose level, flow and pressure simultaneously, during an event. Separating them costs one protector.

---

## 4.6 Cable schedule (extract)

Full version: [`registers/cable-schedule.csv`](registers/cable-schedule.csv)

| Cable No. | From | To | Type | Size / cores | Screen | Supply scope |
|---|---|---|---|---|---|---|
| C-0001 | TX-01 LV terminals | MCC-01 X0 | 415 V power | **TBC** — client scope | — | Client / installer |
| C-0101 | MCC-01 VSD-101 out | P-101 motor TB | VSD motor cable | 3C + E, 70 mm² *(provisional — pending AS/NZS 3008 calc)* | Screened, 360° both ends | Installer |
| C-0102 | MCC-01 X3 | LCS-101 | Control multicore | 12C × 1.5 mm² | Overall screen, MCC end | Installer |
| C-0103 | MCC-01 X3 | P-101 motor TB | Thermistor | 2C × 1.5 mm² | Screened, MCC end | Installer |
| C-0104 | MCC-01 X3 | B101-SEAL | Control | 2C × 1.5 mm² | Screened, MCC end | Installer |
| C-0105 | MCC-01 X5 | LCS-101 E-stop | **Safety** | 4C × 1.5 mm² (dual channel) | Screened, MCC end | Installer |
| C-0111 | MCC-01 VSD-102 out | P-102 motor TB | VSD motor cable | 3C + E, 70 mm² *(provisional)* | Screened, 360° both ends | Installer |
| C-0112 | MCC-01 X3 | LCS-102 | Control multicore | 12C × 1.5 mm² | Overall screen, MCC end | Installer |
| C-0121 | MCC-01 X1 | P-103 sump pump | Power | 4C × 2.5 mm² | — | Installer |
| C-0122 | MCC-01 X3 | Sump float switches | Control | 4C × 1.5 mm² | Screened, MCC end | Installer |
| C-0141 | MCC-01 X1 | MOV-101 | Power | 4C × 2.5 mm² | — | Installer |
| C-0142 | MCC-01 X3 | MOV-101 control | Control multicore | 12C × 1.5 mm² | Overall screen, MCC end | Installer |
| C-0201 | MCC-01 X4 | LIT-101 wet well level | Instrument | 1 pr × 1.5 mm² IS/OS | Individual + overall, MCC end | Installer |
| C-0202 | MCC-01 X4 | FIT-101 discharge flow | Instrument | 1 pr × 1.5 mm² IS/OS | Individual + overall, MCC end | Installer |
| C-0210 | MCC-01 X3 | LSLL-101 low-low float | Control | 2C × 1.5 mm² | Screened, MCC end | Installer |
| C-0301 | MCC-01 X5 | S-ES-PH pump hall E-stop | **Safety** | 4C × 1.5 mm² | Screened, MCC end | Installer |
| C-0401 | MCC-01 X6 | Control room patch panel | Fibre | 2C OM3 multimode | — | Installer |
| C-0402 | MCC-01 X6 | RIO-01 intake kiosk | Fibre | 2C OM3 multimode | — | Installer |
| C-0501 | MCC-01 X1 | DB-01 | Power | 4C × 25 mm² *(provisional)* | — | Installer |
| C-0502 | MCC-01 X1 | PKG-201 dosing skid isolator | Power | 4C × 6 mm² *(provisional)* | — | Installer |

> **Every cable size marked provisional is provisional.** They are placeholders selected on a reasonable rule of thumb for the current involved. **None of them is the output of an AS/NZS 3008.1.1 calculation**, because the route lengths, installation methods, grouping and ambient conditions are not confirmed. See `00-CLAIM-INTEGRITY.md`. On a real job the designer produces the calculation, the PE checks that its inputs match the actual installation, and the cable schedule is not issued for construction until it does.

---

## 4.7 Termination schedule (extract)

Full version: [`registers/termination-schedule.csv`](registers/termination-schedule.csv) — 180+ rows.

### Rail X3 — P-101 block (24 V DC digital)

| Cable No. | From | To | Core | Terminal | Signal | Voltage | Drawing Ref |
|---|---|---|---|---|---|---|---|
| C-0102 | LCS-101 | MCC-01 | 1 | X3:001 | LCS Start PB — 24 V DC supply out | 24 V DC | SCH-0101/12 |
| C-0102 | LCS-101 | MCC-01 | 2 | X3:002 | LCS Start PB — return | 24 V DC | SCH-0101/12 |
| C-0102 | LCS-101 | MCC-01 | 3 | X3:003 | LCS Stop PB — 24 V DC supply out | 24 V DC | SCH-0101/13 |
| C-0102 | LCS-101 | MCC-01 | 4 | X3:004 | LCS Stop PB — return (**NC, fail-safe**) | 24 V DC | SCH-0101/13 |
| C-0102 | LCS-101 | MCC-01 | 5 | X3:005 | LCS selector — Local position | 24 V DC | SCH-0201/04 |
| C-0102 | LCS-101 | MCC-01 | 6 | X3:006 | LCS selector — Remote position | 24 V DC | SCH-0201/05 |
| C-0102 | LCS-101 | MCC-01 | 7 | X3:007 | LCS Running lamp — supply | 24 V DC | SCH-0101/22 |
| C-0102 | LCS-101 | MCC-01 | 8 | X3:008 | LCS Running lamp — return | 24 V DC | SCH-0101/22 |
| C-0102 | LCS-101 | MCC-01 | 9 | X3:009 | SPARE | — | — |
| C-0102 | LCS-101 | MCC-01 | 10 | X3:010 | SPARE | — | — |
| C-0102 | LCS-101 | MCC-01 | 11 | X3:011 | SPARE | — | — |
| C-0102 | LCS-101 | MCC-01 | 12 | X3:012 | SPARE | — | — |
| C-0102 | LCS-101 | MCC-01 | Screen | XS:01 | Overall screen — **MCC end only** | — | SCH-0101 |
| C-0103 | P-101 motor TB | MCC-01 | 1 | X3:013 | PTC thermistor — leg 1 → KT101 | ELV | SCH-0101/08 |
| C-0103 | P-101 motor TB | MCC-01 | 2 | X3:014 | PTC thermistor — leg 2 → KT101 | ELV | SCH-0101/08 |
| C-0103 | P-101 motor TB | MCC-01 | Screen | XS:02 | Screen — MCC end only | — | SCH-0101 |
| C-0104 | B101-SEAL | MCC-01 | 1 | X3:015 | Seal water flow switch — 24 V DC out | 24 V DC | SCH-0201/08 |
| C-0104 | B101-SEAL | MCC-01 | 2 | X3:016 | Seal water flow switch — return (**NC**) | 24 V DC | SCH-0201/08 |
| — | VSD-101 | MCC-01 internal | — | X3:017 | Drive healthy → PLC DI (**NC, fail-safe**) | 24 V DC | SCH-0201/02 |
| — | VSD-101 | MCC-01 internal | — | X3:018 | Drive running → PLC DI | 24 V DC | SCH-0201/03 |
| — | KA101 | MCC-01 internal | — | X3:019 | Run command → VSD-101 terminal 18 | 24 V DC | SCH-0101/18 |
| — | Q11 aux | MCC-01 internal | — | X3:020 | Feeder available → PLC DI | 24 V DC | SCH-0201/01 |
| C-0210 | LSLL-101 | MCC-01 | 1 | X3:021 | Low-low float — 24 V DC out | 24 V DC | SCH-0101/09 |
| C-0210 | LSLL-101 | MCC-01 | 2 | X3:022 | Low-low float — return (**NC, hardwired trip**) | 24 V DC | SCH-0101/09 |
| — | — | — | — | X3:023–030 | **SPARE (8)** | — | — |

### Rail X4 — analogue (disconnect terminals)

| Cable No. | From | To | Core | Terminal | Signal | Voltage | Drawing Ref |
|---|---|---|---|---|---|---|---|
| C-0201 | LIT-101 | MCC-01 | + | X4:001 | Wet well level, 4–20 mA, loop + | 24 V DC loop | SCH-0203/01 |
| C-0201 | LIT-101 | MCC-01 | − | X4:002 | Wet well level, 4–20 mA, loop − | 24 V DC loop | SCH-0203/01 |
| C-0201 | LIT-101 | MCC-01 | Screen | XS:10 | Screen — **MCC end only** | — | SCH-0203 |
| C-0202 | FIT-101 | MCC-01 | + | X4:003 | Discharge flow, 4–20 mA, loop + | 24 V DC loop | SCH-0203/02 |
| C-0202 | FIT-101 | MCC-01 | − | X4:004 | Discharge flow, 4–20 mA, loop − | 24 V DC loop | SCH-0203/02 |
| — | PLC AO ch.1 | VSD-101 term 53 | — | X4:011 | P-101 speed reference, 4–20 mA + | — | SCH-0204/01 |
| — | PLC AO ch.1 | VSD-101 term 55 | — | X4:012 | P-101 speed reference, 4–20 mA − | — | SCH-0204/01 |
| — | — | — | — | X4:019–024 | **SPARE (6, disconnect type)** | — | — |

### Rail X5 — safety circuit (yellow terminals)

| Cable No. | From | To | Core | Terminal | Signal | Voltage | Drawing Ref |
|---|---|---|---|---|---|---|---|
| C-0105 | LCS-101 | MCC-01 | 1 | X5:001 | E-stop 101, **channel A** in | 24 V DC | SCH-0040/03 |
| C-0105 | LCS-101 | MCC-01 | 2 | X5:002 | E-stop 101, **channel A** out | 24 V DC | SCH-0040/03 |
| C-0105 | LCS-101 | MCC-01 | 3 | X5:003 | E-stop 101, **channel B** in | 24 V DC | SCH-0040/04 |
| C-0105 | LCS-101 | MCC-01 | 4 | X5:004 | E-stop 101, **channel B** out | 24 V DC | SCH-0040/04 |
| C-0301 | S-ES-PH | MCC-01 | 1–4 | X5:009–012 | Pump hall E-stop, channels A and B | 24 V DC | SCH-0040/06 |
| — | — | — | — | X5:013–016 | **SPARE (4)** — for a future E-stop | — | — |

> **Note the spare pair on X5.** Additional E-stops get added to plants. Leaving four spare yellow terminals and a documented loop-through arrangement means a future E-stop can be added properly, in series, rather than someone improvising a connection in a junction box. The alternative — someone shorting out the loop because there was nowhere to land it — is a genuine hazard.

---

## 4.8 How termination drawings are checked against the schematic

This is a mechanical, dull, essential process. It is done properly or it is not done.

**Method:**

1. **Build the list from the schematic, not from the termination drawing.** Work through every schematic sheet and list every wire that crosses the board boundary. This gives you the *required* list, independent of what the drafter produced.
2. **Compare that required list to the termination schedule.** Every entry must appear exactly once.
3. **Compare the termination schedule to the cable schedule.** Every core used must exist in a cable; every cable must have enough cores; cable type must suit the signal (screened where required, pairs where required).
4. **Compare the termination schedule to the I/O list.** Every PLC point must trace: field device → cable core → terminal → module → address → tag. Break the chain anywhere and the integrator's program will not match the board.
5. **Check the physical terminal count** against the rail length available on the general arrangement. Terminals that do not fit is a workshop discovery and a cubicle rework.

**The five findings this check reliably produces:**

| Finding | How it happens |
|---|---|
| **A signal on the schematic with no terminal** | Circuit added at Rev B, termination drawing not updated |
| **A terminal with no signal** | Circuit deleted, terminal left behind |
| **Insufficient cores** | 12-core cable specified, 13 cores used after a late addition. Discovered at site, by the installer, with the cable already pulled. |
| **Wrong cable type** | An analogue signal assigned to a core in an unscreened control multicore |
| **Address mismatch** | Schematic says DI-12, I/O list says DI-13 — the classic symptom of two people editing two documents |

> **Do this check at Rev B, before the drawings go Issued for Construction.** After IFC, the same findings cost a drawing revision, a workshop stoppage, or a site variation.

### Traceability chain — what "checked" actually means

For **every** I/O point, this chain must close:

```
Field device tag    (LIT-101)
   ↓ cable          (C-0201)
   ↓ core           (+ / −)
   ↓ terminal       (X4:001 / X4:002)
   ↓ internal wire  (0203-01)
   ↓ module + ch.   (5069-IF8 slot 5, channel 0)
   ↓ PLC address    (per I/O list)
   ↓ SCADA tag      (per integrator)
```

If any one link is missing or inconsistent, the point is not signed off. The I/O list ([`registers/io-list.csv`](registers/io-list.csv)) is the document that holds this chain together, and keeping it at the same revision as the schematics is the PE's responsibility.

---

## 4.9 Interface responsibilities at the terminals

| Boundary | Our responsibility | Their responsibility | Where it goes wrong |
|---|---|---|---|
| MCC terminals ↔ field cable | Supply, label and test terminals; prove the circuit from terminal to PLC to SCADA | Supply cable, gland it, land the cores, test the field side | Installer lands a core on the wrong terminal. Mitigated by labelling every terminal and issuing a clear, current schedule. |
| Gland plate | Supply undrilled removable plate, bonded | Drill to suit actual cables, fit glands, maintain IP rating and bonding | Installer drills a plate and does not re-bond it, or compromises IP |
| Instrument loops | Terminals, loop power, screen bar, PLC scaling | Instrument supply, field termination, field calibration | Screen earthed at both ends by an installer who does not know the convention — **so put it on the termination drawing, not only in the specification** |
| Motor cable screen | EMC gland at the drive end, 360° | 360° termination at the motor end | Pigtail at the motor end. Defeats the EMC design. Put the requirement on the drawing. |
| PLC program | I/O list, functional description, terminals proven | Application code, SCADA graphics | Revision mismatch between I/O list and code |
| Field devices | Terminals and loop power | Supply, install, calibrate | 2-wire vs 4-wire transmitters assumed wrongly — check every data sheet |

> **Put the screen-earthing requirement on the termination drawing face.** The installer reads the termination drawing. They will probably never read the specification. A note on the drawing saying *"SCREEN EARTHED AT MCC END ONLY — DO NOT EARTH AT FIELD END"* prevents an entire class of commissioning problem, and it costs one line of text.

---

## 4.10 What the Project Engineer did at Stage 4

1. Set the terminal numbering and rail allocation philosophy **before** drafting started, and wrote it down as a one-page convention.
2. Ran the full schematic ↔ termination ↔ cable ↔ I/O list check in §4.8 and produced a findings list.
3. Found that the LCS-101 control cable was specified with 12 cores and the schedule used 12, leaving **no spare cores** — and had it changed to 16, because pulling a second cable later is a site variation and four extra cores cost almost nothing.
4. Added the screen-earthing note to the termination drawing face.
5. Added four spare yellow terminals on X5 for a future E-stop, with a note on how to loop it in.
6. Confirmed the terminal count fits the rail length on the general arrangement before the cubicles were fabricated.
7. Issued the termination schedule and cable schedule to the installation contractor early, flagged as **Issued for Information / not for construction**, so they could plan cable procurement without treating provisional sizes as final.

> **Point 3 is the small-decision, large-consequence kind of call a PE makes constantly.** Nobody will ever thank you for the four spare cores. But the day a spare core is needed, the alternative is a cable pull through an operating plant.

---

**Next:** [Stage 5 — Bill of Materials](05-BOM.md)
