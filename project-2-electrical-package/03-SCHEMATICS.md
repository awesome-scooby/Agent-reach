# STAGE 3 — SCHEMATIC / CONTROL DRAWINGS

**Drawings:**
[`NFD-ELE-SCH-0030.svg`](drawings/NFD-ELE-SCH-0030.svg) — Control power distribution
[`NFD-ELE-SCH-0040.svg`](drawings/NFD-ELE-SCH-0040.svg) — Emergency stop and safety circuit
[`NFD-ELE-SCH-0101.svg`](drawings/NFD-ELE-SCH-0101.svg) — P-101 VSD power and control
[`NFD-ELE-SCH-0201.svg`](drawings/NFD-ELE-SCH-0201.svg) — PLC digital inputs (typical)

---

## 3.1 The relationship between the SLD and the schematics

The SLD says **what is connected and how a fault is cleared.**
The schematics say **what makes it operate, what stops it, and what happens when something breaks.**

They meet at the starter. One block on the SLD — `Q11 → VSD-101 → P-101` — expands into:

| SLD element | Schematic sheets it becomes |
|---|---|
| Q11 MCCB | SCH-0101 power section; its auxiliary contact appears on SCH-0201 as "feeder available" |
| VSD-101 | SCH-0101 power and control; its STO terminals appear on SCH-0040; its network port on SCH-0301 |
| Motor thermistors | SCH-0101 via thermistor relay KT101 |
| P-101 motor | SCH-0101 power; local isolator is an interface, not our supply |
| (not on SLD) | SCH-0101 control: L/O/R selector, permissives, run command, feedback, LCS-101 |

**The rule to remember, and to quote:** *anything that carries load current appears on the SLD; anything that carries a decision appears on the schematic.* If a device appears on one and not the other when it should appear on both, that is a reconciliation failure and the PE's job is to find it.

---

## 3.2 Drawing conventions used

| Convention | Value | Note |
|---|---|---|
| Sheet size | A3 landscape | |
| Grid | Vertical current-path numbering, left to right, numbered in the margin | Every rung has a unique reference |
| **Wire numbering** | `SHEET-PATH`, e.g. `0101-14` = sheet 0101, current path 14 | Ferruled both ends. Means any wire number tells you which drawing to open. |
| Cross-referencing | Contact references show the sheet and path of the coil, coil references list every contact | Standard practice; without it, fault-finding a relay is guesswork |
| Device tagging | IEC-style letter codes: Q (protective device), KM (contactor), KA (relay), KT (timer/thermistor relay), S (switch), H (indicator), X (terminal), U (converter/drive), B (sensor) | |
| **Wire colours (internal)** | Per AS 60204.1: black = power; **red = AC control**; **dark blue = DC control**; **orange = interlock supplied from an external source**; light blue = neutral; green/yellow = earth | The orange one matters — see §3.9 |
| Terminal rails | Segregated by voltage and function — see Stage 4 | |
| Revision | Letters (A, B, C…) = preliminary / IFR / IFA. Numbers (0, 1, 2…) = Issued for Construction and onwards | Standard Australian convention |

> **The orange wire rule is worth knowing.** A conductor that stays live when the board's own isolator is opened — because it is fed from somewhere else — is coloured orange under AS 60204.1. In this package that is the MOV-101 actuator's internal supply interface and any client-supplied volt-free contact fed from an external source. The point of the colour is that someone who has isolated the board and opened the door does not assume every wire is dead. This is a safety convention, not a cosmetic one, and it should be called up in the specification and checked at FAT.

---

## 3.3 Control power distribution — SCH-0030

**Purpose.** Create and distribute the 24 V DC control supply in a way that survives a single failure and does not let one field fault take down the control system.

