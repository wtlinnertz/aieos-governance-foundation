# AIEOS — AI-Enabled Operating System

## What AIEOS Is

AIEOS is a governance framework for AI-assisted software delivery. It structures how artifacts — PRDs, architecture documents, release records, SLO profiles, postmortems — are produced, validated, and connected across the full software development lifecycle.

The core idea: when AI generates engineering artifacts, the quality of the output depends on the quality of the structure around it. AIEOS provides that structure. Rules live in specs. AI generates from prompts and templates. Validators judge the output as PASS or FAIL. Humans approve and freeze artifacts before downstream work begins.

The result is a system where every production decision — an SLO target, a deployment strategy, a scope boundary — is traceable back to a governed upstream artifact. Nothing is invented in the middle. Nothing is silently assumed.

## The Problem AIEOS Solves

AI can generate engineering documents. But without structure, the output drifts: scope creeps between artifacts, constraints get silently dropped, assumptions go unvalidated, and downstream work builds on unstable foundations. Teams end up with impressive-looking documents that don't connect to each other and can't be trusted.

AIEOS solves this by enforcing three things:

1. **Separation of concerns** — Rules (specs), structure (templates), generation behavior (prompts), and judgment (validators) are separate files. Changing one doesn't silently break the others.
2. **Freeze-before-promote** — Upstream artifacts are frozen (immutable) before downstream work begins. The architecture document can't shift under the execution plan.
3. **Validators judge, they don't help** — Validation produces PASS or FAIL, not suggestions. This prevents the AI from rationalizing its own output.

## How Work Flows Through AIEOS

AIEOS organizes work into layers. Each layer answers a different question in the value-delivery lifecycle. A **kit** governs each layer — providing the specs, templates, prompts, and validators for that layer's artifacts.

Work flows top-down for delivery and bottom-up for learning:

```
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 1: Strategic Direction          What are we trying to achieve?│
├─────────────────────────────────────────────────────────────────────┤
│  Layer 2: Product Intelligence      What should we build and why?   │
│  WCR → PFD → VH → AR → EL → DPRD                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 3: Flow Control              What do we work on next?        │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 4: Engineering Execution     How do we build it correctly?   │
│  KER → PRD → ACF → SAD → DCF → TDD → WDD → ORD                     │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 5: Release & Exposure        How do we ship it safely?       │
│  RER → RCF → RP → RR                                                │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 6: Reliability & Resilience  How do we keep it running?      │
│  SRER → SRP → IR → RHR                                              │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 7: Insight & Evolution       What did we learn?              │
│  ES → PES                                                            │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 8: Operational Diagnostics   How do we diagnose failures?    │
│  DCR → INR → PMR → RB                                               │
└─────────────────────────────────────────────────────────────────────┘
         ↑ Layer 7 feeds learning back to Layer 2 ↑
```

Artifacts cross layer boundaries as frozen, validated documents. Each kit validates its own inputs — it does not trust upstream kits blindly. The system is a loop, not a pipeline.

## The Kits

Each kit is an independent, self-contained repository. A team can adopt one kit and get immediate value, or use the full system for end-to-end governance.

| Kit | Layer | What It Does |
|-----|-------|-------------|
| **Product Intelligence Kit** | 2 | Transforms a product problem into validated, engineering-ready requirements through structured discovery — problem framing, value hypotheses, assumption testing, and a frozen Discovery PRD. |
| **Engineering Execution Kit** | 4 | Moves from PRD through architecture, design, test strategy, and work decomposition to a production-ready system with a frozen Operational Readiness Document. |
| **Release & Exposure Kit** | 5 | Governs deployment strategy, progressive exposure, rollback conditions, and release authorization. Produces evidence-backed Release Records. |
| **Reliability & Resilience Kit** | 6 | Defines SLOs, error budgets, and burn rate alerts. Records incidents and produces periodic Reliability Health Reports. |
| **Insight & Evolution Kit** | 7 | Synthesizes production signals into actionable insights. Determines whether to maintain, watch, or re-discover — closing the feedback loop to Layer 2. |
| **Operational Diagnostics Kit** | 8 | Structured diagnosis for production failures. Produces root cause analysis, postmortems, and codified runbooks. Triggered by incidents, not SDLC progression. |

