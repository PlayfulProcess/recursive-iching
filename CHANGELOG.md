# Changelog — The Recursive I Ching

## July 11, 2026 — `GRAMMAR_FORMAT.md` added (docs consolidation)

This repo was missing `GRAMMAR_FORMAT.md` entirely, even though
`recursive-tarot/docs/REPLICATE-THE-PATTERN.md` (the fork playbook this repo
was built from) says every fork should carry it forward. Added the mirrored
copy — synced from the canonical `recursive.eco-schemas/GRAMMAR_FORMAT.md`,
which this round also extended with `ref_item_id`, `performance.words`, and
`_category_roles`/`_section_roles` documentation (three real, shipped fields
that had no public write-up until now). Standard header note: *"Mirrored copy
— canonical version lives in recursive.eco-schemas; if they differ, that one
wins."* Listed in the README file tree. Also added one line to
`docs/HOW-TO-WRITE-A-COURSE.md` (identical across tarot/astrology/starter):
courses should link to `GRAMMAR_FORMAT.md` for field shapes, not restate them.

## July 9, 2026 — Stratigraphy grammars: `zhouyi-core` + `ten-wings` (the book as layers)

Per `docs/PLAN-iching-channel.md` §2: the repo's idiosyncratic structure is the I Ching's own
shape — one book in strata across ~3,000 years — so two new grammars carry the two oldest
English-readable layers, kept apart so a reader can SEE which layer is which.

- **`grammars/zhouyi-core`** — the Western Zhou divination core: Judgment (guaci) + six Line
  statements (yaoci) per hexagram, nothing else (plus the "use of nines/sixes" paragraph that
  exists only for hexagrams 1–2). English: **James Legge's public-domain translation** (The Yî
  King, SBE vol. XVI, 1882/1899). Wilhelm (not PD) was never used. The description teaches the
  built-in stratigraphy lesson: Legge's (parentheses) mark his own interpolations — delete them
  mentally and the Bronze Age oracle's bareness shows.
- **`grammars/ten-wings`** — the Confucian layer as its OWN grammar: the complete **Great Image
  (Daxiang)** for all 64 hexagrams (Legge, Appendix II) + 8 concept items describing the Ten
  Wings (overview, Tuan, Xiang, Xici, Wenyan, Shuogua, Xugua, Zagua) — own synthesis, ✔/○
  marked, each with a verbatim Legge sample quote pulled from the PD Appendixes. Honest thesis,
  stated with confidence, not contempt: Wings composed c. 350–100 BCE by multiple Confucian-
  school hands, centuries after the core; "Confucius wrote them" doubted since Ouyang Xiu
  (11th c.) and rejected by modern scholarship (Shaughnessy; Rutt; Redmond & Hon — verified
  via WebSearch this session).
- **Sourcing under a proxy block, and the verification method** (the part worth reusing):
  sacred-texts.com and gutenberg.org are egress-blocked from this sandbox, but GitHub raw is
  open — so the Legge text came from **three independent digitizations fetched losslessly at
  pinned commit SHAs**, then **diffed word-by-word across ALL 64 hexagrams** (not a sample):
  ~137 diff sites were transliteration only (Khien/Qian); every substantive residual was
  adjudicated by 2-of-3 agreement and recorded in an explicit patch list in the build script
  (hex 30's dropped "nourish the cow" sentence restored; hex 51/55 "topmost SIX"; OCR
  "cars"→"ears", "he"→"be", "tinder"→"under"; two unbalanced-paren digitization typos).
  Hexagrams 1, 2, 11, 12, 63, 64 were additionally hand-read against the sacred-texts scrape.
  Per-item `metadata.confidence` + `_source` per the family convention (astro's
  renaissance-lilly pattern).
- **Keys for the viewers**: ids `hex-1`…`hex-64`, `metadata.number`, `metadata.binary` copied
  from `scripts/hexagram-binary.json` (the canonical table — NOT re-derived), Chinese name +
  pinyin copied from `i-ching-chinese-original`.
