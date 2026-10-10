# Build Brief — BB-2026-10-10-arch-massing-gate

**Build:** 33 (re-scoped 2026-10-10; replaces the three-look style study, BB-2026-10-10-arch-style-study)
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-10-arch-massing-gate.md`
**Project State plan:** `c716fa4c-67d8-48bb-b94d-7f5d7d4a9c71` on `total-harness`
**Skills:** orchestrate-build, project-folder
**Speed run:** arch-renders (record plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`; Working Doc https://claude.ai/code/artifact/864ebc78-392a-4840-bf64-bca83b03f76c)
**Harness slices:** block 7 (plan to white-box model), block 8 (overlay check), block 6 (separate checker), block 16 (the massing skill)
**After:** Build 34 (plan `6f66ec4e-f61a-4f8a-bedd-007fd6dabcf8`, landed): the Workflows tab, the start page and the `workflows` / `workflow_runs` tables.
**Target repos:** Chooch333/cbrain-ui (review branch) and Chooch333/arch-renders (created here) · **Overnight:** no (one review stop with Charles)
**Stack Flow:** no change (no new part runs on its own; the review screen and three tables sit inside cbrain)

**What this is:** Proves gate 2, the hardest gate: a 2D plan set becomes a white-box 3D model Charles can check by eye, and when something is wrong he pins it on the sheet or the model and Claude fixes it and shows version 2.

**What I'll do (build chat):** Add a run view to the Architectural renderings start page (traced plan over the sheet, white-box model to orbit, assumptions, pins, a Pass button). Then run one public sample through gate 1 and gate 2 from both its PDF and its DXF, post version 1, answer Charles's pins, post version 2, and write the steps down as a skill.

**What you'll do:** Open the run on the start page, look at the overlay and the model, drop a pin or two (or press Pass). About 10 minutes. Then look at version 2.

**Cost:** $0. One new screen dependency (`@google/model-viewer`, free). **Charles's time:** ~15 minutes.

---

## Current state going in

**Asked for** (Charles, 2026-10-10, frozen): "I think your finish line is wrong. Don't go straight to final output. … the first output of this workflow should be a check in 3d output from the 2d input. I should have a visual check of that step. Colors could be white box just to get massing. Think about how to solve this step because it's the hardest. There needs to be a method to review the output. If there is something wrong how can I communicate 'this aspect is wrong. See here in the plans'. Once this gate is done, then you can proceed to the materials gate." Approved re-scope of Build 33 to this gate: 2026-10-10 13:48. DWG is out (future add-on).

Verified 2026-10-10:
- [verified] Build 34 landed: `/harness?tab=workflows&wf=arch-renders` is the start page; run requests are rows in cbrain `workflow_runs` (status `requested`, `current_gate` 1). Code: `components/harness/workflows-tab.tsx`, `lib/workflow-model.ts`, `lib/db/workflows.ts`, routes under `app/api/workflows/[slug]/`.
- [verified] Cloud workspace: 2 processors, 7 GB, no graphics card. pip installs and runs `pymupdf` 1.28.2, `ezdxf` 1.4.4, `ifcopenshell` 0.9.0; `trimesh` 5.1.1 and `bpy` 5.2.2 are on pip. A Rust toolchain is present.
- [verified] npm has `@google/model-viewer` 4.4.0 (a web component with orbit, hotspots and a surface hit test) and `three` 0.186.1.
- [verified] The workspace cannot reach vercel.app (proxy refuses). The Vercel connector reads preview pages (GET only).
- [verified] Build 29.1: cloud sessions cannot git-clone private repos; use the GitHub connector for repo files.
- [verified] Charles's GitHub is not linked to this session type (`add_repo` refused), so a full local `next build` of cbrain-ui is not possible; Build 34 type-checked new files locally against the app's exact versions with stand-ins, then relied on the Vercel build. Do the same.
- [assumed] A usable public sample exists (see Directive 4 for the search order and fallbacks).
- [assumed] Wall-pair finding from flattened PDF linework works on a clean CAD export. This is what the build proves.

## Receiving chat

New build chat running orchestrate-build, in the daytime with Charles reachable for one review stop.

## Scope

**In scope**
1. **Three cbrain tables** (migration on `lpeswznkxzeeyiqaewma`, RLS on, no policies, like the others):
   - `workflow_assets` (id uuid, run_id → workflow_runs, gate int, version int, kind text: `sheet` | `overlay` | `model` | `side-check`, name, mime, bytes bytea, width, height, created_at). Max 8 MB per asset.
   - `workflow_pins` (id uuid, run_id, gate, version, target `sheet` | `model`, asset_id, x, y numeric (sheet: 0–1 of image width and height), point jsonb (model: [x,y,z] in metres), note text, status `open` | `answered` | `wont-fix`, answer text, answered_in_version int, created_at).
   - `workflow_gate_results` (run_id, gate, version, assumptions jsonb [{item, value, source sheet or "assumed"}], checks jsonb [{name, passed, detail}], status `under-review` | `passed`, passed_at).
