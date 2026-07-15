# AIEOS Roadmap

Single-source tracking for completed work, active initiatives, and planned items across the AIEOS governance framework and system.

**Last updated:** 2026-07-15 (v1.3 "Three Drivers" internal release. Corrected 2026-07-15: the first validation against a real model found the three-driver claim is only partially delivered — the shared freeze/state/lock engine is real and verified, the console leg is not yet reachable on a real kit. See Known limitations.)

**Framework state:** 42 repos, 15 layers. Spec-driven CI/CD live on `aieos-artifact-store`; v1.2 quality pass closed 2026-07-05; v1.3 tagged 2026-07-13.

---

## Current status

v1.3 "Three Drivers" was cut internally on 2026-07-13. It delivers a shared governance engine — one freeze authority, one canonical state block, one cross-driver lock — plus a new autonomous driver, the dark factory. The goal is for sherpa, the console, and the dark factory to run as three drivers over that one engine. **That goal is partially delivered.** The engine is real and now verified against a live model; the console leg is not yet reachable on a real kit. See Known limitations below.

What shipped:

- **A single freeze authority.** Only the harness `apply_freeze_decision` writes `FROZEN`, gated by a human decision and a content-hash check against exactly what the reviewer was shown. It writes nothing on any refusal. Verified against a real model on 2026-07-15, where it correctly declined to promote a failing artifact (FR-020).
- **A canonical freeze representation.** `document-control.yaml` defines one Document Control block, with freeze status and validation outcome as orthogonal fields, plus a harness reader/writer and an instance validator. It is authoritative wherever the harness writes it (FR-018 — see limitations).
- **A cross-driver ownership lock.** One lease-based lock file with session-id ownership and a heartbeat, implemented in both Python (harness) and TypeScript (console) against the same wire format. A crashed unattended run expires instead of wedging the initiative (FR-019).
- **The dark factory: autonomous conductor.** A new control plane (`aieos-dark-factory`) walks the freeze-DAG from `kit-manifest.yml`, parks at each freeze gate, escalates on non-convergence, and halts on an andon signal. It records every decision to an append-only hash-chained Decision Register (FR-007) and never writes `FROZEN` itself.
- **The dark factory to harness path runs against a real model.** On 2026-07-15 a real provider generated a full architecture document from frozen upstream artifacts, the validator returned structured JSON, and the convergence loop parsed it and escalated rather than promoting. All new repos are under CI.

### Known limitations (found by real-model validation, 2026-07-15)

The v1.3 switch proof used a mock provider that returns a canned pass, so it exercised the plumbing without testing any place two real components meet. The first run against a real model and the real kits found the following. All are tracked for v1.3.1 and v1.4.

- **The console cannot yet load a real kit.** It requires a per-kit `flow.yaml`, which no kit repo provides. `kit-manifest.yml` is this framework's declared machine-readable source of truth, and the console does not yet consume it. The console's freeze path is implemented and calls the harness correctly, but it is not reachable on a real initiative until this closes — so the three-way switch is not yet demonstrable end to end.
- **Kit templates do not yet emit the canonical Document Control block.** 15 of 78 templates use the canonical `Artifact ID` field; the rest carry an older shape and status vocabulary. The harness compensates by writing a canonical block when it persists an artifact, which means a generated artifact can carry two Document Control sections. Template migration, and wiring the instance validator into artifact CI, are outstanding.
- **Five artifact types are not autonomously drivable.** The `prd`, `acf`, `dcf`, `dkr`, and `tdd` prompts require principles files as mandatory input, and the harness has no seam to supply them. Separately, entry-point artifacts such as the PRD take their input from a human brief by design and are not intended for autonomous generation.
- **Validator calibration is unresolved.** In back-to-back runs the same validator prompt and model returned opposite verdicts on one hard gate, and in one case failed an artifact for a requirement the spec explicitly exempts. FR-014 covers this, and it is a prerequisite for trusting autonomous promotion.
- **The harness needs explicit UTF-8 file I/O to run on Windows.** CI currently covers Linux only. Tracked for v1.3.1 with a Windows CI job.

---

The v1.2 Framework Quality Pass closed on 2026-07-05. What changed since the March snapshot below:

- **Every repo is under CI.** `aieos-governance-foundation` (B1), `aieos-agent-harness` (B2), all 13 adapters (conformance + signing), and all 15 kit repos (B3) run automated checks on every push.
- **The adapter layer produces real signed attestations.** All 13 adapters pass conformance and emit signed Sigstore attestations in CI, with `continue-on-error` removed so a regression can't pass silently. The earlier "no executable adapters exist" state is closed.
- **Signing identity is verified end-to-end.** M0 chose Sigstore keyless (Fulcio + Rekor); the full build-attest-verify loop runs green (see the 2026-05-17 entry).
- **The agent-harness orchestration core is at 100% line coverage** (routing, state, lifecycle, convergence), running under the B2 job.

Full detail is in the dated Completed entries. Active work and everything still planned are unchanged from the sections further down.

---

## Completed

### Framework foundation (pre-March 2026)

- [x] **FW-001** Core governance model with four-file invariant (spec, template, prompt, validator)
- [x] **FW-002** Layer 2: Product Intelligence Kit (PIK) — WCR, Discovery Intake, PFD, VH, AR, EL, DPRD
- [x] **FW-003** Layer 4: Engineering Execution Kit (EEK) — KER, PRD, ACF, SAD, DCF, TDD, WDD, ORD + BAT
- [x] **FW-004** Layer 5: Release & Exposure Kit (REK) — RER, RCF, RSA, RP, RR
- [x] **FW-005** Layer 6: Reliability & Resilience Kit (RRK) — SRER, SRP, IR, RHR
- [x] **FW-006** Layer 7: Insight & Evolution Kit (IEK) — ES, PES
- [x] **FW-007** Layer 8: Operational Diagnostics Kit (ODK) — DCR, INR, PMR, RB
- [x] **FW-008** Freeze-before-promote enforcement, artifact provenance tracking, deprecation lifecycle

