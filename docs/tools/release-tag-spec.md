# Release Tag Tool Spec

Version: v1.0

Tool ID: TOOL-RELEASE-TAG

## Purpose

Creates a tagged release on an external SCM platform when a Release Record (RR) is frozen. The external system receives the tag and release notes; the AIEOS source remains unmodified.

## Preconditions

- The Release Record (RR) is frozen (Status: Frozen in Document Control)
- The release version is extractable from the RR content
- The target SCM is configured via a binding (field mapping and adapter environment documented)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `rr_artifact_id` | Yes | The AIEOS RR artifact ID (e.g., `RR-TASKFLOW-001`) |
| `rr_path` | Yes | Path to the Release Record file |
| `release_version` | Yes | Semantic version for the tag (e.g., `1.0.0`) |
| `target_system` | Yes | Abstract target identifier — the binding resolves this to a concrete SCM platform |

## Postconditions

- A tag has been created on the external SCM platform
- Release notes have been published (derived from the RR summary)
- An external release ID has been returned identifying the created release
- An audit log entry has been produced recording the operation
- The source RR file is unmodified

## Output

The tool produces structured output conforming to `release-tag-template.md`.

## Constraints

- Only frozen RRs may trigger a release tag — tagging from a non-frozen RR is a hard gate failure
- Push-only — this tool creates tags and releases; it does not read or sync back from the SCM
- Source unmodified — the tool does not alter the RR file in any way
- Idempotent — re-tagging the same version updates the existing release rather than creating a duplicate
- The tool contains no references to specific SCM platforms, APIs, or environments

## Error Handling

| Condition | Behavior |
|-----------|----------|
| RR not found at path | Report error: RR file not found |
| RR not frozen | Report error: RR status is not Frozen — tag blocked |
| Release version empty or invalid | Report error: release version could not be extracted or is malformed |
| Target system not configured | Report error: no binding found for target system |
| External SCM unreachable | Report error: adapter health check failed — tag blocked |
| Tag already exists with different content | Report warning: existing tag found — adapter will update release body per idempotency rules |

## Hard Gates

| Gate | Rule |
|------|------|
| `rr_frozen_check` | The RR's Document Control section shows Status: Frozen |
| `tag_created` | The external SCM accepted the tag and returned a success response |
| `release_notes_published` | Release notes derived from the RR summary were included in the SCM release |
| `external_release_id_returned` | The tag result includes a non-empty external release identifier |
| `audit_logged` | A structured audit log entry was produced for the operation |
| `source_unmodified` | The RR file's content hash is identical before and after the operation |
| `idempotent_behavior` | Re-tagging the same version updates the existing release rather than creating a duplicate |
