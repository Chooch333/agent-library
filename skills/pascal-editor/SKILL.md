---
name: pascal-editor
version: 0.1.1
status: draft
triggers: [used by arch-renders-run and builds that need a Pascal scene loaded or exported; no chat trigger]
dependencies: []
owner: Charles
updated: 2026-10-23
requires: [references/thread-checkin.md]
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

## The pane must be showing (Build 35.1, proven 2026-10-28)
Pascal draws with WebGPU. With the browser pane hidden, the page gets ~1–2 frames a second and GPU work stalls: a hidden Crider export came out with 810 of 1,919 parts (walls missing) and the next one never finished; with the pane showing the same export took ~1 s and matched the lab exactly. Before loading: `tabs_context` must say the pane is **displayed**, and a 2 s `requestAnimationFrame` count in the page must be above 60. Otherwise wait ("show the browser pane on your PC: open this chat in the Claude app, Ctrl+Shift+B"). Never export hidden, and don't patch `requestAnimationFrame` (it doesn't unstick the GPU). A tool session can't show the pane itself; only Charles can, in the chat that owns it.

Large scenes: send the scene text gzip+base64 and inflate in the page with `DecompressionStream('gzip')`, checking its sha256 before loading (100 KB → 10 KB).

## Load a scene (browser pane)
1. Open `http://localhost:3434`, then Settings (`button[aria-label="Settings"]`). Version: the PC's `C:\Users\cecou\code\pascal-start.log` says "Editor runtime 1.0.3 ready" (Settings shows no version).
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

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the building's name + "Pascal export", e.g. "Sample duplex Pascal export"
- Opens when: the run waits for the PC ("waiting for your PC") or stops on the stop rule
- Checks in: when a run leaves something open (thread_key "job:pascal-editor-<run slug>"; next_step says what Charles must do on the PC, in words)
- Closes when: the export's counts check passes on a later run, or Charles clicks Done

## Changelog
- 0.2.0 (2026-10-28) — Run on the PC for real (Build 35.1): pane-must-show rule (WebGPU stalls when hidden), version from pascal-start.log, compressed scene transfer, save-prompt `.tmp` handling (see arch-renders pipeline/pascal/export.md). Calibration now also covers the door and Pascal's own slab, roof and site parts by part ownership (arch-renders 031d175, 26b22aa).
- 0.1.1 (2026-10-23) — Progress tracking section. Per BB-2026-10-21-next-steps-panel.
- 0.1.0 (2026-10-12) — First version, from the 2026-10-11 Crider lab run and Build 35's night build. The PC steps are written but not yet re-run by script (Build 35.1).
