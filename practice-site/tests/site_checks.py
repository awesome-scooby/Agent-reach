"""Stage 4 checks: accessibility, reflow, keyboard, visitor journeys and draft safety.

Runs against a local or staging site with fictional data.
Usage: python3 -I tests/site_checks.py PATH_TO_axe.min.js
"""
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9400"
AXE = open(sys.argv[1]).read()
PAGES = ["/", "/fees/", "/meet/", "/services/", "/services/anxiety-and-stress/", "/services/low-mood/",
         "/services/life-changes/", "/how-sessions-work/", "/for-referrers/", "/contact/", "/privacy/",
         "/complaints/", "/accessibility/", "/?page_id=999999"]
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))


with sync_playwright() as p:
    b = p.chromium.launch()
    phone = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    pg = phone.new_page()

    # 1. Automated accessibility (WCAG 2.2 A/AA rules in axe), admin bar excluded.
    for path in PAGES:
        pg.goto(BASE + path, wait_until="networkidle")
        pg.add_script_tag(content=AXE)
        res = pg.evaluate("""async () => (await axe.run({exclude: [['#wpadminbar']]},
            {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})).violations
            .map(v => v.id + ' x' + v.nodes.length)""")
        check(f"axe WCAG A/AA on {path}", not res, ", ".join(res))

    # 2. Reflow: 320 CSS px wide is the WCAG equivalent of 1280px at 400% zoom.
    narrow = b.new_context(viewport={"width": 320, "height": 640})
    np_ = narrow.new_page()
    for path in PAGES:
        np_.goto(BASE + path, wait_until="domcontentloaded")
        sw = np_.evaluate("document.documentElement.scrollWidth")
        check(f"no sideways scroll at 320px on {path}", sw <= 320, f"scrollWidth {sw}")
    narrow.close()

    # 3. Keyboard: skip link first, visible focus ring.
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.evaluate("document.querySelector('#wpadminbar') && document.querySelector('#wpadminbar').remove()")
    pg.keyboard.press("Tab")
    first = pg.evaluate("document.activeElement.textContent.trim()")
    check("first Tab reaches the skip link", "Skip to content" in first, first)
    pg.keyboard.press("Tab")
    ring = pg.evaluate("getComputedStyle(document.activeElement).outlineStyle")
    check("focused link shows an outline", ring not in ("none", ""), ring)

    # 4. Journeys on a phone.
    pg.goto(BASE + "/", wait_until="networkidle")
    check("Home: booking button in one tap", pg.locator("main a.wp-block-button__link", has_text="Book an appointment").first.is_visible())
    pg.locator("main a[href$='/fees/']").first.click()
    pg.wait_for_load_state()
    check("Home -> Fees in one tap", "/fees/" in pg.url and "$[fee]" in pg.content())
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.locator("button.wp-block-navigation__responsive-container-open").click()
    pg.locator(".wp-block-navigation__responsive-container.is-menu-open a", has_text="For GPs").click()
    pg.wait_for_load_state()
    check("GP: menu -> referral instructions in two taps", "/for-referrers/" in pg.url and "How to refer" in pg.content())
    pg.goto(BASE + "/", wait_until="networkidle")
    check("GP: referral link also in footer", pg.locator("footer a[href$='/for-referrers/']").count() > 0)

    # 5. Drafts stay private: no room pages in navigation or on public pages.
    for path in PAGES[:10]:
        pg.goto(BASE + path, wait_until="domcontentloaded")
        html = pg.content()
        if "room" in html.lower() and ("perth room" in html.lower() or "melbourne room" in html.lower()):
            check(f"no draft room links on {path}", False)
            break
    else:
        check("no draft room links on public pages", True)
    # The local test site logs everyone in as admin, so ask the public REST API (without a nonce, WordPress treats the request as an anonymous visitor).
    for slug in ("melbourne-room", "perth-room"):
        public = pg.evaluate("async s => (await (await fetch('/wp-json/wp/v2/pages?slug=' + s)).json()).length", slug)
        check(f"draft {slug} invisible to the public", public == 0, f"{public} public result(s)")

    # 6. Search engines blocked on staging.
    pg.goto(BASE + "/", wait_until="domcontentloaded")
    robots = pg.locator("meta[name='robots']").get_attribute("content") or ""
    check("staging is noindex", "noindex" in robots, robots)
    b.close()

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
