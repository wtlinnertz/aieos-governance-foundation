# AIEOS Initiative Presets

Five golden paths for the most common initiative types. Each preset defines the complete artifact routing for that type of work.

---

## How to use this guide

1. Identify which preset best describes your initiative
2. Follow the artifact sequence for that preset
3. Required artifacts are mandatory; optional artifacts are situationally valuable
4. Use `initiative-state-view.md` to track status as you progress

---

## Preset 1: new feature

**Description:** A new capability that does not exist in the current system, identified through discovery.

**Starting kit:** Product Intelligence Kit (PIK), Layer 2

**Artifact sequence:**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 1 | SDK | — | SBR, PPR (use SDK when multiple strategic bets compete for capacity) |
| 2 | PIK | WCR, Discovery Intake, PFD, VH, AR, EL, DPRD | Brownfield Analysis (if adding to existing system) |
| 3 | SSK | — | SOER, VER, SDR (use SSK when Build is not the obvious choice) |
| 4 | EEK | KER (Path A), PRD (placed from DPRD), ACF, SAD, DCF, TDD, WDD, ORD | — |
| 9 | QAK | QAER, VP, TCR, QGR | — |
| 10 | SCK | TM (after SAD), SAR (after code), DAR (before release) | CER (if compliance mandate) |
| 11 | DCK | CSPEC (after TDD), DSR (after TDD) | FFLR (if feature flags used) |
| 12 | PINFK | PDR (per decision), ISPEC, SMR, EM | — |
| 13 | DKK | UDR (after release), ARR (after TDD or release) | SKA (if support team exists), DHR (periodic) |
| 14 | PRK | — | PRR for DPRD, SAD, TDD, WDD, ORD, QGR, RP, RHR (when adopted) |
| 15 | BPK | — | PIA (after SAD/TDD), TP, RC (when process-affecting changes identified) |
| 5 | REK | RER, RCF, RSA, RP, RR | — |
| 6 | RRK | SRER, SRP, RHR | IR (only if incidents occur) |
| 7 | IEK | ES | PES (when ≥2 ERs available) |
| 8 | ODK | — | DCR, INR, PMR, RB (only if SEV occurs) |

**Entry gate:** WCR classifies as "New Feature." Discovery Intake must pass 6 hard gates before PFD generation begins.

**Common pitfalls:**
- Starting at EEK (Path B) for new features that haven't been validated through discovery
- Skipping the Experiment Log (EL) when assumption validation was lightweight — document outcomes even for minimal tests
- Missing VH traceability in the DPRD (a PIK traceability gate)
- Skipping TM after SAD freeze — new features introduce new attack surfaces
- Not establishing CSPEC before release — config drift is a top production failure cause
- Not creating UDR after release — user-facing documentation gaps are a top support driver

**Exit condition (each layer):**
- PIK → EEK: DPRD frozen, all 8 hard gates passing
- EEK → QAK: ORD frozen, all 8 hard gates passing, no open blockers
- QAK → REK: QGR frozen with PASS or CONDITIONAL disposition
- SCK: TM frozen before QAK entry; SAR + DAR frozen before REK entry
- REK → RRK: RR frozen with §7 Handoff to Layer 6 complete
- RRK → IEK: ≥2 frozen RHRs covering sufficient observation period

---

## Preset 2: enhancement

**Description:** A bounded improvement to an existing capability. Scope is understood; discovery is optional.

**Starting kit:** Engineering Execution Kit (EEK), Layer 4, Path B — OR — PIK if scope is unclear

**Decision rule:** If the team can state the problem, solution space, and acceptance criteria without discovery, use Path B. If the scope is contested or the problem is poorly understood, run PIK discovery first (treat as Preset 1).

