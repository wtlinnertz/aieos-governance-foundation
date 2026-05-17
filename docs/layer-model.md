# AIEOS Layer Model

AIEOS organizes an organization's operating system into layers. Each layer governs a distinct phase of the value-delivery lifecycle. A kit governs each layer.

---

## Getting started

If you are new to AIEOS or starting a new initiative:

- [`getting-started.md`](getting-started.md) — Task-oriented guide: find your scenario and follow the path
- [`initiative-presets.md`](initiative-presets.md) — Five golden paths for common initiative types (New Feature, Enhancement, Compliance, Performance Fix, Exploratory Research)
- [`initiative-state-view.md`](initiative-state-view.md) — Template for tracking initiative state across all kit layers, with a TaskFlow worked example
- [`flow-reference.md`](flow-reference.md) — All valid entry points, exit conditions, parallelism rules, escalation paths, and flow permutations

---

## Layer architecture

AIEOS layers are organized into three categories:

### Pipeline layers (1–7)

Sequential value delivery from strategy to production learning. The flow is top-down for delivery and bottom-up for learning. Layer 7 feeds insight back to Layer 1. The system is a loop, not a pipeline.

```
┌─────────────────────────────────────────┐
│  1. Strategic Direction                 │  What are we trying to achieve?
├─────────────────────────────────────────┤
│  2. Product Intelligence                │  What should we build and why?
├─────────────────────────────────────────┤
│  3. Flow Control                        │  What do we work on next and when?
├─────────────────────────────────────────┤
│  4. Engineering Execution               │  How do we build it correctly?
├─────────────────────────────────────────┤
│  5. Release & Exposure                  │  How do we ship it safely?
├─────────────────────────────────────────┤
│  6. Reliability & Resilience            │  How do we keep it running?
├─────────────────────────────────────────┤
│  7. Insight & Evolution                 │  What did we learn and what changes?
└─────────────────────────────────────────┘
```

### Operational tracks (8)

Reactive tracks triggered by production events, not SDLC progression.

```
┌─────────────────────────────────────────┐
│  8. Operational Diagnostics             │  How do we diagnose and resolve failures?
└─────────────────────────────────────────┘
```

### Cross-Cutting governance (9–15)

Kits that interact with multiple pipeline layers. Each has defined trigger points rather than a fixed position in the sequence. They can be adopted independently.

```
┌─────────────────────────────────────────┐
│  9. Quality Assurance                   │  Is it verified beyond unit scope?
├─────────────────────────────────────────┤   (gate between 4 → 5)
│  10. Security & Compliance              │  Is it secure and compliant?
├─────────────────────────────────────────┤   (touches 2, 4, 5, 6, 8)
│  11. Data & Configuration               │  Is config governed and flags managed?
├─────────────────────────────────────────┤   (touches 4, 5, 6)
│  12. Platform & Infrastructure          │  What infrastructure supports it?
├─────────────────────────────────────────┤   (foundational input to 4, 5, 6)
│  13. Documentation & Knowledge          │  Is user-facing documentation governed?
├─────────────────────────────────────────┤   (touches 4, 5, 6, 8)
│  14. Peer Review                        │  Has it been reviewed from multiple perspectives?
├─────────────────────────────────────────┤   (touches 2, 4, 5, 6, 8, 9)
│  15. Business Process                   │  Are affected business processes governed?
└─────────────────────────────────────────┘   (touches 4, 5)
```

Layer 8 is a reactive operational track — triggered by production events, not SDLC progression — that feeds findings back into Layers 6, 7, and optionally Layers 2 and 4. Layers 9–15 are cross-cutting governance kits — each operates at defined trigger points across the pipeline rather than occupying a single sequential position.

---

## Layer descriptions

### Layer 1: strategic direction

**Question**: What are we trying to achieve?

This layer governs how an organization captures, validates, and prioritizes strategic bets. It produces falsifiable bets with measurable signals and a strict-rank-ordered portfolio with explicit capacity constraints. The emphasis is on decision quality — falsifiability, measurability, and prioritization honesty — not complete strategy documentation.

**Kit**: `aieos-strategic-direction-kit` *(built — optional upstream entry point)*

