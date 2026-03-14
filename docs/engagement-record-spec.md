# Engagement Record Spec

## Purpose

This document defines the format, section rules, and maintenance responsibilities for the Engagement Record (ER). The ER is a project-level artifact — it lives in the consuming project, not in any kit, and is maintained incrementally by operators as work passes through each AIEOS layer.

The ER is not governed by a four-file system. It has no generation prompt or validator. It is an operational index: a structured record of every artifact ID, key decision, and outcome for a single initiative across all layers.

---

## Authority

This spec is the canonical definition of the ER format. It lives in `aieos-governance-foundation` because ERs span all layers — no single kit should own a cross-layer standard.

---

## Location and Naming

| Field | Value |
|-------|-------|
| Location | `{project}/docs/engagement/er-{initiative}.md` |
| ID format | `ER-{INITIATIVE}-{NNN}` |
| Example | `ER-TASKFLOW-001` |

`INITIATIVE` is a short uppercase identifier for the initiative or service (e.g., `TASKFLOW`, `PAYMENTS-API`, `NOTIFICATIONS`).

---

## ER Sections

### §1 Document Control

| Field | Value |
|-------|-------|
| ER ID | ER-{INITIATIVE}-{NNN} |
| Initiative | {full initiative name} |
| Service(s) | {service name(s) this initiative delivers to or creates} |
| Status | Active / Deprecated / Abandoned |
| Discovery Start | {YYYY-MM-DD — date Discovery Intake was validated in PIK} |
| Latest ES Date | {YYYY-MM-DD — date of most recent frozen ES, or N/A} |
| ER Spec Version | 1.4 |
| Current Position | {Navigation map node ID, e.g., N-EEK-TDD — updated by position-check tool. Optional.} |
| Preset | {P1–P5 or Custom — declared at initiative start} |

**Status values:**
- `Active` — initiative is in progress or in production and under monitoring
- `Deprecated` — initiative completed its lifecycle; the service is no longer active (matches DN type: Deprecated)
- `Abandoned` — initiative was cancelled before completion (matches DN type: Abandoned)

When status changes to `Deprecated` or `Abandoned`, add a `Deprecation Notice` field pointing to the DN ID.

---

### §1a Layer 1 — Strategic Direction (Optional)

This section is present only when the initiative originated from a governed strategic bet (SDK). Omit this section when SDK was not used.

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Strategic Bet Record | SBR-XXX | Frozen | |
| Portfolio Prioritization Record | PPR-XXX | Frozen | Above/below the line: {above/below} |

**Key decisions:**

List the strategic prioritization decision. Minimum entry: the PPR ranking position and cut line status.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

Example: `Priority: Ranked #2 of 5 bets, above the cut line with 1 team for 1 quarter allocation — PPR-001`

---

### §2 Layer 2 — Product Intelligence

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Work Classification Record | WCR-XXX | Frozen | |
| Discovery Intake | {date validated} | N/A | Human intake form — no artifact ID |
| Problem Framing Document | PFD-XXX | Frozen | |
| Value Hypothesis | VH-XXX | Frozen | |
| Assumption Register | AR-XXX | Frozen | |
| Experiment Log | EL-XXX | Frozen | |
| Discovery PRD | DPRD-XXX | Frozen | |

Add rows for Pivot Decision Records (PDR-XXX) if pivots occurred.

**Key decisions:**

List each significant decision made during Layer 2, with enough context to be useful without re-reading the full artifact. Minimum entries: pivot decisions.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

Example: `Pivot: Assumption A-03 (users will self-configure preferences) invalidated by user interviews — PDR-TASKFLOW-001`

---

### §3a Layer 3 — Solution Sourcing (if engaged)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Sourcing Options Evaluation Record | SOER-XXX | Frozen | |
| Vendor/Solution Evaluation Record | VER-XXX | Frozen | |
| Sourcing Decision Record | SDR-XXX | Frozen | Decision: Build / Buy / Adopt |

If Layer 3 was not engaged (fast-path to Build), write "SSK not engaged — fast-path Build justified in KER."

**Key decisions:**

List the sourcing decision and rationale. Minimum entries: the Build/Buy/Adopt decision with brief rationale.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

---

### §3 Layer 4 — Engineering Execution

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Kit Entry Record | KER-XXX | Frozen | Path A or Path B |
| Product Requirements Document | PRD-XXX | Frozen | |
| Architecture Context File | ACF-XXX | Frozen | |
| System Architecture Document | SAD-XXX | Frozen | |
| Domain Context File | DCF-XXX | Frozen | |
| Test Design Document | TDD-XXX | Frozen | |
| Work Decomposition Document | WDD-XXX | Frozen | |
| Operational Readiness Decision | ORD-XXX | Frozen | |

**Key decisions:**

List each significant decision made during Layer 4, with enough context to be useful without re-reading the full artifact. Minimum entries: architectural amendments, re-entry decisions, and any deviation from upstream PRD scope.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

**Gate failures (if any):**

List any hard gate failures encountered during Layer 4, and how they were resolved.

Format: `{artifact ID} / {gate name}: {brief description of failure} → {resolution}`

---