### 2026-03-04 to 2026-03-06: governance hardening

- [x] **FW-009** Amendment model, Freeze Pending status, principle versioning
- [x] **FW-010** Cross-kit escalation protocols
- [x] **FW-011** Structural auto-validation script (`check-structure.sh`)
- [x] **FW-012** End-to-end cross-kit example narrative (Taskflow)
- [x] **FW-013** Engagement Record spec (v1.0) and getting-started guide
- [x] **FW-014** Initiative presets (P1–P5 golden paths)
- [x] **FW-015** Repo renamed `aieos-spec` → `aieos-governance-foundation`; open-sourced (MIT)

### 2026-03-08 to 2026-03-09: standards & cross-Cutting kits

- [x] **FW-016** AI Transparency Principles (v1.0)
- [x] **FW-017** Spec file versioning standard — all 33 specs at v1.0, all 30 templates with provenance fields
- [x] **FW-018** Layer 9: Quality Assurance Kit (QAK) — QAER, VP, TCR, QGR
- [x] **FW-019** Layer 10: Security & Compliance Kit (SCK) — TM, SAR, CER, DAR
- [x] **FW-020** Layer 11: Data & Configuration Kit (DCK) — CSPEC, FFLR, DSR
- [x] **FW-021** Layer 12: Platform & Infrastructure Kit (PINFK) — PDR, ISPEC, EM

### 2026-03-10: documentation kit & code quality

- [x] **FW-022** Layer 13: Documentation & Knowledge Kit (DKK) — UDR, ARR, SKA, DHR
- [x] **FW-023** BAT four-file gap closure (spec, template, validator, escalation template)
- [x] **FW-024** Narrative code documentation standard in `code-craftsmanship.md`
- [x] **FW-025** Dependency direction / onion architecture rule (SAD + TDD layer assignment)
- [x] **FW-026** Flow Reference document (entry points, exit conditions, parallelism rules, escalation paths)
- [x] **FW-027** QAK-SCK integration fix (VP accepts frozen TM + SAR)

### 2026-03-11: testing, tools, navigation & remaining kits

- [x] **FW-028** Three-tier automated testing (Tier 1 lint, Tier 2 pytest 69 tests, Integration drivers)
- [x] **FW-029** Tool governance infrastructure (meta-spec v1.0, 7 hard gates, four-file system for tools)
- [x] **FW-030** AI Sherpa navigation system — navigation map (~70 nodes, ~140 edges, 28 junctions), 4 navigation tools (initiative-router, position-check, decision-router, handoff-navigator), 6 Claude Code bindings
- [x] **FW-031** Layer 14: Peer Review Kit (PRK) — PRR, 9 review lens tools, 9 review points
- [x] **FW-032** Layer 3: Solution Sourcing Kit (SSK) — SOER, VER, SDR (16 hard gates)
- [x] **FW-033** Healthcheck playbook (4 framework checks, 7 initiative checks)

### 2026-03-13: final kits

- [x] **FW-034** Layer 1: Strategic Direction Kit (SDK) — SBR, PPR
- [x] **FW-035** Layer 15: Business Process Kit (BPK) — PIA, TP, RC
- [x] **FW-036** Adapter conformance spec and integration tool governance

### 2026-03-14 to 2026-03-16: sherpa & governance enhancements

- [x] **SH-001** Sherpa bootstrap prompt and skill definition
- [x] **SH-002** Sherpa integration test suite (9 drivers: P1–P5, ambiguous, convergence, resumption, negative)
- [x] **SH-003** Sherpa conversation rubric (manual evaluation, 11 criteria, 3 test personas)
- [x] **FW-037** Decision Outcome Taxonomy (6 outcomes in flow-reference.md §11)
- [x] **FW-038** PRK expanded to 12 lenses (+ observability, resilience)
- [x] **FW-039** SMR in PINFK, RSA in REK
- [x] **FW-040** system roadmap documented (7 adjacent projects identified)

### 2026-03-17: sherpa 14-Feature enhancement program

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

### 2026-03-18: sherpa rubric hardening

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

## In progress

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

### 2026-03-19: kit audit — 12 findings fixed

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

### 2026-03-20: SDK roadmap governance + roadmap ideation

- [x] **FW-054** CLA (Capability Lifecycle Assessment) — 6 hard gates incl. `user_provided_inventory` and tightened `signal_basis`; retroactive onboarding entry point
- [x] **FW-055** PCR (Product Capability Roadmap) — 6 hard gates incl. `capacity_realistic`; 1-3 year horizon
- [x] **FW-056** TIR (Technology Investment Roadmap) — 5 hard gates incl. `driver_traced`; 2-5 year horizon
- [x] **FW-057** SDK playbook — 2 phases (Roadmap + Bets), 5 steps, roadmap ideation utility, retroactive onboarding guidance
- [x] **FW-058** ER spec §1a updated with CLA/PCR/TIR; framework.py updated with dependency edges and IEK→CLA feedback
- [x] **SH-027** Roadmap ideation techniques (R1-R7) in PIK ideation workshop prompt + sherpa roadmap detection and SDK routing
- [x] **FW-059** PIK entry-from-sdk.md updated with PCR as optional upstream artifact
- [x] **ECO-003** AIEOS Artifact Store (`aieos-artifact-store`) — LanceDB vector search over frozen artifacts. Chunker, metadata extractor, embedding wrapper, ingest pipeline, query interface. 23 tests, 44 artifacts ingested from aieos-console (431 chunks). 3 sherpa integration points documented.

