# AIEOS Gap Closure — Implementation Plan

**Date:** 2026-05-17  
**Author:** Claude Sonnet 4.6 + Todd Linnertz  
**Source audit:** `aieos-governance-foundation/findings/aieos-framework-audit-2026-05-17.md`  
**Governance model in scope:** v1.6 → v1.7  

---

## Goal

Close all 25 issues identified in the May 17 audit without introducing new gaps, inconsistencies, or violations of AIEOS structural principles.

## AIEOS Principles Governing This Plan

Every change in this plan follows these rules from the governance model:

1. **Specs are the single source of truth** — hard gate changes live only in spec files; validators and prompts reference specs, never inline rules.
2. **Freeze-before-promote** — the governance-foundation changes (spec-level, model-level) land before kit-level changes that depend on them.
3. **Separation of concerns** — spec changes, validator changes, prompt changes, and documentation changes are handled in separate tasks even when they co-locate in the same commit.
4. **§15 change protocol** — governance-model.md changes first; kit copies updated after; TOOL-KIT-SYNC-AUDIT run at end to verify sync. Governance model version bumps from 1.6 → 1.7.
5. **Spec versioning** — every edited spec file gets a version bump per the spec-file-standard: patch (Minor = clarification only), minor version (Significant = new hard gate or new required field), major version (Breaking = removing a gate or loosening a constraint). Version changes stated per fix.
6. **No scope expansion** — each task changes only what the issue requires. Adjacent improvements, cleanup, or "while we're here" edits are explicitly forbidden.
7. **Human freeze decision** — this plan describes what to change; commit/push to main constitutes the authorization step for each doc change. No AI self-approves governance changes.
8. **Validators judge, they do not help** — validator changes must remain strict PASS/FAIL with no suggestions added.

## Dependency Order

The 25 fixes have strict ordering constraints because some fixes cascade:

```
ORDERING RULES:
  governance-model.md must change BEFORE kit copies are updated
  Spec changes must land BEFORE validator changes that reference them
  governance-model.md version bump (→ v1.7) unlocks all downstream kit-copy syncs
  TOOL-KIT-SYNC-AUDIT runs LAST in each phase to verify copies match
  
DEPENDENCY CHAINS:
  FIX-01 (Trigger 5 definition) → changes governance-model.md §15 + escalation-protocols.md
         → triggers kit-copy sync pass
  FIX-02 (QAK optional/required) → changes governance-model.md §17 + QAK README + layer-model.md
         → triggers kit-copy sync pass (same wave as FIX-01)
  FIX-05 (EEK repo name) → changes governance-model.md §Kit Registry + layer-model.md + README
         → triggers kit-copy sync pass (same wave)
  FIX-03 (compliance VP ordering) → changes QAK vp-spec.md (Significant, v1.0 → v1.1)
         → changes QAK vp-prompt.md (must reference updated spec)
         → changes QAK vp-validator.md (must check new conditional gate)
  FIX-08 (BPK RC → REK gate) → changes REK release-entry-spec.md (Significant, v1.0 → v1.1)
         → changes REK release-entry-validator.md
  FIX-10 (DCF entry gate) → changes EEK dcf-spec.md (Significant, v1.0 → v1.1)
         → changes EEK dcf-validator.md
  FIX-15 (SSK skip gate in KER) → changes EEK kit-entry-spec.md (Significant, v1.0 → v1.1)
         → changes EEK kit-entry-validator.md
  
  All spec changes require:
    1. Spec version bump
    2. Validator update (to check new gate)
    3. Prompt update (to reference new constraint in input context)
    4. Template update (to include new field/section for authors)
    
PHASE GATE:
  Phase 1 (Criticals) must be fully committed and pushed before Phase 2 begins.
  Phase 2 must be fully committed and pushed before Phase 3 begins.
  Final TOOL-KIT-SYNC-AUDIT closes Phase 2 and Phase 3.
```

---

## Phase 1 — Critical Fixes

*Close the 3 issues that can cause wrong decisions or dead references during any active initiative.*

---

### Task 1.1: Define Escalation Trigger 5 in escalation-protocols.md

**What and why:** Trigger 5 is referenced in governance-model.md §15 (Decision Outcome Taxonomy) but does not exist. Any operator who encounters a production SLO rollback scenario follows the taxonomy to "Trigger 5" and finds nothing. Rollback is a distinct decision context from Trigger 3 (code defect post-release from REK) and Trigger 4 (wrong feature from REK) because it can be initiated from RRK during active operation, not only from REK.

**Spec impact:** None — escalation-protocols.md is not a spec file. This is a governance doc addition.  
**Governance model impact:** §15 taxonomy table already references Trigger 5; it just needs the target file to exist.

**Files to change:**
- `aieos-governance-foundation/docs/escalation-protocols.md` — add Trigger 5 definition
- `aieos-governance-foundation/governance-model.md` — no text change needed (taxonomy already references it); bump version 1.6 → 1.7 in §15 to reflect this amendment

**Trigger 5 definition to add (exact text, insert after Trigger 4 block):**

```markdown
### Trigger 5 — Production SLO Violation Requiring Rollback

Source: Layer 6 (RRK), signal = frozen RHR or active burn rate alert with SLO breach  
Criteria (ALL must be true):
  1. An active deployment is in production and has not yet been absorbed into a stable RHR cycle
  2. SLO burn rate has breached the alert threshold OR an error budget has been fully consumed
  3. The breach is traced to the specific deployment (not to pre-existing baseline conditions)
  4. The reliability owner and release owner have assessed that forward-fix risk exceeds rollback risk

Destination: Layer 5 (REK)  
Action: Release owner executes rollback procedure. New RR documents the rollback decision,
  root cause category, and post-rollback SLO state. If rollback reveals a code defect,
  Trigger 3 criteria are re-assessed. If rollback reveals wrong scope, Trigger 4 criteria
  are re-assessed.  
Assessment question: Is the SLO breach caused by this deployment specifically (→ rollback
  assessment), or is it a pre-existing reliability condition (→ stays in Layer 6 Trigger 1/2
  path)?

Note: Trigger 5 is the only trigger that flows to a kit the initiative has already passed
  through (REK). The RR for the rolled-back release is not re-opened; a new RR is created
  documenting the rollback event.
```

