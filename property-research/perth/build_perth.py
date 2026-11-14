#!/usr/bin/env python3
"""Merge Perth data + finance.js into perth/template.html ->
../../perth-southern-buyer-dashboard.html. Never touches the Melbourne page."""
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
OUT = HERE.parent.parent / "perth-southern-buyer-dashboard.html"


def load(n, default):
    p = D / n
    return json.loads(p.read_text()) if p.exists() else default


def main():
    data = load("model.json", {})
    if not data.get("suburbs"):
        raise SystemExit("model.json missing or empty; refusing to build a page without data")
    data["geo"] = load("geo.json", [])
    data["projects"] = load("projects_perth.json", {"projects": []})
    data["changes"] = load("changes.json", {"alerts": [], "changes": [], "signals": []})
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    data["build"] = hashlib.sha1(blob.encode()).hexdigest()[:10]
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    tpl = (HERE / "template.html").read_text()
    fin = (HERE / "finance.js").read_text()
    html = tpl.replace("/*__DATA__*/{}", blob).replace("/*__FINANCE__*/", fin)
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(html)
    os.replace(tmp, OUT)
    print(f"wrote {OUT.name} ({OUT.stat().st_size // 1024} KB, build {data['build']})")


if __name__ == "__main__":
    main()
