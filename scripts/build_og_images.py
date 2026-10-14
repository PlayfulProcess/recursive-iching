#!/usr/bin/env python3
"""Draws the social-share (Open Graph) images: img/og/hexagram-1.png ... hexagram-64.png and img/og/site.png.

    python scripts/build_og_images.py

1200 x 630 PNGs in the zen palette of theme.css (rice paper, sumi ink, one seal red): the six
lines, the Chinese name, the pinyin and the English title. Needs Pillow, and fonts for Latin and
for Chinese (Georgia + Microsoft YaHei on Windows, or DejaVu/Noto on Linux; see FONTS). Font
rendering differs between machines, so build_hexagram_pages.py --check only asks that the files
exist; re-run this after a hexagram's name changes.
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "og")
PAPER, INK, SOFT, SEAL, LINE = "#f3efe6", "#1c1a17", "#655f55", "#9c3b2a", "#dbd4c6"
FONTS = {
    "serif": ["C:/Windows/Fonts/georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "/Library/Fonts/Georgia.ttf"],
    "zh": ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simsun.ttc", "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
           "/System/Library/Fonts/PingFang.ttc"],
}


def font(kind, size):
    for p in FONTS[kind]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    sys.exit(f"no {kind} font found; add one to FONTS in {__file__}")


def short_name(name):
    return re.sub(r"\s*[\(\[].*?[\)\]]", "", name).strip()


def draw_lines(d, binary, x, y, w, h, gap, color):
    for i, bit in enumerate(binary):  # i = 0 is the bottom line
        top = y + (5 - i) * (h + gap)
        if bit == "1":
            d.rectangle([x, top, x + w, top + h], fill=color)
        else:
            seg = int(w * 0.43)
            d.rectangle([x, top, x + seg, top + h], fill=color)
            d.rectangle([x + w - seg, top, x + w, top + h], fill=color)


def fit(d, text, kind, size, max_w):
    while size > 18:
        f = font(kind, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(kind, size)


def save(img, name):
    img = img.convert("P", palette=Image.ADAPTIVE, colors=48)
    img.save(os.path.join(OUT, name), optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    hexes = json.load(open(os.path.join(ROOT, "scripts", "hexagram-binary.json"), encoding="utf-8"))["hexagrams"]
    zy = json.load(open(os.path.join(ROOT, "grammars", "zhouyi-core", "grammar.json"), encoding="utf-8"))
    names = {n["number"]: short_name(n["name"]) for n in zy["nodes"] if isinstance(n.get("number"), int)}
    for k, h in hexes.items():
        n = int(k)
        img = Image.new("RGB", (1200, 630), PAPER)
        d = ImageDraw.Draw(img)
        d.rectangle([40, 40, 1160, 590], outline=LINE, width=2)
        draw_lines(d, h["binary"], 110, 135, 300, 42, 30, INK)
        d.text((500, 120), f"HEXAGRAM {n} OF 64", font=font("serif", 30), fill=SOFT)
        d.text((496, 165), h["chinese_name"], font=font("zh", 150), fill=SEAL)
        d.text((500, 360), h["pinyin"], font=font("serif", 44), fill=INK)
        d.text((500, 420), names[n], font=fit(d, names[n], "serif", 54, 620), fill=INK)
        d.text((500, 520), "iching.recursive.eco · Legge's text & the Chinese", font=font("serif", 24), fill=SOFT)
        save(img, f"hexagram-{n}.png")
    img = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, 1160, 590], outline=LINE, width=2)
    for col, b in enumerate(["111111", "100010", "010101", "000000"]):
        draw_lines(d, b, 110 + col * 140, 120, 100, 20, 16, INK if col % 2 == 0 else SEAL)
    d.text((110, 330), "The Recursive I Ching", font=font("serif", 64), fill=INK)
    d.text((110, 420), "The 64 hexagrams in Legge's translation,", font=font("serif", 34), fill=SOFT)
    d.text((110, 465), "beside the Chinese original. Free, no ads.", font=font("serif", 34), fill=SOFT)
    d.text((110, 530), "iching.recursive.eco", font=font("serif", 26), fill=SEAL)
    save(img, "site.png")
    print(f"wrote {len(hexes) + 1} images to img/og/")


if __name__ == "__main__":
    main()
