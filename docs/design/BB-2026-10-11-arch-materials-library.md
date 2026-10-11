# Build Brief — BB-2026-10-11-arch-materials-library

**Build:** 36
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-11-arch-materials-library.md`
**Project State plan:** `34958d0b-c494-4e5f-b7e2-7795801d9559` on `total-harness`
**Skills:** orchestrate-build; **arch-render** (swatch renders); arch-materials (Build 35's draft)
**Speed run:** arch-renders (record plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`)
**Harness slices:** block 16 (the library as a reusable tool pack)
**After:** Build 35 (plan `da0d7a1a`): the cbrain `materials` table, its seed, and the asset kit.
**Target repos:** Chooch333/cbrain-ui (branch `review`), Chooch333/arch-renders · **Overnight:** yes, except step 5 (a Chrome download needs Charles)
**Stack Flow:** no change

**What this is:** A screen for the materials library: see every material as a real render at true scale, edit it, make variants, and add new ones from Poly Haven. Every arch-renders run picks from it.

**What I'll do (build chat):** Render a swatch for each material, build the Materials view on the Workflows tab, and add "new from Poly Haven".

**What you'll do:** Browse it, edit one material, and make one variant (~10 min). Say yes to the one download batch when you add a new texture.

**Cost:** $0. **Charles's time:** ~10 minutes.

---

## Current state going in
**Asked for** (Charles, 2026-10-10): "I want there to be a materials library with interface"; then "put the library build out into a separate build."
- [verified] The render route is settled: Blender Cycles per `skills/arch-render` (2026-10-11).
- [assumed, from Build 35's scope] The `materials` table exists and is seeded (≈15), with the texture files kept on Charles's PC and staged per run. This build starts by reading Build 35's executor report; if that differs, the DB and report win.

## Receiving chat
New build chat running orchestrate-build.

## Scope
**In scope**
1. **Swatches:** for each material, a 512×512 Cycles render of a 1.2 m × 1.2 m wall sample with a 45° corner, under the `arch-render` sun and sky, at true scale (a scale bar burned into one corner). 16 spp + denoise. Stored as `workflow_assets`-style rows in a new `material_swatches` table (material slug, version, jpeg bytes). Re-rendered whenever a material's settings change.
2. **Materials view** (`/harness?tab=workflows&view=materials`): a grid of swatches; filter by category; search by name or alias. Open one: name, category, aliases (the words drawings use), tile size, tint, saturation, value, roughness, allowed part types, notes, texture source and licence. Save (`POST /api/workflows/materials`), with the same stale-copy guard Build 34 used for conventions.
3. **Duplicate as variant** ("dark iron-spot brick" from "face brick"): same texture, different tint/value/notes.
4. **Re-render queue:** a saved edit marks the swatch stale; the build chat (and later the wake-up set) re-renders stale swatches. The screen shows "updating" until the new swatch lands.
5. **New from Poly Haven:** paste a Poly Haven texture id or link; Claude fetches it through Chrome on Charles's PC (one yes), stages it, adds it to the kit manifest, creates the material with the API's real-world size, and renders its swatch.
6. Update `skills/arch-materials` with how to add and edit a library material.

**Out of scope**
- Uploading arbitrary image files as textures (Poly Haven ids only for now).
- Interior materials.
- Live 3D preview on the screen (swatches are renders).

## Directive
1. Read Build 35's executor report and the live `materials` table.
2. Migration: `material_swatches`; a `swatch_stale` flag on `materials`. Advisors.
3. Swatch script in `arch-renders/pipeline/swatch.py` per `arch-render`; render all; post as JPEG with Build 33's chunked method.
4. cbrain-ui: the Materials view, edit, duplicate, routes, types. Type-check with stand-ins, Vercel READY, read the preview.
5. Add one new material from Poly Haven end to end (Charles's yes for the download).
6. Charles's look (non-blocking): if no response in 2 hours, close out and leave a next move.
7. Close out: Session Log, disclosures, done receipt.

## Acceptance
1. Every seeded material has a swatch at true scale.
2. The Materials view lists, filters, searches, edits and saves; a stale-copy save is refused.
3. A variant made on the screen gets its own swatch.
4. One material added from a Poly Haven id end to end, with licence and size recorded.
5. `skills/arch-materials` updated; Session Log, disclosures done.

## Hard gates
- No money. Chrome downloads only after Charles's yes for the batch. Nothing deleted outside this build's rows.

## Completeness table
| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: swatch renders in the cloud; screen in cbrain-ui | Scope 1–2 |
| 4 Data schema | Answered: `material_swatches`, `swatch_stale` | Directive 2 |
| 5 Storage & recall | Answered | Scope 1 |
| 6 Interconnectivity | Answered: Chrome, device bridge, Supabase, GitHub, Vercel | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered | Header |
| 9 Sequence | Answered | Directive |
| 10 Assumptions & risks | Answered: depends on Build 35's table and kit | Current state |
| 11 Design intent | Answered | Below |

## Design intent
A material is only useful if Charles can see it the way it will render. Swatches are real Cycles renders at true scale, never flat thumbnails. The words drawings use (aliases) matter as much as the look, because assignment reads them. Keep the screen plain and consistent with the Workflows tab.

## Judgment calls made in scoping [Claude]
- Swatches are Cycles renders, not live 3D (one renderer, per `arch-render`).
- Poly Haven ids only for new textures; arbitrary uploads later.
- Overnight allowed except the Chrome download step.
