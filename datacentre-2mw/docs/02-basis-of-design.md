# Basis of Design — Electrical, Critical Power

> **SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN**
> No client, no site, no professional engineering sign-off. Not for construction.

**Document:** DC2MW-EL-BOD-001
**Rev:** 0.1
**Date:** 2026-09-19
**Status:** Issued for 30% Design Review
**Prepared by:** [Engineer] — self-directed project

---

## 0. What a Basis of Design is, and why it exists first

### Engineer Explanation

The Basis of Design (BoD) is the controlling narrative document that records
**every input, assumption, decision, criterion and exclusion** on which the design
rests. It is written before detailed engineering and maintained throughout.

It exists to solve four specific problems:

1. **Traceability.** Six months into a project, someone asks "why is the
   transformer 2,500 kVA?" The BoD answers it, with the load build-up, the margin
   and the redundancy case. Without a BoD, the answer is "because it's on the
   drawing", which is not an answer.
2. **Assumption exposure.** Designs are built on assumptions. The dangerous ones
   are the undocumented ones, because they cannot be challenged or verified. The
   BoD forces every assumption into the open where a reviewer can attack it.
3. **Scope boundary.** It records what is *not* included. Most commercial disputes
   on real projects are about exclusions that were never written down.
4. **Change control.** When a client changes the rack density from 8 kW to 12 kW,
   the BoD is what tells you which twelve calculations and four equipment
   selections now have to be redone — and forms the basis of the variation.

On a real project the BoD is authored by the lead designer, reviewed by the
client and the independent commissioning authority, and becomes a contractual
reference document.

**The discipline that makes a BoD useful** is classifying every number into one of
four categories, and never blurring them:

| Category | Meaning | Who owns it | Can it change? |
|---|---|---|---|
| **Given requirement** | Stated by the client/brief. Not ours to change. | Client | Only by formal change |
| **Engineering assumption** | We chose a value because we had to, pending information. | Designer, pending confirmation | Yes — tracked in Assumptions Register |
| **Calculated value** | Derived from the above by a traceable calculation. | Calculation | Only if inputs change |
| **Design decision** | We chose between valid engineering options. | Designer | Yes, with justification |

Blurring these is the most common failure in engineering documentation. An
assumption presented as a requirement cannot be challenged. A decision presented
as a calculation cannot be revisited. On this project the rule is absolute: **every
number in this document carries its category.**

### Explain Like I'm 10

Before you build a house, you and the builder sit down and agree on all the
rules: how many bedrooms, how big the block is, which way the sun comes in, how
much money there is, what the council will allow. You write it all down. Then
when the builder later says "I made the kitchen smaller", you can point at the
page and say "no — we agreed it was four metres".

The really important bit is being honest about which things you actually *know*
and which things you're just *guessing for now*. "The block is 600 square metres"
— you know that, someone measured it. "A family of four needs three bedrooms" —
that's a guess you've made, and someone might disagree. If you write your guesses
down as if they were facts, then later when a guess turns out wrong, nobody can
find it and fix it. The whole house is built on something nobody remembers
deciding.

### Practical Data Centre Example (our design)

In this document we have **2 given requirements** (2 MW IT load, 2N
architecture — both from the project brief), **31 engineering assumptions** (see
`registers/assumptions-register.csv`), **a set of calculated values** (all shown
with their working), and **12 design decisions** (see
`registers/design-decision-register.csv`). Every table cell below is labelled
`[G]` given, `[A]` assumption, `[C]` calculated or `[D]` decision.

### Interview Connection

If you are asked *"how do you start a data centre electrical design?"*, the answer
is not "with the single line diagram". It is: *"With the Basis of Design — you
establish the load, the redundancy philosophy, the maintainability philosophy and
the environmental conditions first, and you classify every input as a given
requirement, an assumption, a calculated value or a design decision. The SLD is an
output of that, not an input to it."*

---

## 1. Project description

A notional purpose-built data centre facility in an Australian metropolitan
temperate-climate location, providing 2,000 kW of IT load capacity across two data
halls, with 2N critical power distribution and N+1 mechanical plant.

