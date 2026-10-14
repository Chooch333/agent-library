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
    file: clip_cycles_pc.mp4
  - env: Cycles in the cloud
    file: clip_cycles_cloud.mp4
  - env: EEVEE on the PC graphics card
    file: clip_eevee_pc.mp4
  - env: EEVEE in the cloud
    file: ""
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
Blender is a free, open-source 3D program. Its GPL license is fine for company use (Published). Claude drives it entirely by script (Tested). It has two render engines:
- **Cycles** traces real light. This is the photo-like look approved for the arch-renders stills.
- **EEVEE** draws the way a video game does: faster to set up, less true to light.

A flythrough is one scene rendered as hundreds of still frames, 24 per second of video, with the camera moving a little each frame.

## 02 Findings
Blender Cycles on the graphics card in Charles's home PC makes a photo-like flythrough fast enough to use. A 20-second clip takes about **1.9 hours**, unattended, at no cost. The cloud workspace has no graphics card and needs about **13.4 hours** for the same clip, so it isn't practical. EEVEE is only slightly faster than Cycles on the PC (11.3 vs 14.1 seconds a frame) and looks clearly worse: blank windows and flatter light. In the cloud, EEVEE couldn't render the scene at all because it ran out of memory. Cycles on the PC is the route to adopt.

- 14.1 s per frame, Cycles on the PC graphics card (Tested)
- About 7× faster than Cycles in the cloud on the same frames (Tested)
- 1.9 h for a 20 s clip (480 frames), from the measured rate

**Inputs the workflow must supply**
- A 3D model with materials assigned: the Pascal export, with every wall, window and door as a named part.
- The site kit: textures, tree models and sky image, stored on the PC.
- A camera move from a standard set: walk-up, orbit, or rise to aerial.
- A render preset: 1280×720, 16 samples, denoise on, Cycles on the graphics card.

**Harness the Total Harness project needs to build**
- A clip step in the arch-renders run. It renders frames on the PC's card, joins them into an MP4, and hands the MP4 to the motion layer for titles and callouts.
- A standard camera-move set, kept as conventions data.
- A storyboard stop: the first, middle and last frame of each move (about 45 s to render) for review before the full clip.
- Blender 5.2 on the PC, so the distance haze renders.
- A rule that keeps the PC awake for the roughly 2-hour job.

## 03 Experiment parameters
We made a 5-second flyby of the test model in each Blender environment and compared speed and quality. Every environment rendered the same scene, camera move and settings. Only the engine and the machine changed.

| Parameter | Value |
|---|---|
| Test model | The render-lab house from 2026-10-10, the scene approved for stills: Poly Haven textures, modeled windows and trim, 3D grass, about 150 trees, HDRI sky with an aimed sun |
| Camera move | Street eye level (1.6 m) rising to the three-quarter aerial (6.5 m), defined over 480 frames. Every 4th frame was rendered, so the 5 s clip shows the whole move at 4× speed |
| Output | 1280×720 at 24 fps. PC clips: 120 frames (5 s). Cloud clips: 24 frames (the first 1 s), because a full 5 s cloud clip takes about 3.4 h |
| Render settings | Cycles: 16 samples, adaptive sampling, denoise, the same light bounces and look as the stills. EEVEE: 32 samples, shadows and ray tracing on |
| Machines | PC: Intel i7-10850H, NVIDIA Quadro T2000 (4 GB), Blender 4.5.14, Cycles on OptiX (Tested). Cloud: 2-core Xeon, no graphics card, Blender 5.2.2 |
| Blender versions | In 4.5.14, "4.5" is the release series and ".14" is the 14th bug-fix update; 5.2.2 is the 2nd fix of the 5.2 series. Both are long-term-support releases (Tested). Rendering works the same in both. Only the distance haze differs, and 4.5 skips it. The PC's speed lead comes from its graphics card, not its version (Assumed) |
| What we measured | Seconds per frame from Blender's timer; frame-to-frame flicker on flat surfaces; peak graphics memory; one frame (93) compared across all environments; memory when a run failed |
| Side checks | 64 samples on the PC card: 38 s a frame. Simpler box scene at 64 samples: PC card 11.3 s, PC processor 41 s, cloud 126 s (all Tested) |
| Saved test files | On Charles's PC (private), `Documents\flythrough-test\`: `house_anim.py` (scene and timing script), `assets\`, `clip_frames\`, `clip_eevee\`, `clips\` |

