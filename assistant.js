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
   recursive-tarot's include (the pattern source for this repo family).

   Any element with data-assistant-ask="<text>" opens the panel with that text
   waiting in the chat box, unsent (the launcher's ask(); the hexagram detail's
   Cast button uses it). */
(function () {
  // Never render inside an embed: ?embed=1 marks a framed use (matching the
  // rule site-header.js / site-footer.js apply) — this repo has no local
  // instrument that iframes its own pages, but the guard costs nothing to keep.
  if (window.self !== window.top) return;
  if (new URLSearchParams(location.search).get('embed') === '1') return;

  // The grammar on this page, as recursive.eco knows it (Oct 7 2026). The
  // viewers here load a grammar by its repo path (?src=../grammars/<slug>/...)
  // or by ?id=<slug or uuid>; ids.json maps a slug to its recursive.eco id. With
  // that id the embed grounds "this grammar" / "this book" on it, exactly as on
  // recursive.eco's own previews. Fetched now, so it is in hand by the time the
  // embed loads (after the page settles, or on the first open).
  var ecoIds = null;
  try {
    var here = document.currentScript && document.currentScript.src;
    fetch(new URL('ids.json', here || location.href).toString())
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { ecoIds = (j && j.ids) || {}; })
      .catch(function () { ecoIds = {}; });
  } catch (err) { ecoIds = {}; }
  var UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  function pageGrammarId(params) {
    var direct = params.get('grammar_id') || params.get('id') || '';
    if (UUID.test(direct)) return direct;
    var m = (params.get('src') || '').match(/grammars\/([^/]+)\/grammar\.json/);
    var slug = direct || (m ? m[1] : '');
    return (slug && ecoIds && ecoIds[slug]) || '';
  }

  var s = document.createElement('script');
  s.src = 'https://recursive.eco/js/assistant-launcher.js';
  s.defer = true;
  s.onload = function () {
    if (!window.RecursiveAssistant) return;
    window.RecursiveAssistant.init({
      // This site is light-only. Without this the launcher guesses the theme from the
      // page background, and on a dark-mode computer it guessed "dark" and painted an
      // opaque dark square behind the assistant button (Oct 6 2026). opts.theme wins.
      theme: 'light',
      buildSrc: function () {
        var params = new URLSearchParams(location.search);
        var grammarId = pageGrammarId(params);
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
