# -*- coding: utf-8 -*-
"""The odds behind the course 'Casting and Chance' (grammars/casting-and-chance).

Every number the course quotes is computed here, exactly, with fractions, and most of them twice: once by a
formula and once by enumerating every outcome of the method itself (8 coin falls, the yarrow remainders, the 16
cards of a line deck, the 2^16 falls of the cowries, the 2^8 falls of the opele). Nothing is sampled, so nothing
depends on a random seed.

    python scripts/casting_odds.py            # print the tables (Markdown) and check the course quotes them
    python scripts/casting_odds.py --quiet    # only the checks

It fails (exit 1) if an identity below stops holding, or if a figure the course states is missing from
grammars/casting-and-chance/grammar.json (so the prose cannot drift away from the arithmetic).

Model, stated once: a coin, a cowrie and an opele seed each fall either way with probability 1/2, and the
yarrow split leaves each remainder (1 to 4) equally likely. Real shells, seeds and hands need not be fair;
the course says so where it matters.
"""
import itertools
import json
import os
import sys
from fractions import Fraction as F
from math import comb, perm

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COURSE = os.path.join(ROOT, "grammars", "casting-and-chance", "grammar.json")
BINARY = os.path.join(ROOT, "scripts", "hexagram-binary.json")

ERRORS = []


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


def pct(x, nd=1):
    return f"{float(x) * 100:.{nd}f}%"


# ── 1. Line values: three coins, by enumerating the 8 falls (heads 3, tails 2) ─────────────────
def coins_lines():
    dist = {6: F(0), 7: F(0), 8: F(0), 9: F(0)}
    for fall in itertools.product((2, 3), repeat=3):
        dist[sum(fall)] += F(1, 8)
    return dist


# ── 2. Line values: yarrow stalks, by enumerating the remainders of the Xici procedure ─────────
# 49 stalks. Each "change": split into two piles, hang one stalk from the right pile between the fingers,
# count both piles off by fours; the remainder of each pile is 1-4 (4 when it divides evenly). The stalks
# set aside (the hung one + both remainders) are 5 or 9 on the first change, 4 or 8 on the second and third.
# Ideal model: the left pile's remainder is 1, 2, 3 or 4 with probability 1/4 each; the right pile's is then
# fixed by the total. After three changes 36, 32, 28 or 24 stalks remain: divided by 4, a 9, 8, 7 or 6.
def remainder(n):
    r = n % 4
    return 4 if r == 0 else r


def yarrow_change(total):
    """{stalks set aside: probability} for one change, ideal model."""
    out = {}
    for r_left in (1, 2, 3, 4):
        # choose a left pile with that remainder; the right pile, minus the hung stalk, holds the rest
        left = r_left + 4                     # any pile size with this remainder gives the same answer
        right_counted = total - left - 1
        aside = 1 + r_left + remainder(right_counted)
        out[aside] = out.get(aside, F(0)) + F(1, 4)
    return out


def yarrow_lines():
    dist = {}
    for a1, p1 in yarrow_change(49).items():
        for a2, p2 in yarrow_change(49 - a1).items():
            for a3, p3 in yarrow_change(49 - a1 - a2).items():
                left = 49 - a1 - a2 - a3
                v = left // 4
                check(left % 4 == 0 and v in (6, 7, 8, 9), f"yarrow: {left} stalks left is not 24/28/32/36")
                dist[v] = dist.get(v, F(0)) + p1 * p2 * p3
    return dict(sorted(dist.items()))


def yarrow_lines_finite():
    """The same procedure with every split of the pile equally likely (left pile 1..n-2), to show the ideal
    model is a close approximation, not an exact one, for real hands."""
    def change(total):
        out, sizes = {}, range(1, total - 1)
        for left in sizes:
            aside = 1 + remainder(left) + remainder(total - left - 1)
            out[aside] = out.get(aside, F(0)) + F(1, len(sizes))
        return out
    dist = {}
    for a1, p1 in change(49).items():
        for a2, p2 in change(49 - a1).items():
            for a3, p3 in change(49 - a1 - a2).items():
                v = (49 - a1 - a2 - a3) // 4
                dist[v] = dist.get(v, F(0)) + p1 * p2 * p3
    return dict(sorted(dist.items()))


