# Remediation Changelog — v1.2.0/v1.3.0 → v2.0.0 Integrated Masterpiece (thirteen members)

## Integration (2026-10-15, opencode user-level ecosystem)
- Core members `project-artifact-auditor` and `skills-create-excellence` upgraded 1.1.0 → 2.0.0 with the full masterpiece package (calibration, 12+12 trigger coverage, scorer, ledger, gates, TRACEABILITY, docs, ID aliases, deterministic release).
- All eleven domain members standardized from short-form to ten-field measurable metric contracts (canonical set targets; domain operating notes preserved inline); interfaces unchanged so versions stay 1.0.0; `depends-on` floor raised to `project-artifact-auditor@>=2.0.0`.
- Shared layer: audit-findings schema 1.1 (reads 1.0), task-ledger + trigger-matrix schemas registered, calibrated feedback-loop/playbook, release-hardening + residual-risk references added; domain baselines (accessibility/observability/premium) untouched.
- Validation harness 6 → 8 gates (metric semantics across all 13 members, task ledger, trigger scorer, link/TOC, context budgets); trigger matrix 228 cases (114+114, 228 unique IDs) across all members; task ledger 7 tasks.
- Deployed to canonical source `~/.config/opencode/skill-sets/project-artifact-excellence-set` and runtime mirror `~/.config/opencode/skills/project-artifact-excellence-set` (exclusions: `skills-create-excellence/scripts/tests/**`, `.github/**`, `.githooks/**`).
- No `opencode.jsonc` change required: `skills/*/SKILL.md` is auto-loaded recursively.

## Prior 2-member masterpiece (Drive lineage, retained for reference)

## Version
Set + both members: `1.3.0` → `2.0.0`. Additive migration; 1.3.0 validators remain satisfied (all original gates still pass; new gates are additions, not replacements).

## What changed (grouped by audit finding)
- F-01: `evaluation/trigger-evaluation-matrix.json` 7+7 → 12+12 per skill (ID, adversarial, near-miss families); README + metric sample text updated to 12+12 in both manifest.yaml and SET.md (kept synchronized).
- F-02: new `evaluation/runtime-protocol.md`, `evaluation/results-template.md`, executable `scripts/run-trigger-evaluation.py` (coverage + observation grading, SHA-256 freeze, per-skill TPR/FPR).
- F-03: new `shared/contracts/task-evaluation-ledger.schema.json`, `evaluation/task-evaluation-ledger.json` (7 tasks as-of 2026-10-15; F-03 required ≥5, ledger now holds 7), `validation/validate_task_ledger.py` wired into `validation/validate-set.sh` gate 7.
- F-04: new `TRACEABILITY.md`; manifest composition-rules now require it per release.
- F-05: `project-artifact-auditor/references/audit-checklists.md` severity guide rewritten to the calibrated evidence-state-separated rule.
- F-06/F-07: TOC `## Contents` added to 3 references >100 lines; new `scripts/check-links-toc.py` (fixture-excluded, code-span/fence aware, regex-fragment guard) + `scripts/measure-context.py` (500-line budget) wired into gate 7.
- F-08: new `i18n/id/TRIGGER-ALIASES-ID.md`; 6 ID cases in matrix; multilingual notes added to both SKILL.md.
- F-09: new `skills-create-excellence/assets/starter-brief.md` + `assets/timed-evaluation-log.md`.
- F-10/F-11/F-12: `docs/` bundle (ARCHITECTURE, GLOSSARY, ADR-0001..0003, RACI, THREAT-MODEL, OPERATIONS-RUNBOOK, CHANGELOG, CONTRIBUTING); `shared/examples/audit-report.sample.md`; extended `shared-contracts` manifest list; both SKILL.md gained Failure Modes, Observability, Security Boundaries, Versioning sections plus `allowed-tools` least-privilege declarations (line counts 178 / 233, both ≤500).
- `scripts/release_artifact_utils.py`: 4 new executable paths registered for deterministic packaging.
- `.github/workflows/validate-skills.yml`: explicit 8-gate step + scorer/ledger/link/context step.
- New root evidence: `AUDIT-REPORT-MASTERPIECE.md` (this audit), `REMEDIATION-CHANGELOG.md` (this file).

## Verification (2026-10-15, work tree)
- `bash validation/validate-set.sh` → PASS all 8 gates (manifest/DAG, metric semantics, member validation, fixture regressions, trigger matrix (228 IDs) + 94 validation tests + 22 feedback-processor tests (total 116 `def test_`, 2026-10-15), ledger + scorer + links/TOC + context budgets, contract revalidation).
- `python3 scripts/build-release.py --root . --output <outside-tree>.zip` → byte-identical reproducible builds; `python3 scripts/verify-release.py` → checksums + executable modes + required files verified; detached `.sha256` matches via `sha256sum -c`.

## How to verify the shipped ZIP
```bash
python3 scripts/verify-release.py project-artifact-excellence-set-2.0.0-masterpiece.zip
(cd <dir> && sha256sum -c project-artifact-excellence-set-2.0.0-masterpiece.zip.sha256)
# then extract into a dedicated directory and run:
bash validation/validate-set.sh
```

## Residual (accepted, with owners)
- Runtime TPR/FPR + task completion: UNVERIFIED — owner: release evaluator; next: execute `evaluation/runtime-protocol.md` and file dated results.
- Accessibility AT testing, security assurance, production performance: pending independent evaluation — owner: release approver; review: 30-day post-release recurrence.
- Archive authenticity beyond integrity: use a trusted channel + separate signature where required — owner: release approver.
