# AIEOS Spec File Standard

Spec files define the content rules, hard gates, and quality criteria for each governed artifact type. They are the authoritative source of truth for what a compliant artifact looks like. Changes to specs directly affect whether frozen artifacts remain compliant and whether validators produce correct judgments.

This standard defines the minimum versioning requirements for spec files across all kits.

---

## Version Field

Every spec file must carry a version field immediately after its title line, before any content sections:

```
Version: v{N}.{N}
```

Example: `Version: v1.0`

The version field identifies which revision of the spec's rules was active when artifacts were generated and validated against it. This allows frozen artifacts to declare the spec version in effect at generation time, enabling accurate retrospective assessment.

New spec files start at `v1.0`. Retrofitted files that are receiving their first version field also start at `v1.0` — the retrofit is not a content change.

### Change Categories

| Category | Version Bump | Definition | Downstream Impact |
|----------|-------------|------------|-------------------|
| **Minor** | `v_.1 → v_.2` (patch) | Clarification only; no change to what is required; no new constraints; no new hard gates | None — already-generated artifacts remain valid |
| **Significant** | `v1.0 → v1.1` | New hard gate, tightened constraint, new required field, or new content rule added | Artifacts generated after the change should be reviewed against updated spec; already-frozen artifacts are grandfathered but should note the spec version active at generation time |
| **Breaking** | `v1.x → v2.0` | Removal of a hard gate, loosening of a constraint, or restructuring that changes what a compliant artifact looks like | Requires explicit authorization and documented business justification before the change is made; may require re-validation of frozen artifacts |

**When in doubt, use the higher category.** A significant change mistakenly treated as a minor change can propagate outdated validation silently. The cost of a version bump is low; the cost of untracked spec drift is high.

---

## Recording Spec Versions in Generated Artifacts

Every generated artifact's Document Control section must include a `Spec Version` field recording the version of the spec that was active when the artifact was generated. This field is populated at generation time and becomes part of the frozen artifact's provenance record.

Templates must include a `Spec Version` placeholder in their Document Control section:

**Table format:**
```
| Spec Version | {spec version} |
```

**List format:**
```
- Spec Version: {spec version}
```

When a spec version changes (Significant or Breaking), artifacts generated under the previous version are grandfathered — they do not retroactively fail. However, if re-entry occurs on a frozen artifact, the re-generated artifact must be validated against the current spec version, and the new spec version must be recorded.

---

## Recording Principles Versions in Generated Artifacts

When a generation prompt uses principles files as input (as required by the `principles_coverage` hard gate in applicable kits), the generated artifact's Document Control section must include a `Principles Version` field recording the version(s) of the principles file(s) that were active at generation time.

Templates must include a `Principles Version` placeholder in their Document Control section:

**Table format:**
```
| Principles Version | {principles file versions} |
```

**List format:**
```
- Principles Version: {principles file versions}
```

The value should list each principles file and its version (e.g., `security-principles v1.0, product-discovery-principles v1.0`). If no principles files were used, state `N/A`.

---

## What Belongs in a Spec vs. Other Files

| Belongs in Spec | Belongs Elsewhere |
|-----------------|------------------|
| Hard gates and content rules | Organizational policy (principles files) |
| Required sections and format requirements | AI generation behavior (prompt files) |
| Failure examples and completeness rules | Pass/fail judgment procedure (validator files) |
| Relationship rules and upstream dependencies | Document structure (template files) |

Specs define **what a compliant artifact looks like**. They do not define how to generate it (prompts), how to judge it (validators), what it looks like (templates), or what the organization requires (principles).

---

## Maintenance

Spec files are governed documents within their kit. Changes to specs can affect:

1. **Validators** — which reference specs for hard gate definitions
2. **Prompts** — which reference specs for content rules
3. **Frozen artifacts** — which were validated against a specific spec version

When changing a spec:

- Bump the version field with every change, including minor clarifications
- If the change adds a new hard gate, update the corresponding validator to check it (Significant change)
- If the change modifies existing hard gates, assess whether frozen artifacts generated under the old rules need re-validation (Breaking change)
- Record the spec version change in the kit's changelog or commit history

In kit playbooks, spec version changes are a named trigger type in the re-entry protocol: a Significant or Breaking change may require re-validation of artifacts generated under the previous version.
