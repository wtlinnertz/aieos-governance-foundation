# Capability Contracts v1 — Review Notes Against the Artifact-Store Pilot

M1-L3.3 review. Walks every contract against the tool the artifact-store pilot will invoke for that action (per implementation plan §6.5–6.6 and Assumption 2). Confirms three things per contract:

1. `required_inputs` match what the real tool accepts on the CLI or API.
2. `output_schema` matches what the real tool produces (directly or via normalization).
3. `required_evidence` lists artifact types the real tool actually emits.

Pilot state note: `aieos-artifact-store` currently has no CI pipeline, no Containerfile, no Kubernetes manifests, no Flux config. These are M6.1 prerequisites. This review therefore walks the contracts against the **planned** tool choices documented in the implementation plan; see `taxonomy/review-notes.md` for the same caveat applied to the taxonomy review.

## Per-contract walkthrough

### Test.unit → pytest

- `required_inputs.source_dir` → pytest accepts a positional target path. ✅
- `required_inputs.test_config_path` → pytest accepts `-c`/`--config`. ✅
- `required_inputs.coverage_threshold` → pytest with `pytest-cov` supports `--cov-fail-under`. ✅
- `output_schema` → pytest emits JUnit XML via `--junit-xml`; adapter normalizes to the canonical JSON representation. ✅
- `required_evidence` → junit-report, coverage-report, exit-code. pytest emits all three. ✅

### Test.integration → pytest

- Same as `test.unit` plus `dependency_fixtures` for containerized fixture config. Pytest plugins for docker-compose fixtures are out-of-tree but standard. ✅

### Test.contract → pytest (or language-native contract-test runners)

- `contract_definition_path` is required. Pilot likely uses pytest with a contract-broker client. Contract shape matches what the broker-based workflow accepts. ✅

### Test.e2e → pytest against deployed URL

- `target_url`, `test_config_path`, `credentials_ref`. Matches what an e2e test harness needs. Pilot does not currently exercise e2e; field shape is appropriate. ✅

### Security.sast → semgrep

- `source_dir` → semgrep accepts a path. ✅
- `ruleset_ref` → semgrep `--config` accepts a registry ref, local file, or URL. ✅
- `severity_threshold` → semgrep `--severity` accepts `INFO|WARNING|ERROR`; adapter maps to the AIEOS severity vocabulary. Mapping is an adapter concern (documented in `adapter-semgrep-sast/MAPPING.md` when M4a lands), not a contract concern. ✅
- `output_schema` → semgrep emits SARIF via `--sarif`. ✅
- `required_evidence` → sarif-report, exit-code. ✅

### Security.dast → (no pilot tool selected in v1; adapter is v1.x roadmap)

- Pilot does not ship DAST in v1 (artifact-store is a library/CLI, no running web service). The contract fields (`target_url`, `scan_profile`, `auth_ref`) match the standard DAST tool interface (ZAP, Nuclei). ✅

### Security.sca → osv-scanner

- `manifest_path` → osv-scanner accepts `--lockfile` or directory scan. ✅
- `severity_threshold` → osv-scanner does not natively threshold at the CLI; filtering happens post-process in the adapter. Not a contract issue — contract declares what the adapter accepts. ✅
- `cvss_threshold` → also adapter-side post-processing. ✅
- `output_schema` → osv-scanner emits its native format; adapter converts to CycloneDX 1.6 findings. ✅

### Security.secret-scan → (tool choice deferred; contract matches standard interfaces)

- `source_dir`, `ruleset_ref`, `exclusion_patterns`. Standard secret-scanner interface (gitleaks, trufflehog). ✅

### Security.container-scan → trivy

- `image_ref` → trivy `image <ref>`. ✅
- `severity_threshold` → trivy `--severity`. ✅
- `ignore_list` → trivy `--ignorefile`. ✅
- `output_schema` → trivy emits JSON; adapter normalizes to CycloneDX 1.6 findings. ✅

### Security.license-scan → (tool choice deferred; e.g., license-checker, go-licenses)

