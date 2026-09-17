---
name: stack-advisor
version: 1.5.0
status: active
triggers: ["Stack Advisor run"]
owner: Charles
source: BB-2026-08-27-stack-advisor (DA session 2026-08-27); pool/scoring system per BB-2026-09-03-advisor-idea-pool
---

# Stack Advisor

## What
Every scheduled run, understand what Charles is currently building, comb the
world graph's parsed knowledge, and deliver a brief of up to 6 concrete
upgrade ideas for the stack or the process. Propose only — never build,
never edit the stack map (that is the Stack Manager's job).

Ideas don't go straight from evidence to email. Every new transcript is
read once and its candidate ideas go into a hidden, ranked pool
(`cbrain/docs/advisor/pool.json`); the brief is built from the pool by
score, not by whatever happened to arrive that run. Charles never sees the
pool — he sees at most 6 ideas, and only ideas that clear the bar.

## Job boundary
- Stack Manager = librarian (keeps the map accurate). Stack Advisor = scout
  (proposes improvements). Never dispose MAP-EDIT items; never edit
  concepts/stack-map.md.
- Accepted ideas leave through the normal door: Charles takes them to a
  DA chat, which produces a Build Brief. The advisor never queues plans.

## Each run, in order
1. FEEDBACK FIRST. Two sources, always read both — a union, not a
   replacement; either one may be empty and the step still works.
   a. Gmail: find Charles's reply to the most recent advisor
      brief email (subject prefix "Stack Advisor brief"). Record each
      disposition in cbrain docs/advisor/LEDGER.md (statuses: surfaced /
      interested / building / declined). No reply = no change.
   b. Stack screen: on the cbrain Supabase project
      (`lpeswznkxzeeyiqaewma`), read `advisor_dispositions` where
      `consumed_at is null`, oldest `created_at` first. Each row is an
      answer Charles gave on the cbrain-ui Stack screen; fold it into
      LEDGER.md exactly as the same answer in an email reply would be
      folded, matching the row's `adv_id` to the ledger `ID`:
      - `interested` → Status `interested`.
      - `declined` → Status `declined`. The row's `note` is Charles's
        reason and goes in the `Response` column as "declining because
        {note}", the same way a reason given in an email reply would.
      - `scoping` ("Scope it") → Status `interested`, and append
        " — scope requested YYYY-MM-DD (Stack screen)" to the row's
        `Idea` cell. Charles is taking the idea to a DA chat; no Build
        Brief exists yet, so `building` stays the DA chat's flip at
        scoping (with its intended Response), per the ledger contract.
      Several rows for one ID: apply them in order, so the latest wins.
      If an email reply and a row disagree, the later of the two wins.
      Never change an `addressed` row, and never move a `building` row
      back to `interested` — skip that disposition (it is still
      consumed) and say so in the brief's opening paragraph. A row whose
      `adv_id` matches no ledger row is left unconsumed and named in the
      brief.
   c. Commit LEDGER.md once for both sources and read it back. Only
      after the read-back shows the change, set `consumed_at = now()`
      on every row folded or skipped in 1b — so no row is processed
      twice, and none is lost if the commit fails. No reply and no
      unconsumed rows = no change.
2. ORIENT — read live, keep nothing cached:
   a. Project State plan 31fdcb9b (Master Roadmap) — the five-layer map
      and open decision queue.
   b. Plan 076b64ca (Build Map Skeleton) — what's built vs in flight.
   c. The shelf: plans with status queued or running across all projects
      (Supabase SQL join plans→projects is the reliable pattern).
   d. get_activity, all projects, last 7 days.
   e. cbrain get_entity('stack-map') — the canonical component list.
   f. docs/advisor/LEDGER.md + docs/advisor/pool.json + the previous brief.
3. READ THE GRAPH. Dispatch Chooch333/world-graph workflow query.yml
   (workflow_id "query.yml", ref "main" — ref is mandatory) 1–3 times with
   questions shaped by the current shelf. Wait for runs to finish; read the
   new files in answers/. Graph answers are grounded-only; treat "the graph
   doesn't know" as a real answer.
3b. INTAKE NEW SOURCES (videos + articles). Read
    `world-graph/data/ingest_log.json` and
    `world-graph/data/article_ingest_log.json`; for every `outcome:
    ingested` record in either log with `ingested_at >
    meta.last_intake_at` (from `cbrain/docs/advisor/pool.json`), read the
    source file — `world-graph/data/transcripts/{video_id}.md` for a
    video, `world-graph/data/articles/{article_id}.md` for an article —
    and write 0–3 candidate ideas into the pool. A source with nothing
    relevant yields zero candidates — that's normal. Each candidate must
    name at least one `connects_to` item from Charles's own records (a
    stack-map component, a queued/running plan, an open decision); if it
    can't, it is not an idea, it's trivia — don't pool it. Set
    `meta.last_intake_at` to the newest `ingested_at` processed across
    both logs. Cap 12 items per run, combined across videos and articles
    (not 12 each); leftover items wait for the next run (they stay "new"
    by timestamp).
