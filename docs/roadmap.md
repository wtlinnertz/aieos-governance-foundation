# AIEOS Roadmap

Single-source tracking for completed work, active initiatives, and planned items across the AIEOS governance framework and ecosystem.

**Last updated:** 2026-03-19 (aieos-sherpa extracted)

---

## Completed

### Framework Foundation (pre-March 2026)

- [x] **FW-001** Core governance model with four-file invariant (spec, template, prompt, validator)
- [x] **FW-002** Layer 2: Product Intelligence Kit (PIK) — WCR, Discovery Intake, PFD, VH, AR, EL, DPRD
- [x] **FW-003** Layer 4: Engineering Execution Kit (EEK) — KER, PRD, ACF, SAD, DCF, TDD, WDD, ORD + BAT
- [x] **FW-004** Layer 5: Release & Exposure Kit (REK) — RER, RCF, RSA, RP, RR
- [x] **FW-005** Layer 6: Reliability & Resilience Kit (RRK) — SRER, SRP, IR, RHR
- [x] **FW-006** Layer 7: Insight & Evolution Kit (IEK) — ES, PES
- [x] **FW-007** Layer 8: Operational Diagnostics Kit (ODK) — DCR, INR, PMR, RB
- [x] **FW-008** Freeze-before-promote enforcement, artifact provenance tracking, deprecation lifecycle

### 2026-03-04 to 2026-03-06: Governance Hardening

- [x] **FW-009** Amendment model, Freeze Pending status, principle versioning
- [x] **FW-010** Cross-kit escalation protocols
- [x] **FW-011** Structural auto-validation script (`check-structure.sh`)
- [x] **FW-012** End-to-end cross-kit example narrative (Taskflow)
- [x] **FW-013** Engagement Record spec (v1.0) and getting-started guide
- [x] **FW-014** Initiative presets (P1–P5 golden paths)
- [x] **FW-015** Repo renamed `aieos-spec` → `aieos-governance-foundation`; open-sourced (MIT)

### 2026-03-08 to 2026-03-09: Standards & Cross-Cutting Kits

- [x] **FW-016** AI Transparency Principles (v1.0)
- [x] **FW-017** Spec file versioning standard — all 33 specs at v1.0, all 30 templates with provenance fields
- [x] **FW-018** Layer 9: Quality Assurance Kit (QAK) — QAER, VP, TCR, QGR
- [x] **FW-019** Layer 10: Security & Compliance Kit (SCK) — TM, SAR, CER, DAR
- [x] **FW-020** Layer 11: Data & Configuration Kit (DCK) — CSPEC, FFLR, DSR
- [x] **FW-021** Layer 12: Platform & Infrastructure Kit (PINFK) — PDR, ISPEC, EM

### 2026-03-10: Documentation Kit & Code Quality

- [x] **FW-022** Layer 13: Documentation & Knowledge Kit (DKK) — UDR, ARR, SKA, DHR
- [x] **FW-023** BAT four-file gap closure (spec, template, validator, escalation template)
- [x] **FW-024** Narrative code documentation standard in `code-craftsmanship.md`
- [x] **FW-025** Dependency direction / onion architecture rule (SAD + TDD layer assignment)
- [x] **FW-026** Flow Reference document (entry points, exit conditions, parallelism rules, escalation paths)
- [x] **FW-027** QAK-SCK integration fix (VP accepts frozen TM + SAR)

### 2026-03-11: Testing, Tools, Navigation & Remaining Kits

- [x] **FW-028** Three-tier automated testing (Tier 1 lint, Tier 2 pytest 69 tests, Integration drivers)
- [x] **FW-029** Tool governance infrastructure (meta-spec v1.0, 7 hard gates, four-file system for tools)
- [x] **FW-030** AI Sherpa navigation system — navigation map (~70 nodes, ~140 edges, 28 junctions), 4 navigation tools (initiative-router, position-check, decision-router, handoff-navigator), 6 Claude Code bindings
- [x] **FW-031** Layer 14: Peer Review Kit (PRK) — PRR, 9 review lens tools, 9 review points
- [x] **FW-032** Layer 3: Solution Sourcing Kit (SSK) — SOER, VER, SDR (16 hard gates)
- [x] **FW-033** Healthcheck playbook (4 framework checks, 7 initiative checks)

