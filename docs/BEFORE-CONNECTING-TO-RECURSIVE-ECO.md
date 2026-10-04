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
