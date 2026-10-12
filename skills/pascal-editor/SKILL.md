---
name: pascal-editor
version: 0.1.0
status: draft
triggers: [used by arch-renders-run and builds that need a Pascal scene loaded or exported; no chat trigger]
dependencies: []
owner: Charles
updated: 2026-10-12
wiring:
  runs: inside-builds
  reads: [scene.vN.json, Charles's PC (browser pane, Downloads)]
  writes: [model.vN.glb, materials.pascal_signature (calibration)]
  stack: [total-harness]
  origin: yours
  label: Pascal editor
---

# Pascal editor

Pascal (npm `@pascal-app/*`, MIT) is the 3D building editor the arch-renders route writes scenes for. It turns a scene file into a GLB with named parts. Proven 2026-10-11: a 129-node two-storey scene exported to a correct 5.8 MB GLB with 1,919 parts.

## Where it runs: Charles's PC only
- **The cloud export is broken.** Pascal run headless in a cloud session exports a GLB that drops about half the second-floor walls and misplaces the roof (1,897 vs 1,919 parts). It needs a real graphics card. Do not use a cloud export, and do not spend time investigating it (Charles, 2026-10-11).
- Scene writing, validation, signatures and rendering happen in the cloud; only load + export happen on the PC.

## Install and start at login
- `start-pascal.cmd` in `C:\Users\cecou\code` starts Pascal **1.0.3 pinned by exact npm version** on fixed port **3434**, with no browser window: e.g. `npx -y @pascal-app/cli@1.0.3 start --port 3434` (confirm the CLI's flag names on first run; Build 35.1).
- Charles copies it into his Startup folder (Win+R, `shell:startup`) once, so Pascal starts when the PC does.
- Check: `http://localhost:3434` loads in the browser pane and Settings shows 1.0.3.

## Load a scene (browser pane)
1. Open `http://localhost:3434`, then Settings.
2. Fill the hidden JSON file input from script: `pipeline/pascal/load_scene.js` → `pascalLoadScene(<scene text>)` (a `File` set through a `DataTransfer`, then `change`).
3. "Ready to import" shows counts: they must equal the scene's walls, windows and doors.
4. Click **Replace current scene**. The camera opens jammed against the model; it does not matter for export.

## Export
1. Click **Export GLB**.
2. The browser-pane download may sit in Downloads as `*.tmp` behind a hidden save prompt. **It is complete when the GLB header's length equals the file size** (`node sign_glb.mjs check <file>`); stage it as is with `device_stage_files`. Not complete: wait 5 s and look again, up to a minute.
3. Check counts against the scene: `node sign_glb.mjs counts <glb> <scene.json>`.

## Version gotchas
- **Validate every scene on the exact core version** (`@pascal-app/core@1.0.3`, `validate.mjs`): keys from another version are dropped silently on load, so "it loaded" proves nothing.
- Export materials are **unnamed**, textures are 512 px, and the **frame colour is lost** (scene says #1c1c1c, export gives cream). Never key materials by name or image order.
- A new Pascal version on the PC means new signatures: run calibration before rendering.

## Calibration (once per Pascal version)
1. `node calibrate.mjs scene materials.json <dir>` → one wall per library material plus one window carrying the frame colour.
2. Validate, load and export it as above.
3. `node calibrate.mjs read <export.glb> <dir>/calibrate-map.json --version <x.y.z>` must say `ok`: every material exactly one signature, no two the same. Run its `sql` to write `materials.pascal_signature`.

## Stop rule
Three failed tries at one step (reach Pascal, load, export, counts): stop and write down what was tried. If the PC or Pascal can't be reached, the run waits ("waiting for your PC"); never guess and never fall back to a cloud export.

## Changelog
- 0.1.0 (2026-10-12) — First version, from the 2026-10-11 Crider lab run and Build 35's night build. The PC steps are written but not yet re-run by script (Build 35.1).