### 2026-03-25 to 2026-03-27: AI-Native SDLC alignment, new projects, governance enhancements

- [x] **FW-060** AI-Native SDLC v3.1 alignment assessment — 328 items scored (92% FE+PA), 21 gaps, 8 PA thickening packages
- [x] **FW-061** TOOL-DIAGRAM-EXPORT — Mermaid extraction with 3 bindings (drawio, SVG, PNG) + Python CLI implementation (33 tests)
- [x] **FW-062** FR-007 Decision Register — ER spec v1.7, append-only decision format, 8 types, 7 Tier 2 tests, console ER backfilled (12 decisions)
- [x] **FW-063** Sherpa auto-ingest — frozen artifacts automatically indexed in artifact store at freeze time
- [x] **FW-064** Documentation audit — 15 discrepancies fixed across 8 projects, all 22 projects verified clean
- [x] **ECO-009** Agent Harness (`aieos-agent-harness`) — 16 source files, 166 tests, 5 components, 4 routing strategies, 7 invariants. Retroactively governed (ER-HARNESS-001, 8 artifacts frozen). AI SDLC Governance Level 2. GitHub: wtlinnertz/aieos-agent-harness.
- [x] **NEW** AI SDLC Governance (`ai-sdlc-governance`) — Standalone practice governance framework. 38 files, 30 Foundation gates, 94 Standards checklist items, 4 Guidance playbooks, 3 assessment tools. GitHub: wtlinnertz/ai-sdlc-governance.

### 2026-04-10: kit sync agent system

- [x] **FW-065** Kit Manifest (`kit-manifest.yml`) — machine-readable single source of truth for all kit metadata: 15 kits, 63 artifacts, 80 dependency edges, 6 entry points, 5 presets, 21 boundary contracts, cross-cutting triggers with feeds-into model
- [x] **FW-066** TOOL-KIT-SYNC-AUDIT — cross-kit consistency audit tool (four-file set). 3 CRITICAL checks (manifest version pinning, synchronized file identity, kit registry consistency), 5 HIGH checks (boundary contracts, artifact flow, cross-cutting triggers, dependency edges), 3 MEDIUM checks (artifact inventory, layer descriptions, navigation map). Claude Code binding.
- [x] **FW-067** TOOL-KIT-SELF-CHECK — per-kit domain expert tool (four-file set). 6 internal consistency checks, 3 pipeline boundary checks, 4 cross-cutting boundary checks. Claude Code binding.
- [x] **FW-068** Healthcheck A4 — cross-kit sync audit added as Tier 2 check in healthcheck-playbook.md
- [x] **FW-069** Drift fixes — layer-model.md SDK artifact list corrected (was SBR/PPR only, now includes CLA/PCR/TIR), SDK status text updated, README.md updated to reflect all 16 built kits

### 2026-04: spec-driven CI/CD and the adapter ecosystem

- [x] **CI-001** Spec-driven CI/CD shipped v1.0 through v1.1.1 — declarative conformance suites, a shared conformance harness, and self-governing CI live on `aieos-artifact-store`
- [x] **CI-002** 13 pipeline adapters implemented across build, test, scan, sign, and deploy (buildah, pytest-unit, pytest-integration, semgrep, osv, syft, trivy, cosign, http-health, http-smoke, prom-slo, kustomize, flux)

### 2026-05-17: M0 signing identity

- [x] **M0** Signing identity chosen and verified — Sigstore keyless (Fulcio + Rekor). Run #1 of `m0-signing-test.yml` concluded success across all 19 steps: PASS attestation, keyless verify against the Fulcio identity, Rekor transparency-log verify, and negative-payload rejections. The end-to-end build-attest-verify loop is confirmed.

### 2026-07-05: v1.2 Framework Quality Pass — complete

Priority sequence M0 → B1 → A1 → B2 → B3 → C1 → E → A2 → D2 → D. All ten items landed; every repo in the framework is now under CI.

- [x] **B1** CI on `aieos-governance-foundation` (validate + test jobs), green on `main`
- [x] **A1** `adapter-pytest-integration` implemented; conformance green and signed
- [x] **B2** CI on `aieos-agent-harness` (313 tests), green on `main`
- [x] **B3** Reusable kit CI workflow plus an 8-line caller in each of the 15 kit repos; structure, four-file, naming, validator-JSON, governance-model byte-identity, markdownlint, and internal-link checks all green on `main`
- [x] **A2** `adapter-flux-handoff` implemented (v1 scope: git handoff + default reconciler check); conformance green and signed. Live Flux reconcile-verification is a documented adapter TODO.
- [x] **CONF** All 13 adapters brought to real signed conformance loops via harness v1.1 input mapping (env/value/fixture resolvers), with `continue-on-error` removed. Bugs the unmask surfaced and fixed: syft (metadata.component version, specVersion, tools object-form), cosign (bundle format), pytest deps.
- [x] **C1** `qaer-prompt.md` added to the Quality Assurance Kit, framed for QAER's human-authored entry-gate nature
- [x] **E** `aieos-manifests` populated — each `envs/<env>/` carries a `kustomization.yaml` plus the reference consumer's rendered overlay; `kustomize build` verified for all three envs
- [x] **D2** ADR-0001 documenting the `src/cicd/` split in `aieos-agent-harness` (already code-decoupled: a documentation gap, not an architecture problem)
- [x] **D** Agent-harness orchestration core (routing, state, lifecycle, convergence) filled to 100% line coverage; full suite 334 passing, running under the B2 job

### 2026-07-13: v1.3 "Three Drivers" internal release

