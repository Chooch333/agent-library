# Stack Advisor — the Supabase copy (step 6e)

Read at DELIVER. Moved here from SKILL.md v1.8.1 step 6e by
BB-2026-10-05-advisor-reads-smarter (Build 28), adjusted for the run packet:
the ledger is now written by `tools/advisor/run_packet.py` from your
`run_result.json`, so ledger values below come from your own result (new
ideas) and from the refreshed packet's `ledger_changed` (everything else).

**Critic live (Build 28.1, BB-2026-10-05-advisor-thinks-bigger).** When
`critic_live.json` exists, the Advisor does only the last bullet below
(status/response sync of rows that already exist) and the Advisor Critic
does the rest when it publishes — for the ideas it kept. A LEDGER row whose
status is `draft` or `cut` is never written to `advisor_ideas`.

Supabase copy for the cbrain-ui Stack screen (project
`lpeswznkxzeeyiqaewma`). Same data as the ADV file and the ledger, stored as
rows so the screen can read it directly instead of parsing git. Git stays
the record; these rows copy it.

- Upsert one `advisor_runs` row keyed on `run_id` = this run's ADV file
  name without `.md` (e.g. `ADV-2026-10-07`): `run_date`; `preamble` =
  the brief's opening paragraphs (everything before the first idea
  block); `sources_read` = JSON list of the items you skimmed in 3b, each
  `{kind, id, channel_or_feed, title, url}` (one entry per digest member
  you rated); `queue_depth` = packet items left unskimmed after this run
  (0 if none); `graph_answered` = true if any step 3 query came back with
  a grounded answer, false if the graph didn't know; `questions` = JSON
  list of this brief's "Questions for Charles" (empty list if none);
  `brief_path` = the git path from 6a.
- Upsert one `advisor_ideas` row per idea in this brief, keyed on
  `adv_id`: `title` = the ledger `Idea` text (your `surfaced[].ledger_idea`
  for a new idea); `plain_title` = the heading's plain title (rule 6, 10
  words or fewer, no bare codes, no outside company/product names);
  `body` = JSON of the block exactly as written in 6a — `{from_source,
  what_you_have, why_the_connection, what_gets_better, confidence,
  resurfaced_note}` plus `in_plain_terms` holding the "In plain terms:"
  sentence ("What your records show" also goes in `from_source` for
  own-records ideas; `resurfaced_note` is null unless rule e applies);
  `effort` = S/M/L; `high_conviction`; `component_ids` = the stack-map
  component ids the idea connects to, from its `connects_to` (for a plan
  or decision, the component it is about; write an id even if the map
  doesn't list it yet — the screen shows it as Unmapped); `source` =
  `{kind, name, title, url}` from the block heading (`kind: records`,
  `name` = the display IDs, `url` null for own-records ideas);
  `first_seen`; `status` and `response` = the ledger's Status and
  Response (`surfaced` and empty for a new idea); `brief_ref` = the
  ledger `Brief` cell (this run's ADV path); `pool_ref` = the idea's
  `pool_id`. A new idea gets `first_run_id` = `latest_run_id` = this run
  and `resurface_count` 0. A resurfaced idea keeps `first_run_id`, sets
  `latest_run_id` to this run, and adds 1 to `resurface_count`.
- Then sync every other ledger row that already has an `advisor_ideas`
  row: touch **only** `status` and `response`, using the refreshed
  packet's `ledger_changed` (it lists every row whose Status or Response
  changed since the previous packet, from this run's feedback or from a
  DA/Build chat's `building`/`addressed` flip). Never rewrite `title`,
  `plain_title` or `body` for an idea that isn't in this run's brief.
  Only a ledger row with **no** `advisor_ideas` row yet is built fresh
  from its `Brief` file — written straight to this run's standard
  ("Writing for Charles", rule 1a) as it's created. The advisor is the
  only writer of `advisor_ideas.status`; the app never sets it.
- Read back with a SELECT: the run row, plus a count of this run's idea
  rows. If this write fails, 6a–d still stand. Name the error in the 6d
  note; the next run's sync repairs the gap.
