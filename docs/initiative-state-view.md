# Initiative State View

Use this template to track an initiative's artifact state across all AIEOS kit layers. Copy the blank template into your project or Engagement Record to maintain a current snapshot.

**Status values:**
- `—` Not applicable to this initiative
- `⬜ Not Started`
- `🔄 In Progress`
- `✓ Validated` (validator PASS, awaiting human freeze decision)
- `🔒 Frozen`

---

## Blank Template

**Initiative:** `[name]`
**Engagement Record:** `ER-[INITIATIVE]-[NNN]`
**Last Updated:** `[date]`

| Layer | Kit | Artifact | ID | Status | Notes |
|-------|-----|----------|----|--------|-------|
| 2 | PIK | Work Classification Record | WCR | | |
| 2 | PIK | Discovery Intake | — | | |
| 2 | PIK | Problem Framing Document | PFD-[PROJECT]-NNN | | |
| 2 | PIK | Value Hypothesis | VH-[PROJECT]-NNN | | |
| 2 | PIK | Assumption Register | AR-[PROJECT]-NNN | | |
| 2 | PIK | Experiment Log | EL-[PROJECT]-NNN | | |
| 2 | PIK | Discovery PRD | DPRD-[PROJECT]-NNN | | |
| 4 | EEK | Kit Entry Record | KER | | |
| 4 | EEK | PRD | PRD-[PROJECT]-NNN | | |
| 4 | EEK | Architecture Context File | ACF-[PROJECT]-NNN | | |
| 4 | EEK | System Architecture Design | SAD-[PROJECT]-NNN | | |
| 4 | EEK | Design Context File | DCF-[PROJECT]-NNN | | |
| 4 | EEK | Technical Design Document | TDD-[PROJECT]-NNN | | |
| 4 | EEK | Work Design Document | WDD-[PROJECT]-NNN | | |
| 4 | EEK | Operational Readiness Document | ORD-[PROJECT]-NNN | | |
| 5 | REK | Release Entry Record | RER-[PROJECT]-NNN | | |
| 5 | REK | Release Context File | RCF-[ORG]-NNN | | |
| 5 | REK | Release Plan | RP-[PROJECT]-NNN | | |
| 5 | REK | Release Record | RR-[PROJECT]-NNN | | |
| 6 | RRK | Service Reliability Entry Record | SRER-[PROJECT]-NNN | | |
| 6 | RRK | Service Reliability Profile | SRP-[SERVICE]-NNN | | |
| 6 | RRK | Incident Record(s) | IR-[SERVICE]-NNN | | |
| 6 | RRK | Reliability Health Report | RHR-[SERVICE]-NNN | | |
| 7 | IEK | Evolution Signal | ES-[SCOPE]-NNN | | |
| 7 | IEK | Portfolio Evolution Signal | PES-NNN | | |
| 8 | ODK | Diagnostic Context Record | DCR-[SERVICE]-NNN | | |
| 8 | ODK | Investigation Record | INR-[SERVICE]-NNN | | |
| 8 | ODK | Postmortem Record | PMR-[SERVICE]-NNN | | |
| 8 | ODK | Runbook | RB-[SERVICE]-NNN | | |
| 9 | QAK | Quality Assurance Entry Record | QAER-[PROJECT]-NNN | | |
| 9 | QAK | Verification Plan | VP-[PROJECT]-NNN | | |
| 9 | QAK | Test Campaign Record | TCR-[PROJECT]-NNN | | |
| 9 | QAK | Quality Gate Record | QGR-[PROJECT]-NNN | | |
| 10 | SCK | Threat Model | TM-[PROJECT]-NNN | | |
| 10 | SCK | Security Assessment Record | SAR-[PROJECT]-NNN | | |
| 10 | SCK | Compliance Evidence Record | CER-[PROJECT]-NNN | | |
| 10 | SCK | Dependency Audit Record | DAR-[PROJECT]-NNN | | |
| 11 | DCK | Configuration Specification | CSPEC-[PROJECT]-NNN | | |
| 11 | DCK | Feature Flag Lifecycle Record | FFLR-[PROJECT]-NNN | | |
| 11 | DCK | Data Schema Record | DSR-[PROJECT]-NNN | | |
| 12 | PINFK | Platform Decision Record(s) | PDR-[PROJECT]-NNN | | |
| 12 | PINFK | Infrastructure Specification | ISPEC-[PROJECT]-NNN | | |
| 12 | PINFK | Environment Matrix | EM-[PROJECT]-NNN | | |