**Steps:**

1. Open `aieos-governance-foundation/docs/escalation-protocols.md`
2. After the Trigger 4 block, insert the Trigger 5 block exactly as above
3. Update the trigger count in the doc header/intro from "four escalation triggers" to "five escalation triggers"
4. Open `aieos-governance-foundation/governance-model.md`
5. In §15, bump `Current version: 1.6` → `Current version: 1.7`
6. Verify the Rollback row in the Decision Outcome Taxonomy table still maps correctly to Trigger 5 (it does — no text change needed there)
7. Commit: `docs(governance): define Escalation Trigger 5 — SLO rollback path; bump governance model to v1.7`
8. Do not push yet — Tasks 1.2 and 1.3 edit the same governance-foundation files; batch the push at the end of Phase 1.

---

### Task 1.2: Resolve QAK optional/required contradiction

**What and why:** governance-model.md §17 says QAK is "Optional." QAK README says it has "no opt-out path." Both are read by operators. The contradiction causes opposite adoption decisions depending on which document a team reads first.

**Resolution:** QAK is conditionally required. The condition is: any initiative with integration points, external dependencies, or cross-component test scope. For simpler single-service changes with no external integration, QAK is optional. This is consistent with the governance model's spirit and the QAK README's intent.

**Files to change:**
- `aieos-governance-foundation/governance-model.md` §17 — update QAK line
- `aieos-governance-foundation/docs/layer-model.md` — update Layer 9 description
- `aieos-quality-assurance-kit/README.md` — align "no opt-out path" language

**Exact text changes:**

In governance-model.md §17, change:
```
L9  QAK:   Optional — adopt if integration points, external dependencies, or
           cross-component behavior exist
```
to:
```
L9  QAK:   Conditionally required — required when the initiative has
           integration points, external dependencies, or cross-component
           test scope. Optional for single-service changes with no
           external integration. When adopted, no opt-out path after
           QAER is frozen.
```

In QAK README, change the "REQUIRED once the ORD is frozen" statement to:
```
QAK is conditionally required. Engage when the initiative has integration
points, external dependencies, or cross-component test scope. For
single-service changes with no external integration, QAK is optional.

Once QAER is frozen, there is no opt-out path — the quality gate
must complete before REK entry.
```

In layer-model.md Layer 9 description, align with the same conditional framing.

**Steps:**

1. Edit `governance-model.md` §17 (text above)
2. Edit `docs/layer-model.md` Layer 9 paragraph
3. Add to commit from Task 1.1 (same file, same commit is fine for governance-foundation changes)
4. Edit `aieos-quality-assurance-kit/README.md` — SEPARATE commit in that repo
5. Commit QAK change: `docs(qak): align optional/required framing with governance model v1.7`

---

### Task 1.3: Add SCK ordering constraint to QAK VP spec (Significant spec change)

**What and why:** For compliance/regulatory initiatives (Preset 3), QAK VP must not be generated before SCK artifacts are frozen. The constraint exists only in prose. The VP spec's Upstream Dependencies section already mentions SCK as "optional inputs" — but does not make them conditional hard gates for compliance initiatives. We add a conditional hard gate.

**Spec version:** v1.0 → v1.1 (Significant — new conditional hard gate)  
**Impact on frozen artifacts:** Forward-looking only. VPs frozen under v1.0 are grandfathered.

**Files to change:**

1. `aieos-quality-assurance-kit/docs/specs/vp-spec.md` — v1.0 → v1.1, add conditional gate
2. `aieos-quality-assurance-kit/docs/validators/vp-validator.md` — add check for new gate
3. `aieos-quality-assurance-kit/docs/prompts/vp-prompt.md` — add conditional instruction
4. `aieos-quality-assurance-kit/docs/artifacts/vp-template.md` — add SCK compliance check field

**Steps:**

Step 1 — Edit vp-spec.md:

Bump version: `Version: v1.0` → `Version: v1.1`

In the Hard Gates section, add a new gate immediately after the existing QAER gate:

```markdown
### compliance_sck_ordering (conditional)

**Condition:** This gate applies only when the initiative has a Compliance Evidence
Record (CER) in scope — i.e., a compliance mandate was identified and SCK CER
was adopted.

**Rule:** When a CER is in scope, the following SCK artifacts must all be in
Frozen status before VP generation proceeds:
  - Threat Model (TM)
  - Security Assessment Record (SAR)
  - Compliance Evidence Record (CER)
  - Dependency Audit Record (DAR)

**Failure example:** VP generated with CER in scope but TM not yet frozen.

**When CER is not in scope:** This gate does not apply. State explicitly in
VP §Document Control: "CER not in scope for this initiative."
```

Step 2 — Edit vp-validator.md:

Add check for `compliance_sck_ordering` gate:
- If VP §Document Control declares "CER not in scope": gate passes automatically
- If §Document Control does not contain that declaration: validator checks that frozen TM, SAR, CER, and DAR IDs are referenced in §Upstream Dependencies
- FAIL if CER is listed as an input but any of TM/SAR/CER/DAR are not confirmed Frozen

Step 3 — Edit vp-prompt.md:

Add to the input context section: "If the Compliance Evidence Record (CER) is in scope for this initiative, confirm that TM, SAR, CER, and DAR are all Frozen before generating this VP. If any are not Frozen, halt and report the blocking dependency. Do not generate a VP until all required SCK artifacts are Frozen."

Step 4 — Edit vp-template.md:

Add to §Document Control:
```
| SCK compliance ordering | [ ] CER not in scope — compliance gate N/A
                          [ ] CER in scope — TM: {ID}, SAR: {ID}, CER: {ID}, DAR: {ID} all Frozen |
```

Step 5 — Commit: `feat(qak): add compliance SCK ordering gate to VP spec v1.1`

Step 6 — Add prompt evolution log entry to QAK at `docs/prompts/prompt-evolution-log.md`:
```
| vp-prompt.md | 1.0 → 1.1 | Added compliance_sck_ordering conditional halt instruction | AM-001 |
```

