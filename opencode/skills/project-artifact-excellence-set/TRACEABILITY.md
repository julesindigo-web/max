# Traceability Matrix — v2.1.0 (fourteen members)

| Outcome / claim | Requirement / section | Design / contract | Test / gate | Runtime signal | Status |
|---|---|---|---|---|---|
| Calibrated audits without epistemic overclaim | auditor SKILL.md Evidence Calibration; SET.md Evidence Calibration | shared/contracts/audit-findings.schema.json v1.1 | test_process_audit_feedback.py (22 tests); validate-set.sh gate 6 | Dated audit reports with evidence states | Covered (static); runtime sampling per release |
| Precise skill triggering (>=90% TPR, <=10% FPR) | Trigger performance metric (all SKILL.md + SET.md + manifest) | evaluation/trigger-evaluation-matrix.json v1.1 (7 skills at 12+12, 7 skills at 5+5; 238 IDs) | validate_trigger_matrices.py; run-trigger-evaluation.py | Target-runtime activation logs + results-YYYY-MM-DD.md | Structure covered; runtime UNVERIFIED until measured |
| Task usefulness (>=95% acceptance) | Task completion metric | evaluation/task-evaluation-ledger.json v1.0 | validate_task_ledger.py; validate-set.sh gate 7 | Ledger evidence pointers + timed logs | Ledger planned; runtime UNVERIFIED |
| Bounded context overhead (<=500 lines) | Context-token efficiency metric | validate-excellence.sh line gate | measure-context.py; gate 7 | Sampled task traces | Covered |
| Learnable authoring (<=60 min) | Time-to-working-skill metric | assets/starter-brief.md + timed-evaluation-log.md | Ledger tasks task-create-skill/task-upgrade-set | Timed guided records (n>=5 or labeled pilot) | Unknown/Untested (pilot pending; 0 timed records as-of 2026-10-15) |
| Zero open Critical/Major without acceptance | Residual defect density metric | shared/references/residual-risk-template.md | validate_metric_specs.py; release gate | Residual-risk register + 30-day review | Covered by gate |
| Safe feedback (no auto-edit) | SET.md Feedback Boundary; feedback-loop.md | process-audit-feedback.py; skill-improvement-requests v1.0 | Feedback processor tests; CI read-only | Reviewed proposals + regression fixtures | Covered |
| Secure delivery (OWASP/secrets/deps) | security-vulnerability-auditor SKILL.md | audit-findings contract mapping | Member validation + ledger task-secure-review | Fresh scan/retest evidence per engagement | Structure covered; SAST/dependency live scan Unknown/Untested until fresh scan per engagement |
| Tested delivery (unit to E2E) | test-automation-engineer SKILL.md | Fullstack E2E metrics reference | Member validation + ledger task-test-gen | Coverage reports + deterministic runs | Structure covered; runtime per suite |
| Gated deployment (security+tests first) | deployment-devops-orchestrator SKILL.md; manifest composition-rules | Pipeline gate evidence | Member validation; bottom-up gate order | Deployment frequency / change-fail rate | Structure covered; runtime per release |
| Synced docs and contracts | architecture-documentation-generator SKILL.md | AST doc-sync script output | Member validation | Source-to-doc diff evidence | Covered |
| Inclusive interfaces (WCAG 2.1 AA) | accessibility-inclusive-design SKILL.md; shared/references/accessibility-standard.md | ARIA/keyboard/contrast checks | Member validation; precondition for frontend/visual claims | AT testing + user verification per engagement | Structure covered; AT runtime per engagement |
| Observable production (OTel/SLO) | continuous-observability-telemetry SKILL.md; shared/references/observability-standard.md | SLO/alert verification records | Member validation | Trace coverage + alert quality signals | Structure covered; runtime per service |
| Premium visual quality | human-centric-visual-excellence SKILL.md; shared/references/premium-aesthetics.md | Design review records | Member validation | Review acceptance + regression counts | Structure covered; runtime per release |
| Reproducible release | release-artifact-hardening.md | scripts/build-release.py + verify-release.py | test_release_artifacts.py; CI build+verify | Archive SHA-256 + detached checksum | Covered |
| Navigable, linked docs | Progressive disclosure rules | scripts/check-links-toc.py | validate-set.sh gate 7 | Author task success | Covered |
| Visual-regression gate (05) | test-automation-engineer SKILL.md Step 6; visual-regression-runbook.md | Playwright MCP captures + P0–P3 rubric | Member validation; token gate; `/vis-diff` | Diff reports + zero open P0 | Structure covered; live-browser runtime per journey |
| Art direction before code (01) | human-centric-visual-excellence SKILL.md Step 0 | Signed Art Brief per release | Member validation | Brand-recall checks | Structure covered; recall runs per brief |
| Design-tokens contract (02) | design-tokens-and-components.md | scripts/check-design-tokens.py | validate-set.sh gate 7; validation/tests/test_check_design_tokens.py | Zero one-off values per release | Covered by gate |
| Visual-family triggers 12+12 | Trigger performance metric | evaluation/trigger-evaluation-matrix.json v2.0.0 + visual-family update | validate_trigger_matrices.py; run-trigger-evaluation.py | results-2026-10-15-independent.md (semantic; live runtime still pending) | Structure covered; live runtime UNVERIFIED |
| Automatic task routing (>=90% TPR, <=10% FPR) | task-orchestrator SKILL.md + routing-policy.md | scripts/route-task.py + matrix tor-* 5+5 | validate_trigger_matrices.py; classifier probes | Target-runtime activation logs + results-2026-10-16-orchestrator.md (author-semantic) | Structure covered; runtime UNVERIFIED until measured |
| Responsive + AT evidence (04) | accessibility-inclusive-design SKILL.md | evaluation/a11y-device-log-YYYY-MM-DD.md | Member validation | AT logs + device rows per product release | Template covered; product runs pending |
| Mutation score | Time-to-working-skill / ledger acceptance | — (no mutation harness in set) | — | Mutation run per consumer suite | Unknown/Untested (no harness; mutation not run in this set) |

## Contract inventory (denominator 7: 5 schemas + 2 data — PA-TST-05)

| Contract | Verifier | Gate |
|---|---|---|
| shared/contracts/audit-findings.schema.json v1.1 | test_process_audit_feedback.py (22) | gate 6 |
| shared/contracts/skill-improvement-requests.schema.json v1 | process-audit-feedback eligible/ineligible fixtures | gate 4 |
| shared/contracts/skill-set-manifest.schema.json | test_validate_set_manifest.py (5) | gate 3 |
| shared/contracts/trigger-evaluation-matrix.schema.json v1.1 | test_validate_trigger_matrices.py (6) + run-trigger-evaluation.py | gate 5+7 |
| shared/contracts/task-evaluation-ledger.schema.json v1.0 | validate_task_ledger.py + 7 ledger tasks | gate 7 |
| evaluation/trigger-evaluation-matrix.json (238 IDs) | coverage scorer + independent adjudication | gate 7 |
| evaluation/task-evaluation-ledger.json (7 tasks) | ledger validator (all planned → UNVERIFIED runtime) | gate 7 |

No unexplained critical-path orphan. Missing runtime rows are marked UNVERIFIED, not PASS.
