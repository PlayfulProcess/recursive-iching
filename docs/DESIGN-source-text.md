# Design — Source Text: rendering the public-domain book directly

Builder's ask (Jul 2026), near-verbatim: *"there is a bunch of iching seeds maybe the books
itself in schemas seeds I think. the Chinese version for sure. can we render direct public
domain books?"*

## What was found

`recursive.eco-schemas/iching/` (a shared grammar-seed staging area for the whole recursive.eco
family, not this repo specifically) had two I Ching-adjacent grammars not yet in this repo:

1. `i-ching-chinese-original-with-brief-translation/grammar.json` — 64 items, each carrying the
   full **classical Chinese** for Judgment, Image, and all six Line statements, plus
   `metadata.pinyin` / `metadata.chinese_name` / `metadata.trigram_above` / `metadata.trigram_below`
   / `metadata.binary` / `metadata.number`. **This is the one that got built.**
2. `i-ching-hd-meta-categories-...-copy/grammar.json` — checked and found to be a 93/94-item
   subset duplicate of this repo's own `grammars/three-lenses-64/grammar.json` (identical
   description text, near-identical items, same source). **Not ported** — porting it would have
   duplicated content already live in this repo, which the brief itself flagged as the wrong move.

## Public-domain verification — method, not assumption

The grammar's own `description` field named a source: *"extracted from Project Gutenberg's
Archives. https://www.gutenberg.org/ebooks/25501."* That claim was checked, not taken on faith,
before anything was imported or rendered:

- **Direct fetch was blocked.** `WebFetch` against `gutenberg.org/ebooks/25501`,
  `gutenberg.org/cache/epub/25501/pg25501.txt`, `gutendex.com/books/25501`, and a `curl` through
  this sandbox's own proxy all returned `403`. This is a sandbox/proxy limitation, not a signal
  about the source — the same class of block hit `en.wikipedia.org` during the Path Caster work
  (`docs/DESIGN-path-caster.md`), while `github.com` etc. worked fine.
- **`WebSearch` supplied the missing confirmation.** Multiple independent queries
  (`"Project Gutenberg ebook 25501 I Ching"`, `"25501" gutenberg.org 易經 language Chinese
  copyright status public domain`) returned Gutenberg's own catalogue title verbatim:
  **"易經 by Anonymous | Project Gutenberg"** — i.e. Gutenberg's own metadata for #25501 is the
  plain classical Chinese *Yijing* (I Ching) text, author field "Anonymous" (there is no
  named translator, because there is no translation — it's the Chinese source itself). This is
  distinct from, e.g., ebook #3100 ("The Chinese Classics... with a translation" — Legge's
  English editions, which Gutenberg catalogues and licenses separately).
- **Why "Anonymous + hosted on Gutenberg" is sufficient here.** Project Gutenberg's entire
  operating model is: confirm a work is public domain in the US, or don't host it — there is no
  middle tier. An anonymous-authorship classical Chinese text (compiled across the Zhou dynasty,
  ~1046–256 BCE, roughly 3,000 years old) hosted under that model, with no translator layer to
  introduce a second, more recent copyright, is about as unambiguous a public-domain case as
  exists. Nothing found during the search contradicted this reading.
- **Conclusion:** the Chinese source text is safely public domain. Verification is documented
  here and in the grammar's own `_grammar_commons.license` field so a future session doesn't
  have to redo it — and so anyone auditing the grammar sees the reasoning, not just a claim.

## What "with brief translation" in the source folder name actually meant

Read literally, the folder name suggests each hexagram carries a short English translation
alongside the Chinese. Inspecting the actual `sections` data showed otherwise: **every section
(Judgment, Image, Line 1–6) is untouched classical Chinese, with zero embedded English.** The
only AI-added content anywhere in the file is the one-to-three-word English `name` field per
item (e.g. `"The Creative"` for hexagram 1) — a short **title gloss**, not a translation of the
passage. The description was updated accordingly, and the page's honesty chrome says this
explicitly, so nobody mistakes the gloss for a scholarly translation (Wilhelm/Baynes, Legge, or
otherwise) — the same "don't invent, hedge honestly" discipline `docs/PLAN-iching-channel.md`
and `index.html`'s own story section already apply to `i-ching-summarized`'s undocumented
translation lineage.

## Binary table cross-check

The Path Caster session (`docs/DESIGN-path-caster.md`, Jul 8 2026) found and fixed 5 real bugs
in `i-ching-summarized`'s own `metadata.binary` field (hexagrams 15, 16, 46, 63, 64 — 63/64 were
swapped). Before trusting this new grammar's binaries for anything (including any future
cross-linking with the Path Caster), all 64 were diffed programmatically against
`scripts/hexagram-binary.json` (the corrected, independently-verified table). **Zero
mismatches.** This source's binary field is clean; no fix was needed.

## What was built

