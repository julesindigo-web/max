---
description: Deliver a verified full-stack vertical slice with explicit contracts and task-matched evidence
agent: fullstack-delivery
subtask: true
---
Deliver `$ARGUMENTS` as the smallest complete vertical slice. This command is for work that crosses, or must explicitly coordinate, interface, API/contract, domain, data, or E2E behavior.

First inspect the local instructions, architecture, contracts, migrations, tests, and scripts. Define observable acceptance criteria and trace the request from input through validation, authorization, domain logic, persistence/integrations, and user feedback. Implement only the affected boundaries; preserve backwards compatibility unless the request says otherwise.

Use `fullstack-e2e-mastery` as the coordinator. Load frontend/accessibility, backend/documentation, security, observability, or test-automation depth only when their boundary is touched. Execute the relevant AGENTS.md §8.6 checks; use focused checks first, then broaden based on risk. Production, deployment, paid, shared-data, destructive, or credential actions remain blocked pending explicit user authorization.

Report in AGENTS.md §12.3 order. State exact commands and observed results; label anything not run as Unknown/Untested with its reason and the next command.

Examples: `/fullstack-deliver add a tenant-scoped invoice export with UI status and API authorization`; `/fullstack-deliver fix checkout confirmation state drifting after webhook retry`.

Success criteria: acceptance criteria cover every touched boundary; validation and authorization are server-side; affected UI states and error recovery exist; relevant contract/data/E2E evidence is reported; no unrun or external action is represented as complete.