- **Wiring**: registered in `scripts/build_collection.py` (primary-sources, years −825/−250,
  labels citing Shaughnessy's dating and Legge 1882), `_collection.json` regenerated (6
  grammars, 372 items). `viewers/source-text.html` now stacks **five** labeled layers in
  stratigraphic order: Chinese original → Zhouyi core (oldest) → Ten Wings Great Image
  (Confucian addition) → this site's English reading → cross-lens. `python3 check.py` passes
  (6 grammars); Playwright at 390×844 verified hex 1/30/64 render all five layers with no page
  errors (only pre-existing external-resource blocks: Google Fonts + the recursive.eco
  assistant launcher, both proxy-blocked locally).
- **Scoped out**: full Tuan/Xiaoxiang/Xici/Wenyan text (a book, not a grammar item set); the
  contemplative-daoist lens (builder-authored, per the plan); the course (§3); Supabase/ids.json
  publish-loop rows (orchestrator's job).

## July 9, 2026 — Source Text: the classical Chinese, rendered directly (`viewers/source-text.html`)

Builder's ask: *"there is a bunch of iching seeds maybe the books itself in schemas seeds I
think. the Chinese version for sure. can we render direct public domain books?"* Answer: yes —
brought the Chinese-original grammar from `recursive.eco-schemas/iching/` into this repo
properly and built a dedicated reader for it.

- **Public-domain verification, done before import, not assumed.** The grammar's own
  description pointed at Project Gutenberg ebook #25501. `WebFetch`/direct `curl` against
  `gutenberg.org` were blocked by this sandbox's proxy (403, same class of block hit earlier
  by Wikipedia during the Path Caster work) — verification instead used `WebSearch`, which
  independently returned Gutenberg's own catalogue title for #25501: **"易經 by Anonymous |
  Project Gutenberg"** — i.e. the plain classical Chinese *Yijing* text, catalogued with no
  translator (unlike, say, Legge's 1882 "The Yî King," which Gutenberg lists as its own
  separate translated edition). Project Gutenberg's entire hosting model is "public domain
  confirmed in the US, or nothing" — they do not host anything else — so an anonymous-author,
  untranslated classical Chinese catalogue entry is about as clean a public-domain source as
  exists. Cross-checked against multiple independent search results (Gutenberg's Chinese-
  language browse page, other anonymous/unknown-author classical Chinese texts on Gutenberg
  with the same "Anonymous"/"Unknown" attribution pattern) — nothing contradicted the PD
  reading, so the import proceeded.
- **What "with brief translation" in the source repo's own folder name actually meant** (worth
  recording since it reads ambiguously): inspecting the grammar's items showed the `sections`
  (Judgment/Image/Line 1–6) are **100% untouched classical Chinese** — no embedded English
  anywhere in the body text. The only added-by-AI content is the one-to-three-word English
  hexagram `name` (e.g. "The Creative") — a **title gloss**, not a translation of the passage.
  The honesty chrome on the new page says this explicitly so nobody mistakes it for a
  scholarly translation (Wilhelm/Baynes, Legge, or otherwise).
- **Binary table cross-check.** The Path Caster work (Jul 8) found 5 real bugs in
  `i-ching-summarized`'s own `metadata.binary` field (hexagrams 15, 16, 46, 63, 64). Before
  trusting this new grammar's binaries, all 64 were diffed against the corrected, independently
  verified `scripts/hexagram-binary.json` — **zero mismatches**. This source didn't carry the
  same bug.
