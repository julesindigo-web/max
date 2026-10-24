---
description: Refactor with a behavior lock — freeze first, change structure only
---
Run the refactor playbook for $ARGUMENTS (the code area, module, or smell report).

1. Freeze behavior: identify the observable contract (tests, types, consumers) and add characterization tests where coverage is missing before touching structure. State the frozen contract explicitly.
2. Plan the change: pick one smell class at a time (per the routing table, invoke `code-refactoring-optimizer` when the task is smell-driven or complexity reduction). No drive-by refactors, reformatting, renames, or dependency churn outside the declared target.
3. Refactor in small green steps: structure changes only, tests green after every step, never mix behavior change into the same commit. Keep the diff reviewable.
4. Preserve assertions: do not delete, weaken, re-purpose, or skip tests; test edits must stay behavior-faithful (updating *how* facts are asserted is allowed when the behavior contract is unchanged and stated).
5. Verify per AGENTS.md §8.6: full test suite, typecheck, lint; code coverage delta reported; performance not regressed where the changed code is on a hot path; no new warnings.
6. Report per AGENTS.md §12.3: what structural change was made, how behavior is proven unchanged, coverage before/after, and incidental follow-ups discovered but not done, each as a named item.

Success criteria: the behavior contract is frozen and still passes; no assertion or quality threshold was weakened; typecheck, lint, relevant tests, and performance evidence for hot paths are reported with observed outcomes.
