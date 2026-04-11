# Handoff Navigator Output

## Handoff Record Header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-HANDOFF-NAVIGATOR |
| Initiative | {initiative ID} |
| Source Kit | {source kit name} (Layer {N}) |
| Destination Kit | {destination kit name} (Layer {N}) |
| Preset | {P1–P5} |
| Timestamp | {ISO 8601} |

## Exit Condition Verification

| Condition | Status | Evidence |
|-----------|--------|----------|
| {exit condition from source kit playbook} | {Met / Unmet} | {artifact ID, freeze status, file reference} |

| Field | Value |
|-------|-------|
| Exit Conditions Met | {Yes / No} |
| Blocking Items | {list of unmet conditions, or "None"} |

## Handoff Artifacts

| Artifact | Artifact ID | Freeze Status | File Path | Required By Destination |
|----------|-------------|---------------|-----------|------------------------|
| {artifact name} | {ID} | {Frozen / Unfrozen / Missing} | {path} | {Yes / No} |

## Entry-From Reference

| Field | Value |
|-------|-------|
| Entry-From File | {path to entry-from-{source}.md in destination kit} |
| Required Artifacts | {list from entry-from file} |
| First Artifact in Destination | {name of first artifact to produce} |

## Cross-Cutting Kit Activations

| Kit | Trigger Condition | Triggered | Status | Action Needed |
|-----|-------------------|-----------|--------|---------------|
| SCK | {trigger or "N/A"} | {Yes/No} | {Active/Not Started/Complete/N/A} | {what to do, or "None"} |
| QAK | {trigger or "N/A"} | {Yes/No} | {Active/Not Started/Complete/N/A} | {what to do, or "None"} |
| DCK | {trigger or "N/A"} | {Yes/No} | {Active/Not Started/Complete/N/A} | {what to do, or "None"} |
| PINFK | {trigger or "N/A"} | {Yes/No} | {Active/Not Started/Complete/N/A} | {what to do, or "None"} |
| DKK | {trigger or "N/A"} | {Yes/No} | {Active/Not Started/Complete/N/A} | {what to do, or "None"} |

## Next Steps in Destination Kit

| # | Action | Description |
|---|--------|-------------|
| 1 | {first action} | {e.g., "Complete RER (human-authored gate)"} |
| 2 | {second action} | {e.g., "Decide: reuse existing RCF or generate new"} |

## ER Update Instructions

| Field | Update |
|-------|--------|
| Source Kit Section | {what to record in the ER for the completed kit} |
| Destination Kit Section | {what to initialize in the ER for the entering kit} |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |
| Handoff Ready | {Yes / No — blocked by: {list}} |
