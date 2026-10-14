# -*- coding: utf-8 -*-
"""Verdict-word rates of the 384 line texts, cut every way the structure of a hexagram allows.

Feeds pages/verdict-heatmaps.html (the heatmaps) and the small table in the Changing-Lines Lens course. The numbers
are counts of words in the classical Chinese line texts, a text counted once per word, exactly as the course's
"The figures" table counts them (scripts/changing_lines.py checks that the two agree). A count of a word is a blunt
tool: 貞吉 ("firmness brings good fortune") is a condition, 悔亡 ("regret vanishes") holds 悔, and one text can hold
both 吉 and 凶. It shows where the words fall, not what a line means.

    python scripts/verdict_words.py --build         # rewrite data/verdict-words.json
    python scripts/verdict_words.py --check         # fail (exit 1) if that file differs from what --build would write
    python scripts/verdict_words.py --summary       # print the headline tables

The words (substring of the Chinese text; 無咎 is a sub-count of 咎):
  吉 auspicious · 凶 ominous · 悔 regret · 吝 humiliation / distress · 咎 blame (90 texts, 85 of them 無咎 "no blame")
  · 無咎 no blame · 厲 danger.  (The text uses the traditional 無 and 厲 throughout; 无 and 厉 do not occur.)

The cuts (every cell is {"n": texts in the cell, word: texts holding it}):
  position        line 1..6                                        64 texts each
  polarity        yang (a 9 line) / yin (a 6 line), overall        192 each
  position_polarity   position x polarity                          32 each
  correct         a yang line in an odd place or a yin line in an even place, against the rest      192 each
  central         lines 2 and 5 against the others                 128 / 256
  correct_central the two crossed                                  64 / 64 / 128 / 128
  trigram         each of the 8 trigrams as lower and as upper: 'own' = the 3 lines inside that trigram (24 texts),
                  'hex' = all 6 lines of the 8 hexagrams that carry it in that place (48 texts)
  hexagram        each hexagram's 6 line texts
  compare         exact two-sided Fisher p for the pairs the page's header talks about (not adjusted for the
                  many cuts on the page)

Sources: scripts/hexagram-binary.json, grammars/zhouyi-core (the short English titles) and
grammars/i-ching-chinese-original (Project Gutenberg #25501, public domain).
"""
import io
import json
import os
import sys
from fractions import Fraction as F
from math import comb

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BINARY = os.path.join(ROOT, "scripts", "hexagram-binary.json")
ZHOUYI = os.path.join(ROOT, "grammars", "zhouyi-core", "grammar.json")
CHINESE = os.path.join(ROOT, "grammars", "i-ching-chinese-original", "grammar.json")
OUT = os.path.join(ROOT, "data", "verdict-words.json")

ERRORS = []


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


# word, English gloss, what it is
WORDS = [
    ("吉", "auspicious", "good fortune"),
    ("凶", "ominous", "misfortune"),
    ("悔", "regret", "regret or repentance (悔亡, regret vanishes, is 18 of its 30 texts)"),
    ("吝", "humiliation", "humiliation, distress"),
    ("咎", "blame", "blame (85 of its 90 texts are 無咎, no blame)"),
    ("無咎", "no blame", "no blame, a sub-count of 咎"),
    ("厲", "danger", "danger, peril"),
]
KEYS = [w for w, _, _ in WORDS]

# Trigrams, bottom line first ('1' = yang), in Fu Xi order (Heaven first).
TRIGRAMS = [
    ("111", "Qian", "乾", "Heaven"), ("110", "Dui", "兌", "Lake"), ("101", "Li", "離", "Fire"), ("100", "Zhen", "震", "Thunder"),
    ("011", "Xun", "巽", "Wind"), ("010", "Kan", "坎", "Water"), ("001", "Gen", "艮", "Mountain"), ("000", "Kun", "坤", "Earth"),
]

BIN = {int(k): v for k, v in load(BINARY)["hexagrams"].items()}
ZY = {n["number"]: n for n in load(ZHOUYI)["nodes"]}
ZH = {n["number"]: n for n in load(CHINESE)["nodes"]}
check(len(BIN) == 64 and set(ZY) == set(range(1, 65)) and set(ZH) == set(range(1, 65)), "the sources do not hold 64 hexagrams")


