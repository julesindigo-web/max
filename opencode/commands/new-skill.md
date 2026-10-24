---
description: Create or upgrade a skill to excellence standard with metrics and validation
agent: skill-builder
subtask: true
---
Create or upgrade a skill for $ARGUMENTS to excellence standard.
Canonical skill: `skills-create-excellence` (covers `/plugin-creator` requests; there is no separate `/plugin-creator` — see AGENTS.md §6a).

Follow the skill-builder method strictly: clarify use cases and must-trigger utterances first (ask if ambiguous), design frontmatter and contracts, initialize structure under the correct set root, author imperatively with all five canonical metric dimensions (ten fields each) and explicit failure modes, keep SKILL.md at or under 500 lines, implement tested scripts plus one-level references, validate multi-layer until gates pass, and document residual risks. Add a regression fixture for every fixed escape. Never auto-merge production skills on feedback events alone.

Arguments: `$ARGUMENTS` is the skill brief (name plus goal). Examples: `/new-skill rate-limiting for backend APIs`, `/new-skill accessibility checklist for checkout flow`.

Success criteria: the package declares all five canonical metric dimensions with measurable targets; SKILL.md is at or under 500 lines with depth in references/; deterministic scripts are executable and tested; multi-layer validation passes with a regression fixture per fixed escape; residual risks and next validation steps are documented.
