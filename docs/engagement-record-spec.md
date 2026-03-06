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
| ER Spec Version | 1.0 |

**Status values:**
- `Active` — initiative is in progress or in production and under monitoring
- `Deprecated` — initiative completed its lifecycle; the service is no longer active (matches DN type: Deprecated)
- `Abandoned` — initiative was cancelled before completion (matches DN type: Abandoned)

When status changes to `Deprecated` or `Abandoned`, add a `Deprecation Notice` field pointing to the DN ID.

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

---

### §6 Layer 7 — Insight & Evolution

**Artifact table:**

| ES ID | Coverage Period | Signal | VH Verdict |
|-------|----------------|--------|------------|
| ES-XXX | YYYY-MM-DD to YYYY-MM-DD | maintain / watch / re-discover | Validated / Invalidated / Partially Validated / Insufficient Data |

Add a row for each ES produced for this initiative. If no ES has been produced yet, write "No ES produced yet."

**Portfolio ESes:** If this initiative's ER has been included in a Portfolio Evolution Signal, note the PES ID in a separate row.

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
| Engineering Execution Kit | Each Layer 4 artifact frozen | Add artifact IDs to §3 table. Record gate failures and resolutions in §3 Gate Failures. |
| Release & Exposure Kit | Release disposition determined | Add artifact IDs to §4 table. Record release disposition. |
| Reliability & Resilience Kit | Each Layer 6 artifact frozen | Add artifact IDs to §5 table. Add IR entries as incidents are declared and closed. |
| Insight & Evolution Kit | ES frozen | Add ES row to §6 table with signal and VH verdict. Update §7 Initiative Outcome. |

**On initiative end:** The operator who declares the initiative Deprecated or Abandoned updates §1 Status and §7 Initiative Outcome, and adds the DN ID reference.

---

## ER Is Not Governed

The ER has no generation prompt, validator, or hard gates. It is an operational record maintained by humans following kit playbook steps. The format defined in this spec is authoritative but the ER is not validated by an AI session.

This is intentional: the ER's value comes from being maintained continuously throughout the engagement, not from being a point-in-time AI-generated artifact. Lightweight format + operator discipline is the right tradeoff.

---

## Retention

ERs are retained permanently. Changing status to `Deprecated` or `Abandoned` does not delete the ER — the artifact history it contains is valuable for portfolio synthesis even after the initiative ends.
