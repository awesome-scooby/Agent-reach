#!/usr/bin/env python3
"""Collect suburb market data for every locality in perth/data/universe.json
(included == True), reusing the scrapers, cache and rate limit in ../collect.py.

Writes perth/data/suburbs_raw.json atomically. If fewer than MIN_OK suburbs
return a usable price series the previous file is kept (last-known-good)
and the run exits non-zero so a partial pull never looks current.
"""
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import collect  # noqa: E402
sys.path.insert(0, str(HERE))
import reiwa_full  # noqa: E402

UNIVERSE = HERE / "data" / "universe.json"
OUT = HERE / "data" / "suburbs_raw.json"
MIN_OK_SHARE = 0.6


def main():
    uni = [r for r in json.loads(UNIVERSE.read_text())["rows"] if r["included"]]
    rows, ok = [], 0
    for i, u in enumerate(uni, 1):
        nm, pc = u["suburb"], u["postcode"]
        print(f"[{i}/{len(uni)}] {nm}", file=sys.stderr)
        rec = {"suburb": nm, "postcode": pc, "errors": []}
        for key, fn in (("microburbs", lambda: collect.microburbs(nm, pc, "WA")),
                        ("spi", lambda: collect.spi(nm, pc, "WA")),
                        ("reiwa", lambda: collect.reiwa(nm))):
            try:
                rec[key] = fn()
            except Exception as e:  # noqa: BLE001
                rec[key] = {}
                rec["errors"].append(f"{key}: {e}")
        rec["reiwa_full"] = reiwa_full.parse(nm)
        if rec["microburbs"].get("salePoints") or rec["reiwa_full"]:
            ok += 1
        rows.append(rec)
    share = ok / max(1, len(uni))
    if share < MIN_OK_SHARE and OUT.exists():
        print(f"only {ok}/{len(uni)} usable; keeping last-known-good", file=sys.stderr)
        sys.exit(2)
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps({"collected": time.strftime("%Y-%m-%d"), "n_ok": ok, "n": len(uni), "suburbs": rows}))
    os.replace(tmp, OUT)
    print(f"wrote {OUT.name}: {ok}/{len(uni)} with price series", file=sys.stderr)





def backfill():
    """Add parsed REIWA fields from the cache to an existing suburbs_raw.json."""
    d = json.loads(OUT.read_text())
    for r in d["suburbs"]:
        r["reiwa_full"] = r.get("reiwa_full") or reiwa_full.parse(r["suburb"])
    OUT.write_text(json.dumps(d))


if __name__ == "__main__":
    backfill() if "--backfill" in sys.argv else main()
