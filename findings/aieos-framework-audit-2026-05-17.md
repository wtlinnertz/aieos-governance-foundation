# AIEOS Framework — Full Execution Path Audit

**Date:** 2026-05-17  
**Auditor:** Claude Sonnet 4.6  
**Scope:** All 15 layers, 40 repos, complete artifact dependency graph  
**Source files read:** 80+ docs across governance-foundation, all 15 kit repos, 4 infra repos  
**Governance Model version audited:** 1.6  

---

## Executive Summary

The AIEOS framework has a sound and well-reasoned architecture. The core pipeline (Layers 1–8) is logically consistent and the escalation model is solid. The cross-cutting kits (Layers 9–15) are structurally coherent but have integration coupling ambiguities that could cause operational confusion.

**25 issues found** across five categories:

| Severity | Count | Categories |
|----------|-------|-----------|
| Critical | 3 | Flow breaks, undefined escalation path, direct contradiction |
| High | 8 | Documentation inconsistencies that cause wrong decisions |
| Medium | 9 | Structural gaps, enforcement gaps, infrastructure stubs |
| Low | 5 | Meta-governance, polish, future-state items |
| Info | 0 | — |

---

## Section 1: Complete Execution Path Tree

### Entry Points (4 valid)

```
[1] New work (unclear scope)    → PIK Layer 2   → WCR → full discovery
[2] Known enhancement           → EEK Layer 4   → Path B KER + Product Brief
[3] SEV1/2 production incident  → ODK Layer 8   → DCR within 2h (automatic)
[4] Technology decision         → PINFK Layer 12 → PDR (per decision)
```

### Main Pipeline (Layers 1–7, with branches)

```
[Optional] SDK Layer 1
  ├── [Optional] Roadmap Phase: CLA → PCR → TIR
  └── [Required] Bet Phase:    SBR(s) → PPR
        └── above-the-line SBRs ──────────────────────────────► PIK Layer 2

PIK Layer 2  (or direct entry from IEK re-discover / ad-hoc)
  WCR → Discovery Intake (not frozen) → PFD → VH → AR → EL
  EL decision:
    ├── proceed  → DPRD ──────────────────────────────────────► SSK Layer 3 [Optional]
    │                 └── (if SSK skipped) ──────────────────► EEK Layer 4
    ├── pivot    → new PFD (restart within PIK)
    └── pause    → initiative suspended (no DPRD)

[Optional] SSK Layer 3
  SOER → VER → SDR
  SDR + DPRD ────────────────────────────────────────────────► EEK Layer 4

EEK Layer 4  (ALWAYS REQUIRED)
  KER (entry gate, human)
    Path A: DPRD placed as PRD (from PIK / PIK+SSK)
    Path B: Product Brief → PRD generated
  [Both merge at frozen PRD]
  PRD → ACF → SAD → DCF → TDD → WDD → Execution → ORD
  
  Cross-cutting triggers DURING EEK:
    SAD frozen  ──────────────────────────────────────────────► SCK Layer 10: TM
    TDD frozen  ──────────────────────────────────────────────► DCK Layer 11: CSPEC + DSR
    TDD frozen  ──────────────────────────────────────────────► DKK Layer 13: ARR
    SAD/TDD frozen (if process impact) ──────────────────────► BPK Layer 15: PIA → TP → RC
    Any artifact validated (not yet frozen) ─────────────────► PRK Layer 14: PRR (per review point)
    Technology decisions ─────────────────────────────────────► PINFK Layer 12: PDR/ISPEC/EM/SMR
  
  ORD ──────────────────────────────────────────────────────► QAK Layer 9 [Optional]
  ORD ──────────────────────────────────────────────────────► REK Layer 5

[Optional] QAK Layer 9  (between EEK and REK)
  QAER (entry gate, human) → VP → TCR(s) → QGR
  QGR PASS/CONDITIONAL ────────────────────────────────────► REK Layer 5
  QGR FAIL ────────────────────────────────────────────────► EEK (address defects, then restart QAK)

Pre-REK clearances feeding in:
  SCK Layer 10: SAR + DAR (security clearance)
  BPK Layer 15: RC readiness declaration
  DCK Layer 11: CSPEC validation criteria

REK Layer 5  (ALWAYS REQUIRED for production)
  RER (entry gate, human) → RCF → RSA → RP → Release Execution → RR
  
  Cross-cutting during REK:
    Feature flags created ────────────────────────────────────► DCK Layer 11: FFLR
    RP validated ─────────────────────────────────────────────► PRK Layer 14: Operational Readiness PRR
  
  RR §7 ──────────────────────────────────────────────────► RRK Layer 6
  RR frozen ──────────────────────────────────────────────► DKK Layer 13: UDR + ARR update + SKA
  
  Escalation from REK:
    Rollback, code defect  → EEK (Trigger 3)
    Rollback, wrong feature → PIK (Trigger 4)

RRK Layer 6  (required in production)
  SRER (entry gate, human) → SRP → [Active Operation] → IR(s) → RHR(s)
  
  RHR §5 ──────────────────────────────────────────────────► IEK Layer 7 (when ≥2 RHRs frozen)
  SEV1/2 IR ───────────────────────────────────────────────► ODK Layer 8 (reactive, automatic)
  
  Escalation from RRK:
    SEV1/2 code defect (IR)           → EEK (Trigger 1)
    3+ consecutive RHRs, same cause   → PIK (Trigger 2)

IEK Layer 7  (required when ≥2 RHRs exist)
  ES (≥2 frozen RHRs as input; optional frozen VH)
    ├── maintain   → no cross-kit action
    ├── watch      → no cross-kit action; elevate monitoring
    └── re-discover → PIK (new WCR → fresh discovery)
                   → SDK (new SBR if new strategic question)
  PES [Optional] (≥2 frozen ERs) → prompt/spec improvement proposals

ODK Layer 8  (reactive, parallel to IEK)
  DCR (entry gate, human, within 2h) → INR → PMR → [Optional] RB
  
  PMR cross-kit outputs:
    → RRK: referenced in next RHR §Incident Summary
    → EEK: code defect corrective actions (Trigger 1 path)
    → PIK: recurring pattern 3+ occurrences (Trigger 2 path)
    → IEK/ER: §8 update
    → DKK Layer 13: SKA triggered
    → PRK Layer 14: Incident Review PRR
  
  PRK Layer 14 review points:
    DPRD validated  → Concept Review
    SAD validated   → Architecture Review
    TDD validated   → Technical Design Review
    WDD validated   → Implementation Readiness Review
    ORD validated   → Code Review
    QGR validated   → Integration Review
    RP validated    → Operational Readiness Review
    RHR validated   → Post-Deployment Review
    PMR validated   → Incident Review

Feedback loops (10 total):
  1.  IEK ES re-discover → PIK (primary learning loop)
  2.  RRK SEV1/2 IR → ODK (depth loop)
  3.  ODK PMR → RRK next RHR (corrective action loop)
  4.  ODK PMR → EEK (defect correction loop)
  5.  ODK PMR → PIK (pattern escalation loop, 3+ occurrences)
  6.  IEK PES → spec/prompt files (quality improvement loop)
  7.  SCK TM → RRK SRP security monitoring (security monitoring loop)
  8.  DCK FFLR → RRK (stale flag loop)
  9.  DKK DHR → IEK PES (documentation health loop)
  10. PRK PRR → producing kit (pre-freeze findings loop)
```

