#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
CONFIG_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
SET_VALIDATOR="${CONFIG_ROOT}/skill-sets/project-artifact-excellence-set/validation/validate-set.sh"

printf '%s\n' '=== OpenCode remediation post-restore checks ==='
command -v node >/dev/null 2>&1 || { echo 'ERROR: node is required' >&2; exit 127; }
command -v npm >/dev/null 2>&1 || { echo 'ERROR: npm is required' >&2; exit 127; }
command -v python3 >/dev/null 2>&1 || { echo 'ERROR: python3 is required' >&2; exit 127; }

cd "${CONFIG_ROOT}"
npm ci --ignore-scripts --no-audit --no-fund
bash "${CONFIG_ROOT}/excellence-ops/validate-plugins.sh"
bash "${SET_VALIDATOR}"

if [[ -d "${CONFIG_ROOT}/skills/project-artifact-excellence-set/skills-create-excellence/scripts/tests" ]] && \
   find "${CONFIG_ROOT}/skills/project-artifact-excellence-set/skills-create-excellence/scripts/tests" -type f -name SKILL.md -print -quit | grep -q .; then
  echo 'ERROR: runtime skill mirror contains test-fixture SKILL.md files.' >&2
  exit 1
fi

if [[ "${1:-}" == "--install-browser" ]]; then
  bash "${CONFIG_ROOT}/excellence-ops/install-playwright-browser.sh"
fi

printf '%s\n' '=== Static checks complete ==='
printf '%s\n' 'LIVE/UNKNOWN: run opencode debug config, opencode agent list, opencode debug skill, and a real browser MCP smoke test from the target host.'
