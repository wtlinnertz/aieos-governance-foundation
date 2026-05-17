# AIEOS: AI-Enabled Operating System

## What AIEOS is

AIEOS is a governance framework for AI-assisted software delivery. It structures how artifacts: PRDs, architecture documents, release records, SLO profiles, postmortems: are produced, validated, and connected across the full software development lifecycle.

The core idea: AI-generated engineering artifacts need structure around them to be trustworthy. AIEOS provides that structure. Rules live in specs. AI generates from prompts and templates. Validators judge the output as PASS or FAIL. Humans approve and freeze artifacts before downstream work begins.

The result: every production decision: an SLO target, a deployment strategy, a scope boundary: is traceable back to a governed upstream artifact. Nothing is invented in the middle. Nothing is silently assumed.

## The problem AIEOS solves

AI can generate engineering documents. Without structure, the output drifts: scope creeps between artifacts, constraints get silently dropped, assumptions go unvalidated, and downstream work builds on unstable foundations. Teams get impressive-looking documents that don't connect and can't be trusted.

AIEOS solves this by enforcing three things:

1. Separation of concerns: Rules (specs), structure (templates), generation behavior (prompts), and judgment (validators) live in separate files. Changing one doesn't break the others.
2. Freeze-before-promote: Upstream artifacts are frozen (immutable) before downstream work begins. The architecture document can't shift under the execution plan.
3. Validators judge, they don't help: Validation produces PASS or FAIL, not suggestions. This prevents the AI from rationalizing its own output.
## How work flows through AIEOS

AIEOS organizes work into layers. Each layer answers a different question in the value-delivery lifecycle. A kit governs each layer: providing specs, templates, prompts, and validators for that layer's artifacts.

Work flows top-down for delivery and bottom-up for learning:

```
Pipeline Layers (top-down delivery, bottom-up learning)
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 1: Strategic Direction       What are we trying to achieve?  │
│  SBR → PPR                                          (optional)      │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 2: Product Intelligence      What should we build and why?   │
│  WCR → PFD → VH → AR → EL → DPRD                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 3: Solution Sourcing         How do we obtain it?            │
│  SOER → VER → SDR                                   (optional)      │
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
└─────────────────────────────────────────────────────────────────────┘
         ↑ Layer 7 feeds learning back to Layer 2 ↑

Operational Track
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 8: Operational Diagnostics   How do we diagnose failures?    │
│  DCR → INR → PMR → RB                                               │
└─────────────────────────────────────────────────────────────────────┘

Cross-Cutting Governance (Layers 9–15)
┌─────────────────────────────────────────────────────────────────────┐
│  Layer 9:  Quality Assurance        Pre-release quality gate        │
│  Layer 10: Security & Compliance    Threat models, security, audit  │
│  Layer 11: Data & Configuration     Config mgmt, feature flags      │
│  Layer 12: Platform & Infrastructure  Infra decisions, environments │
│  Layer 13: Documentation & Knowledge  User docs, API refs, KB       │
│  Layer 14: Peer Review              Multi-perspective review lenses │
│  Layer 15: Business Process         Process impact & readiness      │
└─────────────────────────────────────────────────────────────────────┘
```

Artifacts cross layer boundaries as frozen, validated documents. Each kit validates its own inputs: it doesn't trust upstream kits blindly. The system is a loop, not a pipeline.

## The kits

Each kit is an independent, self-contained repository. A team can adopt one kit and get immediate value, or use the full system for end-to-end governance.

| Kit | Layer | What it does |
|-----|-------|-------------|
| Strategic Direction Kit | 1 | Portfolio prioritization via strategic bets, capability plans, and Portfolio Prioritization Record. Optional; start at Layer 2 if you don't need portfolio prioritization. |
| Product Intelligence Kit | 2 | Transforms a product problem into engineering-ready requirements through discovery: problem framing, value hypotheses, assumption testing, and Discovery PRD. |
| Solution Sourcing Kit | 3 | Build/Buy/Adopt sourcing decisions with option evaluation and Sourcing Decision Record. Optional; skip when Build is obvious. |
| Engineering Execution Kit | 4 | Moves from PRD through architecture, design, test strategy, and work decomposition to a production-ready system with Operational Readiness Document. |
| Release & Exposure Kit | 5 | Governs deployment strategy, progressive exposure, rollback conditions, and release authorization. Produces Release Records. |
| Reliability & Resilience Kit | 6 | Defines SLOs, error budgets, and burn rate alerts. Records incidents and produces Reliability Health Reports. |
| Insight & Evolution Kit | 7 | Synthesizes production signals into actionable insights. Determines whether to maintain, watch, or re-discover, closing the feedback loop to Layer 2. |
| Operational Diagnostics Kit | 8 | Structured diagnosis for production failures. Produces root cause analysis, postmortems, and codified runbooks. Triggered by incidents, not SDLC progression. |
| Quality Assurance Kit | 9 | Pre-release quality gate between Engineering Execution and Release. Covers verification plans, test coverage reports, and Quality Gate Record. |
| Security & Compliance Kit | 10 | Threat modeling, security assessment, compliance evidence, and dependency audit across layers. Triggered at key points. |
| Data & Configuration Kit | 11 | Configuration management, feature flag lifecycle, and data schema governance. Spans Engineering Execution through Reliability. |
| Platform & Infrastructure Kit | 12 | Infrastructure decisions, deployment targets, environment management. Provides foundational inputs to Engineering, Release, and Reliability. |
| Documentation & Knowledge Kit | 13 | User-facing documentation, API references, and support knowledge bases. Triggered from Engineering, Release, and Operational Diagnostics. |
| Peer Review Kit | 14 | Multi-perspective autonomous review at artifact lifecycle points using specialized lenses (security, reliability, cost, compliance). Optional. |
| Business Process Kit | 15 | Business process impact assessment, transition planning, and readiness confirmation for process-affecting changes. Optional. |

