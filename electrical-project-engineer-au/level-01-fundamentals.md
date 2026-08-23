# Level 1 — Electrical Fundamentals for Project Delivery

## Learning objectives

By the end of this module you can:

1. Read any voltage on an Australian drawing and know what class of equipment, licence
   and access rules apply.
2. Convert between kW, kVA, kVAr, power factor and current for single- and three-phase.
3. Distinguish the **three currents** that drive every design decision: load current,
   prospective short-circuit current, and earth fault current.
4. Estimate a transformer's fault contribution and explain why fault level falls
   downstream.
5. Apply the **chain of ratings** to any part of an installation and spot a broken link.
6. Explain the MEN earthing system in plain language and why it matters on site.
7. Sanity-check volt drop, maximum demand and diversity figures on a submitted design.

---

## 1.0 Why a Project Engineer needs fundamentals

You are not the designer. You will rarely do the calculation yourself. But you are the
person who has to look at a consultant's SLD, a supplier's schedule and an electrician's
question and decide: **is this right, is it safe, and does it hold together?**

Almost every real project failure traces back to a broken link between two numbers that
lived on two different documents. Fundamentals are how you find the break.

The PE mindset in one line: **every number on a drawing came from somewhere and must
agree with the number next to it.**

---

## 1.1 The Australian voltage landscape

| Level | Typical values | Where you see it |
|---|---|---|
| ELV (extra-low) | 24 V DC, 12 V DC, 24 V AC | Control circuits, PLC I/O, instrumentation |
| LV (low voltage) | 230 V single-phase, 400 V three-phase (still widely called 415 V) | MSBs, MCCs, DBs, motors, final circuits |
| HV (high voltage) | 6.6 kV, 11 kV, 22 kV, 33 kV | Site distribution, large motors, DNSP network |
| Sub-transmission / transmission | 66 kV, 132 kV, 220 kV, 275 kV, 330 kV, 500 kV | Zone substations, generation connections |

Notes that matter in practice:

- The **nominal** LV supply in Australia is 230/400 V (harmonised with IEC via AS 60038).
  Older drawings, nameplates and everyday speech still say 240/415 V. They mean the same
  system. Don't raise an RFI over it; do raise one if a *calculation* mixes the two.
- The LV/HV boundary for AC is **1000 V**. Confirm the exact definition and any voltage
  band detail in the current AS/NZS 3000 — do not quote it from memory.
- The voltage class changes **who** may work on it, **what** access procedures apply
  (HV switching, permits, authorised persons), and **which** standards govern the
  switchgear. This is a programme and safety issue long before it is a technical one.

**PE takeaway:** the moment a project has anything above 1000 V, your programme needs
HV authorisation, switching procedures, permits and usually a DNSP or asset-owner
interface. Those have lead times measured in months.

---

## 1.2 The four quantities on every electrical drawing

- **Voltage (V)** — the system it belongs to. Tells you insulation class, clearances,
  and who can touch it.
- **Current (A)** — what determines conductor size, breaker frame size, busbar size and
  heat.
- **Power (W / kW / MW)** — real work done. What the process cares about.
- **Impedance (Ω) / % impedance** — what limits fault current and causes volt drop.

If you know three, the fourth is usually derivable. When a document gives you two
numbers that can't both be true, you've found a problem.

Single phase: `P = V × I × cosφ`
Three phase: `P = √3 × V_LL × I_L × cosφ`
Apparent power: `S(kVA) = √3 × V_LL × I_L ÷ 1000`

Rearranged for the one you'll use constantly:

```
I (A)  =  kVA × 1000 ÷ (√3 × V_LL)          three-phase
I (A)  =  kW  × 1000 ÷ (√3 × V_LL × PF)     three-phase, real power given
I (A)  =  kW  × 1000 ÷ (V × PF)             single-phase
```

**Rules of thumb worth memorising** (for estimating, never for design):

- At 400 V three-phase, current ≈ **1.44 × kVA** (since 1000/(√3×400) = 1.44).
- A 400 V motor draws roughly **2 A per kW** at full load (PF ~0.85, efficiency ~0.9).
  An 11 kW motor ≈ 21 A. A 75 kW motor ≈ 140 A.
- A 1000 kVA transformer at 400 V has a full-load current of about **1440 A**.

These let you glance at an SLD and say "that doesn't look right" before you open a
spreadsheet. That instinct is most of the job.

---

## 1.3 kW, kVA, kVAr and power factor

