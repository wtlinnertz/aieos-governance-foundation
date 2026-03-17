# AIEOS Flow Reference

This document consolidates all valid entry points, exit conditions, layer routing, parallelism rules, and flow permutations across the AIEOS framework. It is the single reference for understanding how initiatives move through the system.

For initiative-specific routing (which layers to use for a given type of work), see [`initiative-presets.md`](initiative-presets.md). For tracking initiative state, see [`initiative-state-view.md`](initiative-state-view.md). For the machine-readable directed graph of all nodes, edges, and decision tables used by AI navigation tools, see [`navigation-map.md`](navigation-map.md).

---

## 1. Entry Points Into AIEOS

There are four valid ways to enter the AIEOS framework. Each leads to a different starting kit.

| Entry Type | Starting Kit | Entry Gate | When to Use |
|-----------|-------------|-----------|-------------|
| New work request (feature, research, compliance mandate) | PIK (Layer 2) | WCR classification + Discovery Intake | Problem space is unclear, solution is unknown, or mandate requires scoping |
| Well-understood enhancement | EEK (Layer 4), Path B | KER justifying Path B + Product Brief | Problem, solution, and acceptance criteria are already known |
| Production incident (SEV1/2) | ODK (Layer 8) | DCR within 2 hours | Automatic for SEV1/2; optional for lower severity |
| Technology decision | PINFK (Layer 12) | PDR (per decision) | Infrastructure or platform choice needs documented rationale |

All other kits are entered via downstream handoff or trigger, not directly from outside the framework.

---

## 2. Pipeline Flows

### 2.1 Full Pipeline (New Feature / Compliance)

The complete pipeline for initiatives that begin with discovery:

```
PIK → [SSK] → EEK (Path A) → [QAK] → REK → RRK → IEK
                  ↑                                    │
                  └────── ES re-discover signal ───────┘
```

SSK (Layer 3) is optional. When engaged, the sub-flow is: `PIK → SSK (SOER → VER → SDR) → EEK`. When skipped (Build is obvious), the flow is: `PIK → EEK` (direct).

**Sequence:**
1. **PIK:** WCR → Discovery Intake → PFD → VH → AR → EL → DPRD (freeze)
1a. **SSK** (optional): SOER → VER → SDR (freeze) — evaluates Build/Buy/Adopt
2. **EEK:** KER (Path A) → PRD (placed DPRD) → ACF → SAD → DCF → TDD → WDD → Execution → ORD (freeze)
3. **QAK** (optional): QAER → VP → TCR(s) → QGR (freeze)
4. **REK:** RER → RCF → RSA → RP → Release Execution → RR (freeze)
5. **RRK:** SRER → SRP → IR (per incident) → RHR (periodic)
6. **IEK:** ES (from 2+ RHRs) → re-entry signal (maintain / watch / re-discover)

**Exit gate per transition:**
- PIK → SSK: DPRD frozen, all 8 hard gates passing (same gate as PIK → EEK)
- PIK → EEK: DPRD frozen, all 8 hard gates passing
- SSK → EEK: SDR frozen, references frozen DPRD
- EEK → QAK/REK: ORD frozen, all 8 hard gates passing
- QAK → REK: QGR frozen with PASS or CONDITIONAL disposition
- REK → RRK: RR frozen with §7 Handoff to Layer 6 complete
- RRK → IEK: 2+ frozen RHRs covering sufficient observation period

### 2.2 Enhancement Pipeline (Path B)

For well-understood enhancements that bypass discovery:

```
EEK (Path B) → [QAK] → REK → RRK → IEK
```

**Differences from full pipeline:**
- No PIK engagement; KER must justify Path B selection
- PRD generated from Product Brief (not placed from DPRD)
- QAK remains optional
- All downstream layers identical

### 2.3 Exploratory Research (Terminal at PIK)

Research that may not lead to a build:

```
PIK → EL decision: proceed → DPRD → EEK (continues as §2.1)
                    pivot   → new PFD (restart within PIK)
                    pause   → initiative suspended (no downstream)
```