### 2026-03-13: Final Kits

- [x] **FW-034** Layer 1: Strategic Direction Kit (SDK) — SBR, PPR
- [x] **FW-035** Layer 15: Business Process Kit (BPK) — PIA, TP, RC
- [x] **FW-036** Adapter conformance spec and integration tool governance

### 2026-03-14 to 2026-03-16: Sherpa & Governance Enhancements

- [x] **SH-001** Sherpa bootstrap prompt and skill definition
- [x] **SH-002** Sherpa integration test suite (9 drivers: P1–P5, ambiguous, convergence, resumption, negative)
- [x] **SH-003** Sherpa conversation rubric (manual evaluation, 11 criteria, 3 test personas)
- [x] **FW-037** Decision Outcome Taxonomy (6 outcomes in flow-reference.md §11)
- [x] **FW-038** PRK expanded to 12 lenses (+ observability, resilience)
- [x] **FW-039** SMR in PINFK, RSA in REK
- [x] **FW-040** Ecosystem roadmap documented (7 adjacent projects identified)

### 2026-03-17: Sherpa 14-Feature Enhancement Program

- [x] **SH-004** Sherpa Journal — append-only operational log with 7 entry types
- [x] **SH-005** Decision Rationale Replay — "why did we decide X?" with journal citations
- [x] **SH-006** Session Resumption with Journal — reconstruct context, preferences, open threads
- [x] **SH-007** Upstream Risk Surfacing — 5 risk patterns scanned before generation
- [x] **SH-008** Heuristic Utility Triggers — 7 context-driven triggers replacing static checklist
- [x] **SH-009** Predictive Path Warnings — exact artifact count, bottleneck alerts at routing
- [x] **SH-010** Fast-Path Detection — 7-kit skip/adopt criteria for cross-cutting decisions
- [x] **SH-011** Quality Scoring — completeness_score with tiered assessment and gap hints
- [x] **SH-012** Cross-Artifact Consistency Checks — 7 defined artifact pairs
- [x] **SH-013** Finding Accumulator — 4 detection patterns for framework gaps
- [x] **SH-014** Cross-Initiative Awareness — sibling ER scanning for overlap detection
- [x] **SH-015** Parallel Artifact Orchestration — 7 parallelizable pairs from flow-reference
- [x] **SH-016** Template Pre-Population — 7 field mapping categories from upstream
- [x] **SH-017** Initiative Retrospective — structured completion report for IEK input
- [x] **SH-018** Sherpa Self-Scoring — auto-evaluate 15 rubric criteria from journal evidence
- [x] **SH-019** Elicitation Protocol — 6 named reasoning techniques for pre-generation
- [x] **SH-020** Briefing Distillation tool — compressed frozen artifact summaries for downstream

### 2026-03-18: Sherpa Rubric Hardening

- [x] **SH-021** 3 live rubric tests (P5/PM x2, P2/TechLead) — score 54/65 → 68/70 (avg 4.9)
- [x] **SH-022** 15 issues fixed: intake probing, freeze counter, permission-seeking, structured output emission
- [x] **SH-023** Critical Rules expanded 11 → 18 bullets; intent translation timing; conditional opening
- [x] **SH-024** Integration checks expanded to 53; BDD scenarios to 111; Tier 2 to 199 tests

### Initiative: aieos-console (ER-CONSOLE-001)

- [x] **INIT-C-001** Layer 2 (PIK): All artifacts frozen (WCR through DPRD) — 2026-03-07
- [x] **INIT-C-002** Layer 4 (EEK): All artifacts frozen through ORD — 259 tests passing — 2026-03-08
- [x] **INIT-C-003** Layer 5 (REK): RER, RCF, RP, RR frozen — release disposition: successful-full-exposure — 2026-03-08
- [x] **INIT-C-004** 10 framework findings documented and all fixed upstream
- [x] **INIT-C-005** Docker verification — image SHA `7252527c`

---

## In Progress

