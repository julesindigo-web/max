---
name: test-automation-engineer
description: Generate and maintain multi-tier automated tests from unit to E2E with measurable coverage. Use when creating test suites or expanding coverage or stabilizing flaky E2E flows or validating functional specs. Triggers include write tests or generate E2E suite or improve coverage or fix flaky test or automate QA.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---

# Test Automation Engineer

## Purpose
Generate and maintain multi-tier automated tests from unit through integration, contract, and end-to-end layers.
Raise measurable coverage on changed code, stabilize flaky flows, and map every result to fullstack metrics so quality stays observable and release-ready.
Use this skill when coverage lags, E2E suites flake, or a release needs proof that critical journeys actually work.
Prefer deterministic focused tests over broad brittle scripts and keep every test owned and budgeted.

## Core Operating Principles
- Test the contract first. Assert observable behavior and API promises before internal details.
- Layer the suite. Cover fast unit tests, focused integration tests, and a small set of critical E2E journeys.
- Measure coverage on change. Hold changed lines to an explicit target of 80 percent or higher and report gaps honestly.
  Coverage honesty (PA-COV-01 Opsi B): set-level coverage in this set means contract/ID/test coverage (228 trigger IDs, 94 plus 22 regression tests, total 116 `def test_` counted 2026-10-15), not line/branch percent via coverage.py; the 80 percent changed-lines bar applies to consumer product repos and is Unknown/Untested in this set.
- Stabilize before expanding. Quarantine flakes, fix root causes, and only then add new E2E cases.
- Design for determinism. Isolate time, randomness, network, and data so reruns agree.
- Keep suites fast and owned. Attribute each test to a layer, owner, and runtime budget.
- Treat quality attributes as assertions. Encode performance, reliability, and accessibility checks where the journey demands them.
- Map results to metrics. Record outcomes against `../project-artifact-auditor/references/fullstack-e2e-metrics.md` as the metric source.
- Keep failures actionable. Attach logs, screenshots, and traces so triage starts in minutes.
- Guard the main branch. Block merges when gates miss and quarantine flakes immediately.

## Process
1. Scope the test target. List changed modules, user journeys, APIs, and data paths. Note existing frameworks and CI limits.
   Define done as passing layers plus coverage plus metric mapping, not as test count alone.
2. Design scenarios. Write BDD-style cases with Given, When, Then plus expected observable outcomes.
   Follow `references/test-generation-patterns.md` for layer placement and keep each scenario independent and data-explicit.
3. Generate unit tests. Cover branches, boundaries, and error paths with Jest or Vitest. Mock only at architectural seams.
   Name tests as behavior statements and keep each test focused on one behavior.
4. Generate integration and contract tests. Verify service wiring, persistence, and API schemas. Fail on breaking contract drift.
   Version contracts and test at least one prior consumer where compatibility matters.
5. Generate E2E flows. Automate critical journeys with Playwright or Cypress using stable selectors and isolated test data.
   Replace fixed sleeps with waits on observable state and capture artifacts on every failure.
   Follow `references/visual-regression-runbook.md` for the visual-regression gate below; it is mandatory for any journey with user-visible changes.
6. Run the visual-regression gate (Opsi B, PA-VIS-05). Never accept a journey only because the code runs: open the app in a real browser, screenshot, diff, and request fixes by priority.
   Drive the browser through the Playwright MCP tools (`browser_navigate` → `browser_snapshot` → `browser_take_screenshot`); do not substitute guessed DOM or pasted markup for a live render.
   Capture 360px (phone), 768px (tablet), and 1440px (desktop) viewports in light and dark themes where the product supports them; freeze the approved set under `snapshots/baseline/` with a versioned manifest.
   Diff each run against baseline with the runbook thresholds (P0 BLOCKING: overlapped CTA, truncated text, CLS regression beyond 10 percent; P1 token drift; P2 polish; P3 optional). Label every finding P0–P3; block release on any open P0 older than 14 days.
   Redact PII before storing screenshots (mask names, emails, balances, ID numbers); retain baselines for at least 5 releases and re-baseline only with reviewer approval recorded in the diff report.
