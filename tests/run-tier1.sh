#!/usr/bin/env bash
# run-tier1.sh — Tier 1: Drop-in Markdown validation
#
# Runs markdownlint and markdown-link-check across all AIEOS kits.
# Exit code 0 = all pass. Non-zero = failures found.
#
# Usage: ./tests/run-tier1.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIEOS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_DIR="$SCRIPT_DIR"

PASS=0
FAIL=0
FAIL_MESSAGES=()

pass() {
  echo "  PASS  $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "  FAIL  $1"
  FAIL=$((FAIL + 1))
  FAIL_MESSAGES+=("$1")
}

# ─── Discover all kit directories ────────────────────────────────────────────

KITS=()
for dir in "$AIEOS_ROOT"/aieos-*/; do
  [[ -d "$dir" ]] && KITS+=("$dir")
done

echo ""
echo "=== Tier 1: Markdown Validation ==="
echo "Found ${#KITS[@]} kits in $AIEOS_ROOT"
echo ""

# ─── Step 1: markdownlint ────────────────────────────────────────────────────

echo "--- Step 1: markdownlint ---"

if ! command -v markdownlint-cli2 &>/dev/null; then
  fail "markdownlint-cli2 not found — install with: npm install -g markdownlint-cli2"
else
  for kit_dir in "${KITS[@]}"; do
    kit_name="$(basename "$kit_dir")"
    # Lint docs/ directory (the governed content)
    if [[ -d "$kit_dir/docs" ]]; then
      if markdownlint-cli2 --config "$CONFIG_DIR/.markdownlint.yaml" "$kit_dir/docs/**/*.md" 2>/dev/null; then
        pass "markdownlint: $kit_name/docs/"
      else
        fail "markdownlint: $kit_name/docs/ — lint errors found"
      fi
    fi
  done
fi

echo ""

# ─── Step 2: markdown-link-check ─────────────────────────────────────────────

echo "--- Step 2: markdown-link-check ---"

if ! command -v markdown-link-check &>/dev/null; then
  fail "markdown-link-check not found — install with: npm install -g markdown-link-check"
else
  for kit_dir in "${KITS[@]}"; do
    kit_name="$(basename "$kit_dir")"
    if [[ -d "$kit_dir/docs" ]]; then
      link_errors=0
      while IFS= read -r -d '' md_file; do
        if ! markdown-link-check --quiet --config "$CONFIG_DIR/.markdown-link-check.json" "$md_file" 2>/dev/null; then
          link_errors=$((link_errors + 1))
        fi
      done < <(find "$kit_dir/docs" -name "*.md" -print0)
      if [[ $link_errors -eq 0 ]]; then
        pass "link-check: $kit_name/docs/"
      else
        fail "link-check: $kit_name/docs/ — $link_errors file(s) with broken links"
      fi
    fi
  done
fi

echo ""

# ─── Step 3: check-structure.sh on all kits ──────────────────────────────────

echo "--- Step 3: structural validation (check-structure.sh) ---"

for kit_dir in "${KITS[@]}"; do
  kit_name="$(basename "$kit_dir")"
  if "$SCRIPT_DIR/check-structure.sh" "$kit_dir" > /dev/null 2>&1; then
    pass "structure: $kit_name"
  else
    fail "structure: $kit_name — run check-structure.sh for details"
  fi
done

echo ""

# ─── Summary ──────────────────────────────────────────────────────────────────

echo "════════════════════════════════════════"
echo "  Tier 1 Results"
echo "  PASS: $PASS    FAIL: $FAIL"
echo "════════════════════════════════════════"

if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "FAILING CHECKS:"
  for msg in "${FAIL_MESSAGES[@]}"; do
    echo "  - $msg"
  done
  echo ""
  echo "Result: FAIL"
  exit 1
else
  echo ""
  echo "Result: PASS"
  exit 0
fi
