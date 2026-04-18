# AIEOS Conformance Framework v1

A conformance suite is the functional-correctness test that an adapter must pass before it can register against a capability contract. Passing produces a signed conformance attestation; the harness at M2 refuses registration without a valid attestation. Failing produces a diagnostic report — no attestation, no registration.

Conformance in v1 covers **functional correctness only** — given a fixture, does the adapter produce canonical findings that match the expected shape and content? Performance bounds, resource limits, failure-mode coverage, and adversarial robustness are v2.

The real conformance test harness ships in **M4 (4.0.1)** as part of the MVP adapter catalog. This directory defines the frozen suite structure the harness will consume; the `run.sh` scripts inside each suite are placeholders until the harness lands.

---

## Directory layout

Every capability contract has one conformance suite. The suite lives at:

```
conformance/<namespace>.<action>-suite/
├── fixtures/        # test inputs the adapter must process
├── expected/        # expected canonical findings shape (JSON, validates against the findings schema)
├── run.sh           # entry point — takes an adapter reference, runs it against fixtures
└── criteria.yaml    # pass criteria
```

The suite directory name is `<namespace>.<action>-suite` — matches the `conformance_suite` field in the corresponding contract under `contracts/<namespace>.<action>.contract.yaml`.

### `fixtures/`

Adapter-agnostic input files. For a `test.unit` suite, this is a minimal repository tree with a failing-and-passing test; for a `security.sast` suite, a source file with one known vulnerability; for a `sbom.generate` suite, a manifest with a handful of dependencies. Fixtures do not reference specific tools — they describe the shape of work the adapter must handle.

### `expected/`

One or more JSON files describing the canonical-findings shape the adapter is expected to produce after processing the fixtures. Each expected file validates against the findings schema pinned in the contract (e.g., `findings/schemas/junit-xml.schema.json` for `test.*` suites, `findings/schemas/sarif-2.1.0.schema.json` for `security.sast`).

The harness compares the adapter's output to `expected/` using structural equivalence plus contract-specific tolerances (e.g., timestamps and file paths may differ; test counts and severity levels must match). Tolerances are encoded in `criteria.yaml`.

### `run.sh`

The entry point the M4 harness invokes. Contract:

- **Input (argv):** a single argument — the adapter reference (binary path, container digest, or registered adapter ID). The harness may set environment variables for fixture paths, output directories, and logging.
- **Behavior:** the script invokes the adapter against every fixture in `fixtures/`, captures the adapter's output, and places structured findings under a harness-provided output directory for comparison.
- **Exit code:** 0 if every fixture ran and produced output; non-zero if the adapter or the driver itself crashed. The harness separately evaluates pass/fail against `criteria.yaml` — `run.sh` does not declare victory.

Until M4 ships, every suite's `run.sh` is a placeholder that prints an explanatory message and exits 0. Adapter authors should treat `run.sh` as the stable interface that the real harness will implement against.

### `criteria.yaml`

Pass criteria for the suite. Each criterion has a type, an assertion, and an optional tolerance. Common types:

- `schema_conformance` — adapter output validates against the contract's `output_schema`.
- `structural_match` — adapter output matches `expected/<file>.json` modulo listed tolerances.
- `exit_code` — adapter exit code matches a declared value for each fixture.
- `evidence_presence` — every artifact type in the contract's `required_evidence` is emitted.

A suite passes when every criterion holds for every fixture.

---

## Running a suite locally

The reference flow once the M4 harness is installed (v1 workflow, subject to refinement):

```bash
# from the repo root
aieos-conformance \
  --suite conformance/test.unit-suite \
  --adapter <adapter-reference> \
  --out ./conformance-output \
  --sign-identity <identity>
```

On pass: a signed conformance attestation appears at `./conformance-output/attestation.sigstore.json` (validates against `findings/schemas/oci-signing-bundle.schema.json`; its payload validates against `schema/conformance-attestation.schema.json`). The adapter can now register via M2's `register_adapter` API.

On fail: a diagnostic report at `./conformance-output/diagnostic.json` lists which criteria failed and why. No attestation is produced.

Until the harness exists, authors can run `bash conformance/<suite>/run.sh <adapter-reference>` to confirm the placeholder contract. The placeholder exits 0 with a message — real pass/fail evaluation is the harness's job.

---

## How the M4 conformance test harness consumes suites

High level (full detail lands with the M4 harness):