```
            kVA (apparent)
             /|
            / |
      kVA  /  | kVAr (reactive — magnetising, does no work)
          /   |
         /φ   |
        +-----+
          kW (real — does the work)
```

- **kW** — what the process consumes. Motors, heaters, process load.
- **kVAr** — reactive power. Motors and transformers need it to magnetise; it does no
  useful work but it still occupies cable and transformer capacity.
- **kVA** — the vector sum. **Equipment is rated in kVA because equipment is limited by
  current, not by useful work.**
- **PF = kW / kVA.** Typical uncorrected industrial site: 0.75–0.85. Target after
  correction: 0.95–0.99.

Why a PE cares:
- Transformers, generators, UPS and cables are sized on **kVA**, not kW. A client saying
  "we need 800 kW" at PF 0.8 actually needs 1000 kVA.
- Poor PF costs money — network tariffs commonly penalise it. That's why capacitor banks
  appear on SLDs. Check whether the tariff actually justifies the capital.
- Modern loads (VSDs, LED drivers, UPS, IT) shift the problem from displacement PF to
  **harmonics**. Detuned capacitor banks or active filters may be required. Flag this on
  any project with heavy VSD content — it is a classic late-stage surprise.

---

## 1.4 The three currents

This is the single most important framing in Level 1. Every LV design decision answers
one of these three questions.

| Current | Symbol (typical) | What it drives | Where it comes from |
|---|---|---|---|
| Load / design current | I_b | Cable size, breaker rating, busbar, volt drop | Load schedule, maximum demand, diversity |
| Prospective short-circuit current | I_k / I_sc | Breaking capacity, cable withstand, busbar bracing | Source impedance (transformer, network, cable) |
| Earth fault current | I_ef | Earth conductor size, disconnection time, touch voltage | Earthing arrangement + fault loop impedance |

Load current is about **normal operation**. Short-circuit current is about **the worst
half-second of the equipment's life**. Earth fault current is about **whether someone
dies**.

A cable can be perfectly sized for load current and still be wrong, because it cannot
survive the fault current for the time the upstream breaker takes to clear. That is
Scenario 1 in your list, and we will solve it properly in Level 4.

---

## 1.5 Fault level — where it comes from and why it decays

Fault current is limited by the **impedance between the source and the fault**. Less
impedance = more fault current.

Approximate transformer fault contribution (the estimate every PE should be able to do
in their head):

```
I_fault  ≈  Full-load current  ×  100 / Z%
```

Worked: a 1000 kVA, 11 kV / 400 V transformer with Z = 5.0 %

```
FLC     = 1000 × 1000 ÷ (√3 × 400)  = 1443 A
I_fault ≈ 1443 × 100 / 5.0          ≈ 28,900 A  ≈ 28.9 kA
```

So the MSB immediately downstream must be rated for at least ~29 kA — in practice you
add the network's contribution and pick a standard rating above it, typically **50 kA**
for a board of this size on an Australian commercial or industrial site.

**Why fault level falls as you go downstream:** every metre of cable adds impedance.
By the time you reach a distribution board three cable runs away, prospective fault
current may have dropped from 29 kA to 6 kA or less. That is why:

- The MSB has **ACBs rated 50 kA**.
- The MCC has **MCCBs rated 36 kA**.
- The final DB has **MCBs rated 6 or 10 kA**.

And it is why a designer will sometimes rely on **cascading / back-up protection** —
a downstream device with a lower rating is permitted because the upstream device helps
clear the fault. This is only valid for **manufacturer-tested combinations**. If a
supplier proposes it, ask for the tested-combination tables. Do not accept "it'll be
fine."

**PE takeaway:** fault level is not one number for a site. It is a number *at every
point*. When someone says "the fault level is 31 kA", your response is: **"at which
board?"**

---

## 1.6 The chain of ratings — your master mental model

Read any part of an installation as a chain. Every link has a rating, and the ratings
must relate correctly:

```
SOURCE  ──►  PROTECTIVE DEVICE  ──►  CABLE  ──►  LOAD
(Tx/gen)      (ACB/MCCB/MCB)       (conductor)   (motor/DB)

   │              │                    │            │
 fault         In (rating)         I_z (capacity)  FLC
 level         Icu (breaking)      k²S² (withstand) starting current
               curve/settings      volt drop        duty
```

The five checks, in order:

