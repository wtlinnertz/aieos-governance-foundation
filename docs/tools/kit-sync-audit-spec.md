# Kit Sync Audit Tool Spec

Version: v1.0

Tool ID: TOOL-KIT-SYNC-AUDIT

## Purpose

Audits the entire AIEOS framework for cross-kit consistency by validating prose documents and structural artifacts against the canonical `kit-manifest.yml`. This is the authoritative audit tool — it reads canonical truth from the manifest and checks all kits against it.

This tool does not validate individual artifact content. It validates that the framework's structural metadata — kit names, layer numbers, artifact inventories, boundary contracts, dependency edges, and cross-cutting triggers — is consistent across all documents that reference it.

## Preconditions

- `kit-manifest.yml` is accessible at the governance-foundation repository root
- All 15 kit repositories are accessible as sibling directories to the governance-foundation
- `governance-model.md` canonical copy is accessible at the governance-foundation repository root

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `workspace_root` | Yes | Path to the parent directory containing all kit repositories |
| `scope` | No | `full` (default), `registry-only`, `boundaries-only`, `sync-files-only`, `single-kit:{KIT}` |

## Postconditions

- Every check category (CRITICAL, HIGH, MEDIUM) has been executed (or scoped out via `scope`)
- A structured drift report has been produced listing every inconsistency found
- Each finding includes severity, location, expected value (from manifest), and actual value (from document)
- No files have been modified

## Output

The tool produces structured output conforming to `kit-sync-audit-template.md`.

## Checks

### CRITICAL

| Check | Description |
|-------|-------------|
| `manifest_version_pinning` | `governance_model_version` in the manifest matches the version declared in the actual `governance-model.md` file. If these disagree, all downstream validation is against stale data. |
| `synchronized_file_identity` | Every file listed in the manifest's `synchronized_files` section matches its canonical copy byte-for-byte. Currently: `governance-model.md` across all 15 kit copies. |
| `kit_registry_consistency` | Kit names, layer numbers, statuses, categories, and repository names in the manifest match every prose location: root `CLAUDE.md` tables, `README.md` Kit Registry, `layer-model.md` Kit Registry. |

### HIGH

| Check | Description |
|-------|-------------|
| `boundary_contract_existence` | Every `entry_from` entry in the manifest has a corresponding `entry-from-{upstream}.md` file in the downstream kit's `docs/` directory. |
| `boundary_contract_content` | Each `entry-from-{upstream}.md` file references the correct handoff artifact(s) listed in the manifest's `expected_artifacts` for that boundary. |
| `artifact_flow_consistency` | The `artifact_flow` list in the manifest matches the artifact sequence described in each kit's `CLAUDE.md` and `docs/playbook.md`. |
| `cross_cutting_trigger_consistency` | Manifest `triggers` entries for cross-cutting kits (Layers 9–15) are consistent with descriptions in `layer-model.md`, `flow-reference.md`, and each cross-cutting kit's `CLAUDE.md`. Validation is structural: every `triggers[].upstream` reference (e.g., `EEK:SAD`) must point to a real artifact in the named kit. Every `feeds_into[].target_kit` and `target_artifact` must exist in the target kit's manifest entry. `internal_dependencies` within cross-cutting kits must not create cycles. |
| `dependency_edge_consistency` | Manifest `dependency_edges` match the `DEPENDENCY_EDGES` list in `tests/models/framework.py` (until framework.py migrates to consume the manifest directly). |

### MEDIUM

| Check | Description |
|-------|-------------|
| `artifact_inventory_completeness` | Every artifact listed in the manifest has a four-file set in the kit's `docs/` directory (spec, template, prompt, validator). Adjusted for `human_authored: true` — human-authored entry gates are not expected to have prompt files. |
| `layer_description_consistency` | The manifest `question` field for each kit matches the layer question in `layer-model.md`, `README.md`, and `getting-started.md`. |
| `navigation_map_alignment` | Node IDs in `navigation-map.md` correspond to valid kit-artifact pairs in the manifest. Artifact nodes of the form `N-{KIT}-{ARTIFACT}` must reference a kit and artifact that exist in the manifest. |

## Constraints

- The tool is **read-only** — it never modifies any file
- The tool **reports findings** — it does not suggest prose rewrites or remediation steps
- The tool **validates against manifest data**, not by parsing prose for semantic meaning
- The tool contains **no vendor or tool references** — it defines an abstract capability
- Cross-cutting trigger condition text is validated by checking that referenced artifact IDs exist, not by interpreting natural-language conditions

## Error Handling

| Condition | Behavior |
|-----------|----------|
| `kit-manifest.yml` not found | Report error: manifest not found at expected location |
| Kit directory listed in manifest not found | Report as CRITICAL finding: kit directory missing |
| Manifest YAML parse failure | Report error: invalid YAML |
| Governance model version field not found | Report as CRITICAL finding: version field missing from governance-model.md |
| Scope parameter references unknown kit | Report error: unknown kit abbreviation |

## Hard Gates

| Gate | Rule |
|------|------|
| `manifest_loaded` | `kit-manifest.yml` was successfully parsed as valid YAML |
| `manifest_version_verified` | `governance_model_version` in manifest matches the actual governance-model.md |
| `all_kits_accessible` | All 15 kit directories listed in the manifest were found and readable |
| `all_check_categories_run` | Every check category (CRITICAL, HIGH, MEDIUM) was executed, or was explicitly scoped out via the `scope` input |
| `output_structured` | Output conforms to the `kit-sync-audit-template.md` schema |
| `no_modifications` | No files were modified during the audit |
