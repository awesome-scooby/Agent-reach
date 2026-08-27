# Agent-reach

A small collection of self-contained HTML pages — research dashboards and
reference sheets, published as Claude Artifacts. There is no framework, no build
step, and no third-party runtime dependency. Each page is one file.

## Layout

| Path | What it is |
| --- | --- |
| `*.html` (repo root) | The pages. One file per page, fully self-contained. |
| `scripts/check_html.py` | The linter: validates a page against the publishing rules below. |
| `scripts/test_check_html.py` | Tests for the linter (stdlib `unittest`). |
| `scripts/preview.py` | Wraps a page in the Artifact skeleton and serves it locally. |
| `.claude/` | Claude Code config: session hook, permissions, slash commands. |

Python 3 (stdlib only) is the only tool required.

## Commands

```bash
python3 scripts/check_html.py                    # lint every page at the repo root
python3 scripts/check_html.py page.html          # lint one page
python3 -m unittest discover -s scripts -p 'test_*.py'   # test the linter
python3 scripts/preview.py --theme dark          # preview as a viewer sees it
```

Slash commands: `/check`, `/preview`, `/new-page`.

Run `python3 scripts/check_html.py` before calling any page change done. It is
fast and it catches exactly the mistakes that render wrong only after publishing.

## Publishing rules these pages must follow

Each page is an **Artifact body**, not a whole document. The publisher wraps it
in `<!doctype html><head>…</head><body>` and a minimal CSS reset at publish time.
The linter enforces all of the following:

- **No document skeleton.** No `<!doctype>`, `<html>`, `<head>`, or `<body>` tags
  in the file. Start with `<title>`, then `<style>`, then the markup.
- **A `<title>` in the first 8KB.** It names the artifact in the tab and gallery,
  so make it a short, distinctive noun phrase — not a summary.
- **Self-contained.** A strict CSP blocks every remote host except Google Fonts
  (`fonts.googleapis.com` / `fonts.gstatic.com`, which still need a real fallback
  stack). Inline all CSS and JS; embed images as `data:` URIs. `<a href>` to an
  external site is fine — that is a link, not a load.
- **Theme-aware in all three states.** The viewer's theme is either an explicit
  `data-theme` on the root element or nothing at all (system default). So:
  define the complete light palette on bare `:root`; override it under
  `@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){…} }`;
  override it again under `:root[data-theme="dark"]{…}`. Never give a color its
  only definition inside a media or `[data-theme]` block.
- **`body` needs an explicit background.** The viewer paints its own ground
  behind the page, so a transparent body borrows the host's theme.
- **Responsive.** Relative units, `max-width:100%` on media, and wide content
  (tables, code, diagrams) scrolling inside its own `overflow-x:auto` container.
  The page body itself must never scroll horizontally.
- **16MB or smaller**, `data:` URIs included.

## Conventions

- CSS custom properties carry every color; nothing is hardcoded in a rule body.
  Extend the existing token set (`--ground`, `--surface`, `--ink`, `--muted`,
  `--rule`, `--accent`, `--good`, `--warn`, `--crit`, …) rather than adding a
  parallel one.
- Numeric columns use the `.num` / `.mono` classes so figures stay tabular.
- Content pages state their assumptions and link their sources inline; keep that
  habit when editing figures — a changed number needs its source changed with it.
- Match the surrounding file's density and idiom. These pages are typographic and
  deliberately plain; they are not dashboards full of chrome.
