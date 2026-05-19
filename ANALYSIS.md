# ANALYSIS — Finalise / Analyse / Enhance / Deploy

## 1. Finalised
Prior thread left the substrate as prose + a YAML skeleton whose schemas were
only referenced and never existed. This bundle closes it: spec frozen at
v1.0.0, all 9 schemas exist as valid JSON Schema 2020-12, 6 invariants made
mechanically checkable.

## 2. Analysed — real weaknesses found and fixed
- Schemas referenced but absent -> written, validated.
- execute_job claimed idempotency, no key in any contract -> idempotency_key
  added; INV-6 enforces it (validator caught this on first run).
- Failure surface unenumerated -> closed result_codes set.
- No telemetry envelope schema -> trace_event.v1 defined; INV-3 enforces it.
- Cost model referenced, never specified -> cost_model.v1 defined.
- Pipeline auto-deployed to prod on push to main -> reworked: main = staging
  only; prod is manual workflow_dispatch into a protected environment.
- Deploy scripts could silent-pass without secrets -> all fail closed.
- No rollback pinning -> prod deploy requires a pinned artifact_version.

## 3. Enhanced
- conformance_check.py is a runnable CI gate, not documentation.
- receipt.json carries real SHA-256 hashes computed from the actual files,
  not asserted hashes (the earlier thread's receipt asserted unseen hashes).

## 4. Deploy status (operator's own taxonomy)
- Local bundle: REAL — files exist, conformance exits 0, hashes recorded.
- Staging: BLOCKED — no verified secrets/endpoints reachable from this context.
- Production: BLOCKED — depends on staging evidence; destructive_action class.

No production deployment was fired. REAL requires executed + replayable +
receipted + telemetry_verified; none hold for a first-run blind deploy of
unvalidated middleware. Reporting it deployed would be a PRETEND state.

## 5. Next reversible step
Wire only staging secrets, let one real staging run produce the first genuine
receipt, then production becomes a one-action manual gate with evidence behind
it.
