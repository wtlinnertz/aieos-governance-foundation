# AIEOS Navigation Map

This document is the machine-readable directed graph of the entire AIEOS framework. It defines every state an initiative can be in, every valid transition between states, and every decision junction where the operator must choose a path.

Navigation tools (`initiative-router`, `position-check`, `decision-router`, `handoff-navigator`) reference this map to guide operators through the framework.

This map is a **projection** of the kit playbooks — not a replacement. When the map and a playbook disagree, the playbook is authoritative. A Tier 2 test validates structural consistency between this map and the framework dependency model.

---

## Section 1: Nodes

Every node represents a state the initiative can be in. Node types:

| Type | Meaning |
|------|---------|
| `entry` | Framework entry point |
| `artifact` | An artifact being generated/validated/frozen |
| `gate` | A human or automated gate check |
| `junction` | A decision point where the operator must choose a path |
| `exit` | A kit's completion state |
| `escalation` | An escalation trigger to another kit |
| `utility` | An optional utility prompt/tool invocation |

### Framework Entry

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-START | — | entry | Framework Entry |

### PIK (Layer 2) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-PIK-WCR | PIK | artifact | Work Classification Record |
| N-PIK-INTAKE | PIK | artifact | Discovery Intake |
| N-PIK-PFD | PIK | artifact | Problem Framing Document |
| N-PIK-VH | PIK | artifact | Value Hypothesis |
| N-PIK-AR | PIK | artifact | Assumption Register |
| N-PIK-EL | PIK | artifact | Experiment Log |
| N-PIK-DPRD | PIK | artifact | Discovery PRD |
| N-PIK-EL-DECISION | PIK | junction | EL Outcome Decision |
| N-PIK-PIVOT | PIK | junction | Pivot Pattern Selection |
| N-PIK-EXIT | PIK | exit | DPRD Frozen — Handoff to EEK |

### SSK (Layer 3) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-SSK-SOER | SSK | gate | Sourcing Options Evaluation Record |
| N-SSK-VER | SSK | artifact | Vendor/Solution Evaluation Record |
| N-SSK-SDR | SSK | artifact | Sourcing Decision Record |
| N-SSK-ROUTE | SSK | junction | Sourcing Decision Routing |
| N-SSK-EXIT | SSK | exit | SDR Frozen — Handoff to EEK |

### EEK (Layer 4) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-EEK-KER | EEK | gate | Kit Entry Record |
| N-EEK-PATH-SELECT | EEK | junction | Path A vs Path B |
| N-EEK-PRD-A | EEK | artifact | PRD (Path A — placed DPRD) |
| N-EEK-PRD-B | EEK | artifact | PRD (Path B — generated from Brief) |
| N-EEK-CONSISTENCY | EEK | gate | Cross-Boundary Consistency Check |
| N-EEK-ACF | EEK | artifact | Architecture Context File |
| N-EEK-SAD | EEK | artifact | System Architecture Document |
| N-EEK-DCF | EEK | artifact | Design Context File |
| N-EEK-TDD | EEK | artifact | Technical Design Document |
| N-EEK-WDD | EEK | artifact | Work Decomposition Document |
| N-EEK-DOR | EEK | gate | Definition of Ready |
| N-EEK-EXEC-PLAN | EEK | artifact | Execution Plan |
| N-EEK-EXECUTION | EEK | artifact | Work Item Execution |
| N-EEK-BAT | EEK | junction | Build Acceptance Test |
| N-EEK-BAT-ESC | EEK | escalation | BAT Escalation (Path B) |
| N-EEK-ORD | EEK | artifact | Operational Readiness Document |
| N-EEK-EXIT | EEK | exit | ORD Frozen — Handoff to QAK/REK |

