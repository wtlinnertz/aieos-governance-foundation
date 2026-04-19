"""M4a.0 — conformance harness tests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

# Make the harness importable without packaging.
import sys

HARNESS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = HARNESS_DIR.parent.parent
sys.path.insert(0, str(HARNESS_DIR.parent.parent))

from conformance.harness.runner import HarnessResult, load_suite, run_conformance


ATTESTATION_SCHEMA = json.loads(
    (REPO_ROOT / "schema" / "conformance-attestation.schema.json").read_text()
)


@dataclass
class _Result:
    findings: dict[str, Any] | None
    evidence: list[str]
    exit_code: int = 0


class _PassingAdapter:
    """Adapter that emits canned passing JUnit-JSON output matching the
    skeleton test.unit-suite's expected shape."""

    def execute(self, inputs):
        expected_path = Path(inputs["expected_dir"]) / "smoke.junit.json"
        findings = json.loads(expected_path.read_text())
        # Inject a timing field that the suite's tolerances list allows to differ.
        findings["time"] = 0.017
        for ts in findings["testsuite"]:
            ts["time"] = 0.017
            for tc in ts["testcase"]:
                tc["time"] = 0.008
        return _Result(
            findings=findings,
            evidence=[
                "junit-report://local/out.json",
                "coverage-report://local/coverage.xml",
                "exit-code:0",
            ],
            exit_code=0,
        )


class _FailingAdapter:
    """Adapter that emits findings that violate the expected structural match."""

    def execute(self, inputs):
        return _Result(
            findings={"name": "smoke", "tests": 99, "failures": 99, "errors": 0, "testsuite": []},
            evidence=["junit-report://local/out.json", "exit-code:0"],
            exit_code=0,
        )


class _SchemaViolatingAdapter:
    """Adapter whose output is missing required JUnit-JSON fields."""

    def execute(self, inputs):
        return _Result(findings={"bogus": True}, evidence=[], exit_code=0)


class _RaisingAdapter:
    def execute(self, inputs):
        raise RuntimeError("adapter crashed")


SUITE_DIR = REPO_ROOT / "conformance" / "test.unit-suite"
SIGNER = (
    "https://github.com/wtlinnertz/adapter-pytest-unit/.github/workflows/"
    "adapter-ci.yml@refs/heads/main"
)


def test_harness_produces_signed_attestation_on_pass():
    suite = load_suite(SUITE_DIR)

    result = run_conformance(
        suite=suite,
        adapter=_PassingAdapter(),
        adapter_id="adapter-pytest-unit",
        adapter_version="1.0.0",
        signing_identity=SIGNER,
        clock=lambda: datetime(2026, 4, 18, 20, 0, 0, tzinfo=UTC),
    )

    assert result.passed is True
    assert result.attestation is not None
    assert result.diagnostic is None
    # Attestation validates against the frozen schema
    errors = list(Draft202012Validator(ATTESTATION_SCHEMA).iter_errors(result.attestation))
    assert errors == []
    assert result.attestation["subject"]["adapter_id"] == "adapter-pytest-unit"
    assert result.attestation["predicate"]["contract_id"] == "test.unit"
    assert result.attestation["predicate"]["contract_version"] == "1.0.0"
    assert result.attestation["result"] == "pass"


def test_harness_rejects_structural_mismatch():
    suite = load_suite(SUITE_DIR)

    result = run_conformance(
        suite=suite,
        adapter=_FailingAdapter(),
        adapter_id="adapter-pytest-unit",
        adapter_version="1.0.0",
        signing_identity=SIGNER,
    )

    assert result.passed is False
    assert result.attestation is None
    assert result.diagnostic is not None
    assert any("structural_match" == f["criterion"] for f in result.diagnostic["failures"])


def test_harness_rejects_schema_violation():
    suite = load_suite(SUITE_DIR)

    result = run_conformance(
        suite=suite,
        adapter=_SchemaViolatingAdapter(),
        adapter_id="adapter-pytest-unit",
        adapter_version="1.0.0",
        signing_identity=SIGNER,
    )

    assert result.passed is False
    assert result.attestation is None
    assert any("schema_conformance" == f["criterion"] for f in result.diagnostic["failures"])


def test_harness_captures_adapter_exception_as_diagnostic():
    suite = load_suite(SUITE_DIR)

    result = run_conformance(
        suite=suite,
        adapter=_RaisingAdapter(),
        adapter_id="adapter-pytest-unit",
        adapter_version="1.0.0",
        signing_identity=SIGNER,
    )

    assert result.passed is False
    assert result.attestation is None
    assert result.diagnostic is not None
    assert any("adapter_execution" == f["criterion"] for f in result.diagnostic["failures"])


def test_harness_enforces_evidence_presence():
    suite = load_suite(SUITE_DIR)

    class _NoEvidenceAdapter:
        def execute(self, inputs):
            expected_path = Path(inputs["expected_dir"]) / "smoke.junit.json"
            findings = json.loads(expected_path.read_text())
            findings["time"] = 0.017
            for ts in findings["testsuite"]:
                ts["time"] = 0.017
                for tc in ts["testcase"]:
                    tc["time"] = 0.008
            return _Result(findings=findings, evidence=[], exit_code=0)

    result = run_conformance(
        suite=suite,
        adapter=_NoEvidenceAdapter(),
        adapter_id="adapter-pytest-unit",
        adapter_version="1.0.0",
        signing_identity=SIGNER,
    )

    assert result.passed is False
    assert any("evidence_presence" == f["criterion"] for f in result.diagnostic["failures"])
