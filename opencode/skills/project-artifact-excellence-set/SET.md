# Project Artifact Excellence Skill Set

## Purpose
Compose fourteen member skills into a full-lifecycle AI agent engineering
ecosystem: audit evidence is normalized, SDLC delivery skills build and verify
systems, fullstack mastery integrates the layers end to end, premium
human-centric skills elevate the experienced quality, and a shared remediation
playbook plus release checks validate the package as a set.

## Member Responsibilities
- `project-artifact-auditor`: inspect project artifacts, classify evidence-backed findings, and identify whether a repeated pattern may indicate a gap in the audit method or its guidance.
- `skills-create-excellence`: evaluate skill trigger design, quality attributes, metrics, validation, human factors, and composition when a skill-improvement request is generated.
- `code-refactoring-optimizer`: detect code smells, reduce cyclomatic complexity, eliminate duplication, and verify gains against audit quality metrics.
- `security-vulnerability-auditor`: scan for OWASP Top 10 issues, secrets leakage, and dependency risk, emitting findings through the audit-findings contract.
- `test-automation-engineer`: generate multi-tier tests from unit to E2E and map results to the fullstack E2E metrics reference.
- `architecture-documentation-generator`: keep architecture docs and OpenAPI contracts synchronized with source, backed by the deterministic AST doc-sync script.
- `deployment-devops-orchestrator`: build minimal container images and gated CI/CD pipelines only after security and test checks pass.
- `fullstack-e2e-mastery`: deliver production-grade systems from interface through domain to data with E2E verification.
- `backend-engineering-excellence`: hold sub-100ms latency budgets, strict encryption, and testable domain modularity.
- `frontend-engineering-excellence`: hold Core Web Vitals targets with resilient client state and cross-browser verification.
- `human-centric-visual-excellence`: deliver premium spatial harmony and luxury motion grounded in human-factors evidence.
- `accessibility-inclusive-design`: enforce WCAG 2.1 AA with correct ARIA and keyboard navigation as a precondition for frontend and visual claims.
- `continuous-observability-telemetry`: instrument OpenTelemetry logs, metrics, and tracing with SLO-driven alerting for production health.
- `task-orchestrator`: route every task to the best skill, command, workflow, subagent, runbook, and domain procedure via a deterministic procedural classifier when no slash command is given.
- `shared/contracts/`: define versioned machine-readable contracts between the audit, skill-evaluation, and set-manifest stages.
- `shared/references/unified-remediation-playbook.md`: canonical cross-skill remediation guidance.
- `shared/references/accessibility-standard.md`, `observability-standard.md`, `premium-aesthetics.md`: shared baselines for inclusive, observable, premium delivery.
- `validation/validate-set.sh`: execute set-level validation, member validation, regression tests, and feedback-processor tests.

## Feedback and Approval Boundary
The feedback processor does not edit production `SKILL.md` files and does not autonomously merge changes. It creates deterministic, structured evaluation requests only when a finding is open and either explicitly flags a suspected skill-level gap or recurs in at least two observations. A qualified agent or reviewer evaluates the proposed skill change; the change then passes CI and human review under repository policy. One-off project defects remain project remediation work unless evidence suggests a skill-level gap.

## Composability
Member dependencies are declared in `manifest.yaml` and must form a directed acyclic graph. Delivery gates compose bottom-up: `security-vulnerability-auditor` and `test-automation-engineer` pass before `deployment-devops-orchestrator` runs; `accessibility-inclusive-design` passes before frontend or visual excellence is claimed. The audit finding contract is the interface from auditing to feedback processing. The skill improvement request contract is the interface from feedback processing to skill specification/evaluation. Inputs are treated as untrusted data; findings never become shell commands or executable instructions.

## Integrated Evaluation
Every relevant milestone assesses both end-to-end technical outcomes and human factors. Use `project-artifact-auditor/references/fullstack-e2e-metrics.md` for technical signals, `project-artifact-auditor/references/human-factors-usability.md` for product/user experience, `shared/references/accessibility-standard.md` for inclusive delivery, `shared/references/observability-standard.md` for production health, `shared/references/premium-aesthetics.md` for visual excellence, and `skills-create-excellence/references/human-factors.md` when evaluating the skill authoring or agent interaction surface. Tailor metrics and thresholds to the context, name their data source and measurement window, and mark non-applicable items with rationale.

