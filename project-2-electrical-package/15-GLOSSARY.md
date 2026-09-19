# 15 — GLOSSARY

Every term and abbreviation used across this package, in plain English, with **why it matters here**.

Use it two ways: as a decoder while you read, and as a self-test — cover the right-hand columns and see how many you can define out loud.

> **Terms marked ⚠ are ones people routinely use wrongly.** Those are the ones worth being precise about.

---

## Abbreviations, quick decode

| | | | |
|---|---|---|---|
| **AC-1 / AC-3** | Contactor utilisation categories | **MCB** | Miniature circuit breaker |
| **BOM** | Bill of materials | **MCC** | Motor control centre |
| **CT** | Current transformer | **MCCB** | Moulded case circuit breaker |
| **DI / DO** | Digital input / output | **MDR** | Manufacturer's data record |
| **AI / AO** | Analogue input / output | **MEB** | Main earth bar |
| **DOL** | Direct on line | **MPCB** | Motor protection circuit breaker |
| **EMC** | Electromagnetic compatibility | **NPSH** | Net positive suction head |
| **FAT** | Factory acceptance test | **PE** | Protective earth |
| **FLC** | Full load current | **PL / PLr** | Performance Level / required PL |
| **GA** | General arrangement | **PLC** | Programmable logic controller |
| **GPO** | General purpose outlet (power point) | **PSCC** | Prospective short-circuit current |
| **HMI** | Human machine interface | **PWM** | Pulse width modulation |
| **IFC** | Issued for construction | **SAT** | Site acceptance test |
| **IGBT** | Insulated gate bipolar transistor | **SCADA** | Supervisory control and data acquisition |
| **IP** | Ingress protection | **SCCR** | Short-circuit current rating |
| **LCS** | Local control station | **SPD** | Surge protective device |
| **L/O/R** | Local / Off / Remote | **STO** | Safe Torque Off |
| **Icu / Ics / Icw** | Breaking and withstand ratings | **TEFC** | Totally enclosed fan cooled |
| **RIO** | Remote I/O | **TQ** | Technical query |
| **THDi / THDv** | Total harmonic distortion, current / voltage | **VSD** | Variable speed drive |

---

## A

**AC-1** — Contactor utilisation category for non-inductive or slightly inductive loads. Gives a *much higher* current rating than AC-3 for the same contactor.
⚠ *Why it matters:* sizing a motor contactor on its AC-1 rating is a classic destructive error. Motors need AC-3.

**AC-3** — Contactor utilisation category for starting and switching off a running squirrel-cage motor. Accounts for making against locked-rotor current (6–8× FLC).
*Why it matters:* this is the rating that applies to every motor contactor in the package.

**Active harmonic filter** — A device that measures harmonic current and injects an equal, opposite current to cancel it. The most effective mitigation, the most expensive, needs its own cubicle and a long lead.
*Why it matters:* it is the cost and schedule risk carried in TQ-006.

**Affinity laws** — For a given pump: flow ∝ speed, head ∝ speed², **power ∝ speed³**.
*Why it matters:* the cube relationship is the entire business case for variable speed pumping. 80 % speed ≈ 51 % power. See `14-CORE-CONCEPTS.md` §5 — including the caveat about static head.

**Arc flash** — The explosive release of energy from an arcing fault. Studies (IEEE 1584) calculate incident energy to determine PPE and labelling.
*Why it matters:* excluded from this package as client scope. Never claim to have done one.

**As-built** — Drawings revised to reflect what was *actually* built and tested, not what was designed.
⚠ *Why it matters:* a transcribed as-built nobody physically verified is worse than none — it looks authoritative and is fiction.

**AS/NZS 3000** — The Wiring Rules. Governs electrical *installations*.
*Why it matters:* applies to the interfaces around this board, not to the assembly itself.

**AS/NZS 3008.1.1** — Cable selection standard: current-carrying capacity, derating, volt drop.
*Why it matters:* every cable size in this package is a provisional placeholder because no calculation to this standard has been done.

**AS/NZS 61439** — The standard for low-voltage switchgear and controlgear assemblies. Part 1 general rules, Part 2 power switchgear assemblies (this MCC).
⚠ *Why it matters:* it puts **design verification** on the *original manufacturer*, not the designer or the client. Knowing that is a competency.

