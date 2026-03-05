# AIEOS Kit Structure Standard

This document is a compliance reference for building and auditing AIEOS-compatible kits. It operationalizes the rules in `governance-model.md` into a checklist format.

A kit passes this standard if every check below is satisfied.

Each check is annotated as:
- `[auto]` — machine-checkable by `aieos-spec/tests/check-structure.sh`
- `[ai]` — requires AI or human review; cannot be automated

---

## Part 1: Repository Structure

### Required Files

Every AIEOS kit must contain:

- [ ] `README.md` — repository overview (purpose, what it produces, how it relates to adjacent kits) `[auto]`
- [ ] `CLAUDE.md` — AI operating instructions for Claude Code `[auto]`
- [ ] `docs/playbook.md` — end-to-end process definition `[auto]`
- [ ] `docs/index.md` — documentation entry point `[auto]`
- [ ] `docs/how-to-adapt.md` — organizational adoption guidance `[auto]`
- [ ] `docs/how-to-use-with-ai.md` — artifact-by-artifact AI usage guide `[auto]`
- [ ] `docs/governance-model.md` — synchronized copy of the canonical governance model `[auto]`

### Required Directories

- [ ] `docs/specs/` — content rules and quality criteria `[auto]`
- [ ] `docs/artifacts/` — structural templates and intake forms `[auto]`
- [ ] `docs/prompts/` — AI behavior instructions `[auto]`
- [ ] `docs/validators/` — evaluation procedures `[auto]`
- [ ] `examples/` — at least one worked example demonstrating the full artifact flow `[auto]`
- [ ] `tests/` — structural integrity checks and/or flow scenario tests `[auto]`

---

## Part 2: Artifact Type Compliance

For each artifact type the kit produces:

### Four-File Completeness

- [ ] `docs/specs/{type}-spec.md` exists `[auto]`
- [ ] `docs/artifacts/{type}-template.md` exists `[auto]`
- [ ] `docs/prompts/{type}-prompt.md` exists `[auto]`
- [ ] `docs/validators/{type}-validator.md` exists `[auto]`

### Naming Convention

- [ ] File names follow `{type}-{role}.md` pattern with no deviations `[auto]`
- [ ] No artifact type has more than four governing files (extras must be utility prompts or intake forms, not additional specs/validators) `[ai]`

### Separation of Concerns

- [ ] Spec contains all hard gates and content rules — nothing is defined only in a prompt or validator `[ai]`
- [ ] Template contains only structure (section headings, placeholders) — no content rules `[ai]`
- [ ] Prompt references the spec for rules; it does not inline them `[ai]`
- [ ] Validator references the spec for hard gates; it does not inline them `[ai]`
- [ ] Validator does not suggest improvements or redesign — it judges only `[ai]`

---

## Part 3: Validator Compliance

Every validator must:

- [ ] Produce JSON output in the standard schema (see `governance-model.md` §5) `[auto]`
- [ ] Include `status`, `summary`, `hard_gates`, `blocking_issues`, `warnings`, `completeness_score` `[auto]`
- [ ] Set `status` to `FAIL` if any hard gate fails — no exceptions `[ai]`
- [ ] List every failing hard gate in `blocking_issues` with description and location `[ai]`
- [ ] Not produce suggestions, redesigns, or improvement guidance in any output field `[ai]`

---

## Part 4: Playbook Compliance

The `docs/playbook.md` must define:

- [ ] The complete artifact flow in the non-negotiable generation order `[ai]`
- [ ] Inputs and outputs for each step `[ai]`
- [ ] Freeze points (where human approval is required before proceeding) `[ai]`
- [ ] Re-entry protocol (what to do when a frozen artifact must change) `[ai]`
- [ ] Upstream boundary contract (what this kit accepts and from where) `[ai]`
- [ ] Downstream boundary contract (what this kit produces and who consumes it) `[ai]`

---

## Part 5: Governance Model Sync

- [ ] `docs/governance-model.md` is byte-for-byte identical to `aieos-spec/governance-model.md` `[auto]`
- [ ] No local modifications to the governance model — all edits go through aieos-spec `[ai]`
- [ ] CLAUDE.md references aieos-spec as the canonical authority for governance-model.md `[ai]`

---

## Part 6: CLAUDE.md Requirements

The kit's `CLAUDE.md` must contain:

- [ ] What the kit is (one-paragraph description) `[ai]`
- [ ] Repository structure overview `[ai]`
- [ ] Artifact types produced (list with brief descriptions) `[ai]`
- [ ] Artifact flow (the generation order) `[ai]`
- [ ] Key rules the AI must follow `[ai]`
- [ ] Boundary contracts (upstream and downstream) `[ai]`
- [ ] File naming conventions `[ai]`
- [ ] Reference to aieos-spec as governance model authority `[ai]`
- [ ] Commit message style guidance `[ai]`

---

## Part 7: Structural Integrity Tests

The `tests/` directory must include:

- [ ] A structural integrity check that verifies four-file completeness for all artifact types `[auto]`
- [ ] A naming convention check `[auto]`
- [ ] At least one end-to-end flow scenario `[ai]`

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

---

## Running Automated Checks

The script `aieos-spec/tests/check-structure.sh` automates all checks annotated `[auto]` above.

**Usage:**
```
./tests/check-structure.sh <kit-root-path>
```

**Example:**
```
./tests/check-structure.sh /path/to/aieos-engineering-execution-kit
```

The script outputs per-check PASS/FAIL results and exits with a non-zero code if any check fails (CI-compatible).

Checks annotated `[ai]` require AI or human review. Run the script first to eliminate structural issues, then review the `[ai]` checks manually against the audit procedure above.
