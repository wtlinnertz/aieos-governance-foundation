# AIEOS Layer Model

AIEOS organizes an organization's operating system into seven layers. Each layer governs a distinct phase of the value-delivery lifecycle. A kit governs each layer.

---

## The Seven Layers

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

The flow is top-down for value delivery and bottom-up for learning. Layer 7 feeds insight back to Layer 1. The system is a loop, not a pipeline.

---

## Layer Descriptions

### Layer 1: Strategic Direction

**Question**: What are we trying to achieve?

This layer governs the organization's goals, priorities, and bets at the strategic level. It produces OKRs, strategic briefs, initiative portfolios, and the tradeoff decisions that constrain all downstream layers.

**Kit**: `aieos-strategic-direction-kit` *(planned)*

**Outputs**: Strategic OKRs, initiative portfolio, tradeoff decisions

**Downstream consumer**: Product Intelligence (Layer 2)

---

### Layer 2: Product Intelligence

**Question**: What should we build and why?

This layer governs the transformation of strategic intent into engineering-ready product requirements. It runs discovery — problem framing, value hypothesis testing, assumption validation — and produces a frozen Discovery PRD.

**Kit**: `aieos-product-intelligence-kit` *(built)*

**Inputs**: Strategic direction, market signals, user research, stakeholder input

**Outputs**: Frozen Discovery PRD (engineering handoff artifact)

**Downstream consumer**: Engineering Execution (Layer 4) via Kit Entry Gate

---

### Layer 3: Flow Control

**Question**: What do we work on next and when?

This layer governs work intake, prioritization, sequencing, and capacity management across the engineering pipeline. It determines which engineering engagements start when, and ensures work arrives at Layer 4 properly classified and prioritized.

**Kit**: `aieos-flow-control-kit` *(planned)*

**Inputs**: Initiative portfolio, engineering capacity, in-flight work state

**Outputs**: Prioritized work queue, engagement authorizations

**Downstream consumer**: Engineering Execution (Layer 4)

---

### Layer 4: Engineering Execution

**Question**: How do we build it correctly?

This layer governs the full execution lifecycle from PRD through production-ready code. It produces architecture, design, work decomposition, and test-first implementation artifacts. It has two entry paths: discovery output from Layer 2 (Path A) or direct human input for well-understood work (Path B).

**Kit**: `aieos-engineering-execution-kit` *(built)*

**Inputs**: Frozen PRD (from PIK via Path A, or Product Brief via Path B), Kit Entry Record (gate)

**Outputs**: Frozen ORD (operational readiness decision), validated implementation artifacts

**Downstream consumer**: Release & Exposure (Layer 5)

---

### Layer 5: Release & Exposure

**Question**: How do we ship it safely?

This layer governs deployment policy, progressive delivery, feature exposure management, and release decisions. It translates production-ready artifacts into controlled, observable releases.

**Kit**: `aieos-release-exposure-kit` *(built)*

**Inputs**: Frozen ORD from Engineering Execution (Layer 4), organizational release policy (Release Context File)

**Outputs**: Frozen Release Record (RR) — release evidence, disposition declaration, Layer 6 handoff package

**Downstream consumer**: Reliability & Resilience (Layer 6)

---

### Layer 6: Reliability & Resilience

**Question**: How do we keep it running?

This layer governs SLOs, incident management, error budgets, and the operational health of systems in production. It defines what "working correctly" means and what to do when it isn't.

**Kit**: `aieos-reliability-resilience-kit` *(built)*

**Inputs**: Frozen Release Record (RR §7 Handoff to Layer 6) from Release & Exposure Kit (Layer 5), completed service reliability intake, incident evidence

**Outputs**: Frozen Reliability Health Report (RHR) — SLO compliance record, error budget state, incident summary, Layer 7 feed

**Downstream consumer**: Insight & Evolution (Layer 7)

---

### Layer 7: Insight & Evolution

**Question**: What did we learn and what changes?

This layer synthesizes operational signals from production into actionable insights that close the feedback loop to the Product Intelligence layer. It takes frozen Reliability Health Reports from Layer 6 and produces Evolution Signals that assess value hypothesis outcomes, identify reliability trends, and recommend whether the system should continue, be watched, or trigger new discovery.