Research terminates at PIK if the EL decision is "pause." No DPRD is generated.

### 2.4 Incident-Triggered Fix

For performance or reliability fixes triggered by production incidents:

```
ODK → EEK (Path B) → [QAK] → REK → RRK
```

**Sequence:**
1. **ODK:** DCR → INR → PMR (freeze) — PMR §8 identifies corrective actions
2. **EEK:** KER (Path B, citing PMR) → PRD → TDD → WDD → Execution → ORD (freeze)
3. Continue through QAK (optional), REK, RRK as normal

### 2.5 RHR-Triggered Fix

For fixes triggered by reliability health review findings:

```
RRK (SRP revision) → EEK (Path B) → REK → RRK (next RHR cycle)
```

---

## 3. Cross-Cutting Kit Activation

Cross-cutting kits (Layers 9–14) do not follow the pipeline sequence. They activate at trigger points and run in parallel with pipeline layers.

### 3.1 Trigger Points

| Kit | Artifact | Trigger | Upstream Dependency |
|-----|----------|---------|-------------------|
| **QAK (L9)** | QAER → VP → TCR → QGR | ORD frozen | Frozen ORD + SAD + TDD + ACF + WDD |
| **SCK (L10)** | TM | SAD frozen | Frozen SAD |
| **SCK (L10)** | SAR | TM frozen + code complete | Frozen TM + implementation |
| **SCK (L10)** | DAR | Dependency manifest available | Complete dependency list |
| **SCK (L10)** | CER | Compliance mandate identified | Regulatory requirement |
| **DCK (L11)** | CSPEC | TDD frozen | Frozen TDD |
| **DCK (L11)** | DSR | TDD frozen (with data model) | Frozen TDD |
| **DCK (L11)** | FFLR | Feature flags created (during REK) | Frozen RR with flag inventory |
| **PINFK (L12)** | PDR | Technology decision arises | Decision context (no upstream artifact required) |
| **PINFK (L12)** | ISPEC | PDRs frozen | Frozen PDRs |
| **PINFK (L12)** | EM | ISPEC frozen | Frozen ISPEC |
| **PINFK (L12)** | SMR | ISPEC frozen | Frozen ISPEC + system inventory |
| **DKK (L13)** | UDR | RR frozen | Frozen RR + PRD + WDD |
| **DKK (L13)** | ARR | TDD frozen (early) or RR frozen (at release) | Frozen TDD or RR |
| **DKK (L13)** | SKA | RR frozen, PMR frozen, or support patterns | Trigger-dependent |
| **DKK (L13)** | DHR | Periodic (aligned with RHR) | 2+ frozen documentation artifacts |
| **PRK (L14)** | PRR (Concept) | DPRD validated | Validated DPRD |
| **PRK (L14)** | PRR (Architecture) | SAD validated | Validated SAD + frozen PRD + frozen ACF |
| **PRK (L14)** | PRR (Tech Design) | TDD validated | Validated TDD + frozen SAD + frozen ACF |
| **PRK (L14)** | PRR (Impl Readiness) | WDD validated | Validated WDD + frozen TDD |
| **PRK (L14)** | PRR (Code Review) | ORD validated | Validated ORD + execution evidence |
| **PRK (L14)** | PRR (Integration) | QGR validated | Validated QGR + frozen TCR(s) |
| **PRK (L14)** | PRR (Ops Readiness) | RP validated | Validated RP + frozen RCF |
| **PRK (L14)** | PRR (Post-Deploy) | RHR validated | Validated RHR + frozen SRP |
| **PRK (L14)** | PRR (Incident) | PMR validated | Validated PMR + frozen INR |
| **BPK (L15)** | PIA | SAD or TDD frozen (with process impacts) | Frozen SAD or TDD |
| **BPK (L15)** | TP | PIA frozen | Frozen PIA |
| **BPK (L15)** | RC | TP frozen + evidence collected | Frozen TP + readiness evidence |

