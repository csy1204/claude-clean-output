---
name: format-output
description: "Use when user asks to format, clean, fix, or copy tables and diagrams from Claude Code output. Also triggered by /format command."
---

# Clean Output Formatting

Claude Code 출력의 마크다운 테이블과 ASCII 다이어그램을 깨끗하게 정규화합니다.

## 핵심 도구

포맷팅 스크립트 위치: `${CLAUDE_PLUGIN_ROOT}/lib/`

### 전체 추출 + 포맷팅
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/extract.py" "$TRANSCRIPT_PATH"
```
마지막 assistant 응답에서 테이블/다이어그램을 추출하고 정규화합니다.

### 테이블만 포맷팅
```bash
echo "| col1 | col2 |
|---|---|
| data | data |" | python3 "${CLAUDE_PLUGIN_ROOT}/lib/format_table.py"
```

### 다이어그램만 포맷팅
```bash
echo "diagram text" | python3 "${CLAUDE_PLUGIN_ROOT}/lib/format_diagram.py"
```
`--normalize-chars` 플래그로 ASCII `+-|`를 유니코드 `┌─│`로 변환할 수 있습니다.

## 포맷팅 규칙

### 테이블
- 각 컬럼을 display width 기반으로 균일하게 패딩
- CJK 문자(한/중/일)는 display width 2로 계산
- 헤더 구분선을 컬럼 폭에 맞게 확장
- 파이프 위치 일관 정렬

### 다이어그램
- 앞쪽 공백 정규화 (최소 공백 기준 재정렬)
- trailing whitespace 제거
- `--normalize-chars`로 ASCII → 유니코드 박스 문자 변환

## 클립보드 복사

포맷팅된 결과를 클립보드에 복사:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/extract.py" "$TRANSCRIPT_PATH" | pbcopy  # macOS
python3 "${CLAUDE_PLUGIN_ROOT}/lib/extract.py" "$TRANSCRIPT_PATH" | xclip -selection clipboard  # Linux
```

## 파일 저장

결과는 항상 `~/.claude/clean-output/latest.md`에도 저장됩니다.
