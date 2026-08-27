#!/usr/bin/env python3
"""Serve a page from this repo the way the Artifact runtime would render it.

The pages here are Artifact bodies: they have no `<!doctype>`, `<html>`, `<head>`
or `<body>` of their own, because the publisher wraps them at publish time. This
wraps a page the same way — including the minimal CSS reset and the theme
attribute — so what you see locally matches what a viewer sees.

Usage:
    python3 scripts/preview.py                          # first page at the repo root
    python3 scripts/preview.py page.html --theme dark   # force a theme
    python3 scripts/preview.py --port 8080 --no-serve   # just write the wrapped file
"""

from __future__ import annotations

import argparse
import functools
import http.server
import pathlib
import socketserver
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / ".preview"

SKELETON = """<!doctype html>
<html lang="en"{theme_attribute}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *,*::before,*::after{{box-sizing:border-box}}
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0}}
  img,svg,video{{max-width:100%;height:auto}}
</style>
</head>
<body>
{page}
</body>
</html>
"""


def build(path: pathlib.Path, theme: str) -> pathlib.Path:
    theme_attribute = "" if theme == "system" else f' data-theme="{theme}"'
    BUILD_DIR.mkdir(exist_ok=True)
    output = BUILD_DIR / "index.html"
    output.write_text(
        SKELETON.format(theme_attribute=theme_attribute, page=path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", type=pathlib.Path)
    parser.add_argument("--theme", choices=("system", "light", "dark"), default="system")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-serve", action="store_true", help="write the wrapped file and exit")
    args = parser.parse_args()

    page = args.page
    if page is None:
        pages = sorted(REPO_ROOT.glob("*.html"))
        if not pages:
            print("no HTML pages found at the repo root", file=sys.stderr)
            return 1
        page = pages[0]
    if not page.exists():
        print(f"{page}: file not found", file=sys.stderr)
        return 1

    output = build(page, args.theme)
    print(f"wrapped {page.name} ({args.theme} theme) -> {output.relative_to(REPO_ROOT)}")
    if args.no_serve:
        return 0

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(BUILD_DIR))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as server:
        print(f"serving at http://127.0.0.1:{args.port}/  (ctrl-c to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