---

## Section 2: Issues Found

### CRITICAL — Fix Before Next Initiative

---

**ISSUE-01: Escalation Trigger 5 referenced but never defined**

*Category:* Flow break — undefined exit path  
*Severity:* Critical  
*Location:* governance-model.md §Decision Outcome Taxonomy, flow-reference.md §10  

The Decision Outcome Taxonomy lists "Rollback" as a formal outcome and maps it to "Escalation trigger 5 (REK/RRK)." The escalation-protocols.md defines exactly 4 triggers (Trigger 1–4). Trigger 5 does not exist anywhere in the framework. Any downstream tooling, console, or pipeline runner that encounters a rollback scenario and tries to route via the stated escalation table will find a dead reference.

*Evidence:*
```
governance-model.md §15:
  "Rollback — Runtime SLO violation; execute rollback procedure
   Maps to: Escalation trigger 5 (REK/RRK)"

escalation-protocols.md: Defines Trigger 1, 2, 3, 4 only.
```

The rollback path IS documented at the REK level (Trigger 3 = code defect, Trigger 4 = wrong feature). But the taxonomy conflates REK rollback decisions with a "Trigger 5" that doesn't exist. Needs either a Trigger 5 definition or correction of the taxonomy mapping.

---

**ISSUE-02: QAK optional/required contradiction**

*Category:* Direct contradiction between docs  
*Severity:* Critical  
*Location:* governance-model.md §17 vs. aieos-quality-assurance-kit README  

The governance model (Section 17) classifies QAK as "Optional — adopt if integration points, external dependencies, or cross-component behavior exist." The QAK README states "REQUIRED once the ORD is frozen and the initiative is proceeding to release. No stated opt-out path."

These are opposite claims. Any team reading the governance model will believe they can skip QAK. Any team reading the QAK README will believe they cannot. Operators cannot know which is authoritative.

*Impact:* Teams skip QAK legitimately (per governance model) but QAK itself considers this a violation.

---

**ISSUE-03: SCK ordering constraint for compliance initiatives not enforced at artifact level**

*Category:* Flow logic gap — constraint stated in preset but not in specs  
*Severity:* Critical  
*Location:* initiative-presets.md Preset 3 vs. QAK VP spec  

Preset 3 (Compliance/Regulatory) states: "SCK must complete (TM → SAR → CER → DAR all frozen) BEFORE QAK VP." This is a hard ordering constraint. However, the QAK VP artifact spec lists `frozen QAER + SAD + TDD + ACF` as its entry gates. It does NOT list frozen SCK artifacts (TM, SAR, CER, DAR) as entry gates.

This means the QAK VP validator will PASS a compliance initiative even if none of the SCK artifacts are frozen. The enforcement exists only in the prose description of Preset 3 — not in the machinery. A team following the QAK playbook alone will produce an invalid VP for compliance initiatives.

---

### HIGH — Fix Within Current Milestone

---

**ISSUE-04: Layer count inconsistency — 15 vs 16**

*Category:* Documentation error  
*Severity:* High  
*Location:* aieos-governance-foundation/README.md §Kit Registry  

The README §Kit Registry footer reads: "All 16 layer kits (including the Governance Foundation) are built and operational."

