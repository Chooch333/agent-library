# Build Brief — BB-2026-10-10-arch-style-study

**Build:** 33
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-10-arch-style-study.md`
**Project State plan:** `c716fa4c-67d8-48bb-b94d-7f5d7d4a9c71` on `total-harness`
**Skills:** orchestrate-build, project-folder
**Speed run:** arch-renders (record: plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`; Working Doc https://claude.ai/code/artifact/864ebc78-392a-4840-bf64-bca83b03f76c)
**Harness slices:** block 7 (PDF to white-box model), block 8 (overlay check), block 6 (separate checker)
**After:** none · **Target repo:** Chooch333/arch-renders (created by this build) · **Overnight:** no (one money stop; daytime with Charles reachable)
**Stack Flow:** no change (a study; nothing new runs on its own)

**What this is:** The style study that decides how the arch-renders speed run makes its stills. One public plan set PDF, one white-box model raised from it, the same three cameras, three looks side by side. Charles picks one, or says none is good enough.

**What I'll do (build chat):** Find a public CAD-exported plan set PDF, raise one model from its linework, render the three cameras two ways (Blender in the cloud; a browser 3D scene in Chrome on the laptop), price one AI finish pass, run it on Charles's yes, and publish one comparison page.

**What you'll do:** Answer one money stop (yes or no on the priced AI pass, ~2 min), keep the laptop awake with Chrome open for the browser look, and pick a look on the comparison page (~5 min).

**Cost:** $0 for looks 1 and 2. Look 3: priced at the money stop; ceiling $20 one-time, no standing subscription without a separate yes. **Charles's time:** ~10 minutes.

---

## Current state going in

**Asked for** (TH-Q-001 handoff, R&D lab 2026-10-09, frozen): "A style study, before anything else is built: one public sample plan, one model, the same three camera positions, and the looks side by side. 1. The browser scene with its finishing passes. 2. Blender from the same model. 3. The better of those two with an AI finish pass. Charles picks, or says none is good enough. That one result decides which route the workflow uses and whether the three ArtCraft apps are adopted. If raising the model from plan layers fails, stop there: nothing downstream matters."
**Charles's dated change** (speed-run requirement, carried by TH-030): the input is a standard plan set PDF with no special prep. This brief raises the model from the PDF, not a DXF.

