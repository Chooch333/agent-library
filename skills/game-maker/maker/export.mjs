// usage: node export.mjs <character.js> <character.glb>
// Runs character.js headless and writes character.glb: every part becomes a rigid skinned mesh
// on one skeleton, and each move in ch.clips is baked by sampling ch.pose(name, t) at 30 fps.
// character.js contract (game-maker skill, Character maker):
//   import * as THREE from 'three'
//   createCharacter() -> { root, play(name), update(dt), pose(name, t), clips: { idle: s, walk: s, jump: s } }
//   bones are THREE.Bone, first bone named 'hips', each with userData.rest = its rest position and NO rest
//   rotation (bone rotations are zeroed for the rest pose: angle the meshes under a bone, not the bone);
//   every mesh sits under 'hips' (anything outside it is not exported).
// Refuses cartoon outline shells (BackSide materials): outlines live in the viewer page only.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const [, , srcPath, outPath] = process.argv;
if (!srcPath || !outPath) { console.error('usage: node export.mjs <character.js> <character.glb>'); process.exit(2); }
globalThis.FileReader = class {
  readAsArrayBuffer(b) { b.arrayBuffer().then((r) => { this.result = r; this.onloadend && this.onloadend(); this.onload && this.onload({ target: this }); }); }
  readAsDataURL(b) { b.arrayBuffer().then((r) => { this.result = 'data:' + (b.type || 'application/octet-stream') + ';base64,' + Buffer.from(r).toString('base64'); this.onloadend && this.onloadend(); }); }
};
const THREE = await import('three');
const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js');
// run a copy beside this tool's node_modules so `import 'three'` resolves here
const src = fs.readFileSync(srcPath, 'utf8').replace(/https:\/\/cdn\.jsdelivr\.net\/npm\/three@[^'"]+\/build\/three\.module\.js/g, 'three');
const tmp = path.join(HERE, '.character.run.mjs');
fs.writeFileSync(tmp, src);
const { createCharacter } = await import(pathToFileURL(tmp).href + '?t=' + Date.now());
const ch = createCharacter();
for (const k of ['root', 'pose', 'clips']) if (!ch[k]) { console.error('createCharacter() must return ' + k); process.exit(1); }

const root = ch.root;
const bones = []; root.traverse((o) => { if (o.isBone) bones.push(o); });
if (!bones.length || bones[0].name !== 'hips') { console.error("first bone must be named 'hips' (the arcade kit keeps games in place by it)"); process.exit(1); }
const rest = () => bones.forEach((b) => { b.position.copy(b.userData.rest); b.rotation.set(0, 0, 0); });
rest(); root.updateMatrixWorld(true);

const hips = bones[0];
const meshes = []; hips.traverse((o) => { if (o.isMesh) meshes.push(o); });
const outlines = meshes.filter((m) => [].concat(m.material).some((x) => x.side === THREE.BackSide));
if (outlines.length) { console.error('outline shells found (BackSide): ' + outlines.map((m) => m.name).join(', ') + ' - outlines belong in the viewer only'); process.exit(1); }
const skeleton = new THREE.Skeleton(bones);
const out = new THREE.Group(); out.name = root.name || 'Character';
let ntri = 0; const skinned = [];
for (const m of meshes) {
  let bp = m.parent; while (bp && !bp.isBone) bp = bp.parent;
  const bi = bones.indexOf(bp);
  const g = m.geometry.clone().applyMatrix4(m.matrixWorld);
  if (g.index === null) g.setIndex([...Array(g.attributes.position.count).keys()]);
  const n = g.attributes.position.count, si = new Uint8Array(n * 4), sw = new Uint8Array(n * 4);
  for (let i = 0; i < n; i++) { si[i * 4] = bi; sw[i * 4] = 255; }
  g.setAttribute('skinIndex', new THREE.BufferAttribute(si, 4));
  g.setAttribute('skinWeight', new THREE.BufferAttribute(sw, 4, true));
  for (const k of Object.keys(g.attributes)) if (!['position', 'normal', 'color', 'skinIndex', 'skinWeight', 'uv'].includes(k)) g.deleteAttribute(k);
  if (m.matrixWorld.determinant() < 0) { const idx = g.index.array; for (let i = 0; i < idx.length; i += 3) { const t = idx[i + 1]; idx[i + 1] = idx[i + 2]; idx[i + 2] = t; } }
  const sm = new THREE.SkinnedMesh(g, m.material.clone()); sm.name = m.name;
  ntri += g.index.count / 3; skinned.push(sm);
}
for (const m of meshes) m.parent.remove(m);
root.remove(hips); out.add(hips);
for (const sm of skinned) out.add(sm);
out.updateMatrixWorld(true);
for (const sm of skinned) sm.bind(skeleton, new THREE.Matrix4());

const fps = 30, clips = [];
for (const [name, dur] of Object.entries(ch.clips)) {
  const N = Math.round(dur * fps), times = [], P = bones.map(() => []), Q = bones.map(() => []);
  for (let f = 0; f <= N; f++) {
    const t = (f / N) * dur; times.push(t);
    ch.pose(name, f === N ? 0 : t);
    bones.forEach((b, i) => { P[i].push(...b.position.toArray()); Q[i].push(...b.quaternion.toArray()); });
  }
  const tracks = [];
  bones.forEach((b, i) => {
    tracks.push(new THREE.VectorKeyframeTrack(b.name + '.position', times, P[i]));
    tracks.push(new THREE.QuaternionKeyframeTrack(b.name + '.quaternion', times, Q[i]));
  });
  clips.push(new THREE.AnimationClip(name, dur, tracks));
}
rest(); out.updateMatrixWorld(true);
const glb = await new GLTFExporter().parseAsync(out, { binary: true, animations: clips });
fs.writeFileSync(outPath, Buffer.from(glb));
fs.rmSync(tmp, { force: true });
console.log(JSON.stringify({ triangles: ntri, bytes: glb.byteLength, meshes: skinned.length, bones: bones.length, clips: Object.keys(ch.clips) }));
if (glb.byteLength > 2e6) console.error(`WARNING: ${(glb.byteLength / 1e6).toFixed(2)} MB is over the 2 MB cap - lower segment counts, not shapes`);
