---
title: "Tech card: ArtCraft Crafting Apps"
reviewed: 2026-10-09
tools: [effectcraft, vectorcraft, filmcraft, photocraft, designcraft, pdfcraft, lightcraft]
draft: true
---
Reviewed 2026-10-09 · first card in the new format · draft, verdict on hold

**Verdict: adopt two of the seven apps now, as a pinned trial for the motion-graphics half of the speed run. Shelf three. Never for two.**

## What it is

Seven free desktop apps from the ArtCraft team, each a from-scratch copy of an Adobe program. ✓ Every one can be run by Claude through typed commands or a direct connector, with no screen, and saves its work as a file a person can also open in the app and adjust by hand. ✓

## Verdict by app

| App | Copies | Verdict | Why | Come back when |
|---|---|---|---|---|
| [EffectCraft](https://github.com/storytold/effectcraft) | After Effects (motion graphics) | **Adopt now, as a trial** | Passed a hands-on test. Serves the speed run. Free for company use. | |
| [VectorCraft](https://github.com/storytold/vectorcraft) | Illustrator (drawings, diagrams) | **Adopt now, as a trial** | Passed a hands-on test. Opens CAD exchange files. Free. | |
| FilmCraft | Premiere (video editing) | **Shelf** | Could cut renders, graphics and sound into one video. Claude's workspace already joins picture and sound, so there is no need yet. Untested. | A speed-run piece needs a real multi-clip edit. |
| PhotoCraft | Photoshop (image editing) | **Shelf** | Could touch up renders. Still an early alpha. | It leaves early alpha, or a render needs touch-up Claude cannot do in code. |
| DesignCraft | InDesign (page layout) | **Shelf** | Could lay out proposal pages. Outside the speed run. | You open a proposal-pages use case. |
| PdfCraft | Acrobat (PDF handling) | **Never** | Claude already reads, splits and merges PDFs. Early alpha. | It does something Claude's built-in PDF tools cannot. |
| LightCraft | Lightroom (photo library) | **Never** | Nothing in the harness manages camera photos. | Photography becomes a harness domain. |

"Trial" means a fixed version, used for the speed run, with a fallback named below. It is not yet the harness's permanent motion tool.

## Where it fits in the harness

- **Layer:** Digital hands (layer 2). It covers pipeline step 6, make it on screen, and helps step 7, check it on screen, because it hands Claude finished frames to look at.
- **What it replaces:** step 3 of the blueprint's "Motion graphics and film" plan, which reads "flat animation is written as code." ✓ That step was a guess marked ~ in the blueprint. This is a tested answer for it.
- **Why the blueprint missed it:** EffectCraft's first commit was October 1, 2026, the same week the blueprint was written. ✓ It did not exist to be considered.
- **Blocks it touches:** 16 (one skill per tool pack), 17 (rubric per domain) and 19 (pre-approved command list). All three are in the digital sweep and not started.
- **What it needs from the harness:** only block 2, the standard project folder, which is done. It runs in the cloud with no PC, no graphics card, no keys and no cost. ✓✓ So it does not have to wait for blocks 3 to 6.

## What we could use it for

**Now, for the speed run**

1. Animated phasing and sequencing charts, title cards and name captions for work. ✓✓ A simple one was built and rendered.
2. A finishing station for renders. Once a still render exists, EffectCraft can add a slow camera drift, finish labels, before-and-after wipes and titles, then put out one clip. This ties the two halves of the speed run together. ~ Bringing images and video into it in the cloud is untested.
3. Phasing drawn over the real site plan. VectorCraft opens DXF, the exchange format CAD programs export, so a plan could come in as clean linework and be animated phase by phase. ~ Untested with a real drawing.
4. Titles with a see-through background, to lay over walkthrough video. ✓ The format is supported. ~ Untested.

**Later, across the harness**

5. Small web animations for your apps. ✓✓ The lightweight web format exported cleanly at 15 KB.
6. Graham's animation work. The file opens in a normal-looking app, so he can adjust it by hand instead of editing code.
7. Flat shapes for making: draw a name plate or sign in VectorCraft, then give it thickness in the geometry stack (block 7) for printing. ~
8. Cut files for laser or vinyl through the fabrication accounts (block 14). ~
9. The harness's own diagrams and explainer graphics.

**What it cannot do**

It cannot make the building image. Its 3D is flat cards arranged in space, the way After Effects does it, not a building model. ✓ The render half of the speed run needs a different tool and its own review.

## What we checked

The hands-on rows were run in the ArtCraft chat earlier today. I read that record; I did not re-run them here.

| Question | Finding | Confidence |
|---|---|---|
| Price and license | Free. EffectCraft is under MIT or Apache-2.0, both of which allow company use at no charge. The maker's site says all seven apps carry permissive licenses. | ✓ |
| How old is it | EffectCraft's first commit was October 1, 2026. It is eight days old, at version 0.6.0, with about 1,000 changes logged and 100 open issues. | ✓ |
| What the makers say | It "isn't yet a replacement for After Effects on client work." Nothing yet checks its output against After Effects. | ✓ |
| Which computers | Mac is the most tested. The makers report basic bugs for Linux and Windows users. Claude's cloud workspace is Linux; your laptop is Windows. | ✓ |
| Can Claude run it with no screen | Yes. Both apps installed in the cloud workspace. Claude built a 7-second phasing chart and a title card by script, rendered the video in 15 seconds, and checked its own frames. | ✓✓ |
| Does it follow a method Claude knows | Yes. It accepts After Effects' own scripting style, which is long established and heavily documented. | ✓✓ |
| What comes out | Video, video with a see-through background, GIF and web animation from EffectCraft. SVG, PDF and PNG from VectorCraft. An editable project file with each. | ✓✓ for video, web animation, PDF, PNG; ✓ for the rest |
| Quality on richer work | Not tested. Only a clean, simple piece was made. Particles, 3D camera moves and longer pieces are unknown. | ~ |
| Does it last between sessions | No. The apps vanish when the session ends. It needs a permanent setup. | ✓✓ |

The age is the finding the earlier chat missed. It does not kill the verdict, but it is why the verdict says trial.

## What else does this job

This is the comparison the ArtCraft chat still owed. It is a comparison of facts. I did not build the same piece in each tool.

| Option | Cost for FA Wilhelm work | Can a person adjust the result by hand | How proven |
|---|---|---|---|
| EffectCraft and VectorCraft | Free ✓ | Yes, in an app laid out like Adobe's ✓ | Eight days old ✓ |
| [Remotion](https://www.remotion.dev/docs/license/pricing) | Paid. Free only for individuals and companies of up to three people. A larger company needs a license, $25 a seat a month with a $100 a month minimum. ✓ | Only by editing code | Established. Said to publish its own guidance for AI agents. ~ one secondary source |
| Motion Canvas | Free, open source ✓ | Only by editing code | Established. One source says its direction now follows a paid editor built on it. ~ |
| Claude writing animation code directly (today's method) | Free | Only by editing code | Works today ✓ but rebuilds every effect from nothing each time |

What decides it: EffectCraft is the only option that is both free for company work and leaves a file a non-programmer can open. Remotion is the mature choice but triggers a money stop for work use. Motion Canvas is the free fallback if EffectCraft stalls.

## Risks and how each is covered

| Risk | Cover |
|---|---|
| An eight-day-old tool changes its commands or breaks. | Fix on version 0.6.0 and keep our own copy of the installers. The license allows it. Upgrade only on purpose. |
| The project stalls or is dropped. | Nothing is locked in. Outputs are standard video, web and print formats. The craft guide and templates are written so they carry over to Motion Canvas. |
| Output looks tidy but generic. | The written craft guide is the real quality lever, as the earlier animation work found. It is part of the build, not an extra. |
| A work piece goes out with a flaw. | During the trial, every work piece gets your eye before it leaves. The makers themselves do not yet call it ready for client work. |
| Linux bugs in the cloud workspace. | The self-review step looks at rendered frames before anything is delivered. The one hands-on test hit no Linux bug; its single fix was to Claude's own script. ✓✓ |

## If adopted: what Total Harness builds

One motion pack, scoped by a Total Harness chat as a single Build Brief. It is the first tool pack, so it also sets the pattern for blocks 16, 17 and 19.

1. **Setup script.** Installs both apps at the fixed version and checks the downloads are genuine.
2. **Connector hookup.** So Claude drives the apps directly, not only by script.
3. **Craft guide.** The rulebook for timing, movement, layout and color. This is the block 17 rubric for motion graphics.
4. **Work template.** FA Wilhelm colors, fonts and reusable pieces: title card, phasing chart, name caption. Needs your brand files.
5. **Self-review loop.** Claude lays out sample frames, grades them against the craft guide, fixes, then delivers video plus the editable file.
6. **Skill and command list.** One skill that tells any session how to use the pack, and the list of commands you approve once.

| Item | Detail |
|---|---|
| Dollars | $0 |
| Your time | About 15 minutes: send brand files, react to the first piece. ~ my estimate |
| Proof of done | A brand-new session, given one sentence, delivers a branded 20-second phasing animation and its editable file with no manual setup. |
| Not included | The render half of the speed run. The other five apps. |

## Sources

All opened October 9, 2026.

- [Crafting Apps overview](https://getartcraft.com/apps): the seven apps, status of each, license statement
- [EffectCraft on GitHub](https://github.com/storytold/effectcraft): license, first-commit date, maker's own limits, platform notes
- [Remotion license and pricing](https://www.remotion.dev/docs/license/pricing)
- [Remotion's comparison with Motion Canvas](https://www.remotion.dev/docs/compare/motion-canvas)
- [Wireflow: Remotion alternatives](https://www.wireflow.ai/blog/best-remotion-alternatives-in-2026) and [Moda: Remotion alternatives](https://moda.app/blog/remotion-alternatives): the two ~ claims in the comparison
- [ArtCraft chat Working Document](https://claude.ai/code/artifact/5e7fe3db-3bdb-4a12-b9e5-9f686af2240a): the hands-on test record
- Total Harness blueprint, "Domain step plans" tab, and Project State project total-harness: harness fit and status
