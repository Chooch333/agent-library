---
name: stack-chief-of-staff
version: 0.1.3
status: draft
triggers: ["what's going on with my stack", "stack status", "Chief of Staff"]
dependencies: []
owner: Charles
updated: 2026-11-28
requires: [references/charter.md, references/project-state.md, references/gotchas.md, references/thread-checkin.md]
description: "On demand, in any chat (built for Duet): reads every automated part of Charles's stack and tells him in about a minute, in plain words, what needs him, what changed since he last heard, what is off and who is on it, and what it could not see. Read-only; never scheduled."
wiring:
  runs: with-you
  starts: "\"what's going on with my stack\", \"stack status\" or \"Chief of Staff\" in any chat (Duet included); on demand, never scheduled"
  runs_in: claude-chat
  reads: [stack-status, stack-repairs, project-state-heartbeat, night-builds, build-shelf, advisor-runs, punch-list, expert-bench, readers, next-steps]
  writes: [project-state-note, stack-repairs]
  stack: [stack-chief-of-staff]
  origin: yours
  label: Stack Chief of Staff
---

# Stack Chief of Staff

**Rules first** (read these even if nothing else survives):
1. Read-only. Never fix, re-run, queue, email, close a card or change anything. The only writes: one receipt note (step 5) and, for something broken with nobody on it, one `reported` row in the stack fix log (step 4).
2. Never scheduled. It runs when someone asks. Never create a scheduled task for it.
3. Tool check first (step 0). A source it cannot reach is named in one plain sentence ("I couldn't see the night builds today"). Reading nothing is never "all fine".
4. Needs you is read from the Next steps list in the cards' own words, never re-judged, re-worded or re-ranked by importance.
5. What Charles hears: plain words, no ids, codes, tool, table or file names, no build numbers (charter, "Communicate cleanly"). About a minute: under 200 words.
6. Summaries first. Read details only when a summary says something is off.

## What

The Stack Chief of Staff tells Charles where his stack stands. He asks (usually through Duet, which reads the answer back to him); it surveys every automated part, the lights, the fix log, last night's builds, the build shelf, the Stack Advisor, the Punch List, the experts' weekly study, the readers and the Next steps list, and answers in about a minute, in this order: a one-line headline, what needs him, what happened since he last heard, what is off and who is on it, and what it could not see. It writes one receipt note so the next ask knows what he has already heard. It judges nothing about how to fix anything; the Stack Repairer, the Rules Inspector and the night builds do the work, and this skill only reports it. Per Build 90 (BB-2026-11-19-stack-chief-of-staff); Charles, 2026-11-17: "survey the automated items and provide a brief clear (non lingo/non tech) description of where things stand."

Cost: one ask is one chat turn on Charles's Claude plan, about ten reads (the Next steps list alone is large, read through a filter), one Project State note (one OpenAI meaning fingerprint, a fraction of a cent), small Supabase reads and a few Vercel calls (Project State and its public heartbeat). No other spend; nothing runs between asks.

## When

**Fire when:**
- A message asks where the stack stands: "what's going on with my stack", "stack status", "Chief of Staff", or the same ask in other words ("how's my stack", "anything broken?"), in any chat, mid-chat included.
- Duet asks on Charles's behalf.

**Do NOT fire when:**
- A scheduled task or night run wants a status line: those have their own (the Stack Repairer's evening recap, the night run's email). This skill never runs unattended.
- Something is broken and the ask is to fix it: that is the Stack Repairer (`Stack Repairer: run`) or a build.
- The ask is about one part's design or how it should work: that is a judgment ask; seat the matching expert (AGENT.md, "Every chat, every message — experts").
- The ask is about a job's tasks (FAW), the family arcade or a tech review card: those are their own skills, even though their cards show on the Next steps list.

## How

Read `references/charter.md` before step 0 when GitHub is reachable; if it is not, the Rules first block carries what this skill needs and step 0 continues.

