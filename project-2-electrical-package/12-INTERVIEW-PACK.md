# INTERVIEW PACK

**Rule before anything else:** you may not use any of this until you can explain the underlying document without reading it. A polished answer you do not understand is worse than a rough answer you do, because the follow-up question exposes it immediately — and then everything else you said becomes suspect.

---

## 1. THE 60-SECOND EXPLANATION

Use when asked "tell me about a project" or "walk me through your portfolio". Time it. It should run 55–70 seconds.

> "The project is a full electrical package for a water utility pump station — a 415-volt motor control centre with two 90-kilowatt variable-speed transfer pumps, some smaller feeders, a PLC with remote I/O, and a fibre link back to SCADA.
>
> I should be upfront: it's a self-directed reference project, not delivered work. I built it because I wanted to understand how a package actually develops rather than just how to read a drawing. So I took it right through — design basis, single line, schematics, terminations, BOM, procurement, fabrication inspection, FAT, and handover.
>
> The two things I got most out of it were the reconciliation work — cross-checking the SLD against the schematics against the BOM, three directions, and finding the things that don't line up — and tracing a late design change through every single document.
>
> And it made me clear on where my limits are. There are things in there I deliberately didn't do: the fault level study, the protection coordination, the functional safety Performance Level. Those are inputs or specialist work. I flagged them as assumptions and escalated them, which is what I'd do on a real job."

**Why this works:** it is specific, it is honest without being apologetic, and the last paragraph pre-empts the trap question. **Do not skip the last paragraph to save time.** It is the most valuable part.

---

## 2. THE 3-MINUTE TECHNICAL EXPLANATION

Use when they say "tell me more" or "walk me through the technical side".

> **The scenario.** A regional water utility upgrading the raw water transfer pump station at a treatment plant. Two old fixed-speed pumps replaced with two variable-speed 90-kilowatt units in duty/assist, and the switchboard replaced with a new Form 3b MCC. The board also feeds a sump pump, an instrument air compressor, a motorised valve, a vendor dosing skid, switchroom services and a light-and-power board. Control is a PLC in the MCC with a remote I/O node at the intake screen, reporting to SCADA over fibre.
>
> **Design basis first.** I built a design input register — every requirement, its source, our engineering response, which document it affects, and its status. What that exposed was how much of the design rests on inputs nobody had supplied: the fault level, the earthing system, the client's own electrical standard, the motor nameplate data, the PLC platform, even the cable entry direction. All of those became technical queries, with dates and with a stated consequence if they weren't answered.
>
> **The single line.** Six-thirty-amp incomer, four-pole, electronic trip so the settings can be tuned once a coordination study exists. Eight-hundred-amp busbar with a full-size neutral — that one matters, because with two six-pulse drives on the board you get triplen harmonics, and triplen currents add in the neutral rather than cancelling. The drafter's first revision had a half-size neutral copied from a project template and I had it changed.
>
> On the drive feeders, the breaker is selected from the drive manual, not from motor full-load current, because that breaker protects the cable and the drive input. The motor is protected by the drive's thermal model plus an independent thermistor relay — the drive's model infers temperature from current, the thermistors measure it.
>
> **Schematics.** Dual-channel monitored E-stop through a safety relay into Safe Torque Off on both drives. Local-Off-Remote at each starter, and Local still enforces every permissive — the first draft had Local bypassing the dry-run and seal-water permissives because that's how a previous job was done, and I had that reversed. Dry-run protection is a hardwired float into the drive's external fault input as well as into the PLC, because a 90-kilowatt pump's asset protection shouldn't depend solely on software somebody can force during commissioning.
>
> **Terminations.** Rails segregated by voltage and function, yellow terminals for the safety circuit, disconnect terminals on every analogue loop so you can inject a calibrator without unwiring. Instrument screens earthed at the MCC end only through an insulated single-point bar; VSD motor cable screens 360 degrees at both ends. Different problems, different solutions.
>
> **BOM and reconciliation.** Three directional passes — SLD to BOM, schematic to BOM, and BOM back to drawings. The schematic pass is where you tally contacts, and that's where I found a contactor using four auxiliary contacts against a device that supplies two. That's the most common defect in the industry and it stops workshops.
>
> **Then a late change.** After the design freeze, the client's hydraulic modelling came back and the motors went from 75 to 90 kilowatts. I traced it through every document — SLD, schematics, terminations, BOM, procurement, fabrication, FAT, as-built. Two or three weeks on the critical path instead of eight, and every reason for that was a decision made before the change arrived.
>
> **FAT.** A hundred and twenty-seven tests. Six defects worth talking about. The one I'd point to is that the protection coordination study still wasn't available, so I recorded the settings verification as a deviation rather than a pass, with a hold point before site energisation. It would have been easy to tick it."