| Item | Value | Type |
|---|---|---|
| Total IT design load | 2,000 kW | [G] |
| Critical power architecture | 2N | [G] |
| Data halls | 2 | [A] |
| Racks | 250 (125 per hall) | [C] = 2,000 / 8 |
| Average rack design density | 8 kW | [A] |
| High-density zone capability | up to 15 kW/rack, 10% of racks | [A] |
| Mechanical architecture | Air-cooled chillers, primary/secondary CHW, CRAH | [D] DDR-001 |
| Mechanical redundancy | N+1 | [D] DDR-002 |
| Design life | 15 years electrical, 20 years civil | [A] |
| Ultimate site capacity | 2 MW day one, no phased expansion | [A] |

---

## 2. Design criteria — electrical

| Parameter | Value | Type |
|---|---|---|
| Utility supply voltage | 11 kV, 3-phase | [A] |
| Utility supply arrangement | 2 feeders, separate zone substations | [A] |
| Utility feeder capacity (each) | 5 MVA minimum, each capable of 100% site | [A] |
| LV distribution voltage | 415 V 3-phase / 240 V 1-phase | [A] |
| Frequency | 50 Hz | [A] |
| Earthing system (LV) | MEN, per AS/NZS 3000 | [D] DDR-003 |
| Earthing system (MV) | Per AS/NZS 2067 — *clause verification required* | [D] |
| Transformer vector group | Dyn11 | [D] |
| Transformer type | Cast resin dry-type, indoor | [D] DDR-005 |
| Transformer impedance | 6.0% | [A] — *vendor confirmation required, TQ-002* |
| LV switchboard form of separation | Form 4 (critical), Form 3b (non-critical) | [D] — *AS/NZS 61439 clause verification required* |
| LV switchboard Icw | 65 kA, 1 s | [A] — *subject to fault study, TQ-004* |
| Design power factor at intake | ≥ 0.95 lagging | [A] |
| Maximum voltage drop, source to load | 5% total | [A] — *AS/NZS 3000 clause verification required* |
| Maximum continuous equipment loading (normal) | 50% | [D] |
| Maximum continuous equipment loading (single path) | 80% | [D] DDR-007 |
| Design ambient (electrical rooms) | 40 °C | [A] |
| Design ambient (external, plant sizing) | 38 °C DB | [A] — *AIRAH/ASHRAE design day verification required, TQ-005* |
| Altitude | < 100 m AHD, no derating | [A] |
| UPS battery autonomy | 10 minutes at full rated path load | [D] DDR-009 |
| Generator fuel autonomy | 48 hours at full facility load | [D] DDR-010 |
| Generator start to on-load | ≤ 15 s | [A] |

---

## 3. Load schedule summary

Full load schedule is a Week 2 deliverable. Summary build-up:

### 3.1 IT load

| Item | Value | Type |
|---|---|---|
| Racks | 250 | [C] |
| Average design density | 8 kW | [A] |
| IT load at rack PDU output | 2,000 kW | [G] |
| Diversity applied | 1.0 (design load already diversified) | [A] |
| IT power factor | 0.99 (modern PSU, PFC) | [A] |
| Single-corded proportion | 5% = 100 kW | [A] — TQ-006 |
| Path A normal share | 1,000 kW | [C] |
| Path B normal share | 1,000 kW | [C] |
| **Per-path design capability** | **2,000 kW** | [C] |

### 3.2 Mechanical load

Thermal load first:

```
IT heat load                          2,000 kW(th)   [C]
Lighting, people, envelope, misc.       150 kW(th)   [A]
------------------------------------------------------
Total sensible cooling load           2,150 kW(th)   [C]
```

Chiller selection:

```
Required thermal duty                 2,150 kW(th)
Chiller COP at 38 degC ambient           2.9         [A] TQ-005
Electrical draw                       2,150 / 2.9 = 741 kW
Round up for part-load and fouling      780 kW       [A]
```

