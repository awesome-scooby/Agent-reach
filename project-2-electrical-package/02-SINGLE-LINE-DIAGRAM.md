# STAGE 2 — SINGLE LINE DIAGRAM

**Drawing:** NFD-ELE-SLD-0001 · Rev C (Issued for Approval)
**View it:** [`drawings/NFD-ELE-SLD-0001.svg`](drawings/NFD-ELE-SLD-0001.svg)

---

## 2.1 What an SLD is actually for

An SLD is not a picture of a switchboard. It is **the power system argument**, compressed onto one sheet, showing how energy gets from the source to every load and how a fault is cleared at every point along the way.

Three people read it and want different things:

| Reader | What they are looking for |
|---|---|
| The protection engineer | Can a fault at any point be cleared, and does the nearest device clear it before the one upstream |
| The operator / maintainer | How do I isolate this load safely, and what else goes dark when I do |
| The estimator and the panel builder | How many cubicles, how much busbar, how many devices |

If your SLD answers all three, it is a good SLD. If it only shows what connects to what, it is a block diagram.

**Every symbol on an SLD is a decision someone made and can be asked to defend.** That is why this document exists — the drawing is the output, the reasoning is the competency.

---

## 2.2 Overall architecture, top to bottom

```
            11 kV network (network operator scope)
                      │
              ┌───────┴───────┐
              │    TX-01      │   500 kVA, 11 kV / 415 V, Dyn11, Z = 5 %
              │   Dyn11       │   (existing, client scope)
              └───────┬───────┘
                      │  4-core + earth, client scope
                      │
      ═══════════════════════════════════  MCC-01 incoming terminals X0
                      │
                 [Q1] 630 A 4P MCCB, electronic trip (LSI + G)
                      │
                      ├──── [SPD] Type 1+2 surge protective device
                      │         on dedicated protective device, status → PLC
                      │
                      ├──── [PM-01] Power meter, 3 × CT 600/5, EtherNet/IP
                      │
                      ├──── [KVP] Phase failure / phase sequence relay
                      │
      ╞══════════════════════════════════╡  800 A busbar, 3P + N + E
      │      │      │      │      │      │
     Q11    Q12    Q13    Q14   … Q19   Q20
   VSD-101 VSD-102  DB-01  PKG   spares  control
```

Full device list is on the drawing. What follows is why each block exists.

---

## 2.3 Device-by-device engineering rationale

### 2.3.1 Incoming terminals and cable interface (X0)

**Why it exists.** A defined, labelled, accessible boundary between the installation contractor's cable and our assembly. Without it, nobody owns the joint.

**Arrangement.** Top-entry cable zone, removable undrilled aluminium gland plate, incoming cable landed on bolted busbar links rated for the incoming conductor, not on the breaker terminals directly.

**Why land on links and not the breaker.** Landing a large incoming cable straight onto an MCCB puts mechanical load and heat onto the breaker terminals, makes the breaker very hard to replace, and gives the installer no room. Links cost almost nothing and make the board maintainable.

**Why the gland plate is aluminium and undrilled.**
- *Undrilled* because the installer's final cable selection is not confirmed at build time. Drilling to a guessed cable size is how you end up with a gland plate that does not suit the cable that turns up.
- *Non-magnetic (aluminium or brass)* matters for **single-core** cables. Passing single-core conductors through a steel plate with individual holes creates a magnetic circuit around each conductor, causing eddy-current heating in the plate. With a 3-core or 4-core multicore, the vector sum through the gland is near zero and it is not an issue. Knowing *which case* it matters in is the mark of someone who has thought about it rather than repeated it.

**Must be confirmed before this is final:**
- Cable entry direction (top or bottom) — **TQ-001**, and the general arrangement cannot be completed without it.
- Incoming cable size, type and number of cables per phase.
- Whether the client requires a separate incoming isolation link or a cable box.

---

### 2.3.2 Main incoming circuit breaker Q1 — 630 A 4-pole MCCB

