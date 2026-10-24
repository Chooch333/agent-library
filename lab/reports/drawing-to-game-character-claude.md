---
title: "Drawing to Game Character - Claude"
type: rd-report
brief: ""
reviewed: 2026-10-24
test_date: 2026-10-21
test_completed: 2026-10-24
status: complete
tools: [claude-code-character-opus, claude-code-character-fable, fable-own-library]
report_url: https://claude.ai/artifact/Jm3p7XfuapinN85DPvQ7j9
clips:
  - env: Claude Opus 5.5, cloud machine
    anchor: opus-cloud
    file: still_opus_cloud.png
  - env: Claude Fable 5.1, cloud machine
    anchor: fable-cloud
    file: still_fable_cloud.png
  - env: Claude Fable 5.1, 15-minute budget, brief only
    anchor: fable-timed-cloud
    file: still_fable15_cloud.png
  - env: Claude Fable 5.1 with the parts library
    anchor: fable-kit-cloud
    file: still_fablekit_cloud.png
  - env: Claude Fable 5.1, own parts library first
    anchor: fable-ownlib-cloud
    file: still_fablelib_fixed_cloud.png
image: compare_same_view.png
clips_home: "Published with the report at report_url; sources in Chooch333/kids-games lab/claude-image-to-3d/ (private)"
draft: false
---
# Drawing to Game Character
## Claude Fable 5.1 · Claude Opus 5.5 (Three.js code)

**Test problem:** Study whether Claude, from one drawing, can produce an editable, rigged, animated game character comparable to Meshy's.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-21 | 2026-10-24 | Complete |

**Rev history**
0. 2026-10-21 · First draft; verdicts proposed, awaiting Charles's likeness judgment
1. 2026-10-23 · Charles judged Opus better than Meshy; two Fable variants added (15-minute budget, with and without the parts library)
2. 2026-10-24 · "Kit" renamed parts library; Fable tested building its own library first; who builds the library now has a tested reason
3. 2026-10-24 · Charles approved: fast mode (Fable) and detail mode (Opus) over one shared parts library; report Complete

Evidence key: **Tested** = we ran it and measured it · **Published** = from the maker's own documentation · **Assumed** = our judgment, not yet checked.

## 01 Tech description
The tech under test is **Claude itself** turning a drawing into a 3D game character written as **Three.js code**, with no outside 3D service. Three.js is the free, open-source library the family arcade's browser games already run on (Published). The character is a list of named parts (head, mask, wrapper ends, arms, legs) with colours and sizes as numbers at the top of one file; the moves (idle, walk, jump) are short formulas of time. The same file is exported to a **.glb** (the standard game-model file Meshy also produces) so it drops into the existing pipeline. A **rig** is the skeleton of bones that lets the parts move; **skin weights** say how much each surface point follows each bone.

### How it runs
- **Where:** the cloud machine Claude works on (2 processors, 7 GB, no graphics card, no screen) for the build; any browser for the result (Tested).
- **Subscription cost:** none new. Three.js is MIT-licensed, Blender (used only to render stills) is GPL (Published).
- **Cost to run:** $0 beyond the Claude plan. The cost is Claude's time: 6 minutes (Fable) or 79 minutes (Opus) per character (Tested).
- **How Claude controls it:** writes and runs the code itself; no login, no captcha, no screen (Tested).
- **What it needs:** `npm i three gltf-validator`, and `pip install bpy` only for stills (Tested). A company may use the output (Published) (library licences); Anthropic's terms give the user the output (Assumed), not re-read today.

## 02 Findings
Claude can build Super Sweets from the drawing as plain code, rigged and animated, with no outside service and at no cost. **Opus 5.5** made the closer likeness (proper swirl, shaped mask, ruffled wrapper ends, folded cape) in **79 minutes**; **Fable 5.1** made a cruder but recognisable character in **6 minutes**, and given a 15-minute budget it still stopped at 6 or 7; handing it a **parts library** of reusable helpers lifted from Opus's run (face decals, a ruffled-fan generator, the pose machinery, the exporter) closed much of the gap in 7 minutes, so the combination is "build the parts library once, then any run builds each character from it." Fable can build such a library itself (4 minutes, 39 general helpers), but the character it then made was a notch below the one built from Opus's library, and it baked its cartoon outlines into the game file, which turns the character black in every viewer except its own. Charles locked the workflow in on 2026-10-24: **fast mode** (Fable, about 7 minutes) and **detail mode** (Opus, about 80 minutes), both reading one standing parts library that Opus builds and grows. Whether Opus holds this level on a second drawing is untested; the skill handed to Total Harness is designed to make it repeatable. Charles opened both viewer pages on 2026-10-23 and judged the Opus build much better, and better than Meshy. All four runs passed the Khronos validator with zero errors and both play idle, walk and jump. The editability claim held: a blue mask and 30% longer legs took 3 changed lines (Fable) and 5 (Opus), re-exported in seconds; on Meshy's file the same legs took a 30-line Blender script and the mask could not be recoloured without repainting its texture. The route to adopt: Claude writes the character as code from the parts library, exports the .glb, and the arcade's games load either.

