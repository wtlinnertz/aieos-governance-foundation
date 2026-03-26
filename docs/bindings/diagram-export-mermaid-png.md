# Diagram Export — PNG Binding

This binding maps the abstract `TOOL-DIAGRAM-EXPORT` capability to PNG (raster) format.

## Tool Reference

- **Tool Spec:** `docs/tools/diagram-export-spec.md`
- **Tool Template:** `docs/tools/diagram-export-template.md`

## Input Mapping

| Tool Input | PNG Rendering |
|------------|---------------|
| Mermaid code block content | Passed as stdin or temp file to `mmdc -i {input} -o {output} -f png` |
| `diagram_filter` | Selects which Mermaid blocks to render |
| `artifact_id` | Used in output filename: `{artifact_id}-diagram-{N}.png` |

## Rendering Approach

This binding delegates to Mermaid CLI (`mmdc`) or an equivalent Mermaid rendering library, using the PNG output flag. Intended for contexts where vector formats are not supported — email attachments, Slack messages, PowerPoint slides, PDF embedding.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Scale | `2` | Pixel density multiplier (`2` = retina/HiDPI) |
| Theme | `default` | Mermaid theme (`default`, `dark`, `forest`, `neutral`) |
| Background | `white` | PNG background color (no transparency in PNG) |
| Width | `1200` | Maximum width in pixels |

## ID Derivation

The output file is named `{artifact_id}-diagram-{N}.png` where `{N}` is the 1-based index of the diagram within the artifact. The adapter generates one `.png` file per Mermaid code block selected by the filter.

## Adapter Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MERMAID_CLI_PATH` | No | Path to `mmdc` binary. If not set, the adapter searches `PATH`. |
| `DIAGRAM_SCALE` | No | Override scale factor (default: `2`) |

## Adapter Conformance Reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is output-only (generates `.png` files from Mermaid source; does not modify original artifacts).

## What This Binding Does Not Define

This binding does not define policy. The rules for when to export diagrams (preconditions, postconditions, constraints, hard gates) are defined in `diagram-export-spec.md`. Quality gates for the export are defined in the validator. This file only describes how Mermaid source is rendered to PNG format and the configuration options available.

If the organization prefers a different raster format, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
