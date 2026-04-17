# AIEOS Action Taxonomy v1

Canonical vocabulary of governable actions for spec-driven CI/CD. Every CI spec and CD spec composes action instances drawn from this set. Every adapter satisfies exactly one action per capability contract (multi-capability adapters declare and attest separately per contract).

Scope: v1 covers eight namespaces — `build`, `test`, `security`, `sbom`, `sign`, `publish`, `deploy`, `verify`. Quality and observability namespaces are v2. Adding a namespace after freeze requires a minor version bump and a cutover announcement per the deprecation protocol.

Each entry has exactly six fields:
1. **Identifier** — namespaced dot notation.
2. **Description** — one-line summary.
3. **Expected inputs** — type and shape the adapter receives.
4. **Expected outputs** — type and shape the adapter emits.
5. **Canonical findings schema** — reference to the upstream schema the adapter normalizes to, or `none` for actions that do not produce structured findings.
6. **Evidence consumer** — who reads the output.

Findings-schema version pins come from `findings/findings-schemas.md`. Do not reference "latest."

---

## build

### build.artifact

- **Identifier:** `build.artifact`
- **Description:** Produce a deployable artifact (OCI image, binary, package) from source.
- **Expected inputs:** source directory path (string), build context (string, optional — e.g., Containerfile path or build target), build args (object, optional).
- **Expected outputs:** artifact reference (string — OCI image digest `sha256:…`, package checksum, or equivalent), build log (text), exit code.
- **Canonical findings schema:** none. Evidence is the artifact reference plus exit code.
- **Evidence consumer:** run validator; downstream `sign.*`, `publish.*`, `deploy.*` actions.

---

## test

### test.unit

- **Identifier:** `test.unit`
- **Description:** Run unit tests — functions and classes in isolation, no external dependencies.
- **Expected inputs:** source directory path (string), test config path (string, optional — e.g., `pytest.ini`, `pyproject.toml` section), coverage threshold (number, optional).
- **Expected outputs:** JUnit XML test report, optional coverage report (Cobertura or equivalent), exit code.
- **Canonical findings schema:** `findings/schemas/junit-xml.schema.json` (JUnit XML, JUnit 4 compatible — testsuites/testsuite/testcase structure).
- **Evidence consumer:** run validator.

### test.integration

- **Identifier:** `test.integration`
- **Description:** Run integration tests — multiple components exercised together against live or containerized dependencies.
- **Expected inputs:** source directory path (string), test config path (string, optional), dependency fixtures config (object, optional — e.g., docker-compose reference).
- **Expected outputs:** JUnit XML test report, exit code.
- **Canonical findings schema:** `findings/schemas/junit-xml.schema.json`.
- **Evidence consumer:** run validator.

### test.contract

- **Identifier:** `test.contract`
- **Description:** Run contract tests — verify an API or integration point matches its declared contract.
- **Expected inputs:** source directory path (string), contract definition path (string — e.g., Pact broker URL, OpenAPI spec, Protocol Buffers file).
- **Expected outputs:** JUnit XML test report, exit code.
- **Canonical findings schema:** `findings/schemas/junit-xml.schema.json`.
- **Evidence consumer:** run validator.

### test.e2e

- **Identifier:** `test.e2e`
- **Description:** Run end-to-end tests against a deployed environment — full user-flow validation.
- **Expected inputs:** target environment URL (string), test config path (string, optional), credentials reference (string, optional).
- **Expected outputs:** JUnit XML test report, exit code.
- **Canonical findings schema:** `findings/schemas/junit-xml.schema.json`.
- **Evidence consumer:** run validator.

---

## security

### security.sast

- **Identifier:** `security.sast`
- **Description:** Static application security testing — scan source for security vulnerabilities.
- **Expected inputs:** source directory path (string), ruleset reference (string, optional), severity threshold (enum: `low`, `medium`, `high`, `critical`, optional).
- **Expected outputs:** SARIF 2.1.0 document, exit code.
- **Canonical findings schema:** `findings/schemas/sarif-2.1.0.schema.json`.
- **Evidence consumer:** run validator; security team; compliance auditor.

### security.dast

- **Identifier:** `security.dast`
- **Description:** Dynamic application security testing — probe a running application for vulnerabilities.
- **Expected inputs:** target application URL (string), scan profile (string, optional), authentication reference (string, optional).
- **Expected outputs:** SARIF 2.1.0 document, exit code.
- **Canonical findings schema:** `findings/schemas/sarif-2.1.0.schema.json`.
- **Evidence consumer:** run validator; security team; compliance auditor.

### security.sca

