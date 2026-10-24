# Latency and Security Budgets

Enforce these budgets as release gates for backend services.

## Hold Latency Budgets

- Hold p95 under 100ms for standard read and write operations at expected load.
- Hold p99 under 250ms for standard operations measured over at least 1000 requests.
- Set timeouts at 1000ms for internal calls and 2500ms for edge-facing operations.
- Alert when p95 exceeds 90ms for 5 consecutive minutes.
- Block release when p95 regresses by more than 15% versus baseline.

## Tune Queries Against Evidence

- Capture execution plans for every query above 50ms.
- Add one selective index at a time and re-measure before and after.
- Keep index count under 8 per high-write table unless evidence justifies more.
- Paginate results over 100 rows and cap page size at 200 rows.
- Cache repeated reads with time-to-live between 30 and 300 seconds.

## Encrypt Data Everywhere

- Require TLS 1.2 or higher for all service-to-service and client traffic.
- Require AES-256 or platform-equivalent encryption for databases, disks, and backups.
- Encrypt sensitive fields at the application layer for defense in depth.
- Verify encryption status in build, staging, and production on every release.
- Rotate keys and credentials within at most 90 days.

## Apply Least Privilege

- Map each operation to the minimum datastore and queue permissions.
- Separate read, write, and admin roles with no shared superuser.
- Scope secrets by service and environment with automatic expiry.
- Test that denied actions fail closed and emit audit events.
- Review access logs weekly for anomalous privilege use.

## Verify With Structured Logging

- Record latency, operation, identity, resource, and decision for sensitive actions.
- Ship logs to centralized storage within 60 seconds of emission.
- Retain security audit logs for at least 90 days.
- Alert on repeated authentication failures and privilege denials within 5 minutes.
- Cross-check log coverage against the shared telemetry contract before release.
