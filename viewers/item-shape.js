/**
 * Ported Oct 4 2026 from recursive-eco apps/landing/assets/js/components/item-shape.js (c164d95), unchanged.
 * Change it there first; this copy follows.
 * item-shape.js — what an item IS, read from its own fields (Oct 3 2026, round D-3).
 *
 * A grammar is a grammar (CLAUDE.md, "Grammar types are dead code"). What
 * makes a deck tarot-shaped or a book hexagram-shaped is the data inside
 * its items, not a type stamp on the row or a `?type=` in the URL. The
 * Cards viewer (grammar-viewer.html) asks these helpers instead of
 * branching on `grammarType`.
 *
 *   isHexagramItem(item)  — a number from 1 to 64 plus binary / trigram /
 *                           Chinese-name fields. Drives the Chinese name,
 *                           the trigrams and the "hexagrams" copy.
 *   isTarotCardItem(item) — has `arcana` and/or `suit`. Drives the REV badge
 *                           and the reversal toggle.
 *   majorityShape(items)  — 'iching' | 'tarot' | 'plain': the shape more than
 *                           half the items have. A grammar's theme.
 *   resolveShape(typeParam, data)
 *                         — the `?type=` param when it names a known shape (a
 *                           manual override callers still send), otherwise the
 *                           shape the data has. Never requires the param.
 *
 * Works on raw nodes (document_data.nodes) and on the viewer's normalized
 * items alike: both keep `metadata`, and the normalized ones lift
 * chinese_name / trigram_* to the top level.
 *
 * Pure functions, no DOM. Pinned by apps/landing/scripts/test-item-shape.mjs.
 */
(function (global) {
    'use strict';

    // `?type=` values that name a shape. Anything else a caller sends
    // ('custom', 'sequence', 'tarot-deck', 'unified', ...) is ignored and
    // the data decides.
    var OVERRIDES = ['tarot', 'iching', 'astrology', 'course'];

    function meta(item) {
        return (item && item.metadata && typeof item.metadata === 'object') ? item.metadata : {};
    }

    function present(v) {
        return v !== undefined && v !== null && v !== '';
    }

    function hexagramNumberCandidates(item) {
        var m = meta(item);
        return [item.hexagram_number, m.hexagram_number, m.king_wen, m.number, item.number];
    }

    function isHexagramItem(item) {
        if (!item || typeof item !== 'object') return false;
        var m = meta(item);
        var hasNumber = hexagramNumberCandidates(item).some(function (n) {
            var x = typeof n === 'string' ? parseInt(n, 10) : n;
            return Number.isInteger(x) && x >= 1 && x <= 64;
        });
        if (!hasNumber) return false;
        return [
            item.binary, m.binary,
            item.trigram_above, m.trigram_above, item.trigram_below, m.trigram_below,
            item.chinese_name, m.chinese_name,
        ].some(present);
    }

    function isTarotCardItem(item) {
        if (!item || typeof item !== 'object') return false;
        var m = meta(item);
        return [item.arcana, item.suit, m.arcana, m.suit].some(present);
    }

    function itemShape(item) {
        if (isHexagramItem(item)) return 'hexagram';
        if (isTarotCardItem(item)) return 'tarot';
        return 'plain';
    }

    function majorityShape(items) {
        if (!Array.isArray(items) || items.length === 0) return 'plain';
        var hex = 0, tarot = 0;
        items.forEach(function (it) {
            var s = itemShape(it);
            if (s === 'hexagram') hex++;
            else if (s === 'tarot') tarot++;
        });
        var half = items.length / 2;
        if (hex > half) return 'iching';
        if (tarot > half) return 'tarot';
        return 'plain';
    }

    // Every item list a grammar document can carry: the `nodes` array,
    // `emergences`, and the legacy `hexagrams` / `cards` arrays.
    function grammarItems(data) {
        if (!data || typeof data !== 'object') return [];
        var out = [];
        ['nodes', 'emergences', 'hexagrams', 'cards'].forEach(function (k) {
            if (Array.isArray(data[k])) out = out.concat(data[k]);
        });
        return out;
    }

    // The legacy astrology document (planets / signs / houses arrays, no items).
    function isLegacyAstrology(data) {
        if (!data || typeof data !== 'object') return false;
        return ['planets', 'signs', 'houses'].some(function (k) {
            return Array.isArray(data[k]) && data[k].length > 0;
        });
    }

    function grammarShape(data) {
        var items = grammarItems(data);
        if (items.length === 0 && isLegacyAstrology(data)) return 'astrology';
        return majorityShape(items);
    }

    function typeOverride(typeParam) {
        var t = String(typeParam || '').trim().toLowerCase();
        return OVERRIDES.indexOf(t) >= 0 ? t : null;
    }

    function resolveShape(typeParam, data) {
        return typeOverride(typeParam) || grammarShape(data);
    }

    var api = {
        OVERRIDES: OVERRIDES.slice(),
        isHexagramItem: isHexagramItem,
        isTarotCardItem: isTarotCardItem,
        itemShape: itemShape,
        majorityShape: majorityShape,
        grammarItems: grammarItems,
        isLegacyAstrology: isLegacyAstrology,
        grammarShape: grammarShape,
        typeOverride: typeOverride,
        resolveShape: resolveShape,
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = api;
    }
    if (global) global.ItemShape = api;
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this));
