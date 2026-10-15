---
name: tech-review
version: 0.3.1
status: draft
triggers: ["Tech review:"]
dependencies: []
owner: Charles
updated: 2026-10-14
source: "Lab rules from the R&D Lab Notebook (read 2026-10-09). Designed in DA chat DA-1009-rd-lab; built in Build 31 (BB-2026-10-09-tech-review-skill). R&D Report format set by Charles 2026-10-14 (Flythrough Renderer - Blender review). Discovery split into tech-discovery by Charles 2026-10-14."
requires: [references/project-state.md]
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

The test run of one tech in the R&D lab. Charles's first message is "Tech review: <name or link>". The tech has usually had a discovery run already (`skills/tech-discovery/SKILL.md`), so Claude finds its Discovery Brief itself and builds on it, then tests the tech across its own variants and ends with one verdict per test environment (Adopt now, Shelf or Never) and an R&D Report. Charles does not have to name the brief. Nothing is filed until Charles approves the report. The lab's record lives as plain files in `lab/` in this repo, so the shelf and the speed-run brief can change without editing this skill.

## When

**Fire this skill when:**
- A chat's first message starts `Tech review:`, for example "Tech review: Blender for flythroughs". That one line is the whole trigger, in any chat or project.

**Do NOT fire this skill when:**
- The first message starts `Tech discovery:`. That is the first look, with no test (`skills/tech-discovery/SKILL.md`).
- "tech review" is only mentioned mid-chat, or a message starts any other way.
- The ask is to review a build plan's architecture before code is written. That is Eng review (`skills/eng-reviewer/SKILL.md`, "eng review").
- The ask is to build permanent setup for a tool. The lab only tests; the Total Harness project builds.
- The ask is to compare several different techs that do the same job. That is the separate overarching review.

## How

### Where things live

All in `Chooch333/agent-library`. Formats for every file are in `lab/README.md`.

- Shelf rows: `lab/shelf/<tool>.md`, one file per tool or variant with a verdict. A shelf row's `brief` field names its Discovery Brief.
- Discovery Briefs (read here, written by tech-discovery): `lab/briefs/<tech>.md`.
- R&D Reports: `lab/reports/<review>.md`, one file per review. (Older reports may still sit in the old `lab/cards/` folder until it is removed; read both.)
- R&D Report template: `lab/templates/rd-report.html`, the approved layout, as a published page.
- The speed-run brief: `lab/speed-run.md`, the active speed runs and their requirements.

This block is the only place these paths are set for this skill. In the rules below, "the speed run" means a speed run listed in `lab/speed-run.md`.

### Lab rules

This space is a lab, not a project plan. Tech for the Total Harness gets tested in any order, as it comes up. Each chat tests one tech and ends with a verdict. The lab never builds permanent setup. The Total Harness project does that.

AT THE START OF EVERY CHAT (my first message is only "Tech review: <name or link>"; pull everything else, do not ask me to paste it)
- Read AGENT.md as usual, then the files this skill's `requires:` header names.
- Harness status: Project State project total-harness (list_plans, latest notes) and the map at Chooch333/cbrain concepts/harness-map.md. Project State is the record.
- Past verdicts: read every `lab/shelf/*.md`, the list of `lab/reports/`, and `lab/speed-run.md`, so nothing is tested twice.
- Find the Discovery Brief, without asking me: if I gave a brief name, use it. Otherwise match the tech to a shelf row and read its `brief` field. Otherwise search the file names and titles in `lab/briefs/` for the tech or its link. Say which brief you found, or that there is none.
- The speed run: see the bottom of these instructions.

