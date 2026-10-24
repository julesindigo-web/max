# Project Artifact Excellence Skill Set — v2.0.0

Full-lifecycle AI agent engineering ecosystem: fourteen member skills composing audit, skill creation, SDLC delivery, fullstack mastery, and premium human-centric quality with controlled evidence-driven improvement feedback.

- Start with [`SET.md`](SET.md) (purpose, responsibilities, metrics, release gate).
- Set contract: [`manifest.yaml`](manifest.yaml). Traceability: [`TRACEABILITY.md`](TRACEABILITY.md).
- Audit evidence: [`AUDIT-REPORT-MASTERPIECE.md`](AUDIT-REPORT-MASTERPIECE.md). Changes: [`REMEDIATION-CHANGELOG.md`](REMEDIATION-CHANGELOG.md) and [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
- Evaluate: [`evaluation/runtime-protocol.md`](evaluation/runtime-protocol.md). Operate: [`docs/OPERATIONS-RUNBOOK.md`](docs/OPERATIONS-RUNBOOK.md).

## Validate

```bash
bash validation/validate-set.sh   # 8 gates must pass
```

## Install (opencode, user level)

No config change required: `~/.config/opencode/skills/*/SKILL.md` is auto-loaded recursively. The runtime mirror preserves the set-root layout so `../shared/*` references resolve identically.

> Mirror note (PA-VAL-08): validate only in the canonical source (`skill-sets/project-artifact-excellence-set`); gates 4/6 plus 2 release tests fail by-design in the runtime mirror.

## Release

```bash
python3 scripts/build-release.py --root . --output ../project-artifact-excellence-set.zip
python3 scripts/verify-release.py ../project-artifact-excellence-set.zip
```
