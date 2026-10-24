#!/usr/bin/env bash
# Automated regression tests for validate-excellence.sh.
# Usage: bash test-validate-excellence.sh
# Side effects: creates temporary log files only; no project files are modified.
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="$TEST_DIR/../validate-excellence.sh"
FIXTURES="$TEST_DIR/fixtures"
ARCHIVE_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'PASS: %s\n' "$*"; }

[[ -x "$VALIDATOR" ]] || fail "Validator is not executable: $VALIDATOR"

log=$(mktemp)
set_tmp=$(mktemp -d)
trap 'rm -f "$log"; rm -rf "$set_tmp"' EXIT

# Positive fixture must pass.
if bash "$VALIDATOR" "$FIXTURES/valid-skill" >"$log" 2>&1; then
  pass "valid fixture exits 0"
else
  cat "$log" >&2
  fail "valid fixture unexpectedly failed"
fi

# Negative fixtures must fail for the intended mandatory gate.
expect_failure() {
  local fixture="$1" expected="$2"
  if bash "$VALIDATOR" "$FIXTURES/$fixture" >"$log" 2>&1; then
    cat "$log" >&2
    fail "$fixture unexpectedly exited 0"
  fi
  grep -Fq "$expected" "$log" || { cat "$log" >&2; fail "$fixture failed for an unexpected reason; expected '$expected'"; }
  pass "$fixture exits non-zero for expected reason"
}

expect_failure invalid-name-skill "does not match directory name"
expect_failure unknown-frontmatter-key-skill "Unknown top-level frontmatter key 'version'"
expect_failure missing-description-skill "Required frontmatter key 'description' is missing"
expect_failure missing-version-metadata-skill "metadata.version must be present exactly once"
expect_failure missing-quality-attributes-skill "A dedicated Quality Attributes section is required"
expect_failure insufficient-metrics-skill "At least five success metrics are required"
expect_failure unmeasurable-metric-skill "Each success metric must state a measurable target"
expect_failure missing-metric-dimension-skill "Required metric dimension 'Context-token efficiency' is missing"
expect_failure missing-human-factors-skill "Human-factors coverage is required"

# Smoke-test both real skills distributed in this archive.
bash "$VALIDATOR" "$ARCHIVE_ROOT/skills-create-excellence" >"$log" 2>&1 || { cat "$log" >&2; fail "skills-create-excellence did not validate"; }
pass "skills-create-excellence validates"
bash "$VALIDATOR" "$ARCHIVE_ROOT/project-artifact-auditor" >"$log" 2>&1 || { cat "$log" >&2; fail "project-artifact-auditor did not validate"; }
pass "project-artifact-auditor validates"

# Set-level manifest metrics and declared member paths are mandatory too.
mkdir -p "$set_tmp/valid-set/skills/valid-skill"
cp "$FIXTURES/valid-skill/SKILL.md" "$set_tmp/valid-set/skills/valid-skill/SKILL.md"
cp "$ARCHIVE_ROOT/SET.md" "$set_tmp/valid-set/SET.md"
cat > "$set_tmp/valid-set/manifest.yaml" <<'MANIFEST'
name: valid-set
version: "1.0.0"
purpose: A valid test skill set
success-metrics:
  - "Trigger performance: Definition: proportion of labeled positive prompts that activate the intended skill and labeled negative prompts that do not; Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation across all fourteen members; Source: evaluation/trigger-evaluation-matrix.json plus target-runtime activation logs; Sample: 12+12 authored prompts for each core skill and at least 5 positive and 5 negative prompts for each domain member; Segmentation: per skill, positive/negative class, and prompt family including Indonesian and near-miss cases; Method: execute each prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change"
  - "Task completion: Definition: fraction of applicable acceptance checks completed successfully without unplanned workaround; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness across audit, authoring, SDLC, fullstack, and premium design tasks; Source: CI acceptance results and evaluation/task-evaluation-ledger.json; Sample: every mandatory CI check plus representative end-to-end tasks covering audit, skill authoring, security review, test generation, and gated deployment per release; Segmentation: by member skill, task type, and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes"
  - "Context-token efficiency: Definition: instruction footprint and relevance of reference material loaded for a representative task; Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage across fourteen members; Source: repository files and sampled execution traces via scripts/measure-context.py; Sample: every member SKILL.md plus at least 5 representative task traces per release; Segmentation: by member skill and task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization"
  - "Time-to-working-skill: Definition: elapsed guided time from task start until a first-time author produces a structurally valid, tested, usable skill result; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks authoring workflow learnability rather than code presence alone; Source: timed guided-evaluation records with skills-create-excellence/assets/starter-brief.md; Sample: at least 5 first-time authors for a major release evaluation, or a clearly labeled pilot when fewer are available; Segmentation: by author experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial authoring-process changes"
  - "Residual defect density: Definition: count of open release-blocking or high-impact defects remaining after final validation, with risk acceptance recorded separately; Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: audit findings, CI results, and the residual-risk register; Sample: all known Critical/Major findings and failed release-gate cases for the candidate; Segmentation: by severity, member skill, security/human/operational impact, and disposition; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review"
members:
  - name: valid-skill
    version: "1.0.0"
    path: skills/valid-skill
MANIFEST
if bash "$VALIDATOR" "$set_tmp/valid-set" >"$log" 2>&1; then
  pass "valid set fixture exits 0"
else
  cat "$log" >&2
  fail "valid set fixture unexpectedly failed"
fi
sed -i 's/Context-token efficiency:/Task completion duplicate:/' "$set_tmp/valid-set/manifest.yaml"
if bash "$VALIDATOR" "$set_tmp/valid-set" >"$log" 2>&1; then
  cat "$log" >&2
  fail "set fixture without all required metric dimensions unexpectedly passed"
fi
grep -Fq "Required metric dimension 'Context-token efficiency' is missing" "$log" || { cat "$log" >&2; fail "invalid set fixture failed for an unexpected reason"; }
pass "invalid set fixture exits non-zero for missing required metric dimension"

# A random directory cannot be reported as a passing skill/set.
mkdir -p "$TEST_DIR/tmp-not-a-skill"
if bash "$VALIDATOR" "$TEST_DIR/tmp-not-a-skill" >"$log" 2>&1; then
  rm -rf "$TEST_DIR/tmp-not-a-skill"
  fail "directory without SKILL.md or set marker unexpectedly passed"
fi
rm -rf "$TEST_DIR/tmp-not-a-skill"
pass "unrecognized target directory exits non-zero"

printf 'All validator regression tests passed.\n'
