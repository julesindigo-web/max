# Activation Log Guide — grading probes

1. Log every routing decision with `assets/routing-log-template.md` fields.
2. Grade coverage with `python3 scripts/run-trigger-evaluation.py --matrix evaluation/trigger-evaluation-matrix.json`.
3. Grade observations with `--observations <runtime-log.json> --out evaluation/results-YYYY-MM-DD.md` per `evaluation/runtime-protocol.md`, with independent label adjudication before inspecting observations.
4. File misses as matrix cases with unique kebab-case IDs, no cross-label overlap after casefold normalization.
5. Never claim TPR/FPR from author-semantic review; only target-runtime logs count.
