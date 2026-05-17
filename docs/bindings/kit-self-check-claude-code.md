# Kit Self-Check — Claude Code Binding

This binding maps the abstract `TOOL-KIT-SELF-CHECK` capability to a concrete implementation using Claude Code.

## Tool reference

- **Tool Spec:** `docs/tools/kit-self-check-spec.md`
- **Tool Template:** `docs/tools/kit-self-check-template.md`

## Implementation

In a Claude Code session, the kit-self-check capability is exercised as follows:

### Input mapping

| Tool Input | Claude Code Action |
|------------|-------------------|
| `kit_abbreviation` | Provided by the operator or by the TOOL-KIT-SYNC-AUDIT orchestrator |
| `workspace_root` | The parent directory containing all `aieos-*` kit repositories |
| `check_scope` | Provided by the operator. Defaults to `full` if not specified |

### Execution steps

1. **Load manifest.** Read `kit-manifest.yml` from the governance-foundation repository root. Locate the entry for the specified `kit_abbreviation`.

2. **Locate the kit.** Resolve the kit directory using the manifest's `repository` field under `workspace_root`.

3. **Internal checks:**
   - **Four-file completeness:** Use the Glob tool to search for `docs/specs/{spec_file}`, `docs/artifacts/{type}-template.md`, `docs/prompts/{type}-prompt.md`, `docs/validators/{type}-validator.md` for each artifact. Skip prompt check when `human_authored: true`.
   - **Artifact flow match:** Read the kit's `CLAUDE.md` and extract the artifact sequence. Compare against the manifest's `artifact_flow` list.
   - **CLAUDE.md artifact list:** Read the kit's `CLAUDE.md` and extract artifact IDs and names. Compare against the manifest's `artifacts` entries.
   - **Playbook sequence:** Read `docs/playbook.md` and extract the artifact generation order. Compare against the manifest.
   - **Governance model sync:** Use the Bash tool to diff `docs/governance-model.md` against the canonical copy.
   - **Spec files exist:** Use the Glob tool to verify each `spec_file` from the manifest exists in `docs/specs/`.

4. **Boundary checks (pipeline kits):**
   - Use the Glob tool to verify `entry-from-{upstream}.md` files exist per manifest `entry_from`
   - Read each file and use the Grep tool to verify it references the `expected_artifacts`
   - Read the upstream kit's `docs/playbook.md` to verify exit artifact alignment

5. **Boundary checks (cross-cutting kits):**
   - For each `triggers[].upstream` reference, verify the artifact exists in the source kit's manifest entry
   - For each `feeds_into` entry, verify the target kit and artifact exist in the manifest
   - Verify `internal_dependencies` order against `artifact_flow`

6. **Produce output.** Format results following the template.

### Environment notes

- Claude Code reads files directly via the Read tool
- File comparisons use the Bash tool (`diff`) for byte-identical checks
- Pattern matching uses the Glob and Grep tools
- When invoked as a sub-agent by TOOL-KIT-SYNC-AUDIT, the agent receives a self-contained context package and returns the complete report

## What this binding does not define

This binding does not define policy. The rules for what constitutes a valid self-check (checks, hard gates) are defined in `kit-self-check-spec.md`. This file only describes how those rules are implemented in the Claude Code environment.

If the implementation environment changes (e.g., from Claude Code to a CI pipeline script), this binding is replaced. The tool spec, template, prompt, and validator remain unchanged.