Reframes sherpa, the console, and the new dark factory as three drivers over one governance engine. Three ADRs accepted (dark factory conductor and harness facade; console-to-harness freeze boundary; andon-cord intervention model). Tags pushed: `aieos-sherpa` v1.1.0, `aieos-agent-harness` v1.3.0, `aieos-console` v0.1.0, `aieos-dark-factory` v0.1.0, `aieos-schema` v1.3.0.

- [x] **FR-018** Canonical freeze representation. `aieos-schema/schema/document-control.yaml` defines one Document Control block, read and written by all drivers; the harness gained the `write_artifact_status` writer it lacked; status vocabulary split into freeze status (`DRAFT`/`VALIDATED`/`FREEZE_PENDING`/`FROZEN` plus `HALTED`/`FAULTED`) and a separate last-validation outcome. Instance validator with 14 tests.
- [x] **FR-020** Single freeze authority. New harness `apply_freeze_decision` is the only writer of `FROZEN`: it checks the human authorization invariant, the approving outcome, and the content hash against disk before writing, and writes nothing on any refusal. A `HarnessDriver` facade exposes the three operations the dark factory needs. The console freezes by calling the harness CLI (argument array, no shell), not by writing status itself.
- [x] **FR-019** Cross-driver ownership lock. Canonical `aieos-schema/schema/lock.yaml` (session-id ownership token, 60-second heartbeat, 5-minute lease); a hostname-aware Python implementation in the harness and a matching TypeScript rewrite in the console read the same wire format. A stale takeover writes an andon sentinel. Handoffs are guaranteed clean only at frozen-artifact boundaries.
- [x] **FR-007** Append-only Decision Register. Hash-chained JSONL in `aieos-dark-factory` records freeze requests, escalations, resumes, fault clears, and halts.
- [x] **FR-008** Machine-readable initiative state. Met by the canonical Document Control blocks plus the ER state block; no separate cache needed.
- [x] **Dark factory** New `aieos-dark-factory` control plane: freeze-DAG walk order from the kit manifest, a conductor that parks at freeze gates and escalates and halts and resumes, the Decision Register, and an andon-cord model (`HALTED`/`FAULTED`, resume and clear-fault routed through the Decision Register, never through freeze). It imports only the harness facade and never writes `FROZEN`.
- [x] **Three-way switch proof** A live end-to-end run: dark factory to the real harness with an offline converging provider, a converged artifact persisted at `FREEZE_PENDING`, a human freeze through the harness authority, then a resumed walk to completion. The escalation path is proven separately (convergence driven to exhaustion surfaces an escalation entry in the Decision Register).
- [x] **CI everywhere** `aieos-sherpa`, `aieos-console`, and `aieos-dark-factory` are now under CI, so the "every repo under CI" claim holds across sherpa and the console too.

---

## Planned — framework refinement

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **FR-001** | Run sherpa manual rubric tests for P1/Skeptic and P3/PM personas | High | — | Two untested persona/preset combinations from the rubric test matrix |
| **FR-002** | Run sherpa manual rubric test for P4/PM (ODK flow) | Medium | — | Tests incident-triggered flow with non-technical persona |
| **FR-003** | Promote soft behavioral checks to hard checks as compliance rates stabilize | Medium | FR-001, FR-002 | Track per-check pass rates; promote at >80% across 3+ runs |
| **FR-004** | Integration test for cross-initiative awareness | Medium | — | Needs fixture with pre-existing sibling initiative ER |
| **FR-005** | Integration test for parallel artifact orchestration | Low | — | Verify ACF+SAD parallel generation in P1/P2 driver |
| **FR-006** | Validate IEK entry-from alignment with retrospective format | Low | INIT-C-007 | Confirm retrospective → ES mapping works end-to-end |
| **FR-007** ✅ | Append-only Decision Register — cross-layer decision log alongside ER | High | — | **Shipped in v1.3 (2026-07-13)** — hash-chained JSONL Decision Register in `aieos-dark-factory`. See the 2026-07-13 entry. |
| **FR-008** ✅ | Machine-readable initiative state — structured block in ER | Medium | — | **Shipped in v1.3 (2026-07-13)** — met by the canonical Document Control blocks plus the ER state block. See the 2026-07-13 entry. |
| **FR-009** | Reassessment gates at layer transitions — check upstream assumptions still valid | Medium | FR-007 | Inspired by GSD. At each kit transition, compare current state against DPRD/PRD assumptions. If material divergence detected, trigger lightweight re-validation. New gate type in flow-reference.md. |
| **FR-010** | Auto-repair healthchecks — `check-structure.sh --repair` flag | Medium | — | Inspired by GSD. Auto-fix: governance model sync, missing spec versions, broken file refs. Healthcheck playbook gains "Remediation" column (auto-remediable vs. manual). |
| **FR-011** | Effort ceiling governance — initiative-level thresholds with graduated enforcement | Low | — | Inspired by GSD. Max convergence iterations, max PRK cycles. At 50%: flag. At 75%: sponsor re-auth. At 90%: escalate to SDK for kill/pivot. |
| **FR-012** | Verification tier classification — classify validator gates as Structural/Referential/Semantic/Human | Low | — | Inspired by GSD. Tells you which tier caught an issue. Run cheap tiers frequently, reserve expensive tiers for milestones. |
| **FR-013** | Process forensics template — lightweight root cause analysis when the governance pipeline stalls | Low | — | Inspired by GSD. Distinct from ODK (production incidents). Covers: scope creep, ambiguous spec, wrong preset, missing context. Referenced from healthcheck-playbook.md. |

### AI-Native SDLC alignment — gap closure (2026-03-25)

