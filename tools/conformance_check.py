#!/usr/bin/env python3
"""Conformance validator for the LLM orchestration substrate.

Checks that are mechanically enforceable from the repo alone:
  - spec parses and is version-pinned
  - every unit references input/output schemas that exist and are valid JSON Schema
  - every unit declares telemetry: true (INV-3)
  - every mutating unit's input schema carries idempotency_key (INV-6)
  - result_codes referenced by the spec are non-empty (INV-5)

Exit code 0 = REAL (conformant), non-zero = BLOCKED with bounded reasons.
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("BLOCKED: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1] / "substrate"
SPEC = ROOT / "substrate.spec.yaml"


def fail(errs):
    print("BLOCKED — conformance violations:")
    for e in errs:
        print(f"  - {e}")
    sys.exit(1)


def main():
    errs = []
    spec = yaml.safe_load(SPEC.read_text())["llm_orchestration_substrate"]

    if spec.get("version", "0").startswith("0"):
        errs.append("INV-4: spec version is not frozen (still 0.x)")

    if not spec.get("result_codes"):
        errs.append("INV-5: result_codes set is empty")

    for unit in spec["units"]:
        name = unit["name"]
        for slot in ("input", "output"):
            schema_path = ROOT / unit[slot]
            if not schema_path.exists():
                errs.append(f"{name}: missing {slot} schema {unit[slot]}")
                continue
            try:
                schema = json.loads(schema_path.read_text())
            except json.JSONDecodeError as exc:
                errs.append(f"{name}: {slot} schema not valid JSON ({exc})")
                continue
            if "$schema" not in schema:
                errs.append(f"{name}: {slot} schema missing $schema dialect")

        if not unit.get("telemetry"):
            errs.append(f"INV-3: unit {name} does not declare telemetry: true")

        if unit.get("mutating") and not unit.get("idempotent_by"):
            in_schema = json.loads((ROOT / unit["input"]).read_text())
            req = in_schema.get("required", [])
            if "idempotency_key" not in req:
                errs.append(
                    f"INV-6: mutating unit {name} input lacks required "
                    f"idempotency_key and declares no idempotent_by"
                )

    if errs:
        fail(errs)
    print(f"REAL — substrate {spec['version']}: "
          f"{len(spec['units'])} units conformant, "
          f"{len(spec['result_codes'])} result codes, all schemas resolve")
    sys.exit(0)


if __name__ == "__main__":
    main()
