#!/usr/bin/env bash
# Perth daily refresh (06:59 Australia/Perth). Isolated from the Melbourne
# pipeline: writes only perth/data/* and ../perth-southern-buyer-dashboard.html.
set -euo pipefail
cd "$(dirname "$0")"
exec 9>data/.run.lock
flock -n 9 || { echo "another Perth refresh is running"; exit 1; }
pip install -q shapely pyproj >/dev/null 2>&1 || true
rm -f ../.cache/reiwa_*.html ../.cache/mb_WA_*.html ../.cache/spi_WA_*.html
python3 collect_perth.py || echo "collection incomplete: model uses last-known-good suburbs_raw.json (its date is shown on the page)"
if [ "$(date +%d)" = "01" ]; then python3 universe.py && python3 hazards_perth.py && python3 geo.py; fi
python3 model_perth.py
python3 daily_perth.py
python3 build_perth.py
