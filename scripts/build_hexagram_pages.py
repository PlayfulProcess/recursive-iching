#!/usr/bin/env python3
"""Writes one static, crawlable page per hexagram, the hexagram chart, and the sitemap.

    python scripts/build_hexagram_pages.py          # write hexagram/*.html, hexagrams.html, sitemap.xml
    python scripts/build_hexagram_pages.py --check  # fail if any of them is stale (writes nothing)

Why (SEO, Oct 14 2026): every hexagram used to exist only inside the JavaScript viewers
(viewers/cards.html?hexagram=N reads the grammar JSON in the browser), so a search engine saw
one page, "Cards", for all 64. These pages carry each hexagram's text in the HTML itself, with a
unique title and description, a canonical URL, JSON-LD and links to its neighbours.

Generated, never hand-edit: hexagrams.html, hexagram/*.html, sitemap.xml and
data/sitemap-lastmod.json. Edit the sources and re-run:
  - grammars/zhouyi-core            Legge's Judgment and line texts (public domain, 1882/1899)
  - grammars/ten-wings              Legge's Great Image, Commentary on the Judgment, Small Image
  - grammars/i-ching-chinese-original  the Chinese text (Project Gutenberg #25501)
  - grammars/i-ching-summarized     the short gloss (this site's, AI-assisted, CC-BY-SA-4.0)
  - scripts/hexagram-binary.json    the line pattern (bottom to top); the trigrams are computed
                                    from it, never read from a grammar's trigram_above/below
  - ids.json                        the recursive.eco grammar id for the "Open in recursive.eco" link

The sitemap's <lastmod> is honest: data/sitemap-lastmod.json stores a hash of each listed page,
and a page's date moves to today only when its bytes change. A hand-edited page listed in
STATIC_PAGES (index.html, the wheel, ...) changing therefore needs a re-run too; --check says so.
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://iching.recursive.eco/"
OUT_DIR = "hexagram"
HUB = "hexagrams.html"
LASTMOD = os.path.join("data", "sitemap-lastmod.json")

# Hand-edited pages that belong in the sitemap (path -> priority). Viewers that only make sense
# with a query string, and course-viewer.html?course=..., are left out on purpose: their static
# HTML is a shell, so the hexagram pages are what should rank.
STATIC_PAGES = {
    "index.html": "1.0",
    "pages/wheel.html": "0.6",
    "pages/verdict-heatmaps.html": "0.6",
    "viewers/caster.html": "0.8",
    "viewers/source-text.html": "0.6",
}

TRIGRAMS = {  # bottom-to-top bits -> (english, chinese, pinyin, unicode)
    "111": ("Heaven", "乾", "Qián", "☰"),
    "000": ("Earth", "坤", "Kūn", "☷"),
    "100": ("Thunder", "震", "Zhèn", "☳"),
    "010": ("Water", "坎", "Kǎn", "☵"),
    "001": ("Mountain", "艮", "Gèn", "☶"),
    "011": ("Wind", "巽", "Xùn", "☴"),
    "101": ("Fire", "離", "Lí", "☲"),
    "110": ("Lake", "兌", "Duì", "☱"),
}
TRIGRAM_ORDER = ["111", "100", "010", "001", "000", "011", "101", "110"]  # King Wen family order
POS_ZH = ["初", "二", "三", "四", "五", "上"]
ORDINAL = ["first", "second", "third", "fourth", "fifth", "sixth"]


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def by_number(slug):
    g = load(f"grammars/{slug}/grammar.json")
    out = {}
    for n in g["nodes"]:
        num = n.get("number") or (n.get("metadata") or {}).get("number")
        if isinstance(num, int) and 1 <= num <= 64 and "role" not in (n.get("metadata") or {}):
            out[num] = n
    if len(out) != 64:
        sys.exit(f"{slug}: expected 64 hexagrams, found {len(out)}")
    return out


def esc(s):
    return html.escape(s or "", quote=True)


def paras(text):
    """Plain text with blank-line paragraphs -> <p> elements (escaped)."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]
    return "".join(f"<p>{esc(b).replace(chr(10), '<br>')}</p>" for b in blocks)


