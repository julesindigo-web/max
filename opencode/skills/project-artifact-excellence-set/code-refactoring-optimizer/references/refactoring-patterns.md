# Refactoring Patterns

Apply these patterns in small tested steps. Measure before and after each pattern.

## 1. Extract Service
Symptoms:
- Business rules embedded in controllers, handlers, or interface components.
- Same rule copied across two or more call sites.
- Function exceeds complexity budget or mixes I/O with decisions.

Steps:
- Isolate the rule block and list its inputs and outputs.
- Create a focused service module with a single responsibility.
- Move the rule without changing behavior.
- Inject the service at call sites.
- Add unit tests for edge cases and error paths.
- Re-measure complexity and duplication rate.

## 2. Split Component
Symptoms:
- Interface component exceeds 200 lines or manages multiple visual jobs.
- Props list grows past 7 inputs or state updates scatter across handlers.
- Re-renders trigger without visible change.

Steps:
- Identify one visual job per subcomponent.
- Extract presentational units with narrow props.
- Lift shared state to the smallest common owner.
- Memoize only proven hot renders.
- Verify visual output and interaction tests still pass.

## 3. Optimize Query
Symptoms:
- N-plus-one access, missing index, or full-table scan on a hot path.
- Endpoint latency dominated by database wait time.
- Repeated identical reads within one request.

Steps:
- Capture the query plan and latency across at least 3 runs.
- Add the missing index or rewrite the join and filter order.
- Batch or cache repeated reads with explicit invalidation.
- Re-run the plan and latency check.
- Record the delta in the before-and-after table.

## 4. Remove Duplication
Symptoms:
- Near-identical blocks in two or more modules.
- Parallel fixes required for a single logical change.

Steps:
- Normalize differences into parameters.
- Create one canonical function or module.
- Replace clones with calls to the canonical unit.
- Add one test covering each prior variant.
- Delete the dead copies and re-run the full suite.
