# HTML 산출물 레이아웃 가이드 (html-layout)

자기완결 HTML 산출물(diff 해설, 리포트 등)에 쓰는 레이아웃 시스템의 핸드오프 문서.
`writing-style.md`가 문장을 정한다면, 이 문서는 HTML의 시각 골격을 정한다.
아래 CSS·컴포넌트·JS를 그대로 복사해 시작하고, 필요한 것만 덜어 쓴다.

## 설계 원칙

- **단일 파일 자기완결**: CSS·JS 인라인, 외부 의존 없음. 한 장짜리 롱 페이지 + 목차
  (최상위 구조에 탭 금지).
- **컴포넌트 소수 정예**: 아래 카탈로그의 7종만으로 대부분의 문서를 조립한다. 문서마다
  새 시각 언어를 만들지 않는다 — 같은 도형 가족을 재사용해야 독자의 학습 비용이 한 번으로
  끝난다.
- **다이어그램은 HTML로**: ASCII 아트 금지. `.flow` + `.node` 조합이 기본 도형 가족이고,
  노드 안에 반드시 **예시 데이터**를 싣는다(`<small>`).
- **코드 블록은 `<pre>`**: 커스텀 div를 쓰면 `white-space: pre-wrap` 필수. 저장 전에
  각 코드 블록의 줄바꿈이 살아 있는지 소스에서 확인한다.

## 디자인 토큰

색은 전부 `:root` CSS 변수로만 참조한다. 의미 축이 넷:

| 축 | 변수 | 용도 |
|---|---|---|
| 잉크/배경 | `--ink` `--sub` `--bg` `--panel` `--line` | 본문·보조 텍스트·패널·경계선 |
| 강조 | `--accent` `--accent-soft` | 링크, 핵심 callout, DB류 노드 |
| 상태 | `--ok(-soft)` `--warn(-soft)` `--bad(-soft)` | 성공/경고/실패 — pill·callout·퀴즈 판정 공용 |
| 코드 | `--code-bg` `--code-ink` | 다크 코드 블록 |

상태 3색은 pill, callout, 퀴즈 피드백이 **같은 변수를 공유**한다 — 문서 전체에서
"초록=성공, 빨강=실패"가 한 번만 학습되게 하는 장치다.

## 컴포넌트 카탈로그

### 1. 목차 `.toc`
`<nav class="toc">` + `<ol>` + 앵커 링크. 문서 맨 위 1회.

### 2. 접이식 배경 `.skippable`
`<details class="skippable" open>` — 독자 수준을 모를 때 깊은 배경을 넣되 접을 수 있게.
`<summary>`에 "아는 분은 접어도 됩니다" 류 안내를 쓴다.

### 3. Callout `.callout`
핵심 개념·정의는 기본(파랑), 엣지 케이스·주의는 `.callout.warn`(주황).
첫 `<b>`가 제목 줄이 된다. 문서당 소수만 — 전부 강조하면 아무것도 강조되지 않는다.

```html
<div class="callout"><b>핵심 용어 — job</b> 설명…</div>
<div class="callout warn"><b>기록 제외는 딱 하나</b> 설명…</div>
```

### 4. 흐름 다이어그램 `.diagram` > `.flow` > `.node`
시스템/데이터 흐름의 기본 도형 가족. 변형은 클래스로:

| 클래스 | 의미 |
|---|---|
| `.node` | 일반 컴포넌트 (흰 배경, 실선) |
| `.node.db` | 저장소/DB (파랑 배경, 아래 모서리 둥글게) |
| `.node.ext` | 외부 행위자 (점선) |
| `.node.dead` | 제거된/폐기된 것 (빨강, 취소선) — before/after 비교에 사용 |
| `.arrow` | 노드 사이 `→` (모바일에서 자동 90° 회전) |

```html
<div class="diagram">
  <div class="title">변경 후 요청 흐름 — 구체 예시 한 줄</div>
  <div class="flow">
    <div class="node ext">클라이언트<small>POST /v1/solve</small></div>
    <div class="arrow">→</div>
    <div class="node db">jobs INSERT<small>status=RUNNING</small></div>
  </div>
</div>
```

### 5. 데이터 로우 카드 `.rowcard`
DB 로우·레코드의 시점별 상태를 보여줄 때. `<span class="lbl">`이 시점 라벨
(t₀/t₁/실패 예), 값 안의 상태는 `.pill`로:

