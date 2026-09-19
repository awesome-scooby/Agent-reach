# 00 — CLAIM INTEGRITY

**Read this before you describe this package to anyone.**

Engineering hiring in Australia runs on trust. An interviewer who catches you overstating one thing will discount everything else you said, including the things that were true. The fastest way to look senior as a graduate is to be precise about the edge of your own competence.

---

## 1. The one-sentence framing you use every time

> "It's a self-directed reference project — I built a complete MCC package from design basis through FAT and handover so I'd understand how the documents actually connect. It's not delivered work, and there are parts of it I'd escalate rather than sign."

Say it early, unprompted. It converts a potential gotcha into evidence of judgement.

**Never say:** "I designed a 415 V MCC", "I delivered this package", "this was for a water utility client".
**Do say:** "I worked this package up as a reference design", "I put myself in the Project Engineer's seat", "I traced how a change propagates".

---

## 2. What you CAN legitimately claim

These are real, demonstrable capabilities that this package evidences:

| Claim | Why it holds |
|---|---|
| **Electrical drawing literacy** — I can read an SLD, a control schematic, a termination drawing and an I/O list, and cross-check them against each other | You built all four and reconciled them |
| **I understand the document hierarchy** — design basis drives SLD, SLD drives schematics, schematics drive terminations and BOM | You traced it |
| **Three-way reconciliation** — SLD ↔ schematic ↔ BOM, and how to find what's missing | You did it and documented the method |
| **Technical query discipline** — what a TQ is for, how to write one, what happens if you don't raise it | You wrote a TQ register |
| **Change management** — I can trace a late change through every affected document and identify cost, schedule and retest impact | Stage 9 |
| **FAT preparation and coordination** — what a FAT procedure covers, how defects get categorised, how punch lists close | Stage 8 |
| **Document control and handover** — what an MDR contains and why | Stage 10 |
| **Interface awareness** — I know where my scope stops and the installer's, the vendor's and the client's begins | Stage 1 interface register |
| **Knowing what needs a specialist** | This document |

That is a genuinely strong graduate offer. Most graduates cannot do the reconciliation or the change trace at all.

---

## 3. What you must NOT claim — and who actually owns it

| Item | Who owns it | What you say instead |
|---|---|---|
| **Prospective fault level at the MCC** | Client / network operator / a formal study using validated source impedance data | "It's a design input. I assumed 25 kA for 1 s and flagged it — I wouldn't finalise breaker ratings without it in writing." |
| **Protection discrimination / selectivity study** | Protection engineer, or verified against manufacturer's published coordination tables | "I know the incomer and feeder need to discriminate and that you verify it against the manufacturer's tables or a study. I haven't done one." |
| **Protection settings (Ir, Isd, Ii, earth fault)** | Whoever does the coordination study; commissioning engineer applies them | "Settings come out of the coordination study. I'd record them on the FAT sheet and in the MDR." |
| **Arc flash incident energy study and labelling** | Specialist, using IEEE 1584 methodology and real system data | "Specialist study. I'd carry it as a client-scope item in the interface register." |
| **Cable sizing to AS/NZS 3008.1.1** | Electrical designer with the actual route length, installation method, grouping and ambient | "I know the inputs: installation method, ambient, grouping, route length, volt drop, fault withstand, and VSD derating. My sizes here are placeholders pending the calc." |
| **Earthing system design / earth grid** | Electrical designer, sometimes a specialist for the HV side | "MCC earthing arrangement I understand. Site earthing design is not mine." |
| **Functional safety Performance Level (PLr / PLd) for the E-stop function** | A machinery risk assessment under AS 4024.1 / ISO 12100, then a PL verification calculation under ISO 13849-1 | "I've designed the circuit the way a PLd architecture normally looks — dual channel, monitored, safety relay, STO. But the *required* PL comes out of a risk assessment I haven't done, and the *achieved* PL needs a calculation I haven't done." **This is the single best honesty answer in the whole package. Use it.** |
| **AS/NZS 61439 design verification** | The **original manufacturer** of the assembly system — by testing, comparison or assessment. Not the designer, not the client. | "Design verification for temperature rise, short-circuit withstand and IP is the switchboard manufacturer's responsibility. As PE I'd ask for their verification evidence for the enclosure system and the form of separation, not do it myself." **Also excellent.** |
| **Harmonic study / compliance with the network operator's distortion limits** | Specialist study using the actual network impedance | "Two 75 kW six-pulse drives on a 500 kVA transformer is enough to need a harmonic assessment. I raised it as a TQ rather than assuming it away." |
| **Thermal / temperature rise verification of the cubicles** | Switchboard manufacturer, per AS/NZS 61439.1 | "I can list the heat sources. Verification is the manufacturer's." |
| **Signing or certifying the design** | CPEng / RPEQ or the responsible engineer under the client's or employer's engineering management system | "I'm not chartered. Design outputs get checked and approved by a senior engineer." |
| **Any physical electrical work** | Licensed electrician / electrical worker | "I'd witness and verify, not wire." |
| **PLC program** | Controls engineer / systems integrator | "I'd produce and check the I/O list and the functional description. The code is the integrator's." |

**If you are asked a question in any row above, the correct answer starts with "I didn't do that, and here's who does."**

---

## 4. Three traps interviewers set, and the answers

**Trap: "What's the fault level on this board?"**
Wrong: quoting 25 kA as fact.
Right: *"25 kA for one second is what I assumed and it's flagged as an assumption. On a real job it comes from the client or the network operator, and I wouldn't let it stay open past the design freeze because every breaker Icu, the busbar Icw and any cascade arrangement hangs off it."*

**Trap: "So you designed this?"**
Wrong: "Yes."
Right: *"I worked it up as a reference package to teach myself the workflow. On a real job the design outputs come from a designer and a drafter, get checked, and get approved by a responsible engineer. My seat is coordinating that, reviewing it, and catching the things that don't line up between documents."*

**Trap: "Walk me through your cable calc for the pump feeder."**
Wrong: inventing a calculation.
Right: *"I haven't done one — the sizes in my BOM are placeholders. I can tell you the inputs it needs: continuous current with the drive's input current not just the motor FLC, installation method, ambient, grouping, route length for volt drop, fault withstand for the disconnection time, and the manufacturer's constraints on VSD cable type and screening. AS/NZS 3008.1.1 is the reference. That calc belongs to the designer and I'd check it against the drive manual."*

That last answer is better than a correct calculation, because it demonstrates you know what a calculation is *for*.

---

## 5. The honesty test

Before you claim any part of this package, ask yourself:

> If the interviewer handed me a whiteboard marker right now and said "draw it and explain it", could I?

If no — it goes in `13-STUDY-GAPS.md`, not on your CV.

---

## 6. A note on the part numbers in this package

Catalogue numbers throughout are indicative, chosen from current manufacturer product families to make the BOM realistic. **Several will be wrong.** Catalogue numbers change, accessories get missed, and voltage/coil/curve variants are the single most common BOM error in the industry.

Do not present any part number here as verified. The correct statement is: *"Every part number gets verified against the manufacturer's current catalogue and confirmed on the vendor quotation before a purchase order is raised — that verification is part of the PE's BOM review."*

That is true, it is what actually happens, and it turns a weakness into a process point.
