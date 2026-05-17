# Handoff Navigator Tool Spec

Version: v1.0

Tool ID: TOOL-HANDOFF-NAVIGATOR

## Purpose

After a kit's exit condition is met, routes the initiative to the next kit(s). Verifies exit conditions, identifies the downstream kit, references the entry-from file, lists the handoff artifacts, and checks for cross-cutting kit activations.

## Preconditions

- The current kit's final artifact is frozen (exit condition met)
- The navigation map (`navigation-map.md`) is accessible
- The downstream kit's entry-from file is accessible
- The Engagement Record is accessible

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `source_kit` | Yes | The kit being exited (e.g., "EEK") |
| `destination_kit` | Yes | The kit being entered (e.g., "REK") — if unknown, provide preset and the tool will determine it |
| `initiative_id` | Yes | The initiative identifier |
| `er_path` | Yes | Path to the Engagement Record |
| `artifact_directory` | Yes | Path to the project's artifact directory |
| `preset` | Yes | The active preset (P1–P5) |

## Postconditions

- The source kit's exit conditions have been verified as met
- The destination kit has been identified and its entry-from file has been cited
- The specific artifacts crossing the boundary have been listed with verified freeze status
- Any cross-cutting kit activations triggered by the current state have been identified
- The first action in the destination kit has been named

## Output

The tool produces structured output conforming to `handoff-navigator-template.md`.

## Constraints

- The tool verifies exit conditions against actual artifact status — it does not assume
- The tool references the downstream kit's entry-from file — it does not invent entry requirements
- The tool does not modify the ER or any artifacts
- The tool does not generate artifacts in the destination kit
- The tool contains no references to specific implementations, environments, or vendor tools

## Error handling

| Condition | Behavior |
|-----------|----------|
| Exit conditions not met (artifacts missing or unfrozen) | Report: exit conditions unmet — list blocking items |
| Destination kit entry-from file not found | Report error: missing boundary contract |
| Preset path does not include stated destination | Report: destination not in preset path — may indicate wrong preset or custom flow |
| Cross-cutting kit should have been activated but was not | Report advisory: missed activation |

## Hard gates

| Gate | Rule |
|------|------|
| `exit_conditions_verified` | The source kit's exit conditions are verified as met (all required artifacts frozen) |
| `next_kit_identified` | The destination kit is identified and consistent with the preset path |
| `entry_from_referenced` | The destination kit's entry-from file is cited with its required artifacts listed |
| `handoff_artifacts_listed` | The specific artifacts crossing the boundary are listed with verified freeze status |
| `cross_cutting_activation_checked` | Any cross-cutting kit activations triggered by the current state are identified (or explicitly stated as none) |
