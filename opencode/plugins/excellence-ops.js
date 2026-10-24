// excellence-ops.js — user-level opencode plugin pack (masterpiece v2.2.0).
//
// Three focused plugins complement the project-artifact-excellence-set:
//   SecretsGuardPlugin        — tool.execute.before: fail-closed secrets + destructive-command guard.
//   ExcellenceValidatePlugin  — tool.execute.after:  auto-validate edited skills / set contracts.
//   ExcellenceTelemetryPlugin — event (session.idle/command.executed/session.error) + experimental.session.compacting.
//
// Design rules: deterministic, offline, dependency-free (node builtins only),
// never mutate user data except the telemetry JSONL log, never throw except
// to block a guarded action. Kill-switch: EXCELLENCE_AUTOVALIDATE=0 disables
// validator execution (reminders are still appended).
//
// v2.2.0 exports only plugin factories from plugins/; pure test helpers live
// in excellence-ops/lib so the runtime never attempts to load a helper as a hook.
// v2.0.0 changes over v1.0.0:
//   - SecretsGuard now checks directory-scoped `path` in addition to `filePath`
//     for read/grep/glob/list (grep/glob scope searches via `path`; verified
//     against 1.18 tool titles `Grep "<pattern>"`/`Glob "<pattern>"` with
//     `t.input.path`). Pattern strings are never blocked (regex false positives).
//   - ExcellenceValidate reads edit args from `input.args` first (1.18 runtime
//     shape for tool.execute.after) with `output.args` fallback (legacy mocks),
//     and warns (never blocks) when `apply_patch` deletes SKILL.md/manifest.yaml/SET.md.
//   - ExcellenceTelemetry uses the documented `event` hook
//     (`event: async ({event}) => …`, see plugins docs Send-notifications example)
//     for session.idle/command.executed/session.error with redacted fields only
//     (ids, command names, error kinds — never message bodies, arguments, or
//     secrets). Legacy `session.idle`/`command.executed` keys are kept as
//     deprecated aliases; `session.error` alias is added.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import {
  GUARDED_READ_TOOLS,
  appendTelemetry,
  extractApplyPatchDeletes,
  findSetRoot,
  isDestructiveCommand,
  isSetCompositionPath,
  redactedErrorKind,
  secretPathFromArgs,
  secretPathFromCommand,
  verdictForEdit,
} from "../excellence-ops/lib/excellence-ops-helpers.js";

// ---------------------------------------------------------------------------
// Plugin 1: SecretsGuard — fail closed on secret reads and destructive shell.
// ---------------------------------------------------------------------------
export const SecretsGuardPlugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      const args = { ...(input.args || {}), ...(output.args || {}) };
      if (GUARDED_READ_TOOLS.has(input.tool)) {
        const hit = secretPathFromArgs(args);
        if (hit !== null) {
          throw new Error(
            `SecretsGuard: refusing to read secret-adjacent path '${hit}'. ` +
              `Redact or reference it indirectly instead.`
          );
        }
      }
      if (input.tool === "bash" && typeof args.command === "string") {
        const secretCommandPath = secretPathFromCommand(args.command);
        if (secretCommandPath !== null) {
          throw new Error(`SecretsGuard: refusing shell command that references secret-adjacent path '${secretCommandPath}'. Use an approved secret scanner or vault integration.`);
        }
        if (isDestructiveCommand(args.command)) {
          throw new Error(
            `SecretsGuard: refusing destructive shell command. Re-run scoped to an explicit safe path.`
          );
        }
      }
    },
  };
};

// ---------------------------------------------------------------------------
// Plugin 2: ExcellenceValidate — validate edited skills and set contracts.
// ---------------------------------------------------------------------------
function runValidator(cmd, args, cwd, timeoutMs) {
  try {
    const out = execFileSync(cmd, args, { cwd, timeout: timeoutMs, encoding: "utf-8", stdio: ["ignore", "pipe", "pipe"] });
    return { ok: true, tail: String(out).trim().split("\n").slice(-4).join("\n") };
  } catch (err) {
    const tail = [err.stdout, err.stderr].filter(Boolean).join("\n").trim().split("\n").slice(-8).join("\n");
    return { ok: false, tail: tail || String(err.message).split("\n")[0] };
  }
}

const PLUGIN_DIR = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_ROOT = path.resolve(PLUGIN_DIR, "..");
const CANONICAL_SET_ROOT = path.join(CONFIG_ROOT, "skill-sets", "project-artifact-excellence-set");

