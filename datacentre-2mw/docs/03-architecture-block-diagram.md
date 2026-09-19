# Architecture Block Diagram and AutoCAD Electrical Brief

> SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN

**Document:** DC2MW-EL-DWG-BRIEF-001
**Rev:** 0.1

---

## 1. What this drawing is trying to communicate

### Explain Like I'm 10 first

When someone who has never seen this building looks at this one page, they should
be able to put a finger on the electricity coming in from the street and trace it
all the way to a computer, saying the whole time: "in here, then through this box,
then that box, then into the computer." And they should be able to see, without
anyone telling them, that there are **two completely separate journeys** — a left
one and a right one — and that they only come together at the very end, at the
computer itself.

If someone can't see those two separate journeys at a glance, the drawing has
failed, no matter how neat it is.

### Engineer Explanation

A single line diagram is the single most important document in an electrical
design package, because it is the only document that shows the **complete
topology** in one view. Every other document — load schedules, cable schedules,
protection settings, commissioning scripts — is a detailed elaboration of
something the SLD asserts.

A data centre SLD must communicate four things simultaneously:

1. **Topology** — what connects to what.
2. **Independence** — which elements are on Path A, which on Path B, and precisely
   where the two paths touch (if anywhere).
3. **Switching state** — which devices are normally open and which normally
   closed. Without this, the drawing does not describe a real operating
   configuration and a reader cannot assess redundancy.
4. **Isolation capability** — where an asset can be separated for safe work.

The third point is the one most commonly omitted, and its omission is fatal. A
drawing that shows a bus tie without marking it `N.O.` is ambiguous about whether
the facility is 2N or not. **On this project every switching device carries an
`N.O.` or `N.C.` annotation.**

---

## 2. Block diagram — Level 0 (the two-path concept)

```
       UTILITY A                                           UTILITY B
    Zone Substation 1                                  Zone Substation 2
           |                                                   |
           v                                                   v
    +-------------+                                     +-------------+
    |   PATH A    |                                     |   PATH B    |
    |             |                                     |             |
    |  MV-A       |                                     |  MV-B       |
    |  TX-A1/A2   |                                     |  TX-B1/B2   |
    |  MSB-A      |<--- GEN-A1/A2                       |  MSB-B      |<--- GEN-B1/B2
    |  UPS-A      |                                     |  UPS-B      |
    |  UOB-A      |                                     |  UOB-B      |
    |  RPP-A1..A8 |                                     |  RPP-B1..B8 |
    |  RackPDU-A  |                                     |  RackPDU-B  |
    +-------------+                                     +-------------+
           |                                                   |
           |            +-------------------------+            |
           +----------->|  DUAL-CORDED IT LOAD    |<-----------+
                        |  250 racks, 2,000 kW    |
                        +-------------------------+

    THE ONLY POINT WHERE PATH A AND PATH B MEET IS INSIDE THE SERVER.
```

**Technical reading:** Path A and Path B share no electrical element upstream of
the IT equipment's dual power supplies. They share no room, no fire compartment,
no cable riser, no control system and no DC control supply. The convergence point
is the server chassis, where two independent PSUs operate in a load-sharing
arrangement and either can carry the full server load.

**Explain Like I'm 10:** Two completely separate electricity journeys, side by
side, never touching, all the way from the street to the computer. They only shake
hands inside the computer itself, where the computer has two plugs and is happy
with either one.

---

## 3. Block diagram — Level 1 (full chain, both paths, with switching states)

