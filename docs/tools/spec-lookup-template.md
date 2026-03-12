# Spec Lookup Output

## Lookup Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-SPEC-LOOKUP |
| Requested Artifact Type | {artifact type} |
| Kit | {kit name} |
| Spec File Path | {path to spec file} |
| Spec Version | {version or "NOT FOUND"} |
| Timestamp | {ISO 8601} |

## Hard Gates Found

| Gate Name | Description |
|-----------|-------------|
| {gate_name} | {brief description from spec} |

## Spec Content

```markdown
{full content of the spec file, unmodified}
```

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
