# Changelog — The Recursive I Ching

## October 7, 2026 (later) — no node for the grammar itself; no empty sections or "9999" labels

PlayfulProcess: "I think the Tree of the Changes in the middle of the thing is disconnected and
irrelevant? Search for other patterns like that to clean up."

- **One rule, in `viewers/dimension-engine.js`: `grammarRootId(items)`.** It finds the item that
  stands for the grammar itself: the only group nothing contains, which reaches every other item
  and has groups under it. Here that is "The Tree of the Changes" (over its eight branches) and
  "The Repair I Ching" (over "Repair as Change" and the twelve hexagrams). No grammar file changed.
- **Genealogy:** that node and its eight spokes are gone from the middle; the eight branches stand
  on their own. The grammar's name is now the page heading, with an "About this tree" button that
  opens the tree's own text in the side panel (open on load at 1440 px and wider) and a "Start
  with the oldest book" step. Names too long for the ring end on a whole word and "…" instead of
  mid-word; the full name is in the tooltip. On a phone the hint that ran under the two buttons
  is hidden.
- **Tree view:** no "Level 3 (1)" row holding the grammar alone; the counts no longer include it
  (the Tree of the Changes: 41 items, 2 levels).
- **Cards sidebar:** starts at the branches instead of one collapsed line named after the grammar.
- **Explorer "emergence" field:** no longer has a group named after the grammar (9 values became
  8 for the Tree; the Repair I Ching's two groups held the same twelve hexagrams).
- **Lenses, provenance ribbon:** undated grammars were placed at year 9999, so 3,000 dated years
  sat in the left tenth and three labels read "9999"; they now share a zone at the right edge
  labelled "undated", and years before 0 read "1000 BCE", not "-1000".
- **The I Ching — All Lenses (meta):** 52 hexagrams had an empty "Wound" section (the Repair I
  Ching reads twelve); `scripts/build_meta_iching.py` now leaves out a lens with nothing to say.
- `dimension-engine.js?v=2` in every viewer that loads it.

## October 7, 2026 — every grammar card has a picture; short rows sit in the middle

PlayfulProcess: "Only thing I don't like about the I Ching is things without thumbnails or not
centralized when there is too few."

- **A drawn mark for every grammar** (`img/covers/<slug>.svg`, by `scripts/build_covers.py`, which
  `scripts/build_collection.py` now runs): the site's ensō in seal red on paper, with the
  grammar's first hexagram inside it in ink and its King Wen number on a small seal at the lower
  right. The I Ching — All Lenses gets the eight trigrams instead; the Tree of the Changes gets
  one whole line and one broken line. Edit the script, not the SVGs.
- **`_collection.json` gains `thumb` and `mark`.** `thumb` is the grammar's own cover when it has
  one, otherwise its mark. Two covers were Commons *file pages* (`/wiki/File:…`, an HTML page, not
  an image), so HD Meta-Categories and Three Lenses showed an empty card; `thumb` turns those into
  the image link for the same Leibniz diagram. Commons links get `?width=400`, so a card no longer
  loads a full-size scan. The grammar files' own `cover_image_url` is unchanged.
- **Home page, "Every grammar in this repo":** each card shows its `thumb`; if that link ever
  breaks, the card switches to the grammar's mark. Photos shot on white take the paper's tone.
  Paintings stay contained, never cropped.
- **The broken Hokusai:** its Commons link 404ed (no such file), leaving the Repair I Ching card
  and the "Mirror, not fate" node blank. Both now show the Repair I Ching's mark.
- **Centred rows:** the three ways in, every row of views, the course card and the grammar rows
  wrap and centre, so a row with one or two cards sits in the middle at every width. At 375 px
  nothing scrolls sideways.
- **Not changed:** the viewers under `viewers/`, and every grammar file.

## October 6, 2026 (later) — a zen look: the seal-red spiral, ink and paper, public-domain zen art

PlayfulProcess: "Maybe the recursive logo in i ching can have the iching colors? also, can we make
the whole theme of the iching a bit more like zen art? maybe even render PD zen art?" And: "I hate
how the assistant is rendering in a black square."

- **The spiral as a seal:** `img/recursive-logo-seal.svg` is recursive.eco's spiral, its path
  unchanged, cut out of a seal-red block like the lines of a hanko. It is the header mark (30 px)
  and the home page's "One branch of a larger tree" mark (44 px), and still links to
  https://recursive.eco/. `scripts/build_zen_marks.py` builds it from `img/recursive-logo.svg`,
  and also draws `img/enso.svg`; edit the script, not the SVGs.
- **Ink and paper (`theme.css`):**
  - rice-paper ground `#f3efe6`, paper-toned sheets instead of white, warm sumi ink `#1c1a17`;
  - seal red `#9c3b2a` is still the one accent, now also named `--seal`;
  - hairline rules, flatter shadows, smaller corners;
  - `.ink-rule` (a hairline that darkens to an ink wash at its centre), `.enso` (a drawn ensō,
    coloured by the theme) and `.zen-art` (a painting on a mat, contained, captioned).
  - Titles are set in Shippori Mincho; reading text stays in Fraunces. Light-only, as before.
  - The header and footer take their colours from the tokens instead of their own hex values.
- **Public-domain zen art** (`img/zen/`, five works, all on Wikimedia Commons; sources and licence
  templates in `NOTICE`, `img/zen/credits.json`, and "The paintings" at the foot of the home page):
  - home page: Hasegawa Tōhaku's *Pine Trees* (right-hand screen) opens it, and Hakuin's *Portrait
    of Daruma* hangs beside "A mirror, never a command";
  - courses, on the first chapter: Sengai's *Circle, Triangle, Square* for Three Lenses, Mu Qi's
    *Six Persimmons* for the translations, Sesshū's 1495 splashed-ink landscape, with all the
    inscriptions above it, for the Books of the Changes.
  - Every image is the whole work as Commons has it, inscriptions and seals included, reduced to
    at most 1600 px wide and 190 KB.
- **The black square:** the assistant launcher guesses a page's theme; this site's page background
  was transparent, so on a dark-mode computer it guessed "dark" and drew a dark box behind the
  button. `assistant.js` now passes `theme: 'light'`, and `theme.css` paints `html` and `body` with
  the paper.
- **`recursive-eco.json` has a `shell` block** (name, home, colours, font) in the same look, for
  recursive.eco's framed previews. No logo and no menu yet.
- **Not changed:** the viewers under `viewers/` (they take the new tokens, untouched otherwise) and
  every grammar.
- **Not verified:** Sengai's file on Commons carries `{{PD-Japan}}`, not PD-Art, and names no
  collection; "Idemitsu Museum of Arts" in its caption was not checked against the museum. The home
  page's Hokusai thumbnail (a Commons link from before this change) returns 404 and still does.

## October 6, 2026 — ready to connect: the open decisions taken

PlayfulProcess: "For I Ching, do what you think is best." Decisions and reasons are in
`docs/BEFORE-CONNECTING-TO-RECURSIVE-ECO.md`, "Decisions, Oct 6 2026".

- **`ids.json` filled:** `zhouyi-core` → `6efa4fc7` (Legge), `i-ching-chinese-original` →
  `476b17da`, `i-ching-summarized` → `b5161d12`, `iching-hd-meta-categories` → `ad36491a`,
  `repair-iching` → `b7a59594`. `ten-wings` and `tree-of-the-iching` are created new on import.
- **Skipped by the importer:** `meta-iching` and `the-recursive-iching-book` now carry
  `_generated: true` (from their builders); `three-lenses-64` carries `_source_of_truth: "repo"`
  until it is retired.
- **`zhouyi-core` ids are now `hexagram-N`**, the app's, so the import pairs all 64 items instead of
  duplicating 31 whose names differ.
- **King Wen numbers:** every hexagram item carries `"number"` at the top level too (finding V-1);
  `check.py` enforces it.
- **The spiral, not the moon** (her word, Oct 6): the header's mark is now recursive.eco's spiral
  (`img/recursive-logo.svg`, copied from recursive-eco `apps/landing/recursive-logo.svg`) and links
  to https://recursive.eco/; the name beside it still links to this site's home. The home page's
  "One branch of a larger tree" mark changed the same way.
- **`CLAUDE.md` added:** this repo keeps no viewer copies (Oct 5 architecture), plus the build order.
- **Not changed in the app:** nothing. Ten Wings `a172fed6` stays private (Chinese only, its
  transcription source unnamed, hexagrams 12 and 32 incomplete).
- **Not verified:** `scripts/check_book_mode.py` (Playwright isn't installed on this machine). The
  Source Text viewer and the Path Caster were opened locally and load without errors.

## Merged October 5, 2026 — what is new, and what was not thoroughly verified

PlayfulProcess merged the cloud session's work (Oct 1–4) and the Desktop check of Oct 5. New, and
not thoroughly verified:

- **The Tree of the Changes** (`grammars/tree-of-the-iching`): 33 books written with AI. 45 claims
  are still ◇ (from memory, unchecked) and 9 are ◆ (sources disagree). The marks on each claim say
  which is which; the timeline and the genealogy show the same marks.
- **The two history courses** are written with AI from that grammar, so they carry the same doubts.
- **The genealogy's edges** are the page's own simplification, not a historian's.
- **`viewers/dialogue.html`** is an unlisted prototype, not tested with readers.
- **`docs/DECIDE-books-and-grammars.md`** lists decisions that are still open.

## October 5, 2026 — The Tree of the Changes: the ◇ claims checked, low-confidence books first

The handover's first Desktop job. Sources a Desktop session could reach: the scan of the 1834 Latin
edition, a Stanford catalogue record, and English, Chinese and German Wikipedia, each cited by revision.
Smith (2008) and Shaughnessy (2014) were not opened; what only they could settle stays ◇.

- **Counts (claims in the sections):** ◇ 57 → 45; ✔ 48 → 78; ◆ 3 → 9; ○ 0 → 3. Guicang, Jing Fang and
  the excavated-texts translations are no longer `low`.
- **Corrections:**
  - the Tsinghua Shifa was published in January 2014 (volume 4), not 2013;
  - Wilhelm finished his translation in Beijing, and translated from the Kangxi-era *Zhouyi zhezhong*;
  - the Jing Fang node had said Wikipedia "gives no dates"; its lead gives 78–37 BC.
- **Now contested (◆), with both sources:**
  - Jing Fang's dates (77 or 78 BCE);
  - whether the eight palaces are his (one study credits another school);
  - Wilhelm's year (1924 in German Wikipedia and the Diederichs title, 1923 in English Wikipedia);
  - the end year of the *Gushi bian* (1941 or 1944);
  - Shaughnessy's Mawangdui translation (1996 or 1997).
- **Régis:** the 1834 preface names the other hands: Joseph de Mailla (word for word, against the
  Manchu) and Pierre du Tartre (the historical explanation).
- **Still ◇:**
  - the years of Hu Wei's book (1706) and of the *Zhezhong* (1715), and whether Legge used it;
  - the Shifa's numbers;
  - McClatchie's keys and Legge's response;
  - whether Dick plotted by casting;
  - how Rutt and Redmond translate *zhen*.


## October 4, 2026 (later) — The Tree of the Changes: a history in books, a timeline, a genealogy, two courses

PlayfulProcess asked for the I Ching's history, the way tarot has a genealogy and a timeline,
"one book per node", with courses on the books and the translations.

- **`grammars/tree-of-the-iching`** (new) has 33 books, 8 branches and a root, in the shape of
  tarot's `tree-of-tarot`.
  - It runs from numbers on bone, through the Zhouyi, the Ten Wings and the Han canon, the
    commentators (images and numbers, meanings and principles, Daoist), and the tombs, to Régis,
    Legge, Wilhelm and Baynes.
  - Every node says what it is, **what it changed in the text**, and where each claim comes from
    (`[@key]` into a root `bibliography`, with a `marks` legend: ✔ ○ ◆ ◇).
  - Checked against Wikipedia (18 articles, cited by revision), the repo's own records and Legge's
    text. **57 claims are still ◇ (from memory)** and are listed for the next pass.
  - Nodes held in the library link to their grammar (`metadata.grammar_slug`).
- **`viewers/timeline.html`** is now recursive-tarot's current timeline (it had been the old copy
  that plotted grammars). It reads the tree.
  - Changed for this repo: BCE years from `metadata.year`, and a scale of 0.75 px per year, since
    the span is 3,000 years.
  - Lanes run in historical order, and each label stays inside its lane.
  - On a phone the rail scrolls sideways inside its box; the page never does.
  - Citations render as links.
- **`viewers/genealogy-tree.html`** (new) is tarot's radial genealogy over the same tree. Its
  menu entry is "Genealogy of the books".
- **Two courses**, read live from the tree through `pages/course-viewer.html`:
  - *The Books of the Changes*: all 33 books, oldest first, with an introduction on the four
    changes;
  - *How the Translators Changed the Text*: the translation and reception nodes, with an
    introduction on the three choices every translation makes, and the word zhen.
- **The course viewer** gained:
  - `chapterWhere` (filter chapters by metadata);
  - `[@key]` citations and paragraphs;
  - a `when` pill;
  - an intro on chapter 1;
  - an "Open this book in the library" link.

  Its chapter links now keep `?course=`; before, every link fell back to the default course.
- `build_collection.py` has a "History" branch for the tree.
- **`docs/DECIDE-books-and-grammars.md`** (new): the history applied to the open decisions
  (one book per node, languages as sections), which nodes could become books here (public domain),
  and what's left to check.
- Checked headless at 1280 and 375 px: the timeline, the genealogy, both courses and the home page
  load with no errors and no sideways page scroll. Detail panels open, citations link. `check.py`
  passes (10 grammars).

## October 4, 2026 — Ready to connect (mostly), and a prototype: reading as dialogue

**Connecting to recursive.eco** (`docs/BEFORE-CONNECTING-TO-RECURSIVE-ECO.md`, new "Findings" section):
- Each folder was compared with the app's grammars over the MCP (read-only) and a mapping
  proposed. Six decisions are left for PlayfulProcess; `ids.json` stays empty until she makes them.
- `ten-wings` does **not** match the private `a172fed6`: that one is a Chinese-only companion of
  `0f8f4088`, and mapping them would duplicate every item.
- The stale `recursive-starter` repo name is gone from the builder, the collection, the header,
  the footer, the home page, the tree viewer and the README. Header cache is now `?v=47`, footer
  `?v=2`.
- Every hexagram item carries `metadata.number`. 76 were missing it: 12 in `repair-iching`,
  64 in `three-lenses-64`.
- `viewers/cards.html` is now recursive-tarot's current viewer (Sep 26), with only paths, accent
  (`#9c3b2a`), branding and default grammar changed. `viewers/item-shape.js` (ported unchanged
  from recursive-eco c164d95) decides I Ching / tarot / plain from the data.
  `viewers/reference-resolve.js` is copied from tarot.
  - Checked headless at 1280 and 375 px on all nine grammars: they render with no errors, and
    the hexagram detail opens.
  - `three-lenses-64` now shows the plain theme, because its items carry no binary or trigrams.
- `check.py` passes again (it had 26 failures on main):
  - `build_meta_iching.py` now prefixes a copied group's `composite_of`;
  - `build_book_grammar.py` writes `grammar_type: "custom"` (`book` isn't a platform type).

**Reading as dialogue (prototype):** `docs/DESIGN-reading-as-dialogue.md` and
`viewers/dialogue.html`. Not in the menu yet.
- A real cast (coins in the page, or your own six numbers) is followed by passages offered in
  rings: the whole figure, the two trigrams, the moving lines, where it may be turning.
- You mark "This speaks to me" or "Not this", and the choices are the reading.
- It is kept in the browser, or downloaded as a selection of pointers (grammar, item, section).
- `caster-engine.js` gains `castLineNumber` / `castLines` (6–9); `castLineValue` and its odds are
  unchanged.
- Checked:
  - 160,000-draw counts match the coin (1/8, 3/8, 3/8, 1/8) and yarrow (1/16, 5/16, 7/16, 3/16)
    odds;
  - `determinism-check.js` passes;
  - a typed cast 8 7 9 8 6 7 gives 18 → 59 with lines 3 and 5 moving, which is correct;
  - headless at 1280 and 375 px.
- `docs/FOR-THE-PLATFORM.md` (new) lists what recursive.eco would need to make this a feature.

## September 23, 2026 — The 64 Hexagrams now carry Legge, not Wilhelm/Baynes

A third-party audit compared `i-ching-summarized` against the known translations. Its Judgment,
Image and Line texts were not "Wilhelm/Baynes-adjacent": they were the **Wilhelm/Baynes English
translation verbatim** ("Hidden dragon. Do not act."; "The Illustrious Ancestor disciplines the
Devil's Country"), about 800 sentences across all 64 hexagrams. That translation (Princeton
University Press, Bollingen Series XIX, © 1950, 1967, renewed 1977) is still in copyright in the
US and in Europe, so it could not sit in this repo under CC-BY-SA.

- **Replaced, not rewritten.** Every Judgment, Image and Line text is now James Legge's
  public-domain translation (1882/1899), copied verbatim from this repo's `zhouyi-core` (Judgment,
  Lines) and `ten-wings` (Great Image), which were already cross-verified against three
  digitizations. A script checked equality for all 64 hexagrams, and none of the old sentences
  remain. The Interpretation gloss, names, symbols and metadata are unchanged.
- **Derived grammars rebuilt:** `the-recursive-iching-book` (its Learn lines are the Image),
  `meta-iching` (it carries a copy of every source item) and `_collection.json`. The book's
  licence line and the collection label now name Legge.
- **`viewers/source-text.html`:** layer 4 would now repeat layers 2 and 3, so it shows only the
  site's own addition, the Interpretation gloss.
- **Still to decide (not changed here):** `iching-hd-meta-categories` opens many of its Judgment,
  Image and Line fields with Wilhelm/Baynes sentences or close paraphrases before its own gloss
  (248 verbatim sentences), and `meta-iching` copies them. That grammar is authored work, so it
  was left alone. The same Wilhelm/Baynes text is also in `recursive.eco-schemas`
  (`iching/iching-hexagrams.json` and `schemas/iching/`) and in the recursive.eco copy of this
  grammar. `repair-iching` quotes six short Wilhelm/Baynes lines with credit, which is quotation,
  not a copy of the text.

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


## 2026-09-05 — Book mode: a book you cast

- `viewers/caster.html`: fourth mode **Cast your Book**. Destiny fixed to Hexagram 1 (the Creative);
  the reader casts where they are, reads the fixed opening, advances one hexagram at a time (Learn +
  Story + the changing line), writes their own transition under each step (kept in localStorage per
  path), and at the end saves the walk as their own grammar (JSON) or downloads it as Markdown to
  print. No backend; nothing else in the page changed.
- `grammars/the-recursive-iching-book/`: the book as a grammar — `frame.json` (hand-written
  beginning and end), `stories/NN.md` (one chapter per hexagram, folded in when present),
  `grammar.json` built by `scripts/build_book_grammar.py`.
- Design: `book-repo/books/gautama-golden-dawn/outline/COMBINATORIAL-DESIGN.md`.
