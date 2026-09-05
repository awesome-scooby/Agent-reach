# mcp-config

> **Parked here temporarily.** This folder is destined for its own repo
> (`awesome-scooby/mcp-config`) and is self-contained — move the whole directory
> when that repo exists. Nothing outside this folder depends on it, and the
> `.mcp.json` is inert while it sits in a subdirectory: Claude Code only picks up
> a `.mcp.json` at a project root. The `curl` line below will 404 until the repo
> is created.

A reusable `.mcp.json` for Claude Code, holding the four officially maintained
MCP reference servers that are useful in almost any project and need no API keys.

## What's in it

| Server | Runtime | What it gives Claude |
|---|---|---|
| `filesystem` | npm, `@modelcontextprotocol/server-filesystem` | Sandboxed file read/write/search, scoped to the directories you list in `args` |
| `git` | Python, `mcp-server-git` | Structured git operations — status, diff, log, blame, branch, commit |
| `fetch` | Python, `mcp-server-fetch` | Retrieves a URL and converts it to markdown for the model |
| `memory` | npm, `@modelcontextprotocol/server-memory` | A knowledge graph that persists across sessions |

All four come from [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers).
Note that `fetch` and `git` are **Python** packages run via `uvx` — there is no
npm `@modelcontextprotocol/server-fetch`, despite what some guides claim.

## Prerequisites

- **Node.js** (for `npx`) — https://nodejs.org
- **uv** (for `uvx`) — `curl -LsSf https://astral.sh/uv/install.sh | sh`

Both `npx -y` and `uvx` fetch the package on first run, so there is nothing to
install ahead of time beyond these two runtimes.

## Use it

Copy `.mcp.json` into the root of any project:

```sh
curl -O https://raw.githubusercontent.com/awesome-scooby/mcp-config/main/.mcp.json
```

Claude Code picks up a project-scoped `.mcp.json` automatically and will prompt
you to approve the servers the first time. Check they connected with:

```sh
claude mcp list
```

## Scoping the filesystem server

`.mcp.json` ships with `"."` — the project directory the config sits in. That is
the safe default: the server can only touch that tree. Add more roots by
appending paths to `args`:

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", ".", "/Users/you/notes"]
```

Do not point it at `/` or your home directory. The allowlist is the only thing
constraining what the model can read and write.

## Memory storage

The `memory` server writes its graph to `.mcp-memory.json` in the project
directory (set via `MEMORY_FILE_PATH`). That file is gitignored here — it is
per-machine state, not config. Drop the `env` block to use the server's default
location inside the npm package instead.

## Not included, and why

- **`everything`** — a test/demo server for exercising the protocol. Pure noise
  in daily use.
- **`sequentialthinking`** and **`time`** — the other two active reference
  servers. Add them if you want; neither needs configuration.
- **`playwright`** (`@playwright/mcp`) — genuinely useful for driving a browser,
  but it downloads Chromium on first run, so it is opt-in rather than a default.
- **GitHub, Slack, Postgres, Sentry, Puppeteer** — these were reference servers
  once and have since been **archived** to
  [`servers-archived`](https://github.com/modelcontextprotocol/servers-archived).
  Use the vendors' own official servers instead; the archived copies are unmaintained.
