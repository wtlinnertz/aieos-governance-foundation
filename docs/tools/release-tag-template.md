# Release Tag Output

## Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-RELEASE-TAG |
| RR Artifact ID | {RR artifact ID} |
| RR Path | {file path} |
| Release Version | {semantic version} |
| Target System | {abstract target identifier} |
| Timestamp | {ISO 8601} |

## Tag Result

| Field | Value |
|-------|-------|
| Tag Name | {tag name, e.g., v1.0.0} |
| External Release ID | {SCM's release identifier} |
| External URL | {URL to the release on the SCM, or "N/A" if not applicable} |
| Action Taken | Created / Updated / Skipped (idempotent no-op) |

## Release Notes Summary

| Field | Value |
|-------|-------|
| Source Section | {RR section used for release notes, e.g., "RR §Summary"} |
| Content Preview | {first 500 characters of published release notes, or "Full content published"} |
| Release Disposition | {from RR: successful-full-exposure, rollback, etc.} |

## Audit Entry

| Field | Value |
|-------|-------|
| Timestamp | {ISO 8601} |
| RR Artifact ID | {RR artifact ID} |
| External Release ID | {external release ID} |
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
| Idempotent | Yes / No / Not Tested (first tag) |
