---
title: "Revit Model Intake - FBX to Blender"
type: rd-report
brief: ""
reviewed: 2026-10-27
test_date: 2026-10-26
test_completed: 2026-10-26
status: complete
tools: [revit-fbx-intake, rvt-rs, fbx2gltf]
report_url: https://claude.ai/artifact/HkvSkRP5Zs1usbLUmQUu6D
clips:
  - env: "Route B: Revit FBX + material script"
    anchor: fbx-named
    file: still_fbx-named_cloud.jpg
  - env: "Route B without the script: Revit FBX as imported"
    anchor: fbx-raw
    file: still_fbx-raw_cloud.jpg
  - env: "Route A: rvt-rs GLB"
    anchor: rvtrs-glb
    file: still_rvtrs-glb_cloud.jpg
  - env: "Route C: FBX converted to GLB"
    anchor: fbx-to-glb
    file: ""
image: intake_compare.jpg
clips_home: "Published with the report at report_url (client model: stills are not stored in this repo)"
draft: false
---
# Revit Model Intake
## Revit 2025 FBX → Blender 5.2.2 (cloud) · rvt-rs 0.9

**Test problem:** Study which Revit export brings a building into Blender in the best shape to render, with the least cleanup.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-26 | 2026-10-26 | Complete |

**Rev history**
0. 2026-10-26 · Test plan (three routes)
1. 2026-10-27 · First draft report
2. 2026-10-27 · Approved; Route B adopted

Evidence key: **Tested** = we ran it and measured it · **Published** = from the maker's own documentation · **Assumed** = our judgment, not yet checked.

## 01 Tech description
**Model intake** is the step that gets an architect's 3D Revit model into Blender, the program that renders our stills and clips. Revit has no export that Blender reads cleanly, so this review tested three routes from two source files:
- **Route A: rvt-rs.** A free, open-source tool (Apache 2.0) that reads a Revit file (.rvt) without Revit and writes a GLB, an open 3D file format (Published). It runs in a web page or by script.
- **Route B: Revit's own FBX export.** FBX is Autodesk's 3D exchange format. Someone with Revit exports a 3D view; Blender opens it. A Claude-written script then reads the Revit material names from the file and builds Blender materials from them.
- **Route C: FBX converted to GLB** with a free converter (FBX2glTF) before Blender. Not run; see results.

