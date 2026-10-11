---
title: "Formula-built 3D shapes (Inigo the Dragon)"
reviewed: 2026-10-10
tools: [formula-shapes]
draft: false
---

## What it is

A way for an AI to build a 3D shape as math, by blending simple blobs (spheres, boxes, tapered tubes), instead of as triangles. Keenan Crane, a Carnegie Mellon graphics professor, showed it with one dragon on Oct 9, 2026. A method, not a product: no app, no tool, one example. ✓

Terms: a **mesh** is the normal 3D model, thousands of tiny triangles, and every game engine uses them. An **implicit shape** (signed distance function) is a formula that gives, for any point, its distance to the surface; nothing is stored, the shape is computed when drawn. **Meshing** turns a formula shape back into triangles. **Rigging** gives a model a hidden skeleton and tells each part of the surface which bone to follow, so it can move in a game.

Facts: the dragon's files are CC0 (free for any use) ✓. The AI used was "Astra", most likely OpenAI's GPT-6 Astra (released Sep 3, 2026) ✓ model exists · ~ same Astra. It took 25 hours of AI work and 27 rounds of human feedback ✓, and 45 minutes to render a short video ✓. The author says it only works for round, simple shapes, and that image-to-3D services beat it on speed, cost and quality ✓.

## Verdict by tool

| Tool | Verdict | Come back when |
| --- | --- | --- |
| Formula-built 3D shapes (Claude writing them) | Shelf | Block 7, Geometry stack, is being built |

Passed the hands-on test, but it serves no listed speed run and block 7 is not next in line. Not Never: free, runs with no screen, and nothing else gives rigging for free.

## Where it fits

Digital hands layer · pipeline step 6 (make on screen), step 7 uses its stills · block 7, Geometry stack, which already lists "game art" · plus a skill under block 16 if adopted · digital-sweep phase. Replaces nothing; sits beside Blender and image-to-3D services. ✓ harness map

## What we could use it for

- **Now:** nothing in the active speed run (arch renders). ✓
- **Later:** simple, round, toy-like characters for the boys' games (Roblox Studio or a Claude-coded browser game) that arrive already rigged; mascots; 3D-print toys of their characters (block 9, formula shapes are always watertight); a geometry project for Graham. ~
- **Cannot:** match a detailed or realistic picture quickly; anything for building renders (hard-edged shapes). ✓ author's own limits

## What we checked

- The full X thread (27+ posts), read in the browser pane. ✓
- The download page: CC0 license, code, triangle version, video. ✓
- The AI model's release and price. ✓
- Meshy and Tripo plans; Roblox and Unreal import rules. ✓
- Hands-on in the cloud workspace (2 CPUs, no graphics card): Claude wrote "Blobbo" as about 25 blended parts in one pass ✓✓; drew stills straight from the formula, 3 s each ✓✓; meshed to 74,512 triangles and trimmed to 8,999 ✓✓; set an 8-bone skeleton with each point's bone taken from the part it came from ✓✓; added a 1 s walk and a 1.1 s jump ✓✓; saved .glb (377 KB) and .gltf (507 KB) in 3.4 s ✓✓; official Khronos glTF validator, 0 errors and 0 warnings ✓✓; read the file back and played both moves frame by frame, shoulders bend cleanly with arms overhead ✓✓.
- Not tested: matching a picture the boys bring in; opening the file in Roblox Studio or Unreal; Claude viewing the published preview page (browser pane not signed in).
- Preview page: https://claude.ai/artifact/TpZ7YfYpgJ52BUYedjP8ED

## What else does this job

