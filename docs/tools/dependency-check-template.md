# Dependency Check Output

## Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-DEPENDENCY-CHECK |
| Target Artifact Type | {artifact type} |
| Kit | {kit name} |
| Artifact Directory | {path} |
| Timestamp | {ISO 8601} |

## Dependency Status

| Upstream Artifact | Artifact ID | File | Freeze Status | Notes |
|-------------------|-------------|------|---------------|-------|
| {artifact type} | {ID or "NOT FOUND"} | {file path or "MISSING"} | Frozen / Unfrozen / Missing | {any relevant detail} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Dependencies Checked | {count} |
| Dependencies Satisfied | {count} |
| Blocking Dependencies | {list of unsatisfied dependencies, or "None"} |
