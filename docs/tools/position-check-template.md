# Position Check Output

## Position Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-POSITION-CHECK |
| Initiative | {initiative ID} |
| Preset | {P1–P5 or "Unknown"} |
| ER Path | {path} |
| Artifact Directory | {path} |
| Timestamp | {ISO 8601} |

## Current Position

| Field | Value |
|-------|-------|
| Current Node | {navigation map node ID, e.g., N-EEK-TDD} |
| Current Node Name | {human-readable name, e.g., "Technical Design Document"} |
| Current Kit | {kit name} |
| Status at Current Node | {In Progress / Awaiting Validation / Awaiting Freeze / Awaiting Decision} |

## Next Action

| Field | Value |
|-------|-------|
| Next Action | {what the operator should do next} |
| Next Node | {navigation map node ID for the next state} |
| Blocking On | {what must happen before the next action can proceed, or "Nothing — ready to proceed"} |

## Artifact Inventory

| Artifact | Node ID | Expected | File Found | ER Status | File Status | Match |
|----------|---------|----------|------------|-----------|-------------|-------|
| {name} | {node ID} | {Yes/No/N/A} | {Yes/No} | {Frozen/Draft/Not Listed} | {Frozen/Draft/Missing} | {OK/Mismatch/Missing} |

## Pending Decisions

| Junction | Node ID | Description | Options |
|----------|---------|-------------|---------|
| {junction name} | {node ID} | {what must be decided} | {brief list of options} |

*(If no pending decisions: "None — next action is artifact generation or handoff.")*

## Cross-Cutting Kit Status

| Kit | Activation Expected | Activated | Trigger | Status |
|-----|--------------------|-----------|---------|---------|
| SCK | {Yes/No/TBD} | {Yes/No} | {trigger condition or "N/A"} | {On Track/Overdue/Not Applicable} |
| QAK | {Yes/No/TBD} | {Yes/No} | {trigger condition or "N/A"} | {On Track/Overdue/Not Applicable} |
| DCK | {Yes/No/TBD} | {Yes/No} | {trigger condition or "N/A"} | {On Track/Overdue/Not Applicable} |
| PINFK | {Yes/No/TBD} | {Yes/No} | {trigger condition or "N/A"} | {On Track/Overdue/Not Applicable} |
| DKK | {Yes/No/TBD} | {Yes/No} | {trigger condition or "N/A"} | {On Track/Overdue/Not Applicable} |

## Anomalies

| # | Anomaly | Severity | Description | Recommended Action |
|---|---------|----------|-------------|--------------------|
| {n} | {anomaly type} | {Blocking/Warning/Advisory} | {what was detected} | {what to do about it} |

*(If no anomalies: "None detected — position is consistent with navigation map.")*

## Health Signals

| # | Signal | Severity | Description | Recommendation |
|---|--------|----------|-------------|----------------|
| {n} | {Staleness / Cross-cutting Gap / Decision Velocity / Upcoming Junction} | {Advisory / Informational} | {what was detected} | {suggested action} |

*(If fewer than 3 artifacts frozen: "Health signals not yet applicable — fewer than 3 artifacts frozen.")*
*(If 3+ artifacts and no signals: "No health signals — initiative is on track.")*

## Cross-Initiative Signals

| # | Other Initiative | Status | Overlap | Recommendation |
|---|-----------------|--------|---------|----------------|
| {n} | {initiative name} | {Active/Complete} | {shared system/component names} | {flag for conflict check / no action needed} |

*(If no sibling initiatives found: "No sibling initiatives detected.")*
*(If sibling initiatives found but no overlap: "Sibling initiatives found ({names}) — no component overlap detected.")*

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Position Confidence | {High / Medium / Low} |
