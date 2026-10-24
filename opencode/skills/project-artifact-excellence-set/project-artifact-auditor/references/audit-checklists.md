# Canonical Audit Checklists


## Contents
- [1. Requirements / PRD / SRS](#1-requirements--prd--srs-completeness-checklist)
- [2. User Stories](#2-user-stories--backlog-quality-invest)
- [3. Architecture](#3-architecture--design-document-checklist)
- [4. API Contracts](#4-api--contract-specification)
- [5. Traceability](#5-cross-artifact-traceability)
- [6. Human Factors summary](#6-human-factors--usability-specific-checklist-summary--full-detail-in-human-factors-usabilitymd)
- [Severity Calibration](#severity-calibration-guide-evidence-state-separated--authoritative)
- [7. E2E + Human-Factors Gate](#7-integrated-end-to-end--human-factors-milestone-gate)
- [8. Feedback Event](#8-optional-audit-to-skill-feedback-event)
- [9. Multilingual & Adversarial](#9-multilingual-adversarial--near-miss-trigger-review)
- [10. Supply-Chain & Readiness](#10-supply-chain-cost--production-readiness-spot-check)

## 1. Requirements / PRD / SRS Completeness Checklist
- [ ] Problem statement / opportunity clearly articulated
- [ ] Business goals and success metrics (measurable)
- [ ] Target users / personas defined with goals, pain points, contexts and extreme cases
- [ ] Jobs-to-be-done or user goal hierarchy present
- [ ] In-scope and out-of-scope explicitly bounded (including which user groups or contexts are excluded)
- [ ] Functional requirements with unique IDs and priority
- [ ] Non-functional requirements (performance, security, scalability, availability, accessibility, localization, compliance, usability targets)
- [ ] Explicit usability / human-factors requirements (learnability, efficiency, error rates, satisfaction targets)
- [ ] Acceptance criteria for every major requirement (testable, including user-observable outcomes)
- [ ] Data requirements / entities / relationships
- [ ] External interfaces and integrations
- [ ] Assumptions and constraints listed and owned
- [ ] Dependencies (technical, organizational, third-party)
- [ ] Risks with probability, impact and mitigation (including human/usability risks)
- [ ] Open questions / decisions pending
- [ ] Glossary of terms (understandable by intended audience)
- [ ] Version history and change control

## 2. User Stories / Backlog Quality (INVEST+)
- [ ] Independent
- [ ] Negotiable
- [ ] Valuable (clear user value)
- [ ] Estimable
- [ ] Small
- [ ] Testable
- [ ] Clear persona + goal + benefit format
- [ ] Explicit acceptance criteria (including edge and error cases)
- [ ] Edge cases, error paths and recovery covered
- [ ] Non-functional / usability notes attached where relevant
- [ ] Cognitive load or complexity implications considered for complex stories

## 3. Architecture / Design Document Checklist
- [ ] Context diagram / system context
- [ ] High-level component / container diagram
- [ ] Key architectural decisions with alternatives considered and rationale (ADR style)
- [ ] Data flow and control flow for critical paths
- [ ] Technology stack with justification
- [ ] Scalability, resilience, security and observability strategies
- [ ] Deployment topology and environments
- [ ] Interface contracts (API, events, schemas)
- [ ] Cross-cutting concerns addressed (including accessibility and internationalization)
- [ ] Known limitations and technical debt acknowledged
- [ ] Human-operability implications of architectural choices noted (e.g., latency impact on perceived performance, complexity impact on debuggability)

## 4. API / Contract Specification
- [ ] Resource model and naming conventions (human-readable and consistent)
- [ ] Request/response schemas with examples
- [ ] Error model and status codes (clear, actionable messages)
- [ ] Authentication / authorization scheme
- [ ] Versioning strategy
- [ ] Rate limiting / pagination / filtering
- [ ] Idempotency and consistency guarantees
- [ ] Backward compatibility policy
- [ ] Developer experience / ease of use considerations (documentation quality, predictability)

## 5. Cross-Artifact Traceability
- [ ] Every requirement maps to at least one design element
- [ ] Every design element maps back to a requirement or explicit non-requirement
- [ ] Test cases / acceptance criteria cover requirements
- [ ] Risks map to requirements or architectural decisions
- [ ] User journeys map to requirements and design elements
- [ ] No orphan artifacts

## 6. Human Factors & Usability Specific Checklist (summary — full detail in human-factors-usability.md)
- [ ] Primary and extreme personas defined with contexts of use
- [ ] Core user goals and success criteria from human perspective
- [ ] Usability targets (effectiveness, efficiency, satisfaction, learnability, error rates) stated or justified as out-of-scope
- [ ] Cognitive load and complexity management addressed
- [ ] Error prevention, recognition and recovery designed
- [ ] Accessibility targets (WCAG level) and inclusive design considerations present
- [ ] Onboarding, empty states, error states and help considered
- [ ] Consistency of interaction patterns
- [ ] Dark patterns and manipulative design absent
- [ ] Validation methods (testing, walkthroughs) planned

## Severity Calibration Guide (evidence-state separated — authoritative)
- Evidence status and severity are independent axes. Missing or inaccessible evidence is `Unknown/Untested`, never a pass and never proof of absence.
- **Critical**: demonstrated or strongly substantiated exposure that blocks delivery or risks material legal/security/safety/exclusion/operational harm, with a stated severity basis and impact rationale.
- **Major**: material impact or high-likelihood quality/cost/schedule/human/operational failure with supporting consequence analysis.
- **Minor**: limited impact, clarity, or polish issues.
- **Suggestion**: optional excellence improvement.
- Never raise severity solely because evidence is missing. For a mandatory control that is unverified, report it as unverified with `severity_basis: conditional_risk` and an explicit conditional consequence; separate severity from confidence and impact.


## 7. Integrated End-to-End + Human-Factors Milestone Gate
Use this compact gate on each material milestone; select the checks relevant to the stage, and record N/A with rationale rather than silently skipping them.
- [ ] Critical user journeys are identified and traced from user outcome → requirement → design/contract → test → runtime/operational signal.
- [ ] E2E test data, environment, baseline, relevant latency percentiles, and pass/fail thresholds are explicit for critical journeys.
- [ ] Core Web Vitals are treated as LCP, INP, and CLS; TTFB, FCP, and TBT are labeled supporting/diagnostic metrics, not Core Web Vitals.
- [ ] Reliability, error, security, recovery, and deployment signals are considered alongside functional success.
- [ ] Human factors are assessed for task success, cognitive/decision load, error prevention and recovery, accessibility, inclusion, satisfaction/trust, and operational maintainability.
- [ ] Usability observations state task, participant/context, sample, method, and success definition. If SEQ is used, confirm its 1–7 direction (1 = very difficult; 7 = very easy) and document the actual question.
- [ ] Accessibility evidence combines automation with relevant manual checks (keyboard/focus, screen reader, zoom/reflow, error and recovery states).
- [ ] Each metric states definition, unit, target rationale, data source, measurement window, owner, and relevant segmentation.
- [ ] Any missing data is labeled unknown/untested, not pass; residual risk and release decision are recorded.
- [ ] Recurrent failure patterns or evidence-backed skill gaps are considered for a normalized feedback event, with no direct automatic skill edits.

## 8. Optional Audit-to-Skill Feedback Event
When an audit will feed the composed skill set, normalize the material finding into `shared/contracts/audit-findings.schema.json`. New events use `schema_version: "1.1"` and require `audit_id`, ISO-8601 `audited_at`, project, and findings. Each finding needs a stable ID, title, allowlisted category, severity, status, evidence, source artifact, recurrence count, evidence status, confidence, verification method, as-of context, impact rationale, and severity basis. Legacy schema 1.0 is accepted by the processor for compatibility only. Set `skill_gap_suspected` only when evidence indicates a gap in skill instructions/checklists/triggers/contracts/tests; it must not be inferred simply because a project defect exists. Count recurrence across distinct audit observations, not duplicate lines in one report. Keep evidence state separate from severity; Critical/Major severity with unknown/untested evidence requires an explicitly conditional risk rationale and `severity_basis: "conditional_risk"`. See `shared/examples/audit-findings.sample.json` and `shared/references/feedback-loop.md`.

## 9. Multilingual, Adversarial & Near-Miss Trigger Review
- [ ] Matrix has ≥12 positive and ≥12 negative cases per member including Indonesian, adversarial, and near-miss families
- [ ] No prompt overlaps across labels after casefold/whitespace normalization; IDs are globally unique kebab-case
- [ ] Near-miss negatives (e.g., containing audit/skill keywords with different intent) are adjudicated with rationale, not keyword matching
- [ ] Any description change triggers a new dated runtime run per evaluation/runtime-protocol.md

## 10. Supply-Chain, Cost & Production-Readiness Spot Check
- [ ] SBOM-relevant dependencies pinned or explicitly justified; secrets handling and rotation evidenced or marked unknown/untested
- [ ] Cost-per-journey or token-budget reasoning present where scale matters; `scripts/measure-context.py` estimate recorded
- [ ] Release reproducibility (deterministic ZIP + SHA-256 + verify) and rollback owner evidenced or explicitly deferred with risk acceptance
