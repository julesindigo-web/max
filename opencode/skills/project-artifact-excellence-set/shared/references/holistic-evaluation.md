# Holistic E2E and Human-Factors Evaluation

## Decision Principle
Evaluate the complete user journey and the people operating, maintaining, or authoring the system—not just isolated component correctness. Technical correctness and human outcomes are separate evidence dimensions; passing one does not imply passing the other. Define project-specific targets before testing and preserve measurement context, baseline, source, sample, and observation window.

## Milestone Evaluation Matrix

| Milestone | End-to-end technical evidence | Human-factors evidence | Gate / decision output |
|---|---|---|---|
| Discovery and requirements | Critical journeys, measurable outcomes, data/security boundaries, dependencies, NFR scenarios, and requirement-to-test traceability | Supported personas and contexts, edge/situational users, task success definitions, accessibility needs, user research or explicit assumptions | Prioritized requirements, out-of-scope boundaries, baseline/target plan, and named unresolved assumptions |
| Architecture and experience design | Component/data/API contracts, failure modes, threat boundaries, observability, resilience/recovery, E2E verification strategy, and load/performance budgets | Journey walkthrough, information architecture, cognitive complexity, terminology, error prevention/recovery, keyboard and assistive-tech design | Approved design decisions, risk acceptance, testable contracts, and traceable acceptance criteria |
| Implementation and integration | Unit/integration/contract/E2E tests, critical-path coverage, performance/security/accessibility automation where feasible, telemetry and rollback | Task-based usability check, error-state walkthrough, keyboard/screen-reader checks, zoom/reflow, user-reported friction and cognitive demand | Pass/fail evidence per critical requirement, defects with owners, and regression coverage for escaped defects |
| Release readiness | Production-like critical-journey tests, Core Web Vitals field/lab strategy, API/error behavior, SLO/alert checks, backup/restore and deployment recovery evidence | End-to-end task success for representative contexts, accessibility review against chosen target, understandable status/errors, safe recovery and support content | Release decision, residual-risk record, rollback/recovery owner, and monitoring plan |
| Operations and post-release | Real-user signals, SLO/SLI, latency/error/saturation, failed deployment recovery, change fail/rework rates, cost, incident and regression trends | Support requests, abandonment/task failures, accessibility reports, error recovery success, qualitative feedback, and differential outcomes where appropriate | Prioritized backlog, regression cases, verified remedial actions, and evidence-backed skill-feedback event when a skill gap is suspected or recurrent |

## Evidence Rules
- Connect a critical journey as `user outcome → requirement ID → design/contract → test case → telemetry/operational signal`. Explain legitimate breaks.
- Record what was inspected, when it was measured, and in which environment/device/user segment. Separate measured results from estimates, hypotheses, and unknowns.
- Use field data for real-user performance where available; lab tests are useful for controlled diagnosis but are not identical to production field outcomes.
- Core Web Vitals are LCP, INP, and CLS. TTFB, FCP, and TBT are supporting or diagnostic measures, not Core Web Vitals. For field assessment use the 75th percentile and segment by mobile/desktop when sample quality allows.
- Select E2E latency percentiles and budgets according to the journey and consequence; do not apply a single generic threshold to every endpoint.
- For usability, state task, participant/context selection, success definition, errors, completion time/effort, and method. SEQ is conventionally a 1–7 post-task ease item where 1 is very difficult and 7 is very easy; a low score signals difficulty. Document the exact prompt and scale used.
- For accessibility, combine automated checks with manual keyboard, screen-reader, zoom/reflow, focus/error-state and representative assistive-technology checks. Automated passes alone do not establish full accessibility.
- Keep privacy, consent, and data minimization in any field instrumentation or user research. Do not place sensitive user data in audit-feedback events.
- A non-applicable dimension requires a short, context-specific rationale; missing evidence must not be recorded as a pass.

## Human-Factors Minimum Set for Critical Journeys
1. Effectiveness: user can complete the intended task and acceptance outcomes are clear.
2. Efficiency and cognitive ergonomics: steps, decisions, memory demands, latency, and error costs are appropriate for use frequency and user expertise.
3. Error prevention and recovery: risky actions have safeguards; errors are understandable; recovery preserves work and communicates next steps.
4. Accessibility and inclusion: keyboard/focus, screen-reader semantics, contrast/reflow, language, motor/sensory/cognitive needs, and situational constraints have relevant checks.
5. Satisfaction, trust, and comfort: users understand what the system is doing, why it asks for data/permissions, and how to obtain help or stop.
6. Operational human factors: maintainers can diagnose failures, interpret alerts, execute recovery, and understand runbook preconditions and blast radius.

## Metric Selection and Review
Every selected metric should define: name, purpose, unit/formula, target or threshold and rationale, data source, sample/population, segmentation, collection method, owner, and review window. Pair leading indicators (e.g., failing contract checks, inaccessible component states, rising task error rates) with lagging outcomes (e.g., production incidents, abandonment, support burden, rework). Avoid presenting a proxy such as TBT as the real-user INP result, or checklist completion as proof of task success.

## Connection to Skill Improvement
When the same failure pattern repeats or evidence directly suggests that a skill's instructions/checklists/tests missed a material issue, create a normalized event using `shared/contracts/audit-findings.schema.json`. Route through `shared/references/feedback-loop.md`. A resulting request asks for skill-spec evaluation and regression tests; it does not directly edit or release the skill.