**Push all Phase 1 changes after this task.**

---

## Phase 2 — High Priority Fixes

*Correct documentation errors, specification inconsistencies, and logic gaps that cause wrong operator decisions.*

All Phase 2 tasks are batched into waves by repo to minimize commits. Each repo gets one commit per wave.

---

### Task 2.1: Governance Foundation — documentation corrections wave

**Wave covers:** FIX-04 (layer count), FIX-05 (EEK repo name in foundation docs), FIX-11 (SDK status)

**Files to change (all in aieos-governance-foundation):**

**README.md:**
- Change "All 16 layer kits (including the Governance Foundation)" → "All 15 layer kits are built and operational. The Governance Foundation is the canonical authority for all kits — it is not a layer kit."
- In §Kit Registry table, correct `aieos-engineering-execution-kit` → `aieos-engineering-execution` in the Repository column

**governance-model.md §Kit Registry:**
- Correct Layer 4 row: `aieos-engineering-execution-kit` → `aieos-engineering-execution`

**docs/layer-model.md:**
- Correct all references to `aieos-engineering-execution-kit` → `aieos-engineering-execution`
- Update Layer 1 description: remove "not yet in standard flow" language. Replace with: "Optional for all initiatives. Engage when portfolio-level prioritization across competing bets is needed. May be bypassed with justification documented in the PIK Discovery Intake or EEK KER."

**docs/flow-reference.md:**
- Correct `aieos-engineering-execution-kit` references

**Commit:** `docs(foundation): correct layer count, EEK repo name, SDK status language`

---

### Task 2.2: Kit-copy sync — propagate governance-model.md v1.7 to all 15 kits

**What:** After governance-model.md changed in Phase 1 (version bump to 1.7 + Trigger 5 addition + QAK framing update + EEK name correction), all 15 kit copies of `docs/governance-model.md` must be updated to match exactly.

**Files to change:** `docs/governance-model.md` in all 15 kit repos.

**Steps:**

1. Copy the updated `aieos-governance-foundation/governance-model.md` to each kit's `docs/governance-model.md`:
   - aieos-strategic-direction-kit
   - aieos-product-intelligence-kit
   - aieos-solution-sourcing-kit
   - aieos-engineering-execution
   - aieos-release-exposure-kit
   - aieos-reliability-resilience-kit
   - aieos-insight-evolution-kit
   - aieos-operational-diagnostics-kit
   - aieos-quality-assurance-kit
   - aieos-security-compliance-kit
   - aieos-data-configuration-kit
   - aieos-platform-infrastructure-kit
   - aieos-documentation-knowledge-kit
   - aieos-peer-review-kit
   - aieos-business-process-kit

2. For each kit, verify the copy matches exactly using `diff`.

3. Commit in each kit: `chore: sync governance-model.md to v1.7`

**Note:** This is mechanical — script it:
```bash
SRC="/mnt/c/Users/wtlin/projects/aieos/aieos-governance-foundation/governance-model.md"
for kit_dir in aieos-strategic-direction-kit aieos-product-intelligence-kit \
  aieos-solution-sourcing-kit aieos-engineering-execution \
  aieos-release-exposure-kit aieos-reliability-resilience-kit \
  aieos-insight-evolution-kit aieos-operational-diagnostics-kit \
  aieos-quality-assurance-kit aieos-security-compliance-kit \
  aieos-data-configuration-kit aieos-platform-infrastructure-kit \
  aieos-documentation-knowledge-kit aieos-peer-review-kit \
  aieos-business-process-kit; do
  DEST="/mnt/c/Users/wtlin/projects/aieos/${kit_dir}/docs/governance-model.md"
  cp "$SRC" "$DEST"
  cd "/mnt/c/Users/wtlin/projects/aieos/${kit_dir}"
  git add docs/governance-model.md
  git commit --author='Todd <5351073+wtlinnertz@users.noreply.github.com>' \
    -m 'chore: sync governance-model.md to v1.7'
  git push origin main
done
```

---

### Task 2.3: EEK repo name corrections in entry-from-eek.md files across kits

**What:** Every kit that has a cross-kit reference to EEK uses the wrong repo name `aieos-engineering-execution-kit`. These appear in `entry-from-eek.md` doc headers across multiple kits.

**Grep first to find all occurrences:**
```bash
grep -rl 'aieos-engineering-execution-kit' /mnt/c/Users/wtlin/projects/aieos/ \
  --include='*.md' | grep -v '.git'
```

For each file found, replace `aieos-engineering-execution-kit` with `aieos-engineering-execution`.

**Commit per kit:** `docs: correct EEK repo name reference (aieos-engineering-execution)`

---

### Task 2.4: PIK README — correct WCR governance status

**What:** FIX-06. PIK README describes WCR in language that implies it is a utility prompt. It is a governed artifact with all four files.

**File:** `aieos-product-intelligence-kit/README.md`

Find the WCR description paragraph and replace with:

```markdown
**WCR — Work Classification Record** (Step 0)

WCR is a governed artifact with its own spec, template, prompt, and validator.
It is required — every initiative entering PIK begins with a WCR. The WCR
classification decision determines whether the work enters full discovery, is
routed directly to EEK, or is handled through incident management. The frozen
WCR is referenced by the EEK KER as confirmation of the routing decision.
```

Remove any language that calls WCR a "utility prompt" or lists it alongside non-governed prompts.

**Commit:** `docs(pik): correct WCR governance status — governed artifact, not utility prompt`

---

### Task 2.5: REK README — correct artifact count

**What:** FIX-07. REK README header states "3 governed artifact types." Actual count is 5: RER, RCF, RSA, RP, RR.

**File:** `aieos-release-exposure-kit/README.md`

Change "3 governed artifact types" to "5 artifact types: RER (entry gate), RCF, RSA, RP, RR."

Also verify the artifact list in the README body matches all 5 and that RSA is represented.

**Commit:** `docs(rek): correct artifact count to 5 — include RSA`

---

### Task 2.6: Add conditional BPK RC gate to REK release-entry-spec (Significant spec change)

**What:** FIX-08. When BPK was adopted for an initiative, its RC (Readiness Confirmation) must be frozen before REK entry is authorized. Currently the RER spec has no check for this — the coupling is advisory only.

