# Stack Advisor — changelog

Moved out of SKILL.md by BB-2026-10-05-advisor-reads-smarter (Build 28).
Newest last.

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
- **v1.5.1** (2026-09-17) — Closes three doctrine references the v1.5.0
  plain-language rewrite left pointing at old wording. Step 4's
  same-theme-new-video bullet now names the `Raised again because:`
  line instead of the retired `Resurfaced:` line. The already-acted-on
  check (signal 3) now checks the component before writing "What you
  have today" instead of the retired "What you have/do" header. Rule b
  (own-records evidence) now matches the current heading shape: the
  heading is still `### ADV-NNN · {plain title, rule 6}`, followed by a
  `Source: your own records — {what the records are, in plain words,
  with codes in parentheses}` line with no URL, and the first header
  still reads **What your records show**. Per
  BB-2026-09-17-stack-plain-language-fixes.
- **v1.5.2** (2026-09-19) — Step 1b: when the winning Stack-screen
  answer for an idea is `declined` and the run folds more than one
  `declined` row for it, `Response` joins every note, oldest first,
  separated by " / ", instead of keeping only the latest. Prompted by
  ADV-020, passed twice on 2026-09-19 — first with the reason, then
  with a follow-up ("Can you remove this to an archive state?") that
  "latest wins" would otherwise have recorded as the reason. Status
  folding is unchanged (latest still wins). Companion to cbrain-ui
  Build 11.5, which now takes passed ideas off the Stack map as soon
  as they are saved. Per BB-2026-09-19-stack-passed-off-map.
- **v1.6.0** (2026-09-20) — The advisor reads an explicit source list:
  videos from the channels in yt-relay/channels.json (phone-shared
  videos from other channels are no longer read) and articles only
  from feeds.json entries marked "stack_advisor": true. Articles are
  read as soon as they are saved (queued or ingested), and "new" means
  "not yet in pool.json sources," so the backlog stranded at "queued"
  since 09-13 is caught up. Per BB-2026-09-20-advisor-sources.
- **v1.7.0** (2026-10-02) — The email becomes a short, formatted quick
  hit; the full brief stays in the ADV file and on the Stack screen.
  New "## Email format" section: sent as HTML (`htmlBody`, plain-text
  `body` fallback) in a fixed 640px column; idea heading 20px and
  section headings 16px, both bold and underlined; each section cut to
  one sentence; "In plain terms" dropped from the email only; one small
  Effort/Checked/Assumed line; a per-idea link to the Stack screen
  (`?sel=advisor:ADV-NNN`, base URL held in one line for go-live). "How
  this run worked" and the git path no longer go in the email (rule 7;
  they stay in the ADV file). Rule 6: titles now start with a verb and
  state the move directly. Step 6c updated to match. Root cause of the
  wide, unstyled emails: they were sent as plain text with no width or
  formatting. Designed and approved by Charles in a DA chat 2026-10-02
  after a sample email in this format; edited inline, no Build Brief.
- **v1.8.0** (2026-10-02) — Step 1b folds the new `done` answer (Stack
  screen Done button) to `addressed`, with `Response` "done another way
  — marked Done on the Stack screen YYYY-MM-DD" (plus the note, if any).
  Done may move a `building` row forward (keeping the prior intended
  response after " / was: ") and names any open Build Brief for that
  ADV ID in the brief's opening paragraph; the advisor never touches
  plans. Per BB-2026-10-02-stack-done-and-idea-format.
- **v1.8.1** (2026-10-06) — Job boundary gains "The brief is the only
  email": a failed run never emails Charles; it stops and leaves the 6d
  note if it can. The Stack Advisor dot's existing output check turns
  it late, and the Stack Repairer covers it in its evening recap. The
  brief email itself is unchanged. Per BB-2026-10-05-stack-repairer
  (Build 27).
- **v1.9.0** (2026-10-06) — Reads smarter. A nightly no-AI script
  (`cbrain/tools/advisor/run_packet.py`, workflow `advisor-packet.yml`,
  08:47 UTC) does the pool bookkeeping and hands the advisor one small
  file, `docs/advisor/run_packet.json` (≤ 40 KB): up to 20 live ideas, a
  one-line index of the rest, ledger statuses, and every waiting item
  with an excerpt (start/middle/end slices for items over 10 KB;
  speechless videos marked `title_only`; feeds marked `"digest": true` —
  gbrain releases, Claude Platform Release Notes — collapsed to one item
  per run). ORIENT reads the packet instead of `pool.json` and
  `LEDGER.md`, which the advisor never opens whole again. Intake becomes
  skim-then-deep-read: skim up to 30 items, rate high/medium/low,
  deep-read the top ~6 in full (low = done, medium = eligible once more),
  with an auto-caption caution on names. The 12-item cap is retired.
  Judgments (feedback, skim verdicts, candidates, re-scores, adoptions,
  surfaced and held ideas) go to `docs/advisor/run_result.json`; the
  script folds them into the pool and the ledger (ledger rules of step
  1b, decay, archive, merge by `topic_key`, source scores) on push.
  Dispositions are consumed after run_result.json reads back. Brief
  format + Writing for Charles, email format, the Supabase copy (6e) and
  this changelog moved to `references/` (read at DELIVER); core skill
  under 12 KB. Per BB-2026-10-05-advisor-reads-smarter (Build 28).
- **v2.0.0** (2026-10-06) — Thinks bigger (BB-2026-10-05-advisor-thinks-bigger,
  Build 28.1). ORIENT reads exactly three files — `stack-briefing.md` (one
  line per part + "Where Charles is headed" from the harness map), the
  day's section file (Mon intake, Wed build-machine, Fri app; written
  nightly by `tools/advisor/stack_briefing.py`) and `run_packet.json` — and
  no longer the Master Roadmap, Build Map Skeleton or full stack map; the
  shelf query moves into Fix scoring. Skim ratings and graph questions aim
  at the day's section. Two lanes: Fix (the old rubric, 60) and Frontier
  (capability 40, recency 20, evidence 25, plug-in point 15; threshold 65;
  one slot; harness step/block ids allowed in `connects_to`; a one-line
  reason when none clears). Every idea adds "What's wrong today" and "Why
  this might be wrong". New Contract and Anti-patterns sections (gbrain
  precedent). DELIVER gains the hand-off switch: when
  `cbrain/docs/advisor/critic_live.json` exists the Advisor stops at a
  draft (`docs/advisor/drafts/`, run_result `stage: draft`, no email) and
  the Advisor Critic (`roles/advisor-critic`) judges, publishes and sends.
