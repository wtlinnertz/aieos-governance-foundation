#!/usr/bin/env python3
"""Validate every AIEOS capability contract against the frozen meta-schema.

Checks:
  1. schema/capability-contract.schema.json parses as JSON Schema Draft 2020-12.
  2. contracts/examples/malformed.yaml fails meta-schema validation (negative test).
  3. Every contracts/*.contract.yaml file validates against the meta-schema.
  4. Every contract's required_inputs field is itself a valid Draft 2020-12 schema.
  5. Every contract references a findings/schemas/*.schema.json file that exists,
     or output_schema is null.
  6. Every contract's action field matches its filename stem.
  7. Every action in taxonomy/actions-v1.md has exactly one contract file.

Exit code:
  0 — every assertion passed.
  1 — at least one assertion failed (details printed).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

REPO_ROOT = Path(__file__).resolve().parent.parent
META_SCHEMA_PATH = REPO_ROOT / "schema" / "capability-contract.schema.json"
CONTRACTS_DIR = REPO_ROOT / "contracts"
MALFORMED_PATH = CONTRACTS_DIR / "examples" / "malformed.yaml"
TAXONOMY_PATH = REPO_ROOT / "taxonomy" / "actions-v1.md"
FINDINGS_SCHEMAS_DIR = REPO_ROOT / "findings" / "schemas"


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def extract_taxonomy_actions(taxonomy_path: Path) -> set[str]:
    """Parse `### <action>` headings out of taxonomy/actions-v1.md."""
    pattern = re.compile(r"^### ([a-z][a-z0-9]*\.[a-z][a-z0-9-]*)\s*$", re.MULTILINE)
    return set(pattern.findall(taxonomy_path.read_text()))


def main() -> int:
    overall_ok = True

    # --- 1. Meta-schema parses as Draft 2020-12 ---
    print("=== meta-schema ===")
    meta_schema = load_json(META_SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(meta_schema)
        print("  [PASS] capability-contract.schema.json is valid Draft 2020-12")
    except SchemaError as exc:
        print(f"  [FAIL] meta-schema invalid: {exc.message}")
        return 1
    meta_validator = Draft202012Validator(meta_schema)

    # --- 2. Malformed example fails (negative test) ---
    print("\n=== negative test ===")
    malformed = load_yaml(MALFORMED_PATH)
    errors = list(meta_validator.iter_errors(malformed))
    if errors:
        print(
            f"  [PASS] malformed.yaml correctly rejected "
            f"({len(errors)} meta-schema error(s))"
        )
        for err in errors[:5]:
            path = "/".join(str(p) for p in err.path) or "<root>"
            print(f"         - {path}: {err.message}")
    else:
        print("  [FAIL] malformed.yaml was accepted — meta-schema too permissive")
        overall_ok = False

    # --- 3-6. Every contract validates + deeper structural checks ---
    print("\n=== contracts ===")
    contract_paths = sorted(CONTRACTS_DIR.glob("*.contract.yaml"))
    if not contract_paths:
        print("  [FAIL] no contract files found under contracts/")
        return 1

    taxonomy_actions = extract_taxonomy_actions(TAXONOMY_PATH)
    actions_with_contracts: set[str] = set()

    for contract_path in contract_paths:
        stem = contract_path.name.replace(".contract.yaml", "")
        print(f"  {stem}")
        contract = load_yaml(contract_path)

        # meta-schema
        errs = list(meta_validator.iter_errors(contract))
        if errs:
            print(f"    [FAIL] meta-schema: {'; '.join(e.message for e in errs[:3])}")
            overall_ok = False
            continue
        print("    [PASS] meta-schema")

        # required_inputs is itself a valid Draft 2020-12 schema
        try:
            Draft202012Validator.check_schema(contract["required_inputs"])
            print("    [PASS] required_inputs is a valid Draft 2020-12 schema")
        except SchemaError as exc:
            print(f"    [FAIL] required_inputs is not valid Draft 2020-12: {exc.message}")
            overall_ok = False

        # output_schema reference points to a real file (or is null)
        out = contract["output_schema"]
        if out is None:
            print("    [PASS] output_schema is null")
        else:
            target = REPO_ROOT / out
            if target.is_file():
                print(f"    [PASS] output_schema -> {out}")
            else:
                print(f"    [FAIL] output_schema -> {out} (file missing)")
                overall_ok = False

        # action field matches filename stem
        if contract["action"] == stem:
            print("    [PASS] action matches filename stem")
            actions_with_contracts.add(contract["action"])
        else:
            print(
                f"    [FAIL] action '{contract['action']}' does not match filename "
                f"stem '{stem}'"
            )
            overall_ok = False

    # --- 7. Every taxonomy action has exactly one contract ---
    print("\n=== taxonomy <-> contracts coverage ===")
    missing = taxonomy_actions - actions_with_contracts
    extra = actions_with_contracts - taxonomy_actions
    if missing:
        print(f"  [FAIL] taxonomy actions without a contract: {sorted(missing)}")
        overall_ok = False
    if extra:
        print(f"  [FAIL] contracts without a taxonomy action: {sorted(extra)}")
        overall_ok = False
    if not missing and not extra:
        print(
            f"  [PASS] {len(actions_with_contracts)} taxonomy actions "
            "each have exactly one contract"
        )

    print()
    if overall_ok:
        print("ALL CHECKS PASSED")
        return 0
    print("ONE OR MORE CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
