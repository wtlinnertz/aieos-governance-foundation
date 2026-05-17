# CONTRIBUTING

Thank you for your interest in contributing to **AIEOS Governance Foundation**.

This repository is the **canonical authority** for the AIEOS governance model and system standards. It defines the rules that all kits follow. Contributions here have system-wide impact — all kit copies of `governance-model.md` must stay in sync with this repo.

---

## Guiding principles

All contributions must uphold these principles:

- **Governance is the source of truth** — kits reference this repo, not vice versa
- **Kit-agnostic standards** — no kit-specific logic belongs here
- **Backwards compatibility by default** — governance changes cascade to all kits
- **Anonymization is mandatory** — no employer, team, or internal system names

If a contribution weakens these principles, it will not be accepted.

---

## What you can contribute

### Governance model (`governance-model.md`)
- Clarifications that resolve genuine ambiguity
- New invariants addressing gaps in the current model
- Corrections to stated rules that conflict with actual kit behavior

All governance model changes require a version bump and changelog entry per §15.

### Foundation guides
- Improvements to `docs/getting-started.md`, `docs/initiative-presets.md`, `docs/initiative-state-view.md`
- Corrections to layer descriptions or kit registry entries in `docs/layer-model.md`
- Clarifications to `docs/philosophy.md` or `docs/kit-structure-standard.md`

### Layer model
- Updates to kit registry status (Planned → Built)
- Corrections to inter-layer handoff descriptions
- New layer documentation when layers are added

---

## What you should NOT contribute

The following will be rejected:

- Kit-specific rules or artifact definitions (those belong in individual kit repos)
- Tool-specific implementations
- Large structural rewrites without prior discussion
- Content that makes this repo dependent on any individual kit

---

## Anonymization requirements (MANDATORY)

All contributions must comply with **`ANONYMIZATION.md`**.

Before submitting a PR, confirm:
- No company names or internal acronyms appear
- No internal URLs, domains, or identifiers appear
- All examples use approved placeholders
- No screenshots or logs expose identifiers

Violations may result in immediate rejection or removal.

---

## Governance model sync requirement

If your contribution modifies `governance-model.md`, you are responsible for:

1. Bumping the version number per §15
2. Adding a changelog entry
3. Noting in your PR which kit copies require re-sync

Kit maintainers are responsible for syncing their copies after governance model changes.

---

## Contribution workflow

### 1. fork and branch
- Fork the repository
- Create a branch from `main`
- Use a descriptive branch name:
  - `governance/…`
  - `docs/…`
  - `layer-model/…`

### 2. make your changes
- Keep changes small and focused
- One logical improvement per PR
- Do not bundle governance model changes with foundation guide changes

### 3. validate your contribution
Before opening a PR, ensure:
- Content is kit-agnostic
- No employer-specific content
- Governance model changes include version bump and changelog

### 4. open a pull request
Use the PR template. Your description should include:
- What problem this change solves
- Which documents are affected
- Whether kit copies require re-sync
- AI Usage Disclosure

---

## Review expectations

Maintainers will review contributions for:

- Alignment with AIEOS design philosophy
- Kit-agnosticism
- Anonymization compliance
- System-wide impact assessment

---

## Style & formatting

- Use Markdown
- Prefer bullet points over long prose
- Keep language precise and unambiguous
- Avoid marketing language
- Favor enforceable rules over guidance

---

## AI usage in contributions

You may use AI tools to assist in drafting content, provided that:

- You review all AI-generated output
- You ensure anonymization compliance
- You do not paste proprietary material into AI tools
- You take responsibility for the final content

---

## Code of conduct

This project follows the **Code of Conduct** defined in `CODE_OF_CONDUCT.md`.

---

## Final note

This repository defines the foundation that all AIEOS kits build on. Changes here have cascading effects. When in doubt, open an issue first and discuss before submitting a PR.
