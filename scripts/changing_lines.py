# -*- coding: utf-8 -*-
"""The changing-lines lens: for a line position p (1-6) and a direction (yang to yin, or yin to yang), every
hexagram whose line p has the starting polarity (always 32), the relating hexagram (line p flipped), the line text
in Legge, the Small Image of that line (Legge's Appendix II), and the trigram that changes.

It feeds the course 'The Changing-Lines Lens' (grammars/changing-lines-lens). The chapters there are hand-written;
the twelve appendix nodes (ids starting 'tbl-') belong to this script and are rewritten by --build.

    python scripts/changing_lines.py                       # the table for line 5, yang to yin (Markdown)
    python scripts/changing_lines.py --line 2 --to yang    # any position and direction
    python scripts/changing_lines.py --counts              # the verdict words by position and polarity
    python scripts/changing_lines.py --build               # rewrite the twelve tbl- nodes of the course grammar
    python scripts/changing_lines.py --check [--quiet]     # identities + the grammar is up to date + it quotes the figures
                                                           # + the verdict-word data and its heatmap page are current

The verdict-word rates by place, polarity, trigram and hexagram live in scripts/verdict_words.py, which writes
data/verdict-words.json for pages/verdict-heatmaps.html; --check here runs its check too.

Sources, all already in this repo and public domain:
  scripts/hexagram-binary.json                 the verified binary of each hexagram (line 1 = first character)
  grammars/zhouyi-core/grammar.json            James Legge's English of the Judgments and line texts (1882/1899)
  scripts/legge-appendices.json                Legge's Smaller Symbolism of the lines (Appendix II)
  grammars/i-ching-chinese-original/grammar.json   the classical Chinese line texts (Project Gutenberg #25501)

--check fails (exit 1) if an identity stops holding, if a Legge line does not name the polarity the binary gives,
if the tbl- nodes differ from what --build would write, or if the course stops stating a figure computed here.
"""
import io
import json
import os
import sys
from fractions import Fraction as F

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BINARY = os.path.join(ROOT, "scripts", "hexagram-binary.json")
ZHOUYI = os.path.join(ROOT, "grammars", "zhouyi-core", "grammar.json")
APPX = os.path.join(ROOT, "scripts", "legge-appendices.json")
CHINESE = os.path.join(ROOT, "grammars", "i-ching-chinese-original", "grammar.json")
COURSE = os.path.join(ROOT, "grammars", "changing-lines-lens", "grammar.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # python -I does not add the script's folder
import verdict_words as vw  # noqa: E402

ERRORS = []


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


# ── Trigrams, bottom line first ('1' = yang). Names in pinyin, with the image the Shuogua gives each. ──
TRIGRAMS = {
    "111": ("Qian", "乾", "Heaven"),
    "110": ("Dui", "兌", "Lake"),
    "101": ("Li", "離", "Fire"),
    "100": ("Zhen", "震", "Thunder"),
    "011": ("Xun", "巽", "Wind"),
    "010": ("Kan", "坎", "Water"),
    "001": ("Gen", "艮", "Mountain"),
    "000": ("Kun", "坤", "Earth"),
}
ORDINAL = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "top"}


def tri(bits):
    n, zh, img = TRIGRAMS[bits]
    return f"{n} {zh} ({img})"


# ── Data ───────────────────────────────────────────────────────────────────────────────────────
BIN = {int(k): v for k, v in load(BINARY)["hexagrams"].items()}
ZY = {n["number"]: n for n in load(ZHOUYI)["nodes"]}
SMALL = {int(k): v["small"] for k, v in load(APPX)["hexagrams"].items()}
ZH = {n["number"]: n for n in load(CHINESE)["nodes"]}
BY_BITS = {v["binary"]: n for n, v in BIN.items()}

check(len(BIN) == 64 and len(BY_BITS) == 64, "hexagram-binary.json is not 64 distinct figures")
check(set(ZY) == set(range(1, 65)), "zhouyi-core does not hold the 64 hexagrams")
check(set(SMALL) == set(range(1, 65)), "legge-appendices.json does not hold the 64 hexagrams")
for n in range(1, 65):
    check(ZY[n]["metadata"]["binary"] == BIN[n]["binary"], f"zhouyi-core {n}: binary differs from hexagram-binary.json")
    check(ZH[n]["metadata"]["number"] == n, f"chinese original: no hexagram {n}")
    for p in range(1, 7):
        txt = ZY[n]["sections"][f"Line {p}"]
        word = "NINE" if BIN[n]["binary"][p - 1] == "1" else "SIX"
        # Legge names the line's number in its first words: 'The fifth NINE, undivided' / 'The fifth SIX, divided'
        check(word in txt[:40].upper(), f"{n} line {p}: Legge's text does not open with {word}: {txt[:40]!r}")