### How it runs
- **Where it runs:** Blender in Claude's cloud workspace (Tested). Blender on Charles's PC was not reachable during the test (the chat wasn't linked) and stays untested. The FBX export needs a Revit seat (Assumed).
- **Subscription cost:** $0. Blender is free (GPL, fine for company use) (Published); rvt-rs is free (Published). Revit is already licensed by whoever exports.
- **Cost to run:** $0 (Tested).
- **How Claude controls it:** entirely by script, with no screen. Blender's official Python package installed in the cloud workspace in one step (Tested). rvt-rs could not be installed in the cloud (a safety check blocked running outside code), so Charles ran it in its browser page on his PC (Tested).
- **What it needs:** the FBX file dropped into chat or a shared folder. No graphics card for intake; renders here ran on the CPU.

## 02 Findings
Revit's own FBX export is the intake to use. It loads into Blender in about a second at the right size, upright, with the Revit camera, and with real doors, toilets, partitions, counters and window frames. It carries **no usable materials**: Blender drops them all. A Claude script fixes that by reading the 68 Revit material names inside the FBX and building a Blender material for each; 53 matched a rule and 341 of 353 elements came out with materials. rvt-rs needs no Revit at all, but it turns every door, fixture and piece of furniture into a plain box and leaves walls with no openings, so it can't beat the FBX for renders. Converting the FBX to GLB adds a step and nothing the FBX lacks. Route to adopt: Revit FBX into Blender plus the material script.

**Key numbers**
- **≈ 50×** · more surface detail in the FBX than the rvt-rs GLB (332,743 vs 6,712 faces) (Tested)
- **53 of 68** · Revit material names matched to a Blender material by the script (Tested)
- **≈ 1 s** · to load the FBX into Blender, at the right scale and upright (Tested)

### Inputs the workflow must supply
- An FBX export of one Revit 3D view, made by someone with Revit (5 minutes a project (Assumed)).
- That 3D view set up the way the render should start: the camera angle, and anything to leave out hidden.
- A material table that maps FA Wilhelm's Revit material names (for example "FAW - Aluminum Frame", "EG-Gypsum 5/8"") to finished Blender materials.

### Harness the Total Harness project needs to build
- An **intake step** in the arch-renders run: open the FBX in Blender by script, read the Revit material names, assign materials, fix the Revit camera, and save a Blender file for the render step.
- The **material table** above, growing as new Revit names appear; names it doesn't know go to a gray default and get listed for review.
- A **camera fix**: Revit's camera arrives unable to see anything closer than 95 m and carrying a stray animation. The script resets both (Tested).
- A **cutaway switch** that hides roofs, ceilings, joists and lights by Revit category.
- A **private home** for client models and their outputs, never the public repo.

## 03 Experiment parameters
We brought one real FA Wilhelm office buildout into Blender by each route and rendered it with the same camera, light and settings, to compare shapes, materials and cleanup. Only the intake route changed.

**Test input:** OfficeBuildout, an FA Wilhelm office interior (about 30 × 17 m, 6.5 m tall). Charles supplied an FBX of its "3D View 1" exported from Revit 2025 (6.6 MB), and a GLB he made from the .rvt in the rvt-rs browser page on his PC (0.5 MB).

**The test:** Open each file in Blender by script; count elements, detail and materials; render one still from Revit's own camera heading and one steep cutaway with roofs, ceilings, joists, lights and rooms hidden.

**Capabilities tested:**
- Geometry: element count and detail per category.
- Materials: how many arrive, and whether a script can rebuild them from Revit names.
- Scale, orientation and position on arrival.
- Revit camera carried into Blender.
- Revit data on each element (family, type, ID).
- Claude driving it all by script with no screen.

**Not tested:**
- **Blender on Charles's PC**: the chat wasn't linked to it.
- **Route C** (FBX to GLB): retired before running; it adds a step and nothing the FBX lacks.
- **Textures** (image-based finishes): neither file carries any, so they're the material table's job.
- **Large models**: one small interior only.
- **rvt-rs on a 2024 file**: its docs say families are boxes on every version (Published), so it wouldn't change the verdict.

**Output:** Stills at 1280×720, one per route per view, plus one comparison sheet.

**Settings:** Cycles on CPU, 48 samples, denoise on, AgX color, sky plus sun at 38°, gray ground plane. Same for every route.

**Machines and versions:** Claude's cloud workspace: 2-core CPU, no graphics card, Blender 5.2.2 LTS (Python package). rvt-rs browser page (built from its main branch; latest release 0.9.0, 2026-10-26) on Charles's PC. FBX written by Revit 2025.

**What we measured:**
- **Detail:** faces per element and in total, from Blender after import.
- **Materials:** count on arrival; names matched by the script; elements left gray.
- **Landing:** size, up direction and position against the other file.
- **Time:** import seconds and render seconds from the script's timer.

**Side checks:**
- The FBX keeps each element's Revit category, family, type and parameters (keynote, area, volume) (Tested).
- Both files place the building at the same spot, about 280 ft from the origin, and need recentering for cameras (Tested).
- The FBX's material records are Autodesk's own type, which Blender's importer skips; a small reader written for this test gets the names out (Tested).

**Saved test files:**
- **Scripts**, private, in `arch-renders/lab/revit-intake/`: `fbxread.py` (reads Revit's material records), `fbx_matnames.py` (element-to-material map), `blender_import.py` (import and report), `blender_render.py` (camera fix, cutaway, materials, render), and a README.
- **FBX and GLB**: Charles's originals, on his PC. They couldn't be pushed from the cloud session.
- **Stills**: on the published report page.

The script's permanent home is to be settled in the Total Harness project. Client model: never the public repo.

## 04 Results by test environment

### Route B: Revit FBX + material script
Blender 5.2.2 · cloud CPU · **Adopt now**
- **Still:** `still_fbx-named_cloud.jpg`, steep cutaway
- **Import:** ≈ 1 s, 353 elements, 332,743 faces (Tested)
- **Materials:** 341 of 353 elements given materials; 53 of 68 names matched a rule; 6 names fell to gray, including "toilet partition" and unnamed slots (Tested)
- **Render:** 55–79 s a still (cloud CPU)
- **Cost:** $0
- **Quality:** Real doors with frames, wall openings, toilets, partitions, counters, table and chairs. Starter materials read correctly (wood counters, black TVs, clear glass). Walls and gypsum stay near-white, which is right for this interior (Tested). Materials are simple color rules, not finished textures.
- **Verdict note:** Adopted 2026-10-27: Charles reviewed the stills and said he'd use it. The script is the key piece; where it lives for good is settled in the Total Harness project.

### Route B without the script: Revit FBX as imported
Blender 5.2.2 · cloud CPU · **Never (alone)**
- **Still:** `still_fbx-raw_cloud.jpg`, steep cutaway
- **Import:** ≈ 1 s, same geometry as above (Tested)
- **Materials:** None. All 353 elements arrive with no material (Tested)
- **Render:** 55–78 s a still
- **Cost:** $0
- **Quality:** Full detail, all white. Fine for a clay study, not a finished render.
- **Verdict note:** Always run with the material script. This would change if Blender's FBX importer learned to read Revit's material records.

### Route A: rvt-rs GLB
rvt-rs browser page (PC) → Blender 5.2.2 · cloud CPU · **Never**
- **Still:** `still_rvtrs-glb_cloud.jpg`, steep cutaway
- **Import:** < 1 s, 517 elements, 6,712 faces (Tested)
- **Materials:** 36 colors. Walls named by color code ("Layer f9f9f9"); most families named only by category ("Category IFCDOOR"). A few real names kept, such as FAW - Aluminum Frame (Tested)
- **Render:** 58–77 s a still
- **Cost:** $0, and no Revit needed
- **Quality:** Right layout and size. Every door, window, fixture, light, beam and piece of furniture is a box (12 triangles each); doors include their swing and stick out of walls; walls have no openings; rooms arrive as solid blocks that must be removed (Tested). One curtain wall name came out scrambled.
- **Verdict note:** Retired by Charles 2026-10-27: it can't improve on the FBX. Its docs say families are boxes on every Revit version (Published). This would change if rvt-rs builds real family shapes.

### Route C: FBX converted to GLB
FBX2glTF → Blender · **Never**
- **Still:** none. Retired before running.
- **Import:** Not run
- **Materials:** Expected to lose the same Revit materials (Assumed)
- **Cost:** $0. Converter is an unmaintained copy kept by the Godot project (Published)
- **Verdict note:** Retired by Charles 2026-10-27: it adds a conversion step and nothing the FBX doesn't already carry, since Blender opens FBX directly. This would change if Blender's FBX import broke on a future Revit export.

**Comparison image:** `intake_compare.jpg`. The same model, camera and light by each route. Top row: Revit's 3D View heading. Bottom row: steep cutaway. Left to right: rvt-rs GLB, FBX as imported, FBX with the material script.

## 05 Use cases
**Now**
- Interior and exterior stills of FA Wilhelm projects that already have a Revit model, with real fixtures and starter materials (Tested).
- Clay (all-white) studies straight from the FBX, with no material step (Tested).
- Cutaways that hide roofs, ceilings and structure by Revit category (Tested).
- Starting renders from the camera the designer set in Revit (Tested).

**Later**
- Finish-option swaps: change one Revit material name's mapping and re-render (Assumed).
- Phasing by Revit category or phase, which the FBX carries in its material and metadata records (Assumed).
- Material callouts labeled from the Revit material names (Assumed).

**Cannot**
- Bring in a model without someone exporting from Revit. rvt-rs does that, but only as boxes.
- Carry Revit's material colors or textures. The FBX only keeps names.

## 06 Requirements check (arch renders)
The arch-renders speed run takes a 2D plan set as its standard input. This intake adds a second door: when a Revit model exists, skip the plans-to-model step.

| Requirement | Answer | Path |
|---|---|---|
| 1. Conventions | Partly | Material callouts can use the Revit material names the FBX carries (Assumed). The Revit camera arrives as a starting angle (Tested); the standard camera set is the render step's job. |
| 2. Storyboard before motion | Not this tool's job | Intake hands a Blender file to the render step, which makes storyboard frames. |
| 3. Menu of motion pieces | Partly | Phasing and finish swaps can key off Revit categories and material names (Assumed). Motion itself is the render and motion steps' job. |
| 4. Graphics quality | Yes | Real fixtures, frames and openings from the FBX are the base for photo-like output (Tested). The finish quality depends on the material table, not built yet. |

## 07 Risks and cover
- **Needs a Revit seat for every export.** Cover: the architect or an FA Wilhelm designer exports; rvt-rs remains a massing-only fallback.
- **Starter materials are crude color rules.** Cover: build the material table with finished materials from the existing site kit.
- **Unnamed material slots (102 of them in this model) fall to gray.** Cover: list them after each intake for a one-time fix in the table (Tested) (the script already lists them).
- **Blender version gap.** Tested on 5.2.2 in the cloud; the PC runs 4.5. Cover: install 5.2 on the PC, as the flythrough review already recommends.
- **Large models may export very dense.** Cover: time the first big project's import before committing.
- **Client data.** Cover: models and outputs live only in private storage.

## 08 If adopted
- **What gets built:** the harness in Findings, built by the Total Harness project.
- **Dollars:** $0.
- **Charles's hours:** about 5 minutes a project to export the FBX, plus an hour once to review the first material table (Assumed).
- **Proof of done:** a new FA Wilhelm Revit FBX dropped in, and a Blender file with materials and the Revit camera produced unattended, rendered to a still Charles would use.

## 09 Sources
- No Discovery Brief: this review started from a question in chat.
- Test scripts: `arch-renders/lab/revit-intake/` (private), from the cloud runs of 2026-10-26.
- [rvt-rs documentation and support table](https://docs.rs/crate/rvt/latest)
- [OSArch: Revit to Blender, best format](https://community.osarch.org/discussion/123) · [Mai add-on: Revit FBX material values](https://superhivemarket.com/products/mai)
- [FBX2glTF (Godot copy, unmaintained)](https://github.com/godotengine/fbx2gltf)
- [Blender Python package (bpy)](https://pypi.org/project/bpy/) · [Blender license](https://www.blender.org/about/license/)
