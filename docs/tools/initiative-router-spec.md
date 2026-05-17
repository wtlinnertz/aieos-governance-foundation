# Initiative Router Tool Spec

Version: v1.1

Tool ID: TOOL-INITIATIVE-ROUTER

## Purpose

The front door to AIEOS. Evaluates the user's situation through structured routing questions, selects the correct entry point, identifies the applicable preset, and names the starting kit and first artifact.

## Preconditions

- A work request, incident, or decision exists that needs to enter the AIEOS framework
- The navigation map (`navigation-map.md`) is accessible
- The initiative presets (`initiative-presets.md`) are accessible
- When `natural_language_intent` is provided, it must be translated to framework vocabulary before evaluating routing questions. The translation must be documented in the output.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `work_context` | Yes | Description of the work request, incident, or decision |
| `user_responses` | Yes | Answers to the routing questions from decision tables J-ENTRY-1 and J-ENTRY-2 |
| `initiative_id` | No | If continuing an existing initiative, its ID |
| `natural_language_intent` | No | The user's original plain-language description of what they want to accomplish, before any framework translation |
| `project_directory` | No | Path to the consuming project (to check for existing ER) |

## Postconditions

- Exactly one entry point has been selected from the navigation map
- A preset (P1–P5) has been identified, or "custom" has been explicitly declared with justification
- The starting kit and first artifact to produce are named
- If a project directory was provided, ER existence has been checked
- Advisory cross-cutting kit relevance has been assessed

## Output

The tool produces structured output conforming to `initiative-router-template.md`.

## Constraints

- The tool **asks** routing questions from the navigation map decision tables — it does not invent its own criteria
- The tool **recommends** — it does not decide. Human confirmation is required before proceeding
- The tool does not generate artifacts or modify files
- The tool does not skip routing questions — all questions from J-ENTRY-1 and J-ENTRY-2 are evaluated
- The tool contains no references to specific implementations, environments, or vendor tools

## Error handling

| Condition | Behavior |
|-----------|----------|
| No routing question matches user context | Report: ambiguous entry point — recommend invoking `position-check` if initiative already in progress, or refining work context if new |
| Multiple entry points equally valid | Report all matching options with rationale; human chooses |
| Initiative ID provided but no ER found | Report: ER missing — recommend creating ER before proceeding |
| Navigation map not accessible | Report error: cannot route without navigation map |

## Hard gates

| Gate | Rule |
|------|------|
| `routing_questions_asked` | All routing questions from navigation-map.md J-ENTRY-1 and J-ENTRY-2 were evaluated |
| `single_entry_point_selected` | Exactly one entry point was selected (or multiple presented for human choice) |
| `preset_identified` | A preset (P1–P5) was identified, or "custom" was explicitly declared with justification |
| `starting_kit_identified` | The starting kit and first artifact are named |
| `er_existence_checked` | If a project directory was provided, ER existence was checked and status reported |
| `no_implementation_detail` | Output contains no implementation-specific references |
