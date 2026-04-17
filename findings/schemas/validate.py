#!/usr/bin/env python3
"""Validate every AIEOS canonical findings schema against its example fixtures.

For each schema under findings/schemas/*.schema.json:
  - The schema itself must parse as JSON Schema Draft 2020-12.
  - findings/schemas/examples/<name>.valid.json must validate (pass).
  - findings/schemas/examples/<name>.invalid.json must fail validation (fail).

Exit code:
  0 — every assertion passed.
  1 — at least one assertion failed (details printed to stderr).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

SCHEMAS_DIR = Path(__file__).parent
EXAMPLES_DIR = SCHEMAS_DIR / "examples"


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return json.load(f)


def check_schema(schema_path: Path) -> tuple[bool, str]:
    """Returns (pass, message). pass=True means the schema parsed as valid
    JSON Schema Draft 2020-12."""
    try:
        schema = load_json(schema_path)
    except json.JSONDecodeError as exc:
        return False, f"JSON parse error: {exc}"
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return False, f"schema meta-validation error: {exc.message}"
    return True, "schema is valid Draft 2020-12"


def check_example(schema_path: Path, example_path: Path, *, expect_valid: bool) -> tuple[bool, str]:
    schema = load_json(schema_path)
    try:
        document = load_json(example_path)
    except json.JSONDecodeError as exc:
        return False, f"example JSON parse error: {exc}"
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda e: e.path)
    if expect_valid:
        if errors:
            messages = "; ".join(e.message for e in errors[:3])
            return False, f"expected valid but found {len(errors)} error(s): {messages}"
        return True, "valid example validates"
    else:
        if not errors:
            return False, "expected invalid but validation passed"
        return True, f"invalid example correctly rejected ({len(errors)} error(s))"


def main() -> int:
    schemas = sorted(SCHEMAS_DIR.glob("*.schema.json"))
    if not schemas:
        print("no schema files found under findings/schemas/", file=sys.stderr)
        return 1

    overall_ok = True
    for schema_path in schemas:
        stem = schema_path.name.replace(".schema.json", "")
        print(f"\n=== {stem} ===")

        ok, msg = check_schema(schema_path)
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] schema parse — {msg}")
        overall_ok &= ok

        valid_path = EXAMPLES_DIR / f"{stem}.valid.json"
        if not valid_path.is_file():
            print(f"  [FAIL] valid example missing at {valid_path}")
            overall_ok = False
        else:
            ok, msg = check_example(schema_path, valid_path, expect_valid=True)
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] valid example — {msg}")
            overall_ok &= ok

        invalid_path = EXAMPLES_DIR / f"{stem}.invalid.json"
        if not invalid_path.is_file():
            print(f"  [FAIL] invalid example missing at {invalid_path}")
            overall_ok = False
        else:
            ok, msg = check_example(schema_path, invalid_path, expect_valid=False)
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] invalid example — {msg}")
            overall_ok &= ok

    print()
    if overall_ok:
        print("ALL CHECKS PASSED")
        return 0
    print("ONE OR MORE CHECKS FAILED", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
