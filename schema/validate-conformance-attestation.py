#!/usr/bin/env python3
"""Validate the conformance-attestation schema and its examples.

Checks:
  1. schema/conformance-attestation.schema.json parses as JSON Schema Draft 2020-12.
  2. examples/conformance-attestation.example.json validates against the schema.
  3. examples/conformance-attestation.invalid.json fails validation.

Exit code 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "conformance-attestation.schema.json"
VALID_EXAMPLE = REPO_ROOT / "examples" / "conformance-attestation.example.json"
INVALID_EXAMPLE = REPO_ROOT / "examples" / "conformance-attestation.invalid.json"


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    print("=== schema ===")
    try:
        Draft202012Validator.check_schema(schema)
        print("  [PASS] conformance-attestation.schema.json is valid Draft 2020-12")
    except SchemaError as exc:
        print(f"  [FAIL] schema invalid: {exc.message}")
        return 1

    validator = Draft202012Validator(schema)

    print("\n=== valid example ===")
    valid_doc = load_json(VALID_EXAMPLE)
    errors = list(validator.iter_errors(valid_doc))
    if errors:
        print(f"  [FAIL] valid example did not validate: {errors[0].message}")
        return 1
    print("  [PASS] conformance-attestation.example.json validates")

    print("\n=== invalid example ===")
    invalid_doc = load_json(INVALID_EXAMPLE)
    errors = list(validator.iter_errors(invalid_doc))
    if not errors:
        print("  [FAIL] invalid example was accepted — schema too permissive")
        return 1
    print(
        f"  [PASS] conformance-attestation.invalid.json correctly rejected "
        f"({len(errors)} error(s))"
    )
    for err in errors[:8]:
        path = "/".join(str(p) for p in err.path) or "<root>"
        print(f"         - {path}: {err.message}")

    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
