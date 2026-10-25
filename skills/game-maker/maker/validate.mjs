// usage: node validate.mjs <character.glb> <validation.json>
// Khronos glTF validator. Prints errors / warnings / clip names / triangles.
import fs from 'node:fs';
import validator from 'gltf-validator';
const [, , glb, out] = process.argv;
const report = await validator.validateBytes(new Uint8Array(fs.readFileSync(glb)), { uri: 'character.glb' });
fs.writeFileSync(out, JSON.stringify(report, null, 2));
const i = report.issues, info = report.info || {};
console.log(JSON.stringify({ errors: i.numErrors, warnings: i.numWarnings, clips: info.animationCount,
  triangles: info.totalTriangleCount, firstMessages: i.messages.slice(0, 5).map((m) => m.code + ': ' + m.message) }));
process.exit(i.numErrors ? 1 : 0);
