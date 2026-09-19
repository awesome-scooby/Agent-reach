# STAGE 6 — PROCUREMENT AND ENGINEERING CONTROL

**Registers:** [`registers/tq-register.csv`](registers/tq-register.csv)

---

## 6.1 The thing most graduates get wrong about this role

A Project Engineer does not design every component. A Project Engineer **makes sure the right person designs each component, that their output is checked, that it is bought correctly, and that the decision is recorded.**

If you go into an interview describing yourself as the person who selected every breaker, one of two things happens: they do not believe you, or they believe you and conclude you do not understand how an engineering organisation works. Neither helps.

The accurate description is:

> *"I own the engineering inputs, the interfaces and the decisions. The designer produces the design. Procurement buys it. The workshop builds it. The client approves what is theirs to approve. My job is that all of those line up, that nothing falls between them, and that when something changes, everyone who needs to know finds out."*

---

## 6.2 Responsibility matrix

`D` = does the work · `R` = reviews · `A` = approves · `I` = informed

| Activity | Designer | **Project Engineer** | Procurement | Workshop | Client | Vendor |
|---|---|---|---|---|---|---|
| Interpret client specification | R | **D** | I | — | A | — |
| Build design input register | I | **D** | — | — | R | — |
| Raise technical queries | R | **D** | I | I | **A** | I |
| Fault level / earthing system determination | — | I | — | — | **D/A** | — |
| Protection coordination study | R | R | — | — | A | Specialist **D** |
| Arc flash study | — | I | — | — | **D/A** | Specialist |
| Machinery risk assessment / required PL | — | I | — | — | **D/A** | Safety consultant |
| Draw SLD | **D** | **R** | — | — | A | — |
| Draw schematics | **D** | **R** | — | — | A | — |
| Functional description | R | **D** | — | — | **A** | — |
| I/O list | **D** | **R** | — | — | A | Integrator R |
| Cable sizing calculation (AS/NZS 3008.1.1) | **D** | **R** | — | — | A | — |
| Termination schedule | **D** | **R** | — | R | I | — |
| Build BOM | **D** | **R** | R | I | — | — |
| **BOM reconciliation (all passes)** | R | **D** | I | — | — | — |
| Request quotations | I | R | **D** | — | — | **D** |
| **Technical review of quotations** | R | **D** | R | — | — | I |
| Commercial evaluation / negotiation | — | I | **D** | — | I | — |
| Raise purchase orders | — | **R (technical sign-off)** | **D/A** | — | — | I |
| Expedite orders | — | I | **D** | I | — | R |
| **Vendor data review (technical)** | R | **D** | I | I | R | **D (supply)** |
| Approve a substitution | R | **R + recommend** | I | — | **A** | I |
| Drawing revision control | **D** | **R/A** | I | I | I | — |
| Release drawings to workshop | I | **D/A** | — | R | — | — |
| Fabricate and wire | — | I | — | **D** | — | — |
| **In-progress inspection** | — | **D** | — | R | R (optional) | — |
| Resolve workshop queries | R | **D** | I | R | I | — |
| Write FAT procedure | R | **D** | — | R | **A** | — |
| Conduct FAT | — | **Coordinate / witness** | — | **D (perform tests)** | **Witness / A** | I |
| Raise and close punch list | R | **D** | I | **D (rectify)** | **A (close)** | I |
| Compile MDR | R | **D** | I | I | **A** | **D (their data)** |
| Site installation | — | I | — | — | **D** (contractor) | — |
| Commissioning / SAT | — | **Support** | — | — | **D** | Support |

> **The rows to notice are the ones where the PE has no `D` at all** — fault level, arc flash, risk assessment, PLC code, installation. Being clear about those is what makes the rows where you *do* have `D` credible.

---

## 6.3 Technical procurement review

Procurement's enquiry goes out with a technical package. The PE's job before it goes out, and again when quotes come back.

### 6.3.1 Before the enquiry

| Check | Why |
|---|---|
| Is the specification complete enough to quote against? | An incomplete enquiry gets an incomplete quote, and the gap becomes a variation later |
| Are the mandatory technical requirements stated separately from the preferences? | A supplier will optimise anything you have not made mandatory |
| Are the standards and the client's standard called up? | |
| Is the required vendor data listed, with a due date? | **Vendor data always arrives late unless it is a stated deliverable with a date.** GA drawings, wiring diagrams, data sheets, test certificates, O&M manuals. |
| Is the delivery requirement stated as a date, not a lead time? | "12 weeks" from an unstated start is not a commitment |
| Are alternatives invited, and is the process for proposing one stated? | If you do not tell them how to propose an alternative, they will simply quote one |