## Success Metrics
- Trigger performance: Definition: proportion of labeled positive prompts that activate the intended skill and labeled negative prompts that do not; Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation across all fourteen members; Source: evaluation/trigger-evaluation-matrix.json plus target-runtime activation logs; Sample: 12+12 authored prompts for each core skill and at least 5 positive and 5 negative prompts for each domain member; Segmentation: per skill, positive/negative class, and prompt family including Indonesian and near-miss cases; Method: execute each prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: fraction of applicable acceptance checks completed successfully without unplanned workaround; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness across audit, authoring, SDLC, fullstack, and premium design tasks; Source: CI acceptance results and evaluation/task-evaluation-ledger.json; Sample: every mandatory CI check plus representative end-to-end tasks covering audit, skill authoring, security review, test generation, and gated deployment per release; Segmentation: by member skill, task type, and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint and relevance of reference material loaded for a representative task; Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage across fourteen members; Source: repository files and sampled execution traces via scripts/measure-context.py; Sample: every member SKILL.md plus at least 5 representative task traces per release; Segmentation: by member skill and task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: elapsed guided time from task start until a first-time author produces a structurally valid, tested, usable skill result; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks authoring workflow learnability rather than code presence alone; Source: timed guided-evaluation records with skills-create-excellence/assets/starter-brief.md; Sample: at least 5 first-time authors for a major release evaluation, or a clearly labeled pilot when fewer are available; Segmentation: by author experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial authoring-process changes
- Residual defect density: Definition: count of open release-blocking or high-impact defects remaining after final validation, with risk acceptance recorded separately; Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: audit findings, CI results, and the residual-risk register; Sample: all known Critical/Major findings and failed release-gate cases for the candidate; Segmentation: by severity, member skill, security/human/operational impact, and disposition; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review

Coverage honesty (PA-COV-01 Opsi B): the set coverage gate means contract/ID/test coverage — 238 trigger case IDs, 122 validation tests plus 22 feedback-processor tests (total 144 `def test_`, counted 2026-10-16) — not line/branch percent via coverage.py; the 80 percent changed-lines bar applies to consumer product repos and is Unknown/Untested in this set.

Mirror limitation (PA-COV-03): full validation is authoritative only in the canonical tree; gates 4 and 6 plus 2 release tests fail by-design in the runtime mirror, which excludes provenance paths. `__pycache__` differences between the trees are ignored (interpreter cache, never committed).

Cost note (PA-CST-08): this set tracks no run-cost budget; use archived `measure-context.py` line counts plus ledger elapsed minutes as token/time proxies per release until sampled traces exist. Run-cost is Unknown/Untested in this set (proxies only).

## Canonical Documentation Index (v2.1.0)
- Architecture & contracts: `docs/ARCHITECTURE.md`, `manifest.yaml`, `shared/contracts/`, `TRACEABILITY.md`
- Decisions: `docs/ADR-0001-scope.md`, `docs/ADR-0002-calibration.md`, `docs/ADR-0003-release.md`, `docs/ADR-0004-visual-automation.md`
- Operations: `docs/THREAT-MODEL.md`, `docs/OPERATIONS-RUNBOOK.md`, `docs/RACI.md`, `docs/RISK-REGISTER.md`, `shared/references/residual-risk-template.md`
- Evaluation: `evaluation/runtime-protocol.md`, `evaluation/trigger-evaluation-matrix.json`, `evaluation/task-evaluation-ledger.json`, `scripts/run-trigger-evaluation.py`, `scripts/check-links-toc.py`, `scripts/measure-context.py`
- Localization: `i18n/id/TRIGGER-ALIASES-ID.md` (Indonesian trigger aliases; canonical descriptions remain English for trigger stability)
- Audit evidence: `AUDIT-REPORT-MASTERPIECE.md`, `REMEDIATION-CHANGELOG.md`

## Traceability & Runtime-Evaluation Rule (v2.1.0)
Every critical user journey and every skill-set claim must be traceable in `TRACEABILITY.md` as `outcome → requirement → design/contract → test → runtime signal`. Static PASS never implies runtime trigger precision, task success, accessibility, security, or performance. Runtime claims require a frozen test set, target-runtime activation logs, independent label adjudication, and a dated results record per `evaluation/runtime-protocol.md`. Delivery gates compose bottom-up as declared in Composability above.

Release packaging and verification policy: `shared/references/release-artifact-hardening.md`; build a deterministic archive with `python3 scripts/build-release.py --output <outside-source-tree.zip>` and verify it with `python3 scripts/verify-release.py <archive.zip>`.

## Release Gate
A release candidate is acceptable only when `bash validation/validate-set.sh` passes (all 8 gates including metric-semantics, task-ledger, trigger-scorer, link/TOC, context-budget, and design-tokens gates); no open Critical/Major skill-quality finding lacks an explicit decision; the feedback path has valid-input, invalid-input, eligible-finding, ineligible-finding, and deterministic-output coverage; and set composition has no unresolved member/dependency/contract error. A successful structural check is not a substitute for runtime, user, accessibility, security, or performance evaluation.
