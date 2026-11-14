#!/usr/bin/env python3
"""Perth daily step: snapshot, diff against the previous snapshot, heuristic
turning-point signals and material alerts -> perth/data/changes.json.
Idempotent per day (re-running overwrites today's snapshot). Uses an
exclusive lock so two runs can't interleave writes."""
import fcntl
import json
import os
from datetime import datetime
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
D = HERE / "data"
HIST = D / "history"
TZ = ZoneInfo("Australia/Perth")


def signals(model, market, prev):
    ind = {i["id"]: i for i in market["indicators"]}
    out = []
    m = [v for _, v in market.get("perth_monthly", {}).get("series", [])]
    if len(m) >= 3:
        a, b, c = m[-3:]
        if c < b < a:
            st, dr = "falls accelerating", "bearish"
        elif all(x > -0.5 for x in m[-2:]):
            st, dr = "stabilising", "bullish"
        elif abs(c) < abs(b):
            st, dr = "falls easing (one month)", "inconclusive"
        else:
            st, dr = "falls steady", "bearish"
        out.append({"name": "Three-month price momentum", "state": st, "dir": dr,
                    "what": f"Monthly changes {', '.join(f'{x:+.1f}%' for x in m[-3:])} (Cotality).",
                    "why": "Accelerating falls usually mean more to come; two months under -0.5% is the first sign of a floor.",
                    "against": "One month is noise; Cotality revises recent months (Sep went from -1.2% to -2.1%).",
                    "material": "Yes if it flips to stabilising: the waiting case weakens." if dr != "bullish" else "Yes: waiting for further falls looks less rewarding."})
    cr = ind.get("cash", {}).get("value")
    pcr = (prev or {}).get("cash_rate")
    out.append({"name": "RBA cash rate", "state": f"{cr}%" + (f" (was {pcr}%)" if pcr and pcr != cr else ", unchanged"),
                "dir": "bearish" if pcr and cr > pcr else ("bullish" if pcr and cr < pcr else "inconclusive"),
                "what": "Cash rate 4.85% after the 3 Nov hike; next decision 8 Dec 2026.",
                "why": "Serviceability caps what buyers can pay; each 0.25pt cuts borrowing power ~2.5%.",
                "against": "Statement dropped the tightening bias; three members voted to hold.",
                "material": "Yes: changes repayments in Row 8 and the bear/base weighting."})
    doms = [s["dom"] for s in model["suburbs"] if s.get("dom")]
    sales = sum(s.get("count") or 0 for s in model["suburbs"])
    pd, ps = (prev or {}).get("dom_median"), (prev or {}).get("sales_total")
    dm = median(doms) if doms else None
    out.append({"name": "Selling time (southern suburbs, REIWA median DOM)", "state": f"{dm} days" + (f" (was {pd})" if pd else ""),
                "dir": "bearish" if pd and dm and dm > pd + 2 else ("bullish" if pd and dm and dm < pd - 2 else "inconclusive"),
                "what": "Median of suburb median days on market for settled sales.",
                "why": "Longer selling times give buyers leverage and often precede discounting.",
                "against": "Settled-sale DOM lags the market by 1-3 months.",
                "material": "Supports negotiating hard if rising."})
    out.append({"name": "Sales volume (12-month house sales, universe)", "state": f"{sales:,}" + (f" (was {ps:,})" if ps else ""),
                "dir": "bearish" if ps and sales < ps * 0.97 else ("bullish" if ps and sales > ps * 1.03 else "inconclusive"),
                "what": "Sum of REIWA 12-month house sales counts across included suburbs.", "why": "Falling turnover = weak demand; a rebound in volumes is an early recovery signal.",
                "against": "12-month windows move slowly; settlements lag contracts.", "material": "Watch for a turn upward before prices."})
    disc = ind.get("disc_cap", {}).get("value")
    out.append({"name": "Vendor discounting (capitals)", "state": f"{disc}%", "dir": "bearish" if disc and disc >= 4 else "inconclusive",
                "what": "Largest since May 2019 (Cotality).", "why": "Bigger discounts = sellers adjusting to buyers.",
                "against": "Capital-city figure, not Perth-only.", "material": "Sets a realistic negotiation target (Row 3)."})
    u = ind.get("wa_unemp", {}).get("value")
    out.append({"name": "WA unemployment", "state": f"{u}%", "dir": "bullish" if u and u < 4.5 else "bearish",
                "what": "4.2% in September (ABS). October due 19 Nov.", "why": "Job losses turn a correction into forced selling.",
                "against": "Monthly state data is noisy.", "material": "A rise above 5% would favour the bear path."})
    return out


def main():
    HIST.mkdir(parents=True, exist_ok=True)
    lock = open(D / ".daily.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    model = json.loads((D / "model.json").read_text())
    market = json.loads((D / "market.json").read_text())
    news = json.loads((D / "news.json").read_text()) if (D / "news.json").exists() else {"items": []}
    snap = {"cash_rate": next((i["value"] for i in market["indicators"] if i["id"] == "cash"), None),
            "model_version": model["model_version"], "data_date": model["generated"],
            "dom_median": median([s["dom"] for s in model["suburbs"] if s.get("dom")] or [0]),
            "sales_total": sum(s.get("count") or 0 for s in model["suburbs"]),
            "suburbs": {s["suburb"]: {"h3": s["h3"], "h3_now": s["h3_now"], "u3": s["u3"], "group": s["group_house"], "count": s["count"]} for s in model["suburbs"]}}
    prevs = sorted(p for p in HIST.glob("*.json") if p.stem < today)
    prev = json.loads(prevs[-1].read_text()) if prevs else None
    tmp = HIST / f"{today}.tmp"
    tmp.write_text(json.dumps(snap, separators=(",", ":")))
    os.replace(tmp, HIST / f"{today}.json")
    changes, alerts = [], []
    if prev:
        for nm, cur in snap["suburbs"].items():
            old = prev["suburbs"].get(nm)
            if not old:
                continue
            for key, label in (("h3", "3-bed house median"), ("u3", "3-bed townhouse median")):
                a, b = old.get(key), cur.get(key)
                if a and b and a != b:
                    pct = round(100 * (b / a - 1), 1)
                    changes.append({"suburb": nm, "what": label, "from": a, "to": b, "pct": pct})
            if old.get("group") != cur.get("group") and cur.get("group", "").startswith(("1", "2")):
                alerts.append({"level": "high", "text": f"{nm} moved into '{cur['group']}' (3-bed now ≈ ${cur['h3_now']/1000:.0f}k).",
                               "why": "A new suburb within reach of the $600k budget."})
        if prev.get("cash_rate") and snap["cash_rate"] != prev["cash_rate"]:
            alerts.append({"level": "high", "text": f"RBA cash rate {prev['cash_rate']}% → {snap['cash_rate']}%.", "why": "Changes repayments and borrowing power."})
        big = [c for c in changes if abs(c["pct"]) >= 3]
        if len(big) >= 5:
            alerts.append({"level": "info", "text": f"{len(big)} suburbs' 3-bed medians moved 3% or more since {prevs[-1].stem}."})
    out = {"date": today, "previous": prevs[-1].stem if prevs else None, "alerts": alerts,
           "changes": sorted(changes, key=lambda c: -abs(c["pct"]))[:40],
           "signals": signals(model, market, prev), "news": news.get("items", [])[:12]}
    tmp = D / "changes.tmp"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, D / "changes.json")
    print(json.dumps({"date": today, "previous": out["previous"], "alerts": alerts, "n_changes": len(changes)}))


if __name__ == "__main__":
    main()
