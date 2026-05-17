# AIEOS Kit Structure Standard

This document is a compliance reference for building and auditing AIEOS-compatible kits. It operationalizes the rules in `governance-model.md` into a checklist format.

A kit passes this standard if every check below is satisfied.

Each check is annotated as:
- `[auto]` — machine-checkable by `aieos-governance-foundation/tests/check-structure.sh`
- `[ai]` — requires AI or human review; cannot be automated

---

## Part 1: repository structure

### Required files

Every AIEOS kit must contain:

- [ ] `README.md` — repository overview (purpose, what it produces, how it relates to adjacent kits) `[auto]`
- [ ] `CLAUDE.md` — AI operating instructions for Claude Code `[auto]`
- [ ] `docs/playbook.md` — end-to-end process definition `[auto]`
- [ ] `docs/index.md` — documentation entry point `[auto]`
- [ ] `docs/how-to-adapt.md` — organizational adoption guidance `[auto]`
- [ ] `docs/how-to-use-with-ai.md` — artifact-by-artifact AI usage guide `[auto]`
- [ ] `docs/governance-model.md` — synchronized copy of the canonical governance model `[auto]`

### Required directories

- [ ] `docs/specs/` — content rules and quality criteria `[auto]`
- [ ] `docs/artifacts/` — structural templates and intake forms `[auto]`
- [ ] `docs/prompts/` — AI behavior instructions `[auto]`
- [ ] `docs/validators/` — evaluation procedures `[auto]`
- [ ] `examples/` — at least one worked example demonstrating the full artifact flow `[auto]`
- [ ] `tests/` — structural integrity checks and/or flow scenario tests `[auto]`

### Optional directories

- [ ] `docs/tools/` — tool capability definitions (four-file sets) `[auto]` *(only required if the kit defines tools)*
- [ ] `docs/bindings/` — implementation mappings `[auto]` *(only required if the kit maps abstract concepts to specific tools)*

---

## Part 2: artifact type compliance

For each artifact type the kit produces:

### Four-File completeness

- [ ] `docs/specs/{type}-spec.md` exists `[auto]`
- [ ] `docs/artifacts/{type}-template.md` exists `[auto]`
- [ ] `docs/prompts/{type}-prompt.md` exists `[auto]`
- [ ] `docs/validators/{type}-validator.md` exists `[auto]`

### Naming convention

- [ ] File names follow `{type}-{role}.md` pattern with no deviations `[auto]`
- [ ] No artifact type has more than four governing files (extras must be utility prompts or intake forms, not additional specs/validators) `[ai]`

### Separation of concerns

- [ ] Spec contains all hard gates and content rules — nothing is defined only in a prompt or validator `[ai]`
- [ ] Template contains only structure (section headings, placeholders) — no content rules `[ai]`
- [ ] Prompt references the spec for rules; it does not inline them `[ai]`
- [ ] Validator references the spec for hard gates; it does not inline them `[ai]`
- [ ] Validator does not suggest improvements or redesign — it judges only `[ai]`

---

## Part 2b: tool type compliance

For each tool type the kit defines (if `docs/tools/` exists):

### Four-File completeness

- [ ] `docs/tools/{tool-name}-spec.md` exists `[auto]`
- [ ] `docs/tools/{tool-name}-template.md` exists `[auto]`
- [ ] `docs/tools/{tool-name}-prompt.md` exists `[auto]`
- [ ] `docs/tools/{tool-name}-validator.md` exists `[auto]`

### Naming convention

- [ ] Tool file names follow `{tool-name}-{role}.md` pattern (kebab-case, capability names) `[auto]`
- [ ] Tool names describe capabilities (verbs/verb-noun phrases), not artifact types `[ai]`

### Separation of concerns

- [ ] Tool spec contains all preconditions, postconditions, constraints, and hard gates — nothing is defined only in a prompt or validator `[ai]`
- [ ] Tool template contains only output structure — no behavioral rules `[ai]`
- [ ] Tool prompt references the tool spec for rules; it does not inline them `[ai]`
- [ ] Tool validator references the tool spec for hard gates; it does not inline them `[ai]`
- [ ] Tool spec contains no implementation details — binding separation is maintained `[ai]`

---

## Part 3: validator compliance

Every validator must:

- [ ] Produce JSON output in the standard schema (see `governance-model.md` §5) `[auto]`
- [ ] Include `status`, `summary`, `hard_gates`, `blocking_issues`, `warnings`, `completeness_score` `[auto]`
- [ ] Set `status` to `FAIL` if any hard gate fails — no exceptions `[ai]`
- [ ] List every failing hard gate in `blocking_issues` with description and location `[ai]`
- [ ] Not produce suggestions, redesigns, or improvement guidance in any output field `[ai]`

---

## Part 4: playbook compliance

The `docs/playbook.md` must define:

- [ ] The complete artifact flow in the non-negotiable generation order `[ai]`
- [ ] Inputs and outputs for each step `[ai]`
- [ ] Freeze points (where human approval is required before proceeding) `[ai]`
- [ ] Re-entry protocol (what to do when a frozen artifact must change) `[ai]`
- [ ] Upstream boundary contract (what this kit accepts and from where) `[ai]`
- [ ] Downstream boundary contract (what this kit produces and who consumes it) `[ai]`

---

## Part 5: governance model sync

- [ ] `docs/governance-model.md` is byte-for-byte identical to `aieos-governance-foundation/governance-model.md` `[auto]`
- [ ] No local modifications to the governance model — all edits go through aieos-governance-foundation `[ai]`
- [ ] CLAUDE.md references aieos-governance-foundation as the canonical authority for governance-model.md `[ai]`

---

## Part 6: cLAUDE.md requirements

The kit's `CLAUDE.md` must contain:

- [ ] What the kit is (one-paragraph description) `[ai]`
- [ ] Repository structure overview `[ai]`
- [ ] Artifact types produced (list with brief descriptions) `[ai]`
- [ ] Artifact flow (the generation order) `[ai]`
- [ ] Key rules the AI must follow `[ai]`
- [ ] Boundary contracts (upstream and downstream) `[ai]`
- [ ] File naming conventions `[ai]`
- [ ] Reference to aieos-governance-foundation as governance model authority `[ai]`
- [ ] Commit message style guidance `[ai]`

---

## Part 7: structural integrity tests

The `tests/` directory must include:

- [ ] A structural integrity check that verifies four-file completeness for all artifact types `[auto]`
- [ ] A naming convention check `[auto]`
- [ ] At least one end-to-end flow scenario `[ai]`

---

## Audit procedure

To audit an existing kit against this standard:

1. **Check repository structure** (Part 1) — verify all required files and directories exist
2. **List all artifact types** — enumerate from the playbook and verify four-file completeness (Part 2) for each
3. **Check tool types** (Part 2b) — if `docs/tools/` exists, verify four-file completeness for each tool
4. **Sample-check separation of concerns** — read one spec, one prompt, one validator and verify rules are not duplicated or inlined (Part 2, Separation of Concerns)
5. **Check validator output format** — confirm JSON schema matches standard (Part 3)
6. **Check playbook completeness** — verify all required sections are present (Part 4)
7. **Verify governance model sync** — diff kit copy against canonical (Part 5)
8. **Read CLAUDE.md** — verify all required sections are present (Part 6)
9. **Check tests directory** — verify structural and flow tests exist (Part 7)

A kit that fails any check is not AIEOS-compatible. Fix before treating the kit as production-ready.

---

## Running automated checks

The script `aieos-governance-foundation/tests/check-structure.sh` automates all checks annotated `[auto]` above.

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
