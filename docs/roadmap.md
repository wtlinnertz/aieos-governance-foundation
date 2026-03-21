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
- [x] **SH-026** Sherpa Ideation Mode — structured brainstorming when user doesn't have a concrete idea
- [x] **FW-053** PIK Ideation Workshop utility prompt — 7 named techniques, technique selection guide, Ideation Workshop Record output format

### 2026-03-20: SDK Roadmap Governance + Roadmap Ideation

- [x] **FW-054** CLA (Capability Lifecycle Assessment) — 6 hard gates incl. `user_provided_inventory` and tightened `signal_basis`; retroactive onboarding entry point
- [x] **FW-055** PCR (Product Capability Roadmap) — 6 hard gates incl. `capacity_realistic`; 1-3 year horizon
- [x] **FW-056** TIR (Technology Investment Roadmap) — 5 hard gates incl. `driver_traced`; 2-5 year horizon
- [x] **FW-057** SDK playbook — 2 phases (Roadmap + Bets), 5 steps, roadmap ideation utility, retroactive onboarding guidance
- [x] **FW-058** ER spec §1a updated with CLA/PCR/TIR; framework.py updated with dependency edges and IEK→CLA feedback
- [x] **SH-027** Roadmap ideation techniques (R1-R7) in PIK ideation workshop prompt + sherpa roadmap detection and SDK routing
- [x] **FW-059** PIK entry-from-sdk.md updated with PCR as optional upstream artifact
- [x] **ECO-003** AIEOS Artifact Store (`aieos-artifact-store`) — LanceDB vector search over frozen artifacts. Chunker, metadata extractor, embedding wrapper, ingest pipeline, query interface. 23 tests, 44 artifacts ingested from aieos-console (431 chunks). 3 sherpa integration points documented.

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
| **FR-007** | Append-only Decision Register — cross-layer `decision-log.md` alongside ER | High | — | Inspired by GSD. Decisions never edited, only superseded. Structured format: decision ID, layer, artifact context, options, rationale, date. Sherpa appends at every junction. |
| **FR-008** | Machine-readable initiative state — structured block in ER or separate `state.md` | Medium | — | Inspired by GSD. Current layer, current artifact, blocking deps, next action, frozen count. Position-check reads this instead of reconstructing from scattered files. |
| **FR-009** | Reassessment gates at layer transitions — check upstream assumptions still valid | Medium | FR-007 | Inspired by GSD. At each kit transition, compare current state against DPRD/PRD assumptions. If material divergence detected, trigger lightweight re-validation. New gate type in flow-reference.md. |
| **FR-010** | Auto-repair healthchecks — `check-structure.sh --repair` flag | Medium | — | Inspired by GSD. Auto-fix: governance model sync, missing spec versions, broken file refs. Healthcheck playbook gains "Remediation" column (auto-remediable vs. manual). |
| **FR-011** | Effort ceiling governance — initiative-level thresholds with graduated enforcement | Low | — | Inspired by GSD. Max convergence iterations, max PRK cycles. At 50%: flag. At 75%: sponsor re-auth. At 90%: escalate to SDK for kill/pivot. |
| **FR-012** | Verification tier classification — classify validator gates as Structural/Referential/Semantic/Human | Low | — | Inspired by GSD. Tells you which tier caught an issue. Run cheap tiers frequently, reserve expensive tiers for milestones. |
| **FR-013** | Process forensics template — lightweight root cause analysis when the governance pipeline stalls | Low | — | Inspired by GSD. Distinct from ODK (production incidents). Covers: scope creep, ambiguous spec, wrong preset, missing context. Referenced from healthcheck-playbook.md. |

### Organizational Readiness Gaps

