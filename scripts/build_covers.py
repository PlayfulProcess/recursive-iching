#!/usr/bin/env python3
"""Draw one cover mark per grammar (Oct 7 2026, the zen look). Zero dependencies.

    python scripts/build_covers.py      # build_collection.py also runs it

Writes img/covers/<slug>.svg for every grammars/*/grammar.json (generated: edit this script,
never the SVGs). A mark is the site's brushed ensō (the same stroke as img/enso.svg, from
scripts/build_zen_marks.py) in seal red on paper, with a figure in sumi ink inside it:

  - by default, the grammar's first hexagram (its first item carrying a King Wen number), drawn
    line by line from scripts/hexagram-binary.json, with that number on a small seal at the
    lower right, where a painting carries its seal;
  - "bagua": the eight trigrams in a ring, bottom lines toward the centre (Fu Xi's order, Qian at
    the top), for a grammar that gathers every lens rather than one hexagram;
  - "liangyi": one whole line and one broken line, the two forms the Changes grow from.

A mark is what a grammar card shows when the grammar has no cover image of its own, and what a
card falls back to when a cover's link breaks (index.html). The colours are read from theme.css
(--panel2 for the paper, so a mark sits flush on the card's mat; --seal; --sumi), so they stay in
step with the tokens.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_zen_marks import build_enso  # noqa: E402  (same folder; the one ensō stroke)

OUT = ROOT / "img" / "covers"
W, H = 300, 400            # 3:4, the shape of the home page's grammar cards
CX, CY = 150, 182          # centre of the ensō and of the figure inside it
ENSO_SCALE = 2.9           # img/enso.svg's 100-unit box -> about 215 px across

# A grammar whose figure is not its first hexagram.
EMBLEM = {
    "meta-iching": "bagua",            # every lens at once: the eight trigrams
    "tree-of-the-iching": "liangyi",   # the history: what the Changes grow from
}


def token(name: str) -> str:
    css = (ROOT / "theme.css").read_text(encoding="utf-8")
    m = re.search(r"--" + re.escape(name) + r"\s*:\s*(#[0-9a-fA-F]{3,8})", css)
    if not m:
        raise SystemExit(f"theme.css has no --{name} colour")
    return m.group(1)


PAPER, SEAL, INK = token("panel2"), token("seal"), token("sumi")


def enso_shapes() -> str:
    """The ensō stroke from build_zen_marks.py, recoloured and placed in the cover's frame."""
    src = build_enso()
    shapes = re.findall(r"<(?:circle|path)\b[^>]*/>", src)
    body = "".join(s.replace('fill="#000"', f'fill="{SEAL}"') for s in shapes)
    tx, ty = CX - 50 * ENSO_SCALE, CY - 50 * ENSO_SCALE
    return f'<g transform="translate({tx:.1f} {ty:.1f}) scale({ENSO_SCALE})">{body}</g>'


def bars(lines: str, cx: float, cy: float, width: float, bar: float, gap: float, split: float) -> str:
    """Rects for a figure of yin/yang lines. `lines` runs bottom to top ('1' whole, '0' broken),
    the convention of hexagram-binary.json. Returns rects centred on (cx, cy), drawn upright."""
    n = len(lines)
    total = n * bar + (n - 1) * gap
    out = []
    for i, ch in enumerate(lines):
        y = cy + total / 2 - (i + 1) * bar - i * gap   # line 1 at the bottom
        x0 = cx - width / 2
        if ch == "1":
            out.append(f'<rect x="{x0:.2f}" y="{y:.2f}" width="{width:.2f}" height="{bar:.2f}"/>')
        else:
            half = (width - split) / 2
            out.append(f'<rect x="{x0:.2f}" y="{y:.2f}" width="{half:.2f}" height="{bar:.2f}"/>')
            out.append(f'<rect x="{x0 + half + split:.2f}" y="{y:.2f}" width="{half:.2f}" height="{bar:.2f}"/>')
    return "".join(out)


def figure_hexagram(binary: str) -> str:
    return f'<g fill="{INK}">' + bars(binary, CX, CY, 104, 12, 9, 18) + "</g>"


def figure_bagua() -> str:
    # Fu Xi (Earlier Heaven) order, clockwise from the top: Qian, Xun, Kan, Gen, Kun, Zhen, Li, Dui.
    # Lines bottom to top; each trigram's bottom line faces the centre.
    ring = ["111", "011", "010", "001", "000", "100", "101", "110"]
    parts = []
    for k, tri in enumerate(ring):
        angle = 45 * k                       # 0 = top, clockwise
        # Draw upright just above the centre, then turn about the centre.
        g = bars(tri, CX, CY - 64, 40, 6, 5, 9)
        parts.append(f'<g transform="rotate({angle} {CX} {CY})">{g}</g>')
    return f'<g fill="{INK}">' + "".join(parts) + "</g>"


def figure_liangyi() -> str:
    return f'<g fill="{INK}">' + bars("01", CX, CY, 104, 12, 16, 18) + "</g>"


def chop(number: int) -> str:
    """A small seal at the lower right carrying the King Wen number, cut in paper colour."""
    x, y, s = 222, 322, 30
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="2.5" fill="{SEAL}"/>'
            f'<text x="{x + s / 2}" y="{y + s / 2 + 5.5}" text-anchor="middle" font-size="16" '
            f'font-family="Georgia,\'Times New Roman\',serif" font-weight="700" fill="{PAPER}">{number}</text>')


def first_hexagram(g: dict) -> int | None:
    items = sorted(g.get("items", []), key=lambda it: (it.get("sort_order") is None, it.get("sort_order") or 0))
    for it in items:
        meta = it.get("metadata") or {}
        if "role" in meta:            # the book's frame items are not hexagrams
            continue
        n = it.get("number", meta.get("number"))
        if isinstance(n, int) and 1 <= n <= 64:
            return n
    return None


def cover(slug: str, g: dict, hexes: dict) -> tuple[str, str]:
    kind = EMBLEM.get(slug)
    n = None if kind else first_hexagram(g)
    if n is None and not kind:
        kind = "bagua"
    if kind == "bagua":
        fig, label, seal = figure_bagua(), "the eight trigrams", ""
    elif kind == "liangyi":
        fig, label, seal = figure_liangyi(), "a whole line and a broken line", ""
    else:
        fig, label, seal = figure_hexagram(hexes[str(n)]["binary"]), f"hexagram {n}", chop(n)
    name = (g.get("name") or slug).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{name}: {label} inside an ensō">\n'
        f"<!-- Generated by scripts/build_covers.py for grammars/{slug}. Edit the script, not this file. -->\n"
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>\n'
        f"{enso_shapes()}\n{fig}\n{seal}\n</svg>\n"
    )
    return svg, label


def main() -> None:
    hexes = json.loads((ROOT / "scripts" / "hexagram-binary.json").read_text(encoding="utf-8"))["hexagrams"]
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for path in sorted((ROOT / "grammars").glob("*/grammar.json")):
        slug = path.parent.name
        g = json.loads(path.read_text(encoding="utf-8"))
        svg, label = cover(slug, g, hexes)
        (OUT / f"{slug}.svg").write_text(svg, encoding="utf-8", newline="\n")
        wanted.add(f"{slug}.svg")
        print(f"wrote img/covers/{slug}.svg ({label})")
    for stale in OUT.glob("*.svg"):
        if stale.name not in wanted:      # a grammar folder was removed
            stale.unlink()
            print(f"removed img/covers/{stale.name}")


if __name__ == "__main__":
    main()