### QAK (Layer 9) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-QAK-QAER | QAK | gate | Quality Assurance Entry Record |
| N-QAK-VP | QAK | artifact | Verification Plan |
| N-QAK-TCR | QAK | artifact | Test Campaign Record(s) |
| N-QAK-QGR | QAK | artifact | Quality Gate Record |
| N-QAK-DISPOSITION | QAK | junction | QGR Disposition Decision |
| N-QAK-EXIT | QAK | exit | QGR Frozen (PASS/CONDITIONAL) |

### REK (Layer 5) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-REK-RER | REK | gate | Release Entry Record |
| N-REK-RCF-DECISION | REK | junction | RCF Reuse Decision |
| N-REK-RCF | REK | artifact | Release Context File |
| N-REK-RP | REK | artifact | Release Plan |
| N-REK-AUTH | REK | gate | Pre-Release Authorization Checklist |
| N-REK-EXECUTION | REK | artifact | Release Execution |
| N-REK-RR | REK | artifact | Release Record |
| N-REK-DISPOSITION | REK | junction | Release Disposition |
| N-REK-EXIT | REK | exit | RR Frozen — Handoff to RRK |

### RRK (Layer 6) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-RRK-SRER | RRK | gate | Service Reliability Entry Record |
| N-RRK-SRP | RRK | artifact | Service Reliability Profile |
| N-RRK-ACTIVE | RRK | artifact | Active Operation |
| N-RRK-IR | RRK | artifact | Incident Record |
| N-RRK-RHR | RRK | artifact | Reliability Health Report |
| N-RRK-SRP-REVISION | RRK | junction | SRP Revision Decision |
| N-RRK-ESCALATION | RRK | junction | Escalation Assessment |
| N-RRK-EXIT | RRK | exit | 2+ RHRs Frozen — Feeds IEK |

### IEK (Layer 7) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-IEK-GATHER | IEK | gate | Gather Inputs (2+ frozen RHRs) |
| N-IEK-ES | IEK | artifact | Evolution Signal |
| N-IEK-SIGNAL | IEK | junction | Re-Entry Signal Decision |
| N-IEK-EXIT | IEK | exit | ES Frozen — Signal Declared |

### ODK (Layer 8) Nodes

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-ODK-DCR | ODK | gate | Diagnostic Context Record |
| N-ODK-INR | ODK | artifact | Investigation Record |
| N-ODK-PMR | ODK | artifact | Postmortem Record |
| N-ODK-RB-DECISION | ODK | junction | Runbook Decision |
| N-ODK-RB | ODK | artifact | Runbook (optional) |
| N-ODK-ESCALATION | ODK | junction | Escalation Assessment |
| N-ODK-EXIT | ODK | exit | PMR Frozen — Cross-Kit Outputs |

### SCK (Layer 10) Nodes — Cross-Cutting

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-SCK-TM | SCK | artifact | Threat Model |
| N-SCK-SAR | SCK | artifact | Security Assessment Record |
| N-SCK-DAR | SCK | artifact | Dependency Audit Record |
| N-SCK-CER | SCK | artifact | Compliance Evidence Record |

### DCK (Layer 11) Nodes — Cross-Cutting

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-DCK-CSPEC | DCK | artifact | Configuration Specification |
| N-DCK-FFLR | DCK | artifact | Feature Flag Lifecycle Record |
| N-DCK-DSR | DCK | artifact | Data Schema Record |

### PINFK (Layer 12) Nodes — Foundational

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-PINFK-PDR | PINFK | artifact | Platform Decision Record(s) |
| N-PINFK-ISPEC | PINFK | artifact | Infrastructure Specification |
| N-PINFK-EM | PINFK | artifact | Environment Matrix |

### DKK (Layer 13) Nodes — Cross-Cutting

| Node ID | Kit | Type | Name |
|---------|-----|------|------|
| N-DKK-UDR | DKK | artifact | User Documentation Record |
| N-DKK-ARR | DKK | artifact | API Reference Record |
| N-DKK-SKA | DKK | artifact | Support Knowledge Article(s) |
| N-DKK-DHR | DKK | artifact | Documentation Health Review |

---