**Spec version:** v1.0 → v1.1 (Significant — new conditional hard gate)

**Files to change:**

1. `aieos-release-exposure-kit/docs/specs/release-entry-spec.md` — v1.0 → v1.1, add gate
2. `aieos-release-exposure-kit/docs/validators/release-entry-validator.md` — add check
3. `aieos-release-exposure-kit/docs/artifacts/release-entry-template.md` — add BPK field

**In release-entry-spec.md, in the Upstream Dependencies section, add:**
```markdown
- Frozen Readiness Confirmation (RC) from the Business Process Kit — required if BPK
  was adopted for this initiative (i.e., if a PIA was generated for this initiative).
  If BPK was not adopted, state explicitly in §Completeness Checklist:
  "BPK not adopted for this initiative — process impact confirmed as none."
```

**New hard gate to add to release-entry-spec.md:**
```markdown
### bpk_rc_status (conditional)

**Condition:** This gate applies only when BPK was adopted — i.e., a PIA was
generated for this initiative.

**Rule:** If BPK was adopted, a frozen RC must be present and its ID referenced
in the RER before this record may be frozen.

**Failure example:** BPK PIA generated for this initiative but RER frozen without
RC ID reference.

**When BPK was not adopted:** State "BPK not adopted" in §Completeness Checklist.
Gate passes automatically.
```

**In release-entry-validator.md, add:**
- Check §Completeness Checklist for either: (a) frozen RC ID is present, or (b) explicit "BPK not adopted" declaration
- FAIL if neither is present

**In release-entry-template.md, add to §Completeness Checklist:**
```
- [ ] BPK: [ ] Not adopted for this initiative | [ ] Adopted — RC ID: {RC-ID}, Status: Frozen
```

**Commit:** `feat(rek): add conditional BPK RC gate to release-entry-spec v1.1`

---

### Task 2.7: Reconcile PRK lens tables — create single authoritative table

**What:** FIX-09. Three PRK docs have different required/optional lens assignments per review point. CLAUDE.md is most complete; playbook and entry-from-eek.md are outdated.

**Files to change:**
1. `aieos-peer-review-kit/CLAUDE.md` — mark as authoritative source, no changes needed (already complete)
2. `aieos-peer-review-kit/docs/playbook.md` — update two rows: add `resilience` to Architecture Review required; add `observability` to Operational Readiness required
3. `aieos-peer-review-kit/docs/entry-from-eek.md` — align required lens list with CLAUDE.md

**In playbook.md, find the review point table and change:**
- Architecture Review row: add `resilience` to the Required column (currently absent)
- Operational Readiness row: add `observability` to the Required column (currently absent)

**Add a note at the top of the lens table in playbook.md:**
```
> Authoritative lens assignments are defined in CLAUDE.md. This table is a
> summary — if any discrepancy exists, CLAUDE.md governs.
```

**Commit:** `docs(prk): reconcile lens tables — playbook aligned with CLAUDE.md`

---

### Task 2.8: Tighten DCF spec entry gate (Significant spec change)

**What:** FIX-10. The DCF spec lists no upstream artifact preconditions. A DCF can be authored and frozen before SAD, violating the logical dependency. TDD requires both frozen SAD and frozen DCF — if DCF precedes SAD, TDD is generated without SAD constraints.

**Spec version:** v1.0 → v1.1 (Significant — new required upstream dependency)

**Files to change:**

1. `aieos-engineering-execution/docs/specs/dcf-spec.md` — v1.0 → v1.1, add upstream dependency
2. `aieos-engineering-execution/docs/validators/dcf-validator.md` — add upstream check

**In dcf-spec.md, in Upstream Dependencies, change:**
```
- Engineering standards, testing expectations, or operational requirements (if provided)
```
to:
```
- Frozen PRD — required. The DCF must reflect the same initiative scope as the PRD it governs.
- Frozen SAD — required when SAD has been generated for this initiative. DCF must not be
  frozen before SAD, as the DCF constrains TDD which depends on both SAD and DCF.
  Exception: when DCF is a reused organizational standard (not initiative-specific), it
  may precede SAD. The KER must document this reuse pattern.
- Engineering standards, testing expectations, or operational requirements (if provided)
```

**Add new hard gate to dcf-spec.md:**
```markdown
### upstream_dependency_ordering

**Rule:** If a SAD exists for this initiative, it must be in Frozen status before this
DCF may be frozen. The DCF may not constrain a TDD without the SAD having defined the
system architecture first.

**Exception:** Reusable organizational-level DCFs (covering all delivery, not a single
initiative) may be frozen before SAD. The KER for the initiative must note that DCF
is reused from a prior initiative or is an organizational standard.

**Failure example:** DCF frozen before SAD for the same initiative.
```

**In dcf-validator.md, add:**
- Check that either: (a) SAD ID is referenced and confirmed Frozen, or (b) §Document Control notes DCF is a reusable organizational standard with a reference to the KER that documents the exception.
- FAIL if neither condition is met.

**Commit:** `feat(eek): add upstream dependency ordering gate to DCF spec v1.1`

---

### Task 2.9: Clarify SDK Layer 1 status in SDK README and governance-model.md

**What:** FIX-11. "Not yet in standard flow" language implies Layer 1 is unfinished or not yet wired. It is complete and may be used today. The phrasing should clarify when to engage it and when to skip it.

**Files to change:**
- `aieos-strategic-direction-kit/README.md` — replace ambiguous status language
- (governance-model.md already updated in Task 2.1 wave — no second edit needed)

**In SDK README, replace any "not yet in standard flow" or similar language with:**
```
Layer 1 is optional for all initiatives. Engage when:
  - Portfolio-level prioritization across competing bets is needed
  - Multiple potential initiatives are competing for the same capacity
  - Strategic alignment documentation is required for investment decisions

Skip when:
  - The initiative direction is settled and no competing bets exist
  - The work is an enhancement to an existing bet already in flight
  - An incident or defect is driving the work (use EEK Path B or ODK instead)

When Layer 1 is skipped, the EEK KER or PIK Discovery Intake must document
the justification.
```