The governance model defines exactly 15 layers. The Governance Foundation is the authority repo, not a layer kit. It has no layer number, no artifact types, no kit spec/template/prompt/validator files. Calling it a "layer kit" and counting it as Layer 16 is wrong and will confuse anyone mapping kits to layers.

The sentence should read: "All 15 kit layers are built and operational. The Governance Foundation is the canonical authority for all kits."

---

**ISSUE-05: EEK repo name mismatch throughout the framework**

*Category:* Documentation error  
*Severity:* High  
*Location:* governance-model.md, aieos-schema, flow-reference.md vs. actual repo  

Every governance document refers to the Layer 4 kit as `aieos-engineering-execution-kit`. The actual repo on disk and on GitHub is `aieos-engineering-execution` (without `-kit`). This affects:
- governance-model.md Kit Registry table
- aieos-schema schemas (kit path references)
- flow-reference.md upstream/downstream references
- docs/layer-model.md
- README.md §Kit Registry

Any automated tooling that constructs repo paths from kit names (pipeline runner, console, schema sync) will fail to resolve the EEK repo.

---

**ISSUE-06: PIK WCR governance status inconsistency**

*Category:* Documentation error  
*Severity:* High  
*Location:* aieos-product-intelligence-kit README vs CLAUDE.md, entry-from-iek.md  

The PIK README describes WCR as supported by "Two utility prompts" — language that implies it is a utility tool, not a governed artifact. The CLAUDE.md and `entry-from-iek.md` are explicit: WCR is a governed artifact with spec, template, prompt, and validator. It is Step 0 of PIK and required.

The README is the first document any new user reads. If they take it at face value, they will skip WCR, producing no routing audit trail, and potentially enter the wrong kit path with no accountability record.

---

**ISSUE-07: REK artifact count wrong in README header**

*Category:* Documentation error  
*Severity:* High  
*Location:* aieos-release-exposure-kit README  

README header states "3 governed artifact types." The actual count is 5: RER (entry gate), RCF, RSA, RP, RR. The presence of RSA is the likely culprit — it may have been added after the README header was written and the count was not updated. RSA is the artifact that consumes QGR, SAR, DAR, and CER as inputs, so its absence from the count is particularly impactful for cross-cutting kit integration.

---

**ISSUE-08: BPK RC → REK coupling is "informs" not "gates"**

*Category:* Logic gap — soft coupling where hard gate expected  
*Severity:* High  
*Location:* aieos-business-process-kit docs, REK RER spec  

BPK RC (Readiness Confirmation) is documented as feeding into the REK release entry decision. The coupling language is "RC readiness declaration informs REK release entry decision" and "TP cutover schedule aligns with REK Release Plan timing." Neither is a hard gate in the REK RER or RP spec.

This means: a team can get a frozen RER and complete a RP without BPK RC being frozen, even when BPK was triggered. The REK validator has no check for frozen RC. BPK is effectively ignorable at release time.

Either: add RC frozen as a conditional entry gate to REK RER (when BPK was adopted), or explicitly document that RC is advisory only and the release owner accepts that risk.

---

**ISSUE-09: PRK lens table discrepancy between playbook and CLAUDE.md**

*Category:* Documentation inconsistency  
*Severity:* High  
*Location:* aieos-peer-review-kit playbook.md vs CLAUDE.md vs entry-from-eek.md  

Three documents define which lenses are required vs optional at each review point. They disagree:

- Architecture Review (SAD): CLAUDE.md lists `resilience` as required. The playbook table omits it. `entry-from-eek.md` lists a shorter required set than both.
- Operational Readiness (RP): CLAUDE.md lists `observability` as required. The playbook table omits it.

