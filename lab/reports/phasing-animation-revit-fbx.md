---
title: "Phasing Animation - Revit FBX"
type: rd-report
brief: ""
reviewed: 2026-10-27
test_date: 2026-10-27
test_completed: 2026-10-27
status: complete
tools: [revit-fbx-phasing, blender-workbench-whitebox]
report_url: https://claude.ai/artifact/6HtVJhsw9H3YGh2sAhy5xL
clips:
  - env: "1. One FBX, view's default phase filter"
    anchor: a1-default-filter
    file: clip_a1-default-filter_cycles_cloud.mp4
  - env: "2. Show All FBX, rebuilt axonometric view"
    anchor: a1b-axo
    file: clip_a1b-axo_cycles_cloud.mp4
  - env: "3. Show All FBX, Time Lapse camera as exported"
    anchor: a1b-revitcam
    file: clip_a1b-revitcam_cycles_cloud.mp4
  - env: "4. Camera move between two Revit views"
    anchor: m1-move
    file: clip_m1-move_workbench_cloud.mp4
image: phase_compare.jpg
clips_home: "Published with the report at report_url (client model: clips are not stored in this repo)"
draft: false
---
# Phasing Animation
## Revit 2025 FBX → Blender 5.2.2 (cloud)

**Test problem:** Study how to tell Blender which model content belongs to which construction phase, with no prep beyond the Revit FBX export, and animate it from the Revit camera views Charles names.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-27 | 2026-10-27 | Complete |

**Rev history**
0. 2026-10-27 · Test plan: three ways to mark phases
1. 2026-10-27 · Phases read from one FBX; demolition needs Show All
2. 2026-10-27 · Clip from the Time Lapse camera as exported
3. 2026-10-27 · Camera move between two Revit views
4. 2026-10-27 · Complete; method passed by Charles

Evidence key: **Tested** = we ran it and measured it · **Published** = from the maker's own documentation · **Assumed** = our judgment, not yet checked.

## 01 Tech description
A **phasing animation** shows a building changing over time: what exists today, what gets torn out, then the new work. Revit already stores each element's phase. Every element has a **Phase Created**, and a view's **phase filter** decides which phases it shows and how (Published). This review tested whether that phase information survives Revit's FBX export into Blender, the program that renders our stills and clips, and how to animate it from Charles's own Revit camera views. It builds on the adopted Revit model intake (Revit FBX into Blender, 2026-10-27).

### How it runs
- **Where it runs:** Blender 5.2.2 by script in Claude's cloud workspace (Tested). The FBX exports come from Revit on Charles's work PC.
- **Subscription cost:** $0. Blender is free (GPL) (Published); Revit is already licensed.
- **Cost to run:** $0 (Tested).
- **How Claude controls it:** entirely by script, with no screen. Small Python readers pull the phases and the cameras out of the FBX; Blender renders (Tested).
- **What it needs:** one FBX of the model from a view set to Show All, plus one FBX per extra camera view. No graphics card for the white-box look.

## 02 Findings
One FBX export tells Claude every element's phase with no tagging, as long as the exported view's phase filter is set to **Show All**. New work comes from each element's Phase Created. Demolished elements arrive wearing Revit's **"Phase - Demo"** material, and kept existing elements wear **"Phase - Exist"**. Revit doesn't export the Phase Demolished field, but it isn't needed. The phase was right for all 391 elements of a real FA Wilhelm model. The clip is rendered from the camera view Charles names, as exported. Each FBX carries one camera, so a camera move needs one extra export per view; only the camera is read from those files. A 21-second white-box move with all three phases rendered in 24 minutes at no cost. Route to adopt: Show All export plus named camera views.

**Key numbers**
- **391 / 391** · elements given the right phase, matching Revit's own phase colors (Tested)
- **0** · elements tagged by hand; the only prep is the export (Tested)
- **2.75 s** · per frame for the white-box move: 21 s clip in 24 min, cloud CPU (Tested)

