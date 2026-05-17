# Spec-Authoring Guide

Audience: developers adopting AIEOS spec-driven CI/CD on their own service.

This guide walks you from "I have a Python service on Kubernetes" to "my
pipeline runs on every PR and deploys via Flux, validated end to end." It
reads front to back; you can skip the CD section if your service only has
CI for now.

The worked example throughout is `aieos-artifact-store`, the v1 pilot.
Its frozen artifacts live at
[`aieos-artifact-store/.aieos/`](https://github.com/wtlinnertz/aieos-artifact-store/tree/main/.aieos).

---

## Before you start

You need three things locally:

1. **A target repo** containing your service code, containerized (has a
   `Containerfile` or `Dockerfile`) with Kubernetes manifests under
   `kustomize/` and Flux resources under `flux/`. If any are missing, the
   pilot's setup (M6.1–6.3 in the implementation plan) is a template.
2. **The AIEOS pipeline runner** installed:
   ```bash
   pip install git+https://github.com/wtlinnertz/aieos-pipeline-runner.git
   ```
3. **The two kits' templates** available as reference:
   - CI: `aieos-engineering-execution/templates/ci-spec/python-k8s-flux.yaml`
   - CD: `aieos-release-exposure-kit/templates/cd-spec/python-k8s-flux.yaml`

Copy the CI template into your repo at `.aieos/ci.spec.yaml` and the CD
template at `.aieos/cd.spec.yaml`. Open both in your editor.

---

## Authoring the CI spec

### 1. code repo reference

Set `code_repo` to your `<owner>/<repo>` slug. The pipeline runner uses
this string in logs, not for cloning.

### 2. pick your actions

The template lists eleven actions — the ten v1 adapters plus
`security.secret-scan`. Keep every action that applies to your service;
delete the ones that don't. Don't add actions outside the frozen
taxonomy (`aieos-governance-foundation/taxonomy/actions-v1.md` lists all
23 v1 actions).

Every action has a `criteria` object. Leave it `{}` if the default for that
action is enough. Override when you want tighter thresholds.

Common overrides:

| Action | Common override |
|---|---|
| `test.unit` | `min_coverage` (default 80 in the template; lower if you're below and tracking) |
| `security.sast` | `max_severity` (default high; drop to medium for stricter) |
| `security.sca` | `max_cvss` (default 7.0) alongside `max_severity` for layered gating |
| `security.container-scan` | `ignore_list` path if you have tolerated CVEs |
| `security.secret-scan` | `expect_zero_findings: true` is strict; switch to severity gating if you have allowlisted test fixtures |

### 3. review the dependency graph

The template's `depends_on` graph is correct for most Python-K8s-Flux
services:

```
test.unit        test.integration    security.sast    security.sca    security.secret-scan
       \________/                             \______|______/
              \                                      |
          build.artifact  <--- depends on tests
              |
        +-----+-----+
        |           |
   sbom.generate    security.container-scan
        |           |
        +-----+-----+
              |
         sign.artifact  <--- gates on everything above
              |
      sign.attestation
              |
       publish.artifact
```

The spec validator refuses cycles and dangling references, so a mistake
shows up in the report, not at runtime.

### 4. pick adapter preferences

Under `policies.adapter_preferences`, map each action to an adapter. The
v1 catalog:

- `test.unit` → `adapter-pytest-unit`
- `test.integration` → `adapter-pytest-integration`
- `build.artifact` → `adapter-buildah-image`
- `security.sast` + `security.secret-scan` → `adapter-semgrep-sast`
- `security.sca` → `adapter-osv-sca`
- `security.container-scan` → `adapter-trivy-container`
- `sbom.generate` → `adapter-syft-sbom`
- `sign.artifact` + `sign.attestation` → `adapter-cosign-sign`
- `publish.artifact` → your org's published-artifact adapter

The resolver refuses ambiguous bindings, so if two adapters claim the
same action in your harness registry you have to pick one explicitly.

### 5. validate locally

```bash
# Compute the sha256 hash the runner will expect
SHA=$(python3 -c "import hashlib; print(hashlib.sha256(open('.aieos/ci.spec.yaml','rb').read()).hexdigest())")

# Dry-run against mock adapters
aieos-pipeline-runner run \
  --spec .aieos/ci.spec.yaml \
  --expected-hash "$SHA" \
  --use-mock-adapters \
  --run-id dryrun-local
```

You should see five event types on stdout (`run.start`, `task.start`,
`task.evidence`, `task.result`, `run.end`) and a report on stderr ending
in `"result": "PASS"`. If it FAILs, the check-level diagnostic in the
report names the failing criterion.

### 6. freeze

Commit `.aieos/ci.spec.yaml`. The commit SHA plus the content hash are
the spec's identity — the runner refuses any spec whose hash doesn't
match what the CI workflow supplies, so a mid-run mutation cannot slip
through.

---

## Authoring the CD spec

CD is heavier than CI because the environment graph is service-specific.
The template assumes three environments (`dev` → `staging` → `prod`) with
auto-promote `dev → staging` and a manual gate before `prod`. Start there
and adjust.

### 1. artifact ref

`artifact_ref` must be a full OCI digest from your CI pipeline's
`publish.artifact` evidence. Tag-only refs are refused. The CD authoring
flow re-freezes the spec with the real digest after each CI run produces
one; until then, use a placeholder.

### 2. environment graph

Each environment has a `name`, a `lifetime` (leave as `persistent` in
v1), and an `actions` array. Every environment needs at least
`deploy.environment`; production typically adds `verify.smoke`,
`verify.health`, and `verify.slo` with a dependency on
`deploy.environment`.

### 3. promotion edges

Edges go in the `promotions` array with a `type`:

- `auto-promote` — runs when the source env's verify.* actions pass
- `promote` — manual trigger, no human approval required
- `manual-gate-required` — human approval required before the runner
  executes the promotion

The reserved extension fields (`bake_duration`, `verification_interval`,
`rollback_on_degradation`) are present in the schema but unused in v1.
Leave them `null` or omit them.

### 4. rollback conditions

The template triggers `deploy.rollback` on any `verify.*` FAIL. Tune if
you want finer-grained rules (for example, rollback only on `verify.slo`
but not on `verify.smoke`).

### 5. validate

Same flow as CI:

```bash
SHA=$(python3 -c "import hashlib; print(hashlib.sha256(open('.aieos/cd.spec.yaml','rb').read()).hexdigest())")
aieos-pipeline-runner run --spec .aieos/cd.spec.yaml --expected-hash "$SHA" --use-mock-adapters
```

Also run the cross-spec integrity check against your CI spec:

```bash
python3 aieos-governance-foundation/scripts/validate-spec-integrity.py
```

This confirms the CI spec's published artifact reference is compatible
with the CD spec's `artifact_ref`.

---

## CI pipeline wiring

Add a GitHub Actions workflow at
`.github/workflows/aieos-ci.yml`. The pilot's version is the reference:

```yaml
name: aieos-ci
on: { push: { branches: [main] }, pull_request: { branches: [main] } }
permissions: { contents: read, id-token: write }
jobs:
  spec-driven-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<pinned-sha>
      - uses: actions/setup-python@<pinned-sha>
        with: { python-version: "3.11" }
      - run: pip install git+https://github.com/wtlinnertz/aieos-pipeline-runner.git@main
      - id: spec
        run: echo "sha=$(python -c 'import hashlib,pathlib; print(hashlib.sha256(pathlib.Path(".aieos/ci.spec.yaml").read_bytes()).hexdigest())')" >> $GITHUB_OUTPUT
      - run: aieos-pipeline-runner run --spec .aieos/ci.spec.yaml --expected-hash "${{ steps.spec.outputs.sha }}" --use-mock-adapters --run-id "run-${{ github.run_id }}"
```

Pin every action to a commit SHA, not a tag. The pilot uses
`actions/checkout@de0fac2e...` and `actions/setup-python@a309ff8b...` for
reference.

---

## Worked example: aieos-artifact-store

The pilot's frozen specs and GHA workflow are the canonical reference.
Read them through once before authoring your own:

- `.aieos/ci.spec.yaml` — 11 actions with realistic defaults
- `.aieos/cd.spec.yaml` — three-environment graph with manual gate to prod
- `.aieos/chaos-tests.sh` — four failure-mode regressions you can copy
  and adapt
- `.github/workflows/aieos-ci.yml` — CI workflow structure

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Exit 2, "spec ingestion failed" | Hash mismatch or unfrozen spec | Recompute `--expected-hash` after any edit |
| Exit 1, "action X not in taxonomy" | Typo or non-v1 action | Use an action from `taxonomy/actions-v1.md` |
| Exit 1, "dag_valid: cycle" | Cyclic `depends_on` | Walk the graph; remove the cycle |
| Exit 1, "no registered evaluator" | Custom criterion key | The run validator ships with a fixed set of evaluators; extend in code or use a supported criterion |
| Exit 2, "non-mock adapter wiring is deferred" | Ran without `--use-mock-adapters` | Add the flag (v1 path); real adapters require registry setup |

For anything else, open an issue on
[aieos-pipeline-runner](https://github.com/wtlinnertz/aieos-pipeline-runner)
with the failing spec and the runner's report output.