**0. Tool check.**
- *Action:* list which sources this session can reach, in this order, with one cheap call each, and keep the list:
  1. **No connector:** Project State's public heartbeat, `https://project-state-mcp.vercel.app/api/heartbeat`, with a plain web fetch (times and yes/no only: night runner's last result, Rules Inspector and Repairer runs, Expert CE's newest receipt, step-in scorer). Never call the Stack Inspector's own link (`/api/cron/stack-status` on cbrain-sync): its plain GET is not a read, it runs a full checker pass and rewrites the status table, and returns counts only.
  2. **Supabase** `execute_sql` on cbrain `lpeswznkxzeeyiqaewma`: one `select count(*) from stack_status`.
  3. **Project State MCP:** `overnight_line` (it is also the first read of step 1).
- *Evidence:* a reached / not reached line per source.
- *Recovery:* a call errors → retry once; still failing → not reached. Never use a Project State SQL fallback for reads here; name the gap instead. Nothing reached at all → say only: "I couldn't see any of your stack's records just now, so I can't say how it stands." Never "all fine".

**1. Read, summaries first.** Each bullet names its source; skip a bullet whose source was not reached and note it for step 3.
- *Lights* (Supabase): `select id, kind, label, state, own_state, reason, via_allowance, last_seen_at, checked_at from stack_status where (kind in ('dot','allowance') and state in ('failing','late')) or id = '_checker'`. `_checker` `checked_at` older than the Stack Inspector dot's `check.every` on the stack map (22m today) → the Stack Inspector itself is down; say so as one thing off. Then the other lights are out of date: say 'the status lights haven't updated since <time>', report lights only as of that time, and write no step 4 row from them. `unknown` rows are not problems (by-hand jobs, no check).
- *Fix log* (Supabase): the newest run marker, `select run_at, finding, detail->>'recap' recap from stack_repairs where dot_id = '_run' order by run_at desc limit 1`; the open rows, `select r.id, r.run_at, r.dot_id, r.action, r.finding, r.plan_id, r.detail from stack_repairs r where r.action in ('reported','needs-you','watching','briefed') and r.dot_id <> '_run' and not exists (select 1 from stack_repairs g where g.action = 'graded' and g.detail->>'grades' = r.id::text) and (r.dot_id = any(<those ids>) or r.action in ('reported','needs-you')) order by r.run_at desc`, where `<those ids>` are the dots that are red or late right now from the Lights read; and the rows since the marker (step 2) with `action in ('rerun','cleared','fixed','built','briefed','graded')`. Watching and briefed rows on dots that aren't red stay out (quiet-source noise).
- *Night builds and the shelf* (Project State): `overnight_line` → `last_night` (each build's plain title and result) and `line` (queued briefs: plain title, ready or what it waits on).
- *Stack Advisor* (Supabase): `select run_date, preamble, questions from advisor_runs order by run_date desc limit 1`.
- *Punch List* (Project State): `list_punch_items` with status `open`, `needs-brief`, `failed`, `regressed`; count them and read `plain_summary` only. An item whose summary starts `[TEST]` is a planted test; skip it.
- *Experts' weekly study:* the heartbeat's Expert CE time is the summary. Only if it is more than 8 days old, or the lights show Expert CE off, read `find_by_tags` on `expert-bench` tags `ce-fold`, limit 1, and only its first paragraph.
- *Readers* (Project State): the newest note on `world-graph` tagged `video-reader`, `world-graph-reader` and `post-reader` each (`find_by_tags`, limit 1 each, keep only rows whose own tags match exactly); read each note's first line only.
- *Next steps* (Project State): `list_open_threads` with `waiting_on: "you"`, so only the cards waiting on Charles come back. Fallback: if that input is refused, or the result holds any card whose `waiting_on` is not `you` (a chat holding the old tool schema drops the input), call it with no input and keep the cards with `waiting_on` `you`. Also read open `needs-you` rows in the fix log whose card is missing (no open card with thread_key `job:stack-repairer-<dot id>`), and say each in its `finding` wording, counted with the job cards. Even filtered, the result is large (dozens of cards); save it and filter it with a short script rather than reading it whole.
- *Evidence:* each read's result, or "not reached".

**2. Since he last heard.**
- *Action:* the marker is the newest note on Project State project `cbrain` tagged `stack-cos-receipt` and NOT also tagged `build-test` (`find_by_tags`, own tags matched exactly; skip any note also tagged `build-test`); the window starts at that note's created_at. Its `cos:` line lists what was named last time. No receipt yet → the window is the last 24 hours. From the window: fix log rows since the marker (fixed, re-run, briefed, graded green), `overnight_line` `last_night` builds that ended inside it, a new Stack Advisor run, new reader notes.
- *Evidence:* the window start and the list of happenings.

**3. Say it.** In this order, under 200 words, plain words only:
1. **Headline**, one line: how it stands overall ("Mostly fine: two small things are being fixed tonight, and nine asks wait on you.").
2. **Needs you.** From the Next steps cards waiting on Charles: the cards whose `kind` is `job` are the asks from the automated parts. Name at most three, newest first, each in its card's own words (its `next_step`, first sentence, unchanged). Every other card waiting on him (job cards past three, and the cards from chats: games, reviews, design chats) is counted, not read: "plus 30 more on your Next steps list, mostly from your chats." A card is counted, not named, when any receipt (not tagged `build-test`) written after the card's own last check-in already names it (read receipts back to that time).
3. **Since you last heard:** at most four lines: builds that landed or failed, fixes that held, what the Advisor and readers did ("The video reader read three videos overnight.").
4. **What's off and who's on it.** Each failing or late light, and each open `reported` row, in one line with who is on it:
   - a `briefed` or `watching` row whose plan is `queued` or `running` → "a fix is queued for tonight" (or "being built now");
   - a card waiting on Charles already asks for it → "it's on your list";
   - a `watching` row whose recheck waits for something to happen first (an email to arrive) → "waits on its own";
   - no row yet and the light changed since the Stack Repairer's last run → "the repairer looks at it at its next run" (its next working run);
   - a `watching` row that points at a draft or blocked plan, a recheck that no running part can run, or nothing at all after the repairer has had a run → **"nobody"**; write the `reported` row in step 4.
   A dot whose `via_allowance` is set is not its own line: say it under that allowance's line ('one account ran out, so N parts are paused'), and it is never 'nobody'.
   Project State not reached, so a plan's status can't be read → say what the fix log row says ("the Stack Repairer has queued a fix").
   A quiet source (a feed or channel with nothing new) is not off; leave it out (WG-213). The Punch List is said only when an item there has `failed` or `regressed` (the Rules Repairer works the rest on its weekly run). An issue named in the marker receipt (step 2) is counted, not described again: "Two known issues are still open."
5. **Couldn't see**, one sentence per source not reached in step 0 or 1, in plain words: "I couldn't see the night builds, the Next steps list or the experts today."
- No ids, codes, plan or build numbers, tool, table, file or repo names. Name parts by the names Charles sees on the Stack screen (the Video Reader, the Stack Repairer, the night builds).
- *Evidence:* the read-out; count its words (under 200) and check it for ids before sending.

**4. Report what nobody is on.** For each "nobody" line in step 3 (Supabase reached):
- First check the open rows from step 1: any open row on the same `dot_id` (reported, watching, briefed or needs-you) whose plan is not a draft or blocked, or any open `reported` row on that dot whose `detail.found_by` is `stack-chief-of-staff` → write nothing (No repeats, stack-repairer).
- Otherwise insert one row through `execute_sql` on `lpeswznkxzeeyiqaewma` in the stack-repairer Reported problems shape: `dot_id` (the dot, or `_unmapped`), `action` `reported`, `finding` one plain line, `detail` `{"evidence": "...", "found_by": "stack-chief-of-staff", "recheck": "<a check anyone can run that passes once it is fixed>"}`; every row this skill writes sets `detail.found_by` to `stack-chief-of-staff`. For a draft or blocked plan, `detail.evidence` names it and says "that plan is a draft, nothing will build it"; never set `detail.plan_id`. Confirm with a separate SELECT. Never UPDATE or DELETE a row. The Stack Repairer picks it up at its next run.
- Supabase not reached → no row; the read-out already says what could not be seen.

**5. Receipt.** Project State reached → one `add_note` on project `cbrain`, topic "Stack Chief of Staff receipt", source "Stack Chief of Staff, <chat or Duet>, <date>", tags `stack-cos-receipt`, `stack-chief-of-staff`. Content: the read-out as said, then one last line `cos: {"window_start": "<ISO>", "named": [<dot ids, card thread_keys and row ids named this time>], "sources_missed": [<sources not reached>], "reported_rows": [<ids written in step 4>]}`. A run Charles will not hear (a build or test session, or any ask not from him or Duet) tags its receipt `build-test` and puts `"build_test": true` in its `cos:` line. Check the reply's `tag_substitutions`; a rewritten tag is fixed with `add_tags` so the next ask can find the marker. Project State not reached → no receipt; the next ask covers the longer window.
- *Evidence:* the note's display id (kept out of the read-out).

**6. Answer.** Send the read-out from step 3 as the reply. Nothing else: no list of sources read, no ids, no offer to fix things (the Stack Repairer already does). If Charles then asks to fix something, that is a new ask (When, Do NOT).

## Progress tracking
None. This skill finishes in one run and leaves nothing open: anything broken with nobody on it becomes a `reported` row for the Stack Repairer (Closing out, bin 3), and Needs you only reads the cards that already exist.

## Examples

### Example 1: the full read on live data (Build 90 test, 2026-11-21 06:40 UTC, every source reached)
Lights: Chats late (the step-in scorer quiet ten days) and RSS feeds late (one feed's articles refused); both have a queued fix on the shelf. Fix log: three briefs queued and the evening recap sent in the last day. Night builds: the experts' weekly catch-up build landed. Readers: three videos, eleven articles. Advisor: two ideas, two questions. 38 cards wait on Charles, 9 of them from automated parts. No receipt yet, so the window is the last 24 hours. Punch List: nothing failed or regressed, so not said. Nobody-on-it lines: none, so no fix-log row written. Read-out (199 words):

> Mostly fine: two small things get fixed tonight, and nine asks from automated parts wait on you.
>
> Needs you: "Turn off the scheduled task "cbrain Tier-2 second opinion" — nothing uses it any more, and it still holds a Project State key in its address." "Open the scheduled task "Stack Repairer" and set it to run at 7:29 am, 12:29 pm and 5:29 pm Indianapolis time." "Recommended: do the five setup steps on this card in order (about 15 minutes) so Claude can read Charles's own inbox as a separate "Personal Gmail" connector; the existing Gmail connector is not touched." Plus 35 more on your Next steps list, most from your chats.
>
> Since yesterday: the experts' weekly catch-up build landed overnight. The Stack Repairer queued three fixes and sent its evening recap. The video reader read three videos; the article reader filed eleven. The Stack Advisor has two ideas and two questions for you.
>
> What's off: the weekly check of when you stepped in hasn't filed since Nov 10, and one news feed's articles are refused. Fixes for both are queued for tonight. One known item waits on its own: checking the first email filed under the new labels.

### Example 2: Project State unreachable (Build 90 test 2, same moment)
Project State's tools treated as unreachable. The public heartbeat still answers (the night runner built; the experts' newest receipt six days old); lights, fix log and Advisor still read from Supabase. No Needs you list, no receipt written; a queued fix is said as the fix log says it, since the shelf can't be checked. Read-out (119 words):

> Mostly fine, but I couldn't see your Next steps list, so I can't tell you what's waiting on you.
>
> Since yesterday: last night's build finished. The Stack Repairer queued three fixes and sent its evening recap. The experts last studied six days ago, on schedule. The Stack Advisor has two ideas and two questions for you.
>
> What's off: the weekly check of when you stepped in hasn't filed since Nov 10, and one news feed's articles are refused. The Stack Repairer has queued a fix for each. One known item waits on its own: checking the first email filed under the new labels.
>
> I couldn't see your Next steps list, the build shelf, the Punch List or the readers' notes today.

## Pitfalls
- The Stack Inspector's plain link looks like a public summary, but a plain call runs the whole checker and rewrites its status table, and it answers with counts only; read the status table, or the Project State heartbeat when no connector is reached. [Build 90 read of cbrain services/api/cron/stack-status.ts; CB-583]
- From a Claude Code cloud session, a shell fetch of the public heartbeat was refused by the network proxy while the web-fetch tool read it; try the web-fetch tool before calling the source not reached. [Build 90 test, 2026-11-21]
- The Next steps list came back at about 85,000 characters (43 cards, 38 waiting on Charles). Ask for only his cards with `waiting_on: "you"`; on 2026-11-28 that still returned about 87,000 characters (42 cards, against 106,000 for all 51), so save it and read it through a filter, never whole into the reply. A chat holding the old tool schema may drop the input and return every card; check each card's `waiting_on` and filter if any is not `you`. [Build 90 test, 2026-11-21; BB-2026-11-27-adv-106-waiting-on-filter proof, 2026-11-28]
- One tag query on the experts' receipts returned fifteen long notes; the heartbeat's Expert CE time is the summary, and the fold note is read only when that time is stale. [Build 90 test, 2026-11-21]
- Project State has rewritten a new tag on write (`ce-dispatch` became `ce-dispatch-failed`), so a marker found only by its tag can vanish; check `tag_substitutions` after the receipt write and fix it with `add_tags`. [EB-085, EB-198]
- Quiet sources had been logged as watching rows three times a day for a week; they are not problems and stay out of the read-out. [stack_repairs watching rows on rss-feeds and youtube, 2026-11-15 to 2026-11-19; WG-213]
- Duet sees only skills saved to Charles's account; the AGENT.md row reaches Project chats only. Until that save is done, a Duet ask does not load this skill. [Build 90 seat review]
- A Duet-made scheduled task carried no connectors yet read mail; what a session can reach is only known by trying, which is why step 0 calls each source rather than reading a connector list. [BB-2026-11-19-stack-chief-of-staff, current state; EB-101]

## Changelog
- **0.1.3** (2026-11-28) — Step 1 Next steps bullet calls `list_open_threads` with `waiting_on: "you"` (the tool's new optional input), keeping today's save-and-filter step as the fallback when the input is refused or ignored by a chat holding the old schema; matching pitfall updated with the measured size. Stack Advisor done-for-you (BB-2026-11-27-adv-106-waiting-on-filter).
- **0.1.2** (2026-11-21) — Night seat round two (c-stack and oversight): fix-log open rows keep every reported and needs-you row, watching and briefed only on red dots; build-test receipts never count a card as named; known issues counted against the marker receipt; stale checker is the map's `check.every` (22m), no extra grace; cost line names the Vercel calls.
- **0.1.1** (2026-11-21) — Night seat revision (c-stack and oversight, report CB-692): build-test receipts skipped as the marker; fix-log reads filtered to the red or late dots, no-repeat test by dot; lights read the allowance columns and the stale checker follows the map; Needs you counts by receipt and reads orphan needs-you rows; cost line; Next steps list name; charter fallback and Duet pitfall; repairer timing; personal address removed from Example 1.
- **0.1.0** (2026-11-21) — First version, written by Build 90 (BB-2026-11-19-stack-chief-of-staff) through Team Builder skill mode. `status: draft` until its first live ask from Duet. Judgment calls at build: the no-connector read is Project State's public heartbeat, not the Stack Inspector's link (its plain GET runs the checker); Needs you names at most three job cards newest first, in their own words, and counts the rest; the receipt's `cos:` line carries what was named, so known issues are said once and then counted; no receipt yet means a 24-hour window.
