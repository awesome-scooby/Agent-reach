"""Editing-contract checks on a local or staging site with fictional data.

1. Change the shared standard fee once -> Home, Fees and service pages all show it.
2. Pause intake by swapping the shared Booking action to the Closed version ->
   no booking button remains on Home, Fees, service pages or Contact.
3. Restore both, proving the change is reversible.

Usage: python3 -I tests/editing_contract.py [SCREENSHOT_DIR]
"""
import re, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9400"
PAGES = ["/", "/fees/", "/services/service-1/", "/services/service-2/", "/contact/"]
FEE_PAGES = PAGES[:4]
TEST_FEE = "$987 (test value)"
shots = sys.argv[1] if len(sys.argv) > 1 else None
results = []

def check(name, ok, detail=""):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    pg.goto(BASE + "/wp-admin/", wait_until="domcontentloaded")
    nonce = pg.evaluate("window.wpApiSettings && wpApiSettings.nonce")
    api = lambda method, path, data=None: pg.evaluate(
        """async ([m, u, d, n]) => { const r = await fetch(u, {method: m, headers: {'X-WP-Nonce': n, 'Content-Type': 'application/json'}, body: d ? JSON.stringify(d) : undefined}); return await r.json(); }""",
        [method, BASE + "/wp-json/wp/v2/" + path, data, nonce])

    blocks = {blk["slug"]: blk for blk in api("GET", "blocks?per_page=50&context=edit")}
    fee, booking = blocks["fee-standard-session"], blocks["booking-action"]
    fee_orig, booking_orig = fee["content"]["raw"], booking["content"]["raw"]

    # 1. Fee changed once.
    api("POST", f"blocks/{fee['id']}", {"content": fee_orig.replace("$[fee]", TEST_FEE, 1)})
    for path in FEE_PAGES:
        pg.goto(BASE + path, wait_until="domcontentloaded")
        check(f"fee shows on {path}", TEST_FEE in pg.content())
    if shots:
        pg.goto(BASE + "/", wait_until="networkidle"); pg.add_style_tag(content="#wpadminbar{display:none!important}html{margin-top:0!important}")
        pg.screenshot(path=f"{shots}/demo-fee-changed-phone.png")

    # 2. Intake paused.
    pg.goto(BASE + "/wp-admin/", wait_until="domcontentloaded")
    closed = api("GET", "block-patterns/patterns")
    closed = next(x["content"] for x in closed if x["name"] == "practice/booking-closed")
    api("POST", f"blocks/{booking['id']}", {"content": closed})
    for path in PAGES:
        pg.goto(BASE + path, wait_until="domcontentloaded")
        html = pg.content()
        check(f"paused state on {path}", "Not taking new clients right now" in html)
        check(f"no booking button on {path}", re.search(r">\s*Book an appointment\s*<", html) is None)
    if shots:
        pg.goto(BASE + "/", wait_until="networkidle"); pg.add_style_tag(content="#wpadminbar{display:none!important}html{margin-top:0!important}")
        pg.screenshot(path=f"{shots}/demo-paused-phone.png")

    # 3. Restore.
    pg.goto(BASE + "/wp-admin/", wait_until="domcontentloaded")
    api("POST", f"blocks/{fee['id']}", {"content": fee_orig})
    api("POST", f"blocks/{booking['id']}", {"content": booking_orig})
    pg.goto(BASE + "/", wait_until="domcontentloaded")
    html = pg.content()
    check("restored fee placeholder", "$[fee]" in html and TEST_FEE not in html)
    check("restored booking button", "Book an appointment" in html)
    revs = api("GET", f"blocks/{fee['id']}/revisions")
    check("shared fee block keeps revisions", isinstance(revs, list) and len(revs) > 0, f"{len(revs) if isinstance(revs, list) else revs.get('code')} revisions")
    b.close()

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
