# Context Traces Template — per-release reference-loading evidence (PA-COV-08)

Copy this file to `context-traces-YYYY-MM-DD.md` each release and record at
least 5 representative task traces: which references were actually loaded per
task class. Proves "only task-relevant references are loaded" instead of
claiming it from SKILL.md line counts alone.

## Trace rows

| Date | Task class | Skill | References loaded | Lines loaded | Justification |
|---|---|---|---|---|---|
| YYYY-MM-DD | visual polish | human-centric-visual-excellence | visual-hierarchy-system.md | ~NN | hierarchy fix, no motion needed |
| YYYY-MM-DD | E2E stabilization | test-automation-engineer | visual-regression-runbook.md | ~NN | baseline diff thresholds |
| YYYY-MM-DD | accessibility audit | accessibility-inclusive-design | wcag-checklist.md | ~NN | contrast evidence per criterion |
| YYYY-MM-DD | interface build | frontend-engineering-excellence | web-vitals-playbook.md | ~NN | LCP budget check |
| YYYY-MM-DD | calibrated audit | project-artifact-auditor | audit-checklists.md | ~NN | severity calibration |

## Acceptance

- At least 5 traces per release, covering distinct task classes.
- Every loaded reference named with a one-line why; unloaded references listed as not-needed where relevant.
- Traces reviewed against `scripts/measure-context.py` budgets (each SKILL.md ≤500 lines).
