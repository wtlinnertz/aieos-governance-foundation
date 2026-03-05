# AIEOS Specification

**AIEOS** (AI-Enabled Operating System) is a governance framework for building AI-native software organizations. It defines how kits are structured, how artifacts are produced and validated, and how kits connect across layers.

This repository is the **canonical authority** for the AIEOS governance model and system standards. It is not a kit — it contains no artifact prompts, templates, or validators. It defines the rules that all kits follow.

---

## Contents

| File | Purpose |
|------|---------|
| `governance-model.md` | Complete structural rules, taxonomy, and invariants for every AIEOS kit |
| `docs/philosophy.md` | Design philosophy — the "why" behind the governance model |
| `docs/layer-model.md` | The seven-layer model and how kits map to organizational layers |
| `docs/kit-structure-standard.md` | Compliance checklist for building and auditing AIEOS-compatible kits |

---

## How Kits Relate to This Repo

Every AIEOS kit:

1. **Carries a synchronized copy** of `governance-model.md` in its own `docs/` directory. This copy exists so the kit is self-contained and usable without this repo.
2. **Treats this repo as canonical.** When the governance model changes, this repo is updated first. Kits are updated to match. Kits do not update governance-model.md independently.
3. **References this repo** in their CLAUDE.md to declare the authority source.

This means a kit copy of governance-model.md is always correct or behind — never ahead.

---

## Governance Model Version

Current: `1.0`

Changes to the governance model follow the protocol in `governance-model.md` §15.

---

## Kit Registry

| Layer | Repository | Status |
|-------|-----------|--------|
| 2. Product Intelligence | `aieos-product-intelligence-kit` | Built |
| 4. Engineering Execution | `aieos-engineering-execution-kit` | Built |
| 5. Release & Exposure | `aieos-release-exposure-kit` | Built |
| 6. Reliability & Resilience | `aieos-reliability-resilience-kit` | Built |

Additional kits will be registered here as they are built.
