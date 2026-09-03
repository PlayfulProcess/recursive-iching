# Field report — running REPLICATE-THE-PATTERN.md on a third site (I Ching)

This is an honest account of following `recursive-tarot/docs/REPLICATE-THE-PATTERN.md`
as the sole process authority to build The Recursive I Ching from `recursive-starter`
(previously an unrelated Next.js scaffold, wiped to `.git` only). The playbook was
largely right and largely sufficient — most of the checklist executed exactly as
written, with zero drama, for `cards.html` and `tree-viewer.html` in particular (both
copied byte-identical in structure from `recursive-astrology`, which itself copied
them byte-identical from `recursive-tarot` — confirmed by diffing all three). But five
places were genuinely ambiguous, one place was actively wrong, and several places
would have stopped a non-developer cold. This is a specific list of what to fix in the
playbook, not a generic "went fine" report.

## Where the playbook was sufficient (worked exactly as written)

- The Prime Rule itself — copy, change 4 things, never structure — is the right
  instinct and caught itself working: every color hex, every `astrology`→`iching`
  string, every `2f5d8a`→`9c3b2a` swap was mechanical and verifiable by diffing before
  and after. No original judgment calls were needed for `site-header.js`'s dropdown
  gap-fix, `site-footer.js`'s newsletter widget, `icons.js`, `grammar-loader.js`,
  `deck-picker.js`, `eco-links.js`, or `dimension-engine.js` — copy, rebrand, done.
- The `grammars/<slug>/grammar.json` + `scripts/build_collection.py` +
  `grammars/_collection.json` pattern (step 1) worked with a straight port of astro's
  script, trimmed to this repo's 3-grammar, 3-branch reality.
- The multi-course, manifest-driven `course-viewer.html` pattern (explicitly sourced
  from astro per the brief) worked with only the expected relabeling —
  `chapterIdPrefix`/`appendixIdPrefix` cleanly expressed "the 64 hexagram-gates are
  chapters, the 3 meta-syntheses are the appendix, the other 27 items in the source
  grammar are neither" as data, not code.
- Playwright verification against a local static server caught real things worth
  catching in a prior draft (see below) and confirmed the header dropdown gap-fix
  actually survives the cursor crossing the gap (`openAfterHover` and
  `openAfterCrossingGap` both `true`), not just a hover snapshot.

## 1. The Prime Rule doesn't say what to do when the "mother pattern" has already forked

