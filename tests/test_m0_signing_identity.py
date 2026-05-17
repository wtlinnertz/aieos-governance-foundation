"""
M0 Signing Identity — pre-flight validation tests.

These tests verify everything that can be checked locally before the GHA run.
They cover:
  - Test payload schema conformance
  - verify-conformance-attestation.py check_payload logic (E-02, E-04, E-05)
  - decode_payload DSSE envelope parsing
  - signing-identity-setup.md completeness (E-06)
  - Predicate type URI and Cosign version documented (E-07)
"""
from __future__ import annotations

import base64
import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
SCHEMA = json.load(open(REPO / "schema/conformance-attestation.schema.json"))
VALIDATOR = Draft202012Validator(SCHEMA)

# Load the verification module without relying on the tools/ package being importable
_spec = importlib.util.spec_from_file_location(
    "vca", REPO / "tools/verify-conformance-attestation.py"
)
_vca = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_vca)


# -- Schema conformance of test payloads -------------------------------------

class TestTestPayloads:
    def test_pass_payload_is_schema_valid(self):
        doc = json.load(open(REPO / "schema/test-payloads/conformance-pass.json"))
        errors = list(VALIDATOR.iter_errors(doc))
        assert errors == [], f"conformance-pass.json schema errors: {[e.message for e in errors]}"

    def test_wrong_version_payload_is_schema_valid(self):
        """Wrong contract_version is semantically wrong, not structurally invalid."""
        doc = json.load(open(REPO / "schema/test-payloads/conformance-wrong-version.json"))
        errors = list(VALIDATOR.iter_errors(doc))
        assert errors == [], f"conformance-wrong-version.json schema errors: {[e.message for e in errors]}"

    def test_fail_payload_is_schema_invalid(self):
        """result='fail' violates const:'pass' — schema should reject it."""
        doc = json.load(open(REPO / "schema/test-payloads/conformance-fail.json"))
        errors = list(VALIDATOR.iter_errors(doc))
        assert errors, "conformance-fail.json should fail schema validation but was accepted"
        result_errors = [e for e in errors if list(e.path) == ["result"] or e.path == []]
        # At minimum the result const violation should be flagged
        messages = " ".join(e.message for e in errors)
        assert "pass" in messages, f"Expected const violation mentioning 'pass', got: {messages}"

    def test_pass_payload_subject_fields(self):
        doc = json.load(open(REPO / "schema/test-payloads/conformance-pass.json"))
        assert doc["subject"]["adapter_id"].startswith("adapter-")
        assert doc["subject"]["adapter_version"]
        assert doc["predicate"]["contract_id"]
        assert doc["predicate"]["contract_version"]
        assert doc["result"] == "pass"
        assert doc["signing_identity"]  # minLength: 1

    def test_wrong_version_has_lower_semver(self):
        """Sanity check: wrong-version payload has an older contract_version."""
        wrong = json.load(open(REPO / "schema/test-payloads/conformance-wrong-version.json"))
        # Should have a lower version than the PASS payload's contract_version
        assert wrong["predicate"]["contract_version"] < "1.0.0"


# -- check_payload verification logic ----------------------------------------

class TestCheckPayload:
    """Covers E-02 (PASS accepted), E-04 (fail rejected), E-05 (version rejected)."""

    def _make_payload(self, result="pass", contract_id="test.unit", contract_version="1.0.0"):
        return {
            "subject": {"adapter_id": "adapter-test", "adapter_version": "0.0.1"},
            "predicate": {"contract_id": contract_id, "contract_version": contract_version},
            "result": result,
            "suite_run_id": "test-run-abc123456789",
            "signing_identity": "https://github.com/wtlinnertz/test/.github/workflows/ci.yml",
            "timestamp": "2026-05-15T00:00:00Z",
        }

    def test_pass_accepted(self):
        """E-02: valid pass attestation is accepted."""
        ok, reason = _vca.check_payload(self._make_payload(), "test.unit", "1.0.0")
        assert ok, f"Expected pass, got rejection: {reason}"
        assert reason == "all checks passed"

    def test_fail_result_rejected(self):
        """E-04: result='fail' is rejected."""
        ok, reason = _vca.check_payload(self._make_payload(result="fail"), "test.unit", "1.0.0")
        assert not ok
        assert "fail" in reason
        assert "pass" in reason

    def test_wrong_contract_version_rejected(self):
        """E-05: attestation with older contract_version is rejected."""
        ok, reason = _vca.check_payload(
            self._make_payload(contract_version="0.9.0"), "test.unit", "1.0.0"
        )
        assert not ok
        assert "version" in reason
        assert "0.9.0" in reason

    def test_wrong_contract_id_rejected(self):
        ok, reason = _vca.check_payload(
            self._make_payload(contract_id="security.sast"), "test.unit", "1.0.0"
        )
        assert not ok
        assert "contract_id" in reason

    def test_missing_predicate_rejected(self):
        payload = {"result": "pass"}  # no predicate key
        ok, reason = _vca.check_payload(payload, "test.unit", "1.0.0")
        assert not ok
        assert "contract_id" in reason

    def test_uppercase_pass_rejected(self):
        """Schema uses lowercase 'pass' const — uppercase must be rejected."""
        ok, reason = _vca.check_payload(self._make_payload(result="PASS"), "test.unit", "1.0.0")
        assert not ok
        assert "PASS" in reason or "pass" in reason


