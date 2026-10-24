---
description: Run the full 8-gate skill-set validation and report verdicts
subtask: false
---
Validate the skill set at $ARGUMENTS (default: the installed project-artifact-excellence-set canonical source).
Set root: `skill-sets/project-artifact-excellence-set` (canonical source; `skills/` is the runtime mirror — validate only in canonical).

Locate the set root containing manifest.yaml and validation/validate-set.sh, run `bash validation/validate-set.sh` from that root, and report the verdict of each of the 8 gates plus the final result. On any FAIL, show the failing gate output verbatim, classify severity, and propose the smallest-effective remediation with a regression pointer. A structural PASS is not evidence of runtime, user, accessibility, security, or performance quality — state that explicitly.

Arguments: `$ARGUMENTS` is the set root (optional). Examples: `/validate-set`, `/validate-set ~/.config/opencode/skill-sets/project-artifact-excellence-set`.

Success criteria: all 8 gate verdicts are reported individually with evidence; any FAIL shows verbatim gate output plus severity plus smallest-effective remediation; the report states explicitly that structural PASS does not imply runtime/user/accessibility/security/performance quality.
