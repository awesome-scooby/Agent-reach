# 16 — THE STORY OF A START COMMAND

**One command, traced end to end, touching every document in the package.**

---

## Why this document exists

The package is organised by *document type* — SLD, schematics, terminations, BOM. That is how it gets produced, but it is a terrible way to explain it, because nobody thinks in document types. They think in **what happens**.

This document runs the other way. It follows a single start command from an operator's click to water actually moving, and names the document that defines each step as it passes through.

Three uses:

1. **It is the best single explanation of the package.** If you can narrate this, you have demonstrated that you understand the whole thing as a system rather than as a stack of drawings.
2. **It is how you check your own understanding.** Any step you cannot narrate is a gap.
3. **It is how fault-finding actually works.** §4 runs the same trace backwards to diagnose a pump that will not start.

---

## 1. The state before the command

It is 04:10. The station is idle.

| Thing | State | Where it is defined |
|---|---|---|
| Wet well level | 3.2 m, rising | `LIT-101` → AI-00, I/O list |
| Both pumps | Stopped, healthy, selectors in **REMOTE** | SCH-0101, SCH-0111 |
| Duty pump | P-101 (fewer accumulated run hours) | Functional description, duty rotation |
| MOV-101 discharge valve | Closed | ZSO/ZSC-101 → DI-25/26 |
| E-stop circuit | Healthy | KS-01 aux → DI-32 |
| 24 V DC system | Both PSUs healthy, all six ECP groups live | SCH-0030 |
| Network | PLC, both drives, meter, RIO-01 all reachable | SCH-0301 |
| SCADA | Showing the station green, "AUTO" | Integrator's scope |

---

## 2. The trace — fourteen steps

### Step 1 · The demand appears

The wet well level crosses the start setpoint. Nobody clicked anything — the demand is physical. The level transmitter LIT-101 is a 2-wire loop-powered device sitting in a 4–20 mA loop, regulating the loop current to represent the level.

At 3.2 m on an 0–10 m range it is drawing:

```
4 + (3.2 / 10) × 16 = 4 + 5.12 = 9.12 mA
```

> **Documents:** `14-CORE-CONCEPTS.md` §9 (how the loop works) · I/O list AI-00 · cable schedule C-0201 · Design basis §1.9

---

### Step 2 · The signal reaches the board

That 9.12 mA travels up a single individually-screened pair, C-0201, from the field to the MCC.

The **screen is earthed at the MCC end only**, on the insulated bar XS. If it were earthed at both ends, the potential difference between the two earth points would drive circulating current along the screen and couple noise straight into the pair — and the level reading would jump around. FAT test E-35 proved the screen bar is bonded at one point only, and that is exactly the defect FD-003 found.

> **Documents:** TRM-0401 · `04-TERMINATIONS.md` §4.4 · FAT E-35 · Punch list FD-003

---

### Step 3 · It lands on a terminal, not on a module

The pair terminates on **X4:001 and X4:002** — **disconnect-type** terminals, specifically so a technician can break the loop and inject a calibrated 4–20 mA signal without unwiring anything.

No field wire in this board lands directly on a PLC module. Ever. The module can then be replaced without disturbing field wiring, and every signal has a physical test and disconnection point.

> **Documents:** Termination schedule X4:001/002 · `04-TERMINATIONS.md` §4.2.1 · BOM item J04

---

### Step 4 · Loop power, from the right group

The 24 V that powers that transmitter comes from **ECP4**, the analogue group — deliberately *separate* from ECP2 and ECP3, which feed the field digital inputs and outputs.

Why: if a field digital output shorted and tripped its protector, every analogue loop on the same group would go dark simultaneously. The operator would lose level, flow *and* pressure at the exact moment something was going wrong.

> **Documents:** SCH-0030 · `03-SCHEMATICS.md` §3.3 · Design basis §1.5

---

### Step 5 · The PLC reads it

The signal enters module `5069-IF8`, slot 7, channel 0. On the PLC's next scan it is copied into the input image table and scaled to engineering units:

```
((9.12 − 4) / 16) × 10 = 3.2 m
```

The PLC also checks the loop is alive. Below about 3.6 mA it raises a **live-zero fault** — because a healthy loop never reads zero, a reading of zero means a broken wire. That detection is what FAT test K-81 verified.

> **Documents:** I/O list AI-00 · SCH-0203 · FAT K-81 · `14-CORE-CONCEPTS.md` §9.3

---

### Step 6 · The PLC decides P-101 is duty