2. **Run view** in cbrain-ui at `/harness?tab=workflows&wf=arch-renders&run=<id>`, opened by clicking a run on the start page:
   - Header: project name, current gate, version, status, back link.
   - **2D first:** the plan sheet image with the traced walls drawn over it in red (the overlay asset). Clicking it drops a pin at that spot.
   - **Then 3D:** the white-box model in `<model-viewer>` (orbit, zoom). Clicking the model drops a pin at the surface point it hits.
   - **Assumptions** table with the sheet each value came from, or "assumed"; **self-checks** with pass or fail.
   - **Pins** list: note, where, status, Claude's answer and the version that answered it. A note box per new pin; Save pin.
   - **Pass this gate** button: sets the gate result `passed`, the run's `current_gate` to 3 and its status to `in-progress`.
   - Assets served by a new route `GET /api/workflows/assets/[id]` (correct content type, private cache); pins by `POST /api/workflows/runs/[id]/pins`; pass by `POST /api/workflows/runs/[id]/pass`.
3. **The massing pipeline**, run in the cloud workspace on one sample, from both its PDF and its DXF:
   - Gate 1: sheet index (plans, elevations, sections, schedules), scale read from the scale note and checked against one dimension string.
   - Gate 2: walls, doors and windows traced; heights from elevations and sections; a white-box `.glb` with wall openings; the overlay image; a side view laid over one elevation.
   - Self-checks before Charles sees it: traced walls within 2% of the sheet's overall dimensions; every exterior wall closes; every opening sits in a wall; side view lines up with the elevation.
   - A fresh checker subagent (one that has not seen the build) grades the overlay and the model against the plan sheets and lists flaws; the builder fixes up to two rounds.
4. **One version-2 loop:** after Charles pins, Claude answers every pin (fix, or say why not), regenerates the assets as version 2, and marks each pin answered with that version.
5. **The massing skill draft:** `agent-library/skills/arch-massing/SKILL.md` (status draft): the gate 1 and gate 2 steps exactly as they worked, the checks, the tolerance, and what to do on a scanned set.
6. Repo `Chooch333/arch-renders` (private) from the project-folder template; the pipeline scripts live in `pipeline/`, the sample in `samples/`.

**Out of scope (forks pre-answered)**
- Materials, stills, motion (gates 3 and 4).
- DWG (future add-on). Scanned sets (the skill notes what to do; not built).
- Upload on the start page (Drive link only, unchanged).
- Anything that processes runs on its own schedule. The build chat runs this one sample by hand; the wake-up set comes later.
- Any FA Wilhelm or client drawing.

## Directive

