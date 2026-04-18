#!/usr/bin/env python3
"""Cross-validate the CI and CD example specs against the frozen taxonomy,
contracts, and their respective schemas.

Five integrity checks:
  1. Every action referenced in both specs exists in the taxonomy.
  2. Every action referenced in both specs has a matching contract.
  3. CI spec dependency graph is a DAG (no cycles).
  4. CD spec promotion graph is a DAG (no cycles).
  5. CD spec artifact_ref is compatible with the CI spec's output — CI spec
     must contain at least one build.artifact or publish.artifact action, and
     the CD spec's artifact_ref must be a non-empty reference string.

Prerequisite: both example specs must validate against their schemas. The
script runs schema validation first and bails early if either fails.

Exit code:
  0 — every check passed.
  1 — at least one check failed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_SCHEMA = REPO_ROOT / "schema" / "ci-spec.schema.json"
CD_SCHEMA = REPO_ROOT / "schema" / "cd-spec.schema.json"
CI_EXAMPLE = REPO_ROOT / "examples" / "artifact-store.ci-spec.yaml"
CD_EXAMPLE = REPO_ROOT / "examples" / "artifact-store.cd-spec.yaml"
TAXONOMY = REPO_ROOT / "taxonomy" / "actions-v1.md"
CONTRACTS_DIR = REPO_ROOT / "contracts"


def load_yaml(path: Path) -> Any:
    with path.open() as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def extract_taxonomy_actions(path: Path) -> set[str]:
    pattern = re.compile(r"^### ([a-z][a-z0-9]*\.[a-z][a-z0-9-]*)\s*$", re.MULTILINE)
    return set(pattern.findall(path.read_text()))


def contract_actions() -> set[str]:
    return {p.name.replace(".contract.yaml", "") for p in CONTRACTS_DIR.glob("*.contract.yaml")}


def ci_action_ids(ci: dict[str, Any]) -> list[str]:
    return [a["action"] for a in ci["actions"]]


def cd_action_ids(cd: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for env in cd["environments"]:
        for a in env["actions"]:
            ids.append(a["action"])
    return ids


def has_cycle_directed(nodes: set[str], edges: list[tuple[str, str]]) -> bool:
    """Kahn's topo sort. Returns True if a cycle is present."""
    in_degree = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = {n: [] for n in nodes}
    for src, dst in edges:
        if src not in in_degree or dst not in in_degree:
            continue
        adj[src].append(dst)
        in_degree[dst] += 1
    queue = [n for n, d in in_degree.items() if d == 0]
    visited = 0
    while queue:
        n = queue.pop()
        visited += 1
        for m in adj[n]:
            in_degree[m] -= 1
            if in_degree[m] == 0:
                queue.append(m)
    return visited != len(nodes)


def check_schema(spec_path: Path, schema_path: Path) -> tuple[bool, str]:
    schema = load_json(schema_path)
    spec = load_yaml(spec_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(spec), key=lambda e: e.path)
    if errors:
        msgs = "; ".join(e.message for e in errors[:3])
        return False, msgs
    return True, f"{spec_path.name} validates against {schema_path.name}"


def main() -> int:
    print("=== schema prerequisites ===")
    ok_ci, ci_msg = check_schema(CI_EXAMPLE, CI_SCHEMA)
    print(f"  [{'PASS' if ok_ci else 'FAIL'}] {ci_msg}")
    ok_cd, cd_msg = check_schema(CD_EXAMPLE, CD_SCHEMA)
    print(f"  [{'PASS' if ok_cd else 'FAIL'}] {cd_msg}")
    if not (ok_ci and ok_cd):
        print("schema prerequisites failed; aborting.")
        return 1

    ci_spec = load_yaml(CI_EXAMPLE)
    cd_spec = load_yaml(CD_EXAMPLE)

    taxonomy = extract_taxonomy_actions(TAXONOMY)
    contracts = contract_actions()

    all_ok = True

    # --- 1. Every action in both specs exists in the taxonomy ---
    print("\n=== 1. actions exist in taxonomy ===")
    referenced = set(ci_action_ids(ci_spec)) | set(cd_action_ids(cd_spec))
    missing_in_tax = referenced - taxonomy
    if missing_in_tax:
        print(f"  [FAIL] actions not in taxonomy: {sorted(missing_in_tax)}")
        all_ok = False
    else:
        print(f"  [PASS] all {len(referenced)} referenced actions are in the taxonomy")

    # --- 2. Every action has a matching contract ---
    print("\n=== 2. actions have contracts ===")
    missing_contracts = referenced - contracts
    if missing_contracts:
        print(f"  [FAIL] actions without a contract: {sorted(missing_contracts)}")
        all_ok = False
    else:
        print(f"  [PASS] all {len(referenced)} referenced actions have a contract")

    # --- 3. CI spec dependency graph is a DAG ---
    print("\n=== 3. CI dependency graph is a DAG ===")
    ci_nodes = {a["action"] for a in ci_spec["actions"]}
    ci_edges: list[tuple[str, str]] = []
    for a in ci_spec["actions"]:
        for dep in a.get("depends_on", []):
            ci_edges.append((dep, a["action"]))
    dangling = {dep for dep, _ in ci_edges} - ci_nodes
    if dangling:
        print(f"  [FAIL] depends_on references actions not declared in the spec: {sorted(dangling)}")
        all_ok = False
    elif has_cycle_directed(ci_nodes, ci_edges):
        print("  [FAIL] CI spec dependency graph has a cycle")
        all_ok = False
    else:
        print(f"  [PASS] CI spec DAG: {len(ci_nodes)} nodes, {len(ci_edges)} edges, acyclic")

    # --- 4. CD promotion graph is a DAG ---
    print("\n=== 4. CD promotion graph is a DAG ===")
    cd_env_names = {e["name"] for e in cd_spec["environments"]}
    cd_edges = [(p["from"], p["to"]) for p in cd_spec.get("promotions", [])]
    dangling_envs = {n for pair in cd_edges for n in pair} - cd_env_names
    if dangling_envs:
        print(f"  [FAIL] promotions reference undeclared environments: {sorted(dangling_envs)}")
        all_ok = False
    elif has_cycle_directed(cd_env_names, cd_edges):
        print("  [FAIL] CD promotion graph has a cycle")
        all_ok = False
    else:
        print(f"  [PASS] CD promotion graph: {len(cd_env_names)} envs, {len(cd_edges)} edges, acyclic")

    # --- 5. artifact_ref compatibility ---
    print("\n=== 5. CD artifact_ref compatible with CI output ===")
    ci_produces_artifact = any(
        a["action"] in {"build.artifact", "publish.artifact"} for a in ci_spec["actions"]
    )
    cd_ref = cd_spec.get("artifact_ref")
    if not ci_produces_artifact:
        print("  [FAIL] CI spec does not contain build.artifact or publish.artifact — nothing to promote")
        all_ok = False
    elif not isinstance(cd_ref, str) or not cd_ref:
        print("  [FAIL] CD spec artifact_ref is missing or empty")
        all_ok = False
    else:
        print(f"  [PASS] CI produces an artifact; CD consumes ref '{cd_ref[:60]}{'…' if len(cd_ref) > 60 else ''}'")

    print()
    if all_ok:
        print("ALL CHECKS PASSED")
        return 0
    print("ONE OR MORE CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
