#!/usr/bin/env python3
"""Daily step: snapshot today's numbers, diff against the last snapshot,
evaluate alert rules, and write data/changes.json for the page and the
morning summary.

Run after collect.py / hazards.py / listings.py / model.py, before build.py:
    python3 daily.py            # uses today's date (Australia/Perth)
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
HIST = DATA / "history"
HIST.mkdir(parents=True, exist_ok=True)
AWST = timezone(timedelta(hours=8))

# Alert rules. Each returns a list of (level, message) for the current state.
PERTH_BUY_WINDOW = 620_000      # cheapest Perth 3-bed median at/below this
MEL_DROP_PCT = -3.0             # any Melbourne shortlist 3-bed down this much since last snapshot
RATE_FILE = DATA / "rates.json"  # {"cash_rate": 4.85, "as_of": "..."} maintained by the daily session


def snapshot(model):
    snap = {"suburbs": {}, "cash_rate": None}
    for s in model["suburbs"]:
        snap["suburbs"][s["suburb"]] = {
            "city": s["city"], "h3": s["house_3br"], "u3": s["unit_3br"], "hm": s["house_median"],
            "rent": s["rent"], "match": s["match"], "g6": s["g6"],
        }
    if RATE_FILE.exists():
        snap["cash_rate"] = json.loads(RATE_FILE.read_text()).get("cash_rate")
    lst = DATA / "listings.json"
    if lst.exists():
        L = json.loads(lst.read_text())
        snap["listing_ids"] = sorted(str(x["id"]) for x in L.get("listings", []))
    return snap


def main():
    today = datetime.now(AWST).strftime("%Y-%m-%d")
    model = json.loads((DATA / "model.json").read_text())
    snap = snapshot(model)
    prev_files = sorted(p for p in HIST.glob("*.json") if p.stem < today)
    prev = json.loads(prev_files[-1].read_text()) if prev_files else None
    (HIST / f"{today}.json").write_text(json.dumps(snap, separators=(",", ":")))

    changes, alerts = [], []
    if prev:
        for name, cur in snap["suburbs"].items():
            old = prev["suburbs"].get(name)
            if not old:
                continue
            for key, label in (("h3", "3-bed house median"), ("u3", "3-bed townhouse median"), ("rent", "house rent")):
                a, b = old.get(key), cur.get(key)
                if a and b and a != b:
                    pct = (b / a - 1) * 100
                    changes.append({"suburb": name, "city": cur["city"], "what": label, "from": a, "to": b, "pct": round(pct, 1)})
                    if key == "h3" and cur["city"] == "Melbourne" and pct <= MEL_DROP_PCT:
                        alerts.append({"level": "info", "text": f"{name} 3-bed median fell {pct:.1f}% to ${b/1000:.0f}k."})
            if old.get("match") != cur.get("match"):
                changes.append({"suburb": name, "city": cur["city"], "what": "match score", "from": old.get("match"), "to": cur.get("match"), "pct": None})
        if prev.get("cash_rate") and snap.get("cash_rate") and prev["cash_rate"] != snap["cash_rate"]:
            alerts.append({"level": "high", "text": f"RBA cash rate changed {prev['cash_rate']}% → {snap['cash_rate']}%."})
        new_ids = set(snap.get("listing_ids", [])) - set(prev.get("listing_ids", []))
        if new_ids:
            alerts.append({"level": "info", "text": f"{len(new_ids)} new listing(s) match 3-bed, ≤$600k in your shortlist."})

    per = [s for s in model["suburbs"] if s["city"] == "Perth" and s["house_3br"]]
    cheapest = min(per, key=lambda s: s["house_3br"])
    if cheapest["house_3br"] <= PERTH_BUY_WINDOW:
        alerts.append({"level": "high", "text": f"Perth buy window: {cheapest['suburb']} 3-bed median is ${cheapest['house_3br']/1000:.0f}k (≤ ${PERTH_BUY_WINDOW/1000:.0f}k trigger)."})

    out = {"date": today, "previous": prev_files[-1].stem if prev_files else None,
           "changes": sorted(changes, key=lambda c: abs(c["pct"] or 0), reverse=True)[:40],
           "alerts": alerts,
           "rules": [f"Cheapest Perth 3-bed median at or below ${PERTH_BUY_WINDOW/1000:.0f}k",
                     f"A Melbourne shortlist 3-bed median falls {abs(MEL_DROP_PCT):.0f}%+",
                     "RBA cash rate changes", "New matching listings appear (needs Domain key)"],
           "cheapest_perth_3br": {"suburb": cheapest["suburb"], "price": cheapest["house_3br"]}}
    (DATA / "changes.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({"date": today, "previous": out["previous"], "n_changes": len(changes), "alerts": alerts}, indent=1))


if __name__ == "__main__":
    main()
