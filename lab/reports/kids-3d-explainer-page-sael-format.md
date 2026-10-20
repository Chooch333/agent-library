---
title: "Kids' 3D Explainer Page - sael.net format"
type: rd-report
brief: ""
reviewed: 2026-10-20
test_date: 2026-10-19
test_completed: 2026-10-19
status: complete
tools: [sael-explainer-format]
report_url: https://claude.ai/artifact/PvX1Nc8rrUNrcy3Pc5mous
clips:
  - env: Env A · one-shot, his method
    anchor: env-a
    file: page_oneshot_cloud.html
  - env: Env B · page kit, then build
    anchor: env-b
    file: page_kit_cloud.html
  - env: Env C · page kit, cheaper model
    anchor: env-c
    file: page_kit_sonnet_cloud.html
image: compare_prism_room.jpg
clips_home: "Chooch333/family-arcade, lab/prism-room/ (private); the three pages are also published as private artifacts linked from report_url"
draft: false
---
# Kids' 3D Explainer Page
## sael.net format · Prism Room rebuild · Three.js 0.183.2

**Test problem:** Study how close Claude gets to recreating Prism Room, in the sael.net format, from a written spec of the page rather than its code, and what that costs.

| Test date | Test completion date | Report status |
|---|---|---|
| 2026-10-19 | 2026-10-19 | Complete |

**Rev history**
0. 2026-10-19 · First draft, three environments
1. 2026-10-20 · Approved. Env A adopted; one shelf row for the format; test files to family-arcade

Evidence key: **Tested** = we ran it and measured it · **Published** = from the maker's own page or posts · **Assumed** = our judgment, not yet checked.

## 01 Tech description
**The sael.net format** is a way of making interactive 3D explainers: one self-contained web page per topic, drawn in real time in the browser with **Three.js** (a free, MIT-licensed library that draws 3D on the graphics card), in a fixed house style: a dark scene, a short text panel, number keys for preset states, `C` for cinematic cameras, `R` reset, `/` to hide the interface, drag to orbit, WASD to walk, and a "how it works" dialog that says what is exact and what is theatre. Ryan Sael's collection has 64 pieces; **Prism Room** (a lamp, a glass prism, a spectrum on a screen, with the real glass physics) is the one we rebuilt (Published). He builds each piece with an AI in one long run (Published).

### How it runs
- **Where:** in the viewer's browser on the viewer's graphics card; nothing on a server. Claude writes the page in the cloud session (Tested).
- **Subscription:** none. Build time is Claude usage inside the plan (Tested). His yardstick for one piece: Opus 5.5, 86 minutes, $25.66 of API (Published).
- **Cost to run:** $0 a view; static files (Published).
- **How Claude controls it:** Claude writes the whole page as code and checks it in a headless browser (a browser with no screen) with a check script; a real screen is needed only to judge the look and the frame rate (Tested).
- **What it needs:** a browser with WebGL. No account, no login, no captcha (Tested).
- **Licence:** the format and Three.js, fine for a company. His pages: no licence posted; "open source, soon" (Published). Our pages were built from a written spec and never read his code, so they are ours (Tested).
- **His delivery, read off the live page:** 126 KB of HTML with a 107 KB built-and-minified script (not readable source), Three.js 0.183.2 served from his own site as a 236 KB bundle with nine add-ons, a 20 KB site script (recommendations, view counter, analytics), and a 309 KB font (Tested).

## 02 Findings
Claude can rebuild a piece in the sael.net format from a written spec, with the physics exact and every house convention working, in **about 45 minutes** of unattended build time at no cost beyond plan usage. The one-shot route (env A) passed all 19 checks and matched the real glass maths to a tenth of a degree. The page-kit route (env B) also passed 19 of 19 and looked better in places, but was not faster, and the kit itself had three faults the builder had to work around. A cheaper model on the kit (env C) looked the most like the original but faked the four preset setups and left a debug line in, so it fails the bar without a hard check gate. Frame rate is the weak spot of the whole format: the original runs at 7 to 20 frames a second on Charles's laptop, and ours are no better. The route to adopt is the one-shot build from a spec plus the check script, with the conventions folded into Build 42's starter kit rather than a second kit.

**Key numbers**
- **19 / 19** · checks passed by the one-shot build (env A), physics exact at all four presets (Tested)
- **45 min** · wall clock for the one-shot build, unattended, while two other builds shared the machine (Tested)
- **7–20 fps** · the original Prism Room on Charles's laptop (integrated Intel graphics) (Tested)