| Item | Duty | Standby | Unit rating | Operating kW | Type |
|---|---|---|---|---|---|
| Air-cooled screw chillers | 3 | 1 | 750 kW(th) | 780 | [D] |
| CHW primary pumps | 3 | 1 | 15 kW | 45 | [A] |
| CHW secondary pumps | 3 | 1 | 30 kW | 90 | [A] |
| CRAH units (EC fan) | 20 | 4 | 8 kW fan | 170 | [A] |
| Mech controls, valves, humidity | — | — | — | 25 | [A] |
| **Total mechanical operating** | | | | **1,110 kW** | [C] |

### 3.3 House and ancillary load

| Item | kW | Type |
|---|---|---|
| Lighting (halls, plant, offices, external) | 60 | [A] |
| Small power and offices | 40 | [A] |
| Fire and life safety | 30 | [A] |
| Security, access control, CCTV | 20 | [A] |
| BMS / EPMS head end | 15 | [A] |
| Lifts, roller doors, workshop | 30 | [A] |
| Generator ancillaries (jacket heaters, chargers, fuel transfer) | 40 | [A] |
| **Total house and ancillary** | **235** | [C] |

### 3.4 Losses

| Item | kW | Basis | Type |
|---|---|---|---|
| UPS losses | 85 | 2,000 kW at 96% efficiency | [C] |
| Transformer losses | 35 | ~1.0% at operating load | [A] |
| **Total losses** | **120** | | [C] |

### 3.5 Total facility load

| Category | kW |
|---|---|
| IT load | 2,000 |
| UPS losses | 85 |
| Mechanical | 1,110 |
| House and ancillary | 235 |
| Transformer losses | 35 |
| **Total facility design load** | **3,465** |
| **At 0.95 PF** | **3,647 kVA** |

**Design-day PUE = 3,465 / 2,000 = 1.73** [C]
**Assumed annualised PUE = 1.40** [A]

Reconciliation note: the two figures differ because design-day is computed at
38 °C ambient with all chillers at worst-case COP, whereas the annualised figure
benefits from the large number of hours at lower ambient. **Design-day is what
sizes the electrical equipment. The annualised figure is an energy-performance
metric only and is not used anywhere in the electrical sizing.**

---

## 4. Equipment sizing

Every selection follows the same sequence and no selection skips a step:

> **Load → Design margin → Redundancy requirement → Selected rating**

### 4.1 Utility intake

```
Step 1  Load                     3,647 kVA (total facility, 0.95 PF)
Step 2  Design margin            +15% future/measurement uncertainty
                                 3,647 x 1.15 = 4,194 kVA
Step 3  Redundancy               Each feeder must carry 100% of site
                                 (2N at the intake)
Step 4  Selected                 2 x 5,000 kVA capacity 11 kV feeders
        Feeder current           3,647 / (1.732 x 11) = 191 A normal
                                 5,000 / (1.732 x 11) = 262 A rated
```

*Network capacity is subject to a formal supply application to the DNSP.
TQ-007.*

### 4.2 Transformers

```
Step 1  Load per path, worst case (full facility on one path)
        IT 2,000 + UPS loss 85 + mech 1,110 + house 235 = 3,430 kW
        at 0.95 PF                                     = 3,610 kVA
Step 2  Design margin            Loading limit 80% in single-path operation
                                 3,610 / 0.80 = 4,513 kVA required per path
Step 3  Redundancy               2 transformers per path, so that one
                                 transformer can be isolated for maintenance
                                 while the path remains in service
Step 4  Selected                 4 x 2,500 kVA (2 per path)
                                 Path capacity = 5,000 kVA per path
```

Loading verification — this is the table a reviewer goes to first:

| Scenario | Path A kVA | On how many TX | Loading | Verdict |
|---|---|---|---|---|
| Normal 2N, both paths | 1,805 | 2 × 2,500 | **36%** | OK |
| Path B out entirely | 3,610 | 2 × 2,500 | **72%** | OK, < 80% |
| TX-A1 in maintenance, Path B healthy | 1,805 | 1 × 2,500 | **72%** | OK, < 80% |
| TX-A1 out **and** Path B out | 3,610 | 1 × 2,500 | **144%** | **OVERLOAD** |

