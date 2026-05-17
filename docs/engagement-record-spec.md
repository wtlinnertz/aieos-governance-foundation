# Engagement Record Spec

## Purpose

This document defines the format, section rules, and maintenance responsibilities for the Engagement Record (ER). The ER is a project-level artifact — it lives in the consuming project, not in any kit, and is maintained incrementally by operators as work passes through each AIEOS layer.

The ER is not governed by a four-file system. It has no generation prompt or validator. It is an operational index: a structured record of every artifact ID, key decision, and outcome for a single initiative across all layers.

---

## Authority

This spec is the canonical definition of the ER format. It lives in `aieos-governance-foundation` because ERs span all layers — no single kit should own a cross-layer standard.

---

## Location and naming

| Field | Value |
|-------|-------|
| Location | `{project}/docs/engagement/er-{initiative}.md` |
| ID format | `ER-{INITIATIVE}-{NNN}` |
| Example | `ER-TASKFLOW-001` |

`INITIATIVE` is a short uppercase identifier for the initiative or service (e.g., `TASKFLOW`, `PAYMENTS-API`, `NOTIFICATIONS`).

---

## ER sections

### §1 document control

| Field | Value |
|-------|-------|
| ER ID | ER-{INITIATIVE}-{NNN} |
| Initiative | {full initiative name} |
| Service(s) | {service name(s) this initiative delivers to or creates} |
| Status | Active / Deprecated / Abandoned |
| Discovery Start | {YYYY-MM-DD — date Discovery Intake was validated in PIK} |
| Latest ES Date | {YYYY-MM-DD — date of most recent frozen ES, or N/A} |
| ER Spec Version | 1.7 |
| Current Position | {Navigation map node ID, e.g., N-EEK-TDD — updated by position-check tool. Optional.} |
| Preset | {P1–P5 or Custom — declared at initiative start} |
| Retroactive | [ ] No — all artifacts generated prospectively during the initiative | [ ] Yes — some or all artifacts generated retrospectively after work was complete. If Yes: note which artifact phases are retroactive and the rationale for retroactive governance. |

**Status values:**
- `Active` — initiative is in progress or in production and under monitoring
- `Deprecated` — initiative completed its lifecycle; the service is no longer active (matches DN type: Deprecated)
- `Abandoned` — initiative was cancelled before completion (matches DN type: Abandoned)

When status changes to `Deprecated` or `Abandoned`, add a `Deprecation Notice` field pointing to the DN ID.

---

### §1b state block

The state block provides a machine-readable snapshot of initiative position. It is updated by the sherpa (or operator) after every artifact freeze, kit transition, and decision junction. Any AI session can determine exactly where the initiative stands by reading this block alone.

**Format:**

| Field | Value |
|-------|-------|
| Current Layer | {layer number — kit name, e.g., "4 — Engineering Execution"} |
| Current Artifact | {artifact type in progress, or "between artifacts"} |
| Current Step | {playbook step reference, e.g., "EEK Step 3: TDD"} |
| Frozen Count | {N} |
| Next Action | {what should happen next, e.g., "Generate TDD from frozen SAD"} |
| Blocking On | {dependency description, or "nothing — ready to proceed"} |
| Last Updated | {YYYY-MM-DD HH:MM} |

**Rules:**
- The state block is updated AFTER each artifact freeze (not before)
- The state block is updated AFTER each kit transition
- The state block is updated AFTER each decision junction (cross-cutting adoption, proceed/pivot/pause)
- "Current Artifact" is the artifact currently being worked on, not the last frozen one
- "Next Action" must be specific enough for a new AI session to continue without reading the full ER
- If the initiative is paused (e.g., waiting for EL experiment results), set Current Artifact to "paused" and Next Action to the resumption condition

---

### §1a layer 1 — strategic direction (Optional)

This section is present only when the initiative originated from a governed strategic bet or roadmap (SDK). Omit this section when SDK was not used.

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Capability Lifecycle Assessment | CLA-XXX vN | Frozen | Note current version; omit if no roadmap phase |
| Product Capability Roadmap | PCR-XXX vN | Frozen | Note horizon (1yr/3yr/5yr); omit if no roadmap phase |
| Technology Investment Roadmap | TIR-XXX vN | Frozen | Note horizon (2-5yr); omit if no roadmap phase |
| Strategic Bet Record | SBR-XXX | Frozen | |
| Portfolio Prioritization Record | PPR-XXX | Frozen | Above/below the line: {above/below} |

If the Roadmap Phase was not used (direct SBR entry), write "Roadmap Phase not used — direct bet entry."

**Key decisions:**

List the strategic prioritization decision and any roadmap lifecycle decisions. Minimum entry: the PPR ranking position and cut line status.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

Examples:
- `Lifecycle: Authentication service marked "sunset" — timeline Q3 2027 — CLA-ACME-001 v2`
- `Priority: Ranked #2 of 5 bets, above the cut line with 1 team for 1 quarter allocation — PPR-001`

---

### §2 layer 2 — product intelligence

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

### §3a layer 3 — solution sourcing (if engaged)

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

