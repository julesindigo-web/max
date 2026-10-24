# Performance and Security

## Purpose
Define latency budgets, data-layer optimization, and OWASP mitigations.

## Latency Budgets
- Set p95 under 500 ms for critical reads and under 1000 ms for writes.
- Allocate budgets per layer including client render, network, domain, and query.
- Measure with realistic data volumes and alert on 20 percent regression.
- Optimize largest contributor first with profiling evidence.

## Data-Layer Optimization
- Index filter, sort, and join keys used by hot queries.
- Paginate list endpoints with default limit at most 50 items.
- Use connection pooling and statement timeouts.
- Cache idempotent reads with explicit TTL and invalidation.
- Review slow-query logs weekly and fix top 5 offenders.

## OWASP Mitigations
- Validate and encode all inputs and outputs.
- Enforce authentication and least-privilege authorization in domain layer.
- Protect against injection, XSS, CSRF, SSRF, and broken access control.
- Store secrets in vaults with rotation at least every 90 days.
- Scan dependencies and images and block High and Critical findings.

## Verification
- Run load tests for peak traffic plus 50 percent headroom.
- Run auth negative tests for every privileged operation.
- Retain performance reports and scan evidence with each release.