### Inputs the workflow must supply
- One FBX of the model, exported from a 3D view whose phase filter is **Show All**.
- One FBX per camera view used (start and end of a move). Only the camera is read from these, so their phase filter doesn't matter.
- Which view to render from, seconds per phase, and whether the camera holds or moves.

### Harness the Total Harness project needs to build
- A **phasing step** in the arch-renders run that reads phases from the Show All FBX: Phase Created for new work, "Phase - Demo" for demolition, "Phase - Exist" for kept work.
- A **camera reader** that takes only the camera from each extra FBX and fixes what breaks on import (an 18.5 m far clip and a stray animation). It never substitutes a different view.
- A **storyboard stop**: one still per phase from the named view, before any motion.
- A **move clip**: straight path with a smooth start and stop, facing direction turned smoothly, phases on time with short fades. No wall-avoidance rule (Charles).
- Final quality later through the adopted routes: the intake material script and Cycles on the PC graphics card.

## 03 Experiment parameters
We exported one real FA Wilhelm model from Revit with and without the Show All phase filter, read its phases by script, and rendered Existing, Demolition and New from a rebuilt view, from Charles's Time Lapse camera, and as a camera move between two of his views. Only the export setting, the camera and the render look changed.

**Test input:** OfficeBuildout, an FA Wilhelm office interior (about 30 × 21 m, 6.5 m tall) with phases Existing and New Construction. Three FBX exports from Revit 2025: "3D View: Time Lapse view" with its default phase filter (422 elements), the same view on Show All (439 elements), and "3D View: Clip End" (camera only).

**The test:** Read every element's phase from the FBX by script and check it against Revit's own phase colors; render one image per phase; then render clips: holds from a fixed view, and a 21 s camera move.

**Capabilities tested:**
- Phase Created per element (Revit stores family, type and element values as a chain of changes; the reader resolves it).
- Demolished elements: with and without Show All.
- The named view's camera: as exported, rebuilt, and moved between two views.
- Phase holds with fades; camera move with three phases.
- Claude driving it all by script with no screen.

**Not tested:**
- **Marking phases on a plan** (for sequences not modeled in Revit) and **one export per phase**: not needed once one Show All export worked.
- **Projects with more than two Revit phases** (Phase 1, 2, 3): only Existing and New Construction were available.
- **Camera data pasted as text** from a Dynamo script: written, not run.
- **Final-quality motion** with materials on the PC: covered by the adopted Cycles-on-PC route.
- **Large models:** one interior only.

**Output:** Four clips with Existing, Demolition and New, plus one comparison sheet. Holds: 3 s per phase, 0.5 s fades, 10 s. Move: 7 s per phase, 21 s, 24 frames a second.

