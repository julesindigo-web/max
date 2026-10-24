#!/usr/bin/env bash
# Validate the user-level excellence-ops plugins set. Exit 0 = pass, 1 = fail.
# Read-only except test temp dirs. Requires: bash, python3, node.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'PASS: %s\n' "$*"; }

[[ -f "$ROOT/AGENTS.md" ]] || fail "AGENTS.md missing"
grep -q "Calibration law" "$ROOT/AGENTS.md" || fail "AGENTS.md lacks calibration law"
grep -q "Hook behavior" "$ROOT/AGENTS.md" || fail "AGENTS.md lacks hook behavior summary"
grep -q "Command catalog" "$ROOT/AGENTS.md" || fail "AGENTS.md lacks command catalog"
grep -q '@fullstack-delivery' "$ROOT/AGENTS.md" || fail "AGENTS.md lacks fullstack delivery route"
[[ -f "$ROOT/agents/fullstack-delivery.md" ]] || fail "fullstack delivery agent missing"
[[ -f "$ROOT/commands/fullstack-deliver.md" ]] || fail "fullstack delivery command missing"
# Every installed skill name must appear; no vague rows allowed.
for s in project-artifact-auditor skills-create-excellence test-automation-engineer code-refactoring-optimizer security-vulnerability-auditor architecture-documentation-generator accessibility-inclusive-design continuous-observability-telemetry backend-engineering-excellence frontend-engineering-excellence human-centric-visual-excellence deployment-devops-orchestrator fullstack-e2e-mastery task-orchestrator; do
  grep -q "\`$s\`" "$ROOT/AGENTS.md" || fail "AGENTS.md missing skill row: $s"
done
grep -q "matching member" "$ROOT/AGENTS.md" && fail "AGENTS.md still contains vague 'matching member' row"
grep -q "matching domain member" "$ROOT/AGENTS.md" && fail "AGENTS.md still contains vague routing row"
pass "AGENTS.md routing table complete (14 skills, hooks, catalog)"

