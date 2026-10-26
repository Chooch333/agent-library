---
name: game-maker
description: 'Use when Charles (or a kid with him) says "New game: …" or "New character: <drawing>" in a Claude chat: one-shot a whole 3D web game on the family-arcade kit as an artifact, design its arcade cabinet, turn a drawing into a 3D game character (Character maker, Opus only), drop a character in as a player''s avatar or a game''s hero ("Drop in: …"), run the play and review gates, and on "Launch" send game + cabinet to the family arcade site with a robot live check.'
version: 0.5.0
status: draft
triggers: ["New game: …", "New character: <drawing>", "Drop in: <character> → <player>'s avatar | <game> hero | saved | hide", "Launch (after a game-maker game is on screen)"]
owner: Charles
source: BB-2026-10-19-family-arcade-v1 (Build 42); cabinet standard 2026-10-23; Character maker = R&D run E 2026-10-25 (TH-092..096)
requires: [references/thread-checkin.md]
wiring:
  runs: in-chat
  reads: [Chooch333/family-arcade kit/README.md, kit/template/index.html, kit/arcade-kit.js, kit/cabinet.md, kit/cabinet/cabinet3d.js, kit/cabinet/preview.html, Chooch333/agent-library skills/game-maker/maker/*]
  writes: [Chooch333/family-arcade public/games/<slug>/ (game + cabinet files), cbrain db arcade_games, runs/<slug>/, Chooch333/kids-games characters/<name>/]
  stack: [family-arcade]
  origin: yours
  label: Game Maker
---

# Game Maker

Turns "New game: …" into a game the boys can play on the family arcade, with saves on every device, standing
in the arcade in its own painted cabinet. Turns "New character: <drawing>" into a 3D character that walks and
jumps in those games (section 9, Character maker).
Charles's words: *"you would 1 shot the whole game from the first prompt, no step by step development."*

**Who does what.** This skill designs the game AND its cabinet (paint, marquee, neon name), and builds any
character a kid draws. The arcade floor (the 3D arcade room) only places cabinets and handles walking up to
them; it never designs a cabinet or a game.

## 1. Read the kit (every time, before writing a line)
Custom GitHub MCP `get_file_contents`, owner `Chooch333`, repo `family-arcade`:
`kit/README.md` (the rulebook), `kit/template/index.html` (the shape), `kit/arcade-kit.js` (paste it unchanged),
`kit/cabinet.md` (the cabinet rulebook), `kit/cabinet/cabinet3d.js` and `kit/cabinet/preview.html` (paste unchanged).
If the repo can't be read, say so and stop — never write a game or cabinet from memory of the kit.

## 2. One-shot the whole game
- One HTML artifact, complete and playable on the first answer: start screen, the game, scoring/levels, win/lose,
  restart, sounds only if cheap. No "first version", no step-by-step builds, no questions first unless the ask is
  truly empty — pick the fun interpretation and go.
- Build it exactly like the template: inline `#game-json` (slug, title, version "1", emoji, slots, settings), the
  importmap (Three.js **0.160.0**), the kit pasted unchanged in its own module script, then the game module using
  `A.start / A.load / A.save / A.settings / A.slot / A.rig / A.input / A.stage / A.loop / A.hud`.
- Quality bar: Charles's chat games (Cubicle Clash, Gust, Eggs on Top 3D) — real 3D scenes, juicy feedback
  (bounce, particles, screen shake, color), a clear goal within 5 seconds, playable by a 6-year-old on a phone.
- Every character or prop that might later get a real 3D model is a **slot** with a code-shape fallback.
  If the kids give a drawing of a character, the Character maker (section 9) builds it and it goes into its slot.
- Every number a parent may tune (speed, lives, gravity, time) is in `settings`.
- Save progress that matters (best score, unlocked levels) with `A.save` on progress, not every frame.

## 3. Design the cabinet (same answer, right after the game)
Every game gets the **standard cabinet** (one shape for all games — never change the shape) painted for this game.
All creative license is yours; follow `kit/cabinet.md`.
- Write **`cabinet.json`**: `marquee.text` (the floating neon name, usually the title), `marquee.color`,
  `body.color`, `body.trim` (the glowing edge color — **choose it for this game**; never reuse one default).
  The control deck is standard and not designed: black panel, black buttons, red joystick.
- Write **`cabinet-paint.js`** (`export default function paint(c, h) { … }`, plain canvas 2D, inches):
  - **Wrap, don't frame.** The skin is one picture around the body (left side u 0–37 → front 37–62 → right side
    62–99). Carry one big simple shape of the game's world — a road, a wave, lightning, vines, a skyline — from
    the side round the corner onto the front. Never "a picture inside little panels". Never a plain box.
  - Paint the left half (u 0–49.5), then `h.mirrorHalf()`; then words and one-sided stickers (they'd read
    backwards if mirrored). One clear hero (the game's character/emoji) on each side.
  - Also paint the marquee (backlit sign with the title) and the screen (an attract picture).
  - Two or three main colors plus the trim neon; bold and readable from across a room.
  - **Vary the finish.** Not every cabinet flat: some flat poster color, others layered and textured
    (overlapping depth layers, shading/highlights, grain, halftone, brush or pattern texture, outlines, drop
    shadows). Pick what suits the game so the arcade doesn't look like one style.
- Show it: fill `kit/cabinet/preview.html` (cabinet.json + title/emoji into `#cabinet-json`, `cabinet3d.js` and
  `cabinet-paint.js` pasted unchanged into their marked spots) and publish it as a second artifact — a turnable
  cabinet with its neon name. Keep both files in the chat; they are what Launch ships.

## 4. Play gate (the kids play it)
After the artifacts, ask the kids to play. Each feedback round: one plain line of what changed, then the updated
full artifact (the game, the cabinet preview, or both). Keep a one-line result per round ("Round 2: faster coins,
bigger jump button, cabinet now has lava down the sides").
**No robot playtest during chat development** — the robot live check runs only after Launch.

## 5. Review gate
When feedback slows, give one line: either "Ready to launch." or "One thing to fix first: …" (and fix it).
Then say exactly: **"If it looks good, tell me Launch and I'll send it to the arcade."**

## 6. Launch (only when Charles says "Launch")
Follow `Chooch333/family-arcade` `tools/launch.md` step by step. In short:
1. Pack `public/games/<slug>/`: `game.json`, `cabinet.json`, `cabinet-paint.js`, `index.html`.
2. Commit `game.json`, `cabinet.json`, `cabinet-paint.js` with `[wip]`.
3. **Always build the cabinet — never skip this.** Custom GitHub MCP `run_workflow(owner Chooch333, repo
   family-arcade, workflow_file build-cabinet.yml, inputs { slug, deploy: "false" })`, then `list_workflow_runs` /
   `get_workflow_run` until completed and `get_job_logs(search "CABINET-RESULT")`; read
   `CABINET-RESULT` in its log (all checks true). It commits `cabinet.glb` + `cabinet-preview.png` and sets
   `"model": "cabinet.glb"`. If it fails, fix the painter (usually a canvas error) and run it again.
4. Commit `index.html` last with `[deploy]`.
5. Upsert the `arcade_games` row and place the game in the arcades (`tools/floor.md`), Supabase
   `lpeswznkxzeeyiqaewma`, `arcade_*` tables only.
6. Wait for the Vercel deploy READY, dispatch `live-check.yml`, read `LIVE-CHECK-RESULT`.
Only after a pass, report: `Launched: <title> → <address>/play/<slug>` and show `cabinet-preview.png`.
If the check fails, fix and re-run. Never touch any non-arcade cbrain table. Never use a paid tool (Meshy etc.)
without Charles's say-so.

**Repainting later** ("make the cabinet blue"): change `cabinet.json` / `cabinet-paint.js` (`[wip]`), dispatch
`build-cabinet.yml` with `deploy: "true"`, wait for READY. The game itself doesn't change.

## 7. Record lessons
After Launch, one Project State note on total-harness (`add_note`, tags `game-maker`, `family-arcade`): game, rounds,
what the kids liked, what the live check caught, and any kit rule that should change (as a suggestion, not an edit).

## 8. Check in
Check in per Progress tracking.

## 9. Character maker (drawing → 3D game character)
Runs on "New character: <drawing>", or inside a game chat when the kids hand over a drawing for a slot.
In: one drawing. Out: `character.js` (the character as editable Three.js code), `character.glb` (the same
character as a game file with skeleton and moves), `still.png`, a viewer page, `log.md`. About **30 minutes**
of Claude's time, unattended. No outside 3D service, $0.

This is the workflow of **R&D run E** (2026-10-25), which Charles made the standard: Super Sweets in 27 min at
84.5% of squares passing, parts attached and edges smooth (measured afterwards; the one flag, at an elbow, was a
false alarm), with no check pass at the end. Before the heat map, the same drawing took Opus 79 min at 58%.
Evidence and every run compared (A–F): R&D report "Likeness Heat Map"
(https://claude.ai/artifact/6yAvpFG33W1chJ1bJnyZcM); reference build Chooch333/kids-games
`lab/claude-image-to-3d/heatmap-runs/run-e/` (character.js, log.md).

### 9.1 Before starting
- **Opus only.** The Character maker runs on Claude Opus 5.5 (Charles, 2026-10-25). If this chat runs another
  model, hand the job to an Opus worker with this section as its brief, or ask Charles to switch the chat to
  Opus. Never run it on Fable.
- **Needs a code workspace** (Node 22+, Python 3.10+). If the chat has none, say so plainly and stop.
- **The drawing:** one clean front view on a plain background (the same input Meshy gets). If the character is
  drawn turned, ask for a front view (the heat map's `--yaw` option exists but has never been used on a turned
  drawing).
- **Get the 2D-3D Maker tool:** read every file in Chooch333/agent-library `skills/game-maker/maker/` (Custom
  GitHub MCP `get_file_contents`, or the public raw files), write them into one folder, run its setup line
  (`maker/README.md`). The tool measures and packages only; it holds **no shapes**. Build every part of every
  character from scratch in its `character.js`. Never rebuild or edit the tool during a character run; a fault in
  it is fixed in the repo, logged with the character that found it.
- **Write the likeness checklist** (one minute, before building): body shape; the face (mask, eyes, pupils,
  mouth, and any expression such as an angry slant); each distinctive feature by name (wrapper ends, cape…);
  pose (e.g. fists on hips); colours; proportions. The heat map scores the whole picture and under-weights small
  face details; this list is what the face is judged against at the end.
- Run `date -u` and note the start time.

### 9.2 The character file (same shape every time)
- `character.js`, an ES module: `import * as THREE from 'three'` (bare name; Three.js **0.160.0**, the arcade
  kit's version, so the same file runs in the viewer, the games and the exporter).
- Colours as named constants at the top (`COLORS`), sizes and positions next (`DIM`), so a later look change is
  a line edit. Clearly named meshes (`mask`, `eye_L`, `wrapper_R`, `fist_L`…): the heat map reports problems by
  these names.
- Parts hang off a tree of `THREE.Bone`s; the first bone is named **`hips`** (the arcade kit keeps a moving
  character in place by it) and **every mesh sits under `hips`** (the exporter skips anything outside it). Every
  bone keeps its rest position in `userData.rest` and has **no rest rotation**: the exporter zeroes bone
  rotations for the rest pose, so angle the meshes under a bone, not the bone (run E: `shaft.rotation.z`,
  `foot.rotation.y`). Moves rotate bones.
- `createCharacter()` returns `{ root, bones, clips, pose(name, t), play(name), update(dt) }`;
  `clips = { idle: s, walk: s, jump: s }` (add `run` only if the game needs it; the kit's `A.rig` knows idle,
  walk, run, jump). Moves are formulas of time inside `pose`, which first resets every bone to rest.
- Faces **+Z** (toward the camera), Y up, feet on y = 0, in its rest pose **as drawn** (the heat map compares the
  front view with the drawing as is).
- **No cartoon outlines in the character.** Outlines live in the viewer page only; an outline shell baked into
  the .glb turns the character black in Blender and in the arcade (tested 2026-10-24). `export.mjs` refuses them.

### 9.3 Build rules (from the very first part, every round)
These are the only quality guard. There is **no check pass afterwards** (Charles, 2026-10-25: checking is
redundant when the rules are in up front; run E proved it).
- **Flat shapes on a body** (mask, eyes, pupils, mouth, patches): build each from its outline. Smooth the outline
  points into a clean curve (run E: centripetal Catmull-Rom), fill the inside with triangles
  (`THREE.ShapeUtils.triangulateShape`, plus interior rings of points so it can bend), then wrap every vertex onto
  the body surface, lifted a hair. **Never** make a shape by keeping or dropping triangles of a fine sphere or
  grid: that leaves stair-stepped edges.
- **Colour bands painted on a part** (swirl, stripes, folds): blend the two colours over a narrow band
  (`smoothstep`), never a hard switch from one vertex to the next, on a mesh fine enough that the band edge
  reads as a curve.
- **Round parts** (joints, fists, balls): at least 32 segments around.
- **Joined parts:** every limb starts **inside** the part it hangs from (shoulder inside the body, wrist inside
  the fist), so nothing floats in any pose or move. Where the drawing shows parts touching (fists on hips, cape
  at the shoulders), make them touch.
- **A real 3D character from every side.** The heat map only sees the front; never flatten a part or fake depth
  to please it. Give flat-looking things depth (run E's wrapper ends: lathed, ruffled, twisted).
- **Size budget from the start:** `character.glb` must stay under 2 MB; aim for about 55,000 triangles. Read
  the size `export.mjs` prints from round 1, not at the end (run E lost about 5 minutes cutting resolution after
  the loop). On Three.js 0.160.0 run E's own code comes out 2.22 MB; with the body sphere at 96×64 and capsules
  at 6 cap segments × 32 around it is 55,776 triangles, 1.78 MB, same look, 84.4% (tested 2026-10-25). Over the
  cap → lower segment counts, never shapes.

### 9.4 Rough model first (within 15 minutes of the start)
Look at the drawing once, then block in **every** part by eye with best-guess sizes, colours and positions.
Export and run heat-map round 1 within 15 minutes (run E: 5 minutes). **Do not** measure the drawing's pixels,
trace outlines or sample colours before round 1: the heat map does that measuring for you.
```
node maker/export.mjs character.js character.glb
python3 maker/heatmap.py --drawing drawing.png --glb character.glb --out heatmap/round_1
```

### 9.5 Heat-map rounds (fix what it flags, by measuring)
1. Look at `heatmap.png` (red = failing squares; blue 8×8 cells A1…H8; numbered boxes = worst areas), read
   `report.md` (score = **fine squares passing %**; each area says what is wrong and which of your parts are
   there), and look at the top `region_N.png` close-ups (drawing left, model right).
2. Fix the **three worst areas** by **measuring that part from the drawing's pixels**: trace its outline or sample
   its colour inside the flagged area, and rebuild the part to match. Never nudge numbers by eye. To turn drawing
   pixels into world units use `report.json` → `fit`: pixel x = X·scale + tx, pixel y = −Y·scale + ty
   (`render_match.png` is your model drawn at the drawing's exact scale and place). Only measure what is flagged.
3. Export, run the next round. Keep rounds short: measure, change, export, check. **Revert** any change that
   makes the score worse.
4. **Stop** at **80%** fine squares passing, or when two rounds in a row each gain under 2 points, or after
   12 rounds. Use the heat map for focus, not perfection: it forgives a few pixels; never spend a round chasing
   single squares inside a busy pattern (run E left the swirl's phase and the cape's inner fold).
5. Log each round: round, minutes since start, score, what changed.

What run E measured, round by round (64.3 → 76.5 → 77.7 → 84.5%): round 2 traced the wrapper outlines (top and
bottom edge per column, ruffled rim), the cape's top and bottom edges and the boot extents, and sampled the
wrapper and cape reds; round 3 traced the mask outline, eye whites, pupil centres and sizes, and the smile's
centre line; round 4 measured the swirl's band count, twist and light share on 5 rings and sampled the candy
colours.

### 9.6 Face check (by eye, once)
Compare the face in `region_N.png` close-ups and a fresh still against the checklist's face lines. The score can
pass with a face that reads wrong (run D lost the mask's angry slant at 85%). A face line that fails gets one more
round, measured from the drawing like any other.

### 9.7 Finish and hand off
1. `node maker/validate.mjs character.glb validation.json`: **zero errors** (warnings such as unused objects or
   skinned meshes under the root group are harmless). Three clips present (`idle`, `walk`, `jump`), file under 2 MB.
2. Look at one frame of `walk` and one of `jump` (`python3 maker/heatmap.py --drawing drawing.png --glb
   character.glb --out heatmap/walk --clip walk --time 0.25`, then `--clip jump --time 0.55`; read
   `render_match.png`): no part comes away from the body.
3. `python3 maker/still.py character.glb still.png`: front three-quarter still, read from the .glb (it shows
   what a game will load; a black or broken still means the .glb is wrong).
4. Viewer: `maker/viewer.html` with `CHARACTER_NAME` filled, beside `character.js`. Publish it as an artifact
   (with `character.js` as a second file; if the artifact can't carry files, paste `character.js`'s code into
   the viewer's module in place of its `import { createCharacter }` line). Show `still.png` with it.
5. `log.md`: model name as the environment reports it, start and end times (`date -u`), minutes to first model
   and to full deliverable, the round table, triangles, file size, validator result, anything that could not be
   done.
6. Save the source: Chooch333/kids-games `characters/<name>/` → `character.js`, `viewer.html`, `log.md` (text
   files; the .glb is rebuilt from `character.js` in seconds by `export.mjs`, which is the point of code as the
   source). Send `character.glb` and `still.png` to Charles as files.
7. Report in two lines: the still, the viewer, minutes, score. Then Charles and the kids judge it (likeness is
   their call, not the score's). Changes they ask for are line edits to `COLORS` / `DIM` /
   the parts, re-exported in seconds (3 to 5 changed lines in the lab's edit test).

### 9.8 Into a game
- **Default: the code itself is the slot's code shape.** Paste `character.js` into the game file as its own
  `<script type="module">` placed before the game module (keep its `import * as THREE from 'three'`; the
  importmap gives it the kit's Three.js — the same module the kit uses, so this is not a second copy of Three.js
  and the kit rule "do not import three again" is about the game module, not this one) and end it with
  `(window.ArcadeCharacters ||= {})['<name>'] = createCharacter;`. In the game:
  ```js
  let ch = null;
  const hero = await A.slot('hero', () => { ch = window.ArcadeCharacters['<name>']();
    const g = new THREE.Group(); g.add(ch.root); g.scale.setScalar(HEIGHT / CHARACTER_HEIGHT); return g; },
    { height: HEIGHT });
  const anim = A.rig(hero);                       // drives a .glb if the slot ever names one
  const play = (n, f, once) => (ch ? ch.play(n) : anim.play(n, f, once));
  // in A.loop: ch ? ch.update(dt) : anim.update(dt);
  ```
  The kit scales a loaded .glb to `height` but not a code shape, hence the `scale` line. `ch.play` loops every
  move, so the game switches back from `jump` when the character lands (as the template does). Works in the chat
  artifact and on the site with no file upload. Tested 2026-10-25 in headless Chromium with the kit's `slot`,
  `rig` and `stage` code copied unchanged (the site, save and input parts left out): no page errors, character
  walking. Not yet tried in a launched game.
- **The .glb route** (`"slots": { "hero": "assets/character.glb" }` or `"char:<name>"`) also tested: the kit
  loads it, finds idle/walk/jump, and walks it. Use it for the arcade's character bucket
  (`tools/launch.md`, "Upgrading a model later") and for other engines (Roblox, Unreal). Open item: that upload
  needs an https link to the file, and the GitHub connector only writes text files; there is no tested way yet
  to host a Claude-made .glb for it.

### 9.9 What not to do (each was tried on Super Sweets)
- Measure the whole drawing before the first model (run A: 101 min).
- Fix flagged areas by eye instead of measuring (run B: stalled near 65%).
- Run the loop without the build rules (run C: 86.7% but jagged eyes, mouth and mask, arms not touching).
- Add a check pass at the end (run D: 11 extra minutes, mostly on a false alarm at a clean elbow).
- Fable, with or without the loop: not used (Charles, 2026-10-25: "only an opus run").
- A shared library of shape helpers (TH-093's parts library): not used. It was only ever tested with Fable;
  run E, the standard Charles chose, built every shape from scratch.
- Outlines inside the .glb; paid 3D services without Charles's say-so (Meshy stays a separate route beside this).

### 9.10 Not proven yet
One drawing so far. The consistency test is a second, different drawing by one of the boys: under 40 minutes,
at least 80%, nothing floating and no stair-stepped edges (judged by eye on the still and the move frames; the
lab's `checks.py` may be run afterwards as a measuring stick, never as a build step), and Charles judges the face
right. If Opus misses on it, fix this section first, not the model. After every character, one Project State note
on total-harness (`add_note`, tags `game-maker`, `character-maker`): drawing, minutes, score per round, what Charles
and the kids said, and any rule that should change.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: game-maker
- build: the game's title + "game", e.g. "Run Around the World game" (thread_key "game-maker:<game slug>");
  a standalone character: its name + "character", e.g. "Super Sweets character" (thread_key
  "game-maker:super-sweets-character")
- Opens when: the first turn, once the game (or the character's viewer) is on screen
- Checks in: end of every turn
- Closes when: the game is Launched and its live check passed (`close_thread`, closed_how "launched"); a
  standalone character when Charles accepts it (closed_how "character accepted")

## Changelog
- 0.4.0 (2026-10-25) — Character maker (section 9), Charles: "Run E is the standard", Opus only. Drawing → character.js + .glb in about 30 min: rough model by eye within 15 min, heat-map rounds that fix the three worst areas by measuring the drawing, stop at 80%; build rules from the start (shapes from smoothed outlines, blended colour bands, 32+ segments, limbs start inside their parent, real 3D); no check pass; face checked by eye against a likeness checklist. Carries the earlier R&D decisions (TH-092..094): character file shape, no outlines in the .glb, validator zero errors, under 2 MB, three clips, log. New tool folder `maker/` (the 2D-3D Maker tool: heat map, exporter, validator, still, viewer; no shapes). Three.js 0.160.0 for characters too (tested: run E's code builds, exports, scores the same and plays in the kit). The tool lives beside this skill in agent-library, not in family-arcade as TH-094 suggested, so the skill and its code change together. Reference build: kids-games heatmap-runs/run-e/. New trigger "New character: <drawing>". Replaces TH-093's fast/detail modes and shared parts library.
- 0.3.1 (2026-10-23) — Charles: trim (edge glow) color chosen per game; vary flat vs layered/textured finishes; control deck is standard (black panel, black buttons, red joystick) and no longer painted; Launch must always run `build-cabinet.yml`.
- 0.3.0 (2026-10-23) — Every game designs its own arcade cabinet: new step 3 (cabinet.json + cabinet-paint.js on the standard cabinet `kit/cabinet/cabinet3d.js`, wrap-around paint, preview artifact); Launch builds `cabinet.glb` with `build-cabinet.yml` before the `[deploy]` commit; repaint path. The arcade floor only places cabinets. Charles, 2026-10-23.
- 0.2.1 (2026-10-23) — The Check in step becomes the Progress tracking section (build naming per thread-checkin 0.3.1; no project_label; no 5 am sweep); step 7 points to it. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 (2026-10-21) — Build 44 (BB-2026-10-20-next-steps-dev-tab): new Check in step — every turn, Project State `checkin` per `references/thread-checkin.md` (kind `game-maker`); `close_thread` when the game is Launched. Feeds the Next steps list on cbrain's Dev tab. New `requires` entry.
- 0.1.0 (2026-10-20) — First version, Build 42 (BB-2026-10-19-family-arcade-v1).