By the third site, there isn't one obvious "the working file" — there are two, and for
several files they disagree. `cards.html` and `tree-viewer.html` are identical across
all three repos (no ambiguity). But `explorer.html`, `timeline.html`, and especially
`lenses.html` are **not**: astro's changelog documents real logic rewrites (its own
`BRANCH_COLOR` taxonomy, its own pivot presets replacing tarot's arcana/suit/rank ones,
its own cross-grammar matching strategy). The brief for this session explicitly named
astro's `course-viewer.html` as the copy source (for the multi-course pattern) but
was silent on `explorer`/`timeline`/`lenses` — the checklist phrasing ("copy tarot's
tree... viewers/ cards+explorer+lenses+tree+timeline") reads as if tarot is the source
for all five.

**What I did:** treated astro's already-generalized versions as the copy source for
`explorer.html`/`timeline.html`/`lenses.html` too, reasoning that re-deriving the same
generalization from tarot's arcana-specific original would just reproduce astro's
already-validated solve through a different, more expensive route. I think this was
the right call, but it's a judgment call the playbook doesn't license.

**Fix the playbook should make:** amend the Prime Rule: *"'the working file' means the
closest already-generalized version anywhere in the family, not always literally
tarot's. Check every existing sibling site before copying from the mother repo — if a
second site already solved the exact generalization your new site needs (de-tarot-
ifying a card-specific concept), copy THAT solve. Only fall back to tarot's original
when no sibling has generalized it yet."*

## 2. `lenses.html` has no generic mother-repo version — the checklist implies one exists

Tarot does not have a first-class `viewers/lenses.html`. It has
`viewers/prototypes/lenses.html`, which is deeply coupled to tarot's stamped
`metadata.trump_key`, a 40+-deck picker, and a `research/synthesis/trumps.json`
cross-deck-evolution file — none of which exist or make sense for a 3-grammar
collection. The actual generic, copyable `lenses.html` only exists because astro
built it from scratch (its own changelog calls it "real logic rewrite," not a port).

A builder following the checklist's step 3 ("copy `index.html`... and `viewers/`
(cards, explorer, lenses, tree, timeline)") literally, against tarot, would open
`viewers/lenses.html`, get a 404/file-not-found, and have no instruction for what to
do next.

**Fix:** the checklist should say explicitly: *"`lenses.html` has no canonical
tarot-sourced version — as of the astro port, copy astro's version instead, and expect
to rewrite its cross-grammar matching key for your domain (see #3 below)."*

## 3. Cross-grammar matching keys are domain-specific, and picking the wrong one fails silently

This was the one place I made a real logic change, not a re-skin — and it's the
single biggest thing the playbook is silent on.

- Tarot matches cards across decks with a stamped `metadata.trump_key` (identical
  Rider-Waite-derived numbering baked into every deck at import time).
- Astro matches by normalized item **name** — valid because astrology entities are
  named identically everywhere ("Saturn" is "Saturn" in Ptolemy, Alan Leo, and the
  flagship set).
- **Neither works for I Ching.** I checked: of the 64 hexagram names shared between
  just two of this repo's own source files (`iching-hexagrams.json` vs
  `i-ching-chinese-original-with-brief-translation/grammar.json`), **31 of 64 (48%)
  differ** even though they're the same hexagram in the same numbering (e.g. "Waiting"
  vs "Waiting (Nourishment)", "Holding Together" vs "Holding Together [Union]"). Name
  matching would under-match roughly half the collection.
- The real shared key is the hexagram **number**, 1–64 — except even that isn't stored
  under a consistent field name: `i-ching-summarized` uses `metadata.number`,
  `repair-iching` uses `metadata.hexagram_number`. A naive "use metadata.number" fix
  would have silently failed to match `repair-iching`'s 14 items to anything.

**What I did:** rewrote `lenses.html`'s `entityKey()` to check both metadata field
names for a numeric hexagram key, falling back to normalized name only for
non-hexagram items (the lens grammar's sign/chakra/trigram items, which have no
number). This is a real code change, and the Prime Rule's "never change structure"
framing doesn't obviously permit it — but leaving it unfixed would have made the
Lenses viewer non-functional for its one job (I tested: with the original name-only
key, `repair-iching`'s "Hexagram 6 · 訟 Sòng · Conflict" would never match
`i-ching-summarized`'s "Conflict" at all).

**Fix the playbook should make:** the Prime Rule needs an escape valve distinguishing
*"the copied file's core algorithm encodes an assumption about your domain's data that
doesn't hold"* from *"I think this could be nicer."* The former is not scope creep;
refusing to fix it ships a viewer that's cosmetically present but functionally inert.
Suggested addition to step 3: *"Before copying a matching/joining algorithm (Lenses'
entity key, Timeline's date field, Tree's composite_of expectations), verify your
domain's data actually satisfies the assumption the algorithm makes. If it doesn't,
fixing the join key is glue, not a rebuild — but write down that you did it and why."*

## 4. The playbook's "if X exists, lift it; if not, Y is the flagship" was neither branch — reality had three candidates of very different quality

The brief said: *"If a full 64-hexagram book grammar exists in those sources, lift it;
if not, the three-lenses grammar IS the flagship — do not hand-write 64 hexagrams."*
In `recursive.eco-schemas` there were actually **three** 64-hexagram-adjacent files:

1. `iching/i-ching-chinese-original-with-brief-translation/grammar.json` — canonical
   `items[]`/`sections{}` shape, but its `sections` are still classical **Chinese**
   text — the "brief translation" its own description promises only landed in the
   English `name` field (e.g. `name: "The Creative"`), not the section bodies. A
   non-Chinese-reading visitor gets a wall of hanzi.
