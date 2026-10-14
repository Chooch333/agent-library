---
title: "Flythrough Renderer - Blender"
type: rd-report
reviewed: 2026-10-14
test_date: 2026-10-13
test_completed: 2026-10-13
status: complete
tools: [blender-cycles-pc, blender-eevee]
report_url: https://claude.ai/artifact/YHCc81fEgUQPHVEfskYUEc
clips:
  - env: Cycles on the PC graphics card
    anchor: cycles-pc
    file: clip_cycles_pc.mp4
  - env: Cycles in the cloud
    anchor: cycles-cloud
    file: clip_cycles_cloud.mp4
  - env: EEVEE on the PC graphics card
    anchor: eevee-pc
    file: clip_eevee_pc.mp4
  - env: EEVEE in the cloud
    anchor: eevee-cloud
    file: ""
image: frame093_compare.png
clips_home: "Charles's PC, Documents\\flythrough-test\\clips\\ (also published with the report at report_url)"
draft: false
---
# Flythrough Renderer
## Blender 4.5.14 (PC) · 5.2.2 (cloud)

**Test problem:** Study the output quality and speed of Blender for architectural flythroughs.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-13 | 2026-10-13 | Complete |

**Rev history**
0. 2026-10-13 · First draft (tech card format)
1. 2026-10-13 · Reformatted as R&D Report; one clip per test environment
2. 2026-10-14 · Blender versions in title; Cycles on PC adopted

Evidence key: **Tested** = we ran it and measured it · **Published** = from the maker's own documentation · **Assumed** = our judgment, not yet checked.

## 01 Tech description
**Blender** is a free, open-source 3D program (GPL license, fine for company use) (Published). Claude drives it entirely by script, with no one clicking (Tested). It has two render engines:
- **Cycles** traces real light. It's the photo-like look approved for the arch-renders stills on 2026-10-10.
- **EEVEE** draws like a video game engine. It's faster to set up and less true to light.

A **flythrough** is the same 3D scene rendered as hundreds of still frames, 24 per second of video, with the camera moving a little each frame.

## 02 Findings
Blender Cycles on the graphics card in Charles's home PC makes a photo-like flythrough fast enough to use. A 20-second clip takes about **1.9 hours**, unattended, at no cost. The cloud workspace has no graphics card and needs about **13.4 hours** for the same clip, so it isn't practical. EEVEE is only slightly faster than Cycles on the PC (11.3 vs 14.1 seconds a frame) and looks clearly worse: blank windows and flatter light. In the cloud it couldn't render the scene at all: it ran out of memory. Cycles on the PC is the route to adopt.

**Key numbers**
- **14.1 s** · per frame, Cycles on the PC graphics card (Tested)
- **≈ 7×** · faster than Cycles in the cloud on the same frames (Tested)
- **1.9 h** · for a 20 s clip (480 frames) on the PC, from the measured rate

### Inputs the workflow must supply
- A 3D model with materials assigned: the Pascal export, every wall, window and door a named part.
- The site kit: textures, tree models and sky image, stored on the PC.
- A camera move picked from a standard set, such as walk-up, orbit or rise to aerial.
- A render preset: 1280×720, 16 samples, denoise on, Cycles on the graphics card.

### Harness the Total Harness project needs to build
- A **clip step** in the arch-renders run. It renders frames on the PC's card, joins them into an MP4, and hands the MP4 to the motion layer for titles and callouts.
- A **standard camera-move set** kept as conventions data.
- A **storyboard stop**: first, middle and last frame of each move (about 45 s) for review before the full clip.
- **Blender 5.2 on the PC**, so the distance haze renders.
- A rule that keeps the PC awake for the roughly 2-hour job.

## 03 Experiment parameters
We created a 5-second flyby of the test model and compared it across Blender's environments to measure speed and quality. Every environment rendered the same scene, the same camera move and the same settings. Only the engine and the machine changed.

**Test model:** The render-lab house from 2026-10-10, the scene approved for stills. It has Poly Haven brick, stone, slate, siding and lawn textures; modeled windows, trim and gutters; 3D grass; about 150 trees; and an HDRI sky with an aimed sun.

