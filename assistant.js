/* The Recursive I Ching — the ONE recursive.eco assistant sidebar.
   <script src="assistant.js" defer></script>   (../assistant.js from pages/)

   NOT a copy of the assistant: this only loads the shared shell,
   https://recursive.eco/js/assistant-launcher.js, which iframes the flow app's
   /assistant embed — the exact same star FAB and tabbed sidebar (Chat · Tarot ·
   I Ching · Astro · Story, same icon bars) every recursive.eco page mounts.
   When the pattern changes in the app, this site follows automatically —
   nothing here to keep in sync. Auth carries too: iching.recursive.eco is a
   .recursive.eco subdomain, so the signed-in session flows into the iframe.
   Ported via recursive-astrology's assistant.js, itself mirroring
   recursive-tarot's include (the pattern source for this repo family). */
(function () {
  // Never render inside an embed: ?embed=1 marks a framed use (matching the
  // rule site-header.js / site-footer.js apply) — this repo has no local
  // instrument that iframes its own pages, but the guard costs nothing to keep.
  if (window.self !== window.top) return;
  if (new URLSearchParams(location.search).get('embed') === '1') return;

  var s = document.createElement('script');
  s.src = 'https://recursive.eco/js/assistant-launcher.js';
  s.defer = true;
  s.onload = function () {
    if (!window.RecursiveAssistant) return;
    window.RecursiveAssistant.init({
      buildSrc: function () {
        var params = new URLSearchParams(location.search);
        var grammarId = params.get('grammar_id') || params.get('id') || '';
        var qs = new URLSearchParams();
        if (grammarId) {
          // A grammar is on the page: the assistant grounds "this grammar" on it.
          qs.set('grammar_id', grammarId);
          qs.set('context', 'iching');
        } else {
          // No grammar: pass page context so "what is this page?" just works.
          qs.set('page_title', document.title || 'The Recursive I Ching');
          qs.set('page_url', location.href);
        }
        return window.RecursiveAssistant.flowBaseUrl() + '/assistant?' + qs.toString();
      }
    });
  };
  document.head.appendChild(s);
})();
