# Validation Status Tool Spec

Version: v1.0

Tool ID: TOOL-VALIDATION-STATUS

## Purpose

Posts AIEOS validator results (the standard JSON output defined in governance-model.md §5) as commit or PR status checks on an external SCM platform. The external system receives the validation result; AIEOS source files remain unmodified.

## Preconditions

- Validator output exists as structured JSON conforming to governance-model.md §5 (status, summary, hard_gates, blocking_issues, warnings, completeness_score)
- A commit SHA or PR identifier is known for the target check
- The target SCM is configured via a binding (field mapping and adapter environment documented)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `validator_output_path` | Yes | Path to the validator JSON output file |
| `artifact_id` | Yes | The AIEOS artifact ID that was validated (e.g., `PRD-TASKFLOW-001`) |
| `commit_ref` | Yes | Commit SHA or PR number to attach the status check to |
| `target_system` | Yes | Abstract target identifier — the binding resolves this to a concrete SCM platform |

## Postconditions

- A status check has been posted to the external SCM platform
- An external check ID has been returned identifying the posted check
- An audit log entry has been produced recording the operation
- The source validator output file and all AIEOS artifact files are unmodified

## Output

The tool produces structured output conforming to `validation-status-template.md`.

## Constraints

- Read-only on AIEOS files — this tool does not modify any AIEOS artifact or validator output file
- Push-only — this tool posts status checks; it does not read or sync check status back from the SCM
- Idempotent — re-posting the same validator result for the same commit/artifact updates the existing check rather than creating a duplicate
- The tool contains no references to specific SCM platforms, APIs, or environments

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Validator output not found at path | Report error: validator output file not found |
| Validator output invalid JSON | Report error: validator output does not conform to governance-model.md §5 schema |
| Commit ref not found on SCM | Report error: commit SHA or PR identifier not found on target SCM |
| Target system not configured | Report error: no binding found for target system |
| External SCM unreachable | Report error: adapter health check failed — post blocked |
| Post succeeded but verify failed | Report warning: posted but verification pending |

## Hard Gates

| Gate | Rule |
|------|------|
| `validator_output_valid` | The input JSON conforms to the governance-model.md §5 schema (has status, summary, hard_gates, blocking_issues, warnings, completeness_score) |
| `status_posted` | The external SCM accepted the status check and returned a success response |
| `external_check_id_returned` | The post result includes a non-empty external check identifier |
| `audit_logged` | A structured audit log entry was produced for the operation |
| `source_unmodified` | No AIEOS files were modified during the operation |
| `idempotent_behavior` | Re-posting the same validator result updates the existing check rather than creating a duplicate |
