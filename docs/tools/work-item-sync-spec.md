# Work Item Sync Tool Spec

Version: v1.0

Tool ID: TOOL-WORK-ITEM-SYNC

## Purpose

Synchronizes work items from a frozen WDD to an external work tracking system. Each WDD work item becomes a corresponding tracker item; work group structure is preserved as parent/child relationships in the tracker.

## Preconditions

- The WDD is frozen (Status: Frozen in Document Control)
- Work items are enumerable from the WDD content
- The target tracker is configured via a binding (field mapping and adapter environment documented)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `wdd_artifact_id` | Yes | The AIEOS WDD artifact ID (e.g., `WDD-TASKFLOW-001`) |
| `wdd_path` | Yes | Path to the WDD artifact file |
| `target_system` | Yes | Abstract target identifier — the binding resolves this to a concrete tracker |

## Postconditions

- Each WDD work item has a corresponding item in the external tracker
- External IDs are mapped back to WDD item IDs
- Work group structure is preserved (groups → epics or parent issues in the tracker)
- Work item dependencies declared in the WDD are represented as tracker links
- An audit log entry has been produced for each sync operation
- The source WDD file is unmodified

## Output

The tool produces structured output conforming to `work-item-sync-template.md`.

## Constraints

- Only frozen WDDs may be synced — syncing a non-frozen WDD is a hard gate failure
- Push-only — this tool creates/updates tracker items; it does not read tracker status back into the WDD
- Source unmodified — the tool does not alter the WDD file in any way
- Idempotent — re-syncing the same WDD to the same tracker updates existing items rather than creating duplicates
- Preserves work item dependencies — if the WDD declares dependencies between items, these are represented as links in the tracker
- The tool contains no references to specific trackers, APIs, or environments

## Error Handling

| Condition | Behavior |
|-----------|----------|
| WDD not found at path | Report error: WDD file not found |
| WDD not frozen | Report error: WDD status is not Frozen — sync blocked |
| Target tracker not configured | Report error: no binding found for target system |
| External tracker unreachable | Report error: adapter health check failed — sync blocked |
| Partial sync (some items synced, others failed) | Report partial: list successful and failed items; overall status is FAIL |
| Work group creation failed | Report error: group structure could not be established — item sync continues but group mapping shows failure |

## Hard Gates

| Gate | Rule |
|------|------|
| `wdd_frozen_check` | The WDD's Document Control section shows Status: Frozen |
| `all_items_synced` | Every work item in the WDD has a corresponding tracker item |
| `external_ids_mapped` | Every synced item has a recorded external ID |
| `group_structure_preserved` | WDD work groups are represented as parent/epic items in the tracker with correct child relationships |
| `audit_logged` | A structured audit log entry was produced for each sync operation |
| `source_unmodified` | The WDD file's content hash is identical before and after the operation |
| `idempotent_behavior` | Re-syncing the same WDD updates existing tracker items rather than creating duplicates |
