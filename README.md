# OpenCode user-level agent configuration — remediated v2.2.0

This package is a remediated snapshot based on the configuration archive dated 2026-10-24. It retains the authoritative canonical skill-set under `opencode/skill-sets/` and a separately curated runtime mirror under `opencode/skills/`.

## Included

- `opencode/`: user-level OpenCode configuration, agents, commands, plugins, tests, validators, dependency manifests, and Playwright wrapper/configuration.
- `opencode/skill-sets/project-artifact-excellence-set/`: canonical source; intentionally retained unmodified by this remediation.
- `opencode/skills/project-artifact-excellence-set/`: runtime mirror with test fixtures removed from the discovery tree.
- `global-skills/`: preserved source payload. Do not assume `~/.opencode/skills` is a native OpenCode discovery path; check the installed version's documented locations before changing symlinks.
- `ARCHIVE-MANIFEST.sha256`: SHA-256 integrity list for archived payload files, regenerated immediately before packaging.

## Restore

1. Extract the ZIP and copy `opencode/` to `~/.config/opencode/` while preserving any existing credentials/session data separately.
2. Review and merge with existing config before replacing live files. Never overwrite `auth.json` or a live telemetry log with archived data.
3. Run `bash ~/.config/opencode/excellence-ops/validate-plugins.sh`.
4. Run `bash ~/.config/opencode/skill-sets/project-artifact-excellence-set/validation/validate-set.sh`.
5. Review the root refusal in `excellence-ops/playwright-launch.sh`. For security, the browser MCP refuses to launch Chromium as root by default; use a non-root OpenCode account for sandboxed Chromium.
6. Install the pinned browser with `bash ~/.config/opencode/excellence-ops/install-playwright-browser.sh` only after reviewing the network/install implications.
7. From a neutral working directory, run `opencode debug config`, `opencode agent list`, and `opencode debug skill`. Verify skill inventory, permission policy, and a browser MCP smoke test in the target runtime.

## Validation status

Automated source-level tests and archive integrity checks are recorded in `REMEDIATION-REPORT.md`. Live OpenCode startup, root/non-root sandbox operation, external-network browser behavior, and the 238-case runtime routing matrix are explicitly **Unknown/Untested** until run on the target host. Static PASS does not imply production readiness.
