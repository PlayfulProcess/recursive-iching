# Plan — the meta I Ching: scenery, action, story

*5 September 2026. The author's idea, restated so it can be built: "render the meta I Ching including
Human Design. Each cast is saved as a spread-like entry. The story is an emergent item of all sub-items
of each I Ching grammar linked, and we tell a story that weaves them all together. Human Design holds
the key to humanize the action the hexagram is asking for; the hexagrams and trigrams are the scenery."*

## Yes, it makes sense — and it maps onto things that already exist

| Her word | What it is in the repo | Status |
|---|---|---|
| **Scenery** | the two trigrams (8 trigram items in `three-lenses-64`) + Legge's Great Image (`ten-wings`) | exists |
| **Text** | Legge's Judgment and six lines (`zhouyi-core`), condensed in `i-ching-summarized` | exists |
| **Action** ("what the hexagram asks of a person") | the Human Design lens — `three-lenses-64` gives each hexagram a gate-flavoured name and keywords (e.g. 29 *The Abysmal Water*: commitment, perseverance, saying-yes) | **thin: names + keywords only; the sections are empty.** This is the gap. |
| **Story** | the book chapter per hexagram (`the-recursive-iching-book/stories/NN.md`) | 0 of 64 written |
| **Wound** | `repair-iching` (14 hexagrams) | exists |
| **Emergent item** | a composite item with `composite_of` pointing at the hexagram's item in every lens — exactly how recursive-tarot's *All Decks, Many Lenses* meta grammar works (`emergence_kind`) | **built: `grammars/meta-iching/`** (`scripts/build_meta_iching.py`) |
| **Each cast saved as a spread-like entry** | a story frame = a spread (`PLAN-story-frames.md`); the cast path = positions | planned; needs the flow POST route |
| **A story that weaves them** | the Book mode reading: per step, Scenery → Text → What it asks → Story → the changing line | Book mode reads the book grammar today; switch it to read the meta composite so all lenses show |

## The Human Design gap, honestly

Human Design maps gate *N* to hexagram *N* — same numbering, so the join is free. What we do not
have is the *content* of the action: Ra Uru Hu's gate keynotes and descriptions are in copyright
(1987 onward), and the three-lenses grammar deliberately carries only a name and keywords. Options:

1. **Write our own one-line "what it asks" per hexagram** (64 lines) from the keywords, in the
   book's voice, as the author's synthesis — honest, ours, CC BY-SA. Recommended.
2. Cite HD keynotes by gate number as short factual labels (a keynote is a couple of words; fair
   use) with attribution, and write the behaviour sentence ourselves.
3. Leave the lens as keywords and let the story chapter carry the action.

## Order of work
1. ✅ Build the meta grammar (composites + all source items) and list it in the collection.
2. Point Book mode's per-step block at the meta composite: Scenery / Text / **What it asks** / Story.
3. Write the 64 "what it asks" lines (option 1) into `three-lenses-64` sections so every lens has text.
4. Story frames + spreads (the other plan) so each cast is saved and the woven story is an entry.
5. Then the stories, 64 chapters, one casting at a time.