**Key numbers**
- **6–7 vs 79 min** · Fable (any variant) vs Opus, brief to full deliverable; Fable ignored a 15-minute budget twice (Tested)
- **3 / 5 lines** · to recolour the mask and lengthen the legs (Fable / Opus); Meshy: 30-line script, mask not possible (Tested)
- **0.5 / 1.4 MB** · .glb size (Fable / Opus) against Meshy's 2.95 MB game file (Tested)

### Inputs the workflow must supply
- One clean drawing of the character, front view, plain background (the same input Meshy gets).
- The sealed brief used here: deliverable list, move names, size cap, validator requirement.
- A choice of model per job: Opus for the finished character, Fable for a quick draft (Assumed).

### Harness the Total Harness project needs to build
- A **code-character step** beside the Meshy step in the asset generator: drawing in, `character.js` + `.glb` + still out, validated.
- A **standard character file shape** (colour and size constants up top, named parts, `createCharacter()` with idle, walk, jump) so every character edits the same way.
- The **Character Studio overlay** Charles asked for on 2026-10-13 now has something to edit: sliders over those constants.
- The **character parts library** as a maintained file: finished code for the shapes every cartoon character needs (face decals that hug a round body, ruffled fans, limbs between two points, ellipsoids, bones, pose and move machinery, the headless exporter). It is not instructions: a run calls it instead of re-inventing. Every character run reads it; it grows when a drawing needs a shape it lacks. Opus builds and grows it; Fable builds characters from it (Tested), one character.
- A **handoff rule**: cartoon outlines live in the viewer only, never in the .glb. Opus and the first Fable followed it; the library-first Fable did not and shipped a black character (Tested). The game-file check in the asset step must catch it.
- A **character-from-drawing skill** with two modes, so detail mode does not re-discover its method and fast mode does not stop early. It writes down what the Opus run did and the others skipped (Tested), one run: sample the drawing's colours; trace the key outlines (mask, eyes, mouth) from the picture's pixels instead of guessing them; build every part from the library and add any missing shape to the library as a general helper, not a one-off; render a still, compare it with the drawing, fix the three biggest differences, and repeat until a likeness checklist passes (body shape, face, each distinctive feature, pose, colours); then the handoff checks. Whether the written steps make Opus consistent is (Assumed) until a second drawing is run.
- A **likeness checklist** the skill fills in per drawing before building, so "done" has a definition. Fable stops when it thinks it is done (Tested); the checklist is what it has to satisfy.

## 03 Experiment parameters
Four sealed runs received the identical drawing and produced the same deliverable list, with no view of each other's work: Fable 5.1 and Opus 5.5 on the plain brief (2026-10-21), then two fresh Fable 5.1 workers with a 15-minute budget, one brief-only and one with a parts library of helpers extracted from Opus's code (2026-10-23); then a fifth Fable run told to write its own general parts library first and build the character from it, 25-minute budget (2026-10-24). Meshy's existing Super Sweets game file is the reference, not a test environment.

**Test input:** The Super Sweets illustration exactly as sent to Meshy on 2026-10-12 (1024×1024, from the private kids-games repo). Recovered by a small GitHub job that wrote it out as text, because the cloud machine cannot download binaries from the private repo.

**The test:** From the drawing, produce: the character as Three.js code with named parts and colour constants; a viewer page with Idle, Walk and Jump; a .glb with skeleton and the three moves baked in, validated with zero errors; one still; a timing log. Method was each model's choice, limited to no-screen routes on the cloud machine.

**Capabilities tested:** Drawing to 3D by eye; rigging; walk and jump; headless .glb export; validation; editability (one scripted change); handoff (the .glb opens in Blender and the validator, the same checks the Meshy pipeline passes).

