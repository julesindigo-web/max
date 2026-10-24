// Unit tests for excellence-ops.js — node:test, dependency-free.
// Covers: secret-path guard (+/-), directory-scoped path guard (+/-),
// destructive-command guard (+/-), set-root discovery, verdict selection,
// apply_patch delete-guard (+/-), telemetry append + redacted event hook,
// hook wiring (including input.args runtime shape).
import { describe, it, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as pluginModule from "../../plugins/excellence-ops.js";
import {
  SecretsGuardPlugin,
  ExcellenceValidatePlugin,
  ExcellenceTelemetryPlugin,
} from "../../plugins/excellence-ops.js";
import {
  appendTelemetry,
  extractApplyPatchDeletes,
  findSetRoot,
  isDestructiveCommand,
  isSecretPath,
  isSetCompositionPath,
  redactedErrorKind,
  secretPathFromArgs,
  secretPathFromCommand,
  telemetryPath,
  verdictForEdit,
} from "../lib/excellence-ops-helpers.js";

const TEST_DIR = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_ROOT = path.resolve(TEST_DIR, "../..");
const SET = path.join(CONFIG_ROOT, "skill-sets", "project-artifact-excellence-set");

describe("plugin module contract", () => {
  it("exports only OpenCode plugin factories from plugins/", () => {
    assert.deepEqual(Object.keys(pluginModule).sort(), [
      "ExcellenceTelemetryPlugin",
      "ExcellenceValidatePlugin",
      "SecretsGuardPlugin",
    ]);
    for (const factory of Object.values(pluginModule)) assert.equal(typeof factory, "function");
  });
});

describe("isSecretPath", () => {
  it("blocks .env variants, .git, keys, secrets dirs, credential basenames", () => {
    for (const p of [
      "/proj/.env", "/proj/.env.local", ".env", ".envrc", "./.envrc",
      "secrets/api.json", ".git/config", "~/.ssh/id_dsa", "/home/u/.ssh/id_ecdsa", "/home/u/.ssh/id_rsa",
      "/repo/.git/config", "/home/u/.git",
      "/proj/secrets/api.json", "/etc/ssh/id_rsa", "/home/u/.ssh/id_ed25519",
      "/tmp/x.pem", "/tmp/cert.key", "/tmp/bundle.p12",
      "/proj/secret-config.yaml", "/proj/credentials.json",
    ]) {
      assert.equal(isSecretPath(p), true, p);
    }
  });
  it("allows ordinary files including docs that mention secrets", () => {
    for (const p of [
      "/proj/src/index.ts", "/proj/README.md",
      path.join(CONFIG_ROOT, "skills/x/security-vulnerability-auditor/SKILL.md"),
      "/proj/design-tokens.json", "/proj/token-bucket.js",
      "/proj/.envrc.example", "/proj/.env.example", "/proj/.env.sample", "",
    ]) {
      if (p === "") { assert.equal(isSecretPath(p), false, "(empty)"); continue; }
      assert.equal(isSecretPath(p), false, p);
    }
  });
});

describe("secretPathFromArgs (v2 directory scope)", () => {
  it("finds secret filePath and directory-scoped path", () => {
    assert.equal(secretPathFromArgs({ filePath: "/x/.env" }), "/x/.env");
    assert.equal(secretPathFromArgs({ path: "/proj/secrets" }), "/proj/secrets");
    assert.equal(secretPathFromArgs({ path: "/proj/secrets/api.json" }), "/proj/secrets/api.json");
    assert.equal(secretPathFromArgs({ filePath: "/x/README.md", path: "/proj/.git" }), "/proj/.git");
  });
  it("ignores patterns and allows ordinary dirs (no false positives on docs)", () => {
    assert.equal(secretPathFromArgs({ pattern: "secret", path: "/proj/src" }), null);
    assert.equal(secretPathFromArgs({ pattern: ".env" }), null);
    assert.equal(secretPathFromArgs({ path: "/proj/src" }), null);
    assert.equal(secretPathFromArgs({ path: "/proj/design-tokens.json" }), null);
    assert.equal(secretPathFromArgs({}), null);
    assert.equal(secretPathFromArgs(null), null);
  });
});

describe("secretPathFromCommand", () => {
  it("blocks common shell and embedded-code references to secrets", () => {
    for (const command of [
      "cat .env", "grep API_TOKEN .envrc", "sed -n '1,10p' ~/.ssh/id_ecdsa",
      "python3 -c \"open('/home/user/.ssh/id_dsa').read()\"", "cat ./secrets/api.json",
      "git show HEAD:.git/config", "cat /tmp/client.pem", "head -n 5 .git/config",
    ]) assert.ok(secretPathFromCommand(command), command);
  });
  it("allows safe examples, docs, and ordinary test commands", () => {
    for (const command of ["cat .env.example", "grep secret README.md", "python3 -m pytest tests/test_auth.py", "cat src/token-bucket.js"]) assert.equal(secretPathFromCommand(command), null, command);
  });
});

describe("isDestructiveCommand", () => {
  it("flags rm -rf on roots, mkfs, dd to devices, fork bombs", () => {
    for (const c of ["rm -rf /", "sudo rm -rf ~", "rm -rf /*", "rm -rf /etc", "mkfs.ext4 /dev/sda1", "dd if=x of=/dev/sda", ":(){ :|:& };:"]) {
      assert.equal(isDestructiveCommand(c), true, c);
    }
  });
  it("allows scoped commands", () => {
    for (const c of ["rm -rf ./build", "rm -rf /tmp/scratch", "git status", "mkfsdoc run", "echo dd"]) {
      assert.equal(isDestructiveCommand(c), false, c);
    }
  });
});

describe("findSetRoot + verdictForEdit", () => {
  it("discovers only the explicitly allowed canonical root from a nested member dir", () => {
    const nested = path.join(SET, "skills-create-excellence", "scripts");
    assert.equal(findSetRoot(nested, SET), SET);
  });
  it("rejects unknown and untrusted marker roots", () => {
    assert.equal(findSetRoot(os.tmpdir()), null);
    const fake = fs.mkdtempSync(path.join(os.tmpdir(), "untrusted-set-"));
    try {
      fs.mkdirSync(path.join(fake, "validation"));
      fs.writeFileSync(path.join(fake, "manifest.yaml"), "untrusted: true\n");
      fs.writeFileSync(path.join(fake, "validation", "validate-set.sh"), "#!/bin/sh\nexit 0\n");
      assert.equal(findSetRoot(fake, SET), null);
    } finally { fs.rmSync(fake, { recursive: true, force: true }); }
  });
  it("does not select skill-like files outside the allowed root", () => {
    assert.deepEqual(verdictForEdit(SET, path.join(os.tmpdir(), "untrusted", "SKILL.md")), { kind: "none" });
  });
  it("selects full gate for manifest/SET, single gate for SKILL.md, none otherwise", () => {
    assert.deepEqual(verdictForEdit(SET, path.join(SET, "manifest.yaml")), { kind: "set" });
    assert.deepEqual(verdictForEdit(SET, path.join(SET, "SET.md")), { kind: "set" });
    const member = path.join(SET, "project-artifact-auditor");
    assert.deepEqual(verdictForEdit(SET, path.join(member, "SKILL.md")), { kind: "skill", memberDir: member });
    assert.deepEqual(verdictForEdit(SET, path.join(member, "references", "x.md")), { kind: "none" });
  });
});

describe("isSetCompositionPath + extractApplyPatchDeletes", () => {
  it("flags SKILL.md/manifest.yaml/SET.md basenames at any depth", () => {
    assert.equal(isSetCompositionPath("src/SKILL.md"), true);
    assert.equal(isSetCompositionPath("manifest.yaml"), true);
    assert.equal(isSetCompositionPath("a/b/SET.md"), true);
    assert.equal(isSetCompositionPath("src/index.ts"), false);
    assert.equal(isSetCompositionPath("SKILL.md.bak"), false);
    assert.equal(isSetCompositionPath(""), false);
  });
  it("parses Delete File markers and ignores other patch lines", () => {
    const patch = [
      "*** Add File: src/new.ts",
      "*** Delete File: src/obsolete.ts",
      "*** Delete File: project-artifact-auditor/SKILL.md",
      "*** Update File: README.md",
    ].join("\n");
    assert.deepEqual(extractApplyPatchDeletes(patch), ["src/obsolete.ts", "project-artifact-auditor/SKILL.md"]);
    assert.deepEqual(extractApplyPatchDeletes("no markers here"), []);
    assert.deepEqual(extractApplyPatchDeletes(null), []);
  });
});

describe("redactedErrorKind", () => {
  it("never returns message bodies or secret-adjacent content", () => {
    assert.equal(redactedErrorKind(null), "unknown");
    assert.equal(redactedErrorKind(undefined), "unknown");
    assert.equal(redactedErrorKind("ProviderAuthError: sk-ant-xyz leaked"), "error-string");
    assert.equal(redactedErrorKind({ message: "AKIA123 secret inside" }), "error-object");
    assert.equal(redactedErrorKind({ type: "ProviderAuthError" }), "ProviderAuthError");
    assert.equal(redactedErrorKind({ code: "ECONNREFUSED" }), "ECONNREFUSED");
    assert.equal(redactedErrorKind({ type: "evil; rm -rf /" }), "error-object");
  });
  it("collapses non-string scalars to unknown (never leaks numeric/boolean errors)", () => {
    // Regression for global-100 push 2026-10-15: covers redactedErrorKind
    // final `return "unknown"` for typeof error === number/boolean/bigint.
    assert.equal(redactedErrorKind(42), "unknown");
    assert.equal(redactedErrorKind(true), "unknown");
    assert.equal(redactedErrorKind(0), "unknown");
  });
});

describe("SecretsGuardPlugin wiring", () => {
  it("throws on secret read and destructive bash, passes normal tools", async () => {
    const hooks = await SecretsGuardPlugin({});
    const before = hooks["tool.execute.before"];
    assert.equal(typeof before, "function");
    await assert.rejects(() => before({ tool: "read" }, { args: { filePath: "/x/.env" } }), /SecretsGuard/);
    await assert.rejects(() => before({ tool: "bash" }, { args: { command: "rm -rf /" } }), /SecretsGuard/);
    await assert.rejects(() => before({ tool: "bash" }, { args: { command: "cat .envrc" } }), /SecretsGuard/);
    await assert.rejects(() => before({ tool: "bash" }, { args: { command: "git reset --hard HEAD" } }), /SecretsGuard/);
    await before({ tool: "read" }, { args: { filePath: "/x/README.md" } });
    await before({ tool: "bash" }, { args: { command: "git status" } });
  });
  it("v2: blocks directory-scoped grep/glob/list paths, never blocks on pattern alone", async () => {
    const hooks = await SecretsGuardPlugin({});
    const before = hooks["tool.execute.before"];
    await assert.rejects(() => before({ tool: "grep" }, { args: { pattern: "foo", path: "/proj/secrets" } }), /SecretsGuard/);
    await assert.rejects(() => before({ tool: "glob" }, { args: { pattern: "**/*.json", path: "/proj/secrets" } }), /SecretsGuard/);
    await assert.rejects(() => before({ tool: "list" }, { args: { path: "/x/.env" } }), /SecretsGuard/);
    await before({ tool: "grep" }, { args: { pattern: "secret", path: "/proj/src" } });
    await before({ tool: "glob" }, { args: { pattern: "**/*.ts", path: "/proj/src" } });
    await before({ tool: "read" }, { args: { filePath: "/proj/design-tokens.json" } });
  });
});

describe("ExcellenceValidatePlugin wiring", () => {
  it("ignores non-edit tools and files outside sets", async () => {
    const hooks = await ExcellenceValidatePlugin({});
    const after = hooks["tool.execute.after"];
    const out = { args: { filePath: "/tmp/notes.txt" }, output: "done" };
    await after({ tool: "read" }, out);
    assert.equal(out.output, "done");
  });
  it("never executes a validator found in an untrusted repository", async () => {
    const fake = fs.mkdtempSync(path.join(os.tmpdir(), "untrusted-validator-"));
    const marker = path.join(fake, "executed.txt");
    try {
      fs.mkdirSync(path.join(fake, "validation"));
      fs.writeFileSync(path.join(fake, "manifest.yaml"), "fake: true\n");
      fs.writeFileSync(path.join(fake, "validation", "validate-set.sh"), `#!/usr/bin/env bash\nprintf executed > '${marker}'\nexit 0\n`, { mode: 0o700 });
      fs.writeFileSync(path.join(fake, "SKILL.md"), "---\nname: untrusted\n---\n");
      const hooks = await ExcellenceValidatePlugin({});
      const prev = process.env.EXCELLENCE_AUTOVALIDATE;
      delete process.env.EXCELLENCE_AUTOVALIDATE;
      try {
        const out = { output: "edited" };
        await hooks["tool.execute.after"]({ tool: "edit", args: { filePath: path.join(fake, "SKILL.md") } }, out);
        assert.equal(out.output, "edited");
        assert.equal(fs.existsSync(marker), false);
      } finally {
        if (prev === undefined) delete process.env.EXCELLENCE_AUTOVALIDATE;
        else process.env.EXCELLENCE_AUTOVALIDATE = prev;
      }
    } finally { fs.rmSync(fake, { recursive: true, force: true }); }
  });

  it("appends reminder (not execution) when EXCELLENCE_AUTOVALIDATE=0", async () => {
    const hooks = await ExcellenceValidatePlugin({});
    const after = hooks["tool.execute.after"];
    const prev = process.env.EXCELLENCE_AUTOVALIDATE;
    process.env.EXCELLENCE_AUTOVALIDATE = "0";
    try {
      const out = { args: { filePath: path.join(SET, "manifest.yaml") }, output: "edited" };
      await after({ tool: "edit" }, out);
      assert.match(out.output, /EXCELLENCE_AUTOVALIDATE=0/);
    } finally {
      if (prev === undefined) delete process.env.EXCELLENCE_AUTOVALIDATE;
      else process.env.EXCELLENCE_AUTOVALIDATE = prev;
    }
  });
  it("v2: reads runtime input.args shape for write/edit (not only output.args)", async () => {
    const hooks = await ExcellenceValidatePlugin({});
    const after = hooks["tool.execute.after"];
    const prev = process.env.EXCELLENCE_AUTOVALIDATE;
    process.env.EXCELLENCE_AUTOVALIDATE = "0";
    try {
      const out = { args: {}, output: "edited" };
      await after({ tool: "edit", args: { filePath: path.join(SET, "manifest.yaml") } }, out);
      assert.match(out.output, /EXCELLENCE_AUTOVALIDATE=0/);
    } finally {
      if (prev === undefined) delete process.env.EXCELLENCE_AUTOVALIDATE;
      else process.env.EXCELLENCE_AUTOVALIDATE = prev;
    }
  });
  it("blocks apply_patch set-composition deletions before mutation", async () => {
    const hooks = await ExcellenceValidatePlugin({});
    const before = hooks["tool.execute.before"];
    await assert.rejects(() => before({ tool: "apply_patch", args: { patchText: "*** Delete File: project-artifact-auditor/SKILL.md\n" } }, { args: {} }), /blocked apply_patch deletion/);
    await before({ tool: "apply_patch", args: { patchText: "*** Delete File: src/obsolete.ts\n" } }, { args: {} });
  });
  it("v2: stays silent when apply_patch deletes only ordinary files", async () => {
    const hooks = await ExcellenceValidatePlugin({});
    const after = hooks["tool.execute.after"];
    const out = { args: {}, output: "patched" };
    await after(
      { tool: "apply_patch", args: { patchText: "*** Delete File: src/obsolete.ts\n" } },
      out
    );
    assert.equal(out.output, "patched");
  });
});

describe("ExcellenceTelemetryPlugin wiring", () => {
  let tmpHome, prevHome;
  beforeEach(() => {
    tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), "home-"));
    prevHome = process.env.HOME;
    process.env.HOME = tmpHome;
  });
  afterEach(() => {
    if (prevHome === undefined) delete process.env.HOME;
    else process.env.HOME = prevHome;
    fs.rmSync(tmpHome, { recursive: true, force: true });
  });
  it("appends JSONL for session.idle and command.executed, injects compaction context", async () => {
    const hooks = await ExcellenceTelemetryPlugin({});
    assert.equal(await hooks["session.idle"]({ sessionID: "s1" }), undefined);
    await hooks["command.executed"]({ sessionID: "s1", command: "audit" });
    const lines = fs.readFileSync(telemetryPath(), "utf-8").trim().split("\n");
    assert.equal(lines.length, 2);
    assert.equal(JSON.parse(lines[0]).event, "session.idle");
    assert.equal(JSON.parse(lines[1]).command, "audit");
    const output = { context: [] };
    await hooks["experimental.session.compacting"]({}, output);
    assert.equal(output.context.length, 1);
    assert.match(output.context[0], /Calibration law holds/);
  });
  it("never touches virtual filesystems and never throws on unusable locations", async () => {
    const hooks = await ExcellenceTelemetryPlugin({});
    process.env.HOME = "/proc/definitely-not-writable";
    await hooks["session.idle"]({ sessionID: "s1" }); // must return fast, not throw
    // A path blocked by a regular file fails closed and fast (ENOTDIR).
    const obstacle = path.join(tmpHome, "obstacle-file");
    fs.writeFileSync(obstacle, "x");
    process.env.HOME = path.join(obstacle, "sub");
    await hooks["command.executed"]({ sessionID: "s1", command: "audit" }); // must not throw
  });
  it("v2: event hook logs redacted session.idle/command.executed/session.error without bodies", async () => {
    const hooks = await ExcellenceTelemetryPlugin({});
    assert.equal(typeof hooks.event, "function");
    await hooks.event({ event: { type: "session.idle", properties: { sessionID: "s1" } } });
    await hooks.event({ event: { type: "command.executed", properties: { sessionID: "s1", name: "audit", arguments: "SECRET-should-not-log" } } });
    await hooks.event({ event: { type: "session.error", properties: { sessionID: "s1", providerID: "openai", modelID: "gpt-6", error: { type: "ProviderAuthError", message: "sk-ant-SECRET" } } } });
    await hooks.event({ event: { type: "message.updated", properties: {} } }); // ignored
    const lines = fs.readFileSync(telemetryPath(), "utf-8").trim().split("\n");
    assert.equal(lines.length, 3);
    const recs = lines.map((l) => JSON.parse(l));
    assert.equal(recs[0].event, "session.idle");
    assert.equal(recs[1].command, "audit");
    assert.ok(!JSON.stringify(recs[1]).includes("SECRET-should-not-log"), "arguments must not be logged");
    assert.equal(recs[2].errorKind, "ProviderAuthError");
    assert.equal(recs[2].provider, "openai");
    assert.equal(recs[2].model, "gpt-6");
    assert.ok(!JSON.stringify(recs[2]).includes("sk-ant-SECRET"), "message bodies must not be logged");
  });
  it("redacts unknown fields, sets private permissions, and rotates oversized logs", async () => {
    const log = telemetryPath();
    fs.mkdirSync(path.dirname(log), { recursive: true, mode: 0o700 });
    fs.writeFileSync(log, "x".repeat(5 * 1024 * 1024 + 8));
    assert.equal(appendTelemetry({ event: "session.idle", sessionID: "rotate-test", message: "secret-value", input: "never-log" }), true);
    assert.equal(fs.existsSync(`${log}.1`), true);
    const stat = fs.statSync(log);
    assert.equal(stat.mode & 0o777, 0o600);
    const records = fs.readFileSync(log, "utf8").trim().split("\\n").map((line) => JSON.parse(line));
    assert.equal(records.length, 1);
    assert.deepEqual(Object.keys(records[0]).sort(), ["event", "sessionID", "ts"]);
    assert.ok(!JSON.stringify(records).includes("secret-value"));
  });
  it("v2: session.error alias redacts string errors and never throws", async () => {
    const hooks = await ExcellenceTelemetryPlugin({});
    await hooks["session.error"]({ sessionID: "s9", error: "boom with AKIAIOSFODNN7EXAMPLE inside" });
    const lines = fs.readFileSync(telemetryPath(), "utf-8").trim().split("\n");
    assert.equal(lines.length, 1);
    const rec = JSON.parse(lines[0]);
    assert.equal(rec.event, "session.error");
    assert.equal(rec.errorKind, "error-string");
    assert.ok(!JSON.stringify(rec).includes("AKIAIOSFODNN7EXAMPLE"));
  });
});
