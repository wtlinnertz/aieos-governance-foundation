"""Conformance harness runner.

Loads a conformance suite (criteria.yaml + fixtures/ + expected/), invokes an
adapter-like callable per fixture, compares outputs against the expected
canonical shape with the suite's declared tolerances, and returns either a
conformance-attestation payload (on pass) or a diagnostic report (on fail).

The adapter interface is minimal — any object with an execute(inputs) method
returning an AdapterResult-like object (findings, evidence, exit_code) is
accepted. This matches the AdapterProtocol used by the harness (M2.3) and
the pipeline runner's MockAgent (M3.7).
"""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
FINDINGS_SCHEMAS_DIR = REPO_ROOT / "findings" / "schemas"


class AdapterCallable(Protocol):
    """Minimal adapter interface the harness consumes."""

    def execute(self, inputs: dict[str, Any]) -> Any: ...


@dataclass(frozen=True)
class SuiteSpec:
    """Parsed conformance suite metadata."""

    suite_dir: Path
    suite_id: str
    contract_id: str
    contract_version: str
    fixtures: tuple[Path, ...]
    expected: dict[str, Any]
    criteria: list[dict[str, Any]]
    inputs: dict[str, Any]  # v1.1: declarative adapter-input mapping (empty => legacy)


@dataclass(frozen=True)
class HarnessResult:
    """Outcome of a conformance run."""

    passed: bool
    attestation: dict[str, Any] | None
    diagnostic: dict[str, Any] | None


def load_suite(suite_dir: Path) -> SuiteSpec:
    criteria_doc = yaml.safe_load((suite_dir / "criteria.yaml").read_text())
    fixtures = tuple(sorted((suite_dir / "fixtures").rglob("*")))
    fixtures = tuple(p for p in fixtures if p.is_file())
    expected_files = sorted((suite_dir / "expected").glob("*.json"))
    expected: dict[str, Any] = {}
    for p in expected_files:
        expected[p.stem] = json.loads(p.read_text())
    return SuiteSpec(
        suite_dir=suite_dir,
        suite_id=criteria_doc["suite"],
        contract_id=criteria_doc["contract"],
        contract_version=criteria_doc["contract_version"],
        fixtures=fixtures,
        expected=expected,
        criteria=list(criteria_doc.get("criteria", [])),
        inputs=dict(criteria_doc.get("inputs", {})),
    )


class ConformanceInputError(Exception):
    """Raised when a suite's declared inputs cannot be resolved."""


def _resolve_inputs(suite: SuiteSpec) -> dict[str, Any]:
    """Build the adapter-input dict from the suite's declarative `inputs` block.

    Each entry maps a contract input key to one resolver:
      fixture: <relpath>  -> absolute path of suite_dir/<relpath>
      value:   <literal>  -> passed through as-is
      env:     <VAR>      -> value of environment variable VAR (set by the
                             run-conformance action for image/service fixtures)

    When a suite declares no `inputs` block, fall back to the v1 legacy shape
    ({fixtures_dir, expected_dir}) so unmigrated suites keep working.
    """
    if not suite.inputs:
        return {
            "fixtures_dir": str(suite.suite_dir / "fixtures"),
            "expected_dir": str(suite.suite_dir / "expected"),
        }
    resolved: dict[str, Any] = {}
    for key, spec in suite.inputs.items():
        if not isinstance(spec, dict):
            raise ConformanceInputError(f"input {key!r}: expected a resolver mapping, got {spec!r}")
        if "fixture" in spec:
            resolved[key] = str((suite.suite_dir / spec["fixture"]).resolve())
        elif "value" in spec:
            resolved[key] = spec["value"]
        elif "env" in spec:
            var = spec["env"]
            val = os.environ.get(var)
            if val is None:
                raise ConformanceInputError(
                    f"input {key!r}: environment variable {var!r} is not set "
                    "(the run-conformance action must export it)"
                )
            resolved[key] = val
        else:
            raise ConformanceInputError(f"input {key!r}: unknown resolver {spec!r}")
    return resolved


def _validator_for_schema(schema_path: Path) -> Draft202012Validator:
    schema = json.loads(schema_path.read_text())
    return Draft202012Validator(schema)


def _resolve_schema_path(relative: str) -> Path:
    return REPO_ROOT / relative


def _apply_tolerances(
    document: dict[str, Any], tolerances: list[dict[str, Any]] | None
) -> dict[str, Any]:
    """Drop fields matched by the tolerance paths before structural comparison.

    v1 supports a single tolerance rule: 'any-non-negative-number' — when
    the rule matches, the field is elided from both sides so structural
    comparison ignores it.
    """
    if not tolerances:
        return document

    def prune(path_segments: list[str], obj: Any) -> Any:
        if not path_segments:
            return None  # drop
        head, rest = path_segments[0], path_segments[1:]
        if head == "[*]":
            if isinstance(obj, list):
                return [prune(rest, item) for item in obj]
            return obj
        if isinstance(obj, dict):
            if head in obj:
                new_value = prune(rest, obj[head])
                cloned = dict(obj)
                if new_value is None:
                    cloned.pop(head, None)
                else:
                    cloned[head] = new_value
                return cloned
        return obj

    pruned = document
    for tol in tolerances:
        segments = [s if s == "[*]" else s.strip() for s in re.split(r"\.|(\[\*\])", tol["path"]) if s]
        pruned = prune(segments, pruned)
    return pruned


