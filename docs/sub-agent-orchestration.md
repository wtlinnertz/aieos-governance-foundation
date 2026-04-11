# Sub-Agent Orchestration Patterns

This document defines how an orchestrating agent (sherpa) delegates work to parallel sub-agents, packages context for each, tracks completion, and reconverges results. It provides operational guidance for executing the parallelism rules defined in [`flow-reference.md` §4.1](flow-reference.md#41-what-can-run-in-parallel).

These are workflow patterns, not tool definitions. The orchestrator follows these patterns procedurally — no four-file tool set is required.

---

## Terms

| Term | Definition |
|------|-----------|
| **Orchestrator** | The coordinating agent (sherpa) that manages fan-out, tracking, and reconvergence. The orchestrator does not generate or validate artifacts itself during orchestration. |
| **Sub-agent** | An independent AI session that receives a context package and produces a single output. Sub-agents do not communicate with each other. |
| **Context package** | The complete, self-contained set of inputs a sub-agent needs to do its work. A sub-agent must be able to operate using only its context package — no external lookups, no orchestrator queries. |
| **Reconvergence** | The point where the orchestrator collects all sub-agent outputs, validates completeness, and proceeds to the next step. |

---

## Core Invariants

These rules apply to all three patterns:

1. **Self-contained context packages** — Every sub-agent receives everything it needs. If a sub-agent would need to ask a question, the context package is incomplete.
2. **No cross-agent communication** — Sub-agents never see each other's outputs during execution. Cross-pollination happens only at reconvergence.
3. **Validate before reconverge** — Every sub-agent output must pass its applicable validator in a separate session before the orchestrator accepts it.
4. **Separate generation and validation sessions** — The sub-agent that generates output must not validate its own output. A distinct validation session is required.
5. **Track all agents to completion** — The orchestrator must account for every sub-agent it launched. No sub-agent may be silently dropped or forgotten. The orchestrator maintains a completion ledger: agent ID, status (running / passed / failed), and output reference.
6. **Orchestrator does not generate** — During active orchestration, the orchestrator coordinates. It does not also act as a sub-agent producing artifacts. Mixing roles causes context contamination.

---

## Pattern 1: Independent Lens Parallelism (PRK)

**When:** PRK Step 1 — lenses have been selected for a review point and are ready to execute.

**Reference:** [`aieos-peer-review-kit/docs/playbook.md`](../../aieos-peer-review-kit/docs/playbook.md) Step 1 — Execute Lens Tools.

### Context Package (per lens)

Each lens sub-agent receives:

| Item | Source |
|------|--------|
| Validated artifact under review | Full document (never summarized) |
| Context documents for this review point | Per the PRK playbook's Context Documents table |
| Lens tool spec | `docs/tools/review-{lens-name}-spec.md` |
| Lens tool template | `docs/tools/review-{lens-name}-template.md` |
| Lens tool prompt | `docs/tools/review-{lens-name}-prompt.md` |

No lens receives another lens's spec, template, prompt, or output.

### Independence

- Each lens runs in a separate AI session.
- No lens sees another lens's output until reconvergence.
- This prevents groupthink and ensures each perspective is authentic.

### Validation

Each lens output is validated in a **separate session** using the lens validator (`docs/tools/review-{lens-name}-validator.md`) and the lens spec.

### Reconvergence

1. All lens sub-agents complete and their outputs pass validation.
2. The orchestrator collects all validated lens outputs.
3. The orchestrator initiates PRR generation (Step 2) by packaging all validated lens outputs into a new generation session.

### Failure Handling

- **Single failure:** Re-execute the failed lens with the same context package. Investigate the cause (usually missing evidence or scope violation in the lens output).
- **Double failure (same lens):** Escalate to the review operator. The lens may require clarified context or the artifact may have gaps the lens cannot evaluate.
- **Validation failure:** The lens output is deficient, not the artifact. Re-execute the lens, not the upstream artifact.

---

## Pattern 2: Parallel-Safe Work Item Execution (EEK)

**When:** The execution plan marks work items within a work group as "parallel-safe" based on file overlap analysis, and the orchestrator is ready to begin the execution loop.

**Reference:** [`aieos-engineering-execution-kit/docs/playbook.md`](../../aieos-engineering-execution-kit/docs/playbook.md) Part 2 — The Execution Loop.

### Context Package (per work item)

Each work item sub-agent receives:

| Item | Source |
|------|--------|
| Work item context file | `{nn}-{wdd-item-id}-context.md` from the execution plan |
| Phase-specific prompt | The prompt for the current phase (tests, plan, code, or review) |
| Frozen upstream artifacts | TDD, SAD, and any other artifacts referenced by the work item |
| Prior phase outputs (if any) | For Phases 2–4, include this item's outputs from prior phases |

No work item sub-agent receives another item's context file or phase outputs.

### Two Execution Modes

#### Mode A: Phase-Synchronized (Safer)

All parallel items execute the same phase together, then gate, then advance:

```
All items: Phase 1 (Tests)  → human gate →
All items: Phase 2 (Plan)   → human gate →
All items: Phase 3 (Code)   → human gate →
All items: Phase 4 (Review) → work group gate
```

**Advantages:** Batched human approvals. Easier to detect emerging file overlaps before code is written. Human can redirect after seeing all test definitions or all plans together.

**When to use:** Default mode. Use when items touch related subsystems, when the team is new to parallel execution, or when human review bandwidth is limited.

#### Mode B: Fully Independent (Faster)

Each item runs all four phases autonomously without waiting for other items:

```
Item A: Phase 1 → Phase 2 → Phase 3 → Phase 4 ─┐
Item B: Phase 1 → Phase 2 → Phase 3 → Phase 4 ─┤→ work group gate
Item C: Phase 1 → Phase 2 → Phase 3 → Phase 4 ─┘
```

**Prerequisites (all must hold):**
- Execution plan confirms zero file overlap between items.
- Human has pre-approved all items' test definitions and plans (or has explicitly waived per-phase gates for this work group).
- Items touch genuinely independent subsystems.

**When to use:** When items are clearly independent (different packages, different services, no shared files) and the team has confidence in the execution plan's overlap analysis.

### Reconvergence

1. All work item sub-agents complete all phases.
2. The orchestrator runs the **work group gate**: full test suite regression check (all tests, not just this group's tests) + lint on all modified files.
3. On work group gate PASS: proceed to BAT (Business Acceptance Testing) for the work group.
4. On work group gate FAIL: diagnose which item(s) caused the regression; fix sequentially.

### Failure Handling

- **File overlap discovered during execution:** Stop both conflicting items immediately. The orchestrator re-sequences them as sequential (one completes before the other begins). Do not attempt to merge concurrent changes.
- **One item's plan rejected by human:** That item revises its plan. Other items continue unaffected. If the rejection changes scope (e.g., interface change), assess impact on other items before they proceed.
- **Test regression at work group gate:** Bisect by running each item's tests in isolation, then together, to identify the conflict. Fix the conflicting item and re-run the gate.

---

## Pattern 3: Provider/Consumer Contract Development (EEK)

**When:** The WDD identifies a provider/consumer pair — two work items that reference the same TDD §4 interface contract, one as provider and one as consumer.

**Reference:** [`aieos-engineering-execution-kit/docs/playbook.md`](../../aieos-engineering-execution-kit/docs/playbook.md) Step 6 — WDD, Interface Contract Reference.

### Context Package

**Provider sub-agent receives:**

| Item | Source |
|------|--------|
| Provider work item context | `{nn}-{wdd-item-id}-context.md` |
| TDD §4 contract | The specific interface contract this item implements |
| Phase-specific prompt | Current phase prompt |
| Instruction | "Implement the real interface as specified in the contract" |

**Consumer sub-agent receives:**

| Item | Source |
|------|--------|
| Consumer work item context | `{nn}-{wdd-item-id}-context.md` |
| TDD §4 contract | The same interface contract (identical copy) |
| Phase-specific prompt | Current phase prompt |
| Instruction | "Build a stub/mock of the provider interface from the contract. Implement your consumption logic against this stub." |

### Independence

- During Phases 1–3, neither sub-agent sees the other's outputs.
- Both work from the same TDD §4 contract as the single source of truth.
- The provider builds the real implementation; the consumer builds against a stub derived from the contract.

### Integration Point

After both items complete Phase 3 (Code):

1. Remove the consumer's stub.
2. Wire the consumer to the provider's real implementation.
3. Run integration tests that exercise the contract boundary.
4. Both items proceed to Phase 4 (Review) incorporating integration test results.

The integration step is performed by the orchestrator (or a dedicated integration session), not by either sub-agent.

### Failure Handling

- **Contract ambiguity discovered:** Both sub-agents pause. The ambiguity is escalated as a TDD re-entry issue. The TDD §4 contract must be clarified and the TDD re-frozen before either sub-agent resumes.
- **Integration test failure:** Diagnose against the TDD §4 contract. If the contract is correctly implemented by both sides, the contract itself is insufficient — escalate to TDD. If one side deviates from the contract, that side fixes and re-runs Phase 3.
- **Stub divergence:** If the consumer's stub does not match the provider's real interface despite both following the same contract, the contract has an ambiguity problem (see above).

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Sharing outputs across parallel sessions | Destroys independence; introduces groupthink (lenses) or hidden dependencies (work items) |
| Skipping validation before reconverge | Unvalidated sub-agent output may contain errors that propagate into the aggregate artifact |
| Fan-out without tracking | Orchestrator loses track of a sub-agent; its output is silently missing from reconvergence |
| Mixing orchestration with generation | Orchestrator contaminates its coordination context with generation details; loses objectivity |
| Unbounded parallelism | Exceeding the parallelism permitted by [`flow-reference.md` §4.1](flow-reference.md#41-what-can-run-in-parallel) violates dependency ordering |
| Summarizing context instead of providing full documents | Sub-agents need complete artifacts, not summaries. Summaries lose detail that sub-agents need for accurate evaluation |
| Re-using a sub-agent session for a second task | Each sub-agent session is single-purpose. Re-use carries over context that may bias the second task |

---

## Relationship to Other Documents

| Document | Relationship |
|----------|-------------|
| [`flow-reference.md`](flow-reference.md) §4.1 | Defines **what** can run in parallel. This document defines **how**. |
| [`aieos-peer-review-kit/docs/playbook.md`](../../aieos-peer-review-kit/docs/playbook.md) Step 1 | Pattern 1 operationalizes PRK lens parallelism |
| [`aieos-engineering-execution-kit/docs/playbook.md`](../../aieos-engineering-execution-kit/docs/playbook.md) Part 2 | Patterns 2 and 3 operationalize EEK execution parallelism |
| [`tool-governance-spec.md`](tool-governance-spec.md) | Orchestration is a pattern, not a tool. It does not require a four-file tool set. |
