#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
FIXTURES="$SCRIPT_DIR/fixtures"
PASS=0
FAIL=0

assert_contains() {
  local label="$1" needle="$2" haystack="$3"
  if echo "$haystack" | grep -qF "$needle"; then
    echo "PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $label — output does not contain '$needle'"
    echo "  actual output:"
    echo "$haystack" | head -20 | sed 's/^/    /'
    FAIL=$((FAIL + 1))
  fi
}

assert_not_contains() {
  local label="$1" needle="$2" haystack="$3"
  if echo "$haystack" | grep -qF "$needle"; then
    echo "FAIL: $label — output should not contain '$needle'"
    FAIL=$((FAIL + 1))
  else
    echo "PASS: $label"
    PASS=$((PASS + 1))
  fi
}

# Test 1: Extracts and formats table from transcript
result=$(python3 "$LIB_DIR/extract.py" "$FIXTURES/sample-transcript.jsonl")
assert_contains "formatted table has aligned pipes" "| foo  |" "$result"
assert_contains "contains separator" "|---" "$result"

# Test 2: Non-table text is excluded
assert_not_contains "excludes prose" "Done!" "$result"
assert_not_contains "excludes intro text" "Here is a table" "$result"

# Test 3: Diagram is included and formatted
assert_contains "diagram present" "┌──────┐" "$result"
assert_contains "diagram box" "│ Test │" "$result"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
