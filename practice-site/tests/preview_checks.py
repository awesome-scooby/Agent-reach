"""Check the exported static draft preview opens and works offline.

Usage: python3 -I tests/preview_checks.py PREVIEW_DIR
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

base = pathlib.Path(sys.argv[1]).resolve().as_uri() + "/"
ok = []


def check(name, cond, detail=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail else ""))


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
    errs = []
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("requestfailed", lambda r: errs.append("failed " + r.url))
    pg.goto(base + "home.html", wait_until="load")
    pg.click("button.wp-block-navigation__responsive-container-open")
    check("phone menu opens", pg.locator(".wp-block-navigation__responsive-container.is-menu-open").count() == 1)
    pg.locator(".is-menu-open a", has_text="For GPs").click()
    pg.wait_for_load_state()
    check("menu link opens For GPs", pg.url.endswith("for-referrers.html"))
    pg.goto(base + "fees.html")
    before = pg.locator(".practice-draft:visible").count()
    pg.click("#pv-drafts")
    check("draft labels can be hidden", before > 0 and pg.locator(".practice-draft:visible").count() == 0, f"{before} -> 0")
    pg.goto(base + "home.html")
    pg.locator("main a.wp-block-button__link").first.click()
    pg.wait_for_timeout(300)
    check("booking button shows a 'not connected' note", pg.locator(".pv-toast").count() == 1)
    check("Inter font loads", pg.evaluate("document.fonts.ready.then(() => document.fonts.check('16px Inter'))"))
    pg.evaluate("window.scrollTo(0, 1500)")
    top = pg.evaluate("Math.round(document.querySelector('.practice-header').getBoundingClientRect().top)")
    check("header stays at the top while scrolling", top == 0, f"top {top}")
    check("no console errors or missing files", not errs, "; ".join(errs[:3]))
    b.close()

print(f"\n{sum(ok)}/{len(ok)} passed")
sys.exit(0 if all(ok) else 1)
