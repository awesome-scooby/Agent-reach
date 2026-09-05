# Agent-reach

Standalone HTML artifacts (`dry-eye-quest-log.html`, `weekend-income-register.html`)
plus a Python environment for web scraping with
[Scrapling](https://github.com/D4Vinci/Scrapling).

## Scraping setup

Requires Python >= 3.10.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # or: pip install -e .
scrapling install                 # downloads the browser binaries
```

`pip install` gets you the library and the Python-side fetcher dependencies
(Playwright, Patchright, curl_cffi, browserforge). `scrapling install` is a
separate step that downloads the actual browser binaries — without it, only
the HTTP fetcher and the parser work; the browser-backed fetchers will fail
at launch.

For the interactive shell (`scrapling shell`) and the MCP server
(`scrapling mcp`):

```bash
pip install -e '.[extras]'
```

### Quick check

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get("https://pypi.org/project/scrapling/")
print(page.status)
print(str(page.css("title::text")[0]))
```

Note the API: `css()` returns a list of `Selector` objects, so wrap in `str()`
before calling string methods.

### Fetchers

| Fetcher | Needs browser binaries | Use for |
| --- | --- | --- |
| `Fetcher` | no | plain HTTP, fastest |
| `AsyncFetcher` | no | same, async |
| `DynamicFetcher` | yes | JavaScript-rendered pages |
| `StealthyFetcher` | yes | pages behind bot detection |

`DynamicFetcher` and `StealthyFetcher` also accept `cdp_url=...` to drive an
already-running Chrome over CDP instead of launching their own browser —
useful where a browser is installed but `scrapling install` can't run.

### Known limitation in sandboxed environments

`scrapling install` shells out to `playwright install chromium`, which
downloads from `cdn.playwright.dev`. Behind an egress allowlist that does not
include that host, the download fails with HTTP 403 and the browser-backed
fetchers stay unusable. In that case either allowlist `cdn.playwright.dev`,
pre-bake the browsers into the image, or point `cdp_url` at an existing Chrome
whose CA trust is already configured for the environment's TLS proxy.
