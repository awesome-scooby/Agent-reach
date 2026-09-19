# 17 — EXPLAINING IT TO OTHER PEOPLE

**Five audiences, twelve hostile follow-ups, and the drills that prove you actually own it.**

---

## Why this document exists

`12-INTERVIEW-PACK.md` assumes a technical interviewer. That is the *last* person you talk to, not the first.

Before an engineer ever reads your CV, a recruiter has skimmed it in about twenty seconds and an HR screener has asked you to "tell me about yourself" on a fifteen-minute phone call. Neither of them knows what an MCC is. If you answer them the way you would answer a senior engineer, you do not reach the senior engineer.

This document fixes that, and then goes the other way: what to do when a technical interviewer pushes *past* your prepared answer.

---

## 1. The audience ladder

Five versions of the same project. **The mistake is using the wrong one**, and the most common failure is using version 4 on audience 1.

| # | Audience | What they actually want to know | Length | Jargon |
|---|---|---|---|---|
| 1 | **Recruiter** | Can I put this person forward without looking silly? | 20 sec | **None** |
| 2 | **HR / talent screener** | Are they real, are they honest, do they communicate? | 60 sec | Almost none |
| 3 | **Non-electrical hiring manager** (mech, civil, ops) | Do they understand *projects*? Will they be easy to work with? | 2 min | Concepts, not codes |
| 4 | **Electrical engineer** | Do they know what they're talking about? | 3–10 min | Full |
| 5 | **Senior / principal engineer** | Do they know what they *don't* know? | Varies | Full, plus boundaries |

---

### Version 1 — Recruiter (20 seconds, zero jargon)

> "I built a complete electrical design package for a water pump station — the electrical control system that runs the pumps. I took it all the way from the initial requirements through to factory testing and handover documentation. It's a self-directed project, not paid work, but it covers the full workflow an electrical project engineer would actually do."

**Rules:** no acronyms at all. Not MCC, not VSD, not PLC. "The electrical control system that runs the pumps" is enough. Say "self-directed" once so it never becomes a surprise later.

---

### Version 2 — HR screener (60 seconds)

> "It's a reference project I built myself, not paid work — I want to be clear about that up front.
>
> The scenario is a water utility replacing two big pumps at a treatment plant, and the electrical package that goes with it: the switchboard that powers and controls them, the control system, and the link back to the plant's monitoring system.
>
> I took it right through the lifecycle — working out the requirements, producing the drawings, building the bill of materials, ordering equipment, checking it during manufacture, running a factory acceptance test, and handing over the documentation.
>
> The reason I built it is that I could read an electrical drawing, but I couldn't explain how a drawing turns into a purchase order, then into a wired panel, then into something a client signs off. Now I can.
>
> And I was careful about limits. There are parts of a real job that need a specialist or a chartered engineer, and I've marked those as out of scope rather than pretending I did them."

**Why it works for HR:** it is honest, it explains *motivation* (which is what they are assessing), and it demonstrates self-awareness — which screens as maturity.

---

### Version 3 — Non-electrical hiring manager (2 minutes)

This person may be mechanical, civil, or an operations manager. They understand projects, interfaces and schedules. They do not want electrical detail and they will switch off if you give it.

> "Two pumps get replaced, and the electrical package is everything that powers and controls them — a switchboard about the size of a wardrobe, with the protective devices, the variable speed drives, and a small computer that runs the automatic sequence.
>
> What I got out of building it wasn't really the electrical content. It was the **interfaces**.
>
> The pump vendor's data arrives late — always — and my drive and cable selection depend on it. The mechanical model changed the duty point after my design was frozen, which uprated the motors and cost about two to three weeks. The air conditioning designer needs a heat load figure from me that nobody will ever ask for, and if I don't send it, the switchroom is undercooled. And the transformer feeding my board belongs to someone else and also feeds loads that aren't on my drawings — so when the motors got bigger, the question worth asking wasn't whether *my* equipment still coped, it was whether *their* transformer did.
>
> That last one is the example I'd point to. Checking my own scope is easy. Noticing that someone else's equipment might now be the constraint is the part that actually saves a project."

**Why it works:** every point is an interface or a schedule consequence — the two things a project manager from any discipline cares about. The transformer story lands with *anyone*.

---

### Version 4 — Electrical engineer

Use `12-INTERVIEW-PACK.md`: the 3-minute technical explanation, or the 10-minute presentation.

---

### Version 5 — Senior engineer

Same content as version 4, but **lead with the boundaries rather than saving them for the end**. A principal engineer is not assessing whether you can recite a design. They are assessing whether you are safe to let near a job.