### 3.2 Cross-Cutting Feeds Into Pipeline

Cross-cutting artifacts feed back into the pipeline at specific points:

| Source | Target | What It Provides |
|--------|--------|-----------------|
| SCK TM | QAK VP | Security test scope (optional VP input) |
| SCK SAR | QAK VP | Security findings to verify (optional VP input) |
| SCK SAR + DAR | REK RER | Security clearance evidence |
| DCK CSPEC | REK RP | Config validation criteria |
| DCK CSPEC | RRK SRP | Config drift detection rules |
| DCK FFLR | RRK RHR | Stale flag alerts |
| PINFK PDRs | EEK ACF | Technology assumptions (already decided) |
| PINFK ISPEC | EEK SAD | Deployment model constraints |
| PINFK EM | REK RP | Environment promotion rules |
| DKK DHR | IEK PES | Documentation health signal |
| PRK PRR | Any kit | Multi-perspective findings that must be addressed before freeze |
| BPK RC | REK RER | Process readiness declaration |
| BPK TP | REK RP | Cutover schedule alignment |

### 3.3 Special Ordering: Compliance Initiatives

For compliance-driven work (Preset 3), SCK must complete before QAK:

```
EEK → SCK (TM → SAR → CER → DAR) → QAK (VP references frozen TM + SAR) → REK
```

Frozen SCK artifacts feed into QAK's Verification Plan as security test inputs. QAK cannot produce a valid VP without them.

---

## 4. Parallelism Rules

### 4.1 What Can Run in Parallel

**Within EEK:**
- ACF and SAD can generate in parallel (both depend on frozen PRD)
- DCF and TDD can generate in parallel (both depend on frozen ACF/SAD)
- WDD work items execute in parallel (Tests → Plan → Code → Review per item)

**Cross-cutting kits during EEK:**
- SCK TM (after SAD freeze), DCK CSPEC + DSR (after TDD freeze), DKK ARR (after TDD freeze), PINFK PDRs (any time) — all run in parallel with EEK pipeline continuation

**Cross-cutting kits during REK:**
- DCK FFLR (during release execution), SCK SAR/DAR (completing before release entry) — parallel with release

**Within cross-cutting kits:**
- SCK: TM, DAR, CER are independent (SAR depends on TM)
- DCK: CSPEC, DSR, FFLR are completely independent
- DKK: UDR, ARR, SKA, DHR are completely independent
- PINFK: PDRs are independent; ISPEC depends on PDRs; EM and SMR depend on ISPEC (can generate in parallel)

**PRK during any kit:**
- PRR generation triggers after artifact validation, runs in parallel with human freeze review preparation
- Multiple PRR lenses run in parallel (all lenses for a review point execute simultaneously)

**Multiple initiatives:**
- Different projects' entire cycles run in parallel with independent Engagement Records

### 4.2 What Cannot Run in Parallel

These transitions are strictly sequential — the upstream artifact must be frozen before the downstream kit begins:

| Upstream | Downstream | Why |
|----------|-----------|-----|
| PIK DPRD | SSK entry (if engaged) | SSK requires frozen DPRD |
| PIK DPRD | EEK entry (Path A, direct) | EEK requires frozen DPRD |
| SSK SDR | EEK entry (via SSK) | EEK requires frozen SDR + frozen DPRD |
| EEK ORD | REK entry | REK requires frozen ORD |
| EEK ORD | QAK entry | QAK requires frozen ORD |
| QAK QGR | REK entry (if QAK adopted) | QGR gates REK |
| REK RR | RRK entry | RRK requires frozen RR §7 |
| RRK 2+ RHRs | IEK entry | IEK requires operational evidence |
| SCK TM | SCK SAR | SAR uses TM as verification input |
| PRK PRR | Artifact freeze (reviewed artifact) | PRR must pass before artifact can freeze |

### 4.3 Sub-Agent Orchestration

