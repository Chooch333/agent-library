---
name: stack-repairer
version: 0.1.0
status: draft
triggers:
  - "Stack Repairer: run"
  - "Claude Code routine \"Stack Repairer\" (7:00, 12:00 and 17:00 America/Indiana/Indianapolis)"
dependencies: [orchestrate-build]
owner: Charles
updated: 2026-10-06
wiring:
  runs: on-its-own
  starts: "\"Stack Repairer: run\" / Claude Code routine 'Stack Repairer', 7:00 · 12:00 · 17:00 Indianapolis"
  runs_in: claude-code
  reads: [stack-status, stack-repairs, github-actions, vercel, project-state]
  writes: [stack-repairs, repos, plans, lessons, email]
  stack: []
  origin: yours
  label: Stack Repairer
---

# Stack Repairer

## What

The Stack Repairer fixes things that break while the stack is running, so Charles never gets a per-problem email and never has to kick off a fix. Three times a day it reads the red and late dots the Stack Inspector (the 15-minute checker, `services/api/cron/stack-status.ts` in cbrain, which writes `stack_status`) has found, works out why each one broke, and fixes it at the smallest size that works: a re-run, a one-file fix, a short brief queued for tonight, or a brief built right away when it's urgent. It logs every action in `stack_repairs`, and the evening run sends Charles one short recap of the whole day. Per BB-2026-10-05-stack-repairer (Build 27).

**Two domains, one pair each.** The Rules Inspector / Rules Repairer (`roles/inspector`, `roles/repairer`) look after rules, skills and the stack map, weekly, through the Punch List. The Stack Inspector / Stack Repairer look after things running, daily. The Stack Inspector finds problems and grades fixes (by turning a dot green again); the Stack Repairer only diagnoses and fixes.

## When

**Fire when:**
- Invoked by name ("Stack Repairer: run").
- The Claude Code routine "Stack Repairer" fires (7:00, 12:00, 17:00 America/Indiana/Indianapolis). If the routine is set up as hourly instead, skip any run outside 06:30–18:30 Indianapolis without writing anything.

**Do NOT:**
- Edit rules, skills or the stack map (`concepts/stack-map.md`, any `SKILL.md`, PROTOCOL.md, AGENT.md). That is the Rules Inspector / Rules Repairer's domain. A broken dot whose real fix is a rules or map change gets a `briefed` row and a short brief, never a direct edit.
- Review its own briefs (`review_plan`) or dispose its own disclosures (`dispose_judgment_call`).
- Email at any time other than the one daily recap (step 7).
- Turn the checker's per-problem alert emails back on (`ALERT_EMAILS_ON` in `services/api/cron/stack-status.ts` stays `false`).

## Tools

- Supabase `execute_sql` on cbrain project `lpeswznkxzeeyiqaewma`: `stack_status` (read), `stack_repairs` (read/write).
- Custom GitHub MCP: `list_workflow_runs`, `get_workflow_run`, `get_job_logs`, `run_workflow` (always pass an explicit `ref`), `get_file_contents`, `replace_in_file`, `create_or_update_file`, `list_commits`.
- Vercel MCP (`teamId team_8nMi0Bd6orQHGeTrMZYWCamm`): `list_deployments`, `get_runtime_logs`, `get_deployment`.
- Project State MCP: `write_plan`, `update_plan_status`, `add_lesson`, `search_state`, `overnight_line`, `post_judgment_call`, `list_plans`.
- Gmail: `send_message` (recap only).

## The `stack_repairs` log

One row per action. Columns: `id`, `run_at` (default now()), `dot_id`, `finding`, `action`, `detail` jsonb, `plan_id`, `commit_sha`, `outcome`.