**Camera move:** Street eye level (1.6 m) rising and swinging out to the three-quarter aerial (6.5 m). The move is defined over 480 frames (20 s). The test renders every 4th frame, so the 5-second clip shows the whole move at 4× speed.

**Output:** 1280×720 at 24 frames per second. The PC clips are 120 frames (5 s). The cloud clips are 24 frames (the first 1 s), because a full 5 s cloud clip takes about 3.4 hours.

**Render settings:** Cycles: 16 samples with adaptive sampling and denoising, and the same light bounces and color look as the approved stills. EEVEE: 32 samples, shadows and ray tracing on.

**Machines:** **PC:** Charles's laptop. Intel i7-10850H, NVIDIA Quadro T2000 (4 GB), Blender 4.5.14. Cycles used NVIDIA OptiX, the card's fast ray-tracing mode (Tested). **Cloud:** Claude's workspace. 2-core Intel Xeon, no graphics card, Blender 5.2.2.

**Blender versions:** The first two numbers name the release series and the last is the bug-fix update: 4.5.14 is the 14th fix of the 4.5 series, and 5.2.2 is the 2nd fix of the 5.2 series. Both are LTS (long-term support) releases (Tested). The PC has 4.5 because that's what was installed for the SINNON test; the cloud uses 5.2. Rendering works the same in both. The one difference seen here is the distance haze, which the script builds a 5.x way and 4.5 skips. The PC's roughly 7× speed lead comes from its graphics card, not its version (Assumed). Installing 5.2.2 on the PC puts both machines on one version.

**What we measured:**
- **Time:** seconds per frame from Blender's own timer, logged for every frame.
- **Flicker:** consecutive frames compared pixel by pixel on flat surfaces (roof, brick).
- **Memory:** peak graphics memory on the PC.
- **Quality:** the same frame (frame 93) compared side by side across all four environments.
- **Failures:** memory use tracked when a run stopped.

**Side checks:**
- **Higher quality:** 64 samples on the PC card took 38 s a frame (Tested).
- **Simpler scene** (boxes, glass, trees) at 64 samples: PC card 11.3 s, PC processor 41 s, cloud 126 s (Tested).

