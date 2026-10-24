#!/usr/bin/env bash
set -euo pipefail
: "${HOME:?HOME must be set}"
export PLAYWRIGHT_BROWSERS_PATH="${HOME}/.cache/opencode/ms-playwright"
mkdir -p "${PLAYWRIGHT_BROWSERS_PATH}"
chmod 700 "${HOME}/.cache/opencode" "${PLAYWRIGHT_BROWSERS_PATH}" 2>/dev/null || true
command -v npx >/dev/null 2>&1 || { echo "ERROR: npx is required to install the pinned Playwright MCP browser" >&2; exit 127; }
# The MCP package pins its Playwright dependency. Install that package's matching Chromium build.
npx --yes @playwright/mcp@0.0.83 install-browser chromium
