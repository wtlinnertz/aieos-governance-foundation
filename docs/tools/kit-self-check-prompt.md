# Kit Self-Check Tool Prompt

You are invoking the kit-self-check tool capability.

## When to Invoke

Invoke this tool to validate the internal consistency of a single kit and its boundary contracts. Specific invocation points:

- When actively working within a kit (to verify the kit's own metadata is consistent)
- After modifying a kit's CLAUDE.md, playbook, or artifact specs
- After adding or removing artifacts from a kit
- After modifying entry-from boundary contract files
- As part of a full framework audit (invoked per-kit by TOOL-KIT-SYNC-AUDIT)

## Why to Invoke

Each kit maintains its own CLAUDE.md, playbook, specs, and boundary contracts. When artifacts are added, renamed, or resequenced, these documents can drift from each other and from the canonical manifest. This tool catches internal inconsistencies within a single kit's scope and verifies that its boundary contracts match what neighbor kits expect.

## Execution Instructions

1. **Load the manifest.** Read and parse `kit-manifest.yml` from the governance-foundation repository root. Locate the entry for the specified `kit_abbreviation`.

2. **Locate the kit.** Use the manifest's `repository` field to find the kit directory under `workspace_root`.

3. **Run internal checks.** For each check defined in `kit-self-check-spec.md`:
   - Read the relevant file in the kit directory
   - Compare against the manifest data for this kit
   - Record PASS or FAIL with detail

4. **Run boundary checks.** For each `entry_from` in the manifest:
   - Verify the `entry-from-{upstream}.md` file exists in the kit's `docs/` directory
   - Read the file and verify it references the `expected_artifacts` from the manifest
   - Read the upstream kit's playbook to verify exit artifact alignment

5. **Cross-cutting boundary checks** (for kits with `category: cross-cutting`):
   - For each trigger, verify that `upstream` artifact references resolve to real artifacts in their source kits
   - For each `feeds_into` entry, verify that `target_kit` and `target_artifact` exist in the target kit's manifest entry
   - Verify `internal_dependencies` are consistent with the `artifact_flow` order

6. **Produce output.** Format results using `kit-self-check-template.md`. Disposition is FAIL if any check fails, PASS if all checks pass.

## Result Interpretation

- **PASS**: The kit is internally consistent and its boundary contracts are aligned with neighbors. No action needed.
- **FAIL**: One or more inconsistencies found. Review the check detail column. Internal failures indicate the kit's own documents disagree with the manifest. Boundary failures indicate misalignment with neighbor kits.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `kit-self-check-spec.md`.