### §3 layer 4 — engineering execution

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

### §4 layer 5 — release & exposure

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Release Entry Record | RER-XXX | Frozen | |
| Release Context File | RCF-XXX | Frozen | |
| Release Safety Assessment | RSA-XXX | Frozen | |
| Release Plan | RP-XXX | Frozen | |
| Release Record | RR-XXX | Frozen | |

**Release disposition:** Released / Rolled Back / Abandoned

If Rolled Back or Abandoned, add a brief note on cause.

**Key decisions:**

List each significant decision made during Layer 5, with enough context to be useful without re-reading the full artifact. Minimum entries: release type justification, deviations from the Release Plan during execution, and any gate failures or validator issues encountered.

Format: `{decision type}: {brief description} — {artifact ID where decision is recorded}`

---

### §5 layer 6 — reliability & resilience

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

### §6 layer 7 — insight & evolution

**Artifact table:**

| ES ID | Coverage Period | Signal | VH Verdict |
|-------|----------------|--------|------------|
| ES-XXX | YYYY-MM-DD to YYYY-MM-DD | maintain / watch / re-discover | Validated / Invalidated / Partially Validated / Insufficient Data |

Add a row for each ES produced for this initiative. If no ES has been produced yet, write "No ES produced yet."

**Portfolio ESes:** If this initiative's ER has been included in a Portfolio Evolution Signal, note the PES ID in a separate row.

---

### §8 layer 8 — operational diagnostics

**Artifact table:**

| Field | Artifact | Status | Notes |
|-------|----------|--------|-------|
| DCR ID | DCR | Frozen | Entry gate |
| INR ID(s) | INR | Frozen | List all INRs |
| PMR ID(s) | PMR | Frozen | List all PMRs |
| RB ID(s) | RB | Frozen | Runbooks codified; N/A if none |

Add a row for each DCR engagement (an incident may produce one DCR, one or more INRs, one PMR, and optionally one or more RBs). If no ODK engagement has been initiated for this initiative, write "No ODK engagement initiated."

---

### §9 layer 9 — quality assurance (if adopted)

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

### §10 layer 10 — security & compliance (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Threat Model | TM-XXX | Frozen | |
| Security Assessment Record | SAR-XXX | Frozen | |
| Compliance Evidence Record | CER-XXX | Frozen | N/A if no compliance mandate |
| Dependency Audit Record | DAR-XXX | Frozen | |

If Layer 10 is not adopted for this initiative, write "SCK not adopted for this initiative."

---

### §11 layer 11 — data & configuration (if adopted)

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

### §12 layer 12 — platform & infrastructure (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Platform Decision Record(s) | PDR-XXX | Frozen | List all PDRs |
| Infrastructure Specification | ISPEC-XXX | Frozen | Note current version |
| Environment Matrix | EM-XXX | Frozen | Note current version |
| System Model Record | SMR-XXX | Frozen | Note current version |

If the ISPEC or EM has been re-frozen, list all versions in the Notes column. If the SMR has been re-frozen, list all versions in the Notes column.

If Layer 12 is not adopted for this initiative, write "PINFK not adopted for this initiative."

---

### §13 layer 13 — documentation & knowledge (if adopted)

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

### §14 layer 14 — peer review (if adopted)

**Artifact table:**

| Review Point | PRR ID | Artifact Reviewed | Status | Disposition | Notes |
|-------------|--------|-------------------|--------|-------------|-------|
| Architecture Review | PRR-XXX | SAD-XXX | Frozen | PASS / FAIL | |
| Technical Design Review | PRR-XXX | TDD-XXX | Frozen | PASS / FAIL | |
| Code Review | PRR-XXX | ORD-XXX | Frozen | PASS / FAIL | |

Add a row for each PRR produced. Disposition must be PASS for the reviewed artifact to freeze.

If Layer 14 is not adopted for this initiative, write "PRK not adopted for this initiative."

---

### §15 layer 15 — business process (if adopted)

**Artifact table:**

| Artifact Type | ID | Status | Notes |
|--------------|-----|--------|-------|
| Process Impact Assessment | PIA-XXX | Frozen | |
| Transition Plan | TP-XXX | Frozen | |
| Readiness Confirmation | RC-XXX | Frozen | Readiness: Ready / Ready-with-conditions / Not Ready |

If Layer 15 is not adopted for this initiative, write "BPK not adopted for this initiative."

---

### §16 impact attribution (Optional)

This section records who contributed what at each layer boundary. It is observational — it captures artifact ownership and contribution levels as they occur during the initiative, not retroactively at quarter end. It is never used for performance evaluation within the ER itself.

**Contributor table:**

| Layer | Artifact ID | Contributor | Role | Contribution Level | Notes |
|-------|-------------|-------------|------|-------------------|-------|
| {layer number} | {artifact-ID} | {name or pseudonym} | {functional role during this artifact} | Primary / Significant / Supporting | {optional context} |

**Contribution Level definitions:**

| Level | Meaning |
|-------|---------|
| **Primary** | Drove the artifact — owned the design, made final decisions, accountable for the outcome |
| **Significant** | Major contributor — owned a subsystem, shaped direction, unblocked the team |
| **Supporting** | Reviewed, consulted, or assisted — meaningful input without decision authority |

