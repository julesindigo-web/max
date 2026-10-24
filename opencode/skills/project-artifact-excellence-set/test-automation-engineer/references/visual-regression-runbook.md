# Visual Regression Runbook

Deterministic browser-to-diff procedure for the test-automation-engineer
visual-regression gate (Opsi B, PA-VIS-05). Proves a journey looks right; never
accept a journey only because the code runs.

## Prerequisites

- Playwright MCP registered and enabled in `opencode.jsonc` (`mcp.playwright`
  with an explicit `command` array). Pin the package version instead of
  `@latest` and keep the browser path portable (see ADR-0004); record the
  pinned version in the diff report.
- Frozen design reference: approved screenshots or Figma exports per viewport,
  plus the Art Brief from human-centric-visual-excellence Step 0.
- Deterministic data: seeded user, fixed clock, masked PII (names, emails,
  balances, ID numbers) before any screenshot is stored.

## Capture Procedure

1. Drive only through Playwright MCP tools in this order: `browser_navigate`
   to the journey URL, `browser_snapshot` to confirm the accessibility tree
   settled, `browser_take_screenshot` for the artifact.
2. Capture three viewports per journey: 360px (phone), 768px (tablet),
   1440px (desktop). Capture light and dark themes where supported.
3. Wait on observable state (network idle plus LCP element visible); fixed
   sleeps are forbidden. Record device, browser version, viewport, theme,
   and timestamp in the screenshot filename.
4. Store approved captures under `snapshots/baseline/<journey>/<vp>-<theme>.png`
   with a versioned `snapshots/manifest.json` (baseline version, approver,
   date, MCP package version, browser version).

## Diff Thresholds and Priority Rubric

- P0 BLOCKING: overlapped CTA or primary action, truncated or clipped text,
  missing loading or error state, focus indicator invisible, CLS regression
  beyond 10 percent versus baseline. Blocks release; fix within 14 days max.
- P1 DRIFT: spacing, color, or type token deviates from
  `design-tokens-and-components.md` without approval. Fix before next minor.
- P2 POLISH: sub-4px decorative shift, non-semantic pixel noise, font
  antialiasing churn. Fix opportunistically with owner and date.
- P3 OPTIONAL: taste-level suggestion with no usability impact. Never blocks.

## Adjudication and Re-baseline

- Every diff is human-adjudicated as intentional (design approved the change)
  or regression (file a P0–P3 fix request). Auto-approve is forbidden.
- Re-baseline only with reviewer approval recorded in the diff report
  (approver, date, rationale). Retain baselines for at least 5 releases.
- Quarantine font and animation flakes: freeze webfonts, disable
  non-essential animation during capture, allowlist documented noise regions.

## Diff Report Format

Journey, viewport, theme, baseline version, P0–P3 counts with screenshots,
failing threshold values, approver decision (accept, fix-by-date, or
re-baseline with rationale), and next review date. Attach the report to the
release record so auditors can verify without re-running the browser.
