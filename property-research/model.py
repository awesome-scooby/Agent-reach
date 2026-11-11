#!/usr/bin/env python3
"""Scenario forecast + 'match score' for each suburb.

This is a scenario model, not a prediction. Every number it produces comes
from the inputs and rules below, so you can disagree with a rule and change it.

1. City paths (annual % change, 2027..2036) in three scenarios. These are
   judgement calls anchored on:
     - Cotality Oct 2026: capitals -8.1% in 7 months; Perth -1.7% m/m, -5.7% q/q
     - RBA cash rate 4.85% (3 Nov 2026), no cut expected before 2028
     - Long-run nominal house growth of roughly 5-6% p.a. in both cities
     - Perth entry-level prices up 100-165% in 5 years (stretched), Melbourne
       outer suburbs up 10-35% (not stretched), Melbourne city 7% below 2021
2. Suburb tilt (p.a., applied to the recovery years) from data in suburbs.json:
     + gross rental yield above city peers   (rent supports price)
     + rent growth above city peers           (real demand)
     - 5-year price run above city peers       (mean reversion)
     - greenfield estate with large land supply (supply caps growth)
     + train station in the suburb
   clamped to +/-1.5% p.a.
3. Bear-case depth scales with how far the suburb ran up in 5 years.
"""
import json
import math
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "data" / "suburbs.json"
OUT = ROOT / "data" / "model.json"

