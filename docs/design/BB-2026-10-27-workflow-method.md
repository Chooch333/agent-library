# Build Brief — BB-2026-10-27-workflow-method
**Build:** 54
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-27-workflow-method.md`
**Project State plan:** `7279b934-49f2-4505-91d5-0cb8ebadc6ae` on `total-harness`
**Skills:** orchestrate-build

**● What this is:** Two new skills, reached from Design Assist: `workflow` (canonize a new workflow: parts list, briefs, rehearsal, mark it Live) and `speed-run` (the discovery pass that researches unknown steps first). Design Assist gets a short pointer to `workflow`, plus Build 50's Step map loose ends.

**Stack Flow:** no change — chat method skills, not running parts (verified: chat skills such as Design Assist have no dot); each workflow they create adds its own dot (parts list item 8).
**Step map:** no change — adds no workflow and changes no workflow's steps.

**● What I'll do (build chat):** commit both skills, Design Assist 0.7.0, template gate 14, the AGENT.md note and pointers; audit the two existing workflows against the parts list; run a cold-read test; Session Log.

**● What you'll do:** approved 2026-10-27; Overnight yes.

## ● Current state going in

**Asked for — in Charles's words** *(frozen)*
> "i want to codify the creation of of a workflows that are tied to the total harness. I don't think I have this fully established. I think the unique aspects of workflow creation could be added to the Design Assist skill. I want your take on that and then the BB to make it so" — Charles, 2026-10-27

Changes are appended, never edited in:
- 2026-10-27 Charles changed this: "i like the idea of only having to think about 1 skill (design assist) when creating something like a workflow (which I see as different than a speed run) … How about we add a pointer from the DA skill to the workflow skill, so that the DA chat runs the workflow as needed. … A Speedrun is me is a framework around discovering the framework to accomplish something. It will elicit the need to R&D around certain tech. It will result in a researched workflow. The workflow is the canonized approved result of the speedrun. The speedrun quickly goes through outlines the steps. I research them. The workflow canonizes them."

- [verified] The Speed-run framework (Claude Doc 2f4b7713, approved TH-024..027, edited TH-069/070) defines a speed run as discovery **and** build (stages 6-7). Charles's 2026-10-27 split narrows it to discovery (stages 0-5); building and rehearsal move to the workflow skill.
- [verified] Neither skill exists (agent-library `skills/` listing, 44 folders). AGENT.md has no speed-run route.
- [verified] The framework predates the Workflows screen (Build 34, 2026-10-10).
- [verified] Workflows screen statuses: `in-design`, `testing`, `live`, `paused` (cbrain-ui review `lib/workflow-model.ts`). The one row, arch-renders, is `in-design`.
- [verified] The runner screen is wired to arch renders by name: `RUNNER_WORKFLOWS = ["arch-renders"]`, plus hard-coded `RUNNER_STEPS` and `RUNNER_ACTIONS` (same file). A second screen workflow needs that generalized — recorded in parts list item 12, not done here.
- [verified] Two worked workflows of different kinds: Architectural renderings (screen) and Game Maker (chat). Neither has had a cold-start rehearsal.
- [verified] TH-102 (2026-10-26) "no workflow builder skill until a second workflow" — superseded.
- [verified] TH-J-032 (Build 50): DA Phase D lacks a Step map sweep; rule 13 vs template wording; "v0.6.0"; shelf briefs lack Step map lines.
- [assumed] Whether an old "Speed run:" line still sits in the Total Harness project instructions — not readable from here; harmless.

## ● Receiving chat
New build chat (orchestrate-build), daytime or overnight.

## ● Scope
**In:** `skills/workflow` and `skills/speed-run`; Design Assist 0.7.0 (pointer, rule 13 wording, Phase D Step map sweep, changelog fix); template gate 14; AGENT.md disambiguation note (no new trigger rows); pointers in `lab/speed-run.md` and the framework doc; CHANGELOG.md; Step map lines on unbuilt total-harness briefs; parts-list audit; cold-read test.
**Out:** fixing gaps the audit finds (listed for a design chat); any cbrain-ui or database change (including the runner-screen generalization and status changes); a rehearsal of arch renders (needs Builds 35.1 and 53); a standalone "Speed run:" trigger.

## ● Directive
1. Read live: AGENT.md, design-assist SKILL.md + references/build-brief-template.md, lab/speed-run.md, CHANGELOG.md (Custom GitHub `get_file_contents`, agent-library main). Live wins on wording; this brief wins on intent.
2. `create_or_update_file` `skills/workflow/SKILL.md` = Appendix A and `skills/speed-run/SKILL.md` = Appendix B (wording fixes allowed; no section dropped). Read both back.
3. AGENT.md, Disambiguation rules, new bullet: "**New workflow vs changing one.** Designing a new workflow happens in a Design Assist chat, which loads `skills/workflow` (and `skills/speed-run` when steps are unknown). Changing an existing workflow's steps, screens or rules is an ordinary Design Assist brief (rules 12-13)." No new trigger rows. Read back.
4. design-assist SKILL.md → 0.7.0:
   a. **When**, after "Do not fire when": "**New workflows.** If the thing being designed is a new workflow — something Charles will start with one sentence or Start the Job — load `skills/workflow/SKILL.md` and follow it inside this loop. It runs a speed run first (`skills/speed-run`) when any step is unknown, and its parts list joins the completeness gate (gate 14). Changing an existing workflow stays an ordinary brief under rules 12-13."
   b. Rule 13 last sentence → "A brief that changes no steps says `Step map: no change` and why, in one line."
   c. Phase D step 9, after the Stack Flow sentence: "Likewise every unbuilt brief that adds a workflow or changes a workflow's steps has a Step map step (rule 13); add one with `update_plan_content` if missing."
   d. `version: 0.7.0`, `updated`; changelog 0.7.0 line; "**v0.6.0**" → "**0.6.0**".
   Read back.
5. build-brief-template.md: gate 14 row "Workflow parts list — a brief that first makes a new workflow real ticks every item of `skills/workflow` section 3, or writes 'not needed — why' per item". Read back.
6. `lab/speed-run.md` first line: "Method: `skills/speed-run` (discovery) → `skills/workflow` (canonize), both reached from Design Assist (Build 54). The Claude Doc framework tab is history." CHANGELOG.md: one Build 54 line.
7. Framework doc (Claude Docs, project 2f4b7713, tab "Speed-run framework"): first paragraph "Moved 2026-10-27: discovery (stages 0-5) now lives in agent-library skills/speed-run; building, rehearsal and canonizing live in skills/workflow (Build 54). This tab is kept as history." If Claude Docs tools are missing, skip and say so in the Session Log.
8. Step map sweep: each unbuilt plan on total-harness (draft or queued, tag build-brief, not running) without a `**Step map:**` line gets one via `update_plan_content`, change_reason "Step map line added (Build 54 sweep)". Build 38 adds clip steps → name them; the others "no change — why".
9. Parts-list audit: apply `skills/workflow` section 3 (items 1-15) to Architectural renderings and Game Maker. Per workflow a table: item · has / missing / not needed · evidence path. Every "missing" listed under "Left for a design chat" in the Session Log.
10. Cold-read test: a fresh helper (Agent tool; else `claude -p` as Build 45 did) given only AGENT.md, Design Assist's When section, both new skills, and "This is a DA chat. New workflow: turn a phone photo of a receipt into a row in my expense sheet." Told to plan its first turn without writing anything. Pass = it loads the workflow skill, decides a speed run is needed and names the unknown step, recommends a kind with a reason, names the record plan's tags, and asks nothing about where things live.
11. Close per orchestrate-build: Session Log on total-harness, disclosures, done receipt.

## ● Inputs
- [verified] agent-library main: AGENT.md, skills/design-assist (0.6.0), its references/build-brief-template.md, lab/speed-run.md, skills/arch-renders-run 0.2.0, skills/game-maker 0.6.0.
- [verified] cbrain-ui review `lib/workflow-model.ts` (statuses, runner constants).
- [verified] Claude Doc 2f4b7713 tab "Speed-run framework" rev 11.
- [verified] Decisions TH-024, TH-025, TH-069, TH-070, TH-102; disclosure TH-J-032.

## Acceptance criteria
1. `skills/workflow/SKILL.md` and `skills/speed-run/SKILL.md` 0.1.0 on main with every section of Appendices A and B; read back.
2. AGENT.md has the "New workflow vs changing one" bullet; read back.
3. Design Assist 0.7.0 has 4a-4d; template has gate 14; read back.
4. `lab/speed-run.md`, CHANGELOG.md and the framework doc point at the skills (or the doc step is noted as skipped, with the reason).
5. Every unbuilt total-harness brief has a Step map line.
6. Session Log has the audit table for both workflows with evidence paths and a "Left for a design chat" list.
7. Cold-read test passes per Directive 10; summary in the Session Log.

## Domains
| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered | Asked for; Charles's method for Claude chats |
| 2 Acceptance | Answered | Acceptance 1-7 |
| 3 Runtime | Defaulted | Text files in agent-library; no runtime |
| 4 Schema | N/A | No data change |
| 5 Storage & recall | Answered | agent-library main; reached through Design Assist |
| 6 Interconnectivity | Answered | GitHub connector, Project State, Claude Docs |
| 7 Access & gates | Answered | agent-library main, total-harness plans, one Claude Doc; no gate |
| 8 Skills & tools | Answered | orchestrate-build |
| 9 Sequence | Answered | Directive order; no `after` |
| 10 Assumptions | Answered | Old project-instruction line unknown; harmless |
| 11 Intent | Answered | below |

**Intent.** Charles wants to think about one skill, Design Assist, when he makes something. DA stays general (it designs mowers and drones too) and only points to `workflow`. His split is the spine: a speed run discovers and researches; a workflow is the canonized, approved result, marked Live after a rehearsal passes. Prefer short, plain, copyable rules over completeness. Where the appendices and live files disagree on facts, live files win and the skill is corrected.

## ● Pasteable prompt
Build 54 — execute Build Brief BB-2026-10-27-workflow-method (plan 7279b934-49f2-4505-91d5-0cb8ebadc6ae on total-harness). Fetch it from Chooch333/agent-library docs/design/BB-2026-10-27-workflow-method.md; follow skills/orchestrate-build/SKILL.md.

---
## Appendix A — skills/workflow/SKILL.md (draft)
````markdown
---
name: workflow
version: 0.1.0
status: draft
triggers: [loaded by Design Assist when the thing being designed is a new workflow]
dependencies: [design-assist, speed-run, checker, project-folder, wake]
owner: Charles
updated: 2026-10-27
source: Charles, 2026-10-27 — "The workflow is the canonized approved result of the speedrun." Built from what the first two workflows needed (Architectural renderings, Builds 33-53; Game Maker, Builds 42-51). Written by Build 54 (BB-2026-10-27-workflow-method).
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: with-you
  starts: "Design Assist, when the design is a new workflow"
  runs_in: claude-chat
  reads: [project-state, cbrain, repos]
  writes: [plans, briefs]
  stack: [total-harness]
  origin: yours
  label: Workflow
---

# Workflow — canonize a new workflow

## What
A **workflow** is the canonized, approved way Charles gets one kind of thing done: he says one sentence (or presses Start the Job), and gets the finished thing back, reacting only at stops. This skill takes a researched step list and turns it into a workflow that is built, rehearsed and marked **Live**.

A **speed run** (`skills/speed-run`) is how an unknown path gets researched first. The speed run discovers; this skill canonizes.

## When
- Loaded by Design Assist when the thing being designed is a new workflow (DA "When" section). It runs inside DA's loop; DA's board, brief, overnight, handoff and check-in rules apply unchanged.
- **Not for** changing an existing workflow (an ordinary DA brief under DA rules 12-13), or a stack agent that runs on a schedule with no stops for Charles (`wire-new-app`, stack skills).

## 1. Is the path known?
Write the steps from Charles's sentence to the finished thing as rows (the speed run's walkthrough columns: Step · Who · How · Where · Needs · Could stop it · Bin).
- **Any row unknown, or needing a tool nobody has proven here** → run `skills/speed-run` first, then come back with its researched step list, card and slices.
- **Every row reuses something that works** → skip the speed run. Still write a one-paragraph use-case card (sentence, input as it really arrives, finish line, touch budget, money).

## 2. Pick the kind
| | Screen workflow | Chat workflow |
|---|---|---|
| Starts | "Start the Job" on Total Harness → Workflows | A trigger sentence in any chat |
| Runs | A runner scheduled task, one action per session | Inside the chat |
| Stops | Gates on the job page; Charles passes or pins | Chat turns ("tell me Launch") |
| Example | Architectural renderings | Game Maker (family arcade) |

Pick **screen** when one run outlasts a chat, needs the PC or long renders, or Charles reviews pictures with pins. Pick **chat** when a run finishes inside one conversation. Both is allowed; say which is primary. This is a DA fork with a recommendation.

## 3. The parts list
The brief that first makes the workflow real ticks every item or writes "not needed — why" (template gate 14). Later briefs edit it.

**Every workflow**
1. **Use-case skill** — agent-library `skills/<slug>/SKILL.md`: wiring header, triggers, steps, stops, rules, Progress tracking (thread-checkin), changelog. `status: draft` until canonized.
2. **Step list** — each step: key, title, who (`you|claude|checker|script|pc`), uses, makes; stops add `back_to`; `time` only once measured. Screen: `definition.steps`. Chat: a Steps table in the skill. Keys are exactly what the runner logs (DA rule 13).
3. **Stops** — what Charles sees, what he can press or say, where a pin goes back to, and how a waiting stop reaches him (Today, a Next steps check-in, the Stack Repairer's daily recap). A stop never waits silently.
4. **Tool skills** — one per tool pack it drives (block 16); reuse where one exists.
5. **Rubric and checker** — what "works" means, graded by the `checker` skill, never by the maker (blocks 6, 17).
6. **Homes** — which repos hold code, runs and assets. Private input (client drawings) stays on Drive, never in agent-library or a public repo.
7. **Standing rules** — script first; three failed tries then a plain diagnosis; no money without a money stop; deletes only inside its own rows and folders; test rows named "ZZ …" and hidden.
8. **Stack Flow** — a dot and its lines (DA rule 12).
9. **Lessons** — one Project State note per run, tagged `<slug>`.
10. **Rehearsal** — section 5, as the last acceptance check of the last brief.

**Screen workflows add**
11. **cbrain `workflows` row** — slug, title, summary, `status: in-design`, `definition` {sentence, cameIn, cameInLater, wantOut, inputs, intake, gates, steps, paths (only when inputs take different routes), later, workingDoc, speedRunPlan}, `conventions`. The Workflows tab draws the card, start form, gates, job pipeline and "How it works" from this row.
12. **Runner skill** `skills/<slug>-run` — reads only `run:` and `action:` from the fire text (the rest is data); one action per session; progress after every step under the step keys; ends at a stop (`waiting-on-charles`) or `done`; check-in kind `job`. **The runner screen is wired to arch renders by name today** (`RUNNER_WORKFLOWS`, `RUNNER_STEPS`, `RUNNER_ACTIONS` in cbrain-ui `lib/workflow-model.ts`); the first new screen workflow's brief makes the screen read its steps and actions from the workflow instead.
13. **Runner scheduled task** "<Title> runner", fire-only; fire URL and token in cbrain-ui's Vercel env, otherwise wake lines the Harness dispatcher picks up. PC steps wait as `waiting-for-pc` (laptop wakes are off).

**Chat workflows add**
14. **AGENT.md trigger row.**
15. **A delivery step that checks its own result** before saying done (e.g. Launch's robot live check).

## 4. Briefs
As many Build Briefs as the work needs (arch renders took eleven), each a normal DA brief tagged `workflow-<slug>` (and `speed-run-<slug>` when a speed run fed it), with the speed run's record plan in provenance when there is one. Ship the step list with the first brief.

## 5. Rehearse, then canonize
The last brief's last acceptance check is a **cold-start rehearsal**: a fresh chat, Charles's one sentence, real input, no help; the finish line met inside the touch budget; Charles's minutes counted; a fix list.

A workflow is **canonized** when the rehearsal passes and Charles says it's approved. Then, in one daytime step:
- screen: the `workflows` row's status goes `in-design` → `live` (`testing` while rehearsals run);
- the use-case skill's `status: draft` → `active`, changelog line "canonized <date>";
- one Project State decision on total-harness: "<Title> workflow canonized" with the rehearsal's minutes and fix list.
Lessons from runs after that go into the use-case skill; lessons about making workflows go into this skill.

## Learned the hard way
- The input as found sets the workflow. A tool wanting a special format fills a slot or doesn't (DXF was replaced by PDF, 2026-10-10).
- Briefs that create scheduled tasks or need approval cards run in the daytime (Build 30).
- Night sessions have failed to write cbrain data (Build 37). Put data edits in daytime briefs, or carry the exact SQL.
- Build sessions often can't clone repos or push binary files (Builds 33, 42, 51). Plan file moves through the GitHub connector or a GitHub Action.
- Ship the step list with the first brief (Build 37 drew a one-node pipeline until Build 50).
- A change to a screen part and the page that feeds it go in one commit (Build 34).

## Changelog
- 0.1.0 (2026-10-27) — First version, Build 54. The workflow is the canonized result; the speed run is the discovery before it (Charles). Two kinds (screen, chat), the parts list, rehearse-then-canonize (status Live), lessons from the first two workflows. Loaded from Design Assist. Supersedes TH-102 ("no workflow builder skill until a second workflow").
````

## Appendix B — skills/speed-run/SKILL.md (draft)
````markdown
---
name: speed-run
version: 0.1.0
status: draft
triggers: [loaded by skills/workflow when a new workflow has steps or tools nobody has proven yet]
dependencies: [workflow, tech-discovery, tech-review]
owner: Charles
updated: 2026-10-27
source: The Speed-run framework (Claude Doc 2f4b7713, approved 2026-10-09 as TH-024..027, changed TH-069/TH-070), narrowed to discovery by Charles on 2026-10-27 — the speed run finds the steps, the workflow skill canonizes them. Written by Build 54 (BB-2026-10-27-workflow-method).
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: with-you
  starts: "the workflow skill, from a Design Assist chat"
  runs_in: claude-chat
  reads: [project-state, cbrain, repos, claude-docs]
  writes: [plans, claude-docs, rd-handoffs]
  stack: [total-harness]
  origin: yours
  label: Speed run
---

# Speed run — discover how a workflow should work

## What
A speed run is the **discovery** pass for a new workflow. It quickly outlines every step from Charles's one sentence to the finished thing, finds the steps nobody has a proven tool for, and sends those to the R&D lab. Its output is a **researched step list**. It does not build anything; `skills/workflow` takes that list and canonizes it.

It runs ahead of the Total Harness campaign order and pulls forward only the thin slice of each harness block the use case needs. A speed run can end without a workflow: if a step has no tool that passes, the use case parks on the R&D Shelf with that step named.

## When
- Loaded by `skills/workflow` (inside a Design Assist chat) when any step of a new workflow is unknown or needs a tool verdict.
- Skipped when every step reuses something that already works; the workflow skill writes the step list directly.

## Stages
Stages 1-4 need no tech decision and run first. A tool never defines the workflow; it fills a slot in a walkthrough already written.

| # | Stage | Produces | Exit check | Charles |
|---|---|---|---|---|
| 0 | Open | Working Doc "Speed run — <use case>" (tabs: card, harness read, walkthrough, gap sort); record plan on `total-harness` (draft, campaign Total Harness, tags `total-harness`, `speed-run`, `speed-run-<slug>`, `block-N` per slice); one line in agent-library `lab/speed-run.md` | All three exist | — |
| 1 | Use-case card | His sentence verbatim; the input **as it really arrives**; finish line; what "works" means; touch budget; where it runs, data handling, money (no defaults) | Charles confirms | Confirm or correct |
| 2 | Harness read | Which of the 11 pipeline steps it hits; block status (`pm_tasks` `harness-map#bNN`); R&D Shelf rows; slices earlier speed runs built (reuse first); blocks or gates worth pulling in now (TH-070) | Every pipeline step marked hit or not | — |
| 3 | Mock walkthrough | One row per micro-step, sentence to delivered file (columns below) | Every row has a bin; no row says "somehow" | — |
| 4 | Gap sort | Each row binned: **Reuse** / **Slice** (block N) / **Tech slot** (questions + fallback) / **You** (one-time checklist, never a per-run step) | Every tech slot names its questions and a fallback | Run the checklist when it suits |
| 5 | Tech intake (R&D) | Each tech slot handed to the lab (`rd-handoff`, `speed-run-<slug>`); each returned card checked against the tech contract; a slot with no candidate goes as "find candidates for this slot" | Every slot filled, or the speed run parks with the slot named | Run the lab chats it asks for |

