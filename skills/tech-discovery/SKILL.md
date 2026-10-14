---
name: tech-discovery
version: 0.1.0
status: draft
triggers: ["Tech discovery:"]
dependencies: []
owner: Charles
updated: 2026-10-14
source: "Split out of tech-review 0.2.1 by Charles, 2026-10-14 (R&D lab chat). Steps and brief format are the tech-review 0.1.1 review and tech card, minus the hands-on test."
wiring:
  runs: with-you
  starts: "\"Tech discovery:\""
  runs_in: claude-chat
  reads: [repos, project-state]
  writes: [repos]
  stack: []
  origin: yours
  label: Tech discovery
---

# Tech Discovery

## What

The first look at one tech for the R&D lab: what it is, what it could do for the Total Harness, and whether it is worth a test run. Charles's first message is "Tech discovery: <name or link>". Claude pulls the harness status and the lab's past verdicts itself, researches the tech from its sources, and ends with a Discovery Brief and a Shelf or Never verdict. There is no hands-on test here. Testing is Tech Review (`skills/tech-review/SKILL.md`), which picks up this brief, often much later. Many techs never get a test run. Nothing is filed until Charles approves the brief.

## When

**Fire this skill when:**
- A chat's first message starts `Tech discovery:`, for example "Tech discovery: https://github.com/storytold/effectcraft". That one line is the whole trigger, in any chat or project.

**Do NOT fire this skill when:**
- The first message starts `Tech review:`. That is the test run (`skills/tech-review/SKILL.md`).
- "tech discovery" is only mentioned mid-chat, or a message starts any other way.
- The ask is to compare several different techs that do the same job. That is the separate overarching review.
- The ask is to build permanent setup for a tool. The lab never builds; the Total Harness project does.

## How

### Where things live

All in `Chooch333/agent-library`. Formats for every file are in `lab/README.md`.

- Discovery Briefs: `lab/briefs/<tech>.md`, one file per tech.
- Shelf rows: `lab/shelf/<tool>.md`, one file per tool or variant with a verdict.
- R&D Reports (test runs, not written here): `lab/cards/<review>.md`.
- The speed-run brief: `lab/speed-run.md`.

This block is the only place these paths are set for this skill. In the rules below, "the speed run" means a speed run listed in `lab/speed-run.md`.

### Lab rules

AT THE START OF EVERY CHAT (my first message is only "Tech discovery: <name or link>"; pull everything else, do not ask me to paste it)
- Read PROTOCOL.md and AGENT.md as usual.
- Harness status: Project State project total-harness (list_plans, latest notes) and the map at Chooch333/cbrain concepts/harness-map.md.
- Past work: read every `lab/shelf/*.md`, the list of `lab/briefs/` and `lab/cards/`, and `lab/speed-run.md`. If this tech already has a brief, say so and ask whether to update it or stop.

THE DISCOVERY, IN ORDER
Keep one Working Document per chat. Findings go in the document. Chat is for choices only.
1. Ground facts, checked at the source today: who makes it, how old it is, which version, price, whether a company may use it, whether Claude can run it with no screen.
2. Use case by Q&A: at most three closed questions to me, each with your recommended answer. Then list uses I did not ask about, across the whole harness.
3. Place it: layer, pipeline step, block, and what it would replace in the blueprint.
4. What else does this job, including what Claude does today without it.
5. Requirements check against the speed run it serves: yes, because of this workflow; no, because it cannot do this; or not this tool's job. A conceptual path is enough.
6. One verdict per tool, then the Discovery Brief.
No hands-on test, no installs, no measured runs. Watching a published demo or reading its examples is fine. If a question can only be settled by running it, write it under "Test run, if we do one".

VERDICTS (discovery can only Shelf or Never)
- Shelf: worth keeping. Name one trigger: a block number, a maturity milestone, a date, or "test run" when the next step is a Tech Review.
- Never: it fails on a hard fact (Claude cannot run it, license or price, duplicates what we have, nothing needs it, unsafe). Name the one fact that would have to change.
- Adopt now is not possible from discovery. It needs a hands-on test I have seen. The best a promising tech gets here is Shelf with trigger "test run".

DISCOVERY BRIEF (one page, plain words, no jargon; explain any term the first time it appears)
Title: the use it could serve, then the tech (e.g. "Video Game Asset Generator - Sinnon"), marked "Discovery Brief" with the date.
Sections, in order:
What it is. Verdict by tool. Where it fits. What we could use it for: now, later, cannot. What we checked. What else does this job. Requirements check. Risks and cover. If adopted: what gets built, dollars, my hours, proof of done. Test run, if we do one: the one test problem, the input, the variants worth comparing, and the questions only a test can settle. Sources.
Mark every claim Published (from the maker's own documentation or another source checked today) or Assumed (our judgment). Nothing in a brief is Tested.
Publish the brief as an artifact page.

FILING (only after I approve the brief)
- Write `lab/briefs/<tech>.md`: the whole brief, word for word with the page. Front matter per `lab/README.md`.
- Write or update one `lab/shelf/<tool>.md` per tool: set `brief` to the brief's file name, the verdict, `come_back_when`, `reviewed`. A new shelf file's first history line is `- YYYY-MM-DD · <Verdict> · Discovery (<brief>)`. A changed verdict adds a dated line at the top; never edit or remove a history line.
- Clear `draft` when the brief is approved.
- Discovery files no handoff to Total Harness and no Project State entries. Do not create a Project State project for the lab.

STANDING RULES
Pick one lane and name what you ruled out. Money always stops. Do not stack assumptions: verify the bottom one first. Push back when I am wrong. Skills fire only when I name them.

THE SPEED RUN
Judge every tool against the requirements of the speed run it serves (`lab/speed-run.md`), and say which steps of that speed run it would serve. A tool that serves no listed speed run waits for its block.

## Examples

### Example 1: a discovery that ends at Shelf, test run next

"Tech discovery: https://github.com/pascalorg/editor" → read the shelf, briefs and speed-run brief (nothing on Pascal) → ground facts (free, open source, runs in a browser) → two closed questions → place it (arch-renders steps 2–3, plans to model) → what else does this job (2D-to-3D route already handed to Total Harness) → requirements check (graphics quality: path exists, not proven) → Shelf, trigger "test run" → brief. After approval: `lab/briefs/pascal-editor.md` and `lab/shelf/pascal-editor.md` with `brief: pascal-editor`. A later "Tech review: Pascal Editor" picks up the brief from the shelf row.

### Example 2: a discovery that ends at Never

"Tech discovery: usecrayon.ai" → no API, connector or command line, so Claude cannot drive it → Never, "Crayon opens an API or connector". The brief still records the pipeline worth copying.

## Pitfalls

- **Client material in this public repo** (Pascal Editor review, 2026-10-11). Briefs are public. Never put a client building's details in one.

## Changelog

- **0.1.0** (2026-10-14) — New skill (Charles, R&D lab). Discovery split out of tech-review: ground facts, use case Q&A, place it, what else does this job, requirements check, Shelf or Never. Output is a Discovery Brief filed in `lab/briefs/`, in the old tech card format plus a "Test run, if we do one" section. Tech Review is now the test run only.
