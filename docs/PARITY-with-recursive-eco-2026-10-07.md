# Parity with recursive.eco (Oct 7 2026)

PlayfulProcess, Oct 6: "If no extra features are in the preview of hexagrams there, maybe let's carry
it to recursive.eco the way we were planning (same header and footer, potentially different css when
coming from iching)?"

The plan is recursive-eco `docs/future_plan/DESIGN-shells-and-shared-previews-2026-10.md`: this repo
keeps a shell and its grammars; recursive.eco owns every preview and draws this site's header and
footer around it when opened with `?shell=iching`.

**Short answer.**
- **A hexagram's preview:** recursive.eco's does what this site's does, and more (sign-in, stars,
  reading progress, its own assistant, print). The hexagram numbers it needed are now in all five
  mapped grammars (below). One extra exists here, on the grid rather than the hexagram: group-by
  chips.
- **The framed preview is not live yet**, so the site's main links stay here for now (section 3).
- **The site's other views** (the Path Caster, the books' genealogy and timeline, the lenses, the
  explorer, the stacked source text, Cards across all books) have no recursive.eco equivalent and
  stay.

## 1. Viewer by viewer

| This site | What it does | recursive.eco | Parity | Decision |
|---|---|---|---|---|
| `viewers/cards.html`, hexagram detail | One book as cards; a hexagram's text, changing lines and relating hexagram; Cast with the assistant; Edit at the item | `pages/grammar-viewer.html` (this file is a copy of it, via recursive-tarot): the same detail, changing lines and relating hexagram, plus sign-in, stars, progress, its own assistant, print | **Yes**, now that each hexagram carries its number (V-1, fixed in the data today) | Move when framed (section 3) |
| `viewers/cards.html`, one book's grid | The cards, filters, the hierarchy sidebar, and **group-by chips**: any field found in the items (upper trigram, lower trigram, keyword…) groups the grid (`DimensionEngine`, `#groupby=` in the address) | The same grid, filters and hierarchy sidebar; **no group-by chips** | Almost: the chips are the one extra | Her call: move anyway, or recursive.eco gains the chips first |
| `viewers/cards.html`, all books | Every folder in `_collection.json` in one view, a "By book" dimension, meta items resolved into their source books (`deck-picker.js`, `reference-resolve.js`) | None: the collection page lists the grammars, and Cards opens one at a time. `meta-iching` is not in the app | No | Stays |
| `viewers/cards.html`, Print | Sends to `../pages/print-viewer.html` | `pages/print-viewer.html` exists, but reads only same-site `localStorage`, so no other site can hand it a grammar | **Broken here**: that page doesn't exist in this repo (404 on iching.recursive.eco) | Needs her (section 4) |
| `viewers/tree-viewer.html` | A grammar's emergence tree | `pages/tree-viewer.html` (this file is a copy) | Yes | No local link opens it for a mapped grammar; nothing to move |
| `viewers/caster.html` | Path Caster: an origin and a destiny hexagram and the changing lines between them; four ways, including Cast your book | The oracle casts one hexagram (`/g/<id>?view=reading`, the assistant's cast) | No path caster | Stays |
| `viewers/genealogy-tree.html` | The books of the I Ching as lines of descent (`tree-of-the-iching`) | No genealogy view; the grammar isn't in the app (PR #4 open) | No | Stays |
| `viewers/timeline.html` | The same books on a time rail | None | No | Stays |
| `viewers/lenses.html` | Five comparisons across every book (Through time, Side by side, Pictures, Which sections where, Read one grammar) | None (one grammar at a time) | No | Stays |
| `viewers/explorer.html` | Pivot all books' items by any field | None | No | Stays |
| `viewers/source-text.html` | One hexagram with its layers stacked: Chinese, Zhouyi, Ten Wings, the 64 Hexagrams, Three Lenses | None (one grammar at a time) | No | Stays |
| `pages/course-viewer.html` | A reading from a manifest: chapters, an appendix, companion books, bibliography, zen art | `pages/courses/course-viewer.html` and `study-viewer.html` read one grammar in order; no manifest, appendix or companions | Partial | Stays; its companion links now open recursive.eco framed, at the chapter's hexagram |
| `viewers/dialogue.html` | Prototype: a cast, then passages to mark | None | No | Stays (prototype) |

## 2. What was carried into recursive.eco

Only additive or corrective changes, each made through `sync_grammar_from_json` with a JSON that
named every item by its app id and carried only the new field, dry-run first. After each write
the grammar was re-read from the database and compared with a snapshot taken before: only the
fields below changed. Names, descriptions, tags, categories and visibility are untouched.

**To undo a change:** `restore_grammar_version(<grammar>, <before>)`. Three grammars had no saved
version at all, so a no-op save was made first to give each one a "before" (marked *baseline*; its
content is the Oct 6 state, unchanged). The version list labels a number-only write "(no content
change)" because its describer doesn't count a top-level `number`; the database rows were re-read
and carry it.

