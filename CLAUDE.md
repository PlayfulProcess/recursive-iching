# CLAUDE.md — The Recursive I Ching

The I Ching collection of recursive.eco, as a repo: `grammars/*/grammar.json` in the sync format,
`ids.json` (slug → recursive.eco grammar id), `recursive-eco.json` (the collection manifest), and a
static site at iching.recursive.eco. Call the owner PlayfulProcess; never write a real name.

## Rules for this repo

- **No viewer copies.** Under the Oct 5 2026 architecture, recursive.eco owns every preview (Cards,
  Playlist, Tree, Study, Course) and a partner repo keeps only a shell and its grammars (recursive-eco
  `docs/future_plan/DESIGN-shells-and-shared-previews-2026-10.md`). Don't refresh, port or add viewer
  files under `viewers/`. The copies there now stay until step P3 replaces them with links into
  recursive.eco's framed previews; fix a viewer bug on recursive.eco, not here.
- **Edit sources and generators, never generated files.** Generated: `grammars/_collection.json`
  (`scripts/build_collection.py`), `grammars/meta-iching/` (`scripts/build_meta_iching.py`),
  `grammars/hd-mandala-wheel/` (`scripts/build_hd_wheel.py`), `grammars/hd-lines-zhouyi/`
  (`scripts/build_hd_lines.py`, which reads the wheel and `zhouyi-core`),
  `grammars/the-recursive-iching-book/grammar.json` (`scripts/build_book_grammar.py`, from
  `frame.json` and `stories/`), and the twelve `tbl-` nodes of `grammars/changing-lines-lens/`
  (`scripts/changing_lines.py --build`; that course's `ch-` chapters are hand-written), and
  `data/verdict-words.json` (`scripts/verdict_words.py --build`: the verdict-word rates behind
  `pages/verdict-heatmaps.html`; the page's three header sentences and the position × polarity table in the course's
  "The figures" are computed there and `--check` fails if either stops stating them verbatim).
- **Before every push**, from the repo root, in this order:
  1. `python scripts/build_book_grammar.py`
  2. `python scripts/build_meta_iching.py` (it copies the book, so it runs after it)
  3. `python scripts/build_hd_wheel.py`
  4. `python scripts/build_hd_lines.py` (after the wheel)
  5. `python scripts/build_collection.py`
  6. `python check.py` (must print OK)
     and `python scripts/casting_odds.py --quiet` (must print OK: the odds behind the Casting and Chance course, and the course quoting them)
     and `python scripts/changing_lines.py --check --quiet` (must print OK: the twelve changing-line tables are current, the Changing-Lines Lens course quotes the figures, and `data/verdict-words.json` and its heatmap page are current)
  7. `node scripts/determinism-check.js`
  8. `python scripts/check_book_mode.py` when the caster or the book changed (needs Playwright)
  9. `python scripts/build_hexagram_pages.py`, then `python scripts/build_hexagram_pages.py --check` (must print OK). It writes the 64 static hexagram pages (`hexagram/*.html`), the chart `hexagrams.html`, `sitemap.xml` and `data/sitemap-lastmod.json`, all generated: never hand-edit them. Re-run it after editing zhouyi-core, ten-wings, i-ching-chinese-original, i-ching-summarized, `scripts/hexagram-binary.json`, or any page it lists in the sitemap (index.html, the wheel, the heatmaps, the caster, the source text): a page's `<lastmod>` moves only when its bytes change. After a hexagram's name changes, also `python scripts/build_og_images.py` (the share images in `img/og/`; needs Pillow).
- **Every hexagram item carries its King Wen number twice:** `"number": N` at the top level and
  `metadata.number`. recursive.eco's relating-hexagram lookup reads the top-level one (finding V-1);
  `check.py` enforces it.
- **What the importer does with each folder** is decided in `docs/BEFORE-CONNECTING-TO-RECURSIVE-ECO.md`
  ("Decisions, Oct 6 2026"). An unmapped folder becomes a NEW grammar on import, public like the
  collection; `_generated: true` or `_source_of_truth: "repo"` makes the importer skip it. Decide
  every new folder before the next import.
- **Item ids must match the app's** for a mapped grammar: the import pairs items by `id`, then by
  `name`, and an unpaired item arrives as a duplicate.
- **No Human Design or Gene Keys text in any grammar.** Jovian Archive Media (Human Design) and Gene Keys Ltd
  reserve their rights, and the Gene Keys terms bar the use of their materials to train or operate AI
  systems, which includes this site's assistant. Facts, positions and our own words only; see
  `docs/RESEARCH-gene-keys-and-human-design-2026-10-12.md`.
- **No live links to jovianarchive.com** (nor to the IHDS or myBodyGraph pages) in a public page or grammar: its
  Terms ask that the site not be linked without written consent. Cite its pages by title and date.
- **`ten-wings` is a mapped grammar:** change it only by adding sections (`scripts/add_ten_wings_sections.py`
  shows how); never change an item id or name.
- Push a branch and open a PR. Claude may merge a PR here once the checks above pass, with a normal merge commit (PlayfulProcess's rule of Oct 13 2026, root `CLAUDE.md` "Merging pull requests", repeated for this repo on Oct 20 2026); recursive-eco still waits for her word.
