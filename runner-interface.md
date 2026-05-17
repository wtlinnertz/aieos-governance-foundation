# AIEOS Pipeline Runner — Public Interface v1.0

The runner is the tool-agnostic boundary between frozen governance specs and
their execution. Kits (M5) integrate downstream; entry-point shims (GitHub
Actions, webhooks, IDP actions) call the runner's CLI; operators observe the
runner's structured events and consume its run records.

This document freezes the runner's public contract. Anything inside the
runner that is not referenced here is implementation detail and may change
without a cutover; anything referenced here is stable until the next
versioned schema bump.

Scope:
1. [CLI](#1-cli) — arguments, subcommands, and exit codes.
2. [Bound plan](#2-bound-plan-schema) — JSON shape of a resolved plan.
3. [Event stream](#3-event-stream) — five event types, one JSON object per line.
4. [Run record](#4-run-record-schema) — JSON shape of a completed run.

---

## 1. CLI

### Invocation

```
aieos-pipeline-runner run \
    --spec <path-or-ref> \
    [--env <env>] \
    [--expected-hash <sha256>] \
    [--artifact-store <dir>] \
    [--use-mock-adapters] \
    [--run-id <id>]
```

### Arguments

| Flag | Required | Description |
|---|---|---|
| `--spec` | yes | Path to a frozen CI or CD spec file. Source kind is auto-detected (CI has `code_repo` + `actions`; CD has `artifact_ref` + `environments`). |
| `--env` | no (default `ci`) | Environment-context tag forwarded to the registry lookup. |
| `--expected-hash` | conditional | sha256 hex digest of the spec file bytes. Required for file-path specs — the runner refuses unfrozen input. |
| `--artifact-store` | no | Directory-backed artifact store. When present, the run record and validator report are written to `runs/<run_id>/record.json` and `runs/<run_id>/report.json`. |
| `--use-mock-adapters` | no | v1 flag. When absent, the CLI returns an infrastructure error (real-adapter wiring lands as a deferred integration). |
| `--run-id` | no | Explicit run identifier. Defaults to `run-<12 hex chars>`. Referenced in every event and in the artifact-store key prefix. |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Overall PASS — every validator (spec, plan, run) passed and every action's criteria held. |
| 1 | Overall FAIL — at least one validator rejected the input. The run report on stderr identifies which check failed. |
| 2 | Infrastructure error — spec not found, unfrozen, hash mismatch, unparseable, artifact-store unavailable, or real-adapter wiring requested in v1. |

### Output streams

- **stdout** — the event stream (§3). JSON lines, one event per line.
- **stderr** — the validator report on terminal stages, plus infrastructure diagnostics.

---

## 2. bound plan schema

The bound plan is the resolver's output and the orchestrator's input. It is
not written to the artifact store in v1 (it exists in-process), but kits that
consume runner output should model it for cross-component interoperability.

```json
{
  "spec_ref": "<source_ref: file:// URI or artifact-store key>",
  "spec_hash": "<sha256 hex of the spec bytes>",
  "tasks": [
    {
      "action": "<taxonomy action identifier, e.g. test.unit>",
      "adapter_id": "<adapter identifier, e.g. adapter-pytest-unit>",
      "adapter_version": "<semver>",
      "criteria": { /* spec's criteria object for this action */ },
      "inputs": { /* spec's config object for this action (adapter-side) */ },
      "depends_on": ["<action identifier>", "..."]
    }
  ],
  "unresolved": [
    {
      "action": "<taxonomy action identifier>",
      "reason": "no_adapter | ambiguous",
      "candidates": ["<adapter-id@version>", "..."]
    }
  ]
}
```

**Invariants.**
- Every task's `action` matches an entry in the frozen v1.0 taxonomy.
- Every task's `adapter_id` + `adapter_version` identifies a registered,
  attested adapter (attestation validity was enforced at registration time
  per `schema/conformance-attestation.schema.json`).
- `depends_on` references only other tasks in the same bound plan.
- When `unresolved` is non-empty, the plan validator refuses to promote the
  plan into a run. The orchestrator is never handed a plan with unresolved
  actions.

---

## 3. event stream

The runner emits one JSON object per line to stdout. Every event carries at
least the following three fields:

- `type` — one of `run.start`, `task.start`, `task.evidence`, `task.result`, `run.end`.
- `run_id` — run identifier from `--run-id` or the default factory.
- `timestamp` — ISO 8601 UTC with `Z` suffix.

Events are emitted `sort_keys=true` for byte-stable output.

### `run.start`

Emitted once at the start of orchestration.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string (const `run.start`) | yes | |
| `run_id` | string | yes | |
| `timestamp` | string (ISO 8601) | yes | |
| `spec_ref` | string | yes | Source reference for the spec being executed. |

### `task.start`

Emitted once per task when the orchestrator hands it to the agent.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string (const `task.start`) | yes | |
| `run_id` | string | yes | |
| `timestamp` | string (ISO 8601) | yes | |
| `task_id` | string | yes | Unique within the run. |
| `action` | string | yes | Taxonomy action identifier. |
| `adapter_id` | string | yes | May be empty string when the event is emitted before registry resolution completes. |

### `task.evidence`

Emitted once per evidence artifact the adapter produces. Multiple
`task.evidence` events per task are expected.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string (const `task.evidence`) | yes | |
| `run_id` | string | yes | |
| `timestamp` | string (ISO 8601) | yes | |
| `task_id` | string | yes | |
| `evidence_ref` | string | yes | Evidence artifact reference. Scheme depends on the evidence kind (e.g., `junit-report://…`, `http-status:200`, `oci-digest:sha256:…`). |

### `task.result`

Emitted once per task at completion.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string (const `task.result`) | yes | |
| `run_id` | string | yes | |
| `timestamp` | string (ISO 8601) | yes | |
| `task_id` | string | yes | Matches the task's `task.start`. |
| `action` | string | yes | |
| `adapter_id` | string | yes | Final adapter identifier that handled the task. Empty string only if no adapter resolution happened (a failure case). |
| `status` | string (`completed` \| `failed` \| `skipped`) | yes | |
| `findings_ref` | string | yes | Reference to the findings payload. Empty string when the action produces no structured findings. |

### `run.end`

Emitted once at the close of orchestration.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string (const `run.end`) | yes | |
| `run_id` | string | yes | |
| `timestamp` | string (ISO 8601) | yes | |
| `status` | string (`pass` \| `fail`) | yes | Mirrors the run validator's verdict. |

### Ordering guarantees

- `run.start` precedes every task-level event.
- `run.end` follows every task-level event.
- For any task, `task.start` precedes all that task's `task.evidence` events,
  which precede that task's `task.result` event.
- Between different tasks, events interleave in orchestration order
  (topological per `depends_on` with deterministic alphabetical tie-break).

---

## 4. run record schema

The run record is the orchestrator's output — a collection of facts about
an executed plan, published to the artifact store by the run validator at
`runs/<run_id>/record.json`.

```json
{
  "run_id": "<run identifier>",
  "spec_ref": "<source reference carried through from the bound plan>",
  "spec_hash": "<sha256 hex carried through from the bound plan>",
  "started_at": "<ISO 8601 UTC or null>",
  "finished_at": "<ISO 8601 UTC or null>",
  "tasks": [
    {
      "action": "<taxonomy action identifier>",
      "adapter_id": "<adapter identifier>",
      "status": "completed | failed | skipped",
      "findings": { /* canonical findings per the action's output_schema, or null */ },
      "evidence": ["<evidence_ref>", "..."],
      "error": "<diagnostic string or null>",
      "started_at": "<ISO 8601 UTC or null>",
      "finished_at": "<ISO 8601 UTC or null>"
    }
  ]
}
```

**Invariants.**
- The record contains one entry per task in the bound plan, in orchestration
  order.
- `findings` matches the canonical findings schema the action's capability
  contract declares (`output_schema` in `contracts/<action>.contract.yaml`)
  or is `null` for actions whose `output_schema` is `null`.
- `evidence` enumerates artifact references corresponding to the contract's
  `required_evidence`.
- The record is not judged — it carries facts. The run validator's
  separate report (`runs/<run_id>/report.json`) carries the PASS/FAIL verdict
  per the canonical validator shape from `aieos-governance-foundation`.

### Validator report (`report.json`)

For completeness — the report companion to the run record:

```json
{
  "result": "PASS | FAIL",
  "checks": [
    {
      "check": "action:<taxonomy action identifier>",
      "result": "PASS | FAIL",
      "details": ["<reason string>", "..."]
    }
  ]
}
```

This is the canonical validator envelope used by every AIEOS validator
(spec, plan, run). A kit consuming a run's outcome should read
`report.json` for the verdict and `record.json` for the underlying facts.

---

## Freeze and cutover

This document freezes at `v1.0-runner-interface`. Breaking changes to any
field, event type, or exit code in this document require a minor-version
bump and a cutover announcement per `docs/change-protocol.md`. Additions
(new optional fields; new event types) are backwards-compatible and do not
require a bump, provided the existing fields retain their semantics.
