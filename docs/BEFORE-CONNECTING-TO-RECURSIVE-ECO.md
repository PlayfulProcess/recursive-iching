# Before connecting this repo to recursive.eco (open since Oct 4 2026)

The platform wants the **I Ching collection** (`recursive.eco/library/channels/iching`, slug `iching`) to come from this repo, the way Astrology already comes from recursive-astrology. A read-only dry run on Oct 4 found what has to be settled first. Nothing has been changed on the platform.

## What exists today

- **The platform's I Ching collection holds 4 cards, all PlayfulProcess's, all public:**
  - `476b17da…` I Ching, Chinese Original With Brief Translation;
  - `ad36491a…` I Ching HD Meta-Categories;
  - `b5161d12…` I Ching Summarized by AI;
  - `6efa4fc7…` Zhouyi (Legge translation).
- **This repo:** `recursive-eco.json` is set up (`channel.slug: "iching"`), but `ids.json` is an **empty skeleton** (`"ids": {}`), so nothing is mapped. `grammars/_collection.json` lists 9 folders.

## To investigate and decide

1. **Which grammar is `zhouyi-core`?** Two public grammars fit:
   - `6efa4fc7…` "Zhouyi (Legge translation)" holds the card now;
   - `0f8f4088…` "周易 — The Zhouyi (original text)" has no card.

   The folder's blurb ("the Judgment and the six Line statements, nothing else") reads closer to the original text. `476b17da…` (Chinese Original) overlaps both. Decide whether there are two or three distinct grammars here, and retire any duplicate.
2. **Three folders have no grammar in the app by name:** `meta-iching`, `the-recursive-iching-book`, `three-lenses-64`. `three-lenses-64` may be the same as `iching-hd-meta-categories` (near-identical blurb). Find each one or create it.
3. **`ten-wings`** matches `a172fed6…` "十翼 — The Ten Wings", which is **private**. Publish it, or keep it private: it would join the collection with no public card.
4. **`repair-iching`** matches `b7a59594…` "The Repair I Ching", which is public and has no card yet. It joins on import.
5. **A stale value:** `grammars/_collection.json`'s top-level `"repo"` reads `PlayfulProcess/recursive-starter`. It should be `PlayfulProcess/recursive-iching`. The importer doesn't read it, but it confuses people.
6. **A viewer bug seen on the platform (V-1):** on the Zhouyi, choosing changing lines never fills in the relating hexagram, because the hexagram number lives in `metadata.number` and the viewer falls back to `sort_order` (hexagram 1 gets number 0). Check the item numbering in this repo's grammars before import: each hexagram should carry its King Wen number 1–64 in `number` (or `metadata.number`).
7. **`viewers/cards.html` is the oldest sibling copy (Jul 11).** Refresh it from recursive-tarot's current viewer, and port `item-shape.js` from recursive-eco so it decides tarot / I Ching / plain from the data.

## Then the connection itself

1. Fill `ids.json` with each `slug → uuid` decided above.
2. On recursive.eco, the collection's Settings → "Add a collection from a repo", or Import, with this repo.
3. Convert it to a repo collection (`channels-to-folders.ts --slugs iching --apply`).
4. Check the I Ching collection page.

## Findings, Oct 4 2026 (I Ching repo session)

Read from the app over the recursive.eco MCP (read-only) and compared to each folder's first items.
**Nothing was changed on the platform and `ids.json` is still empty**: these are proposals, and
PlayfulProcess decides.

### What each folder is