```
      11 kV ZONE SUB 1                                    11 kV ZONE SUB 2
             |                                                    |
        [HV MET/PROT]                                        [HV MET/PROT]
             |                                                    |
  ===========+=============                          =============+==========
  |     MV-A  11 kV       |                          |      MV-B  11 kV     |
  |  Fire compartment 1   |                          |  Fire compartment 2  |
  |                       |                          |                      |
  |  CB-A-INC  N.C.       |                          |  CB-B-INC  N.C.      |
  |                       |                          |                      |
  |         [CB-TIE  N.O.]===== MV BUS TIE ==========[CB-TIE  N.O.]         |
  |                       |   interlocked, key-locked |                      |
  |  CB-A-TX1  N.C.       |                          |  CB-B-TX1  N.C.      |
  |  CB-A-TX2  N.C.       |                          |  CB-B-TX2  N.C.      |
  ===========+======+======                          =====+======+===========
             |      |                                     |      |
          TX-A1   TX-A2                                TX-B1   TX-B2
        2500kVA  2500kVA                              2500kVA  2500kVA
        11/0.415 11/0.415                             11/0.415 11/0.415
        Dyn11 6% Dyn11 6%                             Dyn11 6% Dyn11 6%
          3478A   3478A                                 3478A   3478A
             |      |                                     |      |
  ===========+======+===========             ============+======+============
  |  MSB-A  415V  65kA 1s     |             |  MSB-B  415V  65kA 1s       |
  |  Form 4, withdrawable ACB |             |  Form 4, withdrawable ACB   |
  |                           |             |                             |
  | SEC-1        SEC-2        |             | SEC-1        SEC-2          |
  | ACB-A-T1 N.C.|ACB-A-T2 N.C|             | ACB-B-T1 N.C.|ACB-B-T2 N.C. |
  |      [ACB-A-BC  N.O.]     |             |      [ACB-B-BC  N.O.]       |
  |   BUS SECTION COUPLER     |             |   BUS SECTION COUPLER       |
  |                           |             |                             |
  | ACB-A-GEN N.O. <----------+--- GSB-A    | ACB-B-GEN N.O. <---+-- GSB-B|
  |   (interlocked with       |    GEN-A1   |   (interlocked)    |  GEN-B1|
  |    ACB-A-T1/T2, 4-POLE)   |    GEN-A2   |                    |  GEN-B2|
  |                           |   2400kW ea |                    | 2400kW |
  | Outgoing:                 |   paralleled|                    |parallel|
  |  -> UPS-A input     N.C.  |             |  -> UPS-B input    N.C.     |
  |  -> MECH BOARD A    N.C.  |             |  -> MECH BOARD B   N.C.     |
  |  -> HOUSE BOARD A   N.C.  |             |  -> HOUSE BOARD B  N.C.     |
  |  -> NON-ESS BOARD   N.C.* |             |                             |
  ============+================             ============+==================
              |     * shed on generator transfer        |
  ============+================             ============+==================
  |  UPS-A                    |             |  UPS-B                     |
  |  Fire compartment 3       |             |  Fire compartment 4        |
  |                           |             |                            |
  |  RECTIFIER -> DC BUS -> INVERTER        |  RECTIFIER -> DC BUS -> INV |
  |  Frame 1: 6 x 250kW (N+1) |             |  Frame 1: 6 x 250kW (N+1)  |
  |  Frame 2: 6 x 250kW (N+1) |             |  Frame 2: 6 x 250kW (N+1)  |
  |  Parallel bus, 2500kW     |             |  Parallel bus, 2500kW      |
  |                           |             |                            |
  |  BATTERY-A 480kWh LFP     |             |  BATTERY-B 480kWh LFP      |
  |  4 x 120kWh strings       |             |  4 x 120kWh strings        |
  |  Separate battery room    |             |  Separate battery room     |
  |                           |             |                            |
  |  [STATIC BYPASS   N.O.]   |             |  [STATIC BYPASS   N.O.]    |
  |   auto, <1/4 cycle        |             |   auto, <1/4 cycle         |
  |  [MAINT BYPASS    N.O.]   |             |  [MAINT BYPASS    N.O.]    |
  |   manual, interlocked     |             |   manual, interlocked      |
  ============+================             ============+==================
              |                                          |
        UOB-A 415V                                  UOB-B 415V
     (UPS output board)                          (UPS output board)
              |                                          |
    +---------+---------+                      +---------+---------+
    |                   |                      |                   |
 HALL 1              HALL 2                 HALL 1              HALL 2
 RPP-A1..A4          RPP-A5..A8             RPP-B1..B4          RPP-B5..B8
 400A TP&N ea        400A TP&N ea           400A TP&N ea        400A TP&N ea
    |                   |                      |                   |
 RackPDU-A           RackPDU-A              RackPDU-B           RackPDU-B
 32A 3-ph            32A 3-ph               32A 3-ph            32A 3-ph
    |                   |                      |                   |
    +-------------------+----------+-----------+-------------------+
                                   |
                    +--------------+---------------+
                    |  DUAL-CORDED IT EQUIPMENT    |
                    |  250 racks / 8 kW avg        |
                    |  PSU-1 <- A    PSU-2 <- B    |
                    +------------------------------+

                    SINGLE-CORDED LOADS (assumed 100 kW):
                      RackPDU-A ---+
                                   +--> [rack STS/ATS] --> device
                      RackPDU-B ---+

  MECHANICAL SPLIT (deliberate, prevents one board outage killing all cooling):
    MECH BOARD A: Chiller 1, Chiller 3, Pri pumps 1&3, Sec pumps 1&3, CRAH odd
    MECH BOARD B: Chiller 2, Chiller 4, Pri pumps 2&4, Sec pumps 2&4, CRAH even

  CONTROL POWER (independent per path — a critical anti-common-mode measure):
    DC-A: 110 V DC battery + charger, feeds MV-A, MSB-A, GSB-A protection
    DC-B: 110 V DC battery + charger, feeds MV-B, MSB-B, GSB-B protection
```