Duty rotation is on accumulated run hours. P-101 has fewer, so it is duty; P-102 is standby.

This logic lives in the **integrator's program**, written against the functional description and the I/O list. It is not our code — but it *is* our I/O list, and it must be at the same revision as the board. Defect FD-004 happened precisely because the integrator had an earlier revision.

> **Documents:** Functional description · I/O list · `06-PROCUREMENT-AND-ENGINEERING-CONTROL.md` §6.6 · FAT FD-004

---

### Step 7 · Ten permissives are checked

Before any run command is issued, every one of these must be true:

| # | Permissive | Where it comes from | Current state |
|---|---|---|---|
| 1 | E-stop circuit healthy | KS-01 aux → DI-32 → X3:101 | ✔ |
| 2 | Q11 closed, feeder available | Q11 aux → DI-00 → X3:020 | ✔ |
| 3 | Drive healthy | VSD-101 relay → DI-01 → X3:017 (**NC**) | ✔ |
| 4 | Thermistor relay healthy | KT101 → DI-05 → X3:013 (**NC**) | ✔ |
| 5 | Wet well above low setpoint | LIT-101 → AI-00 | ✔ 3.2 m |
| 6 | Low-low float not tripped | LSLL-101 → X3:021/022, **hardwired + monitored** | ✔ |
| 7 | Seal water flow proven | B101-SEAL → DI-06 (bypass timer on start) | *bypassed for now* |
| 8 | **Discharge valve open** | ZSO-101 → DI-25 | ✘ **closed** |
| 9 | Selector in a valid position | S101-LOR → DI-03 / DI-04 | ✔ REMOTE |
| 10 | No unacknowledged latched trip | PLC | ✔ |

**Permissive 8 fails.** The valve is closed, so the pump does not start yet.

Two things worth noticing:

- **Critical inputs are wired normally closed** (3, 4, 6). A broken wire opens the circuit and reads as a *fault*, not as *healthy*. Fail-safe by wiring, not by trusting code. FAT test K-83 proves it by disconnecting the wire and confirming it reads FAULT.
- **Both selector positions are read separately** (9). One input can only tell you two things and cannot tell you it is broken. Two inputs distinguish Local, Remote and Off — and if both read true, that is a selector fault and an alarm.

> **Documents:** SCH-0101 paths 01–07 · SCH-0201 · I/O list · FAT I-66a–h, K-83

---

### Step 8 · The valve is commanded open

The PLC energises DO-06 → an interposing relay → the open command to MOV-101, out through X3:085 on cable C-0142.

The actuator is a **vendor package** with its own reversing starter, torque and limit switches. Our scope is a protected supply (Q17, MPCB 1.6–2.5 A) and the control interface. That interface was TQ-010, and it had to be resolved before the schematics could be finalised — hardwired open/close/stop with limit feedback, as it turned out.

One detail to be able to explain: some of the actuator wiring is **orange**. Under AS 60204.1, orange marks a conductor that stays live when the board's own isolator is opened, because it is fed from somewhere else. That is why the board carries a **"multiple supplies"** warning label — and why the label being missing was a genuine Category B safety defect at FAT (FD-006c), not a cosmetic one.

> **Documents:** SLD Q17 · SCH-0141 · TQ-010 · `03-SCHEMATICS.md` §3.2 · FAT FD-006c

---

### Step 9 · The valve reports open

ZSO-101 closes. DI-25 goes true at X3:081. Permissive 8 is now satisfied, and all ten are true.

---

### Step 10 · The run command goes out — hardwired

The PLC energises **DO-00**. That drives interposing relay **KA101**, whose contact closes the hardwired run command into VSD-101 terminal 18, via X3:019.

Not over the network. Hardwired, deliberately.

The interposing relay is there to protect the output module from a field fault, to give a volt-free contact, and to give a visible LED and a manual test lever for fault-finding. The cost is a component, some space and a few milliseconds — worth it here, possibly not on a high-speed machine.

> **Documents:** SCH-0101 path 08 · I/O list DO-00 · BOM item J01 · `14-CORE-CONCEPTS.md` §10.3

---

### Step 11 · The speed reference goes out — also hardwired

The PLC's PID controller compares measured discharge flow (FIT-101) against the SCADA setpoint and computes a speed demand. That goes out as **4–20 mA from AO-00**, through disconnect terminals X4:031/032, to drive terminals 53/55.

