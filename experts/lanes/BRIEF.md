---
name: lanes
level: craft
under: c-stack
profiles: [harness]
call_when: "the work decides where a job runs — chat, scheduled task, PC task, GitHub Action, Vercel cron or API pipeline — or assumes what that place can reach, approve or remember"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/charter.md", "cbrain:concepts/stack-map.md (lanes:)", "https://code.claude.com/docs/en/routines", "https://code.claude.com/docs/en/desktop-scheduled-tasks"]
version: 0.2.0
status: active
---

# lanes

Where a job runs, and what that place can reach, approve or remember. GitHub Actions behaviour is github-integrations'; host and key setup is services'; a helper's context and tool inheritance is skill-authoring's.

## Our way

1. Picking the engine: deterministic work on a GitHub Action (or a Vercel function with no Claude), Claude as worker on a scheduled task, and Claude inside app code only on a capped API key; not Claude work on an Action or rote work on a Claude run, because that is the two-engine rule [charter, standing rules]
2. Unattended Claude work: a cloud scheduled task on the subscription; not headless Claude Code on the PC, because that was new, unproven infrastructure next to a cloud runtime already proven, and not a paid orchestrator on the API key, because AI usage stays on the subscription [WG-088; BB-2026-11-02-expert-desk, current state; charter]
3. Work that needs the PC: nothing is parked with "where: pc" and wakes are cloud-only. A PC-bound task reaches only the folders approved on that machine, only while the desktop app is open, and needs a person for apps or the screen; not a laptop-side always-allow task, because Charles chose to leave laptop wakes alone [TH-088; TH-J-024; stack-map lanes: scheduled-pc]
4. Work that needs fresh helpers (seats, checkers, fresh-session tests): run it in a chat that has the helper tool, and stop or hand off where the tool is missing. In a scheduled or overnight run the run itself is the one job; not a helper the lane lacks, because overnight sessions have had none and an overnight build should not need one [TH-J-001; TH-J-022; BB-2026-11-02-expert-desk, revision 7 and current state; BB-2026-11-03-expert-ce, draft]
5. Creating or firing a scheduled task: do it from a live chat where Charles approves the card. When a build can't, it leaves a setup card and a next move; not from an unattended or skip-approvals run, because create_trigger and fire_trigger are refused there [TH-J-003; TH-011; TH-015; WG-192, lessons; WG-190]
6. Setting up a scheduled task: its reach is fixed at creation, so name its connectors (remove the rest), its repos, its approval setting and its model when it is made; not a default task holding every connector, because a run can write through any connector it holds and nobody is there to widen reach mid-run [stack-map lanes: scheduled; CB-504, routine handoff; Anthropic scheduled-tasks docs, read 2026-11-03]
7. A scheduled task's prompt: one line that fetches an agent-library skill and follows it, with the rules kept in the skill; not rules written into the prompt, because the prompt is fixed at creation and drifts from the skill [stack-map lanes: scheduled; CB-504, routine handoff; WG-177]
8. Database writes in a run nobody watches: use inserts, or functions called through SELECT, and roll test rows back in a block that ends by raising an error; not UPDATE, DELETE or DROP through the Supabase connector, because those wait for an approval nobody gives [CB-532; CB-504, lessons; TH-J-018; CB-536]
9. Naming a part's lane: Claude on a key means api-pipeline, even inside an Action. A request-driven Vercel function with no Claude is vercel-cron. A runtime no lane fits (database triggers, the Windows relay, a helper inheriting its parent's lane) is left unplaced and named; not forced into the nearest lane, because the github-action lane says no AI [SM-090]
10. Seeing a protected preview or a screen from a cloud lane: don't fetch it. Builds check code and data, and Charles checks the screen from the brief's What to check list; not CI browser screenshots (the route CB-286 and CB-378 named), because CB-441 retired the browser gate [CB-286; CB-378; CB-441]
11. A step that depends on the surface (memory, past-chat search, a browser, the PC link): the step names its fallback and marks itself not available, with the reason, when the thing is missing; not assumed the same everywhere, because surfaces differ in both directions [MB-007; CB-142]
12. Knowing what a lane can reach, approve or keep: read stack-map lanes: (each row carries its verified date), and when a run shows otherwise, correct that block in the same build; not re-derived per chat or copied into briefs, because comprehension lives in that document [charter, non-negotiable; SM-090]

