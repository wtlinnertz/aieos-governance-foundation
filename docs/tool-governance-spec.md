# Tool Governance Spec

Version: v1.0

This document defines the governance rules for tools within the AIEOS framework. Tools are abstract capabilities that AI agents or human operators may invoke during artifact production. They are governed by the same four-file system that governs artifacts, but they govern a **capability** rather than a **document**.

## What a tool is

A tool is a named, reusable capability with a defined interface contract. It has:

- **Preconditions** — what must be true before the tool can be invoked
- **Postconditions** — what the tool guarantees after successful execution
- **Input** — what the tool accepts
- **Output** — what the tool produces (structured format)
- **Constraints** — behavioral boundaries the tool must respect

A tool is **not** an implementation. The tool definition describes what the capability does and when to use it. How the capability executes in a specific environment is a binding concern (see §Relationship to Bindings).

## The four-File system for tools

Every tool type is governed by exactly four files, following the same separation of concerns as artifact four-files.

| File | Question | Responsibility |
|------|----------|---------------|
| **Spec** | What are the rules? | Preconditions, postconditions, constraints, error handling, hard gates for correct usage |
| **Template** | What is the output structure? | Output format definition — what the tool produces when invoked |
| **Prompt** | When and why should the AI invoke this? | Invocation intent, execution instructions, result interpretation |
| **Validator** | Was the tool used correctly? | Judgment on whether the tool produced compliant output and was invoked appropriately |

### Separation of concerns

- **Tool specs are the single source of truth** for what the tool must do. Prompts and validators reference tool specs — they never inline their own rules.
- **Tool templates define output structure, not behavior.** A tool template contains the output schema and field definitions. It does not contain invocation rules or constraints.
- **Tool prompts define invocation intent, not rules.** A tool prompt tells the AI when and why to invoke the tool. It references the spec for the actual rules.
- **Tool validators judge, they do not help.** A tool validator evaluates whether the tool was used correctly. It does not suggest alternative invocations or expand scope.

### Cross-References

```
Tool Prompt → references → Tool Spec (for invocation rules)
Tool Prompt → references → Tool Template (for expected output format)
Tool Validator → references → Tool Spec (for hard gates to evaluate)
```

No other cross-references are permitted.

## Directory convention

Tool four-file sets live in `docs/tools/` within each kit:

```
aieos-{layer-name}-kit/
  docs/
    tools/
      {tool-name}-spec.md
      {tool-name}-template.md
      {tool-name}-prompt.md
      {tool-name}-validator.md
```

The `docs/tools/` directory is **optional**. Not all kits will define tools. When present, four-file completeness is enforced — if a tool spec exists, the corresponding template, prompt, and validator must also exist.

All four tool files live in the same directory (`docs/tools/`), unlike artifact files which are distributed across `docs/specs/`, `docs/artifacts/`, `docs/prompts/`, and `docs/validators/`. This physical co-location reflects the fact that tool files describe a single cohesive capability.

## Naming convention

Tool files follow the pattern: `{tool-name}-{role}.md`

| File Type | Pattern | Example |
|-----------|---------|---------|
| Spec | `{tool-name}-spec.md` | `dependency-check-spec.md` |
| Template | `{tool-name}-template.md` | `dependency-check-template.md` |
| Prompt | `{tool-name}-prompt.md` | `dependency-check-prompt.md` |
| Validator | `{tool-name}-validator.md` | `dependency-check-validator.md` |

Tool names use lowercase kebab-case and describe capabilities (verbs or verb-noun phrases), not artifact types. This naming distinction prevents confusion with artifact four-file sets.

## Tool ID format

`TOOL-{TOOL-NAME}`

- `TOOL-NAME`: Uppercase kebab-case name matching the file prefix
- Tool IDs are framework-level, not per-initiative

Example: `TOOL-DEPENDENCY-CHECK`, `TOOL-SPEC-LOOKUP`

## Shared vs. kit-Specific tools

- **Shared tools** live in `aieos-governance-foundation/docs/tools/`. These are cross-kit capabilities used across multiple layers (e.g., dependency checking, spec lookup, engagement record updates).
- **Kit-specific tools** live in the respective kit's `docs/tools/`. These are capabilities specific to one layer's artifact production workflow.

When a kit-specific tool is later found useful across multiple kits, it should be promoted to governance-foundation following the same governance model change protocol (§15 of the governance model).

## Relationship to bindings

Tools follow the same policy-vs-implementation separation as all other AIEOS concepts:

- The **four-file set** defines the abstract capability — what, when, why, and judgment. This is **policy**.
- The **binding** maps the abstract capability to a concrete implementation. This is **implementation**.

Tool bindings live in `docs/bindings/` (the same location as other bindings) and follow the naming pattern `{tool-name}-{environment}.md` (e.g., `dependency-check-claude-code.md`).

The four-file set never references a specific implementation. The binding never defines policy. When the implementation environment changes, only bindings are updated — tool specs, templates, prompts, and validators remain unchanged.

When a tool capability needs to execute against an external API (e.g., publishing artifacts to a wiki, syncing work items to a tracker), a third layer is involved: the **adapter**. An adapter is executable code that implements the binding's field mapping against a concrete external system. Adapter code lives outside AIEOS kits. AIEOS defines the interface contract for adapters in `adapter-conformance-spec.md`. The three-layer model is: Tool Spec (policy) → Binding (mapping) → Adapter (code).

## Versioning

Tool specs follow the same versioning protocol as artifact specs, defined in `aieos-governance-foundation/docs/spec-file-standard.md`:

- Every tool spec carries a `Version:` field
- New tools start at `v1.0`
- Changes follow Minor / Significant / Breaking categories
- Validator and prompt references to the spec should be validated against the current spec version

## Validator output format

Tool validators produce JSON in the same schema as artifact validators (governance-model.md §5):

```json
{
  "status": "PASS | FAIL",
  "summary": "<one sentence verdict>",
  "hard_gates": { "<gate_name>": "PASS | FAIL" },
  "blocking_issues": [{ "gate": "", "description": "", "location": "" }],
  "warnings": [{ "description": "", "location": "" }],
  "completeness_score": "<0-100>"
}
```

This ensures existing test infrastructure and tooling works for tools without modification.

## Hard gates for tool spec compliance

Every tool spec must satisfy the following hard gates:

| Gate | Rule |
|------|------|
| `preconditions_defined` | The spec defines what must be true before the tool is invoked |
| `postconditions_defined` | The spec defines what the tool guarantees after execution |
| `input_defined` | The spec defines what the tool accepts as input |
| `output_defined` | The spec defines the structure and format of tool output |
| `constraints_defined` | The spec defines behavioral boundaries the tool must respect |
| `error_handling_defined` | The spec defines what happens when the tool encounters errors |
| `binding_separation` | The spec contains no implementation details — no references to specific tools, scripts, APIs, or environments |
