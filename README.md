# claude-clean-output

Claude Code 출력의 마크다운 테이블과 ASCII 다이어그램을 자동으로 정규화하는 플러그인.

## Features

- **자동 후처리**: Claude 응답 완료 시 Stop hook이 테이블/다이어그램을 감지하고 정규화
- **수동 제어**: `/format` 커맨드로 원할 때 포맷팅
- **CJK 지원**: 한국어/중국어/일본어 문자의 display width(2)를 정확히 계산
- **클립보드 복사**: 포맷팅된 결과를 자동으로 클립보드에 복사
- **크로스 플랫폼**: macOS, Linux 지원 (Windows는 Git Bash 필요)

## Installation

```bash
claude /install-plugin github:user/claude-clean-output
```

## Usage

### 자동 모드
설치만 하면 매 응답 후 자동으로 동작합니다. 깨진 테이블/다이어그램이 감지되면:
- `~/.claude/clean-output/latest.md`에 정리된 버전 저장
- 클립보드에 자동 복사

### 수동 모드
```
/format
```
마지막 응답의 테이블/다이어그램을 정리해서 보여주고 클립보드에 복사합니다.

## Requirements

- Python 3.6+
- jq (선택, 없으면 Python fallback)

## Development

```bash
# Run all tests
bash tests/run-all.sh
```

## License

MIT
