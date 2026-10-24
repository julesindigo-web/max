# Classifier Guide — signals, weights, negative guards

`scripts/route-task.py` implementation notes. Score equals distinct matched phrases per skill. Every phrase is multi-word or domain-specific to avoid single-keyword hits. Matching is word-boundary (alphanumeric edges), so short signals never fire inside longer words — e.g. `aria` does not match Indonesian `pencarian` (near-miss probe 2026-10-16).

## Weights
All signals weigh 1. Corroboration count is the score. No learned weights, no network, fully offline.

## Negative guards
A guard hit subtracts 2 (floor 0) from the penalized skill. Guards: cooking/recipe content penalizes all; meme/slide screenshots penalize `test-automation-engineer`; physics theory penalizes all. Add new guards here and in the script together, with a regression probe per guard.

## Adding signals
1. Propose the phrase with two example utterances (EN + ID where relevant).
2. Check casefold overlap against the frozen matrix prompts for the target skill.
3. Update script + this guide + `routing-policy.md` in one change.
4. Add a probe case with a unique kebab-case ID; re-freeze matrix SHA.

## Known limits
Substring matching cannot resolve sarcasm or heavily code-switched utterances. Low-confidence ties return `clarify` with two candidates instead of guessing.
