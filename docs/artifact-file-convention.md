# Artifact File Convention (v1.0)

The single, canonical rule for how an AIEOS artifact's physical files are
located on disk. `kit-manifest.yml` is the source of truth for *topology*
(what artifacts exist, their order, their edges); **this convention is the
source of truth for *physical file resolution*** — the two concerns FR-023
deliberately keeps separate (see the G-1/G-4 flow-definition design).

Every deriver — the harness (`_resolve_kit_files`), the dark factory, the
console (`deriveFlow`), and sherpa (advisory) — resolves files by this
convention and by nothing else. The machine-readable form lives at
[`schema/artifact-file-convention.yaml`](../schema/artifact-file-convention.yaml);
the cross-language conformance fixture generated from it is asserted by both
the Python and TypeScript test suites, so drift between derivers fails CI
instead of shipping.

## The token rule

For a manifest artifact entry, the **file token** is:

```text
token = artifacts[].spec_file  minus the trailing  "-spec.md"
```

The token is **not** derived from `artifacts[].id`. For most artifacts the
two coincide (`id: PRD` → `prd`), but nine do not, and the `spec_file` form
is authoritative (verified against all 15 kits, 2026-07-25 — 244/244 files
resolve under this rule; the id-derived rule misses 23):

| Artifact | id-derived (wrong) | actual token |
|---|---|---|
| PIK WCR | `wcr` | `work-classification` |
| PIK DI | `di` | `discovery-intake` |
| PIK PFD | `pfd` | `problem-framing` |
| PIK VH | `vh` | `value-hypothesis` |
| PIK AR | `ar` | `assumption-register` |
| PIK EL | `el` | `experiment-log` |
| PIK DPRD | `dprd` | `discovery-prd` |
| EEK KER | `ker` | `kit-entry` |
| REK RER | `rer` | `release-entry` |

## The four files

Relative to the kit repository root:

| File | Path | Required |
|---|---|---|
| spec | `docs/specs/{token}-spec.md` | always |
| template | `docs/artifacts/{token}-template.md` | always |
| prompt | `docs/prompts/{token}-prompt.md` | unless `human_authored: true` (entry gates have no prompt — manifest header, line 51) |
| validator | `docs/validators/{token}-validator.md` | **always** — a missing validator is a hard resolution error, never "no validator to run" (validators judge; skipping judgment silently is forbidden) |

## Output and identity

- Generated artifact instance: `docs/sdlc/{token}.md` under the initiative
  (the harness convention; the console's former ordered `01-prd.md` naming is
  retired — display ordinals derive from `artifact_flow` index as a
  presentation label only).
- Artifact ID: `{ID}-{INITIATIVE_SLUG}-{NNN}` where `{ID}` is the manifest
  `artifacts[].id` uppercase (harness `driver.py::_artifact_id`).

## Failure contract (R2)

A deriver that cannot resolve a required file for an artifact reachable in
`artifact_flow` MUST fail fast at load with a structured error naming the kit
abbreviation, the artifact id, and the exact expected path — e.g.
`QAK/PRD: expected docs/validators/prd-validator.md, not found`.

## Change protocol

This convention is versioned (`convention_version` in the YAML). Any change:
bump the version, regenerate the conformance fixture
(`python scripts/generate-convention-fixture.py`), and land only when every
consuming suite (gf pytest, console vitest, harness) is green against the
regenerated fixture.
