# AIEOS Healthcheck Playbook

This playbook defines the complete set of healthchecks available for the AIEOS framework. Healthchecks are organized into two scopes:

- **Framework healthchecks** validate the AIEOS kits themselves — structural integrity, governance consistency, and cross-kit coherence
- **Initiative healthchecks** validate a consuming project's use of AIEOS — artifact completeness, dependency ordering, and engagement record integrity

Both scopes are essential. Framework healthchecks ensure the rules are sound; initiative healthchecks ensure the rules are being followed.

---

## How to Use This Playbook

1. **Identify which scope applies** — Are you checking the framework itself, or a specific initiative?
2. **Select the appropriate tier** — Each scope has tiered checks from fast/structural to deep/semantic
3. **Run the checks** — Use the commands listed in each section
4. **Interpret results** — Each check produces PASS/FAIL; see remediation guidance per check
5. **Fix and re-run** — Resolve failures before proceeding to the next tier

**Gating rule:** Within each scope, lower tiers gate higher tiers. Do not run Tier 2 until Tier 1 passes.

---

## Scope A: Framework Healthchecks

Framework healthchecks validate the AIEOS kit directories (`aieos-*/`). They answer: "Are the kits well-formed, consistent, and correctly interconnected?"

### A1. Structural Validation (Tier 1)

**What it checks:**
- Markdown syntax quality (markdownlint)
- Internal link integrity (markdown-link-check)
- Kit directory structure compliance (check-structure.sh per kit-structure-standard.md)

**When to run:** On every commit to any kit. In CI on every push.

**Command:**
```bash
aieos-governance-foundation/tests/run-tier1.sh
```

**What passes look like:**
- All markdown files lint-clean
- No broken internal links
- Every kit has the required files and directories (README.md, CLAUDE.md, docs/playbook.md, docs/index.md, docs/governance-model.md, etc.)

**Remediation:**
| Failure | Fix |
|---------|-----|
| Markdown lint error | Edit the flagged file; see markdownlint rule reference |
| Broken link | Update the link target or remove the dead reference |
| Missing required file | Create the file following the kit-structure-standard.md checklist |
| Four-file gap | Create the missing template, prompt, or validator for the spec |

---

### A2. Governance Consistency (Tier 2)

**What it checks:**
- Dependency graph is a valid DAG (no cycles)
- All artifacts are reachable from declared entry points
- Freeze-before-promote ordering is valid
- Governance model copies are byte-identical across all kits
- Four-file completeness (every spec has template + validator)
- All specs have version fields
- Boundary contract entry-from files exist and reference correct upstream artifacts
- Playbook and CLAUDE.md present in every kit
- Cross-cutting kits don't block each other (except QAK→REK)
- Pipeline layers are sequential
- All 5 initiative presets have valid entry points and reachable artifacts
- Escalation paths are valid reverse-direction edges
- BDD scenarios for escalation, presets, and re-entry protocols

**When to run:** On every commit to any kit. In CI on every push. Must pass before agent integration tests.

**Command:**
```bash
aieos-governance-foundation/tests/run-tier2.sh
```

**What passes look like:** All 65+ pytest tests pass.

**Remediation:**
| Failure | Fix |
|---------|-----|
| Cycle in dependency graph | Review DEPENDENCY_EDGES in models/framework.py; a new edge introduced a cycle |
| Unreachable artifact | Add the missing edge or entry point in models/framework.py |
| Governance model mismatch | Copy canonical governance-model.md from governance-foundation to the failing kit |
| Four-file gap | Create the missing template or validator |
| Missing spec version | Add `Version: v1.0` after the spec title |
| Boundary contract missing | Create entry-from-{upstream}.md in the downstream kit |
| Preset artifact unreachable | Add dependency edge or fix preset definition in models/framework.py |

---

### A3. Spec-Version Drift Detection (Tier 2)

**What it checks:**
- Every template's Document Control section references a `Spec Version` placeholder
- No template references a spec version that is older than the current spec version
- Principles version placeholders are present where required

**When to run:** After any spec version bump. Periodically (weekly recommended).