THE REVIEW, IN ORDER
Keep one Working Document per chat. Findings go in the document. Chat is for choices only.
1. Start from the brief. Re-check only what goes stale at the source today: version, price, licence. Carry the rest forward, still marked as the brief marked it. If there is no brief, do the brief's ground facts first (maker, age, version, price, whether a company may use it, whether Claude can run it with no screen) and say the test is running without a discovery.
2. Use case: if the brief settled it, state it in one line and move on. If not, or if it changed, at most three closed questions to me, each with your recommended answer.
3. Map what it can do before designing the test. Go deep when there is no brief or the brief is thin (no clear list of what it can do, no "Test run, if we do one", or how it runs is mostly Assumed). Read the maker's docs, examples, changelog and open issues, and watch a demo, until you can fill in:
   - What it can do: every feature that could touch the use case, and its limits (size, length, resolution, file types in and out, one at a time or in batches).
   - Where it runs: my PC, the cloud machine Claude works on, the maker's servers, or a browser; and what it needs there (graphics card, memory, operating system, an account).
   - Cost to run: per output or per hour of machine time, including any cloud machine or credits it uses.
   - Subscription cost: what the free tier allows, the paid plans, and which plan the test needs. Money still stops.
   - How Claude controls it: an official connector, an API (a way for programs to talk to it), a command line or script, Claude driving a browser or screen, or not at all. Note whether it works with no screen and whether a login or captcha blocks Claude.
   - Licence: whether a company may use what it makes.
   Mark each item Published or Assumed. Anything only a run can settle becomes a test in step 4. Put the map in the Working Document. With a strong brief, check its answers against this list and fill only the gaps.
4. Design the test plan from the map, not from the first feature that looks right. One test problem in one sentence, one test input (reuse a saved lab input when one fits, so reports stay comparable), and the test environments, meaning the tech's own variants (engine, machine, settings). Start from the brief's "Test run, if we do one". The plan must cover:
   - every capability the use case leans on, not only the headline feature;
   - every item from step 3 still marked Assumed: time it, price it, and try Claude's control route for real;
   - for each test, what it proves and how it is measured.
   A capability that matters but cannot be tested now is named in the plan with the reason, and shows as untested in the report. Hold everything else fixed. Put the test plan in the Working Document before running; stop for my yes only if a test costs money or is hard to undo.
5. Hands-on test in every environment wherever possible. Tests only. No permanent setup. Drive the tech the way Claude would in the real workflow (connector, API, script or browser), not by a shortcut the workflow could not use. Measure time, cost and quality the same way in each, and make one output per environment (a clip, a still, a file) so I can judge quality by looking. A failed environment still gets its row, with the reason.
   Save successful test outputs when a later workflow step could use them as input (a model file, an export, stills, the input file that produced them). They become test files for checking the handoff between workflow steps. Store them privately, never in this repo (it is public): for arch-renders, `Chooch333/arch-renders` `lab/<review>/` (private) or a folder on my PC. List each saved file and where it lives under "Experiment parameters".
6. Requirements check: check the tech against each standing requirement of the speed run it serves (listed in `lab/speed-run.md`): yes, because of this workflow; no, because it cannot do this; or not this tool's job. Start from the brief's answers and mark which ones the test now proves.
7. One verdict per test environment, then the R&D Report.
Comparing this tech with other tech ("what else does this job", "where it fits") is not part of a tech review. The brief holds the first look; the separate overarching review does the comparison.

VERDICTS
- Adopt now: it passed a hands-on test, AND I have seen the test output and said I would use it, AND it serves the speed run or a block that is done, in progress or next in line, AND it is free or I approved the cost.
- Shelf: useful, but its block is further down the order, or it is too new or untested to lean on. Name one trigger: a block number, a maturity milestone, or a date.
- Never: it fails on a hard fact (Claude cannot run it, license or price, duplicates what we have, nothing needs it, unsafe). Name the one fact that would have to change.
Only the speed run pulls a tool ahead of build order.

R&D REPORT (plain words, no jargon; explain any term the first time it appears)
Published as an artifact page and filed as `lab/reports/<review>.md`. The template is the first approved report: `lab/templates/rd-report.html` (layout and styling) and `lab/reports/flythrough-renderer-blender.md` (filed form). Copy its layout and change only the content.
- Title block. On the left:
  - the use studied, as the title (e.g. "Flythrough Renderer");
  - the tech and its version on a second line, same size (e.g. "Blender 4.5.14 (PC) · 5.2.2 (cloud)");
  - the test problem in one sentence ("Study the output quality and speed of …").
  On the right, behind a vertical line: Test date, Test completion date, Rev history (numbered from 0, each with a date and a few words), and Report status (Draft or Complete), set apart at the bottom.
