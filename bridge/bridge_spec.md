# Senti Bridge Admission Spec — LLM Orchestration Substrate

## Purpose
Canonical governance wrapper that defines the conditions under which the
substrate + pipeline may be admitted as a bridge-handed-off package.

## Admission contract
A handoff is **REAL** only when ALL hold:
- `tools/conformance_check.py` exits 0 against the committed spec.
- Every artifact in `manifest.yaml` has a matching sha256 in `receipt.json`.
- The pipeline reaches a target via real secrets and returns a 2xx receipt.

A handoff is **PARTIAL** when the bundle is conformant locally but no target
deployment receipt exists (current state of this bundle).

A handoff is **BLOCKED** when conformance fails or required secrets/endpoints
are unresolved.

## Non-negotiables
- No PRETEND state is ever emitted. Absence of a receipt is reported as
  PARTIAL/BLOCKED, never as a synthetic success.
- Production is a `destructive_action` class promotion -> manual protected
  environment, consistent with the caller's own autonomy_boundary carve-out.
