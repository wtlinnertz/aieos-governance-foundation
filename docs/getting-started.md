# Getting started with AIEOS

New to AIEOS? Start with the [Onboarding Guide](onboarding-guide.md) for a step-by-step tutorial. This guide is organized by scenario — find what you're trying to do and follow the path.

For detailed reference, see:
- [`flow-reference.md`](flow-reference.md) — entry points, exit conditions, parallelism rules, and flow permutations
- [`healthcheck-playbook.md`](healthcheck-playbook.md) — validation procedures for frameworks and initiatives
- [`navigation-map.md`](navigation-map.md) — machine-readable flow graph for AI navigation
- [`review-convergence-loop.md`](review-convergence-loop.md) — the bounded retry pattern when validation fails
- [`elicitation-protocol.md`](elicitation-protocol.md) — techniques to surface gaps and challenge assumptions before generating high-value artifacts
- [`briefing-distillation-spec.md`](tools/briefing-distillation-spec.md) — compress frozen artifacts for downstream use

## AI sherpa mode

Use an AI assistant (Claude Code, etc.) as your guide. AIEOS provides navigation tools to let the AI act as a sherpa — route you to the right starting point, track where you are, and guide you through decisions.

**Navigation tools** (in `docs/tools/`, implemented via `docs/bindings/`):

| Tool | Purpose | Use When |
|------|---------|----------|
| `initiative-router` | Routes you to entry point and preset | Starting a new initiative: "where do I begin?" |
| `position-check` | Reads your ER and artifacts to find where you are | Resuming work, context switch, or lost: "where am I?" |
| `decision-router` | Presents options and recommends a path at forks | Hitting a decision point: "which way do I go?" |
| `handoff-navigator` | Checks exit conditions and routes to next kit | Finishing a kit: "what's next?" |

The sherpa invokes these as you work — you don't call them explicitly. It reads [`navigation-map.md`](navigation-map.md) and guides you through the flow.

**Self-correction:** If the AI goes off track, `position-check` reorients by reading your actual files, not just memory. Every decision table has an escape hatch: "if nothing matches, re-check position."

## Kit map

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

## I need to decide which strategic bets to fund

**Start here:** Strategic Direction Kit (SDK), Layer 1

**The path:**
1. Write a Strategic Bet Record (SBR) for each bet.
2. Validate each SBR (6 hard gates: falsifiable thesis, measurable success signal, defined failure signal, bounded time horizon, stated investment, single owner).
3. Freeze each validated SBR.
4. Write a Portfolio Prioritization Record (PPR) ranking all frozen SBRs.
5. Validate the PPR (5 hard gates: strict rank order, trade-off logic, explicit cut line, capacity check, review trigger).
6. Freeze the PPR.
7. Send above-the-line SBRs to PIK for discovery.

**Where:** `aieos-strategic-direction-kit/docs/playbook.md`

**Use SDK when:** Multiple strategic options compete for limited resources and you need a governed prioritization process. SDK is optional — teams with clear direction jump to PIK.

**Skip SDK when:** Direction is settled, you're improving an existing bet, or your team is small enough to align without formality.

## I want to start a new initiative

**Start here:** Product Intelligence Kit (PIK), Layer 2

**The path:**
1. Complete a Work Classification Record (WCR) to classify the work.
2. Fill out the Discovery Intake Form.
3. Validate against `discovery-intake-validator.md`.
4. Generate: PFD → VH → AR → EL → DPRD.
5. Validate and freeze each before the next.
6. Pass the frozen DPRD to the Engineering Execution Kit.

**Where:** `aieos-product-intelligence-kit/docs/playbook.md`

**Setup:** `aieos-product-intelligence-kit/docs/session-setup.md`

**Not sure if you need discovery?** Use the WCR. New features and exploratory work use PIK. Well-understood bugs and enhancements can skip PIK and enter EEK directly via Path B (Kit Entry Record with justification).

## I need to evaluate sourcing options (Build/Buy/Adopt)

