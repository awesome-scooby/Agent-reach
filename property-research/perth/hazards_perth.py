#!/usr/bin/env python3
"""Bushfire-prone and 1% AEP flood share for every included locality,
reusing hazards.wa() (Landgate LGATE-234, OBRM-026, DWER-014 via SLIP).
Adds land-use screening flags from a documented hand list (NOT measured).
Writes perth/data/hazards.json atomically; failures are recorded, not hidden."""
import json
import os
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hazards  # noqa: E402

OUT = HERE / "data" / "hazards.json"
# Screening flags from known land uses (planning schemes / airport ANEF maps).
# Hand-maintained; property-level checks still required.
FLAGS = {
    "Kwinana Strategic Industrial Area nearby (heavy industry, buffer zones)": [
        "Naval Base", "Kwinana Beach", "Hope Valley", "Wattleup", "Postans", "Mandogalup", "Medina", "Calista", "Orelia", "Parmelia", "Leda"],
    "Perth Airport flight path / noise exposure possible (check ANEF)": [
        "Kewdale", "Cloverdale", "Forrestfield", "Redcliffe", "Wattle Grove", "Maida Vale", "Belmont"],
    "Jandakot Airport noise exposure possible (check ANEF)": [
        "Jandakot", "Banjup", "Atwell", "Aubin Grove", "Success", "Hammond Park", "Treeby", "Harrisdale", "Piara Waters", "Canning Vale"],
    "Industrial adjacency (Welshpool/Kewdale/Maddington/Canning Vale industrial)": [
        "Welshpool", "Kewdale", "Maddington", "Kenwick", "Canning Vale", "Bibra Lake", "O'Connor", "Forrestdale", "Henderson"],
    "Freight rail / major road corridor through suburb (Kwinana freight line, Roe/Tonkin/Kwinana Fwy)": [
        "Spearwood", "Hamilton Hill", "Coogee", "Munster", "Wattleup", "Kewdale", "Cannington", "Kenwick", "Maddington", "Gosnells", "Kelmscott"],
    "No freehold residential market (defence / island reserve / industrial)": [
        "Garden Island", "Rottnest Island", "Naval Base", "Kwinana Beach", "Welshpool", "Doobarda"],
}


def main():
    uni = [r for r in json.loads((HERE / "data" / "universe.json").read_text())["rows"] if r["included"]]
    out, failed = {}, []
    for i, u in enumerate(uni, 1):
        nm = u["suburb"]
        print(f"[{i}/{len(uni)}] {nm}", file=sys.stderr)
        try:
            h = hazards.wa(nm.replace("'", "''")) or {}  # SQL-escape apostrophes (O'Connor)
        except Exception as e:  # noqa: BLE001
            h = {}
            failed.append(f"{nm}: {e}")
        if not h:
            failed.append(nm)
        h["flags"] = [k for k, v in FLAGS.items() if nm in v]
        out[nm] = h
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps({"generated": date.today().isoformat(),
                               "sources": {"bushfire": "OBRM-026 Bush Fire Prone Areas (SLIP)", "flood": "DWER-014 1-in-100 floodway/fringe (SLIP)",
                                           "boundaries": "LGATE-234"},
                               "flags_note": "Land-use flags are a hand-maintained screening list, not measured exposure.",
                               "failed": failed, "suburbs": out}, indent=1))
    os.replace(tmp, OUT)
    print(f"done; {len(failed)} failed", file=sys.stderr)


if __name__ == "__main__":
    main()
