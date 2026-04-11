# Adapter Conformance Spec

Version: v1.0

This document defines the interface contract that adapter implementations must satisfy when connecting AIEOS artifacts and tools to external systems.

## What an Adapter Is

An adapter is executable code that implements a binding's field mapping against a concrete external API. Adapters translate AIEOS tool operations into API calls against specific platforms (e.g., Confluence, Jira, GitHub Issues).

An adapter is **not** an AIEOS artifact. It is not governed by the four-file system. It does not live inside an AIEOS kit. Adapter code is owned by the consuming project or a dedicated adapter repository.

## The Three-Layer Integration Model

AIEOS integration follows a three-layer separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│  Tool Spec (abstract capability)                    │
│  "WHAT the capability does"                         │
│  Governed by four-file system (spec/template/       │
│  prompt/validator) in docs/tools/                   │
├─────────────────────────────────────────────────────┤
│  Binding (field mapping)                            │
│  "HOW it maps to a specific platform"               │
│  Static mapping document in docs/bindings/          │
│  Maps abstract fields → platform fields             │
├─────────────────────────────────────────────────────┤
│  Adapter (executable implementation)                │
│  "HOW it runs against the platform API"             │
│  Code — lives OUTSIDE AIEOS kits                    │
│  Implements the binding's mapping via API calls     │
└─────────────────────────────────────────────────────┘
```

**Responsibilities at each layer:**

| Layer | Owns | Does Not Own |
|-------|------|-------------|
| Tool Spec | Preconditions, postconditions, constraints, hard gates | Platform specifics, field mappings, API details |
| Binding | Field mapping, environment variable names, platform-specific notes | Behavioral rules (those are in the spec), executable code |
| Adapter | API calls, authentication, retry logic, error handling | Policy (that is in the spec), field mapping (that is in the binding) |

When the platform changes, the binding and adapter change. The tool spec does not.
When the tool's rules change, the spec changes. The binding and adapter may need updating.

## Interface Contract

Every adapter must implement the following operations:

### `push(payload) → result`

Sends AIEOS content to the external system. The payload conforms to the tool's template structure. The result includes the external system's identifier for the created or updated resource.

### `verify(id) → status`

Confirms that a previously pushed resource exists in the external system and matches expectations. The `id` is the external identifier returned by a prior `push` call.

### `health() → ok | degraded | down`

Reports the adapter's ability to communicate with the external system. This is a connectivity and authentication check, not a content check.

Not all operations apply to all adapters. Push-only adapters implement `push` and `health`. Pull-only adapters implement `verify` and `health`. Bidirectional adapters implement all three.

## Idempotency Requirements

Repeated calls with the same input must produce the same outcome. If the resource already exists in the external system, the adapter updates rather than duplicates.

Adapters must derive a deterministic external ID from the AIEOS artifact ID. The binding documents the ID derivation formula (e.g., `{ARTIFACT_ID}` → Confluence page title prefix, or `{ITEM_ID}` → GitHub issue title prefix). This ensures that re-running a push for the same artifact always targets the same external resource.

## Authentication Handling

Credentials must never appear in AIEOS files — not in specs, bindings, templates, or any governed document.

Adapters accept credentials via:
- **Environment variables** — the binding documents which variables the adapter expects (e.g., `CONFLUENCE_API_TOKEN`, `GITHUB_TOKEN`)
- **Secrets manager references** — the binding documents the secret path or key name

The binding is the authoritative source for which credentials the adapter requires and how they are provided. The adapter is responsible for reading them at runtime.

## Error Handling

Adapters must implement:

| Mechanism | Requirement |
|-----------|-------------|
| **Retry with exponential backoff** | Transient failures (HTTP 429, 502, 503) are retried with increasing delays. Max retry count is adapter-configurable. |
| **Circuit breaker** | After repeated failures, the adapter stops calling the external system and reports `degraded` or `down` via `health()`. |
| **Degraded mode** | When the external system is unavailable, the adapter logs the operation and continues. The consuming project decides whether to block or proceed without external sync. |

Adapters must not swallow errors silently. Every failure is logged via the audit logging mechanism.

## Audit Logging

Every adapter operation produces a structured log entry:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp of the operation |
| `artifact_id` | The AIEOS artifact ID involved |
| `external_id` | The external system's resource identifier (or `null` if creation failed) |
| `action` | `push`, `verify`, or `health` |
| `result` | `success`, `failure`, `skipped` (idempotent no-op), or `degraded` |
| `duration_ms` | Wall-clock time of the operation in milliseconds |
| `error` | Error message if result is `failure`, otherwise `null` |

Log format and destination are adapter-configurable. The structured fields above are the minimum required content.

## Directionality

Each adapter declares its directionality:

| Direction | Operations Implemented | Use Case |
|-----------|----------------------|----------|
| **Push-only** | `push`, `health` | Publishing artifacts, syncing work items to a tracker |
| **Pull-only** | `verify`, `health` | Checking external status, confirming publication |
| **Bidirectional** | `push`, `verify`, `health` | Full sync with status feedback |

The binding documents which direction the adapter supports. The tool spec constrains which directions are valid for the capability (e.g., artifact-publish is push-only).

## Conformance Verification

AIEOS defines the hard gates; it does not define the test harness.

Conformance verification is the responsibility of the consuming project's test suite. The adapter's tests must exercise each hard gate below and produce evidence that the gate is satisfied. How the tests are structured, run, and reported is outside AIEOS scope.

## Hard Gates

| Gate | Rule |
|------|------|
| `idempotency_implemented` | Repeated calls with the same input produce the same outcome — no duplicate resources created |
| `auth_externalized` | No credentials appear in AIEOS files; adapter reads credentials from environment variables or secrets manager |
| `error_handling_defined` | Retry with exponential backoff, circuit breaker, and degraded mode are implemented |
| `audit_logging_implemented` | Every operation produces a structured log entry with the required fields |
| `directionality_declared` | The adapter declares push-only, pull-only, or bidirectional and implements only the corresponding operations |
| `health_check_implemented` | `health()` returns `ok`, `degraded`, or `down` based on external system connectivity |
| `payload_format_compliant` | The adapter accepts input conforming to the integration tool's template structure |

## What This Spec Does Not Define

- **Adapter code** — implementation is owned by the consuming project or adapter repository
- **Test harnesses** — how conformance is verified is the consuming project's concern
- **Deployment strategy** — how adapters are deployed, scaled, or monitored
- **CI/CD pipelines** — how adapters are built and released
- **Platform-specific behavior** — API pagination, rate limits, and platform quirks are adapter concerns
