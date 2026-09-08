#!/usr/bin/env python3
"""
refresh_perth_data.py — fetch what is actually machine-readable for the
Perth Property Bottom Model, and print a paste-ready block for the
dashboard's "Manual data entry" panel (§02).

WHY THIS EXISTS
    perth-property-bottom-model.html is a single sandboxed page. It cannot
    make outbound requests, and the sources it needs do not expose
    CORS-open endpoints anyway. This script does the part that CAN be
    automated, from a machine with normal network access.

HONEST SCOPE — read this before trusting the output
    AUTOMATABLE (this script tries):
        RBA cash rate target ............ RBA F1.1 CSV, a stable public file
        RBA lenders' rates .............. RBA F5 CSV
        WA unemployment ................. ABS Data API (SDMX-JSON), Labour Force
        WA dwelling approvals ........... ABS Data API, Building Approvals
        WA population ................... ABS Data API, quarterly ERP
        CPI ............................. ABS Data API, Consumer Price Index
    NOT AUTOMATABLE (no public API; the script tells you where to look):
        REIWA median prices, listings, days on market, vacancy
        Cotality Home Value Index, vendor discount, rents, yields
        SQM Research vacancy rates
        Suburb-level anything

    The ABS Data API is in beta and its dataflow identifiers change. If a
    lookup fails the script says so and moves on — it never substitutes a
    guess, and it never re-stamps an old value as fresh. That is the same
    rule the dashboard follows.

    NOT VERIFIED AGAINST LIVE ENDPOINTS. The environment this was written in
    had outbound access to abs.gov.au and rba.gov.au blocked by egress
    policy, so the request code below is written from the documented URL
    shapes and has not been executed against the real services. Treat the
    first run as a test run and check the printed values against the source
    pages the script names.

USAGE
    python3 tools/refresh_perth_data.py
    python3 tools/refresh_perth_data.py --json out.json
"""

from __future__ import annotations
import argparse, csv, io, json, sys, datetime as dt
from typing import Any

try:
    import requests
except ImportError:
    sys.exit("This script needs `requests`:  pip install requests")

TIMEOUT = 30
UA = {"User-Agent": "perth-bottom-model/1.0 (personal research)"}

RBA_F11 = "https://www.rba.gov.au/statistics/tables/csv/f1.1-data.csv"
RBA_F5  = "https://www.rba.gov.au/statistics/tables/csv/f5-data.csv"
ABS_API = "https://data.api.abs.gov.au/rest/data"

# Manual sources, printed at the end so you know exactly where to look.
MANUAL = [
    ("medHouseREIWA", "Perth median house sale price",
     "https://reiwa.com.au/the-wa-market/perth-metro/"),
    ("listings", "Perth listings for sale (weekly snapshot)",
     "https://reiwa.com.au/news/  → 'Perth weekly market snapshot'"),
    ("dom", "Median days on market, houses",
     "https://reiwa.com.au/the-wa-market/perth-metro/"),
    ("medDwellCot", "Perth median dwelling value + monthly/quarterly index change",
     "https://www.cotality.com/au/insights  → monthly Home Value Index release"),
    ("drawdown", "Drawdown from cycle peak (derive from the HVI release)",
     "Cotality HVI PDF: 'change from peak' table"),
    ("discount", "Vendor discount",
     "Cotality monthly housing chart pack"),
    ("vacancy", "Perth rental vacancy rate",
     "https://sqmresearch.com.au/graph_vacancy.php?region=wa::Perth"),
    ("rentMed", "Perth median rent", "Cotality quarterly Rental Review"),
    ("yieldGross", "Gross rental yield", "Cotality quarterly Rental Review"),
    ("salesYoY", "Perth sales volumes y/y", "Cotality HVI release, 'estimated sales volumes'"),
    ("sentiment", "Westpac–Melbourne Institute Consumer Sentiment",
     "Westpac IQ monthly bulletin"),
    ("ironOre", "Iron ore forecast average",
     "Dept. of Industry, Resources and Energy Quarterly"),
    ("sfdWA", "WA state final demand", "https://www.watc.wa.gov.au/economic-insights/"),
]


def get(url: str, **kw) -> requests.Response:
    r = requests.get(url, headers=UA, timeout=TIMEOUT, **kw)
    r.raise_for_status()
    return r