**Why it exists.** Three jobs, and they are separate jobs:
1. **Isolation** — a single point to make the whole board dead for maintenance, lockable in the off position.
2. **Overcurrent protection** for the busbar and the assembly.
3. **A defined upstream reference** for discriminating with the feeder devices below it.

**Why 630 A.** Estimated maximum demand without diversity is roughly 400 A (§1.4). 630 A is the next standard frame, covers it with margin, and leaves headroom for the spare feeders to be loaded later. Going to 400 A would save little and constrain the board's future.

**Why 4-pole and not 3-pole.** The neutral is switched. In a TN-S system with a 4-wire supply, switching the neutral means the board can be made genuinely dead for work, rather than leaving a neutral that can carry current from elsewhere in the installation. It also avoids the hazard of a floating neutral during partial isolation. The cost is a physically larger and more expensive breaker. Some client standards mandate it; some accept 3-pole plus a bolted neutral link. **TQ-001.**

**Why an electronic trip unit rather than thermal-magnetic.** Adjustable long-time (Ir), short-time (Isd) and instantaneous (Ii) elements, plus an earth-fault element. That adjustability is what makes discrimination with the downstream feeder breakers achievable **once the coordination study exists**. A fixed thermal-magnetic breaker locks in a characteristic you cannot tune later.

**What must be confirmed before final selection:**

| Input | Why it decides the breaker |
|---|---|
| **Prospective short-circuit current** | Sets the required **Icu** (ultimate breaking capacity) and **Ics** (service breaking capacity — what it can break and still be serviceable). This is the single biggest unknown in the package. |
| Confirmed maximum demand | Frame size, Ir setting range |
| Coordination study output | The actual Ir / Isd / Ii / earth-fault settings |
| Client standard | 3-pole vs 4-pole, brand, whether a withdrawable/air circuit breaker is mandated |
| Whether the client wants remote trip or status | Auxiliary and alarm contacts, shunt trip, motor operator |

> **Honest position.** The 50 kA Icu device carried in the BOM is provisional and selected against the 25 kA assumption with margin. If the confirmed fault level comes back higher, the device changes. If it comes back much lower, there may be a cost saving worth capturing.

---

### 2.3.3 Surge protective device (SPD)

**Why it exists.** The site has overhead reticulation and a stated history of storm damage to electronics. A surge that destroys a PLC and two drive control boards costs more than the SPD by orders of magnitude, and the outage costs more again.

**Type 1+2.** Type 1 handles the partial lightning current associated with a direct or nearby strike on the incoming line; Type 2 handles switching and induced transients. A combined 1+2 at the origin of the installation is the normal arrangement where overhead supply is present.

**Why it is on its own dedicated protective device.** An SPD at end of life fails, and it is designed to fail. If it is connected without its own protection, its failure takes out the incomer and the whole board with it. Its own device means the SPD disconnects and the board keeps running, degraded.

**Why the status contact goes to the PLC.** A failed SPD is invisible. Without monitoring, the first anyone knows is the next storm, when there is no protection. One digital input buys you that knowledge.

**To confirm:** SPD selection should be coordinated with the site's lightning protection assessment (AS/NZS 1768) and the confirmed earthing arrangement. Connecting lead length matters a great deal to SPD performance and is an installation detail, not just a selection detail.

---

### 2.3.4 Power meter PM-01 and current transformers

**Why it exists.**
- Energy accounting — pumping is usually the largest energy cost at a water site, and the utility will want kWh per megalitre.
- **Load verification after commissioning** — is the board actually loaded the way the design assumed?
- Power quality logging — voltage, current, power factor, and enough harmonic indication to tell you whether the harmonic question (TQ-006) needs escalating.
- Fault diagnosis — min/max and demand logging after an event.

**CTs 600/5.** Ratio chosen against the 630 A incomer. CT **class and burden** matter: a metering-class CT (0.5 or 0.5S) is required for revenue-grade accuracy, and the burden must account for the meter plus the lead length. A protection-class CT has different requirements entirely and is not interchangeable.