**Why hardwired when the drive is on EtherNet/IP anyway?** Because a network fault should not leave a duty pump at an unknown speed, and because fault-finding a 4–20 mA loop at 2 a.m. is a multimeter job rather than a laptop-and-configuration-software job.

**The counter-argument is real and you should say it:** all-comms is cheaper, gives far richer diagnostics, and modern drive networks are reliable. Many utilities now specify comms-only. This is a client standards question, not an absolute. FAT test P-115 proved the design decision works — disconnect the network, and hardwired control still functions with a comms-fail alarm raised.

The drive is also configured for **live-zero response**: if the reference is lost, hold last speed and alarm, rather than ramp to zero. A broken wire should not stop the station instantly.

> **Documents:** SCH-0204 · Design basis §1.8 · FAT O-106, P-115

---

### Step 12 · Inside the drive

The drive receives the run command and a speed reference, and does three things:

1. The **rectifier** has already charged the **DC link** to around 560 V DC.
2. The **inverter** starts switching its six IGBTs with **PWM**, synthesising a rising frequency and — following the V/f relationship — a proportionally rising voltage.
3. The motor's own inductance smooths those voltage pulses into approximately sinusoidal current, and the motor accelerates.

**Two consequences arrive at this exact moment:**

- The rectifier starts drawing current in pulses, injecting **5th, 7th, 11th and 13th** harmonic current back toward the point of connection. That is what TQ-006, the harmonic assessment, is about.
- The inverter's fast voltage edges drive high-frequency common-mode current down the motor cable. The screen, terminated **360° at both ends** via EMC glands, gives that current a defined path home instead of letting it find its own way through the building steel and every instrument cable it passes.

Also at this moment, **STO is not active** — the safety relay's outputs are energised, holding the drive's STO inputs live, which is what *permits* the drive to produce torque at all. STO is a permission that is removed, not a command that is sent.

> **Documents:** `14-CORE-CONCEPTS.md` §4 · SLD Q11 · SCH-0040 · TQ-006

---

### Step 13 · Torque, and the motor turns

The stator's rotating field turns at synchronous speed. The rotor, lagging by a few percent of **slip**, produces torque — and *only* produces torque because it is slipping.

Current rises to locked-rotor levels only very briefly, because the drive ramps frequency from near zero rather than applying full voltage at 50 Hz. **This is one of the real benefits of a drive that people forget to mention:** it eliminates the 6–8× starting current surge that a DOL start would produce.

The pump accelerates. Water starts moving.

> **Documents:** `14-CORE-CONCEPTS.md` §3

---

### Step 14 · The loop closes — and the checks that matter

Several things now come back:

| Feedback | Route | Why it exists |
|---|---|---|
| Drive running | Hardwired, DI-02, X3:018 | Confirms the drive actually started |
| Drive healthy | Hardwired, DI-01, **NC** | Broken wire reads as fault |
| Speed, current, power, DC bus, fault codes, run hours | EtherNet/IP | Diagnostics and trending |
| **Actual flow** | FIT-101 → AI-01 | **The only thing that proves water is moving** |
| Running lamp | MCC door and LCS-101 | The operator and the fitter both see it |

**Seal water flow** is now checked for real — the start bypass timer expires and B101-SEAL must prove flow, or the pump trips.

And the cross-check that most people miss: **"commanded running but no flow."** The drive reports running, the current looks plausible, and no water is moving — a closed valve downstream, an airlock, a broken coupling, a blocked suction. None of those are visible to the drive, because the drive is doing exactly what it was told. Only comparing commanded speed against FIT-101, with a time delay, catches it.

> **Documents:** SCH-0201 · I/O list · `03-SCHEMATICS.md` §3.5.4 · Functional description

---

## 3. The same trace, in one breath

For when you have thirty seconds:

> "Wet well level rises. The transmitter regulates a 4–20 mA loop to represent it, comes up a screened pair earthed at one end, lands on a disconnect terminal, and gets read by the PLC. The PLC picks the duty pump on run hours and checks ten permissives — E-stop healthy, feeder available, drive healthy, thermistor healthy, level above setpoint, low-low float clear, seal water, discharge valve open, selector in a valid position, no latched trip. The valve permissive fails, so it commands the valve open first and waits for the limit switch. Then it energises a digital output into an interposing relay, which sends a *hardwired* run command to the drive, plus a *hardwired* 4–20 mA speed reference from a PID on discharge flow. Inside the drive, a rectifier feeds a DC link, and an inverter PWMs that into variable voltage and frequency — which is where the harmonics and the screened-cable requirement both come from. The motor slips, produces torque, and the pump accelerates. Then it all comes back: running and healthy hardwired, diagnostics over Ethernet, and flow from the mag meter — which is the only signal that actually proves water is moving."

