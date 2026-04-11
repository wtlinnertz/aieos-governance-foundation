# Decision Router Tool Prompt

You are invoking the decision-router tool capability.

## When to Invoke

Invoke this tool **at any junction in the AIEOS flow where the operator must choose a path**. Specific situations:

- position-check identifies a pending junction decision
- The operator reaches a fork in the playbook (Path A vs B, BAT outcome, QGR disposition, etc.)
- An escalation trigger fires and the routing must be determined
- A re-entry decision must be made (material vs non-material change)
- The operator asks "which way should I go?"

## Why to Invoke

Junctions are where mistakes happen — choosing the wrong path wastes work. This tool ensures every option is visible, criteria are applied systematically, and the decision is evidence-based rather than gut-feel.

## Execution Instructions

1. Look up the junction ID in navigation-map.md Section 3 (Decision Tables)
2. Present every option from the decision table — do not filter or hide options
3. For each option, evaluate its condition against:
   - The user-provided context
   - The ER content (artifact statuses, decisions recorded)
   - Any relevant frozen artifact content
4. Identify which option(s) have their conditions met
5. If exactly one option matches: recommend it with rationale
6. If multiple options match: present all with rationale; state human must choose
7. If no options match: this is the escape hatch — recommend invoking position-check
8. Document the downstream consequences of the recommended path
9. Produce output conforming to `decision-router-template.md`

## The Escape Hatch

Every decision table has an implicit final row: **"If none of the above conditions match, invoke position-check to re-establish position."** This prevents the AI from forcing a choice when the situation doesn't fit the expected patterns. It is always better to re-orient than to guess.

## Result Interpretation

- **PASS with High Confidence**: One option clearly matches. Proceed after human confirmation.
- **PASS with Medium Confidence**: Multiple options match or evidence is partial. Present options for human choice.
- **FAIL**: No options match or junction ID is invalid. Invoke position-check to re-orient.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `decision-router-spec.md`.
