# -*- coding: utf-8 -*-
"""Build grammars/the-recursive-iching-book/grammar.json.

The book = a fixed beginning + a fixed end (grammars/the-recursive-iching-book/frame.json, hand-written)
+ one item per hexagram carrying what the site knows about it (Learn: the two trigrams meeting + the
Image; Story: the chapter for that hexagram, or an honest blank) so that viewers/caster.html's Book
mode can assemble a cast path into a readable book.

Sources: grammars/i-ching-summarized/grammar.json (Image, trigrams, names) and
scripts/hexagram-binary.json (the VERIFIED binary - never the summarized grammar's own binary field).

Stories: put chapter text in grammars/the-recursive-iching-book/stories/<NN>.md (NN = 01..64). Any
file present is folded in as that hexagram's Story; absent = the honest blank.

Run from the repo root:  python scripts/build_book_grammar.py
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "grammars", "the-recursive-iching-book")
SUMM = os.path.join(ROOT, "grammars", "i-ching-summarized", "grammar.json")
BIN = os.path.join(ROOT, "scripts", "hexagram-binary.json")
STORIES = os.path.join(G, "stories")


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


frame = load(os.path.join(G, "frame.json"))
summ = load(SUMM)
table = load(BIN)["hexagrams"]

by_num = {}
for it in summ["items"]:
    n = (it.get("metadata") or {}).get("number")
    if n:
        by_num[int(n)] = it

BLANK = ("This hexagram's story has not been written yet. The book is being written one casting at a "
         "time. If a story came to you here, write it in your transition below and save the grammar - "
         "that is how this book gets written.")


def story_path(n):
    return os.path.join(STORIES, "%02d.md" % n)


def story_for(n):
    p = story_path(n)
    if os.path.exists(p):
        t = io.open(p, encoding="utf-8").read().strip()
        t = re.sub(r"^#.*\n+", "", t)  # drop a leading heading if present
        return t
    return BLANK


items = [{
    "id": "intro",
    "name": frame["intro"]["name"],
    "symbol": "☯",
    "category": "frame",
    "sort_order": 0,
    "sections": {"Text": "\n\n".join(frame["intro"]["text"])},
    "keywords": ["beginning", "how to cast", "frame"],
    "metadata": {"role": "intro"},
}]

for n in range(1, 65):
    s = by_num.get(n, {})
    md = s.get("metadata") or {}
    entry = table[str(n)]
    above = md.get("trigram_above") or ""
    below = md.get("trigram_below") or ""
    image = (s.get("sections") or {}).get("Image", "")
    meeting = ("%s over %s. " % (above.capitalize(), below.capitalize())) if above and below else ""
    learn = (meeting + image).strip()
    items.append({
        "id": "hex-%d" % n,
        "name": s.get("name") or entry.get("name") or ("Hexagram %d" % n),
        "symbol": s.get("symbol") or entry.get("symbol") or "",
        "category": "hexagram",
        "sort_order": n,
        "sections": {"Learn": learn, "Story": story_for(n)},
        "keywords": list(s.get("keywords") or [])[:8],
        "metadata": {
            "number": n,
            "binary": entry["binary"],
            "trigram_above": above,
            "trigram_below": below,
            "chinese_name": md.get("chinese_name", ""),
            "pinyin": md.get("pinyin", ""),
            "story_written": os.path.exists(story_path(n)),
        },
    })

items.append({
    "id": "end",
    "name": frame["end"]["name"],
    "symbol": "䷀",
    "category": "frame",
    "sort_order": 65,
    "sections": {"Text": "\n\n".join(frame["end"]["text"])},
    "keywords": ["end", "the Creative", "recognition"],
    "metadata": {"role": "end", "number": 1},
})

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": ("CC BY-SA 4.0 (PlayfulProcess) for the frame, the Learn composition and any stories; "
                    "the underlying I Ching text is public domain; the condensed English Image lines are "
                    "from this repo's i-ching-summarized grammar (same licence)."),
        "built_by": "scripts/build_book_grammar.py",
    },
    "name": frame["title"],
    "description": frame["description"],
    "cover_image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/I-Ching-chinese-book.jpg",
    "grammar_type": "book",
    "tags": ["iching", "book", "path-caster", "combinatorial", "cast-your-book"],
    "creator_name": "PlayfulProcess",
    "creator_link": "https://iching.recursive.eco/viewers/caster.html",
    "items": items,
}

out = os.path.join(G, "grammar.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(grammar, ensure_ascii=False, indent=2) + "\n")
written = sum(1 for it in items if it["category"] == "hexagram" and it["metadata"]["story_written"])
print("wrote", out, "-", len(items), "items;", written, "of 64 stories written")
