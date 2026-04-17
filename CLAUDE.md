# Spec-Driven CI/CD — Governance Foundation Context

This repo is the canonical authority for structural rules, policy, and the layer model.
For spec-driven CI/CD, it owns the frozen vocabulary that everything downstream depends on.

## What lives here for CI/CD

- `taxonomy/actions-v1.md` — action taxonomy (8 namespaces, ~22 actions)
- `schema/capability-contract.schema.json` — meta-schema for capability contracts
- `schema/ci-spec.schema.json` — CI spec schema
- `schema/cd-spec.schema.json` — CD spec schema
- `contracts/<namespace>.<action>.contract.yaml` — one contract per action
- `findings/findings-schemas.md` — action-to-schema mapping
- `findings/schemas/` — JSON schema files for canonical findings formats
- `conformance/` — conformance test-suite framework and skeleton suites
- `runner-interface.md` — pipeline runner public contract (frozen end of M3)

## Implementation plan

The full plan with milestones, assumptions, and acceptance criteria is at:
`~/second-brain/AIEOS Spec-Driven CI-CD Implementation Plan.md`

Read it before starting any task. The M1 cascade-freeze checklist in that file
defines the exact task order and acceptance criteria for this repo's work.

## Conventions

- Every frozen artifact gets a v1.0 git tag when it freezes.
- Cascade-freeze order: taxonomy -> findings schemas -> contracts -> spec schemas -> conformance attestation schema -> conformance framework.
- Downstream tasks can start once their upstream dependency freezes, not when the full milestone closes.
- JSON schemas must be valid JSON Schema Draft 2020-12.
- Contract YAML files validate against `capability-contract.schema.json`.
- Pin upstream schema versions (SARIF 2.1.0, CycloneDX 1.6, SPDX 2.3, JUnit XML). Never reference "latest."
- Do not add namespaces, actions, or schema fields beyond what the plan specifies without explicit approval.

## Three invariants (never violate)

1. Separation of concerns — rules, structure, generation behavior, and judgment are separate files.
2. Freeze-before-promote — nothing moves downstream until it's frozen and tagged.
3. Validators judge, they don't help — validators return PASS/FAIL with evidence, never suggestions.

## Python conventions (for any tooling scripts in this repo)

- Type hints on public functions.
- `ruff` for linting. `mypy` if config exists.
- `set -euo pipefail` on any shell scripts.
- Tests in AAA shape. One behavior per test.
