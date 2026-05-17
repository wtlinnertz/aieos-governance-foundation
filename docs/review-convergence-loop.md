# Review Convergence Loop

This document defines how an autonomous agent corrects artifacts that fail validation or peer review, iterates within bounded limits, and escalates to a human when convergence is not achieved. It provides operational patterns for closing the generate → validate → correct loop without requiring human intervention at each iteration.

These are workflow patterns, not tool definitions. No four-file tool set is required.

---

## Terms

| Term | Definition |
|------|-----------|
| **Convergence loop** | A bounded sequence of correction and re-validation attempts that runs after an artifact fails validation or peer review. The loop terminates when the artifact passes or iteration limits are reached. |
| **Correction session** | A fresh AI session that re-generates the artifact with additional constraints derived from validation findings. Correction sessions are always separate from validation sessions. |
| **Correction constraint set** | The set of blocking issues or required remediations from the most recent validation or review, packaged as mandatory fix targets for the correction session. |
| **Convergence criteria** | The conditions under which the loop terminates successfully. At minimum: all hard gates PASS. |
| **Iteration ledger** | A running record of each correction attempt: what findings triggered it, what changes were made, what the result was. Created on first FAIL, updated each cycle. |
| **Oscillation** | A pathological loop state where fixing finding A causes finding B, and fixing finding B causes finding A. Detected by comparing iteration ledger entries. |
| **Staleness** | A pathological loop state where the same finding persists across iterations with unchanged description. The correction is not making progress. |

---

## Core invariants

These rules apply to both patterns:

1. **Session separation preserved** — Correction and validation always run in separate AI sessions. A correction session never validates its own output.
2. **Validators do not help** — Validators produce findings only. They do not suggest fixes, redesign artifacts, or expand scope. This is unchanged from the governance model (§13).
3. **Correction is re-generation with additional constraints** — The correction session re-invokes the original generation prompt with the correction constraint set prepended. It does not edit the failed artifact in place.
4. **Upstream intent re-verified every iteration** — Each correction session re-reads the frozen upstream artifacts to confirm the corrected output still satisfies upstream intent. Drift from upstream intent is a stopping condition.
5. **Minimality** — The correction session makes the smallest change that addresses the blocking findings. It does not improve, refactor, or expand beyond the specific issues identified.
6. **Correction session never validates its own output** — After correction, a separate validation session evaluates the result. This is a restatement of invariant 1 for emphasis.
7. **Iteration is bounded** — Every convergence loop has a hard maximum of 3 iterations. There is no mechanism to extend this limit within the loop. Failure to converge within the limit triggers escalation.

---

## Pattern a: validator convergence loop

**Scope:** Any artifact, any kit. Applies whenever a validator returns FAIL.

### Trigger

A validator returns `status: FAIL` with one or more entries in `blocking_issues`.

### Correction session inputs

| Item | Source |
|------|--------|
| Current artifact (failed version) | The artifact that failed validation |
| Spec | `docs/specs/{type}-spec.md` for the artifact type |
| Template | `docs/artifacts/{type}-template.md` for the artifact type |
| Upstream frozen artifacts | All frozen artifacts that were inputs to the original generation |
| Blocking issues | `blocking_issues` array from the validator output |
| Generation prompt (correction mode) | The original `docs/prompts/{type}-prompt.md` with correction preamble |

### Correction mode

The generation prompt is re-invoked with a constraint preamble prepended to the normal inputs. The preamble contains:

1. **Blocking issues as mandatory fix targets** — Each blocking issue from the validator output, listed as a constraint the correction must satisfy.
2. **Minimality constraint** — "Make the smallest changes necessary to resolve the blocking issues. Do not improve, refactor, or expand scope beyond what is required to pass the failing gates."
3. **Intent re-verification** — "Before generating the corrected artifact, re-read the upstream frozen artifacts and confirm that the correction does not drift from upstream intent."

The correction session produces a complete, corrected artifact — not a diff or patch.

### Re-Validation

The corrected artifact is validated in a **separate session** using the same validator and spec. The correction session is not involved.

### Convergence

The loop converges when all hard gates return PASS. The corrected artifact proceeds to freeze pending (human review).

This pattern corresponds to the **Remediate-and-Retry** outcome in the Decision Outcome Taxonomy (see `flow-reference.md` §11). The decision to enter a convergence loop — rather than blocking or escalating — is made by the operator or orchestrating agent when validator findings are judged to be correctable within the current artifact scope.