The parallelism rules in §4.1 define **what** can run in parallel. For operational guidance on **how** an orchestrating agent should fan out to sub-agents, package self-contained context, track completion, and reconverge validated outputs, see [`sub-agent-orchestration.md`](sub-agent-orchestration.md). That document defines three patterns: independent lens parallelism (PRK), parallel-safe work item execution (EEK), and provider/consumer contract development (EEK).

### 4.4 Convergence Loops

Flow validation rule 3 (FAIL blocks promotion) is operationalized by the convergence loop pattern for autonomous agents. When an artifact fails validation, the convergence loop automates the correction-revalidation cycle with bounded iteration (max 3 attempts), structured feedback from validator findings, and escalation to a human when convergence is not achieved. See [`review-convergence-loop.md`](review-convergence-loop.md) for the full pattern specification. Convergence loops operate within the Draft → Validated transition — they do not affect freeze-before-promote or cross-kit handoffs.

---

## 5. Escalation Paths

Escalation paths move work upstream (against the normal pipeline direction) when downstream evidence reveals issues.

| ID | Source | Trigger | Target | Action |
|----|--------|---------|--------|--------|
| T1 | RRK IR | SEV1/2 incident with code defect | EEK | Escalation record → EEK KER (Path B) → defect fix |
| T2 | RRK RHR | Recurring pattern (3+ occurrences) | PIK | Escalation record → PIK assesses new discovery |
| T3 | REK RR | Rollback caused by code defect | EEK | Escalation record → EEK defect fix → new release |
| T4 | REK RR | Rollback caused by wrong feature | PIK | Escalation record → PIK new discovery engagement |
| T5 | RRK IR | SEV1/2 requiring structured diagnosis | ODK | Automatic → ODK DCR/INR/PMR |
| T6 | IEK ES | "re-discover" signal | PIK | ES §6 → new PIK engagement (product owner decides) |

---

## 6. Re-Entry Protocols

When a frozen artifact must change after downstream work has begun:

### 6.1 Within-Kit Re-Entry

1. Identify the artifact to change
2. Identify all downstream artifacts that reference it
3. Assess impact (scope, decisions, traceability affected?)
4. Issue a new artifact version (v2, v3)
5. Re-validate the new version
6. Re-validate all affected downstream artifacts
7. Document the change with reference to original

### 6.2 Cross-Kit Re-Entry (PIK → EEK)

When a PIK DPRD must change after EEK artifacts exist:

1. PIK flags the DPRD change
2. EEK runs impact analysis (`impact-analysis-prompt.md`) on all frozen EEK artifacts
3. Joint decision: accept changes or negotiate scope
4. If accepted: new DPRD version placed in EEK, cascade re-validation

### 6.3 QAK FAIL Re-Entry

When QGR disposition is FAIL:

1. QGR documents blocking issues → return to EEK
2. EEK addresses defects
3. ORD re-validated
4. New QAK cycle: QAER → VP (reuse if scope unchanged) → TCR → QGR

### 6.4 Non-Material Amendments

A frozen artifact may be corrected in place (no new version) when **all** of:
- Does not affect any hard gate field
- Does not change scope, decisions, owners, or technical specs
- Does not affect any downstream-referenced field

Add an Amendment Log entry. If there is any ambiguity, treat it as material and issue a new version.

---

## 7. Optional vs. Required Layers

### 7.1 Pipeline Layers

| Layer | Required? | Skip Condition |
|-------|-----------|---------------|
| PIK (L2) | Conditional | Skip if scope is well-understood (use EEK Path B) |
| SSK (L3) | Conditional | Skip when Build is the obvious choice; engage when sourcing evaluation (Build/Buy/Adopt) is needed |
| EEK (L4) | Always required | Every initiative passes through EEK |
| REK (L5) | Always required | Every initiative that reaches production releases via REK |
| RRK (L6) | Required in production | Required once system is deployed; not applicable until release |
| IEK (L7) | Required when eligible | Required once 2+ RHRs exist |

### 7.2 Cross-Cutting Layers

