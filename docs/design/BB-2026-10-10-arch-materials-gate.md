# Build Brief — BB-2026-10-10-arch-materials-gate

**Build:** 35
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-10-arch-materials-gate.md`
**Project State plan:** `da0d7a1a-9cd0-4539-b0eb-5ab6e99a8c21` on `total-harness`
**Skills:** orchestrate-build; reads `skills/arch-massing/SKILL.md` (Build 33's draft) for the run's files; writes `skills/arch-materials/SKILL.md`
**Speed run:** arch-renders (record plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`; Working Doc https://claude.ai/code/artifact/864ebc78-392a-4840-bf64-bca83b03f76c)
**Harness slices:** block 6 (separate checker plus fixer), block 8 (render checks), block 16 (the materials skill), block 17 (gate 3 rubric)
**After:** Build 33 (plan `c716fa4c-67d8-48bb-b94d-7f5d7d4a9c71`): the run view, the three asset/pin/result tables, and a sample run whose gate 2 passed with a `.glb` of named, typed parts.
**Target repos:** Chooch333/cbrain-ui (branch `review`) and Chooch333/arch-renders · **Overnight:** no (one review stop with Charles)
**Stack Flow:** no change (nothing new runs on its own; the screen and tables sit inside cbrain)

**What this is:** Proves gate 3. The passed white-box model gets real materials from the drawings and Charles's guidance, is rendered as plain-daylight stills from the three standard cameras, and Charles pins anything that is not the building he means. Claude answers every pin and shows version 2.

**What I'll do (build chat):** Build a starter material library, assign materials to the model's tagged parts from the drawing notes and the guidance, render three daylight stills plus a textured model to orbit, check them, post version 1, answer Charles's pins, post version 2, and write the steps down as a skill.

**What you'll do:** Open the run, look at three stills and the textured model, pin anything wrong ("this should be dark brick, see A-201 keynote 4") or press Pass. About 10 minutes, then a look at version 2.

**Cost:** $0. **Charles's time:** ~15 minutes.

---

## Current state going in

**Asked for** (Charles, 2026-10-10): "Scope the materials gate (gate 3) of the arch-renders speed run. Assume gate 2 passed: a white-box .glb with named, typed parts (Build 33, plan c716fa4c)." Gate 3 as approved on the use-case card: *you see* the same model with materials from your guidance (finish schedule, a named palette, or reference photos), in plain daylight; *it passes when* it reads as the building you mean; *when wrong*, pin and note, the same way as gate 2.

Verified 2026-10-10:
- [verified] Build 33 is running and has already created `workflow_assets`, `workflow_pins`, `workflow_gate_results` on cbrain (`lpeswznkxzeeyiqaewma`). Their checks allow asset kinds `sheet | overlay | model | side-check` only, pin targets `sheet | model` only, gates 1–4, assets ≤ 8 MB. Gate 3 needs new kinds and a new pin target (Scope 1).
- [verified] The workflow's stored conventions (cbrain `workflows`, slug `arch-renders`): camera set `aerial-34` (three-quarter aerial, front-left), `street` (eye level 1.6 m, ~30 m from the front), `entry` (eye level at the main entry); look "Photo-like, not photoreal. Soft late-morning daylight from the front-left. Muted site, no people in the foreground."; material callouts are a gate 4 matter.
- [verified, lab ✓✓] Blender (bpy 5.2.2 from pip) renders stills in the cloud workspace at 65–95 s each. 2 processors, 7 GB, no graphics card (rechecked today).
- [verified] The workspace cannot reach Poly Haven (api.polyhaven.com, dl.polyhaven.org) or ambientCG: connections refused. pip, npm and raw.githubusercontent.com answer. So no downloaded photo textures from the shell.
- [verified] `arch-renders` exists (README only so far; Build 33 fills it).
- [verified] No shelf row in the R&D Lab Notebook names gate 3. PhotoCraft (touch-up), EffectCraft (motion) and VectorCraft (phasing) belong to gate 4; FilmCraft and LightCraft stay shelved.
- [assumed] Blender's glTF exporter carries image textures (baked tiles) into the `.glb` so the orbit view matches the stills. Fallback in Directive 6.
- [assumed] Build 33's sample has some exterior material notes on its elevations. If it is the generated sample with none, Directive 4 says what to do.

## Receiving chat

New build chat running orchestrate-build, in the daytime with Charles reachable for one review stop.

## Scope

**In scope**
1. **Migration on cbrain** (`lpeswznkxzeeyiqaewma`):
   - `workflow_assets.kind` also allows `still`, `id-pass`, `material-tile`.
   - `workflow_pins.target` also allows `still`; a `still` pin needs `x`, `y` and `asset_id` (extend the coords check). New nullable `part text` on pins (the part name the pin resolved to).
   - `workflow_runs.guidance jsonb` (default `{}`): `{materials: {palette text, photosLink https, useDrawingNotes bool, updatedAt}}`.
