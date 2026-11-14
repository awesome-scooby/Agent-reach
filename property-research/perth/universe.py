#!/usr/bin/env python3
"""Southern-Perth suburb universe from official Landgate locality polygons.

Source   : Landgate Localities (LGATE-234) and LGA boundaries (LGATE-233),
           SLIP public ArcGIS MapServer (Boundaries layers 16 and 14).
           Native CRS GDA2020 geographic (WKID 7844); requested as GeoJSON 4326.
CBD point: Perth GPO, Forrest Place: -31.95224, 115.85868 (WGS84/GDA2020;
           sub-metre datum difference is irrelevant at km scale).
Method   : 1. Reproject every polygon to GDA2020 / MGA zone 50 (EPSG:7850),
              an equal-distance-friendly transverse Mercator suited to Perth.
           2. Centre = area centroid of the (multi)polygon in EPSG:7850.
              If the centroid falls outside its own polygon we flag it.
           3. Distance = straight-line metres from centre to CBD point.
           4. "Southern" = centre northing strictly south of the CBD northing
              (i.e. bearing from the CBD between 90 and 270 degrees).
           5. River rule (user decision 14 Nov 2026): the locality must also lie
              south/east of the Swan River. Implemented by Landgate LGA
              membership: LGAs wholly north/west of the river are excluded,
              plus North Fremantle (City of Fremantle, north bank).
           6. Included = southern AND south of the river AND distance <= 35.0 km.
           LGA = the LGA polygon that contains the locality centre.
Writes   : perth/data/universe.json (all candidates with include flag + reason)
"""
import json
import sys
import urllib.parse
from datetime import date
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Point, shape
import warnings
from shapely.ops import transform, unary_union
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from hazards import SLIP, get_json  # noqa: E402  (reuse cached, rate-limited fetch)

CBD = (115.85868, -31.95224)
MAX_KM = 35.0
EPSG = 7850
# Envelope generously wider than 35 km around the CBD (lon/lat).
ENV = (115.40, -32.40, 116.35, -31.70)
OUT = HERE / "data" / "universe.json"
NORTH_OF_RIVER_LGAS = {"Perth, City Of", "Nedlands, City Of", "Claremont, Town Of", "Cottesloe, Town Of",
                       "Mosman Park, Town Of", "Peppermint Grove, Shire Of", "Subiaco, City Of",
                       "Cambridge, Town Of", "Vincent, City Of", "Bayswater, City Of", "Stirling, City Of",
                       "Bassendean, Town Of", "Swan, City Of", "Mundaring, Shire Of"}
NORTH_OF_RIVER_LOCALITIES = {"North Fremantle"}
CORRIDOR = {"Canning, City Of": "South-East", "Gosnells, City Of": "South-East", "Armadale, City Of": "South-East",
            "Serpentine-Jarrahdale, Shire Of": "South-East", "Kalamunda, City Of": "Hills / East",
            "Belmont, City Of": "Inner South", "Victoria Park, Town Of": "Inner South",
            "South Perth, City Of": "Inner South", "Melville, City Of": "Inner South-West",
            "Fremantle, City Of": "Inner South-West", "East Fremantle, Town Of": "Inner South-West",
            "Cockburn, City Of": "South-West", "Kwinana, City Of": "South-West", "Rockingham, City Of": "South-West"}


def ring(km):
    return "Inner" if km < 12 else ("Middle" if km < 22 else "Outer")

to_mga = Transformer.from_crs(4326, EPSG, always_xy=True).transform


def fetch(layer, fields, key):
    p = {"f": "geojson", "outSR": "4326", "outFields": fields, "returnGeometry": "true",
         "geometry": ",".join(map(str, ENV)), "geometryType": "esriGeometryEnvelope", "inSR": "4326",
         "spatialRel": "esriSpatialRelIntersects", "where": "1=1"}
    url = f"{SLIP}/Boundaries/MapServer/{layer}/query?" + urllib.parse.urlencode(p)
    d = get_json(url, key)
    if not d or "features" not in d:
        # hazards.get_json caches whatever came back; drop an error body so a retry refetches
        import re as _re
        bad = Path(__file__).resolve().parent.parent / ".cache" / "hazards" / (_re.sub(r"[^a-zA-Z0-9]+", "_", key)[:120] + ".json")
        bad.unlink(missing_ok=True)
        raise SystemExit(f"SLIP layer {layer} failed; keeping last-known-good {OUT.name}")
    return d["features"]


def main():
    locs = fetch(16, "name,postcode,abs_lga_number,land_area", "perth_univ_localities_v1")
    lgas = fetch(14, "name", "perth_univ_lgas_v2")
    lga_polys = []
    for f in lgas:
        g = transform(to_mga, shape(f["geometry"]).buffer(0))
        lga_polys.append((f["properties"].get("name", "").title(), g))
    cx, cy = to_mga(*CBD)
    by_name = {}
    for f in locs:
        nm = f["properties"]["name"]
        by_name.setdefault(nm, []).append(f)
    rows = []
    for nm, fs in sorted(by_name.items()):
        poly = unary_union([transform(to_mga, shape(f["geometry"]).buffer(0)) for f in fs])
        c = poly.centroid
        inside = poly.contains(c)
        dist = c.distance(Point(cx, cy)) / 1000
        south = c.y < cy
        lga = next((n for n, g in lga_polys if g.contains(c)), None) or \
            next((n for n, g in lga_polys if g.intersects(poly)), None)
        lon, lat = Transformer.from_crs(EPSG, 4326, always_xy=True).transform(c.x, c.y)
        if dist > 60:
            continue
        if not south:
            reason, inc = "Centre north of CBD latitude", False
        elif lga in NORTH_OF_RIVER_LGAS or nm.title() in NORTH_OF_RIVER_LOCALITIES:
            reason, inc = "North/west of the Swan River", False
        elif dist > MAX_KM:
            reason, inc = f"Centre {dist:.1f} km from CBD (> {MAX_KM:.0f} km)", False
        else:
            reason, inc = "South of CBD and centre within 35 km", True
        p0 = fs[0]["properties"]
        rows.append({"suburb": nm.title(), "postcode": p0.get("postcode"), "lga": lga,
                     "km": round(dist, 2), "lat": round(lat, 5), "lon": round(lon, 5),
                     "area_km2": round(poly.area / 1e6, 2), "corridor": CORRIDOR.get(lga, "Other"), "ring": ring(dist), "centroid_inside": inside,
                     "south": south, "included": inc, "reason": reason})
    meta = {"generated": date.today().isoformat(), "source": "Landgate LGATE-234 Localities; LGATE-233 LGAs via SLIP",
            "source_url": f"{SLIP}/Boundaries/MapServer/16", "source_crs": "GDA2020 (WKID 7844)",
            "projected_crs": "GDA2020 / MGA zone 50 (EPSG:7850)", "cbd_point": {"name": "Perth GPO, Forrest Place", "lon": CBD[0], "lat": CBD[1]},
            "rule": "Locality area-centroid (EPSG:7850) south of CBD northing, south/east of the Swan River (by LGA), and <= 35.0 km straight-line",
            "publication_note": "SLIP layer is updated continuously; no single publication date is exposed by the service. Retrieval date recorded as 'generated'."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"meta": meta, "rows": rows}, indent=1))
    inc = [r for r in rows if r["included"]]
    print(f"{len(rows)} candidates within 60 km, {len(inc)} included", file=sys.stderr)


if __name__ == "__main__":
    main()
