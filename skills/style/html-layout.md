# HTML 산출물 레이아웃 가이드 (html-layout)

자기완결 HTML 산출물(diff 해설, 리포트 등)에 쓰는 레이아웃 시스템의 핸드오프 문서.
`writing-style.md`가 문장을 정한다면, 이 문서는 HTML의 시각 골격을 정한다.
아래 CSS·컴포넌트·JS를 그대로 복사해 시작하고, 필요한 것만 덜어 쓴다.

## 설계 원칙

- **단일 파일 자기완결**: CSS·JS 인라인, 외부 의존 없음. 한 장짜리 롱 페이지 + 목차
  (최상위 구조에 탭 금지). 여러 장으로 된 문서 묶음은 아래 "문서 묶음" 절을 따른다.
- **컴포넌트 소수 정예**: 아래 카탈로그의 7종만으로 대부분의 문서를 조립한다. 문서마다
  새 시각 언어를 만들지 않는다 — 같은 도형 가족을 재사용해야 독자의 학습 비용이 한 번으로
  끝난다.
- **다이어그램은 HTML로**: ASCII 아트 금지. `.flow` + `.node` 조합이 기본 도형 가족이고,
  노드 안에 반드시 **예시 데이터**를 싣는다(`<small>`).
- **코드 블록은 `<pre>`**: 커스텀 div를 쓰면 `white-space: pre-wrap` 필수. 저장 전에
  각 코드 블록의 줄바꿈이 살아 있는지 소스에서 확인한다.
- **수식 클래스에는 컴포넌트 접두사를 붙인다**: `.callout.callout-warn`, `.pill.pill-run`.
  `.warn`, `.tbd`처럼 맨이름을 쓰면 다른 컴포넌트(배지 등)의 같은 이름 규칙이 먹어 본문이
  엉뚱한 스타일로 렌더된다.

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

## 브랜드 팔레트

사용자가 조직·브랜드 색을 원할 때 위 토큰 값을 바꾸는 절차. 토큰 이름과 컴포넌트는 그대로
두고 값만 바꾼다.

1. **근거를 뽑는다** — 공식 로고 SVG(파비콘 등)의 `fill` 값과 공식 사이트 CSS에서 자주
   쓰이는 hex를 뽑는다. 공식 출처를 못 찾으면 색을 추측하지 않는다. 자회사·제품 사이트 등
   다른 출처에서 가져왔으면 어디서 가져왔는지 사용자에게 밝힌다. 출처는 `:root` 위 주석에
   남긴다.
2. **브랜드 색은 역할 토큰으로만 쓴다.**
   - `--ink`: 본문 글자. 사이트의 본문 색을 쓴다.
   - `--accent`: 링크, 표 헤더 글자, 현재 문서, 소제목. 브랜드 주색.
   - `--accent-soft`: 표 헤더·현재 항목 배경. 주색을 아주 옅게.
   - `--accent2`, `--accent2-soft`: 보조색. 현재 항목 표시줄, 하위 목록 선 같은 장식에만
     쓴다.
   - `--accent2-ink`: 보조색을 글자로 쓸 때의 진한 변형. 보조색이 배경 대비 4.5:1 미만이면
     만든다(`python3 scripts/contrast.py <글자색> <배경색>`).
   - `--bg`, `--line`, `--sub`: 주색 쪽으로 살짝 기운 회색.
   - `--ok`, `--warn`, `--bad`: 상태색은 브랜드와 분리해 원래 의미(초록·주황·빨강)를
     유지한다.
3. **mermaid도 같은 토큰을 쓴다** — `theme: 'base'`에 `themeVariables`로 넘긴다
   (`primaryColor`=accent-soft, `primaryBorderColor`=accent, `primaryTextColor`·`textColor`=ink,
   `secondaryColor`=accent2-soft, `secondaryBorderColor`=accent2, `lineColor`=sub,
   `noteBkgColor`=accent2-soft, `noteBorderColor`=accent2).
4. **장식은 주색 단색 하나만** — 상단 바 아래 `--accent` 한 색 줄 정도로 그친다. 로고가
   여러 색이어도 색을 나눈 줄로 늘어놓지 않는다.
5. **라이트 고정 요청이면** 다크 모드 블록을 넣지 않는다(문서 묶음 "다이어그램" 절의 테마
   고정과 같다).

## 컴포넌트 카탈로그

### 1. 목차 `.toc`
`<nav class="toc">` + `<ol>` + 앵커 링크. 문서 맨 위 1회.

### 2. 접이식 배경 `.skippable`
`<details class="skippable" open>` — 독자 수준을 모를 때 깊은 배경을 넣되 접을 수 있게.
`<summary>`에 "아는 분은 접어도 됩니다" 류 안내를 쓴다.