# -- decode_payload DSSE envelope parsing ------------------------------------

class TestDecodePayload:

    def _make_envelope(self, predicate: dict) -> dict:
        """Build a synthetic cosign DSSE envelope wrapping the given predicate."""
        statement = {
            "_type": "https://in-toto.io/Statement/v0.1",
            "predicateType": "https://aieos.dev/attestations/conformance/v1",
            "predicate": predicate,
        }
        return {
            "payloadType": "application/vnd.in-toto+json",
            "payload": base64.b64encode(json.dumps(statement).encode()).decode(),
            "signatures": [],
        }

    def test_decode_returns_predicate(self):
        predicate = {"result": "pass", "predicate": {"contract_id": "test.unit"}}
        envelope = self._make_envelope(predicate)
        decoded = _vca.decode_payload(envelope)
        assert decoded is not None
        assert decoded["result"] == "pass"
        assert decoded["predicate"]["contract_id"] == "test.unit"

    def test_decode_handles_malformed_base64(self):
        decoded = _vca.decode_payload({"payload": "!!!not-base64!!!"})
        assert decoded is None

    def test_decode_handles_missing_payload(self):
        decoded = _vca.decode_payload({})
        assert decoded is None

    def test_decode_to_check_pipeline(self):
        """Full decode -> check_payload pipeline with a valid payload."""
        predicate = {
            "subject": {"adapter_id": "adapter-test", "adapter_version": "1.0.0"},
            "predicate": {"contract_id": "test.unit", "contract_version": "1.0.0"},
            "result": "pass",
            "suite_run_id": "test-run-abc123456789",
            "signing_identity": "https://github.com/wtlinnertz/adapter/.github/workflows/ci.yml",
            "timestamp": "2026-05-15T00:00:00Z",
        }
        envelope = self._make_envelope(predicate)
        decoded = _vca.decode_payload(envelope)
        assert decoded is not None
        ok, reason = _vca.check_payload(decoded, "test.unit", "1.0.0")
        assert ok, reason


# -- E-06: signing-identity-setup.md completeness ----------------------------

class TestSigningSetupDoc:
    DOC = REPO / "docs/signing-identity-setup.md"

    def test_file_exists(self):
        assert self.DOC.exists(), "docs/signing-identity-setup.md not found"

    def test_contains_predicate_type_uri(self):
        content = self.DOC.read_text()
        assert "https://aieos.dev/attestations/conformance/v1" in content

    def test_contains_cosign_version(self):
        content = self.DOC.read_text()
        assert "v2.6.3" in content

    def test_contains_id_token_permission(self):
        content = self.DOC.read_text()
        assert "id-token: write" in content

    def test_contains_cosign_attest_command(self):
        content = self.DOC.read_text()
        assert "cosign attest" in content

    def test_contains_cosign_verify_command(self):
        content = self.DOC.read_text()
        assert "cosign verify-attestation" in content

    def test_contains_enterprise_path(self):
        content = self.DOC.read_text()
        assert "Enterprise" in content or "enterprise" in content


# -- E-07: predicate type URI and Cosign version documented ------------------

class TestE07Documentation:
    WORKFLOW = REPO / ".github/workflows/m0-signing-test.yml"

    def test_workflow_exists(self):
        assert self.WORKFLOW.exists()

    def test_workflow_has_correct_predicate_type(self):
        content = self.WORKFLOW.read_text()
        assert "https://aieos.dev/attestations/conformance/v1" in content

    def test_workflow_pins_cosign_v2_6_3(self):
        content = self.WORKFLOW.read_text()
        assert "v2.6.3" in content

    def test_workflow_requires_id_token_write(self):
        content = self.WORKFLOW.read_text()
        assert "id-token: write" in content

    def test_predicate_type_consistent_across_files(self):
        """URI must be identical in workflow, setup doc, and verification script."""
        uri = "https://aieos.dev/attestations/conformance/v1"
        for path in [
            self.WORKFLOW,
            REPO / "docs/signing-identity-setup.md",
            REPO / "tools/verify-conformance-attestation.py",
        ]:
            content = path.read_text()
            assert uri in content, f"Predicate type URI missing from {path.name}"
