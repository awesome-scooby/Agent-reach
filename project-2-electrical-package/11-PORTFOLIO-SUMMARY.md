# PORTFOLIO SUMMARY

# PROJECT 2 — FULL ELECTRICAL PACKAGE

```
        SLD  →  SCHEMATIC  →  TERMINATIONS  →  BOM  →  PROCUREMENT
                                                            ↓
        AS-BUILT / HANDOVER  ←  FAT  ←  FABRICATION  ←──────┘
```

**Northfield Raw Water Pump Station — MCC-01**
415 V Form 3b motor control centre · 2 × 90 kW VSD pump feeders · 5 small feeders · 2 fitted spares · PLC and remote I/O · fibre to SCADA

---

## STAGE 1 — DESIGN BASIS

| | |
|---|---|
| **ENGINEERING INPUTS** | Client specification and functional spec · site visit · existing SLD · transformer nameplate · pump vendor preliminary data · client standards *(requested, not supplied)* |
| **MY RESPONSIBILITIES** | Extract every requirement with an engineering consequence · build the design input register · separate confirmed inputs from assumptions · raise TQs with dates and consequences · declare the heat load to the HVAC designer · brief the designer on what must not be drafted yet |
| **TECHNICAL DECISIONS** | 24 V DC as the primary control voltage · redundant PSUs with grouped DC protection · hardwired dry-run protection independent of the PLC · hardwired speed reference with comms for monitoring · 630 A incomer with 800 A busbar and full-size neutral · 20 % spare capacity |
| **KEY RISKS** | Unconfirmed fault level *(largest cost exposure)* · missing client standard blocking fabrication release · late pump vendor data *(materialised as CR-001)* · unassessed harmonics · undetermined required Performance Level |
| **DOCUMENTS PRODUCED** | Design basis · design input register · assumptions register · load schedule · interface register · TQ register · heat load declaration |
| **INTERFACES** | Client · network operator · pump vendor · HVAC designer · civil · systems integrator · installation contractor |
| **QUALITY CHECKS** | Every requirement traced to a response and a document · every assumption has an owner and a close-out date · exclusions written down explicitly |
| **LESSONS LEARNED** | An unflagged assumption is the most expensive thing in a package. Exclusions matter more than scope — creep enters through what nobody wrote down. Nobody will ask you for the heat load; declare it anyway. |
| **EMPLOYER VALUE** | Turns a vague client brief into a controlled, auditable set of engineering inputs, and surfaces the expensive unknowns in week two instead of week twelve. |

---

## STAGE 2 — SINGLE LINE DIAGRAM

| | |
|---|---|
| **ENGINEERING INPUTS** | Design basis · load schedule · assumed fault level · earthing assumption · client SLD · vendor data |
| **MY RESPONSIBILITIES** | Brief the designer · review the SLD against a written check list · require provisional ratings to be annotated **on the drawing face** · issue for approval with the assumptions listed in the transmittal |
| **TECHNICAL DECISIONS** | 4-pole incomer with electronic trip for adjustability · full-size neutral for triplen harmonics · SPD on its own protective device with status monitoring · VSD feeder breakers selected from the drive manual, not motor FLC · independent thermistor relay alongside the drive's thermal model · separate insulated instrument screen earth bar |
| **KEY RISKS** | Every device rating provisional against an assumed fault level · no coordination study · harmonic mitigation unresolved · motor cable length unconfirmed *(drives whether an output filter is needed)* |
| **DOCUMENTS PRODUCED** | SLD · feeder schedule · earthing arrangement · SLD review check list |
| **INTERFACES** | Network operator *(fault level)* · protection specialist · drive vendor · installation contractor *(cable interface)* |
| **QUALITY CHECKS** | 13-point SLD review · rating consistency up the chain · tag consistency against schematics and BOM · assumptions annotated on the drawing |
| **LESSONS LEARNED** | Caught a half-size neutral inherited from a project template. On a harmonic-rich board that is a genuine overheating hazard, and it was invisible until someone asked why. **Drawing templates carry other projects' assumptions.** |
| **EMPLOYER VALUE** | Can read an SLD as an argument about fault clearance and isolation, not as a connection diagram — and can defend every device on it. |

---

## STAGE 3 — SCHEMATICS

