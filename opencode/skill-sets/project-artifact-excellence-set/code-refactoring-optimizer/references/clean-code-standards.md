# Clean-Code Standards

Follow these rules on every refactor. Calibrate enforcement to end-to-end outcomes.

## Naming
- Choose intention-revealing names for functions, modules, and services.
- Avoid abbreviations that force readers to guess.
- Name boolean checks as questions and side-effect actions as commands.
- Rename during extraction when the old name describes location instead of intent.

## Function Size
- Hold cyclomatic complexity at 10 or less per function.
- Keep functions to one responsibility and under 40 lines excluding tests.
- Limit parameters to 3 or fewer; group related inputs into a single object.
- Restrict nesting to 2 levels; extract deeper branches into helpers.

## Error Handling
- Handle errors at the layer that can decide the outcome.
- Return explicit result types or throw named errors with context.
- Never swallow failures silently; log with action, entity, and cause.
- Validate inputs at boundaries and fail fast with clear messages.

## Module Boundaries
- Separate interface rendering, business rules, and data access.
- Enforce one-way dependencies from interface toward domain and data.
- Export narrow interfaces; keep helpers private by default.
- Remove dead code in the same pass that extracts new units.

## Calibration to E2E Metrics
- Map function budgets to journey latency and error-rate signals in `../../project-artifact-auditor/references/fullstack-e2e-metrics.md` where available.
- Block merges that raise complexity above budget on changed code.
- Track duplication rate, mean complexity, and hot-path latency as release gates.
- Review readability with a maintainer walkthrough before closing the task.