**Start here:** Solution Sourcing Kit (SSK), Layer 3

**Need first:** Frozen Discovery PRD (DPRD) from PIK

**The path:** SOER → VER → SDR

**Use SSK when:** After discovery defines WHAT, before engineering defines HOW. Build isn't the obvious choice — COTS options exist, open-source alternatives are viable, or the team needs to formally evaluate before committing engineers.

**Skip SSK when:** Build is clearly right (no Buy or Adopt options). Document the shortcut in the KER when entering EEK directly from PIK.

**Where:** `aieos-solution-sourcing-kit/docs/playbook.md`

**Coming from PIK:** Read `aieos-solution-sourcing-kit/docs/entry-from-pik.md`

## We are ready to build

**Start here:** Engineering Execution Kit (EEK), Layer 4

**Two entry paths:**
- **Path A** — Frozen Discovery PRD from PIK: place as `docs/sdlc/01-prd.md`, run acceptance check, go.
- **Path B** — Well-understood scope without discovery: write Product Brief, generate PRD, go.

**After PRD is frozen (both paths):**

KER → PRD → ACF → SAD → DCF → TDD → WDD → ORD

**Where:** `aieos-engineering-execution-kit/docs/playbook.md`

**Setup:** `aieos-engineering-execution-kit/docs/session-setup.md`

**From PIK:** Read `aieos-engineering-execution-kit/docs/entry-from-pik.md` first.

**From SSK:** Read `aieos-engineering-execution-kit/docs/entry-from-ssk.md` first. Bring the frozen DPRD and frozen SDR.

## We are ready to release

**Start here:** Release & Exposure Kit (REK), Layer 5

**Need first:** Frozen Operational Readiness Document (ORD) from EEK

**The path:** RER → RCF (if needed) → RP → RR

**Where:** `aieos-release-exposure-kit/docs/playbook.md`

**Setup:** `aieos-release-exposure-kit/docs/session-setup.md`

**From EEK:** Read `aieos-release-exposure-kit/docs/entry-from-eek.md` first.

## We are running a service in production

**Start here:** Reliability & Resilience Kit (RRK), Layer 6

**Need first:** Frozen Release Record (RR §7) from REK

**The path:** SRER → SRP → IR (per incident, as needed) → RHR (periodic review)

**Where:** `aieos-reliability-resilience-kit/docs/playbook.md`

**Setup:** `aieos-reliability-resilience-kit/docs/session-setup.md`

**From REK:** Read `aieos-reliability-resilience-kit/docs/entry-from-rek.md` first.

## We had an incident

**Start here:** Operational Diagnostics Kit (ODK), Layer 8

**Trigger:** SEV1/2 incident (required); lower-severity incidents with high learning value (operator judgment).

**The path:** DCR → INR → PMR → RB (optional, for recurring failure classes)

**Need first:** Active or resolved incident with signals. Frozen SRP from RRK is helpful but not required.

**Where:** `aieos-operational-diagnostics-kit/docs/playbook.md`

**Setup:** `aieos-operational-diagnostics-kit/docs/session-setup.md`

**From RRK after a SEV:** Read `aieos-operational-diagnostics-kit/docs/entry-from-rrk.md` first.

## I want to understand what we have learned

**Start here:** Insight & Evolution Kit (IEK), Layer 7

**Need first:** At least 2 frozen Reliability Health Reports (RHRs) from RRK. Optional: frozen Value Hypothesis (VH) from PIK.

**The path:**
- Per-service: Generate Evolution Signal (ES).
- Portfolio-level: Generate Portfolio Evolution Signal (PES) from 2+ frozen ERs.

**Re-entry signal:** ES §6 re-entry signal says `maintain`, `watch`, or `re-discover` — advising whether to return to PIK. The product owner decides.

**Where:** `aieos-insight-evolution-kit/docs/playbook.md`

**Setup:** `aieos-insight-evolution-kit/docs/session-setup.md`

**From RRK:** Read `aieos-insight-evolution-kit/docs/entry-from-rrk.md` first.

