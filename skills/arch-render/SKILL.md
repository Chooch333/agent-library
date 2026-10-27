---
name: arch-render
version: 0.2.2
status: draft
triggers: [used by builds when an arch-renders run reaches gate 3 (materials stills) or gate 4 (output stills and clip frames); no chat trigger]
dependencies: [arch-massing, arch-materials, pascal-editor]
owner: Charles
updated: 2026-10-27
requires: [references/thread-checkin.md]
wiring:
  runs: inside-builds
  reads: [gate-2 model.glb (typed parts), material assignment, site settings, cbrain workflows.conventions (cameras, look), asset kit]
  writes: [arch-renders outputs/, cbrain workflow_assets, cbrain workflow_gate_results]
  stack: [total-harness]
  origin: yours
  label: Render
---

# Render

Turns the passed white-box model plus its material assignment into photo-like exterior stills: real textures, real sky, aimed sun, site, trees, grass, haze. Proven in the render lab of 2026-10-10 (Total Harness chat); Charles judged the result "great" and settled the rendering route.

Reference implementation: `Chooch333/arch-renders/lab/cycles-house/house.py` (one file, whole scene). Method notes: `lab/cycles-house/README.md`.

## Route (settled)
- **Stills: Blender Cycles, in the cloud workspace.** `pip install --break-system-packages bpy==5.2.2`. CPU only (no graphics card), 2 processors, 7 GB.
- Ruled out for stills: the browser scene (real-time, visibly game-like) and EEVEE (runs, but software-emulated: 55 s for one cube at 320×180).
- AI finish passes are not part of this skill (gate 4 option, money stop).

## Asset kit
Everything comes from Poly Haven (CC0). Textures at 2k JPG with four maps: `diff`, `nor_gl`, `rough`, `disp`. Sky: a `*_puresky_4k.hdr`.
- The cloud shell cannot reach Poly Haven or ambientCG (checked 2026-10-10). Fetch through **Chrome on Charles's PC** (Claude in Chrome), so Claude handles the save dialog itself. Do not use the Claude app's built-in browser for downloads: its save dialogs need Charles's click, and it allows one automatic download per site.
- Bundle many files into one download (fetch in the page, concatenate into one Blob with a JSON index, save once), then `device_stage_files` it to the cloud (86 MB staged fine) and unpack.
- Tile size per texture = Poly Haven API `info/<id>.dimensions` (mm). Use it; never guess scale.
- Trees and shrubs: EZ-Tree 1.1.0 (npm, MIT) presets exported to glTF from headless Chrome (`@sparticuz/chromium` + `puppeteer-core`, GLTFExporter; wait ~4 s for leaf textures). Keep one season: no Aspen presets (autumn yellow). `Bush 3` and some `Bush 1/2` seeds flower yellow — limit to 1 in 4.

