# For the platform (recursive.eco): notes from this repo

*A running list of things the I Ching repo learned that the recursive.eco platform will need.
Newest first. Started Oct 4 2026 with the reading-as-dialogue prototype
(`docs/DESIGN-reading-as-dialogue.md`, `viewers/dialogue.html`).*

## Oct 4 2026: reading as dialogue

The prototype offers passages tied to a real cast. The person marks which ones speak to them,
and the marks are the reading. What the platform would need to make this a feature for any deck:

1. **A saved reading is a Selection made of pointers.** The record (`kind: "reading-selection"`,
   shape in the design doc) keeps `{grammar, item_id, section}` for each passage chosen or set
   aside, plus the person's notes and their own words. It never copies the text.
   - The journal needs a place to keep one.
   - It needs **stable item ids across the repo and the app**. Today the channel merge matches by
     id, then by name, and items added over the MCP get random ids
     (`lib/channel/deep-merge-preserve.ts:74`; búzios channel rule 5). A pointer to an id that
     changed on import points at nothing. Ask: an import keeps the repo's item ids.
2. **The cast must report changing lines.** The dialogue needs the six line values (6–9), the
   primary hexagram, the moving lines and the relating hexagram. If the MCP `cast` tool only
   returns the primary hexagram, an assistant-led dialogue would have to make up the rest, and
   it must never invent a draw. Ask: `cast` on an I Ching grammar returns
   `{lines, primary, moving, relating}`, by the three-coin or yarrow odds
   (`viewers/caster-engine.js` `castLineNumber` is the reference, with its odds checked).
3. **The assistant as the one who offers.** When the assistant plays the diviner's part:
   - it offers passages *from the grammars*, each labelled with its source, and never writes
     its own meaning unless asked;
   - it doesn't rank the offerings ("this one fits you best") and doesn't pre-select;
   - it records "not this" as faithfully as "this one".

   This is a direct eval case for the oracle-values lab: who keeps the decision.
4. **"Set aside" is data, and private.** What did *not* speak to someone is part of the record.
   By default it is private to the person, like the rest of the reading.
5. **An item's own page** (the navigation redesign) can show, for one hexagram:
   - the same hexagram in every grammar: `grammars/meta-iching` already joins them, one composite
     per hexagram with `composite_of` pointing at each lens's item, mirroring tarot's All Decks;
   - the collections and playlists it appears in;
   - the passages the person themselves chose about it, gathered from their saved readings.
     Only theirs, by default; never public without their word.
6. **Offerings come in rings**: the whole figure → the two trigrams → the moving lines → where it
   may be turning. Other decks have rings too: a tarot card has its card, suit or arcana, and
   position in the spread; an odù has the sign and its stories. A generic version could let a
   grammar declare its rings (which sections and which related items to offer). That's a design
   question for later, not a schema change now.

## Oct 4 2026: data the platform can rely on from this repo

- **Every hexagram item carries `metadata.number`** (King Wen 1–64); `repair-iching` and
  `three-lenses-64` were missing it until Oct 4. The platform viewer's V-1 bug (no relating
  hexagram, numbers falling back to `sort_order`) should be fixed in the viewer by reading
  `metadata.number`. `item-shape.js` already counts it as a hexagram number.
- **`three-lenses-64` has no binary, trigram or Chinese-name fields**, so the shape rule reads it
  as plain, not as an I Ching grammar (the Cards viewer shows it with the plain theme now). If it
  survives the duplicate decision, its items should get `binary` and the trigrams. Fix the
  grammar, not the viewer.
- **The trigram items are thin**: keywords only, no text. The trigram images of the Shuo Gua (Ten
  Wings, Legge, public domain) would give the dialogue's trigram ring something to offer.
- **`grammar_type: "book"`** isn't in the platform's list. The book builder now writes `custom`;
  the caster's Book mode never read the type.
