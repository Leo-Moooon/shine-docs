# HTML 산출물 레이아웃 가이드 (html-layout)

자기완결 HTML 산출물(diff 해설, 리포트 등)에 쓰는 레이아웃 시스템의 핸드오프 문서.
`writing-style.md`가 문장을 정한다면, 이 문서는 HTML의 시각 골격을 정한다.

**이 문서가 정하는 스타일이 산출물의 디자인 시스템이다.** 게시 플랫폼(아티팩트 등)의 디자인
지침이 "주제마다 고유한 팔레트·타이포그래피를 정하라"고 해도, 이 스킬의 HTML 산출물에서는
이 문서가 우선한다. 주제에 맞춰 색·글꼴·레이아웃을 새로 고르지 않는다.

- **문서 묶음**은 완성된 셸(`doc_set_shell.css`, `doc_set_shell.html`)과 빌드 스크립트를
  **그대로 쓴다**. 바꿔도 되는 것은 `:root` 토큰 값뿐이다 — 아래 "문서 묶음" 절.
- **단일 파일 산출물**은 아래 기본 CSS·컴포넌트·JS를 복사해 시작하고, 쓰지 않는 컴포넌트의
  규칙만 뺀다. 토큰과 남은 규칙의 값은 바꾸지 않는다.

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

**문서 묶음의 기본 팔레트는 사내 브랜드다** — `doc_set_shell.css`의 `:root`에 이미
들어 있다(인디고 `#403391` 주색, 민트 `#57C29E` 보조색, 잉크 `#1B1B29`, 배경 `#f7f7f9` + 흰
패널). 사용자가 묻지 않아도 이 값으로 낸다.

| 토큰 | 값 | 쓰는 곳 |
|---|---|---|
| `--accent` / `--accent-soft` / `--accent-line` | `#403391` / `#eeebf8` / `#cfc8ec` | 링크, H3, 표 헤더, 상단 바 아래 줄, 현재 문서 / 그 배경 / 후속 칩 테두리 |
| `--accent2` / `--accent2-ink` / `--accent2-soft` | `#57c29e` / `#177a5a` / `#e7f6f0` | 현재 문서 표시줄 / eyebrow·이전·다음 라벨 글자 / 하위 목록 선 |
| `--ink` / `--sub` / `--line` | `#1b1b29` / `#5d5d70` / `#e5e4ec` | 본문 / 보조 글자 / 경계선 |
| `--bg` / `--panel` | `#f7f7f9` / `#ffffff` | 페이지 배경 / 표·다이어그램·목차 패널 |
| `--tbd` / `--tbd-soft` / `--tbd-line` | `#8a5a00` / `#fbf1dc` / `#e8cf98` | 콜아웃, TBD 칩 |

사용자가 **다른 조직**의 브랜드 색을 원할 때만 아래 절차로 토큰 값을 바꾼다. 토큰 이름과
컴포넌트는 그대로 두고 값만 바꾼다. 기본 값은 이 절차의 결과이므로 다시 뽑지 않는다.

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
   - `--ok`, `--warn`, `--bad`, `--tbd`: 상태색은 브랜드와 분리해 원래 의미(초록·주황·빨강,
     TBD는 황토)를 유지한다.
3. **mermaid도 같은 토큰을 쓴다** — 문서 묶음 셸의 스크립트는 `:root` 토큰을 읽어
   `themeVariables`로 넘기므로 따로 고치지 않는다. 단일 파일에 mermaid를 쓰면 같은 대응
   (`primaryColor`=accent-soft, `primaryBorderColor`=accent, `primaryTextColor`·`textColor`=ink,
   `secondaryColor`=accent2-soft, `secondaryBorderColor`=accent2, `lineColor`=sub,
   `noteBkgColor`=accent2-soft, `noteBorderColor`=accent2)을 손으로 넘긴다.
4. **장식은 주색 단색 하나만** — 상단 바 아래 `--accent` 한 색 줄 정도로 그친다. 로고가
   여러 색이어도 색을 나눈 줄로 늘어놓지 않는다.
5. **라이트 고정이다** — 문서 묶음 셸은 다크 모드 블록이 없다. 브랜드를 바꿔도 다크 모드
   블록을 더하지 않는다.

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
단일 파일용 기본 CSS·컴포넌트 카탈로그 대신 아래 셸을 쓴다. "외부 의존 없음"의 예외는
웹폰트(IBM Plex Sans KR·IBM Plex Mono)와 mermaid 로드다.

### 셸 — 그대로 쓴다

| 파일 | 담은 것 |
|---|---|
| `doc_set_shell.css` | `:root` 토큰과 전체 CSS |
| `doc_set_shell.html` | 페이지 골격(상단 바, 사이드바, 좁은 화면 문서 목록, 페이지 머리, 좁은 화면 목차, 이전/다음, mermaid 스크립트)과 `{{이름}}` 자리표시자 |
| `scripts/build_doc_set.py` | 페이지 목록 JSON과 페이지별 Markdown 원고로 셸을 채워 페이지마다 HTML 한 파일을 만드는 빌드 |

