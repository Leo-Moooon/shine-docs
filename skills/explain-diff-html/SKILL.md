---
name: explain-diff-html
description: Legacy skill kept for direct invocation (/explain-diff-html) and backward compatibility only. For natural-language requests to explain a code change, diff, branch, or PR, use write-document (diff_explanation type) instead. Produces HTML output.
---

# Explain Diff

Please make me a rich, interactive explanation of the specified code change.

It should have these sections:

- Background: Explain the existing system relevant to this change. (You should broadly explore surrounding code for this.) We don't know how much the reader already knows, so include a deep background for beginners (note that it can be skipped if the reader is already familiar), and then a more narrow background directly relevant to the change.
- Intuition: Explain the core intuition for the code change. The focus here is to explain the essence, not the full details. Use concrete examples with toy data. Use figures and diagrams liberally.
- Code: Do a high-level walkthrough of the changes to the code. Group/order the changes in an understandable way.
- Quiz: Come up with five questions that test the reader's knowledge of this PR. This should be medium difficulty, difficult enough that you actually need to understand the substance of the PR to answer them, but not gotchas. The goal is to help the reader make sure that they've actually understood. These should be presented as interactive multiple-choice questions, and when the user clicks, it tells them whether they were correct and gives feedback.

Writing (shared with the other document skills in this plugin):

- Write in Korean unless the user asks otherwise, following `../style/writing-style.md` — read it before drafting. It sets headings, terms, sentences, endings, and the fixed formats for tables, cross-references, citations, and code values.
- This is an explanation-type document. Follow its requirements and the `diff_explanation` row in `../style/doc-types.md`.
- Background and Intuition are flowing prose; lists of files or changes are lists or tables (same form rule as `../templates/diff_explanation.md`).
- Only state what you confirmed in the diff and surrounding code. Label toy data as "설명용 예시".

Format:

- Visual layout: use the shared layout system in `../style/html-layout.md` — copy its
  CSS/quiz JS as the starting point and compose the page from its component catalog.
  That layout is the design system: it takes precedence over any publishing platform's
  guidance to pick a per-topic palette or typography. Drop unused component rules only;
  do not change token or rule values.
- Output a single self-contained HTML file which includes CSS and JavaScript. Make the whole thing one long page with section headers and a table of contents. Don't use tabs for the top-level structure. Basic responsive styling so you can view it on a phone is nice too. Ask where to save it (default: the current working directory) and do not prefix the filename with a date. For example: `explanation-<slug>.html`.
- Please write with the clarity and flow of Martin Kleppmann, making it engaging and written in classic style. Transitions between sections should be smooth.
- Some tips on diagrams. Ideally, you should pick a small number of diagram families that can be reused throughout the explanation to explain various cases. Some useful kinds of diagrams:
  - A very simplified version of the UI that the user sees in the app, to explain UI changes.
  - A system diagram showing data flow or communication between components. Make sure to include example data here!
- Don't use ASCII diagrams. Always use simple HTML designs for your diagrams, HTML lists for lists of things, etc.
  - For code blocks, always use `<pre>` tags. If you use a custom styled div instead, it **must** have
    `white-space: pre-wrap` in its CSS, or the browser will collapse all newlines into a single line.
    Before saving the file, scan each code block in the HTML source and confirm its CSS includes
    `white-space: pre` or `pre-wrap`.
- Use callouts for key concepts or definitions, important edge cases, etc.

After saving:

- Run the post-output checks in `../style/html-layout.md` ("산출 뒤 검증": internal links and split words in table cells) and report the results. If Chrome is missing, report the wrap check as skipped, not passed.
- Offer to run `../review-document/SKILL.md` on the page, with the guide-conformity reviewer as an option.

## Reference

- 이 스킬은 Geoffrey Litt의 "Explain Diff" 프롬프트를 기반으로 합니다: https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524
- 원 프롬프트와 다른 점: 문체·형식은 플러그인 공용 스타일(`../style/`)을 따르고, 파일명에 날짜 접두사를 붙이지 않으며, 저장 뒤 검사와 리뷰를 거칩니다.
