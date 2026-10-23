---
name: arch-massing
version: 0.2.0
status: draft
triggers: [used by builds when an arch-renders run reaches gate 1 or gate 2 (plan set -> white-box massing model); no chat trigger]
dependencies: [project-folder, execute-build-task]
owner: Charles
updated: 2026-10-10
wiring:
  runs: inside-builds
  reads: [plan set (vector PDF + DXF), Chooch333/arch-renders pipeline, cbrain workflow_runs]
  writes: [arch-renders outputs/, cbrain workflow_gate_results, cbrain workflow_assets]
  stack: [total-harness]
  origin: yours
  label: Massing gate
---

# Massing gate

Turns a 2D plan set into a white-box 3D model Charles can check against the sheets. Gate 1 reads the sheet index and scale. Gate 2 builds the model, with openings, and every part named and typed.

## Default reader: the takeoff (Build 35)
- On the Pascal route (skill `arch-renders-run`) the sheets are read into a **takeoff**: `arch-renders/pipeline/pascal/takeoff.schema.json`. Every number is `{v, src}` with the sheet it came from, or `src: "assumed"`; finishes map to material library slugs with their sheet.
- A fresh checker agent grades the takeoff against the sheets, at most two fix rounds. `generate.mjs` turns it into the Pascal scene.
- **The tracer below (PDF and DXF routes) is the backup**: use it when the takeoff checker can't settle a dimension, or to cross-check overall sizes and wall counts.
- The sheets stay on Drive; read them through the Google Drive connector and never commit them.

This page records what actually worked on Build 33. The code is in `Chooch333/arch-renders/pipeline` (its README has run commands and file roles).

## Inputs
- One folder holding a vector PDF of the set. A DXF per sheet of the same set is optional; with it, both routes run.
- Sheets needed: one floor plan per level, an exterior elevation (south used for the side check), and a building section.
- A run row in cbrain `workflow_runs` (workflow_slug `arch-renders`). Only ever touch rows for that run id.
- Never give the pipeline an answer key. A grading file (for example `truth.json`) is for the independent checker only.

## Gate 1: sheet index and scale
1. Sheet index: for each page, read the sheet number and title from the title block. Classify it as plan, elevation, section or schedule from the title.
2. Scale: find every `SCALE: ...` note on the page and parse it (1/4" = 1'-0" gives a ratio of 48). Every note on a sheet must agree.
3. Scale check: on the first plan, take the longest dimension string in each direction. Measure the distance between its extension lines in PDF points, convert with the parsed scale, and compare it to the string's text. The sample measured 30'-0" and 24'-0" with 0 in error.
4. Write `gate1-result.json` and a `workflow_gate_results` row (gate 1).

## Gate 2: PDF route, step by step
1. Wall linework: take the heaviest stroke weight whose axis-aligned lines form at least 4 wall-thickness pairs. Do not trust layer names or colours in a PDF.
2. Wall thickness: find face pairs, meaning parallel lines 2 to 18 in apart that overlap and are mutually nearest. The thicknesses come from the data (8 in exterior and 4.5 in interior on the sample). Merge the pairs into runs.
3. Openings: classify each gap in a run.
   - A gap with an arc or a perpendicular leaf line is a door.
   - A gap with thin parallel glass lines is a window.
   - Anything else splits the run.
   - Measure from the linework inside each rough opening: jamb width, leaf length and thickness, and glass spacing.
4. Join corners and T-junctions. Runs with a face on the outer ring of the wall union are exterior.
5. Confirm by looking: render every sheet at 100 dpi (`sheet-*.png`) and look at the trace over it before trusting any number.
6. Heights: read them from the elevation and section. Record the sheet as the source for every value.
   - Level markers: use the circle-and-cross symbol's centre as the datum line, not a nearby stroke.
   - Slab and assembly thicknesses: from the section's cut geometry.
   - Sill, head and door heights: from the general notes, cross-checked against the elevation.
   - Head and sill frame depths: from the elevation insets.
   - Anything not drawn is tagged `assumed`.