1. **Load check:** `I_b ≤ I_n ≤ I_z`
   Design current ≤ device rating ≤ cable current-carrying capacity (derated for
   installation conditions, grouping and ambient temperature).
2. **Fault-breaking check:** device breaking capacity (Icu/Ics) ≥ prospective fault
   current at that point.
3. **Cable withstand check:** the cable must survive the fault for as long as the device
   takes to clear it (the k²S² ≥ I²t adiabatic check).
4. **Volt drop check:** the load still gets acceptable voltage at full load and during
   motor starting.
5. **Disconnection / earth fault check:** an earth fault must be cleared within the
   required time, which depends on fault loop impedance.

**This is the checklist you run in your head every time you open an SLD, a cable schedule
or a shop drawing.** Nine times out of ten, when something is wrong on a real project,
it is one of these five checks that nobody closed out.

Note the derating point in check 1 — it catches people constantly. A 95 mm² cable's
tabulated capacity assumes specific installation conditions. Bunch six of them on a
ladder in a 45 °C plant room and the real capacity can drop 30–40 %. The tables and
derating factors live in **AS/NZS 3008.1.1**; the installation rules live in
**AS/NZS 3000**. Verify current values against the current editions.

---

## 1.7 Protection: three different jobs

A single circuit breaker usually does three jobs. Confusing them is a classic beginner
error.

| Job | Protects against | Magnitude | Timing | Device element |
|---|---|---|---|---|
| **Overload** | Sustained current above rating (a jammed conveyor, too many loads) | 1.05–8 × In | Seconds to minutes (thermal, inverse-time) | Thermal / long-time (L) |
| **Short circuit** | Phase-to-phase or phase-to-neutral fault | 8–20 × In, up to kA | Milliseconds (magnetic/instantaneous) | Short-time (S) / instantaneous (I) |
| **Earth fault** | Current returning via earth | Can be small | Fast, for safety | Ground fault (G) / RCD |

Think of it as a **time–current curve**: high current clears fast, moderate overcurrent
clears slowly.

```
 time
  ▲
  │ ██
  │ ███                 thermal / overload region
  │  ████
  │    ██████
  │         ████
  │             ██████
  │──────────────────┐  magnetic / instantaneous region
  │                  █
  └──────────────────█──────────────────►  current
```

**Discrimination (selectivity)** means: for a fault anywhere, only the **nearest upstream
device** operates. If a fault on one small final circuit trips the main incomer and
blacks out the building, you have a discrimination failure. On paper it is proved by
plotting curves so they don't overlap; in practice you also need current-limiting and
energy-let-through data from the manufacturer.

**PE takeaway:** ask early — *"has a protection discrimination study been done, who owns
it, and when is it issued?"* On many projects this is the deliverable that gets forgotten
until commissioning, when it is far too late and expensive to fix.

---

## 1.8 Earthing and the MEN system

Australia uses **MEN — Multiple Earthed Neutral** (a TN-C-S arrangement in IEC terms).

```
          Transformer                       Main switchboard
          secondary                         ┌───────────────────────┐
             ║                              │  Neutral bar ═══╗     │
   A ════════╬══════════════════════════════╪═════════════    ║     │
   B ════════╬══════════════════════════════╪═════════        ║     │
   C ════════╬══════════════════════════════╪═════           MEN    │  ← MEN link:
   N ════════╬══════════════════════════════╪══════           ║     │    one connection
             ║                              │  Earth bar ═════╝     │    between N and E
            ─┴─  Tx earth                   └──────────┬────────────┘
                                                      ─┴─ Main earth electrode
                                                          + bonding to water/structure
```

What you actually need to know as a PE:

- The neutral and earth are connected at **one** point in the installation — the **MEN
  link** at the main switchboard. Downstream of that, neutral and earth are kept
  **separate**. Ever.
- The purpose is a **low-impedance path** back to the source so an earth fault produces
  enough current to trip protection quickly, and so exposed metalwork stays near earth
  potential.
- Common site issues you will personally encounter:
  - A **second N–E bond** created accidentally in a distribution board or a piece of
    packaged plant. Causes circulating currents, nuisance RCD tripping and very confusing
    fault-finding.
  - **Neutrals borrowed** between circuits — a real safety issue and a defect.
  - Missing **equipotential bonding** to structural steel, pipework, cable ladder.
  - Earth continuity broken by a painted flange, a missing star washer, or an
    unterminated earth in a gland plate.
