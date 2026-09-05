# Book mode — reader's UX review

*5 September 2026. Live: `iching.recursive.eco/viewers/caster.html`, "Cast your Book". Walked twice —
desktop 1280×720 and mobile preset 375×812. Nothing modified. Numbers below are measured document
offsets, not estimates.*

---

## 1. Scrolling and struggle

**The advance control is never near the thing being read.** "Next step" lives in `.statusbar`,
`position: static`, at document y=742 — *above* the reading area, under the settings panel. The book
renders below it and grows downward. Nothing on the page is sticky except the site header.

**There is no auto-scroll.** Verified twice: at scrollY 3100 I pressed Next; the connector and new
card rendered at 3258 and 3343 and scrollY stayed at 3100. The page never moves toward new content.

Round trip to advance one hexagram:

| | up to reach "Next" | back down to the new card | total |
|---|---|---|---|
| Desktop | ~2,360 px | ~2,600 px | ~5,000 px |
| Mobile (375) | 1,907 px (2.3 screens) | 2,863 px (3.5 screens) | ~4,770 px ≈ **5.9 phone screens** |

It worsens every step: the document grows, the button stays at 742.

**The worst moment is on the phone.** The first card ends at y=3783 and the *site footer* begins
immediately — the reader finishes the transition box and the next thing on screen is a spiral logo,
"One branch of a larger tree", and a newsletter signup. No Next button, no hint. The book looks over
after one hexagram.

The settings panel (254 px on mobile) and mode pills stay expanded forever; with the hero and honesty
box that is **1,113 px of chrome above the book on mobile**, re-traversed every step.

Fix: put the advance control at the **foot of the current card**, keep a slim sticky bar as backup,
`scrollIntoView` the new connector on advance, and collapse the settings to one line after Begin.
Explore mode already has the right instinct — there the control *is* the card (tap a line to flip it).

## 2. Reading flow

Rendered order: intro (1,073 px desktop / 1,809 px mobile) → card → LEARN → STORY → YOUR TRANSITION →
connector → next card.

**The connector is in the wrong place.** It reads `LINE 5 CHANGES (FROM HEXAGRAM 22)` — it belongs to
the card being *left*, but sits after that card's transition box. The reader is asked "what were you
carrying when this line changed?" **before being shown which line changed or what it says.** It should
be the tail of the previous card — what changed and why you are leaving — with the box after it. The
Markdown export has the same ordering.

**The blank Story is over-weighted.** Same size and italic as real content, in the same slot every
time; four cards running said the identical paragraph. It reads as a defect, not an invitation. Make
it one quiet line — "No story here yet. Write one." — as a button, not a paragraph.

Hierarchy otherwise works: serif name, diagram numbered 6→1, Judgment, italic gloss, dashed rule, red
small-caps labels. It looks like a book. Cards are 855 px on mobile, so one never fits one screen.

Minor: the arrival card (Hexagram 1) also gets a transition box, though nothing changes out of it.

## 3. The transition box

Placement (last in the card) is right, and the prompt — *"What were you carrying when this line
changed? What did the text make you think of? Nothing, if nothing came."* — is the best copy on the
page; don't shorten it. It is 2 rows / 74 px and does **not** auto-grow, so past ~90 characters you
type into a two-line window. Make it grow.

Don't collapse it or make it feel optional — the intro calls it "the part of this book that matters
most". But **echo the reader's words into the connector**: the connector prints only the 3,000-year-old
line text; printing their sentence beneath it is what turns a cast sequence into their book.

Persistence is broken — see §7.

## 4. The Gautama weave

Each of the 66 items in `grammars/the-recursive-iching-book/grammar.json` carries
`sections: {Learn, Story}` and `metadata: {number, binary, trigram_above, trigram_below,
chinese_name, pinyin, story_written}` — all 64 hexagrams have `story_written: false`. The trigram
fields are already the hooks the design doc needs. Proposed shape:

```
sections: { Meeting, Story, School, Terreiro, Exits: {Line 1..6} }
```

In one card, in this order:

1. **LEARN** — unchanged (Image + trigram meeting). Always open.
2. **THE MEETING** — one always-open line: "Mountain over Fire — stone meeting the first oxidation."
   The hook that makes the chapter worth opening.
3. **STORY** — the ordinary-world scene: first **~120 words inline**, then a `Read the chapter ▾`
   disclosure. Never a modal or a new page; the reader must not lose the path.
4. Inside the expansion, **The school** and **The terreiro** as two quiet labelled sub-blocks below
   the scene, using the existing small-caps labels so they read as apparatus. A reader who wants only
   the novel stops at the scene.