**AS 60204.1** — Safety of machinery, electrical equipment of machines. Source of the wire colour convention and stop categories.

**AS 4024.1** — Safety of machinery series. Where required Performance Level comes from.

---

## B

**Busbar** — Solid copper conductors distributing the incoming supply along the board.
*Why it matters:* 800 A here, with a **full-size neutral** (see *triplen*), rated for both continuous current and short-circuit withstand.

**Burden** — The total resistance in a 4–20 mA loop that the transmitter must drive.
*Why it matters:* too much burden and the transmitter runs out of compliance voltage and the loop goes non-linear at the top of range.

---

## C

**Cascade (back-up protection)** — Using an upstream device's fault-limiting to allow a downstream device to be applied above its own standalone Icu.
⚠ *Why it matters:* only valid for **manufacturer-tested combinations from published tables**. Never derive it yourself.

**Cavitation** — Liquid boiling at the impeller eye because local pressure fell below vapour pressure; the bubbles implode and pit the metal.
*Why it matters:* NPSH available must exceed NPSH required. It is a hydraulic design responsibility, not yours — but know what it is.

**Compliance voltage** — The minimum voltage a 4–20 mA transmitter needs across its own terminals to work.

**Contactor** — An electrically-operated switch for frequent, remote switching of a load.
⚠ *Why it matters:* **a contactor is not an isolator.** Small contact gap, can weld closed, can be re-energised remotely. Never a means of isolation.

**CT (current transformer)** — Steps high primary current down to a small secondary current (5 A here) for metering or protection.
⚠ *Why it matters:* **never open-circuit a CT secondary while the primary is energised** — dangerous voltages develop. Hence shorting links and a specific warning label.

---

## D

**dv/dt** — Rate of change of voltage. High dv/dt from PWM switching is what drives common-mode current and stresses motor insulation.

**DC link** — The smoothed DC bus between a drive's rectifier and inverter, typically 560–580 V DC on a 415 V supply.
⚠ *Why it matters:* it stays charged for minutes after power removal. This is part of why STO is not isolation.

**Design verification** — Proving an assembly design meets AS/NZS 61439 (temperature rise, short-circuit withstand, IP, clearances) by testing, comparison or assessment.
⚠ *Why it matters:* **the manufacturer's responsibility.** The PE's job is to obtain the evidence for the MDR.

**Deviation** — Something that *cannot* be completed for reasons outside your scope, recorded with client acceptance.
⚠ *Why it matters:* different from a defect (something you got wrong). FD-005 — unverified protection settings — is a deviation, and recording it as a pass would have been dishonest.

**Discrimination (selectivity)** — Arranging protection so the device *nearest* a fault clears it, and nothing upstream trips.
*Why it matters:* without it, a feeder fault blacks out the whole station. Unverified in this package — TQ-004.

**Duty / standby / assist** — Duty runs; standby takes over on failure; assist starts *in addition* when the duty pump alone cannot meet demand.

**Duty point** — Where the pump curve and the system curve intersect: the flow and head the pump actually delivers in that system.
*Why it matters:* re-modelling moved it, which is what triggered CR-001 and the 75 → 90 kW uprate.

---

## E

**Earth fault loop impedance (Z_s)** — Total impedance of the path a fault current takes back to the source.
*Why it matters:* too high and not enough fault current flows, so the breaker takes too long to disconnect. It is why an earth bolted through powder coat is a safety defect.

**Earth loop** — An unintended circuit formed by earthing a cable screen at two points at different potentials; circulating current couples noise into the signal.
*Why it matters:* the reason instrument screens are earthed at the MCC end **only**.

**ECP (electronic circuit protector)** — A DC-rated protective device with an adjustable trip and a status contact.
⚠ *Why it matters:* standard AC MCBs must **not** be used on DC — DC has no natural current zero, so the arc does not self-extinguish.

**EMC gland** — A cable gland giving 360° contact with a cable screen.
*Why it matters:* a pigtail is an inductor at PWM frequencies and largely defeats the screen.

---

## F

**Fail-safe wiring** — Wiring critical signals normally closed so a broken wire reads as a *fault*, not as *healthy*.
*Why it matters:* it is safety achieved by wiring, not by trusting code. FAT test K-83 proves it.

**Form of separation** — How much internal barriering an assembly has (Forms 1 to 4b). This package is Form 3b.
*Why it matters:* determines how safely you can work on one section with the rest live. See `14-CORE-CONCEPTS.md` §13.

