# Fullstack Integration Standards

## Purpose
Define layer responsibilities and contract-first integration workflow.

## Layer Responsibilities
- Assign presentation to components, routing, and client state.
- Assign API edge to auth, validation, mapping, and rate limiting.
- Assign domain to entities, use cases, policies, and events.
- Assign persistence to models, queries, migrations, and cache adapters.

## Contract Workflow
- Draft contracts from UI needs and domain capabilities jointly.
- Freeze versioned schemas before parallel implementation.
- Generate clients and server stubs from schemas where feasible.
- Add contract tests blocking breaking changes.

## State Ownership
- Declare single owner for each state element.
- Define cache keys, TTL, and invalidation triggers explicitly.
- Propagate server changes via events or revalidation hooks.
- Avoid duplicating derived state across layers.

## Error Mapping
- Define domain error codes independent of transport.
- Map domain errors to HTTP or protocol codes deterministically.
- Present user-safe messages with recovery actions.
- Include correlation identifiers in logs, never in user details.

## Verification
- Confirm allowed imports per layer in code review.
- Confirm every contract change updates clients, tests, and docs.
- Measure integration defect rate per release.
