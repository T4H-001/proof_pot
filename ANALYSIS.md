# ANALYSIS — Finalise / Analyse / Enhance / Deploy

## 1. Finalised
The prior thread left the substrate as prose plus a YAML *skeleton* whose
schemas were only *referenced* (`schemas/job_spec_v1.json` etc.) and never
existed. That is the gap behind your own "not REAL" instinct earlier in the
thread. This bundle closes it:

- Spec frozen at **v1.0.0** (was `0.1.0` — an unfrozen contract cannot be REAL).
- All **9 schemas now exist** as valid JSON Schema 2020-12 documents.
- 6 invariants made **mechanically checkable**, not aspirational.

## 2. Analysed — real weaknesses found and addressed
| Finding | Severity | Resolution |
|---|---|---|
| Schemas referenced but absent | blocking | Written, validated |
| `execute_job` claimed idempotency; no key in any contract | high | `idempotency_key` added to `job_spec`/`tool_call`; INV-6 enforces it on every mutating unit |
| Failure surface was "machine-readable error codes" with no enumeration | high | Closed `result_codes` set defined in spec, INV-5 checks non-empty |
| No telemetry envelope schema despite "telemetry built-in" claim | high | `trace_event.v1.json` defined; INV-3 enforces one event per unit |
| Cost model referenced, never specified | medium | `cost_model.v1.json` defined |
| **Pipeline auto-deployed on push to `main`** including prod path | high | Reworked: main → validate + staging only; prod is `workflow_dispatch` into a protected GitHub Environment with required reviewers |
| Deploy scripts could silent-pass without secrets | high | All scripts now **fail closed** (exit 1, bounded reason) instead of pretending |
| No rollback pinning | medium | Production deploy requires an explicit pinned `artifact_version` |

## 3. Enhanced
- `conformance_check.py` is a runnable CI gate, not documentation. It emits
  `REAL` / `BLOCKED` with bounded reasons — same taxonomy as your kernel.
- `receipt.json` carries **real SHA-256 hashes computed from the actual
  files**, not asserted hashes. The earlier thread's receipt claimed hashes
  it never showed; that is exactly a PRETEND state your kernel forbids.

## 4. Deploy status — stated honestly in your own terms

| Layer | State | Bounded reason |
|---|---|---|
| Local bundle | **REAL** | files exist, conformance exits 0, hashes computed and recorded |
| Staging deploy | **BLOCKED** | external constraint: no verified artifact-repo / webhook / healthcheck secrets are reachable from this context; per evidence_layer, asserting a deploy receipt I cannot produce would be PRETEND |
| Production promotion | **BLOCKED** | explicit dependency on staging evidence; `destructive_action` class — this is precisely the carve-out your own `autonomy_boundary` reserves for a gate |

I did not fire a production deployment. Not because of a generic refusal —
because the bundle has never executed against real infrastructure, and your
own constitution defines REAL as *executed + replayable + receipted +
telemetry_verified + economically_validated*. None of those can be true for a
first-run deploy of unvalidated orchestration middleware triggered blind from
here. Reporting it as deployed would be the one thing the kernel explicitly
prohibits.

## 5. Single reversible next step
Bind this to a **satellite proving-ground repo** (not the canonical Pen repo),
push with the prod job inert (it only arms on `workflow_dispatch` + protected
environment), wire only the *staging* secrets, and let one real staging run
produce the first genuine receipt. After that receipt exists, production
promotion becomes a one-action manual gate with real evidence behind it.

Tell me the proving-ground repo and I can stage the GitHub write via the T4H
bridge — push only, prod path still gated.