**Kit**: `aieos-insight-evolution-kit` *(built)*

**Inputs**: Frozen Reliability Health Reports (RHRs) from Reliability & Resilience Kit (Layer 6) — minimum 2 required. Optional: frozen Value Hypothesis from Product Intelligence Kit (Layer 2).

**Outputs**: Frozen Evolution Signal (ES) — VH outcome assessment, reliability trend analysis, pattern analysis, re-entry signal (maintain / watch / re-discover), recommended actions.

**Downstream consumer**: Product Intelligence (Layer 2) — if re-entry signal is `re-discover`, ES §6 discovery question and §7 Discovery actions feed a new PIK engagement. Re-entry is advisory; a human product owner decides whether to act.

---

## Kit Registry

| Layer | Kit Repository | Status |
|-------|---------------|--------|
| 1. Strategic Direction | `aieos-strategic-direction-kit` | Planned |
| 2. Product Intelligence | `aieos-product-intelligence-kit` | Built |
| 3. Flow Control | `aieos-flow-control-kit` | Planned |
| 4. Engineering Execution | `aieos-engineering-execution-kit` | Built |
| 5. Release & Exposure | `aieos-release-exposure-kit` | Built |
| 6. Reliability & Resilience | `aieos-reliability-resilience-kit` | Built |
| 7. Insight & Evolution | `aieos-insight-evolution-kit` | Built |

---

## Inter-Layer Handoff Rules

1. **Artifacts cross layer boundaries as frozen, validated documents.** No layer accepts in-progress work from an upstream layer.
2. **Handoff artifacts must satisfy the downstream layer's intake gate.** The downstream kit validates its inputs — it does not trust upstream kits blindly.
3. **Layer skipping is permitted only with explicit justification.** A team with a well-understood bug fix may enter Engineering Execution directly (Path B) without a discovery engagement. The Kit Entry Record captures and justifies the skip.
4. **Layer re-entry is defined in each kit's playbook.** When upstream artifacts change after downstream work has begun, the cross-kit re-entry protocol determines what gets re-validated.

## Cross-Layer Project Artifacts

**Engagement Records (ERs)** are project-level artifacts that span all layers. Unlike kit artifacts, they are not owned by any single layer — they are maintained in the consuming project at `docs/engagement/er-{initiative}.md` and updated by each kit's operators as work passes through that layer.

ERs serve two purposes:
- **Episodic memory** — a structured index of every artifact ID, outcome, and key decision for one initiative, making the full artifact history queryable without re-reading all documents
- **Portfolio synthesis input** — ERs are the primary input to Portfolio Evolution Signals (IEK Layer 7), which synthesize cross-initiative patterns and generate improvement proposals for the governing prompt files

The ER spec lives in `aieos-governance-foundation/docs/engagement-record-spec.md`. No single kit owns the ER format — it is a system-level standard.

---

## Current Build State

As of the current build, Layers 2, 4, 5, 6, and 7 are operational:

- **Layer 2 → Layer 4** is the proven inter-kit handoff path. The frozen DPRD from PIK becomes the EEK PRD via a defined acceptance check.
- **Layer 4 → Layer 5** handoff: the frozen ORD from EEK becomes the Release & Exposure Kit input via the Release Entry Gate.
- **Layer 5 → Layer 6** handoff: the frozen Release Record §7 (Handoff to Layer 6) becomes the Reliability & Resilience Kit input via the Service Reliability Entry Gate.
- **Layer 6 → Layer 7** handoff: frozen Reliability Health Reports (minimum 2) become the Insight & Evolution Kit input. No entry gate — the ES confirms frozen input status in §1. An optional frozen Value Hypothesis from Layer 2 enables VH outcome assessment.
- **Layer 7 → Layer 2** feedback: if the Evolution Signal re-entry signal is `re-discover`, the ES §6 discovery question and §7 recommended actions inform a new PIK Discovery Intake. The feedback loop is advisory — a human product owner decides whether to initiate a new discovery engagement.
- The Kit Entry Gate pattern is used at Layers 4, 5, and 6 to enforce upstream verification before artifact generation begins. Layer 7 uses self-confirming input validation in the ES prompt instead.

The full seven-layer loop is now operational. Layers 1 and 3 remain planned.
