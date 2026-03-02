---
description: "마지막 응답의 테이블/다이어그램을 깨끗하게 포맷팅합니다"
allowed-tools: Bash, Read
---

# /format Command

마지막 Claude 응답에서 마크다운 테이블과 ASCII 다이어그램을 찾아 정규화합니다.

## 실행 절차

1. `$TRANSCRIPT_PATH`를 사용하여 현재 세션의 transcript를 확인합니다
2. 다음 명령을 실행합니다:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/lib/extract.py" "$TRANSCRIPT_PATH"
```

3. 결과가 있으면:
   - 정규화된 테이블/다이어그램을 사용자에게 보여줍니다
   - 클립보드에 복사합니다:
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/lib/extract.py" "$TRANSCRIPT_PATH" | pbcopy
     ```
   - `~/.claude/clean-output/latest.md`에도 저장합니다

4. 결과가 없으면 "포맷팅할 테이블이나 다이어그램이 없습니다"라고 알려줍니다
