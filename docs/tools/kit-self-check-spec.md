# Kit Self-Check Tool Spec

Version: v1.0

Tool ID: TOOL-KIT-SELF-CHECK

## Purpose

Validates the internal consistency of a single AIEOS kit and its boundary contracts with neighboring kits. This is the per-kit domain expert check — it understands one kit deeply, verifying that its artifacts, playbook, CLAUDE.md, and boundary contracts are internally consistent and aligned with the canonical `kit-manifest.yml`.

## Preconditions

- `kit-manifest.yml` is accessible at the governance-foundation repository root
- The target kit's directory is accessible
- Upstream and downstream neighbor kit directories are accessible (for boundary contract validation)
- The target kit abbreviation exists in the manifest

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `kit_abbreviation` | Yes | The manifest key for the target kit (e.g., `EEK`, `PIK`, `SCK`) |
| `workspace_root` | Yes | Path to the parent directory containing all kit repositories |
| `check_scope` | No | `full` (default), `internal-only`, `boundaries-only` |

## Postconditions

- All internal consistency checks have been executed for the target kit
- All boundary contract checks have been executed against neighbor kits (unless scoped to `internal-only`)
- A structured self-check report has been produced
- No files have been modified

## Output

The tool produces structured output conforming to `kit-self-check-template.md`.

## Checks

### Internal Consistency

| Check | Description |
|-------|-------------|
| `four_file_completeness` | Every artifact in the manifest for this kit has a spec file at `docs/specs/{spec_file}`, a template at `docs/artifacts/`, a prompt at `docs/prompts/`, and a validator at `docs/validators/`. When `human_authored: true`, the prompt file is not required. |
| `artifact_flow_match` | The artifact flow described in the kit's `CLAUDE.md` matches the manifest's `artifact_flow` list for this kit (same artifacts, same order). |
| `claude_md_artifact_list` | Artifact abbreviations and full names listed in the kit's `CLAUDE.md` match those in the manifest. |
| `playbook_sequence` | The artifact generation sequence in `docs/playbook.md` matches the manifest's `artifact_flow` for this kit. |
| `governance_model_sync` | `docs/governance-model.md` in the kit is byte-identical to the canonical copy in governance-foundation. |
| `spec_files_exist` | Every `spec_file` value in the manifest for this kit resolves to an existing file at `docs/specs/{spec_file}`. |

### Boundary Contracts — Pipeline Kits (Layers 1–8)

| Check | Description |
|-------|-------------|
| `entry_from_files_exist` | Every `entry_from` key in the manifest for this kit has a corresponding `entry-from-{upstream}.md` file in `docs/`. |
| `entry_from_content` | Each `entry-from-{upstream}.md` file references the correct handoff artifact(s) listed in the manifest's `expected_artifacts` for that boundary. |
| `upstream_exit_alignment` | The handoff artifact mentioned in this kit's `entry-from-{upstream}.md` matches what the upstream kit's playbook declares as its exit artifact. |

### Boundary Contracts — Cross-Cutting Kits (Layers 9–15)

| Check | Description |
|-------|-------------|
| `trigger_upstream_references` | Every `triggers[].upstream` reference (e.g., `EEK:SAD`) resolves to a real artifact in the named source kit's manifest entry. |
| `feeds_into_targets` | Every `feeds_into[].target_kit` and `target_artifact` exists in the target kit's manifest entry. |
| `internal_dependency_order` | `internal_dependencies` are satisfied by the `artifact_flow` order — no downstream artifact appears before its upstream dependency in the flow. |
| `entry_from_cross_cutting` | Entry-from files exist and reference correct upstream artifacts (same as pipeline check, applied to cross-cutting entry points). |

## Constraints

- The tool is **read-only** — it never modifies any file in the target kit or neighbor kits
- The tool **reports findings only** — it does not suggest content fixes or rewrites
- The tool does **not validate artifact content** — that is the artifact validator's job
- When checking boundary contracts, the tool reads upstream/downstream kits but does not modify them
- The tool contains **no vendor or tool references**

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Kit abbreviation not found in manifest | Report error: unknown kit abbreviation |
| Kit directory not found at expected path | Report error: kit directory missing |
| Neighbor kit directory not found | Report as boundary check FAIL: neighbor kit not accessible |
| Spec file listed in manifest does not exist | Report as internal check FAIL: spec file missing |
| Playbook not found | Report as internal check FAIL: playbook missing |

## Hard Gates

| Gate | Rule |
|------|------|
| `manifest_loaded` | `kit-manifest.yml` was successfully parsed and the target kit exists in it |
| `kit_accessible` | The target kit directory was found and is readable |
| `all_internal_checks_run` | Every internal consistency check was executed |
| `all_boundary_checks_run` | Every applicable boundary check was executed (pipeline or cross-cutting, based on kit category) — unless scoped to `internal-only` |
| `output_structured` | Output conforms to `kit-self-check-template.md` |
| `no_modifications` | No files were modified during the check |