| Folder → app grammar | Before | After | What changed |
|---|---|---|---|
| `zhouyi-core` → `6efa4fc7` Zhouyi (Legge translation), Published | `81e14e2bfdd9472141177d753dc36e652da7341b` | `70ff6f21391bc848072bbead797f36f98589ea69` | `number` 1–64 on all 64 items. **The five missing lines filled:** hex 6 line 5, 8 line 3, 12 line 3, 41 line 2, 52 line 5. Each had been glued onto the line before it in the app ("…good fortune. S. The fifth NINE…", "…(for the other). 2 . The second NINE…"), so the line before now ends where Legge's does and the missing line stands on its own. No words were lost; the repo's text was used for both lines. |
| `i-ching-chinese-original` → `476b17da` Chinese Original, Published | `d5558536b00cc7ecddf92f05475601ccb6f4edf1` (baseline) | `780bc419e393250924b69206c9ad40c25477e1d0` (numbers), then `7b7311832a1312e3f489bc64d9f90fbc379f3b4b` (cover) | `number` on 64 items. **Cover:** was a Wikimedia *page* address (`commons.wikimedia.org/wiki/File:I-Ching-chinese-book.jpg`, which serves HTML, so no picture showed); now the same picture's file, `upload.wikimedia.org/wikipedia/commons/f/f8/I-Ching-chinese-book.jpg`. |
| `i-ching-summarized` → `b5161d12` I Ching Summarized by AI, Published | `b71b4204f8bbf9738ab3b714c390c3caabb8a240` | `6bebe0f32e5d410c3112fea62b8561160c09d7c3` | `number` on 64 items. |
| `iching-hd-meta-categories` → `ad36491a` HD Meta-Categories, Published | `e43b9bf73880e2b7adb3c7268f4d82dbe5ae74a9` (baseline) | `72a24abd3a6361079efc8356056cab08e17a11fb` | `number` on the 64 gate items (the 32 sign, chakra, trigram and synthesis items have none). |
| `repair-iching` → `b7a59594` The Repair I Ching, Link | `8fafb94a9941b8689fae6b1d077d1b2f1e584848` (baseline) | `39ccca3253aaf16d59f46f713e98901ce16cdafb` | `number` and `metadata.number` on the 12 hexagram items (they had only `metadata.hexagram_number`). |
| `ten-wings` → **new** `e249829d-e441-4dc2-a9d8-1ad127a06092` The Ten Wings — the Confucian Layer, **Private** | none | `b0572407bd4566b873a845a624383f5ab4c562c7` | Created with `import_grammars` from this repo's `main`: 72 items, ids `hex-N` and `wing-*` as in the repo, numbers on the 64 hexagram items. Private, so it shows to no one else until she publishes it. Mapped in `ids.json`; not in `_public_now`, so this site offers no recursive.eco links for it yet. Undo: delete the grammar. |

**Checked in the browser** (dev.recursive.eco, Zhouyi, `&hexagram=6`): Line 5 shows on its own and
Line 4 ends at "good fortune."; the viewer numbers hexagrams 1, 6 and 64 as 1, 6 and 64 (it gave
hexagram 1 the number 0 before, so `&hexagram=6` used to open hexagram 7).

### Found and left alone

- **Renames and rewrites the full import would make** ("repo wins"): `6efa4fc7` → "Zhouyi Core — the
  Oldest Layer", `b5161d12` → "The 64 Hexagrams", `476b17da` → "I Ching — Chinese Original (Project
  Gutenberg)"; their descriptions, tags, `creator_link` and `_grammar_commons`; `grammar_type`
  `custom` → `iching` on four of them.
- **Categories that disagree:** Zhouyi and the Chinese Original use `trigram` in the app, a trigram
  name in the repo; on `b5161d12`, 56 items name the upper trigram in the app and the lower one in the
  repo.
- **Text the app has newer:** `b5161d12` has 10 Interpretation texts edited Sep 24 that the repo
  lacks. 58 Zhouyi lines differ from the repo mostly in punctuation ("--" vs "—"); not checked one by
  one.
- **Duplicates:** the repo's "All Lines" on hexagrams 1 and 2 repeats the app's "Use of Nine" / "Use
  of Six"; not added.
- **Provenance metadata** (`_source`, `confidence`, `legge_title` on the Zhouyi items): left for the
  import.
- **The 64 HD gate pictures** (`img/hd/gate-NN.svg`): the README calls them provisional placeholders
  that don't match the real bodygraph, so they were not put on `ad36491a`'s items.
