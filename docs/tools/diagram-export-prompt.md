# Diagram Export Tool Prompt

You are invoking the diagram-export tool capability.

## When to invoke

Invoke this tool **after an artifact containing Mermaid diagrams needs visual exports** for external consumption. Typical invocation points:

- After freezing an artifact containing Mermaid diagrams (SAD, TDD, architecture docs)
- When teams need visual representations for external systems (architecture review tools, presentation slides, knowledge bases)
- During DKK (Documentation & Knowledge Kit) work when user-facing documentation needs rendered diagrams
- When preparing content for import into enterprise architecture tools

## Why to invoke

Visual representations aid cross-team understanding, support non-technical teams, and enable integration with enterprise architecture management tools. Mermaid source remains the governed format; exports are renderings for consumption. This tool ensures the extraction is auditable, traceable, idempotent, and does not modify the source artifact.

## Execution instructions

1. Read the source artifact and compute its file hash (SHA256)
2. Extract all Mermaid code blocks (identify by fenced code blocks with `mermaid` language tag). Record the heading context (nearest `##` heading above each block) and assign 1-based indices
3. Read the binding document for the requested output format to determine concrete format, field mappings, and rendering rules
4. For each Mermaid block (or filtered subset): transform per binding rules and write to output directory with traceable naming (`{artifact_id}-diagram-{N}.{ext}`)
5. Compute source artifact file hash again — verify identical to step 1
6. Produce export record conforming to `diagram-export-template.md`

## Result interpretation

- PASS: All blocks exported successfully, source unmodified.
- PARTIAL: Some blocks exported, some skipped (syntax errors or filter mismatch). Check per-diagram results.
- FAIL: No blocks exported. Check the error field in the audit entry for the specific failure reason.

## Spec reference

The authoritative rules, constraints, and hard gates for this tool are defined in `diagram-export-spec.md`.
