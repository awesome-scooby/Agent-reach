#!/usr/bin/env python3
"""Validate the self-contained HTML pages in this repo.

Every page here is an Artifact body: it is published by wrapping it in a
`<!doctype html><head>...</head><body>` skeleton, it must load nothing from the
network, and it must render correctly in light, dark, and system themes.

Usage:
    python3 scripts/check_html.py                # check every *.html at the repo root
    python3 scripts/check_html.py page.html ...  # check specific files
    python3 scripts/check_html.py --quiet        # only print failures

Exit code is 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from html.parser import HTMLParser

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# The Artifact runtime supplies the document skeleton, so the page must not.
SKELETON_TAGS = ("html", "head", "body")

# A strict CSP blocks every remote host except Google Fonts.
ALLOWED_ASSET_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")

# Elements that never carry a closing tag.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}

MAX_BYTES = 16 * 1024 * 1024  # published pages must be 16MB or smaller
TITLE_SCAN_BYTES = 8 * 1024  # only the first 8KB is scanned for <title>


class PageParser(HTMLParser):
    """Collects the structural facts the checks below need."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[tuple[str, int]] = []
        self.unbalanced: list[str] = []
        self.styles: list[str] = []
        self.remote_assets: list[str] = []
        self.saw_title = False
        self.skeleton_tags: list[str] = []
        self._in_style = False

    # -- structure ---------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        if tag in SKELETON_TAGS:
            self.skeleton_tags.append(f"line {self.getpos()[0]}: <{tag}>")
        if tag == "title":
            self.saw_title = True
        if tag == "style":
            self._in_style = True
        if tag not in VOID_TAGS:
            self.stack.append((tag, self.getpos()[0]))
        self._check_assets(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._check_assets(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
        if tag in VOID_TAGS:
            return
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                for orphan, line in self.stack[index + 1:]:
                    self.unbalanced.append(
                        f"line {line}: <{orphan}> is never closed "
                        f"(closed by </{tag}> on line {self.getpos()[0]})"
                    )
                del self.stack[index:]
                return
        self.unbalanced.append(f"line {self.getpos()[0]}: stray </{tag}>")

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)

    # -- assets ------------------------------------------------------------
    def _check_assets(self, tag, attrs):
        attrs = {name: (value or "") for name, value in attrs}
        # An <a href> points somewhere the reader clicks; it loads nothing.
        candidates = []
        if tag == "link" and "stylesheet" in attrs.get("rel", "").lower():
            candidates.append(attrs.get("href", ""))
        if tag in ("script", "img", "audio", "video", "iframe", "embed", "source", "track"):
            candidates.append(attrs.get("src", ""))
        if tag == "object":
            candidates.append(attrs.get("data", ""))
        for url in candidates:
            if _is_remote(url):
                self.remote_assets.append(f"line {self.getpos()[0]}: <{tag}> loads {url}")


def _is_remote(url: str) -> bool:
    url = url.strip()
    if not url or url.startswith(("data:", "blob:", "#")):
        return False
    match = re.match(r"^(?:https?:)?//([^/]+)", url)
    if not match:
        return False
    return match.group(1).lower() not in ALLOWED_ASSET_HOSTS


def _strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def _selector_blocks(css: str) -> list[tuple[str, str]]:
    """Return (selector, body) pairs for top-level-ish rules, at-rules included."""
    blocks: list[tuple[str, str]] = []
    depth = 0
    start = 0
    selector_start = 0
    for index, char in enumerate(css):
        if char == "{":
            if depth == 0:
                selector_start = start
                block_start = index + 1
                selector = css[selector_start:index].strip()
            depth += 1
            if depth == 1:
                pending = (selector, block_start)
        elif char == "}":
            depth -= 1
            if depth == 0:
                blocks.append((pending[0], css[pending[1]:index]))
                start = index + 1
    return blocks


def _root_declarations(css: str) -> dict[str, set[str]]:
    """Map a scope label to the custom properties declared for :root in it."""
    scopes: dict[str, set[str]] = {"light": set(), "dark-media": set(), "dark-attr": set()}
    for selector, body in _selector_blocks(css):
        if selector.startswith("@media"):
            is_dark_query = "prefers-color-scheme" in selector and "dark" in selector
            for inner_selector, inner_body in _selector_blocks(body):
                if ":root" not in inner_selector:
                    continue
                label = "dark-media" if is_dark_query else "light"
                scopes[label] |= _custom_props(inner_body)
            continue
        if ":root" not in selector:
            continue
        if 'data-theme="dark"' in selector:
            scopes["dark-attr"] |= _custom_props(body)
        elif 'data-theme="light"' in selector:
            scopes["light"] |= _custom_props(body)
        else:
            scopes["light"] |= _custom_props(body)
    return scopes


def _custom_props(body: str) -> set[str]:
    return set(re.findall(r"(--[A-Za-z0-9_-]+)\s*:", body))


def check_page(path: pathlib.Path) -> list[str]:
    """Return a list of problems found in one page; empty means it passes."""
    problems: list[str] = []
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")

    if len(raw) > MAX_BYTES:
        problems.append(f"file is {len(raw) / 1024 / 1024:.1f}MB; the 16MB publish limit is exceeded")

    parser = PageParser()
    parser.feed(text)
    parser.close()

    problems.extend(
        f"document skeleton tag must not appear in an Artifact body — {location}"
        for location in parser.skeleton_tags
    )
    problems.extend(f"remote asset blocked by the Artifact CSP — {ref}" for ref in parser.remote_assets)
    problems.extend(f"unbalanced markup — {issue}" for issue in parser.unbalanced)
    problems.extend(
        f"unbalanced markup — line {line}: <{tag}> is never closed"
        for tag, line in parser.stack
    )

    if not parser.saw_title:
        problems.append("no <title>; the artifact needs one for its tab and gallery name")
    elif text.encode("utf-8").find(b"<title") > TITLE_SCAN_BYTES:
        problems.append("<title> sits past the first 8KB, where the publisher stops scanning for it")

    css = _strip_css_comments("\n".join(parser.styles))
    if not css.strip():
        problems.append("no <style> block found; the page carries no styling of its own")
        return problems

    scopes = _root_declarations(css)
    if not scopes["light"]:
        problems.append("no bare `:root` block; the light palette must be defined unconditionally")
    if not scopes["dark-media"]:
        problems.append(
            "no `@media (prefers-color-scheme: dark)` override; viewers on the default "
            "system theme would get the light palette in a dark UI"
        )
    if not scopes["dark-attr"]:
        problems.append(
            'no `:root[data-theme="dark"]` override; an explicit dark choice in the '
            "viewer's theme toggle would not apply"
        )
    if 'data-theme="light"' not in css and scopes["dark-media"]:
        problems.append(
            'the dark media query is not guarded with `:root:not([data-theme="light"])`, '
            "so an explicit light choice loses to the system preference"
        )

    dark_only = (scopes["dark-media"] | scopes["dark-attr"]) - scopes["light"]
    problems.extend(
        f"`{name}` is only defined in a dark-theme block; every token needs a light "
        f"definition on bare `:root`"
        for name in sorted(dark_only)
    )

    used = set(re.findall(r"var\(\s*(--[A-Za-z0-9_-]+)", css))
    declared = _custom_props(css)
    problems.extend(
        f"`var({name})` is used but never declared"
        for name in sorted(used - declared)
    )

    if not re.search(r"(^|[\s,}])body\s*(,[^{]*)?\{[^}]*background", css):
        problems.append(
            "`body` has no explicit background; the artifact viewer paints its own "
            "ground behind a transparent body, so the page borrows the host's theme"
        )

    return problems


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("paths", nargs="*", type=pathlib.Path)
    argument_parser.add_argument("-q", "--quiet", action="store_true", help="only print failures")
    args = argument_parser.parse_args()

    paths = args.paths or sorted(REPO_ROOT.glob("*.html"))
    if not paths:
        print("no HTML pages found to check")
        return 0

    failed = 0
    for path in paths:
        if not path.exists():
            print(f"FAIL {path}: file not found")
            failed += 1
            continue
        problems = check_page(path)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for problem in problems:
                print(f"  - {problem}")
        elif not args.quiet:
            print(f"ok   {path}")

    if failed:
        print(f"\n{failed} of {len(paths)} page(s) failed")
        return 1
    if not args.quiet:
        print(f"\nall {len(paths)} page(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