- **CSS와 골격을 고치지 않는다.** 바꿔도 되는 것은 `:root` 토큰 값뿐이고, 그것도 다른 조직
  브랜드를 요청받았을 때만이다(위 "브랜드 팔레트").
- **규칙을 더하지도 덜지도 않는다.** 쓰지 않는 컴포넌트가 있어도 CSS를 그대로 둔다 — 묶음마다
  CSS가 조금씩 달라지는 것이 스타일이 갈라지는 출발점이다.
- **셸에 없는 컴포넌트가 필요하면** 셸 안의 것으로 바꿔 쓴다(흐름은 mermaid, 비교는 표, 주의는
  콜아웃). 그래도 안 되면 산출 보고에 적고 셸 확장을 사용자에게 제안한다.
- **HTML을 손으로 쓰지 않는다** — 빌드 스크립트로 만든다. 다른 빌드를 써야 하는 환경이면
  스크립트의 산출과 같은 마크업을 낸다.

### 원고와 빌드

```sh
python3 scripts/build_doc_set.py <pages.json> <출력 디렉토리>
```

- **페이지 목록 JSON이 원본이다**(`doc_set.md` "묶음 규칙"). 첫 페이지가 허브다.

```json
{
  "brand": "content-labeler",
  "brand_sub": "서비스 설계",
  "pages": [
    {"file": "index.html", "src": "index.md", "title": "content-labeler 서비스 설계", "type": "개요",
     "lede": "서비스가 하는 일과 요청 흐름, 문서 구성을 다룹니다."},
    {"file": "api.html", "src": "api.md", "title": "클라이언트 API", "type": "참조",
     "lede": "클라이언트가 보내고 받는 것을 다룹니다.", "readers": "클라이언트", "status": "TBD"}
  ]
}
```

| 필드 | 필수 | 설명 |
|---|---|---|
| `brand` | 예 | 상단 바의 고정폭 브랜드명(서비스·주제 이름) |
| `brand_sub` | 아니요 | 브랜드명 옆 보조 글자 |
| `pages[].file` | 예 | 출력 파일 이름 |
| `pages[].src` | 예 | 원고 경로(JSON 파일 기준) |
| `pages[].title` | 예 | H1, 사이드바, 문서 지도, 이전/다음의 이름 |
| `pages[].type` | 예 | 페이지 유형. eyebrow와 사이드바 그룹 이름이 되고, 허브는 `개요` |
| `pages[].lede` | 예 | 한 줄 요약. 페이지 머리와 문서 지도 "다루는 것" 칸 |
| `pages[].readers` | 아니요 | 문서 지도 "주 독자" 칸. 비우면 `—` |
| `pages[].status` | 아니요 | `TBD`·`후속`·`범위 밖`. 페이지 제목·사이드바·문서 지도에 상태 칩 |

- **원고는 개요 문단부터 쓴다** — 페이지 머리(eyebrow·H1·lede), 사이드바, 좁은 화면 목차,
  허브의 문서 지도 표, 이전/다음은 빌드가 페이지 목록에서 만든다.
- **빌드 경고를 남기지 않는다** — 개요 문단이 없거나 메타 담화로 시작할 때, 본문에 "(제안)"이
  있을 때 경고가 나온다. 고친 뒤 다시 빌드한다.
- **빌드 뒤 "산출 뒤 검증"(아래 절)을 돌린다** — 링크 검사가 실패하면 빌드를 실패로 본다.

### 원고 문법

| 원고 | 산출 |
|---|---|
| `## 제목 {#id}` | 고정 id가 붙은 H2. id가 없으면 빌드가 멈춘다 |
| `### 제목`, `### 제목 {#id}` | 주색 H3 |
| `{{doc-map}}` 한 줄 | 문서 지도 표(허브의 "문서 지도" 절에 둔다) |
| `> [!TBD] 제목` 다음 줄부터 `> - 항목` | 콜아웃. `TBD` 자리에 `후속`·`범위 밖`도 쓸 수 있다 |
| `[[TBD]]`, `[[후속]]`, `[[범위 밖]]` | 상태 칩 |
| `→ [페이지 제목](api.md#put)` | 보조 글자색 화살표와 내부 링크. `.md` 링크는 출력 파일 이름으로 바뀐다 |
| `[제목](https://…)` | 새 창으로 여는 외부 링크와 `↗` |
| 인라인 코드 | `/` 뒤에서만 줄이 바뀌는 코드 |
| `mermaid` 코드 블록 | 다이어그램 패널 |
| 그 밖의 코드 블록 | 언어 라벨이 붙은 코드 상자 |
| `- **리드.**`와 들여 쓴 `- 하위 항목` | 중첩 목록 |
| 파이프 표(헤더 아래 구분 줄) | 표 |

