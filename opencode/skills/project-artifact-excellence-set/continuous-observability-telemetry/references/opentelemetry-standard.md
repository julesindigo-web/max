# OpenTelemetry Standard

Instrument backend and frontend with consistent OpenTelemetry signals.

## Install and Configure

- Add OpenTelemetry SDKs for each backend runtime and the web client.
- Enable W3C trace context and baggage propagators everywhere.
- Set service name, version, and environment as resource attributes.
- Sample head-based at 100% for errors and 10% to 25% for high-volume success.
- Ship data to the same collector endpoint across environments.

## Name Spans and Attributes

- Name spans as service plus operation, for example checkout-authorize.
- Mark span status from actual outcome, never default to success on error.
- Attach user, tenant, route, operation, and outcome as low-cardinality attributes.
- Never place passwords, tokens, or personal data in spans or logs.
- Keep attribute count under 15 per span to control cost.

## Unify Logs and Metrics

- Include trace ID and span ID on every structured log line.
- Emit request count, error count, and duration histogram per operation.
- Record frontend navigation, LCP, INP, CLS, and client errors with session ID.
- Use consistent field names that match shared telemetry contracts.
- Validate log-to-trace jumps on at least 5 sampled requests per service.

## Propagate Context

- Forward trace headers across HTTP, queues, and background jobs.
- Create child spans for database, cache, and downstream calls.
- Record queue wait time separately from processing time.
- Confirm end-to-end continuity from browser to backend to datastore.
- Fix breaks at the first service that drops or rewrites headers.

## Verify Pipeline Health

- Deliver metrics within 60 seconds and logs within 90 seconds normally.
- Buffer telemetry locally during collector outages for at least 15 minutes.
- Monitor collector error rate and ingest lag with dedicated alerts.
- Test instrumentation on every release with trace assertions.
- Document ownership and retention for each signal source.
