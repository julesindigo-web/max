# ARIA and Keyboard Patterns

Apply native semantics first. Add ARIA only to fill proven gaps.

## Prefer Native Elements

- Use button for actions, a for navigation, input with label for entry.
- Use select, radio, and checkbox for choice controls.
- Use dialog element or a tested dialog pattern with focus management.
- Use h1 through h3 in order without skipping levels for structure.
- Add ARIA only when native meaning cannot express the design.

## Name, Role, and State

- Give every control an accessible name from visible text where possible.
- Keep aria-label text consistent with visible labels.
- Reflect expanded, pressed, selected, and checked states in markup.
- Announce dynamic results with aria-live polite for status regions.
- Verify name computation in the accessibility tree before sign-off.

## Manage Focus

- Show a visible focus indicator with at least 3 to 1 contrast.
- Move focus to dialogs on open and return focus on close.
- Trap focus inside modal dialogs until dismissal with escape.
- Skip decorative content with tabindex minus 1 where needed.
- Never use positive tabindex values that reorder natural flow.

## Support Keyboard Flows

- Operate menus, tabs, accordions, and dialogs by arrows, enter, space, and escape.
- Provide skip links that become visible on focus.
- Keep focus order matched to visual order across breakpoints.
- Confirm full task completion by keyboard on at least 10 core journeys.
- Document shortcuts and avoid conflicts with screen-reader keys.

## Verify With Technology

- Test with NVDA or VoiceOver plus keyboard on scoped flows.
- Confirm announcements for errors, loading, and success states.
- Check magnification at 200% and high-contrast themes.
- Log tool versions, defects, and retest results per component.
- Treat new ARIA defects as release blockers until fixed and verified.