**Artifact sequence:**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 2 | PIK | — | WCR, Discovery Intake, PFD, VH (if scope is uncertain) |
| 4 | EEK | KER (Path B), Product Brief, PRD, ACF, SAD, DCF, TDD, WDD, ORD | Brownfield Analysis, Codebase Analysis |
| 9 | QAK | — | QAER, VP, TCR, QGR (if integration testing needed) |
| 10 | SCK | — | SAR, DAR (if security-relevant changes) |
| 11 | DCK | — | CSPEC updates, FFLR (if feature flags used) |
| 13 | DKK | — | UDR update (if user-facing behavior changed), ARR update (if API changed) |
| 14 | PRK | — | PRR for SAD, TDD, ORD, RP (when adopted) |
| 15 | BPK | — | PIA, TP, RC (when process-affecting changes identified) |
| 5 | REK | RER, RP, RR | RCF (if not already established), RSA (when upstream risk evidence available) |
| 6 | RRK | IR (if incident occurs), RHR (at next review cycle) | — |
| 7 | IEK | — | ES (if enhancement was significant enough to warrant learning capture) |
| 8 | ODK | — | DCR, INR, PMR (if SEV occurs) |

**Entry gate:** KER must justify Path B selection. The Kit Entry Record is the accountability record for bypassing PIK discovery.

**Common pitfalls:**
- Treating an enhancement as "obvious" and skipping ACF/DCF — organizational standards must be verified regardless of scope
- SRP revision not triggered when the enhancement changes SLO targets or failure modes
- Missing DPRD consistency check when a DPRD exists but is being updated
- Not updating UDR/ARR when enhancement changes user-visible behavior or API contracts

**Exit condition (each layer):**
- EEK → REK (or QAK if adopted): ORD frozen with all 8 hard gates passing
- REK → RRK: RR frozen; update existing SRP at next review cycle

---

## Preset 3: compliance and regulatory

**Description:** Work driven by an external mandate (regulatory requirement, audit finding, legal obligation). Scope is defined by the mandate, not by user research.

**Starting kit:** Product Intelligence Kit (PIK), Layer 2, with compliance intake

**Artifact sequence:**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 1 | SDK | — | SBR, PPR (if compliance is one of several competing investments) |
| 2 | PIK | WCR, Discovery Intake, PFD, AR, DPRD | VH (value hypothesis may be trivial or externally mandated) |
| 3 | SSK | — | SOER, VER, SDR (compliance mandates may require evaluating compliant COTS solutions) |
| 4 | EEK | KER (Path A), PRD (placed from DPRD), ACF, SAD, DCF, TDD, WDD, ORD | — |
| 10 | SCK | TM, SAR, CER, DAR | — |
| 9 | QAK | QAER, VP (references frozen TM+SAR), TCR, QGR | — |
| 14 | PRK | — | PRR for DPRD, SAD, TDD, WDD, ORD, QGR, RP (when adopted) |
| 15 | BPK | — | PIA, TP, RC (compliance changes often impact business processes) |
| 5 | REK | RER, RCF, RSA, RP, RR | — |
| 6 | RRK | SRER (if new service), SRP revision (if adding compliance requirements to existing SRP), RHR | IR (if incidents) |
| 7 | IEK | — | ES (if compliance work changes operational profile significantly) |
| 8 | ODK | — | DCR, INR, PMR (if SEV occurs) |

**Note on ordering:** SCK (Layer 10) appears before QAK (Layer 9) because frozen SCK artifacts (TM, SAR, CER, DAR) feed into QAK's Verification Plan as security test inputs. For compliance initiatives, SCK must complete before QAK's quality gate.

**Entry gate:** WCR classifies as "Compliance/Regulatory." Discovery Intake must identify the specific mandate, jurisdiction, and deadline.

**Guidance for VH:** If the initiative is purely mandate-driven with no user-facing value hypothesis, the VH may be minimal or absent. The DPRD must explicitly note this — blank VH sections fail without justification.

**Principle reference:** `aieos-product-intelligence-kit/docs/principles/compliance-discovery-principles.md` provides interpretive guidance for regulatory initiatives.

**Common pitfalls:**
- Treating compliance scope as fixed and skipping problem framing — PFD still required to bound scope and surface ambiguities in the mandate
- ACF missing compliance constraints — regulatory requirements belong in the Architecture Context File
- EL skipped because "experiments aren't relevant" — document the compliance testing and validation you performed
- CER not started early — compliance evidence should be gathered incrementally, not assembled retroactively
- DAR skipped — compliance mandates often include supply chain requirements

