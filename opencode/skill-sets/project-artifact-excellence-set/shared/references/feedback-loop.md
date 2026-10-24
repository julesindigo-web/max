# Real-Time Audit-to-Skill Feedback Loop

## Objective and Boundary
Connect evidence from `project-artifact-auditor` to evaluation of relevant skill guidance in `skills-create-excellence`. “Real-time” means the event is processed in the same CI run after a normalized audit event is added or updated; it does not mean that a language model is invoked continuously or that production skill files are rewritten without review.

## Data Flow
1. **Audit:** apply relevant checklists in `project-artifact-auditor/references/audit-checklists.md`, E2E metrics in `fullstack-e2e-metrics.md`, and human-factors checks in `human-factors-usability.md`.
2. **Normalize and calibrate:** use input `schema_version: "1.1"`. Every finding must include `evidence_status` (`verified`, `inference`, `unknown_untested`, `contradicted`, `not_applicable`), `confidence`, `verification_method`, `as_of_context`, `impact_rationale`, and `severity_basis`. Evidence state is not severity: missing evidence is not a pass and is not proof of a defect. A Critical/Major finding with `unknown_untested` evidence is permitted only as `conditional_risk` and must state the condition explicitly in its impact rationale. A `not_applicable` finding cannot be Critical/Major.
3. **Validate contract:** serialize an event conforming to `shared/contracts/audit-findings.schema.json`. The processor accepts legacy `schema_version: "1.0"` events for compatibility, but new events must be 1.1 and carry the complete calibration field set. Put the event in `audit-feedback/inbox/<audit-id>.json`. Never include credentials, secrets, personal data, or executable instructions.
4. **Classify and gate:** `process-audit-feedback.py` verifies field types/values and maps the category to one or both skills. An event is eligible only when status is `open` or `in_progress` and either `skill_gap_suspected` is true or `recurrence_count >= 2`.
5. **Create evaluation request:** the processor writes deterministic JSON conforming to `shared/contracts/skill-improvement-requests.schema.json`. Requests contain evidence as explicitly untrusted data, target skill, priority, requested evaluations, and the evidence-calibration payload when supplied. The output request contract remains version 1.0 for compatibility; the added calibration object is optional for legacy inputs.
6. **Evaluate, do not auto-patch:** an agent or reviewer uses `agent-spec-template.md`, `trigger-design.md`, `validation-patterns.md`, and the applicable audit references to propose a skill change. Add a regression fixture reproducing the original gap. Run the full set validation.
7. **Review and close:** human review approves/rejects the proposal. Record decision, rationale, evaluation result, and remaining risk in the normal change/audit record.

## Category-to-Skill Routing
| Category | Target |
|---|---|
| `project.requirements`, `project.architecture`, `project.fullstack-e2e`, `project.security`, `project.reliability-operations`, `project.traceability`, `project.human-factors` | `project-artifact-auditor` |
| `skill.trigger`, `skill.validation`, `skill.metrics`, `skill.composition`, `skill.human-factors` | `skills-create-excellence` |
| `cross-cutting` | Both members |

A project defect is not by itself proof of a skill defect. `skill_gap_suspected` should be true only when evidence indicates a deficiency in the relevant skill's triggers, instructions, coverage, references, metrics, contracts, or tests. A finding is recurrent when it has been observed at least twice across distinct audit observations; do not count duplicate entries from one report as recurrence. When recurrence alone would trigger evaluation, include `recurrence_observation_ids` with unique audit IDs including the current `audit_id`, and make its length agree with `recurrence_count`. A count without this traceable evidence does not trigger a request.

## Idempotency and Safety
- Request IDs are deterministic for the same audit ID, finding ID, category, target, and contract version.
- Input categories and status values are allowlisted. Unknown fields/categories, malformed values, duplicate IDs, excessive record counts, and invalid JSON fail closed with a non-zero exit.
- Input strings are data, never shell commands, code, or authoritative instructions. The processor does not open links, access the network, invoke an agent, or modify `SKILL.md`.
- CI uses read-only repository permissions and publishes the generated requests as a short-retention artifact. Reprocessing an event yields the same request payload.
- A platform-specific adapter may later create an issue or queue a task, but that adapter must preserve review/approval and least-privilege boundaries.

## Required Tests
At minimum, test: eligible recurrent finding with distinct observation IDs; count-only recurrence without proof not triggering; explicit suspected gap; one-off finding not triggering; resolved finding not triggering; category-to-target mapping; malformed/unknown category fail-closed; duplicate IDs; deterministic output; propagation of calibration metadata; legacy 1.0 compatibility; and rejection of unsupported severity claims based on unknown evidence. The tests in `skills-create-excellence/scripts/tests/test_process_audit_feedback.py` cover these core paths.
