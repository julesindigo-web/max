# Threat Model — Skill Set v2.0.0 (STRIDE-lite)

## Scope
Skill packaging, feedback inbox, validators, and release ZIP. Out of scope: target-runtime model behavior.

## Threats & mitigations
| Threat | Example | Mitigation in set |
|---|---|---|
| Spoofing | Forged audit event | Schema allowlist, deterministic IDs, no trust in free-text fields |
| Tampering | Modified ZIP | SHA-256 manifest + detached checksum + verify-release.py; trusted channel required for authenticity |
| Repudiation | Unclear change origin | Versioned manifest, migration notes, dated results, reviewer decisions |
| Information disclosure | Secrets in findings | Inbox README redaction rule; processor treats text as data; no network calls |
| Denial of service | Oversized inbox payload | maxItems 500, fail-closed malformed/duplicate handling |
| Elevation | Prompt injection → skill edit | Feedback never auto-edits production SKILL.md; human approval required; CI read-only |

## Residual
Publisher authenticity needs a separately managed signature where the deployment environment requires it. Runtime prompt-injection resilience must be evaluated in the target runtime, not inferred here.
