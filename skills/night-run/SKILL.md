---
name: night-run
version: 0.1.0
status: draft
wiring:
  runs: on-its-own
  starts: "Claude Code routine 'Night builds', daily 11 pm America/Indiana/Indianapolis"
  runs_in: claude-code-cloud
  reads: [project-state, repos, vercel]
  writes: [plans, night_runs, email]
  label: Night builds
---

# Night run

Builds shelved briefs tagged Overnight, one at a time, in dependency order. Nobody is watching: decide, log, move on. Stop only at hard gates (keys, money, deleting data) — and then only that build stops.

## Tools

- `overnight_line {}` (Project State) — the line: `overnight_line` view rows in order (`plan_id`, `plain_title`, `target_repo`, `queued_at`, `position`, `ready`, `waiting_on`), plus the newest night's `night_runs` rows.
- `night_log { plan_id, result, line, started_at?, ended_at? }` (Project State) — one `night_runs` row per outcome. `result` is one of `built` / `skipped` / `stuck` / `deploy-red` / `interrupted`. The night is computed in America/Indiana/Indianapolis; a start before noon counts toward the previous night.
- `get_plan`, `update_plan_status` (Project State) — read a plan; set it `blocked`.
- `post_judgment_call` (Project State) — non-blocking disclosures.
- `list_deployments` (Vercel) — `projectId: cbrain-ui`, `teamId: team_8nMi0Bd6orQHGeTrMZYWCamm`, branch `review`.
- Gmail `send_message` — the one finish email, to Charles himself.

**Fallback.** If a step's Project State tool is not callable on the connector (new tools aren't visible until the connector is reconnected), use the equivalent SQL on Supabase project `ujditldbqdiqigazkcak`: read the line with `select * from overnight_line order by position`; log with `insert into night_runs (...)`. Confirm each insert with a separate SELECT.

"Landed" = plan status `succeeded` AND its newest `night_runs` row is not `deploy-red`.

## Dry run
If the run text says "dry run": read the line, report the order, what's ready and what each waits on. Build nothing, write nothing, email nothing.

## Loop
0. Clock: America/Indiana/Indianapolis. Start nothing new at or after 05:00.
1. Resume check: an Overnight plan still `running` from an earlier night with no live session → if it has no `interrupted` row, log `interrupted` (`night_log`) and build it first (the builder reconciles against live state); if it already has one, set it `blocked` (`update_plan_status`) and post a disclosure (`post_judgment_call`) "interrupted twice."
2. Read the line (`overnight_line`). Take the lowest-position row with `ready = true`, skipping rows whose `target_repo` is on tonight's skipped-repos list (kept in memory, see step 3). None ready → finish.
3. Repo check: if the plan's repo deploys to Vercel (cbrain-ui → review branch preview), the newest review deployment must be READY (`list_deployments`, projectId `cbrain-ui`, teamId `team_8nMi0Bd6orQHGeTrMZYWCamm`, branch `review`). If it's ERROR, log `skipped` "the preview is broken" (`night_log`) for every row in that repo tonight, add the repo to tonight's skipped-repos list, and go to 2.
4. Build: set nothing yourself — dispatch ONE helper (subagent) with the brief's own pasteable prompt plus: "Autonomous overnight run. Do all the work yourself; no further dispatch. Forks: decide and log. Hard gate: post the question, mark the plan blocked, stop." Wait for it.
5. Confirm it landed (`get_plan`):
   - Plan status `succeeded` with a done receipt → if the repo deploys, poll the review deployment for the build's last commit (`list_deployments`, every 2 min, up to 30 min). READY → log `built`. ERROR → log `deploy-red` (its dependents now wait).
   - Status `blocked` or `failed` → log `stuck` with the reason in plain words.
   - Helper died / usage limit → log `interrupted` and finish the night.
6. Go to 2. The line is re-read every time, so builds unblocked tonight run tonight.

## Finish
- If anything ended `stuck`, `deploy-red`, or interrupted twice: send ONE email to Charles (Gmail, to himself), subject "Night builds — N need you", one plain line per item plus the Build Shelf link (https://cbrain-ui-git-review-chooch333s-projects.vercel.app/shelf). Otherwise send nothing — the shelf's Last night strip is the report.
- Never review a plan, dispose a disclosure, edit a brief, or change a tag. DA chats do that.

## Changelog

- **v0.1.0** (2026-10-04) — Created by Build 26 (BB-2026-10-04-night-builds): the overnight runner for Overnight-tagged briefs, reading `overnight_line` and logging to `night_runs` via `night_log`.
