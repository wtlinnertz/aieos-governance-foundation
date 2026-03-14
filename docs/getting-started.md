# Getting Started with AIEOS

This guide is organized by what you are trying to accomplish. Find your scenario and follow the path.

For a comprehensive reference of all entry points, exit conditions, parallelism rules, and flow permutations, see [`flow-reference.md`](flow-reference.md). For framework and initiative validation procedures, see [`healthcheck-playbook.md`](healthcheck-playbook.md). For the machine-readable flow graph used by AI navigation tools, see [`navigation-map.md`](navigation-map.md). For the autonomous correction loop pattern (bounded iteration on validation failures), see [`review-convergence-loop.md`](review-convergence-loop.md).

---

## AI Sherpa Mode

If you are using an AI assistant (e.g., Claude Code) as your guide through AIEOS, the framework provides navigation tools that enable the AI to act as an interactive sherpa — routing you to the right starting point, tracking your position, and guiding you through decision points.

**Navigation tools** (defined in `docs/tools/`, implemented via `docs/bindings/`):

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| `initiative-router` | Asks routing questions, selects your entry point and preset | Starting a new initiative — "where do I begin?" |
| `position-check` | Reads your ER and artifacts to determine where you are | Resuming work, context switch, or feeling lost — "where am I?" |
| `decision-router` | At any fork, presents options and recommends a path | Reaching a decision point — "which way do I go?" |
| `handoff-navigator` | Verifies exit conditions and routes to the next kit | Completing a kit — "what's next?" |

The AI combines these tools naturally as you work. You don't need to invoke them explicitly — the sherpa reads the [`navigation-map.md`](navigation-map.md) and guides you through the choose-your-own-adventure flow.

**Self-correction:** If the AI gets off track, `position-check` re-orients by reading ground truth (your actual files), not memory. Every decision table includes an escape hatch: "if none of the options match, re-check position."

---

## Kit Map

