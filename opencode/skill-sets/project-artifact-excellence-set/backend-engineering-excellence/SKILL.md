---
name: backend-engineering-excellence
description: Engineer testable backend services with sub-100ms latency budgets and strict data encryption. Use when designing APIs or modeling domains or tuning queries or hardening service security. Triggers include build backend API or optimize latency or design domain service or secure endpoint or tune database query.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
  provides: []
---

# Backend Engineering Excellence

## Purpose
Deliver testable backend services that meet strict latency budgets and strong security guarantees. Provide procedural guidance for API design, domain service modeling, query tuning, and endpoint hardening that base model knowledge leaves underspecified. Treat measurable quality attributes as release gates and treat human factors as first-class for operators, reviewers, and API consumers. Reduce cognitive load with modular boundaries, explicit contracts, and observable behavior.
Use this skill when a backend task needs evidence-backed budgets rather than qualitative claims. Cover the full path from domain decision to deployed operation, including test strategy, security posture, persistence design, and production telemetry. Coordinate with project-artifact-auditor findings where audits flag backend gaps, and route frontend performance questions to the shared telemetry contract.
When latency and security compete, hold both budgets and change the design instead of waiving the gate. Record budget decisions, index rationale, and identity scopes so reviewers, operators, and future maintainers can reason about trade-offs without reverse-engineering the code.

## Core Operating Principles
- Enforce a p95 latency budget under 100ms for standard operations and measure every change against it.
- Design domain services for testability with small modules, explicit dependencies, and pure business rules.
- Encrypt all data in transit and at rest without exception and verify configuration in every environment.
- Apply least-privilege service identity to every workload, secret, queue, and datastore.
- Index deliberately for observed query patterns and prove improvement with execution plans.
- Emit structured logs, metrics, and traces through shared contract telemetry hooks.
- Prefer explicit contracts over implicit conventions across service boundaries.
- Reject unverified performance or security claims and demand evidence before release.
- Keep failure handling explicit with timeouts, retries with jitter, idempotency, and bulkheads.
- Document ownership, data sensitivity, and retention for every service and store.
- Review dependencies for freshness, license risk, and known vulnerabilities on a fixed cadence.
- Optimize for reviewer comprehension with small diffs, clear naming, and decision records.
- Bound background work with queues, visibility timeouts, and dead-letter handling.
- Separate configuration from code and validate it at startup with fail-fast errors.
- Paginate, filter, and sort server-side for collections that can exceed 100 items.
- Cap response payloads and compress large payloads to protect tail latency.
- Rehearse rollback and restore paths quarterly so release safety never depends on memory.

## Process
1. **Clarify service scope** — Capture operations, callers, data sensitivity, throughput targets, and latency budget. Declare what is out of scope.
   - Record expected requests per second, payload sizes, and growth headroom.
   - List upstream callers and downstream dependencies with owners.
   - Confirm compliance needs such as retention, residency, and audit trails.
2. **Model the domain** — Define bounded contexts, entities, value objects, and service operations. Isolate side effects from decision logic.
   - Place validation and policy rules in pure functions that are trivially unit testable.
   - Express state transitions explicitly with allowed events and guards.
   - Name concepts with ubiquitous language shared with API consumers.
3. **Design API contracts** — Specify resources, verbs, error shapes, versioning rules, pagination, and idempotency keys. Validate against consumer needs.
   - Define error codes for validation, authentication, authorization, conflict, rate limit, and downstream failure.
   - Set pagination defaults at 20 items with a maximum of 200 items per page.
   - Version breaking changes explicitly and support at least one prior version during migration.
4. **Design persistence** — Choose schema, keys, indexes, and consistency rules. Record expected query patterns and retention policy.
   - List the top 10 queries by frequency and latency before selecting indexes.
   - Separate hot read paths from write-heavy paths where contention appears.
   - Script every migration with forward steps, rollback steps, and data checks.
5. **Apply security controls** — Assign service identity, scope secrets, enforce transport encryption, enable at-rest encryption, and document access paths.
   - Grant only the datastore actions each operation requires, split by read, write, and admin.
   - Load secrets from a managed vault at startup with rotation within at most 90 days.
   - Verify TLS 1.2 or higher on every listener and client before release.
6. **Implement observability** — Add structured logging with correlation IDs, latency histograms, error counters, and trace spans per operation.
   - Log service, operation, correlation ID, duration in ms, identity, and outcome on each request.
   - Propagate trace context across queues, jobs, and downstream HTTP calls.
   - Dashboard p50, p95, and p99 latency plus error rate by operation.
7. **Verify budgets** — Run load checks, review p50 and p95 and p99 latencies, inspect slow queries, confirm index usage, and remediate regressions.
   - Measure with at least 1000 sampled requests at expected load before sign-off.
   - Block release when p95 regresses by more than 15 percent versus baseline.
   - Re-test after every index, cache, or query-shape change.
8. **Harden and release** — Execute threat review, dependency check, test suite, rollback plan, and production health checklist before rollout.
   - Confirm contract tests pass for every consumer-facing change.
   - Stage rollout with canary traffic and automatic rollback on SLO burn.
   - Schedule a post-release latency and error review within 7 days.
9. **Record and hand off** — Publish contracts, budgets, dashboards, and runbooks where operators and consumers can find them.
   - Attach evidence links for load results, security checks, and coverage reports.
   - Name owners and review dates for every budget, identity grant, and index decision.

