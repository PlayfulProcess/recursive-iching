# Reading as dialogue — design (Oct 4 2026, prototype)

*PlayfulProcess's seed, Oct 4 2026: she heard that in Ifá and búzios divination the diviner
tells several stories tied to the sign, and the person being read says which ones they relate
to. The reading happens in that conversation, not in a fixed meaning. Could a hexagram, its
trigrams, or its yin and yang lines be read this way?*

Mock: [`viewers/dialogue.html`](../viewers/dialogue.html). It's not in the site menu yet, and
nothing more gets built until she has looked at it.

## The one sentence

A reading-as-dialogue is a **real cast** plus **a few offerings** drawn from the published texts
for that cast. The person marks which offerings speak to them, and **what they chose is the
reading**: a Selection of the grammars, kept with their own words.

## What already exists (reused, nothing new underneath)

| Need | Already here |
|---|---|
| A real cast with changing lines | `viewers/caster-engine.js`: three coins or yarrow. `castLineNumber` / `castLines` return 6–9 (split out of `castLineValue` on Oct 4; the old function and its odds are unchanged, and `scripts/determinism-check.js` still passes). |
| Hexagram from lines | `scripts/hexagram-binary.json` (the verified King Wen ↔ binary table the Path Caster uses) |
| The story pool | the grammars: `i-ching-summarized` (Legge Judgment, Image, six lines, plus a short modern gloss), `three-lenses-64` (the eight trigram items and their keywords), `the-recursive-iching-book` (a Story, once one is written) |
| "Your choice is a record" | the platform's **Selection** (a named pick inside a grammar) and the journal |

New: one page, and the shape of the saved choice (below).

## The flow

1. **Your question** (optional). It stays in the browser.
2. **The cast.** Either "Cast the coins" in the page, or **"I cast my own"**: six numbers 6–9 typed
   from real coins on a real table. The page never chooses a hexagram for the person or makes up
   a draw. From the second draw on, it shows how many times you've cast in this session (the
   tarot rule: re-casting is never silent).
3. **The offerings**, grouped by how far in they look:
   - **The whole figure:** the Judgment, the Image (Legge, public domain), and the modern gloss,
     labelled as written with AI and not verified;
   - **The two trigrams meeting:** e.g. "Thunder below, Water above", with each trigram's
     keywords;
   - **The moving lines:** the statement of each changing line (6 or 9). When no line moves, the
     page says so: tradition reads the Judgment alone, and the six lines stay folded away to open
     if the person wants;
   - **Where it may be turning:** the relating hexagram's Judgment, only when lines move;
   - **A story from the book**, when `the-recursive-iching-book` has one for this hexagram (none
     are written yet, so none show).

   Every offering names its source (grammar and section). Each has two buttons: **"This speaks to
   me"** and **"Not this"**. Leaving it unmarked is a third answer.
4. **Your reading** builds itself live from what was chosen, in the order the person chose it,
   with a short "what it touches" note under each choice and one **In your own words** box at
   the end. The page writes no interpretation of its own.
5. **Keep it.** "Keep this reading" saves it in this browser. "Download" gives the Selection as
   JSON. Saving it to the recursive.eco journal is the platform's half (see
   `docs/FOR-THE-PLATFORM.md`).

## The record (what "a Selection of the grammar" means here)

```json
{
  "kind": "reading-selection",
  "made_at": "2026-10-04T15:02:11Z",
  "question": "optional, her words",
  "cast": { "method": "coins | yarrow | own", "lines": [8,7,9,8,6,7],
            "primary": 3, "relating": 42, "moving": [3,5] },
  "chosen":    [ { "grammar": "i-ching-summarized", "item_id": "hexagram-3",
                   "section": "Line 3", "note": "what it touches, her words" } ],
  "set_aside": [ { "grammar": "i-ching-summarized", "item_id": "hexagram-3", "section": "Image" } ],
  "offered":   12,
  "in_her_words": "free text"
}
```

The choices point at **grammar + item + section** and never copy the text, so the record stays
small and always opens onto the current text. "Set aside" is kept on purpose: what didn't speak
to someone is part of the conversation too, and they may want to see it next month.

## Rules it keeps

- **Non-predictive.** The page never says what the cast "means for you" and never tells anyone
  what to do. The creed sits above the cast: read to know yourself, not to be told your fate.
- **The person's agency comes first.** Nothing is pre-selected. Order follows the layers of the
  text, not a ranking, and there is no "best match".
- **No invented draws.** The cast is either coins in the browser or the person's own throw. An
  assistant offering stories later must call the real cast, never make one up.
- **Sources named.** Every offering carries its grammar and section, and AI-written text says so.
- **Nothing leaves the browser** in this mock.

## Open questions for her

1. Does the Ifá/búzios form want the offerings **all at once** (as here) or **one at a time**,
   the way a diviner tells one story and waits?
2. Should "Not this" stay visible in the kept reading, or fold away?
3. When no line moves: show the six lines folded (as here), or not at all?
4. Is the AI-written gloss welcome as an offering, labelled, or should only the classical text be
   offered?
5. The trigram ring is thin (keywords only). Should the trigram *images* from the Shuo Gua (Ten
   Wings, Legge, public domain) be added to the trigram items first?
6. Where does it live: its own Views entry, or a mode of the Path Caster?
