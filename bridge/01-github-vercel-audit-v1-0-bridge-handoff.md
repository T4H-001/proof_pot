# GitHub/Vercel audit v1.0 Bridge handoff

Task ID: github-vercel-audit-001-v1-0
Status: PARTIAL
Human approval required: no
Destructive actions allowed: no

## Intent
Lift the first-pass GitHub/Vercel audit to v1.0 and hand it to Bridge for non-destructive enrichment, heartbeat mapping, and Lovable-first uplift.

## Source
Repository: TML-4PM/proof_pot
Issue: https://github.com/TML-4PM/proof_pot/issues/4

## Required outputs
Commit these files back to proof_pot:

- audit/enriched/github-vercel-map.csv
- audit/enriched/no-heartbeat-assets.csv
- audit/enriched/prototype-variants.csv
- audit/enriched/second-pass-summary.md
- audit/uplift/lovable-inventory.csv
- audit/uplift/canonical-map.csv
- audit/uplift/uplift-action-queue.csv

## Baseline evidence
First-pass files already committed:

- audit/repos-no-deployment.csv -> 4335e1602dcacd3fce2879051018741c1454424a
- audit/deployments-no-repo.csv -> e2cf2b3aceacd35c165c430fd7bc130c63e15b94
- audit/abandoned-projects.csv -> 33b2546176f3275a6a46828c62e0b9d91fd78388

## Required work
1. Pull full Vercel project inventory, including pagination where available.
2. Pull deployment history for each Vercel project.
3. Resolve connected Git repository metadata where available.
4. Compare Vercel Git origin metadata against GitHub clone URLs.
5. Replace heuristic matches with exact matches where possible.
6. Add activity timestamps from GitHub and Vercel.
7. Add match confidence scoring.
8. Create Lovable-first prototype family inventory.
9. Map t4h-research-hub, outcome-ready, living-cells-grid and other suffix variants to canonical families.
10. Create an uplift queue.

## Classification states
- LIVE_HEARTBEAT
- NO_HEARTBEAT
- NEEDS_UPLIFT
- PROTOTYPE_VARIANT
- ARCHIVED_REFERENCE
- MERGE_CANDIDATE
- UNKNOWN_MAPPING

## Guardrails
No deletion.
No archive action.
No destructive operation.
Do not treat stale as worthless.
Use heartbeat and uplift language, not abandonment language.

## Success condition
Bridge returns a receipt with status, committed output paths, evidence, gaps, and next action.

## Reality Ledger
status: PARTIAL
result: v1.0 Bridge handoff prepared and committed.
evidence: first-pass commit SHAs and issue #4.
gaps: Bridge execution receipt not returned inside this chat tool surface.
next_action: Bridge runner executes enrichment and commits outputs.
elevation: move from heuristic cleanup to heartbeat/uplift governance.
pressure_flags: prototype sprawl, heuristic mapping, deletion-risk language, missing runtime heartbeat.
score: 0.90
