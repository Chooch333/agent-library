---
title: "Likeness Heat Map"
type: rd-report
brief: ""
reviewed: 2026-10-25
test_date: 2026-10-24
test_completed: 2026-10-25
status: complete
tools: [likeness-heat-map, claude-code-character-opus, claude-code-character-fable, character-finish-checks]
report_url: https://claude.ai/artifact/6yAvpFG33W1chJ1bJnyZcM
clips:
  - env: "E: Opus 5.5, loop + build rules, no finishing pass"
    anchor: opus-heatmap-e
    file: still_opus_heatmap_e.jpg
  - env: "F: Fable 5.1, loop + build rules, no finishing pass"
    anchor: fable-heatmap-f
    file: still_fable_heatmap_f.jpg
  - env: "D: C + build rules + finish checks"
    anchor: opus-heatmap-d
    file: still_opus_heatmap_d.jpg
  - env: "C: rough model, heat map, traced fixes"
    anchor: opus-heatmap-c
    file: still_opus_heatmap_c.jpg
  - env: "A: measure the whole drawing first"
    anchor: opus-heatmap-a
    file: still_opus_heatmap_a.jpg
  - env: "B: rough model, heat map, fixes by eye"
    anchor: opus-heatmap-b
    file: still_opus_heatmap_b.jpg
image: compare_same_view.jpg
clips_home: "Published with the report at report_url; sources in Chooch333/kids-games lab/claude-image-to-3d/heatmap-runs/ (private)"
draft: false
---
# Likeness Heat Map
## Grid heat map + build rules · Claude Opus 5.5 and Fable 5.1 (Three.js code)

**Test problem:** Study whether a grid heat map that compares Opus's model with the drawing cuts the time to build a game character from a drawing, at the same or better likeness.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-24 | 2026-10-25 | Complete |

**Rev history**

0. **2026-10-24** First draft; verdicts proposed, awaiting Charles's likeness judgment
1. **2026-10-25** Charles: C very good but jagged edges and arms not touching. Two finish checks added (smooth, attached); run D tests the locked-in workflow
2. **2026-10-25** Charles: checks are redundant if the build rules are in up front. Runs E (Opus) and F (Fable): loop + build rules, no finishing pass. Finishing pass dropped
3. **2026-10-25** Charles: "Run E is the standard", Opus only, nothing for Fable. Written into the game-maker skill 0.4.0 as the Character maker; report Complete

(Tested) we ran it and measured it
(Published) from the maker's own documentation
(Assumed) our judgment, not yet checked

## 01 Tech description