```html
<div class="rowcard">
  <span class="lbl">t₀ 수신</span> id=a3f2… · <span class="pill run">RUNNING</span> · result=∅
</div>
```

`.pill.run`(주황) / `.pill.done`(초록) / `.pill.fail`(빨강).

### 6. 표
파일↔역할, 옵션 비교 같은 짧은 사실 나열에만. 설명·해석은 표 밖 산문으로
(`writing-style.md` §6).

### 7. 인터랙티브 퀴즈 `.quiz`
`data-answer`(0-기반 정답 인덱스)를 가진 컨테이너 + 선택지 `<button>` + 빈 `.fb`.
아래 공용 JS가 클릭 시 정오 판정·해설을 표시한다. 해설 텍스트는 JS의 `notes` 맵에
문항 라벨(Q1…)로 넣는다. 함정 금지, 본문을 이해해야 풀리는 중간 난이도.

## 반응형

- 본문 `max-width: 860px`, 모바일(≤640px)에서 `.flow`가 세로로 전환되고 화살표가
  90° 회전한다 — 다이어그램이 폰에서도 깨지지 않는 핵심.
- 넓은 내용(표·pre·diagram)은 각자 `overflow-x: auto`.

## 기본 CSS (복사용 원본)

```css
:root {
  --ink: #1a1f2b; --sub: #5a6272; --bg: #ffffff; --panel: #f6f7f9;
  --line: #e3e6ec; --accent: #2455c3; --accent-soft: #e8effc;
  --ok: #1d7a4f; --ok-soft: #e4f4ec; --warn: #a15c00; --warn-soft: #fdf1de;
  --bad: #b0303c; --bad-soft: #fbe9ea; --code-bg: #0f1420; --code-ink: #dce3f2;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: "Apple SD Gothic Neo","Pretendard","Noto Sans KR",-apple-system,sans-serif;
       color: var(--ink); background: var(--bg); line-height: 1.7; }
main { max-width: 860px; margin: 0 auto; padding: 24px 20px 96px; }
h1 { font-size: 1.7rem; line-height: 1.35; margin: 24px 0 4px; }
h2 { font-size: 1.32rem; margin: 56px 0 12px; padding-top: 16px; border-top: 2px solid var(--ink); }
h3 { font-size: 1.08rem; margin: 32px 0 8px; color: var(--accent); }
p { margin: 12px 0; }
.meta { color: var(--sub); font-size: .92rem; margin-bottom: 24px; }
.toc { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 16px 22px; }
.toc ol { margin: 8px 0 4px; padding-left: 20px; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
pre { background: var(--code-bg); color: var(--code-ink); padding: 14px 16px; border-radius: 8px;
      overflow-x: auto; font-size: .84rem; line-height: 1.55; white-space: pre; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; }
p code, li code, td code { background: var(--panel); border: 1px solid var(--line);
      border-radius: 4px; padding: 1px 5px; font-size: .86em; color: #23304d; }
.callout { border-left: 4px solid var(--accent); background: var(--accent-soft);
           border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 18px 0; }
.callout.warn { border-color: var(--warn); background: var(--warn-soft); }
.callout b:first-child { display: block; margin-bottom: 2px; }
table { border-collapse: collapse; width: 100%; margin: 14px 0; font-size: .9rem; }
th, td { border: 1px solid var(--line); padding: 7px 10px; text-align: left; vertical-align: top; }
th { background: var(--panel); }
.skippable { border: 1px dashed var(--line); border-radius: 10px; padding: 4px 18px 8px; margin: 16px 0; }
.skippable summary { cursor: pointer; font-weight: 700; padding: 8px 0; color: var(--sub); }
.diagram { background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
           padding: 18px; margin: 18px 0; overflow-x: auto; }
.diagram .title { font-weight: 700; font-size: .88rem; color: var(--sub); margin-bottom: 12px; }
.flow { display: flex; align-items: stretch; gap: 8px; flex-wrap: wrap; }
.node { background: #fff; border: 1.5px solid var(--ink); border-radius: 8px; padding: 8px 12px;
        font-size: .84rem; min-width: 96px; text-align: center; display: flex; flex-direction: column; justify-content: center; }
.node small { color: var(--sub); font-size: .76rem; display: block; }
.node.db { border-radius: 8px 8px 14px 14px; border-color: var(--accent); background: var(--accent-soft); }
.node.ext { border-style: dashed; }
.node.dead { border-color: var(--bad); background: var(--bad-soft); text-decoration: line-through; color: var(--sub); }
.arrow { align-self: center; color: var(--sub); font-size: 1.1rem; padding: 0 2px; }
.rowcard { background: #fff; border: 1.5px solid var(--accent); border-radius: 8px; padding: 10px 14px;
           margin: 10px 0; font-size: .84rem; font-family: "SF Mono", Menlo, monospace; }
.rowcard .lbl { display: inline-block; background: var(--accent-soft); color: var(--accent);
                border-radius: 4px; padding: 0 6px; font-weight: 700; margin-right: 6px; font-family: inherit; }
.pill { display: inline-block; border-radius: 999px; padding: 1px 10px; font-weight: 700; font-size: .8rem; }
.pill.run { background: var(--warn-soft); color: var(--warn); }
.pill.done { background: var(--ok-soft); color: var(--ok); }
.pill.fail { background: var(--bad-soft); color: var(--bad); }
.quiz { border: 1px solid var(--line); border-radius: 10px; padding: 16px 20px; margin: 20px 0; }
.quiz .q { font-weight: 700; margin-bottom: 10px; }
.quiz button { display: block; width: 100%; text-align: left; margin: 6px 0; padding: 9px 14px;
               border: 1px solid var(--line); border-radius: 8px; background: #fff; cursor: pointer;
               font-size: .92rem; font-family: inherit; line-height: 1.5; }
.quiz button:hover { border-color: var(--accent); }
.quiz button.correct { border-color: var(--ok); background: var(--ok-soft); }
.quiz button.wrong { border-color: var(--bad); background: var(--bad-soft); }
.quiz .fb { display: none; margin-top: 10px; padding: 10px 14px; border-radius: 8px; font-size: .9rem; }
.quiz .fb.show-ok { display: block; background: var(--ok-soft); color: var(--ok); }
.quiz .fb.show-bad { display: block; background: var(--bad-soft); color: var(--bad); }
@media (max-width: 640px) {
  .flow { flex-direction: column; }
  .arrow { transform: rotate(90deg); align-self: flex-start; margin-left: 40px; }
  h1 { font-size: 1.4rem; }
}
```

