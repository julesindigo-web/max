# E2E Testing Playbook

## Purpose
Define scenario-driven end-to-end validation tied to audit metrics.

## Scenario Design
- Cover happy path, boundary inputs, authorization denials, and failure injection.
- Prioritize signup, core workflow, critical transaction, and recovery flows.
- Keep each scenario independent with explicit setup and teardown.
- Align thresholds with ../project-artifact-auditor/references/fullstack-e2e-metrics.md.

## Fixtures and Data
- Seed deterministic users, catalogs, and balances per scenario.
- Isolate mutable state with per-run namespaces or transactions.
- Clean up test artifacts within 5 minutes of run completion.
- Version fixture schemas alongside API contracts.

## Execution
- Run contract tests before integration tests before browser E2E tests.
- Retry only network-flaky steps up to 2 times with recorded reason.
- Capture screenshots, traces, and logs on failure.
- Keep full suite p95 duration within team budget.

## Failure Injection
- Inject API errors, latency spikes, and offline modes for resilience checks.
- Verify error boundaries, retry behavior, and user messaging.
- Confirm no data corruption after injected faults.

## Reporting
- Publish pass rate, flake rate, duration, and defect escape rate.
- Link failures to scenario, layer, and commit.
- Block release on zero Critical escapes and agreed Major limits.
