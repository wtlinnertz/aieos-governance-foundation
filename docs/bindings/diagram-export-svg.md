# Diagram Export — SVG Binding

This binding maps the abstract `TOOL-DIAGRAM-EXPORT` capability to SVG (Scalable Vector Graphics) format.

## Tool reference

- **Tool Spec:** `docs/tools/diagram-export-spec.md`
- **Tool Template:** `docs/tools/diagram-export-template.md`

## Input mapping

| Tool Input | SVG Rendering |
|------------|---------------|
| Mermaid code block content | Passed as stdin or temp file to `mmdc -i {input} -o {output} -f svg` |
| `diagram_filter` | Selects which Mermaid blocks to render |
| `artifact_id` | Used in output filename: `{artifact_id}-diagram-{N}.svg` |

## Rendering approach

This binding delegates to Mermaid CLI (`mmdc`) or an equivalent Mermaid rendering library. The binding does not implement its own Mermaid parser — it uses Mermaid's native SVG rendering pipeline. All Mermaid diagram types (flowchart, sequence, state, class, ER, Gantt, pie, etc.) are supported through the upstream renderer.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Theme | `default` | Mermaid theme (`default`, `dark`, `forest`, `neutral`) |
| Background | `transparent` | SVG background color |
| Width | `auto` | Maximum width in pixels (`auto` = content-sized) |

## ID derivation

The output file is named `{artifact_id}-diagram-{N}.svg` where `{N}` is the 1-based index of the diagram within the artifact. The adapter generates one `.svg` file per Mermaid code block selected by the filter.

## Adapter environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MERMAID_CLI_PATH` | No | Path to `mmdc` binary. If not set, the adapter searches `PATH`. |

## Adapter conformance reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is output-only (generates `.svg` files from Mermaid source; does not modify original artifacts).

## What this binding does not define

This binding does not define policy. The rules for when to export diagrams (preconditions, postconditions, constraints, hard gates) are defined in `diagram-export-spec.md`. Quality gates for the export are defined in the validator. This file only describes how Mermaid source is rendered to SVG format and the configuration options available.

If the organization prefers a different vector format, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
