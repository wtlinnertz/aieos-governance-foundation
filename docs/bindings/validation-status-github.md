# Validation Status — GitHub Binding

This binding maps the abstract `TOOL-VALIDATION-STATUS` capability to GitHub Check Runs.

## Tool Reference

- **Tool Spec:** `docs/tools/validation-status-spec.md`
- **Tool Template:** `docs/tools/validation-status-template.md`

## Input Mapping

| Tool Input | GitHub Mapping |
|------------|---------------|
| `validator_output_path` | Not mapped to GitHub — used by the adapter to read validator JSON content |
| `artifact_id` | Check run name (e.g., `AIEOS: PRD-TASKFLOW-001`) |
| `commit_ref` | Check run `head_sha` (for commit SHA) or resolved from PR number via GitHub API |
| `target_system` | Resolved to GitHub repository (owner/repo) |

## Field Mapping

| AIEOS Field | GitHub Check Runs Field | Notes |
|-------------|------------------------|-------|
| Validator status (PASS) | Conclusion: `success` | PASS maps to success |
| Validator status (FAIL) | Conclusion: `failure` | FAIL maps to failure |
| Validator summary | Check run output summary | One-sentence verdict from validator JSON |
| Hard gates (individual) | Check run annotations | One annotation per hard gate; level `notice` for PASS, `failure` for FAIL |
| Blocking issues | Check run output text | Rendered as markdown list in the check run detail |
| Warnings | Check run output text | Appended after blocking issues, prefixed as warnings |
| Completeness score | Check run output title | Format: `{ARTIFACT_ID} — {PASS/FAIL} ({score}%)` |
| Artifact ID | Check run `external_id` | Used for idempotent matching |

## ID Derivation

The external ID is derived deterministically: the adapter searches for an existing check run with `external_id` matching the artifact ID on the given commit SHA. If found, the check run is updated. If not found, a new check run is created.

## Adapter Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub App token or PAT with `checks:write` scope |
| `GITHUB_REPO` | Yes | Target repository in `owner/repo` format (e.g., `acme/taskflow`) |

## Adapter Conformance Reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is push-only (posts check runs to GitHub; does not sync check run status back to AIEOS).

## What This Binding Does Not Define

This binding does not define policy. The rules for what constitutes a valid validation status post (preconditions, postconditions, constraints, hard gates) are defined in `validation-status-spec.md`. The interface contract for adapter implementations is defined in `adapter-conformance-spec.md`. This file only describes how validator JSON fields map to GitHub Check Runs fields and configuration.

If the organization migrates from GitHub to another SCM platform, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
