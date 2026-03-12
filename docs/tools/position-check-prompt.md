# Position Check Tool Prompt

You are invoking the position-check tool capability.

## When to Invoke

Invoke this tool **whenever you need to know where the initiative currently stands**. Specific situations:

- At the start of any session to orient ("where are we?")
- When the operator asks "what should I do next?"
- After returning from a break or context switch
- When something feels off or the flow seems wrong
- After an anomaly is suspected (artifact missing, wrong order, stale work)
- When a decision-router returns "none of the above match"
- Before any handoff-navigator invocation (to confirm exit conditions are met)

This is the AI sherpa's compass. When in doubt, invoke position-check.

## Why to Invoke

Position is derived from ground truth (ER + actual files), not from memory or conversation history. This tool ensures the AI is working from verified reality, not accumulated assumptions. It also detects anomalies that might otherwise go unnoticed.

## Execution Instructions

1. Read the Engagement Record at the provided path
2. Scan the artifact directory for all artifact files
3. For each artifact in the initiative's scope (based on preset and kit):
   - Check if the file exists in the artifact directory
   - Read the Document Control section for status (Draft/Frozen)
   - Compare with the ER's recorded status
   - Record in the Artifact Inventory table
4. Cross-reference the artifact inventory against the navigation map:
   - Find the most advanced node where the artifact is frozen
   - The next unfrozen artifact in the sequence is the current position
   - If the current artifact is in progress (exists but not frozen), that is the current node
5. Identify the next action based on the current node's outgoing edges in the navigation map
6. Check for pending junction decisions (is the current or next node a junction?)
7. Check cross-cutting kit activation status against expected triggers
8. Run all anomaly checks from navigation-map.md Section 4
9. Produce output conforming to `position-check-template.md`

## Result Interpretation

- **PASS with High Confidence**: Position is clear, no anomalies, next action is unambiguous. Proceed.
- **PASS with Medium Confidence**: Position identified but minor anomalies or ambiguities exist. Review anomalies before proceeding.
- **FAIL**: Position cannot be determined or blocking anomalies exist. Resolve anomalies before proceeding.

## Self-Correction

This tool IS the self-correction mechanism. When the AI or operator is lost:
1. Invoke position-check — it reads ground truth regardless of conversational context
2. Review anomalies — they explain what went wrong
3. Use the next action recommendation to get back on track
4. If anomalies indicate a wrong path was taken, the recommended actions guide recovery

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `position-check-spec.md`.
