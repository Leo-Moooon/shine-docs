---
name: write-document
description: Use when the user wants to WRITE a new document from scratch — an issue/backlog ticket, bug ticket, pull request description, short chat proposal (Slack etc.), code-change/diff explanation, or a general document — based on conversation context, the codebase, and the user's statements. For restructuring an EXISTING document, use document-refactor instead.
---

# Write Document

원문 없이 지금부터 써야 하는 문서를, 유형별 섹션 골격에 맞춰 새로 작성한다.
`document-refactor`가 **이미 있는 원문**을 재배치하는 스킬이라면, 이 스킬은 **대화 맥락·코드
베이스에서 확인한 사실·요청자가 진술한 내용**을 입력으로 새 문서를 만든다.

## 절대 규율 — "자명한 사실만"
- 취급 가능한 내용: 대화 맥락에 있는 것 + 코드베이스·로그 등에서 직접 확인한 것 + 요청자가
  진술한 것 + 그로부터 3단논법 수준으로 당연히 도출되는 것.
- 맥락상 그럴듯하다는 이유로 알려지지 않은 사실을 써 넣는 것은 **절대 금지**.
- **공란 규칙**: 필수 섹션인데 근거가 없으면 섹션을 남기고 비워 둔 채 "무엇이 없어서 비었는지"
  한 줄로 남긴다(예: 버그 티켓의 재현 절차 — 공란 자체가 문서의 결함을 드러내는 신호다).
  선택 섹션인데 근거가 없으면 생략한다.
- 설명을 돕는 toy data/가짜 데이터는 허용하되 반드시 "설명용 예시" 라벨을 붙인다.

## 지원 유형 (공용 템플릿 풀 `../templates/`)
| 유형 | 템플릿 | 용도 |
|---|---|---|
| issue_ticket | `issue_ticket.md` | issue/backlog 티켓 |
| bug_ticket | `bug_ticket.md` | 버그 티켓 |
| pull_request | `pull_request.md` | 지금 열 PR의 본문 |
| proposal_chat | `proposal_chat.md` | 슬랙 등 대화용 간략 제안 |
| diff_explanation | `diff_explanation.md` | 코드 변경 해설 (Quiz 기본 ON) |
| general | `general.md` | 어느 유형에도 맞지 않을 때의 폴백 |

확정된 템플릿 파일 **하나만** 정독한다. `general`은 필요하면 목적에 맞는 섹션을 즉석
구성해도 된다.

## UX 플로우

**인터랙티브 규칙**: 아래 질문은 클릭형 선택지 도구(harness의 AskUserQuestion 등)로 제시하고,
없는 환경이면 텍스트로 폴백한다. 요청자가 처음부터 값을 명시한 항목은 다시 묻지 않는다.

### 1. 유형 선택 (단독 질문)
위 6종 중 하나를 고른다. 이후 질문의 내용이 유형에 따라 달라지므로 먼저 단독으로 묻는다.

### 2. 강조 사항 · Quiz · 출력 방식 (한 번에 질문)
- **강조 사항** — "반드시 강조할 내용이 있나요?"
  - 템플릿에 이미 있는 섹션에 해당 → 그 섹션을 문서 앞쪽으로 올리거나 분량을 늘려 강조.
  - 템플릿에 없는 내용 → 새 섹션을 만들되, 템플릿 밖 섹션임을 독자가 알 수 있게 **어느 위치에
    넣었는지 산출물에 밝힌다**.
- **Quiz** — 기본 OFF, 단 `diff_explanation`은 기본 ON. 기본값과 다르게 할지 묻는다.
  켜면 규격: 실질을 이해해야 풀 수 있는 중간 난이도, 함정 금지, 확인된 사실에 근거한 문항만.
  HTML=클릭 시 정오·피드백을 주는 인터랙티브 객관식, MD=`<details>` 접이식 Q&A.
- **출력 방식** — 두 가지 중 선택:
  - **파일로 export** — 경로를 함께 묻는다(기본값: 현재 작업 디렉토리). 파일명에 날짜 접두사를
    붙이지 않는다. HTML을 고르면 자기완결 HTML 한 파일(CSS·JS 인라인, 반응형)로 렌더링.
  - **직접 작성** — 파일을 만들지 않고 대화에 본문을 그대로 출력한다(복사·붙여넣기용).
    티켓·PR 시스템에 직접 반영(Jira·GitHub 연동)은 이 스킬의 범위가 아니다 — 출력 후 세션에서
    별도로 하면 된다.

### 3. 초안 작성 (작성자 컨텍스트)
작성 전에 공용 스타일 가이드 `../style/writing-style.md`를 정독한다 — 특히 최우선 규칙
"최종 상태만 flat하게"(과정·시행착오를 본문 논리 구조로 쓰지 않는다). 확정된 템플릿의
섹션 순서대로 작성한다. 절대 규율(위)을 지킨다.

**분할 신호**: 초안 중 분할 신호(스타일 가이드 §11 — H4 이상, 독립 주제 2개 이상, 분량
규격 초과)가 뜨면 그대로 완성하지 말고 멈춰서 §11의 유형별 대응(티켓 분리, PR 분할 신호
보고, proposal_chat의 정식 문서 승격 등)을 사용자에게 제안한다. 사용자가 이미 단일
산출물을 명시했으면 묻지 않는다.

### 4. 리뷰 (opt-in — 초안 후 질문)
초안을 보여주고 "리뷰 루프를 돌릴까요?"를 묻는다. 유형별 기본 제안:
- `proposal_chat` → 단일 패스 사실성 점검.
- 나머지 유형 → `document-refactor`와 같은 2리뷰어(사실성 하드 게이트 + 가독성·구조) 최대
  3라운드. 리뷰어는 작성자와 **분리된 컨텍스트**여야 한다(자기검토 금지).
리뷰 기준: 근거(대화 맥락·확인 사실·요청자 진술) 대비 충실도. 근거가 없어 공란인 필수 섹션은
정상 동작이며 감점하지 않는다. 근거 없는 주장·유추가 하나라도 있으면 반려.
가독성 리뷰어는 `../style/review-checklist.md`를 순회하며 `../style/writing-style.md`
위반(특히 과정 서술이 본문에 섞인 것, bullet 한줄 나열, 설명 없는 어려운 용어)을 반려
사유로 본다.

### 5. 산출
- Audit Trail 부록은 붙이지 않는다 — 공란 사유 한 줄이 본문에 남는 것으로 충분하다.
- 리뷰를 돌렸고 3라운드 소진 후에도 미해결 이슈가 남았다면, 그때만 "문서 말미에 미해결 이슈를
  남길까요?"를 묻는다.

## 유형별 특칙
- **proposal_chat** — 헤딩 없이 짧은 단락·bullet만, 전체 15줄 이내 목표. 단 공유할 데이터가
  표 형태면 표 허용.
- **diff_explanation** — 주변 코드를 넓게 탐색해 Background를 쓴다. 다이어그램 지침은 템플릿
  참조(ASCII 금지). 자연어로 "diff/PR 설명해 줘"류 요청은 이 유형이 담당한다(`explain-diff-html`
  스킬은 직접 호출 전용 하위호환).
