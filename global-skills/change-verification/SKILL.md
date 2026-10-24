---
name: change-verification
description: Verify a completed implementation change. Use when the user requests validation, a release-readiness check, or an evidence-based handoff.
---

# Change Verification

Use this skill for an explicit verification or handoff request. It complements, rather than replaces, focused checks during implementation.

1. Establish the requested outcome, changed paths, risk level, repository-native scripts, and what cannot be tested locally. Inspect the diff before choosing checks.
2. Run the narrowest checks that prove the changed behavior, then add integration, UI, migration, performance, security, or full-suite checks when the impact warrants them. Prefer the repository's documented commands over guessed equivalents.
3. Treat every failure as evidence: determine whether it was introduced by the change, appears pre-existing, or is inconclusive. Do not weaken checks, delete assertions, or retry until green without diagnosing the cause.
4. For UI work, include automated accessibility checks and a keyboard/rendered-path check when tools exist. For API/data work, include contract and negative-authorization coverage where applicable. For dependency or infrastructure work, inspect the lockfile/config diff and use the relevant audit or dry-run.
5. Deliver an evidence-based verdict: outcome, checks actually run with observed result, checks not run and why, residual risks, and the smallest next action. Do not edit implementation files unless the user also asked for fixes.
