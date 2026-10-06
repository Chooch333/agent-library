---
name: stack-advisor
version: 1.9.0
status: active
triggers: ["Stack Advisor run"]
owner: Charles
source: BB-2026-08-27-stack-advisor (DA session 2026-08-27); pool/scoring system per BB-2026-09-03-advisor-idea-pool; run packet per BB-2026-10-05-advisor-reads-smarter
wiring:
  runs: on-its-own
  starts: "Mon/Wed/Fri schedule"
  runs_in: cowork
  reads: [world-graph, project-state, cbrain]
  writes: [idea-pool, advisor-tables, email]
  stack: []
  origin: yours
  label: Stack Advisor
---

# Stack Advisor

## What
Every scheduled run, understand what Charles is building, read the newest
sources, and deliver a brief of up to 6 concrete upgrade ideas for the stack
or the process. Propose only — never build, never edit the stack map.

Code does the counting, you do the thinking. A nightly script
(`cbrain/tools/advisor/run_packet.py`, workflow `advisor-packet.yml`) keeps
the hidden idea pool (`docs/advisor/pool.json`) and the ledger
(`docs/advisor/LEDGER.md`): decay, archive, merges, source scores, ledger
rows. It hands you one small file, `cbrain/docs/advisor/run_packet.json`, and
folds your judgments back from `docs/advisor/run_result.json`. **Never open
`pool.json` or `LEDGER.md` whole.** Shapes of both files:
`cbrain/docs/advisor/README.md`.

## Job boundary
- Stack Manager = librarian (keeps the map accurate). Stack Advisor = scout
  (proposes improvements). Never dispose MAP-EDIT items; never edit
  concepts/stack-map.md.
- Accepted ideas leave through the normal door: Charles takes them to a
  DA chat, which produces a Build Brief. The advisor never queues plans.
- **The brief is the only email.** Never email Charles that a run failed
  (a connector missing, this file unreadable, a tool erroring, the graph
  query timing out). A failing run stops and, if it can, leaves the 6d
  Project State note on stack-map saying what failed. The Stack Advisor
  dot's output check (`advisor_runs.run_date`, Mon/Wed/Fri) goes late
  when runs stop, and the Stack Repairer covers it in its evening recap
  (Build 27, BB-2026-10-05-stack-repairer).

## Each run, in order
1. FEEDBACK FIRST. Collect Charles's answers from both sources (a union;
   either may be empty) as `feedback` entries for run_result.json —
   `{adv_id, answer: interested|declined|scoping|done, note, at, via}`:
   a. Gmail: his reply to the latest "Stack Advisor brief" email
      (`via: email`; map his words to one of the four answers).
   b. Stack screen: `advisor_dispositions` on `lpeswznkxzeeyiqaewma` where
      `consumed_at is null`, oldest first (`via: stack`, `answer` =
      `disposition`, `at` = `created_at`).
   The script applies the ledger rules (latest wins, declined notes join,
   `building`/`addressed` guards, Done → `addressed`). Check each ID
   against the packet's `ledger_status`: an ID with no row is left
   unconsumed and named in the brief; an answer on an `addressed` row, or
   a non-Done answer on a `building` row, is skipped (still consumed) and
   named in the brief's opening. For a Done answer, name in the opening
   any draft/queued/running plan whose tags or provenance cite that ADV ID.
2. ORIENT — read live, keep nothing cached:
   a. Project State plan 31fdcb9b (Master Roadmap) and plan 076b64ca
      (Build Map Skeleton).
   b. The shelf: plans queued or running across all projects (Supabase SQL
      join plans→projects), and get_activity, all projects, last 7 days.
   c. cbrain get_entity('stack-map') — the canonical component list.
   d. `run_packet.json`: live ideas (`ideas`, ≤ 20, with ledger status and
      Response), every other idea as one line (`index`), `ledger_status`,
      `next_pool_id`, `next_adv_id`, the previous brief (`last_brief`) and
      the waiting `items`.
3. READ THE GRAPH. Dispatch Chooch333/world-graph workflow `query.yml`
   (ref `main`, mandatory) 1–3 times with questions shaped by the shelf.
   Read the new files in `answers/`. "The graph doesn't know" is a real
   answer.