## AIEOS console

**[aieos-console](https://github.com/your-org/aieos-console)** is a browser-based guided wizard for running AIEOS processes. Currently under active development.

The console provides:
- Guided sequencing: shows which steps are complete, current, and remaining
- Freeze-before-promote enforcement: prevents generating downstream artifacts until upstream ones are frozen
- Automatic input assembly: reads specs, templates, prompts, and frozen artifacts from kit directories
- LLM integration: generates and validates artifacts with PASS/FAIL results
- Intake forms: guided form experiences instead of raw markdown editing

The console targets three audiences: engineers running the artifact flow, product managers needing form-based intake without kit navigation, and organizational leaders evaluating AIEOS adoption.

## Where to start

**Understanding how AIEOS works**
Read [Design Philosophy](docs/philosophy.md), then the [Layer Model](docs/layer-model.md).

**Running an initiative**
Start with [Getting Started](docs/getting-started.md): find your scenario and follow the path. Unsure which path fits? Use [Initiative Presets](docs/initiative-presets.md) for five golden paths (New Feature, Enhancement, Compliance, Performance Fix, Exploratory Research).

**Seeing a complete example**
Read the [TaskFlow Notifications walkthrough](examples/taskflow-full-flow/README.md): a full initiative from discovery through production operation, including re-entry and escalation scenarios.

**Tracking initiative status**
Use the [Initiative State View](docs/initiative-state-view.md) template to see which artifacts exist, their freeze status, and which layer you're in.

---

## Governance reference

This repository is the canonical authority for the AIEOS governance model and system standards. It's not a kit: it contains no artifact prompts, templates, or validators. It defines the rules that all kits follow.

### Contents

| File | Purpose |
|------|---------|
| `governance-model.md` | Complete structural rules, taxonomy, and invariants for every AIEOS kit |
| `docs/philosophy.md` | Design philosophy: the "why" behind the governance model |
| `docs/layer-model.md` | The sixteen-layer model and how kits map to organizational layers |
| `docs/kit-structure-standard.md` | Compliance checklist for building and auditing AIEOS-compatible kits |
| `docs/getting-started.md` | Task-oriented entry guide: find your scenario and follow the path |
| `docs/initiative-presets.md` | Five golden paths for common initiative types with full artifact routing |
| `docs/initiative-state-view.md` | Template for tracking initiative state across all kit layers |

### How kits relate to this repo

Every AIEOS kit:

1. Carries a synchronized copy of `governance-model.md` in its own `docs/` directory. This copy exists so the kit is self-contained and usable without this repo.
2. Treats this repo as canonical. When the governance model changes, this repo is updated first. Kits are updated to match. Kits do not update governance-model.md independently.
3. References this repo in their CLAUDE.md to declare the authority source.

This means a kit copy of governance-model.md is always correct or behind: never ahead.

### Governance model version

Current: `1.6`

Changes to the governance model follow the protocol in `governance-model.md` §15.

### Kit registry

| Layer | Repository | Status |
|-------|-----------|--------|
| 1. Strategic Direction | `aieos-strategic-direction-kit` | Built (optional) |
| 2. Product Intelligence | `aieos-product-intelligence-kit` | Built |
| 3. Solution Sourcing | `aieos-solution-sourcing-kit` | Built (optional) |
| 4. Engineering Execution | `aieos-engineering-execution` | Built |
| 5. Release & Exposure | `aieos-release-exposure-kit` | Built |
| 6. Reliability & Resilience | `aieos-reliability-resilience-kit` | Built |
| 7. Insight & Evolution | `aieos-insight-evolution-kit` | Built |
| 8. Operational Diagnostics | `aieos-operational-diagnostics-kit` | Built |
| 9. Quality Assurance | `aieos-quality-assurance-kit` | Built |
| 10. Security & Compliance | `aieos-security-compliance-kit` | Built |
| 11. Data & Configuration | `aieos-data-configuration-kit` | Built |
| 12. Platform & Infrastructure | `aieos-platform-infrastructure-kit` | Built |
| 13. Documentation & Knowledge | `aieos-documentation-knowledge-kit` | Built |
| 14. Peer Review | `aieos-peer-review-kit` | Built (optional) |
| 15. Business Process | `aieos-business-process-kit` | Built (optional) |

All 15 layer kits are built and operational. The Governance Foundation is the canonical authority for all kits — it is not a layer kit and has no layer number.
