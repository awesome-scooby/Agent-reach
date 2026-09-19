# 2 MW Data Centre Critical Power Design

> **SELF-DIRECTED ENGINEERING PROJECT — NOT A COMMISSIONED CLIENT DESIGN**
>
> This is a notional facility developed for personal technical development and
> portfolio purposes. There is no client, no site, no contract and no
> professional engineering sign-off. No part of this package may be
> represented as commissioned professional work, and no part of it is
> suitable for construction.

## Purpose

Develop a complete conceptual-to-detailed critical power design for a notional
2 MW IT load data centre with a genuine 2N critical power architecture, plus the
failure-mode analysis, concurrent-maintainability assessment and L1–L5
commissioning matrix that would accompany it on a real project.

The objective is not the drawing set. The objective is being able to **defend the
architecture under challenge** — explaining what happens on every failure, and
proving that every asset can be maintained without dropping IT load.

## Approved CV wording

> "Developed a 2N critical power distribution design and commissioning matrix for
> a notional 2 MW data centre IT load as a self-directed engineering project."

## Confirmed project basis (locked 2026-09-19)

| Item | Value | Type |
|---|---|---|
| IT load | 2,000 kW at rack PDU output | Given requirement |
| Critical power architecture | 2N | Given requirement |
| Cooling architecture | Air-cooled chillers, chilled water, CRAH | Design decision |
| Utility intake | 2 × 11 kV feeders, separate zone substations | Engineering assumption |
| LV distribution | 415/240 V, 50 Hz, MEN | Engineering assumption |
| Standards basis | AS/NZS primary, IEC/ISO/EN/Uptime secondary | Design decision |

## Document register

| Doc | Title | Status |
|---|---|---|
| `docs/01-week1-fundamentals.md` | Critical power fundamentals (Week 1 teaching) | Issued |
| `docs/02-basis-of-design.md` | Basis of Design, Rev 0.1 | Issued for review |
| `docs/03-architecture-block-diagram.md` | Architecture block diagram + AutoCAD brief | Issued |
| `docs/04-glossary.md` | Data centre electrical glossary | Live |
| `docs/05-interview-knowledge-bank.md` | Interview knowledge bank | Live |
| `docs/06-week1-assignment.md` | Week 1 engineering assignment | Issued to engineer |
| `registers/assumptions-register.csv` | Assumptions Register | Live |
| `registers/design-decision-register.csv` | Design Decision Register | Live |
| `registers/tq-register.csv` | Open Issues / TQ Register | Live |

## Programme

| Week | Scope | Status |
|---|---|---|
| 1 | Fundamentals, requirements, Basis of Design | **Complete** |
| 2 | Load development and electrical architecture | Not started |
| 3 | Utility, transformers, MV/LV distribution, generators | Not started |
| 4 | UPS, batteries, bypass, A/B critical paths | Not started |
| 5 | PDU, RPP, STS, rack-level distribution | Not started |
| 6 | Protection, selectivity, metering, controls, BMS/EPMS | Not started |
| 7 | Failure-mode analysis, concurrent maintainability | Not started |
| 8 | Commissioning L1–L5, Integrated Systems Testing | Not started |
| 9 | Drawing and calculation refinement | Not started |
| 10 | Design review, portfolio, HTML front-end, interview prep | Not started |

## Design reviews

- **30% review** — end Week 2. Architecture and design basis.
- **60% review** — end Week 5. Equipment sizing, distribution, redundancy.
- **90% review** — end Week 8. Protection, controls, maintainability, commissioning.
- **100% review** — end Week 10. Complete portfolio.

## Standing rule

Nothing in this package is called "redundant", "2N" or "concurrently
maintainable" unless a written switching sequence or failure scenario in the
failure-mode analysis proves it. Two of something is not redundancy.