4. SCORE AND SELECT. Score every non-archived pool idea, then select what
   goes in this run's brief:
   - **Rubric (0–100):** *connection* 0–40 (names a queued/running plan, an
     open decision, or a live component and says exactly what changes) ·
     *evidence* 0–25 (grounded in a transcript the advisor read; +8 for
     each additional independent source, max 25) · *payoff* 0–20 (what
     gets better ÷ effort: S effort with real payoff scores high; L effort
     caps at 10) · *timeliness* 0–15 (touches something on the shelf now =
     15; roadmap-later = 5; neither = 0).
   - **Threshold:** `total ≥ 60` to be eligible for email.
   - **High conviction:** `total ≥ 85` **and** `sources` has ≥ 2
     independent entries (two different videos, or a video plus a
     `records` source with display IDs). Exactly one per brief; it leads
     the email and its heading gets ` · HIGH CONVICTION` appended. If more
     than one qualifies, the rest are set `held: true`, `status: held`,
     and are first in line next run (re-scored, not automatically sent).
   - **Cap:** at most 6 ideas per brief = 1 high-conviction (if any) + up
     to 5 standard, best score first. A brief with 0, 1 or 2 ideas is
     fine. **Never send a sub-60 idea to fill a slot** — the cap is a
     ceiling, not a target.
   - **Slow day:** if fewer than 5 new eligible ideas exist, fill from
     older pooled ideas that are ≥ 60 and never surfaced, oldest-high-score
     first. Still never below 60.
   - **Same idea, same video — never twice.** A surfaced idea whose only
     new "evidence" is the video it already came from is not resurfaced,
     however high it scores. `sources[].video_id` is the check.
   - **Same theme, new video — may return.** If a *new* video (or a new
     record of Charles's) repeats an idea already surfaced, the source is
     appended, evidence rises, and it may be resurfaced once with the
     `Resurfaced:` line (rule e, below) stating what's new. Recurrence
     across videos is a signal of importance. Before resurfacing, read
     the ledger row's `Response` column if one is present — a `building`
     row can carry an intended response, an `addressed` row a confirmed
     one (signal 4, below). If the Response already covers the new
     angle, the theme is not genuinely new — don't resurface. If the new
     evidence falls outside what the Response describes, resurfacing is
     still warranted and the `Resurfaced:` line should say what the
     existing Response missed. This is the check that would have kept
     ADV-004 from resurfacing unaddressed.
   - **Already acted on — never again.** Before selecting, mark an idea
     `status: adopted` and exclude it forever when any of these is true:
     (1) the ledger row is `building` or `declined` from Charles's reply;
     (2) a Project State plan or decision cites the idea's ADV ID (search
     `plans.provenance/tags` and `decisions.provenance/tags` for
     `ADV-NNN`); (3) the change the idea describes is already present in
     the live component it names (check the component before writing
     "What you have/do" — if the answer is "you already do this", the
     idea is adopted, not sent); (4) the ledger row is `addressed` — the
     authoritative, work-confirmed signal (the Build Chat that landed the
     brief wrote the actual Response, not an inference from `building`)
     and is never resurfaced, full stop. Adopted ideas can still gain
     sources in the pool for the record, but never leave it.
   - **Merge:** before adding a candidate, compare `topic_key` and title
     against pooled/held/surfaced/adopted ideas; if it is the same idea
     from a new video, append to `sources` and re-score (evidence rises)
     instead of adding a row.
   - **Decay/archive:** every run, each pooled idea not selected:
     `runs_below_threshold += 1` if `total < 60`, and `total -= 5` (floor
     0) unless new evidence arrived this run. When an idea has been below
     60 for 14 days since `first_seen` (or 6 consecutive runs, whichever
     first) → move to `archive` with `archive_reason: "below threshold
     14d"`. Archived ideas revive (back to `ideas`, decay reset) only if a
     new source matches them.
   - Ideas from Charles's own records (no video) still enter the pool and
     follow the same rubric; they cannot be high-conviction on records
     alone.
   - **Sources as scored source data.** `pool.json`'s `videos` section is
     renamed `sources`: one record per video or article ever read —
     `{kind, id, channel_or_feed, title, url, first_read, ideas_pooled,
     ideas_surfaced, ideas_adopted, source_score, tier}`, where `kind` is
     `video` or `article`, `id` is the `video_id` or `article_id`, and
     `channel_or_feed` is the YouTube channel name or the RSS/Atom
     source's name (from `feeds.json`). Existing `videos` rows are valid
     unchanged under the new shape (read as `kind: video`, `id:
     video_id`, `channel_or_feed: channel`) — no backfill or rewrite of
     rows already on disk is required. `source_score` = 10 ×
     ideas_surfaced + 25 × ideas_adopted + 2 × ideas_pooled, minus 3 per
     run it has contributed nothing new (floor 0). Tiers: `active`
     (≥ 20), `low` (5–19), `dormant` (< 5). Nothing is ever deleted — a
     dormant source still counts as a matching source for the
     theme-recurrence rule and can climb back. Tier only affects effort:
     re-read `active` sources when looking for corroboration; skip
     `dormant` ones. Write per-channel/per-feed rollups (mean
     `source_score`) to `meta.channel_scores` for the advisor's own use —
     not emailed.
   - Selected ideas are written back to `pool.json` immediately: assign
     `adv_id` (next unused `ADV-NNN`), set `status: surfaced`; the runner-up
     high-conviction idea(s), if any, get `status: held`. This write
     happens before step 6 (DELIVER) renders the brief.
   - Never pad. Zero ideas is a legal brief ("nothing met the bar; graph
     volume still low") — expected in the early weeks while channels fill.
5. ASK IF UNSURE. If the purpose of a current build can't be stated
   confidently in one sentence, add a "Questions for Charles" section —
   max 3, closed choices with a recommendation each. Never block on them.
6. DELIVER, five writes:
   a. Commit brief → cbrain docs/advisor/ADV-YYYY-MM-DD.md (read back to
      verify, per write-before-done).
   b. Update LEDGER.md with the new ideas (status: surfaced), filling the
      `Brief` column with the git path of this run's ADV file and the
      `Pool` column with each idea's `pool_id` (`P-NNNN`) — the `Brief`
      column is how a DA chat resolves an ADV ID to its block, the `Pool`
      column is how it resolves to the idea's full scoring history in
      `pool.json`.
   c. Gmail send to Charles — subject "Stack Advisor brief ADV-YYYY-MM-DD",
      full brief in the body, git path at the bottom.
   d. Project State note on stack-map: one-paragraph digest + git path.
   e. Supabase copy for the cbrain-ui Stack screen (project
      `lpeswznkxzeeyiqaewma`). This is the same data as a–b, stored as
      rows so the screen can read it directly instead of parsing git.
      Git stays the record; these rows copy it.
      - Upsert one `advisor_runs` row keyed on `run_id` = this run's ADV
        file name without `.md` (e.g. `ADV-2026-09-16`): `run_date`;
        `preamble` = the brief's opening paragraphs (everything before
        the first idea block); `sources_read` = JSON list of the sources
        read in 3b, each `{kind, id, channel_or_feed, title, url}`;
        `queue_depth` = sources still waiting for intake after this
        run's 12-item cap (0 if none); `graph_answered` = true if any
        step 3 query came back with a grounded answer, false if the
        graph didn't know; `questions` = JSON list of this brief's
        "Questions for Charles" (empty list if none); `brief_path` = the
        git path from 6a.
      - Upsert one `advisor_ideas` row per idea in this brief, keyed on
        `adv_id`: `title` = the ledger `Idea` text; `plain_title` = the
        heading's plain title (rule 6, 10 words or fewer, no bare
        codes, no outside company/product names); `body` = JSON of the
        block exactly as written in 6a — `{from_source, what_you_have,
        why_the_connection, what_gets_better, confidence,
        resurfaced_note}` plus a new `in_plain_terms` key holding the
        "In plain terms:" sentence ("What your records show" also goes
        in `from_source` for own-records ideas; `resurfaced_note` is
        null unless rule e applies); `effort` = S/M/L; `high_conviction`;
        `component_ids` = the stack-map component ids the idea connects
        to, from the pool entry's `connects_to` (for a plan or decision,
        the component it is about; write an id even if the map doesn't
        list it yet — the screen shows it as Unmapped); `source` =
        `{kind, name, title, url}` from the block heading (`kind:
        records`, `name` = the display IDs, `url` null for own-records
        ideas); `first_seen`; `status` and `response` = the ledger's
        Status and Response; `brief_ref` = the ledger `Brief` cell;
        `pool_ref` = the ledger `Pool` cell. A new idea gets
        `first_run_id` = `latest_run_id` = this run and
        `resurface_count` 0. A resurfaced idea keeps `first_run_id`,
        sets `latest_run_id` to this run, and adds 1 to
        `resurface_count`.
      - Then sync every other ledger row that already has an
        `advisor_ideas` row: touch **only** `status` and `response`.
        Never rewrite `title`, `plain_title` or `body` for an idea that
        isn't in this run's brief. Only a ledger row with **no**
        `advisor_ideas` row yet is built fresh from its `Brief` file —
        and written straight to this run's standard (rule 1a, "Writing
        for Charles") as it's created. This brings step 1's changes,
        and the DA/Build chats' flips to `building`/`addressed`, onto
        the screen. The advisor is the only writer of
        `advisor_ideas.status`; the app never sets it.
      - Read back with a SELECT: the run row, plus a count of this run's
        idea rows. If this write fails, a–d still stand. Name the error
        in the 6d note; the next run's sync repairs the gap.