- **앵커는 고정 id다** — H2 순서 번호(`#s3`)로 앵커를 만들면 절을 하나 넣을 때 기존 링크가
  조용히 엉뚱한 절을 가리킨다.
- **본문의 `→`는 모두 상호 참조 화살표로 칠해진다** — 화살표 체인을 쓰지 않는다
  (`writing-style.md` §8).

### 컴포넌트 규격

셸이 정한 규격이다. 검증 리뷰는 산출 HTML을 이 표와 셸 파일에 대조한다
(`verification-checklist.md` "HTML 산출물").

| 컴포넌트 | 규격 |
|---|---|
| 상단 바 | 위에 붙어 따라온다(sticky). 왼쪽에 고정폭 브랜드명과 보조 글자, 아래에 3px 주색 줄. 좁은 화면에서는 오른쪽에 "문서 목록" 버튼 |
| 사이드바 | 유형 그룹 라벨(고정폭 대문자) 아래 문서마다 접는 토글. 펼치면 "처음" 다음에 그 문서의 H2. 현재 문서는 펼쳐 두고 옅은 주색 배경·주색 굵은 글자·왼쪽 보조색 줄 |
| 페이지 머리 | 유형 eyebrow(고정폭, 진한 보조색 글자) → H1(상태가 있으면 큰 칩) → lede(보조 글자색) → 아래 구분선 |
| 본문 | 15px, 줄 간격 1.72, 문단 폭 72ch. 첫 문단(개요)은 조금 크게. H2 위 구분선, H3 주색 |
| 표 | 흰 패널, 셀마다 1px 테두리. 헤더는 옅은 주색 배경·주색 굵은 글자·아래 2px 주색 줄. 넓으면 표 상자 안에서 가로 스크롤 |
| 다이어그램 | 흰 패널(테두리·둥근 모서리) 안 가운데 정렬 mermaid |
| 콜아웃 | 한 종류뿐이다. 황토 배경·테두리, 제목 줄 맨 앞에 상태 칩. 개요 문단 바로 아래 |
| 상태 칩 | `TBD`(황토)·`후속`(주색)·`범위 밖`(회색) 셋. 페이지 제목·사이드바·문서 지도·목록 항목 앞에 단다 |
| 좁은 화면 목차 | 860px 이하에서만 보인다. 접지 않고 늘 펼친 2단 박스 |
| 링크 | 외부 링크는 새 창과 `↗`. 상호 참조 화살표는 보조 글자색 |
| 이전/다음 | 본문 끝 카드 두 칸, 라벨은 진한 보조색. 480px 이하에서 한 칸 |

- **"처음"은 헤더의 `id="top"`으로 연결한다**(현재 문서는 `#top`, 다른 문서는 `x.html#top`).
  같은 페이지 주소로 걸면 눌러도 움직이지 않는다.
- **넓은 화면에서 페이지 내 목차를 숨긴다** — 사이드바의 H2 목록과 겹친다.

### 다이어그램 (mermaid)

문서 묶음은 흐름도가 많아 mermaid를 쓴다(단일 파일 산출물은 위 `.flow` 원칙 그대로). 셸
스크립트가 아래를 지키므로 스크립트를 바꾸지 않는다.

- **렌더 블록 클래스는 `pre.mmd`다** — `mermaid.initialize({startOnLoad: false})` 후
  `mermaid.run({nodes})`로 직접 그린다. 호스트가 `pre.mermaid`를 스스로 렌더하는 환경(예:
  게시 플랫폼의 메인 페이지)에서는 페이지 스크립트와 겹쳐 그 페이지의 다이어그램만 사라진다.
- **버전을 고정하고 무결성 해시를 단다** — `mermaid@11.4.1`, `integrity` 속성.
- **웹폰트가 준비된 뒤 그린다** — `document.fonts.ready` 뒤에 `mermaid.run`을 부른다. 먼저
  그리면 노드 폭을 대체 폰트로 재서 라벨 끝이 잘린다.
- **색은 `:root` 토큰에서 읽는다** — 토큰 값만 바꾸면 다이어그램 색도 따라 바뀐다.

원고에서는 점선 라벨을 표준 표기 `A -. 라벨 .-> B`로 쓴다.

### 게시

메인 페이지 하나와 부속 파일 여러 개를 함께 올리는 게시 플랫폼에 올릴 때:

- 허브를 메인 페이지로, 나머지 페이지를 부속 파일로 올리고 상대 링크(`api.html#get`)로
  잇는다.
- 빌드 산출은 페이지마다 `<!doctype html>`, `<meta charset="utf-8">`, viewport meta를 갖춘
  완전한 문서다. 플랫폼이 메인 페이지만 문서 골격으로 감싸도 부속 페이지가 quirks 모드로
  렌더되지 않는다.
- 플랫폼의 디자인 지침이 주제별 팔레트·타이포그래피를 요구해도 셸을 바꾸지 않는다(이 문서 첫머리).

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