**Key decisions and pivot points:**

| Date | Layer | Decision | Outcome |
|------|-------|----------|---------|
| | | | |

---

## Worked Example: TaskFlow Notification Service

**Initiative:** TaskFlow Push Notification Service
**Engagement Record:** ER-TASKFLOW-NOTIFICATIONS-001
**Last Updated:** 2026-01-15

| Layer | Kit | Artifact | ID | Status | Notes |
|-------|-----|----------|----|--------|-------|
| 2 | PIK | Work Classification Record | WCR | 🔒 Frozen | Classified: New Feature |
| 2 | PIK | Discovery Intake | — | 🔒 Frozen | 6/6 hard gates passing |
| 2 | PIK | Problem Framing Document | PFD-TASKFLOW-001 | 🔒 Frozen | |
| 2 | PIK | Value Hypothesis | VH-TASKFLOW-001 | 🔒 Frozen | |
| 2 | PIK | Assumption Register | AR-TASKFLOW-001 | 🔒 Frozen | 4 high-risk assumptions validated |
| 2 | PIK | Experiment Log | EL-TASKFLOW-001 | 🔒 Frozen | Outcome: Proceed |
| 2 | PIK | Discovery PRD | DPRD-TASKFLOW-001 | 🔒 Frozen | Delivered to EEK |
| 4 | EEK | Kit Entry Record | KER | 🔒 Frozen | Path A (DPRD) |
| 4 | EEK | PRD | PRD-TF-001 | 🔒 Frozen | Placed from DPRD, acceptance check passed |
| 4 | EEK | Architecture Context File | ACF-TF-001 | 🔒 Frozen | |
| 4 | EEK | System Architecture Design | SAD-TF-001 | 🔒 Frozen | |
| 4 | EEK | Design Context File | DCF-TF-001 | 🔒 Frozen | |
| 4 | EEK | Technical Design Document | TDD-TF-001 | 🔒 Frozen | |
| 4 | EEK | Work Design Document | WDD-TF-001 | 🔒 Frozen | |
| 4 | EEK | Operational Readiness Document | ORD-TF-001 | 🔒 Frozen | |
| 5 | REK | Release Entry Record | RER-TF-001 | 🔒 Frozen | |
| 5 | REK | Release Context File | RCF-TF-001 | 🔒 Frozen | Org-level policy, reused |
| 5 | REK | Release Plan | RP-TF-001 | 🔒 Frozen | Canary deployment |
| 5 | REK | Release Record | RR-TF-001 | 🔒 Frozen | Disposition: Released |
| 6 | RRK | Service Reliability Entry Record | SRER-TF-001 | 🔒 Frozen | |
| 6 | RRK | Service Reliability Profile | SRP-NOTIFICATION-SVC-001 | 🔒 Frozen | v1.0 |
| 6 | RRK | Incident Record(s) | IR-NOTIFICATION-SVC-001 | 🔒 Frozen | Queue exhaustion, SEV2 |
| 6 | RRK | Reliability Health Report | RHR-NOTIFICATION-SVC-001 | 🔒 Frozen | First review cycle |
| 7 | IEK | Evolution Signal | ES-NOTIFICATION-SVC-001 | 🔒 Frozen | Signal: maintain |
| 7 | IEK | Portfolio Evolution Signal | PES-NNN | — | Not applicable (single initiative) |
| 8 | ODK | Diagnostic Context Record | DCR-NOTIFICATION-SVC-001 | 🔒 Frozen | Queue exhaustion incident |
| 8 | ODK | Investigation Record | INR-NOTIFICATION-SVC-001 | 🔒 Frozen | |
| 8 | ODK | Postmortem Record | PMR-NOTIFICATION-SVC-001 | 🔒 Frozen | 3 corrective actions |
| 8 | ODK | Runbook | RB-NOTIFICATION-SVC-001 | 🔒 Frozen | Queue recovery procedure |

**Key decisions and pivot points:**

| Date | Layer | Decision | Outcome |
|------|-------|----------|---------|
| 2025-06-01 | PIK (AR/EL) | High-risk assumption: users will enable push notifications | Validated: 73% opt-in in pilot |
| 2025-07-15 | EEK (WDD) | Scope boundary: iOS/Android only, web push deferred | WDD non-goals updated; ORD verified |
| 2026-01-05 | ODK | SEV2: queue exhaustion caused 6-hour delivery delay | PMR frozen; corrective action routed to EEK |
| 2026-01-15 | IEK | ES signal: maintain | No re-discovery triggered; watch for queue capacity trends |
