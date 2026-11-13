---
name: step-in-scorer
version: 0.2.0
status: draft
triggers: ["Started once a week as a helper by the first Design Assist chat whose intake finds the newest step-in-receipt that read chats more than 7 days old, or none (design-assist step 1)", "Run by hand in a session bound to this claude.ai Project that has the past-chat tools (recent_chats, read_conversation)", "Replay section only: run by a Design Assist chat itself (never a helper) when the Replay Pick step returns a task (design-assist step 1)"]
dependencies: [expert-desk]
owner: Charles
updated: 2026-11-10
requires: [references/step-in-rubric.md, references/project-state.md]
wiring:
  runs: on-its-own
  starts: "once a week, as a helper started by a Design Assist chat's intake"
  runs_in: claude-chat
  reads: [past chats in this Project, project-state]
  writes: [step-in lessons, step-in receipt note, fixed-set-run note, tests/fixed-set.md Runs table]
  stack: [chats]
  origin: yours
  label: Step-in scorer
---

# Step-in scorer

## What
**Rules (read first).**
1. **This Project's chats only.** Read only chats listed by `recent_chats` in this claude.ai Project. The count is never "how often Charles steps in everywhere", and the receipt's first line says so.
2. **Re-score before you look.** Step S2 reads three earlier chats and counts them fresh *before* reading any step-in record. Never open a step-in lesson, a past receipt's counts or this skill's examples for those chats before your own count is written down.
3. **Read to the end.** Every chat is read to its last turn (at most four `read_conversation` pages). A chat longer than that is read as far as four pages go and listed as cut short. Never score from a chat's title, summary or search snippet.
4. **One record per correction** by `references/step-in-rubric.md`: a turn that corrects two things is two records. An ask is counted, never filed. Can't tell step-in from ask → `step-in-unsure`.
5. **Never file twice.** Before filing, match against what is already recorded (S4). TH-157 and TH-158 were filed by hand on 2026-11-09 and must not be filed again.
6. **Zero read is not zero step-ins.** A run that read no chats says `read 0 chats` and why, carries `step-in-attempt`, and never says "no step-ins".
7. **Nobody is present.** Nothing here asks Charles a question or waits on an answer; every outcome is a lesson, a receipt line or a tag. A helper cannot start helpers: do all of it yourself.
8. **Plain records.** Each record holds only what the rubric's record shape allows: no quotes of his words over a few, no people, clients, jobs or amounts.

Counts how often Charles had to step in. Once a week a helper reads the week's chats in this claude.ai Project, finds each turn where he corrected Claude, redid something himself or said the same thing again, and files one plain lesson per step-in on total-harness, tagged by pattern and skill, so the Rules Inspector can fix what keeps happening. It checks its own reading first by re-scoring three chats from last week blind, and ends with one receipt note whose first line says how much it read. It is one of two numbers, never the only one: misses against the fixed set (Build 75) catch wrong answers Charles never noticed. That second number comes from the Replay section below, which the Design Assist chat runs itself, never this skill's helper.

## When
**Fire when:** a Design Assist chat's intake (design-assist step 1) finds the newest `step-in-receipt` note on total-harness that read chats (not tagged `step-in-attempt`) is more than 7 days old, or there is none, and starts one helper told to fetch this file and follow it; or a session bound to this Project runs it by hand.
**Don't fire when:** the session has no past-chat tools (file the attempt receipt in step 0 and stop); a chat would be grading its own step-ins (out of scope: Design Assist chats never log their own); the chats are outside this Project; the job is scoring misses against the fixed set (that is the Replay section, run by the chat; the weekly helper never runs it).

## How
Project for every write: `total-harness`. Source on every write: `Step-in scorer, run <YYYY-MM-DD>`.