The last row is a double contingency and is documented, not designed out. The
mitigation is automatic load shedding: dropping non-essential boards (235 kW) and
the mechanical N+1 standby units brings the load to approximately 3,000 kVA =
120%, still an overload, so IT load reduction or a mechanical setpoint relaxation
would be required. **This is recorded as a known limitation, not concealed.** See
TQ-008 for the load-shedding hierarchy that needs developing in Week 6.

Transformer electrical particulars:

```
Rating              2,500 kVA
Ratio               11,000 / 415 V
Vector group        Dyn11
Impedance           6.0% [A]
LV full load current  2,500,000 / (1.732 x 415) = 3,478 A  [C]
Prospective Isc at LV terminals (transformer only):
                    3,478 / 0.06 = 57,970 A = 58 kA  [C]
```

**Why the LV bus coupler is normally open** — the quantified reason: with both
transformers paralleled on a common bus, prospective fault current approximately
doubles to **116 kA**, which pushes the switchboard from a commercially standard
65 kA class into a specialist and far more expensive class, and materially worsens
arc-flash incident energy. Keeping the coupler open holds fault level at 58 kA.
The second reason is path independence — a paralleled bus is a single bus, and a
busbar fault on it takes both transformers. [D] DDR-011

### 4.3 Generators

```
Step 1  Load per path, worst case            3,430 kW
Step 2  Design margin
        Non-linear load allowance (UPS
        rectifier, modern IGBT front end
        with THDi < 5%)                      +10%
        Loading limit for step-load
        acceptance and long-term health      target <= 75%
                                             3,430 x 1.10 / 0.75 = 5,031 kW
Step 3  Redundancy                           N per path (2 sets), redundancy
                                             provided by the other path
Step 4  Selected                             4 x 3,000 kVA / 2,400 kW standby
                                             (2 per path, paralleled)
                                             Path capacity = 4,800 kW
```

Loading verification:

| Scenario | Path A kW | Sets running | Loading | Verdict |
|---|---|---|---|---|
| Utility loss, normal 2N split | 1,715 | 1 × 2,400 | 71% | OK |
| Utility loss, normal 2N split | 1,715 | 2 × 2,400 | 36% | Low — wet stacking risk on extended runs |
| Utility loss + Path B out | 3,430 | 2 × 2,400 | **71%** | OK |
| Utility loss + Path B out + 1 set failed | 3,430 | 1 × 2,400 | **143%** | Overload — load shed required |

Note the second row. Running both sets at 36% for an extended outage risks
**wet stacking** (incomplete combustion, unburnt fuel fouling the exhaust). The
operating philosophy must therefore include a **generator loading strategy**:
run one set per path for normal split load, and auto-start the second only on
demand or for the takeover case. That is a controls requirement, recorded as
TQ-009, and it is exactly the kind of thing that gets missed when generators are
sized on capacity alone.

Fuel:

```
Total facility on generator          3,465 kW
Specific fuel consumption at ~70%    0.25 L/kWh  [A] TQ-010
Consumption                          3,465 x 0.25 = 866 L/h
48 hours                             866 x 48 = 41,570 L
Unpumpable / margin                  +10% = 45,730 L
Selected                             2 x 25,000 L bulk tanks (one per path)
                                     = 50,000 L, with normally-closed manual
                                       cross-connect
Day tanks                            4 x 1,000 L (one per set)
```

### 4.4 UPS

```
Step 1  Load per path, worst case            2,000 kW (full IT load)
Step 2  Design margin                        Loading limit 80% single-path
                                             2,000 / 0.80 = 2,500 kW per path
Step 3  Redundancy                           2N at system level,
                                             N+1 at module level within frames
Step 4  Selected                             Per path: 2 x 1,250 kW modular
                                             frames on a parallel bus
                                             Each frame: 6 x 250 kW modules
                                             (1,500 kW installed, 1,250 kW
                                              rated, N+1)
                                             Path capacity 2,500 kW
                                             Total installed 6,000 kW modules
                                             for a 2,000 kW load
```

