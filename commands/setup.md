---
description: "claude-clean-output 플러그인 초기 설정"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# /setup Command

claude-clean-output 플러그인을 설정합니다. 프롬프트 규칙 설치, 자동 포맷팅 설정, 동작 검증을 수행합니다.

## Step 0: Verify Python3

```bash
python3 --version 2>&1
```

Python 3가 없으면 설치를 안내하고 중단합니다.

## Step 1: Detect Platform

환경 컨텍스트의 `Platform:` 값을 사용합니다 (darwin/linux/win32).

## Step 2: Verify Plugin Installation

```bash
ls "${CLAUDE_PLUGIN_ROOT}/lib/format_table.py" 2>/dev/null && echo "OK" || echo "MISSING"
```

MISSING이면 플러그인이 제대로 설치되지 않은 것입니다. 사용자에게 안내합니다.

## Step 3: Test Formatter

간단한 테이블을 포맷팅하여 동작을 확인합니다:

```bash
echo "| a | bb |
|---|---|
| ccc | d |" | python3 "${CLAUDE_PLUGIN_ROOT}/lib/format_table.py"
```

출력이 정렬된 테이블이면 정상입니다. 오류가 나면 디버깅합니다.

## Step 4: Configure Options

AskUserQuestion을 사용하여 설정을 수집합니다:

### Q1: Prompt Rules
- header: "Prompt Rules"
- question: "Claude가 처음부터 정렬된 테이블을 출력하도록 프롬프트 규칙을 설치할까요?"
- multiSelect: false
- options:
  - "Standard (추천)" — CJK 폭 계산 규칙 + 정렬 예시 포함
  - "Minimal" — 간단한 정렬 안내만
  - "Strict" — Standard + 패딩/구분선 엄격 규칙
  - "설치 안 함" — 프롬프트 규칙 없이 후처리만 사용

### Q2: Auto-format Options
- header: "자동 포맷팅"
- question: "어떤 자동 기능을 활성화할까요?"
- multiSelect: true
- options:
  - "자동 포맷팅 (추천)" — 매 응답 후 자동으로 테이블/다이어그램 추출
  - "클립보드 복사" — 포맷팅 결과를 자동으로 클립보드에 복사
  - "유니코드 다이어그램" — ASCII 박스 문자를 유니코드로 자동 변환

## Step 5: Install Prompt Rules

Q1 응답에 따라 `~/.claude/rules/clean-output-tables.md`를 설치합니다.

**"설치 안 함"을 선택한 경우**: 이 단계를 건너뜁니다.

규칙 파일의 소스는 강도별로:
- **Minimal**: `${CLAUDE_PLUGIN_ROOT}/rules/clean-output-tables-minimal.md`
- **Standard**: `${CLAUDE_PLUGIN_ROOT}/rules/clean-output-tables.md`
- **Strict**: `${CLAUDE_PLUGIN_ROOT}/rules/clean-output-tables-strict.md`

설치:
```bash
mkdir -p ~/.claude/rules
cp "${CLAUDE_PLUGIN_ROOT}/rules/clean-output-tables<-variant>.md" ~/.claude/rules/clean-output-tables.md
```

## Step 6: Save Config

Q1, Q2 응답을 기반으로 설정을 저장합니다:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set promptRules=<true/false>
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set promptStrength=<minimal/standard/strict>
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set autoFormat=<true/false>
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set clipboard=<true/false>
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set unicodeDiagrams=<true/false>
```

Q2에서 선택되지 않은 항목은 false로 설정합니다.

## Step 7: Verify

"설정이 완료되었습니다!" 라고 안내한 후, 테스트 테이블로 검증:

```bash
echo "| 이름 | 설명 | 상태 |
|---|---|---|
| 홍길동 | 테스트 항목입니다 | 활성 |
| test | short | 비활성 |" | python3 "${CLAUDE_PLUGIN_ROOT}/lib/format_table.py"
```

결과가 정렬되면 성공. "/configure로 나중에 변경할 수 있습니다."라고 안내합니다.