### 6.3.2 When quotations come back

**Read what they actually quoted, not what you asked for.** Line by line.

| Check | What it catches |
|---|---|
| Part number matches the BOM exactly | Silent substitution (DR-003) |
| Quantity matches | Missed items, or a supplier quoting a pack quantity |
| Accessories included or separately listed | The handle, the aux block, the trip unit, the end cap |
| Options and configuration | **A drive is a type code, not a part number.** Enclosure type, EMC filter class, control card, coating, keypad. |
| Lead time stated per line, not as one figure | One line at 16 weeks hidden behind a headline "8 weeks" |
| Exclusions and qualifications in the fine print | "Excludes commissioning", "subject to stock at time of order" |
| Compliance with the called-up standards | |
| Warranty and local support | Matters for the client's whole-of-life cost, not ours |

**Then produce a technical recommendation** — a short written assessment of whether each quotation is technically compliant, with any qualifications listed. That is what procurement needs to negotiate against, and it is what makes the decision auditable later.

---

## 6.4 Vendor data review

Vendor data is the information that turns a purchase into something you can build around. It arrives late and it changes things.

| Vendor data item | What it affects | What goes wrong |
|---|---|---|
| **Drive GA drawing and dimensions** | Cubicle layout, mounting plate, clearances, cable zone | Arrives after the GA is released for fabrication |
| **Drive manual: recommended fuse/breaker** | Feeder device selection, SCCR | Assumed from motor FLC instead |
| **Drive manual: max motor cable length** | Whether an output filter is required | Not checked against the actual route |
| **Drive heat dissipation figure** | Cubicle thermal design, HVAC declaration | Estimated instead of obtained |
| **Motor nameplate data** | Drive sizing, feeder breaker, cable, thermal settings | **Always late. Plan for it.** |
| **MOV actuator wiring diagram** | Schematic and terminal count | Interface assumed, drafted, then redrawn |
| **Dosing skid data sheet** | Feeder rating, control interface | Preliminary figures used as final |
| **UPS status contact arrangement** | PLC digital inputs | Assumed to exist; turns out to be an option |
| **Switch SFP / fibre type** | Fibre patching, splice type | OM3 vs OM4 vs single-mode mismatch |
| **Test certificates, type test evidence** | MDR completeness | Not requested until handover, then unavailable |

**The PE's rule:** every vendor data item is a **register entry with a due date and an owner**, not an expectation. If it is not tracked, it arrives the week you needed it a month ago.

**And the harder rule:** when vendor data arrives and contradicts the design, that is a change, and it goes through change control — it does not get quietly absorbed by the drafter.

---

## 6.5 Technical query register

Full register: [`registers/tq-register.csv`](registers/tq-register.csv)

| TQ | Subject | Raised | Required by | Impact if not answered | Status |
|---|---|---|---|---|---|
| **TQ-001** | Client Electrical Design Standard not supplied. Also covers: earthing system, form of separation, cable entry direction, spare capacity, wire numbering convention, drive brand standard. | Wk 1 | Wk 3 | **Blocks enclosure fabrication release.** Six assumptions depend on it. | **Closed Wk 11** — released as a consequence of DEV-002 (see Stage 5) |
| **TQ-002** | Prospective short-circuit current at the MCC incomer, and expected duration. | Wk 1 | Wk 4 | **Blocks all MCCB and busbar orders.** Highest cost exposure in the package. | **Open** — escalated twice |
| **TQ-003** | Required Performance Level for the E-stop safety function, and required stop category (0 or 1) given hydraulic surge considerations. | Wk 2 | Wk 6 | Blocks safety relay order; may change safety circuit architecture | **Open** |
| **TQ-004** | Who is performing the protection coordination study, and when will settings be available? | Wk 2 | Wk 10 | Settings cannot be applied or recorded at FAT | **Open** |
| **TQ-005** | Must the MCC operate with switchroom HVAC failed? Two options priced. | Wk 2 | Wk 5 | Changes derating basis, possibly drive frame size, or adds a control interlock | **Closed Wk 7** — client selected HVAC-fail interlock (ramp to minimum speed and alarm), not thermal uprating |
| **TQ-006** | Harmonic distortion limits at the point of connection; is a harmonic assessment being performed? | Wk 3 | Wk 6 | May require an active harmonic filter — **additional cubicle, cost and 12+ week lead** | **Open** — carried as the highest technical risk |
| **TQ-007** | PLC platform standard and IP address schedule. | Wk 1 | Wk 4 | **Blocks all PLC hardware orders** | **Closed Wk 9** — CompactLogix confirmed; IP schedule issued |
| **TQ-008** | Motor nameplate data for P-101 / P-102. | Wk 2 | Wk 6 | Blocks drive, feeder breaker, cable and thermal settings | **Superseded by TQ-009** |
| **TQ-009** | **Revised pump duty — hydraulic re-modelling indicates 90 kW motors required.** Confirm and issue nameplate data. | Wk 12 | Wk 13 | **Major change — see Stage 9** | **Closed Wk 13 — change confirmed** |
| **TQ-010** | MOV-101 actuator control interface — hardwired, analogue or fieldbus? Wiring diagram required. | Wk 3 | Wk 7 | Schematic and terminal count cannot be finalised | **Closed Wk 8** — hardwired open/close/stop with limit feedback |

