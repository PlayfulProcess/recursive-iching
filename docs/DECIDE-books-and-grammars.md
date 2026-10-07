# What the history says about the decisions (Oct 4 2026)

**Oct 6 2026:** the library decisions below were taken in `BEFORE-CONNECTING-TO-RECURSIVE-ECO.md`
("Decisions, Oct 6 2026"). Where they differ: `0f8f4088`'s Chinese is already inside `6efa4fc7`,
so nothing is folded; `a172fed6` stays private; the meta and the book wait.

*For PlayfulProcess. The Before-Connecting findings left six decisions open. The history of the
books (`grammars/tree-of-the-iching`, the timeline, the genealogy and the two new courses) turns
out to answer most of them, with one principle: **one book per node.** Each node of the tree is
one historical book, and where the library holds that book, it holds it as one grammar. A
language is a section inside the book, not a second grammar.*

Everything below is a recommendation. Nothing in the app was changed, and `ids.json` is still
empty.

## The history in four lines

1. **The Zhouyi** (c. 825 BCE): figures, judgments, line statements. A diviner's handbook.
2. **The Ten Wings** (c. 300–100 BCE): a later layer, in a later language, that adds yin and yang,
   the trigram cosmology and the moral reading.
3. **The Han canon** (136 BCE): the two layers fixed together as one classic, the received
   text for two thousand years.
4. **The translations** (from 1834): every one of them is also an edition. Legge printed the
   layers apart, and Wilhelm wove them together.

So the library's primary sources aren't four versions of one book. They are **three different
historical books plus one translation**, and the app has extra copies of two of them in Chinese.

## The proposal, node by node

