# STUDY GAPS — WHAT TO CLOSE BEFORE CLAIMING COMPETENCY

Ordered by what will hurt you fastest in an interview or on a job.

---

## Tier 1 — Close these before your next interview

### 1.1 AS/NZS 61439 — who verifies what

**Why it is first.** It is the standard the whole package is judged against, and the single most common misconception is that the *designer* verifies the assembly. They do not. **Design verification is the original manufacturer's responsibility**, by testing, comparison with a tested design, or assessment. It covers temperature rise, short-circuit withstand, IP, clearances and creepage, mechanical operation, EMC.

**What to be able to say:** the difference between design verification and routine verification; that forms of separation are defined in Part 2; what the assembly's rating plate must carry; and that the PE's job is to *obtain the manufacturer's verification evidence*, not to produce it.

**How to close it:** read the scope and verification clauses of AS/NZS 61439.1 and the forms of separation in 61439.2. Then ask any switchboard manufacturer to show you their design verification documentation for a standard enclosure system — most will, and seeing one real example is worth more than a week of reading.

---

### 1.2 Fault level, Icu, Ics, Icw and cascade

**Why.** You will be asked. It is the foundation of every protective device selection on the board.

**What to be able to explain without notes:**
- What prospective short-circuit current means and where it comes from
- **Icu** (ultimate breaking capacity) vs **Ics** (service breaking capacity — what it can break and remain serviceable) and why the difference matters operationally
- **Icw** (short-time withstand) and why it applies to busbars and to devices with a short-time delay
- **Ipk** and the mechanical forces that size busbar bracing
- **Cascade / back-up protection** — how an upstream device can allow a downstream device to be used above its own standalone Icu, and that this is only valid for **manufacturer-tested combinations from published tables**
- Why discrimination and cascade pull in opposite directions

**How to close it:** work through one manufacturer's coordination and cascade tables until you can use them. Schneider, ABB and Eaton all publish them. Take a specific incomer and a specific feeder and read off the answer. Do it twice.

---

### 1.3 Motor protection and utilisation categories

**What to be able to explain:**
- **AC-1 vs AC-3** — and why sizing a contactor on its AC-1 rating for a motor load is destructive
- **Type 1 vs Type 2 coordination** between the short-circuit device and the contactor/overload, and why you must select the pair from the manufacturer's published tables rather than matching current ratings
- How a thermal overload relay actually works, and its limitations
- Why a VSD feeder's upstream device does not protect the motor
- PTC thermistors vs PT100 vs the drive's thermal model

**How to close it:** read one manufacturer's motor starter selection guide end to end. They are written to teach this and they are free.

---

### 1.4 AS/NZS 3008.1.1 — cable selection

**You do not need to become a designer. You need to be able to check one.**

**What to be able to do:** take a stated load, installation method, ambient, grouping and route length, and follow the tables to a size. Do it for three different cases. Understand which derating factors apply and why.

**What to be able to explain:** the four constraints — current-carrying capacity, volt drop, fault withstand (the adiabatic check for disconnection time), and earth fault loop impedance — and that the largest of them governs.

**How to close it:** get access to AS/NZS 3008.1.1 and work three examples by hand. A spreadsheet answer you cannot reproduce by hand is not understanding.

---

### 1.5 The drive manual

**Why.** Half the technical answers in this package come out of a drive manual, and being able to navigate one is directly employable.

**What to find in a real manual, for a specific drive:**
- Recommended fuse and circuit breaker, and the declared SCCR
- Input current vs motor current
- Maximum motor cable length, screened and unscreened, and when a dv/dt or sine filter is required
- Heat dissipation figures and required clearances
- **STO terminal designations and the certified safety data**
- Live-zero / reference-loss configuration options
- Motor thermal protection parameters and external thermistor input
- The type-code structure

**How to close it:** download the Danfoss FC202 design guide, or the equivalent for whatever drive your target employer uses, and find every item above. This is a two-hour exercise and it will pay for itself in the first interview.

---

## Tier 2 — Close within a month

### 2.1 Functional safety fundamentals

You do not need to be able to perform an ISO 13849 calculation. You need to understand the framework well enough to know when to escalate.

