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

# Test 1: Basic misaligned table
input="| Name | Description | Status |
|---|---|---|
| foo | a very long description | active |
| bar | short | inactive |"

expected="| Name | Description             | Status   |
|------|-------------------------|----------|
| foo  | a very long description | active   |
| bar  | short                   | inactive |"

actual=$(echo "$input" | python3 "$LIB_DIR/format_table.py")
assert_output "basic misaligned table" "$expected" "$actual"

# Test 2: CJK content
input="| 이름 | 설명 | 상태 |
|---|---|---|
| 홍길동 | 테스트 항목 | 활성 |
| foo | bar | 비활성 |"

expected="| 이름   | 설명        | 상태   |
|--------|-------------|--------|
| 홍길동 | 테스트 항목 | 활성   |
| foo    | bar         | 비활성 |"

actual=$(echo "$input" | python3 "$LIB_DIR/format_table.py")
assert_output "CJK content table" "$expected" "$actual"

# Test 3: Already aligned table (should pass through unchanged)
input="| A   | B   |
|-----|-----|
| foo | bar |"

actual=$(echo "$input" | python3 "$LIB_DIR/format_table.py")
assert_output "already aligned table" "$input" "$actual"

# Test 4: Single column
input="| Item |
|---|
| hello |
| world |"

expected="| Item  |
|-------|
| hello |
| world |"

actual=$(echo "$input" | python3 "$LIB_DIR/format_table.py")
assert_output "single column table" "$expected" "$actual"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