```
Pipeline Layers:
┌──────────────────────────────────────────────────────────────────────────┐
│  Layer 1: Strategic Direction Kit (SDK)               ← optional         │
│  SBR (per bet) → PPR (portfolio ranking)                                 │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 2: Product Intelligence Kit (PIK)                                  │
│  WCR → Discovery Intake → PFD → VH → AR → EL → DPRD                     │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 3: Solution Sourcing Kit (SSK)              ← optional            │
│  SOER → VER → SDR                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 4: Engineering Execution Kit (EEK)                                 │
│  KER → PRD → ACF → SAD → DCF → TDD → WDD → ORD                          │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 5: Release & Exposure Kit (REK)                                    │
│  RER → RCF → RP → RR                                                     │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 6: Reliability & Resilience Kit (RRK)                              │
│  SRER → SRP → IR (per incident) → RHR (periodic)                         │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 7: Insight & Evolution Kit (IEK)              ← RRK feedback loop │
│  ES → PES (portfolio)                                                     │
└──────────────────────────────────────────────────────────────────────────┘
                    ↑ ES re-discover signal feeds back to PIK ↑

Operational Track:
┌──────────────────────────────────────────────────────────────────────────┐
│  Layer 8: Operational Diagnostics Kit (ODK)          ← triggered by SEV  │
│  DCR → INR → PMR → RB (optional)                                         │
└──────────────────────────────────────────────────────────────────────────┘

Cross-Cutting Governance:
┌──────────────────────────────────────────────────────────────────────────┐
│  Layer 9: Quality Assurance Kit (QAK)                ← gate: EEK → REK  │
│  QAER → VP → TCR → QGR                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 10: Security & Compliance Kit (SCK)           ← multi-layer       │
│  TM → SAR + DAR → CER (as needed)                                        │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 11: Data & Configuration Kit (DCK)            ← multi-layer       │
│  CSPEC → FFLR → DSR                                                      │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 12: Platform & Infrastructure Kit (PINFK)     ← foundational      │
│  PDR → ISPEC → EM                                                         │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 13: Documentation & Knowledge Kit (DKK)       ← multi-layer       │
│  UDR → ARR → SKA → DHR (periodic)                                        │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 14: Peer Review Kit (PRK)                     ← multi-layer       │
│  PRR (per review point)                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 15: Business Process Kit (BPK)                ← cross-cutting     │
│  PIA → TP → RC                                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## I need to decide which strategic bets to fund

**Starting point:** Strategic Direction Kit (SDK), Layer 1

**Path:**
1. For each strategic bet, author a Strategic Bet Record (SBR) with AI assistance
2. Validate each SBR (6 hard gates: thesis falsifiable, success signal measurable, failure signal defined, time horizon bounded, investment envelope stated, single accountable owner)
3. Freeze each validated SBR
4. Author a Portfolio Prioritization Record (PPR) ranking all active frozen SBRs
5. Validate the PPR (5 hard gates: strict rank order, trade-off rationale, cut line explicit, capacity not exceeded, review trigger defined)
6. Freeze the PPR
7. Route above-the-line SBRs to PIK for discovery

**Where to start:** `aieos-strategic-direction-kit/docs/playbook.md`

**When to use:** When the organization has multiple strategic options competing for limited capacity and needs a governed process for prioritization decisions. SDK is optional — teams with clear direction can enter PIK directly.

**When to skip:** When strategic direction is clear and singular, when the initiative is an enhancement within an existing bet, or when the team is small enough that strategic alignment happens naturally.

---

## I want to start a new initiative

**Starting point:** Product Intelligence Kit (PIK), Layer 2

**Path:**
1. Complete a Work Classification Record (WCR) to classify and route the work
2. Fill out the Discovery Intake Form (human input)
3. Validate the intake form against `discovery-intake-validator.md`
4. Generate artifacts in sequence: PFD → VH → AR → EL → DPRD
5. Validate and freeze each artifact before generating the next
6. Deliver the frozen DPRD to the Engineering Execution Kit

**Where to start:** `aieos-product-intelligence-kit/docs/playbook.md`

**Session setup:** `aieos-product-intelligence-kit/docs/session-setup.md`

**If you are not sure whether to run discovery:** Use the Work Classification Record. New features and exploratory work typically need PIK discovery. Well-understood bugs and enhancements may enter EEK directly via Path B (Kit Entry Record with justification).

---

## I need to evaluate sourcing options (Build/Buy/Adopt)

**Starting point:** Solution Sourcing Kit (SSK), Layer 3

**Prerequisite:** Frozen Discovery PRD (DPRD) from PIK

**Path:** SOER → VER → SDR

**When to use:** After discovery defines WHAT the initiative needs, before engineering defines HOW to build it. Use SSK when Build is not the obvious choice — for example, when commercial off-the-shelf (COTS) solutions exist, when open-source alternatives are viable, or when the team needs to formally evaluate sourcing options before committing engineering resources.

**When to skip:** When Build is clearly the right approach (no viable Buy or Adopt alternatives). Document the fast-path justification in the KER when entering EEK directly from PIK.

**Where to start:** `aieos-solution-sourcing-kit/docs/playbook.md`

**Arriving from PIK?** Read `aieos-solution-sourcing-kit/docs/entry-from-pik.md`

---

## We are ready to build

**Starting point:** Engineering Execution Kit (EEK), Layer 4

**Two entry paths:**
- **Path A** — You have a frozen Discovery PRD from PIK → place as `docs/sdlc/01-prd.md`, run acceptance check, proceed
- **Path B** — You have a well-understood scope without discovery → complete Product Brief, generate PRD, proceed

**Path after PRD is frozen (both paths):**

KER → PRD → ACF → SAD → DCF → TDD → WDD → ORD

**Where to start:** `aieos-engineering-execution-kit/docs/playbook.md`

**Session setup:** `aieos-engineering-execution-kit/docs/session-setup.md`

**Arriving from PIK?** Read `aieos-engineering-execution-kit/docs/entry-from-pik.md` first.

**Arriving from SSK?** Read `aieos-engineering-execution-kit/docs/entry-from-ssk.md` first. You will bring both the frozen DPRD (from PIK) and the frozen SDR (from SSK).

---

## We are ready to release

**Starting point:** Release & Exposure Kit (REK), Layer 5

**Prerequisite:** Frozen Operational Readiness Document (ORD) from EEK

**Path:** RER → RCF (if not already established) → RP → RR

**Where to start:** `aieos-release-exposure-kit/docs/playbook.md`

**Session setup:** `aieos-release-exposure-kit/docs/session-setup.md`

**Arriving from EEK?** Read `aieos-release-exposure-kit/docs/entry-from-eek.md` first.

---

## We are running a service in production

**Starting point:** Reliability & Resilience Kit (RRK), Layer 6

**Prerequisite:** Frozen Release Record (RR §7) from REK

**Path:** SRER → SRP → IR (per incident, as needed) → RHR (periodic review)

**Where to start:** `aieos-reliability-resilience-kit/docs/playbook.md`

**Session setup:** `aieos-reliability-resilience-kit/docs/session-setup.md`

**Arriving from REK?** Read `aieos-reliability-resilience-kit/docs/entry-from-rek.md` first.

---

## We had an incident

**Starting point:** Operational Diagnostics Kit (ODK), Layer 8

**Trigger:** SEV1/2 incident (required); lower-severity incidents with high learning value (operator judgment)

**Path:** DCR → INR → PMR → RB (optional, for recurring failure classes)

**Prerequisite:** Active or resolved incident with observable signals. Frozen SRP from RRK provides baseline context (recommended, not required).

**Where to start:** `aieos-operational-diagnostics-kit/docs/playbook.md`

**Session setup:** `aieos-operational-diagnostics-kit/docs/session-setup.md`

**Arriving from RRK after a SEV?** Read `aieos-operational-diagnostics-kit/docs/entry-from-rrk.md` first.

---

## I want to understand what we have learned

**Starting point:** Insight & Evolution Kit (IEK), Layer 7

**Prerequisite:** At least 2 frozen Reliability Health Reports (RHRs) from RRK. Optional: frozen Value Hypothesis (VH) from PIK.

**Path:**
- Per-service: Generate Evolution Signal (ES)
- Portfolio-level: Generate Portfolio Evolution Signal (PES) from 2+ frozen Engagement Records

**Re-entry signal:** The ES §6 re-entry signal (`maintain` / `watch` / `re-discover`) advises whether to return to PIK for a new discovery engagement. This is advisory — a human product owner decides.

**Where to start:** `aieos-insight-evolution-kit/docs/playbook.md`

**Session setup:** `aieos-insight-evolution-kit/docs/session-setup.md`

**Arriving from RRK?** Read `aieos-insight-evolution-kit/docs/entry-from-rrk.md` first.

---

## We need to verify integration quality before releasing

**Starting point:** Quality Assurance Kit (QAK), Layer 9

**Prerequisite:** Frozen ORD from EEK

**Path:** QAER → VP → TCR → QGR

**Where to start:** `aieos-quality-assurance-kit/docs/playbook.md`

**Arriving from EEK?** Read `aieos-quality-assurance-kit/docs/entry-from-eek.md` first.

**When to use:** Adopt QAK when the system has integration points between components, external service dependencies, or cross-component behavior that unit tests cannot verify. For simple, single-component systems, direct ORD → REK handoff may be sufficient.

---

## We need security governance

**Starting point:** Security & Compliance Kit (SCK), Layer 10

**Trigger points:**
- SAD frozen → generate Threat Model (TM)
- Code complete → generate Security Assessment Record (SAR) and Dependency Audit Record (DAR)
- Compliance mandate identified → generate Compliance Evidence Record (CER)

**Where to start:** `aieos-security-compliance-kit/docs/playbook.md`

---

## We need to manage configuration and feature flags

**Starting point:** Data & Configuration Kit (DCK), Layer 11

**Trigger points:**
- TDD frozen → generate Configuration Specification (CSPEC) and Data Schema Record (DSR)
- Feature flags created (during REK) → generate Feature Flag Lifecycle Record (FFLR)
- Periodic → FFLR review at each RHR cycle

**Where to start:** `aieos-data-configuration-kit/docs/playbook.md`

---

## We need to govern infrastructure decisions

**Starting point:** Platform & Infrastructure Kit (PINFK), Layer 12

**Trigger points:**
- Infrastructure decision needed → generate Platform Decision Record (PDR)
- System design phase → generate Infrastructure Specification (ISPEC)
- Project setup → generate Environment Matrix (EM)

**Where to start:** `aieos-platform-infrastructure-kit/docs/playbook.md`

---

## We need to govern user-facing documentation

**Starting point:** Documentation & Knowledge Kit (DKK), Layer 13

**Trigger points:**
- After TDD freeze → generate API Reference Record (ARR) for API contracts
- After REK release → generate User Documentation Record (UDR) for end-user docs
- After REK release or ODK postmortem → generate Support Knowledge Article (SKA)
- Periodic (aligned with RRK health reviews) → generate Documentation Health Review (DHR)

**Where to start:** `aieos-documentation-knowledge-kit/docs/playbook.md`

**When to use:** Adopt DKK when your product has end users who rely on documentation, API consumers who need reference material, or support teams who need structured knowledge bases. For internal-only tools with a small user base, DKK may be optional.

---

## We want multi-perspective peer review

**Starting point:** Peer Review Kit (PRK), Layer 14

**Trigger points:** PRK activates when an artifact passes its own validator but before freeze. It runs specialized review lenses and produces a Peer Review Record (PRR) that must pass before the artifact can freeze.

**Review points:**
- Concept Review → DPRD (business value, cost, compliance)
- Architecture Review → SAD (all 9 lenses)
- Technical Design Review → TDD (security, reliability, performance, maintainability, devex)
- Implementation Readiness → WDD (cost, operability, business value)
- Code Review → ORD (security, performance, reliability, maintainability, devex)
- Integration Review → QGR (reliability, security, performance)
- Operational Readiness → RP (operability, reliability, security, cost)
- Post-Deployment → RHR (reliability, performance, cost, operability)
- Incident Review → PMR (security, reliability, operability)

**Where to start:** `aieos-peer-review-kit/docs/playbook.md`

**When to use:** Adopt PRK when you want the quality assurance benefits of architecture review boards, design reviews, and CABs without requiring human reviewers at every stage. Recommended at minimum for SAD (architecture review) and TDD (technical design review).

---

## I need to govern business process changes

**Starting point:** Business Process Kit (BPK), Layer 15

Not every initiative affects business processes — but when one does, shipping the technical solution without governing the process change leads to adoption failures, broken workflows, and untrained teams.

**When to adopt BPK:**
- The initiative introduces new user-facing workflows
- The initiative changes how an existing process works
- The initiative removes or automates a manual process
- An API redesign affects downstream manual consumers

**Artifact sequence:**
1. SAD or TDD frozen → generate Process Impact Assessment (PIA) — identifies affected processes and roles
2. PIA frozen → generate Transition Plan (TP) — defines transition strategy, communication, training, cutover schedule
3. TP frozen + evidence collected → generate Readiness Confirmation (RC) — captures training completion, SOP updates, stakeholder acknowledgments

**Where to start:** `aieos-business-process-kit/docs/playbook.md`

---

## I want to publish artifacts to external systems

**Starting point:** `artifact-publish` tool in `aieos-governance-foundation/docs/tools/`

**What you need:**
- A frozen artifact to publish
- A binding for your target platform (e.g., `docs/bindings/artifact-publish-confluence.md`)
- An adapter implementing the binding (lives in your project, not in AIEOS)

**Path:**
1. Review the tool spec (`artifact-publish-spec.md`) to understand preconditions and constraints
2. Review or create a binding for your target document platform
3. Build or obtain an adapter that satisfies `docs/adapter-conformance-spec.md`
4. Invoke the tool to publish frozen artifacts

**Example binding:** `docs/bindings/artifact-publish-confluence.md` (Confluence)

---

## I want to sync work items to a tracker

**Starting point:** `work-item-sync` tool in `aieos-governance-foundation/docs/tools/`

**What you need:**
- A frozen WDD with enumerable work items
- A binding for your target tracker (e.g., `docs/bindings/work-item-sync-github-issues.md`)
- An adapter implementing the binding (lives in your project, not in AIEOS)

**Path:**
1. Review the tool spec (`work-item-sync-spec.md`) to understand preconditions and constraints
2. Review or create a binding for your target work tracker
3. Build or obtain an adapter that satisfies `docs/adapter-conformance-spec.md`
4. Invoke the tool to sync work items from the frozen WDD

**Example binding:** `docs/bindings/work-item-sync-github-issues.md` (GitHub Issues)

---

## I want to post validation results to my SCM platform

**Starting point:** `validation-status` tool in `aieos-governance-foundation/docs/tools/`

**What you need:**
- Validator JSON output conforming to governance-model.md §5
- A commit SHA or PR number to attach the status check to
- A binding for your target SCM platform (e.g., `docs/bindings/validation-status-github.md`)
- An adapter implementing the binding (lives in your project, not in AIEOS)

**Path:**
1. Review the tool spec (`validation-status-spec.md`) to understand preconditions and constraints
2. Review or create a binding for your target SCM platform
3. Build or obtain an adapter that satisfies `docs/adapter-conformance-spec.md`
4. Invoke the tool to post validator results as SCM status checks

**Example binding:** `docs/bindings/validation-status-github.md` (GitHub Check Runs)

---

## I want to tag releases on my SCM platform

**Starting point:** `release-tag` tool in `aieos-governance-foundation/docs/tools/`

**What you need:**
- A frozen Release Record (RR) from REK
- A binding for your target SCM platform (e.g., `docs/bindings/release-tag-github.md`)
- An adapter implementing the binding (lives in your project, not in AIEOS)

**Path:**
1. Review the tool spec (`release-tag-spec.md`) to understand preconditions and constraints
2. Review or create a binding for your target SCM platform
3. Build or obtain an adapter that satisfies `docs/adapter-conformance-spec.md`
4. Invoke the tool to create a tagged release from the frozen RR

**Example binding:** `docs/bindings/release-tag-github.md` (GitHub Releases)

---

## I do not know where I am

Use `initiative-state-view.md` to take stock of which artifacts exist for your initiative, their freeze status, and which layer you are in.

Steps:
1. Open `aieos-governance-foundation/docs/initiative-state-view.md`
2. Copy the blank template
3. Fill in which artifacts exist and their status
4. The first row with status `⬜ Not Started` or `🔄 In Progress` is where you are

---

## Engagement Records

For every initiative, create and maintain an Engagement Record (ER) in your consuming project at `docs/engagement/er-{initiative}.md`. The ER is the cross-layer memory of the initiative — artifact IDs, decisions, and outcomes.

ER spec: `aieos-governance-foundation/docs/engagement-record-spec.md`

---

## Not sure which path applies?

Use the initiative presets guide: `aieos-governance-foundation/docs/initiative-presets.md`

Five pre-defined initiative types map your situation to a complete artifact routing path.