**Commit (SDK repo):** `docs(sdk): clarify Layer 1 engagement conditions — replace ambiguous status language`

---

## Phase 3 — Medium Priority Fixes

*Structural enforcement gaps, infrastructure gaps, and orphaned content.*

---

### Task 3.1: Add conditional PINFK check to EEK ACF spec

**What:** FIX-12. PINFK artifacts (PDR, ISPEC) must precede EEK ACF logically, but no EEK spec enforces this. When PINFK is adopted, its artifacts should be referenced in ACF.

**Spec version:** acf-spec.md v1.0 → v1.1 (Significant)

**Files to change:**
1. `aieos-engineering-execution/docs/specs/acf-spec.md`
2. `aieos-engineering-execution/docs/validators/acf-validator.md`
3. `aieos-engineering-execution/docs/artifacts/acf-template.md`

**Add to acf-spec.md Upstream Dependencies:**
```markdown
- Frozen PDR(s) and ISPEC from PINFK (Platform & Infrastructure Kit) — required if PINFK
  was adopted for this initiative. If PINFK was not adopted, state "PINFK not adopted"
  in §Platform Context. Absent PINFK artifacts means platform decisions are being made
  as assumptions within ACF; these assumptions must be stated explicitly in §Platform Context.
```

**New conditional gate:**
```markdown
### pinfk_reference_or_explicit_assumptions

**Rule:** The ACF must do one of the following:
  (a) Reference frozen PDR and ISPEC IDs from PINFK in §Platform Context, OR
  (b) State explicitly "PINFK not adopted — platform assumptions are:" followed by
      the specific platform/infrastructure assumptions the ACF is making.

**Failure example:** §Platform Context is blank or says "TBD."
```

**Commit:** `feat(eek): add PINFK reference gate to ACF spec v1.1`

---

### Task 3.2: Document DCK dual trigger structure clearly

**What:** FIX-13. DCK has two distinct trigger classes that behave differently: EEK-triggered (CSPEC, DSR after TDD) and REK-triggered (FFLR during release). The README and CLAUDE.md present this as one uniform flow, creating confusion for pipeline runners and operators.

**Files to change:**
1. `aieos-data-configuration-kit/README.md` — add trigger summary table
2. `aieos-data-configuration-kit/CLAUDE.md` — add explicit trigger class split

**Add to DCK README (after the artifact list, before the flow section):**
```markdown
## Trigger classes

DCK artifacts have two distinct trigger points from two different upstream kits:

| Artifact | Triggered by | Upstream kit | Timing |
|----------|-------------|--------------|--------|
| CSPEC | TDD frozen (with config items) | EEK Layer 4 | During EEK, parallel with pipeline |
| DSR | TDD frozen (with data models) | EEK Layer 4 | During EEK, parallel with pipeline |
| FFLR | Feature flags created | REK Layer 5 | During REK execution, after release begins |
| DMR | DSR frozen with migration needed | DCK itself | After DSR, before migration runs |

CSPEC and DSR are EEK-phase artifacts. FFLR is a REK-phase artifact. Do not generate
FFLR during EEK — no feature flags exist yet at that point.
```

**Commit:** `docs(dck): document dual trigger structure — EEK phase vs REK phase artifacts`

---

### Task 3.3: Define DHR trigger criteria in DHR spec

**What:** FIX-14. DHR has a vague "periodic" trigger with no defined cadence or responsible owner. Every other AIEOS artifact has a specific trigger event. DHR needs one too.

**Spec version:** dhr-spec.md — current version to be checked; bump to next minor version.

**Files to change:**
1. `aieos-documentation-knowledge-kit/docs/specs/dhr-spec.md`

**Add to Upstream Dependencies / Trigger section:**
```markdown
### Trigger

DHR is triggered by one of the following events (whichever comes first):
  (a) The documentation owner for this initiative reaches the third RHR cycle for the
      monitored system (i.e., three RHRs have been frozen since the last DHR or initial
      documentation release)
  (b) A major release (RR) is frozen that adds, removes, or substantially changes user-
      facing capabilities — indicating that documentation coverage may have drifted
  (c) The documentation owner determines documentation quality has degraded based on
      support escalations, user feedback, or coverage gaps observed during ARR or UDR reviews

**Responsible owner:** The documentation owner named in the Engagement Record §13
(DKK section). If no ER §13 entry exists, the release owner from the most recent RR
is responsible for initiating DHR.

**Cadence floor:** DHR must occur at least once per year for any system with a frozen UDR
or ARR. Annual cadence is the minimum; event-based triggers may produce more frequent reviews.
```

**Commit:** `feat(dkk): define DHR trigger criteria and responsible owner in spec`

---

### Task 3.4: Add SSK skip justification as EEK KER hard gate

**What:** FIX-15. The KER spec's Entry Path section requires SSK bypass justification only through prose guidance, not as a hard gate. The validator passes KERs without it.

**Spec version:** kit-entry-spec.md v1.0 → v1.1 (Significant)

**Files to change:**
1. `aieos-engineering-execution/docs/specs/kit-entry-spec.md`
2. `aieos-engineering-execution/docs/validators/kit-entry-validator.md`
3. `aieos-engineering-execution/docs/artifacts/kit-entry-template.md`

**In kit-entry-spec.md, in the Entry Path section, add a new hard gate:**
```markdown
### ssk_disposition (conditional)

**Condition:** This gate applies when Entry Path A is selected (initiative came through PIK).

**Rule:** The KER must declare one of:
  (a) "SSK was engaged — SDR ID: {SDR-ID}, frozen."
  (b) "SSK was skipped — Justification: {specific reason}." Justification must address
      why Build is the only viable option without an evaluation of alternatives. Acceptable
      justifications: unique domain capability with no market alternatives; enhancement to
      an existing system with no sourcing decision needed; compliance/regulatory mandate
      specifying specific approach. Unacceptable: "we decided not to evaluate vendors" or
      "time pressure."

**Failure example:** Path A KER with no SSK disposition statement.
```

**In kit-entry-validator.md, add:**
- For Path A KERs: check for SSK disposition statement per spec rule above
- FAIL if Path A is selected and no SSK disposition is present