def flip(bits, p):
    i = p - 1
    return bits[:i] + ("0" if bits[i] == "1" else "1") + bits[i + 1:]


def name(n):
    """'5 Waiting (Xū 需)' - the site's short English title, the pinyin and the character."""
    b = BIN[n]
    return f"{n} {ZY[n]['name']} ({b['pinyin']} {b['chinese_name']})"


def table(p, to_yin=True):
    """Rows for line p turning yang->yin (to_yin) or yin->yang. Always 32 rows, in King Wen order."""
    start = "1" if to_yin else "0"
    rows = []
    for n in range(1, 65):
        bits = BIN[n]["binary"]
        if bits[p - 1] != start:
            continue
        rel_bits = flip(bits, p)
        rel = BY_BITS[rel_bits]
        part = slice(0, 3) if p <= 3 else slice(3, 6)
        rows.append({
            "n": n,
            "rel": rel,
            "which": "lower" if p <= 3 else "upper",
            "from": bits[part],
            "to": rel_bits[part],
            "other": bits[3:6] if p <= 3 else bits[0:3],
            "legge": ZY[n]["sections"][f"Line {p}"],
            "small": SMALL[n][p - 1],
            "chinese": ZH[n]["sections"][f"Line {p}"],
        })
    return rows


ALL = {(p, d): table(p, d) for p in range(1, 7) for d in (True, False)}

# ── Identities ─────────────────────────────────────────────────────────────────────────────────
for (p, d), rows in ALL.items():
    check(len(rows) == 32, f"line {p} {'yang->yin' if d else 'yin->yang'}: {len(rows)} rows, not 32")
    # the relating figures of one direction are exactly the primaries of the other
    other = ALL[(p, not d)]
    check(sorted(r["rel"] for r in rows) == sorted(r["n"] for r in other), f"line {p}: directions are not inverse")
    for r in rows:
        check(BY_BITS[flip(BIN[r["rel"]]["binary"], p)] == r["n"], f"line {p}: flipping {r['rel']} does not return {r['n']}")
        check(r["from"] != r["to"], f"line {p}: no trigram changed for {r['n']}")
    # each changed trigram meets each of the 8 trigrams of the other half once: 4 trigrams x 8 = 32
    froms = {}
    for r in rows:
        froms.setdefault(r["from"], set()).add(r["other"])
    check(len(froms) == 4 and all(len(v) == 8 for v in froms.values()), f"line {p}: not 4 trigrams x 8")

# line 5 yang -> yin: the upper trigram has a yang middle line (Qian, Dui, Xun, Kan) and loses it
MID_YANG = sorted({r["from"] for r in ALL[(5, True)]})
FIVE_MAP = {TRIGRAMS[r["from"]][0]: TRIGRAMS[r["to"]][0] for r in ALL[(5, True)]}
check(MID_YANG == sorted(b for b in TRIGRAMS if b[1] == "1"), "line 5 yang: upper trigrams are not those with a yang middle")
check(FIVE_MAP == {"Qian": "Li", "Dui": "Zhen", "Xun": "Gen", "Kan": "Kun"}, f"line 5 yang->yin map {FIVE_MAP}")


# ── The verdict words of the line texts, counted in the Chinese (the 384 lines, by position and polarity) ──
# 吉 good fortune; 凶 misfortune; 无咎/無咎 no blame; 悔 regret; 吝 distress; 厲 danger. A text is counted once per word.
WORDS = [("吉", "auspicious (吉)"), ("凶", "ominous (凶)"), ("咎", "blame (咎, mostly 'no blame')"),
         ("悔", "regret (悔)"), ("吝", "distress (吝)"), ("厲", "danger (厲)")]


