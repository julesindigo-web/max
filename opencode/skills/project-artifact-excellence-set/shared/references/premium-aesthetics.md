# Premium Aesthetics (Shared)

Shared visual-excellence language for `human-centric-visual-excellence`,
`frontend-engineering-excellence`, and audit members. Beauty is measured
through human outcomes, not adjectives.

## Spatial System
- Modular type scale with a fixed ratio. Spacing tokens derived from the
  same base unit. Golden-ratio proportions where they reduce visual noise.
- Strategic whitespace separating task groups. Density must serve scanning
  speed, verified by task-completion evidence rather than taste claims.

## Visual Ergonomics
- Contrast and readability per `accessibility-standard.md`. Line length and
  type size tuned for sustained reading. Transitions under 300ms unless
  the motion carries meaning.
- Progressive disclosure for advanced controls. Destructive actions always
  confirmable and reversible.

## Motion and Emotion
- Micro-interactions acknowledge every user action within one frame budget.
  Organic easing curves for luxury feel. Reduced-motion preferences honored.
- Palette and tone aligned to trust and calm. Every aesthetic choice names
  the user emotion it supports and how it is validated.

## Verification Method
- Pair each aesthetic claim with a human-factors check from
  `project-artifact-auditor/references/human-factors-usability.md`.
  Untested luxury claims are marked unknown, never passed.

## Acceptance Gates for Capabilities 01–05 (PA-DOC-09)

| Capability | Gate (measurable) | Evidence artifact | Threshold |
|---|---|---|---|
| 01 ui-art-director | Signed Art Brief before code; blind brand-recall | `art-brief.md` versioned per release | Recall at least 80 percent on 5 respondents |
| 02 design-system-architect | Zero one-off values; component state matrix | `design-tokens-and-components.md` plus token-lint PASS | 100 percent components render all applicable states |
| 03 premium-frontend-engineer | LCP/INP/CLS budgets; 3-state screenshots; component budget | Web Vitals snapshots plus route screenshots | LCP at most 2500ms, INP at most 200ms, CLS under 0.1; zero undocumented components |
| 04 responsive-accessibility-engineer | Keyboard-10 journeys; AT log; device matrix | `evaluation/a11y-device-log-YYYY-MM-DD.md` | 100 percent scoped flows with AT log; zero critical barriers over 14 days |
| 05 visual-regression-auditor | Live MCP screenshots; baseline diff; P0–P3 labels | Diff report per runbook with approver decision | Zero open P0 at release; re-baseline only with approval |