- Generators, UPS and standby systems complicate this. Whether the generator neutral is
  earthed, and what happens at changeover, is a **design decision that must be shown on
  the SLD**. If it isn't shown, that's an RFI.
- HV and large-site earthing (grid design, step and touch potential, earth resistance
  targets) sits under different standards and usually a specialist earthing study.
  Requirements come from the standard, the DNSP and the project spec — verify, don't
  assume.

**PE takeaway:** the MEN link position, the earthing arrangement of any alternative
supply, and the bonding schedule are three things you should be able to point to on the
drawings. If you can't, ask.

---

## 1.9 Volt drop

Current through cable impedance loses voltage. The motor at the end of a long run sees
less than 400 V — and motor torque falls with the **square** of voltage, so a 10 % drop
costs about 19 % of starting torque.

The commonly applied limit in Australian installations is **5 % from the point of supply
to the point of use** (AS/NZS 3000 — confirm the current wording, and note that many
project specifications impose tighter sub-limits, e.g. 2 % on submains and 3 % on final
subcircuits).

Two cases must be checked, and beginners check only the first:

1. **Steady state** — full load current, continuous.
2. **Motor starting** — a DOL motor draws 6–8 × FLC for several seconds. The transient
   drop must not stall the motor or disturb other equipment (lights dipping, contactors
   dropping out, UPS transferring).

**PE takeaway:** on long runs — pump stations, water/wastewater sites, mine sites,
carparks, distributed campuses — volt drop, not thermal capacity, is usually what sets
the cable size. If a cable schedule shows a 240 mm² cable feeding a modest load 400 m
away, that is probably correct, not a mistake. Understand *why* before you challenge it.

---

## 1.10 Maximum demand and diversity

Not everything runs at once. **Maximum demand (MD)** is the realistic peak, not the
arithmetic sum of every nameplate.

- **Connected load** — add up everything. Always the biggest number.
- **Diversity factor** — the allowance that not all loads coincide.
- **Maximum demand** — what you actually size the supply, transformer, main switchboard
  and submains for.

AS/NZS 3000 provides assessment methods and tables (commonly used for commercial and
residential); industrial and process sites are more often assessed by **load list and
process knowledge**, because the process determines coincidence, not a table.

Where PEs get burned:

- The MD calculation was done at concept stage against an assumed tenancy or process,
  then the process changed and nobody revisited it. **Ask when the MD was last updated
  and against which load list revision.**
- Future capacity / spare capacity requirements in the client brief were ignored — then
  the client asks for 25 % spare at handover and the transformer is already installed.
- EV charging, data halls, electrification of gas loads and battery storage are all
  actively changing MD assumptions. On a commercial project in 2026, "does the MD include
  EV charging provision?" is a genuinely valuable question to ask in week one.

**PE takeaway:** maximum demand is the number that determines the size of the most
expensive, longest-lead items on your project — the transformer, the supply, the main
switchboard. Its accuracy is a **commercial and programme risk**, not just a technical
one.

---

## 1.11 The document set — how it all hangs together

Preview of Levels 2–5. Every one of these documents exists to answer a different
question, and they must all agree.

```
 CLIENT BRIEF / SPEC ──► LOAD SCHEDULE ──► MAXIMUM DEMAND ──► SLD (the spine)
                                                               │
        ┌──────────────────────┬──────────────────┬────────────┼───────────────┐
        ▼                      ▼                  ▼            ▼               ▼
  EQUIPMENT SCHEDULE     CABLE SCHEDULE      SCHEMATICS   SWITCHBOARD GA   LAYOUT DWGS
  (what it is)           (what connects it)  (how it      (how it's built) (where it goes)
                                              behaves)
        │                      │                  │            │               │
        └──────────────────────┴──────────┬───────┴────────────┴───────────────┘
                                          ▼
                              TERMINATION / INTERCONNECTION DRAWINGS
                                  (which wire lands on which screw)
                                          ▼
                                 PHYSICAL INSTALLATION
                                          ▼
                              TEST SHEETS ──► COMMISSIONING RECORDS
                                          ▼
                                      AS-BUILTS
```

**The SLD is the spine.** If the SLD changes, something in every other document below it
probably has to change too. Half of all project defects are caused by that not happening.

---

## 1.12 Worked example — the numbers on a real MSB

A 1000 kVA substation feeds an industrial MSB.

