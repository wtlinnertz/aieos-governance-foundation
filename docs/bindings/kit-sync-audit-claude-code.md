# Kit Sync Audit — Claude Code Binding

This binding maps the abstract `TOOL-KIT-SYNC-AUDIT` capability to a concrete implementation using Claude Code.

## Tool reference

- **Tool Spec:** `docs/tools/kit-sync-audit-spec.md`
- **Tool Template:** `docs/tools/kit-sync-audit-template.md`

## Implementation

In a Claude Code session, the kit-sync-audit capability is exercised as follows:

### Input mapping

| Tool Input | Claude Code Action |
|------------|-------------------|
| `workspace_root` | The parent directory containing all `aieos-*` kit repositories (typically the project root) |
| `scope` | Provided by the operator. Defaults to `full` if not specified |

### Execution steps

1. **Load manifest.** Read `kit-manifest.yml` from the governance-foundation repository root using the Read tool. Parse the YAML content.

2. **Verify manifest version.** Read `governance-model.md` from the governance-foundation root. Search for the `Current value:` reference in the Artifact Provenance section. Compare against the manifest's `governance_model_version`.

3. **Locate kit directories.** For each kit in the manifest, resolve its directory using the `repository` field under `workspace_root` (e.g., `{workspace_root}/aieos-product-intelligence-kit/`).

4. **Run CRITICAL checks:**
   - For synchronized files: use the Bash tool to diff the canonical copy against each kit copy
   - For kit registry: read root `CLAUDE.md`, `README.md`, and `docs/layer-model.md` and compare kit tables against manifest data

5. **Run HIGH checks:**
   - For boundary contracts: use the Glob tool to verify `entry-from-*.md` files exist, then Read to verify content
   - For artifact flow: read each kit's `CLAUDE.md` and compare artifact sequences against the manifest's `artifact_flow`
   - For cross-cutting triggers: read `docs/layer-model.md` and `docs/flow-reference.md` and compare trigger descriptions against manifest `triggers` entries
   - For dependency edges: read `tests/models/framework.py` and compare `DEPENDENCY_EDGES` against manifest `dependency_edges`

6. **Run MEDIUM checks:**
   - For artifact inventory: use the Glob tool to verify four-file sets exist in each kit
   - For layer descriptions: read `docs/layer-model.md`, `README.md`, and `docs/getting-started.md` and compare layer questions
   - For navigation map: read `docs/navigation-map.md` and verify node IDs against manifest artifacts

7. **Produce output.** Format results following the template. Use the Markdown table format with one row per finding.

### Fan-Out for kit self-Checks

When running a `full` scope audit, the orchestrator may invoke TOOL-KIT-SELF-CHECK for each kit using the Agent tool with parallel sub-agents. Each sub-agent receives:
- The manifest content (or path)
- The target kit abbreviation
- The workspace root path

Results are collected and aggregated into the Per-Kit Status table.

### Environment notes

- Claude Code reads files directly via the Read tool
- File comparisons use the Bash tool (`diff`) for byte-identical checks
- YAML parsing is performed by Claude Code's language understanding (no external YAML parser required in the session, though `python3 -c "import yaml"` can be used for validation)
- All kit repositories must be cloned locally under the workspace root

## What this binding does not define

This binding does not define policy. The rules for what constitutes a valid sync audit (checks, severity tiers, hard gates) are defined in `kit-sync-audit-spec.md`. This file only describes how those rules are implemented in the Claude Code environment.

If the implementation environment changes (e.g., from Claude Code to a GitHub Actions workflow), this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