```
 240 V AC from Q19
   │
  [UPS-01]  1 kVA online, ~15 min autonomy
   │
   ├── MCB F1 ──► [PSU-1] 24 V DC 20 A ──┐
   │                                     ├──► [O-ring redundancy module] ──► 24 V DC bar
   └── MCB F2 ──► [PSU-2] 24 V DC 20 A ──┘
                                              │
   ┌──────────────┬──────────────┬────────────┼────────────┬──────────────┐
  [ECP1]        [ECP2]        [ECP3]       [ECP4]       [ECP5]        [ECP6]
  PLC &         Digital        Digital      Analogue     Safety        Indication
  network       inputs         outputs      loop power   circuit       & LCS
  (rack)        (field)        (field)
```

`ECP` = electronic circuit protector, DC-rated, with a status contact.

**Design points and why:**

| Decision | Reason |
|---|---|
| Two PSUs from two separate MCBs | A single MCB trip cannot take out both supplies |
| O-ring redundancy module, not paralleled outputs | Directly paralleling switch-mode supplies causes current sharing problems and lets a failed supply drag the bus down. The redundancy module decouples them. |
| Sized at 20 A each, not 10 A | Each supply must carry the **full** load alone, not half. Sizing two 10 A supplies for a 15 A load is not redundancy. |
| **Electronic circuit protectors, not AC MCBs** | Standard AC MCBs have no DC interrupting rating. DC has no current zero, so the arc does not self-extinguish. Using an AC MCB on a DC circuit is a genuine fault, not a technicality. |
| Grouped protection, not one device | A shorted field cable trips one group. The PLC stays alive and reports the alarm. |
| ECP status contacts to PLC | You find out a group has tripped from SCADA, not from a pump that will not start next Tuesday |
| PSU-1 fail, PSU-2 fail, UPS on battery, UPS fault all monitored | Redundancy you cannot see the state of is not redundancy — you just get two failures instead of one, separated by months |

**INPUT → LOGIC → OUTPUT → FEEDBACK → FAILURE**

| | |
|---|---|
| **INPUT** | 240 V AC from Q19 via UPS-01 |
| **LOGIC** | Two independent conversion paths, decoupled, combined onto one bus, then divided into protected groups |
| **OUTPUT** | 24 V DC to PLC rack, field DI, field DO, analogue loops, safety circuit, indication |
| **FEEDBACK** | PSU healthy contacts, ECP status contacts, UPS status, all as PLC digital inputs |
| **FAILURE** | One PSU fails → bus holds, alarm raised, plant runs. Mains fails → UPS holds PLC and comms, "station supply fail" alarm reaches SCADA before autonomy expires. One field group shorts → that ECP trips, alarm raised, rest of the control system unaffected. **Both PSUs fail or the 24 V bus shorts → total control loss; drives stop on loss of run command; the hardwired E-stop circuit is separately protected on ECP5 so the safety function does not depend on the same group as general control.** |

> **Be ready for this question: "What happens if you lose 24 V?"** The answer is not "everything stops". The answer is: the run commands drop so the drives coast or ramp to stop per configuration, the contactors drop out because the coils are 24 V DC, the PLC is on the UPS so it may still be alive to report, and — importantly — **the safety function is on its own protected group so an ordinary control fault cannot disable the E-stop circuit.**

---

## 3.4 Emergency stop and safety circuit — SCH-0040

**Devices in the circuit:**
- S-ES-MCC — E-stop on the MCC door
- S-ES-101 — E-stop on local control station LCS-101 (at pump P-101)
- S-ES-102 — E-stop on LCS-102 (at pump P-102)
- S-ES-PH — E-stop at the pump hall entry
- KS-01 — safety relay, dual channel, with monitored manual reset
- S-RST — monitored reset pushbutton at the MCC

**Architecture:**

