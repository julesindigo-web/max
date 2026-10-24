# Full-Stack End-to-End Project Development — Maximal Metrics, Quality Attributes & Checklists


## Contents
- [1. Product / Discovery](#1-product--discovery--requirements-metrics)
- [2. Architecture quality attributes](#2-architecture-quality-attributes-iso-25010--modern)
- [3. Frontend](#3-frontend-technical-metrics)
- [4. Backend](#4-backend--service--domain-metrics)
- [5. Data layer](#5-data-layer-metrics)
- [6. Security](#6-security-full-stack-metrics)
- [7. Testing](#7-testing-strategy-metrics)
- [8. CI/CD and DORA](#8-cicd-release--deployment-metrics-current-dora-five-metric-model--complementary-measures)
- [9. Observability](#9-observability--sre-metrics)
- [10. Reliability](#10-reliability--resilience-metrics)
- [11. Performance](#11-performance--scalability-metrics)
- [12. Maintainability](#12-maintainability--technical-debt-metrics)
- [13. Cost and FinOps](#13-cost--finops-metrics)
- [14. Compliance](#14-compliance-governance--auditability)
- [15. Team and process](#15-team-process--knowledge-metrics-space--dora-complementary)
- [Cross-cutting questions](#cross-cutting-checklist-questions-ask-of-every-major-artifact)
- [16. Evidence contract](#16-combined-e2e-and-human-factors-evidence-contract)

This reference provides metric/checklist coverage across the full software/web/full-stack lifecycle. Use it to drive dimensional sweeps and demand measurable statements in artifacts. Pair the technical E2E assessment with `human-factors-usability.md` and the milestone framework in `../../shared/references/holistic-evaluation.md`; technical success and human outcomes must be evidenced separately.

## 1. Product / Discovery / Requirements Metrics
- Outcome metrics linked to leading & lagging indicators
- Opportunity sizing / value hypotheses
- Jobs-to-be-done completeness
- Persona coverage (primary + extreme)
- Requirement quality: SMART / INVEST / testable acceptance criteria ratio
- Ambiguity density (weasel words per page)
- Traceability coverage % (req → design → test → ops)

## 2. Architecture Quality Attributes (ISO 25010 + modern)
- Performance efficiency (response time, throughput, resource utilization)
- Compatibility, Interoperability
- Usability (already covered in human-factors reference)
- Reliability (availability, fault tolerance, recoverability) — SLO/SLI/Error Budget
- Security (confidentiality, integrity, non-repudiation, accountability, authenticity)
- Maintainability (modularity, reusability, analysability, modifiability, testability)
- Portability
- Scalability (horizontal/vertical, elasticity)
- Observability (logs, metrics, traces, continuous profiling)
- Evolvability / Changeability
- Cost efficiency (FinOps)

Every quality attribute in an architecture document SHOULD have at least one concrete scenario + measurable response measure + verification method.

## 3. Frontend Technical Metrics
- **Core Web Vitals (field metrics):** Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS). Assess the 75th percentile of real-user page loads, segmented by mobile and desktop; current “good” thresholds are LCP ≤2.5 s, INP ≤200 ms, and CLS ≤0.1.
- **Supporting / diagnostic performance metrics:** Time to First Byte (TTFB) and First Contentful Paint (FCP) help diagnose loading performance (including LCP); Total Blocking Time (TBT) is a lab diagnostic/proxy for potential responsiveness issues. TTFB, FCP, and TBT are not Core Web Vitals.
- Bundle size & code-splitting effectiveness
- Accessibility conformance (WCAG 2.2 AA/AAA + cognitive)
- Component contract completeness (states, a11y, error, loading, empty)
- State management complexity & predictability
- Offline / resilient UI behaviour
- Design-token & design-system adherence
- Cross-browser / device matrix coverage

## 4. Backend / Service / Domain Metrics
- Domain model purity & bounded-context clarity
- API design quality (consistency, versioning, error model, idempotency, pagination)
- Transactional integrity & consistency guarantees
- Service level objectives per endpoint or use-case
- Dependency health & blast-radius analysis
- Asynchronous / event-driven correctness (idempotency, ordering, DLQ)

## 5. Data Layer Metrics
- Data model normalisation / denormalisation rationale
- Consistency model (strong, eventual, causal) explicitly stated
- Migration safety & rollback
- Retention, archival, legal-hold, privacy-by-design
- Query performance budgets
- Cache invalidation strategy
- Backup / restore RPO-RTO and tested recovery

## 6. Security Full-Stack Metrics
- Threat model existence & coverage (STRIDE or equivalent)
- Authentication / Authorization / SoD completeness
- Secrets management & rotation
- Supply-chain security (SBOM, dependency scanning, signing)
- Data classification & encryption (in transit / at rest / in use)
- Vulnerability management SLAs
- Security testing coverage (SAST, DAST, SCA, penetration, abuse cases)
- Audit logging completeness & integrity

## 7. Testing Strategy Metrics
- Test pyramid balance (unit / integration / E2E ratios)
- Critical-path coverage
- Contract testing existence
- Performance / load / stress / soak test design
- Chaos / resilience experiment catalogue
- Accessibility test automation + manual matrix
- Security test coverage
- Flakiness rate & quarantine policy
- Mutation testing or equivalent strength indicators (where applicable)

## 8. CI/CD, Release & Deployment Metrics (current DORA five-metric model + complementary measures)
DORA's current software-delivery performance model has five metrics grouped into throughput and instability:
- **Throughput:** deployment frequency; change lead time (from code commit to successful production deployment); failed deployment recovery time (time to recover from a deployment that causes production degradation and requires remediation).
- **Instability:** change fail rate (share of production changes requiring immediate intervention such as rollback or hotfix); deployment rework rate (share of deployments that are unplanned work to address a user-facing production bug).
- **Complementary release/operations measures, not additional members of the DORA five:** rollback success rate and time, environment parity, progressive delivery / feature-flag strategy, and release evidence / audit-trail completeness.
- Do not substitute generic incident MTTR for failed deployment recovery time without documenting the different scope; the DORA metric specifically ties recovery to a failed deployment.

## 9. Observability & SRE Metrics
- SLI / SLO / Error Budget policy
- Golden signals (latency, traffic, errors, saturation) + business KPIs
- Alert quality (precision, recall, fatigue)
- Incident response runbook coverage & testedness
- Distributed tracing coverage
- Continuous profiling / continuous verification
- On-call load & toil measurement

## 10. Reliability & Resilience Metrics
- Availability targets per critical user journey
- Fault-injection / chaos experiment results
- Graceful degradation behaviour
- Multi-region / multi-AZ strategy
- Data durability guarantees
- Recovery Time / Point Objectives (RTO/RPO) per critical data class

## 11. Performance & Scalability Metrics
- Latency percentiles (p50/p95/p99) under defined load
- Throughput & concurrency limits
- Resource efficiency (CPU, memory, cost per transaction)
- Auto-scaling behaviour & cool-down
- Capacity planning model
- Performance regression gates in CI

## 12. Maintainability & Technical Debt Metrics
- Code quality gates (complexity, duplication, coverage thresholds)
- Architectural fitness functions
- Dependency freshness & vulnerability age
- Documentation freshness (code ↔ docs drift)
- Onboarding time for new engineers
- Change failure attribution to debt items

## 13. Cost & FinOps Metrics
- Cost per critical user journey or transaction
- Unit economics visibility
- Waste identification (idle resources, over-provisioning)
- Budget vs actual with alerting
- Cost allocation by team / product / environment

## 14. Compliance, Governance & Auditability
- Regulatory / standard mapping completeness
- Change-control evidence trail
- Access review cadence & completeness
- Data subject rights / privacy request handling
- Audit log immutability & retention
- Policy-as-code coverage

## 15. Team, Process & Knowledge Metrics (SPACE / DORA complementary)
- RACI clarity for critical decisions
- Decision log completeness
- Knowledge continuity (bus factor, handover quality)
- Collaboration friction indicators
- Learning & post-incident improvement rate

## Cross-Cutting Checklist Questions (ask of every major artifact)
- Is every critical quality attribute measurable and verified by a named method?
- Does every interface have an explicit contract and failure mode?
- Is there bidirectional traceability from outcome → requirement → design → test → runtime signal?
- Are human costs (cognitive, emotional, inclusion) and operational costs (toil, MTTR, cost) both visible?
- What happens when this component or assumption fails? Is the failure mode designed and observable?
- Can a new team member or auditor reconstruct the “why” from the artifacts alone?

## Severity Calibration Addendum (Full-Stack)
- **Critical**: An inspected design or corroborated runtime state demonstrates a missing threat model for an internet-facing surface, absent SLOs for critical journeys, no recovery path for critical data, violated safety/authority invariants, major accessibility exclusion of core users, or possible silent data loss. An unavailable document alone is `Unknown/Untested`, not proof the control is absent.
- **Major**: Evidence substantiates material lack of performance/scalability measurement, incomplete critical-path testing, absent observability for golden signals, high cognitive load on frequent tasks, absent cost visibility, or weak change control. Where the source was not inspectable, state the conditional risk and lower confidence accordingly.
- **Minor**: Incomplete ADRs, missing secondary metrics, documentation drift, polish issues.
- **Suggestion**: Additional fitness functions, advanced chaos experiments, deeper FinOps allocation, excellence-level inclusive design.


## Metric Definition Sources (checked 2026-10-15)
- DORA, *DORA's software delivery performance metrics*: https://dora.dev/guides/dora-metrics/
- DORA, *A history of DORA's software delivery metrics*: https://dora.dev/insights/dora-metrics-history/
- Google web.dev, *Web Vitals*: https://web.dev/articles/vitals
- Nielsen Norman Group, *Beyond NPS: SUS, NASA-TLX, and the Single Ease Question*: https://www.nngroup.com/articles/measuring-perceived-usability/


## 16. Combined E2E and Human-Factors Evidence Contract
For critical journeys, require the trace `user outcome → requirement → design/contract → automated/manual test → runtime signal` and record any broken link. A missing trace in an inspected repository can demonstrate a traceability gap; an inaccessible or absent source document is only an evidence gap until absence and exposure are substantiated. Do not automatically equate “not evidenced” with “does not exist.” Use `../../shared/references/holistic-evaluation.md` as the cross-cutting milestone gate and `human-factors-usability.md` for detailed user/accessibility checks. Each metric should name its definition, unit, target rationale, environment, data source, sample/population, segmentation, owner, and observation window. Missing evidence is unknown/untested, not a pass. Never substitute proxy metrics for the outcomes they approximate (for example, TBT is not field INP, and a completed checklist is not proof of task success).
