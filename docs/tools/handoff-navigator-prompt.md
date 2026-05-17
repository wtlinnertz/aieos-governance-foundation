# Handoff Navigator Tool Prompt

You are invoking the handoff-navigator tool capability.

## When to invoke

Invoke this tool **when a kit's exit condition is met and the initiative must transition to the next kit**. Specific situations:

- PIK DPRD frozen → handoff to EEK
- EEK ORD frozen → handoff to QAK or REK
- QAK QGR frozen (PASS/CONDITIONAL) → handoff to REK
- REK RR frozen → handoff to RRK
- RRK 2+ RHRs frozen → IEK eligible
- ODK PMR frozen → cross-kit outputs to EEK/PIK
- Any escalation trigger → handoff to target kit

Also invoke when:
- position-check indicates the next action is a handoff
- The operator asks "what do I need to do to move to the next kit?"

## Why to invoke

Cross-kit handoffs are where context gets lost. This tool ensures: exit conditions are actually met (not assumed), the right artifacts cross the boundary, the destination kit's entry requirements are checked, and cross-cutting kit activations are not missed.

## Execution instructions

1. Verify the source kit's exit conditions:
   - Read the source kit's playbook exit section
   - Check that all required artifacts are frozen (read actual files, not just ER)
   - Report any unmet conditions as blocking
2. Identify the destination kit:
   - Use the preset path from the navigation map
   - If multiple destinations are valid (e.g., QAK or direct to REK), invoke decision-router for that junction first
3. Read the destination kit's entry-from file:
   - Locate `docs/entry-from-{source}.md` in the destination kit
   - List the required artifacts and their expected states
   - Cross-reference against the actual artifact statuses
4. List the handoff artifacts with verified freeze status
5. Check cross-cutting kit activations:
   - Review the navigation map's cross-cutting trigger edges
   - Flag any activations that should have occurred by now but haven't
6. Name the first action in the destination kit
7. Provide ER update instructions for both kits
8. Produce output conforming to `handoff-navigator-template.md`

## Result interpretation

- PASS (Handoff Ready: Yes): All exit conditions met, all handoff artifacts frozen, entry requirements satisfied. Proceed to destination kit.
- PASS (Handoff Ready: No): Exit conditions partially met. Blocking items listed. Resolve before proceeding.
- FAIL: Cannot determine handoff readiness. Invoke position-check to re-orient.

## Spec reference

The authoritative rules, constraints, and hard gates for this tool are defined in `handoff-navigator-spec.md`.
