---
description: Lint every page against the Artifact publishing rules and run the checker's own tests
allowed-tools: Bash(python3 scripts/check_html.py:*), Bash(python3 -m unittest:*), Read, Edit
---

Validate this repo's pages before publishing.

1. Run `python3 scripts/check_html.py $ARGUMENTS` (no arguments checks every `*.html` at the repo root).
2. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` so the checker itself is known good.
3. For each reported problem, open the page, fix the underlying markup or CSS, and re-run until clean.

Fix the page, never the checker — unless the check is genuinely wrong about the
publishing rules in `CLAUDE.md`, in which case say so before changing it.
