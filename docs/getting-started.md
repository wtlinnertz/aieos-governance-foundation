# Getting Started with AIEOS

This guide is organized by what you are trying to accomplish. Find your scenario and follow the path.

---

## Kit Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Layer 2: Product Intelligence Kit (PIK)                                  │
│  WCR → Discovery Intake → PFD → VH → AR → EL → DPRD                     │
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
├──────────────────────────────────────────────────────────────────────────┤
│  Layer 8: Operational Diagnostics Kit (ODK)          ← triggered by SEV  │
│  DCR → INR → PMR → RB (optional)                                         │
└──────────────────────────────────────────────────────────────────────────┘
                    ↑ ES re-discover signal feeds back to PIK ↑
```

Layers 1 (Strategic Direction) and 3 (Flow Control) are planned but not yet built.

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