| ID | Item | Priority | Kit | Dependencies | Notes |
|----|------|----------|-----|-------------|-------|
| **ORG-001** | Skills Gap Assessment — pre-execution check in EEK | High | EEK | — | Before WDD, assess team capabilities vs. required skills (languages, frameworks, domain expertise, ops skills). Identifies training needs or hiring/contracting dependencies. Blocks execution planning if critical gaps unresolved. |
| **ORG-002** | Service Ownership Record — comprehensive ownership matrix | High | REK or RRK | — | Who owns: code, on-call, L1/L2/L3 support, product decisions, documentation, dependency updates. Frozen before Layer 6 entry. Extends beyond SRER's reliability-only ownership. |
| **ORG-003** | Extend RRK SRP with support tier definitions | Medium | RRK | ORG-002 | Add L1/L2/L3 support routing, escalation paths, support hours, handoff triggers to SRP spec. Currently SRP covers SLOs but not the human support model. |
| **ORG-004** | Launch Communications Plan — internal + external messaging | Medium | REK | — | New artifact in REK between RP and RR. Internal: org announcement, stakeholder briefing, support team enablement. External: customer comms, changelog, migration guide (if applicable). |
| **ORG-005** | Adoption Plan — strategy, metrics, feedback loops | Medium | REK | ORG-004 | Extend RP or add new artifact. Covers: rollout strategy (big bang vs. phased), adoption success metrics, feedback channels, time-to-value targets, what "adopted" means. Goes beyond BPK's process training. |
| **ORG-006** | Update initiative presets with new artifacts | Low | Governance Foundation | ORG-001 through ORG-005 | Add skills assessment, ownership record, launch comms, adoption plan to P1/P2/P3 preset artifact sequences. Update ER spec with new layer sections. |

### Cross-AI Compatibility (2026-03-19) — Complete

- [x] **FR-008** Machine-readable State Block (§1b) in ER spec — 7-field structured position snapshot
- [x] **XAI-001** Copilot CLI adapter — loading guide, limitations, workarounds
- [x] **XAI-002** AI capability matrix — 9 capabilities × 5 platforms with fallbacks
- [x] **XAI-003** Cross-AI session handoff protocol — checklist, resumption command, troubleshooting
- [x] **XAI-004** Compressed prompt (267 lines, 57% reduction, all sections preserved)
- [x] **XAI-005** Validator consistency testing methodology
- [x] **XAI-006** Smoke test extended to 49 checks (adapter dirs, compact parity, state block)

---

## Planned — Ecosystem Projects

Documented in detail at `docs/ecosystem-roadmap.md`. These are real software projects that operationalize the governance framework.

### Phase 1: Critical Path

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-001** | AIEOS Schema | `aieos-schema` | Machine-readable spec contracts (YAML/JSON). Strengthens framework Tier 2 tests (spec-template drift, gate enumeration, prompt checklist alignment) AND unlocks all downstream ecosystem projects. | Not started | None — this is the keystone |
| **ECO-002** | Evaluation Engine | `aieos-evaluation-engine` | Runtime governance enforcement. Consumes schema to validate artifacts programmatically instead of relying solely on AI judgment. | Not started | ECO-001 |
| **ECO-003** | Artifact Store | `aieos-artifact-store` | Cross-initiative artifact indexing. Query "show me all frozen SADs across all initiatives" or "which initiatives touched the auth module." | **Complete** (v1.0.0) | — (built without Schema dependency) |

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

## Planned — Gap Closure (from 2026-03-21 gap analysis)

### Tier 1: Will come up in first real initiative at work

Build these when you hit them during a real initiative — don't build speculatively.

