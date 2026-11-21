---
title: "Game Dev Workflow Backbone - Godot, World Labs Marble, Spark, Hunyuan3D"
type: discovery-brief
discovered: 2026-11-20
tools: [godot, world-labs-marble, spark, hunyuan3d]
brief_url: ""
draft: false
---

# Game Dev Workflow Backbone - Godot, World Labs Marble, Spark, Hunyuan3D

Discovery Brief · 2026-11-20 · approved by Charles the same day

Started as a discovery of Godot; widened, at Charles's direction, into the backbone of a game dev workflow for the family arcade, with the tech that could plug into each step. Charles will speed-run the workflow and come back to the lab for tech on single steps.

Evidence marks: **Published** = checked at the source today. **Assumed** = our judgment.

## What it is

A game the boys would call good is built from three kinds of ingredients. Claude's past character work tried to code the hardest one by hand, and that is why it failed. *Assumed.*

1. **Art made elsewhere.** Characters and props are 3D models made by an artist or an AI tool, then loaded in. *Published.*
2. **Code for nature and effects.** Terrain, grass, water, sky, fire and glow are patterns plus randomness, which code does well. A specific kid's ninja isn't a pattern, so code does it badly. *Published* (showcase scenes) / *Assumed* (why).
3. **Lighting and finishing.** Light from a photographed sky (an HDRI), shadows, colour grading and glow do most of what reads as "realistic." *Published.*

The four tools in this brief:
- **Godot**: a free, open-source game engine (physics, character animation, a level editor); version 4.7.2. *Published.*
- **World Labs Marble**: an AI tool that turns text or a picture into a 3D world you can walk around in. *Published.*
- **Spark**: World Labs' free, open-source add-on that shows Marble worlds inside Three.js in a browser. It needs Three.js r180 or later, so the arcade's old 0.160 can't run it and the current 0.187 can. *Published.*
- **Hunyuan3D 2.1**: Tencent's free, open-source picture-to-3D model maker; runs on a home graphics card. *Published.*

Terms: a **Gaussian splat** world is like a 3D photograph made of millions of soft dots. It looks real from any angle, but it isn't made of solid objects, so Marble also exports a plain "collider" shape for walking on. *Published.*

## Verdict by tool

| Tool | Verdict | Come back when |
|---|---|---|
| Godot | Shelf | test run (the full-scene test below decides whether the browser kit is good enough or an engine is needed) |
| World Labs Marble | Shelf | test run (world look judged on the free plan before any paid export) |
| Spark | Shelf | test run |
| Hunyuan3D 2.1 | Shelf | test run (side by side with Meshy on the same drawing) |

None is Never: all four are current, maintained, and fill a step nothing we own does well. None is more than Shelf, because nothing is adopted without a test you have seen. *Assumed.*

## Where it fits: the game dev workflow backbone

Each step lists what plugs in today and what could. **Bold** = in use or decided.

| # | Step | What it makes | Plugs in today | Could plug in |
|---|---|---|---|---|
| 1 | Idea | The game in words: goal, controls, characters, world | **Game Maker skill: the boys describe it, Claude writes the plan** | — |
| 2 | Characters (the heroes) | A 3D figure from a kid's drawing, with a skeleton and moves | **Meshy: picture to 3D, then your picked moves (Walking 2, Run 3, Regular Jump)** | Hunyuan3D (free, home PC; shape and paint only, moves still from Meshy or Blender). Retiring: Claude-coded characters |
| 3 | Props and set pieces | Rocks, crates, trees, buildings, pickups | — | Free model libraries (Poly Haven, Kenney, free Sketchfab models); Meshy or Hunyuan3D for one-offs from a picture or a sentence |
| 4 | Materials and sky | Surface looks (wood, stone, grass) and the sky that lights the scene | — | Poly Haven textures and HDRI skies (free) |
| 5 | The world (level) | The ground and backdrop the game happens in | Code-built simple scenes | Three ways, mixable: (a) code-built nature (terrain, grass, water, sky); (b) an AI world from Marble, shown through Spark; (c) a world assembled from library props |
| 6 | Lighting and finishing | What makes it look real or stylish | Basic game lights | Sky lighting, soft shadows, colour grading, glow, film grain |
| 7 | Effects | Fire, force fields, sparks | — | **Second game kit (planned): graphics-card effects on the newest Three.js** |
| 8 | Gameplay and animation | Controls, camera, moves blending into each other, physics, saves | **Arcade starter kit on Three.js** | The kit on the newest Three.js; or Godot as the engine |
| 9 | Play and tune | Kids play, ask for changes, rounds of fixes | **Played in the chat, then feedback rounds** | The arcade's test site, if a step can't run in chat |
| 10 | Launch | Game in its cabinet, in a boy's arcade, robot-checked | **Launch step, cabinet builder, live check** | — |

