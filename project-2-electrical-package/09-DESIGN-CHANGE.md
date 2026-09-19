# STAGE 9 — DESIGN CHANGE EXERCISE

**Change:** CR-001 — Transfer pump motors uprated from 75 kW to 90 kW
**Raised:** Week 12 · **Confirmed:** Week 13 · **Implemented:** drawings Rev 1, Week 14

---

## 9.1 The change

In Week 12 — **after the design freeze at Week 11 and after Issued for Construction drawings had been released to the workshop** — the client issued TQ response TQR-009.

Their hydraulic consultant had re-run the network model with updated demand projections and revised pipe roughness figures for the ageing rising main. The revised duty point moved outside the 75 kW pumps' capability at the required flow. The pump vendor confirmed that meeting the new duty requires a larger impeller and a **90 kW motor**.

**This is not an unusual event.** Hydraulic modelling frequently completes after electrical detailed design has started, because the electrical package is on the critical path and the modelling is not. Anyone who has worked on a water project has seen this. The question is not whether it happens — it is whether the package was built in a way that allows it to be traced.

---

## 9.2 Why the timing is the problem, not the change

A 15 kW uprate is trivial engineering. The difficulty is entirely in *when* it arrived:

| Status at Week 12 | Consequence |
|---|---|
| Design frozen, drawings at IFC Rev 0 | Every affected drawing must be revised and formally re-released |
| Enclosure fabrication released and in progress | Cubicle dimensions may need to change — **potential rework of fabricated steel** |
| VSDs **not yet ordered** (held pending the design freeze and the DEV-002 process) | **This is the single biggest piece of luck in the project — and it was not luck.** See §9.9. |
| MCCBs on order | Feeder breakers may need to change — cancellation or restocking |
| PLC hardware on order | Unaffected |
| Terminals, wiring accessories received | Largely unaffected; lugs and glands affected |
| Wiring not yet started on the drive cubicles | Because of the re-sequencing decision in Stage 6. **Also not luck.** |
| FAT procedure written | Requires revision |
| Heat load declared to HVAC designer | Must be reissued |

---

## 9.3 The trace

```
CLIENT REQUIREMENT  ──  TQR-009: 90 kW motors required
        │
        ▼
TECHNICAL REVIEW    ──  Impact assessment across every document. §9.4
        │
        ▼
SLD                 ──  Motor rating, FLC, feeder device, cable size, load schedule,
                        maximum demand, spare capacity check
        │
        ▼
SCHEMATIC           ──  Drive model, thermal parameters, STO terminals,
                        thermistor relay, parameter schedule
        │
        ▼
TERMINATION         ──  Conductor size, lug size, gland size, gland plate cutout,
                        terminal rating
        │
        ▼
BOM                 ──  Drive, reactor, MCCB, cable, lugs, glands, enclosure
        │
        ▼
PROCUREMENT         ──  PO amendments, cancellations, re-quotes, lead times
        │
        ▼
FABRICATION         ──  Cubicle dimensions, mounting plate, thermal design, build sequence
        │
        ▼
FAT                 ──  Procedure revision, parameter schedule, retest scope
        │
        ▼
AS-BUILT            ──  Revision history, deviation record, MDR
```

---

## 9.4 Impact assessment, document by document

### 9.4.1 Design basis — NFD-ELE-DBS-0001

| Item | From | To | Note |
|---|---|---|---|
| P-101 / P-102 rating | 75 kW | **90 kW** | |
| Estimated FLC (each) | ~135 A | **~160 A** | **Typical figure. Must be confirmed from the motor nameplate.** |
| Both pumps running | 270 A | **320 A** | |
| Estimated maximum demand | ~397 A | **~447 A** | |
| Incomer 630 A adequate? | — | **Yes** | 447 A against a 630 A frame. Confirmed, with margin retained. |
| Busbar 800 A adequate? | — | **Yes** | |
| **Transformer TX-01 capacity** | — | **Must be re-checked** | 500 kVA ≈ 695 A. The MCC's demand is now ~447 A, but **TX-01 also feeds other site loads that are not in our scope.** Raised with the client as TQ-011. **This is the check most likely to be missed and the one with the largest consequence.** |
| Declared heat load to HVAC | Based on 2 × 75 kW | **Reissued** | Drive losses scale roughly with rating. IFM-002 Rev B issued the same week. |

