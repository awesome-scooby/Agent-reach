#!/usr/bin/env python3
"""
update_market_data.py — refresh the inputs behind the Melbourne Bottom Clock.

WHY THIS EXISTS
    A standalone HTML page cannot fetch most Australian market data: browsers
    block cross-origin reads from hosts that do not send CORS headers, and
    almost no Australian statistical or property site sends them. A script run
    outside the browser has no such restriction, so this is the only honest way
    to automate the refresh.

WHAT IT CAN AND CANNOT REACH
    CAN (open data, no licence):
        - RBA cash rate (F1.1 CSV)
        - ABS Data API (CPI, Labour Force, Building Approvals, Population)
    CANNOT (commercial licences — no free public API exists):
        - CoreLogic / Cotality Home Value Index
        - REIV medians
        - Domain / SQM Research listings, clearance, days on market,
          vendor discounting
    Those five are left as MANUAL fields. The script never invents them and
    never silently carries a stale value forward as if it were fresh — it
    marks each one with the date you last set it.

USAGE
    python3 update_market_data.py                  # fetch, then write market-data.json
    python3 update_market_data.py --set clearance=57 --set listingsYoY=39.4
    python3 update_market_data.py --dry-run        # show what would change

    Then open the dashboard, press "Update with latest market data",
    choose "Load a JSON file", and pick market-data.json.

EXIT CODES
    0 wrote a file   1 nothing written   2 all fetches failed
"""

from __future__ import annotations
import argparse, csv, io, json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "market-data.json")
UA = {"User-Agent": "melbourne-bottom-clock/1.0 (+local analysis script)"}
TIMEOUT = 25

RBA_F11 = "https://www.rba.gov.au/statistics/tables/csv/f1.1-data.csv"
ABS_LFS = ("https://data.api.abs.gov.au/rest/data/ABS,LF,1.0.0/"
           "M1.3.1599.20.M?lastNObservations=1&format=jsondata")
ABS_CPI = ("https://data.api.abs.gov.au/rest/data/ABS,CPI,1.0.0/"
           "1.10001.10.50.Q?lastNObservations=2&format=jsondata")

# Fields the script cannot reach. Edit these here, or with --set on the CLI.
MANUAL = {
    "price3mo":        (-3.9,  "Cotality (CoreLogic) Home Value Index, Melbourne, 3-month % change"),
    "priceYoY":        (-4.7,  "Cotality HVI, Melbourne, 12-month % change"),
    "listingsYoY":     (42.8,  "SQM Research, Melbourne total listings, y/y %"),
    "clearance":       (59.0,  "Domain or REIV, Melbourne weekly auction clearance %"),
    "mortgageRate":    (6.22,  "Average owner-occupier variable rate, lender comparison tables"),
    "vendorDiscount":  (-3.8,  "Domain/SQM median vendor discount %"),
    "daysOnMarket":    (39.0,  "Domain/SQM median days on market"),
    "popGrowth":       (1.8,   "ABS state population, Victoria, annual growth %"),
    "buildScore":      (55.0,  "Set directly — no single clean construction series"),
    "monthsToFirstCut":(8.0,   "Months to the first expected RBA cut, per major-bank forecasts"),
    "hikeRisk":        (1.0,   "1 if a further hike is still a live risk, else 0"),
    "cutsDelivered":   (0.0,   "Cuts delivered so far in this easing cycle"),
}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def fetch_cash_rate():
    """Latest RBA cash rate target from the F1.1 CSV."""
    raw = get(RBA_F11).decode("utf-8", "replace")
    rows = list(csv.reader(io.StringIO(raw)))
    col = None
    for row in rows[:15]:
        for i, cell in enumerate(row):
            if "FIRMMCRTD" in cell.upper():
                col = i
                break
        if col is not None:
            break
    if col is None:
        raise ValueError("could not locate the FIRMMCRTD series column in F1.1")
    for row in reversed(rows):
        if len(row) > col:
            try:
                return float(row[col]), row[0]
            except (ValueError, IndexError):
                continue
    raise ValueError("no numeric observation found in F1.1")


