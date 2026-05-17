# Cross-Kit Sync Audit Playbook

This playbook documents how to run the kit sync audit, how to maintain the kit manifest, and how to update it when the framework changes. It is written for human operators and can be followed by the AI sherpa.

---

## Prerequisites

### Workspace layout

All 15 kit repositories and the governance foundation must be cloned as sibling directories under a single workspace root:

```
{workspace_root}/
  aieos-governance-foundation/
  aieos-strategic-direction-kit/
  aieos-product-intelligence-kit/
  aieos-solution-sourcing-kit/
  aieos-engineering-execution-kit/     # local name; GitHub repo is aieos-engineering-execution
  aieos-release-exposure-kit/
  aieos-reliability-resilience-kit/
  aieos-insight-evolution-kit/
  aieos-operational-diagnostics-kit/
  aieos-quality-assurance-kit/
  aieos-security-compliance-kit/
  aieos-data-configuration-kit/
  aieos-platform-infrastructure-kit/
  aieos-documentation-knowledge-kit/
  aieos-peer-review-kit/
  aieos-business-process-kit/
```

If any kit is missing, the audit will report it as a CRITICAL finding. Clone missing repos before running.

### Manifest

The canonical manifest is `aieos-governance-foundation/kit-manifest.yml`. It must exist and be valid YAML. If it does not exist, the audit cannot run.

---

## Running a sync audit

### Full audit

In a Claude Code session, with your working directory at the workspace root:

1. Ask Claude to run `TOOL-KIT-SYNC-AUDIT` with `workspace_root` set to the current directory.
2. Claude reads the manifest, locates all kits, and executes checks in severity order (CRITICAL → HIGH → MEDIUM).
3. Review the output report. Fix CRITICAL findings first, then HIGH, then MEDIUM.
4. Re-run after fixes to confirm a clean report.

Example prompt:
> Run TOOL-KIT-SYNC-AUDIT against this workspace. Full scope. Follow the instructions in `aieos-governance-foundation/docs/tools/kit-sync-audit-prompt.md`.

### Scoped audit

To check only a subset:

| Scope | What it checks | When to use |
|-------|---------------|-------------|
| `registry-only` | Manifest version + kit registry consistency | Quick check after updating kit tables |
| `boundaries-only` | Boundary contract existence + content | After modifying entry-from files |
| `sync-files-only` | Governance model copy sync | After governance model changes |
| `single-kit:EEK` | All checks for one kit only | After modifying a specific kit |

### Single-Kit self-Check

To validate one kit in depth:

1. Ask Claude to run `TOOL-KIT-SELF-CHECK` with `kit_abbreviation` and `workspace_root`.
2. Claude checks internal consistency (four-file completeness, artifact flow, CLAUDE.md, playbook, governance model sync) and boundary contracts.

Example prompt:
> Run TOOL-KIT-SELF-CHECK for PIK against this workspace. Follow the instructions in `aieos-governance-foundation/docs/tools/kit-self-check-prompt.md`.

---

## Maintaining the manifest

### When to update

Update `kit-manifest.yml` **before** updating prose documents. The manifest is the source of truth — prose is validated against it.

| Change | Manifest update required |
|--------|------------------------|
| New kit added | Yes — add full kit entry under `kits:`, add to `synchronized_files` copies, add to relevant preset `required_kits` or `optional_kits` |
| Kit removed or deprecated | Yes — set `status: "deprecated"` |
| Artifact added to existing kit | Yes — add to kit's `artifacts` list, update `artifact_flow`, add `dependency_edges` |
| Artifact removed | Yes — remove from `artifacts`, `artifact_flow`, and `dependency_edges` |
| Artifact renamed | Yes — update `id` and `full_name` in `artifacts`, update `artifact_flow` and `dependency_edges` |
| Boundary contract added | Yes — add to kit's `entry_from` map, add corresponding `dependency_edges` entry |
| Boundary contract removed | Yes — remove from `entry_from` and `dependency_edges` |
| Cross-cutting trigger added/changed | Yes — update `triggers`, `feeds_into`, and/or `internal_dependencies` |
| Governance model version bumped | Yes — update `governance_model_version` field |
| Preset flow changed | Yes — update `presets` section |
| Kit description/question changed | Yes — update `question` field |
| Entry point added/removed | Yes — update `entry_points` section and kit's `entry_points` list |
| Spec file renamed | Yes — update `spec_file` in the artifact entry |

### How to update

1. Open `kit-manifest.yml` in the governance-foundation repo.
2. Make the change in the manifest.
3. Make the corresponding change in the prose documents (layer-model.md, README.md, root CLAUDE.md, flow-reference.md, etc.).
4. Run `TOOL-KIT-SYNC-AUDIT` (at least scoped to the affected area) to verify alignment.
5. Commit the manifest change alongside the prose changes.

