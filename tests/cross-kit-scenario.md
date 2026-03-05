# Cross-Kit Scenario: Frozen DPRD → EEK Kit Entry → PRD Acceptance

This scenario covers the complete cross-kit handoff interface between the Product Intelligence Kit (PIK) and the Engineering Execution Kit (EEK). It exercises both kits' four-file systems at their shared boundary: the Discovery PRD.

This is an integration scenario. Each step references the governing files from the relevant kit. The scenario assumes both kits are available and the DPRD has passed PIK validation.

---

## Scenario Overview

**What:** A frozen, PIK-validated Discovery PRD is handed off to the EEK. The EEK team completes a Kit Entry Record, runs the PRD acceptance check, and begins the EEK artifact chain.

**Actors:** PIK team (produces DPRD), EEK team (receives DPRD, runs intake gate and acceptance check)

**Preconditions:**
- PIK has produced a frozen DPRD with all 8 PIK hard gates passing (6 EEK gates + 2 PIK traceability gates)
- EL in the DPRD's Assumptions section includes EXP-N identifiers
- The EEK is available in a consuming project at the receiving organization

---

## Flow

| Step | Actor | Action | Kit | Files Used | Expected Output | Key Verifications |
|------|-------|--------|-----|------------|-----------------|-------------------|
| 1 | PIK team | Deliver frozen DPRD | PIK | Frozen DPRD | DPRD delivered to EEK team | No edits made to DPRD before or during delivery |
| 2 | EEK team | Place DPRD | EEK | — | `docs/sdlc/01-prd.md` in consuming project | File placed exactly as-is; no reformatting |
| 3 | EEK team | Complete Kit Entry Record — Path A | EEK | `kit-entry-template.md` | Kit Entry Record with: Record ID, date, work summary, classification check (WCR-2026-001 routes to EEK), Path A selected, DPRD reference (path to 01-prd.md), EL references confirmed Yes, priority reference, scope boundary | All 5 substantive sections non-empty; exactly one path selected |
| 4 | EEK team | Validate Kit Entry Record | EEK | `kit-entry-spec.md` + `kit-entry-validator.md` + Kit Entry Record | JSON: `"status": "PASS"` | All 5 hard gates pass: document_control, classification_check, path_selected (Path A: DPRD ref present, EL refs confirmed), priority_on_record, scope_bounded |
| 5 | EEK team | Freeze Kit Entry Record | EEK | — | Frozen Kit Entry Record | Human signs freeze declaration; no artifact generation may begin until this step |
| 6 | EEK team | Run PRD acceptance check | EEK | `prd-spec.md` + `prd-validator.md` + `01-prd.md` | JSON: `"status": "PASS"` (6 gates) | All 6 EEK PRD hard gates pass; extra DPRD traceability sections (PFD, VH, AR, EL references) do not trigger failures |
| 7 | EEK team | Save acceptance check result | EEK | — | `docs/sdlc/01-prd-validation.json` | Result saved alongside the PRD; PASS confirmed before proceeding |
| 8 | EEK team | Freeze PRD slot | EEK | — | PRD slot frozen | EEK begins ACF step; no further modification to 01-prd.md |

---

## Failure Paths

### Scenario A: Kit Entry Record FAIL

If the Kit Entry validator returns FAIL (e.g., EL references field is blank for Path A):
- EEK team corrects the Kit Entry Record
- Re-runs validation in a new session
- Does not proceed to PRD acceptance check until Kit Entry Record passes

### Scenario B: PRD Acceptance Check FAIL

If the EEK `prd-validator.md` returns FAIL on `01-prd.md`:
- The issue belongs in the DPRD — EEK does NOT modify the DPRD
- EEK team returns the DPRD to the PIK team with the validator output
- PIK team applies the PIK re-entry protocol: corrects the DPRD, re-validates against PIK spec, re-freezes
- PIK team re-delivers the corrected DPRD
- EEK team re-runs the PRD acceptance check from step 6

### Scenario C: EL References Absent (Kit Entry Path A — No field)

If the Kit Entry Record Path A section has the EL references field blank (neither Yes checked nor No with explanation):
- Kit Entry validator FAILs `path_selected` gate
- Blocking issue: Path A selected with no EL references field completed
- EEK team must update the Kit Entry Record: either confirm Yes (references are present in DPRD Assumptions section) or explain why EL references are absent
- Re-validate before proceeding

---

## Key Verifications for the Cross-Kit Interface

1. **DPRD is not regenerated** — the EEK `prd-prompt.md` is not invoked for Path A; the DPRD is placed directly as `01-prd.md`
2. **Kit Entry Record gates artifact generation** — the acceptance check may not run until the Kit Entry Record is frozen and validated
3. **EEK PRD validator evaluates only EEK gates** — it does not re-evaluate PIK traceability gates (upstream_traceability, no_scope_expansion); those were evaluated during PIK validation and their outputs are on record in PIK
4. **Path A EL confirmation is structural, not a re-evaluation** — the Kit Entry Record asks whether EL references are present in the DPRD Assumptions section; it does not re-evaluate the quality of the experiments (that was done by PIK gate 7)
5. **Corrections to the DPRD belong in PIK** — if the EEK PRD acceptance check fails, the fix happens in PIK, not in the consuming project

---

## Governing Files by Kit

| File | Kit | Role in this scenario |
|------|-----|-----------------------|
| `discovery-prd-spec.md` | PIK | Defines the 8 DPRD hard gates (including 6 EEK gates) — evaluated before handoff |
| `discovery-prd-validator.md` | PIK | Validated DPRD before handoff; result on record in PIK |
| `kit-entry-spec.md` | EEK | Defines Kit Entry gate — evaluated at step 4 |
| `kit-entry-validator.md` | EEK | Evaluates the completed Kit Entry Record — step 4 |
| `kit-entry-template.md` | EEK | Structure for the Kit Entry Record — step 3 |
| `prd-spec.md` | EEK | Defines the 6 EEK PRD gates — evaluated at step 6 |
| `prd-validator.md` | EEK | Runs acceptance check on the DPRD as `01-prd.md` — step 6 |

---

## Reference

- PIK: `docs/playbook.md` §Downstream Handoff
- PIK: `examples/cross-kit/README.md` — step-by-step handoff mechanics with sample outputs
- EEK: `docs/playbook.md` §PRD Entry Paths (Path A) and §Cross-Kit Re-Entry Protocol
- EEK: `docs/specs/kit-entry-spec.md` — Kit Entry gate rules
- aieos-spec: `docs/layer-model.md` — Layer 2 (PIK) → Layer 4 (EEK) interface
