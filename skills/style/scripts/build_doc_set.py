# 사용: python3 build_doc_set.py <pages.json> <출력 디렉토리>
# 문서 묶음 빌드 — 페이지 목록 JSON과 페이지별 Markdown 원고에 문서 묶음 셸(../doc_set_shell.*)을 입혀
# 페이지마다 완전한 HTML 문서를 만든다. 원고 문법은 html-layout.md "원고 문법" 절이 원본이다.
import html, json, pathlib, re, sys

SHELL = pathlib.Path(__file__).resolve().parent.parent
CHIPS = {'TBD': 'chip chip-tbd', '후속': 'chip chip-future', '범위 밖': 'chip chip-out'}
CHIP_RE = re.compile(r'\[\[(TBD|후속|범위 밖)\]\]')
LIST_RE = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')
HEAD_RE = re.compile(r'^(#{2,3})\s+(.*?)(?:\s+\{#([A-Za-z0-9_-]+)\})?\s*$')
CALLOUT_RE = re.compile(r'^\[!(TBD|후속|범위 밖)\]\s*(.*)$')
META_OPENERS = ('이 페이지는', '이 페이지를 읽으면', '이 페이지에서는', '이 문서는', '이 문서를 읽으면', '이 묶음을 읽으면', '이 문서 묶음을 읽으면')
warnings = []


def fail(msg):
    sys.exit(f'빌드를 멈춥니다: {msg}')


def chip(label, big=False):
    return f'<span class="{CHIPS[label]}{" chip-big" if big else ""}">{label}</span>'


def code_html(src):
    parts = html.escape(src, quote=False).split('/')
    return '<code>' + '/<wbr>'.join(f'<span class="nb">{p}</span>' if p else '' for p in parts) + '</code>'


def inline(text, links):
    codes = []
    def keep(m):
        codes.append(code_html(m.group(1)))
        return f'\x00{len(codes) - 1}\x00'
    text = re.sub(r'`([^`]+)`', keep, text)
    text = html.escape(text, quote=False)
    text = CHIP_RE.sub(lambda m: chip(m.group(1)), text)
    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(('http://', 'https://')):
            return f'<a href="{href}" target="_blank" rel="noopener" class="ext">{label}</a>'
        path, _, frag = href.partition('#')
        path = links.get(path, path)
        return f'<a href="{path}{"#" + frag if frag else ""}">{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = text.replace('→', '<span class="to">→</span>')
    return re.sub('\x00(\\d+)\x00', lambda m: codes[int(m.group(1))], text)


def is_block_start(line):
    s = line.strip()
    return (s.startswith(('```', '>', '|', '## ', '### ')) or s == '{{doc-map}}'
            or LIST_RE.match(line) is not None)


def render_list(items, i):
    indent, ordered = items[i][0], items[i][1]
    out = ['<ol>' if ordered else '<ul>']
    while i < len(items) and items[i][0] == indent:
        text = items[i][2]
        i += 1
        sub = ''
        while i < len(items) and items[i][0] > indent:
            nested, i = render_list(items, i)
            sub += nested
        out.append(f'<li>{text}{sub}</li>')
    out.append('</ol>' if ordered else '</ul>')
    return ''.join(out), i


