#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
PASS=0
FAIL=0

assert_output() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $label"
    echo "  expected:"
    echo "$expected" | sed 's/^/    /'
    echo "  actual:"
    echo "$actual" | sed 's/^/    /'
    FAIL=$((FAIL + 1))
  fi
}

# Test 1: Default config when no file exists
TMPDIR=$(mktemp -d)
actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get autoFormat)
assert_output "default autoFormat" "true" "$actual"

actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get clipboard)
assert_output "default clipboard" "true" "$actual"

actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get unicodeDiagrams)
assert_output "default unicodeDiagrams" "false" "$actual"

actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get promptStrength)
assert_output "default promptStrength" "standard" "$actual"

# Test 2: Set and get a value
python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --set autoFormat=false
actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get autoFormat)
assert_output "set autoFormat false" "false" "$actual"

# Test 3: Set preserves other values
actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --get clipboard)
assert_output "set preserves clipboard" "true" "$actual"

# Test 4: Dump full config as JSON
actual=$(python3 "$LIB_DIR/config.py" --config-dir "$TMPDIR" --dump | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['autoFormat'])")
assert_output "dump shows updated value" "False" "$actual"

rm -rf "$TMPDIR"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
