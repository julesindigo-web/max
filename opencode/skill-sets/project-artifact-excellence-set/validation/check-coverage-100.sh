#!/usr/bin/env bash
# Independent quality gate: global line 100% + branch 100% (eligible Python).
# Usage: bash validation/check-coverage-100.sh [set-root]
# Requires: Python 3.10+ with `coverage` + `pytest` (or unittest fallback).
# Does NOT modify validate-set.sh (8/8 contract unchanged); run separately in CI.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$ROOT}"
TARGET="$(cd "$TARGET" && pwd)"

# Use venv coverage if available, else system coverage.
if [ -x "/tmp/opencode/venv-test/bin/coverage" ]; then
  COV="/tmp/opencode/venv-test/bin/coverage"
  PY="/tmp/opencode/venv-test/bin/python"
else
  COV="coverage"
  PY="python3"
fi

export COVERAGE_PROCESS_START="/tmp/coverage-100gate-coveragerc"
export COVERAGE_FILE="/tmp/coverage-100gate-data/.coverage"

# Config enforces branch + parallel (subprocess) + source = set root, omit tests/fixtures.
mkdir -p /tmp/coverage-100gate-data
cat > "$COVERAGE_PROCESS_START" <<EOF
[run]
branch = True
parallel = True
source = $TARGET
omit =
    */tests/*
    */fixtures/*
    */__pycache__/*
    validation/tests/*
    skills-create-excellence/scripts/tests/*
    .venv/*
[report]
show_missing = True
skip_covered = False
EOF

cd "$TARGET"
rm -f /tmp/coverage-100gate-data/.coverage*
"$COV" run --rcfile="$COVERAGE_PROCESS_START" --branch \
  --source="$TARGET" -m unittest discover -s "$TARGET/validation/tests" -p 'test_*.py'
"$COV" run --rcfile="$COVERAGE_PROCESS_START" --branch \
  --source="$TARGET" -m unittest discover -s "$TARGET/skills-create-excellence/scripts/tests" -p 'test_*.py'
"$COV" combine --rcfile="$COVERAGE_PROCESS_START"
"$COV" report --rcfile="$COVERAGE_PROCESS_START" --show-missing --fail-under=100
# Separate line vs branch check via JSON (fail-under is combined; enforce each 100).
"$COV" json --rcfile="$COVERAGE_PROCESS_START" -o /tmp/coverage-100gate-data/coverage.json
"$PY" - /tmp/coverage-100gate-data/coverage.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
ts = tc = tb = cb = 0
for f in d["files"].values():
    s = f["summary"]
    ts += s["num_statements"]; tc += s["covered_lines"]
    tb += s["num_branches"]; cb += s["covered_branches"]
line = tc / ts * 100 if ts else 100
br = cb / tb * 100 if tb else 100
print(f"LINE: {tc}/{ts} = {line:.2f}%")
print(f"BRANCH: {cb}/{tb} = {br:.2f}%")
if line != 100.0 or br != 100.0:
    print("FAIL: line and branch must each be 100%", file=sys.stderr)
    raise SystemExit(1)
print(f"PASS: global line 100% + branch 100% (eligible Python, {len(d['files'])} files)")
PY
rm -rf /tmp/coverage-100gate-data "$COVERAGE_PROCESS_START"
echo "PASS: coverage-100 gate green."