**The safety point.** A CT secondary must **never** be open-circuited while the primary is energised — the CT will develop a dangerously high secondary voltage. That is why shorting links are fitted on CT terminals and why CT terminals get a specific label. This gets verified at FAT and it is a genuine safety item, not a formality.

**To confirm:** whether the client requires revenue-grade metering (which may bring in National Measurement Institute pattern approval requirements), or whether this is operational metering only. Different answer, different meter, different CT class.

---

### 2.3.5 Phase failure / phase sequence relay

**Why it exists.** Two distinct failure modes:
- **Single-phasing.** Loss of one phase on a running three-phase motor causes the remaining two phases to carry substantially more current. Thermal overloads may or may not catch it in time depending on loading. On a 75 kW motor, a burnt-out winding is a long outage and a large bill.
- **Phase rotation.** Reversed rotation on a centrifugal pump means it turns backwards, produces almost no flow, and can damage the pump. This matters most **after a site supply change** — a transformer replacement or a network switching operation can reverse rotation without anybody noticing until a pump is started.

**How it is used.** The relay's healthy contact is a permissive in the control system and a monitored digital input. It does not trip the incomer; it prevents starts and raises an alarm.

**Caveat worth knowing.** On the VSD feeders, the drive already detects input phase loss and protects itself, and the drive output is regenerated so motor rotation is set by the drive's phase order, not the incoming supply. So the phase sequence function mainly protects the **DOL** feeders and gives a station-wide supply-health indication. Knowing that the relay is doing less for the VSD feeders than for the DOL ones is exactly the kind of detail that separates understanding from recitation.

---

### 2.3.6 Busbar system

**Why it exists.** Distributes the incoming supply to every feeder with a known, verified current rating and a known short-circuit withstand.

**Specification.**
- 800 A continuous, tinned copper, 3 phases + full-size neutral.
- Separate main earth bar (not a busbar phase) running the length of the board.
- Short-time withstand current (**Icw**) and peak withstand (**Ipk**) to match the confirmed fault level, with the bracing designed for the resulting mechanical forces.

**Why 800 A when the incomer is 630 A.** The busbar is rated above the incomer so the incomer is always the limiting device, the board tolerates future load growth into the spare feeders, and there is thermal margin at the top of the board where the cubicles are hottest. Busbar is cheap relative to the cost of being wrong.

**Why the neutral is full size, not half size.** Non-linear loads — and two six-pulse drives, plus switch-mode power supplies, plus any single-phase electronic load — generate triplen (3rd, 9th, 15th) harmonic currents. Triplen currents in a three-phase four-wire system **do not cancel in the neutral; they add.** A reduced-size neutral on a harmonic-rich board can overheat while every phase reads comfortably within rating. This is a genuinely common and genuinely dangerous error.

**Design verification is the manufacturer's, not mine.** Temperature rise verification, short-circuit withstand verification and the mechanical bracing design all sit with the assembly manufacturer under AS/NZS 61439.1. As PE, what I do is **ask for the evidence** — the manufacturer's design verification documentation for this enclosure system, this busbar arrangement and this form of separation — and put it in the MDR. I do not calculate it and I do not certify it.

**What must be confirmed:** the fault level (again — everything comes back to it), and the client's form of separation requirement, because Form 4b changes the busbar chamber construction.

---

### 2.3.7 VSD feeders — Q11 / VSD-101 / P-101 (and the identical Q12 / VSD-102 / P-102)

This is the most important block on the drawing and the one you will be asked about.

```
 Busbar
   │
  [Q11]  250 A MCCB  ── isolation + cable/drive short-circuit protection
   │
  [line reactor]  ── provisional, harmonic / dv/dt mitigation
   │
  [VSD-101]  Danfoss VLT AQUA FC202, 75 kW, 415 V
   │         · integrated EMC filter
   │         · DC link chokes
   │         · STO terminals ← from safety relay (dual channel)
   │         · motor thermal model
   │
  [EMC gland / 360° screen termination]
   │
   │  screened VSD motor cable, screen earthed BOTH ends
   │
  (M)  P-101, 75 kW, with PTC thermistors → thermistor relay KT101
```