## Brief format

```
### ADV-NNN · {plain title, rule 6}
Source: {who they are, in a few words} — "{video or article title}" · {url}

**In plain terms:** {one sentence}

**What they found**
{2–4 sentences}

**What you have today**
{2–3 sentences: the component, process, or convention in Charles's stack this compares to, named by what it does, never a bare code (rules 2 and 4). If nothing comparable exists: "You don't have this today." plus one sentence on the closest thing.}

**Why it matters here**
{2–3 sentences: why the advisor is pulling this out and tying it to that component — the link must be concrete, not thematic}

**What you'd gain**
{2–3 sentences: how Charles's day or stack improves if this is added or changed — plus "Effort: small | medium | large"}

{Checked | Assumed} — {one line}
```

Every idea in the email and the committed ADV file renders exactly like
this, in this order, nothing else between blocks.

Rules:
a. The heading line carries the ADV ID first, always.
b. When the evidence is Charles's own records rather than a video or
   article, the heading reads `### ADV-NNN · your own records —
   {display IDs}` with no URL line, and the first header reads **What
   your records show** (instead of "What they found").
c. To write *What they found* the advisor fetches the source file itself
   — `world-graph/data/transcripts/{video_id}.md` (video id from the
   URL's `v=` parameter) for a video, or
   `world-graph/data/articles/{article_id}.md` (article id: the first 12
   hex characters of SHA-256 of the canonical URL, matching
   `pipeline/article_store.py`'s `compute_article_id()`) for an article
   — via Custom GitHub MCP `get_file_contents`, and grounds the blurb in
   it; if the source file can't be read, the idea is dropped, not
   guessed.
d. One block per idea — the same video or article may appear twice with
   two different ADV IDs.
e. Resurfaced ideas keep their original ID and add a `Raised again
   because: {what changed}` line under Confidence.

## Writing for Charles
Charles is not technical and reads these cold, often days later. Every
sentence must make sense to a smart person who has never seen this
system's files.

1. **Lead with one plain sentence.** Every idea opens with "In plain
   terms:" — what to change and what Charles gets.
2. **No bare codes.** Record codes (D6, CB-138, SM-027, P-0010, BB-…)
   never stand alone. Say what the thing is first; the code can follow
   in parentheses.
3. **Introduce every outside source.** Who they are in a few words, the
   first time: "Y Combinator's in-house engineering team," not "YC's QM
   team."
4. **Name parts of the system by what they do.** "The step that pulls
   facts out of videos (intake-extractors)."
5. **No jargon without a translation.** If a word wouldn't come up in a
   construction-firm meeting, replace it with what it does. Always
   translate: harness, zero-trust, event log, object storage,
   cell-level security, access tier, caller, context window, rubric,
   hook, trace, observability, orchestrator, idempotent, saga, and "the
   X pattern."
6. **Titles:** 10 words max, no record codes, no outside company or
   product names, say the change. (Charles's own system names — cbrain,
   Stack screen — are fine.)
7. **Short opening.** At most three sentences: how many ideas, and
   whether anything needs an answer. Run mechanics (what was read,
   queries sent, reply checks, queue counts) go in a short "How this run
   worked" section at the bottom of the brief.
8. **Reread as Charles before sending.** A sentence that needs a
   glossary gets rewritten, not footnoted.

## Changelog
- **v1.0.0** (2026-08-28) — Initial ship: finalized from the BB-2026-08-27-stack-advisor
  design draft (frontmatter set to active, changelog added). Per
  BB-2026-08-27-stack-advisor.
- **v1.1.0** (2026-09-02) — Per-video block format with source attribution
  (channel/title/URL) replacing the flat "Each idea" list; adds rules a–e
  covering own-records headings, transcript grounding for "From the video",
  one-block-per-idea, and resurfaced-idea marking. Per
  BB-2026-09-02-advisor-source-attribution.
- **v1.1.1** (2026-09-02) — Step 6b now names the LEDGER `Brief` column
  explicitly (review-gate fix; the column itself shipped in v1.1.0's build).
- **v1.2.0** (2026-09-03) — Adds discernment: a hidden ranked idea pool
  (`cbrain/docs/advisor/pool.json`) fed by every new transcript. New step
  3b (INTAKE NEW VIDEOS) reads `world-graph/data/ingest_log.json` and pools
  0–3 grounded candidates per new transcript. Step 4 (GENERATE) replaced
  with SCORE AND SELECT: 0–100 rubric (connection/evidence/payoff/
  timeliness), threshold 60, high-conviction 85 + two independent sources
  (exactly one per brief, runner-up held), cap 6 ideas as a ceiling never a
  target, slow-day look-back into the pool, same-video suppression,
  adopted-idea suppression (ledger status · Project State ADV-ID search ·
  already-present check), merge of repeat ideas by `topic_key`, decay 5/run
  and archive after 14 days or 6 runs (revive on new source), and a
  `videos` section scoring every transcript ever read as source data
  (never deleted, tiered by contribution). Step 6b now also fills the
  LEDGER `Pool` column. Per BB-2026-09-03-advisor-idea-pool.
- **v1.2.1** (2026-09-04) — Suppression signal (4) added: a ledger row of
  `addressed` is the authoritative, work-confirmed adoption signal
  (written by the Build Chat that landed the brief, not inferred from
  `building`) and is never resurfaced. The same-theme resurface check now
  reads the ledger row's `Response` column before resurfacing — if the
  Response already covers the new angle, don't resurface; if it doesn't,
  the `Resurfaced:` line says what the Response missed. Closes the gap
  where all suppression signals were inferred rather than confirmed by
  the work (ADV-004 resurfaced twice while still `surfaced`, no readable
  response). Per BB-2026-09-04-advisor-response-loop.
- **v1.3.0** (2026-09-13) — Generalizes intake from videos-only to videos
  + RSS/Atom articles, matching world-graph's new article-persistence
  parity (BB-2026-09-13-feed-parity-with-transcripts). Step 3b (renamed
  INTAKE NEW SOURCES) now also reads
  `world-graph/data/article_ingest_log.json` and
  `world-graph/data/articles/{article_id}.md`, advancing
  `meta.last_intake_at` across both logs and capping at 12 items/run
  combined across videos and articles (not 12 each). `pool.json`'s
  `videos` section is renamed `sources` and gains a `kind: video |
  article` field plus a generalized `channel_or_feed` label — existing
  rows are valid unchanged under the new shape, no backfill required.
  "From the video" is renamed "From the source" throughout the brief
  format (rule b likewise); rule c gains
  `world-graph/data/articles/{article_id}.md` as a second grounding
  location alongside the transcript path. Per
  BB-2026-09-13-feed-parity-with-transcripts.
- **v1.4.0** (2026-09-16) — Closes the feedback loop through the new
  cbrain-ui Stack screen (CB-291). Step 1 (FEEDBACK FIRST) gains a second
  source alongside the Gmail reply (a union, not a replacement — the step
  still works when either is empty): unconsumed `advisor_dispositions`
  rows on `lpeswznkxzeeyiqaewma` are folded into LEDGER.md as an email
  reply would be. `interested` → `interested`; `declined` → `declined`,
  with the note written to `Response` as "declining because {note}";
  `scoping` → `interested`, with "scope requested" added to the `Idea`
  cell, because `building` stays the DA chat's flip at scoping. The
  latest answer wins; `addressed` rows are never changed, and `building`
  rows are never moved back. Each row gets `consumed_at` only after the
  ledger commit reads back. Step 6 (DELIVER) goes from four writes to
  five: new 6e upserts this run's `advisor_runs` row and its
  `advisor_ideas` rows (body sections, effort, conviction,
  `component_ids` from `connects_to`, source, status/response,
  brief/pool refs, run ids and resurface count), then syncs any ledger
  row that is missing or out of date, so the screen reads rows instead
  of parsing git. Git stays the record, and a failed 6e never blocks
  6a–d. Per BB-2026-09-16-stack-screen.
- **v1.5.0** (2026-09-16) — Replaces the one-line `## Language` rule with
  "Writing for Charles": eight concrete rules (plain-terms opener, no
  bare codes, introduce outside sources, name system parts by function,
  translate jargon, 10-word titles, short opening with run mechanics
  moved to a footer, reread-as-Charles). The brief format is rewritten
  to match (What they found / What you have today / Why it matters here
  / What you'd gain / Checked-or-Assumed, own-records variant "What your
  records show", `Raised again because:` replacing `Resurfaced:`). Step
  6e's `advisor_ideas` write adds `in_plain_terms` and tightens the sync
  bullet so a run never rewrites `title`/`plain_title`/`body` for an
  idea not in that run's own brief — only touches `status`/`response` on
  existing rows, building missing rows fresh. Per
  BB-2026-09-16-stack-plain-language (Build 11.1).
