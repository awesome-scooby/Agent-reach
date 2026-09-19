# STAGE 1 — DESIGN BASIS

**Document:** NFD-ELE-DBS-0001
**Project:** Northfield WTP — Raw Water Transfer Pump Station Upgrade
**Package:** MCC-01, Field Control Stations, Remote I/O Kiosk RIO-01
**Revision:** C (Issued for Approval)

---

## 1.1 Why the design basis exists

Everything downstream is a consequence of this document. If the design basis is wrong or incomplete, the SLD is wrong, the BOM is wrong, and you find out in the workshop or at FAT when it costs ten times as much to fix.

The Project Engineer's job at this stage is not to write the design. It is to **make sure every input the designer needs is either confirmed, or visibly flagged as an assumption with an owner and a due date.** An unflagged assumption is the single most expensive thing in a package.

---

## 1.2 Scope

### In scope (our supply)

- Design, fabrication, wire, test and deliver **MCC-01**: floor-standing 415 V motor control centre, Form 3b, indoor.
- Two variable speed drive feeders for raw water transfer pumps P-101 / P-102 (75 kW each).
- Direct-on-line feeders for sump pump P-103, instrument air compressor C-101.
- Feeder for motorised isolation valve MOV-101 (actuator with integral starter).
- Feeder for vendor chemical dosing skid PKG-201 (supply only to the skid's isolator).
- Feeders for switchroom HVAC, light-and-power distribution board DB-01, and control/UPS.
- Spare feeders and spare chassis capacity (see §1.11).
- PLC, remote I/O node, 24 VDC power system, UPS, network switch, marshalling.
- **Field control stations** LCS-101 and LCS-102 (local control at each pump).
- **Remote I/O kiosk RIO-01** at the intake screen, supplied as a separate small enclosure.
- Factory Acceptance Test.
- Manufacturer's Data Record (MDR) and as-built drawings.

### Out of scope (explicitly excluded)

| Excluded | Whose scope |
|---|---|
| Site installation, positioning, plinth and fixing of MCC-01 | Installation contractor |
| All field cabling, glanding and termination at the field end | Installation contractor |
| Field termination into MCC-01 at site | Installation contractor (we supply terminals, they land cables) |
| Motors, pumps, local motor isolators | Mechanical package / pump vendor |
| Field instruments (supply) | Client free-issue — we terminate and test to terminals only |
| Chemical dosing skid internals | Vendor PKG-201 |
| PLC application software and SCADA configuration | Client's systems integrator |
| Site Acceptance Test and commissioning | Client / integrator — we provide attendance support only |
| Site earthing system design and installation | Client's civil/electrical designer |
| Arc flash incident energy study and labelling | Client specialist |
| Protection coordination study | Client specialist (see TQ-004) |
| Harmonic assessment against network limits | Client specialist (see TQ-006) |
| Machinery risk assessment and functional safety PL determination | Client / safety consultant (see TQ-003) |
| HV side of transformer TX-01 | Network operator |

**Why exclusions matter more than scope.** Scope creep in switchboard packages almost always enters through an undefined exclusion. If it is not written down as excluded, a client will reasonably assume it is included, and you will be arguing about it during FAT with no contractual position.

---

## 1.3 Electrical design parameters

| Parameter | Value | Status |
|---|---|---|
| Incoming supply | 415 V, 3-phase, 4-wire + earth, 50 Hz | **Confirmed** — client drawing NFD-CLI-SLD-9001 |
| Source | TX-01, 500 kVA, 11 kV / 415 V, Dyn11, Z = 5 % (nameplate) | **Confirmed** — nameplate photo on file |
| Earthing system | TN-S (separate neutral and protective earth throughout the MCC) | **Assumed** — TQ-001. Drives whether an earth-fault protection element is required and how the neutral bar is arranged. |
| Prospective short-circuit current at MCC incomer | **25 kA for 1 s — ASSUMPTION** | **OPEN — TQ-002.** Transformer-only contribution from nameplate is approximately 14 kA; 25 kA carries margin for motor contribution and any future transformer upsize. **Not a substitute for a study.** |
| Incomer rating | 630 A | Derived, see §1.4 |
| Busbar rating | 800 A continuous, Icw to match confirmed PSCC | Manufacturer to verify (AS/NZS 61439.1 design verification) |
| Main control voltage | 24 V DC | Design decision, §1.5 |
| Auxiliary AC voltage | 240 V AC, 1-phase (cubicle lighting, GPO, anti-condensation heaters, UPS input) | Design decision |
| System of protection for small feeders | Motor protection circuit breaker (MPCB) + contactor | Design decision, §1.6 |
| Form of separation | Form 3b to AS/NZS 61439.2 | **Assumed** — TQ-001 (client standard may require Form 4b) |
| Ingress protection | IP42 minimum, indoor air-conditioned switchroom | **Assumed** — TQ-001 |
| Enclosure colour | AS 2700 N42 Storm Grey, powder coat | **Assumed** — client standard to confirm |
| Ambient design temperature | 40 °C | **Assumed** — TQ-005, see §1.7 |
| Altitude | < 1000 m (no derating) | Assumed |
| Cable entry | Top entry, removable undrilled gland plates | **Assumed** — TQ-001. Bottom entry is common where there is a cable pit; this changes the whole cubicle layout, so it must be confirmed before general arrangement is drafted. |

> **Interview point.** Notice how many of the parameters that determine equipment selection are *assumptions*. That is completely normal at Rev A/B of a design basis. What is not normal, and what gets packages into trouble, is those assumptions still being open at the design freeze. The PE owns closing them out.

---

## 1.4 Connected load schedule

| Tag | Description | kW | Starting method | Est. FLC (A) | Feeder protection | Notes |
|---|---|---|---|---|---|---|
| P-101 | Raw water transfer pump 1 | 75 | VSD | ~135 | 250 A MCCB | Duty/assist with P-102 |
| P-102 | Raw water transfer pump 2 | 75 | VSD | ~135 | 250 A MCCB | Duty/assist with P-101 |
| P-103 | Switchroom / pit sump pump | 4.0 | DOL | ~8.5 | MPCB 6.3–10 A | Auto on float |
| C-101 | Instrument air compressor | 5.5 | DOL | ~11 | MPCB 9–14 A | Auto on pressure switch |
| MOV-101 | Motorised isolation valve actuator | 0.75 | Integral (vendor) | ~2.0 | MPCB 1.6–2.5 A | Actuator has its own reversing starter |
| PKG-201 | Chemical dosing skid | — | Vendor | 16 (declared) | 32 A MCCB | Supply to skid isolator only |
| HVAC-01 | Switchroom air conditioner | — | Vendor | 10 (declared) | 20 A MCB 3P | |
| DB-01 | Light & power distribution board | — | — | 63 (design) | 80 A MCCB | Sub-board, not our supply |
| UPS-01 | Control system UPS | — | — | 6 | 10 A MCB 1P | Feeds PLC/comms via PSUs |
| CTL | Control transformer / aux supply | — | — | 10 | 16 A MCB 1P | Cubicle lighting, GPOs, heaters |
| SPARE-1 | Spare feeder | — | — | — | 63 A MCCB | Fitted, wired to terminals |
| SPARE-2 | Spare feeder | — | — | — | 32 A MCCB | Fitted, wired to terminals |

**Estimated maximum demand:**

| Case | Calculation | Result |
|---|---|---|
| Both transfer pumps running (duty/assist) | 135 + 135 | 270 A |
| All other loads at declared current | 8.5 + 11 + 2 + 16 + 10 + 63 + 6 + 10 | 126.5 A |
| **Total, no diversity** | | **~397 A** |

Incomer selected at **630 A** frame. Basis: it covers the no-diversity case with margin, it is a standard frame size, and it leaves headroom for the spare feeders to be used later without replacing the incomer.

> **State this honestly.** The FLC values above are typical figures for 4-pole motors at 415 V. They are **not** confirmed. Actual full-load current comes off the motor nameplate, and the VSD's *input* current is what matters for the feeder, not the motor FLC — they differ. The demand figure above is an estimate for frame selection, not a maximum demand calculation to AS/NZS 3000 Clause 2.2. Confirm against pump vendor data before the design freeze.

---

## 1.5 Control voltage — the decision and the trade-off

**Decision: 24 V DC as the primary control voltage,** including contactor coils on the small feeders, with 240 V AC retained only for cubicle services (lighting, GPOs, anti-condensation heaters, UPS input).

| Reason for | Cost of it |
|---|---|
| One ELV control voltage through the whole board simplifies segregation from 415 V | 24 V DC coils draw more current than 240 V AC coils, so the DC system has to be sized for it |
| PLC I/O is 24 V DC anyway — no interposing between PLC and field for digital signals | Volt drop matters on long DC runs; fine inside a board, needs checking on the run to RIO-01 |
| Safer to work on live during fault finding and FAT | Standard AC-rated MCBs **must not** be used for DC circuits — DC breakers or electronic circuit protectors are required, and they cost more |
| Field control stations run at ELV, so E-stop and pushbutton wiring is not at 240 V | A single point of failure in the 24 V system takes out everything — hence redundant PSUs |

**24 V DC architecture:**

- UPS-01 (1 kVA online, ~15 min autonomy at load) feeds two independent 240 V AC MCBs.
- PSU-1 and PSU-2, each 24 V DC 20 A switch-mode, fed from those separate MCBs.
- Both PSUs into a redundancy (O-ring) module, so one PSU can fail without dropping the bus.
- Redundancy module output to a 24 V DC distribution bar, then out through **electronic circuit protectors** in defined groups: PLC/comms, digital I/O field, analogue loop power, safety circuit, indication.
- PSU-1 fail, PSU-2 fail, UPS-on-battery and UPS-fault are all monitored digital inputs to the PLC.

> **Why grouped protection matters.** If everything sits behind one 20 A device, a single field short pulls the whole control system down, including the PLC that was going to tell SCADA what happened. Grouping means a shorted field cable trips one group, and the PLC stays up and raises the alarm. This is a real design decision with a real consequence and it is worth being able to explain.

---

## 1.6 Protection philosophy (overview — detail in Stage 2)

| Item | Approach | Reason |
|---|---|---|
| Incomer | 630 A 4-pole MCCB, electronic trip unit with adjustable long-time, short-time and instantaneous elements | Adjustability allows discrimination to be set once the coordination study is available |
| Earth fault at incomer | Element to be provided, setting per study | Dependent on confirmed earthing system (TQ-001) |
| Surge protection | Type 1+2 surge protective device on the incomer, on its own dedicated protective device, with status contact to PLC | Site has overhead reticulation and a history of storm events (client statement, to be confirmed) |
| VSD feeders | MCCB sized and selected **per the drive manufacturer's recommendation**, not from motor FLC | The breaker protects the cable and the drive. The **motor** is protected by the drive's electronic thermal model plus an independent PTC thermistor relay. |
| Motor thermal protection (VSD feeders) | Drive electronic overload **plus** independent PTC thermistor relay wired to trip | Drive thermal models are inferential; embedded thermistors measure actual winding temperature. On a 75 kW pump motor the redundancy is worth it. |
| DOL feeders | MPCB (combined short-circuit + adjustable thermal overload) + contactor | Compact, fewer parts, fewer wiring errors than MCCB + separate overload |
| Control circuits (240 V AC) | MCBs, C curve | |
| Control circuits (24 V DC) | Electronic circuit protectors, **DC rated** | AC MCBs do not reliably clear DC faults — no natural current zero |
| Phase failure / phase sequence | Relay on the incomer, drops the control system healthy signal and raises an alarm | Protects motors from single-phasing; also catches a phase rotation error after a site supply change |
| Dry-run protection | Independent low-low level float switch, **hardwired** into the pump stop logic, not only into the PLC | A PLC in program-stop mode does not protect a 75 kW pump from running dry. Asset protection that matters should not depend solely on software. |

**Not done here, and must not be claimed:** discrimination/selectivity verification, cascade (back-up protection) verification, protection settings. See `00-CLAIM-INTEGRITY.md`.

---

## 1.7 Environmental and installation conditions

| Condition | Value | Comment |
|---|---|---|
| Installation | Indoor, dedicated switchroom, air-conditioned | |
| Nominal switchroom temperature | 25 °C | With HVAC operating |
| Design ambient for equipment selection | 40 °C | **Assumed.** See the question below. |
| Humidity | Up to 95 % RH non-condensing | Anti-condensation heaters with hygrostat fitted as insurance |
| Corrosive atmosphere | None expected in switchroom; chemical dosing area is separate and not adjacent | To be confirmed against site layout |
| Seismic / vibration | Not a design driver at this site | To be confirmed |
| Dust | Low (sealed switchroom) | Supports IP42 rather than IP54 |

> **The question a good PE asks here, and most graduates miss:**
> *"Does the MCC have to keep operating with the switchroom HVAC failed?"*
>
> If the answer is yes, the design ambient is not 25 °C or even 40 °C — a sealed switchroom with two 75 kW drives dumping roughly 4–5 kW of heat and no cooling will climb well past 50 °C. That derates the drives, the breakers and the busbar, and it may force a larger drive frame or forced cubicle ventilation. If the answer is no, then HVAC failure must trip or ramp down the drives, which is a control requirement that has to appear in the functional description and on the schematics.
>
> Either answer changes the design. "Nobody asked" is how a board ends up tripping on over-temperature the first hot Saturday after handover. Raised as **TQ-005**.

---

## 1.8 Communications and control system requirements

| Item | Requirement | Status |
|---|---|---|
| PLC platform | To client standard | **Assumed** Allen-Bradley CompactLogix 5380 — TQ-007. This drives module selection, spares holding, programming resource and SCADA driver. Getting it wrong is expensive and late. |
| SCADA interface | Existing plant SCADA, via fibre to the control room | Confirmed |
| Field network | EtherNet/IP over copper inside the MCC; multimode fibre to control room and to RIO-01 | Design decision |
| Devices on network | PLC, VSD-101, VSD-102, power meter PM-01, RIO-01 adapter, managed switch | |
| IP addressing | Client IP address schedule required | **OPEN — TQ-007** |
| Remote I/O | RIO-01 at intake screen kiosk, approx. 120 m, fibre | Design decision (120 m exceeds practical copper Ethernet limits with margin, and a separate structure warrants galvanic isolation) |
| Critical control signals | **Hardwired**: run command, drive healthy, drive running, speed reference (4–20 mA). Diagnostics and monitoring over EtherNet/IP. | Design decision — see below |
| Time sync | NTP from SCADA | To be confirmed |

> **Design decision worth defending: why hardwire the speed reference when the drive is on EtherNet/IP anyway?**
>
> Because a network fault should not leave a duty pump at an unknown speed with no way to control it, and because fault-finding a hardwired 4–20 mA loop at 2 a.m. is a multimeter job, not a laptop-and-configuration-software job. The cost is one analogue output channel and a screened pair per drive.
>
> The counter-argument is real and you should acknowledge it: all-comms is cheaper, gives far richer diagnostics, and modern drive networks are reliable. Many utilities now specify comms-only. **This is a client standards question, not an absolute right answer** — which is exactly why it is in the design input register rather than decided unilaterally.

---

## 1.9 Control philosophy (summary — detail in Stage 3)

- **Duty/standby with assist.** One pump is duty. The second starts as assist when demand exceeds the duty pump's capacity at maximum speed, or as standby on duty pump failure.
- **Duty rotation** on accumulated run hours, to even out wear, with changeover on fault.
- **Speed control** by PLC PID on discharge flow against a SCADA setpoint.
- **Start permissives**: wet well level above low-level setpoint, discharge valve MOV-101 open, no active trip, drive healthy, E-stop circuit healthy, selector in the correct position, seal water flow proven.
- **Hardwired dry-run trip** on the independent low-low float, independent of PLC level control.
- **Three-position control mode** at the MCC starter: LOCAL / OFF / REMOTE.
  - LOCAL — start/stop from the local control station at the pump. Permissives and trips still apply. PID and duty rotation do not.
  - OFF — isolated from control (not electrically isolated).
  - REMOTE — PLC/SCADA control.
- **Emergency stop** — dual channel, monitored, via safety relay, driving Safe Torque Off on the drives and dropping contactor coils on the DOL feeders. Manual monitored reset.

> **Say this out loud in an interview and you will stand out:** an E-stop using Safe Torque Off removes torque, it does **not** isolate. The motor terminals may still be live. Safe Torque Off is not an isolation method and is not a substitute for a lockable local isolator at the motor and a proper isolation procedure. Confusing the two is a genuine safety error, not a technicality.

---

## 1.10 Standards referenced

These are the standards a package of this type is normally developed against. **Referenced ≠ compliant.** Compliance is a statement about a finished, verified assembly, most of which is the manufacturer's to demonstrate.

| Standard | Relevance |
|---|---|
| AS/NZS 61439.1 | Low-voltage switchgear and controlgear assemblies — general rules. Contains the design verification requirements (temperature rise, short-circuit withstand, IP, clearances, EMC) that the **manufacturer** must satisfy. |
| AS/NZS 61439.2 | Power switchgear and controlgear assemblies — the part that applies to an MCC of this type. Forms of separation are defined here. |
| AS/NZS 3000 | Wiring Rules. Applies to the *installation*, not to the assembly, but governs the interfaces — supply, earthing, protection against electric shock, disconnection times. |
| AS/NZS 3008.1.1 | Selection of cables — the basis for every cable size in the package. |
| AS 60204.1 | Safety of machinery — electrical equipment of machines. Source of control circuit conventions, wire colour convention, stop categories. |
| AS 4024.1 series | Safety of machinery — risk assessment and safety-related control system design. Where required Performance Level comes from. |
| AS/NZS 60529 | Degrees of protection provided by enclosures (IP codes). |
| AS/NZS 1768 | Lightning protection — informs surge protective device selection and coordination. |
| AS/NZS 61000 series | EMC — emission and immunity, and harmonic current limits relevant to the drives. |
| AS 2700 | Colour standards (enclosure finish, labelling conventions). |
| AS/NZS 4836 | Safe working on low-voltage electrical installations — relevant to how the board is worked on and tested. |
| **Client Electrical Design Standard** | **Not yet obtained — TQ-001.** In practice this governs over everything above where it is more onerous. Water utilities typically mandate specific equipment brands, labelling, terminal types, spare capacity and IP ratings. |

> **This is a real PE point.** A graduate quotes AS/NZS 61439. An engineer who has delivered a package asks for the *client's* standard first, because that is what the board will be judged against at FAT, and it is usually more prescriptive than the Australian Standard.

---

## 1.11 Spare capacity requirements

| Item | Spare provision | Basis |
|---|---|---|
| Feeders | 2 fitted and wired spare feeders (63 A, 32 A) + 20 % spare chassis space | **Assumed** pending client standard |
| Terminals | 20 % spare terminals on every rail, grouped at the end of each rail | Design decision |
| PLC digital inputs | 8 spare (20 % of installed) | |
| PLC digital outputs | 18 spare | Consequence of rounding up to a whole module — see Stage 5 |
| PLC analogue inputs | 10 spare | Consequence of module granularity |
| PLC analogue outputs | 2 spare | |
| Network switch ports | 2 spare copper, 0 spare fibre | Flagged — see Stage 5 discrepancy |
| Cubicle cable entry | Undrilled spare gland plate area | |

> **Why spares are a PE issue, not a drafting issue.** Spare terminals and spare I/O cost almost nothing at build and cost a shutdown to add later. Spare *chassis space* is the expensive one and the one clients most often forget to specify. If the client has not stated a spare capacity requirement, that is a TQ — not a guess.

---

## 1.12 Interfaces with other disciplines and parties

| Interface | Our side stops at | Their side starts at | Risk if undefined |
|---|---|---|---|
| Mechanical / pump vendor | Terminals in MCC-01 | Motor terminal box, local isolator | Motor nameplate data arrives late and the drive is already ordered (**this is the Stage 9 change**) |
| Installation contractor | Gland plate and terminals | Cable supply, glanding, field termination | Gland plate cutouts wrong for the actual cables; cable sizes changed after gland plates were punched |
| Instrumentation | Terminals X4 in MCC-01 | Field instrument terminals | Loop powered vs. externally powered transmitters; who supplies the 24 V; 2-wire vs 4-wire |
| Systems integrator (PLC code) | I/O list, functional description, terminals | PLC application program, SCADA graphics | I/O list revision mismatch — integrator programs to Rev B while the board is built to Rev C |
| Civil / structural | MCC base frame and fixing points | Plinth, floor loading, cable pit | Plinth dimensions vs. actual board footprint; cable entry direction |
| HVAC | Heat load figure we declare | Switchroom cooling design | We declare heat load too late, or too low, and the switchroom cooks |
| Network operator | MCC incoming terminals | Transformer, HV, metering | Fault level, harmonic limits, metering requirements |
| Client operations | FAT sign-off, MDR | Site acceptance test, commissioning, operation | Operator not consulted on local control philosophy, then rejects it at site |
| Safety | Circuit architecture | Risk assessment, PL determination | We build a PLd-looking circuit and the risk assessment later calls for PLe |

> **The heat load interface is the one graduates never think of.** You are the only party who knows how much heat two 75 kW drives will dump into that room. If you do not tell the HVAC designer early, in writing, with a number, nobody will ask — and the switchroom will be undercooled. Drive losses of roughly 2–3 % of rated power is the usual planning figure; the real number comes from the drive manufacturer's data.

---

## 1.13 DESIGN INPUT REGISTER

**Document:** NFD-ELE-REG-0001 · **Rev C** · Also available as `registers/design-input-register.csv`

| # | Requirement | Source | Engineering Response | Drawing / Document Affected | Status |
|---|---|---|---|---|---|
| DI-001 | Supply 415 V 3ph 4W 50 Hz from TX-01 | Client drawing NFD-CLI-SLD-9001 | Adopted as the design supply. Incomer 4-pole to break neutral. | SLD-0001 | **Closed** |
| DI-002 | Transformer 500 kVA, Dyn11, Z = 5 % | TX-01 nameplate (photo on file) | Used for indicative fault contribution only. Not accepted as the design fault level. | DBS-0001 | **Closed** |
| DI-003 | Prospective fault level at MCC | **Not supplied** | 25 kA / 1 s assumed for tender. All breaker Icu/Ics and busbar Icw provisionally selected on this basis. **Must be confirmed before design freeze.** | SLD-0001, BOM | **OPEN — TQ-002** |
| DI-004 | Earthing system (TN-S / TN-C-S) | **Not supplied** | TN-S assumed. Separate neutral and earth bars provided. Earth-fault element provisioned at incomer. | SLD-0001 | **OPEN — TQ-001** |
| DI-005 | Client Electrical Design Standard | **Not supplied** | Generic industry practice adopted as the interim basis. Substantial rework risk if the client standard mandates different equipment brands, Form 4b, or different labelling. | All | **OPEN — TQ-001** |
| DI-006 | Two transfer pumps, 75 kW, variable speed, duty/assist | Client functional spec §4.2 | Two VSD feeders. Duty rotation and assist logic in functional description. | SLD-0001, SCH-0101/0111, FDS | **Closed (superseded by DI-024)** |
| DI-007 | Pump motor full nameplate data | Pump vendor — **not yet issued** | Typical 4-pole figures used for frame selection. Drive, feeder breaker, cable and thermal data cannot be finalised without it. | SLD, BOM, cable schedule | **OPEN — highest schedule risk** |
| DI-008 | Drive must accept motor PTC thermistors | Design decision | Independent thermistor relay per pump specified, trip wired into drive external-fault and into PLC. | SCH-0101, BOM | **Closed** |
| DI-009 | Dry-run protection required | Client functional spec §4.6 | Independent low-low float, hardwired into stop logic in addition to PLC level control. | SCH-0101, SCH-0201 | **Closed** |
| DI-010 | Emergency stop at each pump and at the MCC | Client functional spec §6.1 | Dual-channel monitored E-stop circuit, safety relay, STO to drives, coil drop to DOL feeders, monitored manual reset. | SCH-0040 | **Closed (architecture)** |
| DI-011 | Required Performance Level for the E-stop safety function | **Not supplied** | PLd architecture adopted as a reasonable interim. Required PL must come from a machinery risk assessment; achieved PL must be verified by calculation. **Neither performed by us.** | SCH-0040, BOM | **OPEN — TQ-003** |
| DI-012 | Local control station at each pump | Client functional spec §6.2 | LCS-101/102: Local-Off-Remote selector, Start, Stop, E-stop, Running lamp. IP66 GRP enclosure. | SCH-0101, TRM-0401 | **Closed** |
| DI-013 | Indoor air-conditioned switchroom | Site visit report | IP42 adopted. Anti-condensation heaters with hygrostat fitted as insurance against HVAC outage. | DBS, BOM | **Closed** |
| DI-014 | MCC operation with HVAC failed | **Not stated** | Two options priced: (a) uprate/derate for 50 °C, (b) HVAC-fail interlock ramping the drives down. Client decision required. | DBS, SCH-0201, BOM | **OPEN — TQ-005** |
| DI-015 | Declared heat load to HVAC designer | Interface requirement | Estimated total dissipation issued to the HVAC designer in writing at Rev B. To be reissued if drive rating changes. | Interface memo IFM-002 | **Closed — reopen on DI-024** |
| DI-016 | PLC platform and I/O standard | **Not supplied** | CompactLogix 5380 assumed. Module selection, spares and SCADA driver all depend on this. | SLD, BOM, I/O list | **OPEN — TQ-007** |
| DI-017 | IP address schedule | **Not supplied** | Placeholder scheme used for FAT only. Must be replaced before site. | Network drawing, FAT | **OPEN — TQ-007** |
| DI-018 | SCADA communication over existing plant fibre | Client functional spec §8 | Managed switch with two multimode fibre ports. One to control room, one to RIO-01. | SLD, BOM | **Closed (see Stage 5 discrepancy)** |
| DI-019 | Remote I/O at intake screen, approx. 120 m | Site layout drawing | RIO-01 with EtherNet/IP adapter and fibre link. Separate 240 V supply from DB-01 at the kiosk, with its own 24 V PSU. | SLD, RIO drawings | **Closed** |
| DI-020 | Harmonic distortion limits at the point of connection | **Not supplied** | Two six-pulse drives totalling 150 kW on a 500 kVA transformer is enough to warrant an assessment. Provisional allowance for line reactors; active filter carried as a risk. | SLD, BOM, cubicle GA | **OPEN — TQ-006** |
| DI-021 | Spare capacity requirement | **Not stated** | 20 % spare terminals, 20 % spare I/O, two fitted spare feeders, 20 % spare chassis. | All | **OPEN — TQ-001** |
| DI-022 | Surge protection required | Client functional spec §5.4 | Type 1+2 SPD at incomer on a dedicated protective device, status contact to PLC. | SLD, SCH-0201 | **Closed** |
| DI-023 | Cable entry direction | **Not supplied** | Top entry assumed. **Cannot draft the general arrangement until confirmed** — bottom entry changes cubicle internals, gland plates and the cable zone. | GA, gland plate detail | **OPEN — TQ-001** |
| DI-024 | **Revised pump duty — motors uprated 75 kW → 90 kW** | Client TQ response TQR-009, issued after hydraulic re-modelling | Full change impact assessment raised. See Stage 9. | **SLD, SCH-0101/0111, TRM, BOM, GA, cable schedule, FAT, heat load** | **OPEN — change in progress** |
| DI-025 | Seal water flow proving on each pump | Client functional spec §4.7 | Flow switch per pump wired as a start permissive with a run-delay bypass. | SCH-0101, SCH-0201 | **Closed** |

---

## 1.14 Engineering assumptions register (consolidated)

Every one of these is a liability until it is closed. This list is what a PE reads out at a design review.

| # | Assumption | Consequence if wrong | Owner to close |
|---|---|---|---|
| A-01 | PSCC 25 kA / 1 s | Wrong Icu/Icw. Potentially every protective device replaced. **Highest cost exposure in the package.** | Client / network operator |
| A-02 | TN-S earthing | Neutral and earth bar arrangement, earth-fault element, RCD strategy | Client |
| A-03 | Form 3b acceptable | Form 4b means a materially different and more expensive enclosure build | Client |
| A-04 | Top cable entry | General arrangement, gland plates, cubicle internals | Client |
| A-05 | Motor FLC typical values | Drive frame, feeder breaker, cable size, thermal data | Pump vendor |
| A-06 | 40 °C design ambient | Derating of drives, breakers, busbar | Client (TQ-005) |
| A-07 | CompactLogix PLC platform | All I/O modules, spares, integrator resource, SCADA driver | Client |
| A-08 | Hardwired speed reference acceptable | Two analogue channels and two screened pairs, plus drawing rework | Client |
| A-09 | Line reactors sufficient for harmonics | Active harmonic filter would need an additional cubicle — schedule and cost | Client / specialist study |
| A-10 | PLd adequate for E-stop function | PLe would change safety relay, architecture and possibly device selection | Client / safety consultant |
| A-11 | 20 % spare capacity | Board size, cost | Client |
| A-12 | Catalogue numbers as listed | Standard BOM risk, managed by vendor quote verification | Project Engineer |

---

## 1.15 What the Project Engineer actually did at Stage 1

Not design. This:

1. **Read the client specification and the functional spec properly**, and listed every requirement that had an engineering consequence.
2. **Built the Design Input Register** and separated confirmed inputs from assumptions.
3. **Identified the missing inputs** — fault level, earthing system, client standard, motor data, PLC platform, cable entry, harmonic limits, required PL, ambient case.
4. **Raised technical queries** for each, with an owner and a required-by date tied to the design freeze.
5. **Issued the heat load to the HVAC designer in writing**, because nobody else was going to.
6. **Briefed the designer and drafter** on what was confirmed, what was assumed, and what must not be drafted yet (the general arrangement, pending cable entry direction).
7. **Flagged the schedule risk** from missing pump vendor data to the project manager, early and in writing.

That last one is the difference between a PE and a document administrator. The pump data was always going to be late, and it was always going to change the drive. Saying so in week two is engineering judgement. Saying so in week twelve is an excuse.

---

**Next:** [Stage 2 — Single Line Diagram](02-SINGLE-LINE-DIAGRAM.md)