**Why an MCCB and not an MPCB or fuses.**
The device in a VSD feeder is protecting **the cable and the drive's input**, not the motor. It is selected per the **drive manufacturer's recommendation**, which is published in the drive manual as a recommended fuse or circuit breaker type and rating. This is not optional guidance — many drives require semiconductor-rated (aR/gR) fuses to achieve their declared short-circuit current rating, and fitting a standard MCCB instead can invalidate the drive's SCCR.

**Say this clearly if asked:** *"On a VSD feeder, the upstream breaker doesn't protect the motor. The drive protects the motor — electronic thermal model plus, on a machine this size, an independent thermistor relay. The breaker protects the cable and the drive input, and I'd select it from the drive manual, not from motor FLC."*

**Why 250 A frame.** Provisional, against a 75 kW drive whose input current is in the region of the motor FLC. **Must be confirmed against the drive manual and the confirmed motor data.** Note the drive's input current is not the same as the motor's full-load current — it depends on the DC link arrangement and whether a line reactor or choke is fitted.

**Why an independent PTC thermistor relay when the drive has a thermal model.**
A drive's electronic overload is a *model*. It infers winding temperature from current, time and an assumed thermal time constant. It does not know that the motor's cooling fan has failed, or that the pump hall ventilation is blocked, or that the motor has been running at low speed where a TEFC motor's shaft-mounted fan delivers much less cooling than the model assumes. Embedded PTC thermistors measure the actual winding temperature. On a 75 kW pump motor with a long lead time, the extra relay is cheap insurance.

**Why the line reactor is marked provisional.** It serves two possible purposes — reducing input current harmonic distortion, and limiting dv/dt on long motor cables. Whether it is needed, and whether it is sufficient, depends on:
- the harmonic assessment (**TQ-006**), which may instead call for an active harmonic filter or a low-harmonic drive — either of which is a bigger, more expensive, longer-lead item that may need its own cubicle;
- the **actual motor cable route length**, which is not yet confirmed. Every drive manual states a maximum motor cable length, screened and unscreened. Exceed it and you get reflected wave voltage doubling at the motor terminals, which degrades winding insulation over time and eventually fails it. Above the limit you need an output dv/dt filter or a sine filter.

Carrying it as "provisional, subject to the harmonic assessment and confirmed cable length" is the honest engineering position. Deleting it to save money before those are answered is how a board gets built twice.

**Why the motor cable screen is earthed at BOTH ends — and why instrument screens are not.**
This trips people up, so be precise:

| Cable type | Screen earthing | Why |
|---|---|---|
| **VSD motor cable** | **Both ends**, 360° via EMC glands | The screen's job is to provide a low-impedance return path for high-frequency common-mode current, keeping it out of the building steel, the earthing system and nearby instrument cables. A 360° termination at both ends is what makes that work. Earthing one end only defeats the purpose entirely. |
| **Analogue instrument cable (4–20 mA)** | **One end only**, at the MCC | The screen's job is electrostatic shielding of a low-level signal. Earthing both ends creates an earth loop; any potential difference between the two earth points drives circulating current through the screen, which couples noise into the signal pair — exactly what you were trying to prevent. |

Two different problems, two different solutions, and a common source of "why is my level reading jumping around" at commissioning.

**Safe Torque Off wiring.** The safety relay's dual outputs drive the drive's STO inputs directly. This is what makes the E-stop act on the drive rather than just dropping a run command.

**Say this and you will be remembered:** *"STO removes torque. It does not isolate. The motor terminals can still be live after an E-stop, so STO is not an isolation method and doesn't replace the lockable isolator at the motor."*

**What must be confirmed before the drive is ordered:**
1. Motor nameplate data — kW, voltage, FLC, efficiency, power factor, insulation class, thermistor type (**the schedule-critical one**).
2. Actual motor cable route length and type.
3. Harmonic assessment outcome.
4. Confirmed fault level (drive SCCR and required upstream device).
5. Client's drive brand standard, if any.
6. Whether an output filter is required.
7. Drive configuration type code — enclosure type, EMC filter class, brake option, control card, keypad, coating.

