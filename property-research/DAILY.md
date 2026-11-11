# Daily refresh runbook (7am Perth)

Run from the repository root on branch `claude/affectionate-faraday-jq4eiw`.

1. `cd property-research && rm -rf .cache/mb_* .cache/spi_* .cache/reiwa_*` (force fresh pages; keep .cache/hazards)
2. `python3 collect.py` (rate-limited; ~3 min)
3. `python3 listings.py` (Domain API; writes status "no_key" until a key is saved)
4. News check (Claude does this with web search): RBA decisions, Cotality monthly index,
   Perth/Melbourne price news, the project list in data/projects.json (status changes,
   new funding), and anything in the shortlist suburbs. Update data/news.json (newest first,
   keep ~10 items, each with date, headline, what it does to the forecast, source URL).
   Update data/rates.json if the cash rate changed. Update a project's status only when
   an official source confirms it.
5. Hazards are refreshed monthly: on the 1st, `rm -rf .cache/hazards && python3 hazards.py`
   (needs data/raw/vic_lga_criminal_incidents_*.xlsx; re-download when CSA publishes a new year).
6. `python3 model.py && python3 daily.py && python3 build.py`
7. Republish the artifact https://claude.ai/artifact/94Zdxk9yjb6bBLPGApu3ss from
   `melbourne-perth-600k-shortlist.html` (read it first, keep its capabilities).
8. Read the watchlist (artifact db collection `watch`) and mention those suburbs first.
9. Commit `melbourne-perth-600k-shortlist.html` and `property-research/data/` and push.
10. Send a short phone summary: alerts, biggest changes, watchlist suburbs, one-line market read.
