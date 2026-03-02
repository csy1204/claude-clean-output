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

# Test 1: Normalize leading whitespace
input="    ┌──────┐
    │ Test │
    └──────┘
         │
    ┌────▼────┐
    │  Result │
    └─────────┘"

expected="┌──────┐
│ Test │
└──────┘
     │
┌────▼────┐
│  Result │
└─────────┘"

actual=$(echo "$input" | python3 "$LIB_DIR/format_diagram.py")
assert_output "normalize leading whitespace" "$expected" "$actual"

# Test 2: Strip trailing whitespace
input="┌───┐
│ A │
└───┘   "

expected="┌───┐
│ A │
└───┘"

actual=$(echo "$input" | python3 "$LIB_DIR/format_diagram.py")
assert_output "strip trailing whitespace" "$expected" "$actual"

# Test 3: Mixed box-drawing characters → normalize to unicode
input="+------+
| Test |
+------+"

expected="┌──────┐
│ Test │
└──────┘"

actual=$(echo "$input" | python3 "$LIB_DIR/format_diagram.py" --normalize-chars)
assert_output "ASCII to unicode box chars" "$expected" "$actual"

# Test 4: CJK inside boxes — don't break width
input="┌──────┐
│ 서버 │
└──────┘"

actual=$(echo "$input" | python3 "$LIB_DIR/format_diagram.py")
assert_output "CJK inside box preserved" "$input" "$actual"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
