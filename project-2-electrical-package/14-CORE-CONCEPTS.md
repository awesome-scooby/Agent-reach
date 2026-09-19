# 14 — CORE CONCEPTS

**The physics behind the decisions.**

---

## Why this document exists

Documents 01–13 tell you what a competent engineer decided. They do not tell you how to *derive* those decisions, which means the moment an interviewer asks one question deeper than the script, you are stuck.

This document is the layer underneath. It is pitched at **interview depth**: enough to answer confidently, derive the answer on paper in front of someone, and know where the derivation stops being trustworthy. It is not a textbook and it does not replace one.

**Every worked number here is arithmetic you can check yourself.** That is deliberate, and it is a different thing from the calculations I refused to fabricate — a cable size to AS/NZS 3008 depends on route length, installation method and grouping that nobody has confirmed, so inventing one would be dishonest. Deriving full-load current from kW is just algebra with stated assumptions, and being unable to do it in an interview looks far worse than doing it.

**Rule for every calculation in here:** state your assumptions out loud as you go, and finish with where the real number comes from.

---

## 1. Three-phase power, and where current figures come from

### 1.1 The relationship

For a balanced three-phase load, drawing **real power** from the supply:

```
P = √3 × V_LL × I × cos φ
```

- `P` — real power in watts, the power actually doing work
- `√3` — 1.732, from the geometry of three phases 120° apart
- `V_LL` — line-to-line voltage (415 V here, not 240 V)
- `I` — line current
- `cos φ` — power factor

A **motor** is rated by its *shaft output*, not its electrical input. So for a motor you also divide by efficiency:

```
I = P_shaft / (√3 × V_LL × cos φ × η)
```

### 1.2 Worked: where ~160 A comes from

The 90 kW transfer pump motor, at 415 V. Assume a typical 4-pole machine of that size: **η ≈ 0.945**, **cos φ ≈ 0.87**.

```
I = 90 000 / (1.732 × 415 × 0.87 × 0.945)

  Denominator:  1.732 × 415      = 718.8
                718.8 × 0.87     = 625.4
                625.4 × 0.945    = 591.0

I = 90 000 / 591.0 = 152 A
```

So **roughly 150–160 A**, which is where the "~160 A" in the design basis comes from. The package quotes the upper end because a conservative figure is the safer one to carry into a provisional feeder selection.

Do the 75 kW original the same way (η ≈ 0.94, cos φ ≈ 0.86): `75 000 / (718.8 × 0.86 × 0.94) = 129 A` → ~130–135 A. That matches the pre-change figures.

### 1.3 The transformer

Transformers are rated in **kVA** (apparent power) not kW, because the transformer doesn't care about your power factor — it cares about current and voltage, which is what heats it.

```
I_fl = S / (√3 × V_LL) = 500 000 / (1.732 × 415) = 500 000 / 718.8 = 696 A
```

That is the 695 A quoted throughout the design basis.

### 1.4 kW, kVA, kVAr — say it in one line

- **kVA** is what the supply has to *carry*.
- **kW** is what actually does *work*.
- **kVAr** is the reactive component, shuttled back and forth, doing no work but occupying capacity.
- `cos φ = kW / kVA`.

### 1.5 The honest ending

> *"That gets me to roughly 150 amps, but I'd never leave it there. The nameplate is the number — efficiency and power factor vary between manufacturers and between frame sizes, and for a VSD feeder the number I actually need is the **drive's input current** from the drive manual, which isn't the same as the motor's full-load current anyway."*

**Say that last sentence.** It is the difference between doing arithmetic and understanding what the arithmetic is for.

---

## 2. Fault current — what it actually is

### 2.1 The idea

A short circuit removes the load from the circuit. The only thing left limiting the current is the **impedance of the supply path**: the network, the transformer, and the cable. Take the impedance to near zero and the current goes very high — until a protective device interrupts it.

Fault current matters because it determines:

- **Icu** — the maximum fault current a breaker can interrupt at all
- **Ics** — what it can interrupt *and remain serviceable* afterwards
- **Icw** — short-time withstand: what a busbar can carry for a stated time without damage
- **Ipk** — the peak, which sets the **mechanical** forces the busbar bracing has to survive

### 2.2 Transformer impedance and what %Z means

