# Build Brief — BB-2026-10-10-arch-materials-gate

**Build:** 35 (re-scoped 2026-10-11 after the render lab: Cycles stills by the `arch-render` skill; the library screen moves to Build 36)
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-10-arch-materials-gate.md`
**Project State plan:** `da0d7a1a-9cd0-4539-b0eb-5ab6e99a8c21` on `total-harness`
**Skills:** orchestrate-build; **arch-render** (drives every still — read it first); arch-massing (the model it receives); writes **arch-materials**
**Speed run:** arch-renders (record plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`; Working Doc https://claude.ai/code/artifact/864ebc78-392a-4840-bf64-bca83b03f76c)
**Harness slices:** block 6 (separate checker plus fixer), block 8 (render checks), block 16 (arch-render, arch-materials), block 17 (gate 3 rubric)
**After:** Build 33 (plan `c716fa4c`, succeeded): run `5bc91fe6`, gate 2 passed by Charles 2026-10-11 01:33Z; `model.glb` with 59 typed parts.
**Target repos:** Chooch333/cbrain-ui (branch `review`), Chooch333/arch-renders, Chooch333/agent-library · **Overnight:** no (one review stop with Charles; Chrome downloads need him reachable)
**Stack Flow:** no change (nothing new runs on its own)

**What this is:** Proves gate 3 on the real pipeline: the passed white-box model gets materials from the drawings and Charles's guidance and is rendered by the proven Cycles recipe as three photo-like stills from the standard cameras. Charles pins anything that is not the building he means; Claude answers every pin and shows version 2.

**What I'll do (build chat):** Set up the asset kit, seed the materials data, assign materials to the 59 parts, render three stills with `arch-render`, fix the lab's open flaws, check, post version 1, answer pins, post version 2, and write the `arch-materials` skill.

**What you'll do:** Say yes to one texture download batch in Chrome. Then open the run, look at three stills, pin what's wrong ("this should be dark brick, see A-201 keynote 4") or press Pass. About 10 minutes, then a look at version 2.

**Cost:** $0. **Charles's time:** ~15 minutes.

---

## Current state going in

**Asked for** (Charles, 2026-10-10/11): scope gate 3; then "lock down the workflow of the rendering itself. Make sure there's skills that are driving it." Library screen to its own build.

**Render lab result (2026-10-10, this design chat):** Charles judged the Cycles stills "great — that settles the rendering piece."
- [verified ✓✓] `skills/arch-render/SKILL.md` 0.1.0 (agent-library f1c76ce) records the recipe, settings, checks and measured times. Reference scene: `arch-renders/lab/cycles-house/house.py` (7ae4062).
- [verified ✓✓] 1600×900 at 64 spp: 12–15 min per still on the cloud workspace (2 CPU, 7 GB). Low-res check renders 45–80 s.
- [verified ✓✓] Poly Haven is reachable only from Charles's PC. The lab's kit (7 textures + sky, 86 MB) sits in his Downloads as `ph_bundle_archtest.bin`; `device_stage_files` staged it fine.
- [verified ✓✓] EZ-Tree trees/shrubs export to glTF from headless Chrome in the cloud.
- [verified] Build 33: run `5bc91fe6`, generated two-storey sample, `model.glb` (glTF metres, Y up, origin SW corner), 59 parts typed `exterior-wall | interior-wall | slab | roof | glazing | door | opening-frame` with `facade`, `level`, `host` extras. Flat roof with parapets.
- [verified] cbrain tables (`lpeswznkxzeeyiqaewma`): asset kinds `sheet | overlay | model | side-check`; pin targets `sheet | model`. Gate 3 widens them.
- [verified] Asset posting: Build 33's md5-guarded chunked appends work; slow. Post stills as JPEG (~0.5 MB), not PNG.
- [assumed] The generated sample's elevations carry few or no material notes (it was generated for massing). Directive 5 covers it.

## Receiving chat

New build chat running orchestrate-build, daytime, Charles reachable.

## Scope

