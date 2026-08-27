---
description: Wrap a page in the Artifact skeleton and open it, optionally in a forced theme
allowed-tools: Bash(python3 scripts/preview.py:*), Bash(python3 scripts/check_html.py:*), Read
---

Render a page the way a viewer would see it.

- `python3 scripts/preview.py $ARGUMENTS` serves the wrapped page at http://127.0.0.1:8000/.
- Add `--theme dark` or `--theme light` to force the theme; the default matches the viewer's system setting.
- Add `--no-serve` to just write `.preview/index.html` without starting a server.

Check both themes whenever the change touched colors, and run
`python3 scripts/check_html.py` before calling the page done.