### Technical explanation of the diagram

Read it in four passes, which is how a reviewer will read it:

**Pass 1 — trace the power.** Utility at 11 kV, through HV metering and network
protection, into the MV switchboard. Two transformer feeders per MV board, each to
a 2,500 kVA cast resin transformer stepping to 415 V. Each transformer lands on its
own section of the LV main switchboard. The generator switchboard connects to the
LV main board through an interlocked, 4-pole ACB. From the LV board, four outgoing
groups: UPS input, mechanical board, house board, and (Path A only)
non-essential board. Through the UPS, to the UPS output board, to the RPPs in each
hall, to the rack PDUs, to the server.

**Pass 2 — check the switching states.** Every device is annotated. MV tie
`N.O.` — the paths are not coupled at MV. LV bus couplers `N.O.` — the
transformers are not paralleled, which keeps fault level at 58 kA rather than
116 kA. Generator ACBs `N.O.` — generators are off-load in the normal state.
Static and maintenance bypasses `N.O.` — the UPS is in double conversion.
Reading only the `N.C.` devices gives you the actual normal-state topology, and
it is two completely separate trees.

**Pass 3 — hunt for common elements.** Scan for anything appearing in both trees.
The MV tie is there but open and interlocked. The STS is there, and it is a
deliberate, documented exception serving only single-corded loads. The chilled
water ring main is a mechanical common element (not on this drawing) that requires
sectionalising valves. The IT equipment itself is the intended convergence point.
Everything else — rooms, fire compartments, cable routes, DC control supplies,
fuel systems — is duplicated. **That scan is the actual design review.**

**Pass 4 — check the 4-pole note on the generator ACB.** This is a subtle point
that separates competent from careless. Both the transformer neutral and the
generator neutral are earthed. If the utility/generator changeover switched only
three poles, the two neutrals would remain connected together through the LV
neutral bar, creating a parallel neutral–earth path. Load neutral current would
then divide between the neutral conductor and the earth path, which causes
circulating currents and, more seriously, **causes earth fault protection to
misoperate or fail to operate**, because the earth fault relay sees normal load
current in its measurement path. Switching all four poles keeps exactly one
earthed neutral in service at any time. This is the correct solution and it needs
to be explicit on the drawing, not assumed.

### Explain Like I'm 10

Look at the picture and notice it's a mirror. Everything on the left has a twin on
the right, and there's a gap down the middle where they never touch. The little
`N.O.` labels mean "this switch is normally left open" — like a door that exists
but is kept shut and locked. There *is* a door between the left side and the right
side, but it's locked, and only a person with the key can open it, and only when
they're doing repairs.

At the very bottom, the two sides finally meet — inside the computer, which has
two plugs. That's the whole point of building two of everything: so the computer
always has a working plug.

---

## 4. AutoCAD Electrical brief

I do not operate AutoCAD. Below is the engineering information for you to produce
the drawing yourself.

### 4.1 Drawing register

| Drawing No. | Title | Purpose | Scale |
|---|---|---|---|
| DC2MW-EL-SLD-001 | Electrical Single Line Diagram — Overall Key Diagram | Whole-facility topology on one sheet, both paths | NTS, A1 |
| DC2MW-EL-SLD-002 | Single Line Diagram — 11 kV MV Distribution | MV switchboards, tie, transformer feeders, HV metering | NTS, A1 |
| DC2MW-EL-SLD-003 | Single Line Diagram — MSB-A and Generator SB-A | Path A LV main board, sections, coupler, generator changeover | NTS, A1 |
| DC2MW-EL-SLD-004 | Single Line Diagram — MSB-B and Generator SB-B | Path B equivalent | NTS, A1 |
| DC2MW-EL-SLD-005 | Single Line Diagram — UPS A and B, Bypass Arrangement | Rectifier, inverter, static and maintenance bypass, battery | NTS, A1 |
| DC2MW-EL-SLD-006 | Single Line Diagram — Critical Power Distribution to Rack | UOB, RPP, rack PDU, dual-cord and STS arrangement | NTS, A1 |
| DC2MW-EL-SLD-007 | Single Line Diagram — Mechanical and House Distribution | Mechanical board split, house boards, non-essential shedding | NTS, A1 |
| DC2MW-EL-SCH-001 | Earthing and Bonding Schematic | MEN, transformer and generator neutral earthing, 4-pole switching | NTS, A1 |
| DC2MW-EL-SCH-002 | Control and Metering Schematic | DC control supplies, EPMS/BMS interfaces, protection scheme | NTS, A1 |