Items proposed by the AI-Native SDLC v3.1 alignment assessment (`docs/ai-native-sdlc-alignment.md`). AG items close outright gaps; AL items thicken partial alignment.

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **FR-014** | Prompt/model regression testing — add as Tier 3 test category and model-update trigger in healthcheck | High | — | Source: AG-002 (P116, PR63, PR68). No governance of prompt regression after model updates. Add prompt regression suite as Tier 3 category. Add model-update review trigger to healthcheck-playbook.md. |
| **FR-015** | AI adoption maturity model — 4 levels tied to AIEOS adoption depth | Medium | — | Source: AG-003, AG-007 (P120, PR6a, PR6c, PR65, P131). Define maturity levels: L1 preset use → L2 spec customization → L3 finding contribution → L4 kit extension. |
| **FR-016** | Constraint library tool spec — queryable rejection patterns accessible via MCP | Medium | — | Source: AG-004 (PR32, PR34). Specs serve as distributed constraints but no queryable library. Design for MCP server exposure. Feed from validator FAIL patterns and PRK findings. |
| **FR-017** | AI pipeline observability guidance — LLM call tracing standards | Medium | — | Source: AG-010 (PR61, P114, P115). No governance of LLM call tracing, prompt drift, or AI-specific observability. Extend RRK or create guidance doc. |
| **FR-021** | Review capacity estimation in WDD/PRK | Low | — | Source: AG-008 (P156, PR85, PR86). Add review capacity as optional WDD consideration. Document review rotation guidance in PRK playbook. (Renumbered from FR-018 on 2026-07-13; FR-018/019/020 are the shipped three-drivers items — see the 2026-07-13 entry.) |
| **FR-022** | Bootstrap file token budget recommendation | Low | — | Source: AG-009 (PR35). Add token budget recommendation to kit-structure-standard.md (advisory, not hard gate). (Renumbered from FR-019 on 2026-07-13.) |

### AI-Native SDLC alignment — PA thickening (2026-03-25)

Thickening work packages that strengthen existing partial alignment. Each bundles multiple PA items into a coherent deliverable. Full analysis in `docs/ai-native-sdlc-alignment.md` §PA Thickening Analysis.

| ID | Item | Priority | Effort | PA Items | Notes |
|----|------|----------|--------|----------|-------|
| **AL-001** | Agent Security Hardening — prompt injection, supply chain, shadow agents, OWASP agentic AI, task-scoped permissions | High | Medium | P49, P50, P51, P55, P87, PA16, PA18, PR20, PR21, PR22 | Update SCK TM spec + DAR spec + adapter-conformance-spec + tool-governance-spec. Add named threat categories, MCP verification, permission model. |
| **AL-002** | AI-Generated Code Testing Standards — behavioral verification, test skepticism gate, SAST/DAST, anti-mocking | High | Medium | P111, P112, PA9, PR7, PR8, PR9, PR9a, PR9c, PR40 | Update TDD spec + execution-spec + code-craftsmanship.md + QAK VP spec. Add AI-specific testing dimensions and review gates. |
| **AL-003** | Agent Readiness & Delegation Framework — capability map, readiness checklist, frontier mapping, confidence gating | Medium | Medium | PA3c, PA3d, PA10, PA15b, PA15d, PA19b, PR3, P148, P149, P150 | Update tool-governance-spec + getting-started.md + WDD annotations + QAK playbook. |
| **AL-004** | Knowledge Currency & Documentation Lifecycle — freshness metadata, AI doc audits, brownfield excavation | Medium | Low | P151, P153, PA41, PR66, PR81, PR82 | Update DKK templates + getting-started.md. Add AI-assisted audit mode to DHR. |
| **AL-005** | Process & Workflow Hardening — prompt deprecation, staged adoption, IaC gates, canary deploy, cognitive recovery | Medium | Medium | P124, P129, P133, PA12, PA35, PR10, PR13a, PR53, PR60, PR80, PR87, P43 | Update spec-file-standard + getting-started + PINFK ISPEC + REK RP + EEK playbook. |
| **AL-006** | Enterprise Integration Readiness — NIST AI RMF mapping, A2A/MCP guidance, W3C PROV, tool catalog | Medium | Low | P108, P109, P110, P139, P146, PA6a, PA6b, PA6d, PR64 | Update adapter-conformance-spec + governance-model + ER spec + tool-governance-spec. |
| **AL-007** | Memory Architecture Formalization — five-layer memory model, canonical facts, context compression protocol | Low | Medium | P8, P57, P60, P62, P64, PA4, PA24, PA25, PA27 | New guidance doc (memory-architecture.md) + philosophy.md + code-craftsmanship.md updates. |
| **AL-008** | Organizational AI Alignment — senior role redefinition, cognitive load, working modes, adoption guidance | Low | Low | 27 PA items (see alignment doc) | Update philosophy.md + getting-started.md. Single guidance section, not spec changes. Mostly advisory. |

**Cross-references to existing roadmap items validated by alignment assessment:**

| Existing ID | Validated By | Notes |
|-------------|-------------|-------|
| GAP-002 | AG-001 (P106, PR78) | Data privacy governance confirmed high priority |
| GAP-005 | AG-005 (P102, P117) | Extend scope to AI tooling costs |
| ECO-006 | AG-003 (P120, PR6c) | Governance Analytics addresses adoption quality |
| ECO-001 | AG-011 (P145) | Schema enables richer provenance (model version, context hash) |
| INT-002 | AL-006 | First executable adapter proves integration architecture |
| UX-001 | AL-005 (P129) | Onboarding guide supports staged adoption |

