#!/usr/bin/env bash
# Usage: bash scripts/install-git-hook.sh
# Side effects: sets repo-local core.hooksPath to .githooks; does not edit global Git configuration.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  printf '%s\n' 'FAIL: run this script inside a Git work tree.' >&2
  exit 1
}
[[ -x "$ROOT/.githooks/pre-commit" ]] || {
  printf '%s\n' 'FAIL: .githooks/pre-commit is missing or not executable.' >&2
  exit 1
}
git -C "$ROOT" config --local core.hooksPath .githooks
printf 'PASS: local Git hooks enabled for %s (repo-local configuration only).\n' "$ROOT"
printf '%s\n' 'The hook runs the complete validation suite before each commit. CI remains the authoritative merge gate.'
