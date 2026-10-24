---
name: fullstack-change
description: Implement a scoped cross-tier feature or bug fix. Use when one outcome changes both client and server, API, or data behavior.
---

# Fullstack Change

Use this skill only for a true cross-tier change or when the user explicitly asks for full-stack delivery. Do not use it for a single isolated UI, API, documentation, or configuration edit.

1. Identify the user-visible outcome, affected actors, acceptance criteria, and non-goals. Read applicable repository guidance and trace only the code path needed to understand the change.
2. Map the contract across the boundary: UI state and request, input validation, authorization, application logic, persistence or integration, response/error shape, and user feedback. Preserve compatibility unless the user requests a breaking change.
3. Make the smallest coherent vertical change. Keep validation and authorization server-side; do not trust client-supplied roles, identifiers, prices, or state.
4. Cover applicable states end to end: loading, empty, error, success, retry/partial failure, long content, and unauthorized access. Keep UI semantics, focus behavior, and keyboard access intact.
5. Verify the contract and the affected journey with repository-native checks. Use `$change-verification` when the user asks for a formal validation or handoff pass.

Stop for a material product choice, an unsafe or irreversible action, a production/shared-system operation, or an unresolved compatibility decision. Do not create a new service, dependency, migration, commit, or deployment merely to complete the workflow.