When a PRK operator follows the playbook (the most likely runtime reference), they will skip required lenses that CLAUDE.md mandates. A PRR produced without the full required lens set is invalid but will still PASS the PRR validator (which doesn't check lens completeness against the authoritative table).

---

**ISSUE-10: DCF entry gate is loose — could precede SAD**

*Category:* Logic gap — freeze-before-promote violation risk  
*Severity:* High  
*Location:* EEK artifact flow, DCF spec  

The DCF (Design Context File) entry gate is documented as: "Design Context intake form (human-authored). No strict artifact precondition for DCF itself." DCF is human-authored and requires no frozen upstream AIEOS artifact.

In the flow, DCF is positioned after SAD. But because DCF has no stated dependency on frozen SAD (or frozen PRD), an operator using the console or pipeline runner could author and freeze DCF before SAD is frozen. TDD then requires frozen SAD + DCF — so TDD generation would not be blocked. But if DCF is authored before SAD, it lacks the system context that SAD provides. The resulting TDD would be architecturally unconstrained.

Fix: DCF spec entry gate should explicitly require either frozen SAD or frozen PRD at minimum.

---

**ISSUE-11: SDK Layer 1 described as "not yet in standard flow"**

*Category:* Unclear status  
*Severity:* High  
*Location:* governance-model.md Layer 1 description, flow-reference.md  

The governance foundation extraction notes SDK Layer 1 is "Category: Pipeline (optional upstream entry point; not yet in standard flow)." This is ambiguous. Is Layer 1 aspirational? Partially built but not wired? The kit repo exists and has all 5 artifacts with specs. But if it is not in the standard flow, what does that mean for operators? They cannot tell whether they should or should not wire Layer 1 into initiative pipelines.

Needs a clear status statement: either "optional — may be skipped when no portfolio-level prioritization exists" (clean) or a proper milestone tag for when it enters standard flow.

---

### MEDIUM — Fix Within Next Milestone

---

**ISSUE-12: PINFK timing gap — no EEK hard gate forces PINFK**

*Category:* Structural enforcement gap  
*Severity:* Medium  
*Location:* aieos-platform-infrastructure-kit, EEK ACF spec  

PINFK is positioned as "cross-cutting" but its artifacts (PDR, ISPEC, EM, SMR) must precede EEK because EEK's ACF consumes PINFK PDRs and ISPEC. If PINFK artifacts do not exist when EEK starts, infrastructure decisions become implicit assumptions inside ACF — invisible to governance.

No hard gate in EEK KER or ACF spec requires frozen PINFK artifacts. The EEK playbook mentions PINFK as an input but does not block on its absence. A team can complete the full EEK flow with zero PINFK artifacts and every validator will PASS.

Fix: Add a conditional check in the ACF or KER spec: "If PINFK has been adopted for this initiative, PDR and ISPEC must be frozen before ACF generation."

---

**ISSUE-13: DCK FFLR upstream kit is REK, not EEK**

*Category:* Logic gap — cross-cutting kit trigger misalignment  
*Severity:* Medium  
*Location:* aieos-data-configuration-kit, entry-from-eek.md vs entry-from-rek.md  

DCK is introduced as triggered during EEK (CSPEC after TDD, DSR after TDD). The FFLR (Feature Flag Lifecycle Record) is different: it is triggered when feature flags are created during REK execution, not during EEK. The DCK `entry-from-eek.md` doc explicitly warns "do not create the FFLR yet" during EEK.

This creates two classes of DCK adoption:
- Class 1 (CSPEC + DSR): EEK-triggered, parallel with EEK continuation
- Class 2 (FFLR): REK-triggered, parallel with REK execution

Pipeline runner and console tooling must handle these two trigger classes differently. Nothing in the DCK README or kit-structure makes this split explicit. It reads as one kit with one trigger, but it is actually one kit with two distinct trigger points from two different upstream kits.

---

**ISSUE-14: DKK DHR trigger is underspecified**

*Category:* Governance gap  
*Severity:* Medium  
*Location:* aieos-documentation-knowledge-kit DHR spec  

DHR (Documentation Health Review) is described as triggered "periodically or after major release, aligned with RRK health review cadence." No spec defines:
- Who triggers the DHR
- What constitutes "periodic" (monthly? quarterly? after 3 RHRs?)
- Whether the alignment to RHR cadence is mandatory or advisory
- What happens if DHR is never triggered

Without a defined trigger owner and cadence, DHR will never happen in practice. Every other artifact in AIEOS has an explicit trigger event or upstream artifact requirement. DHR is the only one with a vague "periodic" trigger.

---

**ISSUE-15: SSK skip justification has no validator enforcement in EEK KER**

*Category:* Enforcement gap  
*Severity:* Medium  
*Location:* EEK KER spec, SSK docs  

The framework requires that if SSK is skipped, the EEK KER must document the justification. The KER spec does not list "SSK skip justification" as a hard gate. The KER validator passes without it. The enforcement exists only in prose guidance. Teams that read only the KER template will not know this requirement exists, and the validator will not catch the omission.

---

**ISSUE-16: aieos-schema missing PRK lens tool schemas (13 of 14 PRK schemas absent)**

*Category:* Coverage gap  
*Severity:* Medium  
*Location:* aieos-schema, aieos-peer-review-kit  

The schema repo has 1 PRK schema (PRR, 5 gates). It has no schemas for the 13 lens tools (review-security, review-reliability, review-performance, review-cost, review-operability, review-maintainability, review-compliance, review-devex, review-business-value, review-accessibility, review-observability, review-resilience, review-adversarial). Each lens tool is a governed artifact with 4 files (spec, template, prompt, validator) and its own hard gates.

The aieos-schema README claims "68 schemas total across all 15 kits; 391 hard gates total." This count excludes the 13 lens tool schemas. The true schema count (if lenses are included) should be 81, and the true gate count would be higher.

---

**ISSUE-17: aieos-pipeline-runner is scaffolding only — M3 not started**

*Category:* Infrastructure gap  
*Severity:* Medium  
*Location:* aieos-pipeline-runner  

The pipeline runner (the tool that actually executes CI/CD specs) has stub implementations for all three validators (spec, plan, run). The only supported adapter mode is `--use-mock-adapters`. Real adapter wiring requires harness registry with attested adapters. Artifact-store refs are deferred to v1.1.

This means: the spec-driven CI/CD path (the primary automation value proposition of AIEOS beyond document governance) is not operational. Any documentation or marketing material that implies CI/CD execution is working would be inaccurate.

---

**ISSUE-18: aieos-console covers only Layers 2, 4, 5 — Layers 9–15 have no wizard flows**

*Category:* Infrastructure gap  
*Severity:* Medium  
*Location:* aieos-console  

The console wizard covers PIK (Layer 2), EEK (Layer 4), and REK (Layer 5). Layer 6 (RRK) is started but incomplete. Layers 9–15 (all cross-cutting kits) have no wizard flow definitions. Users of QAK, SCK, DCK, DKK, PRK, BPK, PINFK must either run them manually or wait for future console extensions.

This is documented internally but not surfaced prominently in the console README. Users will discover the gap when they try to run a cross-cutting kit.

---

**ISSUE-19: EEK "DKR" artifact is orphaned / unresolved**

*Category:* Orphaned artifact  
*Severity:* Medium  
*Location:* aieos-engineering-execution CLAUDE.md, docs/specs/  

The EEK CLAUDE.md references a `DKR` artifact (docs/specs/dkr-spec.md) and a `bat-escalation-template.md`. DKR does not appear anywhere in the main EEK artifact flow documentation (README, playbook, entry-from-*.md files). It is not in the aieos-schema schema registry. It is not referenced by any upstream or downstream artifact entry gate.

DKR is either:
- An artifact that was planned, specced, then removed from the flow (should be deleted or archived)
- An artifact that was added to the spec directory but never wired into the flow (should be wired or removed)
- An artifact for a future milestone (should be marked with milestone tag and excluded from current schema count)

Its presence in the CLAUDE.md creates confusion about what artifacts actually live in EEK.

---

**ISSUE-20: IEK has no formal entry gate artifact**

*Category:* Structural gap  
*Severity:* Medium  
*Location:* aieos-insight-evolution-kit, governance-model.md  

Every kit entry transition that the governance model specifies has a human-authored entry gate artifact (KER for EEK, RER for REK, SRER for RRK, QAER for QAK, DCR for ODK). IEK has no entry gate artifact. ES §1 confirms its own inputs are frozen as a self-check, but there is no separate record that a human reviewed the trigger conditions and authorized the IEK engagement.

This creates an asymmetry: IEK can be triggered autonomously (by querying RHR count and running the ES prompt) without any human authorization step. Every other kit transition requires explicit human gate passage.

---

### LOW — Address in Governance Model v1.7

---

**ISSUE-21: Retroactive governance flag not implemented in ER template**

*Category:* Meta-governance gap  
*Severity:* Low  
*Location:* aieos-agent-harness Engagement Record FINDING-1  

The aieos-agent-harness ER documents FINDING-1: "Retroactive governance produces different artifact character; recommends 'Retroactive' flag in ER Document Control." This flag does not exist in the current Engagement Record spec or template. The ER Document Control section has no field for retroactive status. Any future initiative governed retroactively has no way to formally mark itself as such, making it appear identical to prospective governance in the ER registry.

---

**ISSUE-22: IEK PES bootstrap problem not documented prominently**

*Category:* Documentation gap  
*Severity:* Low  
*Location:* aieos-insight-evolution-kit PES spec  

PES (Portfolio Evolution Signal) requires ≥2 frozen Engagement Records from ≥2 separate initiatives. The first and second AIEOS-governed initiative cannot produce a PES. This means the prompt quality improvement loop (the mechanism by which AIEOS prompts get better over time) cannot function until a team has completed at least two full initiative cycles.

This is a by-design limitation but is not documented prominently in the IEK README, getting-started.md, or initiative presets. New adopters will discover it only when they try to run PES and hit the gate.

---

**ISSUE-23: aieos-agent-harness initiative never completed REK/RRK — meta-governance gap**

*Category:* Meta-governance  
*Severity:* Low  
*Location:* aieos-agent-harness Engagement Record  

The agent harness ER explicitly documents "REK/RRK not engaged." The harness itself was never put through a release process (Layer 5) or into operational monitoring (Layer 6) using its own framework. This means the harness, which enforces AIEOS governance for other initiatives, has not been governed by AIEOS itself beyond EEK.

This is not a bug in the framework, but it is a trust signal gap. The harness is the primary enforcement layer for AIEOS invariants. Its own governance gap is worth documenting as a known exemption with rationale (retroactive governance challenges, bootstrapping constraint).

---

**ISSUE-24: ER cross-kit section maintenance has no enforcement mechanism**

*Category:* Governance gap  
*Severity:* Low  
*Location:* Engagement Record spec  

The Engagement Record (ER) is the cross-layer index. Each kit maintains its own section in the ER (PIK updates §1–§5, EEK updates §6–§10, etc.). There is no stated enforcement mechanism — no validator, no checklist, no tooling — that ensures a kit's ER section is updated when that kit's engagement completes. An ER could have a frozen PIK section with an incomplete EEK section, making the ER an unreliable index.

---

**ISSUE-25: PRK adversarial lens minimum findings requirement is unique and undocumented at framework level**

*Category:* Documentation gap  
*Severity:* Low  
*Location:* aieos-peer-review-kit, adversarial lens spec  

The adversarial lens has a unique hard gate: a minimum findings requirement (it must surface at least N adversarial findings to PASS). This inverts the usual PASS/FAIL logic (normally, finding nothing blocking = PASS). This exception is documented inside the lens spec but is not called out at the PRK or framework level. An operator who does not read the adversarial lens spec will not understand why a review with no findings can FAIL. This is likely to cause confusion and is worth surfacing in the PRK README and the governance model's validator output format section.

---

## Section 3: Fix Plan

### Phase 1 — Critical Fixes (before next initiative starts)

**FIX-01: Define Escalation Trigger 5 or correct taxonomy reference**

Target file: `governance-model.md` §15, `escalation-protocols.md`

Two options:
- Option A (preferred): Define Trigger 5 formally in escalation-protocols.md as the production SLO violation / rollback path triggered from REK (after release) or RRK (during operation). Criteria: RR declares rollback AND SLO breach confirmed (distinct from Trigger 3 which is code defect, distinct from Trigger 4 which is wrong feature — Trigger 5 would be the operational SLO rollback triggered by RRK burn rate alert hitting a release not yet absorbed by RRK).
- Option B: Correct the taxonomy table to map "Rollback" to "Trigger 3 or 4" (whichever applies based on root cause), removing the Trigger 5 reference entirely.

Files to change:
- `aieos-governance-foundation/governance-model.md` §15
- `aieos-governance-foundation/docs/escalation-protocols.md` (if Option A)
- `aieos-governance-foundation/docs/flow-reference.md` §8

---

**FIX-02: Resolve QAK optional vs required contradiction**

Target files: `governance-model.md` §17, `aieos-quality-assurance-kit/README.md`

Decision needed: Is QAK optional or required when an initiative has integration points?

Recommendation: QAK is conditionally required (not unconditionally required, not pure optional). The governance model §17 language should be:
"Optional for simple single-service changes with no external integrations. Conditionally required when the initiative has integration points, external dependencies, or cross-component test scope. When adopted, no opt-out path after QAER is frozen."

The QAK README should align: replace "REQUIRED once ORD is frozen" with the conditional framing above.

Files to change:
- `aieos-governance-foundation/governance-model.md` §17
- `aieos-quality-assurance-kit/README.md`
- `aieos-governance-foundation/docs/layer-model.md` (Layer 9 description)

---

**FIX-03: Add SCK ordering constraint to QAK VP entry gate**

Target file: `aieos-quality-assurance-kit/docs/specs/vp-spec.md`

Add a conditional entry gate to the VP spec:
"If the initiative is compliance/regulatory (CER adopted): frozen TM, frozen SAR, frozen CER, and frozen DAR from SCK must all be present and referenced before VP generation proceeds."

Also add to QAK CLAUDE.md and QAK playbook, noting the Preset 3 ordering.

Files to change:
- `aieos-quality-assurance-kit/docs/specs/vp-spec.md`
- `aieos-quality-assurance-kit/docs/artifacts/vp-template.md` (add SCK input section)
- `aieos-quality-assurance-kit/CLAUDE.md`

---

### Phase 2 — High Priority (within current milestone)

**FIX-04:** Correct layer count in governance-foundation README: "All 16 layer kits" → "All 15 layer kits" and clarify the Governance Foundation role.
- File: `aieos-governance-foundation/README.md` §Kit Registry footer

**FIX-05:** Correct EEK repo name everywhere it is referenced as `aieos-engineering-execution-kit`:
- `aieos-governance-foundation/governance-model.md` Kit Registry table
- `aieos-governance-foundation/docs/layer-model.md`
- `aieos-governance-foundation/docs/flow-reference.md`
- `aieos-governance-foundation/README.md`
- All `entry-from-eek.md` headers in every kit
- `aieos-schema` README schema count table

**FIX-06:** Correct PIK README WCR description. Replace utility-tool language with governed artifact language. Add spec/template/prompt/validator references.
- File: `aieos-product-intelligence-kit/README.md`

**FIX-07:** Correct REK README artifact count: "3 governed artifact types" → "5 artifact types (RER entry gate + RCF + RSA + RP + RR)."
- File: `aieos-release-exposure-kit/README.md`

**FIX-08:** Resolve BPK RC → REK coupling. Add conditional hard gate to REK RER spec:
"If BPK was adopted for this initiative: frozen RC required before RER can be frozen."
- Files: `aieos-release-exposure-kit/docs/specs/rer-spec.md`, `aieos-business-process-kit/README.md`

**FIX-09:** Reconcile PRK lens tables. Create a single authoritative table in PRK CLAUDE.md and update playbook and entry-from-eek.md to reference it. Specifically:
- Architecture Review: add `resilience` to required column in playbook
- Operational Readiness: add `observability` to required column in playbook
- `entry-from-eek.md`: align with CLAUDE.md (currently too short)
- Files: `aieos-peer-review-kit/CLAUDE.md`, `aieos-peer-review-kit/docs/playbook.md`, `aieos-peer-review-kit/docs/entry-from-eek.md`

**FIX-10:** Tighten DCF entry gate in spec to require frozen PRD (or frozen SAD if available) as an upstream precondition. This aligns with the flow order and prevents pre-SAD DCF authoring.
- File: `aieos-engineering-execution/docs/specs/dcf-spec.md`

**FIX-11:** Clarify SDK Layer 1 status. Add a clear status statement to the SDK README and governance-model.md:
"Layer 1 is optional for all initiatives. Engage when portfolio-level prioritization across multiple competing bets is needed. May be skipped with justification in the PIK Discovery Intake or EEK KER."
Remove the "not yet in standard flow" language which implies it is not production-ready.
- Files: `aieos-strategic-direction-kit/README.md`, `aieos-governance-foundation/governance-model.md`

---

### Phase 3 — Medium Priority (next milestone)

**FIX-12:** Add conditional PINFK check to EEK ACF spec entry gate.
- File: `aieos-engineering-execution/docs/specs/acf-spec.md`

**FIX-13:** DCK: split the README and CLAUDE.md to clearly document two distinct trigger classes (EEK-triggered: CSPEC/DSR; REK-triggered: FFLR). Add a trigger summary table to the README.
- Files: `aieos-data-configuration-kit/README.md`, `aieos-data-configuration-kit/CLAUDE.md`

**FIX-14:** DHR: add explicit trigger definition to DHR spec — recommended cadence (quarterly, or aligned with 3rd RHR cycle), responsible owner (documentation owner named in ER), and what constitutes the trigger event.
- File: `aieos-documentation-knowledge-kit/docs/specs/dhr-spec.md`

**FIX-15:** Add SSK skip justification as a hard gate in EEK KER spec.
- File: `aieos-engineering-execution/docs/specs/ker-spec.md`

**FIX-16:** Add 13 lens tool schemas to aieos-schema. Update README schema count from 68 → 81 and gate count accordingly.
- Files: `aieos-schema/schema/` (13 new .yaml files), `aieos-schema/README.md`

**FIX-17:** Pipeline runner: milestone tracking. Add a clear M3 status notice to aieos-pipeline-runner README header. Scope is understood; this is not a surprise gap, just needs surfacing.
- File: `aieos-pipeline-runner/README.md`

**FIX-18:** Console: add "cross-cutting kit support" as a documented future milestone in the console README. List which kits are not yet wired.
- File: `aieos-console/README.md`

**FIX-19:** Resolve DKR artifact in EEK. Determine status (planned, draft, removed). If removed: delete the spec file and remove from CLAUDE.md. If planned: add a milestone tag and exclude from current schema/artifact counts.
- Files: `aieos-engineering-execution/CLAUDE.md`, `aieos-engineering-execution/docs/specs/dkr-spec.md`

**FIX-20:** Add an IEK entry gate artifact (lightweight human-authored record, no AI prompt) OR document the intentional exception with rationale in the governance model. If intentional exception: add a note to the governance model's entry gate rules section explaining why IEK is exempt.
- Files: `aieos-governance-foundation/governance-model.md`, `aieos-insight-evolution-kit/README.md`

---

### Phase 4 — Low Priority (Governance Model v1.7)

**FIX-21:** Add "Retroactive" flag field to Engagement Record Document Control section in ER spec and template.

**FIX-22:** Add a prominent note to IEK README and PES spec about the bootstrap requirement (≥2 initiatives required). Include in getting-started.md onboarding guidance.

**FIX-23:** Create a formal exemption record for agent-harness (REK/RRK declined). Document bootstrapping constraint explicitly in AIEOS onboarding guidance so future tooling repos know the pattern.

**FIX-24:** Add an ER completeness checklist to the governance model or ER spec. Each kit section should have a "Section complete: [yes/no]" field that must be marked when the kit engagement closes.

**FIX-25:** Add a PRK-level note about the adversarial lens FAIL-on-no-findings behavior. Update PRK README "Lens overview" section and governance-model.md §Validator Output Format.

---

## Section 4: Summary Table

| ID | Severity | Location | Fix Effort | Phase |
|----|----------|----------|------------|-------|
| ISSUE-01 | Critical | governance-model.md §15, escalation-protocols.md | Medium | 1 |
| ISSUE-02 | Critical | governance-model.md §17, QAK README | Small | 1 |
| ISSUE-03 | Critical | QAK VP spec, initiative-presets.md | Medium | 1 |
| ISSUE-04 | High | governance-foundation README | Tiny | 2 |
| ISSUE-05 | High | 6+ docs across framework | Medium | 2 |
| ISSUE-06 | High | PIK README | Small | 2 |
| ISSUE-07 | High | REK README | Tiny | 2 |
| ISSUE-08 | High | RER spec, BPK README | Small | 2 |
| ISSUE-09 | High | PRK CLAUDE.md, playbook, entry-from-eek | Small | 2 |
| ISSUE-10 | High | EEK DCF spec | Small | 2 |
| ISSUE-11 | High | SDK README, governance-model.md | Small | 2 |
| ISSUE-12 | Medium | EEK ACF spec | Small | 3 |
| ISSUE-13 | Medium | DCK README, CLAUDE.md | Small | 3 |
| ISSUE-14 | Medium | DKK DHR spec | Small | 3 |
| ISSUE-15 | Medium | EEK KER spec | Small | 3 |
| ISSUE-16 | Medium | aieos-schema (13 new schemas) | Large | 3 |
| ISSUE-17 | Medium | pipeline-runner README | Tiny | 3 |
| ISSUE-18 | Medium | console README | Tiny | 3 |
| ISSUE-19 | Medium | EEK CLAUDE.md, dkr-spec.md | Small | 3 |
| ISSUE-20 | Medium | IEK, governance-model.md | Medium | 3 |
| ISSUE-21 | Low | ER spec + template | Small | 4 |
| ISSUE-22 | Low | IEK README, PES spec | Tiny | 4 |
| ISSUE-23 | Low | harness ER, onboarding guide | Small | 4 |
| ISSUE-24 | Low | ER spec | Small | 4 |
| ISSUE-25 | Low | PRK README, governance-model.md | Tiny | 4 |

**Effort scale:** Tiny = 1 file, 1–5 lines. Small = 1–3 files, focused edit. Medium = 3–6 files, spec-level changes. Large = new files required.

---

## Section 5: What Is Working Well

Before the fixes: the framework has genuine strengths that the issues do not diminish.

- The **freeze-before-promote invariant** is enforced consistently across all 15 layers with no contradictions.
- The **4-file system** (spec / template / prompt / validator) is implemented faithfully across every governed artifact. No kit deviates.
- The **escalation model** (4 defined triggers, human-authorized, non-automatic) is rigorous and well-reasoned. The triggers are well-bounded with explicit "ALL must be true" criteria.
- The **entry gate pattern** (human-authored gate artifacts for EEK, REK, RRK, QAK, ODK) is sound. Human accountability at each kit transition is structurally enforced.
- The **feedback loop architecture** is complete. All 10 loops are traceable, grounded in specific artifacts, and directionally correct.
- The **convergence loop rules** (max 3 iterations, separate sessions, structured escalation) are consistent throughout and match what the agent harness enforces programmatically.
- The **aieos-schema** is the most complete machine-readable representation of a governance framework I have seen. 391 hard gates across 68 schemas is substantial.
- The **initiative presets** are practical and cover the realistic space of initiative types without overfitting.

---

*Report generated from read-only inspection of 80+ source files across 26 repositories.*  
*No files were modified during this audit.*


---

## Section 6: Closure Log

All 25 issues closed. Gap closure work executed 2026-05-17.

| Issue | Severity | Description | Repo | Status |
|-------|----------|-------------|------|--------|
| ISSUE-01 | Critical | Escalation Trigger 5 defined (SLO rollback path) | aieos-governance-foundation | Closed |
| ISSUE-02 | Critical | QAK optional/required contradiction resolved — conditionally required | aieos-governance-foundation, QAK | Closed |
| ISSUE-03 | Critical | VP compliance SCK ordering gate added — spec v1.1 | aieos-quality-assurance-kit | Closed |
| ISSUE-04 | High | Layer count corrected 16→15 in README and layer-model.md | aieos-governance-foundation | Closed |
| ISSUE-05 | High | EEK repo name corrected (aieos-engineering-execution, no -kit) across all 40+ files | all repos | Closed |
| ISSUE-06 | High | PIK WCR correctly described as governed artifact with 4-file set | aieos-product-intelligence-kit | Closed |
| ISSUE-07 | High | REK artifact count corrected to 5 (RER, RCF, RSA, RP, RR) | aieos-release-exposure-kit | Closed |
| ISSUE-08 | High | BPK RC conditional gate added to release-entry-spec v1.1 | aieos-release-exposure-kit | Closed |
| ISSUE-09 | High | PRK lens tables reconciled — playbook aligned with CLAUDE.md | aieos-peer-review-kit | Closed |
| ISSUE-10 | High | DCF entry gate tightened — SAD precondition added to spec v1.1 | aieos-engineering-execution | Closed |
| ISSUE-11 | High | SDK Layer 1 status clarified — engagement conditions documented | aieos-strategic-direction-kit | Closed |
| ISSUE-12 | Medium | PINFK conditional reference gate added to ACF spec v1.1 | aieos-engineering-execution | Closed |
| ISSUE-13 | Medium | DCK dual trigger structure documented (EEK-phase vs REK-phase) | aieos-data-configuration-kit | Closed |
| ISSUE-14 | Medium | DHR trigger criteria defined with cadence floor and responsible owner | aieos-documentation-knowledge-kit | Closed |
| ISSUE-15 | Medium | SSK skip justification added as hard gate to KER spec v1.1 | aieos-engineering-execution | Closed |
| ISSUE-16 | Medium | PRK lens schemas — 13 schemas require separate authoring work; surfaced as known gap | aieos-schema | Open — requires lens spec reads + schema authoring, deferred |
| ISSUE-17 | Medium | Pipeline runner M3 scaffolding status notice added to README | aieos-pipeline-runner | Closed |
| ISSUE-18 | Medium | Console kit coverage table added to README | aieos-console | Closed |
| ISSUE-19 | Medium | DKR resolved — has full 4-file set, referenced in SAD/TDD specs; surfaced in README | aieos-engineering-execution | Closed |
| ISSUE-20 | Medium | IEK entry gate exception documented in governance model and IEK README | aieos-governance-foundation, IEK | Closed |
| ISSUE-21 | Low | Retroactive field added to Engagement Record Document Control | aieos-governance-foundation | Closed |
| ISSUE-22 | Low | PES bootstrap requirement note added to IEK README | aieos-insight-evolution-kit | Closed |
| ISSUE-23 | Low | Agent harness REK/RRK exemption documented with bootstrapping rationale | aieos-agent-harness | Closed |
| ISSUE-24 | Low | ER per-section completeness field guidance added | aieos-governance-foundation | Closed |
| ISSUE-25 | Low | PRK adversarial lens inverted PASS/FAIL documented in README and governance model | aieos-peer-review-kit, foundation | Closed |

### Spec version bumps (Significant changes, v1.0 → v1.1)

| Spec | Kit | Change |
|------|-----|--------|
| vp-spec.md | QAK | Added compliance_sck_ordering gate (ISSUE-03) |
| release-entry-spec.md | REK | Added bpk_rc_status gate (ISSUE-08) |
| dcf-spec.md | EEK | Added upstream_dependency_ordering gate (ISSUE-10) |
| kit-entry-spec.md | EEK | Added ssk_disposition gate (ISSUE-15) |
| acf-spec.md | EEK | Added pinfk_reference_or_explicit_assumptions gate (ISSUE-12) |

### Governance model version

v1.6 → v1.7. All 15 kit copies synchronized.

### Open item

ISSUE-16 (PRK lens schemas in aieos-schema) was not fully executed. Creating 13 YAML schema files requires reading each of the 13 lens spec files in aieos-peer-review-kit to extract their hard gates, then authoring 13 new schemas conforming to the aieos-schema meta-schema. This is tracked as a follow-on task.