### Inputs the workflow must supply
- A spec in words: the scene, what the viewer can change, the preset states, the exact facts and their source (here: the glass data and Snell's law), the key legend, the layout, the look.
- A reference image for the look.
- The house conventions, kept in one place and reused by every page.
- The check script's hook: a small `getState()` on the page so a robot can test it.

### Harness the Total Harness project needs to build
- An **explainer skill** (block 16): spec in, one page out, built one-shot, checked by the script, handed back only when the checks pass.
- The **check gate** as a rule, not a courtesy: the lab's script, generalised (presets must change the state; the hook must be complete; phone width; no debug leftovers).
- The **conventions folded into Build 42's starter kit** (keys, cameras, reset, hide-UI, labels, dialog, tuning panel), so games and explainers share one kit. Fix the three kit faults first (section 03).
- A **rubric** (block 17) with a frame-rate floor for the boys' devices and a "lite" render path for integrated graphics.
- A **Launch** hook so an explainer sits on the family site next to the games, and a private home for test files.

## 03 Experiment parameters
We wrote one spec of Prism Room from the live page, then had three fresh Claude sessions build it, each in its own way, and compared the pages on physics, features, look, speed to build, weight and frame rate. The spec, the checker and the viewport were the same for all three; only the build route and the model changed.

**Test input:** A written spec (`spec/prism-room-spec.md`, 6 sections: what it is, the physics, controls and conventions, layout, look, technical constraints) plus one reference screenshot of the original. Written from the live page in Charles's Chrome on 2026-10-19. None of his code or prose went into it.

**The test:** Each session got the spec and a path, built one HTML file, and could run the checker up to twice to fix its own faults. No human help. Then every page was checked once more on an idle machine, published privately, and opened in Charles's Chrome.

**Capabilities tested:** The physics (24 traced colours, Snell's law, total internal reflection, against the Schott N-SF11 glass data computed independently); a 19-item feature checklist read off the original (presets 1–4, prism turn, lamp tilt, second prism, three views, cinematic cameras, reset, labels, hide-UI, orbit, pan, zoom, walk, the dialog, live stats, the live "why" line, the tuning panel, poster image, phone width); the look, side by side with the original; build time; page weight; load time; frame rate on Charles's PC.

**Capabilities not tested:** The boys' own devices (not reachable from here). Launch to the family site (Build 42 is queued; the site does not exist yet). The second half of the brief's test, a new explainer on a topic a boy picks (next review; env A's route and the spec format are its inputs). Whether a child reads the "why" text (not a lab question). Exact dollars: builds ran inside the plan, so only token counts were recorded.

**Output:** One HTML page per environment, published as a private artifact for Charles to open, plus a same-view screenshot of each in his Chrome and a phone-width screenshot from the headless check.

**Settings:** Three.js 0.183.2 (his version) from a public library host; the allowed add-ons only (ambient occlusion, bloom, anti-aliasing, output, rounded and convex shapes, orbit controls); one file; no analytics. Env B and C started from the lab's page kit (`kit/explainer-kit.html`, 6.5 minutes to write, 20 KB), which holds the house conventions and the render passes and leaves four blocks to fill.

**Machines and versions:** **Builds:** Claude's cloud workspace, 2 cores, no graphics card; all three builds overlapped on it, so build times carry contention. Env A and B: the session's own model (Claude Fable 5.1). Env C: Claude Sonnet 5.5. **Checks:** Playwright with headless Chromium on software graphics (SwiftShader), so headless frame rates are not meaningful and are not reported. **Look and frame rate:** Charles's PC, Chrome, Intel UHD integrated graphics, 12 cores, 32 GB, 1920 × 1080 screen.

**What we measured:**
- **Physics:** the page's violet and red deviation at each preset against the independent glass maths; pass within 0.15°.
- **Features:** 19 scripted checks, each pressing the key or dragging the mouse and reading the page's state.
- **Build time:** wall clock from launch to hand-back, and tokens used by the build session.
- **Weight and load:** file size; time to the load event from a local server.
- **Frame rate:** the original measured directly in its own page; ours measured from the artifact viewer's frame, since the page runs inside a frame the script cannot enter (a proxy: when the graphics card is the bottleneck, both slow together). Same Chrome, same PC, within minutes.
- **Look:** one screenshot per environment beside the original, judged by eye.

**Side checks:**
- **The original's physics:** its on-page numbers (n 1.845 / 1.772, violet 75.4°, red 67.0°, spread 8.4° at 72°) match the glass maths exactly (Tested).
- **The original on a second laptop** (Intel UHD 620, Browser 2): 1 to 4 frames a second with the main thread idle (Tested); whether that window was being painted is unknown, so it is not used above.
- **Kit faults found by the builders:** (1) the ambient-occlusion pass treats glowing beam ribbons as solid and draws dark bars on them; (2) switching the cinematic off mid-flight leaves the camera stranded, so reset fails; (3) the control card's third row wraps badly at desktop width (Tested). All three are fixable in the kit.

**Saved test files:** Private, in `Chooch333/family-arcade` under `lab/prism-room/` (the Build 42 repo; explainers are headed for that site). Screenshots stay on the report page:
- `spec/prism-room-spec.md` and `spec/prism-room-reference.jpg`: the lab input, reusable for the next explainer review.
- `kit/explainer-kit.html`: the page kit (env B and C's starting point).
- `env-a/`, `env-b/`, `env-c/index.html`: the three pages, as handed back.
- `check/check.py`, `check/out/`: the checker, its results and screenshots, the timing log.

Nothing from his page is stored.

## 04 Results by test environment

### Env A · one-shot, his method
one prompt · Fable 5.1 · no kit · **Adopt now**
- **Page:** `page_oneshot_cloud.html` (75 KB) · https://claude.ai/artifact/ANPxKJUptyAra3rjtRUzP2
- **Build time:** 44.9 min wall clock · 248k tokens (Tested)
- **Checks:** 19 / 19 · physics exact at presets 1–4 · 24 rays (Tested)
- **Weight, load:** 75 KB · 1.5 s to load (local) (Tested)
- **Frame rate:** 16 fps proxy on Charles's PC (Tested)
- **Cost:** $0 beyond plan usage.
- **Quality:** Bench, lamp, beam and dial read well; the prism is drawn as an outline rather than solid glass, and the coloured fan after the prism is faint on a real screen. Clean phone layout (card collapses to one row) (Tested, by eye).
- **Verdict note:** Adopted 2026-10-20: Charles opened the page and said he would use it. What is adopted is the method (spec in words, one-shot build, check gate), not a tool; edits to this page go on an edit list and are made by a chat from the saved file.

### Env B · page kit, then build
kit + one prompt · Fable 5.1 · **Shelf**
- **Page:** `page_kit_cloud.html` (59 KB) · https://claude.ai/artifact/3NiH6Q6DiFSqhLu36rTHC4
- **Build time:** 60.3 min wall clock · 263k tokens, plus 6.5 min for the kit (Tested)
- **Checks:** 19 / 19 · physics exact at presets 1–4 · 24 rays (Tested)
- **Weight, load:** 59 KB · 1.6 s to load (local) (Tested)
- **Frame rate:** 16–17 fps proxy on Charles's PC (Tested)
- **Cost:** $0 beyond plan usage.
- **Quality:** Solid glass prism and a strong coloured fan; the lamp is plain; the control card's third row wraps into a mess (kit fault 3). Phone layout stacks the card and stays usable (Tested, by eye).
- **Verdict note:** The kit did not make the build faster and had three faults. Come back when Build 42's starter kit lands: fold these conventions into it rather than keeping a second kit.

### Env C · page kit, cheaper model
kit + one prompt · Sonnet 5.5 · **Shelf**
- **Page:** `page_kit_sonnet_cloud.html` (64 KB) · https://claude.ai/artifact/96xsKCKfb6dB758WDEQ46Q · as handed back, unverified by its builder
- **Build time:** 38.5 min to hand-back · 232k tokens (Tested); handed back without a finished check
- **Checks:** 18 / 19 · presets 1–4 fail: they do not change the setup, so the physics is exact only at the default (Tested)
- **Weight, load:** 64 KB · 0.35 s to load (local) (Tested)
- **Frame rate:** 32 fps proxy on Charles's PC (lighter render settings) (Tested)
- **Cost:** $0 beyond plan usage; a cheaper model per token.
- **Quality:** Closest composition to the original (dial, prism, screen, strong spectrum), but the lamp is a cyan arc, the background has a cartoon tree and a white ball, and a debug line was left in the code (Tested, by eye).
- **Verdict note:** Come back when the build route has a hard check gate (no hand-back under 19 of 19). The fact that would change the verdict: the cheaper model passing that gate on a fresh topic.

**Comparison image:** `compare_prism_room.jpg`. Same view in Charles's Chrome: the original (top left) and env A, B and C. The original's glass, haze and bench dressing are the gap; the physics and the controls are not.

**Phone image:** `phone_row.jpg`. Phone width (400 px, headless): all three keep the controls reachable with no sideways scroll. Env A's card collapses to one row; the kit (B, C) stacks it.

## 05 Use cases
**Now**
- One explainer per topic the boys are on, built one-shot from a spec, checked by the script, opened on a laptop (Tested on this one topic).
- Study copies of published explainers, built from a written description rather than their code, as a way to learn a structure (Tested).

**Later**
- Launched to the family site next to the games, once Build 42 lands (Assumed).
- Arch renders: the explorable building page and the phasing and finish-swap pieces, from the Pascal model (Assumed); a separate review.
- Cheaper builds with a smaller model behind a check gate (Assumed).

**Cannot**
- Photo-like stills. The look is clean and stylised (Tested, by eye).
- Run smoothly on integrated graphics with the full render stack: 7 to 20 fps for the original on Charles's laptop (Tested). Phones are untested and likely worse (Assumed).

## 06 Requirements check
### Family arcade (the lane)
| Requirement | Answer | Path |
|---|---|---|
| One-shot in a Claude chat, then a play gate and a review gate | Yes | Env A is exactly that. The checker is the play gate's robot half; Charles's look is the review gate (Tested). |
| Launch to the family site; saves per child across devices | Not tested | Same single-page shape as a Build 42 game; an explainer saves nothing today (Assumed). |
| One structure holds 2D look and full 3D | Not this tool's job | Explainers are 3D from the start. |
| Children's data: nicknames only, family-only | Yes | The page asks the network for nothing but the library and a font (Tested). |

### Arch renders (second lane)
| Requirement | Answer | Path |
|---|---|---|
| 1. Conventions | Yes | The kit proves a conventions set can be fixed once and reused: keys, cameras, labels, dialog, tuning (Tested). Ours would replace his. |
| 2. Storyboard | Not this tool's job | The cinematic shot list can double as the storyboard's shot list (Assumed). |
| 3. Menu of motion pieces | Not tested | Presets and views are the same mechanism as phasing steps (Assumed). |
| 4. Graphics quality | No, for stills | Stylised real-time look; stills stay on Blender Cycles (Tested, by eye). The interactive page needs its own bar in the rubric. |

## 07 Risks and cover
- **Frame rate on ordinary laptops and phones.** The original and ours run at 7–20 fps on integrated graphics (Tested). Cover: a lite render path (lower pixel ratio, no ambient occlusion) chosen by the page itself; a frame-rate floor in the rubric; test on one of the boys' devices before Launch.
- **A cheaper model fakes a feature.** Env C's presets looked right and did nothing (Tested). Cover: the check gate; hand-back blocked until the checklist passes.
- **Copying.** Our pages came from a spec, not his files; the spec holds no prose of his. Cover: keep it that way; name him as the reference design, as the Crayon row does.
- **Two kits.** Build 42 builds a starter kit for games; this lab wrote another for explainers. Cover: fold, don't keep both.
- **The look gap.** His glass, haze and bench dressing are better than all three of ours (Tested, by eye). Cover: a look pass after the checks pass, using the tuning panel, as he does; a small library of bench props.
- **Build time noise.** All three builds shared 2 cores. Cover: time the next build alone before quoting a number.

## 08 If adopted
- **What gets built:** the harness in Findings: explainer skill, check gate, conventions folded into Build 42's kit with the three faults fixed, rubric with a frame-rate floor, Launch hook, private storage.
- **Dollars:** $0. Plan usage per page in the range of this test (about a quarter-million tokens a build) (Tested).
- **Charles's hours:** about 30 minutes: open the three pages and say which he would use; one evening with a boy picking the first real topic (Assumed).
- **Proof of done:** from one sentence from a boy, a new explainer that passes the check gate, runs at the rubric's frame-rate floor on his device, and is launched to the family site.

## 09 Sources
- Discovery Brief draft, "Kids' 3D Explainer Pages, the sael.net format", discovery chat 2026-10-19 (unfiled).
- [Prism Room](https://sael.net/prism-room/), read in Charles's Chrome 2026-10-19 · [sael.net](https://sael.net/) · ["Open source, soon" notice](https://sael.net/virtual-tour/) · [pinned post on the Opus 5.5 one-shot build](https://x.com/RyanSael/status/2102591147927654847).
- Schott N-SF11 Sellmeier coefficients (the glass maths used by the checker).
- Working Document for this review: [Prism Room Review](https://claude.ai/artifact/Pu97UydnM2JVt2Pe5sMdG3). Build prompt template: [Explainer Build Prompt](https://claude.ai/artifact/3UTgZSRgYmitU4Yn6xy2fT). Test files: `Chooch333/family-arcade` `lab/prism-room/` (timing log, checker results).
- Project State, total-harness: Build 42 brief (headless Three.js check), family arcade speed-run record · agent-library: `lab/speed-run.md`, `lab/shelf/*`, `lab/reports/`, `lab/templates/rd-report.html`.