```
 24 V DC (ECP5)
   │
   ├── Channel A ── S-ES-MCC ── S-ES-101 ── S-ES-102 ── S-ES-PH ──► KS-01 input A
   └── Channel B ── S-ES-MCC ── S-ES-101 ── S-ES-102 ── S-ES-PH ──► KS-01 input B
                      (each E-stop: two independent NC contacts)

   S-RST ──► KS-01 reset input (monitored — acts on release, not on press)

   KS-01 safety outputs ─┬─► VSD-101 STO terminals (2 channels)
                         ├─► VSD-102 STO terminals (2 channels)
                         └─► DOL contactor coil circuit (KM103, KM101C)

   KS-01 auxiliary ──────► PLC DI "E-stop circuit healthy"
```

**Why dual channel.** A single-channel E-stop can be defeated by one welded contact or one shorted wire and nobody would know. Two independent channels, monitored by the safety relay for agreement and for timing, mean a single fault is detected and the circuit goes to the safe state rather than silently failing.

**Why monitored manual reset.** An E-stop that resets by itself when released is dangerous — the plant restarts while someone is still in it. "Monitored" means the relay checks the reset button's own behaviour; it acts on the **falling edge** (button released), so a reset button that is stuck pressed or shorted will not reset the circuit.

**Why STO rather than just dropping a run command.**
Removing the run command is a *functional* stop that depends on the drive's firmware behaving. STO is a hardware-level function in the drive that removes the gate drive signals to the output stage — it is designed and certified as a safety function. It is not dependent on the drive's control logic being intact.

**Why STO is NOT isolation — say this:**

> *"Safe Torque Off removes torque. It does not disconnect. The drive output terminals, and therefore the motor terminals, can still be at a hazardous potential after an E-stop is pressed. STO is not isolation, it is not a substitute for a lockable isolator at the motor, and it does not satisfy an isolation procedure for working on the machine. The E-stop is there so you can stop the plant quickly, not so you can put your hands in it."*

That paragraph, delivered calmly in an interview, tells a manager you understand the difference between a control function and a safety-isolation procedure. It is probably the single highest-value thing in this package.

**Stop category.** This is a **Category 0** stop under AS 60204.1 — immediate removal of power to the actuator. A Category 1 stop (controlled stop, then power removed) is sometimes preferred on a pump because an abrupt stop of a 75 kW pump at full speed can cause hydraulic surge and water hammer, which damages pipework and valves.

> **A genuinely good design question to raise, and one I have not resolved here:** should the E-stop on this station be Category 0 or Category 1? Category 0 is simpler and unambiguously safe for the person. Category 1 protects the pipework. Deciding it is not a drafting decision — it requires the machinery risk assessment and a hydraulic surge assessment, neither of which is mine. **TQ-003.** Raising this rather than silently choosing is the correct PE behaviour.

**INPUT → LOGIC → OUTPUT → FEEDBACK → FAILURE**

| | |
|---|---|
| **INPUT** | Any of four E-stop devices, each with two independent normally-closed contacts |
| **LOGIC** | Both channels must be closed and must agree within the safety relay's discrepancy time. Reset is manual and monitored. |
| **OUTPUT** | STO to both drives; contactor coil circuit opened for DOL feeders |
| **FEEDBACK** | Safety relay auxiliary contact → PLC DI "E-stop healthy". Each drive's STO status also reported over EtherNet/IP. |
| **FAILURE** | E-stop pressed → both channels open → STO active, contactors drop, alarm to SCADA, plant will not restart until the E-stop is released **and** reset is pressed and released. **One channel open only (broken wire, welded contact)** → relay detects discrepancy, goes to the safe state, and will not reset until the fault is cleared. **Loss of 24 V on ECP5** → circuit de-energises, which is the safe state (fail-safe by design). **Safety relay itself fails** → this is precisely what the PL verification would quantify, and that verification has not been done. |

**What this circuit is NOT:** verified. See `00-CLAIM-INTEGRITY.md`. The architecture looks like a Category 3 / PLd arrangement. The required PL comes from a risk assessment I have not performed, and the achieved PL requires an ISO 13849-1 calculation using the manufacturers' reliability data, which I have not performed. Saying "this is PLd" without that calculation is a false claim.

---

## 3.5 Transfer pump P-101 control — SCH-0101