- `action` is one of `rerun`, `cleared`, `fixed`, `briefed`, `built`, `needs-you`, `watching`, `graded`.
- **Append-only — never UPDATE or DELETE a `stack_repairs` row.** Scheduled runs can't confirm edits to existing rows (first live run, 2026-10-07: both UPDATEs hung 3 minutes and saved nothing), so the log only ever grows. A grade is its own row: `action = 'graded'`, `dot_id` = the graded row's `dot_id`, `outcome` = `green` or `still-red`, `finding` = one line ("Re-run of world-graph worked — back to green"), `detail` = `{"grades": "<id of the graded row>", "evidence": "..."}`. An action row's own `outcome` column stays null; its grade is the newest `graded` row whose `detail->>'grades'` is its id.
- Every run also writes exactly one **run marker** row: `dot_id = '_run'`, `action = 'watching'`, `finding` = a one-line count ("3 red, 1 late — 2 acted on, 2 watched"), `detail` = `{"window": "07:00|12:00|17:00", "red": [...ids], "late": [...ids], "recap_sent": true|false}`, `outcome` left null forever. The Stack Repairer's own dot on the stack map checks the newest `run_at`, so a quiet day still shows the Repairer alive. Never grade a `_run` row.
- `detail` always carries `{ "evidence": "...", "size": "rerun|urgent-fix|brief|hard-gate|watch", "attempt": n }` plus whatever ids prove it (`run_id`, `deployment_id`, `workflow`, `ref`).

## How