| ID | Gap | Approach | Priority | Notes |
|----|-----|----------|----------|-------|
| **GAP-001** | Technical debt governance | Extend EEK or create cross-cutting artifact. New artifact: **Technical Debt Register (TDR)** — append-only log of debt accrued during execution (what, why, interest cost, paydown plan). Updated during EEK code execution and at each RHR. | High | Don't create a new kit. Add TDR as a cross-cutting artifact in EEK with RRK maintenance. Tracked alongside ER. |
| **GAP-002** | Data privacy / classification | Extend SCK. Add **Data Classification Record (DCL)** as a new SCK artifact — maps all data handled by the initiative to classification levels (PII, PHI, confidential, internal, public). Add hard gate to SAD spec requiring data classification reference. GDPR impact assessment folds into CER. | High | SCK already governs security; privacy is the missing half. DCL triggers after PFD (when data scope is known) and feeds TM + SAR. |
| **GAP-003** | Accessibility compliance | Don't create a new kit. Add accessibility as hard gates to existing specs: PRD spec gains `accessibility_requirements` gate (WCAG level stated); TDD spec gains `accessibility_test_coverage` gate; QAK VP gains accessibility as a test dimension. | High | Lightest possible touch — 3 spec edits, no new kit. Add when the first initiative has user-facing output. |
| **GAP-004** | Operational maintenance governance | Extend RRK (Layer 6), not a new kit. Add **Operational Maintenance Plan (OMP)** artifact to RRK — covers: dependency update cadence, patch policy, secret rotation schedule, backup/DR drill schedule, data retention enforcement. Frozen after first SRP, revised at each RHR. | High | RRK already owns production. OMP is the "steady-state care plan" that SRP doesn't cover. |
| **GAP-005** | Cost governance | Extend SDK. Add cost fields to PCR (budget per capability) and SBR (investment envelope already exists but no tracking). Add **Cost Tracking Record (CTR)** as an optional cross-cutting artifact — actual spend vs. budget at each layer transition. | Medium | Start light: add fields to existing artifacts first. CTR as a full artifact only if cost tracking proves essential. |

### Tier 2: Causes friction at scale

Address when scaling beyond solo/small team use.

| ID | Gap | Approach | Priority | Notes |
|----|-----|----------|----------|-------|
| **GAP-006** | Deprecation/sunset lifecycle | Extend REK (Layer 5). CLA already marks capabilities for sunset. Add **Deprecation Execution Plan (DEP)** to REK — covers: migration path execution, communication timeline, dependency notification, data archival, monitoring teardown. Uses RP/RR patterns but for removal instead of deployment. | Medium | Don't create a new kit. REK already handles release mechanics; deprecation is "release in reverse." |
| **GAP-007** | Customer/support feedback loop | Extend IEK (Layer 7). Add **Feedback Synthesis Record (FSR)** — aggregates support ticket themes, customer feedback, NPS signals into structured input for next ES. Triggered periodically (quarterly) or when support volume spikes. | Medium | IEK's ES is too high-level for granular feedback. FSR is the mid-layer synthesis that's missing. DKK SKA captures individual articles; FSR captures patterns. |
| **GAP-008** | Cross-team coordination | Extend ER spec with a **Cross-Initiative Dependency Map** section. When multiple initiatives share systems/teams, each ER §Dependencies lists the other ERs it depends on or conflicts with. Sherpa cross-initiative scan (already built) detects these; this formalizes the tracking. | Medium | Don't create a new kit. Extend ER + leverage existing cross-initiative awareness in the sherpa. Only matters at 3+ concurrent initiatives. |
| **GAP-009** | Decision authority (RACI) | Add to ER §1 Document Control: a **Decision Authority Table** — lists who can approve freeze at each layer (by role, not by name). Replaces ad-hoc "who approves this?" with explicit authority. | Medium | Lightest possible touch: one new section in an existing artifact. No new kit, no new spec. Fill in at initiative start, reference at each freeze. |

### Guidance: What NOT to build yet

These gaps are real but should be demand-driven, not speculative:

- **ML/AI model governance** — Build when you have an ML initiative. Extend EEK TDD with model-specific gates, not a new kit.
- **Design system / UX patterns** — Build when you have 3+ initiatives sharing UI patterns. Could be a DKK extension.
- **Team health / burnout signals** — Important but organizational, not framework. Track outside AIEOS unless you find a natural artifact home.
- **Solo operator preset** — Address friction as you encounter it. The framework already has solo-operator notes in REK.
- **Async/distributed team support** — Address with process guidance in playbooks, not new artifacts.

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
