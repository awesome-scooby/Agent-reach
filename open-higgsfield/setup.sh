#!/usr/bin/env bash
# Installs and builds Open Higgsfield (Open Generative AI) next to this script.
# Usage: ./setup.sh          install + build
#        ./setup.sh start    install + build, then serve on http://localhost:3000
set -euo pipefail
cd "$(dirname "$0")"

REPO=https://github.com/Anil-matcha/Open-Higgsfield-AI
PIN=fd7dd9207aac1cb14caff220f3a96aaeaa898139   # commit this setup was verified against

if [ ! -d app/.git ]; then
  git clone "$REPO" app
  git -C app checkout --quiet "$PIN"
fi
cd app
npm run setup      # submodules + npm install + workspace packages
npm run build      # Next.js production build

if [ "${1:-}" = "start" ]; then
  exec npx next start -p "${PORT:-3000}"
fi
echo "Built. Run './setup.sh start' to serve the app on port ${PORT:-3000}."
