# Perth Property Bottom Model

An evidence-based Perth property-cycle and price-bottom model for a
$600,000–$650,000 owner-occupier purchase within commuting distance of the CBD.

- `perth-property-bottom-model.html` — the dashboard. Single file, no build step,
  works offline. Open it in a browser.
- `tools/refresh_perth_data.py` — fetches the inputs that are genuinely
  machine-readable and prints a paste-ready block for the dashboard's manual
  entry panel.

Built 8 September 2026.

## The headline result

| | |
|---|---|
| Bottom probability | **34%** — early downturn, not near a trough |
| Market position | Four months and −3.2% past a May 2026 index peak |
| False-bottom risk | **HIGH** — 8 of 8 testable conditions triggered |
| Buying Opportunity Score | **31 / 100** — 🔴 Wait |
| Most likely trough | Q4 2027, 15% · 53% chance it falls in Q1 2027 – Q2 2028 |
| Distribution shape | **Bimodal** — a rates-driven 2027 trough, or a WA income-shock trough around 2030 |
| Data confidence | 69/100 — Moderate |

**The finding that matters most for a $600–650k budget:** a Perth metro median
house is $960,000. Reaching $650,000 needs a 32% fall; Perth's worst downturn in
thirty years was 21.6%. No plausible correction brings the median into range —
but the budget already buys a house today in Armadale ($610k), Brookdale ($622k),
Cannington ($635k), Midland ($636k) and the Kwinana corridor. The question is
timing, not access. And those are exactly the suburbs that ran +25% to +31% in
the year to June 2026, against +15.6% for the metro.

## Method

1. **30-year price history** from 17 sourced anchor points. Everything between
   anchors is drawn as dashed interpolation and labelled as not-data. No
   continuous series was available; none was fabricated.
2. **Cycle anatomy** for every identifiable Perth peak-to-trough episode — with
   the n≈3 warning attached to every summary statistic.
3. **Seven indicator families** (price, supply, demand, market stress, economy,
   finance, rental), each indicator mapped to a 0–100 bottom-likeness score with
   the mapping and its justification shown.
4. **Three weightings** — equal, economically weighted, historically optimised —
   combined into an ensemble. The historically-optimised weighting is capped at
   20% because it was fitted to one event.
5. **Back-test** over eight episodes and three testable troughs, with precision,
   recall and accuracy reported *and* the small-sample caveat attached to each.
6. **Seven forecasting approaches**, reliability-weighted; the machine-learning
   model is excluded for insufficient data and its weight redistributed.
7. **Trough timing** as an explicit two-regime convolution over quarters, not an
   asserted date.
8. **Buy-vs-wait break-even**, including the WA first-home-buyer transfer-duty
   cliff at $600,000.

## Data quality rules this build follows

- Every figure carries a source, a data date (not an access date), a freshness
  grade and a source tier.
- Four source conflicts are documented with cause and resolution rather than
  silently resolved. One figure (a $1.09m Q4-2025 Perth median) is documented as
  a rejected outlier.
- Ten missing or unavailable inputs are named, each with the weight
  redistribution it caused. Nothing missing is set to a default.
- Suburb-level substitutions (SA3/LGA data standing in for suburb data) are
  labelled ⚠ LGA everywhere they appear.
- The final quality gate reports **2 of 13 checks failing** — the history series
  has a documented methodology break, and the live-update button cannot be live
  inside a sandboxed page. Both are disclosed on the page.

## Known limitations

- **No primary release was fetched directly.** Network egress policy blocked
  reiwa.com.au, abs.gov.au, rba.gov.au and sqmresearch.com.au during the build.
  Every Tier-1 figure reaches the model through secondary reporting of a primary
  release. A flat 15% haircut is applied to the source-quality component of the
  confidence score. **Verify any figure at its source before acting on it.**
- **The back-test is n=3.** 100% precision on three events means very little.
- **Suburb data is the weakest layer.** Mixed reference periods, Tier-4
  aggregators, seven of fifteen requested attributes unobtainable, and one
  unresolved conflict on Armadale's own median. Use it to build a shortlist to
  inspect, never to decide what something is worth.
- `tools/refresh_perth_data.py` has **not been run against live endpoints** —
  the same egress policy blocked them. Treat the first run as a test.
- This is a probability model, not a prediction, and not financial advice.

## Updating it

The dashboard's 🔄 button probes each source, reports honestly that none is
reachable from a browser, and opens the manual entry panel. Every model input is
editable there; changes are stored in your browser only, marked `USER` in the
audit table, and drive every number on the page. Run
`python3 tools/refresh_perth_data.py` first to pull what can be automated.
