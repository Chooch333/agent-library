---
name: tech-review
version: 0.2.0
status: draft
triggers: ["Tech review:"]
dependencies: []
owner: Charles
updated: 2026-10-14
source: "Lab rules from the R&D Lab Notebook (read 2026-10-09). Designed in DA chat DA-1009-rd-lab; built in Build 31 (BB-2026-10-09-tech-review-skill). R&D Report format set by Charles 2026-10-14 (Flythrough Renderer - Blender review)."
wiring:
  runs: with-you
  starts: "\"Tech review:\""
  runs_in: claude-chat
  reads: [repos, project-state]
  writes: [repos]
  stack: []
  origin: yours
  label: Tech review
---

# Tech Review

## What

Runs one R&D lab review. Charles's first message is "Tech review: <name or link>". Claude pulls the harness status and the lab's past verdicts itself, tests that one tech across its own variants, and ends with one verdict per test environment (Adopt now, Shelf or Never) and an R&D Report. Nothing is filed until Charles approves the report. The lab's record lives as plain files in `lab/` in this repo, so the shelf and the speed-run brief can change without editing this skill.

## When

**Fire this skill when:**
- A chat's first message starts `Tech review:` — for example "Tech review: https://github.com/storytold/effectcraft". That one line is the whole trigger, in any chat or project.

**Do NOT fire this skill when:**
- "tech review" is only mentioned mid-chat, or a message starts any other way.
- The ask is to review a build plan's architecture before code is written — that is Eng review (`roles/eng-reviewer/SKILL.md`, "eng review").
- The ask is to build permanent setup for a tool. The lab only tests; the Total Harness project builds.
- The ask is to compare several different techs that do the same job. That is the separate overarching review, not a tech review.

## How

### Where things live

All in `Chooch333/agent-library`. Formats for every file are in `lab/README.md`.

- Shelf rows: `lab/shelf/<tool>.md` — one file per tool or variant with a verdict.
- R&D Reports: `lab/cards/<review>.md` — one file per review. (The folder keeps its old name so the R&D tab keeps reading it.)
- R&D Report template: `lab/templates/rd-report.html` — the approved layout, as a published page.
- The speed-run brief: `lab/speed-run.md` — the active speed runs and their requirements.

This block is the only place these paths are set. If the lab moves, edit this skill and nothing else; the R&D project's instructions point only at this skill. In the rules below, "the speed run" means a speed run listed in `lab/speed-run.md`.

### Lab rules

This space is a lab, not a project plan. Tech for the Total Harness gets reviewed in any order, as it appears. Each chat reviews one tech and ends with a verdict. The lab never builds permanent setup. The Total Harness project does that.

AT THE START OF EVERY CHAT (my first message is only "Tech review: <name or link>"; pull everything else, do not ask me to paste it)
- Read PROTOCOL.md and AGENT.md as usual.
- Harness status: Project State project total-harness (list_plans, latest notes) and the map at Chooch333/cbrain concepts/harness-map.md. Project State is the record.
- Past verdicts: read every `lab/shelf/*.md` and `lab/speed-run.md` first, so nothing is reviewed twice.
- The speed run: see the bottom of these instructions.

THE REVIEW, IN ORDER
Keep one Working Document per chat. Findings go in the document. Chat is for choices only.
1. Ground facts, checked at the source today: who makes it, how old it is, which version, price, whether a company may use it, whether Claude can run it with no screen.
2. Use case by Q&A: at most three closed questions to me, each with your recommended answer. Then list uses I did not ask about, across the whole harness.
3. Design the experiment: one test problem in one sentence, one test input (reuse a saved lab input when one fits, so reports stay comparable), and the test environments, meaning the tech's own variants (engine, machine, settings). Hold everything else fixed.
4. Hands-on test in every environment wherever possible. Tests only. No permanent setup. Measure time, cost and quality the same way in each, and make one output per environment (a clip, a still, a file) so I can judge quality by looking. A failed environment still gets its row, with the reason.
   Save successful test outputs when a later workflow step could use them as input (a model file, an export, stills, the input file that produced them). They become test files for checking the handoff between workflow steps. Store them privately, never in this repo (it is public): for arch-renders, `Chooch333/arch-renders` `lab/<review>/` (private) or a folder on my PC. List each saved file and where it lives under "Experiment parameters".
