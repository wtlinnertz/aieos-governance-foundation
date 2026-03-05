# AIEOS Principle File Standard

Principle files define organizational policy for a kit's domain. They are **input material** for artifact generation — not governed artifacts. They are fully customizable, but they must be useful as AI input, which requires minimum structure.

An unstructured principle file is nearly useless as generation input. This standard defines the minimum structure that makes a principle file effective.

---

## Version Field

Every principle file must carry a version field in its header, before any content sections:

```
Version: v{N}.{N}
```

Example: `Version: v1.0`

The version field identifies which revision of the organizational policy was active when artifacts were generated against this file. This allows frozen artifacts to declare the principle version in effect at generation time, enabling accurate retrospective assessment.

New principle files start at `v1.0`. Retrofitted files that are receiving their first version field also start at `v1.0` — the retrofit is not a content change.

### Change Categories

| Category | Version Bump | Definition | Downstream Impact |
|----------|-------------|------------|-------------------|
| **Minor** | `v_.1 → v_.2` (patch) | Clarification only; no change to what is required; no new constraints | None — already-generated artifacts remain valid |
| **Significant** | `v1.0 → v1.1` | New requirement or tightened constraint added | Artifacts generated after the change should be reviewed against updated principles; already-frozen artifacts are grandfathered but should note the principle version active at generation time |
| **Breaking** | `v1.x → v2.0` | Removal of a requirement or loosening of a constraint | Requires explicit service owner authorization and documented business justification before the change is made |

**When in doubt, use the higher category.** A significant change mistakenly treated as a minor change can propagate outdated policy silently. The cost of a version bump is low; the cost of untracked policy drift is high.

---

## What Principle Files Are

Principle files answer: **"What standards does this organization hold in this domain?"**

They are read by AI generation prompts to constrain artifact output. A principle file that states aspirational prose ("we value quality") provides no constraint. A principle file that states specific, imperative rules ("all public APIs must have an OpenAPI spec before implementation begins") provides a constraint that can be applied.

---

## Required Structure

Every principle file must have these three sections:

### 1. Scope

One paragraph stating:
- What domain this file covers (e.g., "Backend API development in Python and Go")
- What it does not cover (e.g., "Frontend standards are in `frontend-standards.md`")
- Which kit artifacts reference this file (e.g., "Used by ACF generation prompt as architectural context")

Without a scope statement, the AI cannot determine whether a principle applies to a given artifact or work item.

### 2. Rules

The substantive content of the file. Each rule must be:

**Imperative, not aspirational.**
- ✓ "All database schema changes must include a rollback migration."
- ✗ "We care about database stability."

**Specific enough to apply without judgment.**
- ✓ "Services must expose a `/health` endpoint returning HTTP 200 when operational."
- ✗ "Services should be observable."

**Stated as a constraint, not a goal.**
- ✓ "PRs may not be merged without at least one approval from a team member who did not author the change."
- ✗ "We aim for high code review quality."

Rules may be grouped into subsections for readability. Each subsection should have a name that identifies the constraint category (e.g., "API Design", "Testing", "Security").

### 3. Enforcement Mapping

A table or list identifying which kit specs enforce each rule category.

| Rule Category | Enforced By |
|---------------|-------------|
| API design constraints | `acf-spec.md` §Security Guardrails, `tdd-spec.md` §4 Interfaces |
| Testing requirements | `dcf-spec.md` §Testing Expectations, `wdd-spec.md` DoR |
| Security baseline | `acf-spec.md` §Security Guardrails |

This mapping serves two purposes:
1. It confirms that principle rules are actually enforced somewhere in the kit's artifact chain. A rule with no enforcement mapping is advisory-only and should be noted as such.
2. It helps maintainers understand which specs need updating when rules change.

---

## What Belongs in a Principle File vs. a Spec

| Belongs in Principle File | Belongs in Spec |
|--------------------------|-----------------|
| "APIs must be versioned from first release" | "The ACF security guardrails section must include an API versioning statement" |
| "No direct database access from the UI layer" | "The SAD must document the data access layer and its boundaries" |
| "Runbooks must be tested, not just written" | Hard gate: `runbook_verification` in `ord-spec.md` |

Principle files define **what the organization requires**. Specs define **what a compliant artifact looks like**. When a principle has no corresponding spec enforcement, it is an aspirational statement and should be labeled as such.

---

## Principle File Quality Indicators

A well-written principle file:
- Has a scope statement that would let a new team member know in 30 seconds whether it applies to their work
- Has rules that could be checked by a code reviewer or QA engineer without ambiguity
- Has no rules that depend on undefined terms (e.g., "appropriate logging" without defining appropriate)
- Has an enforcement mapping with at least one entry per rule category

A poorly written principle file:
- Reads like a mission statement or values document
- Has rules that start with "we believe", "we strive", or "ideally"
- Has no mapping to specs — no enforcement chain exists
- Covers everything without scoping what it applies to

---

## Maintenance

Principle files are not governed artifacts — they have no validator or freeze point. But they should be treated as stable organizational policy:

- Changes to principle files can affect all artifacts generated after the change. Classify each change using the change categories above and follow the appropriate downstream impact protocol.
- Bump the version field with every change, including minor clarifications. This makes the change visible in the Git history and prevents silent drift.
- If a rule becomes outdated (e.g., a technology is retired), remove it. Stale rules degrade AI generation quality. A removal is a Breaking change (version major bump).
- If a rule accumulates exceptions, either tighten the rule or document the exception conditions explicitly. Undocumented exceptions rot the file.

In kit playbooks, principle file revision is a named trigger type in the re-entry protocol: a Significant or Breaking change may require re-validation of artifacts generated under the previous version.
