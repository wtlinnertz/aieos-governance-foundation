# Deprecation Protocol

This document defines the rules and procedures for retiring AIEOS artifacts when the systems or initiatives they governed have ended.

---

## Terminal Lifecycle States

Two terminal states are defined in the governance model §6 Lifecycle States:

- **Deprecated** — The artifact was Frozen. The system or service it governed is no longer active (decommissioned, replaced, or sunset).
- **Abandoned** — The artifact did not complete its lifecycle. The initiative was cancelled before the artifact reached a freeze.

### Key Distinctions

| State | Completed? | System still active? | Why terminal |
|-------|-----------|---------------------|-------------|
| Deprecated | Yes (was Frozen) | No | System ended; artifact is retained for audit |
| Abandoned | No (never Frozen) | N/A — initiative cancelled | Initiative discontinued; artifact is retained for record |

- `Deprecated` ≠ deleted. Artifacts are retained permanently for audit and organizational learning.
- `Abandoned` ≠ failed. Cancellation is a valid outcome. An abandoned initiative may restart under a new artifact series.
- Neither state triggers re-validation. Terminal state artifacts are read-only.

---

## Deprecation Notice (DN)

A **Deprecation Notice** is a non-governed record that formally records the transition to a terminal state. It is not an AIEOS artifact (no spec, validator, or prompt). It is a lightweight administrative record.

### DN Format

```
DN ID: DN-{SERVICE-OR-INITIATIVE}-{NNN}
Date: {YYYY-MM-DD}
Type: Deprecated / Abandoned
Artifacts: {comma-separated list of artifact IDs transitioning to terminal state}
Reason: {one of: service decommission / initiative cancelled / discovery abandoned / other: {detail}}
Authorized By: {name and role}
```

### DN Placement

Deprecation Notices are stored in the project repository alongside the governed artifacts, typically at `docs/sdlc/dn-{identifier}.md`. They are not subject to AIEOS validation.

---

## Use Cases

### Use Case 1: Service Decommission

A service that has gone through the full AIEOS lifecycle (Layers 4–6) is being shut down. All frozen artifacts for that service transition to Deprecated.

**Procedure:**
1. Confirm the service decommission is authorized.
2. Identify all Frozen artifacts for the service across all kits.
3. Issue a single DN covering all affected artifacts.
4. Update each artifact's Status field to `Deprecated` (non-material amendment; add Amendment Log entry per governance model §6).
5. Retain all artifacts in the repository.

**Example:**
```
DN ID: DN-NOTIFICATION-SVC-001
Date: 2026-03-15
Type: Deprecated
Artifacts: SRER-NOTIF-001, SRP-NOTIF-001, IR-NOTIF-002, IR-NOTIF-003, RHR-NOTIF-001
Reason: service decommission — notification service replaced by unified messaging platform
Authorized By: Jane Smith, Engineering Lead
```

---

### Use Case 2: Initiative Cancelled in Product Intelligence (PIK)

A discovery engagement is cancelled mid-flow — for example, after the PFD and VH are frozen but before the Experiment Log is completed. Artifacts that were never frozen are Abandoned. Artifacts that were frozen are Deprecated (the initiative ended).

**Procedure:**
1. Confirm the cancellation decision is authorized.
2. For each artifact in the discovery series:
   - If Frozen: transition to `Deprecated`
   - If not Frozen (Draft, Validated, or Freeze Pending): transition to `Abandoned`
3. Issue a DN covering all affected artifacts.
4. No re-validation is required.

**Example:**
```
DN ID: DN-PROJECT-ALPHA-001
Date: 2026-04-01
Type: Deprecated / Abandoned (mixed)
Artifacts: PFD-ALPHA-001 (Deprecated), VH-ALPHA-001 (Deprecated), AR-ALPHA-001 (Abandoned)
Reason: initiative cancelled — executive decision to redirect resources to Project Beta
Authorized By: Priya Patel, Product Director
```

---

### Use Case 3: Engineering Work Abandoned (EEK)

Engineering execution begins (Kit Entry Record issued), but the work is abandoned before the ORD is frozen — for example, due to a technical blocker, resourcing change, or scope change that invalidates the PRD.

**Procedure:**
1. Confirm the abandonment decision is authorized.
2. Identify all artifacts in the engagement (KER, PRD, ACF, SAD, etc.).
3. For each: if Frozen → `Deprecated`; if not Frozen → `Abandoned`.
4. Issue a DN.
5. If the engagement may restart under a different PRD, note this in the DN reason field.

---

## Rules

1. **Artifacts are retained, not deleted.** Terminal state does not mean removal. Audit records are permanent.
2. **DN is required.** Transitioning to a terminal state without a DN is not permitted. The DN is the authorization record.
3. **Terminal states are non-material amendments.** Updating a Frozen artifact's Status field to `Deprecated` follows the Non-Material Amendment procedure in governance model §6. No re-validation required.
4. **Downstream artifacts follow the same state.** When a Frozen upstream artifact is Deprecated, all downstream artifacts that depended on it should also be reviewed for deprecation. They may remain Frozen if they are still operationally relevant.
5. **A new series restarts from scratch.** If a Deprecated or Abandoned initiative restarts, it produces new artifacts with new IDs. It does not modify or re-activate the terminal-state artifacts.
