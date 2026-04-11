# AIEOS Cross-Kit Escalation Protocols

This document defines the four governed escalation triggers in the AIEOS system. Escalation is assessed, not automatic. No incident or pattern automatically triggers cross-kit re-entry. Each trigger produces a structured escalation record; a human authorizes the escalation before any action is taken.

---

## Purpose

Some events in downstream layers reveal that an upstream layer needs to act. These events cross kit boundaries and require a structured assessment and authorization step to prevent noise (every incident triggering a discovery cycle) while ensuring genuine systemic issues are not ignored.

The escalation assessment prompt (`RRK: docs/prompts/escalation-assessment-prompt.md`) supports evaluation of whether a trigger criterion is met.

---

## The Four Escalation Triggers

### Trigger 1 — SEV1/2 Incident with Code Defect

| Field | Value |
|-------|-------|
| Source Layer | Layer 6 (Reliability & Resilience Kit) |
| Signal | Frozen IR documents a SEV1 or SEV2 incident whose root cause is a code defect |
| Destination Layer | Layer 4 (Engineering Execution Kit) |
| What Destination Does | Creates a Kit Entry Record for expedited re-entry; defect fix proceeds through EEK artifact chain; produces new ORD for the patched system |

**Trigger criteria (all must be true):**
1. Incident severity was SEV1 or SEV2
2. Root cause is a code defect (not configuration, capacity, or external dependency)
3. The defect is in a system governed by the Engineering Execution Kit

**Assessment question:** Is the root cause traceable to a code defect that EEK can fix, or is this a configuration/operational issue that stays within Layer 6?

---

### Trigger 2 — Recurring Reliability Pattern

| Field | Value |
|-------|-------|
| Source Layer | Layer 6 (Reliability & Resilience Kit) |
| Signal | Three or more consecutive RHRs identify the same root cause class with no effective remediation |
| Destination Layer | Layer 2 (Product Intelligence Kit) |
| What Destination Does | Assesses whether a new discovery engagement is warranted; may create a new Work Classification Record using the escalation record as intake context |

**Trigger criteria (all must be true):**
1. Three or more consecutive review periods have documented the same root cause class
2. Each period shows the pattern was active (not just legacy tracking of a prior period's issue)
3. Prior period follow-up actions either were not completed or did not eliminate the pattern

**Assessment question:** Is this a systemic product/design problem that requires a discovery engagement, or a recurring operational issue that can be resolved within Layer 6?

---

### Trigger 3 — Release Rollback (Code/Build Defect)

| Field | Value |
|-------|-------|
| Source Layer | Layer 5 (Release & Exposure Kit) |
| Signal | A release rollback identifies the root cause as a code or build defect in the delivered system |
| Destination Layer | Layer 4 (Engineering Execution Kit) |
| What Destination Does | Creates a Kit Entry Record for the defect fix; produces a new ORD; coordinates with REK for a patch release |

**Trigger criteria (all must be true):**
1. A production release was rolled back
2. The RR root cause identifies a code or build defect (not configuration, infrastructure, or user-reported issue with no defect)
3. The defect is in a system delivered by the Engineering Execution Kit

**Assessment question:** Is the rollback cause a code defect that EEK is responsible for fixing, or an operational/configuration issue that stays within Layer 5?

---

### Trigger 4 — Release Rollback Revealing Wrong Feature

| Field | Value |
|-------|-------|
| Source Layer | Layer 5 (Release & Exposure Kit) |
| Signal | A release rollback reveals the feature should not have been built as specified — a product direction problem, not an execution problem |
| Destination Layer | Layer 2 (Product Intelligence Kit) |
| What Destination Does | Assesses whether a new discovery engagement is warranted; may create a new Work Classification Record for a discovery restart |

**Trigger criteria (all must be true):**
1. A production release was rolled back
2. The post-rollback assessment concludes the problem is product direction (wrong feature, wrong scope, wrong user model) — not code quality
3. Both the release owner and a product stakeholder agree on this assessment

**Assessment question:** Did we build the wrong thing, or did we build the right thing incorrectly? If the former, escalate to PIK. If the latter, it's a Trigger 3 (EEK defect fix).

---

## Escalation Record Format

An escalation record is a lightweight, non-governed document (no spec, validator, or freeze point). It exists to make the escalation decision traceable. File it alongside the triggering artifact in the working project directory.

```markdown
## Escalation Record

| Field | Value |
|-------|-------|
| Trigger | Trigger {N} — {trigger name} |
| Triggering Artifact | {artifact ID — e.g., IR-NOTIF-001, RR-TASKFLOW-001} |
| Destination Kit | {EEK | PIK} |
| Date | {date} |
| Authorized By | {name and role} |

### Signal Description

{1-3 sentences: what happened, what evidence supports the trigger criterion}

### Trigger Criteria Assessment

{For each criterion: met / not met, and why}

### Recommended Action

{What the destination kit should do: specific artifact to create, scope of investigation, etc.}

### Notes

{Any additional context for the receiving team}
```

---

## Receiving Protocol

When a kit receives an escalation record:

1. **Intake assessment, not automatic re-entry.** The receiving kit does not immediately begin re-entry. The escalation record is an invitation to assess, not a mandate to act.

2. **Create the entry artifact.** For EEK: create a Kit Entry Record that references the escalation record. For PIK: run a Work Classification that references the escalation record as context.

3. **Human authorization at receiving kit.** The receiving kit's team lead reviews the escalation record and confirms the escalation is warranted from their perspective. They may decline (with documented rationale) if the escalation does not meet their entry criteria.

4. **Feedback to source kit.** The receiving kit's decision (accept/decline) is communicated back to the source kit for their records.

---

## What Escalation Is Not

- Escalation is **not** automatic. An IR being filed does not automatically trigger Trigger 1.
- Escalation is **not** a blame assignment. The purpose is to route work to the right kit, not to assign fault.
- Escalation is **not** a shortcut for re-entry. The receiving kit still follows its own entry protocol.
- A declined escalation is **not** a failure. Documentation of the decline is sufficient.

---

## Relationship to Re-Entry Protocols

Escalation triggers cross-kit boundaries. Each kit's playbook documents:
- For REK and RRK: the "Escalation Paths" section covers when and how to send escalations
- For EEK and PIK: the "Receiving Escalations" section covers how to receive and process escalations

The escalation record is the handoff document between these playbook sections.
