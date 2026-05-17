# Work Item Sync Output

## Report header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-WORK-ITEM-SYNC |
| WDD Artifact ID | {WDD artifact ID} |
| WDD Path | {file path} |
| Target System | {abstract target identifier} |
| Timestamp | {ISO 8601} |

## Sync summary

| Field | Value |
|-------|-------|
| Total Work Items | {count} |
| Items Synced | {count} |
| Items Failed | {count} |
| Groups Synced | {count} |
| Groups Failed | {count} |

## Item mapping table

| WDD Item ID | Item Title | Work Group | External ID | External URL | Action Taken | Result |
|-------------|------------|------------|-------------|-------------|-------------|--------|
| {item ID} | {title} | {group name} | {external tracker ID} | {URL or "N/A"} | Created / Updated / Skipped | success / failure |

## Group mapping table

| WDD Work Group | External Group ID | External Group URL | Action Taken | Child Items |
|----------------|-------------------|-------------------|-------------|-------------|
| {group name} | {external epic/parent ID} | {URL or "N/A"} | Created / Updated / Skipped | {count} |

## Audit entries

| Timestamp | Artifact ID | Item ID | External ID | Action | Result | Duration (ms) | Error |
|-----------|-------------|---------|-------------|--------|--------|---------------|-------|
| {ISO 8601} | {WDD artifact ID} | {item ID or "group:{group name}"} | {external ID} | push | success / failure / skipped | {time} | {error or "None"} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Source Modified | Yes / No |
| Idempotent | Yes / No / Not Tested (first sync) |
| Partial Sync | Yes / No |
