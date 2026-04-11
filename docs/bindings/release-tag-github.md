# Release Tag — GitHub Binding

This binding maps the abstract `TOOL-RELEASE-TAG` capability to GitHub Releases.

## Tool Reference

- **Tool Spec:** `docs/tools/release-tag-spec.md`
- **Tool Template:** `docs/tools/release-tag-template.md`

## Input Mapping

| Tool Input | GitHub Mapping |
|------------|---------------|
| `rr_artifact_id` | Referenced in release body preamble (e.g., `Source: RR-TASKFLOW-001`) |
| `rr_path` | Not mapped to GitHub — used by the adapter to read RR content |
| `release_version` | Tag name, prefixed with `v` (e.g., `1.0.0` → `v1.0.0`) |
| `target_system` | Resolved to GitHub repository (owner/repo) |

## Field Mapping

| AIEOS Field | GitHub Releases Field | Notes |
|-------------|----------------------|-------|
| Release version | Tag name | Format: `v{release_version}` (e.g., `v1.0.0`) |
| RR Artifact ID | Release body preamble | First line: `Source: {RR_ARTIFACT_ID}` |
| RR §Summary content | Release body | Markdown content from the RR Summary section |
| Release disposition | Release body suffix | Appended as: `Disposition: {disposition}` |
| RR Artifact ID + version | Release name | Format: `{RR_ARTIFACT_ID} — v{release_version}` |
| Pre-release flag | `prerelease` field | Set to `true` if RR disposition is not `successful-full-exposure` |

## ID Derivation

The external ID is derived deterministically: the adapter searches for an existing release with the tag name `v{release_version}` in the configured repository. If found, the release is updated. If not found, a new release is created.

## Adapter Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | Personal access token or GitHub App token with `contents:write` scope |
| `GITHUB_REPO` | Yes | Target repository in `owner/repo` format (e.g., `acme/taskflow`) |
| `GITHUB_TARGET_COMMITISH` | No | Target commitish for the tag (defaults to default branch). Use to tag a specific commit. |

## Adapter Conformance Reference

The adapter implementing this binding must satisfy all hard gates defined in `docs/adapter-conformance-spec.md`. The adapter is push-only (creates tags and releases on GitHub; does not sync GitHub release changes back to AIEOS).

## What This Binding Does Not Define

This binding does not define policy. The rules for what constitutes a valid release tag operation (preconditions, postconditions, constraints, hard gates) are defined in `release-tag-spec.md`. The interface contract for adapter implementations is defined in `adapter-conformance-spec.md`. This file only describes how RR fields map to GitHub Releases fields and configuration.

If the organization migrates from GitHub to another SCM platform, this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
