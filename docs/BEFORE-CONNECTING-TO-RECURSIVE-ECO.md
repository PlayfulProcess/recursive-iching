# Before connecting this repo to recursive.eco (open since Oct 4 2026)

**Oct 6 2026: decided.** See [Decisions, Oct 6 2026](#decisions-oct-6-2026) at the end; the
sections above it are the record of how the questions were found.

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

## Decisions, Oct 6 2026

PlayfulProcess, Oct 6: "For I Ching, do what you think is best." These are the decisions taken on
that word. The app grammars were read over the recursive.eco MCP; nothing in the app was deleted,
renamed or edited.

### 1. `zhouyi-core` is `6efa4fc7` (Zhouyi, Legge translation)

| | `6efa4fc7` Zhouyi (Legge) | `0f8f4088` 周易 (original text) | `476b17da` Chinese Original |
|---|---|---|---|
| Items | 64 | 64 | 64 |
| English | Legge 1882 (public domain), Judgment + lines + "Use of Nine/Six" | **none** (slots left empty) | none (the "brief translation" is only the item names) |
| Chinese | traditional, in a "Chinese Original (Reference)" section | simplified, Judgment + lines | traditional, Judgment + lines + the Xiang Image |
| Provenance | sacred-texts.com (Legge, SBE vol. XVI) | cites `[@open-iching]`, a key with **no bibliography entry**, so the transcription's source and licence are unstated | Project Gutenberg #25501 (public domain) |
| Completeness | **5 line statements missing**: hex 6 line 5, 8 line 3, 12 line 3, 41 line 2, 52 line 5 | complete; at least one typo seen (hex 1 line 2: 再 for 在) | complete |
| State | Published, carries the collection's card | Link, no card | Published, has a card |

**Why `6efa4fc7`:** the folder's text is Legge's Judgment and lines, the same public-domain text,
and that grammar is the one the collection already shows. The repo copy is complete, so the first
import also fills the five missing lines.

**What had to change so the import pairs the items:** the importer matches items by `id`, then by
`name`. The repo used `hex-N` and the app `hexagram-N`, and 31 of the 64 repo names differ from the
app's ("Holding Together [Union]" vs "Holding Together"). Matched that way, 31 items would have
arrived as new items next to the 31 old ones. `zhouyi-core`'s ids are now `hexagram-N`, like the
app's, so all 64 pair by id. The repo's viewers find these items by `metadata.number`, so nothing
else changed; the meta grammar was rebuilt.

**What the first import will do to `6efa4fc7`** (repo wins on shared fields, app-only fields stay):
- its name becomes "Zhouyi Core — the Oldest Layer" and its description the repo's;
- the "Chinese Original (Reference)" section stays (the repo doesn't carry it);
- hexagrams 1 and 2 will show Legge's "use of nine/six" text twice, as the app's "Use of Nine" /
  "Use of Six" and the repo's "All Lines". Delete one label after the import.

**`476b17da` is a companion, not a duplicate.** It is the Han canon node (the received Chinese with
the Wings' Image) and maps to `i-ching-chinese-original` (same ids, same names, same text).

**`0f8f4088` is a duplicate.** What it holds is already in the library, from a source with a known
licence: the same Judgment and lines in traditional characters, in `6efa4fc7`'s reference section
and in `476b17da`. The Oct 4 proposal to "fold its Chinese into `zhouyi-core`" turns out to be done
already. It is not mapped and not deleted.

### 2. The three folders with no app grammar

`list_grammars` holds no grammar for any of them (searched: ching, 周易, zhouyi, lens, hexagram,
recursive, wing).

- **`meta-iching`**: built by `scripts/build_meta_iching.py` from the other folders. **It should
  become a grammar later**, as tarot's All Decks is, but only after `three-lenses-64` is retired:
  today 94 of its 534 items are copies of that duplicate, and 66 are the book's blank chapters. The
  builder now stamps `_generated: true`, which the importer skips.
- **`the-recursive-iching-book`**: built by `scripts/build_book_grammar.py`; 0 of 64 stories are
  written. **It should become a grammar (private) once stories exist.** The builder now stamps
  `_generated: true`. Book mode on this site keeps working from the file.
- **`three-lenses-64`**: its grammar does exist. It is `ad36491a`, which `iching-hd-meta-categories`
  already maps to (same ids; every item's text differs, the app's being newer). **Remove the
  folder** once its four readers move to `iching-hd-meta-categories`:
  `course/three-lenses.manifest.json`, `viewers/caster.html`, `viewers/lenses.html`,
  `scripts/build_meta_iching.py`. Until then it carries `_source_of_truth: "repo"`, so the
  importer doesn't create a second public copy.

### 3. Ten Wings `a172fed6` stays private

- **Not Legge.** It is Chinese only: Tuan, Great Image, Small Images and Sequence per hexagram,
  with the English slots empty.
- **Licence unstated.** The ancient text is public domain, but the transcription cites
  `[@open-iching]` with no bibliography entry, so its digital source and licence can't be checked
  from the grammar.
- **Gaps.** Hexagram 32 has no Tuan, no Judgment and no Sequence; hexagram 12 has no Sequence.
  (Hexagrams 1 and 2 have none, which is right: the Sequence begins at 3.)

The repo's `ten-wings` folder is a different book: Legge's English Great Image plus eight essays on
the wings. Ids and names differ from `a172fed6`, so the folder stays **unmapped and is created as a
new grammar** on the first import (public, like the collection). Publishing `a172fed6` later needs
its source named and hexagrams 12 and 32 filled.

### 4. `_collection.json`'s `"repo"`

It already reads `PlayfulProcess/recursive-iching`, from `scripts/build_collection.py` (fixed Oct
4). Today's rebuild left it unchanged.

### 5. King Wen numbers

Every hexagram item in every grammar now carries `"number": N` at the top level as well as
`metadata.number`. The platform viewer's relating-hexagram lookup reads `item.number`
(`grammar-viewer.html` tries `hexagram_number`, then `number`, then a `hex-N` id, then the
position), so `metadata.number` alone was not enough: that was finding V-1.

- Sources: stamped in the seven hand-made grammars (`zhouyi-core`, `i-ching-chinese-original`,
  `i-ching-summarized`, `iching-hd-meta-categories`, `repair-iching`, `ten-wings`,
  `three-lenses-64`).
- Generators: `build_meta_iching.py` and `build_book_grammar.py` now write it.
- `check.py` fails any hexagram item whose top-level `number` is missing or disagrees with
  `metadata.number`. Frame items (`metadata.role`) are exempt.

The live app grammars get the number when the import runs; until then V-1 stays visible on
recursive.eco. A one-line platform fix would cover every grammar, not only this repo's: read
`metadata.number` in that same chain.

### 6. `ids.json`

| Folder | App grammar | Note |
|---|---|---|
| `zhouyi-core` | `6efa4fc7` | Published |
| `i-ching-chinese-original` | `476b17da` | Published |
| `i-ching-summarized` | `b5161d12` | Published; renamed "The 64 Hexagrams" on import |
| `iching-hd-meta-categories` | `ad36491a` | Published |
| `repair-iching` | `b7a59594` | Link. The app's items have no `metadata.number`; the import adds it |
| `ten-wings`, `tree-of-the-iching` | none | created new on import |
| `meta-iching`, `the-recursive-iching-book` | none | skipped (`_generated`) |
| `three-lenses-64` | none | skipped (`_source_of_truth: "repo"`) |

### Duplicates and leftovers, for PlayfulProcess (nothing deleted)

- `0f8f4088` 周易 (original text): duplicate of `6efa4fc7`'s Chinese section and of `476b17da`.
  Link visibility, no card.
- `three-lenses-64` (repo folder): duplicate of `ad36491a`.
- `a172fed6` 十翼 (Chinese, private) is not a duplicate. Its Great and Small Images overlap
  `476b17da`'s Image section, but its Tuan and Sequence exist nowhere else in the library.
- Two I Ching grammars in the app have no folder here: `57b60ca6` 易經 · Emergent Structure (74
  items) and `5a09240d` 易經 · Leibniz Binary Tree of Change (458 items). Left as they are.

### Viewer copies

Item 7 (refresh `viewers/cards.html`) is closed without a refresh. Under the Oct 5 architecture
(recursive-eco `docs/future_plan/DESIGN-shells-and-shared-previews-2026-10.md`), a partner repo
keeps a shell and its grammars, and recursive.eco owns every preview. This repo's copied viewers
go when step P3 replaces them with framed previews. See `CLAUDE.md`.
