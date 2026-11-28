"""Capture phone and desktop screenshots of Home and Fees for design review.
Usage: python3 -I tests/screens.py OUT_DIR [label]"""
import sys
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:9400"
out, label = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "a")
PAGES = [("/", "home"), ("/fees/", "fees"), ("/meet/", "meet"), ("/services/anxiety-and-stress/", "service"), ("/how-sessions-work/", "telehealth"), ("/for-referrers/", "referrers"), ("/contact/", "contact"), ("/?page_id=999999", "404")]
HIDE_ADMIN = "#wpadminbar{display:none!important} html{margin-top:0!important}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp, scale in (("phone", {"width": 390, "height": 844}, 2), ("desktop", {"width": 1280, "height": 900}, 1)):
        ctx = b.new_context(viewport=vp, device_scale_factor=scale)
        pg = ctx.new_page()
        for path, slug in PAGES:
            pg.goto(BASE + path, wait_until="networkidle")
            pg.add_style_tag(content=HIDE_ADMIN)
            pg.wait_for_timeout(300)
            pg.screenshot(path=f"{out}/{label}-{slug}-{name}.png", full_page=True)
        ctx.close()
    b.close()
print("done")
