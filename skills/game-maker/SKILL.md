---
name: game-maker
description: 'Use when Charles (or a kid with him) says "New game: …" in a Claude chat: one-shot a whole 3D web game on the family-arcade kit as an artifact, design its arcade cabinet, run the play and review gates, and on "Launch" send game + cabinet to the family arcade site with a robot live check.'
version: 0.3.0
status: draft
triggers: ["New game: …", "Launch (after a game-maker game is on screen)"]
owner: Charles
source: BB-2026-10-19-family-arcade-v1 (Build 42); cabinet standard 2026-10-23
requires: [references/thread-checkin.md]
wiring:
  runs: in-chat
  reads: [Chooch333/family-arcade kit/README.md, kit/template/index.html, kit/arcade-kit.js, kit/cabinet.md, kit/cabinet/cabinet3d.js, kit/cabinet/preview.html]
  writes: [Chooch333/family-arcade public/games/<slug>/ (game + cabinet files), cbrain db arcade_games, runs/<slug>/]
  stack: [family-arcade]
  origin: yours
  label: Game Maker
---

# Game Maker

Turns "New game: …" into a game the boys can play on the family arcade, with saves on every device, standing
in the arcade in its own painted cabinet.
Charles's words: *"you would 1 shot the whole game from the first prompt, no step by step development."*

**Who does what.** This skill designs the game AND its cabinet (paint, marquee, neon name). The arcade floor
(the 3D arcade room) only places cabinets and handles walking up to them; it never designs a cabinet or a game.

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
3. Build the cabinet: dispatch workflow `build-cabinet.yml` `{ slug, deploy: "false" }`, wait for it, read
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

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: game-maker
- build: the game's title + "game", e.g. "Run Around the World game" (thread_key "game-maker:<game slug>")
- Opens when: the first turn, once the game is on screen
- Checks in: end of every turn
- Closes when: the game is Launched and its live check passed (`close_thread`, closed_how "launched")

## Changelog
- 0.3.0 (2026-10-23) — Every game designs its own arcade cabinet: new step 3 (cabinet.json + cabinet-paint.js on the standard cabinet `kit/cabinet/cabinet3d.js`, wrap-around paint, preview artifact); Launch builds `cabinet.glb` with `build-cabinet.yml` before the `[deploy]` commit; repaint path. The arcade floor only places cabinets. Charles, 2026-10-23.
- 0.2.1 (2026-10-23) — The Check in step becomes the Progress tracking section (build naming per thread-checkin 0.3.1; no project_label; no 5 am sweep); step 7 points to it. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 (2026-10-21) — Build 44 (BB-2026-10-20-next-steps-dev-tab): new Check in step — every turn, Project State `checkin` per `references/thread-checkin.md` (kind `game-maker`); `close_thread` when the game is Launched. Feeds the Next steps list on cbrain's Dev tab. New `requires` entry.
- 0.1.0 (2026-10-20) — First version, Build 42 (BB-2026-10-19-family-arcade-v1).
