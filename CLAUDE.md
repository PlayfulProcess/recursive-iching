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
  `grammars/the-recursive-iching-book/grammar.json` (`scripts/build_book_grammar.py`, from
  `frame.json` and `stories/`).
- **Before every push**, from the repo root, in this order:
  1. `python scripts/build_book_grammar.py`
  2. `python scripts/build_meta_iching.py` (it copies the book, so it runs after it)
  3. `python scripts/build_collection.py`
  4. `python check.py` (must print OK)
  5. `node scripts/determinism-check.js`
  6. `python scripts/check_book_mode.py` when the caster or the book changed (needs Playwright)
- **Every hexagram item carries its King Wen number twice:** `"number": N` at the top level and
  `metadata.number`. recursive.eco's relating-hexagram lookup reads the top-level one (finding V-1);
  `check.py` enforces it.
- **What the importer does with each folder** is decided in `docs/BEFORE-CONNECTING-TO-RECURSIVE-ECO.md`
  ("Decisions, Oct 6 2026"). An unmapped folder becomes a NEW grammar on import, public like the
  collection; `_generated: true` or `_source_of_truth: "repo"` makes the importer skip it. Decide
  every new folder before the next import.
- **Item ids must match the app's** for a mapped grammar: the import pairs items by `id`, then by
  `name`, and an unpaired item arrives as a duplicate.
- Never merge to `main` yourself; push a branch and open a PR.