COINS = coins_lines()
YARROW = yarrow_lines()
check(COINS == {6: F(1, 8), 7: F(3, 8), 8: F(3, 8), 9: F(1, 8)}, f"coins: {COINS}")
check(YARROW == {6: F(1, 16), 7: F(5, 16), 8: F(7, 16), 9: F(3, 16)}, f"yarrow: {YARROW}")

YANG = (7, 9)
CHANGING = (6, 9)


def p_yang(d):
    return sum(d[v] for v in YANG)


def p_change(d):
    return sum(d[v] for v in CHANGING)


# ── 3. The primary hexagram: each of the 64 is (1/2)^6 = 1/64 under both methods ───────────────
for name, d in (("coins", COINS), ("yarrow", YARROW)):
    check(p_yang(d) == F(1, 2), f"{name}: P(yang) = {p_yang(d)}")
    # enumerate all 4^6 = 4096 casts and count each primary
    prim = {}
    for cast in itertools.product((6, 7, 8, 9), repeat=6):
        key = tuple(v in YANG for v in cast)
        pr = 1
        for v in cast:
            pr *= d[v]
        prim[key] = prim.get(key, F(0)) + pr
    check(len(prim) == 64 and all(v == F(1, 64) for v in prim.values()), f"{name}: primaries not uniform")

# ── 4. How many lines change: binomial(6, 1/4) for both ─────────────────────────────────────────
for name, d in (("coins", COINS), ("yarrow", YARROW)):
    check(p_change(d) == F(1, 4), f"{name}: P(change) = {p_change(d)}")
N_CHANGE = {k: comb(6, k) * F(1, 4) ** k * F(3, 4) ** (6 - k) for k in range(7)}
check(sum(N_CHANGE.values()) == 1, "changing-line counts do not sum to 1")
check(N_CHANGE[0] == F(729, 4096), "P(0 changing) is not 729/4096")


# ── 5. The yarrow asymmetry: which lines change, and where the reading goes ─────────────────────
def p_line_changes_given(d, yang):
    return d[9] / (d[7] + d[9]) if yang else d[6] / (d[6] + d[8])


ASYM = {
    "coins": (p_line_changes_given(COINS, True), p_line_changes_given(COINS, False)),
    "yarrow": (p_line_changes_given(YARROW, True), p_line_changes_given(YARROW, False)),
}
check(ASYM["yarrow"] == (F(3, 8), F(1, 8)), f"yarrow asymmetry {ASYM['yarrow']}")
check(ASYM["coins"] == (F(1, 4), F(1, 4)), f"coin symmetry {ASYM['coins']}")


def p_relating_yang(d):
    # the relating figure has a yang line where the cast had 7 (stays yang) or 6 (yin becomes yang)
    return d[7] + d[6]


REL_YANG = {"coins": p_relating_yang(COINS), "yarrow": p_relating_yang(YARROW)}
check(REL_YANG["coins"] == F(1, 2) and REL_YANG["yarrow"] == F(3, 8), f"relating yang {REL_YANG}")


def p_any_change(d, n_yang):
    """P(at least one changing line) for a primary with n_yang solid lines."""
    a, b = p_line_changes_given(d, True), p_line_changes_given(d, False)
    return 1 - (1 - a) ** n_yang * (1 - b) ** (6 - n_yang)


def p_relating_given_change(d, target_bits):
    """P(relating figure == target | at least one line changed), by enumerating the 4096 casts."""
    num = F(0)
    for cast in itertools.product((6, 7, 8, 9), repeat=6):
        if not any(v in CHANGING for v in cast):
            continue
        rel = tuple((v in (7, 6)) for v in cast)
        if rel == target_bits:
            pr = 1
            for v in cast:
                pr *= d[v]
            num += pr
    return num / (1 - N_CHANGE[0])


# ── 6. One primary -> relating pair ───────────────────────────────────────────────────────────
def p_pair(d, prim_bits, rel_bits):
    pr = F(1)
    for a, b in zip(prim_bits, rel_bits):
        if a and b:
            pr *= d[7]
        elif not a and not b:
            pr *= d[8]
        elif a and not b:
            pr *= d[9]
        else:
            pr *= d[6]
    return pr


with open(BINARY, encoding="utf-8") as fh:
    HEX = {int(k): tuple(c == "1" for c in v["binary"]) for k, v in json.load(fh)["hexagrams"].items()}
