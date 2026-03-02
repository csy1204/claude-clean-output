#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LIB_DIR="$SCRIPT_DIR/../lib"
PASS=0
FAIL=0

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $label — expected '$expected', got '$actual'"
    FAIL=$((FAIL + 1))
  fi
}

# Test 1: Pure ASCII
result=$(echo -n "hello" | python3 "$LIB_DIR/display_width.py")
assert_eq "pure ASCII 'hello'" "5" "$result"

# Test 2: Korean (each char = display width 2)
result=$(echo -n "한글" | python3 "$LIB_DIR/display_width.py")
assert_eq "Korean '한글'" "4" "$result"

# Test 3: Mixed ASCII + Korean
result=$(echo -n "ab한글cd" | python3 "$LIB_DIR/display_width.py")
assert_eq "mixed 'ab한글cd'" "8" "$result"

# Test 4: Japanese katakana (fullwidth)
result=$(echo -n "アイウ" | python3 "$LIB_DIR/display_width.py")
assert_eq "Japanese katakana 'アイウ'" "6" "$result"

# Test 5: Chinese characters
result=$(echo -n "中文" | python3 "$LIB_DIR/display_width.py")
assert_eq "Chinese '中文'" "4" "$result"

# Test 6: Empty string
result=$(echo -n "" | python3 "$LIB_DIR/display_width.py")
assert_eq "empty string" "0" "$result"

# Test 7: Pipe and spaces (table chars)
result=$(echo -n "| 이름 | age |" | python3 "$LIB_DIR/display_width.py")
assert_eq "table row '| 이름 | age |'" "14" "$result"

# Test 8: Multi-line mode (per-line widths)
result=$(printf "abc\n한글" | python3 "$LIB_DIR/display_width.py" --per-line)
assert_eq "multi-line per-line" "3
4" "$result"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