**Not tested:** **Painted texture from the drawing:** not this route's job, and the route that gives it (silhouette inflation) kills editability. **The viewer pages in a browser:** no browser on the cloud machine; both pages are published and Charles opens them. **Run and idle variations beyond the three moves.** **Charles's PC:** not needed.

**Output:** Per environment: `character.js`, `viewer.html` (published as a live page), `character.glb`, `still.png`, `validation.json`, `log.md`.

**Settings:** Three.js 0.186.1, glTF validator via npm, Node 22. Comparison stills: one neutral Blender 5.2.2 Cycles setup (processor only, 40 samples, same camera, lights and background) rendered from each .glb, so the three game files are seen the same way. Each model's own still is shown too.

**Machines and versions:** Cloud machine only: 2-core Intel Xeon, 7 GB, no graphics card. The first Fable 5.1 run was live in the chat; Opus 5.5 and the two later Fable runs were sealed workers in the same chat, each reporting its own model name (`claude-opus-5-5`, `claude-fable-5-1`) (Tested).

**The parts library:** Opus's generic helpers lifted out of its `character.js` with every Super Sweets-specific name and number removed (checked by search: none left): geometry helpers (segment, ellipsoid, sphere-hugging decal patches, a ruffled-fan generator, outline shells), bone and part builders, the pose and move machinery, and the headless exporter. 199 lines. The library worker used 14 of its 15 helpers and copied them into its own file (Tested). Fable's own library (`parts.js`, 32 KB, 39 exports) is broader: shapes, decals with adaptive subdivision, flares, sheets, vertex-colour patterns, outlines, a rig class, exporter. It names wrapper ends and capes as examples but holds no numbers from this drawing (Tested).

**What we measured:**
- **Time:** wall clock from brief to first validated model and to full deliverable, from `date -u` stamps.
- **Cost:** anything beyond the Claude plan.
- **Size:** triangle count and .glb bytes, read from the files, not the logs.
- **Validity:** Khronos glTF validator errors and warnings.
- **Editability:** lines changed and seconds to re-export for one scripted edit (mask to blue, legs +30%), with the same edit attempted on Meshy's file.
- **Likeness:** by eye, Charles's call, from the same-view comparison.

**Side checks:** Both rigs are rigid parts on a bone tree: Opus packages each part as a skinned mesh weighted wholly to one bone, Fable attaches plain meshes to bones; the mechanics are the same (Tested). Meshy's file: 29,817 triangles, one 1024px painted texture plus roughness and normal maps, 24 bones, four moves (Tested).

**Saved test files:** Private, in `Chooch333/kids-games` under `lab/claude-image-to-3d/`: both `character.js` files, viewer pages, logs, the export, validate and render scripts, and the sealed brief. The .glb files are regenerated from `character.js` in seconds by the export script, which is the point of code as the source; they also sit on this page as its outputs. The input drawing and Meshy's game file were already there.

## 04 Results by test environment