| Scenario | Load | Rated capacity | Loading | Verdict |
|---|---|---|---|---|
| Normal 2N | 1,000 kW per path | 2,500 kW | 40% | OK |
| Path B in maintenance bypass | 2,000 kW on A | 2,500 kW | **80%** | OK, at limit |
| Path B out + 1 A module failed | 2,000 kW on A | 2,500 kW (N+1 covers) | 80% | OK |
| Path B out + 1 A **frame** failed | 2,000 kW on A | 1,250 kW | **160%** | **LOAD LOST** |

The 6,000 kW of installed module capacity for a 2,000 kW load is a **3.0× ratio**.
Being able to justify that to a cost-driven client — and to identify the one
double-contingency it still does not cover — is the point of this table.

*Note: 80% is at our stated design limit with no headroom. A reviewer may
legitimately argue for 2 × 1,500 kW frames per path instead, giving 3,000 kW per
path and 67% single-path loading. Recorded as an open design question, TQ-011,
for resolution at the 30% review.*

### 4.5 Battery / energy storage

```
Step 1  Load                         2,000 kW AC (full path load)
        Inverter efficiency          96%  [A]
        DC power required            2,000 / 0.96 = 2,083 kW
Step 2  Autonomy                     10 minutes = 0.167 h
        Energy discharged            2,083 x 0.167 = 348 kWh
        End-of-life derating         80%  [A]
        Usable depth of discharge    90%  [A]
        Installed energy (BOL)       348 / (0.80 x 0.90) = 483 kWh
Step 3  Redundancy                   4 independent strings per path, so one
                                     string can be isolated for maintenance
Step 4  Selected                     Per path: 480 kWh (4 x 120 kWh strings)
                                     Chemistry: LFP lithium-ion  [D] DDR-012
```

| Condition | Available energy | Autonomy at 2,000 kW | Autonomy at 1,000 kW |
|---|---|---|---|
| All 4 strings, BOL | 483 kWh effective | 10.0 min | 20.0 min |
| 3 strings (1 isolated) | 362 kWh effective | **7.5 min** | 15.0 min |
| All 4 strings, EOL | 386 kWh effective | 8.0 min | 16.0 min |

All cases exceed the 15 s generator start requirement by a very wide margin. The
10-minute figure is not about generator start time — it is about giving operators
time to diagnose and intervene on a failed generator start, and to execute a
controlled IT shutdown if they cannot. [D] DDR-009.

*Cell count, string voltage, BMS architecture and fire/thermal-runaway
requirements all require vendor data. TQ-012. Lithium battery room fire
requirements are a specialist area — **standard/clause verification required**
and likely requires a fire engineering input.*

### 4.6 LV switchboards

```
Step 1  Load                         3,610 kVA per path = 5,022 A at 415 V
Step 2  Design margin                +20% = 6,027 A
Step 3  Redundancy                   Bus-sectioned, NO coupler, one section
                                     per transformer
Step 4  Selected                     MSB-A / MSB-B: 415 V, 2 x 4,000 A
                                     sections, NO bus coupler
                                     Icw 65 kA 1 s  [A] pending TQ-004
                                     Form 4 separation, withdrawable ACBs
                                     Compliant with AS/NZS 61439 series
```

### 4.7 Critical power distribution (RPP)

```
Step 1  Load per hall per path       1,000 kW (full takeover for that hall)
Step 2  Design margin                Loading limit 80%
                                     1,000 / 0.80 = 1,250 kVA at PF ~0.99
Step 3  Redundancy                   Multiple RPPs per hall per path so that
                                     one RPP outage affects a subset of racks,
                                     each rack still fed from the other path
Step 4  Selected                     4 x 400 A TP&N RPP per hall per path
                                     = 4 x 288 kVA = 1,152 kVA
                                     16 RPPs total (8 x A, 8 x B)
                                     Each RPP serves approximately 31 racks
```

### 4.8 Rack PDU

