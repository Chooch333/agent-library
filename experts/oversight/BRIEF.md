---
name: oversight
level: craft
under: c-stack
profiles: [harness]
call_when: "the work adds, removes or re-routes a running part (where or how often it runs), or decides how one is checked, how its failure or a wait on Charles reaches him, or what each run leaves behind to show it ran"
altitude: [plan: risks-only, implementation: full]
reads: ["cbrain:concepts/stack-map.md (## Stack Flow; flow_nodes stack-inspector, stack-repairer, email-approval-gate; each dot's ops.check)", "agent-library:skills/stack-repairer/SKILL.md", "agent-library:references/thread-checkin.md"]
version: 0.1.3
status: active
---

# oversight

How a running part is watched and how Charles hears about it: its Stack Flow dot and check, the Stack Inspector and Stack Repairer loop, the evening recap, Next steps cards, and the run's own note. Where a part runs is lanes'; GitHub-specific failure modes are github-integrations'.

## Our way

1. Drawing a running part: the build that adds, removes, renames or re-routes it also edits its Stack Flow dot, lines and side-panel text, or the brief says `Stack Flow: no change` and why. Not a map suggestion filed for later, because filed suggestions were almost never applied and that queue was retired [design-assist rule 12; Charles 2026-10-07 standing authorization; skill-design-framework Q6]
2. Lines on the map: drawn by hand in the map's flow lines, not generated from skill wiring, because wiring would put back lines Charles removed. Wiring feeds a "not on the map yet" drift signal, and the Rules Inspector's weekly walk catches what a build missed [CB-367; stack-map "How this map stays current"]
3. Giving a part a check: every dot carries a hidden check of one of the map's check types, with its normal gap. Thresholds live in the stack map, not in the checker's code, so the Rules Inspector keeps them current along with the map [CB-492 item 5; stack-map Stack Flow section; Build 56]
4. What colour silence gets: silence alone turns a dot amber; red needs a real failure or a used-up allowance. Not red on a quiet spell, because a machine asleep overnight would raise a false alarm [CB-492 item 1]
5. The checker itself: the Stack Inspector is a timer in cbrain's Vercel project and uses no AI; not a GitHub Action, because it would go silent exactly when Actions runs out [CB-484; CB-492 item 4]
6. How Charles hears about a broken part: no email per problem. The Stack Repairer reads red and late dots on its schedule and fixes each one at the smallest size; its evening run sends one recap of the day. Not the checker's own red/fixed alert email, which Build 27 switched off and which stays off [Build 27, BB-2026-10-05-stack-repairer; stack-repairer "Do NOT"; CB-492 item 2 dropped]
7. Fixing a red dot: use the smallest fix that works: a re-run, a one-file fix, a short brief queued with standing approval, or a build right away when urgent. Re-runs are capped before the fix moves up a size. Hard gates (a key, money, an irreversible change) are logged needs-you, never asked as a blocking question [stack-repairer step 4; Build 27]
8. Running parts vs rules: running parts belong to the Stack Inspector and Stack Repairer, daily. Rules, skills and the map belong to the Rules Inspector and Rules Repairer, weekly, through the Punch List. A broken dot whose real fix is a rule or map change gets a brief, never a direct edit by the Stack Repairer [stack-repairer What, Do NOT; stack-map Stack Flow section]
9. Anything waiting on Charles: it goes under Needs you in the evening recap, worded as the exact ask, plus a Next steps card. Not a separate email, because Charles asked for daily only, no immediate email [stack-repairer 0.3.0, Charles 2026-10-23; email-approval-gate dot; Build 13.6]
10. How Charles clears a needs-you: he answers in any chat (for a held email: answer the questions and say "seal the draft"). Not by replying to the recap, because replies to the recap stay unread [CB-537; email-approval-gate dot]
11. A job that leaves something open: it checks in as a job, with a plain next step and who it waits on, and closes its own card when the thing clears. Jobs never reopen a card [thread-checkin.md 0.3.1; stack-repairer Progress tracking]
12. Each scheduled run's own trace: one Project State note per run. Its first line is a plain-English count, then the counts and the paths written. No email, neither a digest nor a failure notice. Not the digest emails, which Build 27 retired [post-reader steps 5–6; Build 27 Collector digest retired; BB-2026-11-03-expert-ce "one note per run; no email"]
13. A problem a run or chat finds in a running part outside its own job: one `reported` row in the stack fix log (stack_repairs) with a recheck anyone can run; the Stack Repairer treats it like a red dot and grades it by that recheck, and design questions stay on the Comms Table; not a Comms Table needs-design-check post, because running-part posts sat there with no runner until a build swept them [WG-103; WG-107; Build 67, BB-2026-11-03-stack-fix-log; AGENT.md; stack-repairer 0.4.0; TH-149; EB-130]
14. Telling quiet from dead: a part writes a marker every run, even when it did nothing, and its dot checks the newest marker. The Stack Repairer also watches the Stack Inspector's own row and treats a stale one as a red dot [stack-repairer `_run` marker and step 1; Build 27 forks]
15. Proving a new or changed check: run the checker in dry mode with a temporary test input that turns the dot red and then back. Do it right after a scheduled check so no real status row records the test [Build 13.6 session log CB-567; CB-502 dry mode]