Layers 1 (Strategic Direction) and 3 (Flow Control) are planned but not yet built.

## AIEOS Console

**[aieos-console](https://github.com/your-org/aieos-console)** is a browser-based guided wizard for running AIEOS processes. It is currently under active development.

The console provides:
- **Guided sequencing** — shows which steps are complete, current, and remaining
- **Freeze-before-promote enforcement** — prevents generating downstream artifacts until upstream ones are frozen
- **Automatic input assembly** — reads specs, templates, prompts, and frozen artifacts from kit directories
- **LLM integration** — generates and validates artifacts with PASS/FAIL results
- **Intake forms** — guided form experiences instead of raw markdown editing

The console targets three audiences: engineers running the artifact flow, product managers who need form-based intake without kit navigation, and organizational leaders evaluating AIEOS adoption.

## Where to Start

**"I want to understand how AIEOS thinks"**
Read [Design Philosophy](docs/philosophy.md), then the [Layer Model](docs/layer-model.md).

**"I want to run an initiative"**
Start with [Getting Started](docs/getting-started.md) — find your scenario and follow the path. If you're unsure which path fits, use the [Initiative Presets](docs/initiative-presets.md) — five golden paths for common initiative types (New Feature, Enhancement, Compliance, Performance Fix, Exploratory Research).

**"I want to see a complete example"**
Read the [TaskFlow Notifications walkthrough](examples/taskflow-full-flow/README.md) — a full initiative traced from discovery through production operation, including a re-entry scenario and an escalation assessment.

**"I want to track where my initiative stands"**
Use the [Initiative State View](docs/initiative-state-view.md) template to see which artifacts exist, their freeze status, and which layer you're in.

---

## Governance Reference

This repository is the **canonical authority** for the AIEOS governance model and system standards. It is not a kit — it contains no artifact prompts, templates, or validators. It defines the rules that all kits follow.

### Contents

| File | Purpose |
|------|---------|
| `governance-model.md` | Complete structural rules, taxonomy, and invariants for every AIEOS kit |
| `docs/philosophy.md` | Design philosophy — the "why" behind the governance model |
| `docs/layer-model.md` | The eight-layer model and how kits map to organizational layers |
| `docs/kit-structure-standard.md` | Compliance checklist for building and auditing AIEOS-compatible kits |
| `docs/getting-started.md` | Task-oriented entry guide — find your scenario and follow the path |
| `docs/initiative-presets.md` | Five golden paths for common initiative types with full artifact routing |
| `docs/initiative-state-view.md` | Template for tracking initiative state across all kit layers |

### How Kits Relate to This Repo

Every AIEOS kit:

1. **Carries a synchronized copy** of `governance-model.md` in its own `docs/` directory. This copy exists so the kit is self-contained and usable without this repo.
2. **Treats this repo as canonical.** When the governance model changes, this repo is updated first. Kits are updated to match. Kits do not update governance-model.md independently.
3. **References this repo** in their CLAUDE.md to declare the authority source.

This means a kit copy of governance-model.md is always correct or behind — never ahead.

### Governance Model Version

Current: `1.0`

Changes to the governance model follow the protocol in `governance-model.md` §15.

### Kit Registry

| Layer | Repository | Status |
|-------|-----------|--------|
| 1. Strategic Direction | `aieos-strategic-direction-kit` | Planned |
| 2. Product Intelligence | `aieos-product-intelligence-kit` | Built |
| 3. Flow Control | `aieos-flow-control-kit` | Planned |
| 4. Engineering Execution | `aieos-engineering-execution-kit` | Built |
| 5. Release & Exposure | `aieos-release-exposure-kit` | Built |
| 6. Reliability & Resilience | `aieos-reliability-resilience-kit` | Built |
| 7. Insight & Evolution | `aieos-insight-evolution-kit` | Built |
| 8. Operational Diagnostics | `aieos-operational-diagnostics-kit` | Built |

Layers 1 and 3 remain planned. All other layers are operational.