> That last point is worth understanding. A drive is not a single catalogue number; it is a configured type code. Ordering "a 75 kW FC202" without specifying the enclosure type, filter class and options gets you a drive that may not fit the cubicle or meet the EMC class. Checking the type code against the specification is a BOM review task and it is genuinely the PE's.

---

### 2.3.8 DOL feeders — sump pump P-103, compressor C-101

```
 Busbar
   │
  [MPCB]  Motor protection circuit breaker
   │      · magnetic element: short-circuit protection
   │      · thermal element: adjustable overload, set to motor FLC
   │      · isolation, lockable
   │
  [KM]   Contactor, 24 V DC coil, AC-3 rated
   │
  (M)    P-103, 4 kW
```

**Why MPCB + contactor rather than MCCB + contactor + separate thermal overload.**
Fewer devices, less internal wiring, less to get wrong, less panel space, one adjustment instead of two. The MPCB combines short-circuit and thermal overload protection in one device with a single current setting.

**The trade-off you should acknowledge:** a separate thermal overload relay can be easier to source and replace in some regions, and gives more flexibility in mixing device brands. MPCBs also have a defined **type of coordination** with the specific contactor they are paired with — Type 1 (damage permitted, device must be replaced after a short circuit) or Type 2 (no damage beyond light contact welding, device is serviceable). **You must select the MPCB/contactor pair from the manufacturer's published coordination tables**, not just match current ratings. Mixing brands breaks the coordination declaration.

**Why AC-3 rated contactors.** AC-3 is the utilisation category for squirrel-cage motor starting and stopping while running — it accounts for the contactor making against locked-rotor current (typically 6–8× FLC). AC-1 ratings are for non-inductive loads and are much higher for the same contactor. Sizing a contactor on its AC-1 rating for a motor load is a classic and destructive error.

**Why 24 V DC coils.** Consistent with the control voltage decision (§1.5). The trade-off is coil inrush on the DC system, which is why the PSUs are sized with margin.

---

### 2.3.9 MOV-101 — motorised valve actuator feeder

**Why it is just a feeder.** The actuator (a packaged unit from the valve vendor) contains its own reversing starter, torque and limit switches, and local controls. Our scope is a protected supply and a control/status interface.

**Why this interface is a classic trap.** Actuator control interfaces vary enormously: hardwired open/close/stop with position feedback; a 4–20 mA position demand and retransmit; or a fieldbus interface. Which one you get determines how many I/O points and terminals you need. **Getting the actuator wiring diagram before the schematics are drafted is a PE task**, and if the vendor is slow, the schematic gets drafted twice. This is exactly the kind of interface that quietly consumes two weeks.

---

### 2.3.10 PKG-201 — chemical dosing skid feeder

**Why supply-only.** The skid is a vendor package with its own internal controls and its own compliance documentation. Our boundary is a protected supply to the skid's isolator.

**What must be confirmed:** the skid's declared full-load current, starting current, whether it needs a neutral, its earthing requirements, and its control interface (typically a handful of status and permissive signals). The declared 16 A is from the vendor's preliminary data sheet and must be confirmed against the final data sheet before the feeder is finalised.

**And one to actually ask about:** the skid is a *chemical dosing* skid. Is any part of its area hazardous-area classified? Sodium hypochlorite is not, but some coagulants and some storage arrangements can attract classification. If it is, nothing in our board changes — but the field wiring and the equipment at the skid does, and it is not a question to leave unasked. **Almost certainly no here, but asking it is the behaviour.**

---

### 2.3.11 DB-01 feeder — light and power distribution board

**Why it exists.** Switchroom and pump hall lighting, general power outlets, small services. It is a sub-board, not our supply.

**Why 80 A.** Against a 63 A design figure with headroom. The actual size comes from the DB's own maximum demand calculation to AS/NZS 3000 Clause 2.2, which is the responsibility of whoever designs DB-01 — not us. We carry a feeder and a stated rating and we ask them to confirm it.

