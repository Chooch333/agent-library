---
name: game-maker
description: 'Use when Charles (or a kid with him) says "New game: …" in a Claude chat: one-shot a whole 3D web game on the family-arcade kit as an artifact, run the play and review gates, and on "Launch" send it to the family arcade site with a robot live check.'
version: 0.2.1
status: draft
triggers: ["New game: …", "Launch (after a game-maker game is on screen)"]
owner: Charles
source: BB-2026-10-19-family-arcade-v1 (Build 42)
requires: [references/thread-checkin.md]
wiring:
  runs: in-chat
  reads: [Chooch333/family-arcade kit/README.md, kit/template/index.html, kit/arcade-kit.js]
  writes: [Chooch333/family-arcade public/games/<slug>/, cbrain db arcade_games, runs/<slug>/]
  stack: [family-arcade]
  origin: yours
  label: Game Maker
---

# Game Maker

Turns "New game: …" into a game the boys can play on the family arcade, with saves on every device.
Charles's words: *"you would 1 shot the whole game from the first prompt, no step by step development."*

## 1. Read the kit (every time, before writing a line)
Custom GitHub MCP `get_file_contents`, owner `Chooch333`, repo `family-arcade`:
`kit/README.md` (the rulebook), `kit/template/index.html` (the shape), `kit/arcade-kit.js` (paste it unchanged).
If the repo can't be read, say so and stop — never write a game from memory of the kit.

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

## 3. Play gate (the kids play it)
After the artifact, ask the kids to play. Each feedback round: one plain line of what changed, then the updated
full artifact. Keep a one-line result per round ("Round 2: faster coins, bigger jump button").
**No robot playtest during chat development** — the robot live check runs only after Launch.

## 4. Review gate
When feedback slows, give one line: either "Ready to launch." or "One thing to fix first: …" (and fix it).
Then say exactly: **"If it looks good, tell me Launch and I'll send it to the arcade."**

## 5. Launch (only when Charles says "Launch")
Follow `Chooch333/family-arcade` `tools/launch.md` step by step: pack `public/games/<slug>/` (index.html + game.json),
commit (`[wip]` … last file `[deploy]`), upsert the `arcade_games` row (Supabase `lpeswznkxzeeyiqaewma`, `arcade_*`
tables only), wait for the Vercel deploy READY, dispatch the `live-check.yml` workflow, read `LIVE-CHECK-RESULT`.
Only after a pass, report: `Launched: <title> → <address>/play/<slug>`. If the check fails, fix and re-run.
Never touch any non-arcade cbrain table. Never use a paid tool (Meshy etc.) without Charles's say-so.

## 6. Record lessons
After Launch, one Project State note on total-harness (`add_note`, tags `game-maker`, `family-arcade`): game, rounds,
what the kids liked, what the live check caught, and any kit rule that should change (as a suggestion, not an edit).

## 7. Check in
Check in per Progress tracking.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: game-maker
- build: the game's title + "game", e.g. "Run Around the World game" (thread_key "game-maker:<game slug>")
- Opens when: the first turn, once the game is on screen
- Checks in: end of every turn
- Closes when: the game is Launched and its live check passed (`close_thread`, closed_how "launched")

## Changelog
- 0.2.1 (2026-10-23) — The Check in step becomes the Progress tracking section (build naming per thread-checkin 0.3.1; no project_label; no 5 am sweep); step 7 points to it. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 (2026-10-21) — Build 44 (BB-2026-10-20-next-steps-dev-tab): new Check in step — every turn, Project State `checkin` per `references/thread-checkin.md` (kind `game-maker`); `close_thread` when the game is Launched. Feeds the Next steps list on cbrain's Dev tab. New `requires` entry.
- 0.1.0 (2026-10-20) — First version, Build 42 (BB-2026-10-19-family-arcade-v1).
