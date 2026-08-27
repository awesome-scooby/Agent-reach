#!/bin/bash
# SessionStart hook: prepare a Claude Code session for this repo.
#
# The project is a set of self-contained HTML pages with no package manifest and
# no third-party dependencies, so there is nothing to install. What this hook
# does instead is verify the interpreter the repo's own tooling needs, make that
# tooling executable, and record a couple of environment variables for the
# session.
set -euo pipefail

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$project_dir"

if ! command -v python3 >/dev/null 2>&1; then
  echo "session-start: python3 not found; scripts/check_html.py and scripts/preview.py will not run" >&2
  exit 0
fi

echo "session-start: python3 $(python3 --version 2>&1 | awk '{print $2}')"

chmod +x scripts/*.py 2>/dev/null || true

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo 'export PYTHONDONTWRITEBYTECODE=1'
    echo "export AGENT_REACH_ROOT=\"$project_dir\""
  } >> "$CLAUDE_ENV_FILE"
fi

# Fail loudly here rather than at publish time: a page that trips these checks is
# one the Artifact runtime would render wrong.
if ! python3 scripts/check_html.py --quiet; then
  echo "session-start: pages currently fail scripts/check_html.py (see above)" >&2
fi

echo "session-start: ready — run 'python3 scripts/check_html.py' to lint, 'python3 scripts/preview.py' to preview"