**Artifacts**: Capability Lifecycle Assessment (CLA, 6 hard gates, optional), Product Capability Roadmap (PCR, 6 hard gates, optional), Technology Investment Roadmap (TIR, 5 hard gates, optional), Strategic Bet Record (SBR, 6 hard gates), Portfolio Prioritization Record (PPR, 5 hard gates)

**Outputs**: Frozen PPR with above-the-line SBRs routed to Product Intelligence

**Downstream consumer**: Product Intelligence (Layer 2) — frozen SBR provides strategic context for discovery

**Feedback loop**: IEK (Layer 7) `re-discover` signals may trigger new SBRs

---

### Layer 2: product intelligence

**Question**: What should we build and why?

This layer governs the transformation of strategic intent into engineering-ready product requirements. It runs discovery — problem framing, value hypothesis testing, assumption validation — and produces a frozen Discovery PRD.

**Kit**: `aieos-product-intelligence-kit` *(built)*

**Inputs**: Strategic direction, market signals, user research, stakeholder input

**Outputs**: Frozen Discovery PRD (engineering handoff artifact)

**Downstream consumer**: Solution Sourcing (Layer 3) when sourcing evaluation is needed, or Engineering Execution (Layer 4) via Kit Entry Gate when Build is obvious

---

### Layer 3: solution sourcing

**Question**: What do we work on next and when?

This layer governs work intake, prioritization, sequencing, and capacity management across the engineering pipeline. It determines which engineering engagements start when, and ensures work arrives at Layer 4 properly classified and prioritized. The full scope includes prioritization and sequencing (future capability). The first kit built for this layer focuses on solution sourcing — the Build/Buy/Adopt decision that determines how an initiative is fulfilled before engineering execution begins.

**Kit**: `aieos-solution-sourcing-kit` *(built)*

**Inputs**: Frozen Discovery PRD (DPRD) from Product Intelligence (Layer 2)

**Outputs**: Frozen Sourcing Decision Record (SDR) — documents Build/Buy/Adopt decision with rationale and downstream routing

**Downstream consumer**: Engineering Execution (Layer 4) — SDR provides sourcing context alongside DPRD

**Note**: SSK is optional. When Build is the obvious choice, initiatives skip Layer 3 and flow directly from PIK to EEK. When engaged, the internal artifact flow is: SOER → VER → SDR.

---

### Layer 4: engineering execution

**Question**: How do we build it correctly?

This layer governs the full execution lifecycle from PRD through production-ready code. It produces architecture, design, work decomposition, and test-first implementation artifacts. It has two entry paths: discovery output from Layer 2 (Path A) or direct human input for well-understood work (Path B).

**Kit**: `aieos-engineering-execution` *(built)*

**Inputs**: Frozen PRD (from PIK via Path A, or Product Brief via Path B), Kit Entry Record (gate). When arriving from SSK: frozen DPRD + frozen SDR.

**Outputs**: Frozen ORD (operational readiness decision), validated implementation artifacts

**Downstream consumer**: Release & Exposure (Layer 5)

---

### Layer 5: release & exposure

**Question**: How do we ship it safely?

This layer governs deployment policy, progressive delivery, feature exposure management, and release decisions. It translates production-ready artifacts into controlled, observable releases.

**Kit**: `aieos-release-exposure-kit` *(built)*

**Inputs**: Frozen ORD from Engineering Execution (Layer 4), organizational release policy (Release Context File)

**Outputs**: Frozen Release Record (RR) — release evidence, disposition declaration, Layer 6 handoff package

**Downstream consumer**: Reliability & Resilience (Layer 6)

---

### Layer 6: reliability & resilience

**Question**: How do we keep it running?

This layer governs SLOs, incident management, error budgets, and the operational health of systems in production. It defines what "working correctly" means and what to do when it isn't.

**Kit**: `aieos-reliability-resilience-kit` *(built)*

**Inputs**: Frozen Release Record (RR §7 Handoff to Layer 6) from Release & Exposure Kit (Layer 5), completed service reliability intake, incident evidence

