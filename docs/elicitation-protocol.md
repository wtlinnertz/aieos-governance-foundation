# Elicitation Protocol

Version: v1.0

## Purpose

Named reasoning techniques applied before artifact generation to surface gaps, challenge assumptions, and strengthen output quality. This is a cross-cutting reference document — prompts cite it, but it is not a tool or artifact.

---

## When to Apply

- Before generating any artifact with 5+ hard gates
- When upstream artifacts contain assumptions marked "Untested" or "Partially Confirmed"
- When the artifact has significant downstream consumers (SAD, DPRD, ORD)

---

## Techniques

### 1. Pre-Mortem Analysis

"Assume this artifact already failed its hard gates or caused a downstream failure. Work backward: what are the 3 most likely causes?"

- Best for: SAD, RP, QGR (high-consequence artifacts)

### 2. First Principles Decomposition

"Strip away inherited context from upstream artifacts. What must be independently true for this artifact to be valid?"

- Best for: DPRD, TDD (artifacts that synthesize multiple inputs)

### 3. Inversion

"List the 5 surest ways to make this artifact fail validation. Verify none exist."

- Best for: Any artifact entering validation for the first time

### 4. Stakeholder Lens Rotation

"Re-read upstream inputs from 3 perspectives: end user, operator, security auditor. Note what each would flag as missing."

- Best for: DPRD, SAD, RP (multi-stakeholder artifacts)

### 5. Constraint Removal

"Temporarily remove the most restrictive constraint. What changes? Does the constraint deserve its weight, or is it over-constraining the solution space?"

- Best for: SAD, VER (design/evaluation artifacts with inherited constraints)

### 6. Assumption Surfacing

"List every implicit assumption this artifact makes that is NOT explicitly stated in any upstream artifact."

- Best for: VER, TDD, SRP (artifacts with many implicit assumptions)

---

## Output Convention

After applying a technique, include a brief Markdown comment at the end of the generated artifact:

```
<!-- Elicitation: [technique name] applied. Key insight: [one sentence]. -->
```

---

## Relationship to Existing Mechanisms

- Complements (does not replace) Intent Verification
- Complements (does not replace) `assumption-stress-test-prompt.md` (PIK utility)
- Operates before generation; convergence loops operate after validation failure