5. **The exit** — the line text at the foot of the card (§2).

A 1,200–1,500-word chapter is ~4 phone screens: inline-by-default makes each step a 7-screen wall,
collapsed-by-default hides the novel. First 120 words plus expand is the only version that survives
both.

## 5. Letting readers write and create in the page

Nothing supports this yet beyond the transition boxes. Missing: **(a)** the blank Story is inert text,
not a `Write the story for this hexagram` button opening a textarea in place; **(b)** the intro and end
framecards are fixed and unwritable; **(c)** there is no account, library write or server — everything
is a file download; **(d)** no share link, print stylesheet, cover or title field.

**MVP:** make every block editable in place (transition, story, opening, closing); persist under a
stable book id, not the path string; add a "My book" title field; add a **Print** button calling
`window.print()` against a `@media print` sheet that hides site chrome, settings and blank Stories.
That is a printable personal edition with no backend. Sharing needs the grammar library — second step.

## 6. Save / print

Both buttons appear only in the completion banner at the very bottom (y=5659), 943 px below the start
of the closing text.

**"Save as my grammar" is misleading.** `saveAsGrammar()` calls `downloadText(...json)` — it downloads
`my-iching-book-22-to-1.json`. The label promises a save into the recursive.eco library ("*my*
grammar"), as does the intro ("save the whole walk … as a grammar of your own"). A reader will assume
it went somewhere. Rename to **"Download my book (.json)"** until a real library write exists.

Markdown is the right print hand-off and `buildBookMarkdown()` is well shaped (title, cast date,
intro, per-step changing line / Judgment / Learn / Story / My transition, closing) — but Markdown is a
developer's format. Most readers want paper: add the Print button above.

## 7. Bugs

1. **Auto-advance destroys Book mode.** With it on I focused a transition box and typed; within 7
   seconds the book ran to the end (Step 0 of 2 → Step 2 of 2, 3 cards) and **focus was stolen from
   the textarea**. Text survived, but the reader is thrown out mid-sentence and the book finishes
   without them. Remove it from Book mode, or suspend it while a textarea has focus.
2. **A reload destroys the book.** Mode resets to Explore, 0 cards, no path. No URL state, no resume.
3. **Notes are orphaned.** `localStorage['iching-book-notes-v1']` is keyed by the full path string —
   `{"101001>101011>101111>111111":{"1":"…"}}`. Notes survive the reload; the path does not, and a
   random cast will never reproduce it. The reader's words become unreachable forever — the most
   damaging bug here, given what the intro promises about them.
4. **The default state is a zero-length book.** Book mode opens with origin = Hexagram 1 = the fixed
   destiny, "0 steps", "Origin and destiny are the same hexagram." Begin is **not** disabled: pressing
   it yields Step 0 of 0, one card, and the "Arrived. Your book is complete" banner with both download
   buttons. Auto-cast on entering Book mode, or disable Begin until an origin is cast.
5. **`[cite: 3]` leaks into reader prose** — visible in the Hexagram 18 gloss ("…restore health and
   order. [cite: 3]"). 10 occurrences in `grammars/i-ching-summarized/grammar.json`.
6. **The floating AI assistant overlaps the transition box** on mobile — the sparkle sits on the right
   edge of the textarea; an accidental tap opens a panel covering half the page.
7. Typo: the blank-Story paragraph uses a hyphen — "save the grammar - that is how" — where the rest
   of the prose uses em dashes.
8. Console otherwise clean: no errors, only `[assistant-embed] auth bootstrap {state: none}`, logged
   twice.

## 8. Priorities

1. **Move "Next step" to the foot of the current card** and `scrollIntoView` the new connector —
   removes ~5,000 px of scrolling per hexagram and rescues the phone reader who currently hits the
   site footer and thinks the book ended (`.statusbar` → per-card footer).
2. **Key notes to a stable book id, not the path string, and restore the book on reload** — otherwise
   every reader loses the writing the intro told them mattered most (`iching-book-notes-v1`).
3. **Move the changing-line connector to the end of the previous card, above the transition box**, so
   the reader knows what changed before being asked what they carried when it did (`.connector`).
4. **Remove Auto-advance from Book mode** — it finishes the book while the reader is typing
   (`#auto-btn`).
5. **Rename "Save as my grammar" to "Download my book (.json)" and add a Print button** with a
   `@media print` sheet — the current label promises a save that does not happen (`#save-btn`).

*Not tested: the downloaded .json and .md files (buttons inspected in source, not opened); yarrow
randomness; Direct vs Wandering; the Courses and Grammars views.*