**Practise the transitions.** The content is fine; what makes it sound senior is moving between sections without hesitating.

---

## 3. THE 10-MINUTE PRESENTATION

Structure, with timings. Have the SLD open on screen or printed from minute two.

### Minute 0–1 — Framing

State up front: self-directed reference project, not delivered work. Say why you built it: *"I could read drawings but I couldn't explain how they connect to procurement, to a workshop, or to a FAT. So I built the whole thing."*

### Minute 1–2 — Scenario and scope

The station, the loads, what is in scope and — more importantly — what is excluded and whose scope it is. Mention that exclusions matter more than scope because creep enters through undefined boundaries.

### Minute 2–4 — Design basis and the input register

**Show the register.** Point at the open items. Make this point explicitly:

> *"What struck me is how much of an electrical design depends on inputs somebody else owns. The fault level determines every breaker rating and the busbar withstand, and it's not mine to produce. So it becomes a technical query with a date and a stated consequence — if we don't get it by this date, we order on the assumption and any change is a variation."*

### Minute 4–6 — SLD walkthrough

**Have it in front of them.** Do not narrate everything. Pick four things and explain *why*:

1. Four-pole incomer with an electronic trip unit — isolation, and adjustability for a coordination study you don't have yet.
2. Full-size neutral — triplen harmonics add in the neutral. Mention that you caught this from a template.
3. VSD feeder breaker from the drive manual, not motor FLC — because it protects the cable and drive, not the motor.
4. The separate insulated instrument screen earth bar — and why it is different from the VSD cable screen.

### Minute 6–7 — Schematics and the safety circuit

Dual channel, monitored, STO. Then deliver this deliberately:

> *"One thing I want to be clear about: Safe Torque Off removes torque, it doesn't isolate. The motor terminals can still be live after an E-stop. STO isn't an isolation method and doesn't replace the lockable isolator at the motor. And I should say — the architecture looks like a PLd arrangement, but the required Performance Level comes out of a machinery risk assessment I haven't done, and the achieved PL needs an ISO 13849 calculation I haven't done. So I wouldn't claim it's PLd. I'd say it's the architecture you'd normally build for PLd, pending verification."*

**That paragraph is the single strongest 30 seconds in the presentation.** Rehearse it until it is natural.

### Minute 7–8 — BOM reconciliation and a discrepancy

Explain the three passes and why one direction is not enough. Then tell the auxiliary contact story in thirty seconds — it is concrete and every panel person in the room will recognise it.

### Minute 8–9 — The design change

The motor uprate. Trace it. Land on two points:

- **TQ-011** — the upstream transformer capacity check. *"The easy check is that our incomer and busbar still cope. The one that takes a step back is whether the transformer upstream still has capacity, because it also feeds site loads that aren't on my drawings. That's the one that could cost six figures."*
- **The held drive order.** Tell it honestly — including that it looked overly cautious for six weeks.

### Minute 9–10 — FAT, handover, and the honest close

The deviation on protection settings. The carried-forward register. Then close:

> *"What this gave me is a real understanding of how the documents connect and where things break. What it doesn't give me is a protection study, a cable calculation or a PL verification — those are specialist, I've flagged them throughout, and I'd escalate rather than attempt them. I think knowing that boundary is part of the job."*

