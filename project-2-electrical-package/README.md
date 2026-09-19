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

A regional water utility is upgrading the raw water transfer pump station at the Northfield Water Treatment Plant. Two ageing fixed-speed 55 kW transfer pumps are being replaced with two 75 kW variable-speed pumps in duty/assist configuration, and the existing switchboard is being replaced with a new Form 3b 415 V motor control centre. The MCC also feeds a sump pump, an instrument air compressor, a motorised isolation valve, a vendor-supplied chemical dosing skid, switchroom services and a light-and-power distribution board. Control is by a plant PLC in the MCC with a remote I/O node at the intake screen kiosk, reporting to the existing plant SCADA over fibre. The package scope is design, supply, fabrication, factory test and delivery of MCC-01 and the associated field control stations. Installation, termination in the field, and commissioning are others' scope.

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

`design-input-register` · `io-list` · `bom` · `termination-schedule` · `cable-schedule` · `tq-register` · `fat-sheet` · `punch-list` · `mdr-index`

## Interactive portfolio

`portfolio.html` — single-file offline HTML portfolio covering the whole package with the drawings inline, the registers browsable, and the interview pack built in. Opens from `file://`, works on a phone, prints.

---

## How to use this to get a job

1. Read `00-CLAIM-INTEGRITY.md`. Learn the boundary.
2. Work through documents 01–10 **in order**, in your own time, until you can redraw the SLD on a whiteboard from memory and explain why each device is there.
3. Do the exposure questions in `12-INTERVIEW-PACK.md` out loud. If you cannot answer one without reading, you do not own that part yet.
4. Close the gaps in `13-STUDY-GAPS.md`.
5. Then, and only then, put it on your CV as *"Self-directed reference project: full industrial electrical package, design basis through FAT and handover."*

The point of this package is not the documents. It is that you can explain them.
