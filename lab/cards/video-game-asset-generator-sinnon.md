---
title: "Video Game Asset Generator - Sinnon"
reviewed: 2026-10-12
tools: [claude-blender-assets, sinnon-asset-generator]
draft: false
---

## What it is

SINNON's Asset Generator: a free Windows app from SINNON Oy (Turku, Finland) that makes game assets from a sentence. Claude, run with no screen, writes Python that drives Blender (free 3D software) in the background. ✓ Outputs: .glb game files and .blend files with skeletons, animations, collision shapes (invisible shapes a game uses to detect bumps) and morph sliders, plus 3D sprites, pixel art, particle effects and ground textures, grouped in style "packs". ✓ Found through a repost on X (@jurlycat, Oct 10 2026) of a game developer's video; the video frame names the app. ✓

This review asks whether we copy that method as the base for the family's own video game asset generator.

## Verdict by tool

| Tool | Verdict | Why | The one fact that would change it |
| --- | --- | --- | --- |
| Our copy: Claude + Blender asset generator | Shelf | Passed hands-on tests. Kids' games is not a listed speed run; the arch-renders use (equipment props) waits for TH-056. | Kids' games speed run is listed, or TH-056 starts |
| SINNON Asset Generator | Never (as a harness tool) | A Windows desktop app Claude can't run unattended; closed source. Kept as the quality yardstick. ✓ | SINNON documents its local service or ships a command-line version |

## Where it fits

Digital hands layer; pipeline step 6 (make it on screen). Block 7 (Geometry stack, which lists game art), a skill under block 16, a quality rubric under block 17. ✓ It replaces nothing: it is the factory that Blender scripts, Meshy (picture to 3D) and free art packs feed into.

## What we could use it for

- **Now:** props, vehicles and buildings for the boys' games, in matched style packs; pixel sprites for 2D games. ✓✓
- **Later:** characters from the boys' drawings via Meshy, then Blender cleanup; construction equipment with moving parts for the arch-renders "construction activity over time" motion piece; 3D-printed toys. ~
- **Cannot:** detailed or organic characters from code alone (they come out toy-like). ✓✓

## What we checked

- The X post, replies and video frame, read in the browser pane on Charles's PC. ✓
- SINNON home page, product and plan page, terms (dated June 10 2026): app free on PC, cloud plan from €14.99 a month, users 16+ (younger only on a Family plan), you own what you make; no code repository linked. ✓
- Meshy Image-to-3D API docs: picture in (PNG, JPG, WEBP, 20 MB), .glb out, T-pose option, rigging and animation endpoints listed; API keys need a paid plan. ✓
- Hands-on in the cloud workspace (2 CPUs, no graphics card):
  - Character: 7-bone skeleton, Walk and Jump, collision box, 100 KB .glb in under 1 s; walked and jumped in a browser 3D scene. ✓✓
  - "Pirate Cove" pack: crate and treasure chest from one style file, baked wood and metal textures, hidden collision boxes, "lid open" slider plus open-close animation, hero stills, 48-pixel sprites; 55 s total. Three script bugs found and fixed in three runs. ✓✓
  - Khronos glTF validator: crate and chest 0 errors and 0 warnings; character 0 errors and 1 minor warning. ✓✓
- Saved files: scripts in private repo `Chooch333/kids-games` (`generator/make_hero.py`, `generator/make_pack.py`). Its `build-assets` job regenerates the .glb files, stills and sprites into `out/`. ✓ Its `meshy` job (picture in, model out, key held as the `MESHY_API_KEY` repo secret) is built. ✓ Both jobs could not run at filing: GitHub Actions failed in 2 s with no steps account-wide, still after Charles raised the minutes limit at about 21:15Z. ✓ runs · ~ cause
- Not tested: SINNON's app itself; a kid's drawing through Meshy; import into Roblox or Unreal; the collision box used by game physics.

## What else does this job

| Option | Strong at | Claude can run it unattended | Cost |
| --- | --- | --- | --- |
| Our copy (Claude + Blender in the cloud) | Props, vehicles, buildings, moving parts, matched packs | Yes ✓✓ | $0 beyond Claude |
| SINNON Asset Generator | Same, more polished, with a UI | No (Windows app) ✓ | Free on PC ✓ |
| Meshy (picture to 3D) | Characters from a drawing, auto-skeleton | Yes, through the GitHub job ✓ built · ~ untested | Paid plan plus API credits ✓ |
| Formula shapes (shelved Oct 10) | Round, toy-like characters with free skeletons | Yes ✓✓ | AI time |
| Blender Kiln (open Claude skill) | Adds AI model makers and free art libraries | Untested ~ | Not stated |
| Free CC0 art packs | Instant, good-looking basics | Yes | $0 ✓ |

## Requirements check

Arch renders, the one listed speed run:

| Requirement | Answer |
| --- | --- |
| 1. Conventions | Not this tool's job |
| 2. Still-shot storyboard | Not this tool's job |
| 3. Menu of motion pieces | Yes, for construction activity over time: equipment with moving parts and animations, by the same method as the chest lid ✓✓ lid · ~ equipment |
| 4. Graphics quality, photo-like | No on its own: script-built models read as toy-like; needs the Build 33 style study's rendering look on top ~ |

Kids' games is not a listed speed run, so there are no listed requirements to check it against. ✓

## Risks and cover

| Risk | Cover |
| --- | --- |
| Code-built models look toy-like | Meshy for characters; style packs and the arch-renders render look for the rest |
| Each new kind of asset needs a few fix rounds | Keep a recipe library of scripts that worked; validator plus a rendered still on every asset |
| GitHub Actions locks when minutes run out (CB-550, again today) | Keep the job small; watch the minutes; the cloud workspace can run Blender directly in the meantime |
| Meshy's cloud workspace access is blocked; only GitHub is reachable | The GitHub job is the bridge; the Meshy web app in the browser pane is the manual fallback |

## If adopted

- **What gets built:** one skill, "asset generator": sentence or drawing in → style pack → model (Blender script, or Meshy for characters) → textures, collision, sliders, animations → validator → .glb, still, sprite → the family asset library.
- **Dollars:** $0 for the copy; Meshy paid plan plus API credits; GitHub Actions minutes beyond the free monthly allowance. ~
- **Charles's hours:** about 1, with the boys for the first drawing-to-game run. ~
- **Proof of done:** a boy's drawing and one sentence produce a character and two matching props that load and move in an arcade game.

## Sources

- @jurlycat on X, Oct 10 2026: https://x.com/jurlycat/status/2109129990029930805
- SINNON home: https://www.sinnon.net/
- SINNON Asset Generator and plans: https://www.sinnon.net/infrastructure?assetgen=open
- SINNON terms: https://www.sinnon.net/terms
- Meshy Image to 3D API: https://docs.meshy.ai/en/api/image-to-3d
- Meshy API quick start: https://docs.meshy.ai/en/api/quick-start
- Blender Kiln listing: https://mcpmarket.com/tools/skills/blender-kiln-3d-forge
- Formula-shapes card (Oct 10 2026): lab/cards/formula-shapes.md
- Test repo (private): https://github.com/Chooch333/kids-games
- Working document: https://claude.ai/artifact/RKEUae3dx7u4wsrH1DuVkg