## 04 Results by test environment
| Environment | Verdict | Per frame | This clip | 20 s clip | Cost | Quality | Clip |
|---|---|---|---|---|---|---|---|
| Cycles on the PC graphics card | Adopt now | 14.1 s (13.3–19.0), Tested | 28.2 min | ≈ 1.9 h | $0 | Photo-like; matches the stills; no flicker on flat surfaces; missing the haze (4.5) | clip_cycles_pc.mp4 |
| Cycles in the cloud | Never (for clips) | 100.5 s (97.7–112.4), Tested | 40.2 min for 24 frames | ≈ 13.4 h | $0 | Same look, with haze | clip_cycles_cloud.mp4 |
| EEVEE on the PC graphics card | Never | 11.3 s after a 62 s first frame, Tested | 23.4 min | ≈ 1.5 h | $0 | Game-like; blank windows; flatter light | clip_eevee_pc.mp4 |
| EEVEE in the cloud | Never | No frame finished, Tested | Failed twice: out of memory (over 5.5 GB of 7 GB) | Not possible | $0 | Not measurable | none |

Verdict notes:
- **Cycles on PC:** adopted 2026-10-14. Charles watched the clip and said he would use it.
- **Cycles in cloud:** still the route for stills (TH-051), but too slow for clips. It would change if the cloud workspace got a graphics card.
- **EEVEE:** saves only about 20% of the time for a clearly weaker look. It would change if a much heavier building makes Cycles far slower than EEVEE.

## 05 Use cases
**Now**
- True 3D camera moves for the 20–30 s piece (one move tested).
- Storyboard frames before any motion, at about 14 s each.
- Faster still checks: 38 s for a 64-sample 720p frame on the card.

**Later** (Assumed)
- Phasing and finish swaps inside a camera move.
- Construction over time, with the month tracker added by the motion layer.
- Game trailers.

**Cannot**
- Render while the PC is asleep.
- Titles or labels (that's the motion layer).
- Possibly very large scenes on the card's 4 GB.

## 06 Requirements check (arch renders)
| Requirement | Answer | Path |
|---|---|---|
| 1. Conventions | Yes | Camera moves are script keyframes, so a fixed set can sit in conventions data. One move tested |
| 2. Storyboard before motion | Yes | First, middle and last frame of each move (about 45 s) before the full clip |
| 3. Menu of motion pieces | Partly | Phasing and finish swaps can be keyframed (Assumed). The tracker and labels belong to the motion layer |
| 4. Graphics quality | Yes | Same Cycles look as the approved stills. Haze needs Blender 5.2 on the PC |

## 07 Risks and cover
- **PC awake for about 2 h a clip.** Run clips overnight, with sleep off during the job.
- **Heat slowdown** (11 s in short runs, 14.1 s over a full clip, Tested). Plan on 14 s a frame.
- **Real buildings are heavier.** Time 10 frames of the first Pascal model before committing to a full clip.
- **The card's 4 GB of memory.** Cut tree count or texture size if a scene doesn't fit.

## 08 If adopted
- **What gets built:** the harness in Findings, built by the Total Harness project.
- **Dollars:** $0.
- **Charles's hours:** about 15 min to approve the Blender 5.2 install and the no-sleep setting.
- **Proof of done:** a 20 s clip of a real Pascal building, rendered unattended on the PC in under 2 h, with no visible flicker, that Charles would use.

## 09 Sources
- Test logs and frames: Charles's PC (`Documents\flythrough-test\`) and Claude's workspace, 2026-10-13.
- Baseline: arch-render skill 0.2.0; decision TH-051.
- https://www.blender.org/download/requirements/ · https://www.blender.org/about/license/ · https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
