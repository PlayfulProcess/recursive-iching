# -*- coding: utf-8 -*-
"""Build grammars/hd-lines-zhouyi/grammar.json: the 384 line cells of the Human Design wheel, each paired with
the Zhouyi line statement of the same hexagram and line number, in James Legge's public-domain English.

Human Design cuts each gate (hexagram) into six lines of 0 degrees 56 minutes 15 seconds, numbered 1 to 6 in the
direction of the zodiac. The Zhouyi has six line statements per hexagram, numbered 1 to 6 from the bottom. This
grammar pairs them by number and position, nothing more. It copies no Human Design text: the Rave I'Ching's
line keynotes belong to Ra Uru Hu and are not used. The Zhouyi sentence on a cell is the Zhouyi's own, not
Human Design's.

Reads grammars/hd-mandala-wheel/grammar.json (run scripts/build_hd_wheel.py first) and grammars/zhouyi-core/
(Legge, Sacred Books of the East vol. 16, 1882; 2nd ed. 1899; public domain). Marked `_generated`, so the
importer skips it.

Run from the repo root:  python scripts/build_hd_lines.py
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "grammars", "hd-lines-zhouyi")
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius",
         "Capricorn", "Aquarius", "Pisces"]
LINE_ARCSEC = 20250 // 6          # 3375 arcseconds = 56 minutes 15 seconds
ORD = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth"}


def zodiac(arcsec):
    arcsec %= 360 * 3600
    sign, rest = divmod(arcsec, 30 * 3600)
    deg, rest = divmod(rest, 3600)
    mnt, sec = divmod(rest, 60)
    return f"{deg}°{mnt:02d}'" + (f"{sec:02d}\"" if sec else "") + f" {SIGNS[sign]}"


def main():
    wheel = json.load(open(os.path.join(ROOT, "grammars", "hd-mandala-wheel", "grammar.json"), encoding="utf-8"))
    core = json.load(open(os.path.join(ROOT, "grammars", "zhouyi-core", "grammar.json"), encoding="utf-8"))
    by_num = {n["number"]: n for n in core["nodes"] if isinstance(n.get("number"), int)}
    gates = sorted((n["metadata"] for n in wheel["nodes"] if n.get("category") == "gate"),
                   key=lambda m: m["wheel_position"])
    assert len(gates) == 64 and len(by_num) == 64
    assert LINE_ARCSEC * 6 == 20250

    nodes = [
        {"id": "note-what-this-is", "name": "What this is", "category": "note", "sort_order": 1,
         "keywords": ["human-design", "zhouyi", "lines"], "metadata": {}, "sections": {
             "The pairing": "Human Design cuts each gate into six lines of 56'15\" and numbers them 1 to 6 in the direction of the zodiac. "
                            "The Zhouyi has six line statements for each hexagram, numbered 1 to 6 from the bottom. This grammar pairs them by "
                            "number: line 3 of gate 43 here is the third line statement of hexagram 43. The pairing by number is an assumption "
                            "we make from how both systems number their lines; it is not a claim about meaning.",
             "Two different texts": "The sentence on each card is the Zhouyi's own, in James Legge's English of 1882 (public domain). It is not "
                                    "Human Design's text for that line, and the two do not say the same thing. Human Design's line texts are Ra Uru Hu's "
                                    "writing and are not used here.",
             "How to use it": "If you know a Human Design placement such as 43.3 (gate 43, line 3), find the card 'Gate 43, line 3' to read the "
                              "Zhouyi sentence for that figure and line, and the degrees where it falls. The wheel page shows the same positions.",
             "Words in brackets": "Words in (brackets) in the English are Legge's own additions to make the terse Chinese read as English.",
         }},
        {"id": "note-sources", "name": "Sources and licence", "category": "note", "sort_order": 2,
         "keywords": ["licence"], "metadata": {}, "sections": {
             "The Zhouyi in English": "James Legge, The Yi King, Sacred Books of the East vol. 16 (Oxford: Clarendon Press, 1882; 2nd ed. 1899). "
                                      "Public domain: Legge died in 1897. Read it at sacred-texts.com/ich/ or in the scan at archive.org "
                                      "(identifier wg916 for the 1882 edition, sacredbooksofchi12conf for the 1899 edition). The text in this library "
                                      "was cross-checked across three digitisations (see grammars/zhouyi-core).",
             "Positions": "From grammars/hd-mandala-wheel: the gate order is the Fu Xi circle, each gate begins at the degree given and is "
                          "5°37'30\" wide, each line 56'15\".",
             "Not used": "Human Design's gate names, keynotes and line texts; any Gene Keys text.",
         }},
    ]
    for g in gates:
        n = g["number"]
        src = by_num[n]
        for line in range(1, 7):
            start = g["start_arcseconds"] + (line - 1) * LINE_ARCSEC
            text = src["sections"].get(f"Line {line}")
            assert text, f"hexagram {n} has no Line {line} in zhouyi-core"
            sections = {
                "Place on the wheel": f"{zodiac(start)} to {zodiac(start + LINE_ARCSEC)}. Line {line} of gate {n}, in the {g['centre']} centre (the system's own grouping).",
                "The Zhouyi line (Legge, 1882)": text,
            }
            if line == 6 and src["sections"].get("All Lines"):
                sections["The extra statement of this hexagram (Legge)"] = (
                    "This is not a line. Hexagrams 1 and 2 carry one more statement, for when every line changes: "
                    + src["sections"]["All Lines"])
            nodes.append({
                "id": f"gate-{n}-line-{line}",
                "name": f"{n}.{line} · {g['title']}, line {line}",
                "category": "line",
                "sort_order": len(nodes) + 1,
                "keywords": ["line", f"gate-{n}", f"line-{line}", g["centre"].lower().replace(" ", "-") + "-centre"],
                "sections": sections,
                "metadata": {"gate": n, "line": line, "start": zodiac(start), "start_arcseconds": start % (360 * 3600),
                             "wheel_position": g["wheel_position"], "source": "zhouyi-core"},
                "image_url": None,
            })

    grammar = {
        "_generated": True,
        "_generated_by": "scripts/build_hd_lines.py",
        "_draft_note": "Oct 12 2026 draft. Skipped by recursive.eco's importer (_generated). The Zhouyi text is Legge 1882, public domain; no Human Design text.",
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "The Zhouyi line statements are James Legge's 1882 English (public domain; Legge died in 1897). The positions are arithmetic and "
                       "the arrangement and notes are CC-BY-SA-4.0 (PlayfulProcess). No Human Design or Gene Keys text is reproduced.",
            "attribution": [{"name": "PlayfulProcess", "date": "2026-10-12",
                             "note": "design and curation; generated by scripts/build_hd_lines.py, notes written with AI"},
                            {"name": "James Legge (tr.)", "date": "1882",
                             "note": "The Yi King, Sacred Books of the East vol. 16; public domain"}],
        },
        "name": "The 384 Lines on the Wheel",
        "description": "Human Design cuts each of the 64 gates into six lines of 56'15\". This grammar pairs each of those 384 cells, in wheel order, with the Zhouyi's own line statement for the same hexagram and line (Legge, 1882, public domain). No Human Design text.",
        "grammar_type": "custom",
        "default_preview": "grammar",
        "is_published": False,
        "creator_name": "PlayfulProcess",
        "tags": ["human-design", "zhouyi", "lines", "wheel", "draft"],
        "nodes": nodes,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "grammar.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(grammar, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote grammars/hd-lines-zhouyi/grammar.json ({len(nodes)} nodes)")


if __name__ == "__main__":
    sys.exit(main())
