# Backend Patterns

Apply these patterns when shaping APIs, domain services, and persistence.

## Define Modular Domain Services

- Isolate each bounded context in its own module with explicit public operations.
- Place business rules in pure functions free of network and clock access.
- Inject repositories, clients, clocks, and ID generators through constructor ports.
- Return typed results that distinguish success, validation failure, and downstream failure.
- Version service interfaces and record breaking changes in a changelog.

## Shape Testable APIs

- Specify request, response, and error schemas before implementation.
- Require idempotency keys for unsafe retries on creation and payment paths.
- Use cursor pagination for collections larger than 50 items.
- Return machine-readable error codes plus human-readable recovery hints.
- Cover contracts with consumer-driven tests on every breaking-change candidate.

## Model Persistence for Observed Queries

- List the top 10 queries by frequency and latency before choosing indexes.
- Prefer narrow composite indexes that match filter plus sort order.
- Constrain unbounded scans with limits, cursors, and time bounds.
- Separate write models from read projections where contention grows.
- Script migrations with forward and rollback steps and test on a copy.

## Harden Service Identity

- Assign one identity per deployable service and environment.
- Grant only the actions and resources required for declared operations.
- Store secrets in a managed vault and load them at startup.
- Deny default network egress and allow only declared dependencies.
- Audit role assignments every 30 days and remove unused grants.

## Emit Structured Telemetry

- Log service, operation, correlation ID, duration in ms, and outcome on every request.
- Increment error counters by operation and error class.
- Record latency histograms with p50, p95, and p99 buckets.
- Propagate trace context across queues and downstream calls.
- Align field names with the shared contract telemetry schema.
