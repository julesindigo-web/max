---
description: Fix a bug root-cause-first with a regression test gate and sibling sweep
---
Run the bug playbook for $ARGUMENTS (the bug report, error output, or failing behavior).

1. Reproduce reliably: capture the exact reproduction (input, command, environment), minimize it to the smallest failing case, and quantify observed vs expected. If reproduction fails, report the blocker instead of fixing by guess.
2. Isolate and hypothesize: form ranked hypotheses from logs, stack traces, and recent git history; test each by observation — never by assuming the first plausible cause.
3. Write the failing regression test first; watch it fail for the reported reason, not an unrelated one.
4. Fix at the root where the defect lives, not at the symptom site. Match surrounding conventions and AGENTS.md §8. No drive-by refactors.
5. Sibling sweep: search for the same defect class elsewhere in the codebase; report every location found and fix only those in scope (out-of-scope items become follow-ups).
6. Verify: the new regression test passes, neighbor tests pass, the full affected suite runs clean, and the original repro is confirmed gone. AGENTS.md §8.6 matrix applies to touched surfaces.
7. Report per AGENTS.md §12.3 including root cause, impact, and the regression fixture path.

Rules: never change or remove tests to make the failure disappear; never widen scope to escape a hard problem (AGENTS.md autonomy §2.5 pushback applies — re-diagnose after three failed approaches).

Success criteria: the original defect is reproduced and absent after the root fix; a regression test failed before and passes after; affected neighbors pass; deferred sibling cases and unrun checks are explicitly reported.