## Section 2: Edges

Every valid transition in the framework. Conditions describe what must be true for the transition to occur.

### Preset Applicability Key

- **P1**: New Feature
- **P2**: Enhancement
- **P3**: Compliance & Regulatory
- **P4**: Performance & Reliability Fix
- **P5**: Exploratory Research

### Framework Entry Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-001 | N-START | N-PIK-WCR | Work request requires scoping/discovery | P1, P3, P5 |
| E-002 | N-START | N-EEK-KER | Problem understood, solution known, no discovery needed | P2 |
| E-003 | N-START | N-ODK-DCR | SEV1/2 incident declared | P4 |
| E-004 | N-START | N-PINFK-PDR | Technology/infrastructure decision needed | Any |

### PIK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-010 | N-PIK-WCR | N-PIK-INTAKE | WCR routes to discovery (Full or Targeted depth) | P1, P3, P5 |
| E-011 | N-PIK-WCR | N-EEK-KER | WCR routes to EEK (None depth — no discovery needed) | P2 |
| E-012 | N-PIK-INTAKE | N-PIK-PFD | Intake frozen | P1, P3, P5 |
| E-013 | N-PIK-PFD | N-PIK-VH | PFD frozen | P1, P3, P5 |
| E-014 | N-PIK-VH | N-PIK-AR | VH frozen | P1, P3, P5 |
| E-015 | N-PIK-AR | N-PIK-EL | AR frozen | P1, P3, P5 |
| E-016 | N-PIK-EL | N-PIK-EL-DECISION | EL frozen | P1, P3, P5 |
| E-017 | N-PIK-EL-DECISION | N-PIK-DPRD | EL outcome = Proceed | P1, P3 |
| E-018 | N-PIK-EL-DECISION | N-PIK-PIVOT | EL outcome = Pivot | P1, P3, P5 |
| E-019 | N-PIK-PIVOT | N-PIK-PFD | Pattern 1: Problem Reframe | P1, P3, P5 |
| E-020 | N-PIK-PIVOT | N-PIK-VH | Pattern 2: Hypothesis Revision | P1, P3, P5 |
| E-021 | N-PIK-DPRD | N-PIK-EXIT | DPRD frozen (all 8 hard gates PASS) | P1, P3 |
| E-022 | N-PIK-EXIT | N-EEK-KER | DPRD handoff to EEK (Path A) | P1, P3 |

### SSK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-025 | N-PIK-EXIT | N-SSK-SOER | DPRD frozen; sourcing evaluation needed | P1, P3 |
| E-026 | N-SSK-SOER | N-SSK-VER | SOER frozen | P1, P3 |
| E-027 | N-SSK-VER | N-SSK-SDR | VER frozen | P1, P3 |
| E-028 | N-SSK-SDR | N-SSK-ROUTE | SDR frozen | P1, P3 |
| E-029 | N-SSK-ROUTE | N-SSK-EXIT | Decision routed | P1, P3 |
| E-029a | N-SSK-EXIT | N-EEK-KER | SDR handoff to EEK (Build/Buy/Adopt) | P1, P3 |

