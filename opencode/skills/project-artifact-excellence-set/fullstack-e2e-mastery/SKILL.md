---
name: fullstack-e2e-mastery
description: Deliver production-grade fullstack systems from interface through domain to data with E2E verification. Use when starting new architectures or designing API contracts or optimizing data layers or assembling E2E validation. Triggers include build fullstack app or design system architecture or optimize database or create E2E flow or integrate frontend backend.
metadata:
  version: "1.0.0"
  set-membership: project-artifact-excellence-set
  depends-on:
    - project-artifact-auditor@>=2.0.0
    - test-automation-engineer@>=1.0.0
    - backend-engineering-excellence@>=1.0.0
    - frontend-engineering-excellence@>=1.0.0
  provides: []
---
# Fullstack E2E Mastery

## Purpose
Deliver production-grade fullstack systems from interface through domain to data with end-to-end verification. Compose client experience, API contracts, business logic, and persistence into coherent releases that meet functional and non-functional targets. Treat measurable quality attributes as acceptance criteria and apply human factors discipline so flows stay intuitive, resilient, and diagnosable across layers.
Execute upstream to downstream from client interface and state through contracts, domain services, data design, error boundaries, E2E validation, and hardening. Coordinate sibling skills for deep layer work and verify every release against audit metrics.

## Core Operating Principles
- Build upstream to downstream in order. Start from client interface and state, then define contracts, domain logic, and storage.
- Define contracts before implementation. Freeze interface shapes before coding handlers and views.
- Isolate domain logic from transport and persistence. Keep business rules testable without UI or database.
- Verify across layers with realistic end-to-end scenarios, not isolated unit checks alone.
- Optimize data access deliberately. Measure query shape, index use, and cache behavior before scaling.
- Handle errors at boundaries with explicit mapping from domain to transport to presentation.
- Coordinate with sibling capabilities including backend-engineering-excellence, frontend-engineering-excellence, and test-automation-engineer for deep layer work.
- Request audit review from project-artifact-auditor before production promotion.
- Measure quality attributes continuously with budgets, scans, and E2E timing on every change.
- Design for usability and accessibility from the first interface draft through final validation.

## Process
1. Capture the end-to-end flow. Record user goal, entry surface, steps, success outcome, and failure expectations.
2. Design the client interface and state. Define screens, components, state ownership, loading states, and optimistic updates.
3. Select protocols and contracts. Choose among REST, GraphQL, gRPC, and WebSocket per interaction and define schemas.
4. Design domain and application services. Define entities, use cases, validation rules, authorization checks, and events.
5. Design the data layer. Define models, indexes, transactions, migrations, caching, and retention.
6. Implement cross-layer error boundaries. Map domain errors to transport codes to user-facing messages with recovery actions.
7. Assemble E2E validation. Build scenario tests tied to ../project-artifact-auditor/references/fullstack-e2e-metrics.md covering happy path, edge cases, and failure injection.
8. Harden performance and security. Apply latency budgets and OWASP mitigations, then verify with measurements and scans.
9. Record release evidence. Attach contracts, migration logs, E2E results, and audit approvals to the release.

## Layered Execution
- Implement client interface first with mocked contracts to validate usability and state transitions early.
- Implement API handlers as thin adapters delegating to domain services.
- Keep domain modules free of HTTP, SQL, and framework imports.
- Implement persistence adapters with explicit query methods and transaction boundaries.
- Enforce dependency direction from outer layers toward domain core.
- Document layer responsibilities and allowed imports in references/fullstack-integration-standards.md.
- Review cross-layer state ownership to prevent duplication and stale caches.
- Validate each layer with focused tests before assembling the full E2E slice.
- Delegate deep frontend concerns to frontend-engineering-excellence and deep backend concerns to backend-engineering-excellence.

## Implementation Checklist
- Confirm interface mocks match frozen contracts before building handlers.
- Confirm domain services enforce validation and authorization without transport dependencies.
- Confirm persistence migrations run forward and backward cleanly on a copy of production shape.
- Confirm error mapping covers validation, auth, conflict, rate-limit, and server faults.
- Confirm E2E suite links each scenario to requirements, contracts, and audit metrics.
- Confirm performance budgets and OWASP checks pass with retained evidence.
- Request test-automation-engineer review for suite reliability and flake control.

## Architecture Patterns
- Select Clean Architecture for complex domains requiring long-term evolvability and testable business rules.
- Select Modular Monolith for early products needing deployment simplicity with enforced module boundaries.
- Select Event-Driven Architecture for asynchronous workflows, integration fan-out, and resilience through queues.
- Record the selected pattern, rationale, and trade-offs in an architecture decision record.
- Define module boundaries, public interfaces, and forbidden dependencies explicitly.
- Enforce boundary checks in CI to prevent architectural erosion.
- Consult references/architecture-patterns.md for pattern selection criteria and module rules.

## Protocol Selection
- Choose REST for resource-oriented CRUD with cacheable reads and broad client compatibility.
- Choose GraphQL for flexible client-driven queries with aggregated views and versioned schema evolution.
- Choose gRPC for high-throughput service-to-service calls with strict typed contracts.
- Choose WebSocket for bidirectional realtime updates with heartbeat, reconnect, and backpressure handling.
- Define authentication, pagination, filtering, error shape, and rate limits for the chosen protocol.
- Version contracts explicitly and document breaking-change policy.
- Document retry, timeout, and idempotency semantics for every mutating operation.
- Record protocol decision with latency, payload, and client-support rationale.