| Node (tree) | One grammar | What happens to the others |
|---|---|---|
| Zhouyi (c. 825 BCE) | `zhouyi-core` ↔ app `6efa4fc7` (Legge, the same text; it already carries a Chinese reference section) | `0f8f4088` (Chinese only) is the same node in another language. **Fold its Chinese into `zhouyi-core` as a section**, then retire it (stays private, as a backup). |
| Ten Wings (c. 300–100 BCE) | `ten-wings` (Legge, English) | `a172fed6` (Chinese only, private) is the same node in another language. **Fold its Chinese into `ten-wings` as sections**, then leave it private. That settles "publish it or not": its content gets published inside `ten-wings`. |
| Han canon (136 BCE) | `i-ching-chinese-original` ↔ app `476b17da` | Nothing to retire. This is the received Chinese text with the Wings' images: exactly the canon node. |
| Legge (1882) | `i-ching-summarized` ↔ app `b5161d12` | The new name "The 64 Hexagrams" fits the node better than "Summarized by AI". Even better: "Legge's I Ching (1882)", so the node and the grammar share a name. |
| Human Design (1987) | `iching-hd-meta-categories` ↔ app `ad36491a` | `three-lenses-64` is a second copy of the same node: **retire it**. First its four readers move to the HD grammar (the Three Lenses course, the Path Caster, the Lenses view, the meta builder). |
| The Recursive I Ching (2026) | `meta-iching` (all lenses, per hexagram) and `the-recursive-iching-book` | Both are this library's own work. The tree is about *books*; the meta is about *hexagrams*. They don't overlap. **Import the meta** (as tarot's All Decks is imported) and **keep the book private** until stories exist. |
| *(new)* | `tree-of-the-iching` | The tree itself. Import it public as the history grammar, the way tarot's Tree of Tarot is. |

**What it costs to do all of it:**
- two data edits, folding the Chinese sections in, done over the MCP with backups;
- one rename;
- one retirement, which needs the four readers moved first;
- three imports.

About one session. The folds are the only step that touches live data, so each one starts with a
backup copy (`copy_grammar`).

**If you'd rather keep languages as separate grammars**, the alternative is to keep `0f8f4088` and
`a172fed6` as their own grammars and link them to their English twins with the cross-link pill
(their ids already line up one to one). That's more grammars and two of every node on the
timeline, and the reason to prefer it would be a reader who wants the Chinese alone.

## One book per node: which nodes can become books here

A node becomes a book in the library only when its text is in the public domain, in Brazil and in
the US.

| Node | Can it become a book here? | Why |
|---|---|---|
| Zhouyi, Ten Wings, Han canon, Legge | **Already here** | Ancient text; Legge 1882 |
| Wang Bi; Kong Yingda; Cheng Yi; Zhu Xi; the Kangxi compendium; Liu Yiming | **Yes, in Chinese** | Ancient and imperial texts. Copy from an unpunctuated old printing or a project that states its licence (ctext.org's terms need checking), never from a modern punctuated edition ◇ |
| Régis, Latin Y-King (1834) | **Yes** | 1834 |
| McClatchie (1876) | **Yes** | 1876 |
| Wilhelm, *I Ging* (1924, German) | **Probably yes** | Wilhelm died in 1930: Brazil and Germany count 70 years after death, so it has been free since 2001. In the US, works published in 1924 entered the public domain in 2020. ◇ Check the edition: later printings add Hellmut Wilhelm's material. |
| Baynes (1950) | **No** | In copyright (Bollingen). The library already removed Baynes wording once. |
| The manuscripts (Mawangdui, Shanghai, Fuyang, Guicang) | **Not yet** | The ancient text is free, but the transcriptions are modern scholarly work. Needs a source that licenses its transcription ◆ |
| Modern translations and studies | **No** | In copyright. They stay nodes with history only. |

A first round could be the **Wilhelm 1924 German**, side by side with Legge. It's the clearest
lesson in "how the translators changed the text", and the courses already point at it. Its text
would need to come from a public-domain scan, which the Desktop session can fetch.

## What needs her word

1. One book per node, languages as sections? Or keep the Chinese grammars separate and linked?
2. Retire `three-lenses-64` once its readers have moved?
3. Rename `i-ching-summarized` to "Legge's I Ching (1882)"?
4. Import the tree and the meta as public, and keep the book private?
5. Should the first new book in the library be Wilhelm's 1924 German?

## The history's own open work

The tree has 33 books. **After the check of Oct 6 2026, 6 claims are still marked ◇** (counted
across the tree's sections: ✔ 197, ○ 13, ◆ 18, ◇ 6; on Oct 5 it was ✔ 78, ○ 3, ◆ 9, ◇ 45). The
sources opened so far: Wikipedia in four languages (cited by revision), the repo's own records,
Legge's text and prefaces, and, on Oct 6, the primary texts that are online (the Hanshu, the Tang
histories, the Siku editors' notes, the prefaces of Cheng Yi, Hu Wei, the Kangxi edition and Liu
Yiming) and the journal articles that could be opened. What would settle the rest:

- **Shaughnessy, *Unearthing the Changes* (2014), pp. 52–53**: what English Wikipedia's line about
  a manuscript "found in 1987, now held by the Shanghai Library" rests on (◆ on the Shanghai node;
  the line itself is still to fix on Wikipedia).
- **Schilling, p. 371**: the German article's stone stele of 171 CE (the Han canon).
- **A date for Wang Bi's commentary**: the timeline's 245 is an estimate within his lifetime.
- **McClatchie's own book (1876)**: which Chinese text he translated. The genealogy's edge from
  the Kangxi edition is still ◇: he cites an "Imp. Ed." but prints the Wings as the school
  editions do.
- **Hon Tze-ki, "Politics, Leadership, and Wisdom" (*Monumenta Serica*, 2023)**: whether
  Wilhelm's commentary follows the Song "meanings and principles" line he learned from Lao
  Naixuan (the page was blocked).
- **Shaughnessy's dissertation itself** (Stanford, 1983): its method is known only from his own
  2022 summary.
- **The title pages of McClatchie 1876 and Wilhelm 1924**: catalogue records stand in for them now.

Richard J. Smith, *Fathoming the Cosmos and Ordering the World* (2008), the standard history, is
still unopened; no claim in the tree depends on it any more.

When a ◇ is checked, change it to ✔ with its `[@key]` in the grammar. The timeline, genealogy and
courses update by themselves, because they read the grammar live.
