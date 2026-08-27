#!/usr/bin/env python3
"""Tests for scripts/check_html.py.

Run with:
    python3 -m unittest discover -s scripts -p 'test_*.py'
    python3 scripts/test_check_html.py -k skeleton     # a single case
"""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from check_html import REPO_ROOT, check_page  # noqa: E402

# A minimal page that satisfies every check; each test breaks exactly one thing.
GOOD_PAGE = """<title>Test Page</title>
<style>
  :root{ --ground:#fff; --ink:#111; }
  @media (prefers-color-scheme:dark){
    :root:not([data-theme="light"]){ --ground:#000; --ink:#eee; }
  }
  :root[data-theme="dark"]{ --ground:#000; --ink:#eee; }
  body{ background:var(--ground); color:var(--ink); }
</style>
<main><p>Hello</p></main>
"""


class CheckPageTest(unittest.TestCase):
    def check(self, source: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "page.html"
            path.write_text(source, encoding="utf-8")
            return check_page(path)

    def assertFlags(self, source: str, fragment: str) -> None:
        problems = self.check(source)
        self.assertTrue(
            any(fragment in problem for problem in problems),
            f"expected a problem containing {fragment!r}, got {problems}",
        )

    def test_good_page_passes(self):
        self.assertEqual(self.check(GOOD_PAGE), [])

    def test_repo_pages_pass(self):
        pages = sorted(REPO_ROOT.glob("*.html"))
        self.assertTrue(pages, "expected at least one page at the repo root")
        for page in pages:
            with self.subTest(page=page.name):
                self.assertEqual(check_page(page), [])

    def test_skeleton_tag_is_flagged(self):
        self.assertFlags(GOOD_PAGE + "<body>oops</body>", "document skeleton tag")

    def test_missing_title_is_flagged(self):
        self.assertFlags(GOOD_PAGE.replace("<title>Test Page</title>", ""), "no <title>")

    def test_remote_script_is_flagged(self):
        self.assertFlags(
            GOOD_PAGE + '<script src="https://cdn.example.com/x.js"></script>',
            "remote asset blocked",
        )

    def test_google_fonts_is_allowed(self):
        source = GOOD_PAGE + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">'
        self.assertEqual(self.check(source), [])

    def test_anchor_to_external_site_is_allowed(self):
        source = GOOD_PAGE + '<p><a href="https://example.com/source">source</a></p>'
        self.assertEqual(self.check(source), [])

    def test_unclosed_tag_is_flagged(self):
        self.assertFlags(GOOD_PAGE + "<section><p>dangling</p>", "unbalanced markup")

    def test_dark_only_token_is_flagged(self):
        source = GOOD_PAGE.replace(
            ':root[data-theme="dark"]{ --ground:#000; --ink:#eee; }',
            ':root[data-theme="dark"]{ --ground:#000; --ink:#eee; --glow:#0ff; }',
        )
        self.assertFlags(source, "only defined in a dark-theme block")

    def test_undeclared_variable_is_flagged(self):
        source = GOOD_PAGE.replace("color:var(--ink)", "color:var(--nope)")
        self.assertFlags(source, "var(--nope)")

    def test_unguarded_dark_media_query_is_flagged(self):
        source = GOOD_PAGE.replace(':root:not([data-theme="light"])', ":root")
        self.assertFlags(source, "not guarded")

    def test_missing_dark_attribute_block_is_flagged(self):
        source = GOOD_PAGE.replace(':root[data-theme="dark"]{ --ground:#000; --ink:#eee; }', "")
        self.assertFlags(source, 'no `:root[data-theme="dark"]`')

    def test_missing_dark_media_query_is_flagged(self):
        source = """<title>T</title>
<style>
  :root{ --ground:#fff; }
  :root[data-theme="dark"]{ --ground:#000; }
  body{ background:var(--ground); }
</style>
"""
        self.assertFlags(source, "prefers-color-scheme: dark")

    def test_transparent_body_is_flagged(self):
        source = GOOD_PAGE.replace("body{ background:var(--ground); color:var(--ink); }", "body{ color:var(--ink); }")
        self.assertFlags(source, "no explicit background")


if __name__ == "__main__":
    unittest.main()
