// Load character.glb (rest pose or a clip time) and dump world-space triangles for the software renderer.
import fs from 'fs';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
const [glbPath, outPath, clip, t] = process.argv.slice(2);
const buf = fs.readFileSync(glbPath);
const ab = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
const gltf = await new Promise((res, rej) => new GLTFLoader().parse(ab, '', res, rej));
const scene = gltf.scene;
if (clip) { const mx = new THREE.AnimationMixer(scene); mx.clipAction(gltf.animations.find((a) => a.name === clip)).play(); mx.update(parseFloat(t)); }
scene.updateMatrixWorld(true);
const P = [], N = [], C = [], I = [];
const v = new THREE.Vector3(), n = new THREE.Vector3(), c = new THREE.Color(), o3 = {};
let id = 0;
scene.traverse((o) => {
  if (!o.isMesh) return;
  const g = o.geometry, idx = g.index, pos = g.attributes.position, col = g.attributes.color;
  const mc = o.material.color.clone();
  if (o.isSkinnedMesh) o.skeleton.update();
  const nm = new THREE.Matrix3();
  const verts = [], norms = [];
  for (let i = 0; i < pos.count; i++) {
    o.getVertexPosition(i, v); v.applyMatrix4(o.matrixWorld); verts.push(v.clone());
  }
  // recompute normals from posed positions (smooth)
  const acc = verts.map(() => new THREE.Vector3());
  const cnt = idx ? idx.count : pos.count, get = (k) => (idx ? idx.getX(k) : k);
  const e1 = new THREE.Vector3(), e2 = new THREE.Vector3();
  for (let k = 0; k < cnt; k += 3) {
    const a = get(k), b = get(k + 1), d = get(k + 2);
    e1.subVectors(verts[b], verts[a]); e2.subVectors(verts[d], verts[a]);
    const fn = new THREE.Vector3().crossVectors(e1, e2);
    acc[a].add(fn); acc[b].add(fn); acc[d].add(fn);
  }
  acc.forEach((q) => q.normalize());
  for (let k = 0; k < cnt; k += 3) {
    for (let j = 0; j < 3; j++) {
      const vi = get(k + j);
      P.push(verts[vi].x, verts[vi].y, verts[vi].z); N.push(acc[vi].x, acc[vi].y, acc[vi].z);
      if (col) c.setRGB(col.getX(vi), col.getY(vi), col.getZ(vi)); else c.setRGB(1, 1, 1);
      c.multiply(mc); C.push(c.r, c.g, c.b); // linear
    }
    I.push(id);
  }
  id++;
});
fs.writeFileSync(outPath, Buffer.concat([Buffer.from(new Float32Array([I.length]).buffer), Buffer.from(new Float32Array(P).buffer), Buffer.from(new Float32Array(N).buffer), Buffer.from(new Float32Array(C).buffer), Buffer.from(new Int32Array(I).buffer)]));
console.log('tris', I.length);
