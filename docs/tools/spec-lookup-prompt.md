# Spec Lookup Tool Prompt

You are invoking the spec-lookup tool capability.

## When to invoke

Invoke this tool **at the start of any artifact generation or validation session** to retrieve the authoritative spec for the artifact type being produced or evaluated. This ensures the AI agent works against the current spec rather than relying on previously seen or memorized rules.

Specific invocation points:
- Before generating an artifact — to know which hard gates and content rules to satisfy
- Before validating an artifact — to know which hard gates to evaluate against
- When a spec version change is suspected — to confirm the current version
- When producing a tool output that references spec gates — to ensure accuracy

## Why to invoke

Specs are the single source of truth for artifact compliance (governance-model.md §2). Working from a stale or incorrectly recalled spec leads to artifacts that fail validation. This tool eliminates that risk by providing the live spec content at the point of need.

## Execution instructions

1. Locate the kit's `docs/specs/` directory
2. Find the file matching `{artifact_type}-spec.md`
3. Read the full file content
4. Extract the `Version:` field from the header
5. Extract hard gate names from the hard gates section
6. Produce output conforming to `spec-lookup-template.md`

Do not summarize, paraphrase, or abbreviate the spec content. Return it in full.

## Result interpretation

- PASS: The spec was found and returned in full. Proceed with generation or validation using the returned content.
- FAIL: The spec could not be found or was ambiguous. Do not proceed — resolve the lookup error first.

## Spec reference

The authoritative rules, constraints, and hard gates for this tool are defined in `spec-lookup-spec.md`.