```
Step 1  Load                         8 kW average rack, 15 kW high density
Step 2  Design margin                Each rack PDU carries 100% of rack load
                                     (not 50%) because the other may be absent
Step 3  Redundancy                   2 per rack (A and B)
Step 4  Selected                     Standard rack: 2 x 32 A 1-phase 240 V
                                     metered/switched rack PDU
                                     8 kW / 240 V = 33.3 A -> 32 A marginal;
                                     see note
                                     High density: 2 x 32 A 3-phase
```

**Flagged issue:** 8 kW at 240 V is 33.3 A, which exceeds a 32 A rack PDU. Either
the average density assumption drops to 7.5 kW, or standard racks use 3-phase
16 A rack PDUs (11 kW capability), or a 40 A single-phase device is used. This is
a genuine sizing error caught by doing the arithmetic rather than assuming.
**Recommendation: standardise on 2 × 32 A 3-phase rack PDUs throughout** — 22 kW
capability, covers both standard and high-density racks, simplifies procurement
and spares. Recorded as DDR-013 and TQ-013.

### 4.9 Static Transfer Switch

```
Step 1  Load                         Single-corded IT load, assumed 5% = 100 kW
Step 2  Design margin                +100% (the assumption is weak and
                                     single-corded proportion tends to grow)
                                     = 200 kW
Step 3  Redundancy                   STS is itself a single point of failure
                                     for the loads it serves. Distributing
                                     across many small units limits exposure.
Step 4  Selected                     Rack-level STS / ATS PDUs rather than a
                                     facility-level STS  [D] DDR-008
                                     Rated per rack requirement, fed A and B
```

**Reasoning for rack-level over facility-level**, because this will be
challenged: a single facility-level 200 kVA STS concentrates all single-corded
load behind one device, and that device is a genuine single point of failure with
no bypass. Rack-level units distribute the exposure so that one unit's failure
affects one rack. The counter-argument is more devices, more maintenance points,
and less centralised monitoring. We have chosen distributed exposure over
concentrated exposure. **Standard/clause verification required** on STS
requirements; note also that an STS introduces a device that both paths pass
through, which is a deliberate and documented exception to our
no-common-element rule.

### 4.10 Summary equipment schedule

| Equipment | Qty | Rating | Redundancy |
|---|---|---|---|
| 11 kV utility feeder | 2 | 5,000 kVA | 2N |
| MV switchboard | 2 | 11 kV, NO tie | 2N |
| Distribution transformer | 4 | 2,500 kVA, 11/0.415 kV, Dyn11 | 2 per path |
| LV main switchboard | 2 | 2 × 4,000 A, 65 kA, Form 4 | 2N, bus-sectioned |
| Diesel generator | 4 | 3,000 kVA / 2,400 kW standby | N per path, 2N facility |
| Generator switchboard | 2 | 415 V, paralleling | 2N |
| UPS frame | 4 | 1,250 kW (6 × 250 kW modules) | 2(N+1) |
| Battery system | 2 | 480 kWh, 4 strings, LFP | 2N |
| UPS output board | 2 | 415 V | 2N |
| RPP | 16 | 400 A TP&N | 2N |
| Rack PDU | 500 | 32 A 3-phase | 2N |
| Rack-level STS | TBC | Per single-corded load | Fed A + B |
| Bulk fuel tank | 2 | 25,000 L | 2N |

---

## 5. Redundancy philosophy

| System | Architecture | Justification |
|---|---|---|
| Utility intake | 2N (2 feeders, separate zone subs) | Utility is the most probable source of supply interruption |
| MV switchgear | 2N, NO interlocked tie | Tie provides maintenance flexibility without normal-state coupling |
| Transformers | 2 per path (4 total) | Allows transformer maintenance without losing a path |
| LV main boards | 2N, bus-sectioned, NO coupler | Limits fault level to 58 kA; prevents bus fault crossing sections |
| Generators | N per path, 2N facility | Path redundancy already provides the second layer; 2(N+1) rejected on cost — DDR-006 |
| UPS | 2(N+1) | Maintains single-fault tolerance during UPS maintenance windows |
| Batteries | 2N, 4 strings per path | String-level maintainability |
| Critical distribution | 2N to every rack | Dual-corded IT equipment makes this useful |
| Mechanical plant | N+1 | Cooling has thermal inertia; instantaneous redundancy not required |
| Mechanical electrical supply | Split across MSB-A and MSB-B | Prevents a single board outage taking all cooling |
| House / essential | Generator-backed, single path | Not critical to IT operation |
| Non-essential | Utility only, shed on generator | Preserves generator capacity for loads that matter |