A transformer's **%Z** (here 5 %) means: *apply 5 % of rated voltage to the primary with the secondary short-circuited, and rated current flows.*

Invert that. At **full** voltage with the secondary shorted, the current is `1 / 0.05 = 20×` rated.

```
I_sc = I_fl / (Z% / 100) = 696 / 0.05 = 13 900 A ≈ 13.9 kA
```

That is the figure quoted in the design basis as "transformer-only contribution".

### 2.3 Why the real number is different — and both ways

| Effect | Direction | Why |
|---|---|---|
| Upstream network impedance | **Lower** | The 11 kV side is not an infinite bus |
| Cable impedance from transformer to board | **Lower** | Every metre adds impedance |
| **Motor contribution** | **Higher** | A spinning induction motor briefly acts as a generator into the fault, typically ~4–6× its FLC, decaying over a few cycles |
| Future transformer upsize | **Higher** | Bigger transformer, lower impedance, more fault current |

That is why 25 kA was assumed against a 13.9 kA transformer-only figure: margin for motor contribution and future growth.

### 2.4 The line that matters

> *"Thirteen point nine kilo-amps is the transformer-only figure from the nameplate. It is not the design fault level. The design fault level comes from the client or the network operator, ideally from a study with real source impedance data, because the network contribution and the motor contribution both matter and I can't derive either from a nameplate. I assumed 25 kA, I flagged it, and I wouldn't finalise a single breaker rating without it in writing."*

---

## 3. The induction motor

### 3.1 How it turns

Three-phase currents in the stator windings, 120° apart in time and 120° apart in space, produce a **rotating magnetic field**. That field induces current in the rotor bars (hence *induction*), the induced current produces its own field, and the two fields drag the rotor around.

**Synchronous speed** — the speed of the rotating field:

```
N_s = 120 × f / p          where p = number of poles

4-pole at 50 Hz:  120 × 50 / 4 = 1500 rpm
2-pole at 50 Hz:  120 × 50 / 2 = 3000 rpm
```

### 3.2 Slip — and why the motor *must* run slower

If the rotor ran at synchronous speed, it would see no relative motion, no changing flux, no induced current, no torque. **An induction motor only produces torque because it is slipping.**

```
slip = (N_s − N_rotor) / N_s
```

Typically 1–3 % at full load. A 4-pole 50 Hz machine therefore runs around 1455–1485 rpm, never 1500.

**More load → more slip → more induced rotor current → more torque.** That is the self-regulating mechanism, and it is why motor current rises with load.

### 3.3 Locked rotor — why DOL draws 6–8× full-load current

At standstill, slip = 1. The rotor is effectively a **short-circuited secondary of a transformer**, and the only thing limiting current is the leakage impedance of the machine. So a direct-on-line start draws typically **6–8× FLC** until the rotor accelerates and slip falls.

Two consequences you should be able to name immediately:

1. **Supply disturbance.** 8 × 160 A = 1280 A for a second or two. On a weak supply that is a visible voltage dip — lights flicker, other equipment misbehaves. This is one reason large motors are not started DOL.
2. **Contactor duty.** The contactor has to *make* against that current. This is exactly why **AC-3** exists as a utilisation category: it is defined for starting and switching off a running squirrel-cage motor, accounting for making against locked-rotor current. **AC-1** is for non-inductive loads and gives a much higher rating for the same contactor. Sizing a motor contactor on its AC-1 rating is a destructive error.

### 3.4 Cooling — the point that connects to the thermistor argument

A standard TEFC (totally enclosed, fan cooled) motor has a fan **on its own shaft**. Cooling airflow therefore falls with speed — and roughly with the square of it, since fan flow behaves like any other rotodynamic machine.

So a motor running at 30 % speed on a drive has dramatically less cooling than at full speed, while still potentially producing substantial torque and losses.

**This is the whole argument for the independent PTC thermistor relay.** The drive's thermal model infers winding temperature from current and time against an assumed thermal characteristic. It does not know the fan is delivering a fraction of the airflow the model assumes, and it does not know the fan has fallen off. Embedded thermistors measure actual winding temperature. For continuous low-speed operation the correct answer is a separately-driven forced-vent fan — which is a mechanical scope item, and one worth raising.

---

## 4. How a VSD actually works