**1. Read.**
- *Precondition:* none — first step every run.
- *Action:* `select id, kind, label, state, own_state, reason, via_allowance, last_seen_at, checked_at, detail from stack_status where state in ('failing','late') and kind in ('dot','allowance')`. Skip `unknown` rows entirely (a `none` check or "couldn't check just now" is not a problem to fix). Also read the `_checker` meta row: if its `checked_at` is more than 45 minutes old, the Stack Inspector itself is down — treat `_checker` as a red dot named "Stack Inspector" (the evidence is cbrain-sync's Vercel cron `/api/cron/stack-status`). Then read today's log: `select * from stack_repairs where run_at >= date_trunc('day', now() at time zone 'America/Indiana/Indianapolis') at time zone 'America/Indiana/Indianapolis' order by run_at`.
- *Success evidence:* a list of red/late ids (possibly empty) and today's prior rows.
- *Recovery:* the query errors → retry once; if it still fails, write nothing else, and (only on the 17:00 run) put "Couldn't read the stack's status today" under Needs you in the recap.

**2. Grade earlier work.**
- *Precondition:* step 1 done.
- *Action:* find every ungraded action row: `action not in ('graded','watching')`, `dot_id <> '_run'`, and no `graded` row exists with `detail->>'grades' = id` (any day, oldest first). Compare each against the current `stack_status` row for that `dot_id`: state `ok` → insert a `graded` row with `outcome = 'green'`; state `failing`/`late` → insert a `graded` row with `outcome = 'still-red'`, but only if the dot's newest evidence is newer than the action's `run_at` (a re-run that hasn't finished yet is not still-red — write nothing for it yet). `briefed` rows stay ungraded until their plan has `succeeded` and the dot has been checked since. Never UPDATE the action row itself (see "The `stack_repairs` log").
- *Success evidence:* each newly graded action has a `graded` row pointing at it; a separate SELECT shows them.
- *Recovery:* a dot that no longer exists on the map → `graded` row with `outcome = 'green'` and `detail.graded_note = 'dot removed from map'`.
- **Size up on still-red.** A dot whose newest `graded` row today is `still-red` moves up one size this run: rerun → urgent fix (or brief if not urgent) → brief built now → `needs-you`. At most 2 re-runs per dot per day, ever.

**3. Diagnose.**
- *Precondition:* a red/late dot from step 1 that has no action already in flight (a row from this run window with no `graded` row yet whose evidence hasn't moved).
- *Action:* read the evidence before acting — never act on the reason text alone.
  - **First, outage modes** (PROTOCOL.md, GitHub Actions rule). Check the `github-actions` allowance row and the run itself: a run that ended in 2–3 seconds with zero steps is a billing lock; HTTP 422 on dispatch is a disabled workflow; a push that never produced a run is a missed trigger. None of these is a code bug. A billing lock is a hard gate (money) → `needs-you`. A disabled workflow → `needs-you` ("re-enable <workflow> in <repo> Settings → Actions") unless a build log shows it was disabled on purpose and should be re-enabled (then re-enable is still Charles's click — log `needs-you`). A missed trigger → re-dispatch (step 4a).
  - **Workflow dots** (`detail.repo` + `detail.workflow`, or `detail.checks[]` for a list): `list_workflow_runs` (owner Chooch333, that repo, `workflow_file`, `per_page` 5), `get_workflow_run` on the newest failed run, `get_job_logs` with `search: "##[error]|Error|FAILED|Traceback"` on the failing job.
  - **Vercel dots** (a heartbeat URL on `*.vercel.app`, or a dot whose part runs on Vercel): `list_deployments` for that project, then `get_runtime_logs` for the window around the failure.
  - **Heartbeat dots:** fetch the `detail.url` (or read `detail.repo`/`detail.path`) and read the field named in `detail.fail_if`.
  - **Output dots** (`late`): find what writes that table/folder (the dot's `made_of` in `get_entity('stack-map')`) and check whether its job ran.
  - **Allowance dots** (`anthropic-api`, `github-actions`, ...): almost always money → `needs-you`.
- *Success evidence:* one plain sentence of cause, grounded in a log line, run id or response.
- *Recovery:* cause unclear after reading the logs → `watching` row with what was read; it's re-examined next run. A second `watching` on the same dot the same day with no new evidence → treat as not-urgent and write a short brief (step 4c) so a build chat can dig in.

**4. Act — the smallest size that fixes it.**
- *Precondition:* a cause from step 3.
- **a. Re-run / clear.** A hiccup (network blip, flaky test, timeout, an outage that has ended) or a push-triggered job that never fired → `run_workflow` with an explicit `ref` (the branch the failed run used; `main` unless it says otherwise). Log `rerun`. If the failed thing has nothing to re-run but is already fixed upstream (e.g. a newer commit landed and the next scheduled run will clear it), log `cleared` with the commit. At most 2 re-runs per dot per day; the third time, go up a size.
- **b. Urgent fix.** Urgent = something has stopped that Charles would feel today, or data is piling up or being lost (email filing, intake, the site). If the cause is in one file and is clear, fix it directly: `replace_in_file` on the right branch (cbrain-ui → `review`, per CB-185; everything else → `main`), commit as Chooch333 (CB-121), never touch `apply.yml` (CB-103). Read the commit back, then re-run the failed job to prove it. Log `fixed` with `commit_sha`. If it's more than one file or the cause needs design, write a short brief (template below) and build it in this same run by following `skills/orchestrate-build/SKILL.md` (fetch it from agent-library). Log `built` with `plan_id` and the last `commit_sha`.
- **c. Not urgent.** Write a short brief (template below) with `write_plan` on project `cbrain`: `overnight: true`, `target_repo` set, tags `stack-repairer`, `build-brief`, a `plain_title` and `plain_summary`; then `update_plan_status` → `queued`. These briefs carry standing approval (PROTOCOL.md, "## The Stack Repairer") — never ask Charles "Overnight: yes or no?". Before writing, `list_plans` on cbrain for a queued/running plan tagged `stack-repairer` for the same dot — if one exists, log `watching` pointing at it instead of writing a second. Log `briefed` with `plan_id`.
- **d. Hard gate** — a key or credential, spending money, or an irreversible data change. Do nothing except log `needs-you` with the exact ask in `finding` ("Top up Anthropic API credit at console.anthropic.com/settings/limits — the graph loaders paused at 14:02"). Never post it as a blocking question; the recap carries it.
- *Success evidence:* a run id, commit SHA or plan id for every action other than `needs-you`/`watching`.
- *Recovery:* a tool call is refused or errors → log `watching` with the error; try the next size next run.

**5. Log.**
- *Precondition:* each action from step 4.
- *Action:* insert one `stack_repairs` row per action (columns above), and confirm with a separate SELECT. For each **new kind** of incident — `search_state` on cbrain for a lesson tagged `stack-incident` with the same cause finds none — `add_lesson` on project `cbrain` (tags `stack-incident`, `stack-repairer`, the dot id) with the situation and the fix, so the Rules Inspector can see repeats.
- *Success evidence:* rows present on re-read.
- *Recovery:* insert fails → retry once, then note the action in the run marker's `detail.unlogged`.

**6. Run marker.**
- *Action:* insert the one `_run` row described above. Always, even when nothing was red.

**7. Daily recap (17:00 run only).**
- *Precondition:* this run started at or after 17:00 America/Indiana/Indianapolis, and today's log has no `_run` row with `detail.recap_sent = true`.
- *Action:* build four short sections from today's `stack_repairs` rows (and the evening's state):
  - **Fixed today** — `rerun`/`cleared`/`fixed`/`built` rows, one line each, saying what broke and what was done, with "(back to green)" when graded `green`.
  - **Queued for tonight** — `briefed` rows, by plain title.
  - **Last night's builds** — from `overnight_line` → `last_night`: one line per build (plain title + result).
  - **Needs you** — every `needs-you` row still open, in its exact-ask wording.
  - Plus one **Reader** line if it can be read from data: articles and facts the Collector processed today, from the newest Project State note on project `world-graph` tagged `world-graph-reader` dated today. If there's no such note, leave the line out.
  - Plain English, at most ~15 lines, no codes or file paths. If every section is empty and there is no Reader line, send nothing.
  - Send with Gmail `send_message` (from the connected claude.go.between@gmail.com account) to cecourtney10@gmail.com, subject `Stack Repairer — <Mon D>` (e.g. `Stack Repairer — Oct 6`), with a link to the Stack screen: https://cbrain-ui-git-review-chooch333s-projects.vercel.app/stack?view=flow
- *Success evidence:* the message id, recorded in the run marker's `detail.recap_message_id` with `recap_sent: true`.
- *Recovery:* the send fails → record `recap_sent: false` and the error; try once more at the end of the run. Never send a second recap the same day.

## Short brief template (for its own briefs)

```
# Build Brief — BB-YYYY-MM-DD-stack-fix-<dot-id>

**Build:** unnumbered (Stack Repairer)
**Overnight:** yes · **target_repo:** <owner/repo> · **after:** none

**What this is:** <one line — what broke and what will fix it>
**What I'll do:** <what the build chat produces>
**What you'll do:** Nothing — Stack Repairer briefs are pre-approved.

## Current state going in
### Asked for
- The <dot label> dot is <failing/late>: <reason>. Evidence: <run id / log line / URL>.
## Receiving chat
The night runner, or the Stack Repairer itself if urgent.
## Scope
In: <the fix>. Out: rules, skills, the stack map; anything past the failing dot.
## Directive
<numbered steps>
## Acceptance
1. <the dot reads green on the next Stack Inspector check> 2. <...>
## Pasteable prompt
> Execute Build Brief BB-YYYY-MM-DD-stack-fix-<dot-id>. Pull the plan from Project State (plan_id <id>, project cbrain). Answer forks yourself; stop only at hard gates. Standing rules CB-185, CB-121, CB-103 apply.
```

## Examples

### Example 1: a flaky run
`world-graph` is failing: `ingest_transcript.yml` failed 40 min ago. The job log shows a network timeout fetching a transcript; the run before succeeded. Not urgent-sized; a re-run fits → `run_workflow` (world-graph, ingest_transcript.yml, ref main, the same inputs) → log `rerun`. The 12:00 run grades it `green`.

### Example 2: a real bug
The same workflow fails three times in a row with the same `KeyError` in one file. Two re-runs already used today → size up. Video intake has stopped (Charles would feel it today) and the cause is one line → fix on main, re-run, log `fixed` with the commit. If the cause spans files → short brief, built now via orchestrate-build, log `built`.

### Example 3: money
`anthropic-api` is failing (the pause flag says the credit balance is too low). Hard gate → log `needs-you`: "Top up Anthropic API credit — video and email intake are paused until then." It shows under Needs you in the 17:00 recap; no other email goes out.

## Pitfalls

- **Don't trust the reason text alone.** The checker's reason can flip between two checks of a list dot (Oct 5: Smoke tests read "failed 9 days ago" then "5 days ago"). Read the runs.
- **A billing lock or a disabled workflow is not a code bug** (PROTOCOL.md, GitHub Actions rule). Re-running into a billing lock wastes nothing but proves nothing either.
- **Push-triggered runs don't replay after an outage** (CB-438). Re-dispatch them.

## Changelog

- **0.1.0** (2026-10-06) — Initial draft, written by Build 27 (BB-2026-10-05-stack-repairer). `status: draft` until the first live routine run. Judgment calls at build: `runs_in: claude-code` (not `claude-code-routine`) so the Skills tab files it in the Claude Code lane; a `_run` marker row every run so the Repairer's own stack-map dot can tell a quiet day from a dead routine.