> **TQ-011 is the finding that matters most in this whole exercise, and it is the one a graduate would miss.** It is easy to check that the MCC's own incomer and busbar still cope. It takes a step back to ask whether the **transformer upstream** — which belongs to someone else and feeds loads that are not on our drawings — still has capacity. If it does not, the consequence is a transformer replacement: six-figure cost, long lead, and an outage. Asking that question in Week 13 rather than at commissioning is worth more than everything else in this document.

### 9.4.2 SLD — NFD-ELE-SLD-0001 → Rev 1

| Element | Change |
|---|---|
| Motor rating annotation | 75 kW → 90 kW |
| FLC annotation | ~135 A → ~160 A (provisional) |
| VSD rating | 75 kW → 90 kW |
| Feeder MCCB Q11 / Q12 | **Re-select from the new drive manual.** Provisionally still a 250 A frame with a different trip setting, but this must be confirmed from the drive's documentation, not assumed. |
| Motor cable | 70 mm² → **95 mm² (provisional)** — pending an AS/NZS 3008.1.1 calculation |
| Line reactor | Re-rated to suit the 90 kW drive |
| Connected load schedule | Updated |
| Drawing notes | Provisional-rating notes updated |

> **The cable size change is a genuine calculation, not a guess.** 70 mm² → 95 mm² above is a plausible step for the increased current, but the actual answer depends on route length, installation method, grouping, ambient, volt drop over the run, fault withstand for the disconnection time, and the drive manufacturer's constraints on VSD cable type. **I have not performed that calculation and do not claim to have.** The designer produces it; the PE checks that its inputs match reality. See `00-CLAIM-INTEGRITY.md`.

### 9.4.3 Schematics — SCH-0101 / SCH-0111 → Rev 1

| Element | Change |
|---|---|
| Drive model reference | Updated |
| **STO terminal designations** | **Must be verified against the new drive's manual.** Within the same product family they are usually identical — but "usually" is not "verified", and this is the safety circuit. Verified: unchanged. |
| Drive parameter schedule | Motor nameplate data, thermal model, current limits, ramp times all revised |
| Thermistor relay | Unchanged — the relay does not care about motor size |
| Control logic | **Unchanged.** The control philosophy is independent of motor size. |
| Feeder device rating annotation | Updated |

> **Checking the STO terminals rather than assuming them is the correct behaviour, and it costs five minutes.** Any change that touches a drive in a safety circuit requires the safety interface to be re-verified, even when you fully expect it to be identical. Expecting is not verifying.

### 9.4.4 Termination drawings and schedule — TRM → Rev 1

| Element | Change |
|---|---|
| Motor cable conductor size | 70 mm² → 95 mm² (provisional) |
| **Compression lugs** | **Changed.** A 95 mm² lug is a different part. Already-ordered lugs are now wrong. |
| **EMC gland size** | **Changed.** A larger cable needs a larger gland. |
| **Gland plate cutout** | **Changed.** And the gland plates may already be fabricated. |
| Drive terminal capacity | **Verify the 90 kW drive's terminals accept 95 mm² directly** — some drives require a cable box or a busbar adaptor above a certain size. **This is a real trap.** |
| Control terminations | Unchanged |
| Termination schedule | Cable size column updated; internal control rows unchanged |

> **"The drive terminals may not accept the cable" is the kind of detail that stops a job dead at site.** It is in the drive manual, it takes two minutes to check, and it is invisible on any drawing. A PE who checks it looks prescient. A PE who does not finds out from an installer on a Friday afternoon.

### 9.4.5 BOM — → Rev D

| Item | Change | Procurement status at Week 13 | Action |
|---|---|---|---|
| C04 — VSD | 75 kW → 90 kW | **NOT ORDERED** | Re-quote and order. **No cancellation cost.** |
| C05 — line reactor | Re-rated | Not ordered | Re-quote |
| C01 — feeder MCCB | Setting change; frame confirmed from drive manual | **ON ORDER** | Confirm suitability. Frame unchanged → **no change required.** |
| K10 — compression lugs | Size change | **ON ORDER** | Amend PO before despatch, or accept and re-order |
| C06 — EMC glands | Size change | Not ordered (deliberately held pending cable size) | Order correct size. **The decision to hold these saved money.** |
| A02 — gland plates | Cutout change | Fabricated, undrilled | **Undrilled — no rework.** |
| A01 — enclosure | Drive cubicle dimensions | **IN FABRICATION** | **See §9.5 — the critical question** |
| Motor cable | 70 → 95 mm² | Installer's scope | Notify installation contractor immediately — they may have ordered cable |