7. Measure and map. Compute line and branch coverage on changed code. Translate journey results via `references/e2e-metrics-mapping.md` into the fullstack metric source at `../project-artifact-auditor/references/fullstack-e2e-metrics.md`.
   Report uncovered lines by file and link each journey result to its metric entry.
   Coverage honesty (PA-COV-01 Opsi B): set gates check contract/ID/test coverage, not coverage.py percent; the 80 percent changed-lines bar is for consumer repos and is Unknown/Untested here — report uncovered files explicitly instead of lowering the bar.
8. Quarantine flakes. Detect nondeterministic failures, isolate them with retry and data fixes, and track quarantine age until the root cause is removed.
   Require at least 20 consecutive green runs before promoting a test back to the main suite.
9. Harden CI. Order suites by speed, parallelize E2E safely, and enforce gates that block merges on target misses.
   Isolate parallel workers with unique tenants or data prefixes so runs stay independent.
10. Feed back gaps. Route recurring coverage or stability gaps through `../shared/references/feedback-loop.md` and align remediation with `../shared/references/unified-remediation-playbook.md`.
   Evaluate suite health with `../shared/references/holistic-evaluation.md` before expanding scope.

## Quality Attributes
Assert functional correctness, reliability, performance, observability, maintainability, and accessibility through automation.
Track these quality attributes with suite results and metric mappings rather than manual claims.
Tie every gate to a number the team can trend across releases.

- Correctness. Cover happy paths, boundaries, and error cases per layer with explicit oracles.
  Prove each critical journey with at least one happy path plus two negative variants.
- Reliability. Require deterministic setup, isolated data, and clean teardown so reruns match within documented tolerance.
  Measure flake rate per 100 runs and hold the main suite to zero known flakes.
- Performance. Add timing budgets for critical journeys and API contracts. Fail on regressions beyond agreed thresholds.
  Record p50 and p95 durations and flag regressions beyond 10 percent or beyond budget.
- Observability. Emit clear test names, logs, traces, and artifacts for every failure so triage starts in minutes.
  Link screenshots, video, and traces directly from the failure report.
- Maintainability. Prefer stable selectors, page objects, and shared fixtures over copied setup blocks.
  Review duplication in test code with the same rigor as production code.
- Accessibility. Include keyboard, focus, and contrast checks on key journeys where the metric source defines them.
  Cover screen-reader labels and readable error messages on ship paths.
- Visual regression. Hold every user-visible journey to its approved screenshot baseline across 360px, 768px, and 1440px viewports.
  Block release on open P0 visual findings; label P1–P3 with owner and fix date; never re-baseline without reviewer approval.
- Security. Cover auth, authorization, and input validation paths with negative tests for denied access.
  Prove denied users stay denied across roles and tenants.

## Human Factors and Usability
Make suites readable, trustworthy, and easy to operate.
Treat cognitive load and usability as suite design constraints.
Judge the suite by whether a newcomer trusts a green build and fixes a red one quickly.

- Write readable scenarios. Use plain BDD language so product, design, and engineering share one expectation.
  Keep scenario titles short and outcomes explicit enough to review without opening code.
- Reduce flake anxiety. Label quarantined tests clearly, show owner and next review date, and keep the main branch green.
  Communicate quarantine status in the pull request so authors know what still protects them.
- Support fast triage. Attach screenshots, videos, and logs to E2E failures and point to the exact step that broke.
  Order failure output so the first lines name the journey, step, and expected state.
- Respect inclusive design. Cover keyboard flows, screen-reader labels, and readable error messages in journey tests.
  Verify focus order and visible focus indicators on interactive journeys.
