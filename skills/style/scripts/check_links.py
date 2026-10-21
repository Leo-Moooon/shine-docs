# 사용: python3 check_links.py <html 디렉토리> — 내부 링크의 페이지·앵커가 실재하는지 검사한다
import re, pathlib, sys
out = pathlib.Path(sys.argv[1])
ids = {p.name: set(re.findall(r'id="([^"]+)"', p.read_text())) for p in out.glob('*.html')}
bad = []
for p in out.glob('*.html'):
    for href in re.findall(r'href="([^"]+)"', p.read_text()):
        if href.startswith(('http', 'mailto:')):
            continue
        page, _, frag = href.partition('#')
        page = page or p.name
        if page not in ids or (frag and frag not in ids[page]):
            bad.append(f'{p.name}: {href}')
print('\n'.join(bad) or '깨진 내부 링크가 없습니다.')
sys.exit(1 if bad else 0)
