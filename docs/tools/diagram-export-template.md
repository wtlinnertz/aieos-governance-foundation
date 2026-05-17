# Diagram Export Output

## Report header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-DIAGRAM-EXPORT |
| Artifact ID | {artifact ID} |
| Artifact Path | {file path} |
| Output Format | {abstract format identifier} |
| Output Directory | {output directory path} |
| Timestamp | {ISO 8601} |
| Binding Used | {binding document reference} |

## Extraction summary

| Field | Value |
|-------|-------|
| Total Mermaid Blocks Found | {count} |
| Blocks Exported | {count} |
| Blocks Skipped | {count} |
| Blocks with Errors | {count} |

## Per-Diagram results

| Index | Heading Context | Output File Path | Concrete Format | File Size (bytes) | Content Hash (SHA256) |
|-------|-----------------|------------------|-----------------|--------------------|-----------------------|
| 1 | {nearest ## heading above block} | {output file path} | {concrete format from binding} | {size} | {SHA256 hash} |
| 2 | {nearest ## heading above block} | {output file path} | {concrete format from binding} | {size} | {SHA256 hash} |

## Source integrity

| Field | Value |
|-------|-------|
| Source File Hash Before | {SHA256 hash} |
| Source File Hash After | {SHA256 hash} |
| Source Modified | Yes / No |

## Audit entry

| Field | Value |
|-------|-------|
| Timestamp | {ISO 8601} |
| Artifact ID | {artifact ID} |
| Action | export |
| Output Files | {comma-separated output file paths} |
| Result | success / partial / failure |
| Duration (ms) | {wall-clock time} |
| Error | {error message or "None"} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL / PARTIAL |
| Summary | {one-sentence verdict} |
| Source Modified | Yes / No |
| Idempotent | Yes / No / Not Tested |
