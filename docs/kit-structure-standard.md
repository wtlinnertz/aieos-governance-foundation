# AIEOS Kit Structure Standard

This document is a compliance reference for building and auditing AIEOS-compatible kits. It operationalizes the rules in `governance-model.md` into a checklist format.

A kit passes this standard if every check below is satisfied.

---

## Part 1: Repository Structure

### Required Files

Every AIEOS kit must contain:

- [ ] `README.md` — repository overview (purpose, what it produces, how it relates to adjacent kits)
- [ ] `CLAUDE.md` — AI operating instructions for Claude Code
- [ ] `docs/playbook.md` — end-to-end process definition
- [ ] `docs/index.md` — documentation entry point
- [ ] `docs/how-to-adapt.md` — organizational adoption guidance
- [ ] `docs/how-to-use-with-ai.md` — artifact-by-artifact AI usage guide
- [ ] `docs/governance-model.md` — synchronized copy of the canonical governance model

### Required Directories

- [ ] `docs/specs/` — content rules and quality criteria
- [ ] `docs/artifacts/` — structural templates and intake forms
- [ ] `docs/prompts/` — AI behavior instructions
- [ ] `docs/validators/` — evaluation procedures
- [ ] `examples/` — at least one worked example demonstrating the full artifact flow
- [ ] `tests/` — structural integrity checks and/or flow scenario tests

---

## Part 2: Artifact Type Compliance

For each artifact type the kit produces:

### Four-File Completeness

- [ ] `docs/specs/{type}-spec.md` exists
- [ ] `docs/artifacts/{type}-template.md` exists
- [ ] `docs/prompts/{type}-prompt.md` exists
- [ ] `docs/validators/{type}-validator.md` exists

### Naming Convention

- [ ] File names follow `{type}-{role}.md` pattern with no deviations
- [ ] No artifact type has more than four governing files (extras must be utility prompts or intake forms, not additional specs/validators)

### Separation of Concerns

- [ ] Spec contains all hard gates and content rules — nothing is defined only in a prompt or validator
- [ ] Template contains only structure (section headings, placeholders) — no content rules
- [ ] Prompt references the spec for rules; it does not inline them
- [ ] Validator references the spec for hard gates; it does not inline them
- [ ] Validator does not suggest improvements or redesign — it judges only

---

## Part 3: Validator Compliance

Every validator must:

- [ ] Produce JSON output in the standard schema (see `governance-model.md` §5)
- [ ] Include `status`, `summary`, `hard_gates`, `blocking_issues`, `warnings`, `completeness_score`
- [ ] Set `status` to `FAIL` if any hard gate fails — no exceptions
- [ ] List every failing hard gate in `blocking_issues` with description and location
- [ ] Not produce suggestions, redesigns, or improvement guidance in any output field

---

## Part 4: Playbook Compliance

The `docs/playbook.md` must define:

- [ ] The complete artifact flow in the non-negotiable generation order
- [ ] Inputs and outputs for each step
- [ ] Freeze points (where human approval is required before proceeding)
- [ ] Re-entry protocol (what to do when a frozen artifact must change)
- [ ] Upstream boundary contract (what this kit accepts and from where)
- [ ] Downstream boundary contract (what this kit produces and who consumes it)

---

## Part 5: Governance Model Sync

- [ ] `docs/governance-model.md` is byte-for-byte identical to `aieos-spec/governance-model.md`
- [ ] No local modifications to the governance model — all edits go through aieos-spec
- [ ] CLAUDE.md references aieos-spec as the canonical authority for governance-model.md

---

## Part 6: CLAUDE.md Requirements

The kit's `CLAUDE.md` must contain:

- [ ] What the kit is (one-paragraph description)
- [ ] Repository structure overview
- [ ] Artifact types produced (list with brief descriptions)
- [ ] Artifact flow (the generation order)
- [ ] Key rules the AI must follow
- [ ] Boundary contracts (upstream and downstream)
- [ ] File naming conventions
- [ ] Reference to aieos-spec as governance model authority
- [ ] Commit message style guidance

---

## Part 7: Structural Integrity Tests

The `tests/` directory must include:

- [ ] A structural integrity check that verifies four-file completeness for all artifact types
- [ ] A naming convention check
- [ ] At least one end-to-end flow scenario

---

## Audit Procedure

To audit an existing kit against this standard:

1. **Check repository structure** (Part 1) — verify all required files and directories exist
2. **List all artifact types** — enumerate from the playbook and verify four-file completeness (Part 2) for each
3. **Sample-check separation of concerns** — read one spec, one prompt, one validator and verify rules are not duplicated or inlined (Part 2, Separation of Concerns)
4. **Check validator output format** — confirm JSON schema matches standard (Part 3)
5. **Check playbook completeness** — verify all required sections are present (Part 4)
6. **Verify governance model sync** — diff kit copy against canonical (Part 5)
7. **Read CLAUDE.md** — verify all required sections are present (Part 6)
8. **Check tests directory** — verify structural and flow tests exist (Part 7)

A kit that fails any check is not AIEOS-compatible. Fix before treating the kit as production-ready.
