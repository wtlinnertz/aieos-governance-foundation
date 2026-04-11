# Decision Router — Claude Code Binding

This binding maps the abstract `TOOL-DECISION-ROUTER` capability to a concrete implementation using Claude Code.

## Tool Reference

- **Tool Spec:** `docs/tools/decision-router-spec.md`
- **Tool Template:** `docs/tools/decision-router-template.md`

## Implementation

In a Claude Code session, the decision-router capability is exercised as an interactive evaluation.

### Execution Steps

1. Read `docs/navigation-map.md` Section 3 to find the decision table for the provided junction ID
2. Read the Engagement Record to gather context (artifact statuses, prior decisions)
3. If needed, read relevant frozen artifacts to gather additional evidence
4. Present all options from the decision table to the user
5. Evaluate each option's condition against the available evidence
6. If user context is insufficient, ask clarifying questions
7. Produce the decision record following the template format
8. Present recommendation and explicitly state human approval is required

### Escape Hatch Implementation

If no decision table option matches:
1. State: "None of the decision table conditions match your situation"
2. Recommend: "Invoking position-check to re-establish position"
3. If the user confirms, invoke position-check and then re-evaluate

### Environment Notes

- Claude Code reads files directly via the `Read` tool
- The AI evaluates decision table conditions conversationally
- No external API calls needed

## What This Binding Does Not Define

This binding does not define policy. The decision criteria, options, and evaluation rules are defined in `decision-router-spec.md` and `navigation-map.md`. This file only describes how those rules are exercised in the Claude Code environment.
