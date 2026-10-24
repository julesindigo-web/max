# E2E Metrics Mapping

Translate suite results into the fullstack metric source. Use the canonical definitions at `../../project-artifact-auditor/references/fullstack-e2e-metrics.md` as the authority.

## Coverage Mapping
- Map line coverage on changed code to the completeness signal; hold at 80% or higher.
- Map branch coverage to edge-case readiness; report uncovered branches by file.
- Map contract pass rate to integration health; require 100% on release branches.
- Map skipped and quarantined counts separately; never count them as passing.

## Stability Mapping
- Map flake rate to reliability; compute failures per 100 runs per suite.
- Quarantine any test failing nondeterministically more than once per 20 runs.
- Require at least 20 consecutive green runs before promoting from quarantine.
- Record owner and expiry for every quarantined case.

## Performance Mapping
- Map journey duration to responsiveness signals with per-journey budgets.
- Map API p95 latency from contract tests to backend service objectives.
- Flag regressions beyond 10% or beyond the stated budget, whichever is tighter.
- Attach traces for any journey exceeding its budget.

## Accessibility and Journey Mapping
- Map keyboard and focus checks to the accessibility signal in the metric source.
- Map critical-journey pass rate to release readiness; require 100% for ship paths.
- Report results per journey with evidence links to logs, video, and traces.
- Route systemic gaps through `../../shared/references/feedback-loop.md` with metric deltas attached.