## Cross-Layer State and Error Boundaries
- Assign single ownership for each piece of state across client cache, server session, and database.
- Define invalidation rules for mutations, realtime events, and background refresh.
- Map domain errors to transport errors deterministically, then to localized user messages.
- Implement client error boundaries isolating failures to the affected view with retry and fallback.
- Implement server error boundaries preventing leakage of internal details while preserving diagnostic identifiers.
- Log correlation identifiers across client, API, domain, and data layers for traceable incidents.
- Test stale-cache, offline, and conflict scenarios explicitly in E2E suites.
- Document recovery actions for each error class with expected user outcome.

## E2E Scenario Strategy
- Derive scenarios from user journeys covering signup, core workflow, payment or critical action, and recovery flows where applicable.
- Tie acceptance thresholds to ../project-artifact-auditor/references/fullstack-e2e-metrics.md for coverage, reliability, and timing.
- Include contract tests, integration tests, and full browser or client-driven E2E tests in one traceable suite.
- Seed deterministic test data and isolate tests from shared mutable state.
- Measure E2E duration, flake rate, and defect escape rate on every run.
- Delegate suite automation patterns to test-automation-engineer for parallelization and quarantine design.
- Consult references/e2e-testing-playbook.md for scenario design, fixtures, and failure-injection patterns.

## Performance and Security Hardening
- Set latency budgets per layer and for full E2E flows, for example p95 under 500 ms for critical reads.
- Optimize data layer with indexes, query limits, connection pooling, and caching with explicit TTL.
- Apply OWASP mitigations including input validation, output encoding, auth checks, CSRF defense, and secret handling.
- Enforce authorization at domain layer, not only at UI or gateway.
- Scan dependencies, images, and IaC before release and block High and Critical findings.
- Retain load-test results, query plans, and scan reports as release evidence.
- Consult references/performance-and-security.md for budgets, checklists, and verification steps.

## Quality Attributes
Address quality attributes explicitly across all layers. Cover functionality through E2E scenario pass rate, performance through latency budgets, scalability through stateless services and indexed queries, reliability through retries and idempotency, security through authentication and OWASP controls, observability through tracing and structured logs, maintainability through modular boundaries, testability through contract and E2E suites, usability through consistent flows, and data integrity through transactions and migrations. Reject releases claiming quality attributes without measurements.

## Human Factors and Usability
Apply human factors and usability discipline across the fullstack experience. Design for cognitive clarity with predictable navigation, explicit loading and error states, and forgiving input handling. Reduce cognitive load with progressive disclosure, consistent terminology, and accessible feedback timing. Support accessibility with keyboard operation, focus management, sufficient contrast, and screen-reader announcements for dynamic updates. Validate with task-based usability checks covering onboarding, core task completion, error recovery, and mobile constraints.

## Success Metrics
- Trigger performance: Definition: correct activation on E2E slice assembly, layer integration, and production-verification requests (member evaluates across at least 20 positive and 20 negative prompts); Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: authoritative trigger matrix plus target-runtime activation logs; Sample: at least 20 positive and 20 negative prompts; Segmentation: per prompt family including positive, negative, and near-miss cases; Method: execute each frozen prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: representative fullstack tasks accepted with interface-through-domain-to-data verification per slice; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: E2E slice verification records; Sample: at least 10 representative fullstack tasks; Segmentation: by task type and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint for fullstack delivery (member completes tasks loading at most 2 reference files); Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled task traces; Sample: representative fullstack tasks; Segmentation: by task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: a new operator assembles a verified E2E slice in a guided evaluation; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: guided slice-assembly sessions; Segmentation: by operator experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial workflow changes
- Residual defect density: Definition: slice defects remaining after final validation (member baseline is zero Critical with at most 1 Major per 10 tasks tracked as an explicit exception when present); Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: slice validation records and exception log; Sample: all fullstack tasks in the release candidate; Segmentation: by severity and security/human/operational impact; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
## Failure Modes and Recovery
- Contract mismatch between frontend and backend breaks integration. Recover by freezing contracts, regenerating clients, and adding contract tests.
- Unbounded queries degrade latency under load. Recover by adding pagination, indexes, and query budgets with load-test confirmation.
- Shared mutable test data causes flaky E2E runs. Recover by isolating fixtures per scenario and resetting state between runs.
- Missing error boundaries expose raw failures to users. Recover by adding layered handlers, user-safe messages, and correlation identifiers.
- Inconsistent state across cache and database confuses users. Recover by defining ownership, adding invalidation hooks, and verifying with E2E refresh tests.
- Security control placed only in UI allows bypass. Recover by moving authorization into domain services and adding negative test cases.
- Event backlog grows without bound during downstream outage. Recover by adding dead-letter queues, replay procedures, and backpressure limits.
- Unversioned contract change breaks mobile clients. Recover by restoring compatibility, versioning the change, and publishing migration guidance.

## References
- references/architecture-patterns.md defines Clean Architecture, Modular Monolith, and Event-Driven selection and module rules.
- references/fullstack-integration-standards.md defines layer responsibilities, contract workflow, and state ownership.
- references/e2e-testing-playbook.md defines scenario design, fixtures, and failure-injection procedures.
- references/performance-and-security.md defines latency budgets, data-layer optimization, and OWASP mitigations.
- Submit fullstack designs to project-artifact-auditor for cross-layer consistency scoring.
- Retain contracts, migration history, and E2E evidence for at least 5 releases.
- Log protocol choices, state ownership, and budget decisions with rationale.