| Folder | Best match in the app | Evidence | Proposal |
|---|---|---|---|
| `zhouyi-core` | `6efa4fc7…` Zhouyi (Legge translation) | Same Legge Judgment and line text; item names match ("The Creative"). The app copy adds "Use of Nine" and a Chinese reference section. | Map to `6efa4fc7`. |
| — | `0f8f4088…` 周易 (original text) | Chinese only (simplified), ids `hexagram-01-qian`, names "01 · 乾 (qián)", English left empty. **No repo folder holds it.** | Her call: keep app-only, add a folder, or retire it as overlapping `476b17da`. |
| `i-ching-chinese-original` | `476b17da…` Chinese Original | First item identical (traditional characters; Judgment, lines and the Xiang Image). | Map to `476b17da`. |
| `i-ching-summarized` | `b5161d12…` I Ching Summarized by AI | Same ids, same Legge text. The repo renamed it **"The 64 Hexagrams"** (commit 901d0b7); a push would rename the app copy too ("repo wins"). The app's items carry R2 images the repo doesn't. | Map to `b5161d12`, knowing the name changes. |
| `ten-wings` | **none.** `a172fed6…` is a different book | Repo: Legge's English Great Image, ids `hex-N`, plus 8 whole-wing items. `a172fed6`: Chinese only (Tuan, Great and Small Images, Sequence), ids `hexagram-01-qian`, **private**, the companion of `0f8f4088`. Neither ids nor names match, so mapping them would duplicate every item. | Treat the repo folder as new. Decide separately whether `a172fed6` (Chinese) is published. |
| `iching-hd-meta-categories` | `ad36491a…` HD Meta-Categories | 96 items, the app's own copy (pulled in Sep 2026). | Map to `ad36491a`. |
| `three-lenses-64` | (`ad36491a` again) | The older copy of the same 94 items (same ids; every item's text differs). | Duplicate. Retiring it means moving its readers first: `course/three-lenses.manifest.json`, `viewers/caster.html`, `viewers/lenses.html`, `scripts/build_meta_iching.py`. |
| `repair-iching` | `b7a59594…` The Repair I Ching | Public, no card yet. | Map to `b7a59594`. |
| `meta-iching` | none | Generated by `scripts/build_meta_iching.py` (534 items). Tarot's meta *is* in the app (`b03937bf`). | Her call: import it as the I Ching meta, or stamp it `_generated: true` so the importer skips it. |
| `the-recursive-iching-book` | none | Generated by `scripts/build_book_grammar.py`; 0 of 64 stories written. | Her call: import now (as a private draft) or wait for stories. |

**Why every folder must be decided before the import:** recursive.eco auto-imports any unmapped
`grammar.json` as a new **public** grammar (`lib/channel/import-new-grammar.ts`). Nothing reads
`recursive-eco.json`'s `grammars.exclude` (checked Sep 24 2026; recursive-learning CLAUDE.md). A
folder left unmapped becomes public; a folder stamped `_generated: true` is skipped.

### Done in this repo (Oct 4)

- Item 4: `"repo"` now reads `PlayfulProcess/recursive-iching`, in `scripts/build_collection.py`,
  `_collection.json`, the header's GitHub tab, the footer, `index.html`, the tree viewer and the
  README.
- Item 6: `metadata.number` (King Wen 1–64) added to the 76 hexagram items that lacked it
  (`repair-iching` 12, `three-lenses-64` 64). Every hexagram item in the repo now carries it.
- Item 7: `viewers/cards.html` replaced by recursive-tarot's current viewer (Sep 26). Only the
  paths, the accent, the branding and the default grammar were changed. `viewers/item-shape.js`
  was ported unchanged from recursive-eco (c164d95), and the viewer now takes the shape from the
  data. `viewers/reference-resolve.js` was copied from tarot (the viewer loads it).
- `check.py` passes again; it had 26 failures on main:
  - 25 came from the meta builder not prefixing copied groups' `composite_of`;
  - 1 came from `grammar_type: "book"`, now `custom`.

### Oct 4 2026, later: the history answers most of the decisions

See [`DECIDE-books-and-grammars.md`](DECIDE-books-and-grammars.md). The proposal is **one book per
node**:
- one grammar per historical book (Zhouyi, Ten Wings, Han canon, Legge, Human Design);
- languages as sections inside it, so the two Chinese-only app grammars (`0f8f4088`, `a172fed6`)
  fold into `zhouyi-core` and `ten-wings`;
- `three-lenses-64` retires;
- the new `tree-of-the-iching` is imported as the history grammar.