- **`grammars/i-ching-chinese-original/grammar.json`** (new, 64 items) — cleaned to match this
  repo's established item shape (id/name/symbol/category/sort_order/sections/keywords/metadata,
  same fields `i-ching-summarized` uses), with a `_grammar_commons` block spelling out the
  license/attribution chain (Gutenberg ebook #25501 for the Chinese; PlayfulProcess/Claude Code,
  CC-BY-SA-4.0, for the one-line name gloss only). Registered in `scripts/build_collection.py`
  (branch `primary-sources`, same era label as `i-ching-summarized`) and `_collection.json`
  regenerated — 4 grammars total now (`recursive-eco.json`'s exclude-note count updated to
  match). The sibling schemas-repo file `i-ching-hd-meta-categories-...-copy/grammar.json` was
  checked and found to be a 93/94-item **subset duplicate** of this repo's own
  `three-lenses-64` (identical description, near-identical items) — correctly **not** ported,
  per the brief's own instruction not to duplicate.
- **`check.py`** (new, repo root) — this repo had no grammar validator of its own; every other
  active family repo does (`recursive-astrology/check.py`, `recursive-tarot/scripts/check_all.py`).
  Ported astro's minimal gate (JSON parses, required top-level fields, `grammar_type` in the
  known set, every item has id/name/sections, `composite_of` refs resolve, no stray
  `metadata.video_id`). All 4 grammars in this repo pass.
- **`viewers/source-text.html`** (new) — a single-hexagram reader, mobile-first, that stacks
  **three separate, clearly-labeled layers** for whichever hexagram is selected: (1) *Original
  Chinese · Project Gutenberg, public domain* — the raw source sections, set in a CJK-capable
  serif stack; (2) *This site's English reading · i-ching-summarized* — the existing flagship
  condensation, sections in the same order; (3) *Cross-lens reading · Three Lenses* — the
  Human Design/zodiac/chakra keywords for that hexagram, where one exists. Prev/Next + a
  64-hexagram `<select>` for navigation, `?hex=N` deep-linking (`history.replaceState`, no
  reload). An honesty box up top states the Gutenberg/PD provenance, the AI-gloss-not-translation
  caveat, and links directly to the ebook page — matching the family's honesty-chrome
  convention (the Path Caster's "a casting, not a prediction" kicker is the same move applied
  to a different risk: mistaking a title gloss for a scholarly translation).
- **Wired in beside the ported set**: `site-header.js`'s Views dropdown gained a "Source Text"
  entry (in the same "By grammar" group as Cards/Explorer/Lenses/Tree — this reads one grammar
  closely, same as those, just cross-referenced against two others); `index.html`'s gallery
  gained a matching card. `site-header.js?v=` bumped 45→46 across every page that includes it
  (cache-bust for the changed dropdown contents).
- **Verified with Playwright at 390×844** (headless Chromium, installed fresh in-session —
  this repo has no browser-automation harness yet, so the browser + CJK font check was done
  ad hoc rather than against a checked-in test): hexagram 1's Chinese Judgment rendered as
  `元，亨，利，貞。` (byte-correct, not mojibake — confirmed via `WenQuanYi Zen Hei`, the
  system's installed CJK font, since no CJK webfont is loaded); all 3 layers rendered; the
  honesty box's Gutenberg link and AI-gloss language were present in the DOM; `?hex=15` deep-link
  landed on the correct hexagram (Modesty, matching the verified binary table) with correct
  Chinese text; Prev/Next navigation worked; the `index.html` card and `site-header.js` dropdown
  both linked correctly; zero console errors traceable to this page's own code (the only
  failures were this sandbox's proxy blocking `fonts.googleapis.com` and
  `recursive.eco/js/assistant-launcher.js` — pre-existing, unrelated to this change, and a
  harmless `/favicon.ico` 404 present repo-wide).

## July 8, 2026 — The Path Caster: the site's own instrument (`viewers/caster.html`)

