---
name: unmeasurable-metric-skill
description: Validate skill quality and quality attributes with clear trigger examples. Use when the user asks for skill validation or excellence review; trigger phrases include validate skill.
metadata:
  version: "1.0.0"
---

## Purpose
Validate a skill with quality attributes, human factors, usability, and accessibility.

## Quality Attributes
Functional completeness, trigger precision, cognitive ergonomics, architecture/contracts, observability, security/least privilege, maintainability, composability, testability, and production readiness are considered.

## Human Factors
Usability, accessibility, inclusivity, clear error messages, and recovery paths are assessed.

## Success Metrics
- Trigger performance: ≥90% true positives and ≤10% false positives on at least five positive and five negative prompts.
- Task completion: ≥95% acceptance checks pass.
- Context-token efficiency: each SKILL.md remains ≤500 lines.
- Time-to-working-skill: a first-time author produces a working result within ≤60 minutes.
- Residual defect density: the amount of open critical work remaining.