check(len(HEX) == 64 and len(set(HEX.values())) == 64, "hexagram-binary.json is not 64 distinct figures")
check(HEX[1] == (True,) * 6 and HEX[2] == (False,) * 6, "1 and 2 are not all-yang / all-yin")
PAIR_43_58 = {n: p_pair(d, HEX[43], HEX[58]) for n, d in (("coins", COINS), ("yarrow", YARROW))}
check(sum(a != b for a, b in zip(HEX[43], HEX[58])) == 1, "43 -> 58 is not one changing line")
# the 4096 primary->relating pairs sum to 1 under each method
for name, d in (("coins", COINS), ("yarrow", YARROW)):
    total = sum(p_pair(d, a, b) for a in HEX.values() for b in HEX.values())
    check(total == 1, f"{name}: pairs sum to {total}")


# ── 7. Card renderings of the I Ching ───────────────────────────────────────────────────────────
# (a) a 64-card deck: one draw gives each primary 1/64 and no changing lines.
#     Drawing a SECOND card from the 64 as the 'relating' figure is a trap: d lines differ with C(6,d)/64.
TWO_CARD_D = {d: F(comb(6, d), 64) for d in range(7)}
check(sum(TWO_CARD_D.values()) == 1, "two-card distances")
# (a') two draws from an 8-card trigram deck (lower, then upper), with replacement: 1/8 * 1/8 = 1/64.
check(F(1, 8) * F(1, 8) == F(1, 64), "trigram pair")

# (b) the line deck: 16 cards, 1 x '6', 5 x '7', 7 x '8', 3 x '9', six draws, each card shuffled back.
LINE_DECK = [6] * 1 + [7] * 5 + [8] * 7 + [9] * 3
check(len(LINE_DECK) == 16, "line deck is not 16 cards")
LINE_DECK_DIST = {v: F(LINE_DECK.count(v), 16) for v in (6, 7, 8, 9)}
check(LINE_DECK_DIST == YARROW, "line deck does not match yarrow")


# ... and drawn WITHOUT putting cards back, the odds change: enumerate every ordered draw of 6 of the 16.
def no_replacement_stats(deck):
    n_change, all_yang, total = {}, F(0), 0
    for draw in itertools.combinations(range(len(deck)), 6):  # order does not change these counts
        vals = [deck[i] for i in draw]
        k = sum(v in CHANGING for v in vals)
        n_change[k] = n_change.get(k, 0) + 1
        if all(v in YANG for v in vals):
            all_yang += 1
        total += 1
    return {k: F(c, total) for k, c in sorted(n_change.items())}, all_yang / total


NOREP_CHANGE, NOREP_ALL_YANG = no_replacement_stats(LINE_DECK)
check(NOREP_CHANGE[0] == F(comb(12, 6), comb(16, 6)), "no-replacement P(0 change) is not hypergeometric")
check(NOREP_ALL_YANG == F(perm(8, 6), perm(16, 6)), "no-replacement all-yang")

# (c) the coin deck: 8 cards, 1 x '6', 3 x '7', 3 x '8', 1 x '9', six draws with replacement = three coins.
COIN_DECK = [6] + [7] * 3 + [8] * 3 + [9]
check({v: F(COIN_DECK.count(v), 8) for v in (6, 7, 8, 9)} == COINS, "coin deck does not match coins")
# the naive four-card deck (one each of 6, 7, 8, 9): half of all lines change.
NAIVE4_CHANGE = F(2, 4)
NAIVE4_ZERO = (1 - NAIVE4_CHANGE) ** 6
check(NAIVE4_ZERO == F(1, 64), "naive four-card P(0 change)")

# (d) a 64-card deck plus change decks: draw the figure, then for each line draw from a small deck that says
#     'changes' or 'stays'. One change deck of 4 (1 'changes') gives the coin odds; two decks of 8, one for solid
#     lines (3 'changes') and one for broken lines (1 'changes'), give the yarrow odds exactly.
CHANGE_DECK_COINS = {9: F(1, 2) * F(1, 4), 7: F(1, 2) * F(3, 4), 6: F(1, 2) * F(1, 4), 8: F(1, 2) * F(3, 4)}
CHANGE_DECK_YARROW = {9: F(1, 2) * F(3, 8), 7: F(1, 2) * F(5, 8), 6: F(1, 2) * F(1, 8), 8: F(1, 2) * F(7, 8)}
check(CHANGE_DECK_COINS == COINS, "change deck (coins)")
check(CHANGE_DECK_YARROW == YARROW, "change decks (yarrow)")

