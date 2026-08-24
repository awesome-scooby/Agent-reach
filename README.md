# Agent-reach

## Perplexity MCP server

This project ships a project-scoped MCP config (`.mcp.json`) for the official
[Perplexity MCP server](https://github.com/perplexityai/modelcontextprotocol)
(`@perplexity-ai/mcp-server`). It adds four read-only tools that hit live web data:

| Tool | Use for |
| --- | --- |
| `perplexity_search` | Ranked web results (title, URL, snippet, date), no AI synthesis |
| `perplexity_ask` | Quick web-grounded answers with citations |
| `perplexity_reason` | Step-by-step analysis with web grounding |
| `perplexity_research` | Deep multi-source research (slow — can take minutes) |

### Setup

1. Create an API key at the [Perplexity API portal](https://www.perplexity.ai/account/api/group).
2. Export it in your shell before starting Claude Code — `.mcp.json` reads it via
   `${PERPLEXITY_API_KEY}`, so the key itself is never committed:

   ```bash
   export PERPLEXITY_API_KEY="pplx-..."
   ```

3. Start Claude Code in this directory and approve the project MCP server when prompted.
   Verify with `claude mcp list`.

Optional environment variables: `PERPLEXITY_TIMEOUT_MS` (default 300000),
`PERPLEXITY_BASE_URL` (default `https://api.perplexity.ai`),
`PERPLEXITY_LOG_LEVEL` (`DEBUG|INFO|WARN|ERROR`, default `ERROR`).
