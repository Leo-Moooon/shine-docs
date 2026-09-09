# shine-docs

문서와 코드 변경을 **가독성 높은 산출물(HTML/Markdown)** 로 만드는 **코딩 에이전트용 스킬 세트**입니다. Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot CLI, Kimi Code에서 플러그인/확장으로 설치해 쓸 수 있습니다.

## 스킬 목록

### document-refactor — 문서 재구조화

임의의 문서를 **유형에 맞는 논리 구조로 재배치**합니다. 기획서·실험 보고서·회의록·PR 설명·붙여넣은 텍스트·URL 등 무엇이든 넣으면, 원문에 충실하게 정돈해 줍니다.

핵심 원칙은 **"자명한 사실만"** 입니다. 원문에서 확인 가능한 내용과 3단논법 수준의 당연한 도출만 다루고, **원문 밖 유추는 하지 않습니다**. 이 규율을 사실성 리뷰어(하드 게이트)가 강제합니다.

- **유형 분류**: 공용 템플릿 풀 `skills/templates/`의 문서 유형 중 맞는 구조를 골라 적용
- **재구조화**: 원문 내용을 템플릿 섹션에 재배치. 근거 없는 필수 섹션은 공란으로 남겨 "문서가 안 다루는 논점"을 드러냄
- **리뷰 루프**: 작성자와 분리된 두 리뷰어(사실성·가독성)가 최대 3라운드 검토
- **산출**: 자기완결 HTML(인라인 CSS/JS, 인터랙티브 Quiz) 또는 Markdown(표·mermaid, 접이식 Q&A). 걸러진 유추·미해결 이슈·공란 섹션은 부록(Audit Trail)에 기록

### write-document — 문서 신규 작성

원문 없이 **지금부터 써야 하는 문서**를 유형별 섹션 골격에 맞춰 새로 작성합니다. document-refactor와 같은 **"자명한 사실만"** 규율을 따르되, 입력은 원문이 아니라 대화 맥락·코드베이스에서 확인한 사실·요청자의 진술입니다.

- **지원 유형 6종**: issue/backlog 티켓 · 버그 티켓 · PR 본문 · 대화용 간략 제안(슬랙 등) · 코드 변경 해설(diff_explanation) · 일반 문서(폴백)
- **인터랙티브 플로우**: 유형 → 강조 사항 → Quiz(기본 off, diff_explanation만 기본 on) → 출력 방식(파일 export / 대화 출력) 순으로 질문
- **공란 규칙**: 필수 섹션인데 근거가 없으면 비워 두고 사유를 한 줄로 남김 — 공란 자체가 문서의 결함을 드러내는 신호
- **리뷰 opt-in**: 초안 작성 후 리뷰 루프 실행 여부를 확인(proposal_chat은 단일 패스, 나머지는 최대 3라운드) — 판정은 review-document에 위임

### review-document — 문서 품질 리뷰

문서를 여덟 개 축으로 판정합니다. **write-document·document-refactor의 리뷰 단계가 호출하는 공용 엔진**이자, 이미 있는 문서(남이 쓴 것 포함)를 리뷰하는 **단독 진입점**입니다.

- **검사 축 8종**: 사실성(하드 게이트) · 참조 유효성 · 공란 규율 · 가독성/구조 · 내부 일관성 · 독자 적합성 · 표기 · 실행가능성(티켓·PR 한정)
- **리뷰어 2분할**: 문서 밖 자료를 들고 대조해야 하는 축은 **검증 리뷰어**(코드베이스·웹검색 권한 보유), 문서 텍스트만으로 판정되는 축은 **가독성 리뷰어**. 가독성 리뷰어에게는 근거를 주지 않습니다 — 배경 지식을 쥐여주면 "독자 적합성" 판정이 무력화되기 때문
- **판정 3등급**: 하드 게이트 반려(사실성) / 수정 요구 / 질문. 웹검색으로 찾은 사실은 반려 근거가 아니라 질문으로만 올립니다 — 판정 기준은 "근거 대비 충실도"이지 세상의 진실이 아니므로
- **수정 권한**: 단독 호출이면 시작할 때 물어봅니다(지적만 / 승인받고 수정 / 알아서 수정 후 보고). 공용 엔진으로 불릴 때는 제안까지만 하고 반영은 호출부가 담당

