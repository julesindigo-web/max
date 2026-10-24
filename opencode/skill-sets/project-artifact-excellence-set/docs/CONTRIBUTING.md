# Contributing — v2.0.0

1. Edit under the relevant member, shared contract, or evaluation file; never edit a released ZIP.
2. Add/update a minimal regression fixture for every validator or behavior change.
3. Run `bash validation/validate-set.sh` from the set root; all 8 gates must pass.
4. For trigger/description changes: freeze a new dated results record per `evaluation/runtime-protocol.md`.
5. Record residual risks with owner + review date; Critical/Major needs explicit disposition.
6. Bump versions + migration notes for breaking contract changes.