This is the single highest-value mechanism in the package, because **four separate things you already assert are all consequences of it.**

### 4.1 The three stages

```
415 V AC  →  [ RECTIFIER ]  →  [ DC LINK ]  →  [ INVERTER ]  →  variable V and f
  3-phase       6 diodes        capacitors      6 IGBTs           to the motor
                                 + choke        switched by PWM
```

1. **Rectifier.** Six diodes in a three-phase bridge convert AC to DC. Each diode conducts for roughly a third of a cycle — current is drawn in **pulses**, not sinusoidally.
2. **DC link.** Capacitors smooth the rectified DC into a stiff bus, typically around 560–580 V DC on a 415 V supply. A **choke** (inductor) is usually added, either on the AC input or in the DC link, to limit the rate of rise of the charging current pulses.
3. **Inverter.** Six IGBTs switch the DC bus on and off very fast (typically 2–8 kHz) to synthesise an AC output of any voltage and frequency. This is **PWM** — pulse width modulation. The motor's own inductance smooths those pulses into something approximately sinusoidal in *current*, even though the *voltage* at its terminals is a train of sharp-edged pulses.

**V/f.** To keep the magnetic flux in the motor roughly constant, voltage is varied in proportion to frequency — so at 25 Hz the drive delivers about half the voltage. That is why a drive can produce full torque at low speed, and why "just change the frequency" is not enough on its own.

### 4.2 The four consequences — this is the payoff

| You already knew | Because of |
|---|---|
| **The drives cause harmonics** and need a harmonic assessment (TQ-006) | The **rectifier**. Drawing current in pulses rather than sinusoidally *is* harmonic distortion. A six-pulse bridge produces characteristic orders **6k ± 1**: 5th, 7th, 11th, 13th. |
| **A DC link / line choke is fitted** | The **DC link**. The choke limits the peak of those charging pulses, which reduces the harmonic distortion and is gentler on the capacitors. |
| **The motor cable must be screened, terminated 360° at both ends** | The **inverter**. PWM produces very fast voltage edges (high dv/dt). Those edges drive high-frequency common-mode current through the cable's capacitance to earth. The screen gives that current a defined low-impedance path home instead of letting it find its own way through the building steel and every instrument cable it passes. A pigtail is an inductor at those frequencies and largely defeats it. |
| **STO works, and is a hardware function** | The **inverter**. Safe Torque Off physically removes the gate drive signals to the IGBTs. With no gate drive, the transistors cannot switch, so no rotating field can be produced, so no torque. It is a hardware interruption, not a software command. |

### 4.3 Why STO is not isolation — now with the mechanism

STO stops the IGBTs switching. It does **not** open the rectifier, does not discharge the DC link, and does not disconnect the output terminals. The DC bus stays charged (and takes minutes to bleed down after power removal). The output terminals remain connected to that bus through the IGBT structure.

> *"Safe Torque Off removes the gate drive to the output transistors, so the drive can't produce a rotating field. It doesn't disconnect anything. The DC link is still charged and the motor terminals are still connected to it through the output stage. It's a safety function for stopping, not an isolation method, and it doesn't replace the lockable isolator at the motor."*

### 4.4 Long motor cables — reflected wave

A PWM edge travelling down a cable meets an impedance mismatch at the motor terminals and reflects. The reflected wave can superimpose on the incoming one and produce a voltage at the motor terminals approaching **twice** the DC bus voltage. Repeated thousands of times a second, that stresses the winding insulation and eventually fails it.

This is why every drive manual states a **maximum motor cable length**, screened and unscreened, and why exceeding it requires a dv/dt filter or a sine filter. It is also why "the route was longer than the drawing said" is a real and expensive problem.

---

## 5. Why variable speed on a pump — the affinity laws

### 5.1 The relationships

For a given pump, changing speed:

```
Flow        Q₂ / Q₁ = (N₂ / N₁)
Head        H₂ / H₁ = (N₂ / N₁)²
Power       P₂ / P₁ = (N₂ / N₁)³      ← this one is the whole argument
```

### 5.2 Worked — and this is the number to have ready

Run the pump at **80 %** speed:

```
Flow  = 0.80        → 80 % of flow
Head  = 0.80²= 0.64 → 64 % of head
Power = 0.80³= 0.512 → 51 % of power
```

