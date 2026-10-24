# Motion and Micro-Interactions

Design motion that confirms action and builds calm confidence.

## Give Every Motion a Job

- Animate only to show cause and effect, state change, or spatial relation.
- Pair each trigger with visible feedback within 100ms.
- End feedback motion between 120ms and 300ms.
- Keep page transitions under 400ms and skippable on repeated use.
- Remove motion that neither informs nor reassures.

## Use Organic Easing

- Prefer ease-out for entrances and ease-in-out for moves between states.
- Avoid linear motion except for progress tied to real load.
- Keep spring effects subtle with low bounce and fast settle.
- Match duration to distance: short moves finish faster than long ones.
- Document easing curves as tokens for reuse across the product.

## Craft Micro-Interactions

- Confirm presses with scale or fill change plus haptic where available.
- Show loading with skeletons that match final layout to avoid shift.
- Celebrate success quietly with a check or fade rather than a takeover.
- Explain errors inline near the field with recovery action attached.
- Preserve focus and scroll position through animated updates.

## Respect Comfort and Choice

- Honor reduced-motion settings by showing instant final states.
- Avoid parallax, autoplay video, and flashing above 3Hz.
- Provide a motion-reduction toggle where ambient animation persists.
- Test with at least 3 users sensitive to motion where feasible.
- Log motion-related complaints as defects with severity and fix date.

## Verify Feel and Performance

- Keep animated properties to transform and opacity for 60fps motion.
- Test on mid-tier mobile hardware, not only on desktops.
- Confirm no layout shift during entrance and exit sequences.
- Measure task time with and without new motion on core flows.
- Record motion tokens, durations, and review notes for audit traceability.