| Layer | Required? | Adoption Criteria |
|-------|-----------|------------------|
| QAK (L9) | Optional | Adopt if integration points, external dependencies, or cross-component behavior exist |
| SCK (L10) | Conditional | Required for security-sensitive or regulated systems; TM mandatory if SAR adopted |
| DCK (L11) | Conditional | CSPEC: if config exists; FFLR: if feature flags used; DSR: if data schemas exist |
| PINFK (L12) | Conditional | PDRs: if technology decisions need documentation; ISPEC: if non-trivial infrastructure |
| DKK (L13) | Conditional | UDR: if end users exist; ARR: if API consumers exist; SKA: if support team exists |
| PRK (L14) | Optional | Adopt when multi-perspective quality assurance is valuable; recommended for SAD and TDD at minimum |
| BPK (L15) | Conditional | Adopt when the initiative changes, adds, or removes business processes or user workflows |

### 7.3 Operational Track

| Layer | Required? | Trigger |
|-------|-----------|--------|
| ODK (L8) | Conditional | Automatic for SEV1/2; optional for lower severity |

---

## 8. Late Adoption and Mid-Initiative Entry

Any cross-cutting kit can be adopted mid-initiative when its trigger conditions are met. Pipeline kits support mid-initiative entry through escalation.

| Kit | Mid-Initiative Entry? | How |
|-----|----------------------|-----|
| PIK | Yes | Escalation from REK (wrong feature) or RRK (recurring pattern) |
| EEK | Yes | Escalation from ODK (code defect) or RRK (reliability fix) |
| REK | Yes | New release cycle after EEK defect fix |
| RRK | Yes | Normal entry after any release |
| IEK | No | Cannot enter until 2+ RHRs exist (time-dependent) |
| QAK | Yes | Adopt when quality gates become needed |
| SCK | Yes | Trigger-based; activate when security/compliance requirements identified |
| DCK | Yes | Trigger-based; activate when config/data governance needed |
| PINFK | Yes | PDRs can be created at any point |
| DKK | Yes | Trigger-based; activate when documentation governance needed |
| ODK | Yes | Reactive; triggered by any qualifying incident |
| BPK | Yes | Trigger-based; activate when process impact is identified during design |

---

## 9. Maximum Parallelism Timeline

For a large initiative adopting all kits, the maximum parallelism looks like:

```
Phase 1 — Discovery (PIK linear):
  PIK:   WCR → Intake → PFD → VH → AR → EL → DPRD ────────────┐
  PINFK: PDR-001, PDR-002 (parallel, as decisions arise) ──────┤
                                                                 │
Phase 1a — Sourcing (SSK, optional):                             ▼
  SSK:   SOER → VER → SDR ─────────────────────────────────────┐
  (skip if Build is obvious — proceed directly to Phase 2)      │
                                                                 │
Phase 2 — Design (EEK + cross-cutting parallel):                 ▼
  EEK:   KER → PRD → ACF ──┬── SAD ──┬── DCF ──┬── TDD ──── WDD
                            │         │         │         │
  PINFK:                    │  ISPEC ─┤── EM    │         │
  SCK:                      │         └── TM ───┤── SAR   │
  DCK:                      │                   └── CSPEC ─┤── DSR
  DKK:                      │                      ARR ────┘
                            │
Phase 3 — Execution (EEK + QAK):
  EEK:   Work items (parallel) ──────────────── ORD freeze
  SCK:   DAR (parallel) ────────────────────────┤
  QAK:                                   QAER → VP → TCR(s) → QGR
                                                                 │
Phase 4 — Release (REK + cross-cutting):                         ▼
  REK:   RER → RCF → RSA → RP → Execute → RR ─────────────────────────┐
  DCK:   FFLR (during release) ──────────────────────────────────┤
                                                                  │
Phase 5 — Operations (RRK + DKK + ODK):                          ▼
  RRK:   SRER → SRP → IR (per incident) → RHR (periodic) ───────┐
  DKK:   UDR, SKA (from RR) ────────────────────────────── DHR   │
  ODK:   (if incident) DCR → INR → PMR ──────────────────────────┤
                                                                   │
Phase 6 — Learning (IEK):                                         ▼
  IEK:   ES (from 2+ RHRs) → re-entry signal
              │
              └── re-discover → new PIK engagement (loop)
```

