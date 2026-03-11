#!/usr/bin/env bash
# run-all.sh — Run all AIEOS framework test tiers in order
#
# Tier 1 (structural) gates Tier 2 (governance).
# Tier 2 gates agent integration tests.
# Use --skip-integration to run only Tiers 1 and 2.
#
# Usage:
#   ./tests/run-all.sh                    # Run Tiers 1 + 2 (skip integration)
#   ./tests/run-all.sh --with-integration # Run all tiers including agent tests
#   ./tests/run-all.sh --tier1-only       # Run Tier 1 only
#   ./tests/run-all.sh --tier2-only       # Run Tier 2 only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_INTEGRATION=false
TIER1_ONLY=false
TIER2_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --with-integration) RUN_INTEGRATION=true ;;
    --tier1-only) TIER1_ONLY=true ;;
    --tier2-only) TIER2_ONLY=true ;;
    *) echo "Unknown argument: $arg"; exit 1 ;;
  esac
done

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  AIEOS Framework Test Suite              ║"
echo "╚══════════════════════════════════════════╝"

# ─── Tier 1 ──────────────────────────────────────────────────────────────────

if [[ "$TIER2_ONLY" != "true" ]]; then
  echo ""
  echo "▶ Tier 1: Structural Validation"
  echo ""

  if ! "$SCRIPT_DIR/run-tier1.sh"; then
    echo ""
    echo "✗ Tier 1 FAILED — stopping. Fix structural issues before running Tier 2."
    exit 1
  fi

  echo ""
  echo "✓ Tier 1 PASSED"
fi

if [[ "$TIER1_ONLY" == "true" ]]; then
  exit 0
fi

# ─── Tier 2 ──────────────────────────────────────────────────────────────────

echo ""
echo "▶ Tier 2: Framework Validation (pytest)"
echo ""

if ! "$SCRIPT_DIR/run-tier2.sh"; then
  echo ""
  echo "✗ Tier 2 FAILED — stopping. Fix governance issues before running integration tests."
  exit 1
fi

echo ""
echo "✓ Tier 2 PASSED"

if [[ "$TIER2_ONLY" == "true" ]]; then
  exit 0
fi

# ─── Agent Integration ───────────────────────────────────────────────────────

if [[ "$RUN_INTEGRATION" == "true" ]]; then
  echo ""
  echo "▶ Agent Integration Tests"
  echo ""

  if ! command -v claude &>/dev/null; then
    echo "  SKIP  claude CLI not found — agent integration tests require Claude Code"
    echo "  Install: https://code.claude.com"
    exit 0
  fi

  "$SCRIPT_DIR/integration/drivers/run-enhancement.sh"
else
  echo ""
  echo "  Agent integration tests skipped (use --with-integration to include)"
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  All requested tiers PASSED              ║"
echo "╚══════════════════════════════════════════╝"