**Automated:** Yes — included in Tier 2 test suite (`test_cross_refs.py`).

**Remediation:**
| Failure | Fix |
|---------|-----|
| Template missing Spec Version field | Add `Spec Version` row to Document Control section |
| Template references outdated spec version | Update the template's spec version reference |
| Principles Version missing | Add `Principles Version` row to Document Control section |

---

### A4. Agent Integration Tests (Tier 3)

**What it checks:**
- An AI agent can generate artifacts from specs, templates, and prompts
- Generated artifacts pass validator hard gates
- The end-to-end artifact chain works (PRD → ACF → SAD → TDD)

**When to run:** Before releasing framework changes. On-demand. Not required for every commit.

**Command:**
```bash
aieos-governance-foundation/tests/run-all.sh --with-integration
```

**Prerequisites:** Claude Code CLI (`claude`) must be installed. Tier 1 and Tier 2 must pass first.

**Remediation:**
| Failure | Fix |
|---------|-----|
| Agent cannot generate artifact | Check the prompt file — it may reference a missing spec section or use ambiguous instructions |
| Generated artifact fails validation | Check the spec for conflicting rules; check the validator for overly strict gates |
| Chain breaks at handoff | Check that upstream artifact output matches downstream input expectations |

---

## Scope B: Initiative Healthchecks

Initiative healthchecks validate a consuming project's SDLC directory and Engagement Record. They answer: "Is this initiative following the AIEOS process correctly?"

These checks run against a specific initiative's artifacts, not against the framework kits.

### B1. Engagement Record Completeness

**What it checks:**
- ER file exists at `{project}/docs/engagement/er-{initiative}.md`
- §1 Document Control is filled (ER ID, initiative name, status, dates, ER spec version)
- Each active layer section has an artifact table with at least one artifact ID
- Artifact IDs follow the `{TYPE}-{INITIATIVE}-{NNN}` naming convention
- Status values are valid (Draft, Validated, Freeze Pending, Frozen, Deprecated, Abandoned)
- Key Decisions sections are populated for layers that have frozen artifacts
- §7 Initiative Outcome is populated for completed/deprecated initiatives

**When to run:** At every layer boundary (before entering the next layer). At initiative completion.

**Automated:** Not yet — candidate for future Tier 2 test if initiative directories follow a convention.

**Manual check procedure:**
1. Open the ER file
2. Verify §1 has all required fields filled
3. For each layer the initiative has entered, verify the artifact table has artifact IDs with valid format
4. For each layer with frozen artifacts, verify Key Decisions has at least one entry
5. If initiative is complete, verify §7 has final status and VH verdict

**Remediation:**
| Failure | Fix |
|---------|-----|
| ER missing | Create from engagement-record-spec.md (§1 + first active layer header) |
| Missing artifact IDs | Update ER with IDs from frozen artifacts |
| Empty Key Decisions | Add decisions per the ER spec format |
| Missing §7 | Complete Initiative Outcome section |

---

### B2. Artifact Dependency Order

**What it checks:**
- Upstream artifacts are frozen before downstream artifacts were generated
- No downstream artifact was generated while its upstream was still in Draft
- Cross-kit handoffs have the required frozen artifact available

**When to run:** Before promoting any artifact to Frozen. Before entering a new layer.

**Manual check procedure:**
1. For the artifact being promoted, identify its upstream dependencies from the dependency graph
2. Confirm each upstream artifact is in Frozen status in the ER
3. For cross-kit entry, confirm the entry-from contract artifacts are frozen

**Example:** Before freezing TDD-TASKFLOW-001, verify:
- ACF-TASKFLOW-001 is Frozen
- SAD-TASKFLOW-001 is Frozen
- PRD-TASKFLOW-001 is Frozen

**Remediation:**
| Failure | Fix |
|---------|-----|
| Upstream not frozen | Freeze the upstream artifact first (validate → freeze pending → freeze) |
| Upstream skipped | Generate the missing upstream artifact; do not skip the dependency chain |

---

### B3. Frozen Artifact Immutability

**What it checks:**
- Files marked as Frozen in the ER have not been modified after freeze date
- If a frozen file has been modified, it should have a corresponding re-entry decision and impact analysis