### write-wiki — 티켓 아카이브 작성

티켓/브랜치/워크트리 단위 작업이 끝날 때, **"어떤 실험·작업을 했고 무엇을 왜 결정했나"** 를 개인 옵시디언 vault에 아카이브합니다.  — 단순 파일 보관이 아니라 **실험·작업 기록과 결정 근거를 문서로 남기는 것**이 우선입니다.

- **구조 규칙**: `<티켓번호> <간단한 설명>/` 폴더에 `<티켓번호> README.md`(진입점) + 실험 단위로 분할한 `<티켓번호> REPORT N (<주제>).md`. 파생/하위 티켓은 부모 폴더 하위에 중첩
- **첨부 선별**: 스크립트·코드는 첨부하지 않고 방법을 문서로 서술. 자기완결 증빙(HTML·스크린샷)만 티켓번호 접두사로 rename해 보관. 민감 데이터 제외
- **규율 계승**: write-document와 같은 "자명한 사실만" 규율 — 수치는 REPORT/결과 파일에서 그대로, 근거 없는 항목은 공란 + 사유
- **개인 설정 분리**: vault 루트 경로·티켓번호 컨벤션은 스킬에 하드코딩되어 있지 않습니다 — 사용자의 전역 설정(CLAUDE.md 등 하네스 메모리)에서 읽고, 없으면 작성 전에 물어봅니다

### explain-diff-html — 코드 변경 해설 (하위호환)

diff·브랜치·PR 등 **코드 변경을 풍부한 인터랙티브 HTML 해설**로 만듭니다. **직접 호출 전용**으로 유지되는 스킬이며, 자연어 요청은 write-document의 diff_explanation 유형이 담당합니다.

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

이 저장소를 체크아웃한 폴더 **밖에서** 실행합니다. 저장소 안에서 실행하면
Codex가 `.agents/plugins/marketplace.json`을 로컬 마켓플레이스로 먼저 인식해
동일한 이름의 원격 마켓플레이스를 가릴 수 있습니다.

```
cd /tmp
codex plugin marketplace add Leo-Moooon/shine-docs --ref main
codex plugin add shine-docs@shine-docs
```

업데이트할 때는 마켓플레이스를 갱신한 뒤 새 대화를 시작합니다.

```
codex plugin marketplace upgrade shine-docs
```

데스크톱 앱이나 Codex CLI의 `/plugins`에서도, 먼저 GitHub 마켓플레이스
`Leo-Moooon/shine-docs`를 추가한 뒤 `Shine Docs` 마켓플레이스에서 설치합니다.

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
/shine-docs:write-document       # 문서 신규 작성 — 유형(티켓/PR/제안/해설/일반), 강조 사항, 출력 방식을 물어봄
/shine-docs:review-document      # 문서 품질 리뷰 — 대조 근거, 수정 권한, 문서 유형을 물어봄
/shine-docs:write-wiki           # 티켓 아카이브 — 마감된 티켓 작업의 실험·결정 기록을 옵시디언 vault에 작성
/shine-docs:explain-diff-html    # 코드 변경 해설 — diff/브랜치/PR을 지정 (하위호환 직접 호출용)
```

## 구조

스킬 본체(`skills/`)는 하나이고, 에이전트별 매니페스트가 이를 공유합니다.

```
shine-docs/
├── skills/                       # 공용 스킬 본체 (모든 에이전트가 공유)
│   ├── templates/                # 공용 템플릿 풀 — 문서 유형별 섹션 골격 12종
│   ├── style/                    # 공용 스타일 가이드 (문체 writing-style.md, 리뷰 체크리스트 2종, HTML 레이아웃 html-layout.md)
│   ├── document-refactor/
│   │   └── SKILL.md
│   ├── write-document/
│   │   └── SKILL.md
│   ├── review-document/
│   │   └── SKILL.md
│   ├── write-wiki/
│   │   └── SKILL.md
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
- 스킬 내용은 document-refactor·write-document·review-document·write-wiki는 한국어, explain-diff-html은 영어입니다.

## 라이선스

MIT License. [LICENSE](LICENSE) 참고.
