# -*- coding: utf-8 -*-
"""Add Legge's Commentary on the Judgments (Appendix I, the Thwan) and his Smaller Symbolism of the lines
(Appendix II) to each hexagram item of grammars/ten-wings/grammar.json, as two new sections.

ten-wings is a MAPPED grammar (recursive.eco e249829d, Private): the import pairs items by id, so this script
only ADDS sections. It changes no id, no name, no existing section, and no item. Run it again and it replaces the
two sections it owns with the same text (idempotent). The text is James Legge's 1882 English (public domain),
read from scripts/legge-appendices.json (its _meta says where it came from and how it was checked).

Run from the repo root:  python scripts/add_ten_wings_sections.py
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATH = os.path.join(ROOT, "grammars", "ten-wings", "grammar.json")
DATA = os.path.join(ROOT, "scripts", "legge-appendices.json")
TUAN = "Commentary on the Judgment (Tuan, Legge)"
SMALL = "Small Image of the lines (Legge)"
ORD = {1: "Line 1", 2: "Line 2", 3: "Line 3", 4: "Line 4", 5: "Line 5", 6: "Line 6"}
LICENSE_ADD = (" The Commentary on the Judgments (Appendix I, the Thwan) and the Smaller Symbolism of the lines (Appendix II) added "
               "on Oct 12 2026 are also Legge verbatim (scripts/legge-appendices.json records the source and the check).")


def main():
    raw = open(PATH, encoding="utf-8", newline="").read()
    g = json.loads(raw)
    data = json.load(open(DATA, encoding="utf-8"))["hexagrams"]
    done = 0
    for node in g["nodes"]:
        n = node.get("number")
        if not (isinstance(n, int) and node.get("category") == "great-image" or isinstance(n, int) and "Great Image (Daxiang)" in node["sections"]):
            continue
        d = data[str(n)]
        tuan = "\n\n".join(d["tuan"])
        small_texts = d["small"]
        parts = [f"{ORD[i + 1]}: {t}" for i, t in enumerate(small_texts[:6])]
        if len(small_texts) > 6:
            parts.append(("Use of Nine: " if n == 1 else "Use of Six: ") + small_texts[6])
        small = "\n\n".join(parts)
        # keep the existing order; add the two sections right after the Great Image
        new = {}
        for k, v in node["sections"].items():
            if k in (TUAN, SMALL):
                continue
            new[k] = v
            if k == "Great Image (Daxiang)":
                new[TUAN] = tuan
                new[SMALL] = small
        node["sections"] = new
        done += 1
    assert done == 64, f"expected 64 hexagram items, changed {done}"
    lic = g["_grammar_commons"]["license"]
    if "Oct 12 2026" not in lic:
        g["_grammar_commons"]["license"] = lic + LICENSE_ADD
    out = json.dumps(g, ensure_ascii=False, indent=1).replace("\n", "\r\n") + "\r\n"
    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"ten-wings: added '{TUAN}' and '{SMALL}' to {done} hexagram items")


if __name__ == "__main__":
    sys.exit(main())
