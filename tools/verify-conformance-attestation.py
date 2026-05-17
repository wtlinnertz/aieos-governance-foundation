#!/usr/bin/env python3
"""
AIEOS M0: Conformance attestation verification prototype.
Verifies a Cosign attestation against the AIEOS conformance predicate schema.

Field paths match schema/conformance-attestation.schema.json:
  - result: const "pass" (lowercase)
  - predicate.contract_id: capability contract identifier
  - predicate.contract_version: contract semver

Usage:
    python3 verify-conformance-attestation.py <image-ref> \\
        --contract-id test.unit \\
        --contract-version 1.0.0 \\
        [--identity-regexp <pattern>] \\
        [--oidc-issuer <issuer>] \\
        [--predicate-type <uri>]

Exit codes:
    0 = verification passed
    1 = verification failed (reason printed to stderr)
    2 = tool error (cosign not found, timeout, etc.)
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from typing import Optional

PREDICATE_TYPE = "https://aieos.dev/attestations/conformance/v1"
OIDC_ISSUER = "https://token.actions.githubusercontent.com"
DEFAULT_IDENTITY_REGEXP = r"https://github\.com/wtlinnertz/.*"


def run_cosign_verify(
    image_ref: str,
    predicate_type: str,
    identity_regexp: str,
    oidc_issuer: str,
) -> tuple[int, str, str]:
    """Run cosign verify-attestation; return (returncode, stdout, stderr)."""
    cmd = [
        "cosign", "verify-attestation",
        "--type", predicate_type,
        "--certificate-identity-regexp", identity_regexp,
        "--certificate-oidc-issuer", oidc_issuer,
        image_ref,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 2, "", "cosign verify-attestation timed out (>30s)"
    except FileNotFoundError:
        return 2, "", "cosign not found — install cosign and ensure it is on PATH"


def decode_payload(raw: dict) -> Optional[dict]:
    """Extract and decode the predicate from a cosign attestation JSON object.

    cosign outputs DSSE envelopes. The payload field is base64-encoded and
    contains an in-toto Statement:
        {"_type": "...", "predicateType": "...", "predicate": {...}}
    We return the predicate dict, which is the AIEOS conformance payload.
    """
    try:
        encoded = raw.get("payload", "")
        decoded = base64.b64decode(encoded).decode("utf-8")
        statement = json.loads(decoded)
        # in-toto statement: {"predicateType": ..., "predicate": {...}}
        predicate = statement.get("predicate")
        if predicate is not None:
            return predicate
        # Fallback: some cosign versions embed the payload directly
        return statement
    except Exception:
        return None


def check_payload(
    payload: dict,
    expected_contract_id: str,
    expected_contract_version: str,
) -> tuple[bool, str]:
    """Apply AIEOS conformance rules to a decoded predicate payload.

    Rules per schema/conformance-attestation.schema.json:
      - result must be exactly "pass" (const — lowercase)
      - predicate.contract_id must match the requested capability
      - predicate.contract_version must match the minimum required version
    """
    result = payload.get("result")
    if result != "pass":
        return False, f"result is '{result}', expected 'pass'"

    predicate = payload.get("predicate", {})

    contract_id = predicate.get("contract_id")
    if contract_id != expected_contract_id:
        return False, (
            f"contract_id mismatch: "
            f"expected '{expected_contract_id}', got '{contract_id}'"
        )

    contract_version = predicate.get("contract_version")
    if contract_version != expected_contract_version:
        return False, (
            f"contract_version mismatch: "
            f"expected '{expected_contract_version}', got '{contract_version}'"
        )

    return True, "all checks passed"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify AIEOS conformance attestation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "image_ref",
        help="OCI image reference to verify (digest form preferred, e.g. ghcr.io/org/img@sha256:...)",
    )
    parser.add_argument(
        "--contract-id",
        required=True,
        help="Expected predicate.contract_id, e.g. test.unit",
    )
    parser.add_argument(
        "--contract-version",
        required=True,
        help="Expected predicate.contract_version, e.g. 1.0.0",
    )
    parser.add_argument("--identity-regexp", default=DEFAULT_IDENTITY_REGEXP)
    parser.add_argument("--oidc-issuer", default=OIDC_ISSUER)
    parser.add_argument("--predicate-type", default=PREDICATE_TYPE)
    args = parser.parse_args()

    returncode, stdout, stderr = run_cosign_verify(
        args.image_ref,
        args.predicate_type,
        args.identity_regexp,
        args.oidc_issuer,
    )

    if returncode == 2:
        print(f"ERROR: {stderr}", file=sys.stderr)
        return 2

    if returncode != 0:
        print("FAIL: cosign signature verification failed", file=sys.stderr)
        print(stderr, file=sys.stderr)
        return 1

    # Parse each attestation line (cosign may return multiple JSON objects)
    passed_count = 0
    for line in stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue

        payload = decode_payload(raw)
        if payload is None:
            print("WARN: could not decode attestation payload, skipping", file=sys.stderr)
            continue

        ok, reason = check_payload(
            payload,
            args.contract_id,
            args.contract_version,
        )
        if ok:
            passed_count += 1
            print(f"PASS: attestation verified")
            subject = payload.get("subject", {})
            predicate = payload.get("predicate", {})
            print(f"  adapter:  {subject.get('adapter_id')} @ {subject.get('adapter_version')}")
            print(f"  contract: {predicate.get('contract_id')} @ {predicate.get('contract_version')}")
            print(f"  result:   {payload.get('result')}")
            print(f"  identity: {payload.get('signing_identity')}")
        else:
            print(f"FAIL: payload check failed — {reason}", file=sys.stderr)
            return 1

    if passed_count == 0:
        print("FAIL: no valid attestations found for this image", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
