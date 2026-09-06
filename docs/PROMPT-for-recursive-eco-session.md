# Prompt to paste into the recursive-eco session (flow) — what the static sites need from the app

*Written 6 Sep 2026 from the recursive-iching side. Paste the block below into the session that owns
`recursive-eco`. Everything it asks for is small and server-side; nothing in the static sites has to
change for it except pointing "save" at the new route.*

---

```
Context: the static sites tarot.recursive.eco and iching.recursive.eco read a signed-in user's saved
spreads through GET /api/spreads (CORS-enabled for the .recursive.eco family with credentials) and can
DELETE. They cannot CREATE. The I Ching site now has a "Book mode" (viewers/caster.html?mode=book) whose
"save" downloads a JSON grammar because there is no write route. A spreads POST was merged locally on the
ai-101 branch; this makes it complete and usable from the static sites.

Please, in apps/flow:

1. /api/spreads POST — accept a SpreadContract v1 body ({ v:1, name, positions:[{label, meaning, x, y}] },
   max 15 positions), validate with the existing validateSpread(), assign id/createdAt via toSavedSpread(),
   merge with mergeSpreadsById() into profiles.profile_data.preferences.spreads (respect MAX_SAVED_SPREADS
   = 30; return 409 with the existing spread when a name collides unless ?replace=1), return the saved
   spread with its encoded `param`. Add POST to Access-Control-Allow-Methods in corsHeaders() and make
   OPTIONS preflight reflect it. Same 401-when-signed-out behaviour as GET. Log like GET/DELETE.

2. Let a position's `meaning` carry a small JSON string (<= 4 KB) without mangling it — the I Ching book
   will store a "story frame" in a spread: position 0 meaning = {"kind":"frame","origin":"cast",
   "destiny":1,"style":"wandering","grammar":"the-recursive-iching-book"} and the opening/closing text in
   the first/last positions' meaning. No schema change; just do not truncate or HTML-escape meaning on
   write. If validateSpread caps meaning length, raise the cap to 4 KB.

3. /api/spreads/convert POST — confirm it is CORS-enabled for the family too (it turns a spread into a
   casting grammar); if not, add the same corsHeaders().

4. One new read: GET /api/grammars/mine?type=book (or reuse an existing "my grammars" endpoint if there
   is one) CORS-enabled the same way, returning id, name, grammar_type, item_count, updated_at — so the
   Book mode can list a signed-in reader's own saved books next to their frames.

5. Tests: the existing /api/spreads tests pattern; add POST happy path, 401, 409 collision, 15-position
   cap, meaning 4 KB round-trip.

Do NOT push to main / production without the author's word (Vercel build minutes) — branch + local
verification, then report the route contract back so the static sites can be pointed at it.
```

---

## Why build it there and not here

- The static sites are backend-free by design (GitHub Pages). Anything that writes to a user's account
  must live behind flow's auth and CORS policy — that is where the cookie is validated and where the
  family-origin check already exists.
- The contract is tiny (one POST, one cap raise, one CORS line, one optional list route). Building a
  parallel write path anywhere else would fork the spreads model.
- The other session already merged a POST locally; finishing it there avoids two divergent versions.

## What changes here when it ships

- `viewers/caster.html` Book mode: "Download my book (JSON grammar)" gains a sibling "Save to my
  recursive.eco" that POSTs the frame (as a spread) and, via /convert, the cast path as a grammar.
- `PLAN-story-frames.md` step 3–4 become live: "My frames" dropdown from GET /api/spreads.
- Docs: DESIGN-path-caster.md "write-back" paragraph flips from "not yet" to "live".