## We need to verify integration quality before releasing

**Start here:** Quality Assurance Kit (QAK), Layer 9

**Need first:** Frozen ORD from EEK

**The path:** QAER → VP → TCR → QGR

**Where:** `aieos-quality-assurance-kit/docs/playbook.md`

**From EEK:** Read `aieos-quality-assurance-kit/docs/entry-from-eek.md` first.

**Use QAK when:** The system has integration points between components, external service dependencies, or cross-component behavior that unit tests can't cover. Skip QAK for simple single-component systems — go straight from ORD to REK.

## We need security governance

**Start here:** Security & Compliance Kit (SCK), Layer 10

**Trigger points:**
- SAD frozen → generate Threat Model (TM).
- Code complete → generate Security Assessment Record (SAR) and Dependency Audit Record (DAR).
- Compliance requirement found → generate Compliance Evidence Record (CER).

**Where:** `aieos-security-compliance-kit/docs/playbook.md`

---

## We need to manage configuration and feature flags

**Start here:** Data & Configuration Kit (DCK), Layer 11

**Trigger points:**
- TDD frozen → generate Configuration Specification (CSPEC) and Data Schema Record (DSR).
- Feature flags created (during REK) → generate Feature Flag Lifecycle Record (FFLR).
- Periodic → review FFLR at each RHR cycle.

**Where:** `aieos-data-configuration-kit/docs/playbook.md`

---

## We need to govern infrastructure decisions

**Start here:** Platform & Infrastructure Kit (PINFK), Layer 12

**Trigger points:**
- Infrastructure decision needed → generate Platform Decision Record (PDR).
- System design phase → generate Infrastructure Specification (ISPEC).
- Project setup → generate Environment Matrix (EM).

**Where:** `aieos-platform-infrastructure-kit/docs/playbook.md`

---

## We need to govern user-facing documentation

**Start here:** Documentation & Knowledge Kit (DKK), Layer 13

**Trigger points:**
- After TDD freeze → generate API Reference Record (ARR).
- After REK release → generate User Documentation Record (UDR).
- After REK release or ODK postmortem → generate Support Knowledge Article (SKA).
- Periodic (aligned with RRK cycles) → generate Documentation Health Review (DHR).

**Where:** `aieos-documentation-knowledge-kit/docs/playbook.md`

**Use DKK when:** Your product has end users relying on docs, API consumers needing reference material, or support teams with knowledge bases. DKK is optional for internal tools with small user counts.

## We want multi-perspective peer review

**Start here:** Peer Review Kit (PRK), Layer 14

**When it activates:** PRK runs when an artifact passes validation but before freeze. It applies specialized review lenses and produces a Peer Review Record (PRR) that must pass before freeze.

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

**Where:** `aieos-peer-review-kit/docs/playbook.md`

**Use PRK when:** You want architecture review board and design review benefits without human reviewers at every stage. Minimum: SAD (architecture) and TDD (technical design).

## I need to govern business process changes

**Start here:** Business Process Kit (BPK), Layer 15

Not every initiative touches business processes. But when it does, shipping the code without governing the process change causes adoption failures, broken workflows, and untrained teams.

**Use BPK when:**
- The initiative introduces new user-facing workflows.
- The initiative changes how an existing process works.
- The initiative removes or automates a manual step.
- An API redesign affects downstream manual work.

**The sequence:**
1. SAD or TDD frozen → generate Process Impact Assessment (PIA).
2. PIA frozen → generate Transition Plan (TP).
3. TP frozen plus evidence → generate Readiness Confirmation (RC).

**Where:** `aieos-business-process-kit/docs/playbook.md`

---

## I want to publish artifacts to external systems

**Tool:** `artifact-publish` in `aieos-governance-foundation/docs/tools/`

**You need:**
- A frozen artifact to publish.
- A binding for your target platform (e.g., `docs/bindings/artifact-publish-confluence.md`).
- An adapter in your project (not in AIEOS).

