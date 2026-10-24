# Operations Runbook — v2.0.0

## Validate
```bash
bash validation/validate-set.sh
```

## Score trigger coverage
```bash
python3 scripts/run-trigger-evaluation.py --matrix evaluation/trigger-evaluation-matrix.json
```

## Runtime run
Follow `evaluation/runtime-protocol.md`; write the dated report from `evaluation/results-template.md`.

## Process feedback inbox
```bash
python3 skills-create-excellence/scripts/process-audit-feedback.py audit-feedback/inbox/<audit-id>.json /tmp/request.json
```

## Build + verify release
```bash
python3 scripts/build-release.py --root . --output ../project-artifact-excellence-skill-set.zip
python3 scripts/verify-release.py ../project-artifact-excellence-skill-set.zip
(cd .. && sha256sum -c project-artifact-excellence-skill-set.zip.sha256)
```

## Rollback
Releases are immutable archives; rollback means re-issuing the prior verified archive and re-running `validate-set.sh` on the extracted tree. Record the decision with owner and date.

## Timing budget (PA-PERF-10)
Reference runner: full 8-gate `validate-set.sh` completes within 15 minutes; scorer and single-skill gates within 2 minutes. Log wall-clock per gate on each release; investigate on breach (repeated work, slow process, or environment variance) before retrying with a larger budget.

## MCP pin + browser path (PA-SEC-03, 2026-10-15)
Playwright MCP is pinned per release in `~/.config/opencode/opencode.jsonc` (currently `@playwright/mcp@0.0.83`; never `@latest`).
`--executable-path` is arch-specific: arm64 uses `.../chromium-1248/chrome-linux-arm64/chrome`, x86_64 uses `.../chromium-1248/chrome-linux/chrome`.
`PLAYWRIGHT_BROWSERS_PATH` (`/tmp/opencode/ms-playwright`) is the portable discovery fallback; keep the pin and path in sync per release and verify `/vis-diff` smoke on the target arch.

## MCP sandbox as root (PA-MCP-SANDBOX, 2026-10-16)
Symptom: `initializeServer: Target page, context or browser has been closed` with `Running as root without --no-sandbox is not supported`.
Cause: container runs as root; Chromium zygote sandbox refuses to start.
Fix (in `~/.config/opencode/opencode.jsonc` command array): `--no-sandbox` plus `--isolated` (in-memory profile avoids stale lock issues). Verified 2026-10-16: stdio initialize + `tools/list` + live `browser_navigate about:blank` with snapshot, zero sandbox errors.
Do NOT remove these flags on root containers. If the environment gains userns sandbox support, re-evaluate via the same stdio smoke before changing the config.
