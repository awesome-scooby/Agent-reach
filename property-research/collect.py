#!/usr/bin/env python3
"""Collect suburb-level property data for the Melbourne (north/west) vs
Perth (south) comparison.

Sources (all public pages, allowed by each site's robots.txt):
  * Microburbs suburb report  - monthly median house/unit sale price and rent,
                                Nov 2021 -> latest; medians by bedroom count.
  * Smart Property Investment - 3m / 12m / 3y / 5y growth, 10-yr average
                                annual growth, gross yield, days on market.
  * REIWA suburb page (WA)    - 12-month median, 3-bed house median, rent.

Politeness: one request at a time, ~1.5 s apart, raw HTML cached in
.cache/ so re-runs don't hit the sites again (delete .cache to refresh).

Usage:  python3 collect.py            -> writes data/suburbs.json
"""
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
OUT = ROOT / "data" / "suburbs.json"
UA = "agent-reach-property-research/1.0 (personal, low-rate research)"
DELAY = 1.5

# (name, postcode, region) -------------------------------------------------
MELBOURNE = [
    # West
    ("Melton", "3337", "West"), ("Melton South", "3338", "West"),
    ("Kurunjang", "3337", "West"), ("Melton West", "3337", "West"),
    ("Brookfield", "3338", "West"), ("Werribee", "3030", "West"),
    ("Wyndham Vale", "3024", "West"), ("Manor Lakes", "3024", "West"),
    ("Hoppers Crossing", "3029", "West"), ("Tarneit", "3029", "West"),
    ("Deer Park", "3023", "West"), ("St Albans", "3021", "West"),
    # North
    ("Craigieburn", "3064", "North"), ("Wallan", "3756", "North"),
    ("Kalkallo", "3064", "North"), ("Mickleham", "3064", "North"),
    ("Donnybrook", "3064", "North"), ("Roxburgh Park", "3064", "North"),
    ("Broadmeadows", "3047", "North"), ("Meadow Heights", "3048", "North"),
    ("Sunbury", "3429", "North"), ("Lalor", "3075", "North"),
    ("Glenroy", "3046", "North"),
]
PERTH = [
    # South-east corridor
    ("Armadale", "6112", "South-East"), ("Kelmscott", "6111", "South-East"),
    ("Gosnells", "6110", "South-East"), ("Maddington", "6109", "South-East"),
    ("Seville Grove", "6112", "South-East"), ("Camillo", "6111", "South-East"),
    ("Brookdale", "6112", "South-East"), ("Haynes", "6112", "South-East"),
    ("Byford", "6122", "South-East"), ("Thornlie", "6108", "South-East"),
    ("Beckenham", "6107", "South-East"),
    # South-west / Kwinana-Rockingham corridor
    ("Medina", "6167", "South-West"), ("Parmelia", "6167", "South-West"),
    ("Calista", "6167", "South-West"), ("Orelia", "6167", "South-West"),
    ("Bertram", "6167", "South-West"), ("Wellard", "6170", "South-West"),
    ("Cooloongup", "6168", "South-West"), ("Rockingham", "6168", "South-West"),
    ("Waikiki", "6169", "South-West"), ("Warnbro", "6169", "South-West"),
    ("Safety Bay", "6169", "South-West"), ("Port Kennedy", "6172", "South-West"),
    ("Baldivis", "6171", "South-West"),
]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def fetch(url, key):
    CACHE.mkdir(exist_ok=True)
    f = CACHE / f"{key}.html"
    if f.exists() and f.stat().st_size > 5000:
        return f.read_text(encoding="utf-8", errors="ignore")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read().decode("utf-8", errors="ignore")
    except Exception as e:  # noqa: BLE001
        print(f"  ! {url}: {e}", file=sys.stderr)
        body = ""
    time.sleep(DELAY)
    if len(body) > 5000:
        f.write_text(body, encoding="utf-8")
    return body


def text_of(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))


