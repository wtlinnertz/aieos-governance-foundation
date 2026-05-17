# Decision Router Tool Spec

Version: v1.1

Tool ID: TOOL-DECISION-ROUTER

## Purpose

At any junction in the AIEOS flow, presents all available options, evaluates the user's context against the decision table criteria, and produces a recommendation. The tool recommends — it does not decide. Human approval is always required.

## Preconditions

- The current position is at or approaching a junction node in the navigation map
- The navigation map (`navigation-map.md`) is accessible
- The Engagement Record and relevant artifacts are accessible for context evaluation

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `junction_id` | Yes | The junction node ID from the navigation map (e.g., "J-EEK-PATH") |
| `initiative_id` | Yes | The initiative identifier |
| `er_path` | Yes | Path to the Engagement Record |
| `context` | Yes | User-provided context relevant to the decision (answers to routing questions) |

## Postconditions

- The specific junction from the navigation map has been identified and cited
- Every option from the junction's decision table has been presented
- The decision criteria have been evaluated against the user's context
- A recommendation has been produced with evidence-grounded rationale
- Human approval has been stated as required
- A plain-language explanation has been provided for the recommendation, citing: the decision table ID, the criteria evaluated, the evidence from context or artifacts, and the applicable Decision Outcome Taxonomy label (see `flow-reference.md` §11)

## Output

The tool produces structured output conforming to `decision-router-template.md`.

## Constraints

- The tool presents **all** options from the decision table — it does not filter or hide options
- The tool **recommends** — it does not auto-decide. Human approval is explicitly required
- The tool evaluates criteria from the navigation map decision tables — it does not invent its own criteria
- The tool does not modify the ER or any artifacts
- The tool does not generate artifacts
- The tool contains no references to specific implementations, environments, or vendor tools

## Error handling

| Condition | Behavior |
|-----------|----------|
| Junction ID not found in navigation map | Report error: unknown junction — recommend invoking position-check |
| User context insufficient to evaluate criteria | Report: insufficient context — list the specific information needed |
| None of the decision table conditions match | Report: no match — recommend invoking position-check to re-establish position. This is the escape hatch. |
| Multiple options equally valid | Present all matching options with rationale; human chooses |

## Hard gates

| Gate | Rule |
|------|------|
| `junction_identified` | The specific junction ID from the navigation map is cited in the output |
| `all_options_presented` | Every option from the junction's decision table is listed |
| `evaluation_criteria_applied` | Each option is evaluated against the decision table criteria using the user's context |
| `recommendation_justified` | The recommended path has a rationale grounded in evidence from the ER or artifact content |
| `no_auto_decision` | The output explicitly states that human approval is required |
| `explanation_provided` | The recommendation includes plain-language reasoning citing the decision table ID, evaluation criteria, supporting evidence, and the applicable Decision Outcome Taxonomy label |
