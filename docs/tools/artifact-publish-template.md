# Artifact Publish Output

## Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-ARTIFACT-PUBLISH |
| Artifact ID | {artifact ID} |
| Artifact Path | {file path} |
| Target System | {abstract target identifier} |
| Timestamp | {ISO 8601} |

## Publish Result

| Field | Value |
|-------|-------|
| External ID | {external system's resource identifier} |
| External URL | {URL to the published resource, or "N/A" if not applicable} |
| Action Taken | Created / Updated / Skipped (idempotent no-op) |
| Content Hash | {hash of the artifact content at time of publish} |

## Audit Entry

| Field | Value |
|-------|-------|
| Timestamp | {ISO 8601} |
| Artifact ID | {artifact ID} |
| External ID | {external ID} |
| Action | push |
| Result | success / failure / skipped |
| Duration (ms) | {wall-clock time} |
| Error | {error message or "None"} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Source Modified | Yes / No |
| Idempotent | Yes / No / Not Tested (first publish) |