**Saved test files:** All on Charles's PC, private, in `Documents\flythrough-test\`:
- `house_anim.py`: the scene and timing script, built from the lab's `house.py` plus the camera move.
- `assets\`: the textures and tree models the script reads.
- `clip_frames\` and `clip_eevee\`: the PC clips as frame images.
- `house_out\`: comparison frames.

## 04 Results by test environment

### Cycles on the PC graphics card
NVIDIA Quadro T2000 · OptiX · 16 samples · **Adopt now**
- **Clip:** `clip_cycles_pc.mp4`, 5 s, 120 frames
- **Per frame:** 14.1 s (13.3–19.0) (Tested)
- **This clip:** 28.2 min
- **20 s clip:** ≈ 1.9 h
- **Cost:** $0. Runs on hardware already owned.
- **Quality:** Photo-like and matches the approved stills. No speckle or flicker on flat surfaces (Tested). Missing the distance haze (Blender 4.5 on the PC). Leaves and grass should be judged by eye (Assumed).
- **Memory:** Peak about 0.8 GB of the card's 4 GB (Tested)
- **Verdict note:** Adopted 2026-10-14: Charles watched the clip and said he'd use it.

### Cycles in the cloud
2-core Xeon · no graphics card · 16 samples · **Never (for clips)**
- **Clip:** `clip_cycles_cloud.mp4`, first 1 s, 24 frames
- **Per frame:** 100.5 s (97.7–112.4) (Tested)
- **This clip:** 40.2 min for 24 frames
- **20 s clip:** ≈ 13.4 h (a 5 s clip ≈ 3.4 h)
- **Cost:** $0
- **Quality:** Same Cycles look as the PC. It includes the distance haze, because the cloud runs Blender 5.2.
- **Verdict note:** Too slow for clips. Stills stay here as settled (TH-051). This would change if the cloud workspace gained a graphics card.

### EEVEE on the PC graphics card
Quadro T2000 · 32 samples · **Never**
- **Clip:** `clip_eevee_pc.mp4`, 5 s, 120 frames
- **Per frame:** 11.3 s, after a 62 s warm-up on frame 1 (Tested)
- **This clip:** 23.4 min
- **20 s clip:** ≈ 1.5 h
- **Cost:** $0
- **Quality:** Game-like. Windows read as blank glass, and the light is flatter under the eaves and in the trees (Tested).
- **Verdict note:** It saves only about 20% of the time over Cycles for a clearly weaker look. This would change if a much heavier real building makes Cycles far slower than EEVEE.

### EEVEE in the cloud
2-core Xeon · software graphics · 32 samples · **Never**
- **Clip:** none. The render failed before frame 1.
- **Per frame:** No frame finished (Tested)
- **This clip:** Failed twice. Blender was shut down for running out of memory (over 5.5 GB of the workspace's 7 GB) while preparing frame 1.
- **20 s clip:** Not possible on this scene
- **Cost:** $0
- **Quality:** Not measurable on the test house. On the simpler box scene it worked, at 37 s a frame (Tested).
- **Verdict note:** With no graphics card, EEVEE has to imitate one in software, which is slow and memory-hungry. This would change if the cloud workspace gained a graphics card.

**Comparison image:** `frame093_compare.png`. The same frame (93) from each environment. The cloud Cycles frame shows the distance haze; the PC frames don't (Blender 4.5). EEVEE in the cloud produced no frame.

## 05 Use cases
**Now**
- True 3D camera moves for the 20–30 s piece: street walk-up rising to the aerial, orbit, entry approach. One move tested (Tested).
- Storyboard frames before any motion. A key frame takes about 14 s, so a full storyboard costs minutes (Tested).
- Faster still checks: a 64-sample 720p frame takes 38 s on the card, against 12–15 min for a full still in the cloud (Tested).

**Later**
- Phasing, with building parts appearing over time, and finish swaps inside a camera move. Blender can keyframe both (Assumed).
- Construction over time: Blender does the 3D and the motion layer adds the month tracker (Assumed).
- Game trailers for the kids' games (Assumed).

**Cannot**
- Render while the PC is asleep or off.
- Titles, labels and month counters. That's the motion layer's job, not Blender's.
- Very large scenes may not fit in the card's 4 GB (Assumed).

## 06 Requirements check (arch renders)
| Requirement | Answer | Path |
|---|---|---|
| 1. Conventions | Yes | Camera moves are keyframes in a script, so a fixed set can live in the conventions data the render step already reads. One move tested (Tested); the set is not built yet. |
| 2. Storyboard before motion | Yes | Render each move's first, middle and last frames (about 45 s) for review before the full clip (Tested, timing). |
| 3. Menu of motion pieces | Partly | Phasing and finish swaps can be keyframed (Assumed). The month tracker and labels belong to the motion layer. |
| 4. Graphics quality | Yes | Same Cycles look as the approved stills. 16 samples on the card matches 16 samples in the cloud (Tested). Haze needs Blender 5.2 on the PC. |

## 07 Risks and cover
- **The PC must stay awake for about 2 hours a clip.** Cover: run clips overnight or while away, with sleep turned off during the job.
- **Heat slowdown.** Frames slowed from 11 s in short runs to 14.1 s over the 28-minute clip (Tested). Cover: plan on 14 s a frame.
- **Real buildings are heavier than the test house.** Cover: time 10 frames of the first Pascal model before committing to a full clip.
- **The card's 4 GB memory.** Cover: cut tree count or texture size if a scene doesn't fit.

## 08 If adopted
- **What gets built:** the harness in Findings, built by the Total Harness project.
- **Dollars:** $0.
- **Charles's hours:** about 15 minutes, to approve the Blender 5.2 install and the no-sleep setting (Assumed).
- **Proof of done:** a 20 s clip of a real Pascal building, rendered unattended on the PC in under 2 hours, with no visible flicker, that Charles would use.

## 09 Sources
- Test logs and frames: `Documents\flythrough-test\` on Charles's PC (the PC runs) and Claude's workspace (the cloud runs), 2026-10-13.
- Baseline: arch-render skill 0.2.0 and decision TH-051 (2.8 min a frame for animation, 12–15 min a still in the cloud).
- [Blender hardware requirements](https://www.blender.org/download/requirements/) · [Blender license](https://www.blender.org/about/license/)
- [Blender manual: GPU rendering (OptiX)](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html)