**Outputs**: Frozen Reliability Health Report (RHR) — SLO compliance record, error budget state, incident summary, Layer 7 feed

**Downstream consumer**: Insight & Evolution (Layer 7)

---

### Layer 7: insight & evolution

**Question**: What did we learn and what changes?

This layer synthesizes operational signals from production into actionable insights that close the feedback loop to the Product Intelligence layer. It takes frozen Reliability Health Reports from Layer 6 and produces Evolution Signals that assess value hypothesis outcomes, identify reliability trends, and recommend whether the system should continue, be watched, or trigger new discovery.

**Kit**: `aieos-insight-evolution-kit` *(built)*

**Inputs**: Frozen Reliability Health Reports (RHRs) from Reliability & Resilience Kit (Layer 6) — minimum 2 required. Optional: frozen Value Hypothesis from Product Intelligence Kit (Layer 2).

**Outputs**: Frozen Evolution Signal (ES) — VH outcome assessment, reliability trend analysis, pattern analysis, re-entry signal (maintain / watch / re-discover), recommended actions.

**Downstream consumer**: Product Intelligence (Layer 2) — if re-entry signal is `re-discover`, ES §6 discovery question and §7 Discovery actions feed a new PIK engagement. Re-entry is advisory; a human product owner decides whether to act.

---

### Layer 8: operational diagnostics

**Question**: How do we diagnose and resolve operational failures?

This layer governs structured investigation, hypothesis tracking, and postmortem analysis for production failures. It adds diagnostic depth for SEV1/2 incidents and incidents with organizational learning value. It is a reactive operational track — triggered by production events, not SDLC progression.

**Kit**: `aieos-operational-diagnostics-kit` *(built)*

**Trigger**: SEV1/2 incident declared (required); operator judgment for lower-severity incidents with learning value.

**Inputs**: Frozen Service Reliability Profile (SRP) from Layer 6 (service baseline, SLO targets, known failure modes); past Incident Records from Layer 6 (known failure patterns); frozen Release Record §7 from Layer 5 (recent changes, deployment state); frozen System Architecture Document (SAD) from Layer 4 (service dependencies).

**Outputs**: Frozen Postmortem Record (PMR) — root cause analysis, SLO impact, corrective actions, lessons learned. Optional frozen Runbook (RB) — codified resolution procedure for a known failure class.

**Downstream consumers**: Reliability & Resilience (Layer 6) — next RHR references PMR IDs; PMR corrective actions may trigger SRP revision. Engineering Execution (Layer 4) — PMR corrective actions may become engineering work items. Product Intelligence (Layer 2) — recurring patterns may warrant discovery re-engagement. Insight & Evolution (Layer 7) — PMR data supplements ER §8 for portfolio synthesis.

**Relationship to Layer 6 Incident Records**: RRK Incident Records (IRs) are the lightweight operational record required for every incident at any severity. ODK adds depth for SEV1/2 or incidents with learning value: the Investigation Record (INR) documents how the team diagnosed the failure; the Postmortem Record (PMR) documents what the organization learned. Complementary, not overlapping.

---

### Layer 9: quality assurance

**Question**: Is it verified beyond unit scope?

This layer governs verification campaigns, integration testing, system testing, and pre-release quality gates. It fills the gap between individual work item review (Layer 4) and release readiness (Layer 5) by verifying cross-component behavior, integration point correctness, and system-level quality.

**Kit**: `aieos-quality-assurance-kit` *(built)*

**Position**: Cross-cutting gate between Layer 4 and Layer 5. Triggered after ORD freeze, before REK entry.

**Inputs**: Frozen ORD from Engineering Execution (Layer 4), SAD (integration points), TDD (test strategy), ACF (constraints), WDD (work items for traceability)

**Outputs**: Frozen Quality Gate Record (QGR) — quality disposition declaration (PASS / CONDITIONAL / FAIL), test campaign evidence, defect status, coverage assessment

**Downstream consumer**: Release & Exposure (Layer 5) — QGR provides quality clearance for release entry

**Artifact flow**: QAER → VP → TCR → QGR

---

### Layer 10: security & compliance

**Question**: Is it secure and compliant?

