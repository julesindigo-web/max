---
name: frontend-experience
description: Build or repair a browser UI flow. Use when changing a page, component, interaction, responsive layout, or accessibility behavior.
---

# Frontend Experience

Use this skill for a user-facing browser change. Do not use it for a copy-only edit with no behavioral or visual effect.

1. Establish the user task, route, data source, and ownership boundary. Match the installed framework, component system, tokens, and existing visual language rather than introducing a parallel pattern.
2. Choose semantic HTML and native controls first. Keep labels, errors, focus, keyboard operation, target size, contrast, and reduced-motion behavior correct. Use ARIA only where native semantics cannot express the behavior.
3. Model asynchronous states deliberately: loading without layout shift, empty state that explains the next action, clear recoverable error, success, and permission or offline states when relevant.
4. Keep state in the narrowest durable place: URL for shareable state, local state for local interaction, and server-state tooling for remote cache and invalidation. Prevent duplicate submits and preserve user input on failure.
5. Test at the changed interaction boundary. When browser tooling exists and the change is visual or interactive, inspect the rendered path at a narrow and a wide viewport, then make a keyboard pass. Report visual checks as unverified if rendering is unavailable.

Do not add animation, client state, a design library, or an image asset unless the requested behavior needs it. Escalate to `$sensitive-change-safety` when the flow handles identity, sensitive data, payment, upload, or consent.
