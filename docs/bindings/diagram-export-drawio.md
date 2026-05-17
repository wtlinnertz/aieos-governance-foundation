# Diagram Export — draw.io Binding

This binding maps the abstract `TOOL-DIAGRAM-EXPORT` capability to draw.io XML format.

## Tool reference

- **Tool Spec:** `docs/tools/diagram-export-spec.md`
- **Tool Template:** `docs/tools/diagram-export-template.md`

## Input mapping

| Tool Input | draw.io Mapping |
|------------|-----------------|
| Mermaid code block content | Parsed and converted to draw.io XML (`<mxGraphModel>` document) |
| `diagram_filter` | Selects which Mermaid blocks to convert |
| `artifact_id` | Used in output filename: `{artifact_id}-diagram-{N}.drawio` |

## Mermaid-to-draw.io mapping

| Mermaid Construct | draw.io XML Mapping | Notes |
|-------------------|---------------------|-------|
| `graph LR` | `<mxGraphModel>` with horizontal layout | Left-to-right flow |
| `graph TB` / `graph TD` | `<mxGraphModel>` with vertical layout | Top-to-bottom flow |
| `A["Label"]` or `A[Label]` | `<mxCell vertex="1" value="Label">` with rectangle style | Standard node |
| `A("Label")` | `<mxCell>` with rounded rectangle style | Rounded node |
| `A{"Label"}` | `<mxCell>` with rhombus/diamond style | Decision node |
| `A(("Label"))` | `<mxCell>` with ellipse style | Circle/start-end node |
| `A --> B` | `<mxCell edge="1" source="A" target="B">` | Solid arrow |
| `A -.-> B` | `<mxCell edge="1">` with dashed style | Dashed arrow |
| `A ==> B` | `<mxCell edge="1">` with thick style | Thick arrow |
| `A -->\|"text"\| B` | `<mxCell edge="1" value="text">` | Labeled edge |
| `subgraph Title` | `<mxCell>` container with child cells | Swimlane/group |
| `classDef name fill:#color` | `style="fillColor=#color"` on matching cells | Color mapping |
| `class A,B name` | Apply classDef style to cells A, B | Class application |
| Sequence `participant` | Vertical lifeline `<mxCell>` | Actor lane |
| Sequence `->>`/`->>` | Horizontal arrow between lifelines | Message |
| State `[*]` | Start/end circle node | State machine |
| State `-->` | Transition arrow | State transition |

## Layout rules

- Nodes positioned on a grid (120px horizontal spacing, 80px vertical spacing)
- Subgraph containers get 20px padding around children
- Edge routing: orthogonal (right-angle connectors) for flowcharts, direct for sequence diagrams
- Default node size: 120x60px (rectangle), 80x80px (diamond), 60x60px (circle)
- Font: Helvetica 12pt (draw.io default)

## Styling defaults

| Element | Fill Color | Stroke Color |
|---------|-----------|--------------|
| Standard node | `#dae8fc` (light blue) | `#6c8ebf` |
| Decision node | `#fff2cc` (light yellow) | `#d6b656` |
| Subgraph container | `#f5f5f5` (light gray) | `#666666` |
| Edge | — | `#333333` |

## ID derivation

The output file is named `{artifact_id}-diagram-{N}.drawio` where `{N}` is the 1-based index of the diagram within the artifact. The adapter generates one `.drawio` file per Mermaid code block selected by the filter.

## Adapter environment variables

None. This binding performs file generation only — no API calls are required.

## Import instructions

| Tool | Steps |
|------|-------|
| draw.io / diagrams.net | File > Open > select `.drawio` file |
| LeanIX Free Draw | Open diagram > File > Import From > Device > select `.drawio` file |
| VS Code | Install Draw.io Integration extension > double-click `.drawio` file |

## Adapter conformance reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is output-only (generates `.drawio` files; does not read or sync from draw.io).

## What this binding does not define

This binding does not define policy. The rules for when to export diagrams (preconditions, postconditions, constraints, hard gates) are defined in `diagram-export-spec.md`. Quality gates for the export are defined in the validator. LeanIX fact sheet linking is a LeanIX-specific concern outside the scope of diagram export. This file only describes how Mermaid constructs map to draw.io XML elements and configuration.

If the organization migrates from draw.io to another diagramming tool, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
