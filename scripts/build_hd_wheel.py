# -*- coding: utf-8 -*-
"""Build grammars/hd-mandala-wheel/grammar.json: the 64 gates in the order of the Human Design wheel
(the "Rave Mandala"), with only facts that can be checked:

  * the order of the gates round the wheel (a list below, checked by this script against the binary
    table in scripts/hexagram-binary.json: it must be the Fu Xi / Shao Yong circle);
  * where each gate begins in the zodiac (arithmetic from two numbers: the wheel starts at 2 degrees
    Aquarius and each gate is 360/64 = 5 degrees 37 minutes 30 seconds wide);
  * the opposite gate (the one directly across the wheel; its figure is this one with every line flipped);
  * the hexagram's own facts (King Wen number, name, trigrams) from the repo's tables;
  * the centre each gate belongs to (the system's own rule; see _grammar_commons.sources).

It copies no Human Design text: the gate names, keynotes, line texts and descriptions of Ra Uru Hu's
Rave I'Ching are not used. Marked `_generated`, so recursive.eco's importer skips it until PlayfulProcess
decides what it becomes (docs/BEFORE-CONNECTING-TO-RECURSIVE-ECO.md, "Decisions, Oct 6 2026").

Run from the repo root:  python scripts/build_hd_wheel.py   (before build_collection.py)
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "grammars", "hd-mandala-wheel")

# The wheel, starting at gate 41 (2 degrees Aquarius) and running round the zodiac.
WHEEL = [41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16, 35, 45,
         12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50, 28, 44,
         1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60]

START_ARCSEC = (300 + 2) * 3600          # 2 degrees Aquarius = 302 degrees of ecliptic longitude
GATE_ARCSEC = 360 * 3600 // 64           # 20250 arcseconds = 5 degrees 37 minutes 30 seconds
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius",
         "Capricorn", "Aquarius", "Pisces"]

CENTRES = {
    "Head": [64, 61, 63], "Ajna": [47, 24, 4, 17, 43, 11],
    "Throat": [62, 23, 56, 35, 12, 45, 33, 8, 31, 20, 16], "G": [1, 13, 25, 46, 2, 15, 10, 7],
    "Heart": [21, 40, 26, 51], "Spleen": [48, 57, 44, 50, 32, 28, 18],
    "Solar Plexus": [6, 37, 22, 36, 49, 55, 30], "Sacral": [5, 14, 29, 59, 9, 3, 42, 27, 34],
    "Root": [53, 60, 52, 19, 39, 41, 58, 38, 54],
}
CENTRE_OF = {g: c for c, gs in CENTRES.items() for g in gs}

TRIGRAMS = {"111": "Heaven", "000": "Earth", "100": "Thunder", "010": "Water", "001": "Mountain",
            "011": "Wind", "101": "Fire", "110": "Lake"}


def zodiac(arcsec):
    arcsec %= 360 * 3600
    sign, rest = divmod(arcsec, 30 * 3600)
    deg, rest = divmod(rest, 3600)
    mnt, sec = divmod(rest, 60)
    s = f"{deg}°{mnt:02d}'" + (f"{sec:02d}\"" if sec else "")
    return f"{s} {SIGNS[sign]}"


def main():
    binary = json.load(open(os.path.join(ROOT, "scripts", "hexagram-binary.json"), encoding="utf-8"))["hexagrams"]
    zc = json.load(open(os.path.join(ROOT, "grammars", "zhouyi-core", "grammar.json"), encoding="utf-8"))
    name_of = {n["number"]: n["name"] for n in zc["nodes"] if isinstance(n.get("number"), int)}

    # --- self-checks: the list is a permutation, the centres cover 1-64, and the wheel is the Fu Xi circle
    assert sorted(WHEEL) == list(range(1, 65)), "WHEEL is not a permutation of 1..64"
    assert sorted(CENTRE_OF) == list(range(1, 65)), "CENTRES do not cover 1..64 once each"
    val = {n: sum(int(c) << (5 - i) for i, c in enumerate(binary[str(n)]["binary"])) for n in range(1, 65)}
    vals = [val[g] for g in WHEEL]
    # The ring is two runs of counting joined end to end: 49 down to 32, then 0 up to 31, then 63 down to 50
    # (and round to 49). Every step is -1 or +1, except the two joins (32 to 0, and 31 to 63).
    steps = [(vals[(i + 1) % 64] - vals[i]) % 64 for i in range(64)]
    assert set(steps) <= {1, 63, 32}, "a step of the wheel is not +1, -1 or a join"
    assert steps.count(32) == 2, f"the wheel should have exactly two joins (32 to 0 and 31 to 63), found {steps.count(32)}"
    assert vals[:19] == list(range(49, 31, -1)) + [0], "the wheel does not start 49 down to 32, then 0 (gate 41 to gate 2)"

    nodes = []
    notes = [
        ("note-what-this-is", "What this is", {
            "The wheel": "Human Design lays the 64 hexagrams round a circle and calls them gates. The circle is the zodiac: "
                         "each gate takes 5 degrees 37 minutes 30 seconds of it (360 degrees divided by 64), and the first, "
                         "gate 41, begins at 2 degrees Aquarius. This grammar lists the gates in that order. Everything on a "
                         "gate's card is a position or a fact about the figure; none of it is Human Design's own text.",
            "The order": "The order round the wheel is not the King Wen order (1, 2, 3 ...). It is the binary counting order "
                         "that Shao Yong drew as a circle in the 11th century, the 'Fu Xi' circle: read the figures with the "
                         "bottom line as the biggest digit and the order is two runs of counting, one up from 0 and one down "
                         "from 63, joined into a ring. scripts/build_hd_wheel.py checks this for the list it uses.",
            "Lines": "Each gate is cut into six lines of 0 degrees 56 minutes 15 seconds each (5 degrees 37 minutes 30 seconds "
                     "divided by six). In Human Design, 'line' names that sixth of a gate, which is where a planet falls. It is "
                     "not the same thing as a changing line in a cast; see the Schools of the I Ching grammar for that.",
        }),
        ("note-what-is-left-out", "What this grammar leaves out", {
            "Left out": "Human Design's gate names and keynotes, the line texts of the Rave I'Ching, the descriptions of the "
                        "channels and the Incarnation Crosses. They are Ra Uru Hu's writing, and Jovian Archive Media states "
                        "that it holds the exclusive rights to it (jovianarchive.com, Terms and Conditions, Copyright notice). "
                        "The wheel, the hexagram figures and the zodiac arithmetic are facts that anyone may state; the "
                        "Florence court order of June 3 2020 says the same about the system as a whole (a system or method is "
                        "not itself covered by copyright). We rely on the narrower point: we copy no text.",
            "Gene Keys": "The Gene Keys use the same wheel and call the pair of opposite gates 'programming partners'. "
                         "Their word lists and book text are not used here (Gene Keys Ltd reserves its rights, and bars use of "
                         "its materials to train or operate AI systems). See docs/RESEARCH-gene-keys-and-human-design-2026-10-12.md.",
        }),
    ]
    for i, (nid, title, sections) in enumerate(notes):
        nodes.append({"id": nid, "name": title, "category": "note", "sort_order": i + 1,
                      "keywords": ["human-design", "wheel"], "sections": sections, "metadata": {}})

    for pos, gate in enumerate(WHEEL):
        b = binary[str(gate)]["binary"]                    # bottom line first
        lower, upper = TRIGRAMS[b[:3]], TRIGRAMS[b[3:]]
        opposite = WHEEL[(pos + 32) % 64]
        assert val[opposite] == 63 - val[gate], f"gate {opposite} is not gate {gate} with every line flipped"
        start = START_ARCSEC + pos * GATE_ARCSEC
        lines = "".join("┄" if c == "0" else "─" for c in reversed(b))      # top line first, as drawn
        centre = CENTRE_OF[gate]
        nodes.append({
            "id": f"gate-{gate}",
            "number": gate,
            "name": f"Gate {gate} · {name_of[gate]}",
            "symbol": binary[str(gate)]["symbol"],
            "category": "gate",
            "sort_order": len(notes) + pos + 1,
            "keywords": ["gate", centre.lower().replace(" ", "-") + "-centre", f"{lower.lower()}-{upper.lower()}"],
            "sections": {
                "The figure": f"Hexagram {gate} (King Wen order), {binary[str(gate)]['pinyin']} {binary[str(gate)]['chinese_name']}: "
                              f"{upper} above, {lower} below. Lines from the bottom: {b} (1 solid, 0 broken).",
                "Place on the wheel": f"Number {pos + 1} of 64, counting from gate 41. It begins at {zodiac(start)} and ends at "
                                      f"{zodiac(start + GATE_ARCSEC)}.",
                "Opposite gate": f"Gate {opposite}, directly across the wheel. Its figure is this one with every line flipped.",
                "Centre": f"The {centre} centre. This is the system's own assignment of gates to its nine centres.",
            },
            "metadata": {
                "number": gate, "binary": b, "wheel_position": pos + 1, "start": zodiac(start),
                "start_arcseconds": start % (360 * 3600), "opposite_gate": opposite, "centre": centre,
                "lower_trigram": lower, "upper_trigram": upper,
            },
            "image_url": None,
        })

    grammar = {
        "_generated": True,
        "_generated_by": "scripts/build_hd_wheel.py",
        "_draft_note": "Oct 12 2026 draft. Skipped by recursive.eco's importer (_generated). PlayfulProcess decides whether it becomes a grammar; see docs/PROPOSAL-hd-gene-keys-grammars-and-course-2026-10-12.md.",
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0 (PlayfulProcess) for the words and the arrangement. The positions, numbers and hexagram facts are facts; "
                       "no Human Design or Gene Keys text is reproduced.",
            "attribution": [{"name": "PlayfulProcess", "date": "2026-10-12",
                             "note": "design and curation; computed by scripts/build_hd_wheel.py, prose written with AI"}],
            "sources": [
                "Order and start of the wheel: checked against the table of gate degrees at https://bonniesorsby.com/human-design-gates-by-degree/ for gates 41, 25, 1, 2 and 60, and against the Fu Xi circle computed from scripts/hexagram-binary.json.",
                "Gates in centres: the system's own rule, as stated for gates 1 and 58 on https://jovianarchive.com/pages/gates-and-hexagrams-in-human-design and checked against this repo's iching-hd-meta-categories grammar.",
                "Hexagram names and facts: grammars/zhouyi-core (James Legge, 1882, public domain) and scripts/hexagram-binary.json.",
            ],
        },
        "name": "The 64 Gates Around the Wheel",
        "description": "The 64 hexagrams in the order of the Human Design wheel, with where each begins in the zodiac, the gate across from it, and the centre it belongs to. Positions and facts only: no Human Design text.",
        "grammar_type": "custom",
        "default_preview": "grammar",
        "is_published": False,
        "creator_name": "PlayfulProcess",
        "tags": ["human-design", "i-ching", "wheel", "zodiac", "draft"],
        "nodes": nodes,
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "grammar.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(grammar, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote grammars/hd-mandala-wheel/grammar.json ({len(nodes)} nodes)")


if __name__ == "__main__":
    sys.exit(main())
