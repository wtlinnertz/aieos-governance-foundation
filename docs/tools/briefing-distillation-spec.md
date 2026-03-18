# Briefing Distillation — Spec

**Tool ID:** TOOL-BRIEFING-DISTILLATION
Version: v1.0

---

## Purpose

Produce a structured, compressed briefing from a frozen artifact. Extracts key decisions, scope boundaries, constraints, risks, and interfaces into a format optimized for downstream AI prompt consumption. Distills only — does not analyze, evaluate, or recommend.

---

## Preconditions

- Source artifact is Frozen (or Validated if pre-freeze briefing is needed)
- Source artifact type is known
- Full source artifact text is provided

---

## Input

| Field | Required | Description |
|-------|----------|-------------|
| source_artifact | Yes | Full frozen artifact text |
| source_artifact_type | Yes | Artifact type (DPRD, SAD, ORD, QGR, etc.) |
| downstream_consumer | No | Kit/role consuming this briefing (tailors emphasis) |
| token_budget | No | Target max length (default: 500 words) |

---

## Postconditions

- Briefing produced conforming to template
- All major decisions from source represented
- No information invented beyond source content
- Length within token budget

---

## Constraints

- Distill only — do not analyze, evaluate, or recommend
- Do not add information not present in the source artifact
- Do not omit decisions to meet length — summarize more aggressively instead
- Preserve the artifact's own terminology (no rephrasing technical terms)
- No vendor-specific references
- If downstream_consumer specified, emphasize sections most relevant to consumer

---

## Error Handling

- Source artifact too short for meaningful distillation → return source as-is with note "Source artifact is already concise; no distillation needed"
- Source artifact type unknown → produce generic briefing using all template sections

---

## Hard Gates

| # | Gate | Rule |
|---|------|------|
| 1 | `source_identified` | Source artifact ID, type, and frozen status present in the briefing header. All present and consistent. |
| 2 | `no_new_information` | Every statement traces to specific source content. No statements that cannot be found in the source. |
| 3 | `key_decisions_complete` | All major decisions from the source are represented. No decision omitted. |
| 4 | `scope_boundaries_present` | Both in-scope and out-of-scope/non-goals documented (or explicitly stated as "not defined in source"). |
| 5 | `fidelity_preserved` | No decision is misrepresented, reversed, or softened in a way that changes its meaning. |
| 6 | `length_constraint` | Output within token budget (default 500 words). |
