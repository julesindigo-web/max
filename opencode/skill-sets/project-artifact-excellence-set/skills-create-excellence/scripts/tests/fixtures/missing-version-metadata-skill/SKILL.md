---
name: missing-version-metadata-skill
description: Validate skill structure and quality attributes with clear triggers. Use when checking skill packages and their metadata; trigger phrases include skill validation.
metadata:
  set-membership: test-set
---

## Purpose
Validate a well-structured skill package.

## Quality Attributes
Functional completeness, trigger precision, cognitive ergonomics, architecture/contracts, observability, security/least privilege, maintainability, composability, testability, and production readiness are assessed.

## Human Factors
Instructions use clear language, accessible states, and error-recovery guidance.

## Success Metrics
- Trigger performance: ≥90% true positives and ≤10% false positives on at least five positive and five negative prompts.
- Task completion: ≥95% of acceptance checks pass.
- Context-token efficiency: this SKILL.md remains ≤500 lines.
- Time-to-working-skill: a first-time author creates a valid skill within ≤60 minutes.
- Residual defect density: zero open Critical or Major findings remain after final validation.
