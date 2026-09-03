#!/usr/bin/env node
/* Determinism proof for the Path Caster (docs/DESIGN-path-caster.md §Verify):
 * "run the deterministic-last-step logic across 50 random start/destiny/step-budget
 * combinations ... assert the final hexagram always equals the destiny."
 *
 * Run:  node scripts/determinism-check.js
 */
const CasterEngine = require('../viewers/caster-engine.js');

const TRIALS = 50;
const randomBinary = () => {
  let s = '';
  for (let i = 0; i < 6; i++) s += Math.random() < 0.5 ? '0' : '1';
  return s;
};

let failures = 0;
for (let t = 1; t <= TRIALS; t++) {
  const origin = randomBinary();
  const destiny = randomBinary();
  const d = CasterEngine.hamming(origin, destiny);
  const style = Math.random() < 0.5 ? 'direct' : 'wandering';
  const budgets = CasterEngine.validBudgets(d, style, 6);
  const budget = budgets[Math.floor(Math.random() * budgets.length)];

  const path = CasterEngine.buildPath(origin, destiny, budget, style);
  const arrived = path[path.length - 1].binary === destiny;
  const lengthOk = path.length === budget + 1;

  // Also confirm every intermediate step really only flips ONE line versus
  // the previous entry (the "a step is one changing line" invariant).
  let oneFlipEachStep = true;
  for (let i = 1; i < path.length; i++) {
    if (CasterEngine.hamming(path[i - 1].binary, path[i].binary) !== 1) oneFlipEachStep = false;
  }

  const ok = arrived && lengthOk && oneFlipEachStep;
  if (!ok) {
    failures++;
    console.error(`[FAIL] trial ${t}: origin=${origin} destiny=${destiny} d=${d} style=${style} budget=${budget}` +
      ` arrived=${arrived} lengthOk=${lengthOk} oneFlipEachStep=${oneFlipEachStep}`);
  } else {
    console.log(`[ok] trial ${t}: origin=${origin} destiny=${destiny} d=${d} style=${style} budget=${budget} -> arrived at ${path[path.length - 1].binary} in ${path.length - 1} steps`);
  }
}

console.log(`\n${TRIALS - failures}/${TRIALS} trials arrived at the chosen destiny with valid single-line steps.`);
if (failures > 0) {
  console.error(`${failures} FAILURES — determinism guarantee is broken.`);
  process.exit(1);
}
console.log('Determinism check PASSED.');