5. Requirements check: check the tech against each standing requirement of the speed run it serves (listed in `lab/speed-run.md`): yes, because of this workflow; no, because it cannot do this; or not this tool's job. A conceptual path is enough.
6. One verdict per test environment, then the R&D Report.
Comparing this tech with other tech ("what else does this job", "where it fits") is not part of a tech review. It belongs to the separate overarching review.

VERDICTS
- Adopt now: it passed a hands-on test, AND I have seen the test output and said I would use it, AND it serves the speed run or a block that is done, in progress or next in line, AND it is free or I approved the cost.
- Shelf: useful, but its block is further down the order, or it is too new or untested to lean on. Name one trigger: a block number, a maturity milestone, or a date.
- Never: it fails on a hard fact (Claude cannot run it, license or price, duplicates what we have, nothing needs it, unsafe). Name the one fact that would have to change.
Only the speed run pulls a tool ahead of build order.

R&D REPORT (plain words, no jargon; explain any term the first time it appears)
Published as an artifact page and filed as `lab/cards/<review>.md`. The template is the first approved report: `lab/templates/rd-report.html` (layout and styling) and `lab/cards/flythrough-renderer-blender.md` (filed form). Copy its layout and change only the content.
- Title block. On the left:
  - the use studied, as the title (e.g. "Flythrough Renderer");
  - the tech and its version on a second line, same size (e.g. "Blender 4.5.14 (PC) · 5.2.2 (cloud)");
  - the test problem in one sentence ("Study the output quality and speed of …").
  On the right, behind a vertical line: Test date, Test completion date, Rev history (numbered from 0, each with a date and a few words), and Report status (Draft or Complete), set apart at the bottom.
