# Dependency Check Tool Prompt

You are invoking the dependency-check tool capability.

## When to Invoke

Invoke this tool **before generating any downstream artifact**. The freeze-before-promote invariant requires that all upstream dependencies are frozen before generation begins. This tool verifies that precondition.

Specific invocation points:
- Before generating any artifact that has upstream dependencies (check the artifact's spec for its "Upstream Dependencies" section)
- At the start of any playbook step that involves artifact generation
- When re-entering a frozen artifact flow (to verify the dependency chain is still intact)

## Why to Invoke

Generating an artifact against unfrozen or missing upstream dependencies produces unreliable output. This tool prevents wasted generation and validation cycles by confirming the dependency chain is satisfied before work begins.

## Execution Instructions

1. Read the target artifact's spec to identify its upstream dependencies
2. For each upstream dependency, locate the artifact in the project's artifact directory
3. Check the artifact's Document Control section for `Status: Frozen`
4. Produce output conforming to `dependency-check-template.md`

## Result Interpretation

- **PASS**: All upstream dependencies are frozen. Proceed with generation.
- **FAIL**: One or more dependencies are missing or unfrozen. Do not proceed with generation. Report the blocking dependencies to the operator.

## Spec Reference

The authoritative rules, constraints, and hard gates for this tool are defined in `dependency-check-spec.md`.