def rba_series(url: str, match: str) -> tuple[float, str] | None:
    """RBA CSVs: metadata rows, then a 'Series ID' row, then dated rows.
    Returns (latest value, date) for the first column whose title contains
    `match` (case-insensitive)."""
    rows = list(csv.reader(io.StringIO(get(url).text)))
    header_idx = next((i for i, r in enumerate(rows)
                       if r and r[0].strip().lower().startswith("series id")), None)
    if header_idx is None:
        return None
    title_idx = next((i for i, r in enumerate(rows[:header_idx])
                      if r and r[0].strip().lower().startswith("title")), 0)
    titles = rows[title_idx]
    col = next((j for j, t in enumerate(titles)
                if j and match.lower() in t.lower()), None)
    if col is None:
        return None
    for r in reversed(rows[header_idx + 1:]):
        if len(r) > col and r[col].strip():
            try:
                return float(r[col]), r[0].strip()
            except ValueError:
                continue
    return None


def abs_latest(dataflow: str, key: str, note: str) -> tuple[float, str] | None:
    """ABS Data API (SDMX-JSON). Returns (value, period) for the last
    observation of the first series returned."""
    url = f"{ABS_API}/{dataflow}/{key}"
    r = get(url, params={"format": "jsondata", "lastNObservations": 1})
    d = r.json()
    ds = d["data"]["dataSets"][0]["series"]
    dims = d["data"]["structure"]["dimensions"]["observation"][0]["values"]
    skey, sval = next(iter(ds.items()))
    oidx, obs = next(iter(sval["observations"].items()))
    return float(obs[0]), dims[int(oidx)]["name"] if int(oidx) < len(dims) else note


def attempt(label: str, fn) -> dict[str, Any]:
    try:
        res = fn()
        if res is None:
            return {"status": "FAILED", "why": "series not found in response"}
        v, when = res
        return {"status": "OK", "value": v, "date": when}
    except Exception as e:                                    # noqa: BLE001
        return {"status": "FAILED", "why": f"{type(e).__name__}: {e}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write the result to this path")
    args = ap.parse_args()

    print("=" * 74)
    print("Perth Property Bottom Model — data refresh")
    print("Run at", dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("=" * 74)

    out: dict[str, Any] = {}

    print("\n--- AUTOMATED ---")
    jobs = [
        ("cashRate",   "RBA cash rate target (%)",
         lambda: rba_series(RBA_F11, "Cash Rate Target")),
        ("mortRate",   "Lenders' variable housing rate, owner-occupier (%)",
         lambda: rba_series(RBA_F5, "Housing loans; Owner-occupier; Variable")),
        # ABS dataflow keys below are the documented shapes; verify against
        # https://api.gov.au/ABS-Data-API and the ABS data explorer, and adjust
        # if a lookup fails rather than accepting a wrong series.
        ("unempWA",    "WA unemployment rate, s.a. (%)",
         lambda: abs_latest("ABS,LF,1.0.0", "M3.3.5.TT.M", "Labour Force, WA")),
        ("inflation",  "CPI, annual (%)",
         lambda: abs_latest("ABS,CPI,1.0.0", "1.10001.10.50.Q", "CPI Australia")),
        ("approvalsWA","WA dwelling approvals, monthly change (%)",
         lambda: abs_latest("ABS,BUILDING_APPROVALS,1.0.0", "TOT.5.NSW.M", "Building Approvals WA")),
        ("popWA",      "WA population growth, annual (%)",
         lambda: abs_latest("ABS,ERP_QUARTERLY,1.0.0", "1.5.Q", "ERP WA")),
    ]
    for key, label, fn in jobs:
        res = attempt(label, fn)
        out[key] = res
        if res["status"] == "OK":
            print(f"  🟢 {label:<52} {res['value']:>10}   ({res['date']})")
        else:
            print(f"  🔴 {label:<52} {'FAILED':>10}   {res['why']}")

    ok = sum(1 for v in out.values() if v["status"] == "OK")
    print(f"\n  {ok} of {len(jobs)} automated variables retrieved.")
    if ok < len(jobs):
        print("  Failures are reported, not filled in. Leave the dashboard's existing")
        print("  value in place for anything that failed — it is still correctly dated.")

    print("\n--- MANUAL (no public API exists for these) ---")
    for key, label, where in MANUAL:
        print(f"  ⚪ {key:<16} {label}")
        print(f"     {where}")

    print("\n--- PASTE INTO §02 OF THE DASHBOARD ---")
    for key, res in out.items():
        if res["status"] == "OK":
            print(f"  {key} = {res['value']}      # {res['date']}")
    print("\n  Then press 'Recalculate model'. The whole page recomputes and stamps")
    print("  a new update time. Values you do not change keep their original dates.")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"fetched": dt.datetime.now().astimezone().isoformat(),
                       "automated": out,
                       "manual_required": [m[0] for m in MANUAL]}, f, indent=2)
        print(f"\n  Written to {args.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