---

## 10. Flow Validation Rules

These invariants must hold for any valid flow through the framework:

1. **Every initiative has an Engagement Record** — created at PIK Step 1 (Path A) or EEK Step 0 (Path B)
2. **Freeze-before-promote is absolute** — no downstream artifact may be generated from an unfrozen upstream artifact
3. **Validators judge, they do not help** — every artifact is validated before freeze; FAIL blocks promotion
4. **Cross-cutting kits do not block each other** — SCK, DCK, DKK, PINFK operate independently
5. **Cross-cutting kits do not block the pipeline** — except QAK when adopted (QGR gates REK entry)
6. **Escalation always creates a new initiative cycle** — escalation from REK/RRK/ODK to EEK/PIK starts a new KER or WCR, not a patch to existing frozen artifacts
7. **Path selection is immutable** — EEK Path A vs. Path B is decided at KER and cannot change mid-engagement
8. **Separate generation and validation sessions** — the AI that generates an artifact must not validate it in the same session
9. **Peer review gates freeze (when adopted)** — when PRK is adopted for a review point, the PRR for that artifact must pass before the artifact freezes
10. **Correction loops are bounded** — autonomous correction of failed artifacts is limited to 3 iterations; failure to converge requires human escalation (see [`review-convergence-loop.md`](review-convergence-loop.md))

---

## 11. Decision Outcome Taxonomy

Six formal outcomes that apply at decision points throughout the framework. These outcomes operate at the decision layer above validators — validators still output PASS/FAIL; the taxonomy classifies the human or orchestrator decision that follows.

| Outcome | Definition | Maps To | Typical Context |
|---------|-----------|---------|-----------------|
| **Approve** | All gates pass; proceed to next state | Validator PASS + human confirmation | Artifact freeze, kit transition |
| **Approve-with-Conditions** | Gates pass with documented risks accepted | QAK CONDITIONAL disposition | Quality gate with accepted risk |
| **Block** | Critical violation; halt and remediate before proceeding | Validator FAIL with critical findings | Hard gate failure, security block |
| **Remediate-and-Retry** | Fixable findings; correct and re-validate (max 3 iterations) | Convergence loop (Pattern A/B) | Validator FAIL with correctable issues |
| **Require-Redesign** | Architecture or design risk too high; return to design phase | Escalation triggers 3/4 | Fundamental approach change needed |
| **Rollback** | Runtime SLO violation; execute rollback procedure | Escalation trigger 5 (REK/RRK) | Production failure after release |

### Relationship to Existing Mechanisms

- **Validators** continue to output `PASS` or `FAIL`. The taxonomy does not change validator behavior.
- **Approve** and **Block** map directly to validator PASS and FAIL respectively when no additional context applies.
- **Approve-with-Conditions** is currently used only at QAK (QGR CONDITIONAL disposition). Other kits may adopt it when risk acceptance is formally documented.
- **Remediate-and-Retry** is the decision to enter a convergence loop. See [`review-convergence-loop.md`](review-convergence-loop.md) for the bounded correction pattern.
- **Require-Redesign** applies when the issue cannot be fixed by correcting the current artifact — the problem is upstream. This triggers cross-kit re-entry (§6.2) or within-kit re-entry to a design-phase artifact.
- **Rollback** applies only after release execution has begun. It triggers the REK abort protocol and escalation paths (T3, T4).

### When to Apply

The taxonomy applies at every junction node in the navigation map and at every artifact freeze decision. It does not apply within validator execution (validators remain PASS/FAIL).

At decision junctions, the `decision-router` tool references this taxonomy when presenting options. The outcome label is recorded in the ER key decisions section for audit traceability.
