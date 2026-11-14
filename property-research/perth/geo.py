#!/usr/bin/env python3
"""Simplified locality outlines for the dashboard map (from the cached
LGATE-234 query made by universe.py). Douglas-Peucker in EPSG:7850 at 60 m,
written as lon/lat rounded to 4 dp. Display only; never used for analysis."""
import json
import warnings
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

warnings.filterwarnings("ignore", category=DeprecationWarning)
HERE = Path(__file__).resolve().parent
CACHE = HERE.parent / ".cache" / "hazards" / "perth_univ_localities_v1.json"
fw = Transformer.from_crs(4326, 7850, always_xy=True).transform
bw = Transformer.from_crs(7850, 4326, always_xy=True).transform


def rnd(c):
    if isinstance(c[0], (int, float)):
        return [round(c[0], 4), round(c[1], 4)]
    return [rnd(x) for x in c]


def main():
    uni = json.loads((HERE / "data" / "universe.json").read_text())["rows"]
    keep = {r["suburb"].upper(): r for r in uni if r["km"] <= 42 and r["south"]}
    feats = json.loads(CACHE.read_text())["features"]
    groups = {}
    for f in feats:
        nm = f["properties"]["name"]
        if nm in keep:
            groups.setdefault(nm, []).append(shape(f["geometry"]).buffer(0))
    out = []
    for nm, gs in groups.items():
        g = transform(bw, transform(fw, unary_union(gs)).simplify(60))
        out.append({"n": keep[nm]["suburb"], "inc": keep[nm]["included"], "g": rnd(mapping(g)["coordinates"]), "t": mapping(g)["type"]})
    (HERE / "data" / "geo.json").write_text(json.dumps(out, separators=(",", ":")))
    print(len(out), (HERE / "data" / "geo.json").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