**The engine choice spans steps 5–8.** Browser Three.js 0.187 keeps phones, logins, saves and in-chat play, and can show Marble worlds. Godot gives built-in animation blending and physics. In the browser it is held to basic graphics; at full graphics it runs only as an installed program on the home PC. *Published* / *Assumed*.

**What the speed run should prove first:** steps 2 + 5 + 6 together. A good character in a good world under good light is the "not garbage" bar. *Assumed.*

## What we could use it for

**Now:**
- Marble's free plan: generate worlds from the boys' ideas and judge the look in Marble's own viewer, at $0. *Published* (free plan generates) / *Assumed* (fit).
- Poly Haven skies and textures in every game. *Assumed.*

**Later (after the test):**
- Marble worlds inside arcade games through Spark. *Assumed.*
- Hunyuan3D for props and characters with no credits spent. *Assumed.*
- Godot if the test shows the browser kit can't reach the bar. *Assumed.*

**Cannot:**
- Spark on the arcade's current kit (old Three.js). *Published.*
- Marble exports on the free plan. *Published.*
- Godot's full graphics in a browser. *Published.*
- Hunyuan3D moves: it makes the figure, not the skeleton or animation. *Assumed.*

## What we checked

| Fact | Finding | Mark |
|---|---|---|
| Godot | 4.7.2 stable; MIT, $0, no royalties; headless command-line export; humanoid move sharing; a bridge to the web page; web export uses only the basic renderer, about 40 MB raw | Published |
| Marble | World Labs (Fei-Fei Li). Text, picture or video in; splat worlds plus collider and visual shapes out; exports also go to Unity, Unreal, Blender. Version 1.1 released April 2026 | Published |
| Marble price | Free plan generates but can't export. Commercial rights and high-quality mesh export need Pro, listed at about $35 a month (a third-party price list, Sept 2026; the official pricing page wasn't read). API mesh export $2.80 a world | Published / third-party |
| Spark | MIT, free; by World Labs; works with Three.js r180 or later; runs on almost every device including phones; 2.0 streams large worlds | Published |
| Hunyuan3D 2.1 | Tencent; code and model weights released; picture to 3D shape plus realistic surface materials; runs on consumer graphics cards. Licence is Tencent's own, not read today: read it before any company use | Published / not checked |
| Three.js | Newest 0.187.0 (Oct 30, 2026); arcade kit on 0.160.0 (Dec 22, 2023) | Published (npm) |
| "Coded" showcases | A jungle-ruins walk with every texture, mesh and sound made in code; a forest scene whose look comes from colour grading, glow, film grain and faked light shafts | Published |

## What else does this job

- **Unreal Engine**: the best graphics and animation, but no web play and heavy for Claude to drive. *Assumed.*
- **Tencent HunyuanWorld 1.0**: a free, open-source world generator, Marble's free rival. Not reviewed. *Published* that it exists.
- **Tripo**: picture-to-3D with automatic skeletons; reviewed on Oct 10 beside Meshy. *Published* (lab record).
- **Claude-coded characters and math-built shapes**: tested; good for round, toy-like shapes only. The coded character workflow is being retired. *Published* (lab record).