## Lens

1. A running part shipped with no Stack Flow line; the Video Reader ran before any build drew its dot [c-stack 16; CB-537]
2. A fix expected to happen on its own with no named runner behind it [c-stack 20; C-071]
3. A check that reads a different record than the one the job writes, so the dot stays red while the job passes; the fix belongs in the check, not the job (reading a checker's reason text instead of the runs is ai-system-design's line) [CB-533; CB-539]
4. A writer's interval set right at the checker's late threshold, so ordinary timing jitter flips the dot late and back [CB-546]
5. A check frozen on a number an agent keeps changing: it goes red on correct behaviour and teaches everyone to ignore red [CB-333]
6. A dot that watches one piece of a part while another piece fails unseen; the transcript loader failed with no check on its workflow until a follow-up build added one [CB-502 "left undone"; CB-507 item 1]
7. A part shipped with check `none` and no named way to watch it; a part that leaves no trace when idle can't be told from a dead one [stack-map shared-posts and post-reader dots, Build 60; stack_status email-watcher row, read 2026-11-03; ~ whether a follow-up check is planned was not searched]
8. A job that becomes hand-only once its schedule is switched off, with no dot noticing; the Advisor's packet job ran only when someone dispatched it by hand, for days, and the Advisor itself found that [SM-088; SM-079]
9. The same needs-Charles note written run after run, with no card and a tag nothing reads; the runner repeated an identical miss instead of raising it once where Charles looks [TH-034; TH-011; CB-278 on the mangled tag]
10. A scheduled run that fires on time but does no work because a tool was down; firing is not proof, so the run's note has to say what it actually did [CB-213]
11. One allowance running out reported as many problems: a used-up allowance turns every dot that counts against it red. One needs-you on the allowance covers them all, and dots red only through it need no action of their own [CB-550; CB-492 item 2]
12. A red that clears on its own before the queued fix runs; the fix brief has to re-check the live state first [CB-539]
13. Repairer grades that never land, so the size-up never fires and a still-red dot gets the same small fix again [CB-532; ~ the insert-only rule that fixed it is lanes' line]
14. A part's status page failing read as the part itself failing, sending Charles to check a healthy machine [CB-565]
15. Side-panel facts left stale after a part changes where or how often it runs: cloud runs still listed a sleeping computer as their weak spot, and the map's cadence disagreed with the task's. The Advisor caught it, not a check [SM-076; SM-078]
16. ~ A dot removed from the map leaves its old status row behind, frozen at its last check [stack_status next-steps-sweep row, last checked 2026-10-23, read 2026-11-03, with no matching dot on the stack map; ~ not confirmed whether anything still reads that row]
17. ~ A URL check that passes whenever the page answers while the page itself reports trouble: the video relay dot read green through a run of dark feeds and stranded videos; point the check at the page's own health field [stack_repairs 35d24e44; CB-591; EB-131]
18. ~ A known cause that comes back every few days, fixed each time by the same re-run and graded green, so the per-day re-run cap and the still-red size-up never fire; when the lasting fix is Charles's to revisit (a trigger he turned off), the ladder never brings it to him [stack_repairs b51452ff, b1a9bb41; CB-562; stack-repairer steps 2 and 4a; EB-132]
19. A pause Charles calls in a build chat recorded only in the plan's report, with no Next steps card and no recap line: it sat for days and froze the builds queued behind it until he was asked [Build 35.1 plan report; TH-154; EB-172]
20. An item carried as waiting on Charles with nothing waiting for it: a key no use case names, a question a decision had already answered, test jobs left at a review stop [Block 5 plan; TH-031; TH-055; EB-173]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms (stack-incident, stack-repairer, live-status, stack-flow, needs-you, recap, check type). Where a record is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against the work.
5. Write the output in the mode the desk named.
6. Read only and write nothing. You are alone and see no other seat.

## Output

**Full**
**Seat:** oversight · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork. An A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson found in step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** oversight · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner (where a job runs is lanes'; Actions, branches and repo queues are github-integrations'); propose a way the record already ruled out without naming the decision that ruled it out.

## Changelog

- 0.1.3 (2026-11-09): folded EB-172, EB-173 by hand in a Total Harness chat at Charles's word ("Add them yourself now"): Lens 19 and 20 added.
- 0.1.2 (2026-11-09): applied EB-130 under the fold rule Charles set 2026-11-09 (a line overtaken by his later decision, or by a fact a build or test proved, is updated and cites it; only a new opinion or a clash between two of his decisions reaches him). Self-learning loop design chat; the matching Comms Table posts are cleared.
- 0.1.1 (2026-11-08): folded EB-131, EB-132 (Expert CE)
- 0.1.0 (2026-11-03): first brief. Researched by roster-builder (desk T2) from the stack wiring team note on expert-bench, row 7. Our way comes from Charles's record (CB-367, CB-484, CB-492, Builds 13.6, 27 and 56, WG-103, thread-checkin, design-assist rule 12). Lens lines 1 and 2 moved down from c-stack (its lines 16 and 20). Fit pass (EB-015): call_when narrowed to adding, removing or re-routing a part; Our way 5 leaves timer placement to services; Lens 2 drops the clause skill-authoring owns.