**A 20 % speed reduction gives you roughly a 49 % power reduction.** At 50 % speed it is 0.5³ = 12.5 % of power.

On two 90 kW pumps running most of the year, that is the business case for the drives, and it is why water utilities specify variable speed.

### 5.3 The alternative, and why it is worse

The old way to reduce flow is to **throttle a valve** on the discharge. That works, but you are adding artificial resistance and burning the surplus energy as heat across the valve. The pump still turns at full speed and still draws close to full power.

> *"Throttling reduces flow by wasting energy. Varying speed reduces flow by not producing the energy in the first place."*

### 5.4 The honest caveats — say these, they matter

The affinity laws describe **the pump**. Your installation is a pump *plus a system*, and that changes things:

1. **Static head breaks the cube law.** The affinity laws apply along a *system curve that passes through the origin* — i.e. a system whose resistance is purely friction. A raw water transfer main usually has real **static lift**: you must produce a minimum head before any flow happens at all, regardless of speed. With significant static head, the operating point moves along a curve that does not pass through the origin, and the actual energy saving is **materially less** than the cube law suggests.
2. **There is a minimum speed.** Below it you cannot overcome static head, so flow goes to zero and you are just heating the water. There is also motor cooling (§3.4) and mechanical seal lubrication to consider. That is why the control philosophy clamps minimum speed rather than letting the PID wind down to zero.
3. **The drive itself has losses**, typically 2–3 % — which is exactly the heat load declared to the HVAC designer.
4. **Efficiency is not constant.** The laws assume it is. Move far from the best efficiency point and it isn't.

> **The answer that lands:** *"The cube law is why we're using drives — 80 % speed is about half the power. But I'd be careful quoting the cube law at a water job, because it only holds cleanly for a friction-dominated system. This main has static lift, so the real saving is less than the cube law implies and there's a minimum speed below which you get no flow at all. The actual number comes from the hydraulic model, which is the same model that changed the duty point and uprated the motors."*

That answer connects the physics to your own Stage 9 change. It is the strongest thing you can say about this project.

---

## 6. Harmonics

### 6.1 Where they come from

A linear load draws a sinusoidal current from a sinusoidal voltage. A **non-linear** load does not — it draws current in pulses or in some other non-sinusoidal shape. Any repeating non-sinusoidal waveform can be decomposed (Fourier) into a fundamental plus a series of harmonics at integer multiples.

### 6.2 Which harmonics, from which source — **this is the part people get wrong**

| Source | Harmonics produced | Sequence | Add in the neutral? |
|---|---|---|---|
| **Three-phase six-pulse rectifier** (your VSDs) | **6k ± 1**: 5th, 7th, 11th, 13th | Negative (5th, 11th), positive (7th, 13th) | **No** |
| **Single-phase** non-linear load (switch-mode PSUs, UPS input, LED drivers, electronic ballasts, anything on a GPO) | Strong **3rd**, plus 5th, 7th, 9th | 3rd and 9th are **zero-sequence** | **Yes** |

A *balanced* six-pulse bridge produces no significant triplen content. Unbalance produces some, but it is small.

**So the two arguments in this package are different arguments:**
- The **drives** are why a harmonic assessment was raised (TQ-006) — they inject 5th/7th/11th/13th back toward the point of connection.
- The **single-phase electronic load**, mostly via DB-01's lighting and GPO circuits, is why the neutral is full size.

### 6.3 Why triplens add — the derivation

Take the three phase fundamentals at 0°, −120°, +120°. Now look at their **third** harmonics — multiply each phase angle by three:

```
Phase A:  3 × 0°    =    0°
Phase B:  3 × −120° = −360°  ≡  0°
Phase C:  3 × +120° = +360°  ≡  0°
```

All three third harmonics are **in phase with each other**. They are zero-sequence. In a four-wire system the neutral carries the sum of the three phase currents: the fundamentals cancel in a balanced system, but the triplens **sum arithmetically** — in the worst case the neutral carries three times the per-phase triplen current.

That is why a reduced-size neutral on a board with heavy single-phase electronic load can overheat while every phase ammeter reads comfortably within rating.

Do the same arithmetic for the 5th: `5 × −120° = −600° ≡ +120°`. Not in phase. Doesn't add in the neutral. That is the check.

