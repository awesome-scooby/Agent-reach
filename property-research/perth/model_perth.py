#!/usr/bin/env python3
"""Perth-only scenario model and decision data.

City scenarios (conditional, not forecasts)
  Quarterly Perth price changes are modelled as an AR(1) process around a
  long-run drift, fitted to ABS RPPI Perth 2003Q3-2021Q4. From today's
  observed quarter (Cotality, -5.7% Aug-Oct 2026) we bootstrap 4,000 paths
  with historical residuals (fixed seed => reproducible). Paths are ranked
  by their 24-month outcome; each scenario is the AVERAGE of the paths in a
  band: bear = 10th-20th percentile, base = 45th-55th, bull = 80th-90th.
  That gives coherent paths that trough and recover (pointwise percentiles
  keep widening for 10 years and imply absurd long-run troughs). Band edges
  were chosen so the 2-year back-test coverage is near 80%; that choice uses
  the same history as the back-test, so coverage is partly in-sample.
  These percentiles describe the model's spread, NOT calibrated real-world
  probabilities; the back-test reports how often reality fell inside.
  Back-test: expanding window, origin t uses only data before t.

Suburb paths
  suburb log-change = beta * city log-change up to Oct 2028 (the current
                      cycle), then the city's later changes unscaled, + tilt
  beta  = cycle amplitude vs. the Perth suburb median, estimated from REIWA
          annual medians 2017-2026 (needs >=20 house sales every year),
          shrunk halfway to 1 and clamped to [0.7, 1.5]. Otherwise 1.
  tilt  = small recovery-phase adjustment (yield, rent growth, run-up, rail),
          used ONLY if its rank back-test beat simple momentum in both
          windows; clamped to +/-0.75% p.a.
  Start = REIWA 3-bed house median (12 months to Oct 2026, settled sales)
          x lag factor 0.959 (Perth path reconstruction in market.json).
  Thin trading (<40 sales) widens bands; <15 sales or no 3-bed median
  suppresses the suburb path entirely.
"""
import json
import math
import os
import random
import sys
from datetime import date
from pathlib import Path
from statistics import mean, median, pstdev

HERE = Path(__file__).resolve().parent
D = HERE / "data"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import reiwa_full  # noqa: E402
from model import spearman  # noqa: E402  (reuse the existing rank-correlation helper)

MODEL_VERSION = "perth-1.0.0"
SEED = 20261114
NPATH = 4000
BUDGET_A = 600_000
START_DATE = "2026-10-31"
Q_LABELS = ["2027-01", "2027-04", "2027-07", "2027-10", "2028-01", "2028-04", "2028-07", "2028-10"]
A_LABELS = [f"{y}-10" for y in range(2029, 2037)]
POINTS = Q_LABELS + A_LABELS                      # 8 quarterly + 8 annual = to Oct 2036
POINT_Q = list(range(1, 9)) + [12 + 4 * i for i in range(8)]   # quarters ahead
HORIZONS = {"6m": 2, "12m": 4, "24m": 8, "3y": 12, "5y": 20, "10y": 40}


def load(name, default=None):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else default


# ------------------------------------------------------------- city model
def fit_ar1(x):
    d = mean(x)
    a = [v - d for v in x[:-1]]
    b = [v - d for v in x[1:]]
    var = sum(v * v for v in a) or 1e-9
    phi = max(-0.2, min(0.95, sum(p * q for p, q in zip(a, b)) / var))
    res = [q - phi * p for p, q in zip(a, b)]
    return {"drift": d, "phi": phi, "res": res, "n": len(x)}


def simulate(fit, q0, nq, npath, seed):
    rng = random.Random(seed)
    d, phi, res = fit["drift"], fit["phi"], fit["res"]
    paths = []
    for _ in range(npath):
        x, cum, row = q0, 0.0, []
        for _k in range(nq):
            x = d + phi * (x - d) + rng.choice(res)
            cum += x
            row.append(cum)
        paths.append(row)
    return paths


