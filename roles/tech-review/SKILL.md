---
name: tech-review
version: 0.1.0
status: draft
triggers: ["Tech review:"]
dependencies: []
owner: Charles
updated: 2026-10-10
source: "Lab rules from the R&D Lab Notebook (read 2026-10-09). Designed in DA chat DA-1009-rd-lab; built in Build 31 (BB-2026-10-09-tech-review-skill)."
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

Runs one R&D lab review. Charles's first message is "Tech review: <name or link>". Claude pulls the harness status and the lab's past verdicts itself, reviews that one tech in a fixed order, and ends with one verdict per tool (Adopt now, Shelf or Never) and a one-page tech card. Nothing is filed until Charles approves the card. The lab's record lives as plain files in `lab/` in this repo, so the shelf and the speed-run brief can change without editing this skill.

## When

**Fire this skill when:**
- A chat's first message starts `Tech review:` — for example "Tech review: https://github.com/storytold/effectcraft". That one line is the whole trigger, in any chat or project.

**Do NOT fire this skill when:**
- "tech review" is only mentioned mid-chat, or a message starts any other way.
- The ask is to review a build plan's architecture before code is written — that is Eng review (`roles/eng-reviewer/SKILL.md`, "eng review").
- The ask is to build permanent setup for a tool. The lab only tests; the Total Harness project builds.

## How

### Where things live

All in `Chooch333/agent-library`. Formats for every file are in `lab/README.md`.

- Shelf rows: `lab/shelf/<tool>.md` — one file per tool.
- Tech cards: `lab/cards/<review>.md` — one file per review.
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
1. Ground facts, checked at the source today: who makes it, how old it is, price, whether a company may use it, whether Claude can run it with no screen.
2. Use case by Q&A: at most three closed questions to me, each with your recommended answer. Then list uses I did not ask about, across the whole harness.
3. Place it: layer, pipeline step, block, and what it would replace in the blueprint.
4. Hands-on test in the cloud workspace wherever possible. Tests only. No permanent setup.
5. Compare: what else does this job, including what Claude does today without it. Then check the tool against each standing requirement of the speed run it serves (listed in `lab/speed-run.md`): yes, because of this workflow; no, because it cannot do this; or not this tool's job. A conceptual path is enough. It does not need its own hands-on test.
6. One verdict per tool, then the tech card.

VERDICTS
- Adopt now: it passed a hands-on test, AND I have seen the test output and said I would use it, AND it serves the speed run or a block that is done, in progress or next in line, AND it is free or I approved the cost.
- Shelf: useful, but its block is further down the order, or it is too new or untested to lean on. Name one trigger: a block number, a maturity milestone, or a date.
- Never: it fails on a hard fact (Claude cannot run it, license or price, duplicates what we have, nothing needs it, unsafe). Name the one fact that would have to change.
Only the speed run pulls a tool ahead of build order.

TECH CARD (one page, plain words, no jargon; explain any term the first time it appears)
What it is. Verdict by tool. Where it fits. What we could use it for: now, later, cannot. What we checked. What else does this job. Requirements check. Risks and cover. If adopted: what gets built, dollars, my hours, proof of done. Sources.
Mark every claim: ✓ checked at a source today, ✓✓ run hands-on, ~ assumed.

FILING (only after I approve the card)
- Only after I approve the card, write `lab/cards/<review>.md` and one `lab/shelf/<tool>.md` per tool with GitHub `create_or_update_file`. A changed verdict (after I approve it) edits the shelf file (`verdict`, `verdict_note`, `come_back_when`, `reviewed`) and adds one dated line at the top of its `## Verdict history`, for example `2026-11-02 · Shelf (was Adopt now) · <reason>`. Never edit or remove a history line. Clear `draft` when the card is approved. If the chat cannot write to the repo, file to the Lab Notebook as before (one row on its Shelf tab, the tech card as a tab beside it, https://claude.ai/code/artifact/f3824046-d946-4da4-bffb-9e68146b619b) and tell me. Do not create a Project State project for the lab.
- Adopt now also files a question on total-harness (origin charles-directed, Session Log ticket per protocol) titled "R&D handoff: <tool>", with the card in its thread, tagged rd-handoff, plus speed-run and speed-run-<slug> when it serves a speed run (the slug is that speed run's entry in `lab/speed-run.md`). Give me the ID.

STANDING RULES
Pick one lane and name what you ruled out. Money always stops. Do not stack assumptions: verify the bottom one first. Push back when I am wrong. Roles fire only when I name them.

THE SPEED RUN
Speed runs are listed in `lab/speed-run.md`, one entry per active speed run, each pointing to its use-case card. Judge every tool against the requirements of the speed run it serves, and say which steps of that speed run the tool serves. A tool that serves no listed speed run waits for its block. Speed runs themselves are designed in the Total Harness project, not in the lab.

## Examples

### Example 1: a suite review (the first card in this format)

"Tech review: ArtCraft Crafting Apps" → read `lab/shelf/*.md` and `lab/speed-run.md` (nothing reviewed yet) → ground facts at the source (seven free apps, EffectCraft eight days old) → up to three closed questions → place it (Digital hands, pipeline step 6, blocks 16, 17, 19) → hands-on test in the cloud workspace (a 7-second phasing chart rendered by script) → compare (Remotion, Motion Canvas, Claude writing animation code) and check each arch-renders requirement → one verdict per app → card. After Charles approved, the chat would write `lab/cards/artcraft.md` and seven `lab/shelf/*.md` files. Those files are seeded in this repo as drafts (`draft: true`), on hold until Charles approves the card.

### Example 2: a changed verdict

A later review finds EffectCraft stalled. Charles approves the change. The chat edits `lab/shelf/effectcraft.md` (`verdict: shelf`, a `come_back_when` trigger, `reviewed` date) and adds at the top of `## Verdict history`: `- 2026-11-02 · Shelf (was Adopt now) · <reason>`. The older line stays untouched.

## Pitfalls

None yet. Pitfalls must come from real traces; this skill has not run yet.

## Changelog

- **0.1.0** (2026-10-10) — Initial draft. Build 31 (BB-2026-10-09-tech-review-skill). Lab rules copied from the R&D Lab Notebook with seven changes: past verdicts and filing now use `lab/` files; Adopt now also needs Charles to have seen the test output and said he would use it; handoff tags add speed-run-<slug>; THE SPEED RUN points at `lab/speed-run.md`; review step 5 adds a requirements check; the tech card adds a "Requirements check" section.