def table_html(rows, links):
    def cells(row):
        return [c.strip() for c in row.strip().strip('|').split('|')]
    head = ''.join(f'<th>{inline(c, links)}</th>' for c in cells(rows[0]))
    body = ''.join('<tr>' + ''.join(f'<td>{inline(c, links)}</td>' for c in cells(r)) + '</tr>' for r in rows[2:])
    return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def blocks(lines, ctx, headings=None):
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
        elif s.startswith('```'):
            lang, buf = s[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            code = html.escape('\n'.join(buf), quote=False)
            if lang == 'mermaid':
                out.append(f'<div class="diagram"><pre class="mmd">{code}</pre></div>')
            else:
                label = f'<span class="lang">{lang}</span>' if lang else ''
                out.append(f'<div class="codewrap">{label}<pre><code>{code}</code></pre></div>')
        elif HEAD_RE.match(s) and headings is not None:
            hashes, text, hid = HEAD_RE.match(s).groups()
            level = len(hashes)
            if level == 2 and not hid:
                fail(f'{ctx["src"]}: H2 "{text}"에 고정 id가 없습니다. "## {text} {{#id}}"로 써 주세요.')
            if hid:
                if hid == 'top' or hid in ctx['ids']:
                    fail(f'{ctx["src"]}: id "{hid}"가 겹칩니다.')
                ctx['ids'].add(hid)
            rendered = inline(text, ctx['links'])
            if level == 2:
                headings.append((hid, rendered))
            out.append(f'<h{level}{f" id={chr(34)}{hid}{chr(34)}" if hid else ""}>{rendered}</h{level}>')
            i += 1
        elif s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            m = CALLOUT_RE.match(buf[0].strip())
            if not m:
                fail(f'{ctx["src"]}: 콜아웃 첫 줄은 "> [!TBD] 제목"(또는 후속·범위 밖) 형식이어야 합니다.')
            inner = blocks(buf[1:], ctx)
            out.append(f'<aside class="callout"><p class="callout-title">{chip(m.group(1))}{inline(m.group(2), ctx["links"])}</p>{inner}</aside>')
        elif s.startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                buf.append(lines[i])
                i += 1
            out.append(table_html(buf, ctx['links']))
        elif s == '{{doc-map}}':
            out.append(ctx['doc_map'])
            i += 1
        elif LIST_RE.match(line):
            items = []
            while i < len(lines):
                m = LIST_RE.match(lines[i])
                if m:
                    items.append([len(m.group(1).expandtabs(4)), m.group(2)[-1] == '.', m.group(3)])
                    i += 1
                elif lines[i].strip() and lines[i][:1].isspace():
                    items[-1][2] += ' ' + lines[i].strip()
                    i += 1
                elif not lines[i].strip() and i + 1 < len(lines) and (LIST_RE.match(lines[i + 1]) or lines[i + 1][:1].isspace()):
                    i += 1
                else:
                    break
            for item in items:
                item[2] = inline(item[2], ctx['links'])
            j = 0
            while j < len(items):
                rendered, j = render_list(items, j)
                out.append(rendered)
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not (buf and is_block_start(lines[i])):
                buf.append(lines[i].strip())
                i += 1
            out.append(f'<p>{inline(" ".join(buf), ctx["links"])}</p>')
    return '\n'.join(out)


def lint(page, body_md):
    first = next((l.strip() for l in body_md if l.strip()), '')
    if is_block_start(first) or first.startswith('#'):
        warnings.append(f'{page["src"]}: 개요 문단이 없습니다. H1 아래 첫 블록은 주제를 정의하는 문단이어야 합니다.')
    elif first.startswith(META_OPENERS):
        warnings.append(f'{page["src"]}: 개요 문단이 메타 담화("{first[:12]}…")로 시작합니다. 주제의 정의로 시작해 주세요.')
    if '(제안)' in '\n'.join(body_md):
        warnings.append(f'{page["src"]}: 본문에 "(제안)" 표기가 있습니다. 미확정 표시는 상태 칩([[TBD]] 등)으로 바꿔 주세요.')


def main():
    if len(sys.argv) != 3:
        sys.exit('사용법: python3 build_doc_set.py <pages.json> <출력 디렉토리>')
    spec_path, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    spec = json.loads(spec_path.read_text())
    pages = spec['pages']
    for p in pages:
        if p.get('status') and p['status'] not in CHIPS:
            fail(f'{p["file"]}: status는 {", ".join(CHIPS)} 중 하나여야 합니다.')
    links = {p['src']: p['file'] for p in pages}
    hub = pages[0]
    rows = ''.join(
        f'<tr><td>{p["type"]}</td><td><a href="{p["file"]}">{html.escape(p["title"])}</a>'
        f'{" " + chip(p["status"]) if p.get("status") else ""}</td><td>{inline(p["lede"], links)}</td>'
        f'<td>{inline(p.get("readers") or "—", links)}</td></tr>' for p in pages[1:])
    doc_map = ('<div class="tablewrap"><table><thead><tr><th>유형</th><th>문서</th><th>다루는 것</th><th>주 독자</th>'
               f'</tr></thead><tbody>{rows}</tbody></table></div>')

    for p in pages:
        md = (spec_path.parent / p['src']).read_text().splitlines()
        lint(p, md)
        p['_ctx'] = {'src': p['src'], 'ids': set(), 'links': links, 'doc_map': doc_map}
        p['_h2'] = []
        p['_body'] = blocks(md, p['_ctx'], p['_h2'])
    if len(hub['_h2']) > 4:
        warnings.append(f'{hub["src"]}: 허브에 H2가 {len(hub["_h2"])}개 있습니다. 서비스가 하는 일·흐름·문서 지도·원칙 밖의 절은 부록 페이지로 옮겨 주세요.')

    groups = list(dict.fromkeys(p['type'] for p in pages))
    css = (SHELL / 'doc_set_shell.css').read_text().strip()
    shell = (SHELL / 'doc_set_shell.html').read_text()
    out.mkdir(parents=True, exist_ok=True)
    for n, cur in enumerate(pages):
        side = []
        for g in groups:
            side.append(f'<p class="grp">{g}</p><ul>')
            for p in (q for q in pages if q['type'] == g):
                here = p is cur
                subs = ''.join(f'<li><a href="{p["file"]}#{hid}">{text}</a></li>' for hid, text in p['_h2'])
                status = f' {chip(p["status"])}' if p.get('status') else ''
                side.append(
                    f'<li><details{" open" if here else ""}><summary{" aria-current=" + chr(34) + "page" + chr(34) if here else ""}>'
                    f'{html.escape(p["title"])}{status}</summary><ul class="sub"><li><a href="{"" if here else p["file"]}#top">처음</a></li>'
                    f'{subs}</ul></details></li>')
            side.append('</ul>')
        side_html = '<nav class="side" aria-label="문서 목록">' + ''.join(side) + '</nav>'
        prev = (f'<a class="prev" href="{pages[n - 1]["file"]}"><small>이전</small>{html.escape(pages[n - 1]["title"])}</a>'
                if n > 0 else '<span></span>')
        nxt = (f'<a class="next" href="{pages[n + 1]["file"]}"><small>다음</small>{html.escape(pages[n + 1]["title"])}</a>'
               if n + 1 < len(pages) else '<span></span>')
        fill = {
            'doc_title': html.escape(cur['title'] if cur is hub else f'{cur["title"]} · {spec["brand"]}'),
            'css': css, 'hub_file': hub['file'], 'brand': html.escape(spec['brand']),
            'brand_sub': html.escape(spec.get('brand_sub', '')), 'side': side_html,
            'eyebrow': html.escape(cur['type']), 'title': html.escape(cur['title']),
            'title_chip': ' ' + chip(cur['status'], big=True) if cur.get('status') else '',
            'lede': inline(cur['lede'], links),
            'ontoc': ''.join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in cur['_h2']),
            'body': cur['_body'], 'prev': prev, 'next': nxt,
        }
        page_html = re.sub(r'\{\{(\w+)\}\}', lambda m: fill[m.group(1)], shell)
        (out / cur['file']).write_text(page_html)
    for w in warnings:
        print(f'경고: {w}', file=sys.stderr)
    print(f'{len(pages)}개 페이지를 {out}에 만들었습니다.')


if __name__ == '__main__':
    main()