- **Identifier:** `security.sca`
- **Description:** Software composition analysis — scan declared dependencies for known vulnerabilities.
- **Expected inputs:** manifest path (string — e.g., `requirements.txt`, `package.json`, `go.sum`), severity threshold (enum, optional), CVSS threshold (number, optional).
- **Expected outputs:** CycloneDX 1.6 vulnerability findings document (CVSS 3.1 scored), exit code.
- **Canonical findings schema:** `findings/schemas/cyclonedx-1.6-findings.schema.json`.
- **Evidence consumer:** run validator; security team; compliance auditor.

### security.secret-scan

- **Identifier:** `security.secret-scan`
- **Description:** Scan source for committed secrets (credentials, tokens, private keys).
- **Expected inputs:** source directory path (string), ruleset reference (string, optional), exclusion patterns (array of strings, optional).
- **Expected outputs:** SARIF 2.1.0 document, exit code.
- **Canonical findings schema:** `findings/schemas/sarif-2.1.0.schema.json`.
- **Evidence consumer:** run validator; security team; incident responders.

### security.container-scan

- **Identifier:** `security.container-scan`
- **Description:** Scan a container image for vulnerabilities in OS packages and application dependencies.
- **Expected inputs:** OCI image reference (string — digest preferred over tag), severity threshold (enum, optional), ignore list (string, optional).
- **Expected outputs:** CycloneDX 1.6 vulnerability findings document (CVSS 3.1 scored), exit code.
- **Canonical findings schema:** `findings/schemas/cyclonedx-1.6-findings.schema.json`.
- **Evidence consumer:** run validator; security team; compliance auditor.

### security.license-scan

- **Identifier:** `security.license-scan`
- **Description:** Scan dependencies for license compliance — flag licenses outside the allowlist.
- **Expected inputs:** manifest path or OCI image reference (string), license allowlist (array of SPDX identifiers).
- **Expected outputs:** CycloneDX 1.6 document with license findings (CVSS 3.1 scored where applicable — most license issues score as 0.0 but are flagged by severity class), exit code.
- **Canonical findings schema:** `findings/schemas/cyclonedx-1.6-findings.schema.json`.
- **Evidence consumer:** run validator; legal/compliance; security team.

---

## sbom

### sbom.generate

- **Identifier:** `sbom.generate`
- **Description:** Generate a software bill of materials for a source tree or container image.
- **Expected inputs:** source directory path OR OCI image reference (string), format preference (enum: `cyclonedx`, `spdx`, default `cyclonedx`).
- **Expected outputs:** CycloneDX 1.6 SBOM (primary) or SPDX 2.3 SBOM (alternative), exit code.
- **Canonical findings schema:** `findings/schemas/cyclonedx-1.6-sbom.schema.json` (primary). SPDX 2.3 accepted as alternative with separate schema.
- **Evidence consumer:** run validator; vulnerability scanner (`security.sca`, `security.container-scan`); security team; compliance auditor.

### sbom.verify

- **Identifier:** `sbom.verify`
- **Description:** Verify an SBOM's signature and structural integrity against the canonical schema.
- **Expected inputs:** SBOM document path (string), expected signer identity (string, optional).
- **Expected outputs:** verification result (pass/fail), failure reasons (array of strings if fail), exit code.
- **Canonical findings schema:** none. Evidence is pass/fail plus failure reasons. A failed verification short-circuits downstream actions.
- **Evidence consumer:** run validator; security team.

---

## sign

### sign.artifact

- **Identifier:** `sign.artifact`
- **Description:** Sign an artifact (typically an OCI image) with a Sigstore-compatible signature.
- **Expected inputs:** OCI image reference (string — digest), signing identity reference (string — key path, OIDC identity, or `ambient` for GHA).
- **Expected outputs:** signed image digest (string, unchanged — signature is attached to the registry), Sigstore bundle (JSON — `application/vnd.dev.sigstore.bundle.v0.3+json`).
- **Canonical findings schema:** `findings/schemas/oci-signing-bundle.schema.json` (OCI image digest + Sigstore bundle).
- **Evidence consumer:** run validator; signature verifier (at deploy-time admission control, at pull time).

### sign.attestation

- **Identifier:** `sign.attestation`
- **Description:** Produce a signed in-toto attestation over a predicate (e.g., conformance claim, SBOM, build provenance).
- **Expected inputs:** subject reference (string — OCI digest or content hash), predicate payload (JSON), predicate type (string — e.g., `https://aieos.dev/attestations/conformance/v1`), signing identity reference (string).
- **Expected outputs:** Sigstore bundle (JSON) wrapping an in-toto statement over the subject and predicate.
- **Canonical findings schema:** `findings/schemas/oci-signing-bundle.schema.json` (Sigstore bundle containing the attestation).
- **Evidence consumer:** run validator; signature verifier; adapter registry (for conformance attestations, per the M2 registration flow).

---

## publish

### publish.artifact