0. **Tools.** Load `recent_chats` and `read_conversation` (ToolSearch, keywords "recent_chats read_conversation conversation_search"). Either one does not load → skip to S6 with C = 0 and the reason `tools not loaded`; tag the receipt `step-in-attempt`. Stop after S6.
1. **S1 Where to start.** `find_by_tags` tags `["step-in-receipt"]`, entity_types `["note"]`, project total-harness. `find_by_tags` expands tags fuzzily: keep only rows whose own tags hold exactly `step-in-receipt`, and drop any tagged `step-in-attempt`. The newest one left is the **previous receipt**; its "Read through" line is the **read-through point**. None → the read-through point is 14 days back (the first run covers the brief's fourteen days) and S2 reads `first run`.
2. **S2 Re-score first.** Previous receipt exists: take three chats from its "Chats read" list (the three newest that were not cut short; fewer listed → all of them). For each, read it to the end (rule 3) and count its step-ins fresh by the rubric. Write the three counts down. Only then `find_by_tags` `["step-in"]` (lessons; exact-tag filter) and count, per chat, the records whose situation names that chat's link (or title and date). A chat's counts match when they are equal. `K` = how many match; the field reads `re-score K of 3` (or `K of M` when fewer than three were listed). Do not file anything from these chats here; they were already scored. No previous receipt → `re-score: first run`.
3. **S3 List chats.** `recent_chats` for chats updated after the read-through point, newest first, at most 5 pages; stop paging once a page reaches past the read-through point. This Project only. Leave out the chat that started you (it is still open; next week's run reads it). `L` = how many listed.
4. **S4 Read each chat.** For each listed chat, `read_conversation` page by page to its end, at most four pages; a chat still going after four is **cut short** (`X` counts them; it still counts as read). A chat that errors or comes back empty is **couldn't read** (listed with the reason; not in C). `C` = chats read. Mark every Charles turn by the rubric:
   - **step-in**: he corrected Claude, redid something himself, or said the same thing again. One per correction.
   - **ask**: his plain answer to a fair question only he could answer (the rubric's rule). Counted as `A`, never filed.
   - **unsure**: can't tell which → counted as `U`, filed with tag `step-in-unsure` instead of `step-in`.
   Before filing, `find_by_tags` `["step-in", "step-in-unsure"]` (lessons, exact-tag filter, limit 200). A step-in is **already recorded** when a record's situation names the same chat (its link; when the record has no link, the same chat title and date) and the same correction. Already recorded → counted in N, not filed again.
   Also check Charles's own correction decisions: `find_by_tags` `["charles-correction"]` (decisions, all projects, exact-tag filter). A step-in that matches a `charles-correction` decision on the same chat (its link, its title and date, or its board tag, the decision's `chat_tag`) **and the same correction** counts as already on record (its display id goes in the receipt's "already on record" list); never filed twice. A chat's other misses, ones no decision names, are still filed.
5. **S5 File.** One `add_lesson` per new step-in (and per unsure), severity `normal`:
   - situation: `Step-in, chat "<title>" (<date>, <link>), turn <n>, <skill-slug and section, or no skill>: Claude did: <one line>.`
   - lesson: `Charles wanted: <one line>.`
   - applies_to: the skill or kind of chat that would carry the fix.
   - tags: `step-in` (or `step-in-unsure`), one `pattern-<name>` from the rubric, `same-correction-twice` beside it when he already corrected the same thing in an earlier chat (check the records you just read), `skill-<slug>` or `skill-none`, `self-learning-loop`. When S2 gave K of 1 or 0, every record this run files also carries `unchecked`; the Rules Inspector skips those (Build 76).
6. **S6 Receipt.** One `add_note`, tags `step-in-receipt`, `self-learning-loop` (plus `step-in-attempt` when C = 0). Content:
   - **First line**, exactly: `Step-ins: N in C chats of this Project only (listed L, cut short X, D days), asks A, unsure U, re-score K of 3` — or `re-score: first run` in place of the last field. N counts every step-in found in the chats read, filed now or already on record. D = whole days from the read-through point to now. When C = 0 the first line instead reads `Step-ins: read 0 chats: <reason> (listed L, D days), re-score: <K of 3 or first run>`; never "no step-ins".
   - `Filed: F new (lesson display ids), already on record: R (display ids).`
   - `By pattern:` one line per pattern with its count (`same-correction-twice` and `step-in-unsure` on their own lines).
   - `Chats read:` one line per chat: title, date, link, `cut short` when it was. The next run re-scores from this list.
   - `Couldn't read:` one line per chat with the reason, or `none`.
   - `Read through: <ISO time>`: the last-updated time of the newest chat read. When C = 0, repeat this run's read-through point unchanged, so the next run starts from the same place.
7. **Report** to the chat that started you, in two lines: the receipt's first line and its display id. That chat does not wait on it past its own reply.

## Replay: run by the chat, never by the scorer's helper
Re-asks the fixed set (`tests/fixed-set.md` on agent-library) so a fix is proven and a slip shows. A helper cannot start helpers, so a replay run inside the weekly helper would answer every "real route" question with the plain setup; the Design Assist chat runs this section itself, starting every answer helper and the grader. A session with no Agent tool (overnight build sessions) does not run a replay; it says so in one line. Project for every write: `total-harness`. Source: `Fixed-set replay, <YYYY-MM-DD>`.

1. **R1 Pick.** Read `tests/fixed-set.md` (note its commit) and `find_by_tags` `["fixed-set-run"]` (notes, exact-tag filter). A task's **last recorded run** is the newest `fixed-set-run` note that ran it; the Runs table rows graded by the design chat count as runs for the dates only, never as graded by a separate helper. A task is **picked** when any of these holds:
   - a file under its `Touches:`, or one of the three routing files every task touches (`AGENT.md`, `experts/INDEX.md`, `skills/expert-desk/SKILL.md`), has a commit on agent-library main after that run (`list_commits` with the path, or the commit history for the named paths);
   - the model this chat runs on differs from that run's model;
   - the task has no run graded by a separate helper.
   At most two tasks per replay: tasks never run first, then the ones run longest ago. Nothing picked → no replay; say `Replay: nothing picked` in one line and stop. The others that qualified are **left waiting** and listed in the note.
2. **R2 Stale points.** For each picked task, check every key point carrying `until:`. When what ends it has happened (a plan landed: `get_plan` status succeeded; a setting changed: read it), the point is **stale**: left out of the grader's key and listed in the note as stale, never scored. The next design pass rewrites it.
3. **R3 Answer.** Each picked task is answered **twice per setup**, two setups (Charles: "two runs each"), every answer by a fresh helper, all started in one message and run in the background:
   - **Plain:** a fresh helper given only `AGENT.md` and `references/charter.md`, as a new chat would be, and the task's Ask.
   - **Real route:** the chat seats the matching expert through the Expert Desk, mode B (`skills/expert-desk/SKILL.md`), with the task's Ask as the issue, as a real chat does now. Note which expert was seated.
   Every answer helper's prompt also says, word for word: `This is a replay. Write nothing anywhere: no commits, notes, queue files, messages or plan changes. Where a right answer would commit, queue or send something, state the exact file and its content instead. Answer in plain prose as you would to Charles, with no headings and no seat or skill names.` Keep each answer whole, with its setup and run number, for R5.
4. **R4 Grade.** When all answers are back, start one fresh grader helper (never an answer helper, never this chat, never the chat that wrote a fix). Give it the picked tasks' Ask and key (stale points removed) and the answers with setup labels, seat names and headings removed, numbered in a shuffled order; keep the map from number to setup and run to yourself. Tell it: for each answer and each key point return `met`, `missed`, `contradicted` or `can't tell`, with the sentence it saw; also flag where the answer asks Charles to fetch or test something Claude could, and where it gives an option list where the key settles one path. Map the reply back. **Step-ins** per answer = missed + contradicted + one per fetch-or-test ask + one per needless option list. `Can't tell` is counted on its own line, never as met.
5. **R5 Record.** One `add_note` on total-harness, tags `fixed-set-run`, `self-learning-loop`. Content: first line `Fixed-set run: <tasks> x 2 setups x 2 runs, step-ins plain <n>, real route <n>, can't tell <n>`; then per task, setup and run the step-ins and each key point's verdict; stale points; tasks left waiting; which expert was seated per task; the commit of `tests/fixed-set.md` and of each touched file; the model; the full answers; the grader's full reply. Then append one row per setup to the file's Runs table (`Date | Setup | T1..T5 | Total | Avg helper tokens | Graded by`): each picked task's cell is its two runs' step-ins (`a, b`), every other task `not run`, Graded by `a separate helper`. Commit with a message naming the note's display id; check the commit landed by comparing the file's blob SHA. A chat that ends before its helpers return files nothing: no note, no row, and the next replay picks the same tasks again.

## Progress tracking
None. This skill finishes in one run and leaves nothing open: a run that reads 0 chats files an attempt receipt, which the heartbeat and the weekly check both skip, so the next Design Assist chat's intake starts it again. A replay that never files its note leaves its tasks picked for the next one.

## Examples
**Seed hand run, 2026-11-09 (before this skill).** The self-learning loop design chat scored two chats by hand and filed TH-157 (the graph engineering chat, 2026-11-04: Claude said it could not get a YouTube transcript; Charles supplied it) and TH-158 (the loop scope chat, 2026-11-09: the same miss again, so it also carries the same-correction-twice tag). Both `pattern-cant-reach`, `skill-none`. No receipt was filed, so the first run under this skill reads `re-score: first run`, and S4's match must find both and count them without filing them again.

**First run, 2026-11-10 (Build 74).** The build session (Claude Code, cloud) could not load `recent_chats` or `read_conversation`. Step 0 sent it to S6: receipt first line `Step-ins: read 0 chats: tools not loaded (listed 0, 14 days), re-score: first run`, tagged `step-in-attempt`. The heartbeat and the weekly check skip it, so the first Design Assist chat of the week starts the real first run.

**First replay (expected after Build 75).** No task has a run graded by a separate helper, and T4 and T5 have never run, so R1 picks T4 and T5 and lists T1, T2 and T3 as left waiting. Eight answer helpers (two tasks x two setups x two runs) and one grader; the note is the first `fixed-set-run`. The replay after it picks T1, T2 and T3 in turn, two at a time.

## Pitfalls
- A printed expected count was open to the scorer, and for one of the two seed chats the expert's own read found more corrections than the count said; the check is a blind re-score of earlier chats, never a printed answer. [TH-160 finding 3]
- A helper started from a chat had no tool to start another helper, twice; this skill does all of its work in the one helper. [BB-2026-11-09-step-in-scorer, current state, verified 2026-11-09]
- The Build 74 session could not load the past-chat tools, though the design chat could; a run without them files an attempt receipt instead of reporting zero step-ins. [Build 74 first run, 2026-11-10]
- `find_by_tags` expands tags fuzzily, so `step-in` also returns `step-in-receipt` and `step-in-unsure` rows; keep only rows whose own tags match exactly. [team-builder update mode rule 1]
- The seed record TH-158 carries `pattern-same-correction-twice`, not the bare `same-correction-twice` this skill files; count both as the same tag. [TH-158, 2026-11-09]
- The first fixed-set rows were graded by the chat that wrote the keys and ran the setups, and the answers were not kept, so they cannot be compared with later rows; the Replay grader is a separate helper, blind to the setup, and the answers are stored in the note. [tests/fixed-set.md Runs; TH-160]
- The transcript task's right answer queues a video under Charles's name; a replay that really did so would put a video he never asked for into intake. Answer helpers state the file and content and write nothing. [TH-160 finding 5]
- Every task touches the routing files, which change often; without the two-task cap one routing edit would re-ask the whole set. [BB-2026-11-09-fixed-test-set, Decisions]

## Changelog
- **0.2.0** (2026-11-10): new section Replay, run by the chat, never by the scorer's helper (Build 75, BB-2026-11-09-fixed-test-set). Picks at most two fixed-set tasks whose touched files or model changed, or that have no separately graded run; drops stale `until:` points; two runs per setup (plain, real route through the Expert Desk mode B); one blind grader helper that may say can't tell; one `fixed-set-run` note and a Runs table row. Replays write nothing else.
- **0.1.0** (2026-11-10): first version (Build 74, BB-2026-11-09-step-in-scorer). Weekly helper started by Design Assist intake; blind re-score of three earlier chats; reads each chat to the end; one lesson per step-in on total-harness; receipt first line says how much it read; attempt receipts when no chats could be read.