## Quality Attributes
Maintain these quality attributes as binding constraints for every backend change.
- Performance — Hold p95 under 100ms for standard reads and writes at expected load. Hold p99 under 250ms. Measure with at least 1000 sampled requests.
- Testability — Keep domain logic free of I/O. Inject clocks, IDs, and external clients. Cover critical paths with unit plus contract plus integration tests.
- Security — Require TLS 1.2 or higher in transit. Require AES-256 or platform-equivalent encryption at rest. Rotate credentials within at most 90 days.
- Reliability — Define timeouts, retries with jitter, idempotency, and circuit breaking for every downstream call. Confirm recovery in at least 99 percent of injected failures.
- Observability — Log in structured JSON with service, operation, correlation ID, duration, and outcome. Export latency and error metrics with consistent names.
- Maintainability — Limit service module size, document ownership, and keep migration and rollback scripts versioned. Record decisions that affect future evolution.
- Composability — Publish versioned contracts and validate breaking changes with contract tests before deployment. Support one prior version during migration.
- Data integrity — Enforce constraints, transactional boundaries, and reconciliation checks for money, inventory, and identity data. Test rollback paths.
- Cost awareness — Track per-operation compute, storage, and egress cost drivers. Cap expensive scans with limits and caching policies.
- Operability — Ship runbooks, dashboards, and rollback steps with every service so on-call responders can act within 5 minutes.
- Compatibility — Version contracts explicitly, support one prior version during migration, and announce breaking changes at least 30 days ahead.
- Auditability — Record schema changes, access grants, and data-handling decisions with dates and owners for traceability.

## Human Factors and Usability
Reduce operator and consumer cognitive load across design, review, incident response, and evolution.
- Write error responses that state what happened, what the caller can do next, and where to find help.
- Keep configuration explicit, documented, and reviewable without tribal knowledge.
- Name operations, fields, and metrics with consistent domain language that matches user mental models.
- Surface health, latency, and error signals in dashboards that support fast diagnosis under pressure.
- Document runbooks with preconditions, commands, expected output, and rollback steps for on-call usability.
- Design admin and review workflows with progressive disclosure so routine tasks stay simple and advanced controls stay reachable.
- Protect trust with clear data-handling statements, audit trails, and least-privilege defaults that remain legible to non-specialists.
- Keep API reference examples runnable, with authentication, pagination, error, and retry samples for every major operation.
- Announce breaking changes with migration guides, timelines, and dual-version support windows of at least 30 days.
- Review alert wording for clarity so a tired responder can act within 5 minutes without searching for context.
- Keep onboarding paths short with a runnable example, seeded data, and one guided end-to-end call.
- Ask for explicit confirmation before destructive operations and show exact blast radius in the prompt.

## Success Metrics
- Trigger performance: Definition: correct activation on API design, domain modeling, query tuning, and endpoint-hardening requests (member samples at least 20 backend prompts per 30-day window); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 sampled backend prompts per 30-day window; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: scoped API plus domain plus query plus security tasks completed with passing tests and budgets per engagement; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: service design records with test and budget evidence; Sample: scoped engagements with test and budget verification; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for backend design (member keeps SKILL.md near 190 lines and cuts context use by at least 30 percent versus full manual review); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: typical design tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a competent engineer produces a budgeted and tested service design on a bounded problem; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: bounded-problem design sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: production escapes and critical security gaps remaining within 30 days after release (member standard is at most 1 escape per 1000 requests with zero known critical gaps); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: escape and gap registers with p95 measurements over at least 500 requests; Sample: all releases in the observation window; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Missed latency budget — Profile hot path, inspect query plans, add or revise indexes, cache repeated reads, split heavy operations, then re-measure p95 over at least 500 requests.
- Untestable domain logic — Extract pure functions, invert dependencies, replace hidden time and randomness with injectable ports, then add unit tests.
- Missing encryption coverage — Inventory data flows, enable transport and at-rest encryption, verify with config audit, rotate exposed secrets, then re-verify.
- Overprivileged identity — Audit roles, narrow to minimum actions and resources, scope by environment, test denial paths, then monitor access logs for 7 days.
- Slow queries — Capture execution plans, add selective indexes, constrain result sets, paginate large scans, then confirm improvement with before and after metrics.
- Noisy or sparse telemetry — Standardize log schema, require correlation IDs, add missing spans and counters, then validate end-to-end trace continuity.
- Brittle contracts — Freeze current schema, add contract tests with consumers, version the next change, then publish a migration guide with dual support.
- Cache stampede — Add jittered expiry, request coalescing, and negative caching with short time-to-live, then load-test the hot key path.
- Secret sprawl — Centralize secrets in a vault, remove copies from code and logs, rotate affected credentials, then verify with a secret scan.
- Migration risk — Test migrations on a production copy, add backward-compatible steps, prepare rollback scripts, then run during a guarded window.
- Connection exhaustion — Pool connections, bound concurrency, add queue timeouts, then load-test at 2x expected peak traffic.
- Stale ownership — Reassign unowned services, update runbooks and dashboards, then confirm on-call routing within one rotation.

## References
- Backend service patterns: references/backend-patterns.md
- Latency budgets and security controls: references/latency-and-security-budgets.md
- Shared telemetry contract hooks: ../shared/contracts/audit-findings.schema.json
- Unified remediation playbook: ../shared/references/unified-remediation-playbook.md
