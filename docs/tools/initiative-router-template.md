# Initiative Router Output

## Routing Record

| Field | Value |
|-------|-------|
| Tool ID | TOOL-INITIATIVE-ROUTER |
| Initiative | {initiative name or ID} |
| Timestamp | {ISO 8601} |

## Routing Questions Evaluated

| # | Question (from J-ENTRY-1) | Answer | Evidence |
|---|--------------------------|--------|----------|
| 1 | Is this a new work request, unscoped problem, or compliance mandate? | {Yes/No} | {brief evidence} |
| 2 | Is the problem well-understood, solution known, acceptance criteria clear? | {Yes/No} | {brief evidence} |
| 3 | Is this an active production incident (SEV1/2)? | {Yes/No} | {brief evidence} |
| 4 | Is this a technology or infrastructure decision? | {Yes/No} | {brief evidence} |

## Preset Selection

| # | Context Factor (from J-ENTRY-2) | Applies | Evidence |
|---|--------------------------------|---------|----------|
| 1 | New product capability, unproven value | {Yes/No} | {brief evidence} |
| 2 | Enhancement to existing system, scope clear | {Yes/No} | {brief evidence} |
| 3 | Regulatory or compliance mandate | {Yes/No} | {brief evidence} |
| 4 | Production incident or performance degradation | {Yes/No} | {brief evidence} |
| 5 | Research/exploration with uncertain outcome | {Yes/No} | {brief evidence} |

## Routing Decision

| Field | Value |
|-------|-------|
| Entry Point | {N-PIK-WCR / N-EEK-KER / N-ODK-DCR / N-PINFK-PDR} |
| Preset | {P1 / P2 / P3 / P4 / P5 / Custom: justification} |
| Starting Kit | {kit name} |
| First Artifact | {artifact name} |
| First Action | {what the operator should do next} |

## Engagement Record Status

| Field | Value |
|-------|-------|
| ER Exists | {Yes / No / Not Checked (no project directory provided)} |
| ER Action Required | {Create new ER / Update existing ER / None} |

## Cross-Cutting Kit Advisory

| Kit | Likely Relevant | Reason |
|-----|----------------|--------|
| SCK (Layer 10) | {Yes/No/TBD} | {reason or "assess after SAD freeze"} |
| QAK (Layer 9) | {Yes/No/TBD} | {reason or "assess after ORD freeze"} |
| DCK (Layer 11) | {Yes/No/TBD} | {reason or "assess after TDD freeze"} |
| PINFK (Layer 12) | {Yes/No/TBD} | {reason or "assess when platform decisions arise"} |
| DKK (Layer 13) | {Yes/No/TBD} | {reason or "assess after release"} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Human Confirmation Required | Yes |
