# Plan — story frames: why the book ends at the Creative, and how readers make their own

*5 September 2026. Written before building, at the author's request ("plan first").*

## The structural point she made

"It only makes sense to set Hexagram 1 as the end if we pin it inside a spread — a story." Yes.
Right now Book mode hard-codes destiny = 1 and hard-codes one opening and one closing. That is a
*story frame* pretending to be a feature of the caster. The fix is to make the frame explicit: **a
story frame is a spread.** The caster does not know where books end; a *frame* does.

## What a frame is

```
frame = {
  name:        "Gautama walks back to the Creative",
  origin:      { mode: "cast" }            // or { mode: "fixed", hexagram: 47 }
  destiny:     { mode: "fixed", hexagram: 1 }   // or "cast"
  steps:       { style: "wandering", budget: "auto" | n }
  intro:       "…text…",                    // the fixed beginning
  end:         "…text…",                    // the fixed end
  stops:       [ { label: "Where I was" }, …, { label: "The Creative" } ]   // optional named positions
  stories:     "grammar id or slug"        // which per-hexagram Story grammar to read from
}
```

The Gautama book is the **first frame**: origin cast, destiny 1, the opening and closing I wrote,
stories from `the-recursive-iching-book`. A second frame could be "From the Creative to the
Receptive" (1 → 2, the Lightning Flash), or "Before Completion" (cast → 64), or a reader's own:
"My year" (fixed origin = the hexagram they cast in January, destiny cast today).

**The end-at-1 becomes a property of a story, not of the tool.** Which is what she said.

## Why this is literally a recursive.eco spread

recursive.eco already has a saved-spread contract, `SpreadContract v1 = { v:1, name, positions:[{label,
meaning, x, y}] }` (max 15 positions, max 30 saved per user; stored in
`profiles.profile_data.preferences.spreads`; read cross-origin by the tarot and astro sites via
`GET /api/spreads` with the `.recursive.eco` cookie; deletable via `DELETE /api/spreads`; convertible
into a casting grammar via `POST /api/spreads/convert`).

A story frame fits that contract with no schema change:

| frame field | SpreadContract |
|---|---|
| name | `name` |
| origin / destiny / steps | `positions[0].label = "origin:cast"`, `positions[last].label = "destiny:1"`, budget in a position meaning — or, cleaner, a `meaning` on position 0 holding a small JSON blob |
| intro / end | `positions[0].meaning` / `positions[last].meaning` (the text) |
| stops | the middle positions |
| stories | a `meaning` field naming the grammar |

So "My spreads" in the caster = "My story frames." The reader's saved frames appear in a dropdown
exactly the way saved spreads appear in the tarot studio's dropdown today (`caster-studio.html`,
`loadMySpreads`). Same code, different domain.

## Write-back: can the page save a frame to the account?

**Not yet — and the gap is one route.** Checked in `recursive-eco/apps/flow/src/app/api/spreads/route.ts`
(5 Sep 2026):

- `GET` and `DELETE` are CORS-enabled for `https://*.recursive.eco` with credentials. ✅
- There is **no `POST`/`PUT` on `/api/spreads`**. Spreads are *written* only through `PATCH
  /api/preferences`, which is same-origin (flow) only — the tarot studio's own comment says so.
- `POST /api/spreads/convert` exists (turns a spread into a grammar) — it is not a save.

So the static page can *read* and *delete* the reader's frames today, and cannot *create* one. The
minimum change on flow: add `POST /api/spreads` (body = SpreadContract; validate with the existing
`validateSpread`; merge with `mergeSpreadsById`; write to preferences), and add `POST` to
`Access-Control-Allow-Methods` in `corsHeaders`. One file, ~40 lines, no schema change. Until it
lands: **download JSON → import** remains the path, and the page should say so in one line.

Test protocol when it lands (from memory: the preview browser is signed out — test signed-in features
in her Chrome): open the caster on iching.recursive.eco while signed in to recursive.eco, save a
frame, reload, see it in the dropdown, then see it in flow's My Spreads.

## What the reader can make in the page (levels)

1. **Their transitions** — shipped (per-step textarea, localStorage, saved into the JSON/Markdown).
2. **Their opening and closing** — two textareas at the top of Book mode, pre-filled with the
   frame's text, editable; saved into the frame. *Small.*
3. **Their story for a hexagram** — an "add my story" textarea under each blank Story; saved into a
   personal stories overlay (localStorage now; a personal grammar later). *Small.*
4. **Their frame** — origin/destiny/steps pickers + the two texts above = "Save this frame" (download
   now; account when POST lands). *Medium.*
5. **Their edition** — assemble frame + path + stories + transitions → Markdown (shipped) → EPUB (an
   in-browser zip, or book-repo's pandoc pipeline). *Medium.*

## How the Gautama story is "weaved in"

Per hexagram the Story block gets sub-sections the design doc already names: *The meeting* (two
trigrams), *The school* (science), *The terreiro* (orixá), *The ordinary world* (Gautama's scene).
On screen: the first paragraph visible, the rest behind "Read the chapter" — the UX review will say
whether that is right. The chapters themselves live in `grammars/the-recursive-iching-book/stories/NN.md`
and fold into the grammar on build. Zero of 64 exist; the frame and the machinery do.

## Order of work (after her word)

1. Extract the frame from the code: `frames/gautama.json` (name, origin, destiny, steps, intro, end,
   stories) and make Book mode read it. Frame picker with one entry. *Same behaviour as today.*
2. Levels 2 and 3 above (edit opening/closing; add my story). Download includes them.
3. `GET /api/spreads` → "My frames" dropdown (read-only, works today for signed-in readers).
4. The flow `POST /api/spreads` route (recursive-eco branch; her Vercel click).
5. Write the first three Gautama chapters (1, 2, and 29 Kan/Water/Oxum) as the weave test.
6. Apply the UX review's top five.

## Docs to update when this ships (so it is remembered faster next time)

- `docs/DESIGN-path-caster.md` — add "Book mode and frames" section.
- `README.md` — the Book mode paragraph already added; add the frames sentence.
- `recursive-eco/docs` — note the `/api/spreads` POST gap and the family-CORS rule.
