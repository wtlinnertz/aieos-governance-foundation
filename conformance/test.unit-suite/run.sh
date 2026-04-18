#!/usr/bin/env bash
# Conformance suite entry point for test.unit-suite.
#
# Contract (stable — the M4 harness will implement against this):
#   Invocation: run.sh <adapter-reference>
#   Environment:
#     AIEOS_FIXTURES_DIR  — absolute path to the fixtures directory
#     AIEOS_EXPECTED_DIR  — absolute path to the expected directory
#     AIEOS_OUTPUT_DIR    — absolute path where the adapter should write findings + evidence
#   Exit 0 if every fixture was invoked and produced output; non-zero on
#   adapter or driver crashes. Pass/fail evaluation against criteria.yaml is
#   the harness's job, NOT this script's.
#
# v1 status: PLACEHOLDER. The real conformance harness ships in M4 (4.0.1)
# and will interpret this script's contract to drive adapters through the
# full fixture set. Until then, this script prints its configured interface
# and exits 0 as a structural-only affirmation that the suite is wired up.

set -euo pipefail

ADAPTER_REF="${1:-<not-provided>}"

cat <<EOF
[test.unit-suite/run.sh — placeholder]
  Adapter reference: ${ADAPTER_REF}
  Fixtures dir:      ${AIEOS_FIXTURES_DIR:-<unset>}
  Expected dir:      ${AIEOS_EXPECTED_DIR:-<unset>}
  Output dir:        ${AIEOS_OUTPUT_DIR:-<unset>}

This script does not invoke the adapter in v1 — the M4 conformance harness
will. The skeleton here is a structural reference for adapter authors and a
stable interface the harness will drive.
EOF

exit 0
