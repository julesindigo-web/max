---
name: backend-contract-data
description: Evolve an API contract, persistence schema, or migration. Use when changing server behavior, a public contract, stored data, or a job boundary.
---

# Backend Contract Data

Use this skill for API, service, persistence, queue, webhook, or migration work. Do not use it for a local-only UI concern.

1. Identify callers, trust boundaries, data classification, existing contract conventions, and compatibility requirements. Inspect the installed framework and repository patterns before selecting APIs or flags.
2. Validate untrusted input at the edge, reject unexpected or oversized fields where the contract requires it, and return stable user-safe errors. Enforce authorization on the server and at the object or tenant boundary.
3. Keep handlers thin. Put business rules in testable application or domain code; make timeouts, retries, idempotency, pagination, and concurrency decisions only where the operation needs them.
4. For a schema change, use the repository's migration mechanism. Prefer additive expand-migrate-contract steps, database constraints, and a rollback or explicit one-way plan. Do not run shared or production migrations without approval.
5. Verify affected contracts and negative authorization paths. For data-path changes, inspect the query shape or execution plan when performance or scale is material.

Stop for an externally visible breaking contract, data backfill with unknown impact, retention-policy change, shared database action, or a product decision about consistency or recovery semantics.