### 3. Callout `.callout`
핵심 개념·정의는 기본(파랑), 엣지 케이스·주의는 `.callout.callout-warn`(주황).
첫 `<b>`가 제목 줄이 된다. 문서당 소수만 — 전부 강조하면 아무것도 강조되지 않는다.

```html
<div class="callout"><b>핵심 용어 — job</b> 설명…</div>
<div class="callout callout-warn"><b>기록 제외는 딱 하나</b> 설명…</div>
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
  <span class="lbl">t₀ 수신</span> id=a3f2… · <span class="pill pill-run">RUNNING</span> · result=∅
</div>
```

`.pill.pill-run`(주황) / `.pill.pill-done`(초록) / `.pill.pill-fail`(빨강).

### 6. 표
파일↔역할, 옵션 비교 같은 짧은 사실 나열에만. 설명·해석은 표 밖에 둔다
(`writing-style.md` §9).

### 7. 인터랙티브 퀴즈 `.quiz`
`data-answer`(0-기반 정답 인덱스)를 가진 컨테이너 + 선택지 `<button>` + 빈 `.fb`.
아래 공용 JS가 클릭 시 정오 판정·해설을 표시한다. 해설 텍스트는 JS의 `notes` 맵에
문항 라벨(Q1…)로 넣는다. 함정 금지, 본문을 이해해야 풀리는 중간 난이도.

## 반응형

- 본문 `max-width: 860px`, 모바일(≤640px)에서 `.flow`가 세로로 전환되고 화살표가
  90° 회전한다 — 다이어그램이 폰에서도 깨지지 않는 핵심.
- 넓은 내용(표·pre·diagram)은 각자 `overflow-x: auto`.

### 표 셀 줄바꿈

좁은 표 칸에서 단어가 중간에 끊기지 않게 한다.

- **한글은 어절 단위로 끊는다** — `body`에 `word-break: keep-all; overflow-wrap: break-word;`
  (기본 CSS에 포함). 없으면 "판정 방/식"처럼 음절 중간에서 끊긴다.
- **인라인 코드에 `overflow-wrap: anywhere`를 쓰지 않는다** — 표 열의 최소 폭이 줄어
  `calibration/_rule`처럼 식별자를 아무 데서나 자른다.
- **경로형 코드는 `/`에서만 끊는다** — 코드를 `/` 기준으로 나눠 조각마다
  `white-space: nowrap`인 `<span>`으로 감싸고, `/` 뒤에 `<wbr>`을 넣는다. 원고를 HTML로
  바꾸는 빌드가 하는 게 가장 확실하다.

