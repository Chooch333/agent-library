---
name: night-run
version: 0.6.0
status: draft
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: on-its-own
  starts: "Claude Code routine 'Night builds', daily 1 am America/Indiana/Indianapolis (Charles set 1 am, 2026-10-04)"
  runs_in: claude-code-cloud
  reads: [project-state, repos, vercel, open-threads, advisor-dispositions]
  writes: [plans, night_runs, open-threads, email]
  label: Night builds
---

# Night run

Builds shelved briefs tagged Overnight, one at a time, in dependency order, then re-checks open cards on the Next steps list. Nobody is watching: decide, log, move on. Stop only at hard gates (keys, money, deleting data) — and then only that build stops.

## Tools

- `overnight_line {}` (Project State) — the line: `overnight_line` view rows in order (`plan_id`, `plain_title`, `target_repo`, `queued_at`, `position`, `ready`, `waiting_on`), plus the newest night's `night_runs` rows.
- `night_log { plan_id, result, line, started_at?, ended_at? }` (Project State) — one `night_runs` row per outcome. `result` is one of `built` / `skipped` / `stuck` / `deploy-red` / `interrupted`, or `night-start` for the every-night start marker (step 0b — the only result written without a `plan_id`). The night is computed in America/Indiana/Indianapolis; a start before noon counts toward the previous night.
- `get_plan`, `update_plan_status` (Project State) — read a plan; set it `blocked` (or `abandoned`, step 2a only).
- `set_overnight` (Project State) — take a declined Stack Advisor brief off the line (step 2a).
- Supabase `execute_sql` on cbrain `lpeswznkxzeeyiqaewma` — read `advisor_dispositions` (step 2a; read only).
- `post_judgment_call` (Project State) — non-blocking disclosures.
- `list_open_threads`, `checkin` (Project State) — read the Next steps cards; write a card's checked status (`context`, `checked_at`, `chats`). Rules: `references/thread-checkin.md`.
- `list_deployments` (Vercel) — `projectId: cbrain-ui`, `teamId: team_8nMi0Bd6orQHGeTrMZYWCamm`, branch `review`.
- Gmail `send_message` — the one finish email, to Charles himself.

**Repos — edits through the connector.** Every repo is changed through the Custom GitHub connector (`get_file_contents`, `create_or_update_file`, `replace_in_file`, `list_commits`, `list_workflow_runs`, `run_workflow`). Never skip a build for "no repos attached", "no git access" or "can't clone". Access check before each build: one `get_file_contents` on the plan's `target_repo` (its README, or the brief's git path). Only if that call fails twice, log `skipped` with the error text in plain words. Pass this paragraph to the helper in step 4.

**Fallback.** If a step's Project State tool is not callable on the connector (new tools aren't visible until the connector is reconnected), use the equivalent SQL on Supabase project `ujditldbqdiqigazkcak`: read the line with `select * from overnight_line order by position`; log with `insert into night_runs (...)`. The start marker by SQL: `insert into night_runs (night, plan_id, result, line) values (<tonight's night date>, null, 'night-start', '<N> briefs on the line')` — the night date is the Indianapolis date, minus one day before noon. Confirm each insert with a separate SELECT. A card's re-check by SQL: `update open_threads set context = '<json>'::jsonb, checked_at = now() where thread_key = '<key>'` (the database still refuses ids/codes in any of its text, and never moves the card for a context change). A client holding an older `checkin` schema may pass `context` and `chats` as JSON text; the tool accepts that.

"Landed" = plan status `succeeded` AND its newest `night_runs` row is not `deploy-red`.

**Site checks.** The cbrain site runs its own checks at the start of every Vercel build (Build 79). A failing check fails the deploy, which step 5 logs as `deploy-red` and step 3 treats as a broken preview. The runner copies no repo.

## Dry run
If the run text says "dry run": read the line, report the order, what's ready and what each waits on, and which open cards step 7 would re-check. Build nothing, write nothing, email nothing (no start marker either).