7. North arrow to facades: read the arrow's rotation on the plan. Rotate plan coordinates so north is up, and set each exterior wall's facade from its outward normal.
8. Model builder (box split, no booleans):
   - Split each wall into piers, sills and headers around its openings.
   - Add parapets, slabs, roof, glass panes, door leaves and frames.
   - Trim frame heads and sills between the jambs so no boxes overlap.
   - Export glTF in metres, Y up, X east, Z south, with the origin at the SW outside corner of level 1.
9. Part naming and extras:
   - Every element is its own node and mesh. Names look like `exterior-wall.south.L1`, `exterior-wall.south.L2-parapet`, `interior-wall.L1.01`, `glazing.W-S1.L1`, `door.D101`, `opening-frame.W-S1.L1`, `slab.L2`, `roof`.
   - Node and mesh carry identical extras:
     - every part: `type`, `level`, `source`;
     - exterior walls: `facade`, plus `part` = `storey` or `parapet`. Parapets have level `PARAPET`;
     - glazing, door and frame parts: `host` (the host wall's node name), plus `facade` only when the host is an exterior wall;
     - measured sizes with the sheet each came from.
10. Overlay (`overlay.png`):
    - Crop the drawing area of each plan render at its own pixel scale (never resized) and place the panels side by side.
    - Draw the traced wall outline in red, outline only: the boundary of the wall union, with no lines across butt joints or T-junctions. Draw traced openings in blue.
    - Labels are part ids without the type prefix (`W-S1.L1`, `D101`). Each must be unique, and is placed where no ink and no other label lies within 5 px.
    - Write `overlay-map.json` so a pin at (x, y) maps back to sheet, plan feet and building feet.
11. Side check (`side-check.png`):
    - Project the model's south view using exterior-wall parts only, clipped at grade (LEVEL 1).
    - Draw it in red over the south elevation crop at the same scale.
    - Compare the outline, every opening edge and the level lines.

## Gate 2: DXF route
- It has the same structure and the same tracer (`ir.py`) and model builder (`model.py`), but reads by layer: `A-WALL`, `A-DOOR`, `A-GLAZ`, `A-ANNO-DIMS`, `A-ANNO-LEVL`, `A-ELEV-OTLN`, `A-SECT-MCUT`.
- Its own renderer draws at 25 px/ft for its overlay and side check.
- It also reads the elevation frame insets for head, sill and jamb.

## Route comparison and the tie rule
- Run both routes, then compare footprint, wall count, openings, wall centreline offsets and every height.
- On the sample they were identical:
  - 30x24 ft footprint (720 sf);
  - 4 exterior and 2 interior walls per floor;
  - 6 windows and 4 doors on L1, 8 windows and 2 doors on L2;
  - wall centrelines 0 in apart, all heights equal;
  - both passed 8/8 checks.
- Choose the route with more checks passed, then the smaller dimension error, then the smaller side-check offset.
- On a full tie, use the PDF route, because most real sets arrive as PDF.

## Self-checks (gate 2)
1. Overall size: traced overall dimensions within 2% of the overall dimension strings, in both directions, on every floor.
   - 1b: every dimension string agrees with the trace within 1/2 in.
2. Every exterior wall loop closes, with a corner gap of 1 in or less, and the solid union is one ring.
3. Every opening sits inside its host wall, in plan and by 3D bounds.
   - 3b: no two boxes overlap inside any one part.
4. Side view lines up with the south elevation within 2 in at full size: outline, every opening edge, level lines.
5. Parts check: read the .glb back with pygltflib.
   - Every node is typed, and all 7 types are present.
   - Every exterior wall has a facade.
   - Each opening part names an existing host, and its facade matches the host's.
   - Part and level are consistent, and node and mesh extras are identical.
6. Overlay labels are unique, with no ink and no other label within 5 px.

Retry rule: the PDF route gets up to 3 tries at check 1. Each try changes only tracer settings:
- try 1: defaults;
- try 2: corner join gap 0.5 ft;
- try 3: thickness search up to 24 in, minimum overlap 1 in.

The check's 2% tolerance never changes. After three failures, stop, record the tries and "2% check failed three times", and report. The sample passed on try 1.

## Independent checker loop
- A separate agent grades the outputs against the answer key. The answer key is grading-only: the pipeline, its routes and its checks never open it.
- The builder does not grade itself.
- Fix what the checker flags, re-run, and send it back. On Build 33:
  - Round 1: geometry exact against the answer key; 7 labelling and tidiness flaws.
  - Round 2: all fixed; ready for review.

## Posting assets to cbrain
- Rows go into `workflow_assets` (overlay, model, side-check; bytea) and `workflow_gate_results` (assumptions `[{item, value, source}]` where source is a sheet or exactly `assumed`, and checks `[{name, passed, detail}]` with short plain details).
- Then set the run to `waiting-on-charles`.
- What failed:
  - One `decode('<base64>','base64')` statement per asset was too large for execute_sql.
  - A temp table plus string_agg does not work, because each execute_sql call is its own session.
- What worked: md5-guarded chunked appends.
  - Insert the first chunk, then append the rest: `update ... set bytes = bytes || <chunk> where id=... and run_id=... and octet_length(bytes)=<expected> and md5(<chunk>)='<local md5>' returning octet_length(bytes), md5(bytes)`.
  - Check every returned md5 against the local prefix. A bad chunk updates nothing.
  - At the end, compare `encode(sha256(bytes),'hex')` with local `sha256sum`.
- This is a stopgap. It is slow and copy-error-prone. A run that posts its own files (storage upload or a server-side script) should replace it.

## Failures met, and their fixes
| failure | fix |
|---|---|
| Slab on grade showed below grade in the side view | Clip the model view at grade (LEVEL 1) before comparing. |
| Glazing and doors filled the opening holes in the side view | Project exterior-wall parts only. |
| Faces drew in the wrong order in the 3D previews | Put every face in one collection so matplotlib depth-sorts them together. |
| Overlay labels collided with dimension text | Place labels only where no ink or label lies within 5 px (check 6). |
| Red lines crossed butt joints and T-junctions in the overlay | Draw the wall union's outline, not each wall's rectangle. |
| Frame boxes overlapped at the corners | Trim heads and sills between the jambs (check 3b). |
| Door frame sizes were assumed | Measure jamb, leaf and glass from plan linework and head/sill from elevation insets. Only the interior door head (not drawn in elevation) stays `assumed` (= measured jamb). |

## Limits
- Orthogonal walls only. Single-swing doors and simple windows only. Flat roof inside the exterior walls. The side check uses the south elevation only.
- Proven only on one generated, clean set (Build 33). Not yet run on a real public set.

## Scanned sets (not built)
If the PDF has no vector linework (scanned or raster pages):
- Stop at gate 1.
- Report: "scanned — needs vector PDF/DXF/IFC or a tracing pass".
- Do not guess walls.

## Stop rule
Three failures at the same step (a check, an upload, a route) means stop. Write what was tried and what failed, and report it. Do not keep retrying or relax a tolerance to get a pass.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the building's name + "massing", e.g. "Sample duplex massing"
- Opens when: a gate stops on the stop rule or a scanned set, or the run is set to `waiting-on-charles` for him to check the model
- Checks in: when a run leaves something open (thread_key "job:arch-massing-<run slug>")
- Closes when: Charles passes gate 2 on the run, or clicks Done

## Changelog
- 0.2.1 (2026-10-23) — Progress tracking section. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 (2026-10-12) — Build 35: the takeoff is the default reader, the tracer is the backup. Draft until Build 35.1 reads a real set into a takeoff.
- 0.1.0 — First version (Build 33, massing gate)
