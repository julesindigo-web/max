# Remediation Report — OpenCode User-Level Agent Configuration v2.2.0

**Snapshot basis:** `opencode-user-agent-config-2026-10-24`  
**Target contract:** OpenCode `v1.18.31` configuration/API assumptions where version-specific behavior matters  
**Remediation status:** source-level remediation applied to the archive copy; target-host/runtime acceptance remains pending.

## Executive result

The original archive has been retained as the starting point. Security, portability, runtime discovery, telemetry, package metadata, and restoration changes have been applied to the working copy. The authoritative `opencode/skill-sets/project-artifact-excellence-set/` content was not intentionally changed; ten test-fixture `SKILL.md` files were removed from the **runtime mirror** only, leaving 14 production skill entries in that mirror.

This package is **not labelled production-verified**. Plugin validation is green. The canonical 8-gate validator was attempted twice but did not complete within the execution limit; its comprehensive test runner reached `test_verifier_rejects_symbolic_link_entries` and the parent process timed out without the final `all skill-set validation gates passed` line. The eight-gate result therefore remains `Unknown/Untested`, not PASS.

## Applied remediation

### Security boundaries and permissions

- `ExcellenceValidatePlugin` no longer discovers a validator by searching arbitrary parent directories for marker files. It only resolves the fixed sibling canonical skill-set root relative to the installed plugin, verifies the root and validator paths are regular non-symlink paths, and refuses an out-of-root edit.
- `apply_patch` deletions of `SKILL.md`, `manifest.yaml`, and `SET.md` are blocked in the before-hook, before a mutation can complete. This is deliberately conservative for composition-named files.
- `SecretsGuard` now covers `.envrc`, `.ssh`, `.git`, `secrets/`, `id_dsa`, `id_ecdsa`, additional private-key extensions, common secret paths in shell command text, and common destructive Git actions (`reset --hard`, forced push, forced clean). Safe examples such as `.env.example` and `.envrc.example` remain allowed.
- The auditor no longer has arbitrary Python execution allowed; the skill-builder no longer has unrestricted `git *`; destructive Git operations are denied or require approval; the test-runner is edit-denied and explicit `webfetch`/`websearch` permissions are `ask`. Common read-only Git commands are exact matches rather than wildcard-suffixed grants.
- The global bash default is `ask`; destructive Git patterns are explicitly denied.

### Browser MCP and persistence

- Chromium assets are directed to `$HOME/.cache/opencode/ms-playwright`, not `/tmp`.
- The Playwright MCP server is pinned to `@playwright/mcp@0.0.83` and uses an explicit configuration with `isolated: true` and `launchOptions.chromiumSandbox: true`.
- Browser installation has its own explicit script. The launcher fails clearly when browser assets are missing and refuses to launch Chromium as root by default. The explicit `OPENCODE_PLAYWRIGHT_ALLOW_ROOT_UNSANDBOXED=1` emergency override disables Chromium sandbox and emits a warning; it must be treated as a temporary residual-risk exception, not a recommended mode.
- The configuration does not place shell variable expressions such as `${HOME}` inside JSONC.

### Runtime skill tree and duplicate discovery

- The test fixture tree under `opencode/skills/project-artifact-excellence-set/skills-create-excellence/scripts/tests/` was removed from the runtime mirror, eliminating its ten fixture `SKILL.md` entries from the discovery tree.
- Canonical source files were preserved; the mirror remains a distinct deployment artifact rather than an assertion that every source file belongs in runtime.
- No symlink is created or removed outside this archive. Duplicate warnings from a target host's existing `~/.claude/skills` or custom skill paths require post-restore inventory before deleting or moving host files.

### Telemetry and evidence

- Telemetry is allowlisted to timestamp, event, session ID, command name, error kind, and provider/model identifiers when present in the event payload. Message bodies, error messages, tool arguments, and unknown fields are not serialized.
- Append operations use a restrictive `0600` file mode, `0700` telemetry directory mode, `O_NOFOLLOW` where supported, an `fsync`, and rotation at 5 MiB with three backups.
- Validator checks now scan the active log and rotated backups for high-confidence secret patterns and enforce the redacted schema and line-size ceiling.
- Telemetry rotation and optional provider/model context are unit-tested with mocked event payloads. They are not proof of crash/power-loss durability or actual provider event shape on the target host.