**Functional description** — The plain-English statement of what the plant does, agreed before schematics are drafted.
*Why it matters:* schematics drafted from a verbal brief get drafted twice.

---

## H

**Harmonics** — Current or voltage components at integer multiples of the fundamental, produced by non-linear loads.
⚠ *Why it matters:* a six-pulse drive produces **6k ± 1** (5th, 7th, 11th, 13th). It does **not** produce significant triplens. See *triplen*.

**Hygrostat** — Humidity-operated switch controlling anti-condensation heaters.

---

## I

**Icu** — Ultimate breaking capacity: the maximum fault current a breaker can interrupt.
**Ics** — Service breaking capacity: what it can interrupt *and remain serviceable* afterwards.
**Icw** — Short-time withstand current: what a busbar or device can carry for a stated time without damage.
**Ipk** — Peak withstand, which sets the *mechanical* forces on busbar bracing.
*Why they matter:* all four depend on the fault level, which is the biggest open assumption in the package.

**IFC (Issued for Construction)** — A drawing revision status. Number revisions (0, 1, 2…) are IFC; letters (A, B, C…) are preliminary.
⚠ *Why it matters:* **nothing is ever built from a letter revision.**

**IGBT** — The fast switching transistor in a drive's inverter stage.
*Why it matters:* STO works by removing the gate drive to these.

**Interposing relay** — A relay between a PLC output and the field device.
*Why it matters:* protects the module, gives a volt-free contact and a visible test point. Costs space and speed.

**Isolator / switch-disconnector** — A device providing a verified, lockable contact gap so equipment can be worked on safely.
⚠ *Why it matters:* this is the thing STO and a contactor are **not**.

---

## L

**Live zero** — Using 4 mA rather than 0 mA as the bottom of an analogue range.
*Why it matters:* a healthy loop never reads 0 mA, so 0 mA means a broken wire — a condition you can detect and alarm. With 0–20 mA you cannot tell a fault from a legitimate zero.

**Locked rotor current** — The current drawn at standstill, typically 6–8× FLC, because the rotor is effectively a short-circuited transformer secondary.
*Why it matters:* it is why AC-3 ratings exist and why large motors aren't started DOL on weak supplies.

---

## M

**MPCB** — Combines short-circuit protection and adjustable thermal overload in one device.
*Why it matters:* fewer parts, less wiring, one setting. Must be paired with its contactor from the manufacturer's **coordination tables**.

**Maximum demand** — The realistic peak load, after diversity, used to size supply equipment.
⚠ *Why it matters:* the ~447 A figure in this package is an *estimate for frame selection*, not a maximum demand calculation to AS/NZS 3000 Clause 2.2.

---

## N

**NPSH** — Net positive suction head. NPSH *available* (from the system) must exceed NPSH *required* (from the pump), with margin, or you get cavitation.

---

## P

**Performance Level (PL)** — A measure of a safety function's reliability, a to e, under ISO 13849-1. **PLr** is the *required* level, from a risk assessment; the *achieved* level comes from a calculation.
⚠ *Why it matters:* this package's E-stop is "the architecture normally built for PLd, **pending verification**". Calling it PLd without both pieces is a false claim.

**Permissive** — A condition that must be true before a start is allowed (distinct from a *trip*, which stops something already running).

**PWM** — Switching a DC bus on and off rapidly to synthesise a variable AC output.
*Why it matters:* it is the mechanism behind high dv/dt, screened motor cables and the reflected-wave problem.

**PSCC** — Prospective short-circuit current: the fault current available at a point.
⚠ *Why it matters:* **25 kA is an assumption in this package.** Every breaker rating and the busbar withstand hang off it.

---

## R

**Reflected wave** — A PWM voltage edge reflecting at the motor terminals, potentially doubling the terminal voltage and degrading insulation.
*Why it matters:* it sets the maximum motor cable length in every drive manual.

**Rectifier** — The six-diode bridge converting AC to DC at a drive's input.
*Why it matters:* it draws current in pulses, which *is* the harmonic distortion.

---

## S

**SCCR** — Short-circuit current rating: the maximum fault current a device is rated to be connected to, when protected as specified.
⚠ *Why it matters:* many drives require a specific fuse or breaker type to achieve their declared SCCR. Substituting one can invalidate it.

