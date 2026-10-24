# Web Vitals Playbook

Apply this playbook to meet lab and field Web Vitals targets.

## Meet Thresholds

- Hold LCP at or under 2500ms for the 75th percentile of loads.
- Hold INP at or under 200ms for the 75th percentile of interactions.
- Hold CLS under 0.1 for the 75th percentile of page views.
- Measure on a mid-tier mobile device with throttled 4G for lab baselines.
- Block release when any metric regresses by more than 10% versus baseline.

## Cut Load Cost

- Keep total JavaScript under 200KB compressed per route where feasible.
- Code-split by route and defer below-fold components until needed.
- Preload the LCP image and one critical font; defer the rest.
- Compress images to modern formats and cap hero images under 200KB.
- Limit third-party scripts to 3 per page and load them after interaction.

## Stabilize Layout

- Reserve width and height for every image, video, ad, and embed slot.
- Use system font fallbacks with matching metrics to limit font swap shift.
- Avoid inserting banners or prompts above existing content after load.
- Animate only transform and opacity to prevent layout work.
- Verify CLS under 0.1 across desktop and mobile viewports.

## Speed Interaction

- Break long tasks into chunks under 50ms and yield to the main thread.
- Debounce search input at 150ms and cancel stale requests.
- Show optimistic feedback within 200ms for saves and votes.
- Move heavy formatting and sorting off the critical interaction path.
- Profile INP with at least 20 sampled interactions per release.

## Verify Across Browsers

- Test current Chrome, Safari, Firefox, and Edge on every release.
- Test 360px and 1440px widths plus one tablet width.
- Record rendering, input, and navigation defects with browser and version.
- Confirm zero blocking defects on declared browsers before rollout.
- Export Web Vitals and client errors to shared telemetry by route.