def texts():
    """All 384 lines: (hexagram, position, yang?, the Chinese text)."""
    out = []
    for n in range(1, 65):
        for p in range(1, 7):
            out.append((n, p, BIN[n]["binary"][p - 1] == "1", ZH[n]["sections"][f"Line {p}"]))
    return out


LINES = texts()
check(len(LINES) == 384 and all(t for _, _, _, t in LINES), "the 384 line texts are not all present")


def cell(rows):
    c = {"n": len(rows)}
    for w in KEYS:
        c[w] = sum(1 for r in rows if w in r[3])
    return c


def where(pred):
    return [r for r in LINES if pred(r)]


def fisher(a, n1, b, n2):
    """Exact two-sided Fisher p for a of n1 against b of n2 (hypergeometric, tables no likelier than the observed)."""
    k, n = a + b, n1 + n2
    tot = comb(n, k)
    pr = lambda x: F(comb(n1, x) * comb(n2, k - x), tot)
    lo, hi = max(0, k - n2), min(k, n1)
    obs = pr(a)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= obs))


def is_correct(p, yang):
    return yang == (p % 2 == 1)


def build_data():
    d = {
        "_note": "Generated by scripts/verdict_words.py --build; do not edit by hand. Counts of verdict words in the classical "
                 "Chinese of the 384 line texts, a text counted once per word. Each cell is {n: texts, word: texts holding it}.",
        "words": [{"key": w, "en": en, "gloss": g} for w, en, g in WORDS],
        "source": "grammars/i-ching-chinese-original (Project Gutenberg #25501); positions from scripts/hexagram-binary.json",
    }
    d["position"] = {str(p): cell(where(lambda r, p=p: r[1] == p)) for p in range(1, 7)}
    d["polarity"] = {"yang": cell(where(lambda r: r[2])), "yin": cell(where(lambda r: not r[2]))}
    d["position_polarity"] = {f"{p}-{'yang' if y else 'yin'}": cell(where(lambda r, p=p, y=y: r[1] == p and r[2] == y))
                              for p in range(1, 7) for y in (True, False)}
    d["correct"] = {"correct": cell(where(lambda r: is_correct(r[1], r[2]))),
                    "incorrect": cell(where(lambda r: not is_correct(r[1], r[2])))}
    d["central"] = {"central": cell(where(lambda r: r[1] in (2, 5))), "not_central": cell(where(lambda r: r[1] not in (2, 5)))}
    d["correct_central"] = {
        f"{'correct' if c else 'incorrect'}_{'central' if m else 'not_central'}":
            cell(where(lambda r, c=c, m=m: is_correct(r[1], r[2]) == c and (r[1] in (2, 5)) == m))
        for c in (True, False) for m in (True, False)}

    tri = {}
    for bits, nm, zh, img in TRIGRAMS:
        low_hex = [n for n in range(1, 65) if BIN[n]["binary"][:3] == bits]
        up_hex = [n for n in range(1, 65) if BIN[n]["binary"][3:] == bits]
        tri[nm] = {
            "chinese": zh, "image": img, "binary": bits,
            "lower_own": cell(where(lambda r, s=low_hex: r[0] in s and r[1] <= 3)),
            "lower_hex": cell(where(lambda r, s=low_hex: r[0] in s)),
            "upper_own": cell(where(lambda r, s=up_hex: r[0] in s and r[1] >= 4)),
            "upper_hex": cell(where(lambda r, s=up_hex: r[0] in s)),
        }
        check(len(low_hex) == 8 and len(up_hex) == 8, f"trigram {nm} is not in 8 hexagrams per place")
    d["trigram"] = tri

    names = {bits: nm for bits, nm, _, _ in TRIGRAMS}
    d["hexagram"] = {}
    for n in range(1, 65):
        b = BIN[n]
        c = cell(where(lambda r, n=n: r[0] == n))
        c.update({"name": ZY[n]["name"], "chinese": b["chinese_name"], "pinyin": b["pinyin"], "symbol": b["symbol"],
                  "binary": b["binary"], "lower": names[b["binary"][:3]], "upper": names[b["binary"][3:]]})
        d["hexagram"][str(n)] = c

    def cmp_(label, word, x, y):
        p = fisher(x[word], x["n"], y[word], y["n"])
        return {"label": label, "word": word, "a": x[word], "a_n": x["n"], "b": y[word], "b_n": y["n"], "p_fisher": round(p, 6)}
    pp = d["position_polarity"]
    d["compare"] = (
        [cmp_("yang in the 5th vs yin in the 5th", w, pp["5-yang"], pp["5-yin"]) for w in ("吉", "凶")]
        + [cmp_("correct places vs incorrect places", w, d["correct"]["correct"], d["correct"]["incorrect"]) for w in ("吉", "凶")]
        + [cmp_("central lines (2, 5) vs the others", w, d["central"]["central"], d["central"]["not_central"]) for w in ("吉", "凶")]
        + [cmp_("yang lines vs yin lines", w, d["polarity"]["yang"], d["polarity"]["yin"]) for w in ("吉", "凶")]
    )

    # identities
    for key in ("position", "polarity", "position_polarity", "correct", "central", "correct_central"):
        check(sum(c["n"] for c in d[key].values()) == 384, f"{key}: the cells do not hold 384 texts")
    for w in KEYS:
        total = sum(c[w] for c in d["position"].values())
        check(total == sum(c[w] for c in d["polarity"].values()) == sum(c[w] for c in d["position_polarity"].values())
              == sum(c[w] for c in d["correct"].values()) == sum(c[w] for c in d["central"].values())
              == sum(c[w] for c in d["correct_central"].values()) == sum(c[w] for c in d["hexagram"].values()),
              f"{w}: the cuts do not add up to one total")
        check(sum(c["lower_own"][w] + c["upper_own"][w] for c in tri.values()) == total, f"{w}: the trigram 'own' cells do not add up")
        check(sum(c["lower_hex"][w] for c in tri.values()) == total, f"{w}: the lower-trigram cells do not add up")
    check(all(c["無咎"] <= c["咎"] for c in d["position_polarity"].values()), "無咎 exceeds 咎")
    return d


