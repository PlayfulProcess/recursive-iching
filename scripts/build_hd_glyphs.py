# -*- coding: utf-8 -*-
"""Draw one glyph per hexagram: the Human Design bodygraph with gate N lit (its centre, its channels,
its partner gates) beside the HD wheel with gate N's segment filled. Pure SVG, no dependencies,
light-on-white, the repo's own drawing (the framework — 64 gate anchors, 36 channels, 9 centres, the
wheel order — is copied from recursive-astrology/viewer/astrology-viewer.html, our own code).

  python scripts/build_hd_glyphs.py            # writes img/hd/gate-01.svg … gate-64.svg
  python scripts/build_hd_glyphs.py --wire     # also sets image_url on the HD grammar's hexagram items
                                                #   -> https://iching.recursive.eco/img/hd/gate-NN.svg
                                                #   then rebuild meta: python scripts/build_meta_iching.py

Gate N in Human Design is hexagram N — same numbering — so gate-29.svg is Hexagram 29's glyph.
"""
import io, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "hd")
BASE_URL = "https://iching.recursive.eco/img/hd/"

GATE_POSITIONS = {
    61: (200, 28), 63: (180, 35), 64: (220, 35),
    4: (175, 85), 11: (230, 115), 17: (170, 115), 24: (200, 70), 43: (215, 95), 47: (225, 85),
    8: (185, 170), 12: (240, 195), 16: (145, 195), 20: (200, 155), 23: (215, 165), 31: (200, 195),
    33: (230, 170), 35: (255, 185), 45: (145, 205), 56: (230, 135), 62: (170, 135),
    1: (185, 245), 2: (200, 295), 7: (200, 230), 10: (175, 260), 13: (225, 245), 15: (200, 305), 25: (155, 265), 46: (215, 300),
    21: (125, 230), 26: (115, 275), 40: (145, 295), 51: (140, 250),
    3: (200, 405), 5: (200, 365), 9: (185, 390), 14: (200, 345), 27: (155, 375), 29: (215, 355), 34: (175, 350), 42: (215, 395), 59: (245, 375),
    18: (115, 390), 28: (115, 405), 32: (125, 370), 44: (120, 320), 48: (135, 345), 50: (145, 360), 57: (155, 335),
    6: (265, 360), 22: (260, 305), 30: (285, 380), 36: (270, 295), 37: (245, 330), 49: (280, 395), 55: (285, 365),
    19: (250, 475), 38: (130, 475), 39: (265, 455), 41: (280, 440), 52: (175, 460), 53: (225, 460), 54: (145, 455), 58: (115, 455), 60: (200, 475),
}
CHANNELS = ["1-8", "2-14", "3-60", "4-63", "5-15", "6-59", "7-31", "9-52", "10-20", "10-34", "10-57", "11-56", "12-22", "13-33",
            "16-48", "17-62", "18-58", "19-49", "20-34", "20-57", "21-45", "23-43", "24-61", "25-51", "26-44", "27-50", "28-38",
            "29-46", "30-41", "32-54", "34-57", "35-36", "37-40", "39-55", "42-53", "47-64"]
CENTERS = {
    "head": dict(x=200, y=45, shape="tri-up", s=30, gates=[61, 63, 64], name="Head"),
    "ajna": dict(x=200, y=105, shape="tri-down", s=30, gates=[4, 11, 17, 24, 43, 47], name="Ajna"),
    "throat": dict(x=200, y=175, shape="square", s=32, gates=[8, 12, 16, 20, 23, 31, 33, 35, 45, 56, 62], name="Throat"),
    "g": dict(x=200, y=270, shape="diamond", s=32, gates=[1, 2, 7, 10, 13, 15, 25, 46], name="G (Identity)"),
    "heart": dict(x=130, y=260, shape="tri-right", s=24, gates=[21, 26, 40, 51], name="Heart / Ego"),
    "spleen": dict(x=130, y=360, shape="square", s=27, gates=[18, 28, 32, 44, 48, 50, 57], name="Spleen"),
    "sacral": dict(x=200, y=375, shape="square", s=32, gates=[3, 5, 9, 14, 27, 29, 34, 42, 59], name="Sacral"),
    "solar": dict(x=270, y=345, shape="tri-left", s=30, gates=[6, 22, 30, 36, 37, 49, 55], name="Solar Plexus"),
    "root": dict(x=200, y=465, shape="square", s=32, gates=[19, 38, 39, 41, 52, 53, 54, 58, 60], name="Root"),
}
GATE_CENTER = {g: c for c, cfg in CENTERS.items() for g in cfg["gates"]}
WHEEL_ORDER = [17, 21, 51, 42, 3, 27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46,
               18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60, 41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25]
WHEEL_START = 3.875  # ecliptic longitude where gate 17 opens; 5.625° per gate

INK = "#1c1b18"; LIT = "#8a2e1c"; LIGHT = "#e9e4d8"; MID = "#b9b2a4"; PAPER = "#ffffff"


def center_path(cfg):
    x, y, s, sh = cfg["x"], cfg["y"], cfg["s"], cfg["shape"]
    if sh == "diamond": return f'<path d="M {x} {y-s} L {x+s} {y} L {x} {y+s} L {x-s} {y} Z"'
    if sh == "tri-up": return f'<path d="M {x} {y-s} L {x+s} {y+s*0.62} L {x-s} {y+s*0.62} Z"'
    if sh == "tri-down": return f'<path d="M {x-s} {y-s*0.62} L {x+s} {y-s*0.62} L {x} {y+s} Z"'
    if sh == "tri-right": return f'<path d="M {x-s*0.55} {y-s} L {x+s*0.75} {y} L {x-s*0.55} {y+s} Z"'
    if sh == "tri-left": return f'<path d="M {x+s*0.55} {y-s} L {x-s*0.75} {y} L {x+s*0.55} {y+s} Z"'
    return f'<rect x="{x-s}" y="{y-s}" width="{2*s}" height="{2*s}" rx="6"'


