# Orchestration Playbook Template

1. Route: run `scripts/route-task.py --text "<utterance>" --json`, record top 3.
2. Announce the route in one sentence with evidence phrases.
3. Sequence bottom-up: audit → domain → security + tests → deployment.
4. Execute with minimal context: selected skills only.
5. Log activation per `assets/routing-log-template.md`.
6. Probe near-misses; file misses as regression cases.