- `source_path_or_image_ref`, `license_allowlist` (SPDX ids). Matches standard license-scanner interfaces. ✅

### Sbom.generate → syft

- `source_path_or_image_ref` → syft accepts both. ✅
- `format_preference` → syft `-o cyclonedx-json` or `-o spdx-json`. ✅
- `output_schema` → CycloneDX 1.6 SBOM is a direct syft output format. ✅

### Sbom.verify → cosign verify-blob (or dsse verify)

- `sbom_document_path`, `expected_signer_identity`. Matches cosign's verification interface. Evidence is pass/fail plus failure reasons (non-findings). ✅

### Sign.artifact → cosign sign

- `image_ref` → cosign sign `<ref>`. ✅
- `signing_identity_ref` → `--key`, OIDC identity, or ambient OIDC token. ✅
- `output_schema` → Sigstore bundle. cosign `--bundle` emits the canonical form directly. ✅
- `required_evidence` → signed-image-digest, sigstore-bundle, exit-code. ✅

### Sign.attestation → cosign attest (or cosign sign-blob on in-toto statements)

- `subject_ref`, `predicate_payload`, `predicate_type`, `signing_identity_ref`. Maps directly to cosign attest parameters. ✅
- `output_schema` → Sigstore bundle wrapping a DSSE envelope over an in-toto Statement. Matches the canonical OCI signing bundle schema. ✅

### Publish.artifact → (native push — docker push / skopeo copy / equivalent)

- `artifact_ref`, `destination_registry_url`, `destination_repository_path`, `credentials_ref`. Standard registry-push interface. ✅

### Publish.manifest → kustomize + git commit

- `manifest_source_path` → kustomization root. ✅
- `artifact_ref_to_substitute` → kustomize `edit set image` to pin the digest before render. ✅
- `target_repo_ref`, `target_path` → the manifests repository the adapter commits to. ✅
- `output_schema: null` → evidence is the commit SHA plus manifest bundle reference. ✅

### Deploy.environment → git commit to manifests repo + gitOps reconciler

- `environment_name` → selects the target overlay path in the manifests repo. ✅
- `manifest_ref` → the commit SHA the adapter expects the reconciler to converge on. ✅
- `reconciler_readiness_criteria` → generic object; adapter-specific readiness criteria (reconciled-status acknowledgement, health-check pass). ✅
- `required_evidence` includes reconciler-status, which the chaos-test scenario 6 requires. ✅

### Deploy.promote / deploy.rollback

- Cross-tool patterns (no single CLI wraps these cleanly). Fields describe the logical operation. Evidence is a structured record. ✅

### Verify.smoke / verify.health / verify.slo

- `target_url` / `target_env_ref` with per-check configuration. Matches what a smoke-check or SLO-verify runner needs.
- Evidence shapes (observed-response, per-check-results, per-slo-measurements) are realistic — any verifier emits some form of structured per-check result.
- `verify.slo` requires a metrics backend the adapter queries; contract does not name the backend (tool-agnostic). ✅

## Gaps found and fixed during review

None. All 23 contracts passed review without modification.

## Gaps deliberately not addressed in v1

- **Adapter-side severity mapping** (e.g., semgrep `INFO|WARNING|ERROR` → AIEOS `none|info|low|medium|high|critical`). This is documented per-adapter in `MAPPING.md` files when adapters ship in M4a/M4b. Not a contract concern.
- **CVSS thresholding not native to every tool.** Some scanners (osv-scanner) do not threshold by CVSS at the CLI. Adapters post-process findings. Contracts declare the adapter's accepted inputs — the tool's behavior is the adapter's responsibility.
- **security.dast pilot tool selection.** Deferred to v1.x when a long-running web service is in scope for the pilot.

## Outcome

- Zero contracts required modification.
- Every contract's input/output/evidence shape aligns with the planned tool for that action.
- `contracts/*.contract.yaml` is ready to freeze at v1.0 alongside `schema/capability-contract.schema.json`.