| | |
|---|---|
| **ENGINEERING INPUTS** | Functional description · SLD · drive manual · safety requirements · vendor wiring diagrams · I/O list |
| **MY RESPONSIBILITIES** | Write the functional description **before** drafting starts and get it agreed · review every sheet against it · run schematic↔SLD↔BOM reconciliation · challenge inherited practice · issue the I/O list to the integrator at the same revision as the board |
| **TECHNICAL DECISIONS** | Dual-channel monitored E-stop driving STO · **Local mode enforces every permissive** · two selector inputs to the PLC so Off and a selector fault are both detectable · critical DIs wired normally closed *(fail-safe)* · contactor read-back from the auxiliary contact, not the DO echo · interposing relays on every output leaving the board |
| **KEY RISKS** | Required Performance Level undetermined · stop category *(0 vs 1)* unresolved against hydraulic surge · auxiliary contact shortfall · integrator working from a superseded I/O list |
| **DOCUMENTS PRODUCED** | Functional description · control power schematic · safety circuit schematic · per-feeder schematics · PLC I/O schematics · I/O list |
| **INTERFACES** | Systems integrator · safety consultant · drive vendor · MOV actuator vendor · client operations |
| **QUALITY CHECKS** | 10-point schematic↔SLD reconciliation · **contact tally per device** · coil voltage against BOM part numbers · cross-reference resolution · control group loading vs PSU sizing |
| **LESSONS LEARNED** | The drafter's first revision had Local mode bypassing the dry-run and seal-water permissives — "because that's how the last one was". **Local changes who gives the command, not what protects the machine.** Inherited practice needs a reason, not a precedent. |
| **EMPLOYER VALUE** | Can take a control philosophy to schematic logic and back, and can reason about failure modes rather than just normal operation. |

---

## STAGE 4 — TERMINATIONS

| | |
|---|---|
| **ENGINEERING INPUTS** | Schematics · I/O list · cable schedule · field device data · client conventions |
| **MY RESPONSIBILITIES** | Set the numbering and rail philosophy **before** drafting · run the four-way reconciliation · put the screen-earthing requirement on the drawing face · verify the terminal count fits the rail length before fabrication |
| **TECHNICAL DECISIONS** | Rails segregated by voltage and function · yellow terminals for the safety circuit only · disconnect terminals on every analogue loop · 20 % spare terminals grouped, not distributed · instrument screens earthed at the MCC end only via an insulated single-point bar · VSD screens 360° at both ends · sheet-path wire numbering |
| **KEY RISKS** | Installer earthing instrument screens at both ends · insufficient spare cores · terminal count exceeding rail length · address drift between I/O list revisions |
| **DOCUMENTS PRODUCED** | Terminal numbering convention · termination drawings · termination schedule · cable schedule |
| **INTERFACES** | Installation contractor · instrumentation · systems integrator · workshop |
| **QUALITY CHECKS** | Full traceability chain closed for every I/O point: device → cable → core → terminal → wire → module → address → SCADA tag |
| **LESSONS LEARNED** | Changed the LCS control cable from 12 cores to 16 because the schedule used all 12. Four extra cores cost almost nothing; a second cable pull through an operating plant costs a variation and an access permit. |
| **EMPLOYER VALUE** | Produces the document that gets used most after handover, and understands that a note on the drawing face prevents an entire class of commissioning fault. |

---

## STAGE 5 — BILL OF MATERIALS

| | |
|---|---|
| **ENGINEERING INPUTS** | SLD · schematics · termination schedule · I/O list · vendor quotations · manufacturer catalogues and coordination tables |
| **MY RESPONSIBILITIES** | Issue a preliminary BOM early purely to surface lead times · run all four reconciliation passes · compare quotations line by line · verify every part number · stop unapproved substitutions |
| **TECHNICAL DECISIONS** | MPCB + contactor over MCCB + separate overload · AC-3 rated contactors · DC-rated protection on DC circuits · fitted-and-wired spare feeders rather than empty chassis space · address reserve module to keep a slot usable |
| **KEY RISKS** | Auxiliary contact shortfall stopping the workshop · obsolete parts silently substituted in quotations · drive type-code misconfiguration · long-lead items blocked on open TQs |
| **DOCUMENTS PRODUCED** | BOM · long-lead register · reconciliation findings · discrepancy records · deviation request DEV-002 |
| **INTERFACES** | Procurement · vendors · designer · workshop · client |
| **QUALITY CHECKS** | SLD→BOM · Schematic→BOM *(with contact tally)* · BOM→Drawings · cross-check to I/O list and termination schedule |
| **LESSONS LEARNED** | Most long-lead items were blocked on open technical queries, not on suppliers. **The PE's procurement job is mostly closing engineering inputs, not chasing deliveries.** |
| **EMPLOYER VALUE** | Finds the errors that stop workshops, before they stop workshops — and knows that technical equivalence is not kW and voltage. |

