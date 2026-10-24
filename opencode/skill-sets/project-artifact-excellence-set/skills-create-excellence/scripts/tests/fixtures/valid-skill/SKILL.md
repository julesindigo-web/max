---
name: valid-skill
description: Validate well-formed skill packages and report deterministic results. Use when checking skill quality. Triggers include validating a skill or checking a skill package.
metadata:
  version: "1.0.0"
---

# Valid Skill

## Purpose
A small but structurally complete skill fixture for validator regression tests.

## Quality Attributes
This fixture tests measurable quality attributes and deterministic validation.

## Human Factors
Instructions are understandable and usability checks are explicit.

## Success Metrics
- Trigger performance: Definition: proportion of labeled positive prompts that activate the intended skill and labeled negative prompts that do not; Unit/formula: true-positive rate = TP/(TP+FN) and false-positive rate = FP/(FP+TN), both reported as percentages; Target: ≥90% true-positive/recall and ≤10% false-positive rate; Rationale: preserves intended coverage without broad unrelated activation; Source: evaluation/trigger-evaluation-matrix.json plus target-runtime activation logs; Sample: at least 5 positive and 5 negative prompts per skill, with 12+12 in the current authored matrix (minimum 5+5 per validator); Segmentation: per skill, positive/negative class, and prompt family; Method: execute each prompt in the intended runtime, log activation, and adjudicate expected labels independently; Owner: release evaluator independent of the skill author where feasible; Window: each release candidate and after any trigger-description change
- Task completion: Definition: fraction of applicable acceptance checks completed successfully without unplanned workaround; Unit/formula: passed applicable checks divided by all applicable checks × 100%; Target: ≥95% acceptance/completion checks pass; Rationale: structural validity alone does not prove task usefulness; Source: CI acceptance results and a versioned representative task-evaluation ledger; Sample: every mandatory CI check plus at least 5 representative end-to-end tasks per release; Segmentation: by member skill, task type, and criticality; Method: predefine binary acceptance criteria, record pass/fail and evidence for every task, and exclude N/A only with rationale; Owner: evaluation lead; Window: each release candidate and after material workflow changes
- Context-token efficiency: Definition: instruction footprint and relevance of reference material loaded for a representative task; Unit/formula: line count per SKILL.md plus references actually loaded per task; Target: each SKILL.md ≤500 lines and only task-relevant references are loaded; Rationale: bounds baseline context overhead while preserving deep reference coverage; Source: repository files and sampled execution traces; Sample: every member SKILL.md plus at least 5 representative task traces per release; Segmentation: by member skill and task class; Method: measure line counts automatically and review loaded-reference traces against task needs; Owner: skill-set maintainer; Window: every release candidate and after reference reorganization
- Time-to-working-skill: Definition: elapsed guided time from task start until a first-time author creates a structurally valid, tested, usable skill result; Unit/formula: minutes from recorded start to acceptance of the first result; Target: ≤60 minutes; Rationale: checks authoring workflow learnability rather than code presence alone; Source: timed guided-evaluation records; Sample: at least 5 first-time authors for a major release evaluation, or a clearly labeled pilot when fewer are available; Segmentation: by author experience and task complexity; Method: use the same starter brief, record elapsed time and assistance, and report median plus range; Owner: human-factors evaluator; Window: each major release and after substantial authoring-process changes
- Residual defect density: Definition: count of open release-blocking or high-impact defects remaining after final validation, with risk acceptance recorded separately; Unit/formula: number of open Critical and Major findings, reported by severity; Target: zero open Critical and Major defects, unless each exception has explicit authorized risk acceptance; Rationale: avoids masking material defects inside an average quality score; Source: audit findings, CI results, and the residual-risk register; Sample: all known Critical/Major findings and failed release-gate cases for the candidate; Segmentation: by severity, member skill, security/human/operational impact, and disposition; Method: verify finding closure against evidence and acceptance criteria; Owner: release approver; Window: final release gate and a 30-day post-release recurrence review
