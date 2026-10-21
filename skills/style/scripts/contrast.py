# 사용: python3 contrast.py <글자색 hex> <배경색 hex> — WCAG 대비율을 출력하고, 본문 글자 기준(4.5:1) 미달이면 1로 끝난다
import sys


def luminance(hex_color):
    channels = [int(hex_color.lstrip('#')[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


hi, lo = sorted([luminance(sys.argv[1]), luminance(sys.argv[2])], reverse=True)
ratio = (hi + 0.05) / (lo + 0.05)
ok = ratio >= 4.5
print(f'{sys.argv[1]} / {sys.argv[2]}: {ratio:.2f}:1 — ' + ('본문 글자로 쓸 수 있습니다.' if ok else '본문 글자로 쓰기에는 대비가 부족합니다(4.5:1 미만).'))
sys.exit(0 if ok else 1)