### User experience improvements (2026-03-21)

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **UX-001** | Onboarding guide — "Your first initiative in 15 minutes" | High | — | Guided walkthrough with a concrete P2 Enhancement example. Progressive disclosure: show only artifacts relevant to the user's preset instead of all 50+ types. Supplement getting-started.md (reference-oriented) with a narrative tutorial. Target: a new user can complete routing + first 2 artifacts without reading any spec files. |
| **UX-002** | Sherpa standalone hardening — versioning, packaging, test harness | High | SH-025 | SH-025 extracted aieos-sherpa with canonical prompt + adapters. Remaining: version the prompt (semver), add a changelog, build a regression test harness that runs rubric tests automatically (headless driver + scoring), document adapter authoring guide for non-Claude platforms. |
| **UX-003** | Expanded rubric test coverage — P1/Skeptic, P3/PM, P4/PM | High | FR-001, FR-002 | FR-001 and FR-002 cover P1/Skeptic and P4/PM. Add P3/PM (compliance flow with non-technical persona). Each new persona/preset combination may surface new behavioral issues. Target: 5 of 15 rubric matrix cells tested (currently 3: P5/PM x2, P2/TechLead). |
| **UX-004** | Convergence loop refinement — targeted correction instead of full re-generation | Medium | — | Current behavior: validation FAIL triggers full artifact re-generation. Improvement: identify the specific failing gate(s), generate a targeted patch addressing only those gates, re-validate. Reduces token cost and preserves content that already passes. Also: graduate the 3-attempt hard limit to a configurable ceiling with sponsor re-auth at threshold (relates to FR-011 effort ceiling governance). |
| **UX-005** | Progressive disclosure in sherpa — adapt detail level to user expertise | Low | UX-003 | P2/TechLead rubric test showed slight over-probing for expert users. Sherpa could detect expertise signals (technical vocabulary, direct answers, "skip the explanation" cues) and adjust: fewer analogies, terser explanations, faster artifact transitions. Risk: over-engineering. Only pursue if rubric tests consistently show calibration as a gap across multiple expert-persona sessions. |

### External tool integration (2026-03-21)

The 13 pipeline adapters (build, test, scan, sign, deploy) are built and produce signed conformance loops in CI — see the 2026-04 and 2026-07-05 Completed entries. The items below cover a different class: platform-integration adapters that sync governance artifacts to external work-tracking tools (GitHub Issues, Releases, and so on). None of those exist yet. This section tracks the path from static binding documentation to working platform integrations.

**Existing foundation:**
- 4 tool specs with external platform bindings: work-item-sync (GitHub Issues), release-tag (GitHub Releases), validation-status (GitHub Issues), artifact-publish (Confluence)
- Adapter conformance spec with 7 hard gates, three-layer model (spec → binding → adapter), and `push()`/`verify()`/`health()` operations, proven end-to-end by the 13 pipeline adapters
- 13 PRK review lenses (governed four-file tools, no external integration needed)

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **INT-001** | Expand platform bindings — Linear, Jira, Slack, GitLab | Medium | — | Static field-mapping documents (no code). Add bindings for: **Linear** (work-item-sync, validation-status), **Jira** (work-item-sync, validation-status), **Slack** (validation-status as channel notifications, health-check summaries), **GitLab** (work-item-sync to GitLab Issues, release-tag to GitLab Releases). Each binding follows the existing pattern in `docs/bindings/`. Low effort per binding (~1 hour each). Extends coverage without requiring executable code. |
| **INT-002** | First executable adapter — GitHub Issues (work-item-sync) | High | — | Prove the adapter architecture works end-to-end. Build `aieos-adapter-github` implementing `push()`, `verify()`, `health()` per adapter-conformance-spec. Scope: sync WDD work items to GitHub Issues using the existing `work-item-sync-github-issues.md` binding. Idempotent (search-then-upsert), structured audit logging, circuit breaker on API failures. Test with aieos-search WDD items. Success: sherpa can say "I've synced 8 work items to GitHub Issues" after WDD freeze. |
| **INT-003** | Second executable adapter — GitHub Releases (release-tag) | Medium | INT-002 | Reuses the `aieos-adapter-github` package. Creates a GitHub Release from a frozen RR artifact using the `release-tag-github.md` binding. Validates that the adapter pattern generalizes beyond a single tool spec. Test with aieos-console RR-CONSOLE-001. |
| **INT-004** | Sherpa adapter integration — offer sync at freeze points | Medium | INT-002 | After WDD freeze, sherpa checks for configured adapters and offers: "I can sync these work items to GitHub Issues now. Want me to?" After RR freeze: "I can create a GitHub Release for this." Adds adapter awareness to sherpa-skill.md Phase 3 post-freeze sequence (new Step F after Step E). Respects the existing "never ask permission between sequential artifacts" rule — sync is offered as a utility, not a gate. |
| **INT-005** | Adapter test harness and CI | Low | INT-002 | Automated tests for adapter conformance: mock external APIs, verify idempotency, test circuit breaker, validate audit log format. Reusable across all future adapters. |

### Organizational readiness gaps

| ID | Item | Priority | Kit | Dependencies | Notes |
|----|------|----------|-----|-------------|-------|
| **ORG-001** | Skills Gap Assessment — pre-execution check in EEK | High | EEK | — | Before WDD, assess team capabilities vs. required skills (languages, frameworks, domain expertise, ops skills). Identifies training needs or hiring/contracting dependencies. Blocks execution planning if critical gaps unresolved. |
| **ORG-002** | Service Ownership Record — complete ownership matrix | High | REK or RRK | — | Who owns: code, on-call, L1/L2/L3 support, product decisions, documentation, dependency updates. Frozen before Layer 6 entry. Extends beyond SRER's reliability-only ownership. |
| **ORG-003** | Extend RRK SRP with support tier definitions | Medium | RRK | ORG-002 | Add L1/L2/L3 support routing, escalation paths, support hours, handoff triggers to SRP spec. Currently SRP covers SLOs but not the human support model. |
| **ORG-004** | Launch Communications Plan — internal + external messaging | Medium | REK | — | New artifact in REK between RP and RR. Internal: org announcement, stakeholder briefing, support team enablement. External: customer comms, changelog, migration guide (if applicable). |
| **ORG-005** | Adoption Plan — strategy, metrics, feedback loops | Medium | REK | ORG-004 | Extend RP or add new artifact. Covers: rollout strategy (big bang vs. phased), adoption success metrics, feedback channels, time-to-value targets, what "adopted" means. Goes beyond BPK's process training. |
| **ORG-006** | Update initiative presets with new artifacts | Low | Governance Foundation | ORG-001 through ORG-005 | Add skills assessment, ownership record, launch comms, adoption plan to P1/P2/P3 preset artifact sequences. Update ER spec with new layer sections. |