### 4.2 Sheet structure for DC2MW-EL-SLD-001

- **Vertical organisation, top to bottom:** utility → MV → transformers → LV main
  → generators (entering from the side at LV level) → UPS → UOB → RPP → rack.
- **Horizontal organisation:** Path A occupies the left half, Path B the right
  half, with a clear vertical whitespace gutter down the centre. Nothing crosses
  that gutter except the MV tie (drawn dashed), the STS feeds, and the final
  convergence at the IT load. **The visual emptiness of that gutter is the
  drawing's most important feature.**
- **Bottom-left:** notes block.
- **Bottom-right:** legend, revision block, title block.
- **Top-right:** key/index to the other SLD sheets.

### 4.3 Required symbols

| Element | Symbol |
|---|---|
| Utility supply | Incoming arrow with network designation |
| HV metering | Circle with 'M', CT and VT symbols |
| MV circuit breaker | Standard CB symbol, withdrawable indicated |
| Transformer | Two-winding, with vector group and impedance annotated |
| Air circuit breaker (ACB) | Standard, withdrawable indicated by carriage symbol |
| Moulded case CB (MCCB) | Standard |
| Bus section coupler | CB symbol, dashed if normally open |
| Generator | Circle with 'G' |
| Generator paralleling | Synchronising check symbol at the breaker |
| UPS | Rectangle containing rectifier/inverter symbols |
| Static bypass | Thyristor pair symbol |
| Maintenance bypass | Manually operated switch, interlock reference |
| Battery | Standard battery symbol with kWh annotation |
| STS | Rectangle with two inputs, one output, thyristor symbols |
| Distribution board / RPP | Rectangle with rating |
| Rack PDU | Rectangle with outlet count and rating |
| Current transformer | Standard CT |
| Protection relay | Rectangle with ANSI device numbers |
| Metering point | Circle with 'M' |
| Earth / MEN connection | Standard earth symbol, MEN link shown explicitly |
| Isolation point | Triangle or specific isolation symbol per your template |
| Interlock | Dashed line between interlocked devices with 'I' annotation |
| Fire compartment boundary | Heavy dash-dot line with FRL annotation |

### 4.4 Equipment tagging convention

Adopt and apply consistently:

```
  [SYSTEM]-[PATH][NUMBER]

  MV-A, MV-B                      MV switchboards
  TX-A1, TX-A2, TX-B1, TX-B2      Transformers
  MSB-A, MSB-B                    LV main switchboards
  GSB-A, GSB-B                    Generator switchboards
  GEN-A1, GEN-A2, GEN-B1, GEN-B2  Generators
  UPS-A1, UPS-A2, UPS-B1, UPS-B2  UPS frames
  BATT-A, BATT-B                  Battery systems
  UOB-A, UOB-B                    UPS output boards
  RPP-A1..A8, RPP-B1..B8          Rack power panels
  MECH-A, MECH-B                  Mechanical boards
  HSE-A, HSE-B                    House boards
  NESS-1                          Non-essential board
  DC-A, DC-B                      DC control supplies

  Devices:  [BOARD]-[TYPE]-[FUNCTION]
  MSB-A-ACB-T1                    ACB on transformer 1 incomer at MSB-A
  MSB-A-ACB-BC                    Bus coupler ACB at MSB-A
  MSB-A-ACB-GEN                   Generator incomer ACB at MSB-A
  MV-A-CB-TIE                     MV tie breaker, MV-A end
```

### 4.5 Information to annotate at each element

**Transformers:** tag, kVA, ratio, vector group, %Z, LV FLC, cooling class,
insulation class, temperature rise, HV and LV protection reference.

**Switchboards:** tag, voltage, busbar rating (A), Icw (kA/s), Form of
separation, IP rating, AS/NZS 61439 reference.

