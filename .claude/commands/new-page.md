---
description: Scaffold a new self-contained page that already satisfies the publishing rules
allowed-tools: Read, Write, Edit, Bash(python3 scripts/check_html.py:*)
---

Create a new page in this repo for: **$ARGUMENTS**

Follow the house structure rather than inventing one:

1. Read `weekend-income-register.html` first and reuse its token names, type scale,
   and section rhythm — pages in this repo should look like one family.
2. Write the new page at the repo root as `kebab-case-name.html`, starting with a
   `<title>`, then one `<style>` block, then the markup. No `<!doctype>`, `<html>`,
   `<head>`, or `<body>` — the publisher supplies those.
3. Define the full light palette on bare `:root`, then override it under
   `@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){...} }` and
   again under `:root[data-theme="dark"]{...}`. Give `body` an explicit background.
4. Inline everything. No CDN scripts, stylesheets, or remote images; embed any asset
   as a `data:` URI. Google Fonts is the one allowed remote host, and needs a real
   fallback stack.
5. Run `python3 scripts/check_html.py` and fix anything it reports.
