# -*- coding: utf-8 -*-
"""Build grammars/meta-iching/grammar.json — "The I Ching, all lenses": one composite item per
hexagram whose `composite_of` points at that hexagram's item in every I Ching grammar in this repo,
plus the 8 trigrams as the scenery. Mirrors recursive-tarot's all-decks-many-lenses meta grammar
(items carry `composite_of` + `emergence_kind`).

The author's framing (5 Sep 2026): the hexagrams and trigrams are the SCENERY; the Human Design
lens (three-lenses-64) is the ACTION the hexagram asks of a person; the book chapter is the STORY;
Legge is the TEXT; the repair grammar is the WOUND. A cast (a path through hexagrams) is saved as a
spread-like entry, and its story is what emerges from the composites it passes through.

Sources (all in grammars/): i-ching-summarized (Judgment/Image/lines, condensed), zhouyi-core (Legge
Judgment + lines, PD), ten-wings (Legge Great Image, PD), three-lenses-64 (HD-flavoured names +
keywords; sections are empty today — the gate ACTION text is the gap to fill), repair-iching (14
hexagrams), the-recursive-iching-book (Learn/Story).

Run from the repo root:  python scripts/build_meta_iching.py && python scripts/build_collection.py
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "grammars")
OUT = os.path.join(G, "meta-iching")


def load(slug):
    p = os.path.join(G, slug, "grammar.json")
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None


def num_of(item, slug):
    md = item.get("metadata") or {}
    for k in ("number", "hexagram_number"):
        if md.get(k):
            return int(md[k])
    m = re.match(r"hex-?(\d+)", str(item.get("id", "")))
    if m:
        return int(m.group(1))
    m = re.match(r"hex(\d+)-", str(item.get("id", "")))
    if m:
        return int(m.group(1))
    return None


SOURCES = ["i-ching-summarized", "zhouyi-core", "ten-wings", "iching-hd-meta-categories", "three-lenses-64", "repair-iching", "the-recursive-iching-book"]
table = json.load(io.open(os.path.join(ROOT, "scripts", "hexagram-binary.json"), encoding="utf-8"))["hexagrams"]

items = []
by_hex = {n: {} for n in range(1, 65)}
trigrams = []
for slug in SOURCES:
    g = load(slug)
    if not g:
        continue
    for it in g["items"]:
        if str(it.get("id", "")).startswith("trigram-") and slug == "three-lenses-64":
            trigrams.append(it)
        n = num_of(it, slug)
        cid = f"{slug}::{it['id']}"
        copy = dict(it)
        copy["id"] = cid
        copy["level"] = 1
        copy["category"] = slug
        copy.setdefault("metadata", {})
        copy["metadata"] = dict(copy["metadata"] or {})
        copy["metadata"]["source_grammar"] = slug
        items.append(copy)
        if n and 1 <= n <= 64 and not str(it.get("id", "")).startswith(("sign-", "chakra-", "trigram-", "l3-", "intro", "end")):
            by_hex[n][slug] = copy

# scenery: 8 trigrams (from three-lenses, which carries them as items)
for t in trigrams:
    pass  # already copied above with category three-lenses-64

def sec(item, key):
    if not item:
        return ""
    s = item.get("sections") or {}
    return s.get(key, "") if isinstance(s, dict) else ""

composites = []
for n in range(1, 65):
    src = by_hex[n]
    summ = src.get("i-ching-summarized"); legge = src.get("zhouyi-core"); wing = src.get("ten-wings")
    lens = src.get("three-lenses-64"); repair = src.get("repair-iching"); book = src.get("the-recursive-iching-book")
    hd = src.get("iching-hd-meta-categories")
    md = (summ or {}).get("metadata") or {}
    above, below = md.get("trigram_above", ""), md.get("trigram_below", "")
    name = (summ or legge or {}).get("name", f"Hexagram {n}")
    scenery = " ".join(x for x in [f"{above.capitalize()} over {below.capitalize()}." if above and below else "", sec(wing, "Great Image (Daxiang)")] if x).strip()
    asks = ""
    if hd:
        asks = sec(hd, "Interpretation") or sec(hd, "Judgment")
        if hd.get("name"):
            asks = f"{hd['name']}. {asks}".strip()
    elif lens:
        kws = ", ".join(lens.get("keywords") or [])
        asks = f"{lens.get('name', '')}" + (f" — {kws}" if kws else "")
    composites.append({
        "id": f"hex-{n}",
        "name": f"{n} · {name}",
        "symbol": (summ or {}).get("symbol") or table[str(n)].get("symbol", ""),
        "level": 2,
        "category": "hexagram",
        "sort_order": n,
        "emergence_kind": "all-lenses",
        "composite_of": [v["id"] for v in src.values()],
        "keywords": list((summ or {}).get("keywords") or [])[:6] + list((lens or {}).get("keywords") or [])[:4],
        "sections": {
            "Scenery": scenery,
            "Text": sec(legge, "Judgment") or sec(summ, "Judgment"),
            "What it asks": asks or "(no Human Design reading yet — the gap to fill)",
            "Story": sec(book, "Story"),
            "Wound": sec(repair, "Repair Reading"),
        },
        "metadata": {
            "number": n, "binary": table[str(n)]["binary"], "trigram_above": above, "trigram_below": below,
            "lenses_present": sorted(src.keys()),
            "human_design_gate": n,   # HD gates share the I Ching numbering
        },
    })

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC BY-SA 4.0 for the composition and the repo's own texts; Legge (1882/1899) is public domain; see each source grammar for its own notice.",
        "built_by": "scripts/build_meta_iching.py",
    },
    "name": "The I Ching — All Lenses (meta)",
    "description": ("Every I Ching grammar in this repo, read together. One composite item per hexagram gathers its item from each lens: "
                    "the trigrams and the Great Image as scenery, Legge's text, the Human Design reading as what the hexagram asks of a "
                    "person, the book chapter as story, the repair reading as wound. A cast path through these is a spread; its story is what "
                    "emerges from the composites it passes through."),
    "grammar_type": "iching",
    "tags": ["iching", "meta", "all-lenses", "human-design", "composite"],
    "creator_name": "PlayfulProcess",
    "creator_link": "https://iching.recursive.eco",
    "items": composites + items,
}
os.makedirs(OUT, exist_ok=True)
io.open(os.path.join(OUT, "grammar.json"), "w", encoding="utf-8").write(json.dumps(grammar, ensure_ascii=False, indent=2) + "\n")
lens_counts = {}
for c in composites:
    for l in c["metadata"]["lenses_present"]:
        lens_counts[l] = lens_counts.get(l, 0) + 1
print("wrote meta-iching:", len(composites), "composites +", len(items), "source items; lens coverage per hexagram:", lens_counts)