3b. INTAKE — skim, then deep-read. The packet already holds only your
   sources (followed channels, feeds marked `stack_advisor`), oldest first,
   each with an excerpt and its full length (`chars`). Items over 10 KB
   carry start/middle/end slices; a `digest` item is one feed's whole
   batch (newest first) and gets one rating for the batch.
   a. **Skim** up to 30 items. Rate each high / medium / low: could it
      change something on the shelf or in a live component?
      `title_only` = a speechless video: judge by title, channel and
      date; never deep-read it.
   b. **Deep-read** the top ~6 (highs first) in full from `path`
      (`repo:file` — owner Chooch333, `get_file_contents`; for a digest,
      the members that matter).
   c. Low = done. Medium = eligible once more next run (the packet marks
      it `medium_once`; any rating then closes it). Unskimmed items wait.
   d. Video text is auto-captioned: names come out misspelled ("Cloud
      Design" for Claude Design). Never quote a caption as a product name
      without checking it.
   e. Each deep-read item yields 0–3 candidate ideas. Each must name a
      `connects_to` item from Charles's own records, or it is trivia and
      is not pooled.
4. SCORE AND SELECT. Score every candidate and every live idea that got
   new evidence:
   - **Rubric (0–100):** *connection* 0–40 (names a queued/running plan,
     an open decision, or a live component and says exactly what
     changes) · *evidence* 0–25 (grounded in a source you read; +8 per
     additional independent source, max 25) · *payoff* 0–20 (S effort
     with real payoff scores high; L effort caps at 10) · *timeliness*
     0–15 (on the shelf now = 15; roadmap-later = 5; neither = 0).
   - **Threshold:** `total ≥ 60` to be eligible for email.
   - **High conviction:** `total ≥ 85` and ≥ 2 independent sources (two
     videos/articles, or one plus Charles's own records). Exactly one per
     brief, leads the email, heading gets ` · HIGH CONVICTION`. Any other
     qualifier goes in `held` (first in line next run, re-scored).
   - **Cap:** at most 6 = 1 high-conviction + up to 5 standard, best score
     first. 0–2 ideas is fine. **Never send a sub-60 idea to fill a slot.**
   - **Slow day:** under 5 new eligible ideas → fill from live ideas
     `≥ 60` never surfaced, oldest-high-score first.
   - **Merge:** compare each candidate's `topic_key` and title with the
     packet's `ideas` and `index`. Same idea from a new source → reuse that
     idea's `topic_key` (the script merges it, reviving it if archived)
     or list it under `rescored` with `add_sources`.
   - **Same idea, same source — never twice.** A surfaced idea whose only
     new evidence is a source it already lists is not resurfaced.
   - **Same theme, new source — may return once** with a `Raised again
     because:` line, unless the idea's ledger Response (in the packet)
     already covers the new angle; if it doesn't, say what it missed.
   - **Already acted on — never again.** Ledger `building`, `declined` or
     `addressed` ideas are excluded by the script. Also exclude (and list
     under `adopt`) an idea when a Project State plan or decision cites
     its ADV ID (search provenance/tags for `ADV-NNN`), or when the change
     is already live in the component it names.
   - Ideas from Charles's own records follow the same rubric but cannot be
     high-conviction on records alone.
   - Assign `adv_id`s from `next_adv_id` upward (a resurfaced idea keeps
     its own) and new pool ids from `next_pool_id` upward.
   - Decay, archive, source scores and ledger rows are the script's job.
     Zero ideas is a legal brief ("nothing met the bar").
5. ASK IF UNSURE. If a current build's purpose can't be stated in one
   sentence, add "Questions for Charles" — max 3, closed choices with a
   recommendation each. Never block on them.
6. DELIVER. First read `references/brief-format.md` (brief format and
   "Writing for Charles"), `references/email-format.md` and
   `references/deliver.md` (the Supabase copy) in this folder. Then:
   a. Commit the brief → `cbrain/docs/advisor/ADV-YYYY-MM-DD.md`; read back.
   b. Commit `cbrain/docs/advisor/run_result.json` (shape in the README):
      `run_id` (the ADV file name), `run_at`, `brief`, `feedback`, `skim`
      (every item you rated: `key`, `ids` copied from the packet,
      `rating`), `candidates`, `rescored`, `adopt`, `surfaced`, `held`.
      Read it back. Only then set `consumed_at = now()` on every
      disposition row folded or skipped in step 1b. The commit triggers
      `advisor-packet.yml`, which folds it into the pool and LEDGER within
      minutes; confirm the new packet shows `last_run_id` = your `run_id`
      (if not after ~10 minutes, name it in the 6d note).
   c. Gmail send — subject "Stack Advisor brief ADV-YYYY-MM-DD", per
      `references/email-format.md`.
   d. Project State note on stack-map: one-paragraph digest + git path,
      plus packet bytes and items skimmed / deep-read.
   e. Supabase copy for the Stack screen, per `references/deliver.md`.

Changelog: `references/changelog.md`. Latest: **v1.9.0** (2026-10-06) — run
packet, skim-then-deep-read, merge-back via run_result.json, formats moved to
references (BB-2026-10-05-advisor-reads-smarter, Build 28).