Verified 2026-10-10 from the cloud workspace this build will run in:
- [verified] 2 processors, 7 GB memory, no graphics card.
- [verified] `pip index versions bpy` → 5.2.2 available (Blender as a Python module); `pymupdf` → 1.28.2.
- [verified, lab ✓✓] Blender rendered stand-in stills in the cloud at 65 to 95 s each.
- [verified, lab ✓✓] A browser 3D scene does not run in the cloud workspace; it runs in Chrome on the laptop, which Claude can drive. Capturing stills from it is untested.
- [assumed, from the workspace's stated allowlist; pip confirmed working] The shell reaches only pip, npm and GitHub. Vendor APIs and download sites are refused, so any paid AI pass runs from the laptop browser or a connector, never from the shell.
- [verified] No image-generation connector is loaded in the scoping session (tool search). The lab's note that one exists is unconfirmed; the build checks its own tool list.
- [verified, source] mnml.ai lists an API and a free trial; third-party review: plans $19 / $39 / $79 a month, 100 credits per render.
- [verified] Build 29.1: cloud sessions cannot git-clone repos; read and write repo files through the GitHub connector.
- [assumed] A public CAD-exported plan set PDF with plans and elevations exists on GitHub or a public archive. Candidate not opened: the permit-set generator at github.com/AchyErrorJ/LegibleStudios (emits plan and elevation PDFs).
- Blocks: 1 done, 2 done, 3 in progress (Build 30.1). This build uses block 1 (laptop Chrome) only for look 1.

## Receiving chat

New build chat running orchestrate-build, in the daytime with Charles reachable.

## Scope

**In scope**
1. Repo `Chooch333/arch-renders` (private) from the project-folder template, folder `study/`.
2. One public sample plan set PDF, CAD-exported (vector), one or two stories, with at least one floor plan and two elevations. Source link and licence noted.
3. Plan to model: PyMuPDF pulls vector paths from the floor plan page; Claude reads the sheet image to tag walls, doors and windows; heights from the elevations; one neutral model file `study/model.glb` both renderers load, so geometry is identical.
4. Three named cameras in `study/cameras.json`, 1920×1080: `aerial-34` (three-quarter aerial, front-left), `street` (eye level 1.6 m, about 30 m from the front), `entry` (eye level near the entry).
5. Look 1 — browser scene: Three.js pinned at the release current at build start, with soft shadows, ambient occlusion, edge lines, sky and ground, and a color grade. Runs in Chrome on the laptop.
6. Look 2 — Blender: bpy 5.2.2 in the cloud, Cycles on the processor, sun and sky, simple materials, same model and cameras. Time cap: 3 minutes a still.
7. Look 3 — AI finish pass on the better of looks 1 and 2, after Charles's yes at the money stop.
8. A separate checker subagent grades every still against the rubric; up to two fix rounds per look.
9. One comparison page (artifact): rows = cameras, columns = looks, each labelled with route, render time and dollars per still, plus a "none good enough" answer.
10. `study/findings.md`: the seven tech-contract answers for each route tried.

**Out of scope (forks pre-answered)**
- DXF input. Ruled out: fails "input as found".
- Any FA Wilhelm or client drawing. Public sample only.
- Motion, touch-up, the use-case skill, the asset kit. Those are stage 6.
- Veras. Ruled out: a plugin inside Rhino, SketchUp or Revit with no way for Claude to drive it.
- Adopting any tool. The study recommends; Charles decides from the page.

## Directive

1. Read live state: `get_plan` on this plan and on plan `37d9e5ef-3ac1-40f7-876d-5bcba64423b0`. Check this session's tool list for an image-generation connector and for `mcp__claude-in-chrome__*` and `mcp__remote-devices__*` tools; record what exists.
2. Create `Chooch333/arch-renders` (Custom GitHub `create_repo`, private) and fill it per `skills/project-folder` (spec = this brief's Scope; features F01 to F06 = acceptance 2 to 7). Run its validator.
3. Find the sample (WebSearch, then GitHub `search_code` / `get_file_contents`; a file from outside GitHub goes through the laptop browser, and each download needs Charles's yes per the safety rules). Spend at most 30 minutes; if no real architect's set is found, use a generated set from the LegibleStudios repo and say so on the page. Commit it to `study/input/` with `SOURCE.md`. Run the vector check (PyMuPDF path count on the plan page); a scan fails this step.
4. Raise the model (Bash in the workspace): extract paths, scale from the scale note or a dimension string, Claude tags walls and openings from the rendered sheet image, extrude to elevation heights, cut openings, export `model.glb`. Write `study/assumptions.md` (every default height, roof shape, wall thickness). Self-check: render the model's top view over the plan page and one side view over an elevation; record the deviation. Pass = within 2% of overall length. **Three failed tries → stop the build here with a diagnosis** (the handoff's stop rule); acceptance 4 to 7 become not applicable and the page shows the diagnosis instead.
5. Look 2 (Blender) first, because it runs without the laptop: install bpy 5.2.2, import `model.glb`, apply cameras, render three stills. Record seconds per still.
6. Look 1 (browser): write a single-page Three.js scene that loads the same `model.glb` and `cameras.json`. Open it in Chrome on the laptop. Get 1920×1080 PNGs back by the first route that works: (a) the page saves into a published artifact's file store if that capability is offered; (b) a download into the laptop's connected folder `C:\Users\cecou\code` after Charles's yes; (c) a browser screenshot at 1920×1080 window size. Record which route worked. Laptop asleep or Chrome unreachable after two tries → finish everything else, hand look 1 off to a draft Build 33.1, and say so on the page.
7. Checker: a fresh subagent (Agent tool) that has not seen the build grades each still on the rubric below and ranks flaws. The builder fixes and re-renders, at most two rounds per look. Equal effort per look: no look gets a third round.
8. Pick the better of looks 1 and 2 by the checker's scores. **Money stop:** post to Charles in chat one priced option for the AI pass (tool, where the images go, dollars for three stills, whether a sign-up is needed — Claude never creates accounts; Charles signs up if needed). Order of preference: an image-generation connector in this session (if present and free or under $20), then mnml.ai's free trial via the laptop browser. No yes within 30 minutes → hand look 3 off to draft Build 33.1.
9. On yes, run the pass on the three approved stills of the better look, keeping geometry strict. Record dollars actually spent.
10. Publish the comparison page (Artifact, load the artifact-design skill first). Commit all stills, the model and `findings.md` to `study/`.
11. Close out per orchestrate-build: Session Log on total-harness referencing BB-2026-10-10-arch-style-study, fork log, disclosures on the Comms Table. Add a next move on total-harness tagged `speed-run-arch-renders`: "Charles picks a look on the style-study page; the next Total Harness chat records it and runs stage 5."

## Rubric (the checker grades 1 to 5 on each)

Geometry matches the plan and elevations · light reads as daylight with soft shadows · materials read as real (not flat gray) · edges and openings crisp, no artefacts · sky, ground and site present · photo-like overall (Charles's requirement 4). A still below 3 on geometry is a fail regardless of the rest.

## Acceptance

1. `Chooch333/arch-renders` exists from the template; validator OK.
2. A public sample PDF in `study/input/` with `SOURCE.md` (link, licence); vector check result recorded.
3. `study/model.glb` raised from the PDF, with the overlay images and a deviation within 2%; or a three-try diagnosis, and the build stopped there.
4. Look 2: three stills at 1920×1080 from the named cameras, seconds per still recorded.
5. Look 1: three stills from the same cameras, capture route recorded; or handed off to Build 33.1.
6. Checker reports for every still, with the fix rounds used (≤2 per look).
7. Look 3: three stills with dollars spent, after Charles's yes; or handed off to Build 33.1.
8. Comparison page published; `study/findings.md` holds the seven contract answers per route tried.
9. Session Log, fork log, disclosures and the "Charles picks" next move exist.

## Hard gates

- Money: the AI finish pass, and any sign-up. Charles's yes in chat, per action.
- File downloads on the laptop: Charles's yes per download.
- No client or FA Wilhelm drawings, ever, in this build.
- Nothing deleted.

## Completeness table

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered: a one-off study for Charles's eye; decides the render route | What this is |
| 2 Acceptance | Answered | Acceptance |
| 3 Runtime | Answered: cloud workspace (Blender, PyMuPDF), laptop Chrome (Three.js) | Directive 4–6 |
| 4 Data schema | N/A: files only | — |
| 5 Storage & recall | Answered: repo `study/`, recall by path | Scope |
| 6 Interconnectivity | Answered: GitHub connector, Chrome extension, Artifact | Directive |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered: orchestrate-build, project-folder, artifact-design | Header, Directive 10 |
| 9 Sequence | Answered: model before looks; look 2 before look 1; money stop before look 3 | Directive |
| 10 Assumptions & risks | Answered: sample availability assumed; laptop may sleep; capture route untested | Current state |
| 11 Design intent | Answered | Below |

## Design intent

The study answers one question: which route makes a still Charles would actually use, from a PDF as it arrives. Protect geometry truth first; a pretty still of the wrong building is a fail. Give each look the same effort so the comparison is fair, and label every still honestly with its route, time and cost. "None is good enough" is a valid, useful result; do not polish around a weak route to avoid it. Prefer the route that runs in the cloud with no laptop when two looks are close, because it removes the laptop and wake-up dependencies. Script first, connector second, screen last.

## Judgment calls made in scoping [Claude]
- PDF input, not DXF (Charles's requirement beats the lab's chain).
- Look 2 before look 1, so a sleeping laptop cannot block the study.
- One neutral model file shared by both renderers, so only the look differs.
- Money ceiling $20 one-time for the AI pass; any subscription needs its own yes.
- Build number 33 (31 and 32 used on 2026-10-09).