**When to run:** Periodically (weekly). Before layer transitions. Before release.

**Manual check procedure:**
1. For each Frozen artifact in the ER, check `git log --follow -1 -- <file>` for last modification date
2. Compare modification date to the freeze date recorded in the ER or artifact's Document Control
3. If modified after freeze: verify a re-entry record exists explaining the change

**Remediation:**
| Failure | Fix |
|---------|-----|
| Frozen artifact modified without re-entry | Either revert the change or formally re-enter: impact analysis → modify → re-validate → re-freeze |
| No freeze date recorded | Add freeze date to Document Control section and ER |

---

### B4. Validator Pass Gates

**What it checks:**
- Every artifact promoted to Frozen has a corresponding PASS validation result
- Validation was performed in a separate session from generation (session discipline)
- Hard gate failures are not present in the final validation

**When to run:** Before every freeze decision.

**Manual check procedure:**
1. Locate the validation output (JSON file or validator session log) for the artifact
2. Confirm `"status": "PASS"`
3. Confirm all hard_gates show `"PASS"`
4. Confirm no blocking_issues are listed
5. Confirm the validation session was separate from the generation session

**Remediation:**
| Failure | Fix |
|---------|-----|
| No validation result | Run the validator against the artifact before freezing |
| FAIL status | Address blocking issues, regenerate or amend, then re-validate |
| Same-session validation | Re-validate in a fresh session (generation context biases validation) |

---

### B5. Cross-Kit Handoff Verification

**What it checks:**
- When entering a new kit, the entry-from contract requirements are met
- Required upstream artifacts are frozen (not just Draft or Validated)
- The downstream kit's first artifact references the correct upstream artifact IDs

**When to run:** At every kit boundary transition.

**Manual check procedure:**
1. Identify the downstream kit being entered
2. Read its entry-from-{upstream}.md file to get required artifacts
3. Verify each required artifact is Frozen in the ER
4. Verify the downstream kit's first artifact (entry record) references the upstream artifact IDs

**Example:** Entering REK from EEK:
1. Read `aieos-release-exposure-kit/docs/entry-from-eek.md`
2. Verify ORD-{INITIATIVE}-001 is Frozen
3. Verify RER references ORD ID

**Remediation:**
| Failure | Fix |
|---------|-----|
| Upstream not frozen | Return to upstream kit and complete the freeze process |
| Entry record doesn't reference upstream | Update the entry record to include upstream artifact IDs |

---

### B6. Initiative Preset Compliance

**What it checks:**
- The initiative is following a declared preset (or has documented deviations)
- Required artifacts for the preset are being produced
- Optional layers that were adopted are fully completed (no partial adoption)

**When to run:** At initiative midpoint. At initiative completion.

**Manual check procedure:**
1. Identify the initiative's preset from the ER or KER/WCR
2. Cross-reference against the preset definition in initiative-presets.md
3. For each required artifact: confirm it exists or is in progress
4. For each adopted optional layer: confirm all layer artifacts are present

**Remediation:**
| Failure | Fix |
|---------|-----|
| Missing required artifact | Generate the artifact per the kit playbook |
| Partial layer adoption | Either complete all artifacts for the adopted layer or formally drop the layer with justification |
| No preset declared | Add preset selection to KER or WCR |

---

### B7. Escalation Tracking

**What it checks:**
- When a validator returns FAIL, an escalation path was followed
- Escalation records reference the triggering failure
- Re-entry after escalation includes impact analysis

**When to run:** After any validation failure. At initiative completion review.

**Manual check procedure:**
1. Search for any FAIL validation results in the initiative's artifacts
2. For each FAIL: verify an escalation was recorded (in ER Gate Failures section or as a separate escalation record)
3. Verify the escalation followed one of the 6 defined paths (T1–T6) or a documented re-entry protocol
4. Verify impact analysis was performed before re-entry

**Remediation:**
| Failure | Fix |
|---------|-----|
| Unrecorded escalation | Add the failure and resolution to the ER's Gate Failures section |
| No impact analysis | Perform impact analysis per the re-entry protocol before proceeding |