**RCD strategy** for the socket outlet circuits sits at DB-01, not at our feeder. Worth confirming that it does, so nobody assumes we provided it.

---

### 2.3.12 Control and UPS feeders

Small feeders serving:
- UPS-01 → PSU-1 and PSU-2 → 24 V DC system → PLC, I/O, network switch, safety relay, indication.
- Cubicle services: internal lighting with door switches, GPO for a laptop at FAT and at site, anti-condensation heaters via hygrostat.

**Why the UPS.** Two reasons that are often conflated:
1. **Ride-through** — a brief supply dip should not reboot the PLC and lose the plant's state.
2. **Alarm on the way down** — on a genuine supply failure, the PLC stays alive long enough to report to SCADA that the station has lost power. Without that, the site just goes silent and the operator has to work out why.

**Why the anti-condensation heaters, in an air-conditioned room.** Because the air conditioning will fail at some point, the room will cool overnight, and condensation on busbars and electronics is a slow, expensive failure. Hygrostat-controlled heaters are cheap insurance. They are also a heat source that has to be counted in the thermal design.

---

### 2.3.13 Spare feeders

Two fitted, wired and labelled spare feeders — 63 A MCCB and 32 A MCCB — each wired out to terminals with a gland plate provision.

**Why fitted-and-wired and not just spare chassis space.** Adding a feeder to a live MCC later means an outage, a hot-work or isolation permit, and a licensed electrician working in an energised board. Fitting it at build time costs a few hundred dollars. Adding it later costs a shutdown. That is a cost-awareness argument a manager will recognise immediately.

**Plus 20 % spare chassis space** for feeders that are not yet conceived of. This is the provision clients most often fail to specify and most often want later.

---

### 2.3.14 Earthing arrangement

| Element | Arrangement | Why |
|---|---|---|
| Main earth bar (MEB) | Tinned copper, full length of the board, accessible | Single reference point, verifiable continuity |
| Cubicle earth bars | One per cubicle, bonded to the MEB | Short, low-impedance path for every device |
| Door bonding | Flexible green/yellow strap on every door carrying equipment | A door with a pilot light on it is an exposed conductive part. Hinges are not a reliable earth path. |
| Gland plates | Bonded to the cubicle earth | The plate is an exposed conductive part and is part of the screen path |
| Equipment earths | Every device with an exposed conductive part bonded | |
| **Instrument screen earth bar** | **Separate bar**, single-point bonded to the MEB | Keeps instrument screen currents off the general protective earth, and gives one defined single-point earth so screens are not accidentally earthed at both ends |
| VSD motor cable screens | 360° EMC glands, both ends | High-frequency return path — see §2.3.7 |
| PE / N separation | Separate neutral bar and earth bar, bonded only at the origin of the installation | TN-S. Assumed — **TQ-001** |

**Testing at FAT.** Earth continuity from the MEB to every door, gland plate, cubicle earth bar and equipment earth, at a defined test current. A visual inspection is not a test.

---

## 2.4 Feeder schedule (as shown on the SLD)

| Ref | Feeder | Protective device (provisional) | Starter | Load | Cable interface | Notes |
|---|---|---|---|---|---|---|
| Q1 | Incomer | 630 A 4P MCCB, electronic trip | — | — | Busbar links | Icu against confirmed PSCC |
| Q11 | VSD-101 / P-101 | 250 A MCCB (per drive manual) | VSD 75 kW | 75 kW | Screened VSD cable, EMC gland | Line reactor provisional |
| Q12 | VSD-102 / P-102 | 250 A MCCB (per drive manual) | VSD 75 kW | 75 kW | Screened VSD cable, EMC gland | Line reactor provisional |
| Q13 | DB-01 | 80 A MCCB | — | Sub-board | 4C multicore | Sub-board MD is DB-01 designer's |
| Q14 | PKG-201 dosing skid | 32 A MCCB | — | Vendor skid | 4C multicore | Supply only to skid isolator |
| Q15 | P-103 sump pump | MPCB 6.3–10 A | Contactor, AC-3 | 4 kW | 4C multicore | Auto on float |
| Q16 | C-101 compressor | MPCB 9–14 A | Contactor, AC-3 | 5.5 kW | 4C multicore | Auto on pressure switch |
| Q17 | MOV-101 | MPCB 1.6–2.5 A | Vendor integral | 0.75 kW | Multicore + control | Actuator interface **TBC** |
| Q18 | HVAC-01 | 20 A 3P MCB | — | Vendor unit | 4C multicore | Fault status to PLC |
| Q19 | UPS-01 / control | 10 A 1P MCB | — | Control system | Internal | Feeds PSU-1 / PSU-2 |
| Q20 | Cubicle services | 16 A 1P MCB | — | Lighting, GPO, heaters | Internal | |
| Q21 | **SPARE** | 63 A MCCB | — | — | Wired to terminals | Fitted spare |
| Q22 | **SPARE** | 32 A MCCB | — | — | Wired to terminals | Fitted spare |