### §4 Layer 5 — Release & Exposure

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Release Entry Record | RER-XXX | Frozen | |
| Release Context File | RCF-XXX | Frozen | |
| Release Plan | RP-XXX | Frozen | |
| Release Record | RR-XXX | Frozen | |

**Release disposition:** Released / Rolled Back / Abandoned

If Rolled Back or Abandoned, add a brief note on cause.

**Key decisions:**

List each significant decision made during Layer 5, with enough context to be useful without re-reading the full artifact. Minimum entries: release type justification, deviations from the Release Plan during execution, and any gate failures or validator issues encountered.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

---

### §5 Layer 6 — Reliability & Resilience

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Service Reliability Entry Record | SRER-XXX | Frozen | |
| Service Reliability Profile | SRP-XXX vN | Frozen | Note current version |
| Incident Reports | IR-XXX, IR-XXX | Frozen | List all; N/A if none |
| Reliability Health Reports | RHR-XXX, RHR-XXX | Frozen | List all in order |

If the SRP has been revised, list all versions in the Notes column (e.g., `v1 → v2 on YYYY-MM-DD`).

**Key decisions:**

List each significant decision made during Layer 6, with enough context to be useful without re-reading the full artifact. Minimum entries: SRP revision decisions, error budget policy invocations, and any escalation trigger activations.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

---

### §6 Layer 7 — Insight & Evolution

**Artifact table:**

| ES ID | Coverage Period | Signal | VH Verdict |
|-------|----------------|--------|------------|
| ES-XXX | YYYY-MM-DD to YYYY-MM-DD | maintain / watch / re-discover | Validated / Invalidated / Partially Validated / Insufficient Data |

Add a row for each ES produced for this initiative. If no ES has been produced yet, write "No ES produced yet."

**Portfolio ESes:** If this initiative's ER has been included in a Portfolio Evolution Signal, note the PES ID in a separate row.

---

### §8 Layer 8 — Operational Diagnostics

**Artifact table:**

| Field | Artifact | Status | Notes |
|-------|----------|--------|-------|
| DCR ID | DCR | Frozen | Entry gate |
| INR ID(s) | INR | Frozen | List all INRs |
| PMR ID(s) | PMR | Frozen | List all PMRs |
| RB ID(s) | RB | Frozen | Runbooks codified; N/A if none |

Add a row for each DCR engagement (an incident may produce one DCR, one or more INRs, one PMR, and optionally one or more RBs). If no ODK engagement has been initiated for this initiative, write "No ODK engagement initiated."

---

### §9 Layer 9 — Quality Assurance (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Quality Assurance Entry Record | QAER-XXX | Frozen | |
| Verification Plan | VP-XXX | Frozen | |
| Test Campaign Record | TCR-XXX | Frozen | |
| Quality Gate Record | QGR-XXX | Frozen | Disposition: PASS / CONDITIONAL / FAIL |

**Quality disposition:** PASS / CONDITIONAL / FAIL

If CONDITIONAL, note the accepted risks. If FAIL, note the return-to-EEK decision.

If Layer 9 is not adopted for this initiative, write "QAK not adopted — direct ORD → REK handoff."

---

### §10 Layer 10 — Security & Compliance (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Threat Model | TM-XXX | Frozen | |
| Security Assessment Record | SAR-XXX | Frozen | |
| Compliance Evidence Record | CER-XXX | Frozen | N/A if no compliance mandate |
| Dependency Audit Record | DAR-XXX | Frozen | |

If Layer 10 is not adopted for this initiative, write "SCK not adopted for this initiative."

---

### §11 Layer 11 — Data & Configuration (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Configuration Specification | CSPEC-XXX | Frozen | |
| Feature Flag Lifecycle Record | FFLR-XXX | Frozen | Note current version |
| Data Schema Record | DSR-XXX | Frozen | Note current version |
| Data Migration Record | DMR-XXX | Frozen | N/A if no migration required |

If the FFLR or DSR has been re-frozen, list all versions in the Notes column. If no data migration is required, write "DMR not required — DSR schema changes are purely additive" in the Notes column.

If Layer 11 is not adopted for this initiative, write "DCK not adopted for this initiative."

---

### §12 Layer 12 — Platform & Infrastructure (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Platform Decision Record(s) | PDR-XXX | Frozen | List all PDRs |
| Infrastructure Specification | ISPEC-XXX | Frozen | Note current version |
| Environment Matrix | EM-XXX | Frozen | Note current version |

If the ISPEC or EM has been re-frozen, list all versions in the Notes column.

If Layer 12 is not adopted for this initiative, write "PINFK not adopted for this initiative."

---

### §13 Layer 13 — Documentation & Knowledge (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| User Documentation Record | UDR-XXX | Frozen | Per released capability |
| API Reference Record | ARR-XXX | Frozen | Per public API |
| Support Knowledge Article(s) | SKA-XXX | Frozen | List all SKAs |
| Documentation Health Review | DHR-XXX | Frozen | Note review period |

If the DHR has been re-frozen (periodic reviews), list all versions in the Notes column.

If Layer 13 is not adopted for this initiative, write "DKK not adopted for this initiative."

