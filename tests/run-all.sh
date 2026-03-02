#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_FAIL=0

run_suite() {
  local name="$1" script="$2"
  echo "=== $name ==="
  if bash "$script"; then
    echo ""
  else
    echo "SUITE FAILED: $name"
    echo ""
    TOTAL_FAIL=$((TOTAL_FAIL + 1))
  fi
}

run_suite "Display Width" "$SCRIPT_DIR/test-display-width.sh"
run_suite "Format Table" "$SCRIPT_DIR/test-format-table.sh"
run_suite "Format Diagram" "$SCRIPT_DIR/test-format-diagram.sh"
run_suite "Extract" "$SCRIPT_DIR/test-extract.sh"

echo "========================="
if [[ $TOTAL_FAIL -eq 0 ]]; then
  echo "ALL SUITES PASSED"
else
  echo "$TOTAL_FAIL SUITE(S) FAILED"
  exit 1
fi