- AS 4024.1 / ISO 12100 risk assessment → **required** Performance Level (PLr)
- ISO 13849-1 → **achieved** PL, from category, MTTFd, diagnostic coverage and common cause failure
- Categories B, 1, 2, 3, 4 and what architecture each implies
- Stop categories 0, 1, 2 under AS 60204.1 and when each is appropriate
- **Safe Torque Off — what it is, what it certifies, and emphatically that it is not isolation**

**How to close it:** read one safety relay manufacturer's introductory guide (Pilz, Sick and Schmersal all publish good ones). Do not attempt to self-certify anything.

---

### 2.2 Harmonics

**Why.** You raised it as a risk in this package and did not drive it to closure, and you said so in your Q10 answer. Be able to talk about it properly.

- Why six-pulse rectifiers produce 5th, 7th, 11th, 13th harmonics
- Why triplens add in the neutral — **be able to explain the phase relationship, not just state the fact**
- THDi vs THDv and why the distinction matters
- Mitigation options and their trade-offs: line reactors, DC link chokes, 12-pulse, passive filters, active harmonic filters, low-harmonic drives
- Why a harmonic assessment needs the actual network impedance and cannot be done from the board alone

---

### 2.3 Earthing systems

- TN-S, TN-C-S, TT — the actual differences, not just the letters
- Why it determines the neutral/earth bar arrangement, the earth-fault protection strategy and RCD applicability
- Earth fault loop impedance and disconnection times under AS/NZS 3000
- Functional earth vs protective earth vs screen earth — three different things that share a bar

---

### 2.4 Australian industry documents

- **WSAA** codes, and whether your target employers work to them
- The major water utilities' electrical design standards — several are publicly available, and reading one shows you what a client standard actually mandates: brands, spare capacity, labelling, terminal types, IP ratings, documentation
- **Read one end to end.** It will change how you think about TQ-001 in this package.

---

## Tier 3 — Build over time, mostly by doing

### 3.1 Drafting tools

You have built illustrative drawings, not CAD deliverables. **Say so.**

- AutoCAD Electrical or EPLAN — most employers use one
- Understand what the software does that manual drafting cannot: automatic cross-referencing, contact tallying against a device database, terminal strip generation, BOM extraction
- **Note the irony worth mentioning in an interview:** the auxiliary contact shortfall you found manually in Stage 5 is exactly the error EPLAN's contact management is designed to prevent. Knowing the manual check is what lets you trust — or distrust — the automated one.

### 3.2 Workshop exposure

The gap you named in Q10. There is no substitute.

- Ask for workshop time in any role you take
- Watch a real FAT if you get the chance, even as an observer
- Learn to see a board rather than read one

### 3.3 Commercial

- Variations, claims, and the difference between a change and a variation
- Estimating, and why your inability to price this package is a real limitation
- Programme and critical path in practice

### 3.4 Protection coordination

Not to perform studies — to read one.

- Time-current curves and how to read discrimination off them
- What software produces (ETAP, PowerFactory, SKM) and what it needs as input
- Enough to check that a study's inputs match your board

---

## The things in this package you must be able to redraw from memory

Test yourself with a blank sheet and no notes:

- [ ] The SLD, at block level, with every device named and its purpose stated
- [ ] The E-stop circuit, dual channel, with the single-fault behaviour explained
- [ ] The 24 V DC control power architecture, including why the groups are separated
- [ ] One VSD feeder, power and control, from busbar to motor
- [ ] The three BOM reconciliation passes and what each one catches
- [ ] The traceability chain from field device to SCADA tag
- [ ] The design change trace through all ten stages
- [ ] The list of things you cannot claim, and who owns each

**If any box is unticked, that section is not yours yet.**

---

## The one-line honest self-assessment

> "I understand the workflow and the documents properly. I can check a design, find what doesn't reconcile, manage a change and run a FAT procedure. I can't do a protection study, a cable calculation or a PL verification, and I know who does. What I need is workshop time and a senior engineer to check my work against."

That is an accurate description of a good graduate electrical project engineer, and it is a better thing to say than any amount of confidence you cannot support.
