# Decision Router Output

## Decision Record Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-DECISION-ROUTER |
| Initiative | {initiative ID} |
| Junction ID | {navigation map junction ID} |
| Junction Name | {human-readable junction name} |
| Current Node | {navigation map node ID} |
| Timestamp | {ISO 8601} |

## Context Summary

{Brief summary of the user-provided context and relevant ER/artifact evidence.}

## Options Evaluated

| # | Option | Condition (from decision table) | Condition Met | Evidence |
|---|--------|--------------------------------|---------------|----------|
| 1 | {option name} | {condition from navigation map} | {Yes/No/Partial} | {evidence from context/ER/artifacts} |
| 2 | {option name} | {condition from navigation map} | {Yes/No/Partial} | {evidence from context/ER/artifacts} |
| ... | ... | ... | ... | ... |

## Recommendation

| Field | Value |
|-------|-------|
| Recommended Option | {option name} |
| Route To | {navigation map node ID} |
| Rationale | {evidence-grounded justification} |
| Confidence | {High / Medium / Low} |

## Consequences of This Path

| Downstream Effect | Description |
|-------------------|-------------|
| Next artifact | {what will be produced next} |
| Cascade impact | {which downstream artifacts are affected} |
| ER update | {what should be recorded in the ER} |

## Human Approval Required

**This is a recommendation, not a decision.** The operator must confirm this path before proceeding. If the recommendation does not feel right, provide additional context and re-evaluate, or invoke `position-check` to re-orient.

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
