# Kit Sync Audit Tool Prompt

You are invoking the kit-sync-audit tool capability.

## When to invoke

Invoke this tool to verify cross-kit consistency across the AIEOS framework. Specific invocation points:

- Before starting a new initiative (to confirm the framework is internally consistent)
- After modifying governance-foundation documents (layer-model.md, flow-reference.md, initiative-presets.md, navigation-map.md)
- After adding a new kit, artifact type, or boundary contract
- After bumping the governance model version
- Periodically as a framework healthcheck (Tier 2, after structural validation and governance consistency checks pass)

## Why to invoke

Kit information is duplicated across many prose documents. When the framework evolves — new kits, renamed layers, updated artifact flows — not all documents are updated simultaneously. This tool detects silent drift between the manifest (single source of truth) and the prose documents that reference it.

## Execution instructions

1. **Load the manifest.** Read and parse `kit-manifest.yml` from the governance-foundation repository root. Verify it is valid YAML.

2. **Verify manifest version.** Read `governance-model.md` and extract the governance model version (look for the `Current value:` reference in the Artifact Provenance section). Confirm it matches `governance_model_version` in the manifest. If it does not match, record a CRITICAL finding and continue — remaining checks may produce stale results.

3. **Apply scope.** If the `scope` input is not `full`, restrict checks to the requested category:
   - `registry-only`: Run only `manifest_version_pinning` and `kit_registry_consistency`
   - `boundaries-only`: Run only `boundary_contract_existence` and `boundary_contract_content`
   - `sync-files-only`: Run only `synchronized_file_identity`
   - `single-kit:{KIT}`: Run all checks but only for the specified kit

4. **Execute checks in severity order.** Run CRITICAL checks first, then HIGH, then MEDIUM. For each check:
   - Read the relevant files
   - Compare against manifest data
   - Record findings with the exact expected value (from manifest) and actual value (from file)
   - Include the file path and line number in the Location field

5. **Cross-cutting trigger validation.** For cross-cutting kits (Layers 9–15), validate:
   - Every `triggers[].upstream` reference resolves to a real artifact in the named kit's manifest entry
   - Every `feeds_into[].target_kit` and `target_artifact` exists in the target kit's manifest entry
   - `internal_dependencies` do not create cycles within the kit
   - Trigger descriptions in `layer-model.md` are consistent with the manifest's trigger conditions

6. **Produce output.** Format results using `kit-sync-audit-template.md`. Apply the disposition rule: FAIL if any CRITICAL finding exists, PASS otherwise.

## Result interpretation

- PASS: All prose documents are consistent with the manifest. No action needed.
- FAIL: One or more inconsistencies found. Review the findings table. CRITICAL findings indicate structural misalignment that may affect downstream tools. HIGH findings indicate boundary contract or flow inconsistencies. MEDIUM findings indicate description drift that should be corrected but does not affect tool behavior.

## Spec reference

The authoritative rules, constraints, and hard gates for this tool are defined in `kit-sync-audit-spec.md`.