def arc(cx, cy, r1, r2, a0, a1):
    """annular sector, angles in degrees, 0° at top, clockwise"""
    def pt(r, a):
        t = math.radians(a - 90); return cx + r * math.cos(t), cy + r * math.sin(t)
    x0, y0 = pt(r2, a0); x1, y1 = pt(r2, a1); x2, y2 = pt(r1, a1); x3, y3 = pt(r1, a0)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M {x0:.2f} {y0:.2f} A {r2} {r2} 0 {large} 1 {x1:.2f} {y1:.2f} L {x2:.2f} {y2:.2f} A {r1} {r1} 0 {large} 0 {x3:.2f} {y3:.2f} Z"


def glyph(n, name=""):
    lit_center = GATE_CENTER[n]
    partners = set()
    for ch in CHANNELS:
        a, b = map(int, ch.split("-"))
        if n in (a, b): partners.add(b if a == n else a)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="80 0 560 500" width="560" height="500" role="img" aria-label="Human Design bodygraph and wheel, gate {n} lit">',
             f'<rect x="80" y="0" width="560" height="500" fill="{PAPER}"/>']
    # channels
    for ch in CHANNELS:
        a, b = map(int, ch.split("-"))
        (x1, y1), (x2, y2) = GATE_POSITIONS[a], GATE_POSITIONS[b]
        lit = n in (a, b)
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LIT if lit else LIGHT}" stroke-width="{4 if lit else 2.2}" stroke-linecap="round"/>')
    # centres
    for cid, cfg in CENTERS.items():
        lit = cid == lit_center
        parts.append(center_path(cfg) + f' fill="{"#f3e3de" if lit else PAPER}" stroke="{LIT if lit else MID}" stroke-width="{2.2 if lit else 1.4}" stroke-linejoin="round"/>')
    # gates
    for g, (x, y) in GATE_POSITIONS.items():
        if g == n:
            parts.append(f'<rect x="{x-9}" y="{y-9}" width="18" height="18" rx="4" fill="{LIT}"/>')
            parts.append(f'<text x="{x}" y="{y+3.6}" text-anchor="middle" font-size="9.5" font-weight="700" font-family="ui-monospace,Menlo,monospace" fill="#fff">{g}</text>')
        elif g in partners:
            parts.append(f'<rect x="{x-8}" y="{y-8}" width="16" height="16" rx="4" fill="{PAPER}" stroke="{LIT}" stroke-width="1.4"/>')
            parts.append(f'<text x="{x}" y="{y+3.2}" text-anchor="middle" font-size="8.5" font-weight="700" font-family="ui-monospace,Menlo,monospace" fill="{LIT}">{g}</text>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{MID}"/>')
    # wheel (right)
    cx, cy, r1, r2 = 490, 250, 78, 112
    for i, g in enumerate(WHEEL_ORDER):
        a0 = i * 5.625; a1 = a0 + 5.625
        lit = g == n
        parts.append(f'<path d="{arc(cx, cy, r1, r2, a0, a1)}" fill="{LIT if lit else PAPER}" stroke="{MID}" stroke-width="0.6"/>')
        if lit:
            t = math.radians((a0 + a1) / 2 - 90); tx, ty = cx + (r2 + 16) * math.cos(t), cy + (r2 + 16) * math.sin(t)
            parts.append(f'<text x="{tx:.1f}" y="{ty+3.5:.1f}" text-anchor="middle" font-size="11" font-weight="700" font-family="ui-monospace,Menlo,monospace" fill="{LIT}">{g}</text>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r1-6}" fill="none" stroke="{LIGHT}" stroke-width="0.8"/>')
    # labels
    parts.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="11" font-family="Georgia,serif" fill="{INK}">Gate {n}</text>')
    parts.append(f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-size="8.5" font-family="Georgia,serif" fill="{MID}">{CENTERS[lit_center]["name"]}</text>')
    if name:
        parts.append(f'<text x="{cx}" y="{cy+r2+40}" text-anchor="middle" font-size="10" font-family="Georgia,serif" fill="{INK}">{name}</text>')
    parts.append(f'<text x="{cx}" y="488" text-anchor="middle" font-size="7.5" font-family="Georgia,serif" fill="{MID}">bodygraph · wheel — The Recursive I Ching</text>')
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hdp = os.path.join(ROOT, "grammars", "iching-hd-meta-categories", "grammar.json")
    hd = json.load(io.open(hdp, encoding="utf-8")) if os.path.exists(hdp) else None
    names = {}
    if hd:
        for it in hd["items"]:
            m = (it.get("metadata") or {}).get("number")
            if m: names[int(m)] = it.get("name", "")
    for n in range(1, 65):
        io.open(os.path.join(OUT, f"gate-{n:02d}.svg"), "w", encoding="utf-8").write(glyph(n, names.get(n, "")))
    print("wrote 64 glyphs to", OUT)
    if "--wire" in sys.argv and hd:
        k = 0
        for it in hd["items"]:
            m = (it.get("metadata") or {}).get("number")
            if m:
                it["image_url"] = f"{BASE_URL}gate-{int(m):02d}.svg"; k += 1
        io.open(hdp, "w", encoding="utf-8").write(json.dumps(hd, ensure_ascii=False, indent=2) + "\n")
        print("wired image_url on", k, "hexagram items; now run scripts/build_meta_iching.py")
