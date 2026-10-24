---
name: missing-human-factors-skill
description: Validate skill quality. Use when checking a skill. Triggers include structural validation.
metadata:
  version: "1.0.0"
---

# Missing Human Factors Fixture

## Quality Attributes
Quality attributes are explicitly mentioned.

## Success Metrics
- Trigger performance: ≥90% true positives across 5 positive prompts and ≤10% false positives across 5 negative prompts.
- Task completion: ≥95% of acceptance checks pass.
- Context-token efficiency: SKILL.md remains ≤500 lines.
- Time-to-working-skill: valid fixture created within ≤60 minutes.
- Residual defect density: zero Critical defects after validation.