def counts():
    """{(p, yang): {word: number of line texts containing it}}, plus the number of texts in each cell."""
    out, size = {}, {}
    for n in range(1, 65):
        for p in range(1, 7):
            key = (p, BIN[n]["binary"][p - 1] == "1")
            size[key] = size.get(key, 0) + 1
            t = ZH[n]["sections"][f"Line {p}"]
            for w, _ in WORDS:
                if w in t:
                    out.setdefault(key, {}).setdefault(w, 0)
                    out[key][w] += 1
    return out, size


COUNTS, SIZE = counts()
check(sum(SIZE.values()) == 384 and all(v == 32 for v in SIZE.values()), "the 384 lines are not 12 cells of 32")
# the sibling script counts the same words the same way: its position x polarity cells must equal these
for (p_, y_), c_ in COUNTS.items():
    cell_ = vw.DATA["position_polarity"][f"{p_}-{'yang' if y_ else 'yin'}"]
    check(all(cell_[w] == c_.get(w, 0) for w, _ in WORDS) and cell_["n"] == SIZE[(p_, y_)],
          f"verdict_words.py and changing_lines.py count line {p_} {'yang' if y_ else 'yin'} differently")
check([(b, n, z) for b, n, z, _ in vw.TRIGRAMS] == [(b, TRIGRAMS[b][0], TRIGRAMS[b][1]) for b in
                                                     ("111", "110", "101", "100", "011", "010", "001", "000")],
      "verdict_words.py names the trigrams differently")


def ji(p, yang):
    return COUNTS.get((p, yang), {}).get("吉", 0)


def xiong(p, yang):
    return COUNTS.get((p, yang), {}).get("凶", 0)


# Line 5 yang lines whose relating hexagram's line 5 (now yin) is auspicious, and so on: the paired texts.
PAIRS_5 = [(r["n"], r["rel"], "吉" in r["chinese"], "吉" in ZH[r["rel"]]["sections"]["Line 5"]) for r in ALL[(5, True)]]

# ── Odds (the same model as scripts/casting_odds.py: coins 1/8 3/8 3/8 1/8; yarrow 1/16 5/16 7/16 3/16) ──
COINS = {6: F(1, 8), 7: F(3, 8), 8: F(3, 8), 9: F(1, 8)}
YARROW = {6: F(1, 16), 7: F(5, 16), 8: F(7, 16), 9: F(3, 16)}
ODDS = {}
for nm, d in (("coins", COINS), ("yarrow", YARROW)):
    change = d[6] + d[9]
    ODDS[nm] = {
        "line5_changes": change,                                   # any polarity
        "line5_yang_to_yin": d[9],                                 # the cast has a 9 in fifth place
        "given_yang": d[9] / (d[7] + d[9]),                        # a solid fifth line moves
        "only_line5_yang_to_yin": d[9] * (1 - change) ** 5,        # ... and no other line moves
    }
check(ODDS["coins"]["line5_yang_to_yin"] == F(1, 8) and ODDS["yarrow"]["line5_yang_to_yin"] == F(3, 16), "odds of a 9")
check(ODDS["coins"]["line5_changes"] == F(1, 4) == ODDS["yarrow"]["line5_changes"], "a line changes 1 in 4")
check(ODDS["coins"]["only_line5_yang_to_yin"] == F(243, 8192), "coins: only line 5 changes, from yang")
check(ODDS["yarrow"]["only_line5_yang_to_yin"] == F(729, 16384), "yarrow: only line 5 changes, from yang")


def pct(x, nd=1):
    return f"{float(x) * 100:.{nd}f}%"


# ── Rendering ──────────────────────────────────────────────────────────────────────────────────
def label(p, to_yin):
    return f"Line {p}, {'yang to yin' if to_yin else 'yin to yang'}"


def node_id(p, to_yin):
    return f"tbl-line-{p}-{'yang-to-yin' if to_yin else 'yin-to-yang'}"


def md_table(rows):
    out = ["| Hexagram | Relating hexagram | Trigram that changes |", "|---|---|---|"]
    for r in rows:
        out.append(f"| {name(r['n'])} | {name(r['rel'])} | {r['which']}: {tri(r['from'])} → {tri(r['to'])} |")
    return "\n".join(out)


def md_texts(rows, p):
    paras = []
    for r in rows:
        paras.append(f"{r['n']} → {r['rel']}. {ZY[r['n']]['name']} → {ZY[r['rel']]['name']}.\n"
                     f"Line: {r['legge']}\nSmall Image: {r['small']}")
    return "\n\n".join(paras)