This layer governs threat modeling, security assessment, compliance evidence, and dependency auditing. It is cross-cutting — artifacts are triggered at different points in the pipeline rather than occupying a single sequential position.

**Kit**: `aieos-security-compliance-kit` *(built)*

**Trigger points**:
- After SAD freeze (Layer 4): Threat Model
- After code complete (Layer 4/9): Security Assessment Record, Dependency Audit Record
- When compliance mandate identified (any layer): Compliance Evidence Record

**Inputs**: SAD (system architecture), ACF §3 (security guardrails), TDD (technical design), implementation code, regulatory mandates, dependency manifests

**Outputs**: Frozen Threat Model (TM) — attack surface analysis and mitigations. Frozen Security Assessment Record (SAR) — pre-release security verification. Frozen Compliance Evidence Record (CER) — regulatory evidence chain. Frozen Dependency Audit Record (DAR) — dependency vulnerability and license audit.

**Downstream consumers**: Quality Assurance (Layer 9) — TM and SAR feed QGR security assessment. Release & Exposure (Layer 5) — SAR provides security clearance for release. Reliability & Resilience (Layer 6) — TM informs security monitoring requirements.

**Artifact flow**: TM → SAR + DAR (parallel) → CER (as needed)

---

### Layer 11: data & configuration

**Question**: Is configuration governed and are feature flags managed?

This layer governs configuration management, feature flag lifecycle, and data schema evolution. It prevents configuration drift, stale feature flags, and untracked schema changes — common sources of production failures that other kits can detect but not prevent.

**Kit**: `aieos-data-configuration-kit` *(built)*

**Trigger points**:
- During EEK (after TDD freeze): Configuration Specification, Data Schema Record
- During REK (when feature flags created): Feature Flag Lifecycle Record
- Periodic: FFLR review at each RHR cycle; DSR versioning when schemas evolve

**Inputs**: TDD (config requirements, data models), ORD (config readiness), RR (feature flag states at release), RP (flag-based exposure strategy), incident data from RRK/ODK

**Outputs**: Frozen Configuration Specification (CSPEC) — config structure, validation rules, per-environment values. Frozen Feature Flag Lifecycle Record (FFLR) — flag inventory, state tracking, retirement criteria. Frozen Data Schema Record (DSR) — schema definitions, evolution rules, migration plans.

**Downstream consumers**: Release & Exposure (Layer 5) — CSPEC provides config validation criteria. Reliability & Resilience (Layer 6) — config drift detection requirements, stale flag alerts. Platform & Infrastructure (Layer 12) — CSPEC references EM for environment-specific values.

---

### Layer 12: platform & infrastructure

**Question**: What infrastructure supports it?

This layer governs infrastructure decisions, deployment targets, and environment management. It is foundational — its artifacts provide inputs to multiple pipeline layers rather than consuming their outputs. It captures the "why" behind infrastructure choices and the "what" of deployment targets.

**Kit**: `aieos-platform-infrastructure-kit` *(built)*

**Trigger points**:
- Initiative planning: Platform Decision Records (per decision)
- System design (during EEK): Infrastructure Specification
- Project setup: Environment Matrix

**Inputs**: Strategic requirements, reliability data from RRK (RHR trends), infrastructure-related PMR findings from ODK

**Outputs**: Frozen Platform Decision Record (PDR) — technology decisions with rationale and tradeoffs. Frozen Infrastructure Specification (ISPEC) — deployment targets, resources, scaling, DR strategy. Frozen Environment Matrix (EM) — environment definitions, promotion rules, parity requirements. Frozen System Model Record (SMR) — service inventory, dependency graph, environment deployment mapping.

**Downstream consumers**: Engineering Execution (Layer 4) — PDRs inform ACF platform assumptions; ISPEC informs deployment model; EM informs testing. Release & Exposure (Layer 5) — ISPEC provides deployment targets; EM provides promotion rules. Reliability & Resilience (Layer 6) — ISPEC provides infrastructure monitoring baseline.

---

### Layer 13: documentation & knowledge

**Question**: Is user-facing documentation governed?