```
              11 kV DNSP network
                     │
                    ╱ ╱ ╱   HV switch / fuse (RMU)
                     │
              ┌──────┴──────┐
              │  TX-01      │   1000 kVA, 11 kV / 400 V
              │  Dyn11      │   Z = 5.0 %
              └──────┬──────┘
                     │  LV cables, 4 runs/phase
                     │
                 ┌───┴───┐  ACB-01   2000 A, Icu 50 kA
                 └───┬───┘
    ══════════════════╪══════════════════  MSB busbar 2000 A, 50 kA 1 s
        │             │             │
      MCCB          MCCB          MCCB
      400 A         250 A         160 A
        │             │             │
      MCC-01        DB-01         DB-02
```

Step through it the way a PE does:

1. **Transformer FLC** = 1000 × 1000 ÷ (√3 × 400) = **1443 A**.
   → A 2000 A incomer is sensible: above FLC, with headroom. A 1250 A incomer would be
   an immediate query.
2. **Fault level at the MSB** ≈ 1443 × 100/5.0 ≈ **28.9 kA**, plus network contribution.
   → The 50 kA busbar and ACB rating is credible. A 25 kA rating would be a red flag.
3. **Busbar rating 2000 A** matches the incomer. If the SLD showed a 1600 A busbar with a
   2000 A incomer, that's a query — the board could be loaded beyond its bar rating.
4. **Sum of outgoing feeders** = 400 + 250 + 160 = 810 A of *device rating*. That's fine
   and normal: outgoing ratings are not meant to add up to the incomer, because of
   diversity. But you should still ask: **what is the calculated maximum demand, and does
   it fit under 1443 A with the client's required spare capacity?**
5. **Fault level at MCC-01** will be materially lower than 28.9 kA after the feeder cable
   impedance — which is why the MCC's devices may legitimately be 36 kA rated.

Notice what just happened: with three rules of thumb and no software, you formed a
credible technical opinion about a switchboard. **That is the Level 1 skill.**

---

## 1.13 Exercises

**Exercise A — sanity check.** A supplier's quote says their MCC will be fed by a
630 A MCCB from the MSB and will supply a total connected motor load of 520 kW.
Using the 2 A/kW rule, what is the approximate connected FLC, and what question does
that raise?

**Exercise B — three currents.** For a 90 kW pump motor at 400 V, state roughly:
(i) full load current, (ii) DOL starting current, (iii) which of the three currents
determines contactor size, and (iv) which determines breaker breaking capacity.

**Exercise C — fault level.** A 1500 kVA transformer, 11 kV / 400 V, Z = 6 %.
Estimate the LV fault level. Is a 50 kA switchboard adequate?

**Exercise D — spot the break in the chain.** A schedule shows:
`Circuit P-14: load 180 A design current, 185 A MCCB, 150 mm² Cu XLPE (I_z = 275 A
tabulated), volt drop 4.1 %, prospective fault 22 kA, MCCB Icu 25 kA.`
Run the five checks. Which check can you *not* close out with the information given?

**Exercise E — the desk scenario.** An email arrives from the consultant:
*"Please confirm the switchboard fault rating is adequate. The fault level is 31 kA."*
Write the two questions you send back before you answer anything.

---

## 1.14 Quiz — Level 1

1. A 250 kW three-phase load at 400 V, PF 0.85. Approximately what current?
   (a) 360 A  (b) 425 A  (c) 510 A  (d) 620 A

2. Which quantity is used to size a transformer, and why?
   (a) kW, because that's the useful work
   (b) kVA, because equipment is limited by current
   (c) kVAr, because magnetising current dominates
   (d) PF, because it sets the tariff

3. A switchboard is marked `400 V, 3200 A, 50 kA 1 s`. What does "50 kA 1 s" describe?

4. Fault level at a distribution board 120 m downstream of the MSB will be:
   (a) higher than at the MSB  (b) the same  (c) lower  (d) depends only on the DB size

5. Where is the neutral connected to earth in a standard Australian LV installation?

6. Which of the five chain-of-ratings checks is most likely to be the *real* reason a
   long cable run to a remote pump station is much bigger than its load current suggests?

7. **Judgement question.** An SLD shows a 1000 kVA transformer feeding an MSB with a
   1600 A incoming ACB and a 1600 A busbar. Is this wrong? Explain your reasoning and
   state what you would ask.

---

## What's next

**Level 2 — Reading Single Line Diagrams.** Every symbol on that SLD, built up from
utility to motor, plus the interrogation routine an experienced PE runs on any SLD that
lands on their desk.