def num(s):
    if s is None:
        return None
    s = s.replace(",", "").replace("$", "").replace("%", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


# --- Microburbs ------------------------------------------------------------
def microburbs(name, pc, state):
    url = f"https://www.microburbs.com.au/suburb-reports-lite/{slug(name)}-{state.lower()}-{pc}"
    raw = fetch(url, f"mb_{state}_{slug(name)}").replace('\\"', '"')
    out = {"url": url}
    for k in ("salePoints", "rentPoints"):
        m = re.search(r'"%s":(\[.*?\])' % k, raw)
        if m:
            try:
                out[k] = json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    m = re.search(r'"metrics":(\{"house":.*?\}\}\})', raw)
    if m:
        blob = m.group(1)
        # bedroom medians for houses and units
        for typ in ("house", "unit"):
            mm = re.search(r'"%s":\{"sale":\{"value":(\d+|null),"growth":([\d.\-e]+|null),"bedrooms":(\[.*?\])' % typ, blob)
            if mm:
                out[f"{typ}_median"] = None if mm.group(1) == "null" else int(mm.group(1))
                out[f"{typ}_growth_12m"] = None if mm.group(2) == "null" else float(mm.group(2))
                try:
                    beds = json.loads(mm.group(3))
                    out[f"{typ}_beds"] = {b["label"]: b["value"] for b in beds}
                except json.JSONDecodeError:
                    pass
        mm = re.search(r'"house":\{"sale":.*?"rent":\{"value":(\d+)', blob)
        if mm:
            out["house_rent"] = int(mm.group(1))
    sample = re.search(r"Based on (\d+) sales in the preceding 12 months", raw)
    if sample:
        out["house_sales_12m"] = int(sample.group(1))
    return out


# --- Smart Property Investment ---------------------------------------------
SPI_FIELDS = {
    "Median Price": "median",
    "Median Quarterly": "g_3m",
    "Median 12 month": "g_12m",
    "Median 3 years": "g_3y",
    "Median 5 years": "g_5y",
    "Rental Yield Percent": "yield",
}


def spi(name, pc, state):
    url = f"https://www.smartpropertyinvestment.com.au/data/{state.lower()}/{pc}/{slug(name)}"
    raw = fetch(url, f"spi_{state}_{slug(name)}")
    out = {"url": url}
    # The page has a HOUSE table then a UNIT table with the same labels.
    for label, key in SPI_FIELDS.items():
        vals = re.findall(re.escape(label) + r"</td>\s*<td[^>]*>\s*([^<]+?)\s*<", raw)
        for typ, v in zip(("house", "unit"), vals):
            out[f"{typ}_{key}"] = num(v)
    t = text_of(raw)
    m = re.search(r"obtained a ([\d.]+)% growth over a ten-year period", t)
    if m:
        out["g_10y_pa"] = float(m.group(1))
    m = re.search(r"wait an average of ([\d.]+) days", t)
    if m:
        out["dom"] = float(m.group(1))
    return out


# --- REIWA (WA only) -------------------------------------------------------
def reiwa(name):
    url = f"https://reiwa.com.au/suburb/{slug(name)}/"
    raw = fetch(url, f"reiwa_{slug(name)}")
    t = text_of(raw)
    out = {"url": url}
    m = re.search(r"([\-\d.]+)% Sales price growth \$([\d.]+)K \* Median sales price ([\-\d.]+)% Rental price growth \$(\d+)pw", t)
    if m:
        out.update(growth_12m=float(m.group(1)), median=float(m.group(2)) * 1000,
                   rent_growth=float(m.group(3)), rent=int(m.group(4)))
    # bedroom split appears in the embedded JSON
    r2 = raw.replace('\\"', '"')
    for beds in ("2", "3", "4"):
        mm = re.search(r'"Bedrooms":"?%s"?[^}]{0,200}?"Median(?:Sale)?Price":"?\$?([\d,\.]+)K?' % beds, r2)
        if mm:
            out[f"house_{beds}br"] = num(mm.group(1))
    return out


def main():
    rows = []
    for city, state, lst in (("Melbourne", "VIC", MELBOURNE), ("Perth", "WA", PERTH)):
        for name, pc, region in lst:
            print(f"{city:9s} {name}", file=sys.stderr)
            row = {"city": city, "state": state, "suburb": name, "postcode": pc, "region": region,
                   "microburbs": microburbs(name, pc, state), "spi": spi(name, pc, state)}
            if state == "WA":
                row["reiwa"] = reiwa(name)
            rows.append(row)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"collected": time.strftime("%Y-%m-%d"), "suburbs": rows}, indent=1))
    print(f"wrote {OUT} ({len(rows)} suburbs)", file=sys.stderr)


if __name__ == "__main__":
    main()