1. Read live state: `get_plan` on this plan, on `37d9e5ef` and on `6f66ec4e`; read `lib/workflow-model.ts`, `lib/db/workflows.ts`, `components/harness/workflows-tab.tsx` on cbrain-ui `review`.
2. Migration (Supabase `apply_migration`, project `lpeswznkxzeeyiqaewma`): the three tables in Scope 1, with foreign keys to `workflow_runs`. Check with `list_tables` and `get_advisors`.
3. cbrain-ui (GitHub connector, branch `review`): extend `lib/workflow-model.ts` (asset, pin, gate-result types and parsers), `lib/db/workflows.ts` (reads and writes), the three routes in Scope 2, and the run view (new file `components/harness/workflow-run-view.tsx`; the start page's run rows link to it). Add `@google/model-viewer` to `package.json` and load it only on the client. Type-check locally against the app's exact versions with stand-ins (Build 34's method) before each push; push each prop change in the same commit as its caller. Wait for the Vercel deploy READY; read the preview with the Vercel connector.
4. **Find the sample** (30 minutes at most), in this order:
   a. A public-domain set with both a CAD-exported PDF and a DXF (US federal or state agency drawings are public domain), reachable from GitHub or by the GitHub connector.
   b. If only a PDF is found, write the DXF route test against a DXF the build makes from the same PDF's vector paths, and say so on the run.
   c. If nothing public fits, generate one: a small two-story building drawn as a DXF with named layers by script, exported to a vector PDF with plans and two elevations. Label it "generated sample" everywhere.
   A file outside GitHub goes through the laptop browser only with Charles's yes per download. Commit the sample to `arch-renders/samples/` with `SOURCE.md` (link, licence, how it was made).
5. Create the run: insert one `workflow_runs` row for the sample (project name "Sample: <name>", scope from the files), status `in-progress`.
6. Gate 1 in the workspace: sheet index and scale. Write the result to `workflow_gate_results` (gate 1, status `passed`, checks). Set `current_gate` 2.
7. Gate 2, PDF route: PyMuPDF paths from the plan page → wall pairs (parallel lines a wall's thickness apart) → Claude reads the rendered sheet image to confirm walls, doors, windows → heights from elevations → trimesh (or bpy) extrude, cut openings → `model.glb`. Overlay PNG (traced walls in red over the sheet at the sheet's own pixel size). Side-check PNG. **Three failed tries at the 2% check → stop with a diagnosis**: post it on the run (gate result checks) and in the Session Log; acceptance 5 to 8 become handed off.
8. Gate 2, DXF route: ezdxf layers → the same walls and openings → model. Compare the two routes' footprints and record the difference on the run. Show the better one as version 1 and say which route made it.
9. Checker subagent pass and up to two fix rounds. Then upload assets to `workflow_assets` (version 1) by `execute_sql` with `decode(..., 'base64')`; if a single statement is too large, split the asset into chunks in a temporary table and assemble with `string_agg` — record which worked. Write the gate-2 result (assumptions, checks, status `under-review`) and set the run status `waiting-on-charles`.
10. **Stop for Charles** (daytime): tell him in chat the run link and that it's ready for review. He pins or passes. If no response in 2 hours, hand acceptance 7 and 8 off to a draft Build 33.1 and finish the rest.
11. Read open pins (SQL). For each: fix the model or explain why not; regenerate assets as version 2; mark each pin `answered` with `answered_in_version` 2; status back to `waiting-on-charles`. If Charles passes after that, the run moves to gate 3.
12. Write `skills/arch-massing/SKILL.md` (draft) from what actually worked, including the route comparison and the failure cases met.
13. Close out per orchestrate-build: Session Log on total-harness with a "What to check" list, disclosures, done receipt. Update the Working Doc's Stage 4 tech-slot rows for "PDF linework to walls" and "White-box model" with the result.

## Acceptance

1. Three tables exist with foreign keys to `workflow_runs`; advisors show nothing new beyond info-level RLS notes.
2. The run view opens from the start page for a run; it shows the overlay, the model in an orbit viewer, assumptions, checks and pins; the deploy is READY and R&D, Build map and the start page work as before.
3. A pin saved on the sheet and one on the model are stored with their positions and notes (SQL read-back); Pass moves the run to gate 3.
4. A sample is in `arch-renders/samples/` with `SOURCE.md`; gate 1's sheet index and scale are recorded.
5. Version 1 assets (overlay, model, side check) are stored and served by the asset route; the 2% check passed, or a diagnosis was posted and the build stopped.
6. Both routes ran; the footprint difference between PDF and DXF is recorded.
7. Charles reviewed version 1 (pins or a pass), or this is handed off to Build 33.1.
8. Every pin has an answer and version 2 exists, or Charles passed version 1 with no pins.
9. `skills/arch-massing/SKILL.md` exists as a draft; Session Log, disclosures and the Working Doc update are done.

## Hard gates

- No money. A file download on the laptop needs Charles's yes per download.
- No client or FA Wilhelm drawings.
- Nothing deleted outside this build's own new rows.

## Completeness table

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered: proves gate 2 for Charles's eye | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: pipeline in the cloud workspace; screen in cbrain-ui on Vercel | Directive 3, 7–9 |
| 4 Data schema | Answered: three new tables | Scope 1 |
| 5 Storage & recall | Answered: assets as bytea in cbrain, served by route; recall by run id | Scope 1–2 |
| 6 Interconnectivity | Answered: GitHub connector, Supabase connector, Vercel connector | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered: orchestrate-build, project-folder; new skill arch-massing | Header, Directive 12 |
| 9 Sequence | Answered: tables → screen → sample → gate 1 → gate 2 → stop → version 2 → skill | Directive |
| 10 Assumptions & risks | Answered: sample availability; wall-pair finding; asset upload size | Current state, Directive 4, 9 |
| 11 Design intent | Answered | Below |

## Design intent

Charles judges this gate by eye, so what he sees must make errors obvious: the flat overlay first, because a wrong wall shows plainly on the plan, then the model. Every height and assumption names the sheet it came from or says "assumed". A pin is the whole way he talks to the build: where, plus a sentence; Claude answers every one, in writing, with the version that fixed it. Prefer exact geometry over looks; white is fine, wrong is not. Run both PDF and DXF on the same building so the comparison is honest, and say which route won. If tracing a PDF fails three times, stop and say why; that is a real result, not a failure of the build. Keep the screen consistent with the start page Build 34 made. Script first, connector second, screen last.

## Judgment calls made in scoping [Claude]
- Assets stored in a cbrain table, not Supabase Storage: this session has no storage upload tool and the service key never enters a cloud session (vault rule).
- `@google/model-viewer` for the 3D view (orbit and surface hit test built in). Ruled out: hand-written three.js (more code for the same result).
- Both PDF and DXF routes on one building, so DXF's promised advantage is measured, not assumed.
- The build runs the sample by hand; nothing consumes run requests automatically yet.
- Build number stays 33; the plan id stays `c716fa4c` with a new revision.
