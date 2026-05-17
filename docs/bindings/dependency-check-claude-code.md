# Dependency Check — Claude Code Binding

This binding maps the abstract `TOOL-DEPENDENCY-CHECK` capability to a concrete implementation using Claude Code.

## Tool reference

- **Tool Spec:** `docs/tools/dependency-check-spec.md`
- **Tool Template:** `docs/tools/dependency-check-template.md`

## Implementation

In a Claude Code session, the dependency-check capability is exercised as follows:

### Input mapping

| Tool Input | Claude Code Action |
|------------|-------------------|
| `target_artifact_type` | Provided by the operator or inferred from the playbook step |
| `kit_name` | Determined from the current working kit |
| `artifact_directory` | The project's `docs/sdlc/` directory |

### Execution steps

1. Read the target artifact's spec file (`docs/specs/{type}-spec.md`) to identify the "Upstream Dependencies" section
2. For each listed upstream artifact type, search the project's artifact directory for the corresponding file
3. Read each upstream artifact's Document Control section and check the `Status` field
4. Produce output following the template format

### Status determination

| Document Control Status Value | Reported Freeze Status |
|------------------------------|----------------------|
| `Frozen` | Frozen |
| `Freeze Pending` | Unfrozen |
| `Draft` | Unfrozen |
| `Approved` / `Validated` | Unfrozen |
| Field missing or unrecognizable | Unfrozen |
| File not found | Missing |

### Environment notes

- Claude Code reads files directly via the `Read` tool
- No external API calls or database queries are needed
- The binding assumes the standard AIEOS directory layout

## What this binding does not define

This binding does not define policy. The rules for what constitutes a valid dependency check (preconditions, postconditions, constraints, hard gates) are defined in `dependency-check-spec.md`. This file only describes how those rules are implemented in the Claude Code environment.

If the implementation environment changes (e.g., from Claude Code to a CI pipeline script), this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
