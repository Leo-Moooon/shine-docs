#!/bin/sh
# 사용: sh check_wrap.sh <html 디렉토리> [폭...]   (기본 폭: 1280 390)
# 폭마다 headless Chrome 으로 각 페이지를 열어, 표 셀 안에서 쪼개진 단어를 출력한다.
# 종료 코드: 0 이상 없음 / 1 쪼개진 단어 있음 / 2 Chrome 이 없어 건너뜀
DIR="$1"; shift
WIDTHS="${*:-1280 390}"

C=""
for cand in "${CHROME:-}" "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
            google-chrome google-chrome-stable chromium chromium-browser; do
  [ -n "$cand" ] || continue
  if [ -x "$cand" ] || command -v "$cand" >/dev/null 2>&1; then C="$cand"; break; fi
done
if [ -z "$C" ]; then
  echo "Chrome 을 찾지 못해 표 셀 줄바꿈 검사를 건너뜁니다. CHROME 환경 변수로 경로를 지정할 수 있습니다."
  exit 2
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -R "$DIR"/. "$TMP"/
cp "$(dirname "$0")/check_wrap.js" "$TMP/__check_wrap.js"
for f in "$TMP"/*.html; do
  if grep -q '</body>' "$f"; then
    sed 's#</body>#<script src="__check_wrap.js"></script></body>#' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  else
    printf '<script src="__check_wrap.js"></script>' >> "$f"
  fi
done

found=0
for w in $WIDTHS; do
  for f in "$TMP"/*.html; do
    r=$("$C" --headless=new --disable-gpu --window-size="$w",900 --virtual-time-budget=3000 \
          --dump-dom "file://$f" 2>/dev/null \
        | grep -o 'data-wrap-broken="[^"]*"' | sed 's/data-wrap-broken=//;s/&quot;/"/g')
    if [ -n "$r" ] && [ "$r" != '"[]"' ]; then
      echo "$w $(basename "$f"): $r"
      found=1
    fi
  done
done
[ "$found" -eq 0 ] && echo "표 셀에서 쪼개진 단어가 없습니다."
exit "$found"