### 6.4 THDi vs THDv

- **THDi** — current distortion. This is what *your* load produces and injects.
- **THDv** — voltage distortion. This is what everyone connected to the network then *experiences*, and it is THDi flowing through the source impedance that creates it.

That is why a harmonic assessment needs **the network's impedance** and cannot be done from the switchboard alone. A stiff supply tolerates a lot of THDi with little THDv; a weak one does not.

### 6.5 Mitigation ladder — cheapest to most expensive

1. **Line reactor / DC link choke** — a few percent impedance. Modest improvement, cheap, always worth having.
2. **Passive harmonic filter** — tuned traps. Better, bulkier, load-dependent.
3. **12-pulse or 18-pulse drive** — phase-shifting transformer cancels lower orders. Effective, expensive, physically large.
4. **Active harmonic filter** — injects a cancelling current. Most effective, most expensive, needs its own cubicle and has a long lead time. **This is the risk carried in TQ-006.**
5. **Active front end drive** — near-sinusoidal input current built into the drive. Excellent, most expensive per drive.

---

## 7. Switching, protecting, isolating — three different jobs

People use these words interchangeably. They are not interchangeable, and this is an easy question to be caught on.

| Device | Switch load current? | Interrupt fault current? | Provide verifiable isolation? | What it is for |
|---|---|---|---|---|
| **Isolator / switch-disconnector** | Some can (on-load), some cannot | **No** | **Yes** — visible or verified contact gap, lockable | Making equipment safe to work on |
| **Contactor** | **Yes**, many times a day | **No** | **No — never** | Frequent, remote switching of a load |
| **Circuit breaker (MCB / MCCB)** | Yes, occasionally | **Yes** | Yes if rated as a disconnector and lockable | Protection, plus isolation |
| **MPCB** (motor protection CB) | Yes | Yes | Yes | Short-circuit *and* adjustable thermal overload in one device |
| **Fuse** | No | **Yes**, very fast and current-limiting | No | Pure protection, often needed for drive SCCR |
| **Thermal overload relay** | No | **No** | No | Protects the motor from sustained overload only |

### 7.1 The three points to be able to make

**A contactor is not an isolator.** It has a small contact gap designed for switching, not a verified isolating distance; it can weld closed; and it can be re-energised remotely by a control signal or a fault. Working on a motor behind nothing but a contactor is how people are killed.

**A thermal overload does not protect against short circuit.** It is a slow, thermal device. A short circuit is thousands of amps in milliseconds. The overload will still be thinking about it when the cable fails. That is why an overload is always paired with a short-circuit device — and why the pairing must come from the manufacturer's published **Type 1 / Type 2 coordination** tables rather than by matching current ratings.

**Type 1 vs Type 2:** after a short circuit, Type 1 permits damage — the contactor and overload may need replacing. Type 2 permits no damage beyond light contact welding that can be separated; the assembly stays serviceable. Type 2 costs more and is what you specify for anything you don't want to rebuild after a fault. **Mixing brands voids the declaration**, because the tables are tested pairs.

---

## 8. Earthing — three different conductors sharing a bar

| Conductor | Job | Connected |
|---|---|---|
| **Protective earth (PE)** | Carry fault current safely, hold exposed metal at earth potential, operate the protective device | **Both ends, always.** It is a safety conductor. |
| **Functional earth** | A reference for electronics to work correctly | Per the equipment's requirements |
| **Cable screen** | Keep interference out (instruments) or contain it (VSD) | **Depends entirely on which problem you're solving** — see §8.3 |

### 8.1 Earthing systems, one line each

- **TN-S** — separate neutral and protective earth throughout, bonded only at the source. Cleanest for electronics; no neutral current in the earth conductor.
- **TN-C-S** — combined PEN conductor for part of the run, split into N and PE at the installation. Common in distribution; a broken PEN is genuinely dangerous.
- **TT** — installation earth is a local electrode, independent of the supply earth. Earth fault loop impedance is high, so RCDs are essential.

The package assumes TN-S. It matters because it determines the neutral/earth bar arrangement, whether an earth-fault protection element is needed and how it behaves, and whether RCDs are the primary protection against indirect contact.

### 8.2 Earth fault loop impedance

For a fault to be cleared by an overcurrent device, enough current has to flow. Current is voltage divided by the impedance of the whole loop — source, phase conductor, fault, protective conductor, back to source.

