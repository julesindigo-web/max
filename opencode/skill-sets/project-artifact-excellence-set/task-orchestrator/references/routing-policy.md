# Routing Policy — task-orchestrator

Authoritative family-to-skill map. The classifier script implements this table; this file is the human-readable source of truth. On conflict, this file wins over script comments.

## Family map
- Audit/review/gap analysis → `project-artifact-auditor` (`/audit`, `@auditor`).
- Skill authoring/composition → `skills-create-excellence` (`/new-skill`, `@skill-builder`).
- Tests/coverage/E2E/visual regression → `test-automation-engineer` (`/vis-diff` visual, `@test-runner`).
- Refactoring/complexity → `code-refactoring-optimizer` (primary + skill).
- OWASP/secrets/auth/deps → `security-vulnerability-auditor` (primary + skill).
- Docs/OpenAPI/diagrams → `architecture-documentation-generator` (primary + skill).
- WCAG/ARIA/keyboard → `accessibility-inclusive-design` (primary + skill).
- OTel/SLO/alerts → `continuous-observability-telemetry` (primary + skill).
- Backend API/domain/latency → `backend-engineering-excellence` (primary + skill).
- Web Vitals/client state → `frontend-engineering-excellence` (primary + skill).
- Art direction/motion → `human-centric-visual-excellence` (primary + skill).
- Containers/CI-CD/gates → `deployment-devops-orchestrator` (primary + skill).
- Fullstack slices/contracts → `fullstack-e2e-mastery` (primary + skill).
- Unclear/multi-skill/no-slash → `task-orchestrator` (primary routes first).

## Tie rules
1. Higher corroborated-signal count wins; minimum 2 signals for a single-skill route.
2. Exact ties break by manifest order (auditor first, orchestrator last).
3. Overlapping frontend/visual/accessibility evidence routes all supported skills together, accessibility first.
4. Requested-name mapping applies before scoring: review-agent → audit, plugin-creator → new-skill, customize-opencode → routing + new-skill. Never invent new skills.

## Composition order
Security + tests pass before deployment orchestration. Accessibility passes before frontend or visual excellence claims. Audit findings feed domain skills bottom-up.
