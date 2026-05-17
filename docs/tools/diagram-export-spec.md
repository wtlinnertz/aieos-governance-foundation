# Diagram Export — Specification

Version: v1.0

Tool ID: TOOL-DIAGRAM-EXPORT

## Purpose

Extracts Mermaid diagram blocks from AIEOS artifacts and transforms them into target formats for external system consumption. The external system receives the rendered output; the AIEOS source remains unmodified.

## Preconditions

- The source artifact file exists and is readable
- The source artifact contains at least one Mermaid code block (fenced code block with `mermaid` language tag)
- The target output format is specified (abstract identifier — the binding resolves this to a concrete format)
- The output directory is writable (or defaults to the same directory as the source artifact)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `artifact_path` | Yes | Path to the source artifact file |
| `output_format` | Yes | Abstract format identifier — the binding resolves this to a concrete format |
| `output_directory` | No | Directory for output files (default: same directory as source artifact) |
| `diagram_filter` | No | Specific diagram index or heading label to export (default: all) |

## Postconditions

- One output file per exported Mermaid block
- Output files named: `{artifact_id}-diagram-{N}.{ext}` where N is 1-indexed and ext is binding-determined
- The source artifact file is byte-identical before and after the operation
- An export record is produced conforming to `diagram-export-template.md`

## Output

The tool produces structured output conforming to `diagram-export-template.md`.

## Constraints

- Read-only on source artifacts — the tool must never modify, annotate, or reformat the source file
- Idempotent — re-exporting with identical inputs overwrites previous outputs with identical content
- Format-agnostic — the spec defines extraction and traceability rules, not rendering rules. Rendering is a binding concern.
- No embedded diagrams — the tool extracts and transforms; it does not insert rendered diagrams back into the source artifact
- Mermaid blocks only — the tool does not process other diagram formats (PlantUML, ASCII art, etc.) from source artifacts
- The tool contains no references to specific platforms, rendering engines, or environments

## Error handling

| Condition | Behavior |
|-----------|----------|
| Artifact file not found | Error: "Artifact not found: {path}" — no output produced |
| No Mermaid blocks in artifact | Error: "No Mermaid diagram blocks found in {artifact_id}" — empty export record with 0 blocks |
| Output format not recognized | Error: "Format '{format}' has no registered binding" — no output produced |
| Output directory not writable | Error: "Cannot write to {directory}" — no output produced |
| Mermaid block has syntax error | Warning per-block: "Block {N} has syntax error: {detail}" — skip block, continue others |
| diagram_filter matches no block | Warning: "Filter '{filter}' matched no blocks" — empty export record |

## Hard gates

| Gate | Rule |
|------|------|
| `preconditions_defined` | Preconditions section present with artifact existence, Mermaid presence, format specified |
| `postconditions_defined` | Postconditions section present with output naming convention, source-unmodified guarantee, export record requirement |
| `input_defined` | Input table present with all fields, required/optional marked, descriptions provided |
| `output_defined` | Output references diagram-export-template.md |
| `constraints_defined` | Constraints section present with read-only, idempotent, format-agnostic, no-embed, mermaid-only rules |
| `error_handling_defined` | Error table covers all 6 error conditions with specific behavior |
| `binding_separation` | Spec contains zero references to specific platforms, file formats, rendering tools, or vendor names |
| `mermaid_extraction` | Spec defines how Mermaid code blocks are identified (fenced code blocks with mermaid language tag) |
| `source_unmodified` | Spec explicitly states source artifact must be byte-identical after operation |
| `output_traceable` | Spec defines output naming that traces each file to source artifact ID + diagram index |