**Slip** — The difference between synchronous speed and actual rotor speed, as a fraction.
*Why it matters:* an induction motor produces torque *only* because it slips.

**STO (Safe Torque Off)** — A drive safety function that removes the gate drive signals to the output transistors, so no torque can be produced.
⚠ *Why it matters:* **STO removes torque; it does not isolate.** The DC link stays charged and the motor terminals stay connected to it. It is not a substitute for a lockable isolator. This is the single most important distinction in the package.

**Stop category** — Cat 0: immediate removal of power. Cat 1: controlled stop, then power removed. Cat 2: controlled stop, power maintained.
*Why it matters:* Cat 0 is drawn here, but Cat 1 may be preferable to limit hydraulic surge on a 90 kW pump. Unresolved — TQ-003.

**Synchronous speed** — The speed of the stator's rotating field: `N_s = 120 f / p`. 1500 rpm for a 4-pole machine at 50 Hz.

---

## T

**THDi / THDv** — Total harmonic distortion of current / of voltage.
*Why it matters:* your load produces THDi; everyone on the network experiences THDv, created by THDi flowing through the source impedance. That is why a harmonic assessment needs network data.

**Thermistor (PTC)** — A temperature-sensitive resistor embedded in the motor windings.
*Why it matters:* it *measures* winding temperature. A drive's thermal model only *infers* it, and cannot know the cooling fan has failed.

**Traffolyte** — Engraved laminated plastic labelling, mechanically fixed.
*Why it matters:* adhesive labels fall off in heat. In ten years they are on the floor of the cubicle.

**Transmittal** — The formal record accompanying a document issue, listing number, revision, status and date.
*Why it matters:* no transmittal, no issue. It is how you prove the integrator had the current revision.

**Triplen harmonics** — The 3rd, 9th, 15th. They are **zero-sequence**: all three phases' triplens are in phase with each other, so they **add** in the neutral instead of cancelling.
⚠ *Why it matters:* this is why the neutral is full size — **and the source is single-phase electronic load (switch-mode supplies, UPS input, lighting and GPO circuits), not the six-pulse drives.** Getting that backwards is a common error.

**Type 1 / Type 2 coordination** — After a short circuit, Type 1 permits damage to the starter; Type 2 permits none beyond light contact welding.
⚠ *Why it matters:* selected from the manufacturer's **tested pairs**, not by matching current ratings. Mixing brands voids the declaration.

---

## U

**UPS** — Uninterruptible power supply.
*Why it matters:* two jobs here — ride through a dip so the PLC doesn't reboot, **and** stay alive long enough on a real outage to tell SCADA the station has lost power.

---

## V

**V/f** — Varying voltage in proportion to frequency to keep motor flux roughly constant.
*Why it matters:* it is why a drive can deliver full torque at low speed.

**Volt-free contact** — A dry contact with no voltage of its own; the receiving device supplies the voltage.
*Why it matters:* preferred from field devices because it avoids importing a foreign voltage into the board.

---

## Terms that sound similar and are not

| These get confused | The actual difference |
|---|---|
| **Isolation** vs **STO** vs **stopping** | Isolation = verified, lockable disconnection. STO = no torque, still connected. Stopping = not running, could restart. |
| **Icu** vs **Ics** | Icu: can it break the fault. Ics: can it break it and still be usable afterwards. |
| **Discrimination** vs **cascade** | Discrimination: only the nearest device trips. Cascade: upstream device helps downstream survive a fault above its own rating. They pull in opposite directions. |
| **Defect** vs **deviation** | Defect: we got it wrong. Deviation: it can't be completed for reasons outside our scope. |
| **kW** vs **kVA** | kW does work. kVA is what the supply has to carry. |
| **Permissive** vs **trip** | Permissive prevents a start. Trip stops something already running. |
| **THDi** vs **THDv** | You produce THDi. The network experiences THDv. |
| **Protective earth** vs **screen** | PE is a safety conductor, always both ends. A screen is an EMC/signal measure, and which end depends on the problem. |
| **Form 3b** vs **Form 4b** | 3b: terminals separated from busbars. 4b: terminals also in their own compartments. |
| **NPSHa** vs **NPSHr** | Available (from your system) must exceed required (from the pump). |

---

**Next:** [The story of a start command](16-START-COMMAND-TRACE.md)