1. **`grammars/i-ching-chinese-original/grammar.json`** — the verified grammar, cleaned to this
   repo's established item shape (matching `i-ching-summarized`: id/name/symbol/category/
   sort_order/sections/keywords/metadata — dropped the source's noisier per-item `origin`/
   `level`/`subcategory`/per-item `grammar_type` fields, which check.py doesn't require and
   this repo's cleaner grammars don't carry). `_grammar_commons.license` spells out the full
   attribution chain. `grammar_type: "iching"` (a valid, thematically correct type per
   `check.py`'s `VALID_TYPES`).
2. **`check.py`** (new, repo root) — this repo had no grammar validator; every other active
   family repo does (`recursive-astrology/check.py`, `recursive-tarot/scripts/check_all.py`).
   Ported astro's version verbatim (same minimal gate: required top-level fields, valid
   `grammar_type`, every item has id/name/sections, `composite_of` refs resolve, no stray
   `metadata.video_id`). All 4 grammars in this repo now pass `python3 check.py`.
3. **`scripts/build_collection.py`** — registered the new slug in `BRANCH_OF` (primary-sources)
   and `YEARS` (same era as `i-ching-summarized`, distinct label), then regenerated
   `grammars/_collection.json`. `recursive-eco.json`'s exclude-note grammar count (three → four)
   updated to match.
4. **`viewers/source-text.html`** (new) — the direct answer to "can we render direct public
   domain books": pick a hexagram, see three separately-labeled layers stacked underneath —
   the classical Chinese (this page's whole point), this site's existing English condensation,
   and the Three Lenses cross-read where it exists. Prev/Next + a 64-entry `<select>`,
   `?hex=N` deep-linking via `history.replaceState`. Mobile-first (390px target), `theme.css`
   tokens only — no new color literals. An honesty box states the Gutenberg/PD provenance and
   the "gloss, not translation" caveat up top, with a direct link to the ebook page, following
   the same honesty-chrome convention as the Path Caster's "a casting, not a prediction" kicker.
5. **Wiring** — `site-header.js`'s Views dropdown gained a "Source Text" entry (in the "By
   grammar" group, alongside Cards/Explorer/Lenses/Tree — it reads one grammar closely, cross-
   referenced against two others, same category as those rather than the Instrument group the
   Path Caster used). `index.html`'s gallery gained a matching card. `site-header.js?v=`
   bumped 45→46 across every including page (cache-bust).

## Verify

Playwright wasn't previously set up in this repo, so headless Chromium was installed fresh
in-session (`npx playwright install chromium`) rather than relying on a checked-in harness —
worth a future session's time to formalize if visual verification becomes routine here. Checked
at 390×844:

- Hexagram 1's Chinese Judgment rendered as `元，亨，利，貞。` — byte-correct, not mojibake.
  No CJK webfont is loaded (the CSS font stack falls back to the system's installed
  `WenQuanYi Zen Hei`), so this also confirms the fallback chain works without adding a new
  font dependency.
- All 3 layers rendered for hexagram 1 (Chinese has all 8 sections; English condensation +
  Interpretation; cross-lens keywords).
- The honesty box's Gutenberg link and "AI-generated" gloss language were present in the DOM.
- `?hex=15` deep-link landed on hexagram 15 (Modesty · 謙 · Qiān) with correct Chinese text —
  spot-checked because 15 was one of the five previously-buggy binaries, confirming the
  verified table (not the buggy field) is what's actually driving lookups here (via the
  grammar's own already-correct `metadata.binary`, cross-checked earlier against the same
  table — this page doesn't use `hexagram-binary.json` directly, it keys by `metadata.number`).
- Prev/Next navigation advanced correctly (hex 1 → hex 2).
- `index.html`'s new card navigates to `viewers/source-text.html`; `site-header.js`'s shadow
  DOM contains the `source-text.html` link.
- Zero console errors traceable to this page's own code. The only failures seen were this
  sandbox's proxy blocking `fonts.googleapis.com` and `recursive.eco/js/assistant-launcher.js`
  (pre-existing, unrelated — every page in this repo hits the same two blocks in this sandbox)
  and a harmless `/favicon.ico` 404 (no favicon exists anywhere in this repo yet).

## Left out of scope

- No favicon anywhere in the repo (pre-existing, not part of this task).
- `eco-links.js` (Cast/View/Edit buttons keyed off `ids.json`) was not wired into this page —
  `ids.json` is still the empty skeleton noted in `docs/PLAYBOOK-FIELD-REPORT.md` /
  `docs/PLAN-iching-channel.md` (no grammar in this repo has been published to recursive.eco
  yet), so the links would render nothing. Natural follow-up once channel activation
  (`docs/PLAN-iching-channel.md` §4) happens.
- A checked-in Playwright test harness — verification this session was ad hoc (a one-off script
  against a temporary static server), not a reusable test file. Worth adding if this repo starts
  shipping enough interactive viewers that regressions become likely.
