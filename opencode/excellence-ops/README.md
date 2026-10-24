# excellence-ops — user-level plugins set (masterpiece v2.2.0)

Runtime wiring that complements the `project-artifact-excellence-set` (knowledge) with behavior: global rules, invocable subagents, slash commands, event hooks, and an evidence trail. The hook plugins auto-load from this config tree; the managed Playwright MCP command is configured explicitly in `../opencode.jsonc`.

## Members

| Member | Path | Role |
|---|---|---|
| Global rules | `../AGENTS.md` | Calibration law, 14-skill routing, full-stack practice law, safety, validation-first, hook summary, command catalog |
| Subagents | `../agents/{auditor,skill-builder,test-runner,fullstack-delivery}.md` | Least-privilege audit, authoring, testing, and cross-tier delivery execution |
| Commands | `../commands/{audit,validate-set,new-skill,vis-diff,fullstack-deliver,build,bugfix,refactor,hotfix}.md` | Subagent entrypoints plus feature, defect, refactor, and emergency playbooks with success criteria |
| Hooks | `../plugins/excellence-ops.js` | `SecretsGuard`, `ExcellenceValidate`, `ExcellenceTelemetry` (v2.2.0) |
| Evidence trail | `session-log.jsonl` (created at runtime) | Data source for trigger/task/time-to-skill claims (redacted only) |
| Routing probes | `eval/routing-probes.json` + `eval/score-routing-probes.py` | Frozen 6×(5+5) probe set with deterministic hygiene scorer (no LLM) |
| Changelog | `CHANGELOG.md` | Versioned release notes for this set |

## Contracts

- Hooks use the version-pinned `@opencode-ai/plugin` 1.18.31 surface: `tool.execute.before`, `tool.execute.after`, the generic `event` hook for `session.idle`/`command.executed`/`session.error`, and `experimental.session.compacting`. Composition-file deletion is guarded from `apply_patch` delete markers in the before hook; unrelated `file.*` event types are not claimed as implemented.
- SecretsGuard checks `filePath` and directory-scoped `path` for `read`/`grep`/`glob`/`list`; `pattern` (regex) strings are never treated as paths. Documented secret-adjacent doc names (e.g. `design-tokens.json`, `security-vulnerability-auditor/SKILL.md`) stay allowed.
- The plugin is dependency-free (node builtins). It never mutates user data except appending the telemetry log, and never throws except to block a guarded action.
- Telemetry records contain ids, command names, and error kinds only — never message bodies, command arguments, or secrets.
- `EXCELLENCE_AUTOVALIDATE=0` disables validator execution (reminders remain).

## Validation

```bash
bash ~/.config/opencode/excellence-ops/validate-plugins.sh
```

Gates: agent/command frontmatter (description required, valid mode/permission keys, steps budgets), `opencode.jsonc` parses, `node --check` on the plugin, unit tests via `node --test <file>` (guard positive/negative incl. directory scope, set-root discovery, verdict selection, apply_patch delete-guard, redacted event hook), eval probe hygiene scorer, version sync (README vs plugin header vs CHANGELOG), line budgets, TODO scan, session-log secrets scan, telemetry-shape gate (redacted-only keys, <2 KB/line).

## Success metrics (plugins-set scope)

- Trigger performance: subagents/commands activate on the documented task classes; target ≥90% correct routing measured against `eval/routing-probes.json` (6 groups × 5 positive + 5 negative, Indonesian + near-miss included) via the deterministic hygiene scorer plus target-runtime activation logs.
- Task completion: every guarded action is blocked with an actionable message; every validation verdict reaches the operator; target 100% on the runtime unit suite.
- Context-token efficiency: AGENTS.md plus one subagent file stay lean (see line budgets in the validator); hooks add zero baseline context (event-driven).
- Time-to-working: a new operator runs `validate-plugins.sh` and `post-restore.sh` green within ≤15 minutes of reading this README.
- Residual defects: zero open Critical/Major; telemetry never breaks a session (all appends are guarded).

## Changelog

See `CHANGELOG.md`. Current version: 2.2.0 (all version markers — README header, plugin header, eval probes, CHANGELOG — are kept in sync by the validator).

## Residual risks

- Hook behavior is asserted by unit tests with mocked contexts, not by live opencode runs; a live smoke (`/audit`, an edit of a scratch SKILL.md, session idle) is recommended after upgrades (still blocked by sandbox FS in this environment).
- `SecretsGuard` is pattern-based: exotic secret layouts outside the documented patterns are not covered — treat the list as a floor, not a proof. Pair with a pre-commit secret scan and vault references; never paste secret values into prompts.
- Telemetry log is local-only evidence; runtime trigger/task claims still need the set's `evaluation/runtime-protocol.md` runs. The bundled probes prove set hygiene only, not live routing precision.
- Ops probes (6 groups × (5+5) = 60 cases) gate the legacy command/agent hygiene cases; validator presence/frontmatter checks cover the expanded catalog. Full 14-skill trigger precision requires the set matrix (238 cases) plus a live run per `evaluation/runtime-protocol.md` — never conflate the two denominators.

## Scope decision (2026-10-15)

Requested but NOT installed: `/review-agent`, `/plugin-creator`, `/customize-opencode`.
Disposition: out-of-scope for this set. Covered instead by `security-vulnerability-auditor` + `project-artifact-auditor` (review), `skills-create-excellence` (plugin/skill authoring), and `AGENTS.md` §2 (opencode configuration).
Resolutions are mapped in `AGENTS.md` §6a (PA-REQ-01): `/review-agent` → `/audit`, `/plugin-creator` → `/new-skill`, `/customize-opencode` → `AGENTS.md` §2 + `/new-skill`.
Raise a `skill-improvement-requests/v1` event only with ≥2 recurring observations per `shared/references/feedback-loop.md`. Never improvise these names as invocable skills.