**In kit-entry-template.md, add to §Entry Path:**
```
SSK disposition: [ ] SSK engaged — SDR ID: ___
                 [ ] SSK skipped — Justification: ___
```

**Commit:** `feat(eek): add SSK skip justification gate to KER spec v1.1`

---

### Task 3.5: Add 13 PRK lens tool schemas to aieos-schema

**What:** FIX-16. The schema repo has 1 PRK schema (PRR). The 13 lens tools each have 4 governing files but no schemas. The README claims 68 total schemas and 391 gates — both are understated.

**Files to change:**
1. `aieos-schema/schema/` — 13 new YAML files (one per lens)
2. `aieos-schema/README.md` — update counts from 68 → 81 schemas, update gate count

**Lens tool names to create schemas for:**
review-security, review-reliability, review-performance, review-cost, review-operability,
review-maintainability, review-compliance, review-devex, review-business-value,
review-accessibility, review-observability, review-resilience, review-adversarial

**Schema template for each lens (example for review-security):**
```yaml
artifact_type: REVIEW-SECURITY
kit: PRK
layer: 14
spec_version: "v1.0"
entry_gate: false

hard_gates:
  - name: scope_defined
    rule: "Review scope explicitly states which artifact is under review and which system/component boundary applies"
  - name: findings_documented
    rule: "Each finding includes: category, severity (critical/high/medium/low/info), description, and location reference"
  - name: verdict_declared
    rule: "Review declares PASS or FAIL at the lens level with explicit rationale"
  - name: no_suggestions_only_findings
    rule: "Review does not offer improvement suggestions without corresponding findings; suggestions without findings are out of scope"
  # adversarial lens adds: minimum_findings_count (unique hard gate)

required_sections:
  - Review Scope
  - Findings
  - Verdict

file_paths:
  spec: aieos-peer-review-kit/docs/specs/review-security-spec.md
  template: aieos-peer-review-kit/docs/artifacts/review-security-template.md
  prompt: aieos-peer-review-kit/docs/prompts/review-security-prompt.md
  validator: aieos-peer-review-kit/docs/validators/review-security-validator.md

upstream_dependencies:
  - artifact_type: PRR
    relationship: aggregated_into

downstream_consumers:
  - artifact_type: PRR
    relationship: feeds

metadata:
  description: "Security lens for Peer Review Kit — assesses threat surface, authentication, authorization, data protection, and secure communication patterns"
```

**Steps:**
1. For each of the 13 lenses, create a schema file in `aieos-schema/schema/prk/`. Use the template above with lens-appropriate hard gates extracted from each lens spec file.
2. Before creating: read each lens spec file in `aieos-peer-review-kit/docs/specs/` to get the correct hard gates.
3. The adversarial lens schema must include a `minimum_findings_required` hard gate (the unique inverted gate).
4. Update `aieos-schema/README.md` schema count: 68 → 81; update gate count by adding up gates from all 13 new schemas.
5. Update validation test to include PRK lens schemas in completeness check.

**Commit:** `feat(schema): add 13 PRK lens tool schemas — total 81 schemas`

---

### Task 3.6: Pipeline runner and console README status notices

**What:** FIX-17, FIX-18. Infrastructure repos should clearly surface what is and is not operational.

**Files to change:**
1. `aieos-pipeline-runner/README.md` — add M3 status header
2. `aieos-console/README.md` — add cross-cutting kit coverage table

**In pipeline-runner README, add at the top (after the title):**
```markdown
> **Implementation status:** Scaffolding. Core architecture and validators are in place
> but use stub/mock implementations. Real adapter execution lands in M3 (June 2026 target).
> Use `--use-mock-adapters` for local validation of spec files. Do not use for production
> adapter execution until M3 is complete.
```

**In console README, add a coverage table:**
```markdown
## Kit coverage

| Kit | Layer | Console support |
|-----|-------|----------------|
| PIK | 2 | Complete |
| EEK | 4 | Complete |
| REK | 5 | Complete |
| RRK | 6 | In progress |
| QAK | 9 | Not yet — planned post-M3 |
| SCK | 10 | Not yet — planned post-M3 |
| DCK | 11 | Not yet — planned post-M3 |
| PINFK | 12 | Not yet — planned post-M3 |
| DKK | 13 | Not yet — planned post-M3 |
| PRK | 14 | Not yet — planned post-M3 |
| BPK | 15 | Not yet — planned post-M3 |

For kits without console support, run kit playbooks manually.
```

**Commit (pipeline-runner):** `docs(runner): add M3 implementation status notice`  
**Commit (console):** `docs(console): add kit coverage table — surface cross-cutting kit gaps`

---

### Task 3.7: Resolve DKR orphan in EEK

**What:** FIX-19. EEK CLAUDE.md references a DKR artifact (dkr-spec.md). It is not in the main artifact flow, not in the schema repo, and has no entry in any kit's entry-from-*.md. Needs resolution.

**Steps:**
1. Read `aieos-engineering-execution/docs/specs/dkr-spec.md` in full
2. Determine status: Is it referenced by any prompt, validator, or template in EEK?

```bash
grep -rl 'DKR\|dkr' /mnt/c/Users/wtlin/projects/aieos/aieos-engineering-execution/ \
  --include='*.md' | grep -v '.git'
```

3. Decision tree:
   - If DKR is referenced nowhere other than dkr-spec.md and CLAUDE.md: mark as removed artifact. Archive it to `docs/specs/archived/` and remove from CLAUDE.md.
   - If DKR is referenced in a prompt or validator but not in the main flow: it is a supporting utility, not a governed artifact. Move to `docs/tools/` and update references.
   - If DKR has a defined role but was never wired: add a milestone tag to the spec and add to CLAUDE.md under "Planned artifacts (not yet in flow)."

4. Update CLAUDE.md to reflect the DKR decision.

**Commit:** `chore(eek): resolve DKR artifact status — [archive/classify/plan per decision]`

---

### Task 3.8: Add IEK entry gate exception documentation

**What:** FIX-20. IEK is the only kit with no human-authored entry gate artifact. This is intentional by design (IEK triggers from objective artifact count, not a human routing decision). But it is not documented as an intentional exception.