def dump(d):
    return json.dumps(d, ensure_ascii=False, indent=1) + "\n"


def pct(a, n):
    """Whole percent, halves rounded up (the page's JavaScript does the same, so the two always print one number)."""
    return f"{(200 * a + n) // (2 * n)}%"


def inline_table_md():
    """The small position x polarity table the course carries: net of 吉 over 凶, with both rates."""
    d = DATA
    rows = ["| Line | Yang (a 9) | Yin (a 6) |", "|---|---|---|"]
    for p in (6, 5, 4, 3, 2, 1):
        cs = []
        for pol in ("yang", "yin"):
            c = d["position_polarity"][f"{p}-{pol}"]
            cs.append(f"吉 {pct(c['吉'], c['n'])} ({c['吉']}/{c['n']}) · 凶 {pct(c['凶'], c['n'])} ({c['凶']}/{c['n']})")
        rows.append(f"| {p}{' (top)' if p == 6 else ''} | {cs[0]} | {cs[1]} |")
    return "\n".join(rows)


def fp(p):
    """A Fisher p as the page prints it."""
    return "p < 0.0001" if p < 0.0001 else f"p = {p:.2g}"


def headline():
    """The three plain sentences in the page header, every number computed from DATA. The page must carry them verbatim."""
    d, pp = DATA, DATA["position_polarity"]
    y5, n5 = pp["5-yang"], pp["5-yin"]
    cmp_ = {(c["label"], c["word"]): c for c in d["compare"]}
    cor, inc = d["correct"]["correct"], d["correct"]["incorrect"]
    ce, ot = d["central"]["central"], d["central"]["not_central"]
    pc = cmp_[("central lines (2, 5) vs the others", "吉")]["p_fisher"]
    px = cmp_[("central lines (2, 5) vs the others", "凶")]["p_fisher"]
    p5 = cmp_[("yang in the 5th vs yin in the 5th", "吉")]["p_fisher"]
    return [
        f"The clearest pattern is the place: the central lines (2 and 5) carry 吉 in {pct(ce['吉'], ce['n'])} of their {ce['n']} texts against {pct(ot['吉'], ot['n'])} of the other {ot['n']}, and 凶 in {pct(ce['凶'], ce['n'])} against {pct(ot['凶'], ot['n'])} ({fp(pc)} and {fp(px)}, exact Fisher).",
        f"Solid or broken matters much less. In the fifth place the broken (yin) line carries 吉 in {n5['吉']} of {n5['n']} texts ({pct(n5['吉'], n5['n'])}) and the solid (yang) line in {y5['吉']} of {y5['n']} ({pct(y5['吉'], y5['n'])}), yet with {y5['n']} texts a side that gap does not separate them ({fp(p5)}).",
        f"Lines in a correct place (yang in 1, 3, 5; yin in 2, 4, 6) carry 吉 in {pct(cor['吉'], cor['n'])} of {cor['n']} texts, no more than lines in an incorrect place ({pct(inc['吉'], inc['n'])}).",
    ]


