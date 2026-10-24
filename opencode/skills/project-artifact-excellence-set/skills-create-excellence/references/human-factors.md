# Human Factors Checklist for Skills and Plugin Sets

## Author Experience
- Clear step-by-step process with explicit decision points.
- Checklists that reduce working memory load.
- Positive and negative examples for difficult decisions (especially description writing).
- Immediate feedback via validation scripts.
- Low frustration path when validation fails (actionable error messages).

## Runtime Agent Experience
- Progressive disclosure keeps context window efficient.
- Imperative language is unambiguous and action-oriented.
- Failure modes and recovery are stated so the agent can self-correct or report clearly.
- No hidden assumptions about prior knowledge beyond base model capability.

## Cognitive Ergonomics
- Chunking: related instructions grouped under clear headings.
- Signaling: critical rules and anti-patterns highlighted.
- Consistency: terminology and structure stable across skills in a set.
- Predictability: same quality bar and process every time.

## Inclusivity and Accessibility of Language
- Avoid unnecessary jargon or define it on first use.
- Prefer concrete over abstract statements.
- Support authors with varying expertise levels via examples and templates.

## Trust and Emotional Experience
- Skill behaves as described (high trigger reliability).
- Errors are informative rather than opaque.
- Success is measurable so the user/agent gains confidence.
- Residual risks are openly declared rather than hidden.

## Application Rule
Every skill produced under this excellence standard must address the above dimensions. Silence is a Major finding. For skill sets, apply the checklist both at member level and at set level (shared language, consistent process, unified validation feedback).


## Set-Level Milestone Integration
At project milestones, use this skill-authoring checklist alongside `project-artifact-auditor/references/human-factors-usability.md` and `shared/references/holistic-evaluation.md`. Distinguish the human factors of the skill author/editor, the agent using the skill, the project's end user, and the operator/maintainer. For each relevant role, assess cognitive load, trigger/interaction predictability, errors and recovery, accessibility/inclusion, trust, and operational clarity. Do not infer a successful user outcome from skill structure or test presence alone.

## Accessibility & Inclusive Design (Agent-Facing)
See the dedicated checklist: `accessibility-agent-facing.md`.  
Apply the residual-risk template from `../../shared/references/residual-risk-template.md` when any accessibility or human-factors dimension remains untested.