This layer governs user-facing documentation, API references, support knowledge bases, and documentation health. It ensures that what users and support teams read is accurate, current, and traceable to what was actually built and released. It is cross-cutting — artifacts are triggered at different points in the pipeline.

**Kit**: `aieos-documentation-knowledge-kit` *(built)*

**Trigger points**:
- After TDD freeze (Layer 4): API Reference Record (contracts defined)
- After RR freeze (Layer 5): User Documentation Record, Support Knowledge Article, API Reference Record (public API released)
- After PMR freeze (Layer 8): Support Knowledge Article (incident learnings)
- Periodic (aligned with RRK health reviews): Documentation Health Review

**Inputs**: Frozen PRD (what was built), frozen TDD (API contracts), frozen RR (what was released), frozen PMR (incident learnings), frozen SRP (what's running)

**Outputs**: Frozen User Documentation Record (UDR) — end-user documentation with capability coverage and accuracy traceability. Frozen API Reference Record (ARR) — structured API documentation with contract fidelity. Frozen Support Knowledge Article (SKA) — support team knowledge base articles. Frozen Documentation Health Review (DHR) — periodic documentation currency and coverage audit.

**Downstream consumers**: Reliability & Resilience (Layer 6) — DHR health scores feed RHR operational health picture. Support teams — SKAs reduce escalation volume. End users — UDRs and ARRs are the primary documentation interface.

---

### Layer 14: peer review

**Question**: Has this artifact been evaluated from multiple expert perspectives?

This layer governs autonomous multi-perspective peer review. It replicates the role of human review boards (architecture review boards, design reviews, code reviews, CABs) by running 12 specialized review lenses against artifacts at key lifecycle points. Each lens represents an expert perspective (security, reliability, cost, operability, etc.) and produces structured findings independently. The aggregated Peer Review Record surfaces findings, conflicts between perspectives, and an overall PASS/FAIL disposition.

**Kit**: `aieos-peer-review-kit` *(built)*

**Trigger points**:
- After DPRD validated (PIK): Concept Review
- After SAD validated (EEK): Architecture Review (all 9 lenses)
- After TDD validated (EEK): Technical Design Review
- After WDD validated (EEK): Implementation Readiness Review
- After ORD validated (EEK): Code Review
- After QGR validated (QAK): Integration Review
- After RP validated (REK): Operational Readiness Review
- After RHR validated (RRK): Post-Deployment Review
- After PMR validated (ODK): Incident Review

**Inputs**: Validated (not yet frozen) artifact from the producing kit, plus relevant context documents (upstream frozen artifacts, principles files)

**Outputs**: Frozen Peer Review Record (PRR) — per-lens findings with severity and remediation, conflict analysis between lenses, aggregate PASS/FAIL disposition. PRR must pass before the reviewed artifact can freeze.

**Downstream consumers**: The producing kit — PRR findings inform artifact revision before freeze. Portfolio synthesis (IEK) — PRR patterns across initiatives surface systematic quality gaps.

### Layer 15: business process

**Question**: Are affected business processes governed through the change?

This layer governs the organizational and process change side of solution delivery. It identifies which business processes are affected by a technical change, plans how users transition from current-state to future-state workflows, and confirms that affected teams are prepared before release.

**Kit**: `aieos-business-process-kit` *(built)*

**Trigger points:**
- After SAD or TDD freeze (Layer 4): Process Impact Assessment
- After PIA freeze: Transition Plan
- Before REK entry: Readiness Confirmation

**Inputs**: Frozen SAD (component boundaries, integration points), frozen TDD (behavior changes, UI changes, API changes)

**Outputs**: Frozen Process Impact Assessment (PIA) — affected process inventory, impact classification, role mapping. Frozen Transition Plan (TP) — transition strategy, communication plan, training plan, cutover schedule. Frozen Readiness Confirmation (RC) — training evidence, SOP updates, stakeholder acknowledgment, readiness declaration.

**Downstream consumers**: Release & Exposure (Layer 5) — RC readiness declaration informs release entry; TP cutover schedule aligns with release timing.

**Artifact flow**: PIA → TP → RC

---

## Kit registry

| Layer | Kit Repository | Category | Status |
|-------|---------------|----------|--------|
| 1. Strategic Direction | `aieos-strategic-direction-kit` | Pipeline | Built (not yet in standard flow) |
| 2. Product Intelligence | `aieos-product-intelligence-kit` | Pipeline | Built |
| 3. Solution Sourcing | `aieos-solution-sourcing-kit` | Pipeline | Built |
| 4. Engineering Execution | `aieos-engineering-execution` | Pipeline | Built |
| 5. Release & Exposure | `aieos-release-exposure-kit` | Pipeline | Built |
| 6. Reliability & Resilience | `aieos-reliability-resilience-kit` | Pipeline | Built |
| 7. Insight & Evolution | `aieos-insight-evolution-kit` | Pipeline | Built |
| 8. Operational Diagnostics | `aieos-operational-diagnostics-kit` | Operational | Built |
| 9. Quality Assurance | `aieos-quality-assurance-kit` | Cross-cutting | Built |
| 10. Security & Compliance | `aieos-security-compliance-kit` | Cross-cutting | Built |
| 11. Data & Configuration | `aieos-data-configuration-kit` | Cross-cutting | Built |
| 12. Platform & Infrastructure | `aieos-platform-infrastructure-kit` | Cross-cutting | Built |
| 13. Documentation & Knowledge | `aieos-documentation-knowledge-kit` | Cross-cutting | Built |
| 14. Peer Review | `aieos-peer-review-kit` | Cross-cutting | Built |
| 15. Business Process | `aieos-business-process-kit` | Cross-cutting | Built |

---

## Inter-Layer handoff rules

1. **Artifacts cross layer boundaries as frozen, validated documents.** No layer accepts in-progress work from an upstream layer.
2. **Handoff artifacts must satisfy the downstream layer's intake gate.** The downstream kit validates its inputs — it does not trust upstream kits blindly.
3. **Layer skipping is permitted only with explicit justification.** A team with a well-understood bug fix may enter Engineering Execution directly (Path B) without a discovery engagement. The Kit Entry Record captures and justifies the skip.
4. **Layer re-entry is defined in each kit's playbook.** When upstream artifacts change after downstream work has begun, the cross-kit re-entry protocol determines what gets re-validated.

## Cross-Layer project artifacts

**Engagement Records (ERs)** are project-level artifacts that span all layers. Unlike kit artifacts, they are not owned by any single layer — they are maintained in the consuming project at `docs/engagement/er-{initiative}.md` and updated by each kit's operators as work passes through that layer.

ERs serve two purposes:
- **Episodic memory** — a structured index of every artifact ID, outcome, and key decision for one initiative, making the full artifact history queryable without re-reading all documents
- **Portfolio synthesis input** — ERs are the primary input to Portfolio Evolution Signals (IEK Layer 7), which synthesize cross-initiative patterns and generate improvement proposals for the governing prompt files

The ER spec lives in `aieos-governance-foundation/docs/engagement-record-spec.md`. No single kit owns the ER format — it is a system-level standard.

---

## Current build state

As of the current build, Layers 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, and 15 are operational:

**Pipeline handoffs (Layers 1–7):**
- **Layer 2 → Layer 4** (direct) is the proven inter-kit handoff path when Build is the obvious choice. The frozen DPRD from PIK becomes the EEK PRD via a defined acceptance check.
- **Layer 2 → Layer 3 → Layer 4** is the path when sourcing evaluation is needed. The frozen DPRD enters SSK, which produces SOER → VER → SDR. The frozen SDR and DPRD are then delivered to EEK. SSK is optional — skip when Build is clearly the right approach (document fast-path justification in KER).
- **Layer 4 → Layer 5** handoff: the frozen ORD from EEK becomes the Release & Exposure Kit input via the Release Entry Gate. When Layer 9 (QAK) is adopted, the frozen QGR supplements the ORD as release entry evidence.
- **Layer 5 → Layer 6** handoff: the frozen Release Record §7 (Handoff to Layer 6) becomes the Reliability & Resilience Kit input via the Service Reliability Entry Gate.
- **Layer 6 → Layer 7** handoff: frozen Reliability Health Reports (minimum 2) become the Insight & Evolution Kit input. No entry gate — the ES confirms frozen input status in §1. An optional frozen Value Hypothesis from Layer 2 enables VH outcome assessment.
- **Layer 7 → Layer 2** feedback: if the Evolution Signal re-entry signal is `re-discover`, the ES §6 discovery question and §7 recommended actions inform a new PIK Discovery Intake. The feedback loop is advisory — a human product owner decides whether to initiate a new discovery engagement.

**Operational track (Layer 8):**
- **Layer 8 (Operational Diagnostics)** is triggered by production events, not SDLC progression. A SEV1/2 incident (or operator judgment for high-learning-value events) triggers DCR → INR → PMR → optional RB. Frozen PMRs feed back into Layers 6, 7, and optionally 2 and 4.

**Cross-cutting governance (Layers 9–15):**
- **Layer 9 (Quality Assurance)** operates as a gate between Layer 4 and Layer 5. After ORD freeze, the QAK runs verification campaigns and produces a Quality Gate Record that declares quality disposition. QAK is conditionally required — engage when the initiative has integration points, external dependencies, or cross-component test scope. For single-service changes with no external integration, QAK is optional. When adopted, no opt-out path after QAER is frozen.
- **Layer 10 (Security & Compliance)** operates at multiple trigger points: Threat Models after SAD freeze, Security Assessments after code complete, Dependency Audits before release, Compliance Evidence Records when mandates apply. Artifacts feed into QAK (Layer 9) and REK (Layer 5) as security clearance evidence.
- **Layer 11 (Data & Configuration)** establishes configuration governance during EEK (CSPEC, DSR), tracks feature flags during REK (FFLR), and provides config drift detection requirements to RRK. The FFLR is periodically re-frozen to track flag lifecycle.
- **Layer 12 (Platform & Infrastructure)** provides foundational inputs to EEK (ACF platform assumptions), REK (deployment targets), and RRK (infrastructure monitoring baseline). PDRs capture technology decisions; ISPEC defines deployment infrastructure; EM defines environments and promotion rules; SMR captures service topology and dependency mapping.
- **Layer 13 (Documentation & Knowledge)** governs user-facing documentation at multiple trigger points: API Reference Records after TDD freeze, User Documentation Records and Support Knowledge Articles after release, SKAs after incident postmortems, Documentation Health Reviews aligned with RRK health review cadence. Adoption is optional — teams not using DKK manage documentation outside AIEOS governance.
- **Layer 14 (Peer Review)** provides autonomous multi-perspective peer review at artifact lifecycle points. When adopted, PRK runs specialized review lenses (security, reliability, resilience, performance, cost, operability, observability, maintainability, compliance, devex, business-value, accessibility) against validated artifacts and produces a Peer Review Record (PRR) that must pass before the reviewed artifact can freeze. Trigger points span PIK, EEK, QAK, REK, RRK, and ODK. Adoption is optional — teams not using PRK proceed with standard validate-then-freeze.
- **Layer 15 (Business Process)** governs the organizational and process change side of solution delivery. It identifies affected business processes after SAD or TDD freeze (Process Impact Assessment), plans user transitions (Transition Plan), and confirms team readiness before release (Readiness Confirmation). RC readiness declaration and TP cutover schedule feed into REK release entry. Adoption is optional — teams not using BPK manage process change outside AIEOS governance.

**Entry gate patterns:**
- The Kit Entry Gate pattern is used at Layers 3, 4, 5, 6, and 9 to enforce upstream verification before artifact generation begins. Layer 3 (SSK) requires a frozen DPRD as its entry gate. Layer 7 uses self-confirming input validation in the ES prompt. Layer 8 uses the Diagnostic Context Record (DCR) as its entry gate. Layers 10–13 and 15 use trigger-based entry rather than sequential gates.

All 15 layer kits are built and operational. Layers 1 (Strategic Direction) and 3 (Solution Sourcing) are optional upstream entry points — initiatives may start at Layer 2 (PIK) when portfolio prioritization isn't needed and skip Layer 3 when Build is obvious. Layer 8 adds a reactive operational track. Layers 9–15 add cross-cutting governance.
