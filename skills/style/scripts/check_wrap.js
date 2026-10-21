// 표 셀 안에서 한 단어가 두 줄로 쪼개졌는지 찾아 body[data-wrap-broken]에 JSON 배열로 남긴다.
// 허용 지점 — 코드: '/' 뒤만. 본문: 공백·괄호·가운뎃점·슬래시·쉼표 앞뒤.
(function () {
  var out = [];
  document.querySelectorAll('td, th').forEach(function (cell) {
    var walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT), n;
    while ((n = walker.nextNode())) {
      var inCode = !!(n.parentElement && n.parentElement.closest('code'));
      var re = inCode ? /[^\s\/]+/g : /[^\s()·\/,]+/g, m;
      while ((m = re.exec(n.data))) {
        var r = document.createRange();
        r.setStart(n, m.index);
        r.setEnd(n, m.index + m[0].length);
        var tops = new Set([].map.call(r.getClientRects(), function (x) { return Math.round(x.top); }));
        if (tops.size > 1) out.push(m[0]);
      }
    }
  });
  document.body.setAttribute('data-wrap-broken', JSON.stringify(out));
})();