def build_node(p, to_yin, sort_order):
    rows = ALL[(p, to_yin)]
    which = "lower" if p <= 3 else "upper"
    start, end = ("yang (solid, a 9 when it moves)", "yin") if to_yin else ("yin (broken, a 6 when it moves)", "yang")
    groups = {}
    for r in rows:
        groups.setdefault(r["from"], r["to"])
    shift = "; ".join(f"{tri(a)} → {tri(b)}" for a, b in groups.items())
    about = (f"The 32 hexagrams whose {ORDINAL[p]} line is {start}, in King Wen order, and where each goes when that "
             f"line alone changes to {end}. The {which} trigram changes: {shift}; each of these meets each of the eight "
             f"trigrams once. Built by scripts/changing_lines.py from this repo's public-domain sources; do not edit "
             f"by hand, run the script.")
    return {
        "id": node_id(p, to_yin),
        "name": label(p, to_yin),
        "category": "appendix",
        "sort_order": 100 + sort_order,
        "keywords": ["changing lines", f"line {p}", "yang to yin" if to_yin else "yin to yang", "table"],
        "sections": {
            "About this table": about,
            "The 32 changes": md_table(rows),
            "The line texts (Legge)": md_texts(rows, p),
        },
        "metadata": {"line": p, "direction": "yang-to-yin" if to_yin else "yin-to-yang", "generated_by": "scripts/changing_lines.py"},
    }


def built_nodes():
    out, i = [], 0
    for p in (5, 1, 2, 3, 4, 6):          # line 5 first: the course starts there
        for d in (True, False):
            out.append(build_node(p, d, i))
            i += 1
    return out


def course_quotes():
    """Figures the course states in words; each must appear verbatim in the grammar's hand-written chapters."""
    c, y = ODDS["coins"], ODDS["yarrow"]
    pairs = {(a, b): sum(1 for _, _, x, z in PAIRS_5 if (x, z) == (a, b)) for a in (True, False) for b in (True, False)}
    fu5 = sum("孚" in r["chinese"] for r in ALL[(5, True)])
    check(all(sum("孚" in ZH[n]["sections"][f"Line {p}"] for n in range(1, 65) if (BIN[n]["binary"][p - 1] == "1") == yang) < fu5
              for p in range(1, 7) for yang in (True, False) if (p, yang) != (5, True)),
          "孚 is not most frequent at the solid fifth line")
    centre5 = sum(1 for r in ALL[(5, True)] if ("centr" in r["small"] or "due mean" in r["small"]))
    ordw = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "top"}
    tot_ji = {p: ji(p, True) + ji(p, False) for p in range(1, 7)}
    tot_xi = {p: xiong(p, True) + xiong(p, False) for p in range(1, 7)}
    rows = [f"| {p}{' (top)' if p == 6 else ''} | {tot_ji[p]} of 64 | {tot_xi[p]} of 64 |" for p in range(1, 7)]
    # the lists of pairs in the chapters' tables: by upper trigram, and by where 吉 falls
    for frm in sorted({r["from"] for r in ALL[(5, True)]}, reverse=True):
        rows.append(", ".join(f"{r['n']}→{r['rel']}" for r in ALL[(5, True)] if r["from"] == frm))
    for key in ((True, True), (False, True), (True, False), (False, False)):
        rows.append(", ".join(f"{n}→{rel}" for n, rel, a, b in PAIRS_5 if (a, b) == key))
    rows.append(", ".join(str(n) for n, _, a, _ in PAIRS_5 if a))
    rows += vw.inline_table_md().split(chr(10))[2:]       # the position x polarity table of "The figures"
    return rows + [
        f"{tot_ji[5]} of the 64 fifth lines", f"{tot_ji[3]} of the 64 third lines",
        f"{tot_xi[5]} of the 64 fifth lines", f"{tot_xi[3]} of the 64 third lines",
        f"{ji(5, True)} of the 32 solid fifth lines", f"{ji(5, False)} of the 32 broken fifth lines",
        f"凶 in {xiong(5, True)} of the 32", f"appears in {fu5} of the 32 solid fifth lines",
        f"the due mean for {centre5} of them",
        f"in {pairs[(True, True)]} of the 32 pairs both", f"in {pairs[(False, True)]} only the broken one",
        f"in {pairs[(True, False)]} only the solid one", f"in {pairs[(False, False)]} neither",
        f"吉 and 凶 each appear in {tot_ji[6]} of 64" if tot_ji[6] == tot_xi[6] else "line 6: 吉 and 凶 differ",
        f"only {tot_ji[3]} of the 64 texts",
        "1 in 4", "1 in 8", "3 in 16", "3 in 8",
        f"{c['only_line5_yang_to_yin']} = {pct(c['only_line5_yang_to_yin'], 2)}",
        f"{y['only_line5_yang_to_yin']} = {pct(y['only_line5_yang_to_yin'], 2)}",
        pct(c["only_line5_yang_to_yin"], 2) + " of coin casts", pct(y["only_line5_yang_to_yin"], 2) + " of",
    ]