### How to write a technical query that actually gets answered

Most TQs get ignored because they are written as questions. Write them as decisions:

| Weak | Strong |
|---|---|
| "Please advise the fault level." | "We have assumed 25 kA for 1 s at the MCC incomer. **Unless advised otherwise by [date], we will place breaker orders on this basis, and any subsequent change will be a variation.** Please confirm or provide the actual value." |
| "What PLC do you want?" | "We propose CompactLogix 5380 per attached. This determines module selection, your spares holding and your integrator's resource. **Confirmation required by [date] to hold the programme.**" |

**Three things every TQ must have:** a stated assumption or proposal, a required-by date, and the consequence of not answering. A TQ without a consequence is a request. A TQ with one is a decision point.

> **And send them one at a time, to the right person.** A ten-item TQ sent to a client project manager gets forwarded to three people and answered by none. Individually addressed queries get answered.

---

## 6.6 Drawing revision control

### 6.6.1 Revision convention

| Revision | Meaning | Who can build from it |
|---|---|---|
| A, B, C… | Preliminary / Issued for Review / Issued for Approval | **Nobody** |
| 0 | Issued for Construction (IFC) | Workshop |
| 1, 2, 3… | Revised IFC | Workshop, after a formal re-release |
| As-built | Reflects what was actually built and tested | The client, forever |

### 6.6.2 The rules that actually prevent errors

1. **Nothing is built from a letter revision.** Ever. If the workshop is building from Rev C, someone has lost control of the process.
2. **Every issue goes out on a transmittal** listing drawing number, revision, status and date. No transmittal, no issue.
3. **Every revision carries a revision cloud and a description** of what changed. "General revision" is not a description and should be rejected at review.
4. **Superseded drawings are physically removed from the workshop.** Not marked, not filed on top — removed. A superseded drawing on a bench will be built from.
5. **Every drawing revision triggers a BOM re-reconciliation** and a check of the I/O list and termination schedule.
6. **The integrator gets the I/O list at the same revision as the schematics**, on a transmittal.

### 6.6.3 Revision history

| Rev | Date | Description | Reason |
|---|---|---|---|
| A | Wk 2 | First issue for internal review | — |
| B | Wk 5 | Reconciliation findings incorporated: neutral corrected to full size; Local mode permissives corrected; LCS cable 12C → 16C; aux contact blocks added; screen earthing note added to termination drawings | Internal review + reconciliation passes |
| C | Wk 9 | Client standard incorporated (TQ-001 closed); HVAC-fail interlock added (TQ-005); MOV interface finalised (TQ-010); PLC platform confirmed (TQ-007) | TQ closures |
| **0** | Wk 11 | **Issued for Construction** | Design freeze |
| **1** | Wk 14 | **Motor uprate 75 → 90 kW — see Stage 9** | TQ-009 / DI-024 |
| As-built | Wk 22 | FAT mark-ups and punch-list rectifications incorporated | Post-FAT |

---

## 6.7 Change control

**A change is anything that alters an approved deliverable.** Not every change is a variation, but every change is a change.

### The process

```
Change identified (client request, vendor data, TQ answer, FAT defect, workshop finding)
   ↓
Logged in the change register with a unique number
   ↓
TECHNICAL IMPACT ASSESSMENT
   Which drawings? Which BOM lines? Which already-purchased items?
   Which already-fabricated work? Which tests must be repeated?
   ↓
COST AND SCHEDULE IMPACT ASSESSMENT
   Re-engineering hours · new material · restocking/cancellation
   rework labour · retest · delay to the critical path
   ↓
CLIENT NOTIFICATION with the assessment attached
   ↓
CLIENT DECISION (proceed / don't proceed / proceed with variation)
   ↓
IMPLEMENT — drawings revised, BOM revised, POs amended,
            workshop re-briefed, FAT procedure updated
   ↓
VERIFY — reconciliation re-run, change register closed
```

