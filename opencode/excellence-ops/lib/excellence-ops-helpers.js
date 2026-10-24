// Pure helpers for the excellence-ops plugin. This file deliberately lives
// outside plugins/: OpenCode loads named exports in plugins/ as hook factories.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const SECRET_BASENAME = /^(secret|secrets|credential|credentials)(\.|-|$)/i;
const SECRET_EXT = /\.(pem|key|p12|pfx|ppk|jks|keystore)$/i;
const SSH_KEY = /^(id_rsa|id_ed25519|id_dsa|id_ecdsa|identity)(_|$|\.)/i;
const SAFE_ENV_EXAMPLES = new Set([".env.example", ".env.sample", ".env.template", ".envrc.example", ".envrc.sample"]);
const SECRET_DIRS = new Set([".git", ".ssh", ".gnupg", "secrets"]);
const MAX_TELEMETRY_BYTES = 5 * 1024 * 1024;
const TELEMETRY_BACKUPS = 3;
const TELEMETRY_FIELDS = new Set(["event", "sessionID", "command", "errorKind", "provider", "model"]);
const TELEMETRY_EVENTS = new Set(["session.idle", "command.executed", "session.error"]);

function normalizePath(value) {
  return String(value).replace(/\\/g, "/").replace(/^file:\/\//i, "");
}

export function isSecretPath(filePath) {
  if (typeof filePath !== "string" || filePath.trim().length === 0) return false;
  const normalized = normalizePath(filePath).replace(/\/+/g, "/");
  const segments = normalized.split("/").filter(Boolean);
  const base = segments.at(-1) || "";
  if (SAFE_ENV_EXAMPLES.has(base.toLowerCase())) return false;
  if (/^\.env(?:rc)?$/i.test(base) || /^\.env(?:rc)?[._-](?!example$|sample$|template$).+/i.test(base)) return true;
  if (segments.some((s) => SECRET_DIRS.has(s.toLowerCase()))) return true;
  if (segments.some((s) => s.toLowerCase() === ".aws" || s.toLowerCase() === ".kube")) return true;
  if (base === "config.json" && segments.some((s) => s.toLowerCase() === ".docker")) return true;
  return SECRET_BASENAME.test(base) || SECRET_EXT.test(base) || SSH_KEY.test(base);
}

export const GUARDED_READ_TOOLS = new Set(["read", "grep", "glob", "list"]);

export function secretPathFromArgs(args) {
  if (!args || typeof args !== "object") return null;
  for (const key of ["filePath", "path"]) {
    const value = args[key];
    if (typeof value === "string" && value.length > 0 && isSecretPath(value)) return value;
  }
  return null;
}

// Shell command inspection is a defensive floor, not a shell parser or sandbox.
// It recognizes path-shaped tokens even when embedded in common command strings.
export function secretPathFromCommand(command) {
  if (typeof command !== "string" || command.length === 0) return null;
  const candidates = new Set();
  const patterns = [
    /(?:~\/|\.\.\/|\.\/|\/)[^\s"';&|<>`]+/g,
    /\.(?:env(?:rc)?|git)(?:[._/-][^\s"';&|<>`)]*)?/gi,
    /\b(?:secrets\/[^\s"';&|<>`]+|id_(?:rsa|dsa|ecdsa|ed25519)(?:[._-][A-Za-z0-9_.-]+)?|identity(?:[._-][A-Za-z0-9_.-]+)?|[A-Za-z0-9_./-]+\.(?:pem|key|p12|pfx|ppk|jks|keystore))\b/gi,
  ];
  for (const re of patterns) {
    for (const match of command.matchAll(re)) {
      const candidate = String(match[1] ?? match[0]).replace(/^[\s"'=(]+|[\s"',;)]+$/g, "");
      if (candidate && candidate.length < 4096) candidates.add(candidate);
    }
  }
  for (const candidate of candidates) {
    if (isSecretPath(candidate)) return candidate;
  }
  return null;
}

const DESTRUCTIVE_BASH = [
  /\brm\s+(-[a-z]*r[a-z]*\s+)+(\/$|~$|\/\*$|\.$|\/$)/i,
  /\brm\s+(-[a-z]*r[a-z]*\s+)+\/(home|root|etc|usr|var)(\s|$)/i,
  /\bmkfs(\s|$|\.)/i,
  /\bdd\s+.*\bof=\/dev\b/i,
  /:\(\)\s*\{\s*:\|\:&\s*};:/,
  /\bgit\s+reset\s+--hard\b/i,
  /\bgit\s+clean\s+.*(?:-[a-z]*f|--force)/i,
  /\bgit\s+push\b.*(?:--force(?:-with-lease)?|\s-f(?:\s|$))/i,
  /\bfind\b.*\s-delete(?:\s|$)/i,
];

export function isDestructiveCommand(command) {
  return typeof command === "string" && DESTRUCTIVE_BASH.some((re) => re.test(command));
}

function insidePath(parent, target) {
  const rel = path.relative(parent, target);
  return rel === "" || (!rel.startsWith(`..${path.sep}`) && rel !== ".." && !path.isAbsolute(rel));
}

// Fail-closed discovery: caller must supply an explicit trusted root. We do not
// discover and run validators merely because an untrusted tree contains markers.
export function findSetRoot(startDir, allowedRoot) {
  if (typeof allowedRoot !== "string" || !allowedRoot) return null;
  const allowed = path.resolve(allowedRoot);
  let realAllowed;
  let realStart;
  try {
    if (fs.lstatSync(allowed).isSymbolicLink() || !fs.statSync(allowed).isDirectory()) return null;
    realAllowed = fs.realpathSync(allowed);
    if (realAllowed !== allowed) return null;
    realStart = fs.realpathSync(path.resolve(startDir));
    if (!insidePath(realAllowed, realStart)) return null;
    for (const marker of ["manifest.yaml", "validation/validate-set.sh"]) {
      const target = path.join(realAllowed, marker);
      const st = fs.lstatSync(target);
      if (!st.isFile() || st.isSymbolicLink() || fs.realpathSync(target) !== target) return null;
    }
    return realAllowed;
  } catch {
    return null;
  }
}

export function verdictForEdit(setRoot, editedPath) {
  const resolvedRoot = path.resolve(setRoot);
  const resolvedEdit = path.resolve(editedPath);
  if (!insidePath(resolvedRoot, resolvedEdit)) return { kind: "none" };
  const base = path.basename(resolvedEdit);
  if (base === "manifest.yaml" || base === "SET.md") return { kind: "set" };
  return base === "SKILL.md" ? { kind: "skill", memberDir: path.dirname(resolvedEdit) } : { kind: "none" };
}

export function isSetCompositionPath(filePath) {
  if (typeof filePath !== "string" || filePath.length === 0) return false;
  const base = normalizePath(filePath).split("/").pop();
  return base === "SKILL.md" || base === "manifest.yaml" || base === "SET.md";
}

export function extractApplyPatchDeletes(patchText) {
  if (typeof patchText !== "string" || patchText.length === 0) return [];
  const found = [];
  for (const line of patchText.split("\n")) {
    const match = /^\*\*\*\s+Delete\s+File:\s*(.+?)\s*$/.exec(line);
    if (match && match[1].length > 0) found.push(match[1]);
  }
  return found;
}

export function redactedErrorKind(error) {
  if (error === null || error === undefined) return "unknown";
  if (typeof error === "string") return "error-string";
  if (typeof error === "object") {
    const value = error.type ?? error.code ?? error.name ?? error.kind;
    if (typeof value === "string" && value.length > 0 && value.length <= 64 && /^[A-Za-z0-9_.-]+$/.test(value)) return value;
    return "error-object";
  }
  return "unknown";
}

export function telemetryPath() {
  const home = process.env.HOME || os.homedir();
  return path.join(home, ".config", "opencode", "excellence-ops", "session-log.jsonl");
}

const VIRTUAL_FS = /^\/(proc|sys|dev)(\/|$)/;
function safeTelemetryValue(value) {
  if (typeof value !== "string") return undefined;
  const clean = value.replace(/[^A-Za-z0-9_./:-]/g, "_").slice(0, 100);
  return clean || undefined;
}

function rotateTelemetry(file) {
  let st;
  try { st = fs.lstatSync(file); } catch (err) { if (err.code === "ENOENT") return true; throw err; }
  if (st.isSymbolicLink() || !st.isFile()) return false;
  if (st.size < MAX_TELEMETRY_BYTES) return true;
  for (let n = TELEMETRY_BACKUPS; n >= 1; n--) {
    const from = n === 1 ? file : `${file}.${n - 1}`;
    const to = `${file}.${n}`;
    try { if (n === TELEMETRY_BACKUPS) fs.rmSync(to, { force: true }); fs.renameSync(from, to); } catch (err) { if (err.code !== "ENOENT") throw err; }
  }
  return true;
}

export function appendTelemetry(record) {
  const file = path.resolve(telemetryPath());
  if (VIRTUAL_FS.test(file) || !record || typeof record !== "object") return false;
  let fd;
  try {
    const dir = path.dirname(file);
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    try { fs.chmodSync(dir, 0o700); } catch {}
    const lineObj = { ts: new Date().toISOString() };
    for (const key of TELEMETRY_FIELDS) {
      if (!Object.hasOwn(record, key)) continue;
      if (key === "event") {
        if (TELEMETRY_EVENTS.has(record.event)) lineObj.event = record.event;
        continue;
      }
      const value = safeTelemetryValue(record[key]);
      if (value !== undefined) lineObj[key] = value;
    }
    if (!lineObj.event) return false;
    const line = JSON.stringify(lineObj) + "\n";
    if (Buffer.byteLength(line, "utf8") >= 2000) return false;
    if (!rotateTelemetry(file)) return false;
    const flags = fs.constants.O_APPEND | fs.constants.O_CREAT | fs.constants.O_WRONLY | (fs.constants.O_NOFOLLOW || 0);
    fd = fs.openSync(file, flags, 0o600);
    fs.fchmodSync(fd, 0o600);
    fs.writeSync(fd, line, null, "utf8");
    fs.fsyncSync(fd);
    fs.closeSync(fd);
    return true;
  } catch {
    if (fd !== undefined) { try { fs.closeSync(fd); } catch {} }
    return false;
  }
}