**Recommendation:** Document the exception explicitly rather than adding an entry gate artifact (which would be artificial — the trigger is automatic and objective).

**Files to change:**
1. `aieos-governance-foundation/governance-model.md` — add IEK exception note to entry gate rules
2. `aieos-insight-evolution-kit/README.md` — add explanation
3. `aieos-governance-foundation/docs/layer-model.md` — add IEK trigger note

**In governance-model.md, in the entry gate rules section, add:**
```markdown
**Exception — IEK (Layer 7):** The Insight & Evolution Kit has no human-authored entry gate
artifact. IEK engagement is triggered automatically when ≥2 Reliability Health Reports are
frozen for a service. The trigger is objective and quantitative — human judgment is exercised
at the ES freeze decision, not at kit entry. ES §1 confirms input artifact frozen status as
the entry gate check. This exception is intentional: adding a human-authored gate at IEK
entry would duplicate the trigger check without adding governance value.
```

**Commit (governance-foundation):** `docs(foundation): document IEK entry gate exception — intentional by design`
**Commit (IEK):** `docs(iek): clarify no entry gate by design — document trigger logic`

---

## Phase 4 — Low Priority Fixes (Governance Model v1.7 polish)

*These items improve meta-governance and long-term maintainability.*

---

### Task 4.1: Add Retroactive flag to Engagement Record template

**What:** FIX-21. Agent harness ER FINDING-1 identified that retroactively governed initiatives produce different artifacts but have no way to mark this in the ER.

**Files to change:**
1. `aieos-governance-foundation/governance-model.md` — add Retroactive field definition to ER spec section
2. The ER template in whichever kit owns it (check `aieos-governance-foundation` or `aieos-agent-harness`)

**Add to ER Document Control field definitions:**
```markdown
| Retroactive | [ ] No — all artifacts generated prospectively during the initiative
              [ ] Yes — some or all artifacts generated retrospectively after work was complete.
                  If Yes: note which artifact phases are retroactive and the rationale
                  for retroactive governance. |
```

**Commit:** `feat(er): add Retroactive field to Engagement Record Document Control`

---

### Task 4.2: Document IEK PES bootstrap requirement prominently

**What:** FIX-22. PES requires ≥2 complete initiative cycles. New adopters discover this only when they hit the gate. Add a visible notice.

**Files to change:**
1. `aieos-insight-evolution-kit/README.md` — add bootstrap note
2. `aieos-governance-foundation/docs/getting-started.md` — add under onboarding guidance

**In IEK README, add a callout:**
```markdown
> **PES bootstrap note:** The Portfolio Evolution Signal (PES) requires ≥2 frozen Engagement
> Records from ≥2 separate initiatives. It is unavailable until at least two complete
> initiative cycles have run under AIEOS governance. This is by design — portfolio-level
> synthesis requires multiple data points. Plan for PES to be available after your second
> complete initiative.
```

**Commit:** `docs(iek): add PES bootstrap requirement callout`

---

### Task 4.3: Document agent-harness REK/RRK exemption

**What:** FIX-23. The agent harness was not put through REK/RRK under its own framework. This should be documented as a known exemption, not a silent gap.

**Files to change:**
1. `aieos-agent-harness` Engagement Record — add exemption note to ER §REK/RRK section
2. `aieos-governance-foundation/docs/getting-started.md` — add bootstrapping note for tooling repos

**In agent-harness ER, in the REK/RRK section:**
```markdown
**Exemption status:** REK and RRK not engaged for this initiative. Rationale: the agent
harness was developed as bootstrapping infrastructure for AIEOS itself. Prospective
governance of the harness using the harness is a bootstrapping constraint. The harness
has been tested (143+ tests), peer-reviewed (M7 operator guide), and is operationally
monitored informally. Full REK/RRK governance is planned for v2.0 when the harness
is used to govern its own next major version.
```

**Commit (agent-harness):** `docs(er): document REK/RRK exemption with bootstrapping rationale`

---

### Task 4.4: Add ER section completeness field

**What:** FIX-24. ER sections can be left incomplete when a kit engagement closes. No enforcement exists.

**Files to change:**
1. `aieos-governance-foundation/governance-model.md` — add completeness field to ER section spec
2. ER template (wherever it lives)

**Add a Completeness field to each ER kit section:**
```markdown
Each kit section in the ER must include a closing line:
  Kit section complete: [ ] Yes — all artifacts frozen; section reflects final state
                        [ ] No — in progress; final artifact: {artifact-type} is {status}
                        [ ] Not adopted — explicitly declined; reason documented above
```

**Commit:** `feat(er): add per-section completeness field to ER template`

---

### Task 4.5: Surface adversarial lens unique behavior in PRK README

**What:** FIX-25. The adversarial lens has an inverted hard gate (FAIL when no findings). This is undocumented at the PRK or framework level.

**Files to change:**
1. `aieos-peer-review-kit/README.md` — add adversarial lens callout in lens overview section
2. `aieos-governance-foundation/governance-model.md` — add note to §Validator Output Format

**In PRK README lens overview, add:**
```markdown
> **Adversarial lens — unique behavior:** The adversarial lens has a minimum findings
> requirement. A review that surfaces zero adversarial findings FAILS. This is intentional:
> every system has an adversarial surface; a reviewer who finds nothing has not looked hard
> enough. The minimum count is defined in the adversarial-lens spec. This is the only lens
> where finding nothing is a failure condition.
```

**In governance-model.md §Validator Output Format:**
```markdown
**Exception:** The PRK adversarial lens validator inverts the standard PASS/FAIL logic
for completeness — it FAILS when findings are absent because the absence of adversarial
findings indicates incomplete review, not a clean system. This is the only exception to
the "no findings = PASS" rule in AIEOS.
```

**Commit (prk):** `docs(prk): surface adversarial lens inverted PASS/FAIL in README`  
**Commit (foundation):** `docs(foundation): note adversarial lens exception to validator output format rule`

---

## Phase 5 — Final Verification

### Task 5.1: Run TOOL-KIT-SYNC-AUDIT