2. `iching/iching-hexagrams.json` — genuinely useful English content (Judgment, all
   six line meanings, an interpretation gloss) — but **not** in the canonical shape
   (`hexagrams[]` array with `judgment`/`lines`/`image_text` as flat top-level item
   fields, not `items[]`/`sections{}`). Needed real conversion, not a lift.
3. Two copies of the "three-lenses" grammar (one in `grammars/`, one in `iching/`) —
   both **100% empty** `sections` on all 94 items (verified: every single item, not a
   sample). Despite the name implying rich "meta-category" content per the schemas
   repo's own documented L1/L2/L3 level system, it's a naming skeleton with zero
   interpretive text.

**What I did:** converted file #2 into the canonical shape (mechanical field
remapping — `judgment`→section "Judgment", `lines[].meaning`→section "Line N",
`interpretation`→section "Interpretation" — no invented text), merged in the unicode
hexagram `symbol` glyph from file #1 by hexagram number, and used the result as the
flagship. Used file #3 (renamed to `three-lenses-64`) only for the course, as
instructed, with its emptiness disclosed rather than papered over.

**Fix:** the playbook's phrasing treats "does a flagship exist" as a boolean. It
should instead say: *"expect multiple candidate files of uneven quality; check each
for (a) canonical shape vs. needs-conversion, (b) whether `sections` actually has
content or is empty/skeletal, (c) whether its own description's claims match its
actual data. A file that LOOKS canonical-shaped but has no real content is worse than
a non-canonical file with real content — you'll need to convert the latter regardless,
so its shape isn't disqualifying."*

## 5. `schemas/iching/` (the path the brief pointed at) was functionally empty — the real content was one level up

The brief said to check `schemas/iching/` as a fallback source. That directory
contains a `README.md`, one `example-hexagram-01.json` (an illustrative schema, not
real content), and four subdirectories (`summary-ai/`, `human-design/`,
`human-design-iching/`, `chinese-and-summary/`) that are **completely empty** — no
files at all. The real, usable content (all three files discussed in #4) lives one
level up, in a **top-level `iching/` directory**, a sibling of `schemas/` rather than
inside it — not where the brief's wording pointed.

**Fix:** recommend explicitly checking both `schemas/<domain>/` (often a stub/template
directory) and a top-level `<domain>/` directory if one exists (often where actual
working sessions dumped content) before concluding a domain has no usable source
material in the schemas repo.

## 6. Two "copy this file" instructions disagreed on a shared mechanism

The brief said "assistant mount as tarot pages do" (tarot's inline `#assistant-toggle`
button + lazy iframe, present verbatim in `cards.html`/`tree-viewer.html` since those
are unchanged across all three repos) — but also said to copy astro's
`pages/course-viewer.html` for the multi-course pattern. Astro's course-viewer was
**already refactored** (its own Jul 7 changelog documents this) to use the newer
shared `assistant.js` loader instead of the inline block. Untangling that to
reintroduce the deprecated inline pattern would mean fighting the very file I was
told to copy verbatim.

**What I did:** left astro's course-viewer.html's `assistant.js` mount as-is (Prime
Rule: copy the working file), so this repo now has two different assistant-mount
mechanisms depending on which page you're on (inline block on cards/tree-viewer,
`assistant.js` loader on course-viewer) — functionally equivalent to the visitor, but
inconsistent under the hood.

**Fix:** when two playbook instructions each say "copy file X verbatim" and X and a
different named file Y disagree on a shared mechanism, the playbook should say which
wins, or say "flag the conflict rather than silently resolving it" (which is what I
did here, explicitly, rather than picking one and hiding the seam).

## 7. Links to instruments/pages the mother repo has that the new repo doesn't ship silently 404 on click — the verify step doesn't catch this

Tarot ships `genealogy.html` (deck lineage) and a casting instrument
(`viewers/caster.html` / `caster-studio.html`). Astro ships neither by name but the
files it ported (mechanically, unedited in these spots) still **contained hrefs
pointing at them** — `viewers/cards.html`'s lens-menu had a "View as Genealogy" option
linking to `../genealogy.html`; `viewers/tree-viewer.html` had a "Get a Reading"
button linking to `caster.html`; `view-switcher.js` had a dead `?lens=genealogy`
deep-link target. None of these are things the checklist's own verify step (page
loads at 200, no console errors, collection loads) would catch — **a page 404s only
on click**, and the checklist's Playwright pass only checks page loads. I found these
three by manually grepping for `genealogy`/`caster` after finishing the port, not
because the playbook told me to.