### Have ready but do not present

The full termination schedule, the FAT sheet, the BOM, the TQ register. Mention they exist; open them only if asked. **Volunteering every document reads as insecurity.**

---

## 4. TEN QUESTIONS A MANAGER WILL ASK — AND MODEL ANSWERS

### Q1. "What's the fault level on this board and how did you get it?"

> "It's an assumption — 25 kA for one second — and it's flagged as an assumption in the design basis, in the input register, and as a note on the SLD face. The transformer nameplate gives roughly 14 kA from impedance alone, and 25 kA carries margin for motor contribution and any future transformer upsize.
>
> On a real job it comes from the client or the network operator, ideally from a study. I wouldn't finalise device selection without it in writing, because every breaker's Icu and Ics and the busbar's Icw hang off it — it's the single biggest cost exposure in the package. I raised it as a technical query in week one and escalated it twice. What I'd say to a project manager is that ordering long-lead breakers against an assumption is a commercial decision, not an engineering one, and it needs to be made by someone who owns the commercial risk."

**Why it works:** admits the assumption immediately, shows you know the consequence, and correctly attributes the decision.

---

### Q2. "Why is the breaker on the VSD feeder sized the way it is?"

> "It's selected from the drive manual, not from motor full-load current. On a VSD feeder that breaker is protecting the cable and the drive's input stage — it isn't protecting the motor. The motor is protected by the drive's electronic thermal model plus an independent PTC thermistor relay.
>
> The reason it matters is that many drives require a specific fuse or breaker type to achieve their declared short-circuit current rating — some need semiconductor-rated fuses. Fit the wrong device and you can invalidate the drive's SCCR. Also, the drive's *input* current isn't the same as the motor's full-load current; it depends on the DC link arrangement and whether there's a line reactor.
>
> And on the thermistor relay — the drive's thermal model infers winding temperature from current and time. It doesn't know the motor's cooling fan has failed, and it doesn't know that a TEFC motor running at low speed on a drive gets much less cooling than the model assumes. Thermistors measure the actual winding temperature. On a 90 kW pump motor with a long lead time, that redundancy is cheap."

---

### Q3. "Walk me through your cable calculation for the pump feeder."

> "I haven't done one. The sizes in my schedule are placeholders and they're marked as provisional.
>
> I can tell you what the calculation needs: the continuous current — and for a VSD feeder that's the drive's input current, not the motor FLC — the installation method, ambient temperature, grouping and derating, route length for volt drop, fault withstand for the required disconnection time, and the drive manufacturer's constraints on cable type and screening. AS/NZS 3008.1.1 is the reference.
>
> That calculation belongs to the designer. My job is to check that its inputs match the actual installation — particularly the route length, because that's usually taken from a drawing rather than measured — and to cross-check the result against the drive manual's maximum cable length, because above that limit you get reflected wave voltage doubling at the motor terminals and you need a dv/dt or sine filter."

**This answer is better than a correct calculation** because it shows you understand what the calculation is for and where it goes wrong.

---

### Q4. "This E-stop circuit — is it Category 3, PLd?"

> "The architecture is what you'd normally build for PLd — dual channel, monitored, safety relay, STO on the drives, monitored manual reset. But I wouldn't claim it *is* PLd, and here's why.
>
> The *required* Performance Level comes out of a machinery risk assessment under AS 4024.1 — severity, frequency of exposure, possibility of avoidance. I haven't done that assessment. The *achieved* Performance Level needs an ISO 13849-1 calculation using the manufacturers' reliability data for each device in the chain. I haven't done that either.
>
> So what I'd say is: this is the architecture you'd normally build for PLd, pending verification by someone qualified to do it. I raised it as a technical query rather than quietly picking a rating.
>
> The other thing I'd raise is the stop category. This is drawn as Category 0 — immediate removal of power. But an abrupt stop of a 90 kW pump at full speed can cause hydraulic surge, which damages pipework. Category 1 — controlled stop then remove power — might be more appropriate. That's a decision that needs the risk assessment and a surge assessment, and neither is mine."