def _evaluate_structural_match(
    actual: dict[str, Any],
    expected: dict[str, Any],
    tolerances: list[dict[str, Any]] | None,
) -> tuple[bool, str]:
    a = _apply_tolerances(actual, tolerances)
    e = _apply_tolerances(expected, tolerances)
    if a == e:
        return True, "structural match"
    return False, f"structural mismatch: {json.dumps(a)} != {json.dumps(e)}"


def _evaluate_schema_conformance(
    actual: dict[str, Any], schema_path: Path
) -> tuple[bool, str]:
    validator = _validator_for_schema(schema_path)
    errors = sorted(validator.iter_errors(actual), key=lambda e: list(e.path))
    if errors:
        path = "/".join(str(p) for p in errors[0].path) or "<root>"
        return False, f"schema violation at {path}: {errors[0].message}"
    return True, "schema valid"


def _build_attestation(
    adapter_id: str,
    adapter_version: str,
    contract_id: str,
    contract_version: str,
    signing_identity: str,
    clock: Any = None,
) -> dict[str, Any]:
    now = (clock() if clock else datetime.now(UTC))
    ts = now.isoformat()
    if ts.endswith("+00:00"):
        ts = ts[:-6] + "Z"
    return {
        "subject": {"adapter_id": adapter_id, "adapter_version": adapter_version},
        "predicate": {"contract_id": contract_id, "contract_version": contract_version},
        "suite_run_id": str(uuid.uuid4()),
        "result": "pass",
        "signing_identity": signing_identity,
        "timestamp": ts,
    }


def run_conformance(
    suite: SuiteSpec,
    adapter: AdapterCallable,
    adapter_id: str,
    adapter_version: str,
    signing_identity: str,
    clock: Any = None,
) -> HarnessResult:
    """Execute the suite against the adapter. Return HarnessResult.

    The caller is responsible for signing the returned attestation (cosign
    sign-blob in adapter CI). On failure, diagnostic is non-null and
    attestation is None — no attestation is produced on any check failure.
    """
    diagnostics: list[dict[str, Any]] = []

    # v1.1: build the adapter input from the suite's declarative `inputs`
    # mapping (contract keys -> fixture paths / literals / env-injected refs).
    # Suites with no `inputs` block fall back to the v1 {fixtures_dir,
    # expected_dir} shape via _resolve_inputs.
    try:
        inputs = _resolve_inputs(suite)
    except ConformanceInputError as exc:
        return HarnessResult(
            passed=False,
            attestation=None,
            diagnostic={
                "suite": suite.suite_id,
                "failures": [{"criterion": "input_resolution", "detail": str(exc)}],
            },
        )
    try:
        result = adapter.execute(inputs)
    except Exception as exc:  # noqa: BLE001 - become a diagnostic
        return HarnessResult(
            passed=False,
            attestation=None,
            diagnostic={
                "suite": suite.suite_id,
                "failures": [
                    {
                        "criterion": "adapter_execution",
                        "detail": f"adapter raised {type(exc).__name__}: {exc}",
                    }
                ],
            },
        )

    actual_findings = result.findings or {}
    actual_evidence = result.evidence or []
    actual_exit_code = getattr(result, "exit_code", 0)

    for crit in suite.criteria:
        ctype = crit["type"]
        assertion = crit.get("assertion", {})
        scope = assertion.get("scope", "every-fixture")

        if ctype == "schema_conformance":
            schema_path = _resolve_schema_path(assertion["schema"])
            ok, reason = _evaluate_schema_conformance(actual_findings, schema_path)
            if not ok:
                diagnostics.append({"criterion": crit["id"], "detail": reason})

        elif ctype == "structural_match":
            # Compare adapter's findings against the first expected doc.
            if not suite.expected:
                diagnostics.append(
                    {"criterion": crit["id"], "detail": "no expected/*.json files found"}
                )
                continue
            expected_doc = next(iter(suite.expected.values()))
            ok, reason = _evaluate_structural_match(
                actual_findings, expected_doc, crit.get("tolerances")
            )
            if not ok:
                diagnostics.append({"criterion": crit["id"], "detail": reason})

        elif ctype == "exit_code":
            expected_code = assertion.get("expected_exit_code", 0)
            if actual_exit_code != expected_code:
                diagnostics.append(
                    {
                        "criterion": crit["id"],
                        "detail": f"exit code {actual_exit_code} != expected {expected_code}",
                    }
                )

        elif ctype == "evidence_presence":
            required = set(assertion.get("required", []))
            observed_kinds = set()
            for ev in actual_evidence:
                # Evidence refs are identifiers like "junit-report" or URIs.
                # Match by prefix (contains) for v1 flexibility.
                for kind in required:
                    if kind in ev:
                        observed_kinds.add(kind)
            missing = required - observed_kinds
            if missing:
                diagnostics.append(
                    {
                        "criterion": crit["id"],
                        "detail": f"missing evidence kinds: {sorted(missing)}",
                    }
                )

        else:
            diagnostics.append(
                {
                    "criterion": crit["id"],
                    "detail": f"unknown criterion type {ctype!r} — harness cannot judge",
                }
            )

    if diagnostics:
        return HarnessResult(
            passed=False,
            attestation=None,
            diagnostic={"suite": suite.suite_id, "failures": diagnostics},
        )

    attestation = _build_attestation(
        adapter_id=adapter_id,
        adapter_version=adapter_version,
        contract_id=suite.contract_id,
        contract_version=suite.contract_version,
        signing_identity=signing_identity,
        clock=clock,
    )
    return HarnessResult(passed=True, attestation=attestation, diagnostic=None)
