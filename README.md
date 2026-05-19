# LLM Orchestration Substrate — Finalised Bundle (v1.0.0)

Reusable, client-agnostic core for LLM job orchestration plus its deployment
pipeline and Senti Bridge admission spec.

## Layout
- `substrate/substrate.spec.yaml` — frozen v1.0.0 spec, 6 invariants, 5 units.
- `substrate/schemas/*.json` — the 9 contracts (now real, previously only referenced).
- `tools/conformance_check.py` — mechanical invariant enforcement (CI gate).
- `pipeline/` — GitHub Actions workflow + fail-closed deploy scripts + config.
- `bridge/bridge_spec.md` — admission contract & state mapping.
- `manifest.yaml` / `receipt.json` — handoff tracking with real sha256 hashes.
- `ANALYSIS.md` — design critique, enhancements applied, and honest deploy status.
- `.github/workflows/deploy-substrate.yml` — active CI (mirror of pipeline/ copy).

## Run conformance locally
    pip install pyyaml
    python tools/conformance_check.py

## Deploy status
Local bundle is REAL and verifiable. Staging/production deployment is BLOCKED
until real secrets/endpoints are wired — see ANALYSIS.md.
