# Signing identity setup (M0 stub)

> Full documentation ships at M7. This stub covers the minimum needed for M0 validation
> and gives adapter authors enough to replicate the signing flow in their own CI.

---

## Overview

AIEOS uses Sigstore keyless signing for adapter conformance attestations. No key management
required. The signing identity is the GitHub Actions workflow identity — scoped to a specific
repository and workflow file path. The trust anchor is the Rekor transparency log entry, not
a locally stored key.

---

## Default: Sigstore keyless (open-source adapters)

### Required GHA permissions

```yaml
permissions:
  id-token: write   # required for OIDC token exchange with Fulcio
  contents: read
  packages: write   # if pushing to GHCR (needed for the OCI attestation subject)
```

### Install Cosign (pinned)

```yaml
- uses: sigstore/cosign-installer@v3
  with:
    cosign-release: 'v2.6.3'
```

Always pin the Cosign version. Breaking changes between Cosign releases have invalidated
attestation formats in the past. The conformance attestation schema version and the pinned
Cosign version are documented together — do not upgrade Cosign without verifying the output
format is unchanged.

### Sign a conformance attestation

```bash
cosign attest \
  --predicate <your-conformance-payload.json> \
  --type "https://aieos.dev/attestations/conformance/v1" \
  --yes \
  <image-ref>@sha256:<digest>
```

The `--yes` flag skips the interactive confirmation prompt (required in CI). The payload must
conform to `schema/conformance-attestation.schema.json` in `aieos-governance-foundation`.

### Verify an attestation

```bash
cosign verify-attestation \
  --type "https://aieos.dev/attestations/conformance/v1" \
  --certificate-identity-regexp "https://github\.com/<your-org>/.*" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  <image-ref>@sha256:<digest>
```

The `--certificate-identity-regexp` is the trust boundary. Scope it to your GitHub org or
a specific repo/workflow path to tighten the acceptable signing identities.

---

## Predicate type URI

```
https://aieos.dev/attestations/conformance/v1
```

This URI is embedded in every `cosign attest` and `cosign verify-attestation` call. It
identifies attestations as AIEOS conformance attestations and cannot change after the first
adapter is attested — changing it would invalidate all existing attestations. Locked in M0,
confirmed in M1 vocabulary freeze.

---

## Attestation payload format

The predicate must conform to `schema/conformance-attestation.schema.json`. Required fields:

| Field | Example |
|-------|---------|
| `subject.adapter_id` | `"adapter-pytest-unit"` |
| `subject.adapter_version` | `"1.2.0"` |
| `predicate.contract_id` | `"test.unit"` |
| `predicate.contract_version` | `"1.0.0"` |
| `suite_run_id` | GitHub Actions run ID or UUID |
| `result` | `"pass"` (const — failures never produce an attestation) |
| `signing_identity` | GHA workflow ref (set from `$GITHUB_WORKFLOW_REF`) |
| `timestamp` | ISO 8601 UTC (e.g., `"2026-05-15T12:00:00Z"`) |

---

## Enterprise path

For organizations that cannot use the public Sigstore infrastructure:

**Self-hosted Rekor/Fulcio:** Set environment variables in adapter CI and pipeline runner:

```bash
export SIGSTORE_REKOR_URL=https://rekor.your-org.internal
export SIGSTORE_FULCIO_URL=https://fulcio.your-org.internal
```

No code changes to the adapter CI or pipeline runner are required. Cosign supports alternative
endpoints natively.

**KMS-backed key:** Use `cosign sign --key gcpkms://...` instead of keyless flow. Verification
uses `cosign verify-attestation --key <pub-key>` instead of OIDC certificate checks. The
predicate payload format is identical.

Full documentation for both enterprise paths ships at M7.

---

**Related:** M0 PRD | `schema/conformance-attestation.schema.json` | `tools/verify-conformance-attestation.py`
