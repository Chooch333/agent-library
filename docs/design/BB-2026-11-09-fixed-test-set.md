# Build Brief — BB-2026-11-09-fixed-test-set
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-fixed-test-set.md`
**Project State plan:** `ba6036f3-44dd-497f-ba11-015f11b55a0f` on `total-harness`

**What this is:** Build 75. A fixed set of questions Claude must keep getting right, re-asked whenever something they touch changes, so a fix is proven and a slip shows. Replaces Build 61.1.
**Stack Flow:** no change — the replay runs inside the step-in scorer's weekly helper (Build 74's part).
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build. **After:** Build 74. **Target repo:** Chooch333/agent-library.

**What I'll do (build chat):** add a replay step to the scorer skill, run the whole set once with a separate grader, retire Build 61.1.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-09 (frozen)
"Run the comparison in TH-155. It becomes the first fixed test set."

## Current state going in (verified 2026-11-09)
- `tests/fixed-set.md` is on main (7c1c19b): four tasks with answer keys built from his records, and the first run's results.
- First run (3 questions x 3 setups x 2 runs, graded by the design chat): plain chat 14 step-ins, chat that reads the stack map and decisions 3, seated stack experts 0. Plain chats followed the charter's two-engine line to GitHub Actions twice.
- Build 61.1 (plan 42c1e70c, queued since 2026-11-03) was the only planned test; this replaces it.

## Scope
**In:** `skills/step-in-scorer/SKILL.md` new step S7 Replay; a baseline run of all four tasks; retire Build 61.1.
**Out:** a screen for results; more than two setups per replay; any change to the answer keys' sources.

## Directive
1. **Add S7 Replay** to the scorer skill:
   - Pick tasks whose `Touches:` files changed since the newest note tagged `fixed-set-run` (git log on agent-library and the named paths), or all tasks when the model the helper runs on differs from that note's.
   - For each picked task, two fresh helpers answer it: one plain (reads AGENT.md and the charter, as a new chat would), one as the route a real chat takes now (seats the matching expert per AGENT.md).
   - One more fresh helper grades every answer against the task's key, blind to which setup wrote it: one step-in per key point missed or contradicted, plus one for asking Charles to fetch or test, plus one for an option list where the record settles one path.
   - File one note on total-harness tagged `fixed-set-run`: per task and setup the step-ins and which key points missed; the commit of `tests/fixed-set.md`, of each touched file, and the model. Append the row to the file's Runs table.
2. **Baseline.** Run S7 on all four tasks now. T4 should read 0 on both setups now that the transcript route is live.
3. **Retire Build 61.1:** `replaces` it from this plan.

## Acceptance criteria
1. S7 is in the skill on main and reads back identical.
2. A `fixed-set-run` note with all four tasks and a separate grader.
3. T4 scores 0 on both setups.
4. Build 61.1 shows replaced by this plan.

## Cost
Subscription only. *Assumed:* a full replay is about nine helpers; weekly replays touch only changed tasks.

## Decisions
- [Claude-per-doctrine] Keys cite his records, never an expert's answer, so the expert setup is not graded against itself (ai-system-design seat).
- [Claude-per-doctrine] A separate grader helper, never the helper that answered or the chat that wrote a fix.
- [Claude-per-doctrine] Three or four tasks are too few to prove small changes; the set grows by one task per fixed cluster (Build 76). A change from 14 to 3 is real; 1 to 0 is not.

## Pasteable prompt
> Build 75 — execute Build Brief BB-2026-11-09-fixed-test-set. Pull the plan from Project State (plan_id ba6036f3-44dd-497f-ba11-015f11b55a0f, project total-harness). Answer forks yourself; stop only at hard gates.