1. **Load.** Harness reads `criteria.yaml` and enumerates `fixtures/` and `expected/`.
2. **Invoke.** Harness calls `run.sh <adapter>`, passing fixture paths and an output directory through environment variables.
3. **Collect.** Harness reads the adapter's emitted findings and evidence from the output directory.
4. **Validate.** For each criterion in `criteria.yaml`, harness asserts the adapter's output against the expected shape and tolerances.
5. **Attest.** If all criteria hold, harness produces a signed conformance attestation per the frozen schema (`schema/conformance-attestation.schema.json`) wrapped in an OCI signing bundle.
6. **Report.** On any failure, harness emits a diagnostic listing the failing criteria; no attestation.

The harness is in this repo (or an adjacent `aieos-conformance-tester`) and runs both in adapter CI (ambient OIDC signing) and locally (keypair signing, for dry runs).

---

## Submitting an adapter for registration after passing conformance

Once the conformance harness has produced a signed attestation for your adapter at a given contract version:

1. **Publish the adapter.** Push the adapter's OCI image or binary to a registry reachable by the AIEOS harness.
2. **Publish the attestation.** Attach the signed conformance attestation bundle to the adapter's release (OCI referrer, GitHub release asset, or artifact store entry — any location the harness registration flow can fetch).
3. **Register.** Call the harness registry API (`register_adapter` — defined in M2.1) with the adapter reference, the attestation reference, and the registration context. Registration verifies the attestation against the frozen conformance-attestation schema and the signing identity, then stores the registry entry.
4. **Verify registration.** Query `find_adapters(<action>, <context>)` and confirm your adapter appears and reports healthy.

The registration API refuses adapters without a valid attestation against the current contract version, or a prior contract version that has not yet reached its cutover date (M2.2 grace logic). No attestation = no registration. No override, no "trust me" bypass.

---

## Suites in this directory

Current state — one skeleton suite exists as a structural reference for adapter authors. Additional suites are authored alongside the adapters they serve in M4a and M4b:

| Suite | Serves contract | Status |
|---|---|---|
| `test.unit-suite/` | `contracts/test.unit.contract.yaml` | skeleton — structural reference only; the `run.sh` is a placeholder |
| `test.integration-suite/` | `contracts/test.integration.contract.yaml` | to be authored in M4a |
| `test.contract-suite/` | `contracts/test.contract.contract.yaml` | to be authored when a contract-test adapter ships |
| `test.e2e-suite/` | `contracts/test.e2e.contract.yaml` | to be authored when an e2e adapter ships |
| `build.artifact-suite/` | `contracts/build.artifact.contract.yaml` | to be authored in M4a |
| `security.sast-suite/` | `contracts/security.sast.contract.yaml` | to be authored in M4b |
| `security.dast-suite/` | `contracts/security.dast.contract.yaml` | deferred — no v1 DAST adapter |
| `security.sca-suite/` | `contracts/security.sca.contract.yaml` | to be authored in M4b |
| `security.secret-scan-suite/` | `contracts/security.secret-scan.contract.yaml` | to be authored when a secret-scan adapter ships |
| `security.container-scan-suite/` | `contracts/security.container-scan.contract.yaml` | to be authored in M4b |
| `security.license-scan-suite/` | `contracts/security.license-scan.contract.yaml` | deferred |
| `sbom.generate-suite/` | `contracts/sbom.generate.contract.yaml` | to be authored in M4b |
| `sbom.verify-suite/` | `contracts/sbom.verify.contract.yaml` | to be authored when a verify adapter ships |
| `sign.artifact-suite/` | `contracts/sign.artifact.contract.yaml` | to be authored in M4a |
| `sign.attestation-suite/` | `contracts/sign.attestation.contract.yaml` | to be authored in M4a |
| `publish.artifact-suite/` | `contracts/publish.artifact.contract.yaml` | to be authored when a publish adapter ships |
| `publish.manifest-suite/` | `contracts/publish.manifest.contract.yaml` | to be authored in M4b |
| `deploy.environment-suite/` | `contracts/deploy.environment.contract.yaml` | to be authored in M4b |
| `deploy.promote-suite/` | `contracts/deploy.promote.contract.yaml` | to be authored when needed |
| `deploy.rollback-suite/` | `contracts/deploy.rollback.contract.yaml` | to be authored when needed |
| `verify.smoke-suite/` | `contracts/verify.smoke.contract.yaml` | to be authored in M4b |
| `verify.health-suite/` | `contracts/verify.health.contract.yaml` | to be authored when needed |
| `verify.slo-suite/` | `contracts/verify.slo.contract.yaml` | to be authored when needed |

The v1 framework freeze is about the suite *shape*, not about having every suite authored. Suites land alongside their adapters.
