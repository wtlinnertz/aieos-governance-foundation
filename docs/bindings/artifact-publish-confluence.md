# Artifact Publish — Confluence Binding

This binding maps the abstract `TOOL-ARTIFACT-PUBLISH` capability to Atlassian Confluence.

## Tool reference

- **Tool Spec:** `docs/tools/artifact-publish-spec.md`
- **Tool Template:** `docs/tools/artifact-publish-template.md`

## Input mapping

| Tool Input | Confluence Mapping |
|------------|-------------------|
| `artifact_id` | Page title prefix (e.g., `PRD-TASKFLOW-001: Product Requirements Document`) |
| `artifact_path` | Markdown content is converted to Confluence storage format (XHTML) |
| `target_system` | Resolved to Confluence space key + parent page ID |

## Field mapping

| AIEOS Field | Confluence Field | Notes |
|-------------|-----------------|-------|
| Artifact ID | Page title prefix | Format: `{ARTIFACT_ID}: {artifact type display name}` |
| Document Control table | Page metadata macro or top-of-page table | Preserves status, version, provenance fields |
| Section headings | Confluence headings (h1–h6) | Markdown heading levels map directly |
| Tables | Confluence tables | Markdown table syntax → XHTML table |
| Content body | Page body (storage format) | Full Markdown → Confluence storage format conversion |
| Artifact status | Page label | `aieos-frozen`, `aieos-draft`, etc. |

## ID derivation

The external ID is derived deterministically: the adapter searches for an existing page whose title starts with `{ARTIFACT_ID}:` in the configured space. If found, the page is updated. If not found, a new page is created under the configured parent page.

## Adapter environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONFLUENCE_BASE_URL` | Yes | Confluence instance URL (e.g., `https://company.atlassian.net/wiki`) |
| `CONFLUENCE_SPACE_KEY` | Yes | Target space key (e.g., `ENG`) |
| `CONFLUENCE_PARENT_PAGE_ID` | Yes | Parent page ID under which artifacts are published |
| `CONFLUENCE_API_TOKEN` | Yes | API token for authentication (user email + token for Confluence Cloud) |
| `CONFLUENCE_USER_EMAIL` | Yes | Email address associated with the API token (Confluence Cloud) |

## Adapter conformance reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is push-only (publishes content to Confluence; does not sync Confluence changes back to AIEOS).

## What this binding does not define

This binding does not define policy. The rules for what constitutes a valid artifact publish operation (preconditions, postconditions, constraints, hard gates) are defined in `artifact-publish-spec.md`. The interface contract for adapter implementations is defined in `adapter-conformance-spec.md`. This file only describes how abstract fields map to Confluence-specific fields and configuration.

If the organization migrates from Confluence to another document platform, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
