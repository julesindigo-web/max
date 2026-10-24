---
name: missing-quality-attributes-skill
description: Validate skill packages and measurable quality requirements. Use when checking skill structure and consistency; trigger phrases include skill validation.
metadata:
  version: "1.0.0"
---

## Purpose
Validate a skill package and its quality attributes.

## Human Factors
Instructions support usability, accessibility, and error recovery.

## Success Metrics
- Trigger performance: ≥90% true positives and ≤10% false positives on at least five positive and five negative prompts.
- Task completion: ≥95% acceptance checks pass.
- Context-token efficiency: SKILL.md remains ≤500 lines.
- Time-to-working-skill: a valid result within ≤60 minutes.
- Residual defect density: zero open Critical or Major defects.