**Walkthrough columns:** Step · Who (Claude, a checker, a connector, you) · How (script, connector, screen, you — in that order of preference) · Where (cloud, laptop, bench) · Needs · Could stop it (✓ checked / ~ assumed) · Bin.
**Skeleton every walkthrough covers:** the skill waking on the sentence · tools present where it runs · the input arriving as it really does · reading it · making · self-check · stops · checker · packaging · delivery · lessons.

**Tech contract** (a blank on 1-4 sends the card back): 1 input as found · 2 drivable with no screen, measured time per job · 3 where it can run, pinned version · 4 where the data goes, licence · 5 editable output · 6 quality ceiling from a real test · 7 cost, maturity, fallback.

## Hand-off to the workflow skill
When stage 5 exits, the speed run hands `skills/workflow`:
- the confirmed use-case card;
- the walkthrough rows as the draft step list (each with its chosen tool);
- the slices it pulls forward, with block numbers;
- Charles's one-time checklist.
Add one line to the record plan: "Researched; handed to the workflow skill <date>." The record plan stays a draft index and is never queued.

## Progress tracking
Follows `references/thread-checkin.md`.
- kind: speed-run
- build: "<use case> speed run" (thread_key `speed-run:<slug>`)
- Opens when: stage 0
- Checks in: end of every turn
- Closes when: handed to the workflow skill (closed_how "researched"), or parked on the R&D Shelf (closed_how "parked")

## Changelog
- 0.1.0 (2026-10-27) — First version, Build 54. Moves the speed-run method out of the Claude Doc into a skill and narrows it to discovery (stages 0-5), per Charles: the speed run finds and researches the steps; the workflow skill canonizes them.
````
