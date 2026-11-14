# Perth southern buyer dashboard: progress log

Branch: `claude/perth-property-intelligence-cf8ob0` (fast-forwarded from
`claude/affectionate-faraday-jq4eiw`, which still owns the Melbourne page and its
06:59 refresh). Page: `perth-southern-buyer-dashboard.html` (repo root),
published at https://claude.ai/artifact/MuXDLmuR1xrzCnQRuG1Yyp (capabilities db + user; watchlist collection `watch`).

## Stages
| Stage | Status | Notes |
|---|---|---|
| 1 Repository discovery | done 14 Nov 2026 | Existing pipeline reused: collect.py scrapers + cache, hazards.wa + SLIP helper, model.spearman, artifact-db watchlist convention |
| 2 Research + source validation | done 14 Nov 2026 | Cotality Nov 2026 HVI checked against PDF; RBA 4.85%; FHOR duty checked on wa.gov.au fact sheet; evidence register in `data/market.json` |
| 2b Suburb universe | done | `universe.py`: LGATE-234 via SLIP, EPSG:7850 centroids, Perth GPO, south of CBD + south/east of Swan River (user choice) + <=35 km -> 141 localities |
| 3 Forecast model | done | `model_perth.py`: AR(1) bootstrap on ABS RPPI Perth 2003-21, path-conditioned bear/base/bull (10-20/45-55/80-90th pct at 24m), expanding-window back-test, REIWA-based suburb beta, tilt gated by rank back-test |
| 4 Finance engine | done | `finance.js` (page + node tests), Python duty parity test |
| 5 Dashboard | done | `template.html` + `build_perth.py` |
| 6 Automation | see below | `run_daily.sh`, `daily_perth.py`; scheduled task at 06:59 Australia/Perth |
| 7 Verification | see commit log | `python3 -m pytest perth/tests -q`, `node --test perth/tests/finance.test.js`; Melbourne page byte-identical rebuild test |
| 8 Git delivery | see commit log | No PR (by instruction) |

## Files (all new unless noted)
perth/universe.py, collect_perth.py, reiwa_full.py, hazards_perth.py, geo.py,
model_perth.py, daily_perth.py, build_perth.py, finance.js, template.html,
run_daily.sh, tests/, data/{universe,suburbs_raw,hazards,geo,market,news,
projects_perth,abs_rppi_perth,model,changes}.json, data/history/.
Modified shared file: property-research/DAILY.md (appended Perth section only).

## Unresolved
- No live listings: Domain API key not saved (listings.py returns 401). Counts of
  "homes for sale" and price reductions are therefore not verified.
- No licensed individual-sale feed: only suburb medians (REIWA 12 months to Oct 2026).
- 3-bed bedroom-subset sample sizes are not published by REIWA/Microburbs.
- Quarterly Perth index 2022-2026 not in the model fit (ABS RPPI discontinued 2021).
- LMI is an indicative table, not an insurer quote. Borrowing power is an approximation.
- 5% Deposit Scheme and FHOG details confirmed by secondary sources only.
- Rent, living costs, ownership costs are labelled placeholders until the buyers enter real figures.

## Next executable step
Run the daily refresh: `cd property-research/perth && ./run_daily.sh`, then follow DAILY.md (Perth section).
Research improvements: Perth monthly Cotality series 2017-2026 to refit; REIWA listings counts per suburb;
Domain API key for listings; ANEF noise contours and DWER contaminated-sites layer for land-use flags.