### 9.4.6 FAT procedure — → Rev 1

| Element | Change |
|---|---|
| Drive parameter verification | New parameter schedule |
| Motor thermal parameters | New nameplate data |
| Speed reference tracking | Unchanged in method |
| STO test | Unchanged, but re-verified against the new drive |
| Protection settings record | Updated device settings |
| All other tests | Unchanged |

---

## 9.5 The critical question: does the cubicle need to change?

This determines whether the change costs a modest amount or a large amount.

**The question:** is the 90 kW drive physically larger than the 75 kW drive?

**The wrong way to answer it:** assume that because they are in the same product family they are the same frame size. Drive manufacturers group ratings into frame sizes, and the boundaries are not intuitive. Two adjacent kW ratings may share a frame, or may not.

**The right way:** obtain the manufacturer's general arrangement drawing for the specific 90 kW unit and compare dimensions, mounting centres, clearance requirements and heat dissipation against what the cubicle was designed for.

**In this case:** the vendor GA confirmed the 90 kW unit is in a **larger frame** — greater height and depth, and a greater required clearance above for airflow.

**Consequence:** the drive cubicles must be deeper and taller.

**Resolution:**

| Option | Assessment |
|---|---|
| Modify the cubicles in fabrication | Fabrication had progressed to the frame and panel stage but the drive cubicle internals were not complete. **Modification feasible.** Selected. |
| Replace the drive cubicles | Full cost of two cubicles plus schedule. Avoided. |
| Fit the larger drive with reduced clearance | **Rejected outright.** Reducing manufacturer-specified clearance causes over-temperature trips, in summer, after handover, when nobody remembers why. It also compromises the thermal verification. Not a real option. |

**Also required:** the heat load declaration to the HVAC designer was reissued, because the switchroom cooling design depends on it, and larger drives dissipate more.

---

## 9.6 Cost impact

> **The figures below are ILLUSTRATIVE PLACEHOLDERS to demonstrate the structure of a cost impact assessment.** They are not quotations and they are not estimates of real market prices. On a real project every line comes from a vendor quote or a rate. **Do not present these numbers as real, and do not let anyone believe you priced this.** Present the *structure* — that is what has value.

