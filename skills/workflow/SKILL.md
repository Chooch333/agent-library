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
- Either way, look up where the input and output live and which tools are connected before asking Charles; ask him only what no tool can tell (speed-run, "First turn").

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