---

### B8. Navigation Map Consistency

**What it checks:**
- Navigation map nodes correspond to known artifact types in the framework dependency model
- Navigation map edges are consistent with the dependency graph
- Every junction in the navigation map has a complete decision table (all options listed)
- Navigation map preset applicability tags match initiative-presets.md definitions

**When to run:** After any playbook change. After any navigation map change. Periodically (weekly recommended).

**Automated:** Partially — Tier 2 test validates structural consistency between navigation-map.md and models/framework.py.

**Manual check procedure:**
1. Verify that every kit's playbook steps are represented as nodes in the navigation map
2. Verify that every edge condition matches the corresponding playbook's freeze point or junction
3. For each junction, confirm all options from the playbook are present in the decision table

**Remediation:**
| Failure | Fix |
|---------|-----|
| Missing node | Add the node to navigation-map.md Section 1 |
| Missing edge | Add the edge to navigation-map.md Section 2 |
| Incomplete decision table | Add missing options to navigation-map.md Section 3 |
| Preset tag mismatch | Update preset applicability in navigation-map.md to match initiative-presets.md |

---

## Healthcheck Schedule

### Per-Commit (Automated)

| Check | Scope | Tier |
|-------|-------|------|
| A1: Structural Validation | Framework | 1 |
| A2: Governance Consistency | Framework | 2 |
| A3: Spec-Version Drift | Framework | 2 |

### Per-Layer-Transition (Manual)

| Check | Scope |
|-------|-------|
| B1: ER Completeness | Initiative |
| B2: Artifact Dependency Order | Initiative |
| B4: Validator Pass Gates | Initiative |
| B5: Cross-Kit Handoff | Initiative |

### Per-Freeze (Manual)

| Check | Scope |
|-------|-------|
| B2: Artifact Dependency Order | Initiative |
| B3: Frozen Artifact Immutability | Initiative |
| B4: Validator Pass Gates | Initiative |

### Periodic (Weekly Recommended)

| Check | Scope |
|-------|-------|
| A3: Spec-Version Drift | Framework |
| B3: Frozen Artifact Immutability | Initiative |

### Per-Initiative-Completion (Manual)

| Check | Scope |
|-------|-------|
| B1: ER Completeness (full) | Initiative |
| B6: Preset Compliance | Initiative |
| B7: Escalation Tracking | Initiative |

### Pre-Release (Manual)

| Check | Scope |
|-------|-------|
| A4: Agent Integration | Framework |
| B2: Artifact Dependency Order | Initiative |
| B3: Frozen Artifact Immutability | Initiative |
| B5: Cross-Kit Handoff | Initiative |

---

## Interpreting Results

### Framework Checks (Scope A)

**All pass:** The framework kits are structurally sound, internally consistent, and correctly interconnected. Safe to use for artifact generation and validation.

**Tier 1 fails:** Structural issue — a file is missing, misnamed, or has broken links. Fix before running Tier 2.

**Tier 2 fails:** Governance consistency issue — a dependency was broken, a governance model copy drifted, or a four-file set is incomplete. Fix before generating any new artifacts.

**Tier 3 fails:** Agent compatibility issue — the framework is internally consistent but an AI agent cannot successfully use it. Review prompts, specs, and validator expectations.

### Initiative Checks (Scope B)

**All pass:** The initiative is following the AIEOS process correctly. Artifacts are in order, dependencies are satisfied, and the engagement record is complete.

**Any B-check fails:** Process deviation detected. The failure description tells you which invariant was violated. Fix before the next layer transition — accumulated process debt compounds downstream.

---

## Adding New Healthchecks

When adding a new healthcheck:

1. **Determine scope** — Framework (A) or Initiative (B)?
2. **Determine tier** — Can it be automated (Tier 1/2) or is it manual?
3. **Write the check** — Follow the format in this playbook (what, when, how, remediation)
4. **Add to schedule** — Update the Healthcheck Schedule section
5. **If automated** — Add to the appropriate test file in `aieos-governance-foundation/tests/`
6. **Update this playbook** — Add the new check to the appropriate scope section