**In scope**
1. **Asset kit** (`arch-renders/assets/`, manifest only in git; files on Charles's PC at `C:\Users\cecou\code\arch-renders-assets\` and staged per run): the lab's 7 textures + sky, plus the textures the seed library needs that the lab lacked (metal wall panel, CMU or concrete block, fiber-cement or painted lap siding, standing-seam or corrugated metal, aluminium/storefront frame finish, a paving). Fetch in one bundle through **Chrome (Claude in Chrome)** after Charles's yes; record id, licence (CC0) and real-world size from the Poly Haven API for each.
2. **Materials data** (cbrain table `materials`, RLS on, no policies): slug, name, category, aliases as drawings write them, tile size m, texture id, tint, saturation, value, roughness multiplier, allowed part types, notes, updated_at. Seed ≈15 from the kit. Build 36 adds the screen; this build only needs the data.
3. **Assignment** (`arch-renders/pipeline/materials.py`): every part gets a library material, a tint and a source (sheet + note, `palette`, `photo`, or `assumed`), from the elevations' notes first, then guidance, then labelled defaults. Stored as the gate-3 result's assumptions.
4. **Render** with `arch-render`: import the gate-2 model, apply the assignment per part, build the site (aimed sun from the conventions' look, HDRI sky, ground, grass, trees, haze), render the three convention cameras at 1600×900, 64 spp; plus a flat **part-ID image** per still so a pin resolves to a part. Fix the lab's open flaws first: grass covers the whole frame or fades (no hard edge), walks masked clear, interiors read as rooms.
5. **Orbit model:** export a `.glb` with base colours from the assignment so the run view's existing viewer shows the materials roughly (stills are the judged output).
6. **Migration:** `materials`; asset kinds add `still`, `id-pass`; pin target adds `still` (needs `x`, `y`, `asset_id`) with nullable `part`; `workflow_runs.guidance jsonb` default `{}` (`materials`: palette text, photos link, use-drawing-notes).
7. **Run view, gate 3 panel** (`components/harness/workflow-run-view.tsx`): three stills (enlarge; click to pin, resolved to a part via the ID image), the orbit model, the assignment table, checks, pins with answers, Pass (`current_gate` 4). A guidance box beside gate 2's Pass for future runs. Route `POST /api/workflows/runs/[id]/guidance`.
8. **Checks:** `arch-render`'s list plus: every part has a library material with a source; tile sizes match the library. Then a fresh checker agent against the drawings and the skill's list; two fix rounds at most.
9. **Version-2 loop** after Charles's pins.
10. **Skills:** write `skills/arch-materials/SKILL.md` (draft); update `skills/arch-render` with what held, what didn't, and times on a two-storey, flat-roof model. Add sourced craft rules from one short deep-research pass (camera, light, materials, site, the ten most common "looks fake" causes) only where they add a checkable rule.

**Out of scope (forks pre-answered)**
- The materials library screen: Build 36.
- A browser live-swap scene. Ruled out: a second renderer to maintain; swaps go through pins and come back as version 2.
- Animation, motion, titles, callouts, AI finish: gate 4.
- Any FA Wilhelm or client drawing.

## Directive
1. Read live state: this plan, `c716fa4c` (executor report, disclosures TH-J-008..013), `37d9e5ef`; `skills/arch-render`, `skills/arch-massing`; run `5bc91fe6` rows. Confirm gate 2 `passed` and the 59 typed parts.
2. Asset kit: list the textures needed (Scope 1), ask Charles once for the download batch, fetch in Chrome as one bundle, stage, unpack, write the manifest.
3. Migration (Supabase `apply_migration`) and seed. `list_tables`, `get_advisors`.
4. Port `lab/cycles-house/house.py` into `pipeline/render.py`: read the gate-2 `.glb` and the assignment instead of building the lab house; keep the site, sun, sky, grass, trees, haze, cameras and settings. Prove it with an 800×450 check render of each camera first.
5. Assignment from notes; if the sample has none, write a short test palette, store it as guidance marked "test palette by Claude", and say so on the run.
6. Full renders (≈45 min for three), ID images, orbit `.glb`. Script checks, checker agent, ≤2 fix rounds. Three failed tries at one check → stop with a diagnosis.
7. cbrain-ui: gate 3 panel, guidance box, routes, model types. Type-check with stand-ins (Build 34's method), Vercel READY, read the preview.
8. Post version 1 (JPEG stills, ID PNGs, orbit `.glb`) with Build 33's chunked method; gate-3 result; run `waiting-on-charles`.
9. **Stop for Charles.** No response in 2 hours → hand acceptance 7–8 to a draft Build 35.1, finish the rest.
10. Answer pins → version 2.
11. Skills (Scope 10). Close out per orchestrate-build: Session Log, disclosures, done receipt; Working Doc Stage 4 row "Look at the materials gate".

## Acceptance
1. Asset kit manifest committed; every texture has id, licence and real-world size; the bundle staged and unpacked.
2. Migration applied; `materials` seeded (≈15, each with aliases, size, texture); advisors nothing new beyond info-level RLS notes.
3. Every one of the 59 parts has a material and a source.
4. Three 1600×900 stills from the convention cameras, rendered by `pipeline/render.py` per `arch-render`, with ID images and times recorded.
5. All checks pass (including no grass edge, walks clear, rooms read), checker report filed with fix rounds used; or a three-try diagnosis posted and the build stopped.
6. Gate 3 panel live: a still pin stores x, y, asset and part (SQL read-back); Pass moves the run to gate 4; deploy READY; start page and gate 2 view unchanged.
7. Charles reviewed version 1, or handed off to Build 35.1.
8. Every pin answered and version 2 exists, or Charles passed version 1 untouched.
9. `skills/arch-materials` draft exists; `skills/arch-render` updated; Session Log, disclosures, Working Doc done.

## Hard gates
- No money.
- Downloads to Charles's PC only through Chrome, after his yes for the batch.
- No client or FA Wilhelm drawings; the sample only.
- Nothing deleted outside this build's own rows.

## Completeness table
| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered: gate 3 on the real pipeline, for Charles's eye | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: Cycles in the cloud workspace; screen in cbrain-ui | Scope 4, 7 |
| 4 Data schema | Answered | Scope 2, 6 |
| 5 Storage & recall | Answered: kit on Charles's PC + manifest in git; data and assets in cbrain | Scope 1–2 |
| 6 Interconnectivity | Answered: Chrome, device bridge, GitHub, Supabase, Vercel | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered: arch-render drives; arch-materials written | Header, Scope 10 |
| 9 Sequence | Answered | Directive |
| 10 Assumptions & risks | Answered: sample notes, upload speed, render time | Current state |
| 11 Design intent | Answered | Below |

## Design intent
Gate 3 answers one question: is this the building Charles means? The look is settled; this build applies it, it does not re-explore it. Follow `arch-render` exactly and change it only by writing down why. Every material names its source so a wrong guess is easy to pin. Spend fix rounds on low-res checks; render full size once. Script first, connector second, screen last.

## Judgment calls made in scoping [Claude]
- Cycles stills via `arch-render` (settled by Charles 2026-10-11). Supersedes TH-045's browser-renderer choice.
- Live material swapping dropped; pins do the job.
- Materials data in this build, the screen in Build 36, so assignment isn't blocked on UI.
- The kit's files live on Charles's PC and are staged per run; only a manifest goes in git (86 MB+ of binaries doesn't belong in a repo through the connector).
- Stills posted as JPEG to cut upload chunks.
