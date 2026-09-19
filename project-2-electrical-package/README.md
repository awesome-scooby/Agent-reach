# PROJECT 2 — FULL ELECTRICAL PACKAGE

**Northfield Raw Water Pump Station — Motor Control Centre MCC-01**
Reference design package: SLD → Schematic → Termination → BOM → Procurement → Fabrication → FAT → Handover

---

## What this is

A **self-directed reference project**. It is not delivered work for a real client. Every document here was produced to work through, end to end, how an industrial electrical package actually develops — from a client's design inputs, through drawings and procurement, into a workshop, through Factory Acceptance Test, and out the other side as a handover dossier.

The scenario, client and site are fictional. The engineering logic, the document set, the workflow and the failure modes are real and are drawn from normal Australian industrial practice.

**Read `00-CLAIM-INTEGRITY.md` before you talk to anybody about this package.** It sets out exactly what you may and may not claim, and gives you the wording. Getting that boundary right is worth more in an interview than any drawing in here.

---

## Scenario in one paragraph

A regional water utility is upgrading the raw water transfer pump station at the Northfield Water Treatment Plant. Two ageing fixed-speed 55 kW transfer pumps are being replaced with two variable-speed pumps in duty/assist configuration — specified at 75 kW, then **uprated to 90 kW by a late client change after the design freeze** (Stage 9) — and the existing switchboard is being replaced with a new Form 3b 415 V motor control centre. The MCC also feeds a sump pump, an instrument air compressor, a motorised isolation valve, a vendor-supplied chemical dosing skid, switchroom services and a light-and-power distribution board. Control is by a plant PLC in the MCC with a remote I/O node at the intake screen kiosk, reporting to the existing plant SCADA over fibre. The package scope is design, supply, fabrication, factory test and delivery of MCC-01 and the associated field control stations. Installation, termination in the field, and commissioning are others' scope.

---

## Document set

| # | Document | What it covers |
|---|---|---|
| 00 | [`00-CLAIM-INTEGRITY.md`](00-CLAIM-INTEGRITY.md) | What you can and cannot claim. Read first. |
| 01 | [`01-DESIGN-BASIS.md`](01-DESIGN-BASIS.md) | Stage 1 — scope, voltages, loads, fault level, environment, standards, assumptions, exclusions, interfaces, Design Input Register |
| 02 | [`02-SINGLE-LINE-DIAGRAM.md`](02-SINGLE-LINE-DIAGRAM.md) | Stage 2 — the engineering logic behind the SLD, device by device |
| 03 | [`03-SCHEMATICS.md`](03-SCHEMATICS.md) | Stage 3 — control philosophy → schematic logic, INPUT→LOGIC→OUTPUT→FEEDBACK→FAILURE |
| 04 | [`04-TERMINATIONS.md`](04-TERMINATIONS.md) | Stage 4 — terminal numbering philosophy, segregation, screens, earths, termination schedule |
| 05 | [`05-BOM.md`](05-BOM.md) | Stage 5 — bill of materials, three-way reconciliation method, worked discrepancy |
| 06 | [`06-PROCUREMENT-AND-ENGINEERING-CONTROL.md`](06-PROCUREMENT-AND-ENGINEERING-CONTROL.md) | Stage 6 — vendor data, technical queries, revisions, responsibility matrix |
| 07 | [`07-FABRICATION-AND-INSPECTION.md`](07-FABRICATION-AND-INSPECTION.md) | Stage 7 — what to inspect during manufacture, inspection checklist |
| 08 | [`08-FAT.md`](08-FAT.md) | Stage 8 — full FAT procedure, FAT sheet, six worked defects |
| 09 | [`09-DESIGN-CHANGE.md`](09-DESIGN-CHANGE.md) | Stage 9 — late motor uprate traced through every document |
| 10 | [`10-HANDOVER-MDR.md`](10-HANDOVER-MDR.md) | Stage 10 — manufacturer's data record structure and handover |
| 11 | [`11-PORTFOLIO-SUMMARY.md`](11-PORTFOLIO-SUMMARY.md) | Stage-by-stage portfolio view: inputs, responsibilities, decisions, risks, documents, interfaces, quality checks, lessons, employer value |
| 12 | [`12-INTERVIEW-PACK.md`](12-INTERVIEW-PACK.md) | 60-second / 3-minute / 10-minute explanations, 10 manager questions with model answers, 5 questions that expose bluffing |
| 13 | [`13-STUDY-GAPS.md`](13-STUDY-GAPS.md) | What you must study before claiming competency, in priority order |
| **14** | [**`14-CORE-CONCEPTS.md`**](14-CORE-CONCEPTS.md) | **The physics behind the decisions** — three-phase power and where current figures come from, fault current, the induction motor, how a VSD actually works, the affinity laws, harmonics, switching vs protecting vs isolating, earthing, the 4–20 mA loop, the PLC scan, what destroys a pump, IP and Forms decoded |
| **15** | [**`15-GLOSSARY.md`**](15-GLOSSARY.md) | **Every term and abbreviation in plain English**, with why it matters here — plus the terms that sound similar and are not |
| **16** | [**`16-START-COMMAND-TRACE.md`**](16-START-COMMAND-TRACE.md) | **One command traced end to end**, from rising water level to water moving, touching every document — then run backwards as a fault-finding method |
| **17** | [**`17-EXPLAINING-TO-OTHERS.md`**](17-EXPLAINING-TO-OTHERS.md) | **Five audiences** from recruiter to principal engineer, analogies that work and analogies that mislead, twelve hostile follow-ups, the teach-back protocol, and recall drills |

