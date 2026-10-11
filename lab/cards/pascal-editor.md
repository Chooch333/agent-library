---
title: "Pascal Editor"
reviewed: 2026-10-11
tools: [pascal-editor]
draft: false
---

## What it is
Pascal is a free, open-source 3D building editor that runs as a web page. ✓ It has two parts:
- **A small program that stores projects and serves the page.** It runs on Pascal's website or on your own PC.
- **The page itself.** It draws the 3D in the browser, using that computer's graphics card.

You draw walls, floors, windows, doors and roofs, and paint them from a material library. You can pull floors apart and walk around the building. ✓ Claude can create and change models without anyone clicking. ✓✓ It also hands models to Blender, through a free add-on, for photo-like stills. ✓

Terms:
- **Graphics card:** the chip that draws 3D. The cloud workspace has none; your PC does.
- **Fork:** your own copy of the code on your GitHub account.
- **Scene file:** Pascal's model saved as one text file.

## Verdict by tool
- **Pascal Editor: Adopt now.** It passed the hands-on test on Charles's PC (round 2). ✓✓ Charles saw the output and said he would use it (2026-10-11).

## Where it fits
- **Speed run arch-renders: gates 2 and 3** (massing and materials), plus the review screen and the 3D source for gate 4 stills. ✓
- Harness map: Digital hands, pipeline step 6. Blocks 7 (geometry stack), 8 (render review), 16 (one skill per tool pack) and 19 (pre-approved command list).
- It overlaps the queued Build 35, which would build its own browser 3D scene with materials and a library screen. Pascal already does most of that on the same technology. ✓

## What we could use it for
**Now**
- The editable building model for every speed run. Charles can fix it himself by dragging a wall or swapping a material, not only by pinning.
- Material options on the facade, swapped live.
- Floors pulled apart for phasing pieces. ✓✓
- Storyboard stills with real sun and shadows. ✓✓
- Hand-off to Blender for photo-like hero stills. ✓ (add-on exists; ~ untested)

**Later**
- Duplex and quadplex layouts and renovation options. Pascal's home toolset is its strongest suit. ✓
- iPhone Pro room scans into an editable model, for example the attic. ✓ (docs; untested)
- An explorable building page on a website. ✓ (docs)

**Cannot**
- Read drawings itself. ✓✓ Claude does the reading.
- Sloped sites or walkout levels. ✓✓
- Finish patches smaller than a full-width band, in the installed version. ✓✓
- Hand over a 3D file through its AI connection. ✓✓ Export from the browser app works (see What we checked).

## What we checked
- **License and status.** MIT license, 17.5k stars, latest release v0.9.1 (June 2026). The local install is runtime 1.0.3. ✓
- **Round 1, cloud workspace.** It built and ran, but with no graphics card and no material images it gave a white box. ✓✓ The look was unproven, not poor.
- **Round 2, Charles's PC.** Claude read the six Crider sheets and wrote the scene file: 56 wall pieces, 58 windows, double doors, 5 canopies, the raised parapet, the brick tower, and finish bands from the A300 schedule. ✓✓ Pascal loaded and drew it with real brick, stone, panels, sun and shadows. ✓✓ Nothing about the building went to Pascal's servers; only stock material pictures came down. ✓✓
- **Version gap.** The one-command install (1.0.3) is older than the code on GitHub, and its finish format differs. The first load lost every finish until the file matched 1.0.3. ✓✓
- **AI connection.** Building piece by piece stalled when segmented walls closed the outline. Writing the scene file and loading it worked. ✓✓
- **Setup.** One command from Charles in PowerShell (`npx.cmd`). Claude cannot type into terminals. ✓✓
- **Export for Blender (2026-10-11).** "Export GLB" on the PC produced a standard 3D file. ✓✓
  - 2.35 MB, glTF 2.0.
  - 819 parts, every wall, window, door, slab and level named and typed: 56 walls, 58 windows.
  - 16 materials, with 6 texture images embedded and the glass set up as glass.
  - It took about a minute to build.
  - Blender opens this format natively ✓, and Pascal also has a one-click "Send to Blender" for a Blender running on the same PC ✓.
  - Opening it in Blender itself was not tested. ~

## What else does this job
**TH's own route: Build 33's tracer, plus Build 35's planned scene.**

| | Build 33 tracer (+ Build 35 scene, planned) | Pascal (lab round 2) |
|---|---|---|
| Proven on | A generated, clean 30×24 ft two-story sample ✓ | A real FA Wilhelm set, six sheets ✓✓ |
| How the drawing is read | A script measures vector lines; dimension error 0% on the sample ✓ | Claude reads the sheets by eye and from dimension text; overall sizes exact, bay positions ±1–2 ft ~ |
| Checks | 8 automatic self-checks plus an independent checker ✓ | Pascal's file validator only ✓✓ |
| What the model holds | White box: walls, openings, slabs, parapets, 59 named parts ✓ | Textured: finish bands, storefront grids, canopies, tower, entry, sun and shadows ✓✓ |
| Materials | Not yet; that is Build 35 (custom scene and library screen to build) ✓ | Built-in library and editor; swaps live ✓✓ |
| Charles's review | Pins on a model viewer ✓ | Pins or direct edits in a full editor, floors apart, 2D plan ✓✓ |
| Where it runs | Cloud ✓ | The model is written in the cloud; the drawing needs a graphics card (PC) ✓✓ |

**Recommendation: take the Python tracer out of the default path.** Build 33's tracer is the better **reader** (measured and checked), but it was proven only on its own clean sample. Claude's reading got the real Crider set close enough for visuals, with sizes and heights exact from dimension text. ✓✓ Pascal is the better **model, editor and viewer**. Keep the tracer on the shelf as a backup for sets without a clean grid; TH decides. ~

