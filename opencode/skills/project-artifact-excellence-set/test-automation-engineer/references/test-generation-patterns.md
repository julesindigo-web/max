# Test Generation Patterns

Place each test at the lowest layer that can prove the behavior.

## 1. Unit with Jest and Vitest
- Cover one module per file with branch and boundary cases.
- Mock only network, time, and filesystem seams.
- Name tests as behavior statements with inputs and expected outputs.
- Assert error paths with explicit messages and types.
- Keep each test under 30 lines and independent of order.

## 2. Integration
- Verify service wiring, database reads and writes, and queue flows.
- Use isolated test databases or in-memory doubles with migration parity.
- Reset state before each test and clean up after.
- Assert side effects plus response contracts together.

## 3. Contract
- Define provider schemas and consumer expectations in one versioned file.
- Fail the build on breaking field removal or type change.
- Test backward compatibility with at least 2 consumer versions where applicable.
- Publish change notes with every contract edit.

## 4. E2E with Playwright and Cypress
- Automate only critical journeys first, then expand by risk.
- Use role and label selectors; avoid fragile CSS paths.
- Isolate data per run with unique users or tenants.
- Capture screenshots, video, and traces on failure.
- Replace fixed sleeps with waits on observable state.

## 5. BDD Scenario Design
- Write Given, When, Then plus expected observable outcome.
- Keep scenarios independent and data-explicit.
- Cover one happy path plus at least 2 negative variants per journey.
- Link each scenario to the requirement or acceptance criterion it proves.