### Stopping rules

The loop stops — without convergence — under any of these conditions:

| Condition | Detection | Action |
|-----------|-----------|--------|
| **Max iterations reached** | 3 correction-validation cycles completed without convergence | Escalate |
| **Staleness** | Same gate failing with the same or equivalent description across 2 consecutive iterations | Escalate |
| **Oscillation** | Fix for finding A introduces finding B; fix for finding B reintroduces finding A | Escalate |
| **Upstream root cause** | Blocking issue traces to ambiguity or error in an upstream frozen artifact, not the current artifact | Escalate (upstream re-entry, not local correction) |

### Escalation

When the loop fails to converge, produce a structured escalation report:

- **Artifact ID** and type
- **Iteration count** (how many cycles ran)
- **Full iteration ledger** (see below)
- **Remaining blocking issues** (from the last validator output)
- **Assessment** — one of: `staleness` (same issue persists), `oscillation` (fixes conflict), `upstream_root_cause` (problem is not in this artifact), `iteration_limit` (exhausted attempts without clear pattern)

The escalation report is delivered to the human operator. The artifact remains in Draft status until the human resolves the issue.

---

## Pattern b: PRK review convergence loop

**Scope:** Artifacts that undergo peer review via the Peer Review Kit (Layer 14). Applies when a PRR returns FAIL disposition.

### Trigger

A frozen PRR has `FAIL` disposition. PRR §6 Required Remediations lists the blocking findings that must be addressed.

### Correction session inputs

| Item | Source |
|------|--------|
| Current artifact (reviewed version) | The artifact that received a FAIL PRR |
| Spec | `docs/specs/{type}-spec.md` for the artifact type |
| Template | `docs/artifacts/{type}-template.md` for the artifact type |
| Upstream frozen artifacts | All frozen artifacts that were inputs to the original generation |
| Required remediations | PRR §6 Required Remediations (blocking findings from all lenses) |
| Generation prompt (correction mode) | The original prompt with correction preamble (same structure as Pattern A) |

### Correction flow

1. **Correct** — Run a correction session with PRR §6 Required Remediations as the correction constraint set. Produce a corrected artifact.
2. **Own validator** — Validate the corrected artifact against its own validator. If FAIL, run Pattern A (validator convergence) before proceeding. The artifact must pass its own validator before re-entering PRK.
3. **Re-execute affected lenses only** — Lenses whose findings were all "no issue" or below the blocking threshold in the original PRR carry forward unchanged. Only lenses that contributed blocking findings are re-executed against the corrected artifact.
4. **New PRR** — Generate a new PRR from the updated lens outputs (re-executed + carried forward). Validate the PRR.

### Convergence

The loop converges when the new PRR returns PASS disposition. The corrected artifact and its PRR proceed to freeze pending.

Pattern B also maps to **Remediate-and-Retry** in the Decision Outcome Taxonomy. When PRR findings are correctable without redesign, the artifact enters this bounded correction loop. If convergence fails (3 iterations), the outcome escalates to **Block** (human must intervene) or **Require-Redesign** (upstream artifact must change).

### Affected lens determination

A lens is "affected" if it contributed at least one finding at critical or high severity in the original PRR. Unaffected lenses carry forward their original outputs without re-execution. This prevents redundant work while ensuring all blocking concerns are re-evaluated.

### Conflict handling

If two lenses oscillate across iterations — lens A's remediation creates a finding for lens B, and lens B's remediation creates a finding for lens A — the loop stops and escalates to a human with both lens perspectives. The human resolves the conflict by making a design decision that satisfies both concerns, or by accepting one lens's finding as a known tradeoff.

### Stopping rules

| Condition | Detection | Action |
|-----------|-----------|--------|
| **Max iterations reached** | 3 full B-loop iterations (correct → validate → re-execute lenses → new PRR) without convergence | Escalate |
| **Oscillation across lenses** | Remediation for lens A creates a new blocking finding from lens B, and vice versa | Escalate with both perspectives |
| **New critical findings** | A re-executed lens surfaces a critical finding not present in any previous PRR for this artifact | Escalate (the correction introduced a new problem) |

### Escalation

When Pattern B fails to converge, the escalation report includes:

- Everything from Pattern A's escalation format
- PRR version history (all PRR IDs generated during the convergence attempt)
- Lens-by-lens finding path (how each lens's findings changed across iterations)

---

## Iteration ledger

The iteration ledger tracks each correction attempt within a convergence loop. It is created on the first FAIL and updated each cycle.

### Structure

| Iteration | Input Findings | Changes Made | Result | Remaining Issues |
|-----------|---------------|-------------|--------|-----------------|
| 1 | Gate X FAIL: description; Gate Y FAIL: description | Changed §3 to add missing field; rewrote §5 constraint | FAIL — Gate X PASS, Gate Y FAIL | Gate Y: description |
| 2 | Gate Y FAIL: description | Restructured §5 to satisfy constraint | PASS — all gates passing | None |

### Lifecycle

- **Created:** When the first validator or PRR returns FAIL and the convergence loop begins.
- **Updated:** After each correction-validation cycle.
- **Retained:** If the loop converges successfully, the ledger is discarded (it served its operational purpose). If the loop escalates, the ledger is persisted as `{nn}-{artifact-type}-convergence-ledger.md` in the project's `docs/sdlc/` directory as an audit trail.
- **Not a governed artifact:** The ledger has no spec, template, prompt, or validator. It is a transient operational record.

---

## Convergence criteria hierarchy

Multiple levels of convergence criteria exist. Higher levels subsume lower levels.

| Level | Criteria | When It Applies |
|-------|----------|----------------|
| **Level 1 (mandatory)** | All hard gates PASS | Always — this is the minimum bar for any artifact |
| **Level 2 (recommended)** | `completeness_score` ≥ artifact-type threshold | When the organization has established quality thresholds per artifact type |
| **Level 3 (when PRK adopted)** | PRR PASS disposition | When PRK is adopted for the artifact's review point |
| **Level 4 (aspirational)** | Per-lens scores meet lens-specific thresholds | When the organization has established per-lens quality targets |

The convergence loop operates at Level 1 by default. Levels 2–4 are advisory — they guide iteration when Level 1 is already satisfied but may suggest further improvement. Only Level 1 blocking failures trigger the convergence loop.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Correction session seeing validator internals | Violates session separation; correction should respond to findings, not reverse-engineer the validator's logic |
| Self-validation | The session that produced the correction evaluates its own output; this is the same bias the governance model prohibits |
| Unbounded loops | Without iteration limits, the loop can run indefinitely, consuming resources and potentially degrading output quality |
| Correcting upstream problems locally | If the root cause is in a frozen upstream artifact, local correction masks the real issue and creates drift from upstream intent |
| Scope expansion during correction | The correction session adds capabilities or content beyond what the blocking findings require; this introduces new untested surface area |
| Skipping re-validation | After correction, the artifact must be re-validated. Assuming the fix worked without verification violates the generate-validate separation |
| Re-executing all lenses when only some had findings | Wastes resources and creates risk of new findings from previously-passing lenses destabilizing the convergence |
| Merging correction and generation sessions | Correction must run in a fresh session with the correction constraint set. Reusing the original generation session carries forward context that may reproduce the original errors |

---

## Relationship to other documents

| Document | Relationship |
|----------|-------------|
| [`governance-model.md`](../../aieos-governance-foundation/governance-model.md) §6 | Convergence loops operate within the Artifact Promotion Model. They automate the Draft → Validated transition. Freeze-before-promote and human freeze approval are unchanged. |
| [`governance-model.md`](../../aieos-governance-foundation/governance-model.md) §13 | Process invariant 8a defines bounded correction loops as a kit invariant. |
| [`flow-reference.md`](flow-reference.md) §10 | Flow validation rule 10 states correction loops are bounded. |
| [`aieos-engineering-execution-kit/docs/playbook.md`](../../aieos-engineering-execution-kit/docs/playbook.md) Phase 3 | EEK Phase 3 iteration rules (max 3 fix attempts, staleness detection, structured failure feedback) are a specific instance of Pattern A applied to code execution. |
| [`aieos-peer-review-kit/docs/playbook.md`](../../aieos-peer-review-kit/docs/playbook.md) Step 3 | PRK Step 3 FAIL handling describes the human-gated correction cycle. Pattern B automates this with bounded iteration and structured escalation. |
| [`sub-agent-orchestration.md`](sub-agent-orchestration.md) | Orchestration defines how parallel sub-agents are managed. Convergence defines how failed outputs are corrected. They are complementary: an orchestrator may invoke a convergence loop when a sub-agent's output fails validation. |
| [`tool-governance-spec.md`](tool-governance-spec.md) | Convergence is a pattern, not a tool. It does not require a four-file tool set. |
