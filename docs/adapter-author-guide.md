# Adapter-Author Guide

Audience: engineers adding a new AIEOS capability adapter or a new
version of an existing one.

An adapter is a small Python package that wraps an external tool
(`pytest`, `cosign`, `syft`, etc.), normalizes the tool's output to the
canonical findings schema declared in the capability contract, and
produces a signed conformance attestation on pass. This guide walks you
from "I want to add an adapter" to "it's registered with the harness and
pipelines can resolve to it."

The worked example throughout is
[`adapter-pytest-unit`](https://github.com/wtlinnertz/adapter-pytest-unit)
for the `test.unit` contract.

---

## Before you start

You need:

- A claim on exactly one capability contract (two if you're building a
  multi-capability adapter; the cosign adapter is the v1 example).
- The frozen taxonomy, contracts, and findings schemas from
  `aieos-governance-foundation` at their `v1.0-*` tags.
- Python 3.11+ locally. The tool you're wrapping installed on your dev
  machine (or available in your CI runner).

---

## 1. claim a contract

Pick the action you're satisfying from `taxonomy/actions-v1.md`. Read
the contract at `contracts/<namespace>.<action>.contract.yaml`. The
contract tells you:

- `required_inputs` — the structured object your adapter's `execute` method
  receives
- `output_schema` — the canonical findings schema your adapter emits (or
  `null` for evidence-only actions)
- `required_evidence` — the artifact types your adapter must produce
- `conformance_suite` — the suite identifier that tests your adapter

Your adapter must honor all four. The conformance harness refuses to sign
an attestation if any contract clause fails.

Multi-capability adapters claim two contracts in one package but register
twice with separate attestations. `adapter-cosign-sign` is the reference:
`SignArtifactAdapter` and `SignAttestationAdapter` in one package.

---

## 2. scaffold the repo

Repo name convention: `adapter-<tool>-<action>` (examples:
`adapter-pytest-unit`, `adapter-cosign-sign`). Under your GitHub user or
org:

```bash
gh repo create <owner>/adapter-<tool>-<action> --public --clone
cd adapter-<tool>-<action>
```

Files the harness expects:

- `pyproject.toml` — package metadata plus dev deps (`ruff`, `pytest`).
  No runtime deps on the harness itself; the adapter is invoked via its
  `execute` method.
- `src/aieos_adapter_<tool>_<action>/__init__.py` — your adapter class.
- `tests/test_adapter.py` — unit tests independent of conformance.
- `MAPPING.md` — documents every normalization decision you make.
- `CLAUDE.md` — the adapter template from `aieos-governance-foundation`'s
  `~/second-brain/AIEOS CI-CD Implementation - Repo CLAUDE Files.md` has
  a template block you can copy with the placeholders filled in.
- `README.md` + `LICENSE`.
- `.github/workflows/ci.yml` — runs ruff and pytest on every push.

---

## 3. implement the adapter class

The harness calls `adapter.execute(inputs)` and expects an
`AdapterResult` back. A working skeleton:

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class AdapterResult:
    findings: dict[str, Any] | None
    evidence: list[str]
    exit_code: int


class MyToolAdapter:
    def __init__(self, tool_binary: str = "mytool") -> None:
        self._tool = tool_binary

    def execute(self, inputs: dict[str, Any]) -> AdapterResult:
        # 1. validate inputs (required fields present, paths exist)
        # 2. invoke the tool via subprocess
        # 3. capture output, normalize to the canonical findings schema
        # 4. compile an evidence list matching required_evidence
        # 5. pick an exit code per the adapter exit-code convention
        ...
```

### Exit-code convention

The ten v1 adapters follow the same convention. Match it.

- `0` on well-formed output, even if the tool found issues. Outcomes
  (failed tests, high-severity CVEs) belong in findings, not in the exit
  code. The run validator evaluates those against the spec's criteria.
- `2` when a required input is missing or invalid.
- `3` when the tool ran but produced unusable output (empty stdout, zero
  exit code without the expected artifact).
- `127` when the tool binary isn't on `$PATH`.
- Otherwise, preserve the tool's native exit code.

### Findings normalization

Your output_schema declares the exact shape. For SARIF-typed adapters,
AIEOS requires `tool.driver.version` and per-result `level` even when
the upstream tool omits them; fill in conservative defaults. For
CycloneDX-findings adapters, map tool-specific severity strings to the
AIEOS vocabulary (`none`, `info`, `low`, `medium`, `high`, `critical`)
using standard thresholds. Document every mapping in `MAPPING.md`.

### Evidence emission

Each `required_evidence` entry from the contract needs a corresponding
string in your result's `evidence` list. Use scheme-prefixed references:

- `junit-report:<filename>` — test results
- `sarif-report:<filename>` — scan results
- `oci-image-digest:sha256:<hex>` — build output
- `sigstore-bundle:inline` — signature metadata
- `http-status:200` — probe observation
- `exit-code:<N>` — always include

Downstream consumers dispatch on the prefix, so stick to lowercase
kebab-case identifiers.

---

## 4. write unit tests

Tests go in `tests/` and should cover:

- Happy path: valid input produces findings validating against the
  canonical schema
- Each error path: missing input, tool missing, malformed output,
  tool-exit non-zero
- Determinism: same input produces the same findings (tolerating
  timestamps and paths that differ between runs)

If the tool isn't installable on every CI runner (buildah, for example),
mock `subprocess.run`. If it is (pytest, git), drive a real temp instance
and test end to end. `adapter-flux-handoff` uses a real temp git repo;
`adapter-buildah-image` mocks the subprocess.

Run the tests locally:

```bash
pip install -e '.[dev]'
pytest
ruff check .
ruff format --check .
```

Everything green before conformance.

---

## 5. run the conformance harness

The harness lives in `aieos-governance-foundation/conformance/harness/`.
It reads the conformance suite for your contract, runs your adapter
against its fixtures, evaluates each criterion (schema conformance,
structural match, exit code, evidence presence), and returns a
conformance-attestation payload on pass.

Run it from the governance-foundation checkout:

```bash
cd aieos-governance-foundation
python3 <<EOF
from pathlib import Path
from conformance.harness.runner import load_suite, run_conformance
from aieos_adapter_<tool>_<action> import <YourAdapter>

suite = load_suite(Path("conformance/<namespace>.<action>-suite"))
result = run_conformance(
    suite=suite,
    adapter=<YourAdapter>(),
    adapter_id="adapter-<tool>-<action>",
    adapter_version="1.0.0",
    signing_identity="<ci-workflow-identity>",
)
print("PASS" if result.passed else "FAIL")
print(result.attestation or result.diagnostic)
EOF
```

On pass: the printed attestation payload validates against
`schema/conformance-attestation.schema.json`. Adapter CI signs that payload
via `cosign sign-blob --bundle` and publishes the resulting Sigstore bundle.

On fail: the diagnostic names every failed criterion. Fix and re-run.

If the suite for your contract doesn't exist yet, author it (fixtures,
expected findings, criteria.yaml, placeholder run.sh) following the
pattern in `conformance/test.unit-suite/`. The `test.integration-suite`
authored in M4a.2 is a good second reference.

---

## 6. wire CI to produce signed attestations

Your `.github/workflows/ci.yml` should, on top of lint + test:

1. Check out the adapter repo and `aieos-governance-foundation` for the
   conformance harness.
2. Run the conformance harness and capture the attestation payload.
3. Sign the payload with cosign's keyless OIDC flow.
4. Upload the signed bundle as a release artifact.

A minimal job skeleton:

```yaml
- uses: actions/checkout@<pinned-sha>
- uses: actions/checkout@<pinned-sha>
  with: { repository: wtlinnertz/aieos-governance-foundation, path: gf }
- uses: actions/setup-python@<pinned-sha>
  with: { python-version: "3.11" }
- uses: sigstore/cosign-installer@<pinned-sha>
  with: { cosign-release: "v3.0.6" }
- run: pip install -e '.[dev]' && pytest
- run: python3 path/to/run_conformance.py > attestation.json
- run: cosign sign-blob --bundle attestation.sigstore.json --yes attestation.json
- uses: actions/upload-artifact@<pinned-sha>
  with: { name: conformance-attestation, path: "attestation.*" }
```

Pin every action to a commit SHA per repo convention.

---

## 7. submit for registration

Once your CI publishes a signed attestation:

1. Open an issue on `aieos-agent-harness` titled "register
   adapter-<tool>-<action> v1.0.0" with a link to the signed attestation
   bundle and the adapter's release.
2. An operator pulls the attestation, verifies it against
   `schema/conformance-attestation.schema.json`, and calls the harness
   `register_adapter` API.
3. The harness registry persists the entry. Downstream spec resolvers
   can now bind to your adapter.

Registration is a governance checkpoint, not a self-service API. The
harness refuses registrations without a valid attestation signed by a
trusted identity — there is no override.

---

## Contract-version cutovers

When a contract you claim advances (say, `test.unit@1.1.0`), your existing
registration stays valid until the cutover date announced in the
governance-foundation changelog. To keep registering past cutover, re-run
conformance against the new contract version, produce a fresh
attestation, and re-register.

The grace logic is in `aieos-agent-harness/src/cicd/attestation.py`
(`ContractRegistration.is_version_acceptable`) — before cutover, both
versions register; at or after cutover, only the new one does.

---

## Multi-capability adapters

`adapter-cosign-sign` is the v1 reference. Key rules:

- Two classes in one package, one per contract.
- Each class has its own `execute` method and its own conformance run.
- Two separate attestations, one per contract.
- Two separate registrations in the harness, each with the attestation
  for that contract.

Do not merge multi-capability claims into a single attestation — the
registry's attestation verifier inspects
`predicate.contract_id` and refuses entries whose claimed capabilities
don't match.

---

## Common pitfalls

- **Silent fallbacks.** Adapters must not guess. If a required input is
  missing or the tool's output is unparseable, return a non-zero exit
  code with diagnostic evidence. The run validator relies on adapters
  being honest about failure.
- **Severity mapping drift.** Different tools use different severity
  scales. Document yours in `MAPPING.md` and keep it consistent with the
  AIEOS vocabulary. When in doubt, map conservatively upward (flag more,
  not less).
- **Determinism regressions.** Unit tests that pass today may fail next
  week when the tool's output format shifts. Pin your tool's version in
  the adapter's `Containerfile` or CI setup.
- **Attestation identity.** The `signing_identity` in your attestation
  must match the identity the harness trusts. CI's ambient OIDC is the
  v1 path; local keypairs are for dry runs only.