```
I_fault = U₀ / Z_s
```

Too high a `Z_s` (long run, undersized protective conductor, poor connection) means too little fault current, which means the breaker takes too long, which means the exposed metal sits at a dangerous touch voltage for too long. **This is why disconnection times exist, and why an earth bolted through powder coat is a safety defect and not a workmanship nit** — it adds impedance exactly where you cannot afford it.

### 8.3 The screen question, resolved by asking what you're solving

**Instrument screen — MCC end only.**
The problem is *keeping interference out* of a small signal. The screen intercepts capacitively-coupled noise and takes it to earth. Earth it at **both** ends and you create a loop: any potential difference between the two earth points (and there always is one) drives circulating current along the screen, which couples into the signal pair. You have built the noise source you were trying to exclude.

**VSD motor cable screen — both ends, 360°.**
The problem is *containing* high-frequency common-mode current generated by PWM switching (§4.2). That current is going to return to the drive one way or another. The screen offers a defined, low-impedance path. Earth it at one end and there is no return path through the screen, so the current returns through the building structure and every cable tray it passes. The 360° termination matters because at those frequencies a pigtail is an inductor, not a conductor.

> *"They're different jobs. One is keeping noise out of a signal, the other is giving noise a path home. Neither is the protective earth conductor, which is always connected at both ends because it's a safety conductor."*

---

## 9. The 4–20 mA loop

### 9.1 How it works

The transmitter is not a voltage source. It is a **current regulator**: it actively controls the current flowing in the loop to represent its measurement, regardless of the loop's resistance (within limits).

```
      +24 V DC ──┬──────────── transmitter (+)
                 │                    │
                 │              regulates current
                 │                    │
                 └──── 250 Ω ── PLC ──┘  → 0 V
                    (input resistor)
```

**Two-wire, loop-powered** is the common case and the one used here: the same two wires carry the transmitter's power *and* its signal. That is possible because the transmitter's minimum output is 4 mA, which is enough to run its own electronics.

**Four-wire** transmitters have a separate supply and are used where the device needs more power than 4 mA can provide — analysers, some flow meters.

### 9.2 Why current and not voltage

Current is **the same everywhere in a series loop**. Voltage drops along a cable; current does not. Over a few hundred metres of field cable, a voltage signal degrades and a current signal does not.

### 9.3 Live zero — the whole point of starting at 4 mA

| Reading | Means |
|---|---|
| 4 mA | Measurement at 0 % |
| 20 mA | Measurement at 100 % |
| **< 3.6 mA** | **Broken wire, dead transmitter, or lost power** |
| **0 mA** | **Definitely a fault** |

If the range started at 0 mA, a broken wire and a legitimate zero reading would be *identical*, and you could not alarm on it. The live zero is what makes a failed loop detectable — and it is what FAT test K-81 checks.

### 9.4 Scaling — the arithmetic

```
Reading = ((I − 4) / 16) × span + zero
```

Wet well level transmitter, ranged 0–10 m, reading 13.2 mA:

```
((13.2 − 4) / 16) × 10 = (9.2 / 16) × 10 = 5.75 m
```

Being able to do that in your head at the 12 mA midpoint (= 50 % of span) is a small thing that sounds like experience.

### 9.5 Burden and compliance

Every resistance in the loop — the PLC input resistor, the cable, any indicator or barrier — is **burden**. The transmitter needs a minimum voltage across its own terminals to function, its **compliance voltage**. If burden is too high, the transmitter runs out of voltage and the loop becomes non-linear at the top of the range.

Rule of thumb check: `available = supply − (loop current × total burden)`. At 20 mA through 250 Ω that is 5 V used, leaving 19 V of a 24 V supply — comfortable. Add a 250 Ω indicator and a long cable and it becomes worth calculating.

---

## 10. The PLC

### 10.1 The scan cycle

A PLC does not work like a normal program. It loops, continuously:

```
1. READ    — copy every physical input into an image table
2. SOLVE   — execute the program against that frozen image
3. WRITE   — copy the output image table to the physical outputs
4. HOUSEKEEPING — comms, diagnostics
   → repeat
```

**Two consequences worth knowing:**

