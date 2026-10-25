# 2D-3D Maker tool

The code the game-maker skill's **Character maker** runs (SKILL.md, section "Character maker").
It measures and packages a character; it holds **no shapes and no parts from any character**. Every character
is built from scratch in its own `character.js` (run E, 2026-10-25, is the standard).

| File | What it does | Run it |
|---|---|---|
| `heatmap.py` + `dump_glb.mjs` | Likeness heat map: renders the .glb front-on, lines it up with the drawing, checks a 32×32 grid for SHAPE, DARK details and COLOUR, names the worst areas and the parts in them. Writes `heatmap.png`, `report.md`, `report.json` (score + `fit`), `render_match.png`, `region_N.png`. ~15 s. | `python3 heatmap.py --drawing D --glb G --out DIR` (`--clip walk --time 0.3` to check a move frame; `--yaw DEG` if the model does not face +Z) |
| `export.mjs` | `character.js` → `character.glb`: rigid skinned parts on one skeleton, idle/walk/jump baked at 30 fps. Refuses outline shells; warns over 2 MB. | `node export.mjs character.js character.glb` |
| `validate.mjs` | Khronos glTF validator → `validation.json`; exits 1 on any error. | `node validate.mjs character.glb validation.json` |
| `still.py` + `still_dump.mjs` | `still.png` 1000×1000, front three-quarter, toon shading, ink outlines, read from the .glb (what a game loads). | `python3 still.py character.glb still.png [yaw=32]` |
| `viewer.html` | Viewer page: orbit, ground, one button per move. Replace `CHARACTER_NAME`; loads `./character.js`. | publish beside `character.js` |
| `package.json` | Three.js **0.160.0** (the arcade kit's version) + gltf-validator. | `npm i` in this folder |

**Setup (once per workspace, ~1 min):** fetch every file in this folder into one directory, then
`npm i` there and `pip install --break-system-packages numpy scipy pillow opencv-python-headless scikit-image`
(skip what is already installed). Node 22+, Python 3.10+. No screen, no GPU, no network beyond npm and pip.

**character.js contract** (export.mjs relies on it): `import * as THREE from 'three'`; `createCharacter()` returns
`{ root, bones, clips, pose(name, t), play(name), update(dt) }`; `clips` maps move name → seconds
(`{ idle, walk, jump }`); bones are `THREE.Bone`, the first one named `hips`, each with `userData.rest` = its rest
position and no rest rotation (the exporter zeroes bone rotations for the rest pose; angle meshes, not bones);
every mesh sits under `hips` (anything outside it is skipped); `pose(name, t)` resets every bone to rest and then
sets the move at time `t`.

**Tested** 2026-10-25 on run E's Super Sweets under Three.js 0.160.0: export 0 validator errors, heat map 84.5%
(same as the 0.186.1 original), still rendered, viewer and both game routes (code shape and .glb slot) run in
headless Chromium with no page errors (the kit's slot, rig and stage code copied unchanged; not a full launched game). Note: 0.160.0 builds capsules with more triangles than 0.186.1, so the
same code came out 71k triangles / 2.22 MB against run E's 62k / 1.97 MB; with the body sphere at 96×64 and capsules at
6 cap segments it is 55,776 triangles / 1.78 MB at 84.4%. Watch the size from round 1.

Source of the heat map: Chooch333/kids-games `lab/claude-image-to-3d/heatmap-runs/tools/` (identical).
`checks.py` (attached / smooth) stays in the lab as a measuring stick only; it is not a build step.
