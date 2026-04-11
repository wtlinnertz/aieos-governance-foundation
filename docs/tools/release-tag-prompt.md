# Release Tag Tool Prompt

You are invoking the release-tag tool capability.

## When to Invoke

Invoke this tool **after a Release Record (RR) is frozen** and the release needs to be tagged on the SCM platform. Typical invocation points:

- After freezing an RR with disposition "successful-full-exposure", to create the production release tag
- After any RR freeze, to ensure the SCM release history matches the AIEOS release governance trail
- As the final step of a Layer 5 (REK) completion, before handing off to Layer 6 (RRK)

## Why to Invoke

Frozen Release Records are the authoritative record of what was released. Creating a corresponding SCM tag and release ensures version control history aligns with AIEOS governance. This enables downstream consumers (operations, support, customers) to reference exact release points through the SCM's native release interface.

## Execution Instructions

1. Verify the RR is frozen by reading its Document Control section
2. Extract the release version from the RR content
3. Read the binding for the target system to determine field mappings and adapter configuration
4. Derive release notes from the RR summary section
5. Invoke the adapter's `push` operation with the tag and release notes mapped per the binding
6. Record the external release ID returned by the adapter
7. Produce output conforming to `release-tag-template.md`

## Result Interpretation

- **PASS**: The release was tagged (or confirmed already tagged via idempotent update). The external release ID is recorded and the source RR is unmodified.
- **FAIL**: The release tag could not be created. Check the error field in the audit entry for the specific failure reason.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `release-tag-spec.md`.