---

## STAGE 6 — PROCUREMENT AND ENGINEERING CONTROL

| | |
|---|---|
| **ENGINEERING INPUTS** | BOM · specifications · vendor quotations and data · client standards · programme |
| **MY RESPONSIBILITIES** | Technical review of enquiries and quotations · vendor data tracking with due dates · TQ register · revision control · change control · hold drawings from release until vendor data confirms them |
| **TECHNICAL DECISIONS** | Nothing built from a letter revision · every drawing revision triggers a BOM re-reconciliation · **hold the long-lead drive order until the design is frozen** · recover schedule by re-sequencing the build rather than compromising the design |
| **KEY RISKS** | Substitution without engineering approval · vendor data arriving after drawing release · integrator revision mismatch · ordering long-lead items against unconfirmed inputs |
| **DOCUMENTS PRODUCED** | TQ register · deviation register · change register · technical recommendations · transmittals · revision history |
| **INTERFACES** | Procurement · vendors · client · designer · workshop · integrator |
| **QUALITY CHECKS** | Quotation line-by-line against BOM · vendor data against drawings · revision control audit · transmittal discipline |
| **LESSONS LEARNED** | **You can draft ahead of vendor data; you must not release ahead of it.** Holding the general arrangement is what made the later cubicle modification possible instead of scrap. |
| **EMPLOYER VALUE** | Understands the boundary of their own authority, escalates properly, and recovers schedule without degrading the design. |

---

## STAGE 7 — FABRICATION AND WIRING

| | |
|---|---|
| **ENGINEERING INPUTS** | IFC drawings · BOM · specifications · client standards · manufacturer installation requirements |
| **MY RESPONSIBILITIES** | Inspect at four points, not one · verify the board being built is the board designed · check the drawing revision in the wireman's hand · capture mark-ups as they happen · answer workshop queries same-day |
| **TECHNICAL DECISIONS** | PLC relocated from directly above a drive · ferrule orientation convention corrected at 50 % wire · every earth bonding point re-checked after two were found bolted through powder coat |
| **KEY RISKS** | Building from a superseded revision · undocumented workshop improvisation · earth bonds through paint · segregation degraded during wiring · swarf left in the board |
| **DOCUMENTS PRODUCED** | Inspection records · workshop query log · captured mark-ups · non-conformance reports |
| **INTERFACES** | Workshop · designer · procurement · client *(optional witness)* |
| **QUALITY CHECKS** | 50-point inspection checklist across enclosure, layout, wiring, terminals, labels, earthing and document control |
| **LESSONS LEARNED** | **The 50 % wiring inspection is the one that pays.** Correcting a convention with half the board still to wire costs nothing. Correcting it at 100 % means either rework or accepting it — and accepting it sets a precedent. |
| **EMPLOYER VALUE** | Adds value in a workshop without getting in the way, and prevents the undocumented decisions that make a board unmaintainable. |

---

## STAGE 8 — FACTORY ACCEPTANCE TEST