---

### Q5. "You found a contactor with the wrong coil voltage at FAT. How did that happen and what did you do?"

> "A 240-volt AC coil supplied instead of 24-volt DC. Same contactor family, same current rating — the difference is one suffix in the part number and the coil marking. A supplier picking error that wasn't caught at goods inward.
>
> I categorised it as Category A because it's not just a non-functional feeder. The risk is that somebody 'solves' it by connecting it to the 240-volt services supply, and now you've got 240 volts AC running through ELV terminals, in the ELV duct, out to a field control station designed for ELV. That's a genuine safety defect.
>
> Replaced same day — it was in stock. But the more important action was that I then physically verified every other contactor and relay coil in the board, because a picking error of that type is rarely isolated. I found one more. That one would otherwise have been found on site.
>
> The process lesson is that goods-inward inspection has to check part numbers, not descriptions. 'Contactor 9 amp' on a delivery docket matches both parts. The suffix is the whole difference."

---

### Q6. "The client uprated the motors after the design freeze. Talk me through it."

> "Hydraulic re-modelling came back in week 12 and the duty point moved outside what 75 kW pumps could do. Vendor confirmed 90 kW.
>
> First thing was a full impact assessment across every document — and I documented what *didn't* change as explicitly as what did, because that determines the retest scope and it stops people reworking things unnecessarily. Control philosophy, I/O list, terminal numbering, safety architecture — all unchanged. Though I did verify the STO terminal designations against the new drive's manual rather than assume they were identical, because that's the safety circuit.
>
> What changed: motor rating, FLC, drive, line reactor, cable size, lugs, glands, gland plate cutouts, and the cubicle — the 90 kW unit is a larger frame, which I confirmed from the vendor's GA drawing rather than assuming it was the same frame as the 75.
>
> The one I'd point to is a query I raised that wasn't on anyone's list: transformer capacity. It's easy to check that our own incomer and busbar still cope — they did, with margin. It takes a step back to ask whether the 500 kVA transformer upstream still has capacity, because it also feeds site loads that aren't on my drawings. If it doesn't, that's a transformer replacement — six figures, long lead, and an outage. Better asked in week 13 than at commissioning.
>
> Net impact was two to three weeks instead of eight to ten, and I'd be honest that every reason for that was a decision made weeks before the change arrived — the drive order hadn't been placed, the build had been re-sequenced so the drive cubicles were last, and the gland plates were still undrilled."

---

### Q7. "Tell me about a decision you made that you weren't sure about."

> "Holding the VSD order.
>
> We had a sixteen-week lead time against a twelve-week programme. The obvious fix was to order the drives immediately — recover the full four weeks. There was real pressure to do it and it was a reasonable suggestion.
>
> I held the order because the motor data wasn't confirmed and the design wasn't frozen, and I'm not willing to commit to a long-lead, high-value, configured item against unconfirmed inputs. I recovered the time a different way — re-sequenced the build so the enclosure, busbar, terminals, PLC section and all the small feeders were wired first and the drive cubicles were last. That got most of it back.
>
> For about six weeks that looked like being overly cautious, and it cost me some goodwill with the planner. Then in week 12 the motors were uprated, and two 75 kW drives ordered in week six would have been scrap — or at best a restocking argument on a configured product.
>
> I'd want to be honest that I didn't predict the change. What I did was refuse to commit against unconfirmed inputs, which is a rule rather than a prediction. The rule is what saved it, not foresight."

**This is your strongest answer.** It is honest, it distinguishes luck from process, and it shows you can hold a position under pressure.

---

### Q8. "What's the difference between how you earth an instrument screen and a VSD motor cable screen?"