# ── 8. Búzios: 16 cowries, the count of open mouths (0..16), by enumerating all 2^16 falls ───────
BUZ = [0] * 17
for fall in range(1 << 16):
    BUZ[bin(fall).count("1")] += 1
check(BUZ == [comb(16, k) for k in range(17)] and sum(BUZ) == 65536, "cowrie counts are not C(16,k)")
BUZ_P = [F(c, 65536) for c in BUZ]
check(BUZ[8] == 12870, "8 open is not 12870/65536")
UNIFORM17 = F(1, 17)


def buz_biased(p):
    return [comb(16, k) * p ** k * (1 - p) ** (16 - k) for k in range(17)]


BUZ_P40 = buz_biased(F(2, 5))

# ── 9. Ifá opele: 8 half-seeds, two legs of 4; enumerate the 2^8 falls ─────────────────────────
legs = {}
for fall in range(1 << 8):
    right, left = fall & 0xF, fall >> 4
    legs[(right, left)] = legs.get((right, left), 0) + 1
check(len(legs) == 256 and set(legs.values()) == {1}, "opele: not 256 equally likely odù")
MEJI = F(sum(1 for (r, l) in legs if r == l), 256)
check(MEJI == F(16, 256), "Meji are not 16/256")

# ── 10. Tarot: 78 cards, drawn without replacement, order and orientation ──────────────────────
T_ORDERED_3 = perm(78, 3)
T_UNORDERED_3 = comb(78, 3)
T_ORIENTED_3 = T_ORDERED_3 * 2 ** 3
T_SPECIFIC_IN_3 = F(3, 78)
T_NO_MAJOR_3 = F(comb(56, 3), comb(78, 3))
T_ORDERED_10 = perm(78, 10)
check(T_ORDERED_3 == 456456 and T_UNORDERED_3 == 76076 and T_ORIENTED_3 == 3651648, "tarot counts")
# with replacement a card could repeat; without, it cannot:
T_REPEAT_WITH_REPL_3 = 1 - F(78 * 77 * 76, 78 ** 3)


