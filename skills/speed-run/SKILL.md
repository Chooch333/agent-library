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

## First turn
The first reply, before anything is written:
- names the step or steps nobody has a proven tool for (that is why this is a speed run);
- names the record plan it opens at stage 0, with its tags: `total-harness`, `speed-run`, `speed-run-<slug>` (plus `block-N` once slices are known);
- recommends screen or chat (`skills/workflow` section 2) with one reason;
- drafts the use-case card from Charles's sentence.

**Look up, don't ask, where things live.** Where the input arrives, where the output goes (a sheet, a folder, a repo) and which tools are connected are found by searching the connected tools (Drive, Gmail, GitHub, Project State, cbrain). Put the best find on the card as "found: … (confirm)", or "not found yet — stage 2 looks". Ask Charles only what no tool can tell: his finish line, what "works" means, the touch budget, money.

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
- 0.1.0 (2026-10-27) — First version, Build 54. Moves the speed-run method out of the Claude Doc into a skill and narrows it to discovery (stages 0-5), per Charles: the speed run finds and researches the steps; the workflow skill canonizes them. "First turn" section added after Build 54's cold-read test (the first draft's helper asked where the sheet lived and did not name the record plan's tags).