### Claude Opus 5.5, cloud machine
sealed worker · Three.js code · rigid parts as skinned meshes · **Adopt now (proposed)**
- **Still:** `still_opus_cloud.png` (neutral render of the .glb). [Live viewer page](https://claude.ai/artifact/NMCYZ91g2DQtACyHz6WeN9) with Idle, Walk, Jump. Opus's own render with outlines: `still_opus_own.png` below.
- **Time:** 79 min to full deliverable; first model at ~68 min (Tested)
- **Cost:** $0
- **Size:** 36,080 triangles · 1.49 MB · 13 bones · 28 parts, each weighted to one bone
- **Validator:** 0 errors, 0 warnings (Tested)
- **Edit test:** 5 lines changed, re-exported in under 1 s (Tested)
- **Quality:** Closest likeness: 8-arm swirl from sampled colours, mask traced from the drawing with slanted eyes, ruffled wrapper ends with pleats, cape with folds, fists on hips. Cartoon outlines exist only in the viewer and its own still, not in the .glb (Tested).
- **Verdict note:** Proposed Adopt now for the family-arcade speed run, pending Charles saying he would use it. The 79 minutes is unattended Claude time, not his.

### Claude Fable 5.1, cloud machine
live in chat · Three.js code · rigid parts · **Shelf (proposed)**
- **Still:** `still_fable_cloud.png` (neutral render of the .glb). [Live viewer page](https://claude.ai/artifact/FYKaFyohKGDY9mf5VnwCyx) with Idle, Walk, Jump.
- **Time:** 6 min to full deliverable; first model at ~2 min (Tested)
- **Cost:** $0
- **Size:** 14,104 triangles · 0.51 MB · bone tree, no skin weights
- **Validator:** 0 errors, 0 warnings (Tested)
- **Edit test:** 3 lines changed, re-exported in 1 s (Tested)
- **Quality:** Recognisable: wrapper ends, mask, eyes, akimbo arms, boots. Weaker swirl, no outline, stiff flat cape, mask too round (Tested).
- **Verdict note:** Charles: "the right speed". Superseded as the fast tier by the parts-library run below; kept as the baseline.

### Claude Fable 5.1, 15-minute budget, brief only
sealed worker · Three.js code · no library · **Never (as a variant)**
- **Still:** `still_fable15_cloud.png`. [Live viewer page](https://claude.ai/artifact/BWJQ8uBXh3ZLCQ9QVwvBbT).
- **Time:** 6 min used of 15; first model at ~4 min (Tested)
- **Cost:** $0
- **Size:** 6,788 triangles · 0.31 MB · 13 bones
- **Validator:** 0 errors, 0 warnings (Tested)
- **Quality:** About the same as the first Fable run: a better mask shape and visible swirl, a disc-shaped body, a stiff cape. The extra budget went unused (Tested).
- **Verdict note:** More time alone buys nothing, because Fable does not spend it. A budget is not the lever.

### Claude Fable 5.1 with the parts library
sealed worker · Three.js code · library lifted from Opus's run · **Adopt now (proposed, as the fast tier)**
- **Still:** `still_fablekit_cloud.png`. [Live viewer page](https://claude.ai/artifact/5nGjBVThxsYSpsX5V7tWMp).
- **Time:** 7 min used of 15; first model at ~3.5 min (Tested)
- **Cost:** $0
- **Size:** 18,928 triangles · 0.82 MB · 11 bones · 30 parts
- **Validator:** 0 errors, 0 warnings (Tested)
- **Quality:** Much closer to Opus: traced mask with slanted eyes, pinwheel swirl, ruffled wrapper ends, a folded cape, akimbo arms. Still short of Opus on the swirl and cape detail (Tested).
- **Verdict note:** Proposed Adopt now as the fast tier of the same route, pending Charles's look. The library, not the time, is what moved Fable.

### Claude Fable 5.1, own parts library first
sealed worker · wrote parts.js (4 min) then the character (8 min) · **Never (as the library builder)**
- **Still:** `still_fablelib_fixed_cloud.png`, outline shells stripped so the character can be seen. As delivered (`still_fablelib_cloud.png`) it renders black.
- **Time:** 12.5 min of 25 (library 4, character 8); first model at ~7 min (Tested)
- **Cost:** $0
- **Size:** 31,128 triangles incl. 16 outline shells · 1.44 MB · 13 bones
- **Validator:** 0 errors, 0 warnings, but the validator cannot see that the outline shells cover the body (Tested)
- **Quality:** Library: broad and general. Character: recognisable, a notch below the Opus-library run (faint swirl, plain cone wrapper ends, less cape shape). Game file: unusable as delivered, black in Blender and the arcade (Tested).
- **Verdict note:** Fable can write a library; the characters it yields are weaker than those from Opus's, and it broke the handoff. Library building stays with Opus. This would change if a second drawing showed Fable's library producing equal characters.

**Comparison image:** `library_test.png`. Library test, same neutral render. Fable with the library lifted from Opus (7 min); Fable's own-library run as delivered (black: outline shells baked into the file) and with the shells removed; Opus.

**Comparison image:** `fable_variants.png`. The Fable variants beside Opus, same neutral render: first run (6 min), 15-minute budget brief-only (used 6), 15-minute budget with the parts library (used 7), Opus (79 min).

**Comparison image:** `compare_same_view.png`. Same-view comparison. The drawing, then the three game files rendered with one neutral Blender setup: Meshy (reference), Fable 5.1, Opus 5.5. Meshy's is a painted mesh; the two Claude characters are code.

**Comparison image:** `edit_test.png`. Editability test, before and after: mask to blue, legs 30% longer. Meshy's legs needed a 30-line Blender script that scaled leg-weighted points and bones; its mask stayed black because the colour is painted into a texture. Fable: 3 lines. Opus: 5 lines.

**Comparison image:** `still_opus_own.png`. Opus's own still: Blender Cycles with outlines added at render time, on the drawing's cream background. The outlines are not part of the .glb.

## 05 Use cases
**Now**
- A drawing becomes an editable, rigged character for the family arcade's Three.js games, with no Meshy credits (Tested).
- Look and move changes as line edits: colours, proportions, move timing (Tested) (colour and proportion).
- A fast character in about 7 minutes from the parts library, close to the long pass; a 6-minute draft without it (Tested).

**Later**
- The Character Studio overlay: sliders bound to the colour and size constants, live in the browser (Assumed).
- New moves added as formulas (run, wave, dance) without re-rigging (Assumed).
- Props and scenery the same way; the SINNON review already showed Claude-written assets work for crates (Published) (lab report 2026-10-12).

**Cannot**
- Painted detail from the drawing: shading, texture, the inked outline inside the .glb. Code characters are flat-coloured parts.
- Organic shapes a child draws freehand (a lumpy monster, fur) will suit Meshy better (Assumed).
- Match Meshy's speed-to-likeness in one pass: 79 minutes versus Meshy's minutes plus credits.

## 06 Requirements check (family arcade)
The family-arcade entry in the speed-run brief lists no standing requirements yet; these are the goals Charles stated for the arcade and its asset pipeline (2026-10-13), checked here.

| Requirement | Answer | Path |
|---|---|---|
| Characters walk, run, jump | Yes | Walk and jump as code formulas, baked into the .glb (Tested). Run is one more formula (Assumed). |
| Revisions chosen through a Claude-side overlay, not inside Meshy | Yes | Every look and size is a named constant; an overlay edits constants (Tested) (edits by hand), overlay (Assumed). |
| Move and look tuning by a standard convention | Yes | Both runs converged on the same shape (constants up top, `createCharacter()`, idle/walk/jump), so a convention can be written from them (Tested). |
| Playable outside Claude, multiplayer, saved progress | Not this tool's job | The character loads into any Three.js game; the arcade site handles the rest. |
| More robust graphics | Partly | Cleaner and smaller than Meshy's file, but flatter: no painted texture (Tested). |

## 07 Risks and cover
- **Likeness is by eye.** Claude sees the drawing once and judges proportions; some characters will come out off-model. Cover: the Fable draft as a cheap check, then edit feedback in words, then Opus.
- **79 minutes per character on Opus** is long if the boys want to see results tonight. Cover: Fable with the parts library in about 7 minutes; Opus unattended when that result is not close enough.
- **The parts library was tested on one character.** Its helpers suit round bodies and flat fans; a different drawing may need new helpers. Cover: Opus extends the library when a shape type is missing (Assumed).
- **Two file shapes.** Fable attached parts to bones directly, Opus packaged them as skinned meshes; both are rigid-parts rigs and both play, but a shared convention should pick one. Cover: the convention in Findings (Assumed).
- **Viewer pages untested in a browser by Claude.** Both published; cover: Charles opens them and reports anything broken.
- **Outlines live in the viewer only.** Games loading the .glb lose the cartoon ink. Cover: the arcade's game shell can add the same outline trick (Assumed).

## 08 If adopted
- **What gets built:** by the Total Harness project: the character-from-drawing skill with fast and detail modes, the parts library as a maintained file (seeded from the Opus run), the character file convention, the likeness checklist, and the handoff check that rejects outlines in the .glb. Beside the Meshy step, not replacing it.
- **Dollars:** $0.
- **Charles's hours:** about 20 minutes: open both viewer pages, judge likeness, and approve the convention (Assumed).
- **Proof of done:** a second, different drawing by one of the boys goes through both modes: fast mode gives a playable character in under 10 minutes, detail mode holds the Super Sweets level without Charles steering, and a look change is made from the overlay. That second drawing is also the consistency test this review could not run.

## 09 Sources
- No Discovery Brief (review ran without one). Working Doc for this review: [Claude image-to-3D vs Meshy](https://claude.ai/artifact/395NdUVFyRdocV4FEk4cPY), 2026-10-21.
- Prior lab reports: Video Game Asset Generator - Sinnon (2026-10-12, the Meshy pipeline); Formula-built 3D shapes (2026-10-10).
- Run logs and sources: `lab/claude-image-to-3d/` in Chooch333/kids-games (private): `fable/`, `opus/`, `fable-timed/`, `fable-kit/` (with `kit/kit.js`, the parts library), and the sealed briefs.
- [Three.js documentation](https://threejs.org/docs/) · [Three.js licence (MIT)](https://github.com/mrdoob/three.js/blob/dev/LICENSE) · [Khronos glTF Validator](https://github.com/KhronosGroup/glTF-Validator) · [Blender licence](https://www.blender.org/about/license/)
