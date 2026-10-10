# Build Brief — BB-2026-10-10-arch-materials-gate

**Build:** 35 (revised 2026-10-10 15:10 on Charles's direction: browser route, a materials library with its own screen, a site and background kit, and an arch-viz expertise skill)
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-10-arch-materials-gate.md`
**Project State plan:** `da0d7a1a-9cd0-4539-b0eb-5ab6e99a8c21` on `total-harness`
**Skills:** orchestrate-build, deep-research (phase A); reads `skills/arch-massing/SKILL.md` (Build 33's draft); writes `skills/arch-viz/SKILL.md` and `skills/arch-materials/SKILL.md`
**Speed run:** arch-renders (record plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`; Working Doc https://claude.ai/code/artifact/864ebc78-392a-4840-bf64-bca83b03f76c)
**Harness slices:** block 6 (separate checker plus fixer), block 8 (render checks), block 16 (the two skills), block 17 (gate 3 rubric)
**After:** Build 33 (plan `c716fa4c-67d8-48bb-b94d-7f5d7d4a9c71`): the run view, the asset/pin/result tables, and a sample run whose gate 2 passed with a `.glb` of named, typed parts.
**Target repos:** Chooch333/cbrain-ui (branch `review`), Chooch333/arch-renders, Chooch333/agent-library (skills) · **Overnight:** no (one review stop with Charles)
**Stack Flow:** no change (nothing new runs on its own; the screens and tables sit inside cbrain)

**What this is:** Proves gate 3. The passed white-box model gets real materials and a real site (sky, ground, trees) in one 3D scene that runs in the browser. Charles turns it around and swaps materials live on the run page; the cloud captures the standard stills from the same scene. A materials library has its own screen. The craft of making an architectural view look right is researched first and written down as a skill, which the checker grades against.

**What I'll do (build chat):** Research arch-viz craft into a skill; build the scene (materials, sky, ground, trees, cameras); build the materials library screen; run the sample through gate 3; post version 1; answer Charles's pins and material swaps; post version 2; write down the steps.

**What you'll do:** Open the run, look at three stills and the live 3D scene, swap any material from the library or pin what is wrong, or press Pass. About 15 minutes, then a look at version 2. Optional: browse and edit the materials library.

**Cost:** $0. **Charles's time:** ~20 minutes.

---

## Current state going in

**Asked for** (Charles, 2026-10-10 14:43): scope gate 3, assuming gate 2 passed with a `.glb` of named, typed parts. **Then (15:04):** "wasn't there some guidance from the lab about being able to do all rendering in browser · I want there to be a materials library with interface · for exterior shots there needs to be some thought about the background — sky, trees, etc. · I want there to be an expertise acquired and maybe stored in a skill that knows how to do this."

Gate 3 as approved on the use-case card: *you see* the model with materials from your guidance (finish schedule, a named palette, or reference photos), in plain daylight; *it passes when* it reads as the building you mean; *when wrong*, pin and note.

Lab guidance (R&D notebook, Handoff tab and "Rendering techniques" doc, 2026-10-09): the strongest pairing is a browser building page Claude codes with Three.js; it doubles as the explorable building page and can carry finish-swap buttons, which Blender cannot. Its blocker was "cannot render the browser page in the cloud workspace" (headless browser installers blocked); fallback was the PC's Chrome. Blender was the hero-still route.

Verified 2026-10-10:
- [verified ✓✓ today] **The blocker is gone.** A headless Chrome that ships inside an npm package (`@sparticuz/chromium` with `puppeteer-core`) installs and runs in the cloud workspace with software 3D (SwiftShader). A Three.js 0.186 test scene (brick box, glass, sky, sun shadows, five trees) rendered to a 1600×900 PNG in 12–16 s end to end, about 1–2 s of drawing. Test files: `arch-renders/lab/browser-test/` (scene.html, shot.mjs).
- [verified ✓✓ today] Realistic procedural trees: `@dgreenheck/ez-tree` 1.1.0 (MIT, npm; oak and ash presets, bark and leaf images built in) rendered in that scene with leaf shadows on the wall. Its textures load a few seconds after the scene starts, so a still must wait for them (the first try rendered black, leafless trees).
- [verified] raw.githubusercontent.com is reachable (a texture file in the three.js repo answered 200), so permissively licensed photo textures hosted on GitHub are usable; Poly Haven and ambientCG are not reachable from the shell.
- [verified] Build 33's tables on cbrain (`lpeswznkxzeeyiqaewma`) allow asset kinds `sheet | overlay | model | side-check` and pin targets `sheet | model` only; gate 3 widens them (Scope 6).
- [verified] Workflow conventions (cbrain `workflows`, slug `arch-renders`): cameras `aerial-34`, `street` (eye level 1.6 m, ~30 m out), `entry`; look "Photo-like, not photoreal. Soft late-morning daylight from the front-left. Muted site, no people in the foreground."
- [verified] The run view already shows models in the browser with `@google/model-viewer` (Build 33).
- [verified] No R&D shelf row names gate 3 (PhotoCraft, EffectCraft, VectorCraft belong to gate 4).
- [assumed] The test scene's look is a floor, not a ceiling: it had flat ground, no soft shadow filtering and poor tree placement. Phase A's skill and the checker are what raise it.
- [assumed] A three.js scene can show the gate-2 `.glb` with materials swapped per named part in Charles's phone browser at a usable frame rate.

## Receiving chat

New build chat running orchestrate-build, in the daytime with Charles reachable for one review stop.

## Scope

**In scope**

**Phase A — the expertise (before anything is built)**
1. **`agent-library/skills/arch-viz/SKILL.md`** (draft): how a good architectural exterior view is made, as rules a script or a checker can test. Researched with the deep-research skill from practitioner sources (arch-viz studios' guides, Blender and three.js documentation, photography of buildings), every rule sourced. Sections:
   - *Camera:* eye height, focal lengths that suit buildings, vertical lines kept vertical (two-point perspective / lens shift), how much sky and ground in frame, where the building sits in frame.
   - *Light:* sun height and direction for a readable facade, sun placed from the site's location and date, sky and haze, shadow softness, exposure.
   - *Materials:* real-world scale (brick courses, panel joints, seam spacing), roughness, how glass should read (reflection vs. seeing in), common tells of fake materials.
   - *Site and background:* ground (lawn, paving, curb, walks), trees (species mix, size against the building, framing without hiding the entry or more than a set share of the facade), a distant tree line or horizon, season, what to leave out (people in the foreground, per convention).
   - *Failure list:* the ten most common reasons an exterior render looks fake, each with a check.
   - A one-page *rubric* the checker uses (Scope 9).

**Phase B — the scene, the library, the site**
2. **One browser scene** (`arch-renders/scene/`, Three.js 0.186, plain files, no build step): loads the gate-2 `.glb`; applies materials per named part; sky with the sun placed from the run's location, date and time; ground and site; EZ-Tree trees; the convention cameras; and a `still` mode that waits for every texture and tree to load before drawing. The same files run two ways:
   - **live** in the run view (orbit, swap materials, toggle trees), and
   - **headless** in the cloud workspace (`@sparticuz/chromium` + `puppeteer-core`, pinned) to capture stills and part-ID images.
3. **Materials library** — the data in a new cbrain table `materials` (shared by every run): slug, name, category (masonry, concrete, metal, cladding, roofing, glazing, wood, paving, ground), aliases as drawings write them ("FACE BRICK", "MTL PNL", "ACM", "STOREFRONT"…), real-world tile size, base color, roughness, metalness, texture source (`procedural` with its parameters, or `image` with URL and licence), allowed part tags, notes, updated_at. Seeded with about 15 materials: face brick, CMU, board-formed and smooth concrete, metal wall panel, ACM, standing-seam roof, membrane roof, asphalt shingle, stucco/EIFS, fiber-cement lap siding, wood, storefront glass, aluminum frame, concrete paving, lawn. Procedural textures are drawn in code from their parameters; image textures only from GitHub-hosted sources with a recorded permissive licence.
4. **Materials library screen** (cbrain-ui, a "Materials" view on the Workflows tab, `?tab=workflows&view=materials`): a grid of swatches, each shown live on a small wall sample at true scale under the scene's daylight; filter by category; open one to edit name, aliases, size, tint, roughness and notes, and save; duplicate one to make a variant ("dark iron-spot brick"). Routes `GET/POST /api/workflows/materials`. Edits apply to the next render of any run.
5. **Site and background kit** (per run, stored in `workflow_runs.guidance.site`, editable on the run page): time of day and date (default: late morning, front-left light, per convention); ground (lawn, with paving, walks and a curb taken from the site plan if gate 1 found one, else a simple apron); trees (preset mix, density, season); distant tree line or open horizon; haze. Placement follows the arch-viz rules: trees frame the building, never stand in front of the main entry, and never cover more than the skill's set share of any camera's facade.
6. **Migration on cbrain:** the `materials` table (RLS on, no policies, like the others); asset kinds add `still`, `id-pass`, `scene-config`; pin target adds `still` (needs `x`, `y`, `asset_id`) with a nullable `part` column; `workflow_runs.guidance jsonb` (default `{}`) holding `materials` (palette text, photos link, use-drawing-notes, and per-part picks) and `site`.

**Phase C — the gate on the sample**
7. **Assignment:** every part tag (plus facade for exterior walls) gets a library material and a tint, with a source: the sheet and note it came from, `palette`, `photo`, `picked on the page`, or `assumed`. Stored as the gate-3 result's assumptions, as gate 2 did.
8. **Run view, gate 3 panel** (`components/harness/workflow-run-view.tsx`): three stills (click to enlarge; click to pin, resolved to a part by the ID image); the **live scene** (orbit; tap a part to see its material and source, or pick another from the library, which saves to the run's guidance); the site settings; the assignment table, checks, pins with answers; Pass (result `passed`, `current_gate` 4, status `in-progress`). The material-guidance box also appears beside gate 2's Pass button, so future runs give guidance in the same touch that passes massing.
9. **Checks before Charles sees it:** script checks: every part has a library material; no missing textures; trees and textures fully loaded before capture; under 2% of pixels clipped; vertical edges within 0.5° of vertical in every still; material tile sizes match the library; no tree covers the entry or more than the set share of a facade (from the ID image). Then a **fresh checker subagent** (has not seen the build) grades each still against the arch-viz rubric and the drawings and lists flaws; the builder fixes, two rounds at most.
10. **One version-2 loop:** after Charles's pins and swaps, answer every pin, regenerate stills and scene as version 2, mark pins answered.
11. **Reference-photo route, run once** on one permissively licensed building photo from GitHub: Claude maps what it sees to library materials and tints; recorded, not shown as a version.
12. **`skills/arch-materials/SKILL.md`** (draft): the gate-3 procedure as it actually worked (guidance order, assignment, scene, capture, checks, render times). The arch-viz skill gets a "held / didn't hold on the sample" note per rule.

**Out of scope (forks pre-answered)**
- Photo-like finish passes beyond the basics (soft-shadow filtering, ambient occlusion, color grade), AI passes, touch-up, motion, callouts, titles: gate 4.
- The Blender comparison: gate 4, against this scene's stills, for hero shots only if the browser stills fall short.
- People, cars and street furniture.
- Uploading textures from the library screen (Drive link or GitHub source for now).
- Processing runs on a schedule. The build chat runs the sample by hand.
- Any FA Wilhelm or client drawing.

## Directive

1. Read live state: `get_plan` on this plan, on `c716fa4c` (Build 33's executor report and fork log) and on `37d9e5ef`; `skills/arch-massing/SKILL.md`; the sample run (SQL on `workflow_runs`, `workflow_gate_results`, `workflow_assets`). Confirm gate 2 is `passed` and the `.glb` has separate typed parts. If not, post a blocking question bound to this plan and stop.
2. Rerun the scoping chat's test in `arch-renders/lab/browser-test/` (`scene.html`, `shot.mjs`, committed a7b8566 and b657556) to confirm the headless route still works here before building on it.
3. **Phase A.** Run deep-research on Scope 1's sections; write `skills/arch-viz/SKILL.md` with sources and the rubric. A fresh subagent reads it and lists any rule that cannot be checked; fix those before Phase B.
4. Migration (Supabase `apply_migration`) per Scope 6; seed the library (Scope 3). Check with `list_tables` and `get_advisors`.
5. Build the scene (Scope 2) in `arch-renders/scene/`. Prove headless capture of the sample's three cameras first; record seconds per still. Three failed tries at the "textures and trees fully loaded" check → stop with a diagnosis.
6. Guidance for the sample: material notes from the elevations first (exterior finishes live there; finish schedules are mostly interiors); anything not noted gets a labelled assumed default. If the sample has no material notes, write a short test palette, store it as guidance marked "test palette by Claude", and say so on the run.
7. Assign, place the site per the arch-viz rules, render stills and ID images, run the script checks, then the checker subagent and up to two fix rounds.
8. cbrain-ui (GitHub connector, branch `review`): the materials library screen, the gate 3 panel with the live scene, the site settings, the guidance box (both places), the routes; extend `lib/workflow-model.ts`. Load Three.js only on the client. Type-check locally with stand-ins (Build 34's method), push each prop change with its caller, wait for Vercel READY, read the preview with the Vercel connector.
9. Upload version 1 (stills, ID images, scene config) to `workflow_assets` gate 3 using Build 33's recorded upload method. Write the gate-3 result; run status `waiting-on-charles`.
10. **Stop for Charles** (daytime): the run link and the library link in chat. No response in 2 hours → hand acceptance 8 and 9 off to a draft Build 35.1 and finish the rest.
11. Read pins and per-part picks. Answer every pin; regenerate as version 2; mark pins answered; status back to `waiting-on-charles`.
12. Reference-photo route (Scope 11), 15 minutes at most; none found → record and hand off.
13. Write `skills/arch-materials/SKILL.md`; add the held/didn't-hold notes to `skills/arch-viz/SKILL.md`.
14. Close out per orchestrate-build: Session Log on total-harness with a "What to check" list, disclosures, done receipt. Update the Working Doc: the Stage 4 tech-slot row "Look at the materials gate", the build-order line, and the input-types note that the browser route now renders in the cloud.

## Acceptance

1. `skills/arch-viz/SKILL.md` exists with sourced rules in all five sections and a rubric; the fresh reader's "can't check" list was cleared.
2. Migration applied; `materials` seeded with ≥15 materials, each with aliases, true size and a texture source (licence recorded for images); advisors show nothing new beyond info-level RLS notes.
3. The materials library screen lists, filters, edits and saves a material, and a saved edit shows in the next render (SQL read-back plus a before/after still).
4. Every part of the sample model has a library material with a source.
5. Three stills at 1600×900 from the convention cameras, captured headless in the cloud from the same scene the run view shows, with ID images and seconds per still recorded; trees and textures fully loaded in every still.
6. All script checks pass, including vertical lines and tree placement, and the checker's report is filed with the fix rounds used (≤2); or a three-try diagnosis was posted and the build stopped.
7. The run view shows the gate 3 panel with the live scene; tapping a part shows its material and source; picking another material saves to the run; a still pin stores x, y, asset and part; Pass moves the run to gate 4; deploy READY and the start page, gate 2 view, R&D and Build map work as before.
8. Charles reviewed version 1 (pins, swaps or a pass), or this is handed off to Build 35.1.
9. Every pin answered and version 2 exists, or Charles passed version 1 untouched.
10. Reference-photo route ran once with its mapping recorded, or handed off.
11. `skills/arch-materials/SKILL.md` exists as a draft; arch-viz has held/didn't-hold notes; Session Log, disclosures and Working Doc updates are done.

## Hard gates

- No money.
- No client or FA Wilhelm drawings; the sample only.
- Image textures only with a recorded permissive licence.
- Nothing deleted outside this build's own new rows.

## Completeness table

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered: proves gate 3 for Charles's eye; library for reuse | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: one Three.js scene, live in Charles's browser and headless in the cloud | Scope 2 |
| 4 Data schema | Answered: `materials` table, check widenings, `guidance` column | Scope 3, 6 |
| 5 Storage & recall | Answered: library and assets in cbrain; scene and skills in repos | Scope 2–6 |
| 6 Interconnectivity | Answered: GitHub, Supabase, Vercel connectors; npm for the headless browser | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered: orchestrate-build, deep-research; arch-viz and arch-materials written | Header, Directive 3, 13 |
| 9 Sequence | Answered: expertise → tables and library → scene and capture → assign and site → checks → screens → stop → version 2 → skills | Directive |
| 10 Assumptions & risks | Answered: look ceiling, phone frame rate, sample may lack notes | Current state, Directive 5–6 |
| 11 Design intent | Answered | Below |

## Design intent

Gate 3 answers one question: is this the building Charles means, standing where it will stand? Material truth comes first; the site is there so the building reads in context, not to decorate it. One scene serves everything: what Charles turns around on his phone is exactly what the cloud captures, so a swap he makes is a swap he gets. Every material and every site choice names its source. The arch-viz skill is the expertise: rules learned from practitioners, each one checkable, so quality comes from method rather than taste on the day, and the skill improves with every run. Script first, connector second, screen last.

## Judgment calls made in scoping [Claude]
- **Browser scene is the renderer** for gate 3, live and headless. This reverses the first draft (Blender only), which missed the lab's recommendation; today's test removed the lab's one blocker. Blender moves to gate 4 as the hero-still comparison. Supersedes TH-044.
- The library lives in cbrain, not the repo, because it is edited from a screen and shared by every run.
- Procedural textures first, GitHub-hosted licensed images second; no texture uploads yet.
- EZ-Tree for trees (MIT, ran today). Ruled out hand-built low-poly trees (they looked like toys in today's first test).
- Expertise is researched before building and is the checker's rubric, so the builder does not grade its own taste.
- Review stills at 1600×900.
- Build number stays 35; same plan, new revision.
