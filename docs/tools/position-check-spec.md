# Position Check Tool Spec

Version: v1.0

Tool ID: TOOL-POSITION-CHECK

## Purpose

Determines "you are HERE" in the AIEOS flow. Reads the Engagement Record and artifact directory (ground truth), cross-references against the navigation map, and reports the current position, next action, and any anomalies.

This is the AI sherpa's compass — it can be invoked at any time to re-orient.

## Preconditions

- An initiative is in progress (at least one artifact exists or an ER has been created)
- The Engagement Record for the initiative is accessible
- The project's artifact directory is accessible
- The navigation map (`navigation-map.md`) is accessible

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `initiative_id` | Yes | The initiative identifier (e.g., "CONSOLE-001") |
| `er_path` | Yes | Path to the Engagement Record file |
| `artifact_directory` | Yes | Path to the project's artifact directory (e.g., `docs/sdlc/`) |
| `preset` | No | The preset in use (P1–P5), if known; derived from ER if not provided |

## Postconditions

- Every artifact in the initiative's scope has a verified status (Frozen / In Progress / Not Started / N/A)
- The current position node from the navigation map has been identified
- The next expected action has been named
- Any pending junction decisions have been listed
- Any anomalies have been detected and reported

## Output

The tool produces structured output conforming to `position-check-template.md`.

## Constraints

- The tool reads ground truth (ER + actual files) — it does not rely on memory or prior conversation
- The tool derives position from evidence — it does not ask the user where they think they are
- The tool reports anomalies — it does not fix them
- The tool does not modify the ER or any artifacts
- The tool contains no references to specific implementations, environments, or vendor tools

## Error Handling

| Condition | Behavior |
|-----------|----------|
| ER file not found | Report error: ER missing — recommend creating ER (PIK Step 1 or EEK Step 0) |
| Artifact directory not found | Report error: directory not found — confirm project path |
| ER references artifact not found in directory | Report anomaly: ER/directory inconsistency (see anomaly patterns) |
| Current state maps to no valid node | Report anomaly: unrecognized position — recommend invoking decision-router |
| Preset unknown and not derivable from ER | Report warning: preset unknown — position report is best-effort |

## Anomaly Detection

The tool checks for anomalies defined in navigation-map.md Section 4:

| Anomaly | Severity |
|---------|----------|
| Artifact exists without frozen upstream | Blocking |
| ER lists artifact as frozen but file not found | Blocking |
| ER artifact status inconsistent with file | Blocking |
| Current state maps to no valid node | Warning |
| Skipped node in sequence | Warning |
| Cross-cutting kit not activated when expected | Advisory |
| Stale position (no activity beyond expected cadence) | Advisory |

## Hard Gates

| Gate | Rule |
|------|------|
| `er_read` | The ER was read and its content is reflected in the output |
| `artifact_inventory_complete` | Every artifact in the initiative's scope has a verified status |
| `current_position_identified` | Exactly one current position node from the navigation map is identified |
| `next_action_identified` | The next expected action is named (artifact, decision, or handoff) |
| `anomalies_checked` | All anomaly patterns from navigation-map.md Section 4 were evaluated |
| `pending_decisions_listed` | Any pending junction decisions are listed (or "none" is explicitly stated) |