- The program works on a **snapshot**. An input that changes mid-scan is not seen until the next scan. Very short pulses can be missed entirely — which is why a pulse output from a flow meter usually goes to a dedicated high-speed counter input, not an ordinary DI.
- **Scan time** (typically a few milliseconds) sets the worst-case reaction delay. For a pump station this is irrelevant. For a high-speed machine or a safety function it is not — which is one more reason the E-stop here does not depend on the PLC.

### 10.2 Sinking and sourcing

Defined by which way current flows at the terminal:

- A **sourcing** device supplies current out of its terminal (connects the load to +24 V).
- A **sinking** device accepts current into its terminal (connects the load to 0 V).

They must be complementary: a sourcing field device feeds a sinking input; a sourcing output drives a sinking load.

> **Honest flag:** vendors are genuinely inconsistent in how they use these words, and some label modules by the field device's behaviour rather than the module's. **Check the manual, draw the current path, don't assume.** Saying that out loud is better than confidently using the wrong convention.

### 10.3 Why interposing relays

A PLC output module drives a relay, which drives the field device, rather than driving the field device directly.

**For:** protects an expensive module from a field short or induced surge (a $15 relay fails instead of a $900 module); gives a volt-free contact that can switch a different voltage; gives a visible LED and a manual test lever for fault-finding.

**Against:** more components, more panel space, more things to fail, and slower than a solid-state output.

For a pump station it is the right call. For a high-speed machine it might not be. **Being able to state the against is what makes the for credible.**

---

## 11. What actually destroys a pump

You protect against these throughout the package. Know what you are protecting against.

### 11.1 Dry running

A mechanical seal has two very flat faces pressed together, separated by a microscopic film of the pumped liquid. That film **lubricates and cools** the faces. Run dry and the film goes: the faces heat, distort, and fail — often in minutes on a large pump.

That is why the low-low float is hardwired into the drive's external-fault input and not left to the PLC alone, and why FAT test I-67 proves it with the PLC in program-stop.

### 11.2 Cavitation

If the absolute pressure at the impeller eye falls below the liquid's vapour pressure, the water **boils**. Those vapour bubbles are carried into the higher-pressure region of the impeller and **implode**, each one a tiny shockwave against the metal. The result is a distinctive gravel-rattling noise, vibration, lost performance, and pitted impeller metal.

The controlling relationship:

```
NPSH available (from the system)  must exceed  NPSH required (from the pump), with margin
```

NPSHa is reduced by suction lift, friction in the suction line, high liquid temperature, and low atmospheric pressure. **NPSH is a mechanical/hydraulic design responsibility, not the electrical engineer's.** Knowing it exists, knowing what it causes, and knowing whose it is — that is the right amount for you.

### 11.3 Running against a closed discharge valve

With no flow, the pump churns the same liquid, and essentially all the input power becomes heat in a small volume of water. Temperature rises fast, and it can flash to vapour and wreck the pump.

That is why "discharge valve open" (ZSO-101) is a start permissive, and why a **"commanded running but no flow"** cross-check between commanded speed and FIT-101 is worth having: it catches a closed valve, an airlock, a broken coupling or a blocked suction — none of which the drive can see, because the drive is doing exactly what it was told.

### 11.4 Seal water

Some seals need an external flush for lubrication and cooling. Losing it is a fast seal failure, which is why seal water flow is a permissive — with a bypass timer, because you cannot prove flow before the pump starts.

---

## 12. IP ratings, decoded

`IP` + first digit (solids) + second digit (liquids).

| 1st digit | Protects against | | 2nd digit | Protects against |
|---|---|---|---|---|
| 0 | Nothing | | 0 | Nothing |
| 1 | > 50 mm (back of hand) | | 1 | Dripping water, vertical |
| 2 | > 12.5 mm (finger) | | 2 | Dripping, enclosure tilted 15° |
| 3 | > 2.5 mm (tool) | | 3 | Spraying water, up to 60° |
| 4 | > 1 mm (wire) | | 4 | Splashing from any direction |
| 5 | Dust protected | | 5 | Water jets |
| 6 | **Dust tight** | | 6 | **Powerful water jets** |
| | | | 7 | Temporary immersion |
| | | | 8 | Continuous immersion |

**Reading the package's ratings:**

