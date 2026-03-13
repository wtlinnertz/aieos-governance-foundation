# Work Item Sync Tool Prompt

You are invoking the work-item-sync tool capability.

## When to Invoke

Invoke this tool **after a WDD is frozen** and work items need to be created in an external work tracking system. Typical invocation points:

- After freezing a WDD, to populate the project tracker with work items
- After a WDD re-entry and re-freeze, to update existing tracker items with revised scope

## Why to Invoke

A frozen WDD is the authoritative breakdown of implementation work. Syncing it to an external tracker ensures the team's day-to-day work management reflects the governed plan. This tool ensures the sync is auditable, idempotent, preserves group structure, and does not modify the source WDD.

## Execution Instructions

1. Verify the WDD is frozen by reading its Document Control section
2. Parse the WDD to enumerate all work groups and work items
3. Read the binding for the target system to determine field mappings and adapter configuration
4. For each work group, invoke the adapter's `push` operation to create or update the parent/epic item
5. For each work item, invoke the adapter's `push` operation to create or update the tracker item, linking it to its group's parent item
6. Record all external IDs returned by the adapter
7. Produce output conforming to `work-item-sync-template.md`

## Result Interpretation

- **PASS**: All work items and groups were synced successfully. External IDs are recorded and the source WDD is unmodified.
- **FAIL**: One or more items could not be synced. Check the Item Mapping Table and Audit Entries for specific failures. A partial sync (some items succeeded, others failed) is still a FAIL — all items must sync for a PASS.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `work-item-sync-spec.md`.