YEARS = list(range(2027, 2037))
CITY_PATHS = {
    "Melbourne": {
        "bear": [-6, -2, 1, 2, 3, 3, 3, 3, 3, 3],
        "base": [-3, 1, 3.5, 4.5, 5, 5, 5, 5, 5, 5],
        "bull": [0, 4, 6, 6, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5],
    },
    "Perth": {
        "bear": [-10, -6, -1, 1, 2, 3, 3, 3, 3, 3],
        "base": [-6, -2, 2, 4, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
        "bull": [-2, 3, 6, 6, 6, 6, 6, 6, 6, 6],
    },
}

# Approximate road distance to CBD (km) and whether the suburb has its own
# train station. From general knowledge, not a sourced dataset - check commute
# times yourself at 7:30am before buying.
GEO = {
    "Melton": (40, True), "Melton South": (40, True), "Kurunjang": (39, False),
    "Melton West": (42, False), "Brookfield": (38, False), "Werribee": (32, True),
    "Wyndham Vale": (35, True), "Manor Lakes": (36, False), "Hoppers Crossing": (25, True),
    "Tarneit": (25, True), "Deer Park": (18, True), "St Albans": (17, True),
    "Craigieburn": (25, True), "Wallan": (45, True), "Kalkallo": (30, False),
    "Mickleham": (30, False), "Donnybrook": (32, True), "Roxburgh Park": (22, True),
    "Broadmeadows": (16, True), "Meadow Heights": (19, False), "Sunbury": (38, True),
    "Lalor": (17, True), "Glenroy": (12, True),
    "Armadale": (28, True), "Kelmscott": (24, True), "Gosnells": (20, True),
    "Maddington": (16, True), "Seville Grove": (28, False), "Camillo": (23, False),
    "Brookdale": (27, False), "Haynes": (29, False), "Byford": (35, True),
    "Thornlie": (16, True), "Beckenham": (13, True), "Medina": (33, False),
    "Parmelia": (33, False), "Calista": (34, False), "Orelia": (33, False),
    "Bertram": (32, False), "Wellard": (33, True), "Cooloongup": (40, False),
    "Rockingham": (41, True), "Waikiki": (43, False), "Warnbro": (45, True),
    "Safety Bay": (44, False), "Port Kennedy": (46, False), "Baldivis": (41, False),
}
# Suburbs where a large share of sales are new house-and-land packages with
# plenty of land still to come. Their 2021 medians are also distorted by
# land-only / off-the-plan settlements, so their 5-year growth is overstated.
GREENFIELD = {"Kalkallo", "Mickleham", "Donnybrook", "Wallan", "Tarneit", "Manor Lakes",
              "Melton West", "Brookfield", "Kurunjang", "Byford", "Baldivis", "Wellard",
              "Bertram", "Haynes"}

BUDGET = 600_000


def z(vals, v):
    sd = pstdev(vals) or 1
    return (v - mean(vals)) / sd


def main():
    rows = json.loads(SRC.read_text())["suburbs"]
    out = []
    # ---------------- per-suburb derived metrics ----------------
    for r in rows:
        mb, sp = r["microburbs"], r["spi"]
        pts = [p for p in mb.get("salePoints", []) if p.get("house")]
        rpts = [p for p in mb.get("rentPoints", []) if p.get("house")]
        h0, h1 = pts[0]["house"], pts[-1]["house"]
        rent0, rent1 = rpts[0]["house"], rpts[-1]["house"]
        r_last12 = rpts[-13]["house"] if len(rpts) > 13 else rent0
        beds = mb.get("house_beds", {})
        ubeds = mb.get("unit_beds", {})
        km, rail = GEO[r["suburb"]]
        d = {
            "city": r["city"], "suburb": r["suburb"], "postcode": r["postcode"], "region": r["region"],
            "km": km, "rail": rail, "greenfield": r["suburb"] in GREENFIELD,
            "house_median": mb.get("house_median") or h1,
            "house_3br": beds.get("3 bed"), "house_4br": beds.get("4 bed"), "house_2br": beds.get("2 bed"),
            "unit_median": mb.get("unit_median"), "unit_3br": ubeds.get("3 bed"), "unit_2br": ubeds.get("2 bed"),
            "rent": mb.get("house_rent") or rent1,
            "yield": round(52 * rent1 / h1 * 100, 2),
            "yield_2021": round(52 * rent0 / h0 * 100, 2),
            "g5": round((h1 / h0 - 1) * 100, 1),
            "g5_pa": round(((h1 / h0) ** (1 / 5) - 1) * 100, 1),
            "g12": round((pts[-1]["house"] / pts[-13]["house"] - 1) * 100, 1),
            "g6": round((pts[-1]["house"] / pts[-7]["house"] - 1) * 100, 1),
            "rent_g12": round((rent1 / r_last12 - 1) * 100, 1),
            "spi_g10_pa": sp.get("g_10y_pa"), "spi_g5": sp.get("house_g_5y"),
            "dom": sp.get("dom"), "sales_12m": mb.get("house_sales_12m"),
            "series": [[p["date"][:7], p["house"], p.get("unit")] for p in pts],
            "rent_series": [[p["date"][:7], p["house"]] for p in rpts],
            "sources": {"microburbs": mb["url"], "spi": sp["url"], **({"reiwa": r["reiwa"]["url"]} if r.get("reiwa") else {})},
        }
        if r.get("reiwa"):
            d["reiwa_median"] = r["reiwa"].get("median")
            d["reiwa_rent"] = r["reiwa"].get("rent")
        out.append(d)

    # ---------------- tilt within each city ----------------
    for city in ("Melbourne", "Perth"):
        grp = [d for d in out if d["city"] == city]
        ys = [d["yield"] for d in grp]; rg = [d["rent_g12"] for d in grp]; g5 = [d["g5"] for d in grp]
        for d in grp:
            parts = {
                "yield": 0.45 * z(ys, d["yield"]),
                "rent_growth": 0.30 * z(rg, d["rent_g12"]),
                "price_run": -0.40 * z(g5, d["g5"]),
                "supply": -0.60 if d["greenfield"] else 0.0,
                "rail": 0.30 if d["rail"] else -0.10,
            }
            tilt = max(-1.5, min(1.5, sum(parts.values())))
            d["tilt"] = round(tilt, 2)
            d["tilt_parts"] = {k: round(v, 2) for k, v in parts.items()}
            stretch = max(0.0, z(g5, d["g5"]))
            paths = {}
            for sc, path in CITY_PATHS[city].items():
                adj = []
                for i, g in enumerate(path):
                    if i < 2:  # correction years: tilt half-weight, bear deepened by stretch
                        gg = g + tilt * 0.5
                        if sc == "bear" and g < 0:
                            gg = g * (1 + 0.25 * stretch)
                    else:
                        gg = g + tilt
                    adj.append(round(gg, 2))
                paths[sc] = adj
            d["paths"] = paths
            start = d["house_3br"] or d["house_median"]
            proj = {}
            for sc, p in paths.items():
                v = start; vals = []
                for g in p:
                    v *= 1 + g / 100
                    vals.append(round(v))
                proj[sc] = vals
            d["proj_3br"] = proj
            d["trough_bear"] = round((min([start] + proj["bear"]) / start - 1) * 100, 1)
            d["cagr10_base"] = round(((proj["base"][-1] / start) ** 0.1 - 1) * 100, 2)
            d["cagr10_bear"] = round(((proj["bear"][-1] / start) ** 0.1 - 1) * 100, 2)
            d["cagr10_bull"] = round(((proj["bull"][-1] / start) ** 0.1 - 1) * 100, 2)

    # ---------------- match score (0-100) ----------------
    cg = [d["cagr10_base"] for d in out]; tr = [d["trough_bear"] for d in out]
    for d in out:
        p3 = d["house_3br"] or d["house_median"]
        afford = 1.0 if p3 <= BUDGET else max(0.0, 1 - (p3 - BUDGET) / 150_000)
        growth = (d["cagr10_base"] - min(cg)) / (max(cg) - min(cg))
        downside = (d["trough_bear"] - min(tr)) / (max(tr) - min(tr))
        rent = min(1.0, max(0.0, (d["yield"] - 3.2) / 1.6))
        access = (0.6 if d["rail"] else 0.2) + 0.4 * max(0.0, 1 - (d["km"] - 12) / 35)
        parts = {"afford": afford * 35, "growth": growth * 25, "downside": downside * 15,
                 "rent": rent * 10, "access": access * 15}
        d["match_parts"] = {k: round(v, 1) for k, v in parts.items()}
        d["match"] = round(sum(parts.values()))
        d["in_budget_house"] = bool(d["house_3br"] and d["house_3br"] <= BUDGET)
        d["in_budget_unit"] = bool(d["unit_3br"] and d["unit_3br"] <= BUDGET)

    # ---------------- city index from suburb series ----------------
    city_idx = {}
    for city in ("Melbourne", "Perth"):
        grp = [d for d in out if d["city"] == city]
        n = min(len(d["series"]) for d in grp)
        idx = []
        for i in range(n):
            vals = [d["series"][i][1] / d["series"][0][1] for d in grp if not d["greenfield"]]
            idx.append([grp[0]["series"][i][0], round(100 * math.exp(mean(math.log(v) for v in vals)), 1)])
        city_idx[city] = idx

    OUT.write_text(json.dumps({"years": YEARS, "city_paths": CITY_PATHS, "city_index": city_idx,
                               "budget": BUDGET, "suburbs": out}, separators=(",", ":")))
    out.sort(key=lambda d: -d["match"])
    for d in out[:47]:
        print(f'{d["match"]:3d} {d["city"][:3]} {d["suburb"]:16s} 3br {d["house_3br"]} tilt {d["tilt"]:+.2f} '
              f'base10 {d["cagr10_base"]:.2f}% bear trough {d["trough_bear"]}% yld {d["yield"]} g5 {d["g5"]}')


if __name__ == "__main__":
    main()