---

### §14 Layer 14 — Peer Review (if adopted)

**Artifact table:**

| Review Point | PRR ID | Artifact Reviewed | Status | Disposition | Notes |
|-------------|--------|-------------------|--------|-------------|-------|
| Architecture Review | PRR-XXX | SAD-XXX | Frozen | PASS / FAIL | |
| Technical Design Review | PRR-XXX | TDD-XXX | Frozen | PASS / FAIL | |
| Code Review | PRR-XXX | ORD-XXX | Frozen | PASS / FAIL | |

Add a row for each PRR produced. Disposition must be PASS for the reviewed artifact to freeze.

If Layer 14 is not adopted for this initiative, write "PRK not adopted for this initiative."

---

### §15 Layer 15 — Business Process (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Process Impact Assessment | PIA-XXX | Frozen | |
| Transition Plan | TP-XXX | Frozen | |
| Readiness Confirmation | RC-XXX | Frozen | Readiness: Ready / Ready-with-conditions / Not Ready |

If Layer 15 is not adopted for this initiative, write "BPK not adopted for this initiative."

---

### §7 Initiative Outcome

| Field | Value |
|-------|-------|
| Current Status | Active / Deprecated / Abandoned |
| Deprecation/Abandonment Notice | DN-XXX or N/A |
| Final Re-Entry Signal | maintain / watch / re-discover / N/A (if no ES yet) |
| Final VH Verdict | Validated / Invalidated / Partially Validated / Insufficient Data / N/A |
| Notes | {any context useful for portfolio synthesis — e.g., "initiative pivoted twice; second pivot was the right call"} |

---

## Per-Kit Maintenance Responsibilities

Each kit's playbook includes a "Maintaining the Engagement Record" section with kit-specific steps. Summary:

| Kit | Trigger | What to update |
|-----|---------|---------------|
| Product Intelligence Kit | Discovery Intake validated | Create ER (§1 Document Control + §2 header). Add artifact IDs as each Layer 2 artifact freezes. Record pivot decisions in §2 Key Decisions. |
| Solution Sourcing Kit | Each Layer 3 artifact frozen | Add artifact IDs to §3a table. Record sourcing decision and rationale in §3a Key Decisions. If SSK not engaged, write "SSK not engaged — fast-path Build justified in KER." |
| Engineering Execution Kit | Each Layer 4 artifact frozen | Add artifact IDs to §3 table. Record key decisions (architectural amendments, re-entry, scope deviations) in §3 Key Decisions. Record gate failures and resolutions in §3 Gate Failures. |
| Release & Exposure Kit | Release disposition determined | Add artifact IDs to §4 table. Record release disposition. Record key decisions (release type justification, RP deviations, gate failures) in §4 Key Decisions. |
| Reliability & Resilience Kit | Each Layer 6 artifact frozen | Add artifact IDs to §5 table. Add IR entries as incidents are declared and closed. Record key decisions (SRP revisions, error budget invocations, escalations) in §5 Key Decisions. |
| Insight & Evolution Kit | ES frozen | Add ES row to §6 table with signal and VH verdict. Update §7 Initiative Outcome. |
| Operational Diagnostics Kit | DCR frozen | Add DCR ID to §8 table. |
| Operational Diagnostics Kit | INR frozen | Add INR ID to §8 table. |
| Operational Diagnostics Kit | PMR frozen | Add PMR ID to §8 table. |
| Operational Diagnostics Kit | RB frozen | Add RB ID to §8 table (N/A if no runbook produced). |
| Quality Assurance Kit | Each Layer 9 artifact frozen | Add artifact IDs to §9 table. Record quality disposition. |
| Security & Compliance Kit | Each Layer 10 artifact frozen | Add artifact IDs to §10 table. |
| Data & Configuration Kit | Each Layer 11 artifact frozen | Add artifact IDs to §11 table. Note FFLR/DSR version changes. |
| Platform & Infrastructure Kit | Each Layer 12 artifact frozen | Add artifact IDs to §12 table. Note ISPEC/EM version changes. |
| Documentation & Knowledge Kit | Each Layer 13 artifact frozen | Add artifact IDs to §13 table. Note DHR version changes for periodic reviews. |
| Peer Review Kit | Each PRR frozen | Add PRR IDs to §14 table. Note review point and disposition. |
| Business Process Kit | Each Layer 15 artifact frozen | Add artifact IDs to §15 table. Note RC readiness declaration. |

**On initiative end:** The operator who declares the initiative Deprecated or Abandoned updates §1 Status and §7 Initiative Outcome, and adds the DN ID reference.

---

## ER Is Not Governed

The ER has no generation prompt, validator, or hard gates. It is an operational record maintained by humans following kit playbook steps. The format defined in this spec is authoritative but the ER is not validated by an AI session.

This is intentional: the ER's value comes from being maintained continuously throughout the engagement, not from being a point-in-time AI-generated artifact. Lightweight format + operator discipline is the right tradeoff.

---

## Retention

ERs are retained permanently. Changing status to `Deprecated` or `Abandoned` does not delete the ER — the artifact history it contains is valuable for portfolio synthesis even after the initiative ends.