### Initiative: aieos-search (ER-SEARCH-001)

- [x] **INIT-S-001** Layer 4 entry (Path B): KER-SEARCH-001 frozen — 2026-03-18
- [x] **INIT-S-002** PRD-SEARCH-001 frozen (from Product Brief) — 2026-03-18
- [x] **INIT-S-003** ACF-SEARCH-001 frozen — 2026-03-18
- [x] **INIT-S-004** SAD-SEARCH-001 frozen (5 components, async index sync, circuit breaker) — 2026-03-18
- [ ] **INIT-S-005** DCF-SEARCH-001 — in progress
- [ ] **INIT-S-006** TDD-SEARCH-001
- [ ] **INIT-S-007** WDD-SEARCH-001
- [ ] **INIT-S-008** Execution Plan + code execution
- [ ] **INIT-S-009** ORD-SEARCH-001
- [ ] **INIT-S-010** Cross-cutting kit adoption decisions (QAK, SCK, DCK, DKK, PRK)
- [ ] **INIT-S-011** Layer 5 (REK): RER through RR
- [ ] **INIT-S-012** Layer 6 (RRK): SRER, SRP, RHR

### Initiative: aieos-console (remaining layers)

- [ ] **INIT-C-006** Layer 6 (RRK): SRER, SRP, first RHR — handoff from RR-CONSOLE-001 §7
- [ ] **INIT-C-007** Layer 7 (IEK): ES after sufficient RHR observation period

---

### 2026-03-19: Kit Audit — 12 Findings Fixed

- [x] **FW-041** H-1: PIK DPRD spec — added gate 9 `principles_coverage` to match validator
- [x] **FW-042** H-2: PIK DPRD prompt — removed cross-kit dependency on EEK `product-craftsmanship.md`; references PIK `product-discovery-principles.md` only
- [x] **FW-043** H-3: QAK — created `qa-principles.md` v1.0 (6 principles)
- [x] **FW-044** M-1: REK — created `entry-from-qak.md` and `entry-from-sck.md` boundary documents
- [x] **FW-045** M-2: RRK — SRER spec allows deferred SLO baselines with capture trigger notation
- [x] **FW-046** M-3: DCK — created `configuration-principles.md` v1.0 (6 principles)
- [x] **FW-047** M-4: PINFK — created `infrastructure-principles.md` v1.0 (6 principles); defined SMR trigger (3+ services) and downstream consumers
- [x] **FW-048** M-5: DKK — defined DHR cadence (semi-annual minimum, quarterly default)
- [x] **FW-049** L-1: Governance model — added entry gate exception to four-file rule; synced to all 15 kits
- [x] **FW-050** L-2: DCK — fixed DSR downstream from "EEK" to "REK/RRK"
- [x] **FW-051** L-3: DKK — added DHR health score default weighting (Coverage 40%, Currency 30%, Accuracy 30%)
- [x] **FW-052** L-4: QAK — added frozen TM and SAR from SCK as optional VP upstream inputs
- [x] **SH-025** Extracted `aieos-sherpa` as standalone project with canonical tool-agnostic prompt, Claude Code adapter, generic bootstrap adapter, docs, and test suite

---

## Planned — Framework Refinement

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **FR-001** | Run sherpa manual rubric tests for P1/Skeptic and P3/PM personas | High | — | Two untested persona/preset combinations from the rubric test matrix |
| **FR-002** | Run sherpa manual rubric test for P4/PM (ODK flow) | Medium | — | Tests incident-triggered flow with non-technical persona |
| **FR-003** | Promote soft behavioral checks to hard checks as compliance rates stabilize | Medium | FR-001, FR-002 | Track per-check pass rates; promote at >80% across 3+ runs |
| **FR-004** | Integration test for cross-initiative awareness | Medium | — | Needs fixture with pre-existing sibling initiative ER |
| **FR-005** | Integration test for parallel artifact orchestration | Low | — | Verify ACF+SAD parallel generation in P1/P2 driver |
| **FR-006** | Validate IEK entry-from alignment with retrospective format | Low | INIT-C-007 | Confirm retrospective → ES mapping works end-to-end |

---

## Planned — Ecosystem Projects