def short_name(name):
    return re.sub(r"\s*[\(\[].*?[\)\]]", "", name).strip()


def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def clip(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    if len(s) <= n:
        return s
    cut = s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:—-")
    return cut + "…"


def line_name(pos, yang):
    """Chinese line name: 初九 / 六二 / ... / 上六."""
    num = "九" if yang else "六"
    if pos == 1:
        return "初" + num
    if pos == 6:
        return "上" + num
    return num + POS_ZH[pos - 1]


def hex_svg(binary, size=1.0, cls="hx"):
    w, h, gap = 120 * size, 11 * size, 8 * size
    total = 6 * h + 5 * gap
    parts = [f'<svg class="{cls}" viewBox="0 0 {w:g} {total:g}" width="{w:g}" height="{total:g}" role="img" aria-hidden="true">']
    for i, bit in enumerate(binary):  # i = 0 is the bottom line
        y = total - (i + 1) * h - i * gap
        if bit == "1":
            parts.append(f'<rect x="0" y="{y:g}" width="{w:g}" height="{h:g}"/>')
        else:
            seg = w * 0.43
            parts.append(f'<rect x="0" y="{y:g}" width="{seg:g}" height="{h:g}"/><rect x="{w - seg:g}" y="{y:g}" width="{seg:g}" height="{h:g}"/>')
    parts.append("</svg>")
    return "".join(parts)


def small_images(blob):
    """Ten Wings 'Small Image of the lines' blob -> {1..6: text, 'all': text}."""
    out = {}
    for b in re.split(r"\n\s*\n", blob or ""):
        b = b.strip()
        m = re.match(r"Line (\d):\s*(.*)", b, re.S)
        if m:
            out[int(m.group(1))] = m.group(2).strip()
        elif re.match(r"Use of (Nine|Six)", b):
            out["all"] = b
    return out


CSS = """
html,body{margin:0;background:var(--bg);color:var(--ink);color-scheme:light;font-family:var(--sans);line-height:1.6}
.wrap{max-width:860px;margin:0 auto;padding:18px 16px 70px}
.crumbs{font-size:13px;color:var(--muted);margin:4px 0 14px}
.crumbs a{color:var(--muted)}
.kicker{font-size:11px;text-transform:uppercase;letter-spacing:.16em;color:var(--muted);margin:0}
h1{font-family:var(--serif-display);font-weight:600;font-size:30px;line-height:1.2;margin:6px 0 8px}
h1 .zh{color:var(--seal);margin-right:.25em}
h2{font-family:var(--serif-display);font-weight:600;font-size:21px;margin:30px 0 8px;border-top:1px solid var(--line);padding-top:18px}
h3{font-family:var(--serif-display);font-weight:600;font-size:17px;margin:20px 0 4px}
.head{display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;margin:8px 0 6px}
@media (max-width:560px){.head{grid-template-columns:1fr}.head svg.hx{width:96px;height:auto}}
svg.hx rect{fill:var(--ink)}
.facts{margin:0;font-size:14.5px;color:var(--ink-soft)}
.facts b{color:var(--ink);font-weight:600}
.gloss{font-family:var(--serif-body);font-size:16px;margin:12px 0 0}
.gloss small{display:block;font-family:var(--sans);font-size:12px;color:var(--muted)}
.zhtext{font-family:"Noto Serif TC","Noto Serif SC","Songti TC","SimSun",serif;font-size:19px;letter-spacing:.04em;color:var(--ink);margin:6px 0}
.legge{font-family:var(--serif-body);font-size:16.5px;line-height:1.7}
.legge p{margin:6px 0}
.src{font-size:12px;color:var(--muted);margin:2px 0 0}
.line{border-left:3px solid var(--line);padding:2px 0 2px 14px;margin:16px 0}
.line .ln{font-size:13px;color:var(--muted);margin:0}
.line .ln b{color:var(--seal);font-weight:600}
.line .si{font-size:14.5px;color:var(--ink-soft);margin:6px 0 0}
.line .chg{font-size:13px;margin:6px 0 0}
details{margin:10px 0;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:8px 14px}
summary{cursor:pointer;font-weight:600;font-size:14.5px}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:10px 0}
.rel a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px 12px;text-decoration:none;color:var(--ink)}
.rel a:hover{background:var(--chip-hover)}
.rel .k{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px}
.btn{display:inline-block;padding:8px 14px;border-radius:3px;border:1px solid var(--seal);color:var(--seal);text-decoration:none;font-size:14px}
.btn.primary{background:var(--seal);color:var(--on-seal)}
.pn{display:flex;justify-content:space-between;gap:10px;margin:34px 0 0;font-size:14.5px;border-top:1px solid var(--line);padding-top:14px}
.pn a{color:var(--ink)}
.fine{font-size:12.5px;color:var(--muted);margin-top:26px;line-height:1.55}
.fine a{color:var(--muted)}
a{color:var(--seal)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0;padding:0;list-style:none}
.grid a{display:flex;gap:10px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px;text-decoration:none;color:var(--ink);height:100%;box-sizing:border-box}
.grid a:hover{background:var(--chip-hover)}
.grid svg.hx{flex:none}
.grid .t{font-size:13.5px;line-height:1.3}
.grid .t b{display:block;font-size:12px;color:var(--muted);font-weight:500}
.chart{overflow-x:auto;margin:12px 0}
.chart table{border-collapse:collapse;font-size:13px;min-width:520px}
.chart th,.chart td{border:1px solid var(--line);padding:6px;text-align:center}
.chart th{background:var(--surface);font-weight:600}
.chart td a{text-decoration:none;color:var(--ink);display:block}
.chart td a:hover{color:var(--seal)}
.chart .tg{font-size:20px;display:block;line-height:1}
"""


def page(title, desc, canonical, og_image, ldjson, body, header_prefix):
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>'
        for x in ldjson
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The Recursive I Ching">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{header_prefix}img/recursive-logo-seal.svg">
<link rel="stylesheet" href="{header_prefix}theme.css?v=4">
<style>{CSS}</style>
{ld}
</head>
<body>
<!-- Generated by scripts/build_hexagram_pages.py: edit the grammars and re-run, never this file. -->
<script src="{header_prefix}site-header.js?v=52"></script>
<site-header active="cards"></site-header>
<main class="wrap">
{body}
</main>
<script src="{header_prefix}site-footer.js?v=3"></script>
<site-footer></site-footer>
</body>
</html>
"""


BOOK = {
    "@type": "Book",
    "name": "The Yî King",
    "alternateName": "I Ching (Zhouyi)",
    "translator": {"@type": "Person", "name": "James Legge"},
    "datePublished": "1882",
    "publisher": {"@type": "Organization", "name": "Oxford University Press"},
    "isPartOf": {"@type": "BookSeries", "name": "Sacred Books of the East", "volumeNumber": "XVI"},
    "inLanguage": "en",
    "license": "https://creativecommons.org/publicdomain/mark/1.0/",
}


def build():
    zy = by_number("zhouyi-core")
    tw = by_number("ten-wings")
    zh = by_number("i-ching-chinese-original")
    sm = by_number("i-ching-summarized")
    binmap = {int(k): v["binary"] for k, v in load("scripts/hexagram-binary.json")["hexagrams"].items()}
    by_bin = {b: n for n, b in binmap.items()}
    ids = load("ids.json")
    app_id = ids["ids"].get("i-ching-summarized") if "i-ching-summarized" in ids.get("_public_now", []) else None

    info = {}
    for n in range(1, 65):
        node = zy[n]
        meta = node.get("metadata") or {}
        b = binmap[n]
        name = short_name(node["name"])
        pinyin = meta.get("pinyin", "")
        info[n] = {
            "n": n,
            "name": name,
            "full_name": node["name"],
            "zh": meta.get("chinese_name", ""),
            "pinyin": pinyin,
            "symbol": node.get("symbol", ""),
            "bin": b,
            "lower": TRIGRAMS[b[:3]],
            "upper": TRIGRAMS[b[3:]],
            "slug": f"{n}-{ascii_slug(pinyin)}-{ascii_slug(name)}",
        }

    def url(n):
        return f"{SITE}{OUT_DIR}/{info[n]['slug']}.html"

    def rel_link(n, kind, note=""):
        i = info[n]
        return (f'<a href="{i["slug"]}.html"><span class="k">{esc(kind)}</span>'
                f'{i["n"]}. {esc(i["name"])} <span class="zh">{esc(i["zh"])}</span>'
                + (f'<br><small>{esc(note)}</small>' if note else "") + "</a>")

    files = {}
    for n in range(1, 65):
        i = info[n]
        z, t, c, s = zy[n]["sections"], tw[n]["sections"], zh[n]["sections"], sm[n]["sections"]
        lo, up = i["lower"], i["upper"]
        si = small_images(t.get("Small Image of the lines (Legge)", ""))
        judg = z.get("Judgment", "")
        title = f"I Ching Hexagram {n}: {i['name']} ({i['pinyin']} {i['zh']})"
        if len(title) + len(" · Recursive I Ching") <= 70:
            title += " · Recursive I Ching"
        desc = clip(
            f"Hexagram {n}, {i['name']} ({i['zh']} {i['pinyin']}), {up[0].lower()} over {lo[0].lower()}. "
            f"Judgment: {judg} The six lines in Legge's translation beside the Chinese original.", 158)

        lines_html = []
        for p in range(1, 7):
            yang = i["bin"][p - 1] == "1"
            flipped = i["bin"][: p - 1] + ("0" if yang else "1") + i["bin"][p:]
            to = by_bin[flipped]
            lines_html.append(
                f'<div class="line" id="line-{p}">'
                f'<h3>Line {p} <span class="zh">{line_name(p, yang)}</span></h3>'
                f'<p class="ln">The {ORDINAL[p - 1]} line from the bottom, {"yang (solid, nine)" if yang else "yin (broken, six)"}</p>'
                f'<p class="zhtext" lang="zh-Hant">{esc(c.get(f"Line {p}", ""))}</p>'
                f'<div class="legge">{paras(z.get(f"Line {p}", ""))}</div>'
                + (f'<p class="si"><b>Small Image:</b> {esc(si[p])}</p>' if p in si else "")
                + f'<p class="chg">If this line changes, it becomes <a href="{info[to]["slug"]}.html">Hexagram {to}, {esc(info[to]["name"])}</a>.</p>'
                "</div>")
        if z.get("All Lines"):
            lines_html.append(
                '<div class="line" id="all-lines"><h3>All six lines changing '
                f'<span class="zh">{"用九" if n == 1 else "用六"}</span></h3>'
                f'<div class="legge">{paras(z["All Lines"])}</div>'
                + (f'<p class="si"><b>Small Image:</b> {esc(si["all"])}</p>' if "all" in si else "")
                + "</div>")

        b = i["bin"]
        nuclear = by_bin[b[1:4] + b[2:5]]
        opposite = by_bin["".join("0" if x == "1" else "1" for x in b)]
        inverse = by_bin[b[::-1]]
        related = [rel_link(nuclear, "Nuclear hexagram 互卦", "lines 2-4 below, 3-5 above")]
        related.append(rel_link(opposite, "Opposite 錯卦", "every line changed"))
        if inverse != n:
            related.append(rel_link(inverse, "Inverse 綜卦", "turned upside down"))

        prev_n = 64 if n == 1 else n - 1
        next_n = 1 if n == 64 else n + 1
        gloss = s.get("Interpretation", "")
        app_link = (f'<a class="btn" href="https://recursive.eco/g/{app_id}?node=hexagram-{n}" target="_blank" rel="noopener">Open in recursive.eco ↗</a>'
                    if app_id else "")

        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">The Recursive I Ching</a> › <a href="../{HUB}">The 64 hexagrams</a> › Hexagram {n}</nav>
<article>
<div class="head">
{hex_svg(b)}
<div>
<p class="kicker">Hexagram {n} of 64 · King Wen order</p>
<h1><span class="zh" lang="zh-Hant">{esc(i['zh'])}</span>{esc(i['name'])}</h1>
<p class="facts"><b>{esc(i['pinyin'])}</b> · {esc(i['symbol'])} · above: <b>{up[0]}</b> {up[3]} {up[1]} {up[2]} · below: <b>{lo[0]}</b> {lo[3]} {lo[1]} {lo[2]}</p>
</div>
</div>
{f'<p class="gloss">{esc(gloss)}<small>A one-line gloss written for this site (AI-assisted). Everything below it is the classical text.</small></p>' if gloss else ''}
<div class="actions">
<a class="btn primary" href="../viewers/caster.html">Cast a hexagram</a>
<a class="btn" href="../viewers/cards.html?src=../grammars/i-ching-summarized/grammar.json&amp;hexagram={n}">Open in the card viewer</a>
{app_link}
</div>

<h2 id="judgment">The Judgment <span class="zh">卦辭</span></h2>
<p class="zhtext" lang="zh-Hant">{esc(c.get('Judgment', ''))}</p>
<div class="legge">{paras(judg)}</div>
<p class="src">James Legge, <cite>The Yî King</cite> (1882), the Text. Words in (parentheses) are Legge's own additions.</p>
<details><summary>Commentary on the Judgment 彖傳 (Tuan, the first Wing)</summary><div class="legge">{paras(t.get('Commentary on the Judgment (Tuan, Legge)', ''))}</div></details>

<h2 id="image">The Image <span class="zh">象</span></h2>
<p class="zhtext" lang="zh-Hant">{esc(c.get('Image', ''))}</p>
<div class="legge">{paras(t.get('Great Image (Daxiang)', ''))}</div>
<p class="src">Legge's Great Image (Appendix II). The Chinese above also carries the Small Images of the six lines.</p>

<h2 id="lines">The six lines <span class="zh">爻辭</span></h2>
<p class="src">Read from the bottom (line 1) to the top (line 6). Each line: the Chinese, Legge's translation, and the Small Image commentary on it.</p>
{''.join(lines_html)}

<h2 id="related">Related hexagrams</h2>
<div class="rel">{''.join(related)}</div>

<p class="fine">A hexagram is a mirror, not a command: read it to reflect, never to obey.
Sources: James Legge (tr.), <cite>The Yî King</cite>, Sacred Books of the East vol. XVI (Oxford, 1882; 2nd ed. 1899), public domain;
the Chinese text from Project Gutenberg ebook #25501 (易經), public domain. The trigram facts and the related hexagrams are computed from the line pattern.
The gloss, selection and arrangement are CC-BY-SA-4.0 (PlayfulProcess). Data: <a href="https://github.com/PlayfulProcess/recursive-iching">github.com/PlayfulProcess/recursive-iching</a>.</p>
</article>
<nav class="pn" aria-label="Previous and next hexagram">
<a href="{info[prev_n]['slug']}.html" rel="prev">← {prev_n}. {esc(info[prev_n]['name'])}</a>
<a href="../{HUB}">All 64</a>
<a href="{info[next_n]['slug']}.html" rel="next">{next_n}. {esc(info[next_n]['name'])} →</a>
</nav>"""
        canonical = url(n)
        ld = [
            {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title,
                "description": desc,
                "url": canonical,
                "inLanguage": "en",
                "isPartOf": {"@type": "WebSite", "name": "The Recursive I Ching", "url": SITE},
                "mainEntity": {
                    "@type": "Chapter",
                    "name": f"Hexagram {n}: {i['name']} ({i['zh']} {i['pinyin']})",
                    "position": n,
                    "isPartOf": BOOK,
                    "license": "https://creativecommons.org/publicdomain/mark/1.0/",
                },
                "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "The Recursive I Ching", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "The 64 hexagrams", "item": SITE + HUB},
                    {"@type": "ListItem", "position": 3, "name": f"Hexagram {n}: {i['name']}", "item": canonical},
                ],
            },
        ]
        files[f"{OUT_DIR}/{i['slug']}.html"] = page(
            title, desc, canonical, f"{SITE}img/og/hexagram-{n}.png", ld, body, "../")

    # ── the hub: all 64 as a list and as the 8 x 8 trigram chart ──
    cards = "".join(
        f'<li><a href="{OUT_DIR}/{info[n]["slug"]}.html">{hex_svg(info[n]["bin"], 0.32)}'
        f'<span class="t"><b>{n} · {esc(info[n]["zh"])} {esc(info[n]["pinyin"])}</b>{esc(info[n]["name"])}</span></a></li>'
        for n in range(1, 65))
    head_cells = "".join(f'<th scope="col"><span class="tg">{TRIGRAMS[u][3]}</span>{TRIGRAMS[u][0]}</th>' for u in TRIGRAM_ORDER)
    rows = []
    for lo in TRIGRAM_ORDER:
        cells = []
        for up in TRIGRAM_ORDER:
            n = by_bin[lo + up]
            cells.append(f'<td><a href="{OUT_DIR}/{info[n]["slug"]}.html" title="{esc(info[n]["name"])}">'
                         f'<span class="tg">{esc(info[n]["symbol"])}</span>{n}</a></td>')
        rows.append(f'<tr><th scope="row"><span class="tg">{TRIGRAMS[lo][3]}</span>{TRIGRAMS[lo][0]}</th>{"".join(cells)}</tr>')
    hub_title = "The 64 I Ching Hexagrams: Legge's text, the Chinese, every line"
    hub_desc = ("All 64 hexagrams of the I Ching, one page each: the Judgment, the Image and the six line texts "
                "in James Legge's public-domain translation beside the Chinese original, plus the trigram chart.")
    hub_body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">The Recursive I Ching</a> › The 64 hexagrams</nav>