| Cost element | Direction | Basis | Comment |
|---|---|---|---|
| VSD price difference, 75 → 90 kW (× 2) | **Increase** | Vendor re-quote | Real, unavoidable |
| VSD cancellation / restocking | **Nil** | — | **Because the order had not been placed** |
| Line reactor re-quote | Increase | Vendor | Modest |
| Feeder MCCB | **Nil** | Frame unchanged | Confirmed from drive manual |
| Compression lugs and glands | Increase | Minor | Glands had not been ordered |
| Gland plates | **Nil** | Undrilled | The undrilled decision paid off |
| Cubicle modification | **Increase** | Panel builder variation | The largest fabrication item |
| Cable size increase (installer's scope) | Increase | Installer's variation | **Not our cost, but our responsibility to notify early** |
| Engineering — drawing revisions | Increase | Hours | SLD, 2 schematics, termination, GA, BOM, FAT |
| Engineering — cable calculation | Increase | Hours | Designer |
| FAT procedure revision | Increase | Hours | Minor |
| **Avoided cost — scrapped drives** | **Avoided** | — | **See §9.9** |

**The structure of the answer is the deliverable.** When an interviewer asks "what did that change cost?", the credible reply is:

> *"I can't give you a figure without the quotes, and I wouldn't trust one that I could. What I can tell you is where the cost sits: the drives, the cubicle modification, the engineering hours for the revisions, and the cable variation on the installer's side. The two biggest potential costs — cancelling the drive order and reworking finished cubicles — were both avoided, and they were avoided because of decisions made weeks earlier."*

---

## 9.7 Schedule impact

| Activity | Impact | Mitigation |
|---|---|---|
| Drawing revisions | ~1 week | Prioritised; the drive cubicle drawings were revised first because fabrication was waiting |
| VSD procurement | **Re-quote and re-order, ~1 week lost on an already 14–16 week item** | This is the critical path. Escalated immediately. |
| Cubicle modification | ~1 week | Overlapped with other fabrication |
| Wiring | **Nil** | Drive cubicles were already scheduled last (Stage 6 re-sequencing) |
| FAT | Deferred to match drive delivery | Client notified in Week 13, with a revised programme |
| **Net impact** | **Approximately 2–3 weeks on the critical path** | |

**What made it 2–3 weeks instead of 8–10:**

1. The drive order had not been placed. *(No cancellation, no restocking dispute, no scrapped equipment.)*
2. The build had been re-sequenced so the drive cubicles were last. *(No wiring rework.)*
3. The gland plates were undrilled. *(No plate rework.)*
4. The glands and lugs were held pending confirmed cable sizes. *(Minimal wrong stock.)*
5. The general arrangement was held from release until vendor data arrived. *(Stage 6 — the cubicle was modifiable, not scrap.)*

> **Every one of those five is a decision made before the change was known.** That is the real lesson of this stage and it is the thing worth saying in an interview:
>
> *"The change cost two to three weeks instead of eight, and none of the reasons for that happened after the change arrived. They were all decisions taken earlier — holding the drive order until the design was frozen, sequencing the build so the drives were last, leaving the gland plates undrilled, holding the GA until vendor data landed. None of them looked clever at the time. One of them looked slow. Project engineering is mostly about not closing doors before you have to."*

---

## 9.8 What did NOT change — and why saying so matters

| Element | Why unchanged |
|---|---|
| Control philosophy | Independent of motor size |
| Schematic control logic | Same permissives, same interlocks, same modes |
| PLC I/O list | Same points, same addresses |
| Safety circuit architecture | Same devices, same channels *(STO terminals verified, not assumed)* |
| Terminal numbering | Same |
| Incomer and busbar | Adequate with margin, verified |
| Network design | Same |
| Field control stations | Same |

**A good impact assessment states what is unaffected as explicitly as what is affected.** It prevents unnecessary rework, it prevents unnecessary retest scope, and it gives the client confidence that the assessment was actually done rather than guessed. An assessment that only lists changes leaves everyone wondering what was checked.

---

## 9.9 The decision that mattered most

Go back to Stage 6, §6.9. Four options were considered for the 16-week drive lead time. One of them was:

> *"Order the specified drive immediately, before the design freeze."*

On schedule alone, it was the most attractive option. It would have recovered the full four weeks. There was real pressure to take it.

It was rejected because **the design was not frozen, the motor data was not confirmed, and ordering a long-lead, high-value, configured item against unconfirmed data is a commercial risk that belongs to whoever takes it.**

Six weeks later the motors were uprated.

**Two 75 kW drives, ordered in Week 6, would have been scrap** — or at best the subject of a restocking negotiation on a configured product that suppliers are reluctant to take back.

**Say this in an interview, exactly like this:**

> *"There was a decision I made that looked wrong for about six weeks. We had a sixteen-week lead time on the drives against a twelve-week programme, and the obvious fix was to just order them early. I held the order because the motor data wasn't confirmed and the design wasn't frozen, and I recovered the time by re-sequencing the build instead. For six weeks that looked like being overly cautious and it cost me some goodwill with the planner. Then in week twelve the client uprated the motors, and those drives would have been scrap. I'd like to say I predicted it — I didn't. What I actually did was refuse to commit to a long-lead, configured item against unconfirmed inputs, which is a rule rather than a prediction. The rule is what saved it."*

That answer is strong because it is honest about not having foreseen the change, it identifies the transferable principle, and it demonstrates that you understand the difference between luck and process. A manager will recognise it immediately.

---

## 9.10 Change record

| Field | Entry |
|---|---|
| Change number | CR-001 |
| Raised | Week 12, client TQ response TQR-009 |
| Description | Transfer pump motors uprated 75 kW → 90 kW following hydraulic re-modelling |
| Origin | Client — external to our scope |
| Technical assessment | Completed Week 12–13 |
| Documents revised | DBS-0001, SLD-0001, SCH-0101, SCH-0111, TRM-0401, TRM-0405, GA-0020, BOM Rev D, FAT-0001, cable schedule, IFM-002 (heat load) |
| Documents verified unchanged | I/O list, SCH-0040 *(STO terminals verified)*, SCH-0030, SCH-0201–0204, LCS drawings, RIO drawings |
| New technical query raised | **TQ-011 — TX-01 transformer capacity with revised MCC demand plus existing site loads** |
| Cost impact | Assessed and issued to client Week 13 — structure per §9.6 |
| Schedule impact | ~2–3 weeks on the critical path |
| Client approval | Received Week 13 |
| Implemented | Drawings Rev 1, Week 14 |
| Verification | Full BOM reconciliation re-run at Rev 1. FAT procedure revised. |
| Closed | Week 14 |

---

**Next:** [Stage 10 — Handover and MDR](10-HANDOVER-MDR.md)