# ── Report ─────────────────────────────────────────────────────────────────────────────────────
def report():
    out = []
    w = out.append
    w("## Line values\n")
    w("| Line | Coins | Yarrow (ideal) | Yarrow (every split equally likely) |")
    w("|---|---|---|---|")
    fin = yarrow_lines_finite()
    names = {6: "6 old yin (changing)", 7: "7 young yang", 8: "8 young yin", 9: "9 old yang (changing)"}
    for v in (6, 7, 8, 9):
        w(f"| {names[v]} | {COINS[v]} = {pct(COINS[v], 2)} | {YARROW[v]} = {pct(YARROW[v], 2)} | {pct(fin[v], 2)} |")
    w("\n## Changing lines per cast (both methods): binomial(6, 1/4)\n")
    w("| Changing lines | Probability |")
    w("|---|---|")
    for k, p in N_CHANGE.items():
        w(f"| {k} | {p.numerator}/{p.denominator} = {pct(p, 2 if p < F(1, 100) else 1)} |")
    w("\n## The yarrow asymmetry\n")
    for name in ("coins", "yarrow"):
        a, b = ASYM[name]
        w(f"- {name}: a solid line changes {a} = {pct(a)}, a broken line {b} = {pct(b)}; "
          f"relating figure has a solid line with {REL_YANG[name]}")
    for name, d in (("coins", COINS), ("yarrow", YARROW)):
        w(f"- {name}: P(hexagram 1 has a changing line) = {pct(p_any_change(d, 6))}, "
          f"hexagram 2: {pct(p_any_change(d, 0))}")
        r1 = p_relating_given_change(d, HEX[1])
        r2 = p_relating_given_change(d, HEX[2])
        w(f"- {name}: given at least one change, relating = 1: {pct(r1, 2)}; relating = 2: {pct(r2, 2)}")
    w("\n## One pair\n")
    for name in ("coins", "yarrow"):
        p = PAIR_43_58[name]
        w(f"- 43 changing to 58 by {name}: {p} = {pct(p, 3)} (about 1 in {round(1 / p):,})")
    for name, d in (("coins", COINS), ("yarrow", YARROW)):
        stay2, stay1 = p_pair(d, HEX[2], HEX[2]), p_pair(d, HEX[1], HEX[1])
        all1to2, all2to1 = p_pair(d, HEX[1], HEX[2]), p_pair(d, HEX[2], HEX[1])
        w(f"- {name}: 2 unchanged {pct(stay2, 2)}; 1 unchanged {pct(stay1, 2)}; "
          f"1 -> 2 all lines 1 in {round(1 / all1to2):,}; 2 -> 1 all lines 1 in {round(1 / all2to1):,}")
    w("\n## Cards\n")
    w("| Lines that differ | Cast (either method) | Two cards from a 64-card deck |")
    w("|---|---|---|")
    for k in range(7):
        w(f"| {k} | {pct(N_CHANGE[k], 2)} | {pct(TWO_CARD_D[k], 2)} |")
    w(f"\n- line deck without replacement: P(0 changing) = {pct(NOREP_CHANGE[0])}; "
      f"P(hexagram 1) = {pct(NOREP_ALL_YANG, 2)} (vs {pct(F(1, 64), 2)})")
    w(f"- naive four-card deck: a line changes 50%; P(0 changing) = {pct(NAIVE4_ZERO, 2)}")
    w("\n## Búzios: 16 cowries\n")
    w("| Open | Ways | Weighted deck | Uniform 17 cards | If a shell opens 40% |")
    w("|---|---|---|---|---|")
    for k in range(17):
        w(f"| {k} | {BUZ[k]:,} | {pct(BUZ_P[k], 3 if BUZ_P[k] < F(1, 100) else 1)} | {pct(UNIFORM17)} | "
          f"{pct(BUZ_P40[k], 2)} |")
    w(f"\n- uniform-17 shows 0 open {float(UNIFORM17 / BUZ_P[0]):,.0f} times too often; "
      f"8 open {float(BUZ_P[8] / UNIFORM17):.1f} times too rarely")
    w("\n## Ifá opele\n")
    w(f"- 256 odù, each 1/256 = {pct(F(1, 256), 2)}; Meji 16/256 = {pct(MEJI, 2)}; others 240/256 = {pct(1 - MEJI, 2)}")
    w("\n## Tarot\n")
    w(f"- three cards in order: {T_ORDERED_3:,}; as a set: {T_UNORDERED_3:,}; with reversals: {T_ORIENTED_3:,}")
    w(f"- a given card in a three-card spread: 3/78 = {pct(T_SPECIFIC_IN_3, 2)}")
    w(f"- no Major in three cards: {pct(T_NO_MAJOR_3)}; at least one: {pct(1 - T_NO_MAJOR_3)}")
    w(f"- if cards went back after each draw, a repeat in three would happen {pct(T_REPEAT_WITH_REPL_3, 2)}")
    w(f"- ten cards in order (Celtic Cross positions): {T_ORDERED_10:.3e}")
    return "\n".join(out)


# Figures the course states in words; each must appear verbatim in the grammar.
def course_quotes():
    q = [
        pct(N_CHANGE[0]), pct(N_CHANGE[1]), pct(N_CHANGE[2]), pct(N_CHANGE[3]),
        "12,870", pct(BUZ_P[8]), pct(UNIFORM17), "3,855", "65,536",
        pct(MEJI, 2), "456,456", "76,076", "3,651,648", pct(T_SPECIFIC_IN_3, 2),
        pct(p_any_change(YARROW, 6)), pct(p_any_change(YARROW, 0)), pct(p_any_change(COINS, 6)),
        pct(NOREP_CHANGE[0]), pct(NOREP_ALL_YANG, 2),
        f"{round(1 / PAIR_43_58['coins']):,}", f"{round(1 / PAIR_43_58['yarrow']):,}",
    ]
    return q


def main():
    quiet = "--quiet" in sys.argv
    if not quiet:
        sys.stdout.reconfigure(encoding="utf-8")
        print(report())
    if os.path.exists(COURSE):
        text = open(COURSE, encoding="utf-8").read()
        for s in course_quotes():
            check(s in text, f"course does not state {s!r}")
    else:
        ERRORS.append(f"missing {COURSE}")
    if ERRORS:
        print("\nFAILED:\n" + "\n".join(ERRORS))
        return 1
    print("\nOK: casting odds verified; the course quotes them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
