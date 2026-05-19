# HOUSE_RULES — TML-4PM/proof_pot

**Status:** canonical · binds every LLM/agent that reads or writes this repo.
Derived from `governance/KERNEL_ASSESSMENT.md` (GLOBAL_RULE_KERNEL_V6). Where a
chat thread, memory summary, or prior turn conflicts with these rules, **these
rules win**. `LLM_CANONICAL.md` remains the substrate pointer; this file is the
behaviour contract on top of it.

## The rules

**R1 — Receipt or it didn't happen.**
No "done" / "deployed" / "shipped" claim without a typed receipt: a commit SHA,
an evidence_hash, a 2xx response body, or a DB row id. Absence of a receipt is
reported as PARTIAL or BLOCKED. Synthetic success is forbidden (kernel:
`evidence`, no PRETEND).

**R2 — State the ledger state every time.**
Every substantive action ends with one of REAL / PARTIAL / BLOCKED and a
bounded reason. "REAL" requires the kernel's `REAL_requires` met for that
claim's scope. A spec is never REAL on the strength of being well-written.

**R3 — Downgrade on any trip condition.**
If any kernel `downgrade_conditions` is present — manual dependency, missing
telemetry, receipt mismatch, economic failure, ontology drift — the affected
claim drops to PARTIAL/BLOCKED immediately, in the same response, before any
forward action.

**R4 — Repo must equal receipt.**
Before asserting bundle integrity, read files back and hash against
`receipt.json`. A size or hash mismatch is `receipt mismatch` → R3. (This rule
exists because it already caught a real 2-file drift in this repo.)

**R5 — Frozen means versioned.**
`substrate/substrate.spec.yaml` is v1.0.0. Any change to contracts, invariants,
or units is a **new version + new receipt**, never an in-place edit of the
frozen spec. Editing frozen contracts in place = `ontology drift` → R3.

**R6 — Destructive actions do not self-execute.**
DELETE / DROP / wipe / mass-mutation / production promotion are
`destructive_action`. They require an explicit, *scoped* authorization naming
target + retention before execution. "Archive never delete" is the default;
a literal wipe that contradicts it must be called out, not silently performed.
Undefined scope = BLOCKED, bounded reason stated.

**R7 — Verify against ground truth, not cache.**
A rendered/cached view (e.g. a stale GitHub HTML page) is not evidence. Verify
via API/DB read-back. Conflicting sources → trust the one with a typed receipt.

**R8 — One honest unresolved beats five confident asserts.**
When blocked, surface the single precise question that unblocks it and stop.
Do not pad with adjacent work to manufacture progress (kernel: `economic
governance` — orphan/zombie work decays).

**R9 — Memory is superseded, not trusted.**
Prior per-thread context yields to this repo. Carrying contradictory thread
memory forward as fact = `ontology drift` → R3.

**R10 — No new long-lived infra without a kill switch + rollback.**
Anything that runs unattended ships with a documented stop and a rollback path
*before* it goes live (kernel: `deterministic recovery`, `autonomous
survivability`). Unproven survivability stays PARTIAL — it is never asserted.

## Quick self-check (run before every "done")

1. Typed receipt attached? → if no, not REAL (R1)
2. Ledger state + bounded reason stated? (R2)
3. Any downgrade condition present? → downgrade now (R3)
4. Claiming bundle integrity? → read back + hash vs receipt (R4)
5. Touching the frozen spec? → new version, not in-place (R5)
6. Destructive? → scoped authorization exists? else BLOCKED (R6)
7. Relying on a cached view? → re-verify against ground truth (R7)

## Current standing of this repo under these rules

- Conformance: **REAL** (`tools/conformance_check.py` exits 0).
- Repo == receipt: **REAL** (read-back verified; prior drift fixed).
- Deploy: **PARTIAL** (no staging/prod receipt — R1).
- Kernel runtime / 72h survivability: **PARTIAL** (kernel's own `gaps`).
- System-wide memory deletion: **BLOCKED** (R6 — scope undefined).
