# claude-clean-output

Claude Code 출력의 마크다운 테이블과 ASCII 다이어그램을 자동으로 정규화하는 플러그인.

## Features

- **프롬프트 규칙 주입**: `~/.claude/rules/`에 테이블 포맷팅 규칙을 설치하여 Claude가 처음부터 정렬된 테이블을 출력하도록 유도
- **자동 후처리**: Claude 응답 완료 시 Stop hook이 테이블/다이어그램을 감지하고 정규화
- **수동 제어**: `/format` 커맨드로 원할 때 포맷팅
- **CJK 지원**: 한국어/중국어/일본어 문자의 display width(2)를 정확히 계산
- **클립보드 복사**: 포맷팅된 결과를 자동으로 클립보드에 복사
- **설정 시스템**: `/setup`으로 초기 설정, `/configure`로 변경
- **크로스 플랫폼**: macOS, Linux 지원 (Windows는 Git Bash 필요)

## Installation

```bash
claude plugin add -- https://github.com/csy1204/claude-clean-output
```

설치 후 초기 설정:
```
/setup
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

### 설정 변경
```
/configure
```
자동 포맷팅, 클립보드 복사, 유니코드 변환, 프롬프트 규칙 강도를 변경할 수 있습니다.

## Prompt Rules

`/setup` 시 `~/.claude/rules/clean-output-tables.md`에 프롬프트 규칙이 설치됩니다. 3단계 강도:

| 강도 | 설명 |
|------|------|
| Minimal | 간단한 정렬 안내 |
| Standard | CJK 폭 계산 규칙 + 정렬 예시 |
| Strict | Standard + 엄격한 패딩/구분선 규칙 |

## Config

설정 파일: `~/.claude/plugins/claude-clean-output/config.json`

| 키 | 기본값 | 설명 |
|----|--------|------|
| `autoFormat` | `true` | Stop hook 자동 실행 |
| `clipboard` | `true` | 클립보드 자동 복사 |
| `savePath` | `~/.claude/clean-output/latest.md` | 저장 경로 |
| `unicodeDiagrams` | `false` | ASCII→유니코드 박스 문자 변환 |
| `promptRules` | `true` | 프롬프트 규칙 설치 여부 |
| `promptStrength` | `standard` | 규칙 강도 |

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
