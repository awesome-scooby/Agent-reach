# Job Sprint

Hub page: https://claude.ai/artifact/EB55yL6BcEynjBwqxd9qfE (private)

## What runs where

| Piece | What it does |
|---|---|
| `scan.py` | Pulls employer job feeds (Greenhouse and Workday public JSON) using Scrapling's Fetcher, keeps Melbourne and Perth roles, scores 0-100 |
| `feeds.json` | Which employers are scanned. `python3 scan.py --probe` tests they still answer |
| `profile.json` | Scoring rules: role tiers, sector words, $135k package floor, contract and FIFO flags |
| Hub page db | `jobs/*` written by the nightly scan or the page's "Add a job" form. `tracker/*` written by the page (status, applied date, follow-up, notes, draft). `meta/scan` holds the last run |
| Scheduled task | Every evening at 6:47pm Melbourne time, a fresh cloud session runs the scan and adds new jobs to the db |

## Score (out of 100)

- Role fit, from the title: core target 40, strong adjacent 30, stretch 15. Titles outside the list are dropped
- Sector words (data centre, critical, HV, substation, BESS, switchgear and similar): up to 20
- City: Melbourne 15, Perth 12. Anywhere else is dropped
- Seniority: senior or lead 10, mid 6, director-level 2. Graduate, technician and trade roles are dropped
- Pay: 15 if the advertised ceiling clears $135k package, 7 if no pay is stated, 0 plus a "pay cut risk" flag if it's below
- Contract or fixed-term: minus 5 and flagged. Different discipline (HVAC, mechanical, fire): minus 25

Grades: A is 80 or more, B is 65, C is 50.

## Known gaps

- SEEK, Jora and LinkedIn block automated requests (403). SEEK jobs go in through the page's paste form.
- Gmail job-alert parsing would cover SEEK and LinkedIn properly, but the Gmail connector currently fails to authenticate.
- Contractors without a public feed (Fredon, Stowe, Nilsen, SKS, NHP) are not scanned.

## Nightly run (what the scheduled task does)

1. `git fetch origin claude/eloquent-ptolemy-3nepag && git checkout FETCH_HEAD -- job-sprint`
2. List every `jobs` doc id from the hub db into `job-sprint/known.json`
3. `python3 job-sprint/scan.py --known job-sprint/known.json`
4. Write each chunk in `job-sprint/out/writes.json` with an ArtifactData batch, then update `meta/scan` from `out/meta.json`
