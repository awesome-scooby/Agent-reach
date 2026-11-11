#!/usr/bin/env python3
"""Inject data/model.json into template.html -> ../melbourne-perth-600k-shortlist.html"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
tpl = (ROOT / "template.html").read_text()
data = (ROOT / "data" / "model.json").read_text().replace("</", "<\\/")
out = ROOT.parent / "melbourne-perth-600k-shortlist.html"
out.write_text(tpl.replace("/*__DATA__*/{}", data))
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