## Lens

1. Two lanes that look alike treated as one: a cloud scheduled task given a "computer asleep" weak spot, or a chat assumed to have the PC because another chat did; the PC link follows where the chat is open [charter, non-negotiable; SM-076; stack-map lanes: chat]
2. An approval-gated step in an unattended run read as a timeout or a flaky tool and retried; it is waiting for consent, and the fired prompt can't give it [TH-J-018; CB-532; Anthropic scheduled-tasks docs, "can't act as approval or consent"]
3. A dispatcher run told to fire another scheduled task is refused, and the item was already marked sent before delivery [TH-011; TH-015]
4. A PC-bound task fired on the assumption it gets the computer: it starts in the cloud with no device tools, or with no folders until someone approves on the machine [TH-018; TH-034; TH-043; TH-130]
5. The Windows relay on the PC assumed to drain on its schedule: it runs only while Charles is signed in, and its wake setting is unlikely to wake the machine [WG-058]
6. A connector that answers with nothing (Drive) taken to mean "nothing there" rather than "can't see" [TH-128; TH-130; TH-132]
7. A job assumed able to start, read or link to a chat: no scheduled job reads claude.ai chats, and a running chat can't see its own link [CB-490; ~ "one chat cannot start another" is cited to a dry run of 2026-11-02 in BB-2026-11-02-expert-desk; that dry run's own record was not opened]
8. A cloud run assumed to reach any host or repo: hosts outside the environment's allowlist are refused, repos not attached won't clone, and protected previews redirect to sign-in; connectors are the way through, and how a run commits is github-integrations' Our way 17 [CB-286; TH-010; TH-130; SM-091; Anthropic scheduled-tasks docs, environments]
9. Memory assumed missing outside claude.ai chats, or past-chat search assumed present outside them; it is the other way round [MB-007]
10. A UI dry run reported done by a session with no browser, with a type-check standing in for a click-through [CB-142; CB-148]
11. A fresh-session test run inside the already-informed session because the lane had no helper tool [TH-J-001, which declined to fake it; ~ TH-J-022 used a separate headless Claude process instead, not yet reviewed]
12. A scheduled task's prompt left asking for something its skill dropped, or pointing at a moved path, and the run follows whichever it reads [WG-177; WG-166]
13. A step's lane picked by default without a test: sent to the PC when the cloud workspace could run it, or kept in the cloud after its cloud run failed its check [TH-032, Charles: where each step runs is open; TH-045; TH-058]
14. A lane fact read from the map after the platform changed: ~ the scheduled-tasks page read 2026-11-03 says cloud runs start in auto mode with no mode chosen at creation, while stack-map lanes: scheduled (verified 2026-10-29) says approvals are set per task; check the task's own setting [Anthropic scheduled-tasks docs, permission prompts; stack-map lanes: scheduled]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms (scheduled task, lane, unattended, approval, PC, requires this computer, helper, create_trigger, fire_trigger, cloud environment). Where a result is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against it.
5. Write the output in the mode the desk named.
6. Read only, write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** lanes · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork. An A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson found in step 2 that changes an Our way line (the desk files it as a lens-note), or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** lanes · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner; propose a way the record already ruled out without naming the decision that ruled it out.

## Changelog

- 0.2.0 (2026-11-03): replaces chat-access 0.1.0. Renamed `lanes` (Charles confirmed) and widened from what a chat can reach to where any job runs (chat, scheduled task, PC task, GitHub Action, Vercel cron, API pipeline) and what that place can reach, approve or remember. Our way added from Charles's record, format 0.2.0. Lens re-sourced: chat-access lines 1 and 3 became Our way 4 and 3; line 2 went to services; lines 7 and 8 were left to skill-authoring; lines 4, 5, 9, 10 and 11 became Lens 6, 7, 8, 9 and 10; line 6 (a helper's fixed overhead) went to skill-authoring at the fit pass (EB-015). c-stack lens lines 2, 11, 12, 13, 14 and 15 moved down. reads: dropped skills/checker/SKILL.md; added the charter and Anthropic's two scheduled-task pages (read 2026-11-03). Team EB-007 on expert-bench, confirmed by Charles 2026-11-03.
