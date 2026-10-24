#!/usr/bin/env bash
# Canonical fail-closed gate for the composed project-artifact-excellence-set.
# Usage: bash validation/validate-set.sh [set-root]
# Side effects: test fixtures in temporary directories only; no production source edits.
# Required tools: Bash, standard Unix utilities, Python 3.10+.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$ROOT}"
TARGET="$(cd "$TARGET" && pwd)"

printf '%s\n' '== 1/8: Validate manifest, dependency graph, and member contracts =='
python3 "$TARGET/validation/validate_set_manifest.py" "$TARGET"
printf '%s\n' '== 2/8: Semantically validate all metric specifications =='
python3 "$TARGET/validation/validate_metric_specs.py" --root "$TARGET"
printf '%s\n' '== 3/8: Validate set and every manifest member =='
bash "$TARGET/skills-create-excellence/scripts/validate-excellence.sh" "$TARGET"
printf '%s\n' '== 4/8: Run validator positive/negative regression fixtures =='
bash "$TARGET/skills-create-excellence/scripts/tests/test-validate-excellence.sh"
printf '%s\n' '== 5/8: Validate authoritative trigger matrix and manifest/metric regression tests =='
python3 "$TARGET/validation/validate_trigger_matrices.py" "$TARGET"
python3 -m unittest discover -s "$TARGET/validation/tests" -p 'test_*.py' -v
printf '%s\n' '== 6/8: Run feedback processor regression tests =='
python3 -m unittest discover -s "$TARGET/skills-create-excellence/scripts/tests" -p 'test_*.py' -v
printf '%s\n' '== 7/8: Validate task ledger, trigger coverage scoring, links/TOC, context budgets, and design tokens =='
python3 "$TARGET/validation/validate_task_ledger.py" "$TARGET"
python3 "$TARGET/scripts/run-trigger-evaluation.py" --matrix "$TARGET/evaluation/trigger-evaluation-matrix.json"
python3 "$TARGET/scripts/check-links-toc.py" --root "$TARGET"
python3 "$TARGET/scripts/measure-context.py" --root "$TARGET" --budget-lines 500
python3 "$TARGET/scripts/check-design-tokens.py" --root "$TARGET"
printf '%s\n' '== 8/8: Revalidate contracts, authoritative evaluation data, and release integrity rules =='
python3 - "$TARGET" <<'PY'
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
contracts = (
    "shared/contracts/audit-findings.schema.json",
    "shared/contracts/skill-improvement-requests.schema.json",
    "shared/contracts/skill-set-manifest.schema.json",
    "shared/contracts/trigger-evaluation-matrix.schema.json",
    "shared/contracts/task-evaluation-ledger.schema.json",
)
for relative in contracts:
    json.loads((root / relative).read_text(encoding="utf-8"))
matrix = json.loads((root / "evaluation/trigger-evaluation-matrix.json").read_text(encoding="utf-8"))
ledger = json.loads((root / "evaluation/task-evaluation-ledger.json").read_text(encoding="utf-8"))
if ledger.get("schema_version") != "1.0" or len(ledger.get("tasks", [])) < 5:
    raise SystemExit("task-evaluation ledger is missing schema 1.0 / >=5 tasks")
if matrix.get("schema_version") != "1.1" or matrix.get("evaluation_type") != "candidate-test-set-not-runtime-results":
    raise SystemExit("authoritative trigger matrix is missing schema 1.1 / candidate-test-set declaration")
print("PASS: all JSON contract schemas and authoritative evaluation data are syntactically valid")
PY
printf '%s\n' 'PASS: all skill-set validation gates passed.'
