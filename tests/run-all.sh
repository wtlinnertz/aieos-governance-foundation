#!/usr/bin/env bash
# run-all.sh — Run all AIEOS framework test tiers in order
#
# Tier 1 (structural) gates Tier 2 (governance).
# Tier 2 gates agent integration tests.
#
# Usage:
#   ./tests/run-all.sh                              # Run Tiers 1 + 2 (skip integration)
#   ./tests/run-all.sh --with-integration           # Run all tiers including agent tests
#   ./tests/run-all.sh --with-integration --preset p5  # Run only the P5 sherpa test
#   ./tests/run-all.sh --tier1-only                 # Run Tier 1 only
#   ./tests/run-all.sh --tier2-only                 # Run Tier 2 only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_INTEGRATION=false
TIER1_ONLY=false
TIER2_ONLY=false
PRESET_FILTER=""

for arg in "$@"; do
  case "$arg" in
    --with-integration) RUN_INTEGRATION=true ;;
    --tier1-only) TIER1_ONLY=true ;;
    --tier2-only) TIER2_ONLY=true ;;
    --preset)
      # Next arg is the preset name — handled below
      ;;
    *)
      # Check if previous arg was --preset
      if [[ "${prev_arg:-}" == "--preset" ]]; then
        PRESET_FILTER="$arg"
      else
        echo "Unknown argument: $arg"; exit 1
      fi
      ;;
  esac
  prev_arg="$arg"
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

  INTEGRATION_DIR="$SCRIPT_DIR/integration/drivers"
  INTEGRATION_FAIL=0

  # Non-sherpa tests (always run unless preset filter is set)
  if [[ -z "$PRESET_FILTER" ]]; then
    echo ""
    echo "  ── Non-sherpa integration tests ──"
    echo ""
    if [[ -f "$INTEGRATION_DIR/run-enhancement.sh" ]]; then
      if ! "$INTEGRATION_DIR/run-enhancement.sh"; then
        INTEGRATION_FAIL=1
      fi
    fi
  fi

  # Auto-discover sherpa test drivers
  echo ""
  echo "  ── Sherpa integration tests ──"
  echo ""

  SHERPA_DRIVERS=()
  for driver in "$INTEGRATION_DIR"/run-sherpa-*.sh; do
    [[ -f "$driver" ]] || continue
    SHERPA_DRIVERS+=("$driver")
  done

  if [[ ${#SHERPA_DRIVERS[@]} -eq 0 ]]; then
    echo "  SKIP  No sherpa drivers found"
  else
    for driver in "${SHERPA_DRIVERS[@]}"; do
      driver_name=$(basename "$driver" .sh)
      # Extract preset name: run-sherpa-p5 → p5, run-sherpa-ambiguous → ambiguous
      preset_name="${driver_name#run-sherpa-}"

      # Apply preset filter if set
      if [[ -n "$PRESET_FILTER" ]] && [[ "$preset_name" != "$PRESET_FILTER" ]]; then
        continue
      fi

      echo ""
      echo "  ── $driver_name ──"
      echo ""
      if ! "$driver"; then
        INTEGRATION_FAIL=1
      fi
    done
  fi

  if [[ $INTEGRATION_FAIL -gt 0 ]]; then
    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║  Integration tests had FAILURES          ║"
    echo "╚══════════════════════════════════════════╝"
    exit 1
  fi
else
  echo ""
  echo "  Agent integration tests skipped (use --with-integration to include)"
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  All requested tiers PASSED              ║"
echo "╚══════════════════════════════════════════╝"