**All device ratings above are provisional** pending confirmed fault level, confirmed motor data and the coordination study. See `00-CLAIM-INTEGRITY.md`.

---

## 2.5 How the SLD is checked before it is issued

The PE does not draft the SLD. The PE checks it. This is the check list actually used:

| # | Check | What "failed" looks like |
|---|---|---|
| 1 | Every load in the connected load schedule has a feeder, and every feeder has a load | A feeder on the drawing that nobody can name — usually a leftover from a previous revision |
| 2 | Every device has a unique tag, and the tags match the schematic sheets and the BOM | Q15 on the SLD, Q16 on the schematic |
| 3 | Ratings are self-consistent up the chain: feeder device < busbar < incomer | A 100 A feeder on an 800 A busbar with a 63 A incomer |
| 4 | Fault rating shown, and the same value appears on every device's spec | Icu stated on the incomer, missing on the feeders |
| 5 | Neutral is shown, and shown as full-size | Neutral drawn as a dotted afterthought |
| 6 | Earth bar shown, and shown as separate from neutral | Earth and neutral shown as one bar in a TN-S system |
| 7 | Every cable interface is a labelled terminal or link with a cable number | Motor drawn connected straight to the drive with no boundary |
| 8 | Isolation is achievable for every load without de-energising others | Two motors on one isolating device |
| 9 | CT ratio and class stated; CT shorting arrangement noted | CT with no ratio, or a protection CT used for metering |
| 10 | Spare feeders shown, labelled SPARE, with their rating | Spares shown but not rated, so nobody knows what they can be used for |
| 11 | Drawing references to schematic sheets are present and correct | SLD points to SCH-0102, which does not exist |
| 12 | Revision block matches the revision in the drawing register | The classic — a Rev C drawing in a Rev B transmittal |
| 13 | Assumptions annotated on the drawing, not just in the design basis | The fabricator builds to the drawing and never reads the design basis |

> **Item 13 is the one that matters most in practice.** If the fault level is an assumption, it belongs in a note on the SLD, because the drawing is what the workshop, the client and the checker actually look at. Assumptions buried in a design basis nobody opens are not managed assumptions.

---

## 2.6 What the Project Engineer did at Stage 2

1. Gave the designer a written, complete brief: the design basis, the confirmed inputs, and an explicit list of what must **not** be drafted yet (general arrangement, pending cable entry direction).
2. Reviewed the Rev A SLD against the check list above and marked it up.
3. Caught that the drafted SLD showed a half-size neutral (drawn from a previous project template) and had it changed — with the harmonic reasoning recorded, so the next person does not reverse it.
4. Required every provisional rating to be annotated as provisional **on the drawing face**.
5. Chased the missing motor data and escalated the schedule risk in writing.
6. Issued the SLD for client approval at Rev C, with the open assumptions listed in the transmittal, so the client approval was against a known set of assumptions rather than a silent one.

> **Point 6 is a real PE skill.** If a client approves a drawing without being told what it assumes, you have not transferred the risk; you have hidden it. The transmittal note is what makes the approval meaningful.

---

**Next:** [Stage 3 — Schematics](03-SCHEMATICS.md)