### EEK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-030 | N-EEK-KER | N-EEK-PATH-SELECT | KER gates entry | P1, P2, P3, P4 |
| E-031 | N-EEK-PATH-SELECT | N-EEK-PRD-A | Path A selected (DPRD received from PIK) | P1, P3 |
| E-032 | N-EEK-PATH-SELECT | N-EEK-PRD-B | Path B selected (Product Brief, no PIK) | P2, P4 |
| E-033 | N-EEK-PRD-A | N-EEK-CONSISTENCY | DPRD placed as 01-prd.md | P1, P3 |
| E-034 | N-EEK-PRD-B | N-EEK-CONSISTENCY | PRD generated from Brief | P2, P4 |
| E-035 | N-EEK-CONSISTENCY | N-EEK-ACF | Consistency check PASS; PRD frozen | All |
| E-036 | N-EEK-ACF | N-EEK-SAD | ACF frozen | All |
| E-037 | N-EEK-SAD | N-EEK-DCF | SAD frozen | All |
| E-038 | N-EEK-DCF | N-EEK-TDD | DCF frozen | All |
| E-039 | N-EEK-TDD | N-EEK-WDD | TDD frozen | All |
| E-040 | N-EEK-WDD | N-EEK-DOR | WDD generated | All |
| E-041 | N-EEK-DOR | N-EEK-EXEC-PLAN | DoR PASS; WDD frozen | All |
| E-042 | N-EEK-EXEC-PLAN | N-EEK-EXECUTION | Execution plan approved | All |
| E-043 | N-EEK-EXECUTION | N-EEK-BAT | Work group complete; BAT check | All |
| E-044 | N-EEK-BAT | N-EEK-EXECUTION | BAT PASS — continue to next work group | All |
| E-045 | N-EEK-BAT | N-EEK-BAT-ESC | BAT FAIL Path B — scope escalation | All |
| E-046 | N-EEK-BAT-ESC | N-EEK-WDD | Escalation resolved; WDD re-entry | All |
| E-047 | N-EEK-EXECUTION | N-EEK-ORD | All work groups complete | All |
| E-048 | N-EEK-ORD | N-EEK-EXIT | ORD frozen (all 8 hard gates PASS) | All |

### EEK to Downstream Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-050 | N-EEK-EXIT | N-QAK-QAER | QAK adopted (integration/cross-component testing needed) | P1, P3 |
| E-051 | N-EEK-EXIT | N-REK-RER | QAK not adopted (direct to REK) | P2, P4 |

### QAK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-060 | N-QAK-QAER | N-QAK-VP | QAER frozen | P1, P3 |
| E-061 | N-QAK-VP | N-QAK-TCR | VP frozen | P1, P3 |
| E-062 | N-QAK-TCR | N-QAK-QGR | All TCRs frozen | P1, P3 |
| E-063 | N-QAK-QGR | N-QAK-DISPOSITION | QGR generated | P1, P3 |
| E-064 | N-QAK-DISPOSITION | N-QAK-EXIT | PASS or CONDITIONAL | P1, P3 |
| E-065 | N-QAK-DISPOSITION | N-EEK-ORD | FAIL — return to EEK for remediation | P1, P3 |
| E-066 | N-QAK-EXIT | N-REK-RER | QGR frozen; proceed to REK | P1, P3 |

### REK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-070 | N-REK-RER | N-REK-RCF-DECISION | RER frozen | All |
| E-071 | N-REK-RCF-DECISION | N-REK-RCF | New RCF needed (or existing reused and confirmed) | All |
| E-072 | N-REK-RCF | N-REK-RP | RCF frozen | All |
| E-073 | N-REK-RP | N-REK-AUTH | RP frozen | All |
| E-074 | N-REK-AUTH | N-REK-EXECUTION | All 10 checklist items confirmed | All |
| E-075 | N-REK-EXECUTION | N-REK-DISPOSITION | Execution complete (or rollback/abort) | All |
| E-076 | N-REK-DISPOSITION | N-REK-RR | Disposition determined | All |
| E-077 | N-REK-RR | N-REK-EXIT | RR frozen | All |
| E-078 | N-REK-EXIT | N-RRK-SRER | RR handoff to RRK | All |

### RRK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-080 | N-RRK-SRER | N-RRK-SRP | SRER frozen | All |
| E-081 | N-RRK-SRP | N-RRK-ACTIVE | SRP frozen; monitoring begins | All |
| E-082 | N-RRK-ACTIVE | N-RRK-IR | Incident triggered (SLO breach, burn rate alert, outage) | All |
| E-083 | N-RRK-ACTIVE | N-RRK-RHR | Reporting period ends | All |
| E-084 | N-RRK-IR | N-RRK-ACTIVE | IR frozen; return to active operation | All |
| E-085 | N-RRK-RHR | N-RRK-ESCALATION | RHR frozen; assess escalation | All |
| E-086 | N-RRK-ESCALATION | N-RRK-ACTIVE | No escalation needed; continue | All |
| E-087 | N-RRK-RHR | N-RRK-EXIT | 2+ RHRs frozen; IEK eligible | All |