**Rules:**

- Contributor names follow the pseudonym convention from release-entry-spec.md §Release Owner: pseudonyms are acceptable when paired with a traceability note stating where the real-name mapping is maintained.
- Contribution Levels are observational, not evaluative — they record what happened, not how well it was done.
- Rows are added at each layer boundary when an artifact is frozen, not retroactively.
- Multiple contributors can be listed per artifact. Only one contributor per artifact should be "Primary."
- Tool references (repository URLs, ticket IDs, etc.) must not appear in this table — use role descriptions and artifact IDs only.
- This section is optional. If impact attribution is not adopted for this initiative, write "Impact attribution not adopted for this initiative."

---

### §7 initiative outcome

| Field | Value |
|-------|-------|
| Current Status | Active / Deprecated / Abandoned |
| Deprecation/Abandonment Notice | DN-XXX or N/A |
| Final Re-Entry Signal | maintain / watch / re-discover / N/A (if no ES yet) |
| Final VH Verdict | Validated / Invalidated / Partially Validated / Insufficient Data / N/A |
| Notes | {any context useful for portfolio synthesis — e.g., "initiative pivoted twice; second pivot was the right call"} |

---

## Per-Kit maintenance responsibilities

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
| All kits (if impact attribution adopted) | Each artifact frozen | Add contributor row(s) to §16 table with layer, artifact ID, contributor name/pseudonym, role, and contribution level (Primary / Significant / Supporting). |

**On initiative end:** The operator who declares the initiative Deprecated or Abandoned updates §1 Status and §7 Initiative Outcome, and adds the DN ID reference.

---

## Decision register governance

The "Key decisions" subsection in each ER layer section constitutes an **append-only decision register**. Decisions are the most valuable content in the ER — they explain *why* the initiative took the shape it did, not just *what* artifacts were produced.

### Decision format

Every decision entry follows this format:

```
{DECISION-ID} | {type} | {description} | {artifact_id} | {date}
```

**Decision ID:** `DEC-{INITIATIVE}-{NNN}` (e.g., `DEC-TASKFLOW-001`). Sequential across all layers — not per-layer.

**Decision types:**

| Type | When Used |
|------|-----------|
| `Architecture` | Architectural trade-off, pattern selection, component design choice |
| `Pivot` | Assumption invalidated, direction changed based on evidence |
| `Priority` | Ranking, sequencing, above/below cut line |
| `Scope` | Boundary change — scope added, excluded, or deferred |
| `Adoption` | Cross-cutting kit adopted or declined with rationale |
| `Release` | Release strategy, exposure level, rollback decision |
| `Operational` | SRP revision, error budget invocation, escalation trigger |
| `Escalation` | Work escalated to upstream layer or external authority |

### Append-Only rules

1. **Decisions are never edited.** Once recorded, a decision entry is immutable.
2. **Superseding decisions reference the original.** If a decision is reversed or revised, add a new entry: `DEC-XXX-NNN | Scope | Revised: DEC-XXX-MMM — now includes mobile clients | SAD-XXX | 2026-04-01`
3. **Every decision traces to an artifact.** The `artifact_id` field identifies where the decision is formally recorded or expressed.
4. **Decision recording happens at freeze points.** The sherpa (or operator) checks at each artifact freeze whether the artifact represents or influenced a key decision. If yes, a decision entry is appended.

### Minimum entries per layer

| Layer | Minimum Decision Entries |
|-------|-------------------------|
| §1a SDK | Priority ranking (PPR position + cut line status) |
| §2 PIK | Pivot decisions (if any occurred). If no pivots: "No pivots — all assumptions validated." |
| §3a SSK | Build/Buy/Adopt decision with rationale |
| §3 EEK | Architectural choices (if any deviate from PRD/SAD). Scope changes (if any). |
| §4 REK | Release type justification. Deviations from Release Plan (if any). |
| §5 RRK | SRP revisions (if any). Error budget invocations (if any). |
| Cross-cutting | Kit adoption/decline decision for each evaluated kit |

Layers with no decisions should state: "No key decisions at this layer."

### Backward compatibility

Existing ERs with informal "Key decisions" entries (free-text format) remain valid. New entries should follow the standardized format. Existing entries may be backfilled to the standardized format when an ER is actively maintained.

The informal format `{decision type}: {brief description} — {artifact ID}` is accepted as a shorthand. The full format with decision IDs is preferred for traceability.

---

## ER is not governed

The ER has no generation prompt, validator, or hard gates. It is an operational record maintained by humans following kit playbook steps. The format defined in this spec is authoritative but the ER is not validated by an AI session.

This is intentional: the ER's value comes from being maintained continuously throughout the engagement, not from being a point-in-time AI-generated artifact. Lightweight format + operator discipline is the right tradeoff.

---

## Retention

ERs are retained permanently. Changing status to `Deprecated` or `Abandoned` does not delete the ER — the artifact history it contains is valuable for portfolio synthesis even after the initiative ends.