DATA = build_data()


PAGE = os.path.join(ROOT, "pages", "verdict-heatmaps.html")


def check_page():
    """The page's header states the computed sentences verbatim, and fetches the data file."""
    if not os.path.exists(PAGE):
        ERRORS.append("missing pages/verdict-heatmaps.html")
        return
    html = io.open(PAGE, encoding="utf-8").read()
    for s in headline():
        check(s in html, f"pages/verdict-heatmaps.html does not state {s!r}")
    check("../data/verdict-words.json" in html, "the page does not read data/verdict-words.json")


def check_file():
    check_page()
    if not os.path.exists(OUT):
        ERRORS.append(f"missing {os.path.relpath(OUT, ROOT)}: run scripts/verdict_words.py --build")
    elif io.open(OUT, encoding="utf-8", newline="").read() != dump(DATA):
        ERRORS.append("data/verdict-words.json differs from the script: run scripts/verdict_words.py --build")


def summary():
    d = DATA
    print("position    " + "  ".join(f"{w}" for w in KEYS))
    for p in range(1, 7):
        c = d["position"][str(p)]
        print(f"line {p}      " + "  ".join(f"{c[w]:>2}" for w in KEYS) + f"   /{c['n']}")
    for k in ("yang", "yin"):
        c = d["polarity"][k]
        print(f"{k:<11} " + "  ".join(f"{c[w]:>3}" for w in KEYS) + f"   /{c['n']}")
    for k, c in d["position_polarity"].items():
        print(f"{k:<11} " + "  ".join(f"{c[w]:>2}" for w in KEYS) + f"   /{c['n']}")
    for grp in ("correct", "central", "correct_central"):
        for k, c in d[grp].items():
            print(f"{k:<22} " + "  ".join(f"{c[w]:>3}" for w in KEYS) + f"   /{c['n']}")
    for nm, c in d["trigram"].items():
        print(f"{nm:<5} lower_own {c['lower_own']['吉']:>2}/{c['lower_own']['凶']:>2}  upper_own {c['upper_own']['吉']:>2}/{c['upper_own']['凶']:>2}"
              f"  lower_hex {c['lower_hex']['吉']:>2}/{c['lower_hex']['凶']:>2}  upper_hex {c['upper_hex']['吉']:>2}/{c['upper_hex']['凶']:>2}")
    for c in d["compare"]:
        print(f"{c['label']:<38} {c['word']} {c['a']}/{c['a_n']} vs {c['b']}/{c['b_n']}  p={c['p_fisher']}")
    for v in headline():
        print(v)


def main():
    args = sys.argv[1:]
    sys.stdout.reconfigure(encoding="utf-8")
    if "--build" in args:
        if ERRORS:
            print("FAILED:\n" + "\n".join(ERRORS))
            return 1
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        io.open(OUT, "w", encoding="utf-8", newline="\n").write(dump(DATA))
        print(f"wrote {os.path.relpath(OUT, ROOT)}")
        return 0
    if "--summary" in args:
        summary()
        return 1 if ERRORS else 0
    check_file()
    if ERRORS:
        print("FAILED:\n" + "\n".join(ERRORS))
        return 1
    print("OK: data/verdict-words.json is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
