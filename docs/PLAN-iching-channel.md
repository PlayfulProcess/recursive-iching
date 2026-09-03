# Plan — The Recursive I Ching becomes a real channel

Builder direction (Jul 2026), for the next session(s).

## Who this is for — a strategic correction
Not vibe coders. **Domain experts** — the person who knows the I Ching (or a deck, or a
tradition) and has content, not code. The playbook + this repo exist so a domain expert
brings knowledge and the mechanisms carry it. All docs, prompts, and the eventual "make
your own site" course speak to that reader. MCP/recursive.eco infrastructure help =
lowering *their* friction: the publish loop as clicks, the grammar shape as a fill-in
document, the AI as the one who runs terminals.

## 1. Content: lift everything that already exists
- Sweep BOTH sources for I Ching grammars: the recursive.eco app (user_documents — the
  canonical iching book the Journal oracle uses, plus any others) and
  recursive.eco-schemas (more grammars + **Python visualizers that are I Ching-specific
  — port `schemas/iching/` tooling into this repo's scripts/**, they only make sense here).
- Fill the empty three-lenses chapter sections from these sources where they overlap.

## 2. Grammars by the AGE of the one book (stratigraphy — the idiosyncratic structure)
No structure fits all; **the repo is where idiosyncrasies live**. The I Ching's own shape
is layers of one book across ~3000 years, so the grammars follow the strata, not a template:
- **zhouyi-core** — the oldest divination text (Western Zhou): hexagram + judgment + line
  statements, terse, oracular, pre-Confucian. (PD translations: Legge 1882; Wilhelm is NOT PD.)
- **ten-wings** — the Confucian commentarial layer (Great Commentary etc.) as its OWN grammar,
  so the reader can SEE the moralizing layer as an addition, not the origin.
- **contemplative-daoist reading** — Dao De Jing resonances + the contemplative stream, as an
  owned lens ("my reading, sourced"), per the nara charter.
- Contextual texts (Dao De Jing chapters etc.) as grammars **playable in the tarot oracle /
  as cards** — any public grammar ID loads in any oracle; the caller picks the rules. Draw a
  hexagram like a card; draw a DDJ chapter as a contemplation card.

**Built (Jul 9 2026): `grammars/zhouyi-core` + `grammars/ten-wings`.**
- **Source**: James Legge's public-domain translation (The Yî King, Sacred Books of the East
  vol. XVI, 1882/1899). Wilhelm was never touched. Direct fetches of sacred-texts.com and
  gutenberg.org are proxy-blocked from the sandbox, so the text came from **three independent
  digitizations of Legge fetched losslessly from GitHub raw** (pinned to commit SHAs):
  limjiechao/ts-hexagram-generator (structured, base), accelon/cct (bilingual, witness), a
  DS5001 course's raw scrape of sacred-texts.com ic01–64 (witness), plus rluu/iching's full
  mirror of sacred-texts.com/ich for Appendix II and the wing quotes (witness).
- **Verification**: automated word-by-word diff of ALL 64 hexagrams × (Judgment + 6 lines +
  Daxiang) across the mirrors — not just a sample. ~137 diff sites were all transliteration
  (Khien/Qian); the ~20 substantive residuals were adjudicated by 2-of-3 agreement and are
  recorded as an explicit patch list (e.g. hex 30's dropped cow sentence restored, hex 51/55
  "topmost SIX", OCR "cars"→"ears", "tinder"→"under", two unbalanced-paren typos). Hexagrams
  1, 2, 11, 12, 63, 64 additionally hand-read against the sacred-texts scrape. Per-item
  `confidence: high` + `_source` in metadata, per the family convention.
- **ten-wings scope**: the 64 Great Image (Daxiang) texts (Legge Appendix II) + 8 concept
  items (overview + one per Wing group, ✔/○ marked own-synthesis with verbatim Legge samples
  from Appendixes I–VII). Full Tuan/Xiaoxiang/Xici/Wenyan text was scoped OUT (that's a book,
  not a grammar). Dating claims verified via WebSearch Jul 2026: Wings c. 350–100 BCE,
  composite, not Confucius (doubted since Ouyang Xiu); Zhouyi core c. 9th century BCE
  (Shaughnessy), Rutt "Bronze Age document".
- **Wired**: both registered in `scripts/build_collection.py` (primary-sources branch, years
  −825 / −250), `_collection.json` regenerated, and `viewers/source-text.html` now stacks five
  labeled layers in stratigraphic order (Chinese original → Zhouyi core → Ten Wings Great
  Image → site English reading → cross-lens). Verified with Playwright at 390×844 (hex 1, 30,
  64: all layers render, no page errors). The contemplative-daoist lens grammar remains
  builder-authored (not built here); the course is §3, also not built here.

## 3. The course — "The History of the I Ching"
Anchored in Dao De Jing + contemplative Asian traditions. Thesis to research honestly (it is
historically defensible, with real scholarship — Shaughnessy, Rutt, Redmond & Hon): the Zhouyi
began as divination, arguably closer to a contemplative/oracular practice; the Confucian
canonization (Ten Wings, Han classicization) ADDED the moral-philosophical frame that now
reads as "the" I Ching. Course = that story, era by era, each layer in its own words
(HOW-TO-WRITE-A-COURSE method; ✔/○/◆ discipline; the stratigraphy grammars as companions).

## 4. Channel activation (the publish loop, per REPLICATE-THE-PATTERN §4)
recursive-eco.json (channel slug + id_map) → import/insert rows (public) → tools rows →
ids.json UUIDs → webhook binding → verify a touch-push reindexes. Then Pages domain.

## 5. Astro enrichment lane (parked, noted)
Astro is much richer than currently expressed: **aspects and significators/dignities**
deserve their own commented grammars (each aspect as an item with tradition-sourced
commentary; dignities/rulerships as a lens grammar). Same PD-source discipline.