BAND = (0.15, 0.5, 0.85)  # chosen so back-test coverage >= 80% (see backtest; in-sample choice, disclosed)


def quantiles(paths, k, qs=BAND):
    col = sorted(p[k - 1] for p in paths)
    n = len(col)
    return [col[min(n - 1, int(q * n))] for q in qs]


RANK_AT = 8  # paths are ranked by their 24-month outcome
BANDS = {"bear": (0.10, 0.20), "base": (0.45, 0.55), "bull": (0.80, 0.90)}


def conditioned(paths, nq_rank=RANK_AT):
    """Coherent scenario paths: average of the simulated paths whose outcome at
    the ranking horizon falls in each band (bear 10-20th pct, base 45-55th,
    bull 80-90th). Unlike pointwise percentiles these paths trough and recover."""
    order = sorted(range(len(paths)), key=lambda i: paths[i][nq_rank - 1])
    n, out = len(paths), {}
    for sc, (lo, hi) in BANDS.items():
        sel = [paths[i] for i in order[int(lo * n):int(hi * n)]]
        out[sc] = [mean(p[k] for p in sel) for k in range(len(paths[0]))]
    return out


def city_scenarios(fit, q0):
    paths = simulate(fit, q0, 40, NPATH, SEED)
    c = conditioned(paths)
    return {sc: [c[sc][k - 1] for k in POINT_Q] for sc in c}  # cumulative log changes at POINTS


def backtest_city(series):
    x = [math.log(series[i][1] / series[i - 1][1]) for i in range(1, len(series))]
    dates = [s[0] for s in series[1:]]
    rows = []
    for t in range(20, len(x)):
        fit = fit_ar1(x[:t])
        q0 = x[t - 1]
        sims = simulate(fit, q0, 12, 800, SEED + t)
        cond = conditioned(sims)
        for h in (4, 8, 12):
            if t + h > len(x):
                continue
            real = sum(x[t:t + h])
            lo, mid, hi = cond["bear"][h - 1], cond["base"][h - 1], cond["bull"][h - 1]
            mom = mean(x[max(0, t - 4):t]) * h
            rows.append({"origin": dates[t - 1], "h": h, "real": real, "p10": lo, "p50": mid, "p90": hi,
                         "rw": 0.0, "mom": mom, "drift": fit["drift"] * h, "correction": q0 < 0})
    summ = {}
    for h in (4, 8, 12):
        for label, filt in (("all", lambda r: True), ("correction", lambda r: r["correction"])):
            rs = [r for r in rows if r["h"] == h and filt(r)]
            if not rs:
                continue
            mae = lambda key: round(100 * mean(abs(r[key] - r["real"]) for r in rs), 2)  # noqa: E731
            cover = round(100 * sum(1 for r in rs if r["p10"] <= r["real"] <= r["p90"]) / len(rs))
            below = round(100 * sum(1 for r in rs if r["real"] < r["p10"]) / len(rs))
            summ[f"{label}_h{h}"] = {"n": len(rs), "coverage_band": cover, "below_bear": below,
                                     "mae_model": mae("p50"), "mae_random_walk": mae("rw"),
                                     "mae_momentum": mae("mom"), "mae_drift": mae("drift")}
    worst = sorted([r for r in rows if r["h"] == 8], key=lambda r: abs(r["real"] - r["p50"]), reverse=True)[:5]
    return {"summary": summ, "worst_8q": [{"origin": r["origin"], "real_pct": round(100 * (math.exp(r["real"]) - 1), 1),
                                            "base_pct": round(100 * (math.exp(r["p50"]) - 1), 1)} for r in worst],
            "rows_8q": [{"o": r["origin"], "real": round(100 * (math.exp(r["real"]) - 1), 1), "p10": round(100 * (math.exp(r["p10"]) - 1), 1),
                         "p50": round(100 * (math.exp(r["p50"]) - 1), 1), "p90": round(100 * (math.exp(r["p90"]) - 1), 1)}
                        for r in rows if r["h"] == 8]}