| | |
|---|---|
| **ENGINEERING INPUTS** | Approved drawings · BOM · FAT procedure · PLC program · vendor data · calibrated test equipment |
| **MY RESPONSIBILITIES** | Write the procedure and get it approved two weeks out · run it internally first · agree defect categories and motor simulation method in advance · declare outstanding items in the opening · coordinate and witness · manage the punch list |
| **TECHNICAL DECISIONS** | Independent point-to-point checking *(caught FD-001)* · electronics disconnection list written into the procedure with a signed reconnection step · single-channel safety fault simulation · hardwired dry-run trip tested with the PLC stopped · **protection settings recorded as a deviation, not a pass** |
| **KEY RISKS** | Damaging electronics during insulation testing · client discovering an undeclared incomplete item · testing against the wrong program revision · a defect class being treated as a single instance |
| **DOCUMENTS PRODUCED** | FAT procedure · completed FAT sheet with individual results · punch list · red-marked drawings · deviation records |
| **INTERFACES** | Client · workshop · integrator · vendors |
| **QUALITY CHECKS** | 127-test procedure across 19 sections · every result recorded individually · retest scope agreed at the time of each defect |
| **LESSONS LEARNED** | **Never let the client witness the first energisation.** And when one picking error appears, check the whole class — the second wrong device would otherwise have gone to site. |
| **EMPLOYER VALUE** | Can run a FAT that finds real defects and still finishes with the client's confidence intact — and will not sign something as verified when it is not. |

---

## STAGE 9 — DESIGN CHANGE

| | |
|---|---|
| **ENGINEERING INPUTS** | Client TQ response · pump vendor data · drive vendor GA · procurement status · fabrication status |
| **MY RESPONSIBILITIES** | Full impact assessment across every document · identify what is unaffected as explicitly as what changes · cost and schedule assessment · client notification · implement and verify |
| **TECHNICAL DECISIONS** | Obtain the drive GA rather than assume the frame size · verify STO terminals rather than assume them · reject reduced clearance outright · modify cubicles rather than replace · **raise TQ-011 on transformer capacity** |
| **KEY RISKS** | Upstream transformer capacity *(not on our drawings, not our scope, potentially six figures)* · drive terminals not accepting the larger cable · change implemented in drawings but not in the BOM or FAT procedure |
| **DOCUMENTS PRODUCED** | Impact assessment · change record CR-001 · revised drawings at Rev 1 · BOM Rev D · revised FAT procedure · reissued heat load declaration |
| **INTERFACES** | Client · pump vendor · drive vendor · panel builder · installation contractor · HVAC designer |
| **QUALITY CHECKS** | Full BOM re-reconciliation at Rev 1 · verified-unchanged list · FAT procedure updated before the board was tested |
| **LESSONS LEARNED** | The change cost 2–3 weeks instead of 8–10, and **every reason for that was a decision made before the change was known.** Holding the drive order looked overly cautious for six weeks and then saved two drives from scrap. |
| **EMPLOYER VALUE** | Can trace a change through an entire package without losing a document, and understands that good project engineering is mostly about not closing doors before you have to. |

---

## STAGE 10 — AS-BUILT AND HANDOVER

| | |
|---|---|
| **ENGINEERING INPUTS** | FAT mark-ups · punch-list rectifications · vendor certificates · test records · parameter backups · registers |
| **MY RESPONSIBILITIES** | Agree the MDR index early · chase certificates before final payment · verify as-builts against the physical board · produce and get signature on the carried-forward register · run the handover with the maintenance team |
| **TECHNICAL DECISIONS** | Include the assumptions register so the design basis survives · include drive parameter **files**, not printouts · state explicitly what the FAT did not prove · write the spare capacity record unprompted |
| **KEY RISKS** | As-built not matching the board *(destroys trust in the whole set)* · certificates never obtained after payment · open engineering items evaporating at the FAT certificate |
| **DOCUMENTS PRODUCED** | MDR · as-built drawings · carried-forward register · spare capacity record · FAT limitations statement · close-out certificate |
| **INTERFACES** | Client project team · **client maintenance team** · vendors · installation contractor · commissioning |
| **QUALITY CHECKS** | MDR against agreed index · as-built physically verified · carried-forward items signed by both parties |
| **LESSONS LEARNED** | **A transcribed as-built nobody verified is worse than no as-built** — it looks authoritative and is fiction. And hand over to the people who will still be there in ten years. |
| **EMPLOYER VALUE** | Leaves an asset that can be maintained, modified and understood long after everyone involved has moved on. |

---

## WHAT THIS PROJECT DEMONSTRATES

Honest assessment, capability by capability. **"Demonstrated"** means this package evidences it. **"Partially"** means the understanding is there but real-world exposure is not. **"Not demonstrated"** means do not claim it.