<p class="kicker">The Zhouyi · King Wen order</p>
<h1>The 64 hexagrams</h1>
<p class="legge">Each hexagram has its own page: the Judgment, the Image and the six line texts in James Legge's
1882 translation, beside the Chinese original, with the Commentary on the Judgment and the Small Images from the
Ten Wings, and the hexagram each changing line leads to. A hexagram is a mirror, not a command.</p>
<div class="actions"><a class="btn primary" href="viewers/caster.html">Cast a hexagram</a>
<a class="btn" href="viewers/cards.html?src=../grammars/i-ching-summarized/grammar.json">Read them as cards</a></div>
<h2>In King Wen order</h2>
<ul class="grid">{cards}</ul>
<h2 id="chart">The hexagram chart</h2>
<p class="src">Rows are the lower trigram, columns the upper trigram. Each cell links to its hexagram.</p>
<div class="chart"><table><thead><tr><th scope="col">below ↓ / above →</th>{head_cells}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="fine">Sources: James Legge (tr.), <cite>The Yî King</cite> (Oxford, 1882; 2nd ed. 1899), public domain;
Project Gutenberg ebook #25501 (易經), public domain. Selection and arrangement CC-BY-SA-4.0 (PlayfulProcess).</p>"""
    hub_ld = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": hub_title,
            "description": hub_desc,
            "url": SITE + HUB,
            "isPartOf": {"@type": "WebSite", "name": "The Recursive I Ching", "url": SITE},
            "about": BOOK,
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": 64,
                "itemListElement": [
                    {"@type": "ListItem", "position": n, "url": url(n), "name": f"Hexagram {n}: {info[n]['name']}"}
                    for n in range(1, 65)
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "The Recursive I Ching", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "The 64 hexagrams", "item": SITE + HUB},
            ],
        },
    ]
    files[HUB] = page(hub_title, hub_desc, SITE + HUB, f"{SITE}img/og/site.png", hub_ld, hub_body, "")
    return files


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")  # a Windows checkout (autocrlf) is the same page


