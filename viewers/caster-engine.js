/* The Recursive I Ching — Path Caster engine (docs/DESIGN-path-caster.md).
 * Pure functions, no DOM: the 6-bit hexagram hypercube math + path generation +
 * traditional-randomizer line casting. Shared between caster.html (browser) and
 * scripts/determinism-check.js (Node, run at the CLI to prove the "final step
 * always arrives" guarantee across many random trials — see that script and
 * the design doc's own §Verify).
 *
 * Binary convention (matches scripts/hexagram-binary.json's _meta.convention):
 * bottom-to-top. Character index 0 = Line 1 (bottom line), index 5 = Line 6
 * (top line). '1' = yang/solid, '0' = yin/broken.
 */
(function (root) {
  'use strict';

  // ── hypercube math ────────────────────────────────────────────────────
  function hamming(a, b) {
    let d = 0;
    for (let i = 0; i < 6; i++) if (a[i] !== b[i]) d++;
    return d;
  }
  function diffIndices(a, b) {
    const out = [];
    for (let i = 0; i < 6; i++) if (a[i] !== b[i]) out.push(i);
    return out;
  }
  function flipBit(bin, idx) {
    const arr = bin.split('');
    arr[idx] = arr[idx] === '1' ? '0' : '1';
    return arr.join('');
  }

  // ── traditional randomizers (docs/DESIGN-path-caster.md: "three-coin method
  //    by default; yarrow probabilities as a setting — same honest-randomness
  //    note the tarot caster carries"). Both methods are 50/50 yin/yang per
  //    line overall; they differ in the classical 6/7/8/9 distribution, which
  //    is what makes the toggle an honest nod to two real historical methods
  //    rather than a cosmetic label on the same coin flip. ──────────────────
  function castLineValue(method) {
    if (method === 'yarrow') {
      // Classical yarrow-stalk probabilities (Wilhelm/Baynes appendix):
      // 6 (old yin) = 1/16, 7 (young yang) = 5/16, 8 (young yin) = 7/16, 9 (old yang) = 3/16.
      const r = Math.random();
      if (r < 1 / 16) return '0';               // 6, old yin
      if (r < 1 / 16 + 5 / 16) return '1';       // 7, young yang
      if (r < 1 / 16 + 5 / 16 + 7 / 16) return '0'; // 8, young yin
      return '1';                                 // 9, old yang
    }
    // Three-coin method: each coin heads(3)/tails(2) at 50/50; sum of three
    // coins is 6-9; even sums (6, 8) = yin, odd sums (7, 9) = yang.
    let sum = 0;
    for (let i = 0; i < 3; i++) sum += Math.random() < 0.5 ? 3 : 2;
    return (sum % 2 === 0) ? '0' : '1';
  }
  function castBinary(method) {
    let bits = '';
    for (let i = 0; i < 6; i++) bits += castLineValue(method); // index i = Line (i+1), bottom-to-top
    return bits;
  }

  // ── step-budget validity (docs/DESIGN-path-caster.md: "wandering paths ...
  //    any step budget >= d with the same parity ... each detour costs 2") ──
  function validBudgets(d, style, maxExtra) {
    maxExtra = maxExtra == null ? 6 : maxExtra;
    if (style === 'direct') {
      // Direct = the d! minimal-route orderings only; budget is fixed at d.
      // (d===0 direct is the trivial "already there" case — still offered so
      // the UI can say so rather than silently disabling everything.)
      return [d];
    }
    // Wandering: d, d+2, d+4, ... up to d+maxExtra. If d===0 a 0-step
    // "journey" is offered too (identical to direct's only case), plus loop
    // budgets (2, 4, 6, ...) that leave and return — legitimate per the
    // design doc ("nothing prevents loops ... a legitimate reading").
    const out = [];
    for (let extra = 0; extra <= maxExtra; extra += 2) out.push(d + extra);
    return out;
  }

  // ── path generation ───────────────────────────────────────────────────
  // Returns [{binary, flippedIdx}], one entry per hexagram in the stack
  // (path[0].flippedIdx === null — it's the origin, nothing flipped yet to
  // reach it). `budget` is the total number of line-flips (== path.length-1).
  // `style` is 'direct' (only ever flips a currently-differing line — the
  // d! minimal-route family) or 'wandering' (may also flip a matching line
  // as a deliberate detour, biased toward eventually closing the gap).
  // The FINAL flip is always deterministic: whatever single line still
  // differs gets flipped, guaranteeing arrival at the destiny hexagram.
  function feasible(c, stepsLeft) {
    // Can `c` (currently-differing-line count) reach exactly 1 in `stepsLeft`
    // more ordinary flips, staying within the hypercube's 0-6 dimensions and
    // respecting flip parity (each flip changes c by exactly ±1)?
    if (c < 1 || c > 6) return false;
    const need = Math.abs(c - 1);
    return stepsLeft >= need && (stepsLeft - need) % 2 === 0;
  }
  function buildPath(originBin, destBin, budget, style) {
    let cur = originBin;
    const path = [{ binary: cur, flippedIdx: null }];
    for (let step = 1; step <= budget; step++) {
      const diff = diffIndices(cur, destBin);
      const same = [];
      for (let i = 0; i < 6; i++) if (diff.indexOf(i) === -1) same.push(i);
      let idx;
      if (diff.length === 0) {
        // Only reachable when the origin already equals the destiny (d===0)
        // and the user asked for a wandering "loop" budget > 0: the first
        // move must be a deliberate detour (there's nothing to "close" yet).
        idx = same[Math.floor(Math.random() * same.length)];
      } else if (step === budget) {
        // Deterministic final step: by construction exactly one line still
        // differs here — flip it and the destiny is reached.
        idx = diff[0];
      } else if (style === 'direct') {
        idx = diff[Math.floor(Math.random() * diff.length)];
      } else {
        const stepsLeftAfterThis = budget - step - 1;
        const c = diff.length;
        const canClose = feasible(c - 1, stepsLeftAfterThis);
        const canDetour = same.length > 0 && feasible(c + 1, stepsLeftAfterThis);
        let doClose;
        if (canClose && canDetour) doClose = Math.random() < 0.7; // bias toward closing
        else doClose = canClose || !canDetour;
        idx = doClose ? diff[Math.floor(Math.random() * diff.length)] : same[Math.floor(Math.random() * same.length)];
      }
      cur = flipBit(cur, idx);
      path.push({ binary: cur, flippedIdx: idx });
    }
    return path;
  }

  const CasterEngine = { hamming, diffIndices, flipBit, castLineValue, castBinary, validBudgets, buildPath };

  if (typeof module !== 'undefined' && module.exports) module.exports = CasterEngine;
  else root.CasterEngine = CasterEngine;
})(typeof window !== 'undefined' ? window : globalThis);
