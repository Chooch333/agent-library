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

**Out of scope:** any change to the lab's review steps, verdict rules, confidence marks or card sections; cbrain-ui code (Brief 2); the R&D project's instructions; judging or editing the seeded verdicts.

## Directive

1. **Write the skill** at `roles/tech-review/SKILL.md` to `CONVENTIONS.md`: front matter name `tech-review`, version 0.1.0, status draft, triggers `["Tech review:"]`, dependencies `[]`, owner Charles, updated today, and a `wiring:` block: runs `with-you`, starts `"Tech review:"`, runs_in `claude-chat`, reads `[repos, project-state]`, writes `[repos]`, stack `[]`, origin `yours`, label `Tech review`. Model it on `skills/wire-new-app/SKILL.md`. Check the allowed `reads`/`writes` words against `CONVENTIONS.md` and use the nearest valid ones. Six sections (What, When, How, Examples, Pitfalls, Changelog), under 500 lines. Pitfalls: none yet, say so (they must come from real traces).
2. **"Where things live"** — the first block under How. State: shelf rows in `lab/shelf/<tool>.md`, tech cards in `lab/cards/<review>.md`, the speed-run brief in `lab/speed-run.md`, all in `Chooch333/agent-library`, formats in `lab/README.md`. This is the only place those paths appear in any instruction Charles pastes, so moving the lab means editing this skill and nothing else.
3. **How** — copy Appendix A (the Lab rules) word for word, with exactly two changes because the home moved:
   - "Past verdicts": read every `lab/shelf/*.md` and `lab/speed-run.md` first, so nothing is reviewed twice.
   - FILING: only after Charles approves the card, write `lab/cards/<review>.md` and one `lab/shelf/<tool>.md` per tool with GitHub `create_or_update_file`. A changed verdict (after Charles approves it) edits the shelf file (`verdict`, `verdict_note`, `come_back_when`, `reviewed`) and adds one dated line at the top of its `## Verdict history`, for example `2026-11-02 · Shelf (was Adopt now) · <reason>`. Never edit or remove a history line. Clear `draft` when the card is approved. If the chat cannot write to the repo, file to the Lab Notebook as before and tell Charles. The adopt-now handoff on `total-harness` stays as written.
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
2. The skill's How section matches Appendix A word for word except the two stated changes, and has a "Where things live" block naming the three lab paths.
3. `AGENT.md` has the new row and a changelog line; "tech review" no longer appears in Eng review's triggers in AGENT.md or `roles/eng-reviewer/SKILL.md` (now 0.1.1).
4. `lab/` holds `README.md`, `speed-run.md`, seven shelf files (each `draft: true` with one 2026-10-09 history line) and `cards/artcraft.md`, each read back.
5. The Chats node in `concepts/stack-map.md` has a "Tech review" part and the file still parses.
6. Session Log, disclosures and done receipt written.

## Pasteable prompt

See the Handoff Reference block in the DA chat.

---

# Appendices (copy source for the build)

## Appendix A — Lab rules: source text for the skill (verbatim from the Lab Notebook)

Two lines change per Directive step 3: "Past verdicts" and the first bullet under FILING.

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

Copied from the Notebook tab "Tech card: ArtCraft Crafting Apps", converted to markdown. The card is 8.5 KB and is too long to repeat in this file a second time; the build copies it from the Lab Notebook tab (node `336ae06c-d110` in the R&D Lab Notebook) when it can read it, and otherwise from the Project State plan revision history of this brief's DA chat. If neither is reachable, set the plan `blocked` naming this appendix and stop. Front matter to put on the file:

````markdown
---
title: "Tech card: ArtCraft Crafting Apps"
reviewed: 2026-10-09
tools: [effectcraft, vectorcraft, filmcraft, photocraft, designcraft, pdfcraft, lightcraft]
draft: true
---
````

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