## Requirements check

**family arcade** (one-shot game, kids play and give feedback, Launch, saves on every device, 3D characters, phone-playable):
- Marble + Spark: **yes in concept**, because Spark runs in the browser on phones beside normal Three.js objects; needs the newest Three.js. *Published* / *Assumed*.
- Hunyuan3D: **yes for steps 2–3**, because it outputs standard 3D files; moves come from elsewhere. *Assumed.*
- Godot: **yes except in-chat play**, as in the earlier draft of this brief. *Assumed.*
- All four: **the "not garbage" bar is unproven**; only the test settles it. *Assumed.*

**arch-renders:** Marble could make site context and backdrops for building renders. That isn't this brief's job; it's worth its own look. *Assumed.*

## Risks and cover

- **Splat worlds look real but aren't solid objects** (walk-through walls, odd edges far from the source picture). Cover: Marble's collider shape; keep the action close to the detailed area. *Published* / *Assumed*.
- **Money:** Marble exports are paid. Cover: judge on the free plan first; any plan is your call. *Published.*
- **Download size:** splat worlds are millions of dots. Cover: Spark's lower-detail streaming and the smaller export. *Published* / *Assumed*.
- **Mixing art styles** (photo-real world, cartoon hero). Cover: the lighting and finishing step sets one look across both. *Assumed.*

## If adopted

- **What gets built:** the second game kit on the newest Three.js with Spark, a lighting and finishing preset, a props and skies library, and a Game Maker skill that walks the 10 steps.
- **Dollars:** $0 for the four tools themselves; Marble Pro about $35 a month only if worlds are used in games (your call).
- **Your hours:** the speed run, then reacting at its stops.
- **Proof of done:** a game where the boys' Meshy character runs through a world they described, lit well, launched to their arcade, and they say it looks like a real game.

All *Assumed.*

## Test run, if we do one

- **Test problem:** one full game scene that meets the "not garbage" bar.
- **Input:** the Meshy ninja (walk, run, jump); one world idea from the boys; Poly Haven sky and textures.
- **Variants:** (A) a Marble world shown through Spark on Three.js 0.187; (B) a code-built terrain and sky on Three.js 0.187; (C) a Godot version on the home PC. Same lighting and finishing, and the force field fire effect, in each.
- **Questions only a test can settle:** Does any variant look like the scenes Charles has seen? Do the ninja's moves sit right in a splat world? What frame rate on the home desktop, and on a phone? How big is the download? Which do the boys pick?
- **Run place:** the home desktop's Chrome (connected through the browser extension) for A and B; your PC, only with a folder already connected in that chat, for C.

## Sources

- https://godotengine.org/ · https://godotengine.org/license/ · https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html · https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/retargeting_3d_skeletons.html · https://docs.godotengine.org/en/4.7/tutorials/platform/web/javascript_bridge.html
- https://invideo.io/blog/world-labs-marble-3d-worlds/ · https://docs.worldlabs.ai/marble/export/gaussian-splat/index.md · https://docs.worldlabs.ai/api/pricing.md · https://www.aixploria.com/en/?p=33903 (plan prices, third-party)
- https://github.com/sparkjsdev/spark · https://radiancefields.com/platforms/spark
- https://www.producthunt.com/products/hunyuan3d-2.1/launches · https://github.com/Tencent/Hunyuan3D-2
- https://gitee.com/theyn/jungle-trail · https://discourse.threejs.org/t/forest-environment-built-with-three-js-and-webgpu/96126 · https://threejs-journey.com/lessons/haunted-house
- npm registry for three (read 2026-11-20); Project State total-harness and agent-library lab records (read 2026-11-20)