> "They're solving different problems.
>
> An instrument screen on a 4–20 mA loop is doing electrostatic shielding of a low-level signal. You earth it at one end only — the MCC end. If you earth both ends you create an earth loop, and any potential difference between those two earth points drives circulating current through the screen, which couples noise into the pair. That's exactly what you were trying to prevent.
>
> A VSD motor cable screen is doing something else entirely. Its job is to give high-frequency common-mode current a low-impedance return path back to the drive, so it doesn't go through the building steel, the earthing system and everything nearby. That needs a 360-degree termination at *both* ends — at the drive via an EMC gland and at the motor. Earthing one end defeats it. And a pigtail instead of a 360-degree gland largely defeats it too, because a pigtail is an inductor at those frequencies.
>
> Neither of those is the protective earth conductor, which is always connected at both ends because it's a safety conductor.
>
> Practically — I put a note on the face of the termination drawing saying screens are earthed at the MCC end only. The installer reads the termination drawing. They'll probably never read the specification."

---

### Q9. "How do you know the BOM matches the drawings?"

> "Three directional passes, because each one catches a different class of error.
>
> SLD to BOM — walk every device on the power drawing and confirm it's purchased with the right rating and the right accessories. Catches missing devices and missing accessories: handles, aux contacts, trip units, end caps.
>
> Schematic to BOM — walk every sheet, and critically, **tally the contacts**. How many auxiliary contacts does the schematic use on each device, and how many does the part number actually supply? That's where I found a contactor using four contacts against a device that provides two. Also catches coil voltage mismatches.
>
> BOM back to drawings — walk every BOM line and find where it appears. Anything that can't be traced is either a duplicate, a leftover from a copied BOM, or an error. Neither forward pass can find something that shouldn't be there.
>
> Then cross-check to the I/O list and termination schedule — module counts against points used plus spares, terminal counts against the schedule.
>
> And the rule is that any drawing revision triggers a re-reconciliation. A BOM frozen at Rev B against drawings at Rev C is how a board gets built wrong."

---

### Q10. "What would you do differently?"

> "Three things.
>
> First, I'd escalate the fault level harder and earlier. I raised it in week one and chased it twice, but it was still open at FAT. Looking at it again, I should have made the commercial exposure explicit to the project manager much earlier — quantified how much equipment was committed against an assumption — because that turns it from an engineering nag into a commercial decision someone has to actually make.
>
> Second, I'd have pushed harder on the harmonic question. Two six-pulse drives totalling 180 kW on a 500 kVA transformer is enough to need an assessment. I carried line reactors provisionally and flagged it as a risk, but if that assessment comes back needing an active harmonic filter, that's another cubicle, significant cost and a long lead. That's a risk I identified but didn't drive to closure, and that's a genuine shortfall.
>
> Third — and this is about me rather than the package — I'd want a lot more workshop time. I can write an inspection checklist. I can't yet look at a board and immediately see what's wrong with it, and I know that's a different skill that only comes from standing in workshops. That's why I'd want a role where I'm in a workshop regularly rather than only at milestones."

**Why this works:** two specific technical self-criticisms and one honest capability gap that doubles as a statement about what you want from the job.

---

## 5. FIVE QUESTIONS THAT WILL EXPOSE YOU IF YOU DON'T ACTUALLY UNDERSTAND IT

**Answer these out loud, from memory, with nothing in front of you. If you cannot, you do not own that part of the package yet.**

---

### E1. "Draw me the E-stop circuit on this whiteboard and show me what happens if one wire breaks."

You must be able to draw: two channels, each E-stop with two independent NC contacts in series in both channels, into the safety relay's two inputs, monitored reset, outputs to both drives' STO and to the DOL contactor coil circuit, auxiliary to PLC.

Then explain: one channel opens, the safety relay detects a discrepancy between the channels within its monitoring time, it goes to the safe state, and it will not reset until the fault is cleared — that's the entire point of dual channel. A single-channel circuit with a broken wire fails silently.

**If you cannot draw this, remove every safety claim from your CV.**

---

### E2. "Why is the neutral full-size? Talk me through the physics."