I removed all three (hid the button, dropped the menu option and its NAV entry)
rather than build the missing instruments — consistent with "site-specific
instruments are additions, never required," but the *removal* itself isn't something
the checklist calls for; it just says instruments are optional additions, not that the
ported chrome might reference optional instruments the new repo doesn't have.

**Fix:** add to the verify step: *"grep every copied file for hrefs to pages the
mother repo ships that yours doesn't (`genealogy.html`, `wheel.html`, `caster.html`,
`viewer/*-viewer.html`, or whatever your specific mother repo's extra instruments
are) — a 200 status and zero console errors on page LOAD does not catch a link that
only 404s on click."*

## 8. Minor: the target repo's own name doesn't match the site's brand

`recursive-starter` (the actual GitHub repo name, a leftover from its previous life as
an unrelated Next.js scaffold) is what every ported page's GitHub link points at and
displays — while the site brands itself "The Recursive I Ching" everywhere else. The
playbook doesn't mention whether the target repo should be renamed to match. This
session left it as `recursive-starter` since renaming a GitHub repo is outside a
write-files-only session's scope (and is arguably the orchestrator's/builder's call),
but flagging it: every ported page's footer/header GitHub link now reads oddly
("recursive-starter" next to a page titled "The Recursive I Ching").

**Fix:** add a step-0 note: *"if the target repo's existing name doesn't match the new
site's brand, decide explicitly whether to rename it (GitHub Settings → repository
name) before publicizing the site — every ported chrome file hardcodes the repo name
into its GitHub link, so a rename after the fact means re-touching all of them (or,
better, parameterizing the repo name — currently it's a hardcoded string in
`site-header.js`, `site-footer.js`, `index.html`, and every viewer, not a token)."*

## What a non-developer would have gotten stuck on, concretely

1. Searching `recursive.eco-schemas` for I Ching content and finding four
   similarly-named grammar files across three directories, several of which are empty
   stubs — with nothing in the playbook to say "check content quality and canonical
   shape, not just whether a file with the right name exists."
2. Opening `recursive-tarot/viewers/lenses.html`, finding it doesn't exist, and having
   no next step (it's at `prototypes/lenses.html` and is unusable as-is for a new
   domain).
3. Not noticing that `entityKey()` (or any matching/joining logic in a copied file)
   encodes a domain assumption — shipping a Lenses viewer that "loads fine" but never
   actually cross-matches anything, with no error to signal the failure.
4. Not noticing empty `sections`/missing `composite_of` in a lifted grammar until
   *after* wiring up the course/tree viewer and finding the content pane blank — the
   playbook's "lift it" language doesn't prompt a content-completeness check first.
5. Declaring victory after Playwright shows 200s and no console errors, without
   grepping for hrefs to instrument pages (genealogy/caster/wheel) that the mother
   repo has and the new repo doesn't — those only fail when a real visitor clicks them.

## Summary of concrete playbook edits proposed

1. Prime Rule: "the working file" = closest already-generalized sibling, not always
   literally tarot's.
2. Step 3: flag that `lenses.html` has no tarot-native generic version; astro's is the
   current copy source, and its matching-key logic must be re-verified per domain.
3. New guidance: distinguish "the copied algorithm's domain assumption is false"
   (fix it, document it) from "I think this could be nicer" (don't).
4. Step 1: "does a flagship exist" is not boolean — check shape AND content
   completeness AND whether the file's own claims (description, naming) match its
   actual data.
5. Step 1: check both `schemas/<domain>/` and a top-level `<domain>/` directory.
6. Note: when two "copy verbatim" instructions conflict on a shared mechanism, say
   which wins or flag it explicitly rather than silently resolving it.
7. Step 6 (verify): grep for hrefs to mother-repo-only instrument pages, not just page
   load status.
8. Step 0: decide explicitly whether the target repo needs a rename to match brand.
