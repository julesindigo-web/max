# Architecture Patterns

## Purpose
Guide selection among Clean Architecture, Modular Monolith, and Event-Driven options.

## Select Clean Architecture
- Choose for complex domains with long lifespan and heavy business rules.
- Isolate entities and use cases from frameworks and delivery mechanisms.
- Enforce dependency direction toward domain core.
- Document ports and adapters for UI, API, database, and external services.

## Select Modular Monolith
- Choose for early products needing single deployment with clear boundaries.
- Define modules with public interface and private internals.
- Forbid cross-module database access and UI coupling.
- Plan extraction path to services with recorded triggers.

## Select Event-Driven
- Choose for async workflows, notifications, and integration fan-out.
- Define events with versioned schemas and ownership.
- Implement idempotent consumers with dead-letter handling.
- Record ordering, delivery, and retention guarantees.

## Decision Record
- Record context, options, decision, rationale, and consequences.
- List measurable trade-offs for latency, complexity, and operability.
- Set review date after 90 days or 3 releases.

## Verification
- Inspect imports to confirm boundary compliance.
- Run module or layer tests on every change.
- Track coupling metrics and review quarterly.
