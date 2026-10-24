---
description: Build a feature or scope end-to-end through the full-stack verification matrix
---
Run the feature playbook for $ARGUMENTS (the scope, feature brief, or problem statement).

1. Orient and specify. Read the relevant code, migrations, contracts, and tests first. Restate goal, non-goals, and testable acceptance criteria. For multi-file work keep a checklist plan.
2. Design thin. Choose the smallest architecture satisfying the full-stack practice law (AGENTS.md §8). Record decisions as an ADR only if they bind future work. Greenfield without a stack: default per AGENTS.md §8.1 and verify current stable versions before pinning.
3. Implement in vertical slices that stay runnable: contract/data model first, then tests, then logic, then UI. Each slice passes at least typecheck and tests before the next.
4. Verify per AGENTS.md §8.6 matrix: typecheck, lint, format; unit; affected integration including authz negative cases; component/E2E for the touched journey; axe plus keyboard-only pass and loading/empty/error state capture for UI changes; migrate up (and down if supported) on empty and seeded DBs; bundle delta for dependency or UI changes.
5. Security pass before delivery: AGENTS.md §8.5 diff review (new endpoints without authz, string-built queries, new outbound calls, secrets in logs, removed checks). Invoke `security-vulnerability-auditor` for auth, payments, uploads, or third-party trust changes.
6. Deliver the report format of AGENTS.md §12.3: outcome first, changes by behavior, verification commands with observed results, decisions and assumptions, risks and follow-ups.

Use the canonical depth skills by routing table (AGENTS.md §2): `fullstack-e2e-mastery` for the system flow, `frontend-engineering-excellence` / `backend-engineering-excellence` / `architecture-documentation-generator` for their domain slices. For a greenfield repo without AGENTS.md, scaffold from the project template (AGENTS.md §10) before writing code.

Success criteria: acceptance criteria are demonstrably met or listed as waived; no threshold, test, or gate was weakened to pass; anything not run is named with the reason.
