# Spec Lookup Tool Spec

Version: v1.0

Tool ID: TOOL-SPEC-LOOKUP

## Purpose

Retrieves and surfaces the relevant spec file for a given artifact type and kit. Ensures the AI agent works against the correct, current spec rather than relying on remembered or copy-pasted rules.

## Preconditions

- The target artifact type is known (e.g., "TDD", "PRD", "SLO")
- The kit is identified
- The kit's `docs/specs/` directory is accessible

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `artifact_type` | Yes | The artifact type to look up (e.g., "tdd", "prd") |
| `kit_name` | Yes | The kit containing the spec |
| `kit_directory` | Yes | Path to the kit root directory |

## Postconditions

- The correct spec file for the requested artifact type has been identified
- The spec file's full content has been returned
- The spec version has been extracted
- The hard gate names have been extracted

## Output

The tool produces structured output conforming to `spec-lookup-template.md`.

## Constraints

- The tool **returns** the spec — it does not **interpret** it
- The tool does not summarize, paraphrase, or abbreviate the spec content
- The tool does not evaluate whether the spec is well-written or complete
- The tool does not suggest which spec to use if the requested type is ambiguous — it reports an error
- The tool contains no references to specific implementations, environments, or vendor tools

## Error handling

| Condition | Behavior |
|-----------|----------|
| Artifact type not found in kit's specs directory | Report error: spec not found for type |
| Multiple specs match the artifact type | Report error: ambiguous match |
| Spec file exists but has no Version field | Report warning: version field missing; return content anyway |
| Kit directory does not exist | Report error: kit directory not found |

## Hard gates

| Gate | Rule |
|------|------|
| `correct_spec_identified` | The returned spec file matches the requested artifact type exactly |
| `full_content_returned` | The complete spec file content is included in the output — no truncation or summarization |
| `no_interpretation` | The output does not add commentary, analysis, or opinions about the spec content |
| `version_extracted` | The spec version field value is extracted and reported (or explicitly noted as missing) |
| `hard_gates_extracted` | The hard gate names from the spec are listed (or explicitly noted if none found) |