### Package metadata, portability, and operators

- `package.json` and lockfile root metadata (`name`, `version`, direct dependency map) have been statically aligned. The dependency graph inside the existing lockfile was preserved.
- The validator and plugin tests derive config paths from their own source location instead of `/root/.config/opencode`.
- Added `post-restore.sh`, a persistent browser config, browser installer/launcher, and a new versioned changelog entry.
- The root README no longer instructs the operator to blindly create a `~/.opencode/skills` symlink. OpenCode's actual skill inventory must be verified on the target version.

## Verification record

| Check | Result | Evidence / limits |
|---|---|---|
| JavaScript syntax checks for plugin/helper | PASS | `node --check` |
| Plugin unit/regression tests | PASS | `node --test excellence-ops/tests/excellence-ops.test.js`: 30 tests, 30 pass, 0 fail |
| Plugin/config validator | PASS | `bash excellence-ops/validate-plugins.sh`: all plugin-set gates passed, version sync 2.2.0, static permission/browser/package/runtime-fixture checks passed |
| 60 legacy hygiene probes | PASS | Deterministic hygiene scorer, not semantic runtime routing |
| Runtime mirror inventory | PASS | 14 `SKILL.md` files; mirror test-fixture tree absent; canonical set contains 24 `SKILL.md` files including fixtures |
| JSONC syntax and package root metadata | PASS | Parser and validator static check |
| Canonical skill-set 8-gate validation | UNKNOWN/UNTESTED | Attempted twice; suite did not finish within the environment execution limit. Output reached a release-artifact test but no aggregate PASS line was obtained. |
| `npm ci` on a clean target | UNKNOWN/UNTESTED | Offline lockfile regeneration could not fetch an uncached registry dependency (`ENOTCACHED`, `yaml`). Metadata was aligned statically; networked install must be tested on the target host. |
| OpenCode live startup / permission enforcement | UNKNOWN/UNTESTED | No live target-host OpenCode server was launched here. |
| Playwright MCP launch, Chromium sandbox, network behavior | UNKNOWN/UNTESTED | Browser package/browser binary was not installed or launched in this session; root launch is intentionally refused by default. |
| 238-case semantic runtime routing | UNKNOWN/UNTESTED | Probe inventory/hygiene is not a live semantic-accuracy result. Run the canonical runtime protocol. |
| External duplicate skill warnings | UNKNOWN/UNTESTED | This archive cannot safely edit directories outside the snapshot; inventory the actual target host before changing aliases or removing duplicate skills. |

## Target-host acceptance checklist

1. Restore/merge the package into the intended user config; do not overwrite credentials or active logs.
2. Run `bash ~/.config/opencode/excellence-ops/post-restore.sh` and separately capture the complete canonical 8-gate result.
3. Run `opencode debug config`, `opencode agent list`, and `opencode debug skill`; confirm four agents, expected skill names, and zero unexpected duplicate/fixture entries.
4. Use a non-root OpenCode account. Install the pinned browser using `bash ~/.config/opencode/excellence-ops/install-playwright-browser.sh`; verify sandboxed browser launch and that MCP stdio is not contaminated by wrapper output.
5. Test deny/ask/allow behavior with non-sensitive fixtures: secret paths, secret paths embedded in shell commands, unsafe Git patterns, `apply_patch` composition deletion, and an untrusted fake repository containing a decoy validator.
6. Run the 238-case runtime routing protocol. Record precision/recall values from measured outcomes; do not infer them from the deterministic hygiene scorer.
7. Recompute and archive the test output, OpenCode version, Node/npm versions, platform/architecture, and timestamps as the final runtime evidence bundle.

## Residual security statement

SecretsGuard is a pattern-based preventive layer, not a complete shell parser, access-control system, or OS sandbox. The safest design still depends on least-privilege account permissions, review before destructive operations, trustworthy repository provenance, sandboxed browser execution, and an external secret scanner such as Gitleaks/TruffleHog. No test result in this report means all secrets or attack paths are blocked.
