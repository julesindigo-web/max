# Runtime Evaluation Protocol (v2.0.0)

Runtime trigger precision/recall and task completion are **measured**, never inferred from static PASS.

## Trigger runtime run
1. Freeze `evaluation/trigger-evaluation-matrix.json` (record SHA-256 and `as_of` date).
2. Install the candidate skill set in the target runtime; record runtime identity, version, config, and timestamp.
3. Execute every frozen prompt verbatim via `python3 scripts/run-trigger-evaluation.py --matrix evaluation/trigger-evaluation-matrix.json --observations <runtime-log.json> --out evaluation/results-YYYY-MM-DD.md`.
4. Adjudicate expected labels independently **before** inspecting observations.
5. Report per skill: TP, FN, FP, TN, recall/TPR, specificity, precision, FPR, sample size (n positive / n negative), per-family breakdown (ID, adversarial, near-miss), and confidence intervals where appropriate.
6. Store the dated results file separately; never overwrite `results-2026-10-15.md` (historical author-semantic review).

## Task-completion run
1. Freeze `evaluation/task-evaluation-ledger.json`.
2. Execute each task with the starter brief in `assets/starter-brief.md`; record elapsed minutes, assistance given, validation output, and evidence pointers.
3. Mark each task passed/failed/waived with a binary acceptance check; waivers require rationale + owner + review date.
4. Target: >=95% applicable acceptance checks pass; zero open Critical/Major without authorized risk acceptance.

## Independence
The release evaluator should be independent of the skill author where feasible. Author-side semantic review is labeled `AUTHOR-SEMANTIC-REVIEW` and does not satisfy runtime gates.
