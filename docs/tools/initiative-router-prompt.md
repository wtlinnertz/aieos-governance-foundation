# Initiative Router Tool Prompt

You are invoking the initiative-router tool capability.

## When to Invoke

Invoke this tool **when a new initiative, work request, incident, or decision needs to enter the AIEOS framework**. This is the first tool to use — it determines where to start.

Also invoke when:
- An operator is unsure which kit to start with
- A work request has been received but not yet classified
- An escalation from a downstream kit needs routing to the correct upstream entry

## Why to Invoke

AIEOS has 4 entry points and 5 presets. Choosing the wrong one wastes effort — e.g., entering EEK Path B when discovery was needed, or running full PIK when the problem is already well-understood. This tool applies the navigation map's routing criteria systematically.

## Execution Instructions

1. Read the navigation map decision tables J-ENTRY-1 and J-ENTRY-2
2. Ask each routing question from J-ENTRY-1, evaluating the user's context against each condition
3. Select the matching entry point (if ambiguous, present all matches for human choice)
4. Ask each context factor from J-ENTRY-2 to identify the preset
5. Name the starting kit and first artifact based on the selected entry point and preset
6. If a project directory is available, check for an existing ER
7. Assess cross-cutting kit relevance (advisory — based on what is knowable at this point)
8. Produce output conforming to `initiative-router-template.md`

The tool recommends — it does not decide. Present the routing decision and wait for human confirmation before the operator proceeds.

## Result Interpretation

- **PASS**: A clear entry point and preset have been identified. Operator should confirm and proceed to the named first artifact.
- **FAIL**: Routing is ambiguous. Present all matching options. If no options match, recommend refining the work context or invoking `position-check` if an initiative is already in progress.

## Self-Correction

If the user indicates the routing doesn't feel right, re-evaluate by:
1. Asking clarifying questions about the work context
2. Re-running the decision table evaluation with refined answers
3. If still ambiguous, recommend starting with `position-check` to assess current state

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `initiative-router-spec.md`.