> "Before I walk you through it — the things I deliberately didn't do are probably more relevant to you than the things I did. There's no fault level study, so every breaker rating in there is provisional against an assumed 25 kA. There's no coordination study, so discrimination is unverified, and I recorded that as a deviation at FAT rather than ticking it. There's no cable calculation, so the cable sizes are placeholders. And the E-stop circuit is the architecture you'd normally build for PLd, but I haven't got a risk assessment or an ISO 13849 calculation, so I won't call it PLd.
>
> With that said, here's what it does cover…"

**That opening will get you taken seriously immediately.** It is the single highest-leverage thirty seconds in this entire package.

---

## 2. Analogies — the ones that work, and the ones that mislead

Analogies are how you reach audiences 1–3. A bad one costs you credibility with audience 4, so know which is which.

### Safe to use

| Concept | Analogy |
|---|---|
| **MCC** | "A wardrobe-sized cabinet that's the switchboard and the control system for a set of motors, all in one." |
| **VSD** | "A dimmer switch for a motor — except that unlike a light dimmer, slowing a pump down saves a *lot* more energy than you'd expect." |
| **Why variable speed saves energy** | "Halve the speed and you use about an eighth of the power. It's a cube relationship, not a straight line." |
| **PLC** | "A small industrial computer that reads sensors and operates equipment. Very reliable, very boring, very hard to crash — which is the point." |
| **SCADA** | "The screen in the control room that shows operators what's happening and lets them intervene." |
| **Permissive** | "A pre-flight checklist. Every item has to be true before it's allowed to start." |
| **FAT** | "You test it fully in the workshop, where it's on a bench and the spare parts are on a shelf, rather than on site where it's bolted to a wall and everything is two days away." |
| **Technical query** | "A written question to the client that says: here's what we've assumed, here's what it'll cost if the assumption is wrong, and here's the date we need an answer by." |
| **As-built drawings** | "Updating the drawings to match what was actually built — because in ten years the drawings are the only thing left." |
| **Reconciliation** | "Checking that the drawings, the parts list and the wiring all agree with each other. They usually don't, and finding that early is most of the job." |

### Use carefully

| Concept | Analogy | The catch |
|---|---|---|
| **Fault level** | "How much current the supply can dump into a short circuit." | Fine for non-engineers. With an engineer, be precise about Icu/Ics/Icw. |
| **Harmonics** | "Distortion — the equipment draws power in a choppy way rather than smoothly, and that ripples back into the network." | Do not extend it to audio distortion; it breaks down fast. |

### ⚠ Do not use

| Analogy | Why it's wrong |
|---|---|
| **"Voltage is like water pressure, current is like flow"** | It's a tired analogy that breaks immediately on anything real — and in a *water* interview it is actively confusing, because there is genuine water pressure and flow in the conversation. |
| **"The E-stop makes it safe to work on"** | **It does not.** This is the one analogy that could get somebody hurt. STO removes torque; it does not isolate. |
| **"A contactor is just a big switch"** | It leads straight to the idea that you can use one for isolation. You cannot. |
| **"The PLC is the brain"** | It sounds harmless, but it undercuts your own best design decision — the whole point of the hardwired dry-run trip is that safety and asset protection must work *when the brain is stopped*. |

---

## 3. Objection handling — twelve hostile follow-ups

You have model answers. This is what happens *after* them, when an interviewer decides to push.

---

**"This is all hypothetical. Why should I care?"**
> "Because the mechanics are the same whether the client is real or not. Reconciling a BOM against a schematic finds the same errors either way. What's missing is the commercial pressure and the difficult conversations, and I'm not claiming to have had those. What I'm claiming is that when I do, the engineering won't be the part I'm struggling with."

---

**"You said the fault level is an assumption. Isn't the whole design therefore worthless?"**
> "No — it's provisional, which is a normal state for a design at that stage. Every device rating is selected against the assumption with margin, the assumption is annotated on the drawing face, and the query is raised with a date and a consequence. That's how real packages run for the first few months. What would make it worthless is if the assumption were *unflagged* — then somebody downstream treats it as fact."

---

**"Anyone can copy a design from a textbook."**
> "They can, and a lot of what's in there is standard practice — I'd be suspicious of a graduate who claimed to have invented any of it. What's not copyable is the reconciliation, the change trace, and knowing which decisions weren't mine to make. Ask me why the neutral is full size and I'll tell you the physics and tell you why the drives *aren't* the reason, which is the part people get backwards."

---

**"Your drawings aren't CAD."**
> "They're not, and I wouldn't present them as production drawings. They're drawn to communicate intent and to be explained. I haven't used AutoCAD Electrical or EPLAN, and that's a genuine gap — though I'd note that the auxiliary contact shortfall I found by hand is exactly the error EPLAN's contact management is designed to prevent. Knowing the manual check is what lets you trust the automated one."

---

**"You've clearly written all this to look good."**
> "I've written it to be defensible, which is different. If I'd written it to look good there'd be a protection study and a set of cable calculations in there, because that's what would impress someone skimming it. There isn't, because I can't do them yet. The FAT record has a test marked as a deviation rather than a pass for the same reason."