## Drawings (`drawings/`)

| Drawing | Title |
|---|---|
| `NFD-ELE-SLD-0001.svg` | MCC-01 Single Line Diagram |
| `NFD-ELE-SCH-0030.svg` | Control power distribution — 240 VAC and 24 VDC |
| `NFD-ELE-SCH-0040.svg` | Emergency stop and safety circuit |
| `NFD-ELE-SCH-0101.svg` | Transfer Pump P-101 — VSD power and control |
| `NFD-ELE-SCH-0201.svg` | PLC digital input schematic (typical) |
| `NFD-ELE-TRM-0401.svg` | Termination drawing — terminal rail X3 (24 VDC digital) |

These are drawn to communicate engineering intent and to be readable in an interview. **They are not CAD deliverables and are not to be presented as production drawings.** A real package is drafted in AutoCAD Electrical, EPLAN or SEE Electrical with a proper title block, drawing register and revision control.

## Registers (`registers/`)

CSV and XLSX versions of the working documents, so they can be opened, sorted and edited the way real registers are:

`design-input-register` · `tq-register` · `io-list` · `cable-schedule` · `termination-schedule` · `bom` · `fat-sheet` · `punch-list` · `inspection-checklist` · `mdr-index`

`project-2-registers.xlsx` contains all ten as formatted, filterable sheets with a cover page carrying the same claim-integrity warnings.

## Interactive portfolio

`portfolio.html` — single-file offline HTML portfolio (305 KB, no external requests). Thirteen modules covering claim integrity, all ten stages, interview preparation and study gaps, with all six drawings embedded as scalable SVG and 47 knowledge-check questions that explain *why* each wrong answer is wrong.

Opens straight from `file://`, works at phone width, and prints with the navigation stripped and all answer feedback expanded. Progress is stored in your browser only. The registers are **not** duplicated inside it — open the CSV/XLSX for those.

---

## How to use this to get a job

1. Read `00-CLAIM-INTEGRITY.md`. Learn the boundary.
2. Read `14-CORE-CONCEPTS.md`. **Do this before the stage documents, not after.** It is the physics that makes everything else derivable rather than memorised, and it is the layer an interviewer reaches within about two questions.
3. Work through documents 01–10 **in order**, keeping `15-GLOSSARY.md` open beside you.
4. Read `16-START-COMMAND-TRACE.md`. If you can narrate that, you understand the package as a system rather than as a stack of drawings.
5. Do the recall drills in `17-EXPLAINING-TO-OTHERS.md` §5 — whiteboard and numbers, no notes. Recognition is not recall.
6. Do the exposure questions in `12-INTERVIEW-PACK.md` out loud. If you cannot answer one without reading, you do not own that part yet.
7. Rehearse the audience ladder in `17-EXPLAINING-TO-OTHERS.md` §1. A recruiter screens you before an engineer ever does.
8. Close the remaining gaps in `13-STUDY-GAPS.md`.
9. Then, and only then, put it on your CV as *"Self-directed reference project: full industrial electrical package, design basis through FAT and handover."*

The point of this package is not the documents. It is that you can explain them.

---

## Errata

Errors found and corrected are recorded here rather than quietly fixed, because the correction is more instructive than the original.

| Date | Error | Correction |
|---|---|---|
| Rev 2 | The full-size neutral was justified by "triplen harmonics from the six-pulse drives". **Wrong.** A balanced six-pulse rectifier produces characteristic harmonics of order 6k ± 1 (5th, 7th, 11th, 13th), which are positive- and negative-sequence and do **not** add in the neutral. | The conclusion stands — the neutral is full size — but the source is the **single-phase** non-linear load: switch-mode supplies, the UPS input, and the lighting and GPO circuits on DB-01. The drives justify the *harmonic assessment*; the single-phase load justifies the *neutral*. Corrected on the SLD face, in `02`, `11`, `12`, `13` and the portfolio. See `14-CORE-CONCEPTS.md` §6.2. |