**The failure mode to avoid at all costs:** a change gets implemented on the drawings but not in the BOM, or in the BOM but not in the FAT procedure. Then the board gets built one way, tested against a procedure written for another, and nobody notices until site.

**The other failure mode:** absorbing small changes without logging them, because each one individually seems too minor to be worth the paperwork. Ten absorbed changes is a package that no longer matches its own documentation.

---

## 6.8 Worked example — vendor data forces a change

**Event.** The drive GA drawing arrives from the manufacturer in Week 10. The drive's required clearance above the unit for airflow is greater than the cubicle layout allowed, because the layout was drafted from a generic dimension rather than the actual manufacturer's data.

**Why it happened.** The GA was drafted before the vendor data arrived, using a dimension from a previous project. It was drafted early because the programme demanded it. That is a reasonable commercial decision **provided the drawing is not released for fabrication until the vendor data confirms it** — and in this case the release was pending, so the cost was contained.

**Impact assessment:**

| Impact | Detail |
|---|---|
| Drawings | GA-0020 revised — drive cubicle height increased |
| Fabrication | Not yet released. **No rework.** |
| BOM | Enclosure dimensions revised; no new items |
| Cost | Modest increase in enclosure cost |
| Schedule | Nil — fabrication had not started |
| Thermal | Heat load declaration to the HVAC designer reissued |

**What made this cheap.** The general arrangement was held from release pending vendor data. Had it been released, this would have been a fabricated cubicle requiring modification or replacement.

> **The transferable rule:** *you can draft ahead of vendor data, but you must not release ahead of it.* Knowing which documents can run ahead and which cannot is a scheduling skill, and it is exactly what a Project Engineer is paid for.

---

## 6.9 Long-lead equipment issue — worked example

**Event.** VSD lead time quoted at 16 weeks against a 12-week programme allowance (Stage 5, DR-005).

**Options and assessment:**

| Option | Cost | Schedule | Risk | Assessment |
|---|---|---|---|---|
| Substitute an alternative drive | −8 % headline, but the option card erodes most of it | −4 wks | Drawing rework, client standard conflict, whole-of-life orphan brand | **Rejected by client** |
| Order the specified drive immediately, before the design freeze | Nil | −0 wks | **Commercial risk — if the design changes, the drive may be wrong** | Considered, not taken. **And this turned out to be the right call — the motor uprate in Stage 9 would have made those drives scrap.** |
| Accept the lead time and re-sequence the build | Nil | −3 wks recovered | Workshop scheduling complexity | **Selected** |
| Escalate to the client for programme relief | Nil | Depends | — | Done in parallel |

**Selected action.** Re-sequence: build and wire the enclosure, busbar, terminals, PLC section and all small feeders first. Leave the drive cubicles until last. Net programme impact reduced from 4 weeks to approximately 1 week.

> **Two things worth noticing, and both are worth saying out loud in an interview:**
>
> **First — the recovery came from re-sequencing, not from compromising the design.** That is the move that distinguishes a project engineer from an expediter.
>
> **Second — the option that looked most attractive on schedule (order early, before the design freeze) would have been a disaster.** The motor uprate arrived in Week 12. Two 75 kW drives ordered in Week 6 would have been scrap or a restocking fight. Holding the order until the design was frozen looked slow at the time and was correct. **Being able to say "the cautious call looked wrong for six weeks and then turned out to be right" is a more honest and more convincing story than a run of clean wins.**

---

## 6.10 What the Project Engineer did at Stage 6

1. Issued a preliminary BOM early purely to surface lead times.
2. Wrote TQs as decision points with dates and consequences, and sent them individually.
3. Escalated TQ-002 (fault level) twice, in writing, and made the commercial exposure explicit to the project manager — because the decision to order breakers against an assumption is a commercial decision, not an engineering one.
4. Reviewed every quotation line by line against the BOM.
5. Tracked vendor data as register items with dates, not as expectations.
6. Held the general arrangement from fabrication release until the drive vendor data arrived.
7. Stopped an unapproved substitution and converted it into a formal deviation.
8. Maintained revision control, with a hard rule that nothing is built from a letter revision.
9. Kept the systems integrator on the same revision as the board.

---

**Next:** [Stage 7 — Fabrication and Inspection](07-FABRICATION-AND-INSPECTION.md)