- **IP42** (MCC-01, indoor switchroom) — keeps a wire out, copes with dripping water at a slight tilt. Appropriate for a clean, dry, air-conditioned room, and it allows ventilation, which matters when you are dissipating several kilowatts.
- **IP66** (LCS-101/102 in the pump hall, RIO-01 outdoors) — dust tight and rated for hose-down. A pump hall gets washed.

**The point:** higher is not automatically better. IP66 on the MCC would seal in the drives' heat and force forced cooling you do not otherwise need. IP is chosen against the actual environment, not maximised.

---

## 13. Forms of separation, decoded

AS/NZS 61439.2 defines how much internal barriering an assembly has. Increasing form = more separation = safer to work on live or adjacent sections = more expensive to build.

```
Form 1   No internal separation at all.

Form 2   Busbars separated from the functional units.
         2a — terminals not separated from busbars
         2b — terminals separated from busbars

Form 3   Busbars separated from functional units,
         AND functional units separated from each other.
         3a — terminals not separated from busbars
         3b — terminals separated from busbars  ← THIS PACKAGE

Form 4   As Form 3b, plus terminals separated from each other.
         4a — terminals in the same compartment as their functional unit
         4b — terminals in separate compartments
```

**What Form 3b buys you here:** you can work on one feeder's terminals with the busbar chamber barriered off and the adjacent feeders separated, without exposing yourself to the whole board.

**What Form 4b would add:** each feeder's terminals in their own compartment. More cubicle, more cost — and this is exactly why "Form 3b assumed" sits in the design basis as **TQ-001**. Many water utilities mandate Form 4b.

> **Flag it honestly:** the sub-form (a/b) definitions are frequently misquoted, including in vendor literature. Read them from the standard, and confirm the interpretation with the manufacturer before pricing. *"I'd check the exact sub-form definition against the standard rather than trust my memory"* is a better answer than a confidently wrong recitation.

---

## 14. Scale — answering "how big a job was this?"

No dollar figures, for the reasons in `00-CLAIM-INTEGRITY.md`. But you should be able to describe the shape of it.

| Dimension | This package |
|---|---|
| Programme, design start to dispatch | ~22 weeks, including ~2–3 weeks lost to CR-001 |
| Critical path | The VSDs, at 14–16 weeks |
| Cubicles | 5 |
| Feeders | 12, including 2 fitted spares |
| I/O points | 40 DI, 14 DO, 6 AI, 2 AO + 12 at the remote node |
| Terminals | ~500 across seven rails |
| Drawings | SLD, GA, ~12 schematic sheets, 5 termination sheets, label schedule |
| Registers | 10 |
| FAT | 127 tests, 3 days, 8 punch-list items |
| People involved | Client PM and ops rep, designer, drafter, PE, buyer, workshop supervisor, wireman, integrator, several vendors |

> *"It's a five-cubicle board, twelve feeders, about sixty I/O points and five hundred terminals, on roughly a twenty-two week programme with the drives on the critical path at sixteen weeks. Not a big job by MCC standards — big enough that everything has to be controlled properly, small enough that one engineer can hold all of it in their head."*

---

## 15. What you still cannot derive — the honest boundary

Everything above lets you *reason*. None of it makes you qualified to *produce* the following, and the boundary has not moved:

| Still not yours | Why the physics above doesn't get you there |
|---|---|
| The design fault level | Needs real network source impedance data you do not have |
| A protection coordination study | Needs device characteristic curves, the study software, and judgement about grading margins |
| Arc flash incident energy | IEEE 1584 methodology, real system data, specialist |
| A cable size to AS/NZS 3008.1.1 | Needs confirmed route length, installation method, grouping, ambient — none confirmed |
| Required or achieved Performance Level | Risk assessment, then reliability data per device and an ISO 13849-1 calculation |
| AS/NZS 61439 design verification | The manufacturer's, by test or assessment — not something you calculate |
| The hydraulic duty point | The hydraulic model, which is the mechanical consultant's |

> *"Understanding the physics means I can check someone's work, ask the right question, and know when an answer smells wrong. It doesn't make me the person who signs the study."*

---

**Next:** [Glossary](15-GLOSSARY.md) · [The story of a start command](16-START-COMMAND-TRACE.md) · [Explaining it to other people](17-EXPLAINING-TO-OTHERS.md)
