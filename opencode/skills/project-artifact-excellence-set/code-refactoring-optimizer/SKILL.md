---
name: code-refactoring-optimizer
description: Detect code smells and optimize fullstack performance through systematic refactoring patterns. Use when refactoring legacy code or reducing complexity or eliminating duplication or improving runtime efficiency. Triggers include refactor code or optimize performance or reduce complexity or fix code smell or clean up module.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---

# Code Refactoring Optimizer

## Purpose
Deliver systematic detection of code smells and disciplined performance optimization across fullstack codebases.
Reduce cyclomatic complexity, eliminate duplication, and extract cohesive modules without changing observable behavior.
Feed before-and-after metric comparisons back into audit evaluation so refactoring value stays measurable and reviewable.
Use this skill when a module feels hard to change, slow at runtime, or risky to review.
Prefer small proven moves over sweeping rewrites and keep every change backed by tests and numbers.

## Core Operating Principles
- Preserve observable behavior. Refactor structure and performance while keeping contracts, outputs, and user-visible flows stable.
- Measure before changing. Capture baseline complexity, duplication, and runtime signals before editing any module.
- Enforce complexity budgets. Hold every function to a cyclomatic budget of 10 or less and split anything that exceeds it.
- Eliminate duplication once. Replace clones with a single tested abstraction owned in one place.
- Extract by responsibility. Separate interface rendering, business rules, and data access into distinct cohesive units.
- Optimize with evidence. Change only hot paths proven by profiling, tracing, or query-plan analysis.
- Keep diffs reviewable. Ship small incremental refactors with passing tests at every step.
- Treat quality attributes as gates. Block completion when reliability, performance, or maintainability regress.
- Document each move. Record what changed, why it changed, and which metric it improves.
- Protect the release path. Keep the main branch green and revert quickly when a refactor misbehaves.

## Process
1. Scope the target. List modules, entry points, and excluded paths. Record language, framework, data stores, and test coverage status.
   Define what staying unchanged means for contracts, payloads, and user journeys before touching code.
2. Capture baselines. Measure cyclomatic complexity per function, duplication rate, module coupling, and bundle size where relevant.
   Record runtime or query latency for hot paths across at least 3 runs and save the raw numbers.
3. Detect smells. Flag god functions, long parameter lists, deep nesting, shotgun surgery, and duplicated blocks.
   Flag oversized interface components, fat services, N-plus-one reads, missing indexes, and dead code paths.
4. Prioritize by impact. Rank findings by defect risk, change frequency, performance cost, and reviewer pain.
   Tackle high-churn high-complexity code first and defer cosmetic cleanups to a later pass.
5. Apply patterns. Use extract service, split component, and optimize query from `references/refactoring-patterns.md`.
   Apply naming, size, and error-handling rules from `references/clean-code-standards.md` on every touched line.
6. Verify behavior. Run existing unit and integration tests after each move. Add characterization tests where coverage is thin.
   Compare outputs, contracts, status codes, and performance after each step and stop on any mismatch.
7. Compare metrics. Recompute complexity, duplication, coupling, and latency. Record the delta per module in a before-and-after table.
   Confirm every changed function sits within budget unless an explicit waiver names the owner and expiry.
8. Feed back to audit. Summarize metric deltas and residual risks for the audit evaluation loop using `../shared/references/holistic-evaluation.md`.
   Route recurring structural gaps through `../shared/references/feedback-loop.md` with file evidence attached.
9. Harden the gate. Record new budgets and review checks so the same smells stay blocked in review and CI.
   Add lint rules, reviewer checklist entries, and dashboard alerts where the team will actually see them.

## Quality Attributes
Address performance, maintainability, reliability, testability, observability, and modularity on every refactor.
Track these quality attributes explicitly with before-and-after numbers rather than descriptive claims.
Calibrate thresholds to user journeys so local cleanup translates into release-level gains.

- Performance. Profile first. Optimize hot loops, payload size, render cost, and query plans. Confirm gains with repeated measurements.
  Record p50 and p95 latency deltas for each optimized path and keep the raw profiling output linked.
- Maintainability. Lower complexity to a budget of 10 or less per function. Shorten functions, narrow interfaces, and remove dead paths.
  Report mean complexity, worst-case function, and duplication rate before and after the pass.
- Reliability. Preserve contracts. Keep error handling explicit and avoid swallowing failures during extraction.
  Verify error paths, retries, and timeouts still behave identically under fault injection or failure simulation.
- Testability. Increase seam clarity. Inject dependencies so extracted services accept focused unit tests.
  Require a direct unit test for each new service and an integration test for each rewired call site.
- Observability. Keep logs, traces, and metrics intact across moves. Add timing around optimized queries and endpoints.
  Confirm dashboards and alerts resolve to the same signals after renames and file moves.