The tech under test is a **likeness heat map**: a small checking tool Claude wrote for this test, plus **Claude Opus 5.5** using it while it builds. The tool loads the character's game file (`.glb`), draws it straight from the front at the drawing's size with cartoon outlines, lines it up with the drawing, and lays a 32 × 32 grid over the character. Each square is checked three ways: **shape** (is there character where the drawing has character), **dark details** (mask, eyes, pupils, smile, boots, fists, outlines in the same place) and **colour** (the square's average colour, so stripe order inside the candy does not count). A square fails if any check is over its limit. It returns a picture with failing squares in red, the score as **squares passing**, and a ranked list of problem areas named by grid cell (A1 to H8) and by the model's own part names. Jev was not part of this test: it is metered, and a free way to run it is still unconfirmed.

Two **finish checks** run after the heat-map rounds. **Attached:** every part must connect to the body through parts that touch, in the standing pose and through every frame of every move; parts that come close without touching are listed as near misses to compare with the drawing. Face shapes that lie on the candy a hair above its surface count as attached. **Smooth:** the model is drawn from the front at 2048 pixels tall, and every part's edge and every colour band (swirl, stripes) is measured for zig-zag, meaning turns that are undone by an opposite turn a few pixels later, the mark of a stair-step. A part fails above 18% zig-zag on its edge or 8% on a colour band.

### How it runs

- **Where:** the cloud machine Claude works on (2 processors, 7 GB, no graphics card, no screen) (Tested).
- **Subscription cost:** none. It uses Three.js (MIT) and standard Python image libraries already on the machine (Published).
- **Cost to run:** $0. About 6 to 10 seconds per check (Tested).
- **How Claude controls it:** one command per check; Claude reads the picture and the problem list it writes (Tested).
- **Finish checks:** about 1.5 minutes per run, most of it checking every frame of the three moves (Tested).
- **What it needs:** three files (`heatmap.py`, `checks.py`, `dump_glb.mjs`) and `npm i three@0.186.1`. A front-view drawing on a plain background, and a model that faces the camera in the drawn pose (Tested).

## 02 Findings

**Decision (Charles, 2026-10-25): run E is the standard, on Opus only.** It is now the Character maker in the game-maker skill (agent-library skills/game-maker/SKILL.md 0.4.0, section 9), with the heat map, exporter, validator, still renderer and viewer in skills/game-maker/maker/. Fable is not used.

**Revision 2:** the build rules alone are enough. Two fresh builds used the heat-map loop and the build rules with no finishing pass: **Opus (run E) 84.5% in about 27 minutes** and **Fable (run F) 88.3% in about 26 minutes**. Measured afterwards, both are attached and smooth; the one smooth flag (E's elbow) is a false alarm, and it was the same spot that cost run D its 11-minute finishing pass. So the finishing pass is dropped, as Charles proposed. Fable, given the loop, matched or beat Opus on this drawing and kept the mask's angry slant; its wrapper ends are flat slabs from the side, where Opus's are twisted paper. One sample each, run side by side.

The heat map cut Opus's build time only when it was used one way: **a rough model first, then short rounds where the heat map says where the model is off and Opus measures just that part from the drawing**. Run that way (run C), Opus reached Wednesday's likeness score in 10 minutes and delivered at **86.7% of squares passing in 18.5 minutes**, against 79 minutes and 58% on Wednesday. Charles judged C very good but saw two faults: jagged edges on the eyes, mouth and mask, and arms that do not touch the body. Both came from how C built its parts, not from the heat map: it cut face shapes out of a fine sphere triangle by triangle, switched swirl colours hard from point to point, and started the right arm short of the body. Two **finish checks** now catch both (attached, smooth), and build rules prevent them. **Run D**, a fresh build with the whole locked-in workflow, passed both checks at **85.4%** in **31.7 minutes**: 21 minutes of heat-map rounds, then 11 minutes of finishing. Smoothing cost one point of score. By eye, D is the best of the runs: smooth face shapes, ruffled wrapper ends, fists on the hips and a cape that attaches. It lost the angry slant of the mask over the eyes. The score weighs every square the same, so small face details like that still need Charles's eye. Two other loop rules did not work: measuring the whole drawing first (run A, 101 minutes) and fixing by eye (run B, stalled near 65%). One drawing; C and D are two samples of the same loop.

26–27 vs 79 min

runs F (Fable) and E (Opus), loop + build rules, vs Wednesday's Opus, brief to full deliverable (Tested)

88% / 85% vs 58%

squares passing, Fable F / Opus E vs Wednesday's Opus, same tool (Tested)

0 real faults

found by the finish checks in E and F, run afterwards as a measure only (Tested)

### Inputs the workflow must supply

- One clean drawing, front view, plain background (as before).
- A model that faces the camera, upright, standing in the drawn pose, so the front view can be compared as is.
- The 2D-3D Maker tool: heat map, exporter, validator, still renderer, viewer (agent-library `skills/game-maker/maker/`).
- A stop line for the rounds: 80% of squares passing, or two rounds that each gain under 2 points.
- A done line: 80% reached, zero validator errors, under 2 MB, and the face passes Charles's eye. No check pass (revision 2).

### Where it went (no Total Harness build needed)

- The **heat-map tool** and the packaging scripts as the 2D-3D Maker tool, beside the skill in agent-library, so the skill and the code it runs live and change together (TH-094 had suggested the family-arcade repo; no game loads this code). `checks.py` stays in the lab as a measuring stick.
- The **Character maker** is section 9 of the game-maker skill (0.4.0): rough model in under 15 minutes with no measuring; rounds that measure only what the heat map flags, revert any round that scores worse, stop at 80%; no finishing pass (Tested) (runs C, D, E).
- The **build rules** that keep parts smooth and joined: face shapes built from a smoothed outline and wrapped onto the body, colour bands blended, round parts with at least 32 segments, every limb starting inside the part it hangs from, plus a triangle budget (Tested) (runs D, E; the budget on run E's code under Three.js 0.160.0: 55,776 triangles, 1.78 MB, 84.4%).
- A **face check** on top of the score, so a lost expression (D's mask slant) or a cruder face (B) cannot pass on outline alone: the likeness checklist from TH-093 names each face feature (Assumed).
- One mode, Opus only, about 30 minutes, replacing TH-093's fast (Fable) and detail (Opus) modes and the shared parts library (Assumed) until a second drawing confirms the time.

## 03 Experiment parameters

Four sealed Opus 5.5 runs received the same drawing and the same deliverable list as Wednesday's Opus run, built from scratch with no parts library and no earlier character code, and used the heat map under different loop rules; the fourth (D) added the build rules and finish checks. Wednesday's Opus and Fable game files were rebuilt from their saved code and scored with the same tool as the baseline.

Test input

The Super Sweets drawing used for Meshy and for Wednesday's runs (1024 × 1024, from the private kids-games repo), recovered from its text copy and checked byte for byte against the repo (165,109 bytes).

The test

Wednesday's sealed brief word for word (character code, viewer page, validated .glb with idle, walk and jump, a three-quarter still, a timing log), plus one new section: the likeness loop. Only the loop rules differed between runs.

The four loop rules

- **A:** make the first complete model as early as reasonable, then fix the three worst areas; stop at 60%.
- **B:** rough model by eye within 15 minutes with no measuring of the drawing, then fix the three worst areas; stop at 80% or when two rounds each gain under 2 points.
- **C:** as B, but each flagged area is fixed by measuring that part from the drawing's pixels, using the tool's reported scale and offset, and a round that scores worse is reverted.
- **D:** as C, plus build rules (face shapes from smoothed outlines, blended colour bands, round parts of 32+ segments, limbs starting inside their parent) and a finishing pass: both checks must pass with the score at least 75%, up to three passes.

Capabilities tested

Time to first model, time to full deliverable, score per round, whether the loop converges, validator result, and whether the model stays a real 3D character (three-quarter and back views).

Not tested

**Jev as the square judge:** metered, free route unconfirmed. **Fable 5.1 with the loop:** not in runs A–D (they were about Opus's time); tested later as run F. **A second drawing:** the score limits and line-up were tuned on this drawing. **Viewer pages in a browser:** no browser on the cloud machine; the two pages are published for Charles.

Output

Per run: `character.js`, `viewer.html`, `character.glb`, `validation.json`, `still.png`, `log.md`, and the heat-map picture and problem list for every round.

Settings

Three.js 0.186.1, glTF validator via npm, Node 22. Heat map: 32 × 32 fine grid, 8 × 8 coarse grid; a square fails above 12% wrong shape, 12% wrong dark detail, or a colour gap of 14; about 10 pixels of misalignment forgiven; outline weight measured from the drawing (about 19 px).

Machines and versions

Cloud machine only: 2 processors, 7 GB, no graphics card. Each run was a sealed Opus worker that reported its own model name (`claude-opus-5-5`) (Tested).

What we measured

- **Time:** wall clock from the worker's first `date -u` to first model, to each round, and to full deliverable, checked against file times.
- **Score:** squares passing, re-run by the review chat on each final .glb rather than read from the logs.
- **Validity:** Khronos glTF validator errors and warnings.
- **Likeness:** by eye, Charles's call, from the same-view comparison and the two viewer pages.

Side checks

**Finish-check calibration** on the finished runs (Tested): run C fails both (right arm 1% of height off the body; mask, eyes, pupils, smile and swirl stair-stepped), matching what Charles saw; run A fails attached (cape hovers behind the candy) and passes smooth; Wednesday's Opus fails both (cape 4% off the body, sawtooth swirl); run B passes both. On edges, stair-stepped face shapes scored 0.22 to 0.36 zig-zag and every smooth one 0.00 to 0.16; on colour bands, hard switches scored 0.10 to 0.18 and blends 0.03 to 0.05. **Heat-map calibration:** the tool scored Wednesday's Opus at 58.2% and Wednesday's Fable at 25.2%, the same order Charles ranked them (Tested). Both rebuilt files matched Wednesday's exactly (Opus 1,488,852 bytes; Fable 14,104 triangles). **Tool fixes before the runs:** the first version drew outlines that hid the eyes, flagged stripe order inside the candy, and lined models up on the whole outline, so a long cape pulled the body off centre; all three were fixed before any run started. **Grading:** no run edited the tool.

Saved test files

`Chooch333/kids-games` `lab/claude-image-to-3d/heatmap-runs/` (private): the tool (`tools/`), `WORKFLOW.md`, `run-d/` and `run-e/` (`character.js`, `log.md`; run E is the reference build). The tool as the skill uses it: agent-library `skills/game-maker/maker/`. Other runs' files stayed in the review chat's workspace.

## 04 Results by test environment

### F: Fable 5.1, loop + build rules, no finishing pass

sealed Fable 5.1 worker · 5 rounds · **Shelf**

**Image:** `still_fable_heatmap_f.jpg`

Its own still, three-quarter view. [Live viewer page](https://claude.ai/artifact/9tARLa2x7psaGfzPpGPdJV) with Idle, Walk, Jump.

- **Time:** ~26 min full deliverable; first model 5.3 min; 80% at 22.5; loop stopped 23.4 (Tested)
- **Rounds:** 43.2 → 68.7 → 74.5 → 81.8 → 88.3%
- **Checks (after, as a measure):** Attached PASS, smooth PASS. Near miss: fists about 5% of height off the hips (Tested)
- **Size:** 69,984 triangles · 1.88 MB · 13 bones · 3 clips
- **Validator:** 0 errors, 0 warnings (Tested)
- **Quality:** Highest score of all runs; smooth face shapes with the mask's angry slant kept. Wrapper ends are thick flat slabs, which read as flat from the side; fists hover just off the hips (Tested).
- **Verdict note:** Shelf. Charles chose Opus only ("This is only an opus run. Nothing for fable."). Best score of the runs, but flat slab wrapper ends from the side and fists off the hips. Without the loop, Wednesday's Fable stopped at 6 minutes with a much weaker model.

### E: Opus 5.5, loop + build rules, no finishing pass

sealed Opus 5.5 worker · 4 rounds · **Adopt now**

**Image:** `still_opus_heatmap_e.jpg`

Its own still, three-quarter view. [Live viewer page](https://claude.ai/artifact/94nGdCfzCh4GYQ4L8kigYr) with Idle, Walk, Jump.

- **Time:** ~27 min full deliverable; first model 5.2 min; 80% at 20.2 (Tested)
- **Rounds:** 64.3 → 76.5 → 77.7 → 84.5%
- **Checks (after, as a measure):** Attached PASS. Smooth flags the right elbow, a false alarm: the close-up shows a clean corner where the two arm pieces meet (Tested)
- **Size:** 61,856 triangles · 1.97 MB (cap 2 MB) · 15 bones · 3 clips
- **Validator:** 0 errors, 22 warnings (harmless placement of skinned parts) (Tested)
- **Quality:** Smooth face shapes with the angry slant kept; ruffled, twisted wrapper ends that hold up from the side; fists on the hips; cape attached (Tested).
- **Verdict note:** Adopt now: Charles, 2026-10-25, "Run E is the standard". Written into the game-maker skill as the Character maker. The skill adds a triangle budget because this file sat at the 2 MB cap.

### D: C + build rules + finish checks

sealed Opus 5.5 worker · 7 rounds + 2 finishing passes · **Superseded by E**

**Image:** `still_opus_heatmap_d.jpg`

Its own still, three-quarter view. [Live viewer page](https://claude.ai/artifact/H6VqUA5maC4oq4NbHJrnNb) with Idle, Walk, Jump.

- **Time:** 31.7 min full deliverable; first model 8.3 min; 80% at 20.8; both checks passed at 30.4 (Tested)
- **Rounds:** 55.8 → 60.5 → 65.9 → 68.7 → 72.2 → 73.6 → 86.4%; 85.4% after finishing
- **Checks:** Pass 1: attached PASS, smooth FAIL (where two arm pieces met at the right elbow). Pass 2: both PASS, after an elbow joint ball and fists moved onto the hips (Tested)
- **Cost:** $0
- **Size:** 78,528 triangles · 1.92 MB (cap 2 MB) · 17 bones · 3 clips
- **Validator:** 0 errors, 76 warnings (unused bone weights on the cape; harmless) (Tested)
- **Quality:** Best of the runs by eye: smooth mask, eyes, pupils and smile; ruffled wrapper ends with crease strokes; fists on the hips; cape attached and shaded. Lost the angry slant of the mask over the eyes; the swirl reads as six twisted bands without the drawing's highlights (Tested).
- **Verdict note:** Showed the build rules and checks working together. Runs E and F then showed the rules alone are enough, and that the finishing pass here fixed a false alarm at the elbow.

### C: rough model, heat map, traced fixes

sealed Opus 5.5 worker · 4 rounds · **Superseded by D**

**Image:** `still_opus_heatmap_c.jpg`

Its own still, three-quarter view. [Live viewer page](https://claude.ai/artifact/YCiTDzhkfJvPZfvUQgkJTf) with Idle, Walk, Jump.

- **Time:** 18.5 min full deliverable; first model 4.1 min; 60% at 9.9; 80% at 15.8 (Tested)
- **Rounds:** 59.8 → 63.9 → 78.9 → 86.7%
- **Cost:** $0
- **Size:** 37,288 triangles · 1.89 MB · 15 bones · 3 clips
- **Validator:** 0 errors, 0 warnings (Tested)
- **Checks:** Attached FAIL (right arm 1% of height off the body; fists hover 4% off the hips). Smooth FAIL (mask, eyes, pupils, smile, swirl, elbow balls) (Tested)
- **Quality:** Close proportions: body size, legs, boots, arm pose and cape outline traced from the drawing. Weak spots: stair-stepped mask, eye and mouth edges; right arm not touching the body; plain bell-shaped wrapper ends; flat cape (Tested).
- **Verdict note:** Charles: "very good", with the jagged edges and loose arms as the faults. Its loop is kept; D adds the build rules and finish checks that fix both.

### A: measure the whole drawing first

sealed Opus 5.5 worker · 3 rounds · **Never (as a variant)**

**Image:** `still_opus_heatmap_a.jpg`

Its own still, three-quarter view. [Live viewer page](https://claude.ai/artifact/UpQCDYnJCSAJb9FMzzSa2y) with Idle, Walk, Jump.

- **Time:** 101 min full deliverable; first model and first round at 91 min (Tested)
- **Rounds:** 79.4 → 79.7 → 79.9%
- **Cost:** $0
- **Size:** 32,519 triangles · 1.26 MB · 15 bones · 3 clips
- **Validator:** 0 errors, 0 warnings (Tested)
- **Checks:** Attached FAIL (cape hovers 0.7% of height behind the candy, up to 3% during the jump). Smooth PASS (Tested)
- **Quality:** Clean finish: smooth traced mask and eyes, pleated wrapper ends, cape behind the candy (not touching it). From the side the wrapper ends read as rounded cones (Tested).
- **Verdict note:** Slower than Wednesday. Measuring everything before building is what made Opus slow on Wednesday too (first model at 68 minutes). The heat map changed nothing here: it ran once the model was nearly done.

### B: rough model, heat map, fixes by eye

sealed Opus 5.5 worker · 9 rounds · **Never (as a variant)**

**Image:** `still_opus_heatmap_b.jpg`

Its own still, three-quarter view.

- **Time:** 14.8 min full deliverable; first model 6.4 min; 60% at 6.6 (Tested)
- **Rounds:** 63.7 → 59.8 → 59.5 → 64.5 → 59.1 → 62.4 → 65.0 → 64.8 → 64.5%
- **Cost:** $0
- **Size:** 30,376 triangles · 1.08 MB · 14 bones · 3 clips
- **Validator:** 0 errors, 2 warnings (unused texture data) (Tested)
- **Checks:** Both PASS: plain shapes have nothing to stair-step (Tested)
- **Quality:** Good body and leg proportions; the mask is a plain band, the eyes are generic, the wrapper ends are flat triangles (Tested).
- **Verdict note:** Fixing by eye did not converge: four of eight rounds scored worse. Knowing where the model is wrong is not enough without measuring the fix.

**Image:** `compare_same_view.jpg`

Same-view comparison. Top: each game file drawn straight from the front and lined up with the drawing, which is what the heat map scores. Bottom: the same flat renderer with the model turned 35°. Outlines come from the renderer, not the game files.

**Image:** `compare_def.jpg`

Runs D (with finishing pass), E (Opus, rules only) and F (Fable, rules only), same views as above.

**Image:** `elbow_false_alarm.jpg`

The smooth check's only flag on run E: a clean corner where the upper arm and forearm meet. A false alarm, the same spot run D's finishing pass "fixed".

**Image:** `smooth_c_vs_d.jpg`

Smooth check. Run C: red outlines are stair-stepped edges (mask, eyes, pupils, smile, swirl). Run D: none.

**Image:** `attached_c_vs_d.jpg`

Attached check. Run C: the right arm (magenta) touches nothing it hangs from; orange parts are near misses (fists hovering off the hips). Run D: the fists sit on the hips, as drawn.

**Image:** `heatmap_c_round1.jpg`

Run C, round 1 (4.4 min, 59.8%): the rough model by eye. Red squares and the numbered boxes are what the next round measured.

**Image:** `heatmap_c_final.jpg`

Run C, final (86.7%). What still fails: the wavy ruffled tips of the wrapper ends and the swirl inside the candy.

**Image:** `heatmap_wed_opus.jpg`

Wednesday's Opus, scored the same way (58.2%): wrapper ends too tall and spread, cape too long and low, legs straight where the drawing's are apart.

## 05 Use cases

### Now

- The Character maker: a rough model, heat-map rounds with measured fixes, build rules from the start, in about 30 minutes on Opus (Tested), one drawing.
- The lab's finish checks as a measuring stick for any character's game file (loose parts, stair-stepped edges); not a build step, and the smooth check false-alarms at limb joints (Tested).
- A number for "done": stop at 80% squares passing, in place of the model deciding it looks fine (Tested).
- An independent check of any character's game file against its drawing, including Meshy's, as long as the colours are not painted in a texture (Tested) on code characters only.

### Later

- Fable 5.1: tested with the loop (run F) and shelved by Charles's choice of Opus only.
- Jev as the judge of each square, compared with the plain arithmetic used here, once a free or approved route exists (Assumed).
- A heavier weight on face squares, so the score tracks what people notice first (Assumed).

### Cannot

- Judge the back or the side: it sees the front only. The three-quarter still and Charles's eye cover the rest.
- Judge which details matter most: every square counts the same.
- Read painted textures: models with colour painted into an image (Meshy's) are scored on shape only.

## 06 Requirements check (family arcade)

The family-arcade speed run lists no standing requirements yet; these are Charles's stated goals for its characters.

| Requirement | Answer | Path |
| --- | --- | --- |
| Characters walk, run, jump | · **Yes** | All three runs baked idle, walk and jump into a validated .glb (Tested). Run is one more move (Assumed). |
| Revisions through a Claude-side overlay | · **Yes** | Colours and sizes stay named constants at the top of the file in all three runs (Tested); traced outlines are lists of points further down, so a look change to those is a re-trace, not a slider (Assumed). |
| Results while the boys wait | · **Yes** | About 30 minutes on Opus with the full workflow, down from about 80 (Tested), one drawing. |
| Finished look: smooth edges, nothing floating | · **Yes** | Build rules from the first part, no check pass (Tested) (run E attached and smooth, measured afterwards; runs A, C and Wednesday's Opus each fail one or both checks). |
| Likeness without Charles steering | · **Partly** | The score gives a stop line the model cannot argue with (Tested); small face details still need the checklist or Charles's eye (Tested) (run B). |

## 07 Risks and cover

- **One drawing, one run each.** Run C's 18.5 minutes may not repeat. Cover: the second-drawing proof already planned for TH-092 runs this loop.
- **The tool was tuned on this drawing.** Its limits and line-up were set while scoring Super Sweets. Cover: check the calibration again on the second drawing (Wednesday's order still holds) (Assumed).
- **Teaching to the test.** A model could flatten itself to please the front view. Cover: the brief forbids it and the three-quarter still and back view are checked; none of the three runs did it (Tested).
- **Score is not likeness.** Run B outscored Wednesday's Opus with a cruder face. Cover: the likeness checklist and Charles's eye stay the final check.
- **Stair-stepped shapes and loose parts.** Run C had both. Cover: the build rules from the first part; runs D and E came out attached and smooth (Tested).
- **The checks were tuned on these four characters.** Their limits may need adjusting on a very different drawing (a spiky or furry character). Cover: re-check the limits on the second drawing (Assumed).
- **File size.** Runs D and E sat at the 2 MB cap; on the arcade's Three.js 0.160.0 the same E code comes out 2.22 MB (capsules carry more triangles). Cover: a triangle budget in the build rules, read from round 1: run E's code at the budget is 1.78 MB with the same score (Tested).

## 08 If adopted

- **What got built:** in this chat, at Charles's word: the Character maker section of the game-maker skill (0.4.0) and the 2D-3D Maker tool folder beside it, written from run E, with the earlier decisions (character file shape, no outlines in the .glb, validator, size cap, log, face checklist) carried over. Tested on run E's character under the arcade's Three.js 0.160.0, in the viewer and in both game routes (code shape and .glb slot).
- **Dollars:** $0.
- **Charles's hours:** none beyond judging each new character.
- **Proof of done:** a second, different drawing through the Character maker: full character in under 40 minutes, at least 80% of squares passing, attached and smooth, and Charles judges the face right.

---

## 09 Sources

- No Discovery Brief (the heat map was designed in this chat). Prior R&D Report: [Drawing to Game Character - Claude](https://claude.ai/artifact/Jm3p7XfuapinN85DPvQ7j9) (2026-10-24), filed at `lab/reports/drawing-to-game-character-claude.md`.
- Total Harness handoff and addenda: TH-092 (Claude code characters), TH-093 (guardrails), TH-094 (naming and placement), TH-095 (locked workflow), TH-096 (finishing pass dropped).
- Wednesday's run files: `lab/claude-image-to-3d/opus/` and `fable/` in Chooch333/kids-games (private), rebuilt here for the baseline.
- [Three.js documentation](https://threejs.org/docs/) · [Khronos glTF Validator](https://github.com/KhronosGroup/glTF-Validator)