Third harmonic currents in a three-phase system are in phase with each other across all three phases — they're 120° apart in the fundamental, which is 360° apart at the third harmonic, so they're co-phasal. The fundamental currents cancel in the neutral of a balanced system; the triplens don't. They add.

So on a board with significant non-linear load — six-pulse drives, switch-mode power supplies, electronic ballasts — the neutral can carry substantially more current than any phase. A reduced-size neutral on a harmonic-rich board can overheat while every phase reads comfortably within rating.

**If you say "because of harmonics" and cannot explain why triplens add, you have memorised a phrase.**

---

### E3. "Your Local mode enforces all the permissives. A fitter says that's inconvenient — he can't test the pump with the wet well low. What do you say?"

You must be able to argue this on its merits, not by citing a rule.

*Local mode is for maintenance and fault-finding, not for bypassing protection. A Local mode that drops the dry-run and thermistor trips is how a 90 kW pump gets destroyed by someone who reasonably assumed it was protected. Local changes who gives the command, not what protects the machine.*

Then — and this is the part that shows judgement — acknowledge that the fitter's problem is real:

*If a genuine bypass is required for testing, it has to be a deliberate function: key-switched, alarmed at SCADA, time-limited, and specified by the client. Not an accidental consequence of selecting Local. I'd rather design the bypass properly than pretend the requirement doesn't exist.*

---

### E4. "Which of these could you not do on a real job, and who does it?"

You should be able to list, without hesitation and without prompting:

- Fault level determination — client / network operator / formal study
- Protection coordination and settings — protection engineer or manufacturer's coordination tables
- Arc flash study — specialist, IEEE 1584 methodology
- Cable sizing to AS/NZS 3008.1.1 — electrical designer
- Machinery risk assessment and required PL — safety consultant; achieved PL by ISO 13849 calculation
- AS/NZS 61439 design verification — **the assembly manufacturer**, not the designer and not the client
- PLC application code — systems integrator
- Design approval and certification — a chartered or otherwise responsible engineer
- Any physical electrical work — licensed electrical worker

**Hesitating here is worse than getting one wrong.** It suggests you have not thought about the boundary at all.

---

### E5. "This is a reference project you built yourself. Why should I believe you'd cope with a real one, where the client is difficult and the programme is already late?"

There is no clever answer. There is an honest one:

> "You shouldn't believe it from this alone, and I wouldn't ask you to. What this shows is that I understand the mechanics — how the documents connect, where packages fail, what a project engineer actually controls and what they don't. That's the part you can learn without being on a job, and I've done it properly rather than superficially.
>
> What it doesn't show is how I behave when a client is unreasonable, when the programme is gone, or when I have to tell someone senior that something they want isn't going to work. I haven't been tested on that and I'm not going to pretend I have.
>
> What I'd say is that I've built the technical foundation so that when I am in those situations, the engineering isn't the thing I'm struggling with. And I'd want to be somewhere I can sit alongside someone who has done it, rather than being handed a package and left to find out."

**That answer is strong because it refuses the premise of bluffing.** An experienced manager will respect it far more than confidence you cannot back.

---

## 6. WHAT TO DO IF YOU DON'T KNOW SOMETHING

You will get asked something you cannot answer. This is not a failure — it is expected of a graduate, and how you handle it is being assessed more than the answer itself.

**The formula:**

1. Say you don't know. Plainly. No hedging, no waffle.
2. Say what you *do* know that is adjacent to it.
3. Say how you would find out.

> *"I don't know. What I do know is that it's governed by [the drive manual / AS/NZS 3008 / the coordination tables], and I'd go to [that source / the designer / the vendor's application engineer] rather than guess. If it mattered to a decision I'd get it confirmed in writing before I committed anything."*

**Never** invent a number. **Never** say "I think it's about..." for something with a real answer. An interviewer who catches one fabricated figure will re-evaluate everything you have said, and they will be right to.

---

**Next:** [Study Gaps](13-STUDY-GAPS.md)
