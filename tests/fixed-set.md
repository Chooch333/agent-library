# Fixed test set (draft)

The questions Claude must keep getting right. Each has an answer key built from Charles's own records, never from an expert's answer. Replayed after a change to anything a task touches (see `skills/step-in-scorer`, Replay). One task grows from every step-in cluster that leads to a fix.

**Score = step-ins:** the number of times Charles would have had to step in to get a correct answer. One per key point missed or contradicted, plus one each for asking him to fetch or test what Claude could, or giving an option list where the record settles one path. Lower is better; 0 is the target.

Seeded 2026-11-09 in the self-learning loop design chat (replaces Build 61.1). Plan: see Build 75.

## Tasks

### T1. New YouTube channels
**Ask:** "I want Claude to keep up with three new YouTube channels about robotics and pull the useful facts out of each new video every week. Where should getting the transcripts happen, where should the reading happen, and does it need its own scheduled task?"
**Touches:** experts/intake, experts/lanes, skills/video-reader, skills/post-reader
**Key:**
1. Transcripts are fetched by the PC relay (yt-relay), never from the cloud or an Action, because YouTube blocks cloud addresses [WG-063; WG-073; intake Our way 9]
2. Reading is the existing Video Reader on the Claude plan, not the API [WG-088; WG-092; intake Our way 1]
3. No new scheduled task: a channel is one line in yt-relay channels.json, no build [CB-349; intake Our way 6; EB-016]
4. Says that today a new transcript reaches the Reader's list only by a hand-started step until Build 72 lands [CB-562; WG-233; WG-236]

### T2. A nightly timer for a cbrain-ui page
**Ask:** "I need a timer that calls an endpoint every night at 2am for a new page I'm adding to cbrain-ui. Where should that timer live?"
**Touches:** experts/services, experts/lanes, references/charter.md
**Key:**
1. Not in cbrain-ui's Vercel project: Vercel crons run only against a production deployment and cbrain-ui work lands on review [CB-492 item 4; CB-551; services Our way 15]
2. In cbrain's Vercel project (services/vercel.json) or the production project that owns the data [CB-581; services Our way 15]
3. Not a GitHub Actions schedule: Actions timers are off since 2026-10-12 [SM-079; CB-562]
4. Locks the endpoint with a secret the build makes, asking Charles for no key [CB-580]

### T3. Hearing about a new job's problems
**Ask:** "I'm adding a new scheduled job to my stack. When it hits a problem, how should I hear about it?"
**Touches:** experts/oversight, skills/stack-repairer, AGENT.md
**Key:**
1. No email from the job; per-problem alerts are off [Charles 2026-10-05; Build 27]
2. The job gets a dot with a real check on the stack map; the Stack Inspector colours it, the Stack Repairer fixes it, and anything only Charles can clear rides the 5 pm recap under Needs you plus a Next steps card [stack-repairer; Charles 2026-10-23]
3. The job leaves a run marker every run, so silence shows as late [oversight Our way 14; CB-546]
4. A problem it finds outside its own job is one `reported` row in the stack fix log with a recheck, not a Comms Table post [Build 67; AGENT.md]

### T4. A YouTube link in chat (from step-ins TH-157, TH-158)
**Ask:** "What does this talk say? https://youtu.be/<a video not yet in intake>"
**Touches:** the youtube-transcript account skill, experts/intake
**Key:**
1. Checks world-graph data/transcripts/<id>.md, then cbrain intake_items, before saying anything about the transcript [TH-157]
2. If absent, queues it: commits yt-relay queue/<id>.json (url, source charles, status pending, requested_at), never editing an existing one [yt-relay api/receive.js; WG-234]
3. Tells Charles it is queued and the home PC fetches it; never "there is no transcript" [TH-158; Charles 2026-11-09]
4. Does not ask Charles to paste the transcript

## Runs

| Date | Setup | T1 | T2 | T3 | T4 | Total | Avg helper tokens | Graded by |
|---|---|---|---|---|---|---|---|---|
| 2026-11-09 | plain chat (AGENT.md + charter only), 2 runs | 2, 2 | 3, 3 | 2, 2 | not run | 14 | ~85k | the design chat, against the keys above |
| 2026-11-09 | chat that reads the stack map and searches decisions, 2 runs | 0, 0 | 0, 2 | 0, 1 | not run | 3 | ~117k | the design chat |
| 2026-11-09 | seated stack expert (intake / services / oversight), 2 runs | 0, 0 | 0, 0 | 0, 0 | not run | 0 | ~134k | the design chat |

What the misses were: plain chats sent transcript fetching to GitHub Actions (T1) and put the timer on a GitHub Actions schedule (T2, both runs), following the charter's two-engine line; one records chat put the timer in cbrain-ui's own Vercel project (T2); one records chat offered "the repair log or the Comms Table" (T3). Seated experts matched every key point in both runs. From here on a separate grader helper scores replays (Build 75).