The main event. Both transfer pumps are identical; P-102 is drawn on SCH-0111 with the same logic.

### 3.5.1 Power section

```
 Busbar ─► Q11 (250 A MCCB) ─► [line reactor, provisional] ─► VSD-101
                                                                │
                                                     EMC gland, 360° screen
                                                                │
                                                   screened VSD motor cable
                                                                │
                                                  local isolator (field, others' scope)
                                                                │
                                                              (M) P-101
                                                                │
                                                      PTC thermistors ─► KT101
```

### 3.5.2 Control section — device list

| Tag | Device | Location |
|---|---|---|
| S101-LOR | Local / Off / Remote selector, 3-position stay-put | MCC door |
| S101-STR | Start pushbutton, green | MCC door |
| S101-STP | Stop pushbutton, red | MCC door |
| H101-RUN | Running lamp, green LED 24 V DC | MCC door |
| H101-FLT | Fault lamp, red LED 24 V DC | MCC door |
| H101-PWR | Available lamp, white LED 24 V DC | MCC door |
| KT101 | PTC thermistor relay | MCC |
| KA101 | Run command interposing relay | MCC |
| S101L-LOR | Local / Remote selector | LCS-101 at pump |
| S101L-STR | Start pushbutton | LCS-101 |
| S101L-STP | Stop pushbutton | LCS-101 |
| S-ES-101 | E-stop, mushroom, twist release, 2 × NC | LCS-101 |
| H101L-RUN | Running lamp | LCS-101 |
| B101-SEAL | Seal water flow switch | Field |
| B101-LSLL | Wet well low-low float (shared, common trip) | Field |

### 3.5.3 Control logic in words

**Permissives — ALL must be true before a start is allowed:**

| # | Permissive | Source | Why |
|---|---|---|---|
| 1 | E-stop circuit healthy | KS-01 aux (hardwired to drive STO as well) | Obvious |
| 2 | Q11 closed / feeder available | Q11 auxiliary contact → PLC DI | Do not command a start into a dead feeder; also tells the operator why the pump will not run |
| 3 | Drive healthy / ready | VSD-101 relay output → PLC DI | Drive has no active trip and has completed its power-up |
| 4 | Thermistor relay healthy | KT101 contact | Motor winding temperature acceptable |
| 5 | Wet well level above low-level setpoint | LIT-101 via PLC | Do not start a pump into an empty well |
| 6 | Low-low float not tripped | B101-LSLL **hardwired** into the drive's external-fault input **and** to a PLC DI | Independent of the PLC and independent of the transmitter. See below. |
| 7 | Seal water flow proven | B101-SEAL, with a start bypass timer | Mechanical seals fail quickly without flush water. The bypass exists because flow cannot be proven before the pump starts. |
| 8 | Discharge valve MOV-101 open | ZSO-101 limit switch → PLC DI | Starting against a closed discharge valve causes rapid heating and can damage the pump |
| 9 | Selector in a valid position (Local or Remote) | S101-LOR | Off means off |
| 10 | No unacknowledged latched trip | PLC | Forces the operator to look at why it tripped |

**Why permissive 6 is hardwired and duplicated — this is the design decision to be able to defend:**

Dry-running a 75 kW pump destroys the mechanical seal in minutes and can damage the pump and the motor. There are three ways that protection could be implemented:

1. PLC reads the level transmitter and stops the pump. *Fails if the transmitter drifts, if the PLC is in program-stop, or if someone forces the tag during commissioning.*
2. An independent float switch read by the PLC. *Better — independent sensor — but still depends on the PLC.*
3. An independent float switch **hardwired** into the drive's external-fault input, **and also** read by the PLC for alarming. *Protects the asset even with the PLC stopped, and still tells SCADA what happened.*

Option 3 is what is drawn. The cost is one extra float, one extra pair and one drive input. The benefit is that asset protection worth tens of thousands of dollars does not depend on software that a contractor might have in a forced state at 11 p.m. during commissioning.