def print_table(p, to_yin):
    rows = ALL[(p, to_yin)]
    print(f"## {label(p, to_yin)}\n")
    print(md_table(rows))
    print()
    print(md_texts(rows, p))


def print_counts():
    print("| Line | Polarity | 吉 | 凶 | 咎 | 悔 | 吝 | 厲 | texts |")
    print("|---|---|---|---|---|---|---|---|---|")
    for p in range(1, 7):
        for yang in (True, False):
            c = COUNTS.get((p, yang), {})
            print(f"| {p} | {'yang' if yang else 'yin'} | " + " | ".join(str(c.get(w, 0)) for w, _ in WORDS)
                  + f" | {SIZE[(p, yang)]} |")
    print()
    for p in range(1, 7):
        print(f"line {p}: 吉 {ji(p, True) + ji(p, False)}/64, 凶 {xiong(p, True) + xiong(p, False)}/64")
    print()
    for n, rel, a, b in PAIRS_5:
        print(f"{n:>2} -> {rel:>2}: yang fifth 吉 {a!s:5}  relating yin fifth 吉 {b}")
    for nm in ("coins", "yarrow"):
        o = ODDS[nm]
        print(f"{nm}: a 9 in fifth place {o['line5_yang_to_yin']}; a solid fifth line moves {o['given_yang']}; "
              f"only the fifth moves, from yang {o['only_line5_yang_to_yin']} = {pct(o['only_line5_yang_to_yin'], 2)}")


def build():
    raw = io.open(COURSE, encoding="utf-8").read()
    g = json.loads(raw)
    keep = [n for n in g["nodes"] if not n["id"].startswith("tbl-")]
    g["nodes"] = keep + built_nodes()
    io.open(COURSE, "w", encoding="utf-8", newline="\n").write(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {len(built_nodes())} tables into {os.path.relpath(COURSE, ROOT)}")


def check_course():
    vw.check_file()
    ERRORS.extend(vw.ERRORS)
    if not os.path.exists(COURSE):
        ERRORS.append(f"missing {COURSE}")
        return
    g = load(COURSE)
    have = [n for n in g["nodes"] if n["id"].startswith("tbl-")]
    if have != built_nodes():
        ERRORS.append("the tbl- nodes of grammars/changing-lines-lens differ from the script: run --build")
    text = json.dumps([n for n in g["nodes"] if not n["id"].startswith("tbl-")], ensure_ascii=False)
    for s in course_quotes():
        check(s in text, f"course does not state {s!r}")


def main():
    args = sys.argv[1:]
    sys.stdout.reconfigure(encoding="utf-8")
    if "--build" in args:
        if ERRORS:
            print("FAILED:\n" + "\n".join(ERRORS))
            return 1
        build()
        return 0
    if "--check" in args:
        check_course()
        if ERRORS:
            print("FAILED:\n" + "\n".join(ERRORS))
            return 1
        if "--quiet" not in args:
            print_counts()
        print("OK: 12 tables of 32 verified; the course's tables are current and it quotes the figures")
        return 0
    if "--counts" in args:
        print_counts()
        return 1 if ERRORS else 0
    p = int(args[args.index("--line") + 1]) if "--line" in args else 5
    to_yin = not ("--to" in args and args[args.index("--to") + 1] == "yang")
    print_table(p, to_yin)
    if ERRORS:
        print("\nFAILED:\n" + "\n".join(ERRORS))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