**Explicitly rejected options and why:**

- **2(N+1) generators** — rejected. Two additional 2,400 kW sets, their fuel,
  acoustic treatment, emissions approvals and capital cost for a second layer on
  top of existing path redundancy. Marginal availability gain judged not to
  justify it. DDR-006. *A reviewer may reasonably disagree; the argument is
  recorded so it can be had properly.*
- **Distributed redundant / catcher UPS** — rejected. Cheaper than 2N at scale,
  but the switching and control complexity is harder to operate, harder to
  commission and harder to explain. At 2 MW the capital saving does not justify
  the operational complexity. DDR-014.
- **Normally-closed MV tie** — rejected. Would create a single MV bus and destroy
  2N at the intake.
- **Facility-level STS** — rejected in favour of rack-level. DDR-008.
- **Water-cooled chillers with cooling towers** — rejected. Better COP (and
  therefore better PUE), but introduces water treatment, legionella management,
  makeup water dependency and an additional critical utility. Air-cooled chosen
  for reduced dependency count. DDR-001. *This is a defensible decision in either
  direction and should be argued at the 30% review.*

---

## 6. Maintainability philosophy

Every asset in the critical power chain shall be capable of full isolation,
de-energisation, proving dead, earthing and safe personnel access while the IT
load remains fully operational and, where practical, while single-fault tolerance
is retained.

Enabling requirements, all of which are **specification items** not topology
items:

1. Withdrawable or fully isolatable circuit breakers on all critical boards.
2. Form 4 internal separation on all critical LV boards (AS/NZS 61439 series —
   *clause verification required*).
3. Earthing and short-circuiting provisions on all switchboard busbars and
   incoming/outgoing circuits.
4. Test/isolation links on all protection CT and VT circuits, permitting relay
   secondary injection without a bus outage.
5. Maintenance bypass on every UPS system, mechanically and electrically
   interlocked to prevent paralleling the UPS output with raw supply.
6. Independent DC control supply (battery and charger) per path.
7. Load bank connection points at each generator switchboard for on-load testing
   without the facility load.
8. Sectionalising valves on the chilled water ring main (mechanical interface,
   TQ-003).
9. Segregated Path A and Path B cable containment, in separate risers and
   separate fire compartments, with no shared penetration.

**Verification method:** A written switching sequence for each asset, in the
Concurrent Maintainability Assessment (Week 7 deliverable). No asset will be
recorded as concurrently maintainable without one. Assertion is not verification.

---

## 7. Operating philosophy summary

Full sequences are a Week 4 deliverable. Summary of the normal state and the two
principal events:

**Normal state.** Both utility feeders live. MV tie OPEN. All four transformers
energised. All LV bus couplers OPEN. Generators available, off, jacket heaters
on, day tanks full. Both UPS systems on-line in double conversion, ~40% loaded,
batteries fully charged. All four paths of critical distribution live. IT load
split approximately 50/50 between Path A and Path B. Facility state: 2N, single
fault tolerant.

**Utility failure (both feeders).** UPS A and B pick up the full IT load from
battery instantaneously — zero transfer, zero interruption, because the inverters
were already supplying the load. Non-essential boards shed. Generators receive a
start signal, reach rated speed, achieve stable voltage and frequency, parallel on
their respective generator switchboards, and the utility/generator changeover
transfers within ~15 s. UPS rectifiers walk in over 10–30 s to avoid a step load.
Chillers restart on a sequenced ramp over 60–120 s. Batteries recharge. IT load
never sees an event.

