# shine-docs

문서와 코드 변경을 **가독성 높은 산출물(HTML/Markdown)** 로 만드는 **코딩 에이전트용 스킬 세트**입니다. Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot CLI, Kimi Code에서 플러그인/확장으로 설치해 쓸 수 있습니다.

## 스킬 목록

### document-refactor — 문서 재구조화

임의의 문서를 **유형에 맞는 논리 구조로 재배치**합니다. 기획서·실험 보고서·회의록·PR 설명·붙여넣은 텍스트·URL 등 무엇이든 넣으면, 원문에 충실하게 정돈해 줍니다.

핵심 원칙은 **"자명한 사실만"** 입니다. 원문에서 확인 가능한 내용과 3단논법 수준의 당연한 도출만 다루고, **원문 밖 유추는 하지 않습니다**. 이 규율을 사실성 리뷰어(하드 게이트)가 강제합니다.

- **유형 분류**: `templates/`의 문서 유형(기획서·실험보고서·회의록·PR·제안서·기본) 중 맞는 구조를 골라 적용
- **재구조화**: 원문 내용을 템플릿 섹션에 재배치. 근거 없는 필수 섹션은 공란으로 남겨 "문서가 안 다루는 논점"을 드러냄
- **리뷰 루프**: 작성자와 분리된 두 리뷰어(사실성·가독성)가 최대 3라운드 검토
- **산출**: 자기완결 HTML(인라인 CSS/JS, 인터랙티브 Quiz) 또는 Markdown(표·mermaid, 접이식 Q&A). 걸러진 유추·미해결 이슈·공란 섹션은 부록(Audit Trail)에 기록

### explain-diff-html — 코드 변경 해설

diff·브랜치·PR 등 **코드 변경을 풍부한 인터랙티브 HTML 해설**로 만듭니다.

- **구성**: Background(주변 코드 탐색 기반 배경 설명) → Intuition(토이 데이터·다이어그램으로 핵심 직관) → Code(변경 워크스루) → Quiz(이해도 확인용 5문항 인터랙티브 객관식)
- **산출**: 목차·다이어그램·콜아웃을 갖춘 자기완결 HTML 한 장 (모바일 대응)
- **레퍼런스**: Geoffrey Litt의 ["Explain Diff" 프롬프트](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)를 기반으로 합니다(거의 그대로 따름).

## 설치

에이전트(하네스)별로 설치 방법이 다릅니다. 여러 에이전트를 쓰면 각각 설치하세요.

### Claude Code

```
/plugin marketplace add Leo-Moooon/shine-docs
/plugin install shine-docs@shine-docs
```

또는 CLI:

```
claude plugin marketplace add Leo-Moooon/shine-docs
claude plugin install shine-docs@shine-docs
```

### Codex CLI

```
/plugins
```

플러그인 검색 화면에서 이 레포 URL(`https://github.com/Leo-Moooon/shine-docs`)로 설치하거나, 커스텀 마켓플레이스로 등록해 설치합니다.

### Cursor

Cursor Agent 채팅에서:

```
/add-plugin https://github.com/Leo-Moooon/shine-docs
```

### Gemini CLI

```
gemini extensions install https://github.com/Leo-Moooon/shine-docs
```

업데이트:

```
gemini extensions update shine-docs
```

### GitHub Copilot CLI

```
copilot plugin marketplace add Leo-Moooon/shine-docs
copilot plugin install shine-docs@shine-docs
```

### Kimi Code

```
/plugins install https://github.com/Leo-Moooon/shine-docs
```

> OpenCode·Pi 등 커스텀 로더 코드가 필요한 하네스는 아직 지원하지 않습니다.

## 사용

설치 후 해당 맥락이면 에이전트가 자동으로 불러오거나, 직접 호출합니다. Claude Code 기준:

```
/shine-docs:document-refactor    # 문서 재구조화 — 대상 문서, 출력 모드(HTML/MD), 저장 위치를 물어봄
/shine-docs:explain-diff-html    # 코드 변경 해설 — diff/브랜치/PR을 지정
```

## 구조

스킬 본체(`skills/`)는 하나이고, 에이전트별 매니페스트가 이를 공유합니다.

```
shine-docs/
├── skills/                       # 공용 스킬 본체 (모든 에이전트가 공유)
│   ├── document-refactor/
│   │   ├── SKILL.md
│   │   └── templates/            # 문서 유형별 섹션 골격 6종
│   └── explain-diff-html/
│       └── SKILL.md
├── .claude-plugin/               # Claude Code (marketplace.json + plugin.json)
├── .codex-plugin/plugin.json     # Codex
├── .cursor-plugin/plugin.json    # Cursor
├── .kimi-plugin/plugin.json      # Kimi Code
├── .agents/plugins/marketplace.json  # GitHub Copilot CLI
├── gemini-extension.json         # Gemini CLI
└── GEMINI.md                     # Gemini 컨텍스트 파일 (스킬 라우팅)
```

## 요구사항

- 플러그인·스킬을 지원하는 코딩 에이전트 (Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot CLI, Kimi Code)
- 스킬 내용은 document-refactor는 한국어, explain-diff-html은 영어입니다.

## 라이선스

MIT License. [LICENSE](LICENSE) 참고.
