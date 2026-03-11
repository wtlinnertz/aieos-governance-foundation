#!/usr/bin/env bash
# run-tier2.sh — Tier 2: Python test suite for framework validation
#
# Runs pytest against the AIEOS governance test suite.
# Exit code 0 = all pass. Non-zero = failures found.
#
# Usage: ./tests/run-tier2.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "=== Tier 2: Framework Validation (pytest) ==="
echo ""

cd "$SCRIPT_DIR"
python3 -m pytest "$@"