---

**"Why 415 V and not 400 V?"** *(a small trap to see if you know local practice)*
> "415 V is the nominal three-phase distribution voltage in Australia — 240 V phase to neutral. IEC harmonisation puts it at 400/230 with a tolerance band that covers it, and equipment is generally rated 380–415 V, so the distinction rarely matters in practice. I'd use the client's own nomenclature on the drawings."

---

**"How do you know your BOM part numbers are right?"**
> "I don't, and I'd say that before you found one that's wrong. Catalogue numbers change and the coil-voltage and curve variants are the most commonly botched field in any switchboard BOM. That's exactly why every part number gets verified against the current catalogue and confirmed on the vendor quotation before a PO is raised — and it's why I compare quotations line by line, because suppliers substitute silently. I found an obsolete part that way."

---

**"You keep saying you'd escalate. Can you actually decide anything?"**
> "Yes — and the distinction matters. I stopped an unapproved substitution, that was my call. I corrected Local mode bypassing the dry-run permissive, my call. Holding the drive order against schedule pressure, my call, and it was unpopular for six weeks. What I *escalated* was a brand substitution on a client's twenty-year asset while their own standard was still an open query. That's not indecision, it's knowing whose asset it is."

---

**"Two or three weeks lost on that motor change sounds bad."**
> "It would have been eight to ten if the drives had been ordered and the cubicles finished. The reason it was two to three is that the order hadn't been placed, the build had been re-sequenced so the drive cubicles were last, and the gland plates were still undrilled. None of those decisions were made after the change arrived. That's the actual lesson — you don't respond to a late change, you make yourself able to absorb one."

---

**"What if I told you your E-stop design is wrong?"**
> "I'd want to know which part, genuinely. The thing I'd be least confident about is stop category — I've drawn Category 0, immediate removal of power, and there's a real argument that Category 1 is better on a 90 kW pump because an abrupt stop causes hydraulic surge. I flagged it as a query rather than deciding it, because it needs a risk assessment and a surge assessment and I have neither. If it's something else, tell me and I'll take it away."

---

**"You're a graduate. Why should I hire you over someone with five years?"**
> "You probably shouldn't, if the role needs five years. What I'd offer is that I've done the document work properly rather than superficially, so I won't need to be taught what a technical query is for or why the BOM has to be reconciled in three directions. And I'd rather be somewhere I'm checked than somewhere I'm trusted too early."

---

**"What's the worst mistake in this package?"**
> "Two. The first is that I originally wrote that the drives cause the triplen harmonics that justify the full-size neutral. That's wrong — a balanced six-pulse rectifier makes 6k±1, fifth, seventh, eleventh, thirteenth, and those don't add in the neutral. Triplens are zero-sequence and they come from the single-phase electronic load. The conclusion was right and the reason was wrong, and it was written on the drawing face.
>
> The second is that I let TQ-006, the harmonic assessment, stay open all the way to FAT. I identified it as the biggest technical risk and then didn't drive it to closure. If it comes back needing an active filter, that's another cubicle and a long lead."

**That answer is the strongest one in this document.** Volunteering a real error you found and corrected demonstrates something no polished answer can.

---

## 4. The teach-back protocol

Reading is not understanding. **Explaining out loud to someone who can interrupt you** is understanding.

**The method:**

1. Pick one concept — the E-stop circuit, or why the neutral is full size.
2. Explain it out loud, to a real person if possible, to a wall if not, **without notes**, in under two minutes.
3. **Record yourself.** You will hate it. Do it anyway.
4. Listen for these three failures:
   - **Jargon you can't unpack.** If you say "zero-sequence" and couldn't define it if stopped, you don't own it.
   - **Hedging.** "Sort of", "basically", "kind of" cluster exactly where understanding is thin. They are a diagnostic.
   - **Reciting.** If it sounds like the document, you are reading from memory rather than reasoning. Explain it a second time using *different words* — if you can't, you memorised it.
5. Then have someone ask you **"why?"** three times in a row. Most explanations survive one why and collapse on the third.

**Worked example of the three-why test:**

> **Why is the neutral full size?** Because triplen harmonics add in it.
> **Why do they add?** Because they're zero-sequence — the three phases' third harmonics are all in phase with each other.
> **Why are they in phase?** Because the fundamentals are 120° apart, and three times 120° is 360°, which is back to zero. So multiplying each phase angle by three puts them all at the same place.

Survives three. Now try:

> **Why is the breaker on a VSD feeder selected from the drive manual?** Because it protects the cable and the drive, not the motor.
> **Why doesn't it protect the motor?** Because the drive protects the motor — thermal model plus thermistors.
> **Why can't the breaker do it?** Because the drive is between them. The breaker only sees the drive's input current, which isn't the motor's current — the drive is producing a different frequency and voltage on the other side. A motor overload downstream of the drive doesn't necessarily show up as an overcurrent upstream of it.