| Capability | Level | Evidence and honest limit |
|---|---|---|
| **Electrical drawing literacy** | **Demonstrated** | Built and cross-checked an SLD, control schematics, termination drawings and an I/O list, and can explain every device and every design decision. *Limit: these are illustrative drawings, not CAD deliverables. No production drafting experience in AutoCAD Electrical or EPLAN.* |
| **Multidisciplinary coordination** | **Partially** | Identified and managed nine discipline interfaces, including the heat-load declaration nobody asks for. *Limit: coordinating documents is not the same as coordinating people under commercial pressure. That only comes from doing it.* |
| **Design management** | **Partially** | Briefed the design, reviewed outputs against written criteria, ran reconciliation, controlled revisions, challenged inherited practice. *Limit: has not managed a design team, a budget or competing priorities.* |
| **Procurement management** | **Demonstrated (process)** | Technical review of enquiries and quotations, vendor data tracking, long-lead management, stopped an unapproved substitution and escalated it correctly. *Limit: no commercial negotiation experience, and no real supplier relationships.* |
| **Technical problem-solving** | **Demonstrated** | Six worked BOM discrepancies and six worked FAT defects, each with root cause, consequence, action and retest scope. |
| **Change management** | **Demonstrated** | Traced a late motor uprate through every document, identified what was unaffected, and found the upstream transformer risk nobody had asked about. |
| **Cost awareness** | **Partially** | Understands where cost sits and the difference between purchase price and whole-of-life cost. **Explicitly did not fabricate dollar figures.** *Limit: has not priced or managed a real package budget, and should say so.* |
| **Schedule awareness** | **Demonstrated** | Identified long-lead items and their real blockers, and recovered schedule by re-sequencing rather than compromising the design. |
| **Fabrication support** | **Partially** | A four-point inspection regime, a 50-point checklist, and an understanding of which defects are cheap now and expensive later. *Limit: workshop judgement is built by standing in workshops.* |
| **Quality assurance** | **Demonstrated** | Reconciliation as a defined method rather than a read-through. Independent checking. Inspection hold points. |
| **FAT coordination** | **Demonstrated (procedure)** | A 127-test procedure, defect categories agreed in advance, punch-list discipline, and the integrity to record a deviation instead of a pass. *Limit: has not stood in a workshop with a client asking hard questions. That is a different skill.* |
| **Client communication** | **Partially** | TQs written as decision points with consequences. Deviations put to the client as recommendations. Approvals made meaningful by stating their assumptions. *Limit: no experience of a client who is angry, late or unreasonable.* |
| **Document control** | **Demonstrated** | Revision conventions, transmittals, superseded drawing removal, integrator revision alignment, and an understanding of the specific failures each rule prevents. |
| **Engineering handover** | **Demonstrated** | Full MDR structure, carried-forward register with named owners, explicit statement of what the FAT did not prove, spare capacity record. |
| **Protection design** | **NOT DEMONSTRATED** | No coordination study, no settings, no arc flash. Correctly identified as specialist scope and correctly escalated. **Do not claim this.** |
| **Functional safety** | **NOT DEMONSTRATED** | Circuit architecture understood. Required PL not determined, achieved PL not calculated. **Do not claim this.** |
| **Cable sizing** | **NOT DEMONSTRATED** | Knows the inputs a calculation needs. Has not performed one to AS/NZS 3008.1.1. **Do not claim this.** |
| **Assembly design verification** | **NOT DEMONSTRATED — and correctly attributed** | Knows this is the manufacturer's responsibility under AS/NZS 61439.1 and that the PE's job is to obtain the evidence. **Knowing this is itself a competency.** |

---

## THE HONEST ONE-PARAGRAPH SUMMARY

> This project demonstrates that I understand how an industrial electrical package is actually delivered: how design inputs become drawings, how drawings become purchase orders and a wired board, how that board gets tested, and how it gets handed over as an asset somebody has to maintain for thirty years. It demonstrates that I can find the errors that stop workshops, trace a change through a document set without losing anything, and recognise when a decision is not mine to make. It does not demonstrate that I can perform a protection study, size a cable to AS/NZS 3008, or determine a Performance Level — those are specialist activities, I have correctly identified them as such throughout, and I would escalate them rather than attempt them. **What I am offering is the coordination and control capability, an honest view of where its edges are, and the judgement to know the difference.**

---

**Next:** [Interview Pack](12-INTERVIEW-PACK.md) · [Study Gaps](13-STUDY-GAPS.md)
