#!/usr/bin/env bash
set -euo pipefail
: "${HOME:?HOME must be set}"
export PLAYWRIGHT_BROWSERS_PATH="${HOME}/.cache/opencode/ms-playwright"
BASE_CONFIG="${HOME}/.config/opencode/excellence-ops/playwright-mcp-config.json"
mkdir -p "${PLAYWRIGHT_BROWSERS_PATH}"
chmod 700 "${HOME}/.cache/opencode" "${PLAYWRIGHT_BROWSERS_PATH}" 2>/dev/null || true
if [[ ! -r "${BASE_CONFIG}" ]]; then
  echo "ERROR: Playwright MCP config missing: ${BASE_CONFIG}" >&2
  echo "Restore the complete OpenCode config snapshot before launching browser MCP." >&2
  exit 78
fi
CONFIG="${BASE_CONFIG}"
if [[ "${EUID}" -eq 0 ]]; then
  if [[ "${OPENCODE_PLAYWRIGHT_ALLOW_ROOT_UNSANDBOXED:-0}" != "1" ]]; then
    echo "ERROR: refusing to launch Chromium as root. Use a non-root OpenCode account; do not disable Chromium sandbox by default." >&2
    echo "Emergency exception is possible only with OPENCODE_PLAYWRIGHT_ALLOW_ROOT_UNSANDBOXED=1 and remains an accepted security risk." >&2
    exit 77
  fi
  CONFIG="${PLAYWRIGHT_BROWSERS_PATH}/playwright-mcp-root-exception.json"
  printf '%s\n' '{"browser":{"browserName":"chromium","isolated":true,"launchOptions":{"chromiumSandbox":false}},"capabilities":["core","core-navigation","core-tabs","core-input"],"saveSession":false}' > "${CONFIG}"
  chmod 600 "${CONFIG}"
  echo "WARNING: emergency root exception disables Chromium sandbox; avoid untrusted URLs and remove this override as soon as possible." >&2
fi
if [[ ! -d "${PLAYWRIGHT_BROWSERS_PATH}" ]] || ! find "${PLAYWRIGHT_BROWSERS_PATH}" -maxdepth 1 -type d -name 'chromium-*' -print -quit | grep -q .; then
  echo "ERROR: pinned Chromium browser is not installed in ${PLAYWRIGHT_BROWSERS_PATH}" >&2
  echo "Run: bash \"${HOME}/.config/opencode/excellence-ops/install-playwright-browser.sh\"" >&2
  exit 78
fi
exec npx --yes @playwright/mcp@0.0.83 --config "${CONFIG}"
