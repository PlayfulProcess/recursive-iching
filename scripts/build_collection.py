# -*- coding: utf-8 -*-
"""Build grammars/_collection.json for The Recursive I Ching — the collection-index
file the ported viewers (cards.html, explorer.html, lenses.html, tree-viewer.html,
timeline.html) read to discover every grammar in this repo, in the SAME schema
recursive-tarot/tarot/_collection.json and recursive-astrology/grammars/_collection.json
use (only the root path differs: grammars/ here). Port of
recursive-astrology/scripts/build_collection.py, itself a port of recursive-tarot's
build_tarot_collection.py + refresh_collection.py, collapsed into one script since this
repo has no separate "migrate from source repo" step — the grammars already live in
grammars/*/grammar.json.

The grammar files are the source of truth for name/type/items/cover_image_url/blurb;
this script only ADDS curation this repo doesn't otherwise have anywhere (branch
grouping + a historical year where a grammar actually has one). Unlisted / future
grammars still get included automatically (glob-driven, no hardcoded slug list to fall
out of date) — they just land in the "synthesis" branch with no year, which reads
honestly as "undated / contemporary" rather than inventing a false date.

Run from the repo root:  python3 scripts/build_collection.py
"""
import json
import os
import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GRAMMARS_DIR = os.path.join(ROOT, "grammars")
OUT = os.path.join(GRAMMARS_DIR, "_collection.json")

REPO = "PlayfulProcess/recursive-starter"
BRANCH = "main"

BRANCHES = [
    ("primary-sources", "Primary Sources — the classical text itself, in translation"),
    ("synthesis",        "Synthesis — cross-lens readings of the 64 hexagrams"),
    ("readings",         "Readings — thematic contemplative practices, not interpretation sets"),
]

# slug -> branch id. Curated by hand (mirrors tarot's DECKS dict / astro's BRANCH_OF)
# but NOT load-bearing: any grammar not listed here still appears in the collection,
# just in "synthesis" with no curated year — an honest "undated" default, never a guess.
BRANCH_OF = {
    "i-ching-summarized":     "primary-sources",
    "i-ching-chinese-original": "primary-sources",
    "zhouyi-core":            "primary-sources",
    "ten-wings":              "primary-sources",
    "three-lenses-64":        "synthesis",
    "repair-iching":          "readings",
}

# slug -> (sortable year, display label, provenance). Only the classical text itself
# has a genuine ancient anchor; the derived lens/reading grammars are honestly
# "living" (contemporary synthesis, not a historically dated artifact).
YEARS = {
    "i-ching-summarized": (
        -1000,
        "Zhou I Ching, compiled c. 1046–256 BCE · this English condensation's own translation lineage is undocumented",
        "record",
    ),
    "i-ching-chinese-original": (
        -1000,
        "Zhou I Ching, compiled c. 1046–256 BCE · classical Chinese, Project Gutenberg ebook #25501, no translation layer",
        "record",
    ),
    "zhouyi-core": (
        -825,
        "Zhouyi core (Judgment + Line statements), late Western Zhou, c. 9th century BCE (Shaughnessy) · English: James Legge 1882, public domain",
        "record",
    ),
    "ten-wings": (
        -250,
        "Ten Wings, Confucian school, late Warring States–early Han, c. 350–100 BCE · English: James Legge 1882, public domain",
        "record",
    ),
}


def blurb_of(g):
    desc = (g.get("description") or "").strip().split("\n")[0]
    return (desc[:200] + "…") if len(desc) > 200 else desc


def main():
    paths = sorted(glob.glob(os.path.join(GRAMMARS_DIR, "*", "grammar.json")))
    grammars_index = []
    for path in paths:
        slug = os.path.basename(os.path.dirname(path))
        try:
            g = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            print(f"  SKIP {slug}: {e}")
            continue
        branch = BRANCH_OF.get(slug, "synthesis")
        entry = {
            "slug": slug,
            "name": g.get("name"),
            "type": g.get("grammar_type"),
            "branch": branch,
            "is_meta": False,
            "default_preview": g.get("default_preview"),
            "items": len(g.get("items", [])),
            "cover_image_url": g.get("cover_image_url"),
            "blurb": blurb_of(g),
            "path": f"grammars/{slug}/grammar.json",
            "provenance": "living",
        }
        if slug in YEARS:
            year, label, provenance = YEARS[slug]
            entry["year"] = year
            entry["year_label"] = label
            entry["provenance"] = provenance
        grammars_index.append(entry)

    branch_index = [
        {"id": bid, "name": bname,
         "deck_slugs": [e["slug"] for e in grammars_index if e["branch"] == bid]}
        for bid, bname in BRANCHES
    ]

    collection = {
        "repo": REPO,
        "branch": BRANCH,
        "github_url": f"https://github.com/{REPO}",
        "collection": "iching",
        "name": "The Recursive I Ching",
        "version": "1.0.0",
        "license": "Mixed — see each grammar's own `license` field (public-domain classical text; original synthesis/interpretation CC-BY-SA-4.0)",
        "original_creator": None,
        "creator_name": "PlayfulProcess",
        "meta_grammar": "i-ching-summarized",
        "branches": branch_index,
        "grammars": grammars_index,
    }
    json.dump(collection, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n_items = sum(e["items"] for e in grammars_index)
    print(f"Wrote {OUT} — {len(grammars_index)} grammars ({n_items} items), {len(branch_index)} branches")


if __name__ == "__main__":
    main()
