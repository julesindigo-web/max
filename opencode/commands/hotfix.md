---
description: Stabilize an emergency with minimal safe patch and a root-cause follow-up
---
Run the hotfix playbook for $ARGUMENTS (the incident or failing surface). This command may only touch staging/local by default — any production action stays governed by AGENTS.md §2 permissions.

1. Stabilize first, fix later. Prefer the least-risky stabilizer: revert the offending change, disable the feature flag, or isolate the component. Root-cause fixes come after the bleeding stops.
2. Minimal patch. Smallest diff that restores correct behavior for the incident path. No refactoring, dependency changes, or opportunistic work.
3. Regression test the failure mode before or with the patch; the original failure must have a test that fails without the patch and passes with it.
4. Root-cause follow-up: state the true cause hypothesis, evidence so far, and where it is recorded (ticket or ADR), so the permanent fix is not silently dropped.
5. Verify per AGENTS.md §8.6 migrated minimum: tests for the incident path, affected full suite, and dry-run of the rollback path. Screenshot or log evidence for the stabilized state when UI or service-level incident.
6. Report per AGENTS.md §12.3 with rollback plan first: how to undo, what is patched, what remains at risk, the follow-up owner, and any production steps that still require explicit user authorization.

Rules: never widen scope; never mask evidence (falsified logs, swallowed errors); never ship the workaround labeled as a root fix — label partial fixes as temporary with expiry criteria.

Success criteria: the incident path is stabilized with the smallest reversible change; a regression check proves the patch; the rollback path and root-cause follow-up are explicit; any production action remains unexecuted without user authorization.