**Settings:** Stills and holds: Cycles on CPU, 48–64 samples, denoise on, AgX look; 1280×720 for the rebuilt view and 1280×960 (the Revit camera's 4:3) for the Time Lapse view. Move: Blender's Workbench engine, flat white with cavity shading and outlines, 1280×960.

**Machines and versions:** Claude's cloud workspace: 2-core CPU, 7 GB, no graphics card, Blender 5.2.2 LTS (Python package). Exports from Revit 2025.

**What we measured:**
- **Phase accuracy:** each element's resolved phase against the phase material Revit put on it.
- **Demolition:** elements carrying "Phase - Demo", per export.
- **Camera:** what the exported view frames, and where the straight move crosses walls.
- **Time:** seconds per render from Blender's timer.

**Side checks:**
- Revit's view properties show only Eye Elevation and Target Elevation, not the camera's position or direction (Published).
- Blender shortens element names over 63 characters; the reader matches those by name start (Tested).
- Render-look timing on one frame of the Clip End view: Workbench 4.1 s at 960×720 vs. Cycles 14.6 s at 640×480 (Tested).

**Saved test files:** Private, in `Chooch333/arch-renders` `lab/phasing-intake/`: `phases.py` (phase reader), `b_getcam.py` (camera-only reader), `b_phase_stills.py` (rebuilt view), `b_phase_cam.py` (stills from the named view), `b_phase_move.py` and `composite_move.py` (move clip), `README.md`, `A1b-notes.md`. Needs `lab/revit-intake/fbxread.py`. The three FBX files stay on Charles's PC (client model). Clips are on the published page.

## 04 Results by test environment

### 1. One FBX, view's default phase filter
Rebuilt axonometric · Cycles · cloud · **Never**
- **Clip:** `clip_a1-default-filter_cycles_cloud.mp4`, 10 s
- **Phases:** Existing and New right for 391 of 391 elements (Tested)
- **Demolition:** None. The filter hid the 17 demolished elements, so they weren't exported (Tested)
- **Per image:** 74–85 s (1280×720, 64 samples)
- **Cost:** $0
- **Quality:** Phases read clearly; the Demolition hold shows nothing removed.
- **Verdict note:** Use Show All instead. This would change if a project has no demolition.

### 2. Show All FBX, rebuilt axonometric view
Camera heading only · Cycles · cloud · **Never**
- **Clip:** `clip_a1b-axo_cycles_cloud.mp4`, 10 s
- **Phases:** All three right: 35 existing, 17 removed, 281 added after the cutaway (Tested)
- **Per image:** 71–83 s (1280×720, 64 samples)
- **Cost:** $0
- **Quality:** Clear overview with roof and ceilings cut away, but it isn't the view Charles named.
- **Verdict note:** Charles: the view he names must be used, fixed if needed, never replaced. This would change if he asks for an overview.

### 3. Show All FBX, Time Lapse camera as exported
Phase holds · Cycles · cloud · **Adopt now**
- **Clip:** `clip_a1b-revitcam_cycles_cloud.mp4`, 10 s, 1280×960
- **Phases:** All three right; a demolished wall in front of the camera disappears, then the new TV wall closes the view (Tested)
- **Camera:** Exact: 5'-6" eye height, facing northwest, 50° lens. Fixed only the 18.5 m far clip and a stray animation (Tested)
- **Per image:** 148–249 s (1280×960, 48 samples)
- **Cost:** $0
- **Quality:** Daylight interior; roof and ceilings stay visible but let light through.
- **Verdict note:** Adopted 2026-10-27: Charles watched it ("Perfect") and passed the method.

### 4. Camera move between two Revit views
Time Lapse view → Clip End · Workbench white box · cloud · **Adopt now**
- **Clip:** `clip_m1-move_workbench_cloud.mp4`, 21 s, 504 frames, 1280×960
- **Move:** 6.7 m straight path with smooth start and stop; facing turned from northwest to west (Tested)
- **Per frame:** 2.75 s (528 renders incl. fades)
- **This clip:** 24 min
- **Cost:** $0
- **Quality:** Clean white-box model with outlines; no frame-to-frame flicker. A preview look, not a finished render.
- **Verdict note:** Adopted 2026-10-27: Charles said the camera path worked well. In this test the move finished at 17 s so the camera passed two new walls before they appeared; Charles says passing through a wall is acceptable and not a rule.

**Comparison image:** `phase_compare.jpg`. Each environment's Existing, Demolition and New Construction images. Row 1 has no demolition; rows 2–4 do. Rows 3 and 4 use Charles's Revit camera views.

## 05 Use cases
**Now**
- Phasing holds (existing, demolition, new) from any Revit view Charles names (Tested).
- A camera move between two Revit views with the phases changing along the way (Tested).
- Storyboard stills, one per phase, before any motion (Tested).

**Later**
- Final-quality phasing clips with materials, on the PC graphics card (Assumed).
- Projects with Phase 1, 2, 3: Phase Created comes through for any phase name (Assumed).
- The 2D plan fading in under the 3D view, per the phasing convention (Assumed).
- Camera data pasted as text from a Dynamo script instead of extra exports (Assumed).

**Cannot**
- Read the Phase Demolished field: Revit doesn't export it (Tested). The demolition material replaces it.
- Carry more than one camera per FBX (Tested), or the Revit view's crop region (Published).
- Show demolition from a view whose phase filter hides it (Tested).

## 06 Requirements check (arch renders)

| Requirement | Answer | Path |
|---|---|---|
| 1. Conventions | Partly | Cameras come from named Revit views, used as exported (Tested). Seconds per phase and fades are settings. The plan-underlay rule isn't built. |
| 2. Storyboard before motion | Yes | One still per phase from the named view before the clip (Tested). |
| 3. Menu of motion pieces | Yes (phasing) | Phasing holds and phasing with a camera move both work (Tested). Finish swaps and the month tracker are other pieces. |
| 4. Graphics quality | Not this test | White box by request. Photo-like output comes from the intake material script and Cycles on the PC (Assumed). |

## 07 Risks and cover
- **Export view not on Show All** drops demolition silently. Cover: after each intake, report how many "Phase - Demo" elements came in, and flag zero.
- **A template that renames Revit's phase materials** breaks the rule. Cover: read the material names from the file and ask once if neither "Phase - Exist" nor "Phase - Demo" appears.
- **More than two phases:** the Exist/Demo materials are relative to the view's phase, so demolition in an earlier phase may be ambiguous (Assumed). Cover: test on the first multi-phase project; one Show All export per phase if needed.
- **Long clips in the cloud.** The white box is fast; photo-like frames take minutes each in the cloud. Cover: final frames on the PC graphics card (adopted route).
- **Client data.** Cover: FBX files and outputs stay private, never in the public library.

## 08 If adopted
- **What gets built:** the harness in Findings, built by the Total Harness project.
- **Dollars:** $0.
- **Charles's hours:** about 2 minutes per project to set Show All and export, plus about 1 minute per extra camera view (Assumed).
- **Proof of done:** a new phased Revit model and two named camera views go in, and storyboard stills plus a 21 s phasing move come out unattended, matching the views Charles named.

## 09 Sources
- No Discovery Brief: this review started from a question in chat and builds on the Revit Model Intake report (2026-10-27).
- Working Doc: [Phasing Intake - Revit FBX to Blender](https://claude.ai/artifact/XGauStMdv6FkXNWbamjtk3). Test scripts: `arch-renders/lab/phasing-intake/` (private).
- [Autodesk: phase filters](https://help.autodesk.com/cloudhelp/2024/ENU/RevitLT-GetStarted/files/GUID-FE4C8D4D-F51D-486F-81E9-53A530E833A2.htm) · [About phase filters (Show All)](https://help.autodesk.com/cloudhelp/2023/ENU/RevitLT-DocumentPresent/files/GUID-DB104358-4D5A-494E-ACAE-BB8B4E72E572.htm)
- [Autodesk: Revit exports only what the view shows](https://help.autodesk.com/cloudhelp/2023/ENU/Revit-DocumentPresent/files/GUID-7C4D89EF-01B9-490E-90CC-0CE96F496F12.htm)
- [Autodesk: Revit cameras after FBX export (crop region not carried)](https://download.autodesk.com/us/3dsmax/2012help/files/GUID-093F5CD7-02FF-4467-884E-B7A68A9D601-2784.htm)
- [Autodesk: 3D view properties](https://help.autodesk.com/cloudhelp/2023/ENU/Revit-DocumentPresent/files/GUID-5492CCEA-EDE1-4C2E-B828-6D7077465441.htm) · [Revit API: ViewOrientation3D](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/027b44d6-a473-4e99-4b43-c938847ea7e3.htm)
- [Blender: FBX import](https://docs.blender.org/api/latest/bpy.ops.import_scene.html) · [Blender license](https://www.blender.org/about/license/)
