# Signing Identity — Conformance Attestations

Conformance attestations (see `schema/conformance-attestation.schema.json`, lands M1 Cascade Level 5) require a signing identity. This document is the operational reference for producing and verifying signatures. It covers two paths:

- **Local keypair path** — for development, experimentation, and offline work. No OIDC, no browser, no Rekor dependency on the signer's machine.
- **GHA keyless OIDC path** — for adapter CI pipelines that produce real, published conformance attestations. Ambient OIDC from GitHub's provider; no keys to manage.

Both paths use the Sigstore bundle format (`--bundle`) as their signature artifact. Do not use `--output-signature` or `--signature` — those flags are deprecated in cosign v3 and will be removed.

**Minimum cosign version: 2.0.0.** Verified end-to-end against cosign v3.0.6. Check with `cosign version`.

---

## Local keypair path (development)

Use when iterating locally, writing tests against signed payloads, or demonstrating the signing/verification flow without needing OIDC.

### Prerequisites

- `cosign` v2.0.0 or later on `$PATH`. Install the static binary from the Sigstore release page:
  ```bash
  curl -sSL -o $HOME/.local/bin/cosign \
    https://github.com/sigstore/cosign/releases/download/v3.0.6/cosign-linux-amd64
  chmod +x $HOME/.local/bin/cosign
  cosign version
  ```
- A scratch directory for the keypair. This directory must be `.gitignore`d. In this repo, use `test-keys/`.

### Generate a keypair

```bash
cd test-keys
COSIGN_PASSWORD="" cosign generate-key-pair
# Produces cosign.key (private, 0600) and cosign.pub (public, 0644).
```

`COSIGN_PASSWORD=""` produces an unencrypted private key. This is acceptable for local test keys only. Never commit `cosign.key`. Never reuse a test keypair for production attestations.

### Sign a blob

```bash
# test-payload.json already exists.
COSIGN_PASSWORD="" cosign sign-blob \
  --key cosign.key \
  --bundle test-payload.sigstore.json \
  --yes \
  test-payload.json
```

`--yes` skips the interactive consent prompt for uploading the signature to the Rekor public transparency log. The bundle embeds the Rekor entry; verification can operate offline once the bundle exists, but the signing step itself does reach out to Rekor.

The resulting `test-payload.sigstore.json` is a Sigstore bundle (`application/vnd.dev.sigstore.bundle.v0.3+json`) containing the public key hint, the signature, and the Rekor inclusion promise.

### Verify a blob

```bash
cosign verify-blob \
  --key cosign.pub \
  --bundle test-payload.sigstore.json \
  test-payload.json
# Expected: "Verified OK" and exit code 0.
```

Verification is offline once the bundle is in hand (no network needed to validate signature against the public key).

### When to use this path

- Iterating on adapter code that produces or consumes signed artifacts.
- Writing and running local tests.
- Demonstrating the signing flow in documentation or training.
- Anything where the resulting signature is *not* intended to be trusted as a production conformance attestation.

---

## GitHub Actions keyless OIDC path (production)

Use when producing a real conformance attestation from an adapter's CI pipeline. Ambient OIDC from GitHub's provider supplies the identity; there are no long-lived keys to manage or rotate.

### Prerequisites

- The workflow runs on `github.com`-hosted runners (or a self-hosted runner with OIDC enabled).
- The workflow declares `permissions: id-token: write` so GitHub issues the OIDC token for Sigstore Fulcio.
- The adapter repo's CI has authority to publish its attestation artifact (e.g., to the release, to the attestation registry, or attached to the adapter image).

### Sample workflow snippet

Pin `sigstore/cosign-installer` to a specific commit SHA (not a tag) per repo convention.

```yaml
# .github/workflows/adapter-ci.yml (excerpt)
name: adapter-ci

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  id-token: write   # required for keyless signing via OIDC

jobs:
  conformance-and-sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<pinned-sha>

      - name: Install cosign
        uses: sigstore/cosign-installer@<pinned-sha>   # pin to a specific commit SHA
        with:
          cosign-release: 'v3.0.6'

      - name: Run conformance suite against this adapter
        run: ./scripts/run-conformance.sh
        # On pass, produces conformance-attestation.json (unsigned predicate).

      - name: Sign the conformance attestation (keyless OIDC)
        run: |
          cosign sign-blob \
            --bundle conformance-attestation.sigstore.json \
            --yes \
            conformance-attestation.json

      - name: Upload signed attestation
        uses: actions/upload-artifact@<pinned-sha>
        with:
          name: conformance-attestation
          path: |
            conformance-attestation.json
            conformance-attestation.sigstore.json
```

No `--key` flag. Cosign detects the ambient GitHub OIDC token, requests a short-lived certificate from Fulcio, signs, logs to Rekor, and writes the Sigstore bundle. The bundle is the full proof.

### Verifying a keyless signature

Verification uses the workflow identity that produced the signature, not a public key.

```bash
cosign verify-blob \
  --bundle conformance-attestation.sigstore.json \
  --certificate-identity "https://github.com/wtlinnertz/adapter-<tool>-<action>/.github/workflows/adapter-ci.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  conformance-attestation.json
```

Both `--certificate-identity` and `--certificate-oidc-issuer` are mandatory — verifying without them accepts *any* Sigstore signature, which defeats the point.

### When to use this path

- Every adapter CI pipeline that produces a conformance attestation.
- Any attestation intended to support registration of an adapter in the AIEOS capability registry.
- Any attestation consumed by `aieos-agent-harness` for registration verification.

---

## Choosing between paths

| Situation | Path |
|-----------|------|
| Writing adapter code, running local tests | Local keypair |
| Docs, demos, tutorials | Local keypair (with the test keypair clearly marked as such) |
| Adapter CI producing a real conformance attestation | GHA keyless OIDC |
| Anything the harness will treat as registration evidence | GHA keyless OIDC |

**Never mix paths.** A conformance attestation produced with a local keypair is not a valid registration artifact. The harness verification in M2.2 checks the signing identity; local keypair identities will be refused.

---

## Key-handling rules

- `test-keys/` is in `.gitignore` at the repo root. Never remove it from `.gitignore`.
- `cosign.key` (private key) must never be committed. If you suspect a commit included one, rotate it immediately and force it out of history via a secret-removal workflow.
- Local test keypairs are disposable — regenerate at any time. Do not treat the test public key as trust-rooted.
- Production signing identity is the workflow identity (OIDC issuer + subject). There is no private key to exfiltrate.

---

## Verification record

The local keypair path was verified end-to-end on 2026-04-16 against cosign v3.0.6 on Linux x86_64:

```
$ cosign version
GitVersion: v3.0.6
$ COSIGN_PASSWORD="" cosign generate-key-pair
Private key written to cosign.key
Public key written to cosign.pub
$ COSIGN_PASSWORD="" cosign sign-blob --key cosign.key --bundle test-payload.sigstore.json --yes test-payload.json
Using payload from: test-payload.json
Signing artifact...
Wrote bundle to file test-payload.sigstore.json
$ cosign verify-blob --key cosign.pub --bundle test-payload.sigstore.json test-payload.json
Verified OK
```

The GHA keyless path is documented but will be exercised end-to-end in M4 when the first adapter CI pipeline ships. That run is the first real conformance attestation.