> **The general principle, and it is worth stating this way:** *"Protection that matters shouldn't depend solely on software that someone can force. If it protects a person or a major asset, I want it hardwired as well as monitored."*

**Local / Off / Remote behaviour:**

| Selector position | Start / stop source | Speed reference | Permissives | Duty rotation / PID |
|---|---|---|---|---|
| **LOCAL** | LCS-101 or MCC pushbuttons | Fixed local speed preset in the drive | **All still apply** | Not active |
| **OFF** | None — pump will not run | — | — | Not active. PLC sees "not available" and will not select this pump as duty. |
| **REMOTE** | PLC / SCADA | PLC AO 4–20 mA, PID on discharge flow | All apply | Active |

**Why LOCAL still enforces every permissive.** Local mode is for maintenance and fault-finding, not for bypassing protection. A "local" mode that drops the dry-run trip and the thermistor trip is how a pump gets destroyed by a fitter who assumed it was protected. **Local changes who gives the command, not what protects the machine.** If a genuine bypass is ever required, it must be a deliberate, key-switched, alarmed and time-limited function — and that is a client decision, not a drafting decision.

**Why two selector inputs to the PLC, not one.** Reading both "Local selected" and "Remote selected" as separate digital inputs lets the PLC distinguish three states — Local, Remote, and Off — and also detect a fault: if both read true, something is wrong with the selector or the wiring, and that is an alarm. One input can only ever tell you two things, and it cannot tell you it is broken.

### 3.5.4 INPUT → LOGIC → OUTPUT → FEEDBACK → FAILURE

| | |
|---|---|
| **INPUT** | Start command (SCADA in Remote, or pushbutton in Local); wet well level LIT-101; discharge flow FIT-101; valve position ZSO-101; seal flow B101-SEAL; low-low float B101-LSLL; thermistor relay KT101; drive healthy; E-stop healthy; feeder available; selector position |
| **LOGIC** | PLC: if all permissives true AND start command present AND (this pump is duty OR assist is called) THEN energise run command. Speed reference from PID on discharge flow against SCADA setpoint, clamped between minimum and maximum speed. Duty rotation on accumulated run hours. Assist starts when the duty pump is at maximum speed and the setpoint is still not met. |
| **OUTPUT** | PLC DO → KA101 → hardwired run command to VSD-101 terminal. PLC AO 4–20 mA → drive speed reference. Hardwired dry-run trip → drive external fault input. Safety relay → drive STO. |
| **FEEDBACK** | Drive running (hardwired DI); drive healthy (hardwired DI); actual speed, current, power, DC bus, fault code, run hours (EtherNet/IP); running lamp at MCC and at LCS; flow FIT-101 confirming the pump is actually moving water |
| **FAILURE** | **Drive trips** → "drive healthy" DI drops, run command removed, fault lamp on, alarm to SCADA, standby pump called after a delay. **Motor over-temperature** → KT101 opens, drive external fault, pump stops, latched alarm requiring manual acknowledgement. **Dry-run** → hardwired float trips the drive directly, independent of PLC. **Loss of PLC** → run command DO de-energises, pump stops. **Loss of 24 V** → same. **Broken 4–20 mA speed reference** → drive detects live-zero loss (< 4 mA) and acts per its configured live-zero response — configured to hold last speed and alarm, rather than ramp to zero, so a broken wire does not stop the station instantly. **Network failure** → hardwired run/stop and speed reference still work; only diagnostics are lost. **This is why the reference is hardwired.** |

> **"Commanded running but no flow" is the failure mode most people miss.** The drive reports running, the current looks plausible, and no water is moving — a closed valve, an airlock, a broken coupling, a blocked suction. The only thing that catches it is a cross-check of the flow measurement against commanded speed, with a time delay. Worth calling up in the functional description. It costs nothing and it is the difference between a monitored pump station and a pump station with instruments on it.

---

