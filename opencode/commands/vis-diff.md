---
description: Run the visual-regression gate with Playwright MCP screenshots and prioritized fix requests
agent: test-runner
subtask: true
---
Run the visual-regression gate for $ARGUMENTS using test-automation-engineer Step 6 plus `test-automation-engineer/references/visual-regression-runbook.md` (set-root-relative).

Drive the browser only through Playwright MCP tools (`browser_navigate` → `browser_snapshot` → `browser_take_screenshot`); capture 360px, 768px, and 1440px in light and dark themes where supported; diff against `snapshots/baseline/` with the runbook P0–P3 rubric; redact PII before storing screenshots.

Deliver the runbook diff report format: journey, viewport, theme, baseline version, P0–P3 counts with screenshots, failing threshold values, approver decision (accept, fix-by-date, or re-baseline with rationale), and next review date. Block on any open P0. Never accept a journey only because the code runs.

Arguments: `$ARGUMENTS` is the journey or route to gate (URL, route path, or journey name). Examples: `/vis-diff /checkout`, `/vis-diff halaman pembayaran`, `/vis-diff pricing page dark theme`.

Success criteria: three-viewport screenshots captured live via MCP (no guessed DOM); every diff labeled P0–P3 with owner and fix date; zero open P0 at handoff; re-baselines carry approver, date, and rationale.