### Cross-AI compatibility (2026-03-19) — complete

- [x] **FR-008** Machine-readable State Block (§1b) in ER spec — 7-field structured position snapshot
- [x] **XAI-001** Copilot CLI adapter — loading guide, limitations, workarounds
- [x] **XAI-002** AI capability matrix — 9 capabilities × 5 platforms with fallbacks
- [x] **XAI-003** Cross-AI session handoff protocol — checklist, resumption command, troubleshooting
- [x] **XAI-004** Compressed prompt (267 lines, 57% reduction, all sections preserved)
- [x] **XAI-005** Validator consistency testing methodology
- [x] **XAI-006** Smoke test extended to 49 checks (adapter dirs, compact parity, state block)

### Agent harness integrations (2026-03-27)

High-value integrations that mix deterministic tool checks with AI reasoning via the harness pipeline routing strategy.

**Completed:**

- [x] **HI-001** ORD verification pipeline — Tool adapters (test suite, build, lint) → AI assessment of operational readiness
- [x] **HI-002** Codebase analysis pipeline — SAST/linter/dependency tools → AI interpretation for ACF/DCF/SAD intake (brownfield)
- [x] **HI-003** RHR health review pipeline — Metrics collection (JSONL, health checks) → AI trend analysis against SLO baselines

**Planned (incremental value):**

| ID | Item | Priority | Dependencies | Notes |
|----|------|----------|-------------|-------|
| **HI-004** | Briefing distillation cost-aware routing — route to cheapest model for low-risk compression | Low | ECO-009 | Distillation doesn't need premium models. Use cost_aware routing strategy. |
| **HI-005** | Cross-artifact consistency as independent validator — separate adapter validates PRD→SAD and SAD→TDD alignment | Medium | ECO-009 | Current: same session checks. With harness: independent context, catches drift that self-review misses. |
| **HI-006** | Assumption stress testing via different provider — route adversarial review to different AI provider | Medium | ECO-009 | Same AI that generated assumptions shouldn't stress-test them. Use fallback to different provider. |
| **HI-007** | Cross-initiative awareness via artifact store tool adapter — structured retrieval feeds AI context | Low | ECO-003, ECO-009 | Currently: sherpa queries store ad-hoc. With harness: Tool adapter queries store, AI interprets. Pipeline strategy. |

---

## Planned — system projects

Documented in detail at `docs/ecosystem-roadmap.md`. These are real software projects that operationalize the governance framework.

### Phase 1: critical path

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-001** | AIEOS Schema | `aieos-schema` | Machine-readable spec contracts (YAML/JSON). Strengthens framework Tier 2 tests (spec-template drift, gate enumeration, prompt checklist alignment) AND unlocks all downstream system projects. | Substantially built (69 per-artifact schemas across all 15 kits, meta-schema, tests); currency/freeze audit pending | None — this is the keystone |
| **ECO-002** | Evaluation Engine | `aieos-evaluation-engine` | Runtime governance enforcement. Consumes schema to validate artifacts programmatically instead of relying solely on AI judgment. | Not started | ECO-001 |
| **ECO-003** | Artifact Store | `aieos-artifact-store` | Cross-initiative artifact indexing. Query "show me all frozen SADs across all initiatives" or "which initiatives touched the auth module." | **Complete** (v1.0.0) | — (built without Schema dependency) |

### Phase 2: observe & integrate

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-004** | System Twin | `aieos-system-twin` | Live system topology graph. Maps what's running in production to what's governed in AIEOS. | Not started | ECO-001, ECO-003 |
| **ECO-005** | Playground | `aieos-playground` | Interactive learning environment. Guided walkthrough of AIEOS with sandbox initiatives. | Not started | ECO-001 |

### Phase 3: measure & report

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-006** | Governance Analytics | `aieos-governance-analytics` | Cross-initiative intelligence. Quality trends, cycle time, finding patterns, adoption rates. | Not started | ECO-001, ECO-003 |
| **ECO-007** | Compliance Reporter | `aieos-compliance-reporter` | Automated audit packages. Generate compliance evidence from frozen artifacts + ER history. | Not started | ECO-001, ECO-003 |

### Phase 4: people & impact

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-008** | Engineer Impact Framework | `aieos-engineer-impact` | Quarterly engineer impact assessment. Two tiers (Starter ~2hrs, Advanced ~8hrs), four dimensions, calibration process, gaming detection. Optional ER §16 integration and IEK consumption. | Complete | None |

### Phase 5: orchestrate & execute

| ID | Project | Repository | Purpose | Status | Dependencies |
|----|---------|-----------|---------|--------|-------------|
| **ECO-009** | Agent Harness | `aieos-agent-harness` | Pluggable multi-agent orchestration engine for AIEOS. Binds different AI providers (and non-AI tools) to artifact lifecycle events. Provides fallback routing, cost-aware routing, multi-provider consensus, and per-invocation observability. Enforces AIEOS invariants (generation/validation separation, human freeze, disk-based state). | Not started | ECO-001 (schema for artifact event contracts), INT-002 (adapter pattern proven) |

---

## Planned — gap closure (from 2026-03-21 gap analysis)

### Tier 1: will come up in first real initiative at work

