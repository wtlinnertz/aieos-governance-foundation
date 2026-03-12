# Handoff Navigator — Claude Code Binding

This binding maps the abstract `TOOL-HANDOFF-NAVIGATOR` capability to a concrete implementation using Claude Code.

## Tool Reference

- **Tool Spec:** `docs/tools/handoff-navigator-spec.md`
- **Tool Template:** `docs/tools/handoff-navigator-template.md`

## Implementation

In a Claude Code session, the handoff-navigator capability is exercised by reading and cross-referencing multiple files.

### Execution Steps

1. Read the source kit's `docs/playbook.md` to identify exit conditions
2. Verify each exit condition by reading the actual artifact files and their Document Control sections
3. Read the destination kit's `docs/entry-from-{source}.md` to identify entry requirements
4. Cross-reference entry requirements against actual artifact statuses
5. Read `docs/navigation-map.md` cross-cutting trigger edges to check for missed activations
6. Read the Engagement Record to verify recorded statuses match file statuses
7. Produce the handoff record following the template format

### Kit Directory Discovery

The binding locates kit directories using the standard AIEOS monorepo layout:
- Source kit: `aieos-{layer-name}-kit/`
- Destination kit: `aieos-{layer-name}-kit/`
- Entry-from file: `{destination-kit}/docs/entry-from-{source-abbrev}.md`

### Environment Notes

- Claude Code reads files directly via the `Read` tool
- Claude Code uses the `Glob` tool to discover kit directories and entry-from files
- No external API calls needed
- The binding reads across multiple kit directories in a single session

## What This Binding Does Not Define

This binding does not define policy. The exit conditions, entry requirements, and cross-cutting activation rules are defined in `handoff-navigator-spec.md`, the kit playbooks, and `navigation-map.md`. This file only describes how those rules are verified in the Claude Code environment.
