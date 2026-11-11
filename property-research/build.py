#!/usr/bin/env python3
"""Merge data files into template.html -> ../melbourne-perth-600k-shortlist.html"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = ROOT / "data"


def load(name, default):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else default


data = load("model.json", {})
data["news"] = load("news.json", {"items": []})
data["changes"] = load("changes.json", {"changes": [], "alerts": []})
data["listings"] = load("listings.json", {"status": "no_key"})
data["rates"] = load("rates.json", {})
tpl = (ROOT / "template.html").read_text()
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
out = ROOT.parent / "melbourne-perth-600k-shortlist.html"
out.write_text(tpl.replace("/*__DATA__*/{}", blob))
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
