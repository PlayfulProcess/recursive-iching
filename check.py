#!/usr/bin/env python3
"""Minimal grammar gate for a starter site — run before you commit.

Walks grammars/*/grammar.json (or pass paths as args), validates each
against the canonical shape the recursive.eco family's viewers expect, and
fails loud on the mistakes that keep a grammar from loading. Zero dependencies.

Ported from recursive-astrology/check.py (itself the family's shared shape —
recursive-tarot has the same gate as scripts/check_all.py). This repo had no
validator of its own until now; every other active repo in the family does,
so this closes that gap rather than leaving grammars unchecked.

    python3 check.py            # check every grammar under grammars/
    python3 check.py path.json  # check one file
"""
import json
import re
import sys
from pathlib import Path

VALID_TYPES = {
    "tarot", "iching", "astrology", "sequence",
    "course", "prompt", "birthchart", "altar", "music", "custom",
}

# Trigram guard (Oct 14 2026). trigram_above / trigram_below were once swapped in 56 of the 64
# hexagrams of i-ching-chinese-original. The lines are the truth: scripts/hexagram-binary.json
# holds each hexagram bottom to top, so the lower trigram is the first three lines and the upper
# trigram the last three (11 Tai = Kun above, Qian below; 12 Pi = Qian above, Kun below).
TRIGRAM_BITS = {
    "heaven": "111", "earth": "000", "thunder": "100", "water": "010",
    "mountain": "001", "wind": "011", "fire": "101", "lake": "110",
}
_BITS_TRIGRAM = {v: k for k, v in TRIGRAM_BITS.items()}


def _trigram_name(value) -> str | None:
    """'heaven' or a glyph form like '<glyph> Qian (Heaven)' / '(Wind/Wood)' -> 'heaven'."""
    if not isinstance(value, str):
        return None
    m = re.search(r"\(([A-Za-z]+)", value)
    return (m.group(1) if m else value).strip().lower()


def _line_table() -> dict:
    try:
        raw = json.loads((Path(__file__).parent / "scripts" / "hexagram-binary.json").read_text(encoding="utf-8"))
        return {int(k): v["binary"] for k, v in raw["hexagrams"].items()}
    except Exception:  # noqa: BLE001
        return {}


LINES = _line_table()


def check_trigrams(path: Path, items: list) -> list[str]:
    """Fail when a hexagram's trigram_above / trigram_below disagree with its lines."""
    errs = []
    for it in items:
        meta = it.get("metadata") or {}
        n = meta.get("number", it.get("number"))
        above = meta.get("trigram_above", it.get("trigram_above"))
        below = meta.get("trigram_below", it.get("trigram_below"))
        if above is None and below is None:
            continue
        if not isinstance(n, int) or not 1 <= n <= 64 or "role" in meta:
            continue
        lines = LINES.get(n)
        if not lines:
            errs.append(f"{path}: hexagram {n} has no line pattern in scripts/hexagram-binary.json")
            continue
        want_below, want_above = _BITS_TRIGRAM[lines[:3]], _BITS_TRIGRAM[lines[3:]]
        got_above, got_below = _trigram_name(above), _trigram_name(below)
        if (got_above, got_below) != (want_above, want_below):
            errs.append(
                f"{path}: hexagram {n} ({it.get('id') or it.get('name')}) has trigram_above={above!r}, "
                f"trigram_below={below!r}, but its lines {lines} (bottom to top) make {want_above} above and "
                f"{want_below} below"
            )
        own = meta.get("binary")
        if own is not None and own != lines:
            errs.append(f"{path}: hexagram {n} has metadata.binary {own!r}, but scripts/hexagram-binary.json says {lines!r}")
    return errs


def check(path: Path) -> list[str]:
    errs = []
    try:
        g = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"{path}: not valid JSON — {e}"]

    for field in ("name", "description", "grammar_type"):
        if field not in g:
            errs.append(f"{path}: missing required top-level '{field}'")
    if g.get("grammar_type") not in VALID_TYPES:
        errs.append(f"{path}: grammar_type '{g.get('grammar_type')}' is not one of {sorted(VALID_TYPES)}")
    if "emergences" in g:
        errs.append(f"{path}: has a top-level 'emergences' array — move those items into nodes[] with parts")
    items = g.get("nodes")
    if not isinstance(items, list) or not items:
        errs.append(f"{path}: 'nodes' must be a non-empty array")
        return errs

    ids = {it.get("id") for it in items}
    for it in items:
        for field in ("id", "name", "sections"):
            if field not in it:
                errs.append(f"{path}: item {it.get('id') or it.get('name') or '?'} missing '{field}'")
        for child in it.get("parts", []):
            if child not in ids:
                errs.append(f"{path}: parts references missing id '{child}'")
        meta = it.get("metadata") or {}
        if "video_id" in meta:
            errs.append(f"{path}: item {it.get('id')} uses metadata.video_id — rename to youtube_video_id")
        # A hexagram carries its King Wen number at the TOP level too: the recursive.eco viewer's
        # relating-hexagram lookup reads item.number and otherwise falls back to the position
        # (finding V-1, Oct 2026). Frame items (metadata.role) are not hexagrams.
        n = meta.get("number")
        if isinstance(n, int) and 1 <= n <= 64 and "role" not in meta and it.get("number") != n:
            errs.append(f"{path}: hexagram item {it.get('id')} has metadata.number {n} but top-level number {it.get('number')!r} — add \"number\": {n}")
    errs += check_trigrams(path, items)
    return errs


def main() -> int:
    args = sys.argv[1:]
    root = Path(__file__).parent
    paths = [Path(a) for a in args] if args else sorted(root.glob("grammars/*/grammar.json"))
    if not paths:
        print("No grammars found under grammars/*/grammar.json")
        return 1
    all_errs = []
    for p in paths:
        all_errs += check(p)
    if all_errs:
        print("\n".join(all_errs))
        print(f"\nFAILED: {len(all_errs)} problem(s) across {len(paths)} grammar(s)")
        return 1
    print(f"OK: all checks passed ({len(paths)} grammar{'s' if len(paths) != 1 else ''})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
