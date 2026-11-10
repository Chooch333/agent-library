# Build Brief — BB-2026-11-09-fixed-test-set
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-fixed-test-set.md`
**Project State plan:** `ba6036f3-44dd-497f-ba11-015f11b55a0f` on `total-harness`

**What this is:** Build 75. A fixed set of questions Claude must keep getting right, re-asked whenever something they touch changes, so a fix is proven and a slip shows. Replaces Build 61.1.
**Stack Flow:** no change — the replay is run by the Design Assist chat that starts the weekly step-in scorer (Build 74's part); no new running part.
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build. **After:** Build 74. **Target repo:** Chooch333/agent-library.

**What I'll do (build chat):** add a Replay section to the scorer skill and one line to Design Assist, and check that Build 61.1 shows replaced.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-09 (frozen)
"Run the comparison in TH-155. It becomes the first fixed test set."

## Current state going in (verified 2026-11-09)
- `tests/fixed-set.md` is on main: five tasks with answer keys built from his records, the rules every task follows, and the first run's results. Revised 2026-11-09: real file paths under Touches, `until:` on key points that are true only for now, experts' own lines removed from the keys, and a fifth task whose right answer is to stop and ask.
- First run (3 questions x 3 setups x 2 runs, graded by the design chat): plain chat 14 step-ins, chat that reads the stack map and decisions 3, seated stack experts 0. Those answers were not kept and the grader was the chat that wrote the keys, so the rows are not comparable with later ones.
- A helper cannot start helpers. Verified twice on 2026-11-09: two helpers started from a chat had no tool to start another. So a replay cannot run inside the scorer's helper; the chat has to start every answer and the grader.
- Overnight build sessions have had no helper tool (lanes Our way 4; TH-J-001, TH-J-022), so this build cannot run a replay itself.
- Build 61.1 (plan 42c1e70c) was the only planned test; this replaces it.
- *Revised 2026-11-09* after the scoring-and-testing expert reviewed this brief (TH-160, TH-162). What changed: who runs the replay, two runs per setup, a grader that is really blind and can say it can't tell, answers kept, replays that write nothing.

## Scope
**In:** `skills/step-in-scorer/SKILL.md` new section Replay; `skills/design-assist/SKILL.md` step 1, one line; Build 61.1 shown as replaced.
**Out:** a screen for results; more than two setups per replay; running a replay inside this build; changes to `tests/fixed-set.md` (done in the design pass).

## Directive
1. **Add a Replay section** to the scorer skill, headed "Run by the chat, never by the scorer's helper":
   - **Pick.** A task is picked when a file under its `Touches:` (or one of the three routing files every task touches) changed since that task's last recorded run (commit history on agent-library for the named paths), when the model differs from that run's, or when the task has no run graded by a separate helper. At most two tasks per replay: tasks never run go first, then the ones run longest ago. The run note lists the tasks left waiting.
   - **Stale points.** A key point whose `until:` has happened is marked stale and not scored.
   - **Answer.** Each picked task is answered twice per setup (Charles: "two runs each"). Plain setup: a fresh helper given AGENT.md and the charter, as a new chat would be. Real route: the chat seats the matching expert through the Expert Desk, mode B, as a real chat does now. Every answer helper is told this is a replay: write nothing anywhere; where a right answer would commit, queue or send something, state the exact file and content instead; answer in plain prose as you would to Charles, with no headings and no seat or skill names.
   - **Grade.** One fresh helper gets the keys and the answers with setup labels removed and the order shuffled. For each key point it returns met, missed, contradicted or can't tell, with the sentence it saw. Step-ins = missed + contradicted, plus one for asking Charles to fetch or test, plus one for an option list where the record settles one path. Can't tell is counted on its own line, never as met.
   - **Record.** One note on total-harness tagged `fixed-set-run`: per task, setup and run, the step-ins and each key point's verdict; the full answers and the grader's reply; which expert was seated; the commit of `tests/fixed-set.md` and of each touched file; the model. Append the row to the file's Runs table with "a separate helper" under Graded by. A chat that ends before its helpers return files nothing, and the next replay picks the same tasks again.
2. **Design Assist step 1,** one line after the scorer line Build 74 adds: run the scorer skill's Replay section in this chat when its Pick step returns a task; the helpers run in the background and the note is filed when they return.
3. **Build 61.1:** confirm plan 42c1e70c shows replaced by this plan; set it if not.

## Acceptance criteria
1. The Replay section is in the skill on main and reads back identical.
2. The Design Assist line is on main and reads back identical.
3. Build 61.1 shows replaced by this plan.
4. Handed on, not proven here (A-101): the first replay. No task has a separately graded run, so the first Design Assist chat after this lands picks T4 and T5 and files the first `fixed-set-run` note. The Pick rule is what guarantees it; no separate plan is needed.

## Cost
Subscription only, no money. A replay is at most eight answer helpers and one grader, each about the size of one expert seat (the first run averaged 85k to 134k tokens a helper). *Assumed:* at most one replay a week, because the weekly scorer line is what starts it.

## Decisions
- [Claude-per-doctrine] Keys cite his records, never an expert's answer or an expert's brief, so the expert setup is not graded against itself (ai-system-design seat; scoring-and-testing Lens 2, which found the first keys citing experts' lines).
- [Claude-per-doctrine] A separate grader helper, never the helper that answered or the chat that wrote a fix. The grader sees no setup labels, seat names or headings (scoring-and-testing Lens 18) and may answer can't tell (Lens 22).
- [Claude-per-doctrine] The chat runs the replay, not the scorer's helper, because a helper cannot start helpers; inside a helper the "real route" setup would have been the plain one again (scoring-and-testing seat, TH-160 finding 4; verified).
- [Claude-per-doctrine] Two runs per setup, as Charles asked for the first comparison; the expert asked for three and his words win. One run was the earlier draft, and the first run already showed one setup scoring differently on two runs of one task.
- [Claude-per-doctrine] Two tasks per replay at most: every task touches the routing files, which change often, so without a cap one routing edit would re-ask the whole set (c-stack Lens 4: plan usage has no meter and no brake).
- [Claude-per-doctrine] Replays write nothing: the transcript task's right answer queues a video under Charles's name, and a replay that really did so would put a video he never asked for into intake (TH-160 finding 5).
- [Claude-per-doctrine] A handful of tasks is too few to prove small changes; the set grows by one task per fixed cluster (Build 76). A change from 14 to 3 is real; 1 to 0 is not.

## Pasteable prompt
> Build 75 — execute Build Brief BB-2026-11-09-fixed-test-set. Pull the plan from Project State (plan_id ba6036f3-44dd-497f-ba11-015f11b55a0f, project total-harness). Answer forks yourself; stop only at hard gates.