## 퀴즈 공용 JS (복사용 원본)

```html
<div class="quiz" data-answer="2">
  <div class="q">Q1. 질문…</div>
  <button>선택지 A</button>
  <button>선택지 B</button>
  <button>선택지 C (정답, 0-기반 인덱스 2)</button>
  <div class="fb"></div>
</div>

<script>
document.querySelectorAll('.quiz').forEach(function (quiz) {
  var answer = parseInt(quiz.dataset.answer, 10);
  var buttons = quiz.querySelectorAll('button');
  var fb = quiz.querySelector('.fb');
  var notes = {
    'Q1': '정답 해설 — 왜 이게 맞는지 한두 문장.',
    'Q2': '…'
  };
  var qLabel = quiz.querySelector('.q').textContent.trim().slice(0, 3).replace('.', '');
  buttons.forEach(function (btn, idx) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('correct', 'wrong'); b.disabled = true; });
      if (idx === answer) {
        btn.classList.add('correct');
        fb.className = 'fb show-ok';
        fb.textContent = '✓ 정답. ' + (notes[qLabel] || '');
      } else {
        btn.classList.add('wrong');
        buttons[answer].classList.add('correct');
        fb.className = 'fb show-bad';
        fb.textContent = '✗ 오답. ' + (notes[qLabel] || '');
      }
    });
  });
});
</script>
```

## 문서 골격 (섹션 순서)

`<h1>` 제목 + `.meta`(규모·수치 한 줄) → `.toc` → 배경(깊은 배경은 `.skippable`)
→ 직관(다이어그램·rowcard 중심) → 코드 워크스루(겹 단위 그룹핑) → 퀴즈 5문항.
섹션 구성 자체는 각 스킬 템플릿(예: `templates/diff_explanation.md`)이 우선하고,
이 문서는 그 골격을 시각적으로 어떻게 입히는지만 정한다.
