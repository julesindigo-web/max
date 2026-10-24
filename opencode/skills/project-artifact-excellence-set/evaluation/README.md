# Evaluation Artifacts

This directory holds the authoritative trigger candidate test set, the task-evaluation ledger, and separate evaluation reports for the thirteen-member project-artifact-excellence-set v2.0.0.

- `trigger-evaluation-matrix.json` — authoritative schema 1.1 matrix; core skills carry 12+12 cases (including Indonesian, adversarial, and near-miss families) and each domain member carries 5+5 cases with stable IDs and expected labels. It is a test-set definition, not an observation log.
- `task-evaluation-ledger.json` — versioned representative task-evaluation record (schema `shared/contracts/task-evaluation-ledger.schema.json`); structure gate only.
- `runtime-protocol.md` — frozen-set runtime measurement procedure for triggers and tasks.
- `results-template.md` — template for dated runtime measurements.
- `results-2026-10-15.md` — historical author-semantic review note for the v2.0.0 matrix.
- Pilot intake (PA-LRN-06, open 2026-10-15): 5 first-time-author sessions using `../skills-create-excellence/assets/starter-brief.md` with `../skills-create-excellence/assets/timed-evaluation-log.md` per session; ledger stays `planned` until evidence + `measured_at` are recorded per `runtime-protocol.md`. Do not flip ledger status without real sessions.
- `../shared/examples/trigger-evaluation-cases.json` — lightweight schema 1.0 documentation sample; it is not used as the release-gate default.

A manual semantic review is not a measurement of runtime trigger activation. Runtime true-positive/false-positive rates require actual activation outcomes for every frozen test prompt in the target environment. Structural PASS similarly does not establish end-to-end task completion.