## Loop
0. Clock: America/Indiana/Indianapolis. Start nothing new at or after 05:00.
0b. **Start marker — every night, first write, even when nothing is queued.** Read the line (`overnight_line`), count its rows, and log ONE row: `night_log { result: "night-start", line: "<N> briefs on the line" }` (no `plan_id`; e.g. "0 briefs on the line", "3 briefs on the line, 1 ready"). Write it once per run, before step 1, whatever the line holds — a quiet night must still show the runner ran. The 15-minute stack checker reads the newest `night_runs` row through Project State's public heartbeat (`https://project-state-mcp.vercel.app/api/heartbeat` → `night_runner.last_night`) and turns the Night builds dot late after 2 days with no row. If the write fails, retry once, then carry on with the night (a missing marker only makes the dot look late; it never stops a build).
1. Resume check: an Overnight plan still `running` from an earlier night with no live session → if it has no `interrupted` row, log `interrupted` (`night_log`) and build it first (the builder reconciles against live state); if it already has one, set it `blocked` (`update_plan_status`) and post a disclosure (`post_judgment_call`) "interrupted twice."
2. Read the line (`overnight_line`). Take the lowest-position row with `ready = true`, skipping rows whose `target_repo` is on tonight's skipped-repos list (kept in memory, see step 3), and rows set aside tonight by 2a. None ready → go to step 7.
2a. **Stack Advisor briefs** (plan tagged `advisor-auto`; check with `get_plan`). These are small upgrades the Stack Advisor put on the shelf itself; Charles has a day to say no. Before building one:
   - **Too new:** queued (`queued_at`) less than 18 hours ago → not ready tonight. Set it aside for tonight and go to 2. No `night_log` row, no card, no email; it builds on a later night.
   - **Declined:** read its ADV id from its tags (`adv-NNN` → `ADV-NNN`) or its brief, then on cbrain Supabase `lpeswznkxzeeyiqaewma`: `select 1 from advisor_dispositions where adv_id = '<ADV-NNN>' and disposition = 'declined' and created_at > '<queued_at>' limit 1`. A row → Charles said no: `update_plan_status` → `abandoned` (executor_report "Declined on the Stack screen before it built"), `set_overnight false`, and go to 2. No `night_log` row, no card, no email — the Advisor folds his answer on its next run. If the query errors, retry once; if it still errors, set the plan aside for tonight (never build an unchecked one, never abandon on an error), log nothing, and check again tomorrow.
3. Repo check: if the plan's repo deploys to Vercel (cbrain-ui → review branch preview), the newest review deployment must be READY (`list_deployments`, projectId `cbrain-ui`, teamId `team_8nMi0Bd6orQHGeTrMZYWCamm`, branch `review`). If it's ERROR, log `skipped` "the preview is broken" (`night_log`) for every row in that repo tonight, add the repo to tonight's skipped-repos list, and go to 2.
4. Build: set nothing yourself — dispatch ONE helper (subagent) with the brief's own pasteable prompt plus: "Autonomous overnight run. Do all the work yourself; no further dispatch. Forks: decide and log. Hard gate: post the question, mark the plan blocked, stop. Don't run the unit-tests workflow on GitHub." Wait for it.
5. Confirm it landed (`get_plan`):
   - Plan status `succeeded` with a done receipt → if the repo deploys, poll the review deployment for the build's last commit (`list_deployments`, every 2 min, up to 30 min). READY → log `built`. ERROR → log `deploy-red` (its dependents now wait).
   - Status `blocked` or `failed` → log `stuck` with the reason in plain words.
   - Helper died / usage limit → log `interrupted` and go to step 7.
