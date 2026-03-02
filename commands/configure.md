---
description: "claude-clean-output 포맷팅 설정 변경"
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# /configure Command

claude-clean-output 플러그인의 설정을 변경합니다.

**FIRST**: 현재 설정을 읽습니다:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --dump
```

설정 파일이 없으면 (에러 또는 모두 기본값) Flow A, 파일이 있으면 Flow B를 사용합니다.

---

## Flow A: New User (설정 없음)

아직 설정이 없습니다. `/setup`을 먼저 실행하도록 안내합니다:

"아직 설정이 없습니다. `/setup`을 먼저 실행해주세요."

---

## Flow B: Returning User (설정 있음)

현재 설정을 읽어 표시한 후 변경할 항목을 묻습니다.

### Q1: Toggle Features
- header: "기능 설정"
- question: "변경할 기능을 선택하세요 (선택한 항목의 상태가 반전됩니다)"
- multiSelect: true
- options (현재 상태를 라벨에 표시):
  - "자동 포맷팅 [현재: ON/OFF]" — 매 응답 후 자동 테이블/다이어그램 추출
  - "클립보드 복사 [현재: ON/OFF]" — 포맷팅 결과 자동 클립보드 복사
  - "유니코드 다이어그램 [현재: ON/OFF]" — ASCII→유니코드 박스 문자 변환

선택한 항목의 값을 반전합니다 (ON→OFF, OFF→ON).

### Q2: Prompt Rules
- header: "프롬프트 규칙"
- question: "프롬프트 규칙을 변경할까요? (현재: <현재 강도 또는 '없음'>)"
- multiSelect: false
- options:
  - "유지" — 현재 설정 그대로
  - "Minimal" — 간단한 정렬 안내만
  - "Standard" — CJK 폭 계산 + 예시
  - "Strict" — 엄격한 정렬 규칙
  - "제거" — 프롬프트 규칙 삭제

### Processing

1. Q1 선택에 따라 config 값을 토글합니다
2. Q2 선택에 따라:
   - "유지": 변경 없음
   - "제거": `~/.claude/rules/clean-output-tables.md` 삭제, `promptRules=false` 설정
   - 나머지: 해당 강도의 규칙 파일을 `~/.claude/rules/clean-output-tables.md`에 복사, `promptStrength` 업데이트, `promptRules=true` 설정

### Save & Confirm

변경 사항 요약을 보여주고 저장합니다:

```
변경 사항:
  - 자동 포맷팅: ON → OFF
  - 프롬프트 규칙: standard → strict
```

저장:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/config.py" --set <key>=<value>
```

"설정이 저장되었습니다! 변경 사항이 즉시 적용됩니다."