**Circuit breakers:** tag, frame rating, trip unit setting range, Icu, poles,
withdrawable/fixed, protection functions (ANSI numbers), interlock references.

**Generators:** tag, kVA and kW standby rating, voltage, PF, alternator class,
governor/AVR class, day tank litres, ISO 8528 performance class
(*verification required*).

**UPS:** tag, kW rating, module count and rating, input/output voltage, efficiency
at stated load, bypass arrangement, battery autonomy at stated load.

**Batteries:** tag, chemistry, kWh, string count, nominal DC voltage, autonomy at
full and half load, BMS reference.

**Cables/busduct:** circuit reference, conductor size and material, insulation,
number of parallel runs, length, calculated volt drop, AS/NZS 3008 reference.

**Every switching device:** `N.O.` or `N.C.`

### 4.6 Required notes block

```
NOTES
1.  SELF-DIRECTED ENGINEERING PROJECT. NOT A COMMISSIONED CLIENT DESIGN.
    NOT FOR CONSTRUCTION. NO PROFESSIONAL ENGINEERING CERTIFICATION APPLIES.
2.  ALL SWITCHING DEVICES SHOWN IN NORMAL OPERATING POSITION.
    N.O. = NORMALLY OPEN, N.C. = NORMALLY CLOSED.
3.  MV BUS TIE MV-A-CB-TIE / MV-B-CB-TIE IS NORMALLY OPEN, MECHANICALLY
    AND ELECTRICALLY INTERLOCKED, AND KEY-LOCKED. CLOSURE PERMITTED ONLY
    UNDER WRITTEN SWITCHING INSTRUCTION.
4.  LV BUS SECTION COUPLERS NORMALLY OPEN. TRANSFORMERS SHALL NOT BE
    PARALLELED. PROSPECTIVE FAULT CURRENT IS BASED ON ONE TRANSFORMER
    PER SECTION.
5.  UTILITY / GENERATOR CHANGEOVER IS 4-POLE. NEUTRAL SWITCHING IS
    REQUIRED TO MAINTAIN A SINGLE EARTHED NEUTRAL POINT AND TO PREVENT
    EARTH FAULT PROTECTION MALOPERATION.
6.  PATH A AND PATH B SHALL BE INSTALLED IN SEPARATE FIRE COMPARTMENTS
    WITH SEPARATE CABLE CONTAINMENT AND SEPARATE RISERS. NO SHARED
    PENETRATIONS.
7.  DC CONTROL SUPPLIES ARE INDEPENDENT PER PATH. NO PROTECTION OR
    CONTROL FUNCTION SHALL DEPEND ON BOTH DC SYSTEMS.
8.  PROSPECTIVE FAULT LEVELS SHOWN ARE PRELIMINARY, BASED ON TRANSFORMER
    IMPEDANCE ONLY. A FORMAL FAULT LEVEL STUDY IS REQUIRED.
9.  PROTECTION COORDINATION IS NOT PROVEN BY THIS DRAWING. A SELECTIVITY
    STUDY USING SPECIALIST SOFTWARE IS REQUIRED.
10. ALL EQUIPMENT RATINGS ARE PRELIMINARY PENDING VENDOR CONFIRMATION.
    REFER ASSUMPTIONS REGISTER DC2MW-EL-REG-001.
```

### 4.7 Revision philosophy

| Rev | Trigger | Issue status |
|---|---|---|
| A / 0.1 | First issue | Issued for internal review |
| B / 0.2 | Post 30% design review comments | Issued for review |
| C / 0.3 | Post 60% design review, equipment sizing confirmed | Issued for review |
| D / 0.4 | Post 90% review, protection and controls added | Issued for review |
| 1.0 | Post 100% review | Issued for portfolio |

Rules: never reissue without a revision. Every revision carries a revision cloud
and a revision description in the title block. A revision that changes topology
requires a re-run of the failure mode analysis and the concurrent maintainability
assessment — **the SLD is not a standalone document, and a topology change
invalidates the analysis downstream of it.**

### 4.8 What you should be able to understand by looking at the finished drawing

1. Where the electricity comes from, and that there are two independent sources.
2. Every box it passes through, in order, on its way to a server.
3. Which side is Path A and which is Path B, without reading any labels.
4. That the two sides do not touch, because the gutter down the middle is empty.
5. The normal operating state of every switching device.
6. Where you could safely isolate any given asset.
7. What protects each element, and what it is protected against.
8. The one place where the two paths deliberately meet, and why.

If a reviewer has to ask you any of those eight questions, the drawing needs
another revision.
