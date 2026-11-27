// node unit-tower/test-meshfix.cjs — checks the Bambu-style STL check / repair (MeshFix) and the merged tower solid
const fs = require('fs'), path = require('path'), assert = require('assert');
const load = f => fs.readFileSync(path.join(__dirname, f), 'utf8');
const html = load('index.html'), cat = fs.readFileSync(path.join(__dirname, '../minimal-surfaces/index.html'), 'utf8');
const block = h => h.slice(h.indexOf('// ===================== MESHFIX-BEGIN'), h.indexOf('// ===================== MESHFIX-END'));
assert.strictEqual(block(html), block(cat), 'MeshFix must be the same code in unit-tower/ and minimal-surfaces/');
const src = html.slice(html.indexOf('// ===================== CORE-BEGIN'), html.indexOf('// ===================== CORE-END'));
const m = { exports: {} }; new Function('module', 'TextDecoder', src)(m, TextDecoder);
const Core = m.exports, M = Core.MeshFix;
const soup = (V, F) => M.parseSTL(Core.meshSTL(Float64Array.from(V), Uint32Array.from(F), 'test'));
// 1. labels: one closed solid per text, no shared edges
for (const txt of ['18-2', '1-1', '20-1', '7-2', '0-1', '4-2', '8-8']) {
  const H = 3.2, g = Core.glyphRects(txt, H * 0.6, H, Math.max(0.6, H * 0.16), H * 0.2);
  for (const map of [(u, v) => [u, v], (u, v) => [-v, u]]) {
    const V = [], F = []; Core.rectSolid(g.R, 0.5, 1.2, map, V, F);
    const c = M.meshCheck(soup(V, F)); assert(c.ok, 'label ' + txt + ' ' + JSON.stringify(c));
    assert(Core.volumeCentroid(Float64Array.from(V), Uint32Array.from(F)).vol > 0, 'label faces outward');
  }
}
// 2. two boxes touching along one edge (4 faces on it); repair separates them
const V = [], F = [];
const quadBox = (x0, y0, x1, y1) => { const b = V.length / 3; V.push(x0, y0, 0, x1, y0, 0, x1, y1, 0, x0, y1, 0, x0, y0, 1, x1, y0, 1, x1, y1, 1, x0, y1, 1);
  for (const [i, j, k] of [[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5], [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7]]) F.push(b + i, b + j, b + k); };
quadBox(0, 0, 1, 1); quadBox(1, 1, 2, 2);
const bad = soup(V, F), c0 = M.meshCheck(bad);
assert(c0.nonManifold === 1 && !c0.ok, 'two boxes share one edge: ' + JSON.stringify(c0));
const r = M.repairBest(bad); assert(r.after.ok, 'repaired: ' + JSON.stringify(r.after));
// flipped faces are turned back
const Fr = F.slice(); for (let i = 0; i < 6; i += 3) { const t = Fr[i + 1]; Fr[i + 1] = Fr[i + 2]; Fr[i + 2] = t; }
const r2 = M.repairBest(soup(V, Fr)); assert(r2.after.ok && r2.before.reversed > 0, 'reversed faces fixed');
// a hole is closed
const r3 = M.repairBest(soup(V.slice(0, 24), F.slice(0, 33))); assert(r3.after.ok && r3.holes === 1, 'hole closed');
// 4. not an STL
assert(!M.isSTL(new ArrayBuffer(10)) && !M.isSTL(new Uint8Array(200).fill(7).buffer), 'junk is not an STL');
assert(M.isSTL(Core.meshSTL(Float64Array.from(V), Uint32Array.from(F), 'x')), 'binary STL recognised');
// 5. sew: a sheet split down the middle with the two edges 1e-6 apart is welded back into one; a real slit stays open
{
  const sheet = (gap, slit) => {
    const n = 20, Vs = [], Fs = [], id = (i, j, side) => side * (n + 1) * (n + 1) + j * (n + 1) + i;
    for (const side of [0, 1]) for (let j = 0; j <= n; j++) for (let i = 0; i <= n; i++) Vs.push((side ? 1 + gap : 0) + i / n, j / n, 0);
    for (const side of [0, 1]) for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) { const a = id(i, j, side), b = id(i + 1, j, side), c = id(i + 1, j + 1, side), d = id(i, j + 1, side); Fs.push(a, b, c, a, c, d); }
    return { V: Float64Array.from(Vs), F: Uint32Array.from(Fs) };
  };
  const a = Core.sew(sheet(1e-6)), b = Core.sew(sheet(0.02));
  assert.strictEqual(Core.edgeStats(a.F, a.V.length / 3).boundary.length, 2 * (40 + 20), 'seam welded: only the outer edge stays open');
  assert(!b.sewn, 'a 0.02 slit is not a seam');
}
// 6. simplifying a dense wavy sheet keeps its open edge and stays close to it
(async () => {
  const n = 120, Vs = [], Fs = [];
  for (let j = 0; j <= n; j++) for (let i = 0; i <= n; i++) { const x = i / n, y = j / n; Vs.push(x, y, 0.05 * Math.sin(6 * x) * Math.cos(5 * y)); }
  for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) { const a = j * (n + 1) + i; Fs.push(a, a + 1, a + n + 2, a, a + n + 2, a + n + 1); }
  const A = { V: Float64Array.from(Vs), F: Uint32Array.from(Fs) }, B = await Core.simplifyMesh(A.V, A.F, { target: 2000 });
  assert(B.V.length / 3 <= 2000, 'reached the target');
  assert.strictEqual(Core.edgeStats(B.F, B.V.length / 3).boundary.length, 4 * n, 'open edge untouched');
  const dev = await Core.meshDeviation(A, B); assert(dev < 0.004, 'stays close: ' + dev);
  console.log('PASS: labels are closed solids, MeshFix splits shared edges, turns faces, closes holes, rejects non-STL; sew welds a split seam but keeps a real slit; simplify keeps the open edge (deviation ' + dev.toFixed(4) + '); both pages carry the same MeshFix.');
})();
