# ADR-0004 — Visual Automation Stays Out of the Governance Plugin

- Status: Accepted (v2.0.0 + visual-family update 2026-10-15)
- Context: PA-VIS-05 added a Playwright MCP visual-regression gate and PA-PLUG-08
  asked whether token-lint, contrast-gate, or screenshot-diff hooks belong in
  `plugins/excellence-ops.js` next to SecretsGuard, ExcellenceValidate, and
  ExcellenceTelemetry.
- Decision: keep `excellence-ops.js` strictly for governance (secrets guard,
  validation reminders, redacted telemetry). Visual automation lives in skill
  procedure (`test-automation-engineer` Step 6 plus
  `references/visual-regression-runbook.md`), the deterministic token gate
  (`scripts/check-design-tokens.py` in validate-set.sh gate 7), and the
  `/vis-diff` command. No visual rule is added to the plugin.
- Rationale: governance plugins must stay deterministic, offline, and
  dependency-free; visual checks need a live browser, product routes, and
  human adjudication, which cannot fail closed without false positives.
  Mixing them would weaken the SecretsGuard fail-closed guarantee and the
  telemetry never-throws guarantee.
- Consequences: pinning the Playwright MCP package version and keeping the
  browser path portable is a deployment concern documented in the runbook,
  not a plugin concern; any future auto-lint hook ships as a separate
  opt-in plugin with its own kill-switch and ADR.
