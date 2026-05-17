# Work Item Sync — GitHub Issues Binding

This binding maps the abstract `TOOL-WORK-ITEM-SYNC` capability to GitHub Issues.

## Tool reference

- **Tool Spec:** `docs/tools/work-item-sync-spec.md`
- **Tool Template:** `docs/tools/work-item-sync-template.md`

## Input mapping

| Tool Input | GitHub Issues Mapping |
|------------|----------------------|
| `wdd_artifact_id` | Referenced in issue body preamble (e.g., `Source: WDD-TASKFLOW-001`) |
| `wdd_path` | Not mapped to GitHub — used by the adapter to read WDD content |
| `target_system` | Resolved to GitHub repository (owner/repo) |

## Field mapping

| AIEOS Field | GitHub Issues Field | Notes |
|-------------|-------------------|-------|
| Work group name | Milestone | One milestone per work group |
| Work item ID | Issue title prefix | Format: `[{ITEM_ID}] {item title}` |
| Work item title | Issue title (after prefix) | Combined with ID prefix |
| Work item description | Issue body | Markdown content preserved directly |
| Assignee type (AI/Human/Either) | Label | `assignee:ai`, `assignee:human`, `assignee:either` |
| Complexity estimate | Label | `size:S`, `size:M`, `size:L`, `size:XL` |
| Work item dependencies | Issue cross-references | `Depends on: #NN` in issue body |
| Acceptance criteria | Checklist in issue body | Rendered as GitHub task list (`- [ ]`) |
| Work group → item relationship | Milestone membership | Items in the same group share a milestone |

## ID derivation

The external ID is derived deterministically: the adapter searches for an existing issue whose title starts with `[{ITEM_ID}]` in the configured repository. If found, the issue is updated. If not found, a new issue is created. Milestones are matched by name (work group name); created if missing.

## Adapter environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | Personal access token or GitHub App token with `issues:write` and `project:write` scope |
| `GITHUB_REPO` | Yes | Target repository in `owner/repo` format (e.g., `acme/taskflow`) |

## Adapter conformance reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is push-only (creates/updates GitHub Issues; does not sync issue status changes back to the WDD).

## What this binding does not define

This binding does not define policy. The rules for what constitutes a valid work item sync operation (preconditions, postconditions, constraints, hard gates) are defined in `work-item-sync-spec.md`. The interface contract for adapter implementations is defined in `adapter-conformance-spec.md`. This file only describes how WDD fields map to GitHub Issues fields and configuration.

If the organization migrates from GitHub Issues to another tracker, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
