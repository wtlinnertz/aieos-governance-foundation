# Briefing Distillation — Validator

## Purpose

Evaluate the output of the briefing distillation tool against the hard gates defined in `briefing-distillation-spec.md`. Produce a PASS/FAIL judgment. Do not help, suggest improvements, or expand scope.

## Inputs

1. The briefing output to evaluate
2. `docs/tools/briefing-distillation-spec.md` — the authoritative rules
3. The source artifact that was distilled (for cross-reference)

## Evaluation Process

Evaluate each hard gate independently.

### Gate 1: `source_identified`

- Briefing header contains source artifact ID, type, and frozen status
- All three fields are present and consistent with the source artifact
- Frozen date is present

### Gate 2: `no_new_information`

- Every claim in the briefing traces to specific source artifact content
- No statements that cannot be found in the source
- No interpretations, opinions, or recommendations added

### Gate 3: `key_decisions_complete`

- Compare Key Decisions table against source artifact's decision sections
- All major decisions are represented
- No decision is omitted (even if summarized aggressively)

### Gate 4: `scope_boundaries_present`

- Both in-scope and out-of-scope/non-goals sections are populated
- Or explicitly stated as "not defined in source" if the source artifact lacks scope boundaries

### Gate 5: `fidelity_preserved`

- No decision is reversed, softened, or reframed in a way that changes its meaning
- Technical terms are preserved from the source (not rephrased into generic language)
- Constraints are not weakened or made conditional when they are absolute in the source

### Gate 6: `length_constraint`

- Word count does not exceed stated budget
- Word count is accurately reported in the briefing header

## Output Format

```json
{
  "status": "PASS | FAIL",
  "summary": "<one-sentence verdict>",
  "hard_gates": {
    "source_identified": "PASS | FAIL",
    "no_new_information": "PASS | FAIL",
    "key_decisions_complete": "PASS | FAIL",
    "scope_boundaries_present": "PASS | FAIL",
    "fidelity_preserved": "PASS | FAIL",
    "length_constraint": "PASS | FAIL"
  },
  "blocking_issues": [
    {
      "gate": "<gate_name>",
      "description": "<what is wrong>",
      "location": "<section reference>"
    }
  ],
  "warnings": [
    {
      "description": "<non-blocking observation>",
      "location": "<section reference>"
    }
  ],
  "completeness_score": "<0-100>"
}
```

## Rules

- Do not suggest fixes or improvements to the briefing output
- Do not expand scope beyond what the spec requires
- Evaluate only against the hard gates
- Do not evaluate the quality of the summarization — only whether the output meets structural and fidelity requirements