Build these when you hit them during a real initiative — don't build speculatively.

| ID | Gap | Approach | Priority | Notes |
|----|-----|----------|----------|-------|
| **GAP-001** | Technical debt governance | Extend EEK or create cross-cutting artifact. New artifact: **Technical Debt Register (TDR)** — append-only log of debt accrued during execution (what, why, interest cost, paydown plan). Updated during EEK code execution and at each RHR. | High | Don't create a new kit. Add TDR as a cross-cutting artifact in EEK with RRK maintenance. Tracked alongside ER. |
| **GAP-002** | Data privacy / classification | Extend SCK. Add **Data Classification Record (DCL)** as a new SCK artifact — maps all data handled by the initiative to classification levels (PII, PHI, confidential, internal, public). Add hard gate to SAD spec requiring data classification reference. GDPR impact assessment folds into CER. | High | SCK already governs security; privacy is the missing half. DCL triggers after PFD (when data scope is known) and feeds TM + SAR. |
| **GAP-003** | Accessibility compliance | Don't create a new kit. Add accessibility as hard gates to existing specs: PRD spec gains `accessibility_requirements` gate (WCAG level stated); TDD spec gains `accessibility_test_coverage` gate; QAK VP gains accessibility as a test dimension. | High | Lightest possible touch — 3 spec edits, no new kit. Add when the first initiative has user-facing output. |
| **GAP-004** | Operational maintenance governance | Extend RRK (Layer 6), not a new kit. Add **Operational Maintenance Plan (OMP)** artifact to RRK — covers: dependency update cadence, patch policy, secret rotation schedule, backup/DR drill schedule, data retention enforcement. Frozen after first SRP, revised at each RHR. | High | RRK already owns production. OMP is the "steady-state care plan" that SRP doesn't cover. |
| **GAP-005** | Cost governance | Extend SDK. Add cost fields to PCR (budget per capability) and SBR (investment envelope already exists but no tracking). Add **Cost Tracking Record (CTR)** as an optional cross-cutting artifact — actual spend vs. budget at each layer transition. | Medium | Start light: add fields to existing artifacts first. CTR as a full artifact only if cost tracking proves essential. |

### Tier 2: causes friction at scale

Address when scaling beyond solo/small team use.

| ID | Gap | Approach | Priority | Notes |
|----|-----|----------|----------|-------|
| **GAP-006** | Deprecation/sunset lifecycle | Extend REK (Layer 5). CLA already marks capabilities for sunset. Add **Deprecation Execution Plan (DEP)** to REK — covers: migration path execution, communication timeline, dependency notification, data archival, monitoring teardown. Uses RP/RR patterns but for removal instead of deployment. | Medium | Don't create a new kit. REK already handles release mechanics; deprecation is "release in reverse." |
| **GAP-007** | Customer/support feedback loop | Extend IEK (Layer 7). Add **Feedback Synthesis Record (FSR)** — aggregates support ticket themes, customer feedback, NPS signals into structured input for next ES. Triggered periodically (quarterly) or when support volume spikes. | Medium | IEK's ES is too high-level for granular feedback. FSR is the mid-layer synthesis that's missing. DKK SKA captures individual articles; FSR captures patterns. |
| **GAP-008** | Cross-team coordination | Extend ER spec with a **Cross-Initiative Dependency Map** section. When multiple initiatives share systems/teams, each ER §Dependencies lists the other ERs it depends on or conflicts with. Sherpa cross-initiative scan (already built) detects these; this formalizes the tracking. | Medium | Don't create a new kit. Extend ER + use existing cross-initiative awareness in the sherpa. Only matters at 3+ concurrent initiatives. |
| **GAP-009** | Decision authority (RACI) | Add to ER §1 Document Control: a **Decision Authority Table** — lists who can approve freeze at each layer (by role, not by name). Replaces ad-hoc "who approves this?" with explicit authority. | Medium | Lightest possible touch: one new section in an existing artifact. No new kit, no new spec. Fill in at initiative start, reference at each freeze. |

### Guidance: what NOT to build yet

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
| **BL-004** | Artifact diff visualization — show what changed between artifact versions | system | Useful for re-entry/amendment flows |
| **BL-005** | Initiative portfolio dashboard — active/complete/abandoned across all ERs | system | Lightweight version of ECO-006 |
| **BL-006** | Spec authoring assistant — guided creation of new artifact types with four-file scaffold | Framework | Would help external contributors extend AIEOS |
| **BL-007** | Adapter library — pre-built adapters for GitHub Issues, Linear, Jira for tool bindings | system | Per adapter-conformance-spec.md |
| **BL-008** | Ideation & Opportunity Kit (IOK) — pre-Layer-1 kit governing structured ideation with OLR, ISR, OB artifacts | Framework | Full four-file system for ideation. Graduate from sherpa ideation mode (SH-026/FW-053) if ideation proves valuable enough to warrant its own governance layer. Flow: Signals → OLR → ISR(s) → OB(s) → SDK or PIK |

---

## How to use this roadmap

**Adding items:** Append to the appropriate section with the next available ID in that category (FW-NNN for framework, SH-NNN for sherpa, INIT-X-NNN for initiatives, ECO-NNN for system, FR-NNN for refinement, BL-NNN for backlog).

**Completing items:** Move from Planned/In Progress to Completed with a date. Change `[ ]` to `[x]`.

**Prioritizing backlog:** Move items from Backlog to Planned when scope and dependencies are clear.

**ID prefixes:**
- `FW` — Framework core (kits, governance, testing)
- `SH` — Sherpa capabilities
- `INIT-C` — aieos-console initiative
- `INIT-S` — aieos-search initiative
- `FR` — Framework refinement (testing, hardening)
- `ECO` — system software projects
- `BL` — Backlog (unprioritized ideas)
