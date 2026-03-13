# Validation Status Tool Prompt

You are invoking the validation-status tool capability.

## When to Invoke

Invoke this tool **after a validator produces structured JSON output** and the result needs to be reflected as a status check on the SCM platform. Typical invocation points:

- After running any artifact validator, to post the PASS/FAIL result as a commit status check
- After a PRK review validator run, to make review results visible in the SCM's PR checks interface
- After a QAK quality gate (QGR) validation, to gate a PR merge on quality results

## Why to Invoke

Validator results are produced within the AIEOS project files. Posting them to the SCM platform makes validation status visible to all contributors without requiring them to read validator JSON. This bridges the gap between AIEOS governance and SCM-native workflows (e.g., requiring all checks to pass before merge).

## Execution Instructions

1. Read the validator output file and confirm it conforms to governance-model.md §5 schema
2. Read the binding for the target system to determine field mappings and adapter configuration
3. Invoke the adapter's `push` operation with the validator result mapped per the binding
4. Record the external check ID returned by the adapter
5. Produce output conforming to `validation-status-template.md`

## Result Interpretation

- **PASS**: The status check was posted (or confirmed already posted via idempotent update). The external check ID is recorded and no AIEOS source files were modified.
- **FAIL**: The status check could not be posted. Check the error field in the audit entry for the specific failure reason.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `validation-status-spec.md`.