**What:** governance-model.md §15 change protocol step 6 requires running TOOL-KIT-SYNC-AUDIT (scope: `sync-files-only`) after governance-model.md changes to verify all kit copies match exactly.

**Steps:**
1. Run the kit-sync-audit tool per its binding in `docs/bindings/kit-sync-audit-claude-code.md`
2. Verify all 15 kit copies of `docs/governance-model.md` match the foundation copy exactly
3. If any discrepancy: re-run the sync for that kit (Task 2.2 script)
4. Record sync verification in findings/: `findings/governance-model-v1.7-sync-verification.md`

---

### Task 5.2: Audit schema counts in aieos-schema README

**What:** After adding 13 lens schemas (Task 3.5), verify README counts are accurate.

**Steps:**
1. Count actual schema files: `find /mnt/c/Users/wtlin/projects/aieos/aieos-schema/schema -name '*.yaml' | wc -l`
2. Count actual gates: `grep -c 'name:' $(find /mnt/c/Users/wtlin/projects/aieos/aieos-schema/schema -name '*.yaml')`
3. Verify README counts match
4. Run schema validation tests: `cd /mnt/c/Users/wtlin/projects/aieos/aieos-schema && PYTHONPATH=. pytest tests/ -v`

---

### Task 5.3: Spec version consistency check

**What:** Every spec changed in this plan had its version bumped. Verify no spec was edited without a version bump.

**Steps:**
For each spec file touched by this plan, verify:
- vp-spec.md: v1.1 ✓
- release-entry-spec.md: v1.1 ✓
- dcf-spec.md: v1.1 ✓
- kit-entry-spec.md: v1.1 ✓
- acf-spec.md: v1.1 ✓
- dhr-spec.md: version bumped ✓

All validator, prompt, and template files paired with these specs do not have separate version headers — they are governed by the spec version. No additional version tracking needed for them.

---

### Task 5.4: Commit audit report update

**What:** Update the original audit report in `findings/` to mark all 25 issues as closed, referencing the commit that closed each one.

**File:** `aieos-governance-foundation/findings/aieos-framework-audit-2026-05-17.md`

Add a §6 Closure Log table at the end:
```markdown
## Section 6: Closure Log

| Issue | Severity | Closing commit | Phase | Date closed |
|-------|----------|----------------|-------|-------------|
| ISSUE-01 | Critical | {commit hash} | 1 | 2026-05-XX |
...
```

**Commit:** `docs(audit): mark all 25 issues closed with commit references`

---

## Change Summary Table

| Task | Fix(es) | Repos affected | Spec version bumps | Commits |
|------|---------|----------------|--------------------|---------|
| 1.1 | ISSUE-01 | governance-foundation | none (doc addition) | 1 |
| 1.2 | ISSUE-02 | governance-foundation, QAK | none | 2 |
| 1.3 | ISSUE-03 | QAK | vp-spec v1.0→v1.1 | 1 |
| 2.1 | ISSUE-04, -05, -11 | governance-foundation | none | 1 |
| 2.2 | (cascade) | all 15 kit repos | none | 15 |
| 2.3 | ISSUE-05 | kits with EEK refs | none | N (per kit) |
| 2.4 | ISSUE-06 | PIK | none | 1 |
| 2.5 | ISSUE-07 | REK | none | 1 |
| 2.6 | ISSUE-08 | REK | release-entry-spec v1.0→v1.1 | 1 |
| 2.7 | ISSUE-09 | PRK | none | 1 |
| 2.8 | ISSUE-10 | EEK | dcf-spec v1.0→v1.1 | 1 |
| 2.9 | ISSUE-11 | SDK | none | 1 |
| 3.1 | ISSUE-12 | EEK | acf-spec v1.0→v1.1 | 1 |
| 3.2 | ISSUE-13 | DCK | none | 1 |
| 3.3 | ISSUE-14 | DKK | dhr-spec version bump | 1 |
| 3.4 | ISSUE-15 | EEK | kit-entry-spec v1.0→v1.1 | 1 |
| 3.5 | ISSUE-16 | aieos-schema | none | 1 |
| 3.6 | ISSUE-17, -18 | pipeline-runner, console | none | 2 |
| 3.7 | ISSUE-19 | EEK | none (TBD per DKR investigation) | 1 |
| 3.8 | ISSUE-20 | governance-foundation, IEK | none | 2 |
| 4.1 | ISSUE-21 | governance-foundation | none | 1 |
| 4.2 | ISSUE-22 | IEK | none | 1 |
| 4.3 | ISSUE-23 | agent-harness | none | 1 |
| 4.4 | ISSUE-24 | governance-foundation | none | 1 |
| 4.5 | ISSUE-25 | PRK, governance-foundation | none | 2 |
| 5.1–5.4 | Verification | governance-foundation, schema | none | 1 |

**Total commits:** ~45  
**Spec version bumps:** 5 specs (vp, release-entry, dcf, kit-entry, acf) + dhr  
**Governance model version:** 1.6 → 1.7  
**Repos touched:** 21 of 40 (governance-foundation, 15 kit repos for sync, EEK, QAK, REK, PRK, PIK, SDK, DCK, DKK, IEK, aieos-schema, pipeline-runner, console, agent-harness)

---

## What This Plan Does Not Change

To be explicit about scope boundaries:

- **No artifact content changes** — no frozen or in-progress artifact documents are modified
- **No new artifact types added** — Trigger 5 is a governance definition, not an artifact type
- **No validator logic changes beyond the 5 new conditional gates** — existing gates are untouched
- **No prompt content rewrites** — prompts are updated only to add new conditional halt instructions where specs add new gates
- **No kit SDLC changes** — kit versioning is not changed; the changes are clarifications and additions, not breaking restructures
- **No cross-kit dependency additions** — the conditional gates added (PINFK in ACF, BPK RC in RER, SCK ordering in VP, DCF upstream in dcf-spec) are all conditions that formalize already-stated intent, not new constraints

---

*Plan saved to: /home/todd/.hermes/plans/2026-05-17-aieos-gap-closure.md*  
*Source audit: aieos-governance-foundation/findings/aieos-framework-audit-2026-05-17.md*