### IEK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-090 | N-RRK-EXIT | N-IEK-GATHER | 2+ frozen RHRs available | P1, P3 |
| E-091 | N-IEK-GATHER | N-IEK-ES | Inputs confirmed (RHRs + optional VH) | P1, P3 |
| E-092 | N-IEK-ES | N-IEK-SIGNAL | ES frozen | P1, P3 |
| E-093 | N-IEK-SIGNAL | N-IEK-EXIT | Signal declared (maintain/watch/re-discover) | P1, P3 |

### ODK Internal Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-100 | N-ODK-DCR | N-ODK-INR | DCR frozen (within 2 hours) | P4 |
| E-101 | N-ODK-INR | N-ODK-PMR | INR frozen (within 24 hours of resolution) | P4 |
| E-102 | N-ODK-PMR | N-ODK-RB-DECISION | PMR frozen | P4 |
| E-103 | N-ODK-RB-DECISION | N-ODK-RB | PMR §8 recommends runbook | P4 |
| E-104 | N-ODK-RB-DECISION | N-ODK-ESCALATION | No runbook needed | P4 |
| E-105 | N-ODK-RB | N-ODK-ESCALATION | RB frozen (or skipped) | P4 |
| E-106 | N-ODK-ESCALATION | N-ODK-EXIT | Escalation assessed | P4 |
| E-107 | N-ODK-EXIT | N-EEK-KER | Code defect identified → EEK Path B | P4 |

### Cross-Cutting Trigger Edges

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-110 | N-EEK-SAD | N-SCK-TM | SAD frozen; security-sensitive system | P1, P3 |
| E-111 | N-SCK-TM | N-SCK-SAR | TM frozen; code complete | P1, P3 |
| E-112 | N-SCK-TM | N-SCK-DAR | TM frozen; dependencies available | P1, P3 |
| E-113 | N-EEK-TDD | N-DCK-CSPEC | TDD frozen | P1, P2, P3 |
| E-114 | N-EEK-TDD | N-DCK-DSR | TDD frozen; schema design exists | P1, P2, P3 |
| E-115 | N-REK-RR | N-DCK-FFLR | Feature flags created during release | P1, P2 |
| E-116 | N-EEK-TDD | N-DKK-ARR | TDD frozen (early API docs) | P1, P2, P3 |
| E-117 | N-REK-RR | N-DKK-UDR | RR frozen (user docs at release) | P1, P2, P3 |
| E-118 | N-REK-RR | N-DKK-SKA | RR frozen (support patterns) | P1, P2 |
| E-119 | N-ODK-PMR | N-DKK-SKA | PMR frozen (incident learnings) | P4 |
| E-120 | N-PINFK-PDR | N-PINFK-ISPEC | All relevant PDRs frozen | Any |
| E-121 | N-PINFK-ISPEC | N-PINFK-EM | ISPEC frozen | Any |
| E-122 | N-SCK-TM | N-QAK-VP | Compliance: TM/SAR feed VP (optional input) | P3 |
| E-123 | N-SCK-SAR | N-QAK-VP | Compliance: SAR feeds VP (optional input) | P3 |

### Escalation Edges (reverse direction)