- **Identifier:** `publish.artifact`
- **Description:** Publish a built artifact to a downstream registry (OCI registry, package repository).
- **Expected inputs:** artifact reference (string — local tag or path), destination registry URL (string), destination repository path (string), credentials reference (string).
- **Expected outputs:** published artifact reference (string — e.g., `registry.example.com/org/app@sha256:…`), exit code.
- **Canonical findings schema:** none. Evidence is the published reference plus exit code.
- **Evidence consumer:** run validator; downstream `deploy.*` actions; release manager.

### publish.manifest

- **Identifier:** `publish.manifest`
- **Description:** Render and publish a deployment manifest bundle (Kustomize, Helm, raw YAML) to a manifests repository.
- **Expected inputs:** manifest source path (string — kustomization root, Helm chart, or directory), artifact reference to substitute (string), target repository reference (string), target path (string).
- **Expected outputs:** commit SHA in the manifests repository (string), manifest bundle reference (string), exit code.
- **Canonical findings schema:** none. Evidence is the commit SHA plus manifest bundle reference.
- **Evidence consumer:** run validator; GitOps reconciler (e.g., FluxCD); release manager.

---

## deploy

### deploy.environment

- **Identifier:** `deploy.environment`
- **Description:** Cause an environment to converge on a published manifest. For GitOps, this commits or promotes manifests and waits for the reconciler to acknowledge.
- **Expected inputs:** environment name (string), manifest reference (string — commit SHA, chart version, or equivalent), reconciler readiness criteria (object — e.g., Kustomization reconciled status, HealthCheck pass).
- **Expected outputs:** deployment reference (string — commit SHA that was reconciled), reconciler status (string), exit code.
- **Canonical findings schema:** none. Evidence is the reconciled commit SHA plus reconciler status. Must include reconcile-verification to satisfy the chaos-test criterion (M6.7 scenario 6).
- **Evidence consumer:** run validator; release manager; downstream `verify.*` actions.

### deploy.promote

- **Identifier:** `deploy.promote`
- **Description:** Promote a deployment from one environment to the next along the promotion graph declared in the CD spec.
- **Expected inputs:** source environment (string), target environment (string), artifact reference (string), gate approval reference (string, optional — for `manual-gate-required` edges).
- **Expected outputs:** promotion record (object — source, target, artifact, timestamp), exit code.
- **Canonical findings schema:** none. Evidence is the promotion record.
- **Evidence consumer:** run validator; release manager.

### deploy.rollback

- **Identifier:** `deploy.rollback`
- **Description:** Roll an environment back to a prior known-good artifact reference.
- **Expected inputs:** environment name (string), target artifact reference (string — prior good commit or image digest), rollback reason (string).
- **Expected outputs:** rollback record (object — environment, prior artifact, target artifact, reason, timestamp), reconciler status (string), exit code.
- **Canonical findings schema:** none. Evidence is the rollback record plus reconciler status.
- **Evidence consumer:** run validator; release manager; incident responders; postmortem authors.

---

## verify

### verify.smoke

- **Identifier:** `verify.smoke`
- **Description:** Run a minimal liveness check against a deployed environment — does the application respond at all.
- **Expected inputs:** target environment URL (string), check configuration (object — HTTP method, path, expected status).
- **Expected outputs:** pass/fail, observed response (status code, body snippet, latency ms), exit code.
- **Canonical findings schema:** none. Evidence is the observed response plus pass/fail.
- **Evidence consumer:** run validator; release manager; on-call.

### verify.health

- **Identifier:** `verify.health`
- **Description:** Run deeper health checks — application-specific readiness, dependency reachability, self-reported health endpoints.
- **Expected inputs:** target environment URL (string), health endpoint configuration (object — paths, expected status codes, expected response shape).
- **Expected outputs:** per-check pass/fail, observed responses, exit code.
- **Canonical findings schema:** none. Evidence is the per-check results.
- **Evidence consumer:** run validator; on-call; SRE.

### verify.slo

- **Identifier:** `verify.slo`
- **Description:** Verify that live service-level objectives are being met in a running environment over a measurement window.
- **Expected inputs:** target environment reference (string), SLO definitions (array of objects — metric, threshold, window), measurement window seconds (integer).
- **Expected outputs:** per-SLO pass/fail, observed values over the window, exit code.
- **Canonical findings schema:** none. Evidence is the per-SLO measurements.
- **Evidence consumer:** run validator; SRE; release manager; post-v1 bake-time promotion edges (reserved extension point in the CD spec).

---

## Summary

- 8 namespaces.
- 23 actions total.
- 13 findings-producing actions (map to 5 canonical schemas: SARIF 2.1.0, CycloneDX 1.6 findings, CycloneDX 1.6 SBOM, JUnit XML, OCI signing bundle).
- 10 non-findings actions (evidence is artifact reference, commit SHA, or pass/fail observation).

All schemas referenced above resolve to files under `findings/schemas/` after M1 Cascade Level 2 freezes.
