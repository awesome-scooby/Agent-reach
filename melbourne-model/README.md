# Melbourne Bottom Clock

A transparent, multi-factor probability model for timing the bottom of Melbourne's
house-price cycle, built for a **$600k–$650k house purchase within ~35 km of the CBD**.

## Files

| File | What it is |
|---|---|
| `melbourne-bottom-model.html` | The dashboard. Self-contained — no build step, no dependencies. |
| `update_market_data.py` | Server-side refresh script. Writes `market-data.json`, which the dashboard loads. |

Open the HTML directly in a browser, or use the published Artifact link.

## The model in one paragraph

Ten weighted factors each score 0–100, where 0 means "deep in a downturn, far from the
bottom" and 100 means "conditions that have historically marked a Melbourne bottom".
The weighted total places the market in one of five bands. As at **7 September 2026**
the score is **22/100 — before the bottom**, and the call is **WAIT**.

Weights differ from a naive setup on purpose: **interest rates 25%, price trend 20%**
(not the reverse). Price trend is a *coincident* indicator — it confirms a bottom only
after the fact — so weighting it heavily makes the model systematically late. The rate
cycle is the only factor that has consistently *led* Melbourne troughs.

Every score is derived from a published formula, listed in the update dialog. Change
the weights with the sliders and the whole dashboard recomputes.

## Refreshing the data

A standalone HTML page **cannot** fetch most Australian property data. Browsers block
cross-origin reads from hosts that send no CORS headers, and CoreLogic/Cotality, REIV,
Domain and SQM publish no free public API at all. The dashboard is honest about this:
the update button genuinely attempts each source, reports per-source success or failure
verbatim, and **never substitutes an invented number for a failed fetch**.

The working path is the script:

```bash
python3 update_market_data.py                       # fetch open sources
python3 update_market_data.py --set clearance=57 \
                              --set listingsYoY=39.4 # set what can't be fetched
python3 update_market_data.py --dry-run             # preview, write nothing
```

Then in the dashboard: **Update with latest market data → Load a JSON file…**

Reachable without a licence: RBA cash rate (F1.1 CSV), ABS Data API (CPI, Labour Force).
Not reachable: Cotality HVI, REIV medians, Domain/SQM listings, clearance, days on
market, vendor discounting — these are `--set` fields, tagged `assumption` until you
set them.

## Data quality

Every figure carries a provenance tag: **live / recent / historical / assumption /
conflict**. Where sources disagree, both figures are shown rather than the one that
suits the conclusion — see the conflicts table in Panel 9.

Two limits worth stating plainly:

- **No primary-source downloads.** The environment that built this had rba.gov.au,
  abs.gov.au, domain.com.au and tradingeconomics.com blocked by network policy. Figures
  come from search-result citations of those sources, not the source files. Verify
  before acting.
- **The 30-year price line is eight sourced points plus an interpolated curve**, shaped
  to documented peak-to-trough percentages. The dashboard has a toggle that strips it
  back to only the sourced anchors.

## Back-test

Tested against eight Melbourne episodes, 1992–2024, with no period excluded:
5 correct, 2 false signals, 1 late. Both failure modes are documented in Panel 6.
The weights were chosen knowing the outcomes, so real predictive accuracy will be
lower than 5/8.

Not financial advice.