**Utility restoration.** Generators remain on load until the utility is proven
stable for a set time (assumed 5 minutes — [A], TQ-014). Retransfer to utility
occurs either open-transition (brief interruption absorbed by UPS) or
closed-transition (synchronised, no interruption). Generators unload, run for a
cooldown period, then stop. **Design decision required: open or closed transition
retransfer.** DDR-015, to be resolved in Week 3 — closed transition avoids a UPS
battery discharge on every retransfer, but requires synchronising and introduces a
brief period where utility and generator are paralleled, which has network
protection implications requiring DNSP agreement.

---

## 8. Design margins

| Item | Margin | Basis |
|---|---|---|
| Utility intake | +15% on facility load | Future/measurement uncertainty |
| Transformer | 80% max single-path loading | Thermal, and headroom for load growth |
| Generator | 75% max target loading | Step load acceptance and engine health |
| UPS | 80% max single-path loading | Manufacturer recommendation and thermal |
| Battery | EOL 80%, DoD 90% | Ageing and battery management limits |
| Switchboard | +20% on calculated current | Load growth |
| Cables | Per AS/NZS 3008, 5% max volt drop | Standard |
| Fault level | 65 kA against 58 kA calculated | Margin for motor and generator contribution |

---

## 9. Exclusions

Not included in this design package:

- Structural, architectural, civil, hydraulic and fire suppression design.
- Mechanical design beyond the electrical load characteristics of the plant.
- Detailed protection coordination study (requires ETAP / PowerFactory / SKM).
- Arc flash incident energy study and PPE category determination.
- Harmonic analysis and filter design.
- Earthing grid design and soil resistivity study.
- Lightning and surge protection design.
- Structured cabling, ICT and containment design.
- DNSP connection application, network studies and network protection settings.
- Acoustic assessment and emissions approvals for generators.
- Fire engineering for the lithium battery rooms.
- Cost estimate, procurement, programme and construction methodology.
- Any form of professional engineering certification.

---

## 10. Limitations — stated plainly

1. **No professional engineering review has occurred.** This is self-directed
   work by a single engineer. It has not been independently checked.
2. **Protection selectivity is not proven.** A protection philosophy will be
   developed in Week 6, but proving selectivity requires software modelling that
   is outside this project's scope. **This design does not claim proven
   coordination.**
3. **Fault levels are estimated from transformer impedance only.** Motor
   contribution, generator contribution, cable impedance and utility source
   impedance are not modelled. The 65 kA switchboard rating is a judgement, not a
   calculated result.
4. **Vendor data is assumed throughout.** Transformer impedance, chiller COP,
   generator SFC, UPS efficiency and battery characteristics are all engineering
   assumptions pending real vendor documentation.
5. **Continuous cooling is not resolved.** The current design does not provide
   UPS-backed CHW pumps or CRAH fans, nor thermal storage. Under a utility failure
   the data halls will experience a cooling interruption of 60–120 s. Whether this
   is acceptable requires a thermal transient analysis that has not been done.
   TQ-001. **This is the most significant open technical issue in the design.**
6. **Two double contingencies drop IT load**, both documented: UPS frame failure
   during the opposite path's maintenance bypass, and transformer failure during
   the opposite path's outage.
7. **Single-corded load proportion is a guess.** 5% is assumed with no basis. On a
   real project this comes from the IT equipment schedule. TQ-006.
8. **No standard clause numbers are cited anywhere in this document**, because
   they have not been verified against current editions. Standards are referenced
   by number and title only. Every place requiring clause-level compliance is
   marked *clause verification required*.

---

## Explain Like I'm 10 — what this document proves

This document is the rulebook for the whole project. It writes down every single
number we're using, and next to each one it says whether we were *told* that
number, whether we *guessed* it, whether we *worked it out*, or whether we
*chose* it.

That last part is the important bit. Anyone can produce a design full of
confident-looking numbers. What makes this document trustworthy is that it points
at its own weak spots — it says "we guessed the chillers are this efficient, and
if that guess is wrong then the generator is too small", and "if two things break
at once in this particular way, the computers do go off". A rulebook that hides
its weak spots isn't a rulebook, it's an advertisement.