export const ExcellenceValidatePlugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      // Block set-composition deletions before apply_patch mutates the tree.
      // This is deliberately conservative: any SKILL.md/manifest.yaml/SET.md
      // deletion through apply_patch requires a separate, reviewed operation.
      if (input.tool !== "apply_patch") return;
      const args = { ...(input.args || {}), ...(output.args || {}) };
      const patchText = args.patchText ?? args.patch ?? input.patchText;
      const deletes = extractApplyPatchDeletes(patchText);
      const hits = deletes.filter(isSetCompositionPath);
      if (hits.length > 0) {
        throw new Error(`[excellence-ops] blocked apply_patch deletion of composition file(s): ${hits.join(", ")}. Preserve SKILL.md/manifest.yaml/SET.md composition; use a reviewed manual remediation if deletion is truly required.`);
      }
    },
    "tool.execute.after": async (input, output) => {
      if (input.tool === "apply_patch") return;
      if (input.tool !== "write" && input.tool !== "edit") return;
      const edited = (input.args && input.args.filePath) ?? (output.args && output.args.filePath);
      if (typeof edited !== "string") return;
      const setRoot = findSetRoot(path.dirname(path.resolve(edited)), CANONICAL_SET_ROOT);
      if (!setRoot) return;
      const verdict = verdictForEdit(setRoot, edited);
      if (verdict.kind === "none") return;
      const enabled = process.env.EXCELLENCE_AUTOVALIDATE !== "0";
      const single = path.join(setRoot, "skills-create-excellence", "scripts", "validate-excellence.sh");
      if (!enabled) {
        output.output = `${output.output}\n\n[excellence-ops] EXCELLENCE_AUTOVALIDATE=0: skipped auto-validation for '${edited}'. Run the gate manually.`;
        return;
      }
      if (verdict.kind === "skill" && fs.existsSync(single) && !fs.lstatSync(single).isSymbolicLink()) {
        const res = runValidator("bash", [single, verdict.memberDir], setRoot, 120000);
        output.output = `${output.output}\n\n[excellence-ops] single-skill gate ${res.ok ? "PASS" : "FAIL"} for '${verdict.memberDir}':\n${res.tail}`;
        return;
      }
      const validator = path.join(setRoot, "validation", "validate-set.sh");
      if (!fs.existsSync(validator) || fs.lstatSync(validator).isSymbolicLink()) {
        output.output = `${output.output}\n\n[excellence-ops] full set gate FAIL: canonical validator missing or is a symlink.`;
        return;
      }
      const res = runValidator("bash", [validator], setRoot, 300000);
      output.output = `${output.output}\n\n[excellence-ops] full set gate (8 gates) ${res.ok ? "PASS" : "FAIL"}:\n${res.tail}`;
    },
  };
};

// ---------------------------------------------------------------------------
// Plugin 3: ExcellenceTelemetry — evidence trail + compaction context.
// ---------------------------------------------------------------------------
const COMPACTION_CONTEXT = `## Excellence continuity (auto-injected)
Preserve across compaction: current task and status, files being modified, open Critical/Major findings with evidence states, next validation step. Calibration law holds: missing evidence is Unknown/Untested, never a pass; severity is never raised on missing evidence alone.`;

// Shared redacted handler for Event-bus records. Logs ids, command names,
// and error kinds only — never message bodies, command arguments, or secrets.
async function handleTelemetryEvent(ev) {
  if (!ev || typeof ev.type !== "string") return;
  if (ev.type === "session.idle") {
    appendTelemetry({ event: "session.idle", sessionID: ev.properties && ev.properties.sessionID });
  } else if (ev.type === "command.executed") {
    appendTelemetry({
      event: "command.executed",
      sessionID: ev.properties && ev.properties.sessionID,
      command: ev.properties && ev.properties.name,
    });
  } else if (ev.type === "session.error") {
    appendTelemetry({
      event: "session.error",
      sessionID: ev.properties && ev.properties.sessionID,
      errorKind: redactedErrorKind(ev.properties && ev.properties.error),
      provider: ev.properties && (ev.properties.providerID ?? ev.properties.provider),
      model: ev.properties && (ev.properties.modelID ?? ev.properties.model),
    });
  }
}

export const ExcellenceTelemetryPlugin = async () => {
  return {
    // Documented Event-bus entry point (see plugins docs Send-notifications
    // example: `event: async ({event}) => { if (event.type === …) … }`).
    // This is the runtime-correct path; the `session.*`/`command.*` keys
    // below are deprecated aliases kept for backward compatibility.
    event: async (input) => {
      try {
        await handleTelemetryEvent(input && input.event);
      } catch {
        // telemetry must never break a session
      }
    },
    // Deprecated aliases (v1 hook-key style). Retained so existing mocks and
    // any shim dispatching by event-type key keep working; new code should
    // rely on `event` above.
    "session.idle": async (input) => {
      try {
        appendTelemetry({ event: "session.idle", sessionID: input.sessionID });
      } catch {
        // telemetry must never break a session
      }
    },
    "command.executed": async (input) => {
      try {
        appendTelemetry({ event: "command.executed", sessionID: input.sessionID, command: input.command ?? input.name });
      } catch {
        // telemetry must never break a session
      }
    },
    "session.error": async (input) => {
      try {
        const err = (input && (input.error ?? (input.properties && input.properties.error))) ?? null;
        appendTelemetry({
          event: "session.error",
          sessionID: input.sessionID ?? (input.properties && input.properties.sessionID),
          errorKind: redactedErrorKind(err),
          provider: input.providerID ?? input.provider ?? (input.properties && (input.properties.providerID ?? input.properties.provider)),
          model: input.modelID ?? input.model ?? (input.properties && (input.properties.modelID ?? input.properties.model)),
        });
      } catch {
        // telemetry must never break a session
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push(COMPACTION_CONTEXT);
    },
  };
};