# ------------------------------------------------------------ finance (py)
def pmt(p, rate, years):
    i, n = rate / 100 / 12, years * 12
    return p * i / (1 - (1 + i) ** -n) if p > 0 else 0


def duty_fhor(v):
    if v <= 600_000:
        return 0.0
    if v <= 800_000:
        return math.ceil((v - 600_000) / 100) * 16.15
    bands = [(725_000, 28453, 5.15), (360_000, 11115, 4.75), (150_000, 3135, 3.80), (120_000, 2280, 2.85), (0, 0, 1.90)]
    for lo, base, r in bands:
        if v > lo:
            return base + math.ceil((v - lo) / 100) * r
    return 0.0


ASSUME = {"income1": 120_000, "income2": 80_000, "deposit": 130_000, "keep_buffer": 20_000, "other_costs": 3_000,
          "rate": 6.39, "stress": 2.0, "term": 25, "share": 0.30}


def conservative_price(a=ASSUME):
    cap = (a["income1"] + a["income2"]) * a["share"] / 12
    r, n = (a["rate"] + a["stress"]) / 100 / 12, a["term"] * 12
    max_loan = cap * (1 - (1 + r) ** -n) / r
    lo, hi = 300_000, 1_200_000
    for _ in range(60):
        mid = (lo + hi) / 2
        loan = mid + duty_fhor(mid) + a["other_costs"] - (a["deposit"] - a["keep_buffer"])
        lo, hi = (mid, hi) if loan <= max_loan else (lo, mid)
    return round(lo / 5000) * 5000, round(max_loan)


# ------------------------------------------------------------ helpers
def z(vals, v):
    sd = pstdev(vals) or 1
    return (v - mean(vals)) / sd


def norm(vals, v, invert=False):
    lo, hi = min(vals), max(vals)
    t = 0.5 if hi == lo else (v - lo) / (hi - lo)
    return round(1 - t if invert else t, 3)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def trend_map(r):
    return {t[0]: t for t in (r or {}).get("trend", [])}


def rent_map(r):
    return {t[0]: t for t in (r or {}).get("rent_trend", [])}


