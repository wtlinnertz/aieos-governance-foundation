# Taxonomy v1 — Review Notes Against the Artifact-Store Pilot

M1-L1.2 review. Walks the taxonomy against `aieos-artifact-store`'s current state and its planned post-M6.1 pipeline (per implementation plan §6.1–6.6).

## Pilot state at time of review

Current state of `aieos-artifact-store` (2026-04-17):

- Python library/CLI project. `src/` with chunker, config, embeddings, ingest, metadata, query modules. `tests/` with pytest tests.
- Dependencies: lancedb, sentence-transformers, pyarrow, pandas, pytest.
- No `Containerfile` or `Dockerfile`.
- No `kustomize/` or `k8s/` manifests.
- No Flux deployment config.
- No `.github/workflows/` CI config.

Assumption 10 of the implementation plan explicitly lists these as prerequisites for M6.1 ("containerize the service and add Flux deployment if not already in place"). They are not present today. The taxonomy review therefore addresses the **planned** pipeline, not the current empty one.

## Planned pipeline (per plan §6.5–6.6)

CI (§6.5):
- pytest unit + integration tests.
- buildah container image build.
- semgrep SAST scan.
- osv-scanner SCA scan.
- trivy container scan.
- syft SBOM generation.
- cosign artifact sign.

CD (§6.6):
- Kustomize manifest render.
- Manifest commit to the manifests repository.
- Flux reconcile on the deployed cluster.
- verify.smoke and verify.health against the reconciled environment.

## Coverage walk — pilot step → taxonomy action

| Pilot step | Taxonomy action | Fit |
|---|---|---|
| pytest unit | `test.unit` | clean |
| pytest integration | `test.integration` | clean |
| buildah image | `build.artifact` | clean — evidence is OCI digest |
| semgrep | `security.sast` | clean — SARIF 2.1.0 |
| osv-scanner | `security.sca` | clean — CycloneDX 1.6 findings |
| trivy | `security.container-scan` | clean — CycloneDX 1.6 findings |
| syft | `sbom.generate` | clean — CycloneDX 1.6 SBOM |
| cosign sign | `sign.artifact` + `sign.attestation` | clean — multi-capability; adapter registers twice |
| Kustomize → manifest commit | `publish.manifest` | clean — evidence is commit SHA in manifests repo |
| Flux reconcile | `deploy.environment` | clean — evidence is reconciled commit SHA plus reconciler status |
| smoke check | `verify.smoke` | clean |
| health check | `verify.health` | clean |

No pilot step lacks a taxonomy action. No taxonomy action's shape had to be adjusted to fit the pilot.

## Actions the pilot does not exercise in v1

Kept in the taxonomy. The taxonomy serves all AIEOS-adopted projects, not just the pilot.

- `test.contract` — artifact-store has a clear API boundary (query, ingest) but no contract tests today. Plausible post-v1.
- `test.e2e` — no deployed HTTP service surface in v1; the pilot exercises its pipeline through CLI invocation and pytest. Other archetypes will need this.
- `security.dast` — library/CLI profile; no long-running service surface to probe. DAST applies to web-service archetypes.
- `security.secret-scan` — not called out in §6.5 but a reasonable default for any repo. Will likely land in the CI spec template for the pilot even if not enumerated in the plan.
- `security.license-scan` — valuable for governance tooling; not in §6.5. Will not block v1.
- `sbom.verify` — pilot produces SBOMs via `sbom.generate`; it doesn't consume and verify SBOMs produced by others. Consumer-side action; other archetypes will exercise it.
- `deploy.promote` — the plan's example CD spec models a dev → staging → prod graph with a manual gate at staging. Pilot will exercise this in M6.
- `deploy.rollback` — pilot's `rollback_conditions` in the CD spec will wire this up (plan §6.7 chaos test 6 stresses reconcile failures).
- `verify.slo` — pilot uses this in prod per §6.6.

## Gaps — does the pilot need anything the taxonomy lacks?

None identified.

Specifically reviewed:

- **SBOM attestation.** Pilot signs the artifact (`sign.artifact`) and produces a conformance attestation (`sign.attestation`). Signing the SBOM itself is an instance of `sign.attestation` with a different predicate type, not a separate action. No new action needed.
- **Image promotion between registries.** The plan's pilot publishes once and deploys via Flux; registry-to-registry promotion is a `publish.artifact` instance with source/destination inputs, already covered.
- **Database migrations.** Not applicable to `aieos-artifact-store` (LanceDB is file-based and migrations are handled in-app). Other archetypes may want a `deploy.migrate` action; deferred to v2.
- **Policy checks / OPA / conftest.** Not in v1 plan. Belongs in a v2 `policy` namespace.

## Field-level observations

- `deploy.environment` explicitly notes that evidence must include reconcile-verification. This aligns with M6.7 chaos-test scenario 6 (Flux-refused reconcile must surface as a run-validator failure). Keep the current wording.
- `sign.attestation`'s evidence-consumer list includes "adapter registry" — that is the correct target for conformance attestations produced by M4 adapter CI pipelines, and the pilot's adapters will use exactly this path.
- `security.license-scan` output is typed as CycloneDX 1.6 findings with a note that most license issues score 0.0 under CVSS. That framing is deliberate — it lets `security.license-scan` share the findings schema with CVE-scored SCA findings without forcing a false vulnerability severity.

## Outcome

- No additions to the taxonomy.
- No removals.
- No field changes.
- `taxonomy/actions-v1.md` is ready to freeze at v1.0 once cascade levels 2 and beyond are staged to start.

## Flagged for downstream work

- The artifact-store containerization, Kustomize, and Flux config must land before M6.1 (captured in the plan). The taxonomy does not block this.
- `security.secret-scan` should be included in the pilot's CI spec template when M5 arrives even though it isn't enumerated in §6.5; it's low-cost insurance for a public repo and matches an existing taxonomy action.