2. **Material library** in `arch-renders/library/`: about 12 procedural Blender materials (face brick, CMU, board-formed concrete, smooth concrete, metal wall panel, standing-seam roof, membrane roof, asphalt shingle, stucco/EIFS, fiber-cement lap siding, wood, glass, aluminum frame), each baked once to a 1024 px tile of known real-world size. `materials.json`: name, aliases as they appear on drawings ("FACE BRICK", "BRICK VENEER", "MTL PNL", "ACM", "STOREFRONT"…), tile size in metres, base color, roughness, which part tags it may go on. Tints are applied per run, not baked.
3. **Assignment** per run: every part tag (plus facade for exterior walls) gets a material, a tint and a source: the sheet and keynote it came from, `palette`, `photo`, or `assumed`. Stored in the gate-3 result's `assumptions` (same shape as gate 2: item, value, source), so the run view's assumptions table shows it unchanged.
4. **Renders** (Blender Cycles on the processor, in the workspace): the three convention cameras at 1600×900, sun plus procedural sky matching the "look" convention, plain ground plane, no people or planting. Time cap 3 minutes a still. For each still, a flat part-ID image (one color per part) so a pin's pixel resolves to a part name. A textured `model.glb` (baked tiles) for the orbit view.
5. **Run view additions** (cbrain-ui `components/harness/workflow-run-view.tsx`):
   - Gate 3 panel: three stills side by side (click to enlarge; click a still to drop a pin, which stores x, y, asset and the part the ID image names), the textured model in the same orbit viewer (model pins as in gate 2), the assignment table, checks, pins with answers, Pass.
   - **Material guidance box**: palette text, a Drive link for reference photos, "use drawing notes" (on by default). It also appears beside gate 2's Pass button, so future runs give guidance in the same touch that passes massing. Saved by `POST /api/workflows/runs/[id]/guidance`.
   - Pass on gate 3 sets the result `passed`, `current_gate` 4, status `in-progress`.
6. **Checks before Charles sees it** (script): every part has a non-default material; no missing-texture color anywhere in a still; under 2% of pixels clipped to white or black; every material's tile size matches the library; glazing parts show sky or interior, not opaque; each still renders under the time cap. Then a **fresh checker subagent** (has not seen the build) compares the stills to the elevations, the drawing notes and the guidance, and lists mismatches; the builder fixes, two rounds at most.
7. **One version-2 loop** after Charles pins, as in gate 2.
8. **Reference-photo route, run once:** one public-domain building photo from a GitHub-hosted source; Claude reads it, maps what it sees to library materials and tints, and records the mapping in the skill. Not shown to Charles as a version.
9. **The materials skill draft:** `agent-library/skills/arch-materials/SKILL.md` (status draft): guidance order, the library, assignment, cameras and settings that worked, the checks, the ID-pass pin method, render times.

**Out of scope (forks pre-answered)**
- Photo-like finish, AI passes, touch-up, motion, callouts, titles: gate 4.
- The three-look comparison (browser scene, Blender, AI finish). It moves to gate 4, where "photo-like" is the test; gate 3 only asks whether the materials are right.
- Downloaded photo textures (sites unreachable from the shell). Revisit at gate 4 if procedural tiles look too plain.
- Landscaping, site context, entourage.
- Processing runs on a schedule. The build chat runs the sample by hand.
- Any FA Wilhelm or client drawing.

## Directive

