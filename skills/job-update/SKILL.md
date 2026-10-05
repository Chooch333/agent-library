---
name: job-update
version: 0.1.0
status: active
triggers:
  - "add this" / "log this" / "put this on the job" (or plainly the same ask) in a FAW chat
owner: Charles
updated: 2026-10-05
source: Designed in DA chat DA-1005-faw-chat-input (2026-10-05). Uses the existing graph write door (world-graph docs/contracts/WRITE_PACKAGE.md); no new plumbing.
wiring:
  runs: with-you
  starts: "\"add this\" / \"log this\" in a FAW chat"
  runs_in: claude-chat
  reads: [cbrain-supabase]
  writes: [graph]
  origin: yours
  label: Job Update
---

# Job Update

## What

Lets a chat read a FAW job's current state and, **only when Charles asks**, write changes into the graph. Changes appear on the job's project screen labeled "Inferred · Claude"; Charles corrects them there.

## When

- **Write only on request.** Charles says "add this", "log this", "put this on the job" or the same thing in other words. FAW chats are also used for general construction and permitting talk that must not land in cbrain — never write without the ask.
- **Read any time** Charles asks about a job ("what's open on IMI?").
- Not for app/build work. That's Project State, via a Design Assist chat.

## Read

Supabase project `lpeswznkxzeeyiqaewma`, `execute_sql`.

1. **Jobs:** `select slug, title, coalesce(frontmatter->'lens_sources'->>'graph', 'project_'||slug) as group_id from pages where type='project' and deleted_at is null and frontmatter->>'kind' in ('faw-job','construction');`
   Match Charles's name for the job to a slug. If two could match, ask which.
2. **Current state** (filter every table by `group_id`):
   `pm_tasks` (task_id, title, type, status, due, duration, milestone_id, accountable) · `pm_milestones` (milestone_id, name, target, status, sort_order) · `pm_team` (person_slug, name, role) · `pm_raci` (task_id, person_slug, letter) · `pm_waits_on` · `pm_decisions` (is_current = true).
3. **People:** `select slug, title from pages where type='person' and deleted_at is null and title ilike '%<name>%';` Never guess who someone is.

## Write

1. **Collect** only what Charles stated as true in the stretch he's asking to log — not what-ifs, not options discussed, not your own suggestions he didn't adopt.
2. **Match before creating.** Use an existing task / milestone id when one fits; `create_task` / `create_milestone` only when nothing does. Same for subjects of design decisions (`pm_decisions.subject_id`).
3. **Unknown person or company:** leave that piece off (the task is still written), and tell Charles who was left off. Offer to add them through the cbrain capture path (`agent-library/references/chat-capture.md` → Archivist). Never invent a slug.
4. **Build one package** (contract: `Chooch333/world-graph` `docs/contracts/WRITE_PACKAGE.md` — read it if you need an op not shown here):

```json
{
  "schema": "write-package/v1.1",
  "package_id": "CHAT-YYYYMMDD-<job-slug>-<n>",
  "kind": "change",
  "project_slug": "<job slug>",
  "author": "claude",
  "source_ref": "CHAT-YYYYMMDD-<job-slug>-<n>",
  "true_from": "<ISO datetime: when this became true; default now>",
  "ops": [ ... ]
}
```

   Common ops: `create_task` (ref, title, type task|issue, status, due, duration, milestone, raci {a, r[], c[], i[]}, waits_on[]) · `set` (task, field status|due|duration|milestone|accountable|title, value) · `clear` (task, field due|milestone|accountable) · `add` / `remove` (task, field responsible|consulted|informed|waits_on, value) · `note` (task, text, effect neutral|reinforce|weaken|contradict, decision true|false, said_by) · `create_milestone` (ref, name, target, order) · `set_milestone` · `add_member` / `remove_member` (person, role) · `create_subject` + `decide` (design decisions).
   Statuses: task `open | in_progress | in_review | done | blocked`; milestone `planned | active | complete`. If Charles gave a date for when something happened, put it on that op's own `true_from` with `"date_basis": "stated"`.
   `<n>` = 1 for the first package on that job that day; check `select package_id from pm_package_status where package_id like 'CHAT-YYYYMMDD-<job-slug>-%'` and use the next number.
5. **Save it:** Custom GitHub MCP `create_or_update_file` → owner `Chooch333`, repo `world-graph`, path `data/project_writes/<package_id>.json`, branch `main`. The push starts the writer.
6. **Check it** after the writer runs (usually 2–6 min): `select status, counts, rejected from pm_package_status where package_id='<package_id>';` If no row after ~8 min, check `list_workflow_runs` on world-graph for a `write_protocol` run and say what you found — don't report success on silence.
7. **Receipt** — three lines, plain words:
   - **Logged to <job>:** what landed (e.g. "2 new tasks, 1 due date moved, 1 note").
   - **Skipped:** anything rejected or left off, and why. "None" if none.
   - **See it:** `https://cbrain-ui-git-review-chooch333s-projects.vercel.app/projects/<slug>`

## Never

- Write without Charles's ask.
- Write as author `charles` (that's only for his own screen edits).
- Edit the screen's tables (`pm_*`) directly — they're rebuilt from the graph.
- Log job work in Project State. App ideas or complaints from a FAW chat: one `add_note` on Project State project `cbrain`, tagged `faw`.

## Changelog

- **0.1.0** (2026-10-05) — Initial version. Write-on-request (Charles: FAW chats carry general construction/permitting talk that must not be dumped in cbrain). DA-1005-faw-chat-input.
