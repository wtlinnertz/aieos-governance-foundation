# Kit Self-Check Report

## Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-KIT-SELF-CHECK |
| Kit | {abbreviation} ({full_name}) |
| Layer | {layer number} |
| Category | {pipeline / operational / cross-cutting} |
| Workspace Root | {path} |
| Check Scope | {full / internal-only / boundaries-only} |
| Manifest Version | {manifest_version from kit-manifest.yml} |
| Timestamp | {ISO 8601} |

## Internal Consistency

| Check | Status | Detail |
|-------|--------|--------|
| Four-file completeness | PASS / FAIL | {count} artifacts checked; {detail of any gaps} |
| Artifact flow match | PASS / FAIL | {detail} |
| CLAUDE.md artifact list | PASS / FAIL | {detail} |
| Playbook sequence | PASS / FAIL | {detail} |
| Governance model sync | PASS / FAIL | {detail} |
| Spec files exist | PASS / FAIL | {detail} |

## Boundary Contracts

| Direction | Neighbor Kit | Contract File | Status | Detail |
|-----------|-------------|---------------|--------|--------|
| upstream | {kit abbreviation} | {entry-from file} | PASS / FAIL | {detail} |
| downstream | {kit abbreviation} | {declared in playbook} | PASS / FAIL | {detail} |

For cross-cutting kits, additional rows:

| Check | Status | Detail |
|-------|--------|--------|
| Trigger upstream references | PASS / FAIL | {count} triggers checked; {detail of any invalid references} |
| Feeds-into targets | PASS / FAIL | {count} feed targets checked; {detail of any invalid references} |
| Internal dependency order | PASS / FAIL | {detail} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Internal Checks | {pass count}/{total count} |
| Boundary Checks | {pass count}/{total count} |