- Modularity. Reduce coupling between interface, domain, and data layers. Enforce one-way dependencies where the stack allows.
  Measure afferent and efferent coupling per module and show the trend arrow in the report.
- Reusability. Consolidate duplicated logic into a single well-named unit with documented inputs and outputs.
  Delete the superseded copies and prove single ownership with code search results.

## Human Factors and Usability
Design refactors for the humans who read, review, and operate the code.
Treat readability and cognitive load as first-class outcomes alongside runtime gains.
Judge success by whether a maintainer understands the result faster and with less effort.

- Reduce cognitive load. Give extracted units intention-revealing names. Keep each function to one responsibility and each component to one visual job.
  Prefer plain language over clever shorthand and keep nesting shallow so control flow scans in one pass.
- Protect reviewers. Keep diffs small, explain each move, and preserve history-friendly file organization where practical.
  Separate pure moves from logic changes so reviewers verify relocation and behavior independently.
- Support operators. Maintain clear error messages, stable log fields, and unchanged runbooks unless an improvement is explicit.
  Announce any operational change in the release notes with rollback steps included.
- Respect accessibility of the codebase. Use consistent structure, predictable file layout, and inclusive design in naming and comments so newcomers navigate quickly.
  Avoid idioms that exclude readers unfamiliar with a single framework dialect.
- Validate usability. Ask a maintainer to locate the new service, explain its contract, and run its tests without extra guidance.
  Record time on task and points of confusion and fix the top friction before closing.
- Sustain trust. Show before-and-after numbers in the pull request so the team sees proof rather than stylistic preference.

## Output Format
Produce a concise report with a metric table the audit loop can consume directly.
Include file paths, line ranges, and the exact pattern applied per finding.
Close with residual risks and the next measurement date.

```text
# Refactor Report
Target modules: ...
Baseline date: ...
Patterns applied: ...

## Before and After
| Module | Complexity before | Complexity after | Duplication before | Duplication after | Latency before | Latency after |

## Changes
- File and lines, pattern used, behavior verification, test command

## Residual Risks
- Remaining smells, waivers with owner and expiry, follow-up tasks
```

## Success Metrics
- Trigger performance: Definition: correct activation on refactoring, complexity-reduction, and duplication-removal requests (member operates with at least 10 mixed prompts per evaluation run); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 10 mixed prompts per evaluation run; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: in-scope smell remediations completed with passing tests and documented metric deltas per bounded module set; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: refactor verification logs with before/after complexity and test evidence; Sample: bounded module sets with full detect-measure-refactor-verify loops; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for the detect-measure-refactor-verify loop (member budgets at most 8000 tokens of guidance context per representative refactor); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: representative refactor tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent engineer runs the full detect-measure-refactor-verify loop on a sample module after first reading this skill; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: sample-module refactor sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: behavior regressions and complexity-budget breaches remaining at handoff (member standard is zero known regressions with changed functions inside the stated complexity budget or an explicit waiver); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: refactor verification logs and waiver records; Sample: all changed functions in the release candidate; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Baseline missing. Halt structural edits. Capture complexity, duplication, and latency first, then proceed.
  Never claim improvement without a recorded starting point tied to a commit hash.
- Tests absent or weak. Write characterization tests for current behavior before extracting. Quarantine uncertain areas to small diffs.
  Expand coverage on the seam under change before widening the refactor scope.
- Over-large extraction. Revert to the last green commit. Split the change into smaller moves with passing tests between each.
  Enforce one pattern per pull request until the suite proves stable.
- Performance regression. Restore the prior implementation for the hot path. Re-profile, correct the query or render path, and re-measure across at least 3 runs.
  Keep the regression trace linked to the incident record for review.
- Duplication returns. Consolidate to the canonical abstraction. Add a lint or review checklist entry pointing to `references/clean-code-standards.md`.
  Search the codebase for remaining clones before declaring done.
- Merge conflicts from moves. Rebase frequently. Prefer pure moves in one commit and logic changes in a follow-up commit.
  Coordinate file moves with the team in advance during high-churn weeks.
- Scope creep. Freeze the target list. Log new smells for a follow-up pass instead of expanding the active diff.
  Track deferred items in the backlog with severity and estimated payoff.

## References
- Refactoring patterns with symptoms and steps: references/refactoring-patterns.md
- Clean-code naming, size, and error-handling standards: references/clean-code-standards.md
- Unified remediation playbook for the packaged set: ../shared/references/unified-remediation-playbook.md
- Integrated technical and human evaluation: ../shared/references/holistic-evaluation.md
- Audit-to-skill feedback routing: ../shared/references/feedback-loop.md