## Materials (how a texture becomes a believable surface)
- Principled BSDF with all four maps: colour, roughness, normal (Normal Map node), and displacement as bump (distance 0.01 m).
- Map in **real-world size**: Object coordinates → Mapping scale `1/tile_m` → Image Texture with **Box projection, blend 0.15**. No UV unwrapping needed for walls.
- Roofs: real displaced geometry. Grid mesh (500×200), UVs in metres / tile size, Displace modifier from the `disp` map (strength 0.035 m), Solidify 0.18 m. Seat the ridge cap on the slabs (no gap).
- Crop texture edges that carry non-repeating features. `roof_slates_03` has a flashing strip and a ridge course in its top 140 px; cropped → no band across the roof.
- Grass photos on Poly Haven are dry/brown: desaturate (0.25) and multiply by green (0.42, 0.60, 0.22).
- Tint, don't hand-paint: painted siding = plank texture, saturation 0, value ×1.6, tint.
- Interiors behind glass must not be brick: cut the wall shell with an `interior`-material cutter (the boolean copies the cutter's material onto the inner faces). Add a dim warm area light (≈90 W) and curtains so windows read as rooms, not voids.
- Glass: Principled, transmission 1, roughness 0.02, IOR 1.5.

## Geometry detail that matters (model it; don't fake it)
Recessed windows (frame set back 0.11 m) with frames, mullions, sloped sills and lintels · lap siding as individual boards tilted 4° · fascia, rakes, gutters, downspout · stoop and steps · mulch beds with shrubs along the foundation · small bevels (4–30 mm) on trim and stone.

## Site
- **Sun: an explicit Sun lamp**, aimed from the conventions' "look" (default: front-left, azimuth ≈245° to the sun when the front faces −y, elevation ≈38°), strength 4, angle 0.8°, colour (1.0, 0.95, 0.88).
- **Sky: the HDRI**, clamped with Vector Math MINIMUM (8,8,8) so its own sun doesn't cast a second shadow. Do not aim the sun by rotating the HDRI: it was unreliable (three wrong tries).
- Check before rendering: the sun must light the facades the cameras see (dot(facade normal, sun dir) > 0.3 for the main facade).
- **Ground:** 400 m plane, lawn material plus large-scale noise variation (scale 0.06).
- **Grass blades:** one modeled clump of 36 blades (5–11 cm), instanced by geometry nodes (Distribute Points on Faces, density ≈450/m², random rotation and scale 0.7–1.4) over the ground the cameras see. Mask it with a vertex group fed to **Selection** (Density Factor only works in Poisson mode). Particle hair at visible density runs out of memory (2.6 M strands killed the 7 GB machine).
- **Tree line:** ~140 instanced trees at 60–120 m behind and beside the building, plus ~9 near trees placed to frame, never in front of the entry.
- **Haze:** mist pass (start 25 m, depth 220 m, quadratic) mixed toward (0.62, 0.70, 0.80) at 0.35 in the compositor (Blender 5: `scene.compositing_node_group`, NodeGroupOutput).

## Cameras
- From `workflows.conventions` (`aerial-34`, `street` eye level 1.6 m, `entry`).
- **Level camera, lens shift for framing** (rotation x = 90°, `shift_y = (target_z − cam_z)/dist × focal/36`): verticals stay vertical.
- Focal 26–32 mm on a 36 mm sensor. Street: ~20 m out at ~30° off the facade, not square-on and not 25 m+ away (the house reads small).

## Render settings
Cycles CPU · 64 samples stills, adaptive threshold 0.02 · OpenImageDenoise · light tree on · bounces 8 (diffuse 3, glossy 3, transmission 6, transparent 16) · AgX, look "Medium High Contrast" · PNG.

Measured (2 CPU, 1600×900, 64 spp, full site): eye level 12–14 min, aerial 14–15 min, entry 12.5 min. Scene build adds ~1 min. Low-res checks (800×450, 16–24 spp) take 45–80 s: use them for every fix round, full size only at the end.

## Checks before Charles sees a still
1. Sun lights the main facade (see Site).
2. No hard edge where the grass instances end; the grass field covers everything in frame or fades out.
3. Walks and paving stay clear of grass (mask them).
4. No band or seam repeating across any large surface.
5. Ridge cap seated; no sky showing between roof parts.
6. Rooms behind glass read as rooms (not brick, not black).
7. One season; shrubs not dominated by yellow.
8. Verticals vertical (level camera).
9. A fresh checker agent grades the stills against the drawings and this list; up to two fix rounds.

## Known open flaws (lab, 2026-10-10)
Grass instanced on a fixed rectangle (visible edge in the aerial; covered the walk) · interiors plain · leaves slightly dark up close · no asphalt shingles on Poly Haven (slate used).

## Animation
- Quality holds frame for frame: 1280×720, 16 spp + denoise ≈ **2.8 min/frame** (measured, aerial camera). Looks close to the 64 spp still.
- Cost: 24 fps × 20 s = 480 frames ≈ 22 h on the cloud workspace. Not viable as the default.
- Default clip method: short true camera moves (4–6 s) rendered as frames, plus camera drift over the approved stills (EffectCraft). Faster frames need a graphics card (Charles's PC or a rented GPU): an R&D question with a money stop.
- Untested: frame-to-frame flicker at 16 spp (per-frame denoising), cloud session lifetime over multi-hour renders.

## Stop rule
Three failed tries at the same check means stop, write down what was tried, and report. Never relax a check to pass.

## The Pascal GLB route (Build 35, from the 2026-10-11 run)
- The model now comes from **Pascal**: a scene file (`arch-renders/pipeline/pascal/generate.mjs`) exported to GLB by Pascal **on Charles's PC** (skill `pascal-editor`; the cloud export is broken). Blender 5.2.2 imports it with every wall, window and door as a named part (`wall_<id>`, `window_<id>`, `door_<id>`).
- The renderer is `pipeline/pascal/render.py`. It reads cameras, sun, site kit, output and look from `workflows.conventions` **data**, and maps materials by **signature** (`sign_glb.mjs`, calibrated per Pascal version into `materials.pascal_signature`), never by name or image order.
- **Revit models (FBX):** render with `pipeline/revit-intake/render_revit.py` (same arguments and outputs, `--blend` in place of `--glb`); `render.py` stays the Pascal/PDF renderer.
- Modes: `preview` (800×450, 16 samples), `idpass` (one flat colour per part, no anti-aliasing, plus a colour→part map so a pin on a preview names a part), `still` (1600×900, 64 samples).
- Measured 2026-10-11 (two-storey commercial building, simpler near site): check renders 50–60 s each; stills 5.9–7.8 min each.

## Fix rules (the four check-render fixes of 2026-10-11, now in render.py)
1. The facade line comes from **wall parts only**: canopies and other blocks project past the walls and opened a lawn gap at the front.
2. Drives are **always flat asphalt**: a textured drive read as stone pavers.
3. Lawn brightness comes from the library (value 0.8), so the lawn is **not lighter than the grass blades**.
4. Walk slabs **meet edge to edge, never overlap**: overlapping slabs rendered a black patch.
Also: every site item not on the sheets (walks, curb, drive, trees, lawn) is listed on the run as `assumed`.

## Gotchas
- **Never name a bpy script `inspect.py`**: it shadows the stdlib module bpy imports and crashes Blender.
- Blender adds `.001` to repeated names: strip it before matching a part or a signature.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the building's name + "renders", e.g. "Sample duplex renders"
- Opens when: a still set stops on the stop rule, or is posted for Charles's review (gate 3 or gate 4 under review)
- Checks in: when a run leaves something open (thread_key "job:arch-render-<run slug>")
- Closes when: Charles passes gate 4 on the run, or clicks Done

## Changelog
- 0.2.2 (2026-10-27) — Revit models render with `pipeline/revit-intake/render_revit.py`; `render.py` stays the Pascal/PDF renderer (Build 53).
- 0.2.1 (2026-10-23) — Progress tracking section. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 (2026-10-12) — Build 35 night run: Pascal GLB route, signature mapping, conventions as data, preview/id-pass/still modes, times, the four fix rules, the inspect.py gotcha. Draft until Build 35.1 renders by script.
- 0.1.0 — First version, from the 2026-10-10 render lab (Total Harness chat).
