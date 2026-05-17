# Artifact Publish Tool Prompt

You are invoking the artifact-publish tool capability.

## When to invoke

Invoke this tool **after an artifact is frozen** and needs to be published to an external document management system. Typical invocation points:

- After freezing a DPRD, to publish it to a wiki or document store
- After freezing an ORD, to make it available to operations teams in their documentation platform
- After freezing any artifact that external teams need access to outside the project repository

## Why to invoke

Frozen artifacts are the authoritative versions. Publishing them to external systems ensures teams who do not access the project repository can review the definitive content. This tool ensures the publish is auditable, idempotent, and does not modify the source artifact.

## Execution instructions

1. Verify the artifact is frozen by reading its Document Control section
2. Read the binding for the target system to determine field mappings and adapter configuration
3. Invoke the adapter's `push` operation with the artifact content mapped per the binding
4. Record the external ID returned by the adapter
5. Produce output conforming to `artifact-publish-template.md`

## Result interpretation

- PASS: The artifact was published (or confirmed already published via idempotent update). The external ID is recorded and the source artifact is unmodified.
- FAIL: The artifact could not be published. Check the error field in the audit entry for the specific failure reason.

## Spec reference

The authoritative rules, constraints, and hard gates for this tool are defined in `artifact-publish-spec.md`.
