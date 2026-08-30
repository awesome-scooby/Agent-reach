# 🔒 SEALED — BRK-AUDIT-01 Answer Key

> **DO NOT READ THIS UNTIL PHASE 10 (Week 16).**
>
> If you read it now, you lose the single best assessment in the course.
> There is no way for me to un-teach you the answers.
> Do the audit first. Send me your findings. Then open this.

---

## The 14 planted defects

| # | Activity | Family | Defect | Consequence |
|---|---|---|---|---|
| 1 | `BA1020` Project Management and Reporting | Type / Duration | 120-day **Task Dependent** activity that should be **Level of Effort**. It also has no successor. | A task-dependent 120d bar can drive the critical path and consume float that belongs to real work. LOE activities must never drive logic. |
| 2 | `BA1060` Issue SLD for Client Approval | Logic | **Redundant relationship** — `BA1040` links to it directly, but `BA1040 → BA1050 → BA1060` already exists. | Clutters the network, hides the true driving path, and makes driving-predecessor analysis unreliable. |
| 3 | `BA1070` Client Approval — SLD | Lag | **FS+45** lag. Forty-five working days of nothing. | A lag is invisible, unresourced, un-progressable time. If that wait is real, it must be an activity you can track and claim against. |
| 4 | `BA1120` Design Sign-off | Duration | **Zero-duration Task Dependent** activity. | Zero-duration work is a milestone by definition. As a task it behaves unpredictably and reports meaningless % complete. |
| 5 | `BA1150` Manufacture and Delivery — ACBs | Calendar | 120-day supplier lead time sitting on **FACTORY-5D**. | The supplier does not stop for weekends. On a 5-day calendar this adds roughly 48 calendar days of pure fiction. Should be `CAL-7D`. Also breaches the DCMA excessive-duration test (>44 days). |
| 6 | `BA1260` Internal Wiring — Power | Lag | **FS−10 negative lag (lead)** from ACB installation. | Says wiring starts 10 days before ACB install finishes. If that is true, the relationship is SS+lag, not a lead. Auditors treat leads as a defect because they hide the real dependency and can distort float. |
| 7 | `BA1280` Labelling and Warning Signage | Logic | **Open end — no successor.** | Nothing pulls it. It can slip indefinitely with no effect on the finish date, so the schedule says labelling doesn't matter. It does — the board can't be released without it. |
| 8 | `BA1310` Factory Acceptance Test | Constraint | **Mandatory Finish** constraint. | The most dangerous constraint in P6. It *overrides logic* — predecessors can slip and this date will not move, silently hiding the delay and destroying the float calculation downstream. |
| 9 | `BA1320` / `BA1330` FAT defect loop | Logic | `BA1320` Client Defect List Issued has **no successor**, and `BA1330` Rectify FAT Defects is driven **SS from FAT itself**. | Rectification begins the same day FAT starts — before anyone knows what the defects are. Reverse logic. The rectification duration is also unearned: it should be driven by the defect list. |
| 10 | `BA1360` / `BA1370` Transport & Offload | Calendar | Transit and site offload sitting on **FACTORY-5D**. | Transport runs on calendar days; offload happens on a 6-day site. Wrong calendars in the site handover window — exactly where interface delays get argued about. |
| 11 | `BA1390` Pull LV Power Cables | Logic | **Open end — no predecessor (dangling start).** | It floats free and can be scheduled on day one of the project. In reality it cannot start until the board is set to position. Its float will read as enormous and nobody will chase it. |
| 12 | `BA1410` Site QA and Snag | Relationship type | **Start-to-Finish** with no justification. | SF is legitimate in perhaps one relationship in a thousand (shift handovers, temporary supply changeover). Here it is almost certainly a mis-click for FS. Every SF must carry a written justification. |
| 13 | `BA1430` Energisation | Constraint / Logic | **No predecessor at all** — driven only by a `Start On` constraint. Pre-Energisation Testing (`BA1420`) therefore has no successor. | The single most important date on the job is a typed date, not a calculated one. If testing slips, energisation does not move. The schedule cannot tell you that you are late. |
| 14 | `BA1460` Practical Completion | Constraint | **Finish On or Before** constraint. | Generates artificial negative float across the whole network. Negative float from a constraint is not a real delay signal — it masks where the genuine pressure is. |

---

## How to score it

| Band | Score | Verdict |
|---|---|---|
| Found 12–14 | 90–100 | You audit like a lead planner. |
| Found 9–11 | 70–89 | Strong. You would pass a project controls interview. |
| Found 6–8 | 50–69 | Competent but you are missing the constraint and calendar families. |
| Found 3–5 | 30–49 | You are reading the bar chart, not the network. |
| Found 0–2 | 0–29 | Re-do Phase 5 before continuing. |

**The schedule's own score under the roadmap rubric: 31/100.** It would be rejected by any competent client planner.

---

## The three defects that would cost real money

If you only catch three, catch these:

1. **`BA1310` Mandatory Finish on FAT** — hides delay until it is too late to recover.
2. **`BA1430` Energisation with no logic** — the client's date is disconnected from the work that delivers it.
3. **`BA1150` lead time on the wrong calendar** — you will order too late and never know why you were late.