| Option | Picture in? | Moves in a game? | Cost | Mark |
| --- | --- | --- | --- | --- |
| Meshy | Yes, about 3 minutes | Yes: auto-rigging and animation, 0 credits in the web app | Free: 100 credits a month, about 4 models. Pro about $20 a month. API is separate prepaid credits: about 41 per character with two moves | ✓ |
| Tripo | Yes | Yes: auto-rigging; .glb and .fbx; Unreal and Godot add-ons; MCP connector | Free: 300 credits, no commercial use. Pro $15.90 to $19.90 a month | ✓ review, date unclear |
| Formula method (this card) | Only with many hours of AI time; untested | Yes, rigging free from the parts | AI time only | ✓✓ moves · ~ picture |
| Blender, driven by Claude (block 7) | No | Yes, with Blender's rigging | Free | ~ |
| Roblox Cube, inside Studio | Text only as of March 2025 | Not covered as of March 2025 | Not stated | ✓ 2025 · ~ today |

Meshy has an official MCP connector (local install on the laptop, needs an API key and prepaid credits). It is not in Claude's connector directory, and the cloud workspace cannot reach Meshy's servers. ✓

## Requirements check

Arch renders, the one listed speed run:

| Requirement | Answer |
| --- | --- |
| 1. Conventions | Not this tool's job |
| 2. Still-shot storyboard | Not this tool's job |
| 3. Menu of motion pieces | Not this tool's job |
| 4. Graphics quality, photo-like | No: makes smooth toy shapes; buildings are hard-edged and regular modeling already handles them |

Serves no step of the arch-renders chain. Kids' games is not a listed speed run, so there are no listed requirements to check it against. ✓

Game engines: Roblox Studio imports .gltf and .fbx with skeleton, skin, animation and vertex colours; limits are 20,000 triangles per mesh, 4 bones per point, one animation per exported file. Blobbo fits, with Walk and Jump exported separately. ✓ Unreal lists glTF and .glb as importable; skeletal glTF import is described in its forums, also at 4 bones per point. ✓ format · ~ skeleton

## Risks and cover

| Risk | Cover |
| --- | --- |
| Matching a kid's drawing could take many hours of AI time | Start from an image-to-3D model, as the researcher did, and rebuild as parts only when needed |
| Ragged colour edges (colour stored per triangle corner) | Bake colour into a painted texture at export |
| Untested inside Roblox Studio and Unreal | One import on Charles's PC before any adopt |
| One-day-old technique, single example | Shelf, not adopt; recheck at block 7 |

## If adopted

- **What gets built:** one agent-library skill, "formula characters": picture or sentence in, parts written, meshed, rigged, textured, one .gltf per move, plus a preview page.
- **Dollars:** $0 beyond Claude usage.
- **Charles's hours:** about 1, sitting with the boys for the first Roblox import. ~
- **Proof of done:** a character from one of the boys' drawings walks and jumps inside Roblox Studio.

## Sources

- Keenan Crane's thread: https://x.com/keenanisalive/status/2108708523236602056 (read 2026-10-10)
- Inigo the Dragon download page: https://www.cs.cmu.edu/~kmcrane/Projects/ModelRepository/index.html#inigo
- GPT-6 Astra release note: https://docs.apiyi.com/en/news/gpt-6-astra-launch
- Meshy app pricing: https://docs.meshy.ai/en/webapp/pricing
- Meshy API pricing: https://docs.meshy.ai/en/api/pricing
- Meshy MCP connector: https://docs.meshy.ai/en/api/ai
- 3D AI price comparison: https://sloyd.ai/blog/3d-ai-price-comparison
- Tripo review: https://pasqualepillitteri.it/en/news/7811/tripo-ai-review-3d-model-generator
- Roblox 3D Importer: https://create.roblox.com/docs/art/modeling/3d-importer
- Roblox mesh specifications: https://create.roblox.com/docs/art/modeling/specifications
- Unreal Interchange import reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/interchange-import-reference-in-unreal-engine
- Roblox Cube announcement: https://about.roblox.com/newsroom/2025/03/introducing-roblox-cube
- Working document: https://claude.ai/code/artifact/38d32084-8a70-4f70-aa9a-b1ef0ddc6e8d