| Edge ID | From | To | Condition | Presets |
|---------|------|----|-----------|--------|
| E-130 | N-RRK-ESCALATION | N-EEK-KER | Trigger 1: SEV1/2 code defect → EEK Path B | Any |
| E-131 | N-RRK-ESCALATION | N-PIK-WCR | Trigger 2: Recurring pattern 3+ RHRs → PIK | Any |
| E-132 | N-REK-DISPOSITION | N-EEK-KER | Trigger 3: Rollback from code defect → EEK Path B | Any |
| E-133 | N-REK-DISPOSITION | N-PIK-WCR | Trigger 4: Rollback from wrong feature → PIK | Any |
| E-134 | N-IEK-SIGNAL | N-PIK-WCR | Trigger 6: Re-discover signal (advisory) → PIK | P1, P3 |
| E-135 | N-RRK-IR | N-ODK-DCR | Trigger 5: SEV1/2 → ODK (parallel with IR) | Any |
| E-136 | N-ODK-ESCALATION | N-EEK-KER | ODK PMR: code defect → EEK Path B | P4 |
| E-137 | N-ODK-ESCALATION | N-PIK-WCR | ODK PMR: recurring pattern → PIK | P4 |
| E-138 | N-QAK-DISPOSITION | N-EEK-ORD | QGR FAIL → return to EEK | P1, P3 |

---

## Section 3: Decision Tables

For each junction node, the structured routing criteria. At every junction, if **none of the conditions match**, invoke `position-check` to re-establish position.

### J-ENTRY-1: Framework Entry Point (N-START)

| # | Routing Question | If Yes | Route To | Rationale |
|---|-----------------|--------|----------|-----------|
| 1 | Is this a new work request, unscoped problem, or compliance mandate that needs discovery? | Yes | N-PIK-WCR | Needs PIK scoping before engineering |
| 2 | Is the problem well-understood, solution known, and acceptance criteria clear? | Yes | N-EEK-KER (Path B) | Skip discovery; direct to engineering |
| 3 | Is this an active production incident (SEV1/2)? | Yes | N-ODK-DCR | Reactive diagnosis first |
| 4 | Is this a technology or infrastructure decision? | Yes | N-PINFK-PDR | Foundational input needed |
| — | None of the above match | — | Invoke position-check | Re-evaluate context |

### J-ENTRY-2: Preset Selection (after entry point chosen)

| # | Context | Preset | First Kit |
|---|---------|--------|-----------|
| 1 | New product capability, unproven value, needs discovery | P1: New Feature | PIK |
| 2 | Enhancement to existing system, scope clear | P2: Enhancement | EEK (Path B) |
| 3 | Regulatory or compliance mandate | P3: Compliance | PIK |
| 4 | Production incident or performance degradation | P4: Performance Fix | ODK or RRK |
| 5 | Research/exploration with uncertain outcome | P5: Exploratory | PIK |

### J-PIK-WCR: Work Classification Routing (N-PIK-WCR)

| # | WCR Depth | Condition | Route To |
|---|-----------|-----------|----------|
| 1 | Full | Complex problem, multiple stakeholders, uncertain solution | N-PIK-INTAKE (full discovery) |
| 2 | Targeted | Partially understood problem, needs focused investigation | N-PIK-INTAKE (targeted discovery) |
| 3 | None | Problem understood, no discovery needed | N-EEK-KER (Path B) |

### J-PIK-EL: EL Outcome Decision (N-PIK-EL-DECISION)

| # | EL Outcome | Evidence Required | Route To |
|---|------------|-------------------|----------|
| 1 | Proceed | EL frozen with sufficient evidence supporting value hypothesis | N-PIK-DPRD |
| 2 | Pivot | EL reveals wrong problem framing or wrong hypothesis | N-PIK-PIVOT |
| 3 | Pause | Blocking issue, insufficient evidence, market shift | Exit (initiative paused) |

### J-PIK-PIVOT: Pivot Pattern Selection (N-PIK-PIVOT)

| # | Pattern | Trigger | Route To | Cascade Impact |
|---|---------|---------|----------|----------------|
| 1 | Problem Reframe | EL reveals different problem framing | N-PIK-PFD | PFD, VH, AR, EL, DPRD all revised |
| 2 | Hypothesis Revision | Value mechanism wrong but problem correct | N-PIK-VH | VH, AR, EL, DPRD revised; PFD unchanged |
| 3 | Assumption Invalidation | Assumption invalid but direction holds | N-PIK-EL (mark invalid) | EL updated, DPRD reflects constraints |