# ------------------------------------------------------------ main
def main():
    uni = load("universe.json")
    raw_all = load("suburbs_raw.json", {"suburbs": []})
    raw = {s["suburb"]: s for s in raw_all["suburbs"]}
    hz = load("hazards.json", {"suburbs": {}})
    market = load("market.json")
    abs_s = load("abs_rppi_perth.json")["series"]
    lag = market["monthly_path_reconstruction"]["lag_factor"]

    # ---- city model
    x = [math.log(abs_s[i][1] / abs_s[i - 1][1]) for i in range(1, len(abs_s))]
    fit = fit_ar1(x)
    q0 = math.log(1 - 0.057)
    city = city_scenarios(fit, q0)
    bt_city = backtest_city(abs_s)
    drift = fit["drift"]

    # ---- suburb records
    rows = []
    for u in uni["rows"]:
        if not u["included"]:
            continue
        nm = u["suburb"]
        rw = (raw.get(nm) or {}).get("reiwa_full") or {}
        mb = (raw.get(nm) or {}).get("microburbs") or {}
        sp = (raw.get(nm) or {}).get("spi") or {}
        h = (hz.get("suburbs") or {}).get(nm, {})
        beds = mb.get("house_beds") or {}
        ubeds = mb.get("unit_beds") or {}
        h3_r, h3_m = rw.get("MedianHouseSalePriceThreeBed"), beds.get("3 bed")
        u3_r, u3_m = rw.get("MedianUnitSalePriceThreeBed"), ubeds.get("3 bed")
        cnt = rw.get("CountOfHousesSold") or mb.get("house_sales_12m") or 0
        ucnt = rw.get("CountOfUnitsSold") or 0
        h3 = h3_r or h3_m
        h3_src = "REIWA" if h3_r else ("Microburbs" if h3_m else None)
        u3 = u3_r or u3_m
        agree = None
        if h3_r and h3_m:
            agree = round(100 * (h3_m / h3_r - 1), 1)
        if not h3 or cnt < 15:
            conf = "Insufficient"
        elif h3_r and cnt >= 60 and agree is not None and abs(agree) <= 10:
            conf = "High"
        elif cnt >= 25:
            conf = "Medium"
        else:
            conf = "Low"
        tm, rm = trend_map(rw), rent_map(rw)
        yrs = sorted(tm)
        def g(a, b):  # noqa: E306
            pa, pb = (tm.get(a) or [None, None])[1], (tm.get(b) or [None, None])[1]
            return round(100 * (pb / pa - 1), 1) if pa and pb else None
        rent = rw.get("MedianHouseRentPrice") or mb.get("house_rent")
        hm = rw.get("MedianHouseSalePrice") or mb.get("house_median")
        rent_prev = (rm.get(2025) or [None, None])[1]
        rows.append({
            "suburb": nm, "postcode": u["postcode"], "lga": (u["lga"] or "").replace(", City Of", "").replace(", Town Of", "").replace(", Shire Of", ""),
            "corridor": u["corridor"], "ring": u["ring"], "km": u["km"], "lat": u["lat"], "lon": u["lon"],
            "h3": h3, "h3_src": h3_src, "h3_reiwa": h3_r, "h3_mb": h3_m, "h3_agree_pct": agree,
            "h3_now": round(h3 * lag / 1000) * 1000 if h3 else None,
            "u3": u3, "u3_now": round(u3 * lag / 1000) * 1000 if u3 else None, "u3_count": ucnt,
            "h2": rw.get("MedianHouseSalePriceTwoBed") or beds.get("2 bed"), "h4": rw.get("MedianHouseSalePriceFourBed") or beds.get("4 bed"),
            "house_med": hm, "house_lq": rw.get("HouseSalePriceLowerQuartile"), "house_uq": rw.get("HouseSalePriceUpperQuartile"),
            "unit_med": rw.get("MedianUnitSalePrice"), "unit_lq": rw.get("UnitSalePriceLowerQuartile"),
            "land_med": rw.get("MedianLandSalePrice"), "land_count": rw.get("CountOfLandSold") or 0,
            "count": cnt, "dom": rw.get("dom_house") or sp.get("dom"), "rent": rent, "rent3": rw.get("MedianHouseRentPrice3Bed") or rw.get("MedianHouseRentPriceThreeBed"),
            "rent_g1": round(100 * (rent / rent_prev - 1), 1) if rent and rent_prev else None,
            "yield": round(52 * rent / hm * 100, 2) if rent and hm else None,
            "g1": rw.get("g1") if rw else (round(100 * mb["house_growth_12m"], 1) if mb.get("house_growth_12m") is not None else None),
            "g3": g(2023, 2026), "g5": rw.get("g5"), "g10": rw.get("g10"), "g10_pa": rw.get("g10_pa"),
            "trend": [[t[0], t[1], t[2]] for t in rw.get("trend", [])],
            "trains": rw.get("trains") or "", "rail": bool((rw.get("trains") or "").strip()),
            "population": rw.get("population"), "house_pct": rw.get("dwelling_house_pct"), "semi_pct": rw.get("dwelling_semi_pct"),
            "rented_pct": rw.get("tenure_rented_pct"),
            "bushfire_pct": h.get("bushfire_pct"), "flood_pct": h.get("flood_pct"), "flags": h.get("flags", []),
            "conf": conf, "as_at": rw.get("as_at"), "period": rw.get("period"),
            "src": {k: v for k, v in (("reiwa", rw.get("url")), ("microburbs", mb.get("url")), ("spi", sp.get("url"))) if v},
        })

    # ---- beta from REIWA annual medians (cycle amplitude)
    good = [r for r in rows if len(r["trend"]) >= 9 and all((t[2] or 0) >= 20 and t[1] for t in r["trend"])]
    years = sorted({t[0] for r in good for t in r["trend"]})
    city_chg = {}
    for y in years[1:]:
        ch = [math.log(dict((t[0], t[1]) for t in r["trend"])[y] / dict((t[0], t[1]) for t in r["trend"])[y - 1])
              for r in good if y in dict((t[0], t[1]) for t in r["trend"]) and (y - 1) in dict((t[0], t[1]) for t in r["trend"])]
        city_chg[y] = median(ch) if ch else None
    for r in rows:
        r["beta"], r["beta_raw"] = 1.0, None
        if r in good:
            tm = dict((t[0], t[1]) for t in r["trend"])
            pairs = [(math.log(tm[y] / tm[y - 1]), city_chg[y]) for y in years[1:] if y in tm and y - 1 in tm and city_chg.get(y) is not None]
            if len(pairs) >= 7:
                cs = [c for _, c in pairs]
                mc = mean(cs)
                var = sum((c - mc) ** 2 for c in cs) or 1e-9
                b = sum((s - mean(s for s, _ in pairs)) * (c - mc) for s, c in pairs) / var
                r["beta_raw"] = round(b, 2)
                r["beta"] = round(clamp(1 + 0.5 * (b - 1), 0.7, 1.5), 2)

    # ---- tilt rank back-test (REIWA annual data)
    def tilt_bt(y0, y1):
        feats = []
        for r in rows:
            tm, rm = dict((t[0], t[1]) for t in r["trend"]), None
            rw = (raw.get(r["suburb"]) or {}).get("reiwa_full") or {}
            rm = dict((t[0], t[1]) for t in rw.get("rent_trend", []))
            if not all(tm.get(y) for y in (y0 - 3, y0, y1)) or not rm.get(y0) or not rm.get(y0 - 1) or r["count"] < 20:
                continue
            feats.append({"s": r["suburb"], "yield": 52 * rm[y0] / tm[y0], "rg": rm[y0] / rm[y0 - 1] - 1,
                          "run": tm[y0] / tm[y0 - 3] - 1, "rail": r["rail"], "act": tm[y1] / tm[y0] - 1})
        if len(feats) < 15:
            return None
        ys, rg, rn = [f["yield"] for f in feats], [f["rg"] for f in feats], [f["run"] for f in feats]
        sc = [0.45 * z(ys, f["yield"]) + 0.30 * z(rg, f["rg"]) - 0.40 * z(rn, f["run"]) + (0.3 if f["rail"] else -0.1) for f in feats]
        act = [f["act"] for f in feats]
        return {"window": f"{y0}->{y1}", "n": len(feats), "rho_tilt": spearman(sc, act),
                "rho_momentum": spearman(rn, act), "rho_yield": spearman(ys, act)}
    tbt = [b for b in (tilt_bt(2020, 2023), tilt_bt(2023, 2026)) if b]
    use_tilt = bool(tbt) and all(b["rho_tilt"] > b["rho_momentum"] and b["rho_tilt"] > 0 for b in tbt)

    pool = [r for r in rows if r["yield"] and r["rent_g1"] is not None and r["g5"] is not None]
    ys, rgs, g5s = [r["yield"] for r in pool], [r["rent_g1"] for r in pool], [r["g5"] for r in pool]
    for r in rows:
        if use_tilt and r in pool:
            parts = {"yield": 0.45 * z(ys, r["yield"]), "rent_growth": 0.30 * z(rgs, r["rent_g1"]),
                     "price_run": -0.40 * z(g5s, r["g5"]), "rail": 0.3 if r["rail"] else -0.1,
                     "supply": -0.3 if r["count"] and r["land_count"] / max(1, r["count"]) > 0.25 else 0.0}
            r["tilt"] = round(clamp(sum(parts.values()) * 0.5, -0.75, 0.75), 2)
            r["tilt_parts"] = {k: round(v * 0.5, 2) for k, v in parts.items()}
        else:
            r["tilt"], r["tilt_parts"] = 0.0, {}

    # ---- suburb scenario paths (houses, 3-bed)
    for r in rows:
        r["paths"] = None
        if r["conf"] == "Insufficient" or not r["h3_now"]:
            continue
        widen = 1 + max(0, (40 - r["count"])) / 40
        out = {}
        i8 = POINT_Q.index(8)

        def cum_for(sc, i, k):
            # beta scales the current cycle (to Oct 2028); afterwards the suburb moves with the city
            c = r["beta"] * city[sc][min(i, i8)] + (city[sc][i] - city[sc][i8] if i > i8 else 0.0)
            return c + (r["tilt"] / 100) * max(0, k - 8) / 4
        base_cum = [cum_for("base", i, k) for i, k in enumerate(POINT_Q)]
        for sc in ("bear", "base", "bull"):
            vals = []
            for i, k in enumerate(POINT_Q):
                cum = cum_for(sc, i, k)
                if sc != "base":
                    cum = base_cum[i] + (cum - base_cum[i]) * widen
                vals.append(round(r["h3_now"] * math.exp(cum) / 1000) * 1000)
            out[sc] = vals
        r["paths"] = out
        r["widen"] = round(widen, 2)
        start = r["h3_now"]
        r["bear_trough"] = min(out["bear"])
        r["bear_trough_date"] = POINTS[out["bear"].index(r["bear_trough"])]
        r["first_below_A"] = {sc: next((POINTS[i] for i, v in enumerate(out[sc]) if v <= BUDGET_A), None) for sc in out}
        r["need_fall_A"] = round(100 * max(0.0, 1 - BUDGET_A / start), 1)

    # ---- stretch budget: buyer affordability ceiling x market evidence
    ceiling, max_loan = conservative_price()
    priced = sorted(r["h3_now"] for r in rows if r["h3_now"] and r["ring"] in ("Middle", "Outer") and r["conf"] != "Insufficient")
    market_p40 = priced[int(0.4 * len(priced))] if priced else None
    stretch_hi = min(ceiling, round((market_p40 or ceiling) / 5000) * 5000)
    stretch = {"ceiling": ceiling, "max_loan_conservative": max_loan, "market_p40_mid_outer_3bed_now": market_p40,
               "low": 625_000, "high": stretch_hi,
               "method": "High end = lower of (a) the conservative affordability ceiling: repayments at rate+2pts over 25 years within 30% of gross income, keeping a $20k cash buffer, FHOR duty and $3k costs included; and (b) the 40th percentile of lag-adjusted 3-bed house medians in middle/outer southern suburbs. Low end = $625k (first price that clearly exceeds the $600k duty-free threshold by more than typical negotiation)."}

    # ---- affordability groups
    neg_cut = BUDGET_A / (1 - 0.047)  # lag-adjusted value minus avg capital-city vendor discount 4.7%
    def group(now):  # noqa: E306
        if now is None:
            return "Insufficient data"
        if now <= BUDGET_A:
            return "1 Evidenced <= $600k"
        if now <= neg_cut:
            return "2 Negotiable to $600k"
        if now <= stretch_hi:
            return "3 Stretch budget"
        return "4 Unlikely without big falls"
    for r in rows:
        r["group_house"] = group(r["h3_now"] if r["conf"] != "Insufficient" else None)
        r["group_th"] = group(r["u3_now"] if r["u3_now"] and r["u3_count"] >= 15 else None)
        r["lq_under_A"] = bool(r["house_lq"] and r["house_lq"] <= BUDGET_A)
        r["median_settled_under_A"] = bool(r["h3"] and r["h3"] <= BUDGET_A and r["conf"] != "Insufficient")

    # ---- score components (0-1); weights applied in the page
    valid = [r for r in rows if r["conf"] != "Insufficient"]
    lc = [math.log(max(1, r["count"])) for r in valid]
    doms = [r["dom"] for r in valid if r["dom"]]
    yv = [r["yield"] for r in valid if r["yield"]]
    rgv = [r["rent_g1"] for r in valid if r["rent_g1"] is not None]
    for r in rows:
        if r["conf"] == "Insufficient":
            r["comp"] = None
            continue
        p = r["h3_now"]
        loan = max(0, p + duty_fhor(p) + 3000 - 110_000)
        share = pmt(loan, ASSUME["rate"] + 2, 25) / (200_000 / 12)
        risk = 1 - 0.6 * (r["bushfire_pct"] or 0) / 100 - 0.4 * min(1, (r["flood_pct"] or 0) / 10) - 0.12 * len([f for f in r["flags"] if not f.startswith("No freehold")])
        r["comp"] = {
            "afford": round(clamp(1 - (p - BUDGET_A) / (stretch_hi + 50_000 - BUDGET_A), 0, 1), 3),
            "sustain": round(clamp(1 - (share - 0.25) / 0.15, 0, 1), 3),
            "suit": round(0.5 * (1 if r["h3"] else 0) + 0.5 * ((r["house_pct"] or 50) / 100), 3),
            "access": round(0.5 * (1 if r["rail"] else 0) + 0.5 * clamp(1 - r["km"] / 35, 0, 1), 3),
            "fund": round(0.5 * (norm(yv, r["yield"]) if r["yield"] else 0.5) + 0.5 * (norm(rgv, r["rent_g1"]) if r["rent_g1"] is not None else 0.5), 3),
            "liquid": round(0.6 * norm(lc, math.log(max(1, r["count"]))) + 0.4 * (norm(doms, r["dom"], invert=True) if r["dom"] else 0.5), 3),
            "risk": round(clamp(risk, 0, 1), 3),
            "conf": {"High": 1.0, "Medium": 0.6, "Low": 0.3}[r["conf"]],
        }

    # ---- corridor / ring comparison
    def agg(sel):  # noqa: E306
        v = [r for r in rows if sel(r)]
        pr = [r["h3_now"] for r in v if r["h3_now"] and r["conf"] != "Insufficient"]
        return {"n": len(v), "n_priced": len(pr), "median_3bed_now": round(median(pr)) if pr else None,
                "g1": sum(1 for r in v if r["group_house"].startswith("1")), "g2": sum(1 for r in v if r["group_house"].startswith("2")),
                "g3": sum(1 for r in v if r["group_house"].startswith("3")),
                "dom": round(median([r["dom"] for r in v if r["dom"]])) if any(r["dom"] for r in v) else None,
                "yield": round(median([r["yield"] for r in v if r["yield"]]), 2) if any(r["yield"] for r in v) else None,
                "rail_share": round(100 * sum(1 for r in v if r["rail"]) / max(1, len(v))),
                "bushfire_avg": round(mean([r["bushfire_pct"] or 0 for r in v]), 1) if v else None,
                "flood_avg": round(mean([r["flood_pct"] or 0 for r in v]), 1) if v else None,
                "beta_med": round(median([r["beta"] for r in v]), 2) if v else None,
                "g5_med": round(median([r["g5"] for r in v if r["g5"] is not None]), 1) if any(r["g5"] is not None for r in v) else None,
                "sales": sum(r["count"] or 0 for r in v)}
    corridors = {c: agg(lambda r, c=c: r["corridor"] == c) for c in sorted({r["corridor"] for r in rows})}
    rings = {g: agg(lambda r, g=g: r["ring"] == g) for g in ("Inner", "Middle", "Outer")}

    # ---- market temperature (documented, judgement-based mapping)
    temp_signals = [
        {"k": "Quarterly price change -5.7%", "s": -2, "w": 2, "why": "Fastest Perth quarterly fall since the series' worst periods; correction established"},
        {"k": "Monthly trend: Aug -2.0, Sep -2.1, Oct -1.7, 28d to 9 Nov -1.7", "s": -1.5, "w": 2, "why": "Large but no longer clearly accelerating"},
        {"k": "Days on market 39 (capitals)", "s": -1, "w": 1, "why": "Highest since Aug 2020; not Perth-specific"},
        {"k": "Vendor discount 4.7% (capitals)", "s": -1, "w": 1, "why": "Largest since May 2019; not Perth-specific"},
        {"k": "Listings: highest for season since 2019 (capitals)", "s": -1, "w": 1, "why": "Stock building despite fewer new listings"},
        {"k": "Perth sales volume back to 2019 levels (REIWA)", "s": -1, "w": 1, "why": "Fewer transactions = weak demand"},
        {"k": "Cash rate 4.85% after 5 hikes; no cut priced before 2028", "s": -1.5, "w": 2, "why": "Serviceability is the binding constraint"},
        {"k": "WA unemployment 4.2%", "s": 1, "w": 1, "why": "Jobs market still solid; forced selling limited"},
        {"k": "WA population +2.1% (fastest state)", "s": 1, "w": 1, "why": "Underlying housing demand intact (lagging data)"},
        {"k": "Rental vacancy 1.7% REIWA / 0.6% SQM", "s": 0.5, "w": 1, "why": "Tight but loosening"},
    ]
    tw = sum(s["w"] for s in temp_signals)
    temp = round(sum(s["s"] * s["w"] for s in temp_signals) / tw, 2)

    # ---- summary counts
    counts = {
        "universe": len(rows),
        "priced": sum(1 for r in rows if r["conf"] != "Insufficient"),
        "insufficient": sum(1 for r in rows if r["conf"] == "Insufficient"),
        "median_3bed_settled_under_A": sum(1 for r in rows if r["median_settled_under_A"]),
        "lag_adjusted_under_A": sum(1 for r in rows if r["group_house"].startswith("1")),
        "negotiable": sum(1 for r in rows if r["group_house"].startswith("2")),
        "stretch": sum(1 for r in rows if r["group_house"].startswith("3")),
        "unlikely": sum(1 for r in rows if r["group_house"].startswith("4")),
        "townhouse_under_A": sum(1 for r in rows if r["group_th"].startswith("1")),
        "lq_under_A": sum(1 for r in rows if r["lq_under_A"]),
        "listings_verified": None,
        "individual_sales_verified": None,
    }

    city_pts = {sc: [round(100 * (math.exp(v) - 1), 1) for v in vals] for sc, vals in city.items()}
    out = {
        "model_version": MODEL_VERSION, "generated": date.today().isoformat(), "data_collected": raw_all.get("collected"), "start_date": START_DATE,
        "points": POINTS, "point_q": POINT_Q, "horizons": HORIZONS, "budget_a": BUDGET_A,
        "assumptions": ASSUME, "stretch": stretch, "negotiable_cut": round(neg_cut), "lag_factor": lag,
        "city": {"pct": city_pts, "fit": {"drift_q_pct": round(100 * fit["drift"], 2), "drift_pa_pct": round(100 * (math.exp(4 * fit["drift"]) - 1), 2),
                                           "phi": round(fit["phi"], 3), "n": fit["n"], "resid_sd_pct": round(100 * pstdev(fit["res"]), 2)},
                 "q0_pct": -5.7, "npath": NPATH, "seed": SEED},
        "backtest_city": bt_city, "backtest_tilt": tbt, "use_tilt": use_tilt,
        "abs_series": abs_s, "temperature": {"value": temp, "signals": temp_signals,
                                             "formula": "Weighted mean of signal scores (-2 strongly bearish .. +2 strongly bullish). Scores are analyst judgements mapped from cited data, not statistics."},
        "counts": counts, "corridors": corridors, "rings": rings, "market": market,
        "universe_meta": uni["meta"], "universe": uni["rows"], "hazard_meta": {k: v for k, v in hz.items() if k != "suburbs"},
        "suburbs": rows,
    }
    tmp = D / "model.tmp"
    tmp.write_text(json.dumps(out, separators=(",", ":")))
    os.replace(tmp, D / "model.json")
    print(json.dumps({"fit": out["city"]["fit"], "city_12m": {k: v[3] for k, v in city_pts.items()},
                      "city_24m": {k: v[7] for k, v in city_pts.items()}, "city_10y": {k: v[-1] for k, v in city_pts.items()},
                      "bt": {k: v for k, v in bt_city["summary"].items() if "h8" in k or "h4" in k},
                      "tilt_bt": tbt, "use_tilt": use_tilt, "stretch": stretch, "counts": counts, "temp": temp}, indent=1))


if __name__ == "__main__":
    main()