That third answer is the one most people cannot give, and it is the one that proves you understand a drive rather than just repeating a rule.

---

## 5. Recall drills

The knowledge checks in the portfolio are **recognition** — pick the right answer from four. Your actual test is **recall** — produce it from nothing.

### 5.1 Whiteboard drills

Blank sheet, pen, no notes. Time yourself.

| # | Drill | Target | Pass condition |
|---|---|---|---|
| 1 | Draw the SLD at block level | 5 min | Every device named, every rating stated, and you can say why each exists |
| 2 | Draw the E-stop circuit | 3 min | Both channels, two NC contacts per E-stop, safety relay, STO to both drives, monitored reset, aux to PLC — **and explain what happens if one wire breaks** |
| 3 | Draw the 24 V DC architecture | 3 min | UPS, two MCBs, two PSUs, O-ring, six groups — and say why the groups are separate |
| 4 | Draw one VSD feeder, busbar to motor | 4 min | Breaker, reactor, drive, EMC gland, isolator, motor, thermistor loop |
| 5 | Draw the drive's three stages | 2 min | Rectifier, DC link, inverter — and name one consequence of each |
| 6 | Write the traceability chain | 1 min | Device → cable → core → terminal → wire → module + channel → address → SCADA tag |
| 7 | List the three reconciliation passes | 1 min | And what class of error only each one catches |
| 8 | List the ten permissives for P-101 | 2 min | And which are wired normally closed, and why |
| 9 | List what you cannot claim, and who owns each | 2 min | **No hesitation** — hesitating is worse than getting one wrong |
| 10 | Trace CR-001 through every document | 4 min | Including what *didn't* change, and TQ-011 |

### 5.2 Number drills

No calculator.

| Ask yourself | Answer | Method |
|---|---|---|
| 90 kW at 415 V — roughly what current? | ~150–160 A | P / (√3 × V × cosφ × η) |
| 500 kVA at 415 V? | ~695 A | S / (√3 × V) |
| 5 % impedance — fault current at the secondary? | 20 × FLC ≈ 13.9 kA | I_fl / 0.05 |
| Pump at 80 % speed — power? | ~51 % | 0.8³ |
| Pump at 50 % speed — power? | 12.5 % | 0.5³ |
| 12 mA on a 0–10 m range? | 5 m | Midpoint of 4–20 |
| 13.2 mA on 0–10 m? | 5.75 m | ((13.2−4)/16) × 10 |
| 4-pole motor, 50 Hz — synchronous speed? | 1500 rpm | 120 f / p |
| Which harmonics from a six-pulse rectifier? | 5, 7, 11, 13 | 6k ± 1 |
| Which harmonics add in the neutral, and from where? | 3rd, 9th — from **single-phase** load | Zero-sequence |
| DOL starting current? | 6–8 × FLC | Locked rotor |

### 5.3 The two-minute version

Set a timer. Explain the whole project in two minutes without notes. Do it once a day for a week. You will find that around day three it stops being a recitation and becomes an explanation — and that is the point at which you are ready to use it.

---

## 6. Common mistakes when explaining this

| Mistake | What it looks like | Fix |
|---|---|---|
| **Jargon dumping** | "It's a Form 3b MCC with two VSD feeders and a CompactLogix on EtherNet/IP" to a recruiter | Version 1. No acronyms at all. |
| **Burying the framing** | Getting six minutes in before saying it's self-directed | Say it in the first two sentences, every time |
| **Volunteering every document** | Opening the FAT sheet, the BOM and the TQ register unasked | Mention they exist. Open on request. It reads as insecurity. |
| **Defending an error** | Arguing when someone catches something | "You're right, let me correct that" is a stronger position than being right |
| **Over-claiming under pressure** | A friendly interviewer makes you relax into "I designed…" | The framing sentence is a habit, not a disclaimer |
| **Answering the question they didn't ask** | Asked "what's a VSD", you deliver the harmonics lecture | Answer the question. Offer the depth. |
| **Apologising** | "It's only a reference project, sorry…" | It's a reference project. Full stop. No apology — you built 57,000 words of it. |
| **Flat delivery** | Reciting from memory | The two-minute drill, daily, until it becomes explanation |

---

## 7. The one thing to get right

Every audience, every version, every length:

> **State what you built, state what you deliberately didn't, and be able to explain any part of it when asked "why?" three times.**

Everything in this document is a variation on those three.

---

**Back to:** [README](README.md) · [Core concepts](14-CORE-CONCEPTS.md) · [Glossary](15-GLOSSARY.md) · [Start command trace](16-START-COMMAND-TRACE.md)