## 3.6 DOL feeder control — P-103 sump pump (SCH-0121, typical)

Simpler, and worth understanding precisely because it is simple.

```
 24 V DC (ECP2)
   │
  [Q15 aux] ── [KT-OL, MPCB trip aux] ── [S103-LOR] ──┬── LOCAL: S103-STR / S103-STP latch
                                                      └── REMOTE: PLC DO
                                                           │
                                                      [safety relay contact]
                                                           │
                                                        (KM103 coil)
                                                           │
                                                    KM103 aux ──► PLC DI "running"
```

| | |
|---|---|
| **INPUT** | Float switch in the sump (via PLC in Remote), or local pushbuttons |
| **LOGIC** | PLC: high float starts, low float stops, with a maximum run timer to catch a stuck float. In Local, a conventional latched start/stop with the stop button in series with the coil. |
| **OUTPUT** | KM103 contactor coil, 24 V DC |
| **FEEDBACK** | KM103 auxiliary contact → PLC DI "running". **Not** the DO echo — see below. |
| **FAILURE** | MPCB trips on overload → auxiliary contact → "not available" alarm, and the PLC stops calling it. Contactor fails to pull in → "commanded but not running" discrepancy alarm after a delay. Contactor welds closed → "running but not commanded" discrepancy alarm. Loss of 24 V → coil drops, pump stops. E-stop → coil circuit opened by safety relay contact. |

> **Read back the contactor, not the output.** Using the PLC's own output as the "running" indication tells you only that the PLC told it to run. A separate auxiliary contact on the contactor tells you the contactor actually moved. The difference between those two signals is how you detect a welded contactor, a blown coil, or a tripped MPCB — and comparing them with a time delay gives you a genuinely useful discrepancy alarm. This is a small point that experienced people notice immediately.

---

## 3.7 PLC interface — SCH-0201 onwards

### 3.7.1 Digital inputs

- 24 V DC sourcing field devices into sinking input modules.
- **Every field digital input passes through a terminal on rail X3** — no field wire lands directly on a PLC module. The module can then be replaced without disturbing field wiring, and every signal can be tested and disconnected at a terminal.
- Volt-free contacts from the field wherever possible. Where a field device provides a voltage output, an interposing relay is used.
- Critical inputs (drive healthy, E-stop healthy, thermistor relay) are wired **normally closed**, so a broken wire reads as a fault rather than as healthy. **Fail-safe wiring — this is a real design decision and a good interview answer.**

### 3.7.2 Digital outputs

- PLC DO → interposing relay → field device, for anything leaving the board.
- **Why interpose.** It protects the PLC module from a field short or an induced surge (the relay is far cheaper than the module and far quicker to replace), it gives a volt-free contact that can switch a different voltage than the PLC's 24 V, and it gives a visible LED and a physical test point for fault-finding.
- The trade-off, and it is real: more components, more panel space, more things to fail, and a relay is slower than a solid-state output. For a pump station it is the right call. For a high-speed machine it might not be.

### 3.7.3 Analogue inputs

- 4–20 mA, 2-wire loop-powered transmitters, loop power from the dedicated analogue group (ECP4) — **not** from the same group as the digital field outputs, so a DO field short cannot corrupt every analogue reading at once.
- Individually screened pairs, screen earthed **at the MCC only**, on the dedicated instrument screen earth bar.
- Every loop lands on a **disconnect-type terminal** on rail X4, so the loop can be broken and a calibrator injected without unwiring anything.
- **Why 4–20 mA and not 0–20 mA or 0–10 V:** the live zero. A healthy loop never reads 0 mA, so 0 mA means a broken wire or a dead transmitter — a condition you can detect and alarm. With 0–20 mA, a broken wire reads the same as a legitimate zero, and you cannot tell the difference. 0–10 V is also far more susceptible to volt drop and noise over field distances.

### 3.7.4 Analogue outputs

