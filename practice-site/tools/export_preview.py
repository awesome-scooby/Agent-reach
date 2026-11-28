"""Export the running local site as a static, clickable draft preview.

Fetches each public page as a logged-out visitor, downloads its CSS, fonts and
images, rewrites links to flat .html files, swaps WordPress's menu script for a
tiny local one, and adds a "draft preview" bar. The output is for review only;
the real site stays in WordPress.

Usage: python3 -I tools/export_preview.py OUT_DIR
"""
import os, re, sys, urllib.parse, urllib.request

BASE = "http://127.0.0.1:9400"
OUT = sys.argv[1]
PAGES = {
    "/": "home.html", "/meet/": "meet.html", "/services/": "services.html",
    "/services/anxiety-and-stress/": "service-anxiety.html", "/services/low-mood/": "service-low-mood.html",
    "/services/life-changes/": "service-life-changes.html", "/fees/": "fees.html",
    "/how-sessions-work/": "how-sessions-work.html", "/for-referrers/": "for-referrers.html",
    "/questions/": "questions.html", "/contact/": "contact.html", "/privacy/": "privacy.html",
    "/complaints/": "complaints.html", "/accessibility/": "accessibility.html", "/?page_id=999999": "404.html",
}
fetched = set()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "preview-export"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.read()
    except urllib.error.HTTPError as e:  # the 404 page is still a page
        return e.read()


def local_path(url_path):
    return urllib.parse.urlsplit(url_path).path.lstrip("/")


def save_asset(url_path):
    path = local_path(url_path)
    if not path or path in fetched:
        return path
    fetched.add(path)
    data = get(BASE + "/" + path + ("?" + urllib.parse.urlsplit(url_path).query if "?" in url_path else ""))
    dest = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if path.endswith(".css"):
        css = data.decode("utf-8", "replace")
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css):
            if ref.startswith(("data:", "#", "http")) and not ref.startswith(BASE):
                continue
            target = urllib.parse.urljoin("/" + path, ref.replace(BASE, ""))
            save_asset(target)
        data = css.replace(BASE + "/", "/" * 0 + _rel_prefix(path)).encode()
    with open(dest, "wb") as f:
        f.write(data)
    return path


def _rel_prefix(path):
    return "../" * path.count("/")


def page_link(m):
    url = m.group(2)
    path, _, frag = url.replace(BASE, "").partition("#")
    path = path or "/"
    if path in PAGES:
        return m.group(1) + PAGES[path] + ("#" + frag if frag else "") + m.group(3)
    return m.group(0)


EXTRA = """
<style>
.pv-bar{position:relative;z-index:100;background:#1d1d1f;color:#f5f5f7;font:500 14px/1.4 Inter,system-ui,sans-serif;padding:8px max(16px,5vw);display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center}
.pv-bar a,.pv-bar button{color:#f5f5f7;font:inherit;background:none;border:1px solid #6e6e73;border-radius:999px;padding:4px 12px;cursor:pointer;text-decoration:none}
.pv-bar a:focus-visible,.pv-bar button:focus-visible{outline:3px solid #e7b065;outline-offset:2px}
.pv-hide-draft .practice-draft{display:none!important}
.pv-toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#1d1d1f;color:#fff;padding:12px 18px;border-radius:12px;font:15px/1.4 Inter,system-ui,sans-serif;z-index:200;max-width:calc(100% - 32px)}
</style>
<div class="pv-bar" role="region" aria-label="Draft preview controls"><span>Draft preview, not public. Text in [brackets] is a placeholder.</span><button type="button" id="pv-drafts" aria-pressed="false">Hide draft labels</button><a href="index.html">All pages</a></div>
"""

SCRIPT = """
<script>
{
  const root = document.documentElement, btn = document.getElementById('pv-drafts');
  const set = on => { root.classList.toggle('pv-hide-draft', on); btn.setAttribute('aria-pressed', on); btn.textContent = on ? 'Show draft labels' : 'Hide draft labels'; try { localStorage.setItem('pvHide', on ? '1' : ''); } catch (e) {} };
  let saved = false; try { saved = localStorage.getItem('pvHide') === '1'; } catch (e) {}
  set(saved); btn.addEventListener('click', () => set(!root.classList.contains('pv-hide-draft')));
  const nav = document.querySelector('.wp-block-navigation__responsive-container');
  const open = document.querySelector('.wp-block-navigation__responsive-container-open');
  const close = document.querySelector('.wp-block-navigation__responsive-container-close');
  const toggle = on => { if (!nav) return; nav.classList.toggle('is-menu-open', on); nav.classList.toggle('has-modal-open', on); root.classList.toggle('has-modal-open', on); if (on && close) close.focus(); if (!on && open) open.focus(); };
  open && open.addEventListener('click', () => toggle(true));
  close && close.addEventListener('click', () => toggle(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href*="example.invalid"]');
    if (!a) return;
    e.preventDefault();
    const t = document.createElement('div'); t.className = 'pv-toast'; t.setAttribute('role', 'status');
    t.textContent = 'On the live site this opens the booking system. Not connected in the draft.';
    document.body.appendChild(t); setTimeout(() => t.remove(), 3500);
  });
}
</script>
"""

os.makedirs(OUT, exist_ok=True)
for path, name in PAGES.items():
    html = get(BASE + path).decode("utf-8", "replace")
    # Drop WordPress module scripts (menu interactivity) and server-only links.
    html = re.sub(r"<script\b[^>]*type=[\"']importmap[\"'][^>]*>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<script id=\"wp-emoji-settings\"[^>]*>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<script\b[^>]*type=[\"'](?:module|speculationrules)[\"'][^>]*>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<link rel=\"modulepreload\"[^>]*>", "", html)
    html = re.sub(r"<link rel=['\"](?:alternate|EditURI|https://api\.w\.org/|shortlink|canonical|wlwmanifest|dns-prefetch)['\"][^>]*>", "", html)
    html = re.sub(r"<script[^>]*src=['\"][^'\"]*(?:wp-emoji|interactivity)[^'\"]*['\"][^>]*></script>", "", html)
    # Assets: stylesheets, scripts, images, fonts in inline styles.
    for ref in set(re.findall(r"(?:" + re.escape(BASE) + r")?(/wp-(?:content|includes)/[^\s'\")]+)", html)):
        if "*" in ref:
            continue
        save_asset(ref)
        html = html.replace(BASE + ref, local_path(ref)).replace(ref, local_path(ref))
    # Page links.
    html = re.sub(r"(href=[\"'])((?:" + re.escape(BASE) + r")?/[^\"']*)([\"'])", page_link, html)
    html = html.replace(BASE + "/", "home.html").replace(BASE, "home.html")
    html = re.sub(r"(<body[^>]*>)", r"\1" + EXTRA, html, count=1)
    html = html.replace("</body>", SCRIPT + "</body>")
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)
    print("page", name)

leftover = [n for n in PAGES.values() if "127.0.0.1" in open(os.path.join(OUT, n)).read()]
print("assets", len(fetched), "| pages still pointing at the local server:", leftover or "none")
