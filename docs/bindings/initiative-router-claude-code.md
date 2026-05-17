# Initiative Router — Claude Code Binding

This binding maps the abstract `TOOL-INITIATIVE-ROUTER` capability to a concrete implementation using Claude Code.

## Tool reference

- **Tool Spec:** `docs/tools/initiative-router-spec.md`
- **Tool Template:** `docs/tools/initiative-router-template.md`

## Implementation

In a Claude Code session, the initiative-router capability is exercised as an interactive conversation.

### Execution steps

1. Read `docs/navigation-map.md` Section 3 decision tables J-ENTRY-1 and J-ENTRY-2
2. Ask the user each routing question from J-ENTRY-1, one at a time
3. Based on answers, evaluate which entry point conditions are met
4. Ask context factors from J-ENTRY-2 to identify the preset
5. If a project directory is known, use the `Read` tool to check for an ER at `docs/engagement/er-*.md`
6. Produce the routing record following the template format
7. Present the recommendation and wait for user confirmation

### Interactive pattern

Unlike batch tools, the initiative-router is conversational. The AI asks questions, listens to answers, and adapts follow-up questions based on responses. This is the "sherpa greeting" — the first interaction when entering AIEOS.

### Environment notes

- Claude Code reads files directly via the `Read` tool
- Claude Code uses the `Glob` tool to search for existing ERs
- No external API calls needed
- The binding assumes the standard AIEOS monorepo layout

## What this binding does not define

This binding does not define policy. The routing rules and decision criteria are defined in `initiative-router-spec.md` and `navigation-map.md`. This file only describes how those rules are exercised in the Claude Code environment.