**Steps:**
1. Review `artifact-publish-spec.md` for preconditions.
2. Create or review a binding for your platform.
3. Build or get an adapter meeting `docs/adapter-conformance-spec.md`.
4. Run the tool.

**Example:** `docs/bindings/artifact-publish-confluence.md` (Confluence).

## I want to sync work items to a tracker

**Tool:** `work-item-sync` in `aieos-governance-foundation/docs/tools/`

**You need:**
- A frozen WDD with enumerable work items.
- A binding for your tracker (e.g., `docs/bindings/work-item-sync-github-issues.md`).
- An adapter in your project.

**Steps:**
1. Review `work-item-sync-spec.md`.
2. Create or review a binding for your tracker.
3. Build or get an adapter meeting `docs/adapter-conformance-spec.md`.
4. Run the tool.

**Example:** `docs/bindings/work-item-sync-github-issues.md` (GitHub Issues).

## I want to export diagrams from artifacts

**Tool:** `diagram-export` in `aieos-governance-foundation/docs/tools/`

**You need:**
- An artifact with Mermaid diagram blocks (e.g., a frozen SAD).
- A target format: draw.io, SVG, or PNG.

**Steps:**
1. Review `diagram-export-spec.md`.
2. Review the binding for your format (e.g., `docs/bindings/diagram-export-drawio.md`).
3. Run: `python -m scripts.diagram_export --input docs/sdlc/05-sad.md --format drawio`.
4. Import the `.drawio` file into your tool (LeanIX, diagrams.net, or VS Code).

**Bindings:**
- `docs/bindings/diagram-export-drawio.md` — draw.io XML for LeanIX.
- `docs/bindings/diagram-export-svg.md` — SVG for docs and web.
- `docs/bindings/diagram-export-mermaid-png.md` — PNG for presentations.

**List diagrams:** `python -m scripts.diagram_export --input docs/sdlc/05-sad.md --list`

## I want to post validation results to my SCM platform

**Tool:** `validation-status` in `aieos-governance-foundation/docs/tools/`

**You need:**
- Validator JSON output (from governance-model.md §5).
- A commit SHA or PR number.
- A binding for your SCM platform (e.g., `docs/bindings/validation-status-github.md`).
- An adapter in your project.

**Steps:**
1. Review `validation-status-spec.md`.
2. Create or review a binding for your SCM platform.
3. Build or get an adapter meeting `docs/adapter-conformance-spec.md`.
4. Run the tool.

**Example:** `docs/bindings/validation-status-github.md` (GitHub Check Runs).

## I want to tag releases on my SCM platform

**Tool:** `release-tag` in `aieos-governance-foundation/docs/tools/`

**You need:**
- A frozen Release Record (RR) from REK.
- A binding for your SCM platform (e.g., `docs/bindings/release-tag-github.md`).
- An adapter in your project.

**Steps:**
1. Review `release-tag-spec.md`.
2. Create or review a binding for your SCM platform.
3. Build or get an adapter meeting `docs/adapter-conformance-spec.md`.
4. Run the tool.

**Example:** `docs/bindings/release-tag-github.md` (GitHub Releases).

## I don't know where I am

Use `initiative-state-view.md` to see which artifacts exist, their freeze status, and which layer you're in.

Steps:
1. Open `aieos-governance-foundation/docs/initiative-state-view.md`
2. Copy the blank template
3. Fill in which artifacts exist and their status
4. The first row with status `⬜ Not Started` or `🔄 In Progress` shows where you are

## Engagement records

For every initiative, create and maintain an Engagement Record (ER) in your project at `docs/engagement/er-{initiative}.md`. The ER is the cross-layer memory — artifact IDs, decisions, and outcomes.

ER spec: `aieos-governance-foundation/docs/engagement-record-spec.md`

## Not sure which path applies?

Use the initiative presets guide: `aieos-governance-foundation/docs/initiative-presets.md`

Five pre-defined initiative types map your situation to a complete artifact routing path.