### Validation

After editing the manifest, verify it is valid YAML:

```bash
python3 -c "import yaml; yaml.safe_load(open('kit-manifest.yml')); print('YAML valid')"
```

---

## Common scenarios

### Adding a new kit

1. Create the kit repository with standard structure (per `kit-structure-standard.md`).
2. Run `check-structure.sh` on the new kit — fix any failures.
3. Copy `governance-model.md` from governance-foundation to `docs/governance-model.md` in the new kit.
4. Update `kit-manifest.yml`:
   - Add the kit entry under `kits:` with all fields (layer, full_name, repository, category, status, optional, question, artifacts, artifact_flow, entry_from).
   - Add to `synchronized_files[0].copies`.
   - Add `dependency_edges` for the new kit's internal and cross-kit dependencies.
   - Add to relevant `presets`.
   - Add `entry_points` if the kit has external entry.
5. Update prose documents:
   - `docs/layer-model.md` — add layer description section, update Kit Registry table.
   - `README.md` — add to kit table and Kit Registry.
   - Root `CLAUDE.md` — add to kit tables and data flow diagram.
   - `docs/flow-reference.md` — add entry points and flow information.
   - `docs/initiative-presets.md` — add to relevant preset tables.
   - `docs/navigation-map.md` — add nodes and edges.
   - `docs/getting-started.md` — add scenario if applicable.
6. Run `TOOL-KIT-SYNC-AUDIT` full scope.
7. Run Tier 2 tests (`run-tier2.sh`).
8. Commit and push all changes.

### Bumping the governance model version

1. Update the version in `governance-model.md` (the `Current version:` line in §15 and the `Current value:` in §Artifact Provenance).
2. Update `governance_model_version` in `kit-manifest.yml`.
3. Copy the updated `governance-model.md` to all 15 kit repos.
4. Run `TOOL-KIT-SYNC-AUDIT` with scope `sync-files-only` to verify all copies match.
5. Commit and push governance-foundation first, then each kit.

### Adding an artifact to an existing kit

1. Create the four-file set (spec, template, prompt, validator) in the kit.
2. Update the kit's `CLAUDE.md` and `playbook.md` with the new artifact.
3. Update `kit-manifest.yml`:
   - Add the artifact to the kit's `artifacts` list.
   - Update `artifact_flow`.
   - Add `dependency_edges`.
4. Run `TOOL-KIT-SELF-CHECK` for the affected kit.
5. If the artifact creates a new boundary contract, update the downstream kit's `entry_from` in the manifest and create the `entry-from-{upstream}.md` file.
6. Run `TOOL-KIT-SYNC-AUDIT` to verify cross-kit alignment.

### Renaming a kit or artifact

1. Update `kit-manifest.yml` first (all references: `kits`, `dependency_edges`, `entry_from`, `triggers`, `feeds_into`, `presets`, `entry_points`).
2. Update all prose documents that reference the old name.
3. Run `TOOL-KIT-SYNC-AUDIT` full scope — the audit will catch any missed references.

---

## Recommended schedule

| Frequency | Action |
|-----------|--------|
| Every framework change | Run scoped audit for affected area |
| Weekly | Run full `TOOL-KIT-SYNC-AUDIT` |
| Before releasing framework changes | Run full audit + Tier 1 + Tier 2 |
| Before starting a new initiative | Run `registry-only` scope (fast check that framework is consistent) |

---

## Relationship to other healthchecks

This playbook covers the **A4 Cross-Kit Sync Audit** check in `docs/healthcheck-playbook.md`. It sits at Tier 2 in the healthcheck hierarchy:

```
Tier 1: Structural Validation (check-structure.sh per kit)
Tier 2: Governance Consistency (pytest suite)
Tier 2: Spec-Version Drift Detection
Tier 2: Cross-Kit Sync Audit (this playbook)    ← here
Tier 3: Agent Integration Tests
```

Lower tiers gate higher tiers. Do not run the sync audit until Tier 1 passes for all kits.

---

## Future automation

The following are planned but not yet built:

- CI integration: GitHub Action on governance-foundation PRs that validates the manifest against all kit repos.
- Scheduled agent: Weekly cron via Claude Code that runs a full audit and reports findings.
- Sherpa integration: Sherpa offers a sync audit before starting new initiatives if the last audit is stale.
- framework.py migration: The Tier 2 test suite's `KIT_REGISTRY` in `models/framework.py` will be migrated to consume `kit-manifest.yml` directly, eliminating one duplication point.