- Evidence key, one line: Tested (we ran it and measured it), Published (from the maker's own documentation), Assumed (our judgment, not yet checked). Mark every claim with one of these.
- 01 Tech description. What it is, with no commentary.
- 02 Findings. The gist in one paragraph that reads without scrolling: what works, how fast, at what cost, and the route to adopt. Then three key numbers. Then two lists: the inputs the workflow must supply, and the harness the Total Harness project needs to build.
- 03 Experiment parameters. One sentence on what was tested and compared, then a table: test input, the test itself, output, settings, machines and versions, what was measured, side checks, saved test files.
- 04 Results by test environment. One row per environment of the studied tech only. Each row puts its output (the clip or image, playable in the page) beside its numbers: time per output, time for the full deliverable, cost, quality, verdict pill and verdict note. Then one same-frame or same-view comparison image across all environments.
- 05 Use cases: now, later, cannot.
- 06 Requirements check.
- 07 Risks and cover.
- 08 If adopted: what gets built, dollars, my hours, proof of done.
- 09 Sources.
Output files keep stable names (`<output>_<engine>_<machine>.<ext>`, e.g. `clip_cycles_pc.mp4`). The filed report lists them in its front matter (`clips`, `report_url`) so the R&D tab can show them.

FILING (only after I approve the report)
- Only after I approve the report, write `lab/cards/<review>.md` and one `lab/shelf/<tool>.md` per tool or variant with a verdict, using GitHub `create_or_update_file`.
- A changed verdict (after I approve it) edits the shelf file (`verdict`, `verdict_note`, `come_back_when`, `reviewed`) and adds one dated line at the top of its `## Verdict history`, for example `2026-11-02 · Shelf (was Adopt now) · <reason>`. Never edit or remove a history line.
- Clear `draft` when the report is approved.
- If the chat cannot write to the repo, file to the Lab Notebook as before (one row on its Shelf tab, the report as a tab beside it, https://claude.ai/code/artifact/f3824046-d946-4da4-bffb-9e68146b619b) and tell me.
- Do not create a Project State project for the lab.
- Adopt now also files a question on total-harness: origin charles-directed, Session Log ticket per protocol, titled "R&D handoff: <tool>", with the report in its thread. Tag it rd-handoff, plus speed-run and speed-run-<slug> when it serves a speed run (the slug is that speed run's entry in `lab/speed-run.md`). Give me the ID.

STANDING RULES
Pick one lane and name what you ruled out. Money always stops. Do not stack assumptions: verify the bottom one first. Push back when I am wrong. Roles fire only when I name them.

THE SPEED RUN
Speed runs are listed in `lab/speed-run.md`, one entry per active speed run, each pointing to its use-case card. Judge every tool against the requirements of the speed run it serves, and say which steps of that speed run the tool serves. A tool that serves no listed speed run waits for its block. Speed runs themselves are designed in the Total Harness project, not in the lab.

## Examples

### Example 1: the template review (the first R&D Report)

"Tech review: Blender for flythroughs" → read `lab/shelf/*.md` and `lab/speed-run.md` → ground facts (free, GPL, scriptable; versions 4.5.14 on the PC, 5.2.2 in the cloud).

Design the experiment:
- Test problem: "Study the output quality and speed of Blender for architectural flythroughs."
- Input: the render-lab house, already approved for stills.
- Four environments: Cycles and EEVEE, each on the PC graphics card and in the cloud.

Test each one: same camera move, one clip each. The cloud EEVEE run failed for lack of memory and kept its row.

Requirements check → verdicts: Cycles on PC Adopt now; cloud Cycles Never for clips; EEVEE Never → R&D Report. Filed as `lab/cards/flythrough-renderer-blender.md` with two shelf rows.

### Example 2: a changed verdict

A later review finds EffectCraft stalled, and Charles approves the change. The chat edits `lab/shelf/effectcraft.md`: `verdict: shelf`, a `come_back_when` trigger, and the `reviewed` date. It adds at the top of `## Verdict history`: `- 2026-11-02 · Shelf (was Adopt now) · <reason>`. The older line stays untouched.

## Pitfalls

- **Test outputs not kept** (Pascal Editor review, 2026-10-11). The GLB export was checked inside the browser and never saved, so TH had no file for testing the Pascal-to-Blender handoff. Save outputs as step 4 says.
- **Client material in this public repo** (same review). A script holding a client building's dimensions was committed to `lab/`, then deleted; it stays in git history. Test inputs and outputs from client drawings go to private storage only.
- **Mismatched versions across environments** (Blender review, 2026-10-14). The PC ran 4.5 and the cloud 5.2, so one effect (the distance haze) rendered in one place only. Put the same version in every environment, or name each version in the title and explain the difference under Experiment parameters.

## Changelog

- **0.2.0** (2026-10-14) — R&D Report replaces the tech card (Charles, R&D lab). The new format comes from the Flythrough Renderer - Blender review. Review steps 3–6 now design and run one experiment across the tech's own environments, with one output per environment. "Place it" and "What else does this job" move out to the separate overarching review. Template at `lab/templates/rd-report.html`. One new pitfall.

- **0.1.1** (2026-10-11) — Review step 4: save successful test outputs privately for workflow handoff tests (Charles, R&D lab). Two pitfalls from the Pascal Editor review.

- **0.1.0** (2026-10-10) — Initial draft. Build 31 (BB-2026-10-09-tech-review-skill). Lab rules copied from the R&D Lab Notebook with seven changes: past verdicts and filing now use `lab/` files; Adopt now also needs Charles to have seen the test output and said he would use it; handoff tags add speed-run-<slug>; THE SPEED RUN points at `lab/speed-run.md`; review step 5 adds a requirements check; the tech card adds a "Requirements check" section.