- **Two broken covers, fix prepared but not written:** this session's permission check refused the
  write. `b5161d12`'s cover is a Wikipedia page address (`en.wikipedia.org/wiki/Yin_and_yang#/media/…`);
  the same picture's file is `https://upload.wikimedia.org/wikipedia/commons/3/3c/Yin_and_Yang_symbol.svg`.
  `ad36491a`'s is a Commons page address (`…/wiki/File:Diagram_of_I_Ching_hexagrams_owned_by_Gottfried_Wilhelm_Leibniz,_1701.jpg`);
  its file at 960 px is `https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Diagram_of_I_Ching_hexagrams_owned_by_Gottfried_Wilhelm_Leibniz%2C_1701.jpg/960px-Diagram_of_I_Ching_hexagrams_owned_by_Gottfried_Wilhelm_Leibniz%2C_1701.jpg`.
- **Skipped on purpose:** `tree-of-the-iching` (PR #4 open), `meta-iching` and
  `the-recursive-iching-book` (`_generated`), `three-lenses-64` (`_source_of_truth: "repo"`).

## 3. Links: what moved, what stays

**Why most links stay.** A framed preview needs three things, and none is in place for the I Ching:

1. **Shells P1 on recursive.eco.** It is on `dev.recursive.eco` only (branch
   `seedlings/shells-p1`, not in `main`): `recursive.eco/assets/js/partner-shell.mjs` answers 404,
   and on recursive.eco `?shell=` is ignored.
2. **The shell block stored on the collection.** The I Ching collection (`6e19ea89`, slug `iching`)
   has `document_data.shell` empty: only the channel import writes it, and it has not been run.
3. **The grammars as links in the collection.** P1 frames only a grammar that is a link inside the
   collection (`document_data.items`, `item_type: "reference"`). The I Ching collection is the older
   kind, with no items, so it needs converting (`channels-to-folders.ts --slugs iching --apply`).

Checked: every URL below answers 200 on both dev and recursive.eco
(`/pages/grammar-viewer.html`, `/pages/study-viewer.html`, `/pages/tree-viewer.html`, `/view/<id>`,
each with `?shell=iching`), and the dev Cards page, opened in the browser, drew recursive.eco's own
header. Moving the home page's links now would take visitors off this site with no way back in the
header, which is what the plan is meant to avoid. The repo's `CLAUDE.md` says the same: the copies
stay until framed previews replace them.

**Moved now:**
- **The course's companion links** (`pages/course-viewer.html`): Cards, Study and Tree on
  recursive.eco already opened in a new tab; they now carry `&shell=iching`, so they become framed
  the day recursive.eco carries the I Ching shell, with no further change here. Cards opens at the
  chapter's own hexagram (`&hexagram=N`), as the manifest always said it should; that works now that
  the numbers are right.
- **Private grammars get no links.** `viewers/cards.html`, `assistant.js` and the course read
  `ids.json`'s `_public_now`, so the mapped-but-Private Ten Wings gets no Cast, Edit or assistant
  link that would fail for visitors.

**The flip, once 1–3 are done** (each link to a slug in `_public_now`; the URL is
`https://recursive.eco/pages/grammar-viewer.html?type=iching&id=<id>&shell=iching`):
- `index.html`: line 203 (The 64 Hexagrams, read the full text), 214 and 252 (the 64 Hexagrams way
  and node), 230 and 272 (the Repair I Ching way and node), and the deck grid's builder at line 439
  (mapped slugs only; the others keep the local Cards).
- `site-header.js` line 233, the header's book menu (same rule).
- `pages/course-viewer.html` line 267, "Open this book in the library" (same rule).
- In-viewer links (`cards.html` deck menu, `genealogy-tree.html`, `timeline.html`, `lenses.html`)
  stay local: they open books recursive.eco doesn't hold or the all-books view.

## 4. What needs PlayfulProcess

1. **Shells P1:** merge and deploy `seedlings/shells-p1` (her word).
2. **The I Ching collection:** convert it to a folder collection, then run the channel import from
   this repo; that stores the shell and pairs the folders. Before running it, decide on the renames
   and rewrites listed under "Found and left alone": the import applies them all (repo wins).
3. **Two covers** (`b5161d12`, `ad36491a`): the exact addresses are above.
4. **Ten Wings:** publish `e249829d` or keep it private. If published, add `ten-wings` to
   `_public_now` in `ids.json`.
5. **Print on this site** (404): either recursive.eco's print viewer learns `?id=`, or the button
   goes.
6. **What recursive.eco lacks:** the group-by chips on one book's Cards grid; and whole views: the
   Path Caster, the genealogy and timeline of the books, the lenses, the cross-book explorer, the
   stacked source text, manifest courses, and Cards across all books. Each stays here until
   recursive.eco has its own, or she decides otherwise.
7. **V-1 on the platform:** recursive.eco's Cards still reads only `item.number` or a `hex-N` id.
   The five grammars are fixed in their data. Four other I Ching grammars (`0f8f4088`, `a172fed6`,
   `57b60ca6`, `5a09240d`) have no top-level number and no `hex-N` ids, so the viewer falls back to
   their position there. Reading `metadata.number` and `hexagram-N` ids in that chain would fix them
   all.