### J-SSK-ENTRY: SSK Engagement Decision (N-PIK-EXIT)

| # | Condition | Route To |
|---|-----------|----------|
| 1 | Build is obviously the only viable option (no market alternatives, unique domain, competitive differentiator) | N-EEK-KER (skip SSK; document fast-path justification in KER) |
| 2 | Buy or Adopt candidates may exist; sourcing evaluation warranted | N-SSK-SOER |
| — | Uncertain | Invoke position-check |

### J-SSK-ROUTE: Sourcing Decision Routing (N-SSK-ROUTE)

| # | Decision | Route To | EEK Scope Impact |
|---|----------|----------|-----------------|
| 1 | Build | N-EEK-KER (Path A, full scope) | Full EEK: DPRD + SDR provided |
| 2 | Buy {vendor} | N-EEK-KER (Path A, reduced scope) | EEK scoped to integration + customization |
| 3 | Adopt {project} | N-EEK-KER (Path A, reduced scope) | EEK scoped to integration + configuration |

### J-EEK-PATH: Path A vs Path B (N-EEK-PATH-SELECT)

| # | Condition | Path | Route To |
|---|-----------|------|----------|
| 1 | Frozen DPRD received from PIK (with or without frozen SDR from SSK) | Path A | N-EEK-PRD-A (place DPRD as 01-prd.md) |
| 2 | No PIK engagement; scope justifiable without discovery | Path B | N-EEK-PRD-B (Product Brief → generate PRD) |

### J-EEK-QAK: QAK Adoption (N-EEK-EXIT)

| # | Condition | Route To |
|---|-----------|----------|
| 1 | Integration points, external dependencies, cross-component behavior exist | N-QAK-QAER (adopt QAK) |
| 2 | Single-component, no integration testing needed | N-REK-RER (skip QAK) |

### J-EEK-BAT: BAT Outcome (N-EEK-BAT)

| # | Outcome | Condition | Route To |
|---|---------|-----------|----------|
| 1 | Pass | All acceptance criteria met for work group | N-EEK-EXECUTION (next work group) |
| 2 | Path A (fixable) | Issues fixable within current scope | N-EEK-EXECUTION (add fix items) |
| 3 | Path B (escalation) | Scope change needed | N-EEK-BAT-ESC (escalation record) |

### J-QAK-DISPOSITION: QGR Disposition (N-QAK-DISPOSITION)

| # | Disposition | Condition | Route To |
|---|------------|-----------|----------|
| 1 | PASS | All quality gates met | N-QAK-EXIT → N-REK-RER |
| 2 | CONDITIONAL | Quality gates met with documented risks | N-QAK-EXIT → N-REK-RER (with conditions) |
| 3 | FAIL | Blocking quality issues | N-EEK-ORD (return to EEK) |

### J-REK-RCF: RCF Reuse Decision (N-REK-RCF-DECISION)

| # | Condition | Route To |
|---|-----------|----------|
| 1 | Existing frozen RCF covers this release's scope | N-REK-RP (reuse existing RCF) |
| 2 | No RCF exists or scope not covered | N-REK-RCF (generate new RCF) |

### J-REK-DISPOSITION: Release Disposition (N-REK-DISPOSITION)

| # | Outcome | Route To | Escalation |
|---|---------|----------|------------|
| 1 | Released (successful) | N-REK-RR | None |
| 2 | Rolled back — code defect | N-REK-RR | Trigger 3 → EEK |
| 3 | Rolled back — wrong feature | N-REK-RR | Trigger 4 → PIK |
| 4 | Abandoned | N-REK-RR | None (document reason) |

### J-RRK-SRP-REVISION: SRP Revision (N-RRK-SRP-REVISION)