6. Go to 2. The line is re-read every time, so builds unblocked tonight run tonight.
7. **Re-check open cards** (BB-2026-10-21-next-steps-panel). Runs every night after the build loop, before Finish — also on nights with no builds. Still start nothing new at or after 05:00: stop picking cards then, and go to Finish.
   - **Pick up to 15 open cards** (`list_open_threads`): first those with `checked_at` null; then the oldest `checked_at` older than 7 days; then cards whose source moved since `checked_at` (its plan's status or `completed_at` changed, a newer commit or workflow run, a wake next move completed).
   - **Read the source the `thread_key` names**: `job:plan-<id>` / `job:draft-<id>` → `get_plan` (status, executor_report, done receipt, its disclosures via `list_judgment_calls`), and any workflow runs (`list_workflow_runs`) or commits (`list_commits`) the plan or card names; `job:wake-<id>` → that next move; a chat tag (`DA-…`) or `<kind>:<slug>` → its design topic, its plan by `chat_tag`, the Working Doc or links on the card. Read only what the card points at.
   - **Write the checked status** with `checkin` (same `thread_key`, `kind`, `plain_name`; `source: "job"`): `context` = `{ stand: one sentence, done/left/watch: [{text, checked}], recommend: one sentence, verdict }`, at most 8 lines across done/left/watch, plain words only (the database refuses ids and codes in any of it). A line is `checked: true` only if this run read the evidence for it; anything taken from the card's own words without reading the source is `checked: false`. Set `checked_at` to now. Identical context changes nothing and never moves the card.
   - **Verdict**: every left item done → `looks-done`; the waiting reason is no longer true → `stale-reason`, and send a rewritten `next_step` / `waiting_on` that say what is really next; otherwise `open`. A `looks-done` card whose every line is `checked: true` is closed (`close_thread`, closed_how "nothing left for you"); one with any unchecked line stays open for the next check. Never close a card whose source this run did not read (Closing out, `references/thread-checkin.md`; Charles 2026-11-09 replaces the old click-Done finish).
   - **Build-session links**: for a plan card, look for commits whose message names the plan's BB id or plan id (`list_commits` on its `target_repo`, branch `review` for cbrain-ui); add each commit's `Claude-Session:` url to `chats` with role `build-session` (label "Build session <date>"). `chats` merges by url and never drops entries.
   - **Tonight's trouble**: for every `stuck`, `deploy-red` or `skipped` result tonight, `checkin` a card: `thread_key` `job:plan-<plan id>`, `kind` `job`, `source` `job`, `plain_name` = the build's plain title, `next_step` = what Charles needs to do in words, `waiting_on` `you`. A skip means a ready brief did not build, so it always needs a look.
   - **Leftovers**: for every `built` result tonight whose report names a hand-on (Closing out, bin 4: something only Charles can do; a step handed to a later build or a check Claude can run is not one), `checkin` a card the same way with that leftover as `next_step`. No email for these.
   - If a check-in fails, retry once, then move on; the card is picked again tomorrow.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the brief's plain title, for a build that ended stuck or deploy-red (e.g. "Next steps side panel")
- Opens when: a build ends `stuck`, `deploy-red` or `skipped`, is interrupted twice, or is built with something left for Charles (step 7, "Tonight's trouble" and "Leftovers")
- Checks in: when a run leaves something open; and every night's re-check writes checked status on up to 15 open cards (step 7)
- Closes when: the job clears it (a later night builds the plan and it lands), or nothing on it waits on Charles (`close_thread`, closed_how "nothing left for you"; Closing out in `references/thread-checkin.md`)

## Finish
- If anything ended `stuck`, `deploy-red`, `skipped`, or interrupted twice: send ONE email to Charles (Gmail, to himself), subject "Night builds — N need you", one plain line per item plus the Build Shelf link (https://cbrain-ui-git-review-chooch333s-projects.vercel.app/dev?tab=shelf). Otherwise send nothing — the shelf's Last night strip is the report.
- Never review a plan, dispose a disclosure, edit a brief, change a tag, close a Next steps card, or set a card's project. DA chats and Charles do that. (Abandoning a Stack Advisor brief Charles declined, step 2a, is his answer carried out, not a review.)

## Changelog

- **v0.6.0** (2026-11-10) — New "Site checks (cbrain-ui builds only)" section: a night build that changes the cbrain site runs the site's own `npm test` on a read-only copy before it is called done (builder in step 4; runner backstop in step 5, failure → Next steps card + email line, row stays `built`); check machinery that can't run never blocks a build (disclosure + one email line). "Repos" paragraph now says edits go through the connector and the one copy is read-only. Build 59 (BB-2026-10-28-night-site-checks), ADV-053 adopted narrower (no saved cloud environment). Timings measured 2026-10-28 with `add_repo`: copy 2 s, install 20 s, checks 29 s, 35 files. In the Night builds session on 2026-11-10 there was no `add_repo` and the clone was refused, so the copy path is unproven there; the runner falls back to step 5 until it has read access.
- **v0.5.1** (2026-11-10) — Kinds line: the job card closes once nothing on it waits on Charles, not on a click; step 7 names the old finish without the phrase. Build 78 (BB-2026-11-09-closing-out).
- **v0.5.0** (2026-11-09) — Step 7 closes a `looks-done` card whose every line was checked against its source this run (closed_how "nothing left for you"), replacing "Never close a card — Charles clicks Done"; leftover cards only for hand-ons (Closing out, `references/thread-checkin.md` 0.4.0). Charles, 2026-11-09, Design Assist chat. Edited inline at his direction.
- **v0.4.0** (2026-10-29) — New step 2a for Stack Advisor briefs (tag `advisor-auto`, Build 57, BB-2026-10-28-advisor-done-for-you): one queued under 18 hours ago is not ready tonight (no log, no card), so Charles always gets a day; one with a `declined` Stack-screen answer (`advisor_dispositions`, cbrain Supabase) newer than its `queued_at` is set `abandoned` and taken off the line (`set_overnight false`) with no `night_log` row, no card and no email. Tools gain `set_overnight` and a read-only `advisor_dispositions` query.
- **v0.3.1** (2026-10-28) — Step 7: `skipped` results now get a Next steps card like `stuck` and `deploy-red`, and join the Finish email; new "Leftovers" bullet: a `built` result whose report names something still left for Charles gets a card (no email). Night of 2026-10-21 skipped both builds on a false reason with no alert. Adopted narrower from ADV-086 (Advisor's daily watcher idea) in a Design Assist chat at Charles's direction; no new scheduled task.
- **v0.3.0** (2026-10-23) — New loop step 7, "Re-check open cards": every night after the build loop (also on nights with no builds, still stopping at 05:00) the runner picks up to 15 open Next steps cards (never checked first, then checked more than 7 days ago, then source moved), reads the source each card names, writes `context` + `checked_at` honestly, marks `looks-done` / `stale-reason` (rewriting a stale reason), adds build-session chat links from commits, and checks in a card for every stuck or deploy-red build. Never closes a card. Replaces the retired 5 am Next steps sweep. New Progress tracking section. Per Build BB-2026-10-21-next-steps-panel.
- **v0.2.1** (2026-10-22) — "Repos — no clone needed": repos are reached through the Custom GitHub connector; an access check is one `get_file_contents` on the target repo; never skip for "no repos attached". Night of 2026-10-21 skipped both builds on that mistaken reason.
- **v0.2.0** (2026-10-08) — New loop step 0b: every night the runner starts it logs one `night_runs` row with `result = 'night-start'`, no `plan_id`, and `line` = how many briefs were on the line — even when none are queued — so a quiet night is not mistaken for a dead runner. Project State migration `build27_1_night_start_marker` lets `plan_id` be null (only for `night-start`) and adds `night-start` to the allowed results; `night_log` accepts it. Read by the stack map's Night builds dot through Project State's public heartbeat. Per Build 27.1 (BB-2026-10-07-stack-checks-claude-side).
- **v0.1.0** (2026-10-04) — Created by Build 26 (BB-2026-10-04-night-builds): the overnight runner for Overnight-tagged briefs, reading `overnight_line` and logging to `night_runs` via `night_log`.
