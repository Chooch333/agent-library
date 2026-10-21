---
name: next-steps-sweep
version: 0.1.0
status: draft
owner: Charles
updated: 2026-10-21
source: BB-2026-10-20-next-steps-dev-tab (Build 44)
requires: [references/project-state.md, references/thread-checkin.md]
wiring: {runs: alone, starts: "5 am daily", runs_in: claude-code-cloud,
  reads: [project-state, cbrain-db], writes: [project-state], label: Next steps sweep}
---
# Next steps sweep

Runs at 5 am Indianapolis. Fills the open-threads list with what chats did not
report, and fixes wording. Never emails. Never writes "no change".

Every write goes through Project State `checkin` with `source: 'sweep'` and a
thread_key of the form "<kind>:<id>" (e.g. "job:plan-<plan id>"). Every
next_step is plain words Charles can act on cold: no ids, tags, build codes or
file names (the database refuses them anyway). Read the list first with
`list_open_threads` (`include_closed: true`) so you know which keys exist and
which are chat-made.

1. Wait for night builds: if overnight_line shows a build running, check every
   10 minutes, up to 60 minutes, then go on.
2. Backfill (source 'sweep', thread_key "<kind>:<id>"), via `checkin`:
   - Comms Table disclosures with action_needed needs-charles, status noted:
     one row per build, kind 'job', waiting_on 'you', next_step = what he must
     do, in words.
   - Plans blocked, or night_log stuck/deploy-red last night: waiting_on 'you'.
   - Draft follow-up briefs not queued for 3+ days: waiting_on 'claude'.
   - cbrain workflow_runs status waiting-on-charles (lpeswznkxzeeyiqaewma).
   - Open next moves tagged wake: waiting_on 'a-build' or 'nobody'.
   - Active speed runs in agent-library lab/speed-run.md without an open row.
3. Close sweep rows whose source cleared (disclosure disposed, plan succeeded,
   run moved on). Never close a chat-made row.
4. Rewrite any open row whose text has ids or codes; same meaning, plain words.
5. Leave every other row alone. If a row's source has not changed, send the
   same next_step (or skip it) — never "still waiting".

## Where things live

- Project State MCP: `list_judgment_calls`, `list_plans`, `overnight_line`,
  `list_open_threads`, `checkin`, `close_thread`. Tables on Supabase
  `ujditldbqdiqigazkcak`: `open_threads`, `open_thread_history`, `night_runs`,
  `build_questions`, `plans`, `next_moves`.
- cbrain database (Supabase `lpeswznkxzeeyiqaewma`): `workflow_runs`.
- The list Charles reads: cbrain → Dev → Next steps (oldest at the top).

## Scheduled task

Name "Next steps sweep", `CRON_TZ=America/Indiana/Indianapolis 0 5 * * *`
(exact time, no jitter), prompt "Run agent-library
skills/next-steps-sweep/SKILL.md.", no local device, no notifications. Created
in a daytime chat with Charles's approval (unattended sessions cannot create
scheduled tasks).

## Changelog

- 0.1.0 (2026-10-21) — First version, Build 44 (BB-2026-10-20-next-steps-dev-tab).
  Seeded the list by one hand-run sweep the same night.