Documented in detail at `docs/ecosystem-roadmap.md`. These are real software projects that operationalize the governance framework.

### Phase 1: Critical Path

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-001** | AIEOS Schema | `aieos-schema` | Machine-readable spec contracts (YAML/JSON). Strengthens framework Tier 2 tests (spec-template drift, gate enumeration, prompt checklist alignment) AND unlocks all downstream ecosystem projects. | Not started | None — this is the keystone |
| **ECO-002** | Evaluation Engine | `aieos-evaluation-engine` | Runtime governance enforcement. Consumes schema to validate artifacts programmatically instead of relying solely on AI judgment. | Not started | ECO-001 |
| **ECO-003** | Artifact Store | `aieos-artifact-store` | Cross-initiative artifact indexing. Query "show me all frozen SADs across all initiatives" or "which initiatives touched the auth module." | Not started | ECO-001 |

### Phase 2: Observe & Integrate

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-004** | System Twin | `aieos-system-twin` | Live system topology graph. Maps what's running in production to what's governed in AIEOS. | Not started | ECO-001, ECO-003 |
| **ECO-005** | Playground | `aieos-playground` | Interactive learning environment. Guided walkthrough of AIEOS with sandbox initiatives. | Not started | ECO-001 |

### Phase 3: Measure & Report

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-006** | Governance Analytics | `aieos-governance-analytics` | Cross-initiative intelligence. Quality trends, cycle time, finding patterns, adoption rates. | Not started | ECO-001, ECO-003 |
| **ECO-007** | Compliance Reporter | `aieos-compliance-reporter` | Automated audit packages. Generate compliance evidence from frozen artifacts + ER history. | Not started | ECO-001, ECO-003 |

---

## Backlog

Ideas not yet prioritized or scoped. Move to Planned when ready to commit.

| ID | Idea | Category | Notes |
|----|------|----------|-------|
| **BL-001** | Multi-org governance — federated AIEOS instances sharing specs but independent initiatives | Framework | Needs org-boundary model in governance-model.md |
| **BL-002** | Governance model versioning migration tooling — automated sync when GM version bumps | Framework | Currently manual across 15 kit copies |
| **BL-003** | Sherpa voice/chat mode — conversational UI beyond CLI | Sherpa | Depends on Claude capabilities |
| **BL-004** | Artifact diff visualization — show what changed between artifact versions | Ecosystem | Useful for re-entry/amendment flows |
| **BL-005** | Initiative portfolio dashboard — active/complete/abandoned across all ERs | Ecosystem | Lightweight version of ECO-006 |
| **BL-006** | Spec authoring assistant — guided creation of new artifact types with four-file scaffold | Framework | Would help external contributors extend AIEOS |
| **BL-007** | Adapter library — pre-built adapters for GitHub Issues, Linear, Jira for tool bindings | Ecosystem | Per adapter-conformance-spec.md |
| **BL-008** | Ideation & Opportunity Kit (IOK) — pre-Layer-1 kit governing structured ideation with OLR, ISR, OB artifacts | Framework | Full four-file system for ideation. Graduate from sherpa ideation mode (SH-026/FW-053) if ideation proves valuable enough to warrant its own governance layer. Flow: Signals → OLR → ISR(s) → OB(s) → SDK or PIK |

---

## How to Use This Roadmap

**Adding items:** Append to the appropriate section with the next available ID in that category (FW-NNN for framework, SH-NNN for sherpa, INIT-X-NNN for initiatives, ECO-NNN for ecosystem, FR-NNN for refinement, BL-NNN for backlog).

**Completing items:** Move from Planned/In Progress to Completed with a date. Change `[ ]` to `[x]`.

**Prioritizing backlog:** Move items from Backlog to Planned when scope and dependencies are clear.

**ID prefixes:**
- `FW` — Framework core (kits, governance, testing)
- `SH` — Sherpa capabilities
- `INIT-C` — aieos-console initiative
- `INIT-S` — aieos-search initiative
- `FR` — Framework refinement (testing, hardening)
- `ECO` — Ecosystem software projects
- `BL` — Backlog (unprioritized ideas)