**Exit condition (each layer):**
- PIK → EEK: DPRD frozen with compliance mandate traceable to requirements
- EEK → QAK: ORD frozen; compliance evidence explicitly documented
- SCK: CER frozen with all mandate requirements traced to evidence; SAR frozen; DAR frozen
- QAK → REK: QGR frozen with PASS disposition (CONDITIONAL not acceptable for compliance initiatives without explicit risk acceptance)

---

## Preset 4: performance and reliability fix

**Description:** A targeted improvement to system performance, reliability, or operational stability, typically triggered by an SLO violation or incident pattern.

**Starting kit:** Varies by trigger — see below

**Decision rule:**
- Triggered by a SEV1/2 incident → start at ODK (DCR), then route corrective actions to EEK
- Triggered by RHR findings (error budget burn, SLO trend) → start at RRK (SRP revision) or EEK (Path B)
- Triggered by proactive discovery → start at PIK (treat as Preset 1 or 2)

**Artifact sequence (incident-triggered path):**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 8 | ODK | DCR, INR, PMR | RB (if recurring failure class) |
| 4 | EEK | KER (Path B, citing PMR corrective action), PRD, TDD, WDD, ORD | ACF, SAD (if architecture changes) |
| 9 | QAK | — | QAER, VP, TCR, QGR (if fix affects integration points) |
| 10 | SCK | — | SAR (if fix touches security-sensitive paths) |
| 13 | DKK | — | SKA (if incident exposed user-facing knowledge gap) |
| 14 | PRK | — | PRR for TDD, ORD, PMR (when adopted) |
| 5 | REK | RER, RP, RR | RSA (when upstream risk evidence available) |
| 6 | RRK | SRP revision (if SLO targets change), RHR | IR (if further incidents) |

**Artifact sequence (RHR-triggered path):**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 6 | RRK | SRP revision | — |
| 4 | EEK | KER (Path B), PRD, TDD, WDD, ORD | — |
| 5 | REK | RER, RP, RR | — |
| 6 | RRK | RHR (next cycle) | — |

**Common pitfalls:**
- Skipping the KER when routing from PMR to EEK — the cross-layer entry gate is required regardless of trigger
- SRP not revised when the fix changes SLO definitions or measurement methodology
- PMR corrective actions not traced into EEK WDD items — traceability breaks the audit trail

**Exit condition (each layer):**
- ODK → EEK: PMR frozen with corrective actions identified and owners named
- EEK → REK: ORD frozen; rollback plan verified (critical for reliability fixes)
- REK → RRK: RR frozen; SRP revision assessed at next RHR cycle

---

## Preset 5: exploratory research

**Description:** Open-ended investigation to understand a problem space, validate a market hypothesis, or determine whether a capability is worth building. No solution commitment.

**Starting kit:** Product Intelligence Kit (PIK), Layer 2

**Artifact sequence:**

| Layer | Kit | Required Artifacts | Optional Artifacts |
|-------|-----|-------------------|-------------------|
| 1 | SDK | — | SBR, PPR (if research is one of several competing investments) |
| 2 | PIK | WCR, Discovery Intake, PFD, VH, AR, EL | DPRD (only if research concludes with a build recommendation) |
| 4+ | — | — | All downstream kits only if research leads to a committed initiative |

**Entry gate:** WCR classifies as "Exploratory Research." The PFD defines the research question; the VH defines what would constitute a positive finding.

**Guidance on DPRD:** Do not generate a DPRD if research concludes with a "no build" or "insufficient evidence" outcome. The EL is the terminal artifact in this case. Document the conclusion in the EL and freeze.

**Guidance on pivots:** If research results in a significant pivot (different problem statement, different user group), return to PFD. Do not patch the existing PFD — create a new artifact version.

**Common pitfalls:**
- Running experiments before the AR is frozen — assumptions must be cataloged before testing
- Stress-testing assumptions (via `assumption-stress-test-prompt.md`) before the AR hard gates pass
- Generating a DPRD before EL results are definitive — the EL outcome drives the proceed/pivot/pause decision

**Exit condition:**
- Research complete → proceed: EL frozen with proceed decision, DPRD generated and frozen
- Research complete → pivot: EL frozen with pivot decision, new PFD initiated
- Research complete → pause: EL frozen with pause decision, initiative suspended (use Deprecation Note if abandoned)