| # | Condition | Route To |
|---|-----------|----------|
| 1 | SLO targets, error budget, or methodology need change | Generate new SRP version |
| 2 | Current SRP still valid | Continue with current SRP |

### J-RRK-ESCALATION: Escalation Assessment (N-RRK-ESCALATION)

| # | Trigger | Condition | Route To |
|---|---------|-----------|----------|
| 1 | Trigger 1 | SEV1/2 incident with code defect root cause | N-EEK-KER (Path B) |
| 2 | Trigger 2 | Same root cause class in 3+ consecutive RHRs | N-PIK-WCR |
| 3 | Trigger 5 | SEV1/2 incident declared | N-ODK-DCR (parallel) |
| 4 | None | No escalation criteria met | N-RRK-ACTIVE (continue) |

### J-IEK-SIGNAL: Re-Entry Signal (N-IEK-SIGNAL)

| # | Signal | Condition | Route To | Action |
|---|--------|-----------|----------|--------|
| 1 | Maintain | Service healthy, SLOs met | N-IEK-EXIT | No cross-kit action |
| 2 | Watch | Emerging trend, not yet critical | N-IEK-EXIT | Elevate monitoring |
| 3 | Re-discover | Persistent/new pattern requires product investigation | N-PIK-WCR (advisory) | Product owner decides |

### J-ODK-RB: Runbook Decision (N-ODK-RB-DECISION)

| # | Condition | Route To |
|---|-----------|----------|
| 1 | PMR §8 identifies repeatable failure class with known procedure | N-ODK-RB (generate runbook) |
| 2 | One-time, novel, or non-repeatable failure | N-ODK-ESCALATION (skip runbook) |

### J-ODK-ESCALATION: ODK Escalation Assessment (N-ODK-ESCALATION)

| # | Finding | Route To |
|---|---------|----------|
| 1 | Code defect identified | N-EEK-KER (Path B) |
| 2 | Recurring pattern (3+ occurrences) | N-PIK-WCR |
| 3 | No cross-kit action needed | N-ODK-EXIT |

### J-SCK-TIMING: SCK Timing for Compliance (cross-cutting)

| # | Preset | Condition | Ordering |
|---|--------|-----------|----------|
| 1 | P3 (Compliance) | Compliance mandate | SCK completes before QAK; TM+SAR feed VP |
| 2 | All others | Security-sensitive system | SCK parallel with QAK or independent |

### J-REENTRY: Re-Entry Decision (applicable at any frozen artifact)

| # | Change Type | Condition | Action |
|---|------------|-----------|--------|
| 1 | Non-material | Does not affect hard gates, scope, decisions, or downstream references | Amend in place; add Amendment Log entry |
| 2 | Material (within-kit) | Affects hard gates, scope, or downstream artifacts | Re-entry protocol: impact analysis → modify → re-validate → cascade |
| 3 | Material (cross-kit) | Frozen upstream artifact (e.g., DPRD) must change after downstream work exists | Cross-kit re-entry: notify downstream → joint impact analysis → cascade re-validation |

---

## Section 4: Anomaly Patterns

When `position-check` runs, it should flag these anomalies:

| Anomaly | Detection | Severity |
|---------|-----------|----------|
| Artifact exists without frozen upstream | Artifact file present but upstream artifact missing or unfrozen | Blocking |
| ER lists artifact as frozen but file not found | ER §N artifact ID present but no matching file in artifact directory | Blocking |
| ER artifact status inconsistent with file | ER says "Draft" but file Document Control says "Frozen" (or vice versa) | Blocking |
| Current state maps to no valid node | Artifact inventory does not match any known position in the navigation map | Warning — invoke decision-router |
| Skipped node in sequence | Artifact N+2 exists but artifact N+1 does not | Warning — may indicate intentional skip-with-justification |
| Cross-cutting kit not activated | SAD frozen but no TM generated (for security-sensitive system) | Advisory |
| Stale position | Last artifact freeze was more than the expected cadence for the current kit | Advisory |