**That is about 45 seconds and it demonstrates the whole package.** It is a better answer to "walk me through it" than reciting the document list.

---

## 4. Running it backwards — fault-finding

Same trace, opposite direction. **"P-101 won't start."** This is also how you demonstrate that the documentation is usable rather than decorative.

| Check | How | Document | If it fails |
|---|---|---|---|
| **1** | What does SCADA say is blocking it? | Alarm list | Should name the failed permissive directly — *unless* the description is wrong, which is exactly defect FD-004 |
| **2** | Selector position? | S101-LOR, DI-03/04 | Both true = selector or wiring fault, not an operational problem |
| **3** | Is Q11 closed? | Q11 aux, DI-00 | Tripped feeder. Why did it trip? |
| **4** | Drive healthy and no fault code? | Drive keypad, and EtherNet/IP diagnostics | Fault code points at the cause |
| **5** | E-stop circuit healthy? | KS-01 aux, DI-32; check the relay's own LEDs | **One channel open = a broken wire.** The relay detects the discrepancy and will not reset — that is dual channel working |
| **6** | Thermistor relay? | KT101, DI-05 | Motor hot — or the circuit is open. **FD-001 was this contact wired to NO instead of NC** |
| **7** | Level and low-low float? | AI-00, and X3:021/022 | Reading 0 mA = broken loop, not an empty well. That distinction is what live zero buys you |
| **8** | Valve open? | ZSO-101, DI-25 | Actuator fault, or a limit switch out of adjustment |
| **9** | Seal water proven? | B101-SEAL, DI-06 | Flush supply, or the switch |
| **10** | Is the DO actually energising the relay? | **Look at KA101's LED.** Then measure at X3:019 | Module output fault, relay coil, or wiring |
| **11** | Is the 24 V group live? | ECP status contacts, DI-41 | A tripped group. Which one, and what shorted? |

**Step 10 is where the design pays off.** The interposing relay has an LED and a test lever, the terminal is accessible and labelled, and the wire is ferruled at both ends with a number that tells you which drawing to open. A technician with a multimeter and the termination schedule can find this without a laptop and without calling anyone.

> **That is the argument for every terminal, ferrule and label decision in the package** — and it is a much better way to justify them than "good practice".

---

## 5. Where each document got used

Narrate the trace once and you have touched every deliverable:

| Document | Where it appeared |
|---|---|
| Design basis | Control philosophy, control voltage, permissive list |
| SLD | Q11, the drive, the motor, the earthing |
| SCH-0030 | Which ECP group powers what, and why they are separate |
| SCH-0040 | STO permitting the drive to run at all |
| SCH-0101 | Permissives, run command, interposing relay |
| SCH-0201/0203/0204 | Every I/O point |
| TRM-0401 | Terminals, disconnect type, screen earthing |
| Cable schedule | C-0201, C-0142, the motor cable |
| I/O list | The whole traceability chain |
| BOM | Interposing relay, disconnect terminals, EMC glands |
| TQ register | TQ-006 harmonics, TQ-010 actuator interface |
| FAT sheet | I-66, K-81, K-83, O-106, P-115, E-35 |
| Punch list | FD-001, FD-003, FD-004, FD-006c |
| Core concepts | The loop, the drive, slip, harmonics |

---

## 6. How to use this in an interview

**Do not recite all fourteen steps.** It is too long and it sounds rehearsed.

**Do** use it three ways:

1. **When asked "walk me through the project"** — give the thirty-second version in §3. It shows systems thinking rather than document recall.
2. **When asked about any single component** — you now have the context to answer *"where does that sit in the sequence"*, which is a much stronger answer than a definition.
3. **When asked "how would you fault-find this"** — §4 is the answer, and it is the question that most separates people who have understood a system from people who have read about one.

**The single best moment to deploy it:** when an interviewer asks something narrow — *"why an interposing relay?"* — answer the narrow question, then add *"and the practical payoff is at three in the morning: the technician can see the LED, throw the test lever, and measure at a labelled terminal with a ferruled wire that tells them which drawing to open. That's really why it's there."*

That connects a component to a human being, which is what engineering judgement sounds like.

---

**Next:** [Explaining it to other people](17-EXPLAINING-TO-OTHERS.md)
