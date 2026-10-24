# excellence-ops CHANGELOG

Agent-facing release notes for the user-level `excellence-ops` plugins set. The knowledge set (`project-artifact-excellence-set`) is versioned separately and is not modified by these entries.

## 2.2.0 (2026-10-24)

- Security: fixed-root allowlisting for canonical skill-set auto-validation; untrusted marker trees are never executed, and `apply_patch` set-composition deletions are blocked before mutation.
- SecretsGuard: added shell-path detection, `.envrc`, `.ssh`, `.git`, `id_dsa`/`id_ecdsa` patterns, destructive Git command guards, and explicit safe-example exceptions.
- Telemetry: allowlisted schema, bounded values, restrictive file permissions, fsync on append, and 5 MiB rotation with three backups.
- Runtime: removed test fixtures from the runtime skill mirror, persisted/pinned Playwright browser provisioning, enabled Chromium sandbox by default, and added an explicit root-run refusal.
- Portability: validator and unit tests derive paths from their source files; package metadata is aligned with its lockfile.
- Permissions: removed unrestricted Python/Git shell grants, made the test runner read-only, and documented live-runtime checks as unverified until run.

## 2.1.1 (2026-10-24)

- Runtime repair: plugin-only exports now contain the three hook factories; test helpers moved to `lib/` so OpenCode 1.19.4 no longer rejects a non-function helper export at startup.
- Validation: added a regression gate for the runtime plugin export contract; a clean local server startup is now part of the operational smoke test.

## 2.1.0 (2026-10-24)

- Full-stack delivery: added the `fullstack-delivery` least-privilege subagent and `/fullstack-deliver <scope>` command. It traces UI through contract, authorization, domain, data, and feedback; selects sibling depth only when relevant; and reports task-matched verification.
- Workflows: completed explicit success criteria for `/bugfix`, `/hotfix`, and `/refactor`; added the global canonical handoff contract at `AGENTS.md` §12.
- Validation/docs: validator now requires the full-stack route and artifacts, applies the documented 220-line global-rule budget, and version-syncs 2.1.0. README now matches the 14 skills, 4 subagents, and 9 commands.

## 2.0.0 (2026-10-15)

- AGENTS.md: full 13-member routing table (one explicit row per skill; no vague rows), hook behavior summary with kill-switch, command catalog, and good/bad calibration examples.
- Hooks (`plugins/excellence-ops.js`):
  - SecretsGuard now guards directory-scoped `path` in addition to `filePath` for `read`/`grep`/`glob`/`list`; `pattern` strings are never blocked.
  - ExcellenceValidate reads after-hook args from `input.args` first (1.18 runtime shape) with `output.args` fallback, and warns (never blocks) when `apply_patch` deletes `SKILL.md`/`manifest.yaml`/`SET.md`. No `file.deleted` event exists in 1.18, so patch markers are the delete signal.
  - ExcellenceTelemetry uses the documented `event` hook for `session.idle`/`command.executed`/`session.error` with redacted fields only (ids, command names, error kinds); legacy hook-key aliases are retained. `session.error` logging never includes message bodies.
- Subagents: added `steps` budgets (auditor 25, skill-builder 30, test-runner 30), `color`, explicit `hidden: false`, and role-specific failure-mode guidance. Permissions unchanged (least-privilege).
- Commands: per-command success criteria plus argument examples, including an Indonesian `/audit` example. No duplication of base commands.
- Harness: new `eval/` frozen routing probes (6 groups × 5+5, Indonesian + near-miss included) with a deterministic scorer gate; validator adds version-sync, line-budget, TODO-scan, and session-log secrets-scan gates.
- Tests: unit suite extended from 12 to 23 (11 new: directory scope, runtime args shape, delete-guard, redacted event hook).

## 1.0.0 (prior)

- Initial plugins set: AGENTS.md with 3-skill routing table, three subagents, three commands, three hook plugins (SecretsGuard, ExcellenceValidate, ExcellenceTelemetry via hook-key style), README, single-gate validator, 12 unit tests.
- Known gaps carried into 2.0.0 and now closed: vague routing row, filePath-only guard, silent set-file deletions, missing session.error logging, untestable routing claim, validator without version/budget/TODO/log-secret gates.
