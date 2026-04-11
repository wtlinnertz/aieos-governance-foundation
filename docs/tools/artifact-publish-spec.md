# Artifact Publish Tool Spec

Version: v1.0

Tool ID: TOOL-ARTIFACT-PUBLISH

## Purpose

Publishes a frozen AIEOS artifact to an external document management system. The external system receives the artifact content; the AIEOS source remains unmodified.

## Preconditions

- The artifact is frozen (Status: Frozen in Document Control)
- The artifact ID is known
- The target system is configured via a binding (field mapping and adapter environment documented)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `artifact_id` | Yes | The AIEOS artifact ID (e.g., `PRD-TASKFLOW-001`) |
| `artifact_path` | Yes | Path to the artifact file |
| `target_system` | Yes | Abstract target identifier — the binding resolves this to a concrete platform |

## Postconditions

- The artifact content has been published to the external system
- An external ID has been returned identifying the published resource
- An audit log entry has been produced recording the operation
- The source artifact file is unmodified

## Output

The tool produces structured output conforming to `artifact-publish-template.md`.

## Constraints

- Only frozen artifacts may be published — publishing a non-frozen artifact is a hard gate failure
- Push-only — this tool publishes content; it does not read or sync back from the external system
- Source unmodified — the tool does not alter the AIEOS artifact file in any way
- Idempotent — re-publishing the same artifact to the same target produces the same external resource (update, not duplicate)
- The tool contains no references to specific platforms, APIs, or environments

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Artifact not found at path | Report error: artifact file not found |
| Artifact not frozen | Report error: artifact status is not Frozen — publish blocked |
| Target system not configured | Report error: no binding found for target system |
| External system unreachable | Report error: adapter health check failed — publish blocked |
| Publish succeeded but verify failed | Report warning: published but verification pending |

## Hard Gates

| Gate | Rule |
|------|------|
| `artifact_frozen_check` | The artifact's Document Control section shows Status: Frozen |
| `publish_confirmed` | The external system accepted the content and returned a success response |
| `external_id_returned` | The publish result includes a non-empty external resource identifier |
| `audit_logged` | A structured audit log entry was produced for the operation |
| `source_unmodified` | The artifact file's content hash is identical before and after the operation |
| `idempotent_behavior` | Re-publishing the same artifact updates the existing external resource rather than creating a duplicate |
