# Accessibility and Device-Matrix Log — 2026-10-15 (PA-RSP-04)

Per-release evidence log for responsive plus accessibility claims. Structure
is `Verified` (this file and its matrix exist and are inspected); product-UI
results below are honestly marked pending where no product UI is in scope.

## Device-Behavior Matrix (required per journey)

- Phone 360px: touch input, safe-area insets, portrait plus landscape,
  tap targets at least 44px, hover affordances replaced with touch equivalents.
- Tablet 768px: touch plus optional keyboard, split-view behavior, focus
  order re-verified (visual order may differ from phone).
- Desktop 1440px: pointer plus keyboard, hover states present, focus-visible
  ring at 3 to 1 contrast against adjacent colors.
- Record per journey: viewport, input modality, orientation, text scaling,
  and any breakpoint-specific defect with severity.

## Assistive-Technology Run (required per release)

- Screen reader plus version plus browser (at least one combination),
  keyboard-only completion across at least 10 core journeys, focus order
  and focus-return on dialogs, live-region politeness on async updates.
- Contrast tool plus version per theme (4.5 to 1 body, 3 to 1 large text
  and essential graphics), 200 percent zoom with reflow check, reduced-motion
  final-state check.
- Remaining gaps filed with severity, owner, and fix date; re-audit within
  90 days.

## This Release Entry

- Scope: skill-set release validation (no product UI ships with this set),
  so no AT run attaches here. Status for product-UI claims: `Unknown/Untested`.
- Verified instead: trigger matrix 228 cases PASS, token-contract gate PASS,
  link/TOC/context gates per `validate-set.sh` (see validation output).
- Next action: the first product release consuming this set must fill one
  entry above (device rows plus AT rows) before claiming WCAG 2.1 AA or
  responsive masterpiece status.
