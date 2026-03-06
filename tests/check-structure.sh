#!/usr/bin/env bash
# check-structure.sh — AIEOS Kit Structural Auto-Validation Script
#
# Usage: ./check-structure.sh <kit-root-path>
#
# Checks all [auto]-annotated items from aieos-governance-foundation/docs/kit-structure-standard.md.
# Exits with non-zero code if any check fails (CI-compatible).
#
# See aieos-governance-foundation/docs/kit-structure-standard.md for full check descriptions.

set -euo pipefail

AIEOS_SPEC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  echo "Usage: $0 <kit-root-path>"
  echo ""
  echo "Example:"
  echo "  $0 /path/to/aieos-engineering-execution-kit"
  exit 1
}

if [[ $# -ne 1 ]]; then
  usage
fi

KIT_ROOT="$(cd "$1" && pwd)"

if [[ ! -d "$KIT_ROOT" ]]; then
  echo "ERROR: Kit root path does not exist: $KIT_ROOT"
  exit 1
fi

# ─── Output helpers ──────────────────────────────────────────────────────────

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

check_file() {
  local rel_path="$1"
  local description="$2"
  if [[ -f "$KIT_ROOT/$rel_path" ]]; then
    pass "[$description] $rel_path exists"
  else
    fail "[$description] $rel_path missing"
  fi
}

check_dir() {
  local rel_path="$1"
  local description="$2"
  if [[ -d "$KIT_ROOT/$rel_path" ]]; then
    pass "[$description] $rel_path/ exists"
  else
    fail "[$description] $rel_path/ missing"
  fi
}

# ─── Part 1: Required Files ───────────────────────────────────────────────────

echo ""
echo "=== Part 1: Required Files ==="
check_file "README.md" "P1-F1"
check_file "CLAUDE.md" "P1-F2"
check_file "docs/playbook.md" "P1-F3"
check_file "docs/index.md" "P1-F4"
check_file "docs/how-to-adapt.md" "P1-F5"
check_file "docs/how-to-use-with-ai.md" "P1-F6"
check_file "docs/governance-model.md" "P1-F7"

# ─── Part 1: Required Directories ────────────────────────────────────────────

echo ""
echo "=== Part 1: Required Directories ==="
check_dir "docs/specs" "P1-D1"
check_dir "docs/artifacts" "P1-D2"
check_dir "docs/prompts" "P1-D3"
check_dir "docs/validators" "P1-D4"
check_dir "examples" "P1-D5"
check_dir "tests" "P1-D6"

# ─── Part 2: Four-File Completeness ──────────────────────────────────────────

echo ""
echo "=== Part 2: Four-File Completeness ==="

if [[ ! -d "$KIT_ROOT/docs/specs" ]]; then
  fail "[P2-4F] docs/specs/ directory missing — cannot check four-file completeness"
else
  spec_count=0
  for spec_file in "$KIT_ROOT/docs/specs/"*-spec.md; do
    [[ -f "$spec_file" ]] || continue
    spec_count=$((spec_count + 1))

    spec_filename="$(basename "$spec_file")"
    type_name="${spec_filename%-spec.md}"

    # Template
    template_path="docs/artifacts/${type_name}-template.md"
    if [[ -f "$KIT_ROOT/$template_path" ]]; then
      pass "[P2-4F] $type_name: template exists ($template_path)"
    else
      fail "[P2-4F] $type_name: template missing ($template_path)"
    fi

    # Prompt
    prompt_path="docs/prompts/${type_name}-prompt.md"
    if [[ -f "$KIT_ROOT/$prompt_path" ]]; then
      pass "[P2-4F] $type_name: prompt exists ($prompt_path)"
    else
      # Some artifact types (e.g., SRER — human-authored entry gates) intentionally
      # have no generation prompt. Issue a warning rather than a hard fail.
      echo "  WARN  [P2-4F] $type_name: prompt missing ($prompt_path) — verify this is intentional"
    fi

    # Validator
    validator_path="docs/validators/${type_name}-validator.md"
    if [[ -f "$KIT_ROOT/$validator_path" ]]; then
      pass "[P2-4F] $type_name: validator exists ($validator_path)"
    else
      fail "[P2-4F] $type_name: validator missing ($validator_path)"
    fi
  done

  if [[ $spec_count -eq 0 ]]; then
    fail "[P2-4F] No spec files found in docs/specs/"
  else
    pass "[P2-4F] Found $spec_count spec file(s) in docs/specs/"
  fi
fi

# ─── Part 2: Naming Convention ────────────────────────────────────────────────

echo ""
echo "=== Part 2: Naming Conventions ==="

# Specs must match *-spec.md
non_spec_specs=()
for f in "$KIT_ROOT/docs/specs/"*.md; do
  [[ -f "$f" ]] || continue
  basename_f="$(basename "$f")"
  if [[ ! "$basename_f" =~ ^.+-spec\.md$ ]] && [[ "$basename_f" != "README.md" ]]; then
    non_spec_specs+=("$basename_f")
  fi
done
if [[ ${#non_spec_specs[@]} -eq 0 ]]; then
  pass "[P2-NC] All docs/specs/ files match *-spec.md naming pattern"
else
  fail "[P2-NC] docs/specs/ files with non-standard names: ${non_spec_specs[*]}"
fi

# Validators must match *-validator.md
non_validator_validators=()
for f in "$KIT_ROOT/docs/validators/"*.md; do
  [[ -f "$f" ]] || continue
  basename_f="$(basename "$f")"
  if [[ ! "$basename_f" =~ ^.+-validator\.md$ ]] && [[ "$basename_f" != "README.md" ]]; then
    non_validator_validators+=("$basename_f")
  fi
done
if [[ ${#non_validator_validators[@]} -eq 0 ]]; then
  pass "[P2-NC] All docs/validators/ files match *-validator.md naming pattern"
else
  fail "[P2-NC] docs/validators/ files with non-standard names: ${non_validator_validators[*]}"
fi

# ─── Part 3: Validator JSON Output Schema ─────────────────────────────────────

echo ""
echo "=== Part 3: Validator Output JSON Schema ==="

json_files_found=0
json_schema_fail_count=0
required_keys=("status" "hard_gates" "blocking_issues" "warnings" "completeness_score")

shopt -s globstar nullglob 2>/dev/null || true

for json_file in $(find "$KIT_ROOT/examples" -path "*/validator-outputs/*.json" -type f 2>/dev/null | sort -u); do
  [[ -f "$json_file" ]] || continue
  json_files_found=$((json_files_found + 1))
  rel_json="$(realpath --relative-to="$KIT_ROOT" "$json_file")"
  schema_ok=true
  for key in "${required_keys[@]}"; do
    if ! grep -q "\"$key\"" "$json_file" 2>/dev/null; then
      fail "[P3-JSON] $rel_json: missing required key '$key'"
      schema_ok=false
      json_schema_fail_count=$((json_schema_fail_count + 1))
    fi
  done
  if [[ "$schema_ok" == "true" ]]; then
    pass "[P3-JSON] $rel_json: all required keys present"
  fi
done

if [[ $json_files_found -eq 0 ]]; then
  echo "  WARN  [P3-JSON] No validator output JSON files found in examples/**/validator-outputs/"
else
  pass "[P3-JSON] Checked $json_files_found JSON file(s)"
fi

# ─── Part 5: Governance Model Sync ───────────────────────────────────────────

echo ""
echo "=== Part 5: Governance Model Sync ==="

CANONICAL_GM="$AIEOS_SPEC_DIR/governance-model.md"
KIT_GM="$KIT_ROOT/docs/governance-model.md"

if [[ ! -f "$CANONICAL_GM" ]]; then
  fail "[P5-GM] Canonical governance-model.md not found at $CANONICAL_GM"
elif [[ ! -f "$KIT_GM" ]]; then
  fail "[P5-GM] Kit governance-model.md not found at $KIT_GM"
else
  if diff -q "$CANONICAL_GM" "$KIT_GM" > /dev/null 2>&1; then
    pass "[P5-GM] docs/governance-model.md is identical to aieos-governance-foundation/governance-model.md"
  else
    fail "[P5-GM] docs/governance-model.md differs from aieos-governance-foundation/governance-model.md (run: diff $CANONICAL_GM $KIT_GM)"
  fi
fi

# ─── Part 7: Tests Directory ─────────────────────────────────────────────────

echo ""
echo "=== Part 7: Structural Integrity Tests ==="

if [[ ! -d "$KIT_ROOT/tests" ]]; then
  fail "[P7-TESTS] tests/ directory missing"
else
  test_files=("$KIT_ROOT/tests/"*.md)
  if [[ ${#test_files[@]} -eq 0 ]] || [[ ! -f "${test_files[0]}" ]]; then
    fail "[P7-TESTS] No test files found in tests/"
  else
    test_file_names=()
    for tf in "${test_files[@]}"; do
      [[ -f "$tf" ]] && test_file_names+=("$(basename "$tf")")
    done
    pass "[P7-TESTS] Found ${#test_file_names[@]} test file(s) in tests/: ${test_file_names[*]}"
  fi
fi

# ─── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════"
echo "  Kit: $(basename "$KIT_ROOT")"
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
