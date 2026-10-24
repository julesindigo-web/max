# Client State Patterns

Manage client state so interfaces stay fast and resilient.

## Separate State Kinds

- Treat server cache, form state, UI state, and routing state as distinct stores.
- Keep server state in a cache with keys, staleness, and retry rules.
- Keep form drafts local until submit succeeds.
- Keep ephemeral UI flags near the component that owns them.
- Document ownership and lifetime for each store in code comments.

## Prevent Load Lag

- Fetch only fields required for the current view.
- Paginate lists at 20 to 50 items and prefetch the next page on idle.
- Cache repeated queries for 60 to 300 seconds based on volatility.
- Render cached data first, then refresh in the background with status hints.
- Cancel obsolete requests when filters or routes change.

## Handle Race and Conflict

- Tag mutations with request IDs and ignore stale responses.
- Apply optimistic updates only where rollback stays safe and simple.
- Reconcile conflicts with last-writer-wins plus user confirmation for edits.
- Queue offline mutations and replay in order on reconnect.
- Preserve user input across reloads for forms longer than 3 fields.

## Bound Failures

- Place error boundaries at route level and around third-party widgets.
- Show retry, go-back, and contact-support actions on every failure panel.
- Log component, route, state snapshot ID, and error class on capture.
- Test empty, loading, error, and offline states for every data view.
- Confirm recovery without full reload in at least 99% of sampled failures.

## Test State Transitions

- Cover load, refresh, create, update, delete, and conflict paths.
- Simulate slow networks at 4G and offline gaps in tests.
- Assert focus returns to a sensible target after dialogs and errors.
- Verify no duplicate mutations under double submit.
- Export state errors and retry counts to shared telemetry.