def fetch_abs(url: str, label: str):
    """Latest observation from an ABS Data API jsondata response."""
    doc = json.loads(get(url).decode("utf-8", "replace"))
    series = doc["data"]["dataSets"][0]["series"]
    key = next(iter(series))
    obs = series[key]["observations"]
    last = max(obs.keys(), key=lambda k: int(k))
    val = obs[last][0]
    if val is None:
        raise ValueError(f"{label}: latest observation was null")
    return float(val)


def main() -> int:
    ap = argparse.ArgumentParser(description="Refresh Melbourne Bottom Clock inputs.")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="override a manual field, e.g. --set clearance=57")
    ap.add_argument("--dry-run", action="store_true", help="print the result, write nothing")
    ap.add_argument("--out", default=OUT, help="output path (default: market-data.json beside this script)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    inputs = {k: v for k, (v, _) in MANUAL.items()}
    prov = {k: {"value": v, "tag": "assumption", "source": src, "asAt": "manually set"}
            for k, (v, src) in MANUAL.items()}

    for item in args.set:
        if "=" not in item:
            print(f"  ! ignoring --set {item!r}: expected KEY=VALUE", file=sys.stderr)
            continue
        k, v = item.split("=", 1)
        k = k.strip()
        if k not in inputs:
            print(f"  ! ignoring --set {k}: not a known field", file=sys.stderr)
            continue
        try:
            inputs[k] = float(v)
        except ValueError:
            print(f"  ! ignoring --set {k}={v!r}: not a number", file=sys.stderr)
            continue
        prov[k].update(value=inputs[k], tag="recent", asAt=now)
        print(f"  · set {k} = {inputs[k]}")

    ok = failed = 0
    print("Fetching open sources…")

    try:
        rate, asat = fetch_cash_rate()
        prov["cashRate"] = {"value": rate, "tag": "live", "source": "RBA F1.1", "asAt": asat}
        inputs["cashRate"] = rate
        print(f"  ok  RBA cash rate: {rate}% (as at {asat})")
        ok += 1
    except Exception as e:
        print(f"  FAIL RBA cash rate: {e.__class__.__name__}: {e}")
        failed += 1

    for label, url, field in (("ABS unemployment", ABS_LFS, "unemployment"),
                              ("ABS CPI", ABS_CPI, "cpi")):
        try:
            val = fetch_abs(url, label)
            inputs[field] = val
            prov[field] = {"value": val, "tag": "live", "source": label, "asAt": now}
            print(f"  ok  {label}: {val}")
            ok += 1
        except Exception as e:
            print(f"  FAIL {label}: {e.__class__.__name__}: {e}")
            failed += 1

    if "unemployment" not in inputs:
        inputs["unemployment"] = 4.5
        prov["unemployment"] = {"value": 4.5, "tag": "assumption",
                                "source": "ABS Labour Force (last known)", "asAt": "Jul 2026"}

    payload = {
        "generatedAt": now,
        "generator": "update_market_data.py",
        "fetchedOk": ok,
        "fetchFailed": failed,
        "note": ("Fields tagged 'assumption' were not fetched — no free public API exists for "
                 "CoreLogic/Cotality, REIV, Domain or SQM. Set them with --set after reading "
                 "the published figure. Nothing here is estimated or interpolated."),
        "provenance": prov,
        **{k: v for k, v in inputs.items()},
    }

    text = json.dumps(payload, indent=2)
    if args.dry_run:
        print("\n--- dry run, nothing written ---\n")
        print(text)
        return 1

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(f"\nWrote {args.out}  ({ok} fetched, {failed} failed)")
    print("Load it in the dashboard: Update with latest market data → Load a JSON file…")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