- Validate human factors with a dry run. Ask a newcomer to run the suite, read one failure, and locate the responsible test without help.
  Record time to first useful signal and fix the top friction before expanding.
- Sustain confidence. Publish coverage, stability, and duration trends so the team sees suite health at a glance.

## Output Format
Deliver generated tests plus a coverage and stability summary mapped to the metric source.
List commands to run each layer and the gate verdict per layer.
Close with quarantined items, owners, and next review dates.

```text
# Test Report
Target: ...
Frameworks: Jest or Vitest plus Playwright or Cypress
Metric source: ../project-artifact-auditor/references/fullstack-e2e-metrics.md

## Layer Results
| Layer | Tests | Passing | Coverage | Duration | Gate |

## Journey Mapping
| Journey | Result | Metric entry | Evidence |

## Quarantine
- Test name, owner, expiry, promotion rule
```

## Success Metrics
- Trigger performance: Definition: correct activation on test-generation, coverage-expansion, and flaky-E2E stabilization requests (member evaluates across at least 10 mixed prompts per cycle); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 10 mixed prompts per evaluation cycle; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: planned unit, integration, and E2E scenarios delivered with passing deterministic runs and mapped metric entries per bounded suite request; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: suite execution logs and coverage reports; Sample: bounded suite requests across test tiers; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for multi-tier generation (member budgets at most 9000 tokens of guidance context per representative task); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: representative generation tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent engineer generates a running unit plus integration plus one E2E flow with coverage report on a sample module; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: sample-module generation sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: flaky tests in the main suite and coverage shortfalls remaining at handoff (consumer-repo standard is 80 percent line coverage on changed code with zero known flakes and every quarantine carrying owner and expiry; in this skill-set repo this bar is Unknown/Untested per PA-COV-01 — report uncovered files explicitly); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: coverage reports and quarantine register; Sample: all suites in the release candidate; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Coverage below target. Add focused tests for uncovered branches first. Narrow scope rather than lowering the bar silently.
  Report uncovered files explicitly so the gap stays visible to reviewers.
- Flaky E2E blocks merges. Quarantine the flake immediately. Fix data isolation, timing, or selector stability, then promote back only after at least 20 consecutive green runs.
  Track quarantine age daily and escalate stale items past expiry.
- Brittle selectors. Switch to role, label, or test-id selectors. Remove sleeps in favor of explicit waits on observable state.
  Audit selector health whenever the interface structure changes.
- Shared-state pollution. Reset databases or sandboxes per run. Isolate parallel workers with unique tenants or prefixes.
  Verify teardown with a repeat run before declaring the fix complete.
- Slow suites. Split by layer, parallelize E2E, and move heavy setup into fixtures. Enforce per-layer runtime budgets.
  Profile the slowest 5 tests first and fix setup cost before adding capacity.
- Contract drift. Freeze the provider version. Update consumer and provider schemas together with versioned change notes.
  Require contract tests to pass before any E2E expansion on the affected surface.
- False green. Audit mocks and skipped tests. Require at least one real integration or E2E proof per critical journey.
  Treat skipped coverage as uncovered until a real test replaces it.
- Visual P0 escape. Block release on any open P0 visual finding; file P0–P3 with owner and fix date; re-baseline only with approver, date, and rationale in the diff report; quarantine font and animation flakes per the runbook.

## References
- Layered generation patterns and BDD design: references/test-generation-patterns.md
- Visual-regression gate runbook (Playwright MCP wiring, baselines, thresholds, P0–P3 rubric): references/visual-regression-runbook.md
- Result-to-metric translation tables: references/e2e-metrics-mapping.md
- Fullstack metric source for mapping: ../project-artifact-auditor/references/fullstack-e2e-metrics.md
- Unified remediation playbook for the packaged set: ../shared/references/unified-remediation-playbook.md
- Integrated technical and human evaluation: ../shared/references/holistic-evaluation.md
- Audit-to-skill feedback routing: ../shared/references/feedback-loop.md
