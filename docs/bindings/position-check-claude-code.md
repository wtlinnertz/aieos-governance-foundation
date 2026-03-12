# Position Check — Claude Code Binding

This binding maps the abstract `TOOL-POSITION-CHECK` capability to a concrete implementation using Claude Code.

## Tool Reference

- **Tool Spec:** `docs/tools/position-check-spec.md`
- **Tool Template:** `docs/tools/position-check-template.md`

## Implementation

In a Claude Code session, the position-check capability is exercised by reading ground truth files.

### Execution Steps

1. Read the Engagement Record at the provided path using the `Read` tool
2. Use the `Glob` tool to discover all artifact files in the artifact directory
3. For each discovered artifact, read the Document Control section to extract status
4. Read `docs/navigation-map.md` to identify the expected artifact sequence for the active preset
5. Compare the artifact inventory against the navigation map to identify the current position
6. Identify the next action from the navigation map's outgoing edges
7. Run anomaly checks (navigation-map.md Section 4) against the inventory
8. Produce the position report following the template format

### Status Extraction

| Document Control Value | Mapped Status |
|----------------------|---------------|
| `Status: Frozen` | Frozen |
| `Status: Freeze Pending` | In Progress |
| `Status: Draft` | In Progress |
| `Status: Validated` | In Progress |
| Field missing | Unknown (flag as anomaly) |
| File not found | Missing |

### Environment Notes

- Claude Code reads files directly via the `Read` tool
- Claude Code uses the `Glob` tool to discover artifact files
- The binding reads actual file content — it does not rely on cached state
- No external API calls needed

## What This Binding Does Not Define

This binding does not define policy. The position derivation rules, anomaly patterns, and hard gates are defined in `position-check-spec.md` and `navigation-map.md`. This file only describes how those rules are executed in the Claude Code environment.