- 4–20 mA speed references to the drives, screened pair, terminal rail X4, disconnect terminals.
- Drive configured for live-zero detection with a defined response (§3.5.4).

### 3.7.5 I/O allocation principle

| Principle | Reason |
|---|---|
| Group signals by equipment, not by module convenience | Fault-finding one pump means looking at one module group, not six |
| Never split a safety-related signal across modules with other functions | Clarity, and it simplifies any future safety assessment |
| Keep spare points contiguous and at the end of each module | A tidy spare block is usable; scattered spares are not |
| Reserve one spare slot in the chassis, not just spare points | A future function may need a module type you do not have |
| Document every point in the I/O list before the schematics are drafted | The I/O list is the contract between the electrical package and the integrator |

---

## 3.8 Schematic-to-SLD reconciliation check

| # | Check | Typical failure found |
|---|---|---|
| 1 | Every SLD feeder has a schematic sheet, and every schematic sheet has an SLD feeder | An orphan schematic from a copied project |
| 2 | Device tags identical on both (Q11 is Q11 everywhere) | Renumbered on one drawing only |
| 3 | Every contactor on the schematic appears on the SLD | An interlock contactor that exists only on the schematic, and therefore not in the BOM |
| 4 | Every auxiliary contact used on a schematic actually exists on the device as specified in the BOM | **The most common error in the whole package.** Four auxiliary contacts used, two supplied. |
| 5 | Coil voltages on the schematic match the BOM part numbers | 24 V DC on the drawing, 240 V AC coil ordered |
| 6 | Every wire that leaves the board goes to a terminal, and that terminal is on the termination drawing | Wire drawn straight out of the board |
| 7 | Every PLC point on a schematic exists in the I/O list at the same address | Address drift between revisions |
| 8 | Cross-references resolve — every coil lists its contacts, every contact points at its coil | Dangling reference after a sheet is deleted |
| 9 | Safety circuit devices are consistent: the number of E-stops on SCH-0040 equals the number in the BOM and on the termination schedule | Field E-stop added late to the schematic, never added to the BOM |
| 10 | Control supply group loading matches the PSU and ECP sizing | Circuits added over revisions until the group exceeds its protector |

> **Item 4 deserves its own paragraph.** Auxiliary contact shortfall is the single most common cause of workshop stoppages on switchboard jobs. The schematic designer uses contacts freely because on a drawing they are free. The contactor arrives with two. Someone then has to source an add-on auxiliary block, which may be out of stock, and the wireman stops.
>
> **The check is mechanical and it takes an hour:** count every contact used per device across every sheet, list what the BOM part number actually provides as standard, and list the add-on blocks required. Do it at Rev B, not in the workshop. This exact error appears as the worked discrepancy in Stage 5.

---

## 3.9 What the Project Engineer did at Stage 3

1. Wrote the **functional description** — plain-English control philosophy — *before* the schematics were drafted, and had the client agree it. Schematics drafted from a verbal brief get drafted twice.
2. Reviewed each schematic sheet against the functional description, line by line.
3. Ran the reconciliation check in §3.8 and raised the auxiliary contact shortfall (Stage 5).
4. Challenged the drafter's first revision, where **Local mode bypassed the seal-water and dry-run permissives** — drawn that way because "that's how the last one was". Had it changed and recorded why, so the next person does not reverse it.
5. Raised **TQ-003** on the E-stop stop category and the required Performance Level, rather than quietly choosing Category 0.
6. Confirmed that every critical digital input is wired fail-safe (normally closed).
7. Issued the I/O list to the systems integrator **at the same revision as the schematics**, with a transmittal, so the code is written against the board that is actually being built.

> **Point 7 is a genuine failure mode.** The integrator writes code from the I/O list. If the board goes to Rev C and the integrator still has Rev B, you find out at FAT when an input does not do what the program expects — and it is expensive, because by then the board is wired. Document control is not administration; it is how you stop this.

---

**Next:** [Stage 4 — Terminations](04-TERMINATIONS.md)
