"""AIEOS conformance test harness.

Runs a conformance suite against a candidate adapter and emits a
conformance-attestation payload on pass or a diagnostic report on fail.

v1 scope: produces the unsigned attestation payload matching
schema/conformance-attestation.schema.json. Signing (wrapping the payload
in a DSSE envelope inside a Sigstore bundle) is performed by the adapter
CI pipeline via cosign-installer + sign-blob.
"""