# Agent frontmatter: description required, valid mode, known permission keys,
# plus v2 budgets (steps, color, explicit hidden).
for f in "$ROOT"/agents/*.md; do
  [[ -f "$f" ]] || fail "no agents found"
  grep -qE '^description:' "$f" || fail "description missing: $f"
  grep -qE '^mode: (subagent|primary|all)$' "$f" || fail "invalid mode: $f"
  grep -qE '^steps: [0-9]+$' "$f" || fail "steps budget missing: $f"
  grep -qE '^color: .+$' "$f" || fail "color missing: $f"
  grep -qE '^hidden: false$' "$f" || fail "explicit hidden:false missing: $f"
  python3 - "$f" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"^permission:\n((?:[ \t]+.*\n?)+)", text, re.M)
if not m:
    print("no permission block (allowed)");
else:
    allowed = {"read","edit","glob","grep","list","bash","task","external_directory","webfetch","websearch","lsp","skill","question","doom_loop"}
    for line in m.group(1).splitlines():
        mm = re.fullmatch(r"  ([a-z_]+):.*", line)
        if mm and mm.group(1) not in allowed:
            sys.exit(f"unknown permission key '{mm.group(1)}' in {sys.argv[1]}")
print("permission keys ok")
PY
  pass "agent ok: $(basename "$f")"
done

# Command frontmatter: description + template body + success criteria required.
for f in "$ROOT"/commands/*.md; do
  [[ -f "$f" ]] || fail "no commands found"
  grep -qE '^description:' "$f" || fail "description missing: $f"
  body=$(awk 'BEGIN{p=0} /^---$/{c++; next} c>=2{p=1} p' "$f")
  [[ -n "${body//[[:space:]]/}" ]] || fail "empty template: $f"
  grep -q "Success criteria" "$f" || fail "success criteria missing: $f"
  pass "command ok: $(basename "$f")"
done
grep -q "audit arsitektur" "$ROOT/commands/audit.md" || fail "audit.md lacks Indonesian argument example"

# Config must still parse (we require zero changes to it).
python3 - "$ROOT/opencode.jsonc" <<'PY'
import json, sys
text = open(sys.argv[1], encoding="utf-8").read()
out, i, n, in_str, esc = [], 0, len(text), False, False
while i < n:
    ch = text[i]
    if in_str:
        out.append(ch)
        if esc: esc = False
        elif ch == "\\": esc = True
        elif ch == '"': in_str = False
        i += 1
    elif ch == '"':
        in_str = True; out.append(ch); i += 1
    elif ch == "/" and i + 1 < n and text[i+1] == "/":
        while i < n and text[i] != "\n": i += 1
    elif ch == "/" and i + 1 < n and text[i+1] == "*":
        i += 2
        while i + 1 < n and not (text[i] == "*" and text[i+1] == "/"): i += 1
        i += 2
    else:
        out.append(ch); i += 1
json.loads("".join(out))
print("opencode.jsonc parses")
PY

# Plugin syntax + unit tests (file-target invocation; directory form fails here).
node --check "$ROOT/plugins/excellence-ops.js" || fail "plugin syntax invalid"
pass "plugin syntax ok"
node --input-type=module -e '
const module = await import(process.argv[1]);
const expected = ["ExcellenceTelemetryPlugin", "ExcellenceValidatePlugin", "SecretsGuardPlugin"];
const actual = Object.keys(module).sort();
if (JSON.stringify(actual) !== JSON.stringify(expected) || actual.some((name) => typeof module[name] !== "function")) {
  throw new Error(`invalid plugin export surface: ${actual.join(", ")}`);
}
console.log("plugin export surface ok");
' "file://$ROOT/plugins/excellence-ops.js" || fail "plugin export surface invalid"
pass "plugin export surface ok"
node --test "$ROOT/excellence-ops/tests/excellence-ops.test.js" || fail "plugin unit tests failed"

# Eval routing probes: deterministic hygiene scorer (no LLM).
[[ -f "$ROOT/excellence-ops/eval/routing-probes.json" ]] || fail "eval routing probes missing"
[[ -f "$ROOT/excellence-ops/eval/score-routing-probes.py" ]] || fail "eval scorer missing"
python3 "$ROOT/excellence-ops/eval/score-routing-probes.py" "$ROOT/excellence-ops/eval/routing-probes.json" || fail "eval probe hygiene failed"

# Version sync: README header vs plugin header vs CHANGELOG vs eval probes.
README_VER=$(grep -oE 'masterpiece v[0-9]+\.[0-9]+\.[0-9]+' "$ROOT/excellence-ops/README.md" | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') || fail "README version unreadable"
PLUGIN_VER=$(grep -oE 'masterpiece v[0-9]+\.[0-9]+\.[0-9]+' "$ROOT/plugins/excellence-ops.js" | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') || fail "plugin header version unreadable"
CHANGELOG_VER=$(grep -oE '^## [0-9]+\.[0-9]+\.[0-9]+' "$ROOT/excellence-ops/CHANGELOG.md" | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') || fail "CHANGELOG version unreadable"
PROBES_VER=$(python3 -c "import json;print(json.load(open('$ROOT/excellence-ops/eval/routing-probes.json'))['version'])") || fail "probes version unreadable"
[[ "$README_VER" == "$PLUGIN_VER" ]] || fail "version drift: README $README_VER vs plugin $PLUGIN_VER"
[[ "$PLUGIN_VER" == "$CHANGELOG_VER" ]] || fail "version drift: plugin $PLUGIN_VER vs CHANGELOG $CHANGELOG_VER"
[[ "$PLUGIN_VER" == "$PROBES_VER" ]] || fail "version drift: plugin $PLUGIN_VER vs probes $PROBES_VER"
[[ "$PLUGIN_VER" == "2.2.0" ]] || fail "expected 2.2.0, found $PLUGIN_VER"
pass "version sync ok (2.2.0 across README, plugin, CHANGELOG, probes)"

# Remediation gates: fixed-root validator, permission regressions, runtime exclusions,
# dependency lock consistency, and secure browser configuration.
node --input-type=module - "$ROOT" <<'NODEGATE' || fail "security regression gate failed"
import fs from "node:fs";
import path from "node:path";
const root = process.argv[2];
const auditor = fs.readFileSync(path.join(root, "agents/auditor.md"), "utf8");
const builder = fs.readFileSync(path.join(root, "agents/skill-builder.md"), "utf8");
const runner = fs.readFileSync(path.join(root, "agents/test-runner.md"), "utf8");
if (/"python3 \*": allow/.test(auditor)) throw new Error("auditor permits arbitrary Python execution");
if (/"git \*": allow/.test(builder)) throw new Error("skill-builder permits unrestricted Git execution");
if (!/^  edit: deny$/m.test(runner)) throw new Error("test-runner must be read-only");
if (!/^  webfetch: ask$/m.test(runner) || !/^  websearch: ask$/m.test(runner)) throw new Error("test-runner web permissions must be explicit ask");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const lock = JSON.parse(fs.readFileSync(path.join(root, "package-lock.json"), "utf8"));
if (manifest.name !== lock.name || manifest.version !== lock.version) throw new Error("package.json and lockfile root name/version drift");
if (JSON.stringify(manifest.dependencies || {}) !== JSON.stringify(lock.packages?.[""]?.dependencies || {})) throw new Error("package.json and lockfile root dependencies drift");
const mirrorTests = path.join(root, "skills/project-artifact-excellence-set/skills-create-excellence/scripts/tests");
if (fs.existsSync(mirrorTests) && fs.readdirSync(mirrorTests, { recursive: true }).some((name) => String(name).endsWith("SKILL.md"))) throw new Error("runtime mirror still contains fixture SKILL.md");
const config = fs.readFileSync(path.join(root, "opencode.jsonc"), "utf8");
if (config.includes("/tmp/opencode/ms-playwright") || config.includes("--no-sandbox")) throw new Error("unsafe or ephemeral Playwright setting in opencode.jsonc");
if (!config.includes("playwright-launch.sh")) throw new Error("opencode.jsonc must launch the managed Playwright wrapper");
const browser = JSON.parse(fs.readFileSync(path.join(root, "excellence-ops/playwright-mcp-config.json"), "utf8"));
if (browser.browser?.isolated !== true || browser.browser?.launchOptions?.chromiumSandbox !== true) throw new Error("Chromium isolation and sandbox must be enabled");
console.log("security, browser, package, and runtime-exclusion gates ok");
NODEGATE
pass "remediation static gates ok"

# Line budgets (context-token efficiency floor).
check_budget() { # file max
  local n; n=$(wc -l < "$1")
  [[ "$n" -le "$2" ]] || fail "line budget exceeded: $1 has $n lines (max $2)"
  pass "budget ok: $1 ($n/$2)"
}
check_budget "$ROOT/AGENTS.md" 220
for f in "$ROOT"/agents/*.md; do check_budget "$f" 80; done
for f in "$ROOT"/commands/*.md; do check_budget "$f" 40; done
check_budget "$ROOT/plugins/excellence-ops.js" 500
check_budget "$ROOT/excellence-ops/README.md" 120
check_budget "$ROOT/excellence-ops/CHANGELOG.md" 80

# TODO scan: no leftover code markers in managed files (delimiter required
# so gate-name prose like "TODO scan" does not false-positive).
if grep -rnE 'TODO[[:space:]]*[:(\[]|FIXME[[:space:]]*[:(\[]|XXX[[:space:]]*[:(\[]' "$ROOT/AGENTS.md" "$ROOT"/agents/*.md "$ROOT"/commands/*.md "$ROOT/plugins/excellence-ops.js" "$ROOT/excellence-ops/README.md" "$ROOT/excellence-ops/CHANGELOG.md" "$ROOT/excellence-ops/eval/" "$ROOT/excellence-ops/tests/" 2>/dev/null; then
  fail "TODO/FIXME/XXX markers found (see above)"
fi
pass "TODO scan clean"

# Session-log secrets scan (high-precision key formats only; log may be absent).
LOG="$ROOT/excellence-ops/session-log.jsonl"
for candidate in "$LOG" "$LOG.1" "$LOG.2" "$LOG.3"; do
if [[ -f "$candidate" ]]; then
  if grep -qE -- '-----BEGIN ([A-Z ]*PRIVATE KEY|OPENSSH PRIVATE KEY)-----|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{10,}|xox[bpas]-[A-Za-z0-9-]+' "$candidate"; then
    fail "secret pattern found in $(basename "$candidate")"
  fi
  pass "$(basename "$candidate") secrets scan clean"
fi
done
if [[ ! -f "$LOG" ]]; then pass "session-log absent (nothing to scan)"; fi

# Telemetry shape gate (PA-OBS-02): live log lines must carry redacted-only
# keys (ts, event, sessionID, command, errorKind) and stay under 2 KB.
# Verbose client dumps fail closed here even when the secrets scan passes.
python3 - "$LOG" "$LOG.1" "$LOG.2" "$LOG.3" <<'PY'
import json, os, sys
logs = [p for p in sys.argv[1:] if os.path.exists(p)]
if not logs:
    print("telemetry shape ok (logs absent)")
    raise SystemExit(0)
allowed = {"ts", "event", "sessionID", "command", "errorKind", "provider", "model"}
for log in logs:
    with open(log, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                keys = set(json.loads(stripped).keys())
            except json.JSONDecodeError:
                sys.exit(f"{os.path.basename(log)} line {i} is not valid JSON")
            extra = keys - allowed
            if extra:
                sys.exit(f"{os.path.basename(log)} line {i} keys {sorted(extra)} exceed {sorted(allowed)}")
            if len(stripped) >= 2000:
                sys.exit(f"{os.path.basename(log)} line {i} oversized ({len(stripped)} chars, max 1999)")
print("telemetry shape ok (all active/rotated logs, redacted-only keys, <2 KB/line)")
PY
pass "telemetry shape gate ok"

printf 'PASS: all plugins-set validation gates passed.\n'