```html
<code><span>/api/</span><wbr><span>admin/</span><wbr><span>v1/</span><wbr><span>operations</span></code>
```

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
       color: var(--ink); background: var(--bg); line-height: 1.7;
       word-break: keep-all; overflow-wrap: break-word; }
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
code span { white-space: nowrap; }
p code, li code, td code { background: var(--panel); border: 1px solid var(--line);
      border-radius: 4px; padding: 1px 5px; font-size: .86em; color: #23304d; }
.callout { border-left: 4px solid var(--accent); background: var(--accent-soft);
           border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 18px 0; }
.callout.callout-warn { border-color: var(--warn); background: var(--warn-soft); }
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
.pill.pill-run { background: var(--warn-soft); color: var(--warn); }
.pill.pill-done { background: var(--ok-soft); color: var(--ok); }
.pill.pill-fail { background: var(--bad-soft); color: var(--bad); }
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

## 문서 묶음 (다중 페이지)

허브 + 유형별 페이지로 된 문서 묶음(`../templates/doc_set.md`)을 HTML로 낼 때의 규칙.
페이지마다 위 디자인 토큰·컴포넌트를 그대로 쓰고, 아래만 더한다. "외부 의존 없음"의
예외는 mermaid 로드 하나다.

### 원고와 빌드

- **원고는 페이지마다 Markdown 한 파일**이고, 빌드 스크립트가 HTML로 바꾼다. 손으로
  HTML 여러 장을 고치면 공통 부분이 어긋난다.
- **빌드는 페이지 목록(`doc_set.md` "묶음 규칙")을 읽어** H1, lede, 사이드바, 허브의
  문서 지도, 이전/다음 링크를 만든다.
- **앵커는 고정 id다** — 원고에 `## 제목 {#id}`로 쓰고, H3에도 같은 문법을 지원한다.
  H2 순서 번호(`#s3`)로 앵커를 만들면 절을 하나 넣을 때 기존 링크가 조용히 엉뚱한 절을
  가리킨다.
- **빌드 뒤 "산출 뒤 검증"(아래 절)을 돌린다** — 링크 검사가 실패하면 빌드를 실패로 본다.

### 탐색

- **공통 사이드바** — 페이지를 유형별 그룹(개요·설명·참조·가이드·부록 등)으로 묶는다.
  - 문서마다 `<details>` 토글 하나. 펼치면 첫 항목 "처음"(문서 맨 위) 다음에 그 문서의
    H2가 하위 링크로 나온다.
  - 현재 문서는 `open`으로 열고 `aria-current="page"`로 강조한다.
  - 좁은 화면(≤860px)에서는 사이드바를 숨기고 상단 "문서 목록" 버튼(`<details class="mnav">`)
    안에 같은 목록을 넣는다.
- **이전/다음 링크**를 본문 끝에 둔다(페이지 목록 순서).
- **페이지 내 목차는 좁은 화면에서만** 보인다 — 넓은 화면에서는 사이드바의 H2 목록과
  겹치므로 숨긴다.

```css
.cols { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 32px; }
.sidecol { position: sticky; top: 56px; align-self: start; max-height: calc(100vh - 64px); overflow-y: auto; }
.side summary[aria-current="page"] { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
.side .sub { font-size: .86rem; }
.mnav { display: none; }
.pn { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 56px; }
.pn .next { text-align: right; }
@media (min-width: 861px) { .ontoc { display: none; } }
@media (max-width: 860px) {
  .cols { grid-template-columns: 1fr; }
  .sidecol { display: none; }
  .mnav { display: block; }
}
```

### 다이어그램 (mermaid)

문서 묶음은 흐름도가 많아 mermaid를 허용한다(단일 파일 산출물은 위 `.flow` 원칙 그대로).

- **렌더 블록 클래스를 `mermaid`가 아닌 자체 클래스(예: `pre.mmd`)로 두고 직접 렌더한다**
  — `mermaid.initialize({startOnLoad: false})` 후 `mermaid.run({nodes})`. 호스트가
  `pre.mermaid`를 스스로 렌더하는 환경(예: 게시 플랫폼의 메인 페이지)에서는 페이지
  스크립트와 겹쳐 그 페이지의 다이어그램만 사라진다.
- **버전을 고정해 로드한다** — `https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js`
  처럼 정확한 버전을 쓴다.
- **웹폰트가 준비된 뒤 그린다** — `document.fonts.ready`가 끝난 다음 `mermaid.run`을
  부른다. 폰트가 로드되기 전에 그리면 노드 폭을 대체 폰트로 재서 라벨 끝이 잘린다.
- **점선 라벨은 표준 표기** `A -. 라벨 .-> B`를 쓴다.
- **테마를 고정하면 둘 다 고정한다** — 라이트 고정을 원하면 다크 모드용 토큰
  (`prefers-color-scheme: dark` 블록)을 넣지 않고 mermaid `theme`도 라이트 계열 하나로
  고정한다.

### 게시

메인 페이지 하나와 부속 파일 여러 개를 함께 올리는 게시 플랫폼에 올릴 때:

- 허브를 메인 페이지로, 나머지 페이지를 부속 파일로 올리고 상대 링크(`api.html#get`)로
  잇는다.
- 플랫폼이 메인 페이지만 문서 골격으로 감싸면, 부속 페이지는 `<!doctype html>`,
  `<meta charset="utf-8">`, viewport meta를 갖춘 완전한 문서로 빌드한다. 빠지면 quirks
  모드로 렌더된다.

## 산출 뒤 검증

HTML을 저장한 뒤(문서 묶음은 빌드 뒤) 아래 두 스크립트를 돌리고, 결과를 산출 보고에
적는다. 스크립트는 이 문서 옆 `scripts/`에 있다.

| 스크립트 | 검사하는 것 | 종료 코드 |
|---|---|---|
| `python3 scripts/check_links.py <html 디렉토리>` | 내부 링크(`page.html#id`, `#id`)의 페이지·id가 실재하는지 | 0 이상 없음 / 1 깨진 링크 있음 |
| `sh scripts/check_wrap.sh <html 디렉토리> 1280 390` | 표 셀 안에서 단어가 두 줄로 쪼개졌는지(폭마다 headless Chrome으로 렌더) | 0 이상 없음 / 1 쪼개진 단어 있음 / 2 Chrome이 없어 건너뜀 |

- **줄바꿈 검사의 허용 지점** — 코드는 `/` 뒤만, 본문은 공백·괄호·가운뎃점·슬래시·쉼표
  앞뒤만 끊겨도 된다. 그 밖에서 끊긴 단어를 보고한다.
- **Chrome이 없으면 건너뛰고 그 사실을 보고한다** — 통과로 적지 않는다. 경로가 다르면
  `CHROME` 환경 변수로 지정한다.
- **쪼개진 단어가 나오면 위 "표 셀 줄바꿈" 처방으로 고친 뒤 다시 돌린다.**