Built per `docs/DESIGN-path-caster.md` (the builder's design) — the I Ching site's
site-specific instrument, analogue of astro's chart wheel and tarot's Spread Caster.
Three modes, all sharing one pure-logic engine:

- **Explore** — cast or pick an origin + destiny hexagram, tap any of the 6 lines on
  the current hexagram to flip it (any line, not just a differing one — a detour is
  allowed, loops are legitimate per the design doc's own correction). The stack grows
  one hexagram per tap; Undo pops it; a distance-remaining counter tracks progress;
  reaching the destiny completes the path.
- **Cast the Path** — one tap casts a full path at a chosen step budget. Intermediate
  steps flip a differing line (direct style) or any line with a bias toward closing
  (wandering style); the final step always flips whatever single line still differs,
  guaranteeing arrival.
- **Sequential Caster** — the same casting, revealed one step at a time (tap Next, or
  auto-advance every 2.2s).

Every hexagram in the stack renders through `grammars/i-ching-summarized/grammar.json`
(Judgment, Image, all six line texts, symbol/pinyin/Chinese name) with
`grammars/three-lenses-64/grammar.json` layered in as a secondary "also read as" voice
(Human Design gate name + keywords) where its name differs from the flagship's. Each
transition shows the changing line's text from the **origin side** of that specific
step — what the tradition says a changing line means. "Save this path" downloads the
journey as a sequence grammar JSON (items = the path's hexagrams in order, metadata =
the flipped line per step) — static-site style, no backend. Honesty chrome throughout:
a "casting, not a prediction" kicker + an explicit synthesis note that one transition
is classical, the multi-step journey is this project's own extension.

- **The load-bearing fix: the King Wen ↔ binary table.** The design doc flagged this as
  the one risk to get right — and it was right to. `grammars/i-ching-summarized/grammar.json`'s
  own `metadata.binary` field turned out to have **5 real bugs** (hexagrams 15, 16, 46,
  63, 64 — the 63/64 binaries were literally swapped with each other), caught by
  cross-checking that field against the same grammar's own `metadata.trigram_above`/
  `trigram_below` fields using the standard trigram-to-3-bit mapping (confirmed via
  WebSearch against general I Ching reference material: Qian/Kun/Zhen/Kan/Gen/Xun/Li/Dui
  = 111/000/100/010/001/011/101/110, bottom-to-top). Rather than patch the buggy field,
  **`scripts/hexagram-binary.json`** was built fresh by recomputing binary from the
  (independently verified) trigram fields for all 64 hexagrams — verified as a full
  bijection onto 0–63, cross-referenced by name+binary against the independent
  `adamblvck/iching-wilhelm-dataset` (GitHub) for hexagrams 1–15 (13/15 binaries matched
  directly, the 2 exceptions being exactly the two already-flagged-buggy entries), and
  landmark-checked per the design doc's own request (hexagram 1 = six yang, hexagram 2 =
  six yin, hexagrams 11/12 are exact bitwise complements). Full method and sources are
  documented in the file's own `_meta` block. Wikipedia's King Wen sequence article was
  unreachable (403 from this sandbox) — the verification route above was used instead.
- **`viewers/caster-engine.js`** — the pure hypercube math (Hamming distance, line-flip,
  path generation, coin/yarrow line-casting), shared between the browser page and
  `scripts/determinism-check.js` (no DOM dependency, so the hardest logic isn't
  duplicated or drifting between a browser copy and a test copy).
- **Determinism proof** (design doc's own §Verify requirement): `scripts/determinism-check.js`
  runs 50 random origin/destiny/step-budget/style trials and asserts the final hexagram
  always equals the chosen destiny with every intermediate step a single-line flip —
  passed 50/50, plus a separate explicit check of the d=0 (origin equals destiny, a pure
  "loop" journey) edge case at budgets 0/2/4/6.
- **Wired in beside the ported set** (never replacing it): `site-header.js`'s Views menu
  gained an "Instrument" section (Path Caster), `index.html`'s gallery gained a card, and
  `viewers/tree-viewer.html`'s "Get a Reading" button — hidden since the initial port
  because no local casting instrument existed yet (`docs/PLAYBOOK-FIELD-REPORT.md` §7) —
  now points at `caster.html` instead of staying hidden.
- **Verified with Playwright** at 390×844 and 1280×900 against a local static server:
  cast completes and lands on the chosen destiny in all three modes, Explore's flip/undo
  cycle, Sequential's step-by-step advance, the header/index/tree-viewer wiring, the
  "Save this path" download, and zero page errors throughout (the external assistant
  widget's script load fails in this offline sandbox, as expected — not a page error).

## July 7, 2026 — Site built from scratch, following `recursive-tarot/docs/REPLICATE-THE-PATTERN.md`

This is the third site in the family (tarot → astrology → I Ching), and the first one
built as a deliberate **test of the playbook itself**: follow the doc as the only
process authority, change nothing it doesn't call for, and write down everywhere it was
ambiguous or wrong. Full account in `docs/PLAYBOOK-FIELD-REPORT.md`.

- **Wiped the old scaffold.** This repo previously held an unrelated Next.js auth
  starter app; everything except `.git` was deleted per the builder's instruction and
  rebuilt as a static site, mirroring `recursive-tarot`'s and `recursive-astrology`'s
  shape (root-level `index.html`, `viewers/`, `pages/`, `grammars/`, `scripts/`,
  `course/`).
- **Content lifted, not authored.** Three grammars, all sourced from
  `recursive.eco-schemas` with only mechanical conversion (never hand-written
  interpretation):
  - `grammars/i-ching-summarized/grammar.json` — the flagship: all 64 hexagrams
    (Judgment, Image, all six line texts, a short interpretation gloss), converted
    from `recursive.eco-schemas/iching/iching-hexagrams.json` (a non-canonical
    `hexagrams[]` shape) into the canonical `items[]`/`sections{}` shape, with
    `symbol` (the unicode hexagram glyph) merged in by hexagram number from
    `iching/i-ching-chinese-original-with-brief-translation/grammar.json`. Flagged
    honestly in its own `_grammar_commons.license`: the source file carried zero
    attribution metadata, so the translation lineage reads as Wilhelm/Baynes-adjacent
    but is unverified.
  - `grammars/repair-iching/grammar.json` — copied verbatim from
    `recursive.eco-schemas/grammars/repair-iching/` (14 hexagrams read as a
    contemplative repair practice, real content, no changes needed).
  - `grammars/three-lenses-64/grammar.json` — renamed from
    `i-ching-hd-meta-categories-three-lenses-for-viewing-the-64-hexagrams-my-version`
    per the brief. One real fix applied: `grammar_type` was `"tarot"` in the source
    (copy-paste residue on a 94-item hexagram/sign/chakra/trigram grammar with zero
    tarot structure) — corrected to `"custom"`. **Not fixed** (see field report): all
    94 items have empty `sections` and `level: 1` regardless of their intended
    hexagram/sign/chakra/trigram/meta-category tier — the source grammar is a naming
    skeleton, not populated content. Lifted as-is per the "don't author content"
    constraint.
  - `scripts/build_collection.py` (ported from `recursive-astrology`'s script of the
    same name) generates `grammars/_collection.json` — 3 grammars, 3 branches
    (primary-sources / synthesis / readings — no `castings` branch, this repo has no
    spread-grammars).
- **Chrome ported from the family**, cinnabar-retoned (`#9c3b2a` / `#7a2d20` per the
  brief) instead of tarot's gold or astro's blue: `site-header.js`, `site-footer.js`,
  `theme.css`, `view-switcher.js`, `icons.js`, `assistant.js`. `viewers/cards.html` and
  `viewers/tree-viewer.html` are copied byte-identical in structure from
  `recursive-astrology` (which itself carried them byte-identical from
  `recursive-tarot` — both are already grammar-type-generic, confirmed by diffing all
  three repos' copies before editing). `viewers/explorer.html` and
  `viewers/timeline.html` are based on astro's already-de-tarot-ified versions
  (BRANCH_COLOR trimmed to this repo's 3 branches). `viewers/lenses.html` — see the
  field report for why this one needed a real logic fix, not just a re-skin: its
  cross-grammar entity-matching key (astro matched by normalized item NAME) doesn't
  transfer to I Ching, so `entityKey()` now prefers `metadata.number` /
  `metadata.hexagram_number` (the two different field names the two hexagram-bearing
  grammars happen to use) and falls back to name only for the non-hexagram lens items.
- **Two known-missing links found and removed** rather than left pointing at 404s:
  `viewers/cards.html`'s lens-menu "View as Genealogy" option and
  `viewers/tree-viewer.html`'s "Get a Reading" button both pointed at pages this repo
  doesn't ship (`genealogy.html`, `caster.html` — no deck-lineage content and no local
  casting instrument exist for a 3-grammar I Ching collection). `view-switcher.js`'s
  dead `?lens=genealogy` deep-link target was removed for the same reason.
- **Course**: `pages/course-viewer.html` copied from
  `recursive-astrology/pages/course-viewer.html` (the multi-course, manifest-driven
  pattern) per the brief, re-pointed to a single course. `course/three-lenses.manifest.json`
  reads its chapters live from `grammars/three-lenses-64/grammar.json`:
  `chapterIdPrefix: "hex-"` (the 64 hexagram-gate items) as the main throughline,
  `appendixIdPrefix: "l3-"` (the 3 meta-category syntheses) as the closing appendix.
  The `sign-*` / `chakra-*` / `trigram-*` items (27 of the 94) are deliberately not
  surfaced as chapters or appendix — a course needs one throughline, and those items
  don't have one; an honest omission, not a hidden fallback. **Because the source
  grammar's items have empty `sections`, every chapter body currently renders empty**
  (title + keywords only) — flagged in-page and in the field report, not silently
  shipped.
- **`recursive-eco.json` + `ids.json`** written to the pattern (channel slug
  `iching`, `grammars.paths: ["grammars/*/grammar.json"]`, `id_map: "ids.json"`).
  `ids.json` is an intentional skeleton (`{"ids":{}, "_public_now":[]}`) — none of
  these three grammars have been imported into recursive.eco yet; publishing is a
  separate step the playbook itself calls out as part of "the eco binding," not
  something this session did.
- **`.github/workflows/build-collection.yml`** added (this repo had no GitHub Actions
  before): rebuilds `grammars/_collection.json` and deploys to Pages on push to
  `main`. Not verified against the actual push branch — this session could not run
  `git` (write-files-only constraint) — flagged in the workflow file's own comment.
- **Verified with Playwright** (chromium, local static server, 390px and 1280px):
  every page returns 200 with zero same-origin 404s; the header dropdown gap-hover fix
  (inherited via astro from tarot's commit 84934e6) survives the cursor actually
  crossing the gap; the homepage's dynamic grammar/course galleries and the header's
  live Grammars menu all populate correctly from `grammars/_collection.json`; the
  course TOC renders all 64 hexagram chapters plus the 3-item appendix. Google Fonts,
  recursive.eco, and Wikimedia Commons images all fail to load in this sandbox
  (`ERR_TUNNEL_CONNECTION_FAILED` / `ERR_CONNECTION_RESET`), same as both sibling
  repos' own verification notes — a sandbox network restriction, not a new bug; needs
  a real network (GitHub Pages or an unblocked preview) to confirm the fully-dressed
  visual pass. `viewers/timeline.html`'s d3-driven chart is one casualty of that same
  block (`d3 is not defined`, CDN unreachable) — page chrome around it still renders.
- **No `research/` dossiers, no `caster`/coin-cast instrument** — out of scope for this
  session; the brief asked for the ported mechanisms + lifted content + one course, not
  new research writing or a new site-specific instrument.
