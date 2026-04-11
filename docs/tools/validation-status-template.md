# Validation Status Output

## Report Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-VALIDATION-STATUS |
| Artifact ID | {artifact ID} |
| Validator Output Path | {file path} |
| Commit Ref | {commit SHA or PR number} |
| Target System | {abstract target identifier} |
| Timestamp | {ISO 8601} |

## Status Check Result

| Field | Value |
|-------|-------|
| External Check ID | {SCM's check identifier} |
| External URL | {URL to the status check on the SCM, or "N/A" if not applicable} |
| Check State | {SCM-mapped state: e.g., success / failure / pending} |
| AIEOS Status | {PASS / FAIL from the validator output} |
| Action Taken | Created / Updated / Skipped (idempotent no-op) |

## Gate Summary

| Gate Name | Result |
|-----------|--------|
| {gate name from validator output} | {PASS / FAIL} |

## Audit Entry

| Field | Value |
|-------|-------|
| Timestamp | {ISO 8601} |
| Artifact ID | {artifact ID} |
| External Check ID | {external check ID} |
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
| Idempotent | Yes / No / Not Tested (first post) |
