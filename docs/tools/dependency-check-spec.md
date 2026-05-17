# Dependency Check Tool Spec

Version: v1.0

Tool ID: TOOL-DEPENDENCY-CHECK

## Purpose

Verifies that all required upstream artifacts are frozen before downstream artifact generation begins. Enforces the freeze-before-promote invariant (governance-model.md §13, invariant 5).

## Preconditions

- The target artifact type is known (e.g., "TDD", "SAD", "WDD")
- The kit and its playbook are identified
- The artifact spec for the target type is accessible (to determine upstream dependencies)

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `target_artifact_type` | Yes | The artifact type about to be generated (e.g., "TDD") |
| `kit_name` | Yes | The kit in which generation will occur |
| `artifact_directory` | Yes | Path to the project's artifact directory (e.g., `docs/sdlc/`) |

## Postconditions

- Every upstream artifact required by the target type has been identified
- Each upstream artifact's freeze status has been checked
- A structured report has been produced listing each dependency and its status
- If any required upstream artifact is missing or unfrozen, the report indicates FAIL

## Output

The tool produces structured output conforming to `dependency-check-template.md`.

## Constraints

- The tool checks **freeze status only** — it does not validate artifact content
- The tool does not modify any artifacts
- The tool does not infer dependencies beyond what the spec and playbook declare
- The tool reports what it finds — it does not suggest remediation
- The tool contains no references to specific implementations, environments, or vendor tools

## Error handling

| Condition | Behavior |
|-----------|----------|
| Target artifact type not found in kit | Report error: unknown artifact type |
| Upstream spec not accessible | Report error: cannot determine dependencies |
| Artifact directory does not exist | Report error: directory not found |
| Upstream artifact file exists but status field is missing | Report as UNFROZEN (ambiguity is a failure condition) |

## Hard gates

| Gate | Rule |
|------|------|
| `all_dependencies_identified` | Every upstream dependency declared in the spec and playbook is listed in the output |
| `freeze_status_checked` | Every listed dependency has a verified freeze status |
| `output_structured` | Output conforms to the template schema |
| `no_content_validation` | The tool did not evaluate artifact content — only freeze status |
| `no_remediation` | The tool did not suggest fixes or next steps |
