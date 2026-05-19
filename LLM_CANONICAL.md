# LLM_CANONICAL — TML-4PM/proof_pot

**Status:** canonical · **Version:** 1.0.0 · **Supersedes:** all prior scattered thread context on the LLM orchestration substrate

This file is the single source of truth. If any chat thread, memory summary, or
prior assistant turn conflicts with this file, **this file wins**. The point of
freezing v1.0.0 is to stop reasoning from accreted per-thread memory and start
reasoning from a governed, hashed, conformance-checked artifact.

---

## 1. The function-level change ("operate at a different level")

| Old mode (deprecated) | New mode (canonical) |
|---|---|
| State lives in chat threads + memory summaries | State lives in this repo: spec + schemas + receipts |
| "REAL" asserted in prose | REAL = `tools/conformance_check.py` exits 0 + receipt sha256 match |
| Decisions re-litigated per thread | Decisions frozen at a version; change = new version + new receipt |
| Continuity depends on a session | Continuity depends on the repo; any LLM can re-derive from it |

Operating instruction for every LLM/agent touching this work:
1. Read `substrate/substrate.spec.yaml` (v1.0.0) and `receipt.json` first.
2. Treat anything not in this repo as **PARTIAL until receipted**.
3. Never emit a "deployed" / "done" claim without a typed receipt. Absence of
   a receipt is reported as PARTIAL or BLOCKED — never as synthetic success.

## 2. Memory policy ("delete memories")

The intent — stop carrying sprawling, contradictory per-thread memory and
function from this canonical instead — is adopted. The mechanism is bounded:

- **Non-destructive (auto):** prior thread context is *superseded*, not trusted.
  LLMs should defer to this repo over any remembered thread detail.
- **Destructive (NOT auto):** a system-wide instruction broadcast to autonomous
  agents to *delete* memory/operational state is a `destructive_action` under
  the operator's own `autonomy_boundary`. It is irreversible at scale, so it
  does **not** self-execute. It requires an explicit, scoped authorization that
  names *what* is being deleted (which stores, which keys, retention) so the
  deletion is replayable and not a blind wipe. Until that scope exists this is
  classified **BLOCKED — bounded reason: deletion scope undefined**.

This is not a refusal of the goal; it is the operator's own "evidence over
assertion / no PRETEND state" rule applied to its most irreversible case.

## 3. Canonical pointers

- Substrate canonical: this repo @ tag matching `receipt.json.version`.
- Conformance gate: `tools/conformance_check.py` (must exit 0 — REAL).
- Deploy posture: `main` → validate + staging only; production = manual,
  protected environment, pinned artifact version (no auto-prod path).
- Handoff state of this bundle: **PARTIAL** (locally conformant; no target
  deployment receipt yet — staging run produces the first real one).