- Evidence key, one line: Tested (we ran it and measured it), Published (from the maker's own documentation), Assumed (our judgment, not yet checked). Mark every claim with one of these.
- 01 Tech description. What it is, with no commentary. Then a short "How it runs" list from step 3: where it runs, subscription cost, cost to run, how Claude controls it, and what it needs (hardware, accounts), each marked Tested, Published or Assumed.
- 02 Findings. The gist in one paragraph that reads without scrolling: what works, how fast, at what cost, and the route to adopt. Then three key numbers. Then two lists: the inputs the workflow must supply, and the harness the Total Harness project needs to build.
- 03 Experiment parameters. One sentence on what was tested and compared, then a table: test input, the test itself, capabilities tested, capabilities not tested (with why), output, settings, machines and versions, what was measured, side checks, saved test files.
- 04 Results by test environment. One row per environment of the studied tech only. Each row puts its output (the clip or image, playable in the page) beside its numbers: time per output, time for the full deliverable, cost, quality, verdict pill and verdict note. Then one same-frame or same-view comparison image across all environments.
- 05 Use cases: now, later, cannot.
- 06 Requirements check.
- 07 Risks and cover.
- 08 If adopted: what gets built, dollars, my hours, proof of done.
- 09 Sources. The Discovery Brief is the first source when there is one.
Output files keep stable names (`<output>_<engine>_<machine>.<ext>`, e.g. `clip_cycles_pc.mp4`). The filed report lists them in its front matter (`clips`, `report_url`) so the R&D tab can show them.

FILING (only after I approve the report)
- Only after I approve the report, write `lab/reports/<review>.md` and one `lab/shelf/<tool>.md` per tool or variant with a verdict, using GitHub `create_or_update_file`. Set the report's `brief` front matter to the brief's file name when there is one. On the shelf row, set `report` and keep `brief`.
- The filed report is the whole report, word for word with the published page: every section, every result row and every evidence mark. Do not condense it. Write each result environment as its own `###` heading with its numbers as bold-labelled bullets, and give each clip an `anchor` in the front matter (the page's row id) so the R&D tab can link to it. Name the comparison image in `image`. Clips and images stay on the published page and in private storage, never in this repo. When the report is revised, edit the page and the filed copy together.
- Never edit the Discovery Brief. It records the first look; the report records the test.
- A changed verdict (after I approve it) edits the shelf file (`verdict`, `verdict_note`, `come_back_when`, `reviewed`) and adds one dated line at the top of its `## Verdict history`, for example `2026-11-02 · Shelf (was Adopt now) · <reason>`. Never edit or remove a history line.
- Clear `draft` when the report is approved.
- If the chat cannot write to the repo, file to the Lab Notebook as before (one row on its Shelf tab, the report as a tab beside it, https://claude.ai/code/artifact/f3824046-d946-4da4-bffb-9e68146b619b) and tell me.
- Do not create a Project State project for the lab.
- Adopt now also files a question on total-harness: origin charles-directed, Session Log ticket per protocol, titled "R&D handoff: <tool>", with the report in its thread. Tag it rd-handoff, plus speed-run and speed-run-<slug> when it serves a speed run (the slug is that speed run's entry in `lab/speed-run.md`). Give me the ID.

STANDING RULES
Pick one lane and name what you ruled out. Money always stops. Do not stack assumptions: verify the bottom one first. Push back when I am wrong. Skills fire only when I name them.

THE SPEED RUN
Speed runs are listed in `lab/speed-run.md`, one entry per active speed run, each pointing to its use-case card. Judge every tool against the requirements of the speed run it serves, and say which steps of that speed run the tool serves. A tool that serves no listed speed run waits for its block. Speed runs themselves are designed in the Total Harness project, not in the lab.

## Examples

### Example 1: the template review (the first R&D Report)

"Tech review: Blender for flythroughs" → read `lab/shelf/*.md` and `lab/speed-run.md`; no Discovery Brief (it predates the split), so ground facts first (free, GPL, scriptable; versions 4.5.14 on the PC, 5.2.2 in the cloud).

Design the experiment:
- Test problem: "Study the output quality and speed of Blender for architectural flythroughs."
- Input: the render-lab house, already approved for stills.
- Four environments: Cycles and EEVEE, each on the PC graphics card and in the cloud.

Test each one: same camera move, one clip each. The cloud EEVEE run failed for lack of memory and kept its row.

Requirements check → verdicts: Cycles on PC Adopt now; cloud Cycles Never for clips; EEVEE Never → R&D Report. Filed as `lab/reports/flythrough-renderer-blender.md` with two shelf rows.

### Example 2: picking up a brief without being told

"Tech review: Pascal Editor" → `lab/shelf/pascal-editor.md` has `brief: pascal-editor` → read `lab/briefs/pascal-editor.md` → re-check version and licence only → its use case and "Test run, if we do one" become steps 2 and 4 → step 3 fills only the gaps the brief left → test → report with `brief: pascal-editor` in its front matter.

### Example 3: a changed verdict

A later review finds EffectCraft stalled, and Charles approves the change. The chat edits `lab/shelf/effectcraft.md`: `verdict: shelf`, a `come_back_when` trigger, and the `reviewed` date. It adds at the top of `## Verdict history`: `- 2026-11-02 · Shelf (was Adopt now) · <reason>`. The older line stays untouched.

## Pitfalls

- **Test outputs not kept** (Pascal Editor review, 2026-10-11). The GLB export was checked inside the browser and never saved, so TH had no file for testing the Pascal-to-Blender handoff. Save outputs as step 4 says.
- **Client material in this public repo** (same review). A script holding a client building's dimensions was committed to `lab/`, then deleted; it stays in git history. Test inputs and outputs from client drawings go to private storage only.
- **Mismatched versions across environments** (Blender review, 2026-10-14). The PC ran 4.5 and the cloud 5.2, so one effect (the distance haze) rendered in one place only. Put the same version in every environment, or name each version in the title and explain the difference under Experiment parameters.

## Changelog

- **0.3.1** (2026-10-14) — "Cards" retired (Charles, R&D lab). Reports live in `lab/reports/`; the shelf field `card` is now `report`. Build 32.1 moves the files and points the R&D tab at the new folder.

- **0.3.0** (2026-10-14) — Tech Review is now the test run only (Charles, R&D lab). Discovery moves to the new `skills/tech-discovery/SKILL.md` ("Tech discovery:"), which files Discovery Briefs in `lab/briefs/`. This skill finds the brief itself (shelf row `brief` field, then `lab/briefs/` by name), re-checks only version, price and licence, and starts the experiment from the brief's "Test run, if we do one". Reports and shelf rows carry `brief`. The brief is never edited here.

- **0.2.1** (2026-10-14) — Filing: the filed report in `lab/cards/` is the whole report, word for word with the published page, with one `###` heading per result environment, clip `anchor`s and the comparison `image` in front matter (Charles, DA-1014-rd-reports). The Blender report was refiled this way the same day.

- **0.2.0** (2026-10-14) — R&D Report replaces the tech card (Charles, R&D lab). The new format comes from the Flythrough Renderer - Blender review. Review steps 3–6 now design and run one experiment across the tech's own environments, with one output per environment. "Place it" and "What else does this job" move out to the separate overarching review. Template at `lab/templates/rd-report.html`. One new pitfall.

- **0.1.1** (2026-10-11) — Review step 4: save successful test outputs privately for workflow handoff tests (Charles, R&D lab). Two pitfalls from the Pascal Editor review.

- **0.1.0** (2026-10-10) — Initial draft. Build 31 (BB-2026-10-09-tech-review-skill). Lab rules copied from the R&D Lab Notebook with seven changes: past verdicts and filing now use `lab/` files; Adopt now also needs Charles to have seen the test output and said he would use it; handoff tags add speed-run-<slug>; THE SPEED RUN points at `lab/speed-run.md`; review step 5 adds a requirements check; the tech card adds a "Requirements check" section.