**Other options.**
- **Blender alone:** best stills, no live editing, heavy for Claude to drive. ✓ (lab, 2026-10-09)
- **Revit or SketchUp:** paid desktop apps, hard for Claude to drive. ~

## Requirements check (arch-renders)
1. **Conventions: yes, with a build.** Pascal saves a camera view on any part of the model. ✓ TH stores the standard camera set (aerial-34, street, entry) on each run's model. ~ Opening text and callouts are not Pascal's job.
2. **Storyboard: yes.** Stills come from the browser on the PC. ✓✓
3. **Motion menu: phasing yes; the rest is not its job.** Floors come apart in one click. ✓✓ Pascal stills feed the motion tool.
4. **Graphics quality: partly.** Round 2 is a clean, textured model look with real sun and shadows, not photo-like. ✓✓ The path to photo-like runs through Blender (free, ~ untested) or Studio (paid credits), using the same model.

## Risks and cover
- **Version drift.** Cover: fork it, lock one version, and update on purpose. ✓✓
- **Material pictures come from Pascal's servers.** Cover: keep a mirror copy on the PC or in the fork. ✓✓
- **Thin material library** (one stone; no metal or wood siding in 1.0.3). Cover: newer versions add siding ✓; add custom materials to the scene. ~
- **Claude's reading is by eye.** Cover: Build 33's tracer for geometry, and an assumption list at every stop. ~
- **Client drawings.** Cover: local Pascal only, never the hosted site. ✓✓

## If adopted
- **What gets built:** see the handoff below.
- **Dollars:** $0. Studio credits are optional and stop at a money stop.
- **Charles's hours:** about 1 hour across review stops. ~
- **Proof of done:** one real plan set goes in and comes out as a saved Pascal project on the PC with three standard stills. Charles passes gate 2 and gate 3 in Pascal.

## Handoff: how the speed run could organize around Pascal
*Thoughts for TH to scope, not a workflow spec. Charles's direction: no laptop runner, and the Blender hero still is the next step.*

**1. Where Pascal lives (no laptop runner)**
- Pascal runs on Charles's PC, version-locked from the fork, on a fixed port: `npx.cmd @pascal-app/cli start --port 3434`.
- It starts by itself at Windows login through a one-time startup shortcut. Charles sets that up once; nothing else runs it. ~
- Never use the hosted site for client work.
- Open question for TH: the work PC instead of the personal PC (FA Wilhelm IT rules).

**2. How Claude drives it**
- **Read:** the cloud session reads the plan set and writes `takeoff.json`. Every value names its sheet or is marked assumed. Build 33's tracer is not in the default path.
- **Write:** a generator in arch-renders turns the takeoff into a Pascal scene file for the locked version. The lab's generator, about 9 KB, is the starting point.
- **Check:** the cloud checks the file with Pascal's own validator, from the same version, before it is used. ✓✓
- **Load:** through the Browser pane in the Claude desktop app, with "Load build". It takes seconds. ✓✓
  - The loaded model is not saved as a Pascal project, so the scene file in the run folder is the record and is simply reloaded each time. ~ Saving as named projects is optional and untested.
- **Review:** Charles looks, pins or edits in the Browser pane. Any edit he makes gets saved back with "Save build" into the run folder as the next version.
- **Cameras:** the standard set (aerial-34, street, entry) is stored with the model, using Pascal's per-part saved views. ~

**3. Where files live (one folder per run)**
- `runs/<run-id>/` holds:
  - `sheets/`
  - `takeoff.json`
  - `scene.v1.json`, `scene.v2.json`, and so on
  - `stills/`
  - `export/model.glb`
- Source of truth: the run folder plus cbrain's run tables. Pascal's own database on the PC is not relied on.
- Client drawings stay on the PC and in private storage only.

**4. Gates mapped onto Pascal**
- **Gate 1:** sheet index and scale, read by Claude.
- **Gate 2:** a Pascal model with textures off (white box). Charles reviews, pins or edits.
- **Gate 3:** the same model with materials from the finish schedule. Charles swaps materials live. One model serves both gates, which folds the materials step into modeling.
- **Gate 4, next step for TH:** export the GLB (proven ✓✓), bring it into Blender, and make the photo-like hero still. Two routes for TH to choose between:
  - "Send to Blender" on the same PC (one click, uses the PC's graphics card).
  - Move the GLB to the cloud and render with Blender there (no graphics card, slower).

  Stills and floors-apart views also feed the motion tool.

**5. Decisions for TH**
- Rescope Build 35 around Pascal instead of a custom scene and library screen.
- Lock the version: 1.0.3, or the fork's current code (newer finishes, siding).
- Set up the startup shortcut.
- Settle how the GLB and stills get from the PC into the run folder. Each browser download needs Charles's OK, or use "Send to Blender".
- Keep a copy of the material images.
- Run the first Blender hero still on the Crider model as the gate 4 proof.

## Sources
- github.com/pascalorg/editor (README, license, releases) ✓
- editor.pascal.app/docs: mcp, studio-renders, credits, blender, guide-images, export ✓
- `@pascal-app/core` 1.0.3 schema (wall bands, slots) and repo `main` (face regions) ✓
- Lab tests 2026-10-10 and 2026-10-11, Crider study page: https://claude.ai/artifact/X8Zi76V8kN7AUvW2DEUh3o ✓✓
- agent-library `skills/arch-massing/SKILL.md` 0.1.0; arch-renders `progress.md`; Project State Build 33 (c716fa4c) and Build 35 (da0d7a1a) ✓
