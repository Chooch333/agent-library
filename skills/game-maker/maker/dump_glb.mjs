// Loads a .glb with Three.js (exactly as a browser game would), poses it,
// and dumps world-space triangles + sRGB colours + part names for the rasteriser.
// usage: node dump_glb.mjs <in.glb> <outPrefix> [clipName] [timeSeconds]
import fs from 'node:fs';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const [, , glbPath, outPrefix, clipName, tArg] = process.argv;
globalThis.self = globalThis;
const buf = fs.readFileSync(glbPath);
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);

new GLTFLoader().parse(ab, '', (gltf) => {
  const scene = gltf.scene;
  if (clipName) {
    const clip = gltf.animations.find((a) => a.name === clipName);
    if (clip) {
      const mixer = new THREE.AnimationMixer(scene);
      mixer.clipAction(clip).play();
      mixer.update(parseFloat(tArg || '0'));
    } else console.error(`clip ${clipName} not found; using rest pose`);
  }
  scene.updateMatrixWorld(true);

  const pos = [], col = [], part = [], side = [], names = [];
  const v = new THREE.Vector3(), c = new THREE.Color(), s = {};
  let textured = 0;
  scene.traverse((o) => {
    if (!o.isMesh) return;
    for (let p = o; p; p = p.parent) if (p.visible === false) return;
    const g = o.geometry, idx = g.index, P = g.attributes.position, C = g.attributes.color;
    const mats = Array.isArray(o.material) ? o.material : [o.material];
    const n = idx ? idx.count : P.count;
    const groups = g.groups.length ? g.groups : [{ start: 0, count: n, materialIndex: 0 }];
    const id = names.length;
    names.push(o.name || (o.parent && o.parent.name) || `mesh${id}`);
    for (const gr of groups) {
      const m = mats[gr.materialIndex] || mats[0];
      if (!m || m.visible === false || (m.transparent && m.opacity < 0.5)) continue;
      if (m.map) textured++;
      const mc = m.color ? m.color.clone() : new THREE.Color(1, 1, 1);
      const end = Math.min(gr.start + gr.count, n);
      for (let k = gr.start; k + 2 < end + 0; k += 3) {
        for (let j = 0; j < 3; j++) {
          const vi = idx ? idx.getX(k + j) : k + j;
          o.getVertexPosition(vi, v);
          v.applyMatrix4(o.matrixWorld);
          pos.push(v.x, v.y, v.z);
          if (C) c.setRGB(C.getX(vi), C.getY(vi), C.getZ(vi)); else c.setRGB(1, 1, 1);
          c.multiply(mc);
          c.getRGB(s, THREE.SRGBColorSpace);
          col.push(s.r, s.g, s.b);
        }
        part.push(id);
        side.push(m.side ?? 0);
      }
    }
  });
  const nt = part.length;
  const out = Buffer.concat([
    Buffer.from(new Float32Array(pos).buffer),
    Buffer.from(new Float32Array(col).buffer),
    Buffer.from(new Int32Array(part).buffer),
    Buffer.from(new Int8Array(side).buffer),
  ]);
  fs.writeFileSync(outPrefix + '.bin', out);
  fs.writeFileSync(outPrefix + '.json', JSON.stringify({ ntri: nt, names, textured,
    clips: gltf.animations.map((a) => a.name),
    durations: Object.fromEntries(gltf.animations.map((a) => [a.name, a.duration])) }));
  console.log(`dumped ${nt} triangles, ${names.length} parts${textured ? `, ${textured} textured materials (texture ignored)` : ''}`);
}, (e) => { console.error('GLB load failed:', e.message || e); process.exit(1); });
