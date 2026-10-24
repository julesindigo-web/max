# Design Tokens and Components Contract

Machine-enforceable companion to the human-centric-visual-excellence SKILL.md
(PA-DSY-02). Every production style resolves to a token below; one-off values
are defects, not shortcuts. Frontend implementations reference this contract;
`scripts/check-design-tokens.py` validates its structure in gate 7.

## Grid and Spacing

- Base unit 8px; spacing tokens `s-1` (8px), `s-2` (16px), `s-3` (24px),
  `s-4` (32px), `s-6` (48px), `s-8` (64px). Section spacing is at least twice
  the inner element spacing.
- Columns: 12 desktop at 1440px, 8 tablet at 768px, 4 phone at 360px.
- Gutters `g-4/8/16/24` and container tokens `container-sm/md/lg` with
  max-width values recorded once here, never per page.

## Color Roles

- Roles: background, surface, text, muted-text, border, accent (exactly one
  interactive accent), success, warning, danger, focus-ring.
- Each role carries light and dark values meeting WCAG 2.1 AA (4.5 to 1 body,
  3 to 1 large text and essential graphics, 3 to 1 focus indicators).
- Meaning is never color alone: pair every semantic color with text or icon.

## Type Scale

- One size per role across body, label, heading, display on a fixed modular
  ratio. Body at 16px or larger with line height 1.5 or higher.
- Line length 45 to 75 characters on desktop; type voice at most 1 display
  plus 1 body family per the Art Brief.

## Component Contract

Each component ships a contract block with anatomy, props and variants
(size, state, density), token references per slot, and accessibility notes
(role, name computation, keyboard path, focus target).

## Interaction State Matrix

Every interactive component renders all applicable states with token refs:
default, hover, focus-visible, active, disabled, loading, error, empty.
Touch targets are at least 44px; hover-only affordances always have a touch
and keyboard equivalent. Destructive actions confirm explicitly and offer
undo where the platform allows.

## Naming and Versioning

- Pattern `--{tier}-{role}-{state}-{scale}`, for example
  `--color-action-hover` or `--space-section-lg`.
- Tokens are versioned with the set release; renames ship a deprecation alias
  valid for exactly one release, then the alias is removed.
- Token owners and review dates are recorded alongside each scale, palette,
  and motion decision in the handoff record.

## Export and Lint

- Single source of truth exports to CSS custom properties plus the project's
  theme mapping (for example Tailwind config); generated files are never
  hand-edited.
- CI rule: zero literal hex colors or ad-hoc pixel spacing outside tokens in
  product styles. Exceptions need an allowlist entry with owner and expiry;
  expired entries fail the gate.
