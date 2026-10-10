# Build Brief — BB-2026-10-09-tech-review-skill

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-09-tech-review-skill.md`
**Project State plan:** `4584ba7c-cd63-4e15-af9f-b157f98702d5` on `misc-builds`
**Build:** 31
**Skills:** orchestrate-build
**Depends on:** none. Brief 2 (`BB-2026-10-09-rd-tab`, Build 32) waits for this one.
**Stack Flow:** add a "Tech review" part to the Chats node of `concepts/stack-map.md` (skill `roles/tech-review`, saves to `lab/` in `Chooch333/agent-library`), shaped like the existing "Wire up a new app" part.

**What this is:** A new skill, `roles/tech-review/SKILL.md`, that runs when a chat's first message starts `Tech review:`. Plus the `lab/` folder in the agent library that the skill reads and writes, seeded with today's seven shelf rows, the ArtCraft tech card and the speed-run brief.

**What I'll do:** Create the skill, the AGENT.md row and the `lab/` files; remove the clashing "tech review" trigger from Eng review; add the Stack Flow part; prove the Skills screen lists the skill; close with a Session Log and done receipt.

**What you'll do:** After this lands, paste two texts (given in the DA chat's design page) and let the ArtCraft chat finish its card through the skill. The R&D project's instructions stay as they are: already final, pointing only at this skill.

---

## Current state going in

**Asked for — in Charles's words** *(frozen at intake; never reworded)*
> "Design Assist. Scope the R&D lab build-out: a tech-review skill, and an R&D tab on the Total Harness screen." — Charles, 2026-10-09
> "Turn the lab rules ... into one skill in the agent library, roles/tech-review/SKILL.md, plus one row in AGENT.md so that a first message starting "Tech review:" triggers it in any chat. That one line is the whole trigger. Keep it that simple." — Charles, 2026-10-09
> "The speed-run brief and the shelf stay outside the skill, so they can change without editing it. The skill reads them at the start of each review." — Charles, 2026-10-09
> "The R&D project's instructions are already final and point only at this skill. So the skill itself must say where the shelf, the tech cards and the speed-run brief live. I must never have to edit the project instructions when those move." — Charles, 2026-10-09
> "Pick one lane and bring me something concrete to react to." — Charles, 2026-10-09
- 2026-10-09 Charles approved the lane (lab files in the agent library, read by the R&D tab) and said yes to: chats file into `lab/` after he approves the card, with no brief; the second tab is "Build map".

Labels: **[verified]** = checked 2026-10-09; **[assumed]**; **[draft]**.

- **The lane.** Shelf rows and tech cards are plain files in `lab/` in `Chooch333/agent-library`: one file per tool in `lab/shelf/`, one per review in `lab/cards/`, plus `lab/speed-run.md` and `lab/README.md`. The Skills screen lists only `roles/`, `skills/` and `external/`, so `lab/` does not show there. **[verified]** (`lib/db/skills.ts` on cbrain-ui `review`)
- **Why not a cbrain page type.** No type fits a tool; the health types (`protocol`, `content-record`) are documented in `contracts/SCHEMA.md` but were never wired: `services/lib/clients.ts` and `manifest.ts` have no health entries, `.github/workflows/sync.yml` watches six folders and no health folder, the live `pages` table has zero such rows, and cbrain has only a `main` branch. The Archivist appends and never changes a filled value, so a moving verdict has no home. **[verified]**
- **Skills appear on screen automatically.** `lib/db/skills.ts` reads `Chooch333/agent-library@main` live (5-minute cache) and parses front matter and the `wiring:` block. **[verified]**
- **Name clash.** `roles/eng-reviewer/SKILL.md` lists `"tech review"` in its `triggers` and the AGENT.md Plan-mode row lists it too. The new skill fires only on a first message that starts `Tech review:`. **[verified]**
- **Stack Flow precedent.** The Chats rim node (`id: chats`) already has a `made_of` part "Wire up a new app" (skill `skills/wire-new-app`). Design Assist and brainstorm have no parts there. **[verified]**
- **Research chats can write to the agent library.** **[assumed]** Chats read it today; write access from the R&D project is unconfirmed. If a chat can't write, the skill files to the Lab Notebook and says so.
- **Filing gate.** The lab's rule stays: nothing is filed until Charles approves the card. **[verified]** (Lab Notebook, Paste-ready text, "Lab rules")

## Receiving chat

New build chat.

## Scope

**In scope:**
- `roles/tech-review/SKILL.md`, v0.1.0, status draft.
- `lab/` folder: `README.md`, `speed-run.md`, seven `shelf/` files, `cards/artcraft.md` (Appendices B to E).
- `AGENT.md`: one new row, a dated changelog line, and "tech review" removed from the Plan-mode row.
- `roles/eng-reviewer/SKILL.md`: remove `"tech review"` from `triggers`, version 0.1.1, changelog line.
- `concepts/stack-map.md` in `Chooch333/cbrain`: the Chats part.

**Out of scope:** any change to the lab's review steps, confidence marks or card sections, or to the verdict rules other than the one Adopt now change in Directive step 3; cbrain-ui code (Brief 2); the R&D project's instructions; judging or editing the seeded verdicts.

## Directive

1. **Write the skill** at `roles/tech-review/SKILL.md` to `CONVENTIONS.md`: front matter name `tech-review`, version 0.1.0, status draft, triggers `["Tech review:"]`, dependencies `[]`, owner Charles, updated today, and a `wiring:` block: runs `with-you`, starts `"Tech review:"`, runs_in `claude-chat`, reads `[repos, project-state]`, writes `[repos]`, stack `[]`, origin `yours`, label `Tech review`. Model it on `skills/wire-new-app/SKILL.md`. Check the allowed `reads`/`writes` words against `CONVENTIONS.md` and use the nearest valid ones. Six sections (What, When, How, Examples, Pitfalls, Changelog), under 500 lines. Pitfalls: none yet, say so (they must come from real traces).
2. **"Where things live"** — the first block under How. State: shelf rows in `lab/shelf/<tool>.md`, tech cards in `lab/cards/<review>.md`, the speed-run brief in `lab/speed-run.md`, all in `Chooch333/agent-library`, formats in `lab/README.md`. This is the only place those paths appear in any instruction Charles pastes, so moving the lab means editing this skill and nothing else.
3. **How** — copy Appendix A (the Lab rules) word for word, with exactly three changes: two because the home moved, one because Charles asked (the third bullet):
   - "Past verdicts": read every `lab/shelf/*.md` and `lab/speed-run.md` first, so nothing is reviewed twice.
   - FILING: only after Charles approves the card, write `lab/cards/<review>.md` and one `lab/shelf/<tool>.md` per tool with GitHub `create_or_update_file`. A changed verdict (after Charles approves it) edits the shelf file (`verdict`, `verdict_note`, `come_back_when`, `reviewed`) and adds one dated line at the top of its `## Verdict history`, for example `2026-11-02 · Shelf (was Adopt now) · <reason>`. Never edit or remove a history line. Clear `draft` when the card is approved. If the chat cannot write to the repo, file to the Lab Notebook as before and tell Charles. The adopt-now handoff on `total-harness` stays as written.
   - VERDICTS, Adopt now (a rule change Charles asked for on 2026-10-09, before this build ran): add one requirement. The line becomes: "Adopt now: it passed a hands-on test, AND I have seen the test output and said I would use it, AND it serves the speed run or a block that is done, in progress or next in line, AND it is free or I approved the cost." Change nothing else in VERDICTS. The chat must therefore show Charles the test output and get his word before it can call a tool Adopt now.
4. **Create the `lab/` files** from Appendices B to E, byte for byte: `lab/README.md`, `lab/speed-run.md`, `lab/shelf/*.md` (7), `lab/cards/artcraft.md`. Commit with the Brief ID in the message. Read each back to confirm.
5. **`AGENT.md`** — add one row: a first message that starts `Tech review:` → `roles/tech-review/SKILL.md`, in the group with the other first-message triggers. Remove "tech review" from the Plan-mode row's Eng review triggers. Add a dated changelog line at the top citing this Brief ID.
6. **`roles/eng-reviewer/SKILL.md`** — remove `"tech review"` from `triggers` (and from the When section if it appears there), bump to 0.1.1, add a changelog line. Nothing else.
7. **Stack Flow** — in `Chooch333/cbrain` `concepts/stack-map.md`, add a `made_of` part to the Chats node named "Tech review", copying the field shape of "Wire up a new app": skill `roles/tech-review`, saves to `lab/` in the agent library, with a one-sentence story in plain words. Check how Build 28 added its part and follow the same route. Read it back and confirm the file still parses.
8. **Prove it** — read the new SKILL.md back through the same parser the Skills screen uses (`lib/db/skills.ts` logic) and confirm name, trigger and wiring parse and that `lab/` is not listed. Confirm a search for "tech review" in AGENT.md and eng-reviewer finds only the new row.
9. **Close** — Session Log on `misc-builds` with the Brief ID; done receipt with all acceptance items; disclosures for any call made (`post_judgment_call`).

Standing rules: CB-121 (commits authored as Chooch333). No browser tests.

## Inputs

- Appendices A to E in this file: the Lab Notebook text, read in full 2026-10-09 (R&D Lab Notebook: https://claude.ai/code/artifact/f3824046-d946-4da4-bffb-9e68146b619b). **[verified]**
- `CONVENTIONS.md`, `AGENT.md`, `skills/wire-new-app/SKILL.md`, `roles/eng-reviewer/SKILL.md`, `concepts/stack-map.md`. **[verified]**
- Research chats can write to the agent library. **[assumed]**

## Acceptance criteria

1. `roles/tech-review/SKILL.md` exists, parses, and shows on the Skills screen in the Claude chat lane with starts `Tech review:`.
2. The skill's How section matches Appendix A word for word except the three stated changes (including the Adopt now line with "AND I have seen the test output and said I would use it"), and has a "Where things live" block naming the three lab paths.
3. `AGENT.md` has the new row and a changelog line; "tech review" no longer appears in Eng review's triggers in AGENT.md or `roles/eng-reviewer/SKILL.md` (now 0.1.1).
4. `lab/` holds `README.md`, `speed-run.md`, seven shelf files (each `draft: true` with one 2026-10-09 history line) and `cards/artcraft.md`, each read back.
5. The Chats node in `concepts/stack-map.md` has a "Tech review" part and the file still parses.
6. Session Log, disclosures and done receipt written.

## Pasteable prompt

See the Handoff Reference block in the DA chat.

---

# Appendices (copy source for the build)

## Appendix A — Lab rules: source text for the skill (verbatim from the Lab Notebook)

Three changes per Directive step 3: "Past verdicts", the first bullet under FILING, and the Adopt now line under VERDICTS. The text below is the Notebook's, unchanged; the build applies the changes.

````
This space is a lab, not a project plan. Tech for the Total Harness gets reviewed in any order, as it appears. Each chat reviews one tech and ends with a verdict. The lab never builds permanent setup. The Total Harness project does that.

AT THE START OF EVERY CHAT (my first message is only "Tech review: <name or link>"; pull everything else, do not ask me to paste it)
- Read PROTOCOL.md and AGENT.md as usual.
- Harness status: Project State project total-harness (list_plans, latest notes) and the map at Chooch333/cbrain concepts/harness-map.md. Project State is the record.
- Past verdicts: the Shelf tab of the Lab Notebook, https://claude.ai/code/artifact/f3824046-d946-4da4-bffb-9e68146b619b. Read it first so nothing is reviewed twice.
- The speed run: see the bottom of these instructions.

THE REVIEW, IN ORDER
Keep one Working Document per chat. Findings go in the document. Chat is for choices only.
1. Ground facts, checked at the source today: who makes it, how old it is, price, whether a company may use it, whether Claude can run it with no screen.
2. Use case by Q&A: at most three closed questions to me, each with your recommended answer. Then list uses I did not ask about, across the whole harness.
3. Place it: layer, pipeline step, block, and what it would replace in the blueprint.
4. Hands-on test in the cloud workspace wherever possible. Tests only. No permanent setup.
5. Compare: what else does this job, including what Claude does today without it.
6. One verdict per tool, then the tech card.

VERDICTS
- Adopt now: it passed a hands-on test, AND it serves the speed run or a block that is done, in progress or next in line, AND it is free or I approved the cost.
- Shelf: useful, but its block is further down the order, or it is too new or untested to lean on. Name one trigger: a block number, a maturity milestone, or a date.
- Never: it fails on a hard fact (Claude cannot run it, license or price, duplicates what we have, nothing needs it, unsafe). Name the one fact that would have to change.
Only the speed run pulls a tool ahead of build order.

TECH CARD (one page, plain words, no jargon; explain any term the first time it appears)
What it is. Verdict by tool. Where it fits. What we could use it for: now, later, cannot. What we checked. What else does this job. Risks and cover. If adopted: what gets built, dollars, my hours, proof of done. Sources.
Mark every claim: ✓ checked at a source today, ✓✓ run hands-on, ~ assumed.

FILING (only after I approve the card)
- Each verdict is one row on the Shelf tab of the Lab Notebook, with its tech card as a tab beside it. A changed verdict updates the row and adds a dated line to the card. Do not create a Project State project for the lab.
- Adopt now also files a question on total-harness (origin charles-directed, Session Log ticket per protocol) titled "R&D handoff: <tool>", with the card in its thread, tagged rd-handoff, plus speed-run when it applies. Give me the ID.

STANDING RULES
Pick one lane and name what you ruled out. Money always stops. Do not stack assumptions: verify the bottom one first. Push back when I am wrong. Roles fire only when I name them.

THE SPEED RUN
One use case, not two: architectural renderings and motion graphics for my work at FA Wilhelm, built ahead of harness order. Judge every tool against the whole chain: plans in, a model built from them, rendered stills, touch-up, motion and labels, one finished clip out. Say which of those steps the tool serves.
- Renders: design options and finish swaps, pursuit visuals, an explorable building page.
- Motion graphics: titles, animated phasing and sequencing, branded stills.
- Finish line: from one plan set and a finish list, with me only reacting at stops, deliver inside a day three rendered stills, one 20 to 30 second animated piece, and the editable files.
````

## Appendix B — `lab/README.md`

````markdown
# lab/ — the R&D lab's record

Written by `Tech review:` chats (`roles/tech-review/SKILL.md`). Read by the R&D tab on the Total Harness screen in cbrain-ui. Plain files. Nothing here is a cbrain page, and the Skills screen ignores this folder.

## Files

- `shelf/<tool>.md` — one file per tool. The front matter is the shelf row. The body holds `## Verdict history`, newest line first.
- `cards/<review>.md` — one file per review: the tech card. A review of a suite covers several tools.
- `speed-run.md` — the speed-run brief. Read at the start of each review. Not shown on the screen.

## Shelf file fields

| Field | Meaning |
|---|---|
| `tool` | The tool's name. |
| `does` | One line: what it does. |
| `verdict` | `adopt-now`, `shelf` or `never`. |
| `verdict_note` | Short qualifier such as `as a trial`. May be empty. |
| `come_back_when` | The one trigger for a shelf or never verdict. Empty for adopt-now. |
| `blocks` | Total Harness block numbers it touches, such as `[16, 17, 19]`. May be empty. |
| `card` | File name in `cards/` without `.md`. May be empty. |
| `reviewed` | Date of the latest review, `YYYY-MM-DD`. |
| `draft` | `true` until Charles approves the card. Remove it or set `false` on approval. |

## History line

`- YYYY-MM-DD · <Verdict> (<note>) · <reason, or "First review (<card>)">`

Newest on top. A line is never edited or deleted. A change of verdict adds a line such as `Shelf (was Adopt now)`.

## Card file

Front matter: `title`, `reviewed`, `tools` (shelf file names the card covers), `draft`. The body is the tech card: the sections named in the lab rules, as `##` headings in order. "Verdict by tool" is the verdict on the review date; the shelf file holds the current one.

Every claim carries a mark: ✓ checked at a source today, ✓✓ run hands-on, ~ assumed.
````

## Appendix C — `lab/shelf/*.md` (seven files)

### lab/shelf/effectcraft.md

````markdown
---
tool: EffectCraft
does: "Motion graphics, a copy of After Effects"
verdict: adopt-now
verdict_note: "as a trial"
come_back_when: ""
blocks: [16, 17, 19]
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Adopt now, as a trial (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/vectorcraft.md

````markdown
---
tool: VectorCraft
does: "Drawings and diagrams, a copy of Illustrator"
verdict: adopt-now
verdict_note: "as a trial"
come_back_when: ""
blocks: [16, 17, 19]
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Adopt now, as a trial (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/filmcraft.md

````markdown
---
tool: FilmCraft
does: "Video editing, a copy of Premiere"
verdict: shelf
verdict_note: ""
come_back_when: "A speed-run piece needs a real multi-clip edit"
blocks: [16]
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Shelf (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/photocraft.md

````markdown
---
tool: PhotoCraft
does: "Image editing, a copy of Photoshop"
verdict: shelf
verdict_note: ""
come_back_when: "It leaves early alpha, or a render needs touch-up Claude cannot do in code"
blocks: [16]
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Shelf (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/designcraft.md

````markdown
---
tool: DesignCraft
does: "Page layout, a copy of InDesign"
verdict: shelf
verdict_note: ""
come_back_when: "You open a proposal-pages use case"
blocks: [16]
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Shelf (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/pdfcraft.md

````markdown
---
tool: PdfCraft
does: "PDF handling, a copy of Acrobat"
verdict: never
verdict_note: ""
come_back_when: "It does something Claude's built-in PDF tools cannot"
blocks: []
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Never (draft, on hold) · First review (ArtCraft card)
````

### lab/shelf/lightcraft.md

````markdown
---
tool: LightCraft
does: "Photo library, a copy of Lightroom"
verdict: never
verdict_note: ""
come_back_when: "Photography becomes a harness domain"
blocks: []
card: artcraft
reviewed: 2026-10-09
draft: true
---
## Verdict history
- 2026-10-09 · Never (draft, on hold) · First review (ArtCraft card)
````

## Appendix D — `lab/cards/artcraft.md`

Copied from the Notebook tab "Tech card: ArtCraft Crafting Apps" (node `336ae06c-d110` in the R&D Lab Notebook), converted to markdown. Copy everything inside the fence below into `lab/cards/artcraft.md`.

`````markdown
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
`````

## Appendix E — `lab/speed-run.md`

````markdown
# The speed run

*Draft, copied from the Lab Notebook on 2026-10-09. The finish line below is a draft by Claude, not yet Charles's.*

One use case, not two: architectural renderings and motion graphics for my work at FA Wilhelm, built ahead of harness order. Judge every tool against the whole chain: plans in, a model built from them, rendered stills, touch-up, motion and labels, one finished clip out. Say which of those steps the tool serves.

- Renders: design options and finish swaps, pursuit visuals, an explorable building page.
- Motion graphics: titles, animated phasing and sequencing, branded stills.
- Finish line: from one plan set and a finish list, with me only reacting at stops, deliver inside a day three rendered stills, one 20 to 30 second animated piece, and the editable files.

## Where each half stands (2026-10-09)

| Half | What Charles chose | Where it stands |
|---|---|---|
| Renders | Design options and finish swaps, pursuit visuals, and an explorable building page (variants B, C, D in the animation chat). ✓ | First test under way: white-box stills from 2D plans, to set a baseline. No tool reviewed yet. |
| Motion graphics | Better Claude-made animation and graphics for personal and work use (variants A and C in the ArtCraft chat). ✓ | Tool tested and reviewed. See the tech card. |

**Proposed finish line (Claude's draft, not yet Charles's).** From one plan set and a finish list, with Charles only reacting at stops, Claude delivers inside a day: three rendered stills, one 20 to 30 second animated piece with titles and a phasing diagram, and the editable files behind both.

Without a finish line, "serves the speed run" has no edge and every graphics tool would qualify for adopt now.

**One cost to see clearly.** Charles capped build fronts at two. The speed run takes one of them while block 3 is still open.
````
