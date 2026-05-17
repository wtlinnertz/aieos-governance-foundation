# Kit Sync Audit Report

## Report header

| Field | Value |
|-------|-------|
| Tool ID | TOOL-KIT-SYNC-AUDIT |
| Workspace Root | {path} |
| Scope | {full / registry-only / boundaries-only / sync-files-only / single-kit:{KIT}} |
| Manifest Version | {manifest_version from kit-manifest.yml} |
| Governance Model Version | {governance_model_version from kit-manifest.yml} |
| Timestamp | {ISO 8601} |
| Kits Audited | {count} |

## Summary

| Severity | Findings | Status |
|----------|----------|--------|
| CRITICAL | {count} | PASS / FAIL |
| HIGH | {count} | PASS / FAIL |
| MEDIUM | {count} | PASS / FAIL |

## Disposition

| Field | Value |
|-------|-------|
| Status | PASS / FAIL |
| Summary | {one-sentence verdict} |

Disposition rule: FAIL if any CRITICAL finding exists. Otherwise PASS.

## CRITICAL findings

| ID | Check | Kit | Location | Expected | Actual | Detail |
|----|-------|-----|----------|----------|--------|--------|
| C-{NNN} | {check name} | {kit abbreviation or "—"} | {file:line} | {value from manifest} | {value found in file} | {factual description} |

## HIGH findings

| ID | Check | Kit | Location | Expected | Actual | Detail |
|----|-------|-----|----------|----------|--------|--------|
| H-{NNN} | {check name} | {kit abbreviation} | {file:line} | {value from manifest} | {value found in file} | {factual description} |

## MEDIUM findings

| ID | Check | Kit | Location | Expected | Actual | Detail |
|----|-------|-----|----------|----------|--------|--------|
| M-{NNN} | {check name} | {kit abbreviation} | {file:line} | {value from manifest} | {value found in file} | {factual description} |

## Per-Kit status

| Kit | Layer | CRITICAL | HIGH | MEDIUM | Status |
|-----|-------|----------|------|--------|--------|
| {abbreviation} | {layer number} | {count} | {count} | {count} | PASS / FAIL |