1. Read live state: `get_plan` on this plan, on `c716fa4c` (Build 33's executor report and fork log) and on `37d9e5ef`; `skills/arch-massing/SKILL.md`; the run Build 33 used (SQL on `workflow_runs`, `workflow_gate_results`, `workflow_assets`). Confirm gate 2 is `passed` and the `.glb` has separate typed parts (read it with trimesh). If gate 2 is not passed, stop: post a blocking question bound to this plan and end.
2. Migration (Supabase `apply_migration`) per Scope 1. Check with `list_tables` and `get_advisors`.
3. Library: install bpy 5.2.2; build the procedural materials, bake each to a tile, write `materials.json`; commit to `arch-renders/library/` through the GitHub connector.
4. Guidance for the sample: read material notes from the elevations (keynotes, tags, legends) and the finish schedule if there is one; map each note to a library alias. Anything not noted gets a labelled assumed default ("assumed: light gray metal panel"). If the sample has no material notes at all, write a short test palette yourself, store it as the run's guidance with "test palette by Claude" in the text, and say so on the run. Do not ask Charles for guidance first; his pins correct it.
5. Assign, then render the three stills and their ID images (Scope 4). Record seconds per still.
6. Export the textured `model.glb`. If the baked textures do not survive export (open the file and check for images), export with flat base colors only and say so on the run.
7. Script checks (Scope 6). Three failed tries at one check → stop with a diagnosis on the run and in the Session Log; acceptance 6 to 8 become handed off.
8. Checker subagent and up to two fix rounds.
9. cbrain-ui (GitHub connector, branch `review`): the gate 3 panel, guidance box (both places), the guidance route; extend `lib/workflow-model.ts` for the new kinds, the `still` target and guidance. Type-check locally with stand-ins (Build 34's method), push each prop change with its caller, wait for Vercel READY, read the preview with the Vercel connector.
10. Upload version 1 assets (stills, ID images, textured model) to `workflow_assets` gate 3 by `execute_sql`, using whichever upload method Build 33 recorded as working. Write the gate-3 result (assignment as assumptions, checks, `under-review`); run status `waiting-on-charles`.
11. **Stop for Charles** (daytime): the run link in chat, ready for review. No response in 2 hours → hand acceptance 6 and 7 off to a draft Build 35.1 and finish the rest.
12. Read open pins. For each: change the assignment or explain why not; re-render as version 2; mark each pin `answered` with `answered_in_version` 2; status back to `waiting-on-charles`.
13. Reference-photo route (Scope 8): 15 minutes at most to find a public-domain photo on GitHub; none found → record that and hand it off.
14. Write `skills/arch-materials/SKILL.md` (draft) from what actually worked.
15. Close out per orchestrate-build: Session Log on total-harness with a "What to check" list, disclosures, done receipt. Update the Working Doc: Stage 4 tech-slot row "Look at the materials gate" with the result, and the build-order line for the materials gate.

## Acceptance

1. Migration applied; new kinds, `still` pins, `part` and `guidance` exist; advisors show nothing new beyond info-level RLS notes.
2. Library committed: tiles plus `materials.json`, each material with aliases and tile size.
3. Every part of the sample model has an assigned material with a source (sheet and note, palette, photo, or assumed).
4. Three stills at 1600×900 from the convention cameras, each under 3 minutes, with matching ID images; seconds per still recorded.
5. All script checks pass and the checker subagent's report is filed with the fix rounds used (≤2); or a three-try diagnosis was posted and the build stopped.
6. The run view shows the gate 3 panel; a pin on a still stores x, y, asset and the resolved part (SQL read-back); a model pin stores its point; Pass moves the run to gate 4; the guidance box saves; deploy READY and the start page, gate 2 view, R&D and Build map work as before.
7. Charles reviewed version 1 (pins or a pass), or this is handed off to Build 35.1.
8. Every pin answered and version 2 exists, or Charles passed version 1 with no pins.
9. Reference-photo route ran once with its mapping recorded, or handed off.
10. `skills/arch-materials/SKILL.md` exists as a draft; Session Log, disclosures and the Working Doc update are done.

## Hard gates

- No money.
- No client or FA Wilhelm drawings; the sample only.
- Nothing deleted outside this build's own new rows.

## Rubric (block 17 slice; the checker grades 1 to 5)

Each part carries the material the drawings or guidance call for · tints read as the named colors · material scale is believable (brick courses, panel joints, seam spacing) · glazing reads as glass · daylight is even with no blown-out or black areas · geometry is unchanged from the passed gate 2 model. A score below 3 on the first item fails the still regardless of the rest.

## Completeness table

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered: proves gate 3 for Charles's eye | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: Blender in the cloud workspace; screen in cbrain-ui on Vercel | Directive 3–9 |
| 4 Data schema | Answered: three check widenings, two new columns | Scope 1 |
| 5 Storage & recall | Answered: assets in cbrain by run and gate; library in the repo | Scope 1–2 |
| 6 Interconnectivity | Answered: GitHub, Supabase, Vercel connectors | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered: orchestrate-build, arch-massing (read), arch-materials (new) | Header, Directive 14 |
| 9 Sequence | Answered: confirm gate 2 → tables → library → assign → render → checks → screen → stop → version 2 → skill | Directive |
| 10 Assumptions & risks | Answered: textures through glTF; sample may lack notes; render time on 2 processors | Current state, Directive 4, 6 |
| 11 Design intent | Answered | Below |

## Design intent

Gate 3 answers one question: is this the building Charles means? Material truth beats beauty here; a plain still with the right brick passes, a lovely still with the wrong cladding fails. Every material says where it came from, the same way gate 2's heights did, so a wrong guess is easy to spot and pin. The orbit model and the stills use the same tiles so what Charles turns around is what he will get. Pins on a still must land on a named part, so "this should be darker" needs no back-and-forth about which wall. Keep the screen consistent with gate 2. Script first, connector second, screen last.

## Judgment calls made in scoping [Claude]
- Blender in the cloud is the only renderer. Ruled out: the browser scene (needs the laptop awake; capture untested) and an AI pass (money and the client-drawings rule; belongs to gate 4).
- The parked three-look comparison moves from gate 3 to gate 4 (the Working Doc had it returning here). Gate 3's pass test is material correctness, which the comparison does not decide.
- Procedural materials baked to tiles. Ruled out: downloaded photo textures, because the texture sites are unreachable from the workspace (checked today).
- Exterior materials read from elevation notes first; finish schedules are mostly interiors.
- Guidance is not asked for up front on this run; the box joins gate 2's Pass for future runs, so gate 3 adds no extra touch.
- Review stills at 1600×900, not full size: this gate judges materials, and it keeps renders near the measured 65–95 s.
- Build number 35 (33 and 34 used).