def sitemap_entries(files):
    entries = [(p, pr) for p, pr in STATIC_PAGES.items()]
    entries.append((HUB, "0.9"))
    entries += [(p, "0.7") for p in sorted(files, key=lambda x: int(re.search(r"/(\d+)-", x).group(1)) if x.startswith(OUT_DIR + "/") else 0) if p.startswith(OUT_DIR + "/")]
    return entries


def render_sitemap(entries, lastmod):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generated by scripts/build_hexagram_pages.py; never hand-edit. -->',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio in entries:
        loc = SITE if path == "index.html" else SITE + path
        out.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod[path]['lastmod']}</lastmod><priority>{prio}</priority></url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    check = "--check" in sys.argv
    files = build()
    problems = []
    for rel, text in files.items():
        if read(rel) != text:
            problems.append(f"{rel} is stale")
    if check:
        on_disk = {f for f in os.listdir(os.path.join(ROOT, OUT_DIR))} if os.path.isdir(os.path.join(ROOT, OUT_DIR)) else set()
        extra = on_disk - {os.path.basename(p) for p in files if p.startswith(OUT_DIR + "/")}
        problems += [f"{OUT_DIR}/{e} is not generated by this script" for e in sorted(extra)]
        for n in range(1, 65):
            if not os.path.exists(os.path.join(ROOT, "img", "og", f"hexagram-{n}.png")):
                problems.append(f"img/og/hexagram-{n}.png missing (python scripts/build_og_images.py)")
                break

    entries = sitemap_entries(files)
    lastmod = json.loads(read(LASTMOD) or "{}")
    today = datetime.date.today().isoformat()
    new_lastmod = {}
    for path, _ in entries:
        text = files.get(path) if path in files else read(path)
        if text is None:
            problems.append(f"{path} (listed in the sitemap) does not exist")
            continue
        h = sha(text)
        old = lastmod.get(path)
        if old and old["sha"] == h:
            new_lastmod[path] = old
        else:
            if check:
                problems.append(f"{path} changed since the sitemap's lastmod was set")
            new_lastmod[path] = {"sha": h, "lastmod": today}
    sm = render_sitemap(entries, new_lastmod)
    lm_text = json.dumps(new_lastmod, indent=1, sort_keys=True) + "\n"
    if read("sitemap.xml") != sm:
        problems.append("sitemap.xml is stale")
    if read(LASTMOD) != lm_text:
        problems.append(f"{LASTMOD} is stale")

    if check:
        if problems:
            print("STALE: " + "; ".join(problems[:8]) + (" ..." if len(problems) > 8 else ""))
            print("Fix: python scripts/build_hexagram_pages.py")
            sys.exit(1)
        if "--quiet" not in sys.argv:
            print(f"OK: {len(files) - 1} hexagram pages, the chart and sitemap.xml ({len(entries)} URLs) are current")
        else:
            print("OK")
        return

    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    for rel, text in list(files.items()) + [("sitemap.xml", sm), (LASTMOD, lm_text)]:
        if read(rel) != text:
            with open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    print(f"wrote {len(files) - 1} hexagram pages, {HUB}, sitemap.xml ({len(entries)} URLs)")


if __name__ == "__main__":
    main()
