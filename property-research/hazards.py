#!/usr/bin/env python3
"""Bushfire, flood and crime figures per suburb from government open data.

  Victoria
    * Suburb boundary, Designated Bushfire Prone Area, and Victorian Flood
      History (areas observed flooded), from the Vicmap open-data WFS
      (opendata.maps.vic.gov.au).
    * Crime Statistics Agency: criminal incidents by suburb, year ending
      June 2026 (Table 03 of the LGA file), divided by 2021 census
      population -> incidents per 1,000 residents.
  Western Australia
    * Landgate localities (LGATE-234), Bush Fire Prone Areas (OBRM-026) and
      DWER 1-in-100 (1% AEP) floodway and flood-fringe areas (DWER-014),
      from the SLIP public ArcGIS services.
    * WA Police publishes locality crime only through an interactive
      dashboard with no download, so Perth crime is left blank.

Note the two flood measures differ: Victoria = land that has flooded in
recorded events; WA = land inside the modelled 1-in-100-year floodplain.
Writes data/hazards.json. Network results are cached in .cache/hazards/.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache" / "hazards"
CACHE.mkdir(parents=True, exist_ok=True)
UA = "agent-reach-property-research/1.0 (personal, low-rate research)"
VIC_WFS = "https://opendata.maps.vic.gov.au/geoserver/wfs"
SLIP = "https://public-services.slip.wa.gov.au/public/rest/services/SLIP_Public_Services"
CRIME_XLSX = ROOT / "data" / "raw" / "vic_lga_criminal_incidents_jun2026.xlsx"


def get_json(url, key):
    f = CACHE / (re.sub(r"[^a-zA-Z0-9]+", "_", key)[:120] + ".json")
    if f.exists():
        return json.loads(f.read_text())
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode("utf-8"))
            f.write_text(json.dumps(data))
            time.sleep(0.8)
            return data
        except Exception as e:  # noqa: BLE001
            print(f"  retry {attempt + 1}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    return None


def wfs(type_name, cql=None, bbox=None):
    p = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": type_name,
         "outputFormat": "application/json", "srsName": "EPSG:4326"}
    if cql:
        p["CQL_FILTER"] = cql
    if bbox:  # this GeoServer takes lon,lat order here (tested: lat,lon returns nothing)
        p["bbox"] = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},EPSG:4326"
    return VIC_WFS + "?" + urllib.parse.urlencode(p)


def share(poly, feats):
    if not feats:
        return 0.0
    geoms = []
    for ft in feats:
        try:
            g = shape(ft["geometry"])
            if not g.is_valid:
                g = g.buffer(0)
            geoms.append(g)
        except Exception:  # noqa: BLE001
            pass
    if not geoms:
        return 0.0
    inter = unary_union(geoms).intersection(poly)
    return round(100 * inter.area / poly.area, 1)


def vic(name):
    d = get_json(wfs("open-data-platform:vmlite_locality_polygon", cql=f"locality_name='{name.upper()}'"), f"vic_loc_{name}")
    feats = [f for f in (d or {}).get("features", []) if f["properties"].get("state", "VIC") in ("VIC", None)]
    if not feats:
        return None
    poly = unary_union([shape(f["geometry"]).buffer(0) for f in feats])
    minx, miny, maxx, maxy = poly.bounds
    bb = (minx, miny, maxx, maxy)
    bpa = get_json(wfs("open-data-platform:bushfire_prone_area", bbox=bb), f"vic_bpa_{name}")
    fl = get_json(wfs("open-data-platform:vic_flood_history_public", bbox=bb), f"vic_flood_{name}")
    return {"bushfire_pct": share(poly, (bpa or {}).get("features", [])),
            "flood_pct": share(poly, (fl or {}).get("features", [])),
            "flood_measure": "Area flooded in recorded events (Vic Flood History)",
            "area_km2": round(poly.area * 111.32 * 111.32 * 0.81, 1)}


def slip_query(layer_path, params, key):
    base = {"f": "geojson", "outSR": "4326", "outFields": "objectid"}
    base.update(params)
    return get_json(f"{SLIP}/{layer_path}/query?" + urllib.parse.urlencode(base), key)


def wa(name):
    d = slip_query("Boundaries/MapServer/16", {"where": f"name='{name.upper()}'", "returnGeometry": "true"}, f"wa_loc_{name}")
    feats = (d or {}).get("features", [])
    if not feats:
        return None
    poly = unary_union([shape(f["geometry"]).buffer(0) for f in feats])
    minx, miny, maxx, maxy = poly.bounds
    env = {"geometry": f"{minx},{miny},{maxx},{maxy}", "geometryType": "esriGeometryEnvelope",
           "inSR": "4326", "spatialRel": "esriSpatialRelIntersects", "returnGeometry": "true"}
    bpa = slip_query("Bush_Fire_Prone_Areas/MapServer/23", env, f"wa_bpa_{name}")
    fl = slip_query("Water/MapServer/23", env, f"wa_flood_{name}")
    return {"bushfire_pct": share(poly, (bpa or {}).get("features", [])),
            "flood_pct": share(poly, (fl or {}).get("features", [])),
            "flood_measure": "Inside 1-in-100-year floodway/fringe (DWER)",
            "area_km2": round(poly.area * 111.32 * 111.32 * 0.85, 1)}


def vic_crime(suburbs):
    import openpyxl
    if not CRIME_XLSX.exists():
        print("  crime file missing; skipping", file=sys.stderr)
        return {}
    wb = openpyxl.load_workbook(CRIME_XLSX, read_only=True)
    ws = wb["Table 03"]
    want = {s.upper(): s for s in suburbs}
    tot = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] != 2026:
            continue
        nm = str(row[4] or "").strip().upper()
        if nm in want:
            tot[want[nm]] = tot.get(want[nm], 0) + (row[8] or 0)
    return tot


def population(name, state):
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower())
    f = ROOT / ".cache" / f"mb_{state}_{slug}.html"
    if not f.exists():
        f = ROOT / ".cache" / f"mb_{state}_{slug.replace('_', '-')}.html"
    if not f.exists():
        return None
    m = re.search(r"Population\s*(?:<[^>]+>\s*)*([\d,]+)\s*(?:<[^>]+>\s*)*ABS 2021", f.read_text(errors="ignore"))
    return int(m.group(1).replace(",", "")) if m else None


def main():
    rows = json.loads((ROOT / "data" / "suburbs.json").read_text())["suburbs"]
    mel = [r["suburb"] for r in rows if r["state"] == "VIC"]
    crime = vic_crime(mel)
    out = {}
    for r in rows:
        nm, st = r["suburb"], r["state"]
        print(f"{st} {nm}", file=sys.stderr)
        h = vic(nm) if st == "VIC" else wa(nm)
        h = h or {}
        pop = population(nm, st)
        h["population_2021"] = pop
        if st == "VIC" and nm in crime and pop:
            h["crime_incidents"] = crime[nm]
            h["crime_per_1000"] = round(1000 * crime[nm] / pop, 1)
        out[nm] = h
    vic_rates = sorted(v["crime_per_1000"] for v in out.values() if v.get("crime_per_1000"))
    (ROOT / "data" / "hazards.json").write_text(json.dumps(
        {"crime_period": "Year ending June 2026", "crime_source": "Crime Statistics Agency Victoria",
         "vic_median_crime_per_1000": vic_rates[len(vic_rates) // 2] if vic_rates else None,
         "suburbs": out}, indent=1))
    for k, v in out.items():
        print(f"{k:16s} bush {v.get('bushfire_pct')}% flood {v.get('flood_pct')}% crime/1k {v.get('crime_per_1000')} pop {v.get('population_2021')}")


if __name__ == "__main__":
    main()
