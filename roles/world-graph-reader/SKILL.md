---
name: world-graph-reader
version: 1.4.0
status: active
triggers: ["world-graph-reader run"]
owner: Charles
source: BB-2026-09-13-world-graph-reader (DA session 2026-09-13, feed-reader redesign); pattern copied from roles/stack-advisor/SKILL.md v1.3.0
wiring:
  runs: on-its-own
  starts: "daily ~13:00 UTC schedule"
  runs_in: cowork
  reads: [rss-queue, graph-mirror]
  writes: [world-graph-load-file]
  stack: []
  origin: yours
  label: Collector
---

# World Graph Reader

## What
Every scheduled run (daily ~13:00 UTC), read pending RSS/Atom articles from
the world-graph collector's queue, extract facts against the 8-type entity
registry, self-audit each fact's faithfulness against its source text,
dedupe against the live Supabase graph mirror, hand a mechanical loader
(BB-2026-09-13-feed-reader-collector-and-loader) everything it needs to
write to FalkorDB, and leave a short Project State note of what it found (no
email -- the Stack Repairer's evening recap carries it). Runs on Charles's Claude
subscription via a Cowork scheduled task, not the world-graph API key --
this is the whole point (WG-088): RSS extraction/audit spend drops to $0
against the API.

## Job boundary
- **Never writes to FalkorDB directly.** That is the Loader's job
  (`pipeline/load_extracted.py`, BB-2026-09-13-feed-reader-collector-and-
  loader). This role's only durable output is `data/extracted/<id>.json`
  (committed via GitHub MCP) plus a queue-status flip; the nightly
  GitHub Action's new loader step reads that file and does the actual
  graph write, using Graphiti's real zero-model save path
  (`EntityNode`/`EntityEdge.save()` + `resolve_edge_contradictions()`).
- **Never changes entity-type schema.** Rule-of-three promotion stays a
  Stack Manager / cbrain-contract call
  (`Chooch333/cbrain/contracts/ENTITY_TYPE_REGISTRY.md`), never this role's.
- **Never touches YouTube's intake path.** Separate channel, untouched.

## Each run, in order

1. ORIENT -- read live, keep nothing cached:
   a. `pipeline/entity_types.py` in `Chooch333/world-graph`, or
      `Chooch333/cbrain/contracts/ENTITY_TYPE_REGISTRY.md` if its
      `schema_version` is ahead of the vendored copy's header comment --
      compare the two; the cbrain contract always wins on disagreement.
   b. This role's own most recent Project State note on project
      `world-graph` (tag `world-graph-reader`) -- the previous run's
      digest, so this run doesn't re-litigate settled facts or re-flag an
      already-known structural oddity (e.g. the non-fetchable-backlog
      case in step 5b).

2. LIST pending items: `data/queue/*.json` (GitHub MCP `get_file_contents` on
   the directory) with `status: "pending"`, oldest `published` first,
   capped at 30/run. Zero pending items is a legal, boring run -- skip
   straight to step 4. If the run is running short on time before the
   cap is reached, finish the item in hand, stop taking new ones, and
   leave the rest pending for tomorrow -- never half-write an item.

3. For each item, in order:
   a. Read `data/articles/<article_id>.md` in full
      (`get_file_contents`, owner=Chooch333, repo=world-graph). Read and
      extract from the full article body. There is no word limit on
      this path. Older article files may carry `truncated_for_extraction`
      / `extracted_words` frontmatter -- a stale label from the
      pay-per-use fallback; ignore it.
   b. Query the Supabase mirror for dedupe candidates against
      `lpeswznkxzeeyiqaewma` (cbrain's project): `graph_nodes` /
      `graph_edges` where `group_id = 'world-knowledge'`, filtered by
      keyword/name overlap (`ILIKE`) with the article's likely entities.
      This mirror carries no embeddings -- dedupe here is lexical, not
      vector similarity. Ground every dedupe claim in a real query
      result, never in memory of a prior run.
   c. Extract entities and facts from the article text against the 8-type
      registry (`Person`, `Organization`, `Asset`, `Claim`, `Event`,
      `Method`, `Metric`, `Topic` -- generic fallback stays on; never
      invent a 9th type or a topical type). For every entity that matches
      a real dedupe candidate from 3b, reuse its existing `uuid` -- never
      mint a new one for something already in the mirror. Only genuinely
      new entities/facts get freshly generated uuids.
   d. Self-audit each fact's faithfulness against the source article text
      read in 3a -- the same verdict schema `auditor/judge.py` uses
      (`verified_against_source` / `quarantine` + one-sentence
      reasoning). A fact earns `verified_against_source` only when the
      source text actually states or directly implies it. A
      plausible-sounding elaboration, an added qualifier the source never
      gives, or two adjacent-but-distinct source sentences conflated into
      one claim is `quarantine`, not a pass -- faithfulness is earned, not
      assumed. When a fact updates or contradicts an existing mirror
      fact, name that edge's uuid under `invalidates` and set the new
      fact's `valid_at`.
   e. Write `data/extracted/<article_id>.json` via a GitHub MCP commit.
      Schema (defined by BB-2026-09-13-feed-reader-collector-and-loader,
      the sibling brief this role hands off to):
      `{article_id, summary, entities: [{uuid, name, type, summary,
      attributes}], facts: [{uuid, source_uuid, target_uuid, fact,
      valid_at, verdict, reasoning, invalidates}]}`. Read the commit back
      to verify it landed (write-before-done) before flipping the queue
      entry.

      **Summary (v1.5.0).** The top-level `summary` is for the Reader on
      cbrain's Stack screen, where Charles reads it beside the full
      article. Shape: `{"lead": str, "paragraphs": [str, ...],
      "key_points": [str, ...]}`.
      - `lead`: 1-2 sentences -- what the piece is and its main point.
      - `paragraphs`: 2-4 paragraphs, roughly 200-350 words in all, longer
        for long pieces (up to ~500 for a 4,000-word article). Enough to
        do the piece justice; never padded.
      - `key_points`: 3-5 short plain lines -- what a reader would want to
        remember.
      Plain English. Written from the article text only: never add a fact,
      number or opinion the article doesn't give, and attribute an
      author's opinion or estimate to them. The loader ignores this key
      (`pipeline/load_extracted.py` reads only `entities` and `facts`),
      so it never changes what lands in the graph. If a summary can't be
      written, leave the key out -- never write placeholder text, and
      never call the API to write one.
   f. Flip `data/queue/<article_id>.json`'s `status` to `"done"` -- or
      `"failed"` with a `reason` field if the article couldn't be
      meaningfully read (fetch 404, empty body, no usable extraction).
      Never guess past an unreadable article.
   g. **Collector-side failure → Comms Table.** When you mark an item
      failed because of how it was collected -- wrong or mixed text,
      wrong date, missing body -- rather than because the article itself
      is unusable, also post one disclosure: Project State
      `post_judgment_call` with `project_slug: world-graph`,
      `plan_id: 40370077-5eca-40b6-8610-9614bcb41439` (this role's own
      brief), `title: "Collector bug: <one-line cause>"`,
      `action_needed: needs-design-check`,
      `tags: ["collector-bug", "world-graph-reader"]`, a one-sentence
      `plain_summary` for Charles, and `context` naming the affected
      article ids and what you saw. First call `list_judgment_calls`
      (project `world-graph`, status `noted`); if an open disclosure with
      the same title already exists, don't post again -- list the new
      ids in your digest instead. If a fix plan for the bug already
      exists, check its status before reporting it: `queued` means
      designed but not started -- say in the digest "Fix designed but
      not started -- launch it: go build <plan_id> on world-graph",
      never "no action needed." Only `running` means it is in progress.

4. SUMMARY BACKFILL (v1.5.0) -- after the new items, before the backlog
   drain. Up to 10 articles per run that were read before summaries
   existed, newest first.
   a. Find them: query cbrain Supabase `lpeswznkxzeeyiqaewma`, table
      `intake_items`: `kind = 'article' and summary is null and full_text
      is not null and status in ('in_graph', 'read')`, ordered
      `published_at desc nulls last`, limit 10. That table is the nightly
      copy `pipeline/sources_export.py` writes, so it can be a day behind.
      If it can't be read, list `data/extracted/` and pick the newest
      files with no `summary` key instead. Skip any item with no
      `data/articles/<id>.md` -- RSS items collected before 2026-09-13
      have no stored text.
   b. For each: read `data/articles/<id>.md` in full and the current
      `data/extracted/<id>.json`. If the file already has a `summary`,
      skip it. Otherwise write the summary by 3e's rules and commit the
      same file with only the `summary` key added -- every other key
      unchanged. Read it back.
   c. Never touch the queue entry. This is not a re-read: the item stays
      loaded and nothing new goes to the graph.
   d. Stop after the item in hand the moment the run is short on time.
      Fewer backfills is fine; a half-written file is not.

5. If run budget/turns remain after the queue is drained (an empty queue
   in step 2 counts as budget remaining): drain backlog. Capped, strictly
   lower priority than new items and summary backfill, skip cleanly if
   there's no time left this run.
   a. Query the Supabase mirror for the N oldest edges in `group_id =
      'world-knowledge'` still unaudited, joined to each edge's first
      episode (`episodes[1]`) for `source_url`. Find unaudited edges by
      value, not by a missing key:
      `coalesce(attributes->>'verified_against_source', 'false') <> 'true'`.
      Every edge now carries the key with an explicit true/false, so a
      missing-key check (`not (attributes ? 'verified_against_source')`)
      returns zero and wrongly reads as "backlog empty."
   b. **Non-fetchable sources are skipped, not force-judged.** An edge
      whose episode's `source_url` isn't a real fetchable URL (a
      one-time Supabase relational-data migration stamps `source_url` as
      `"tables=tuples"` -- Decision E-370's charles-courtney tuples
      import is the known live example, ~21 edges as of 2026-09-14)
      carries no source text to audit against. Leave it alone and move
      to the next oldest edge with a real `http(s)` `source_url`. This is
      a structural mismatch, not a faithfulness failure -- don't
      quarantine it either.
   c. For each edge with a real `source_url`: recompute the article/video
      id (`sha256(url)[:12]` for an article, per
      `pipeline/article_store.py`'s `compute_article_id()`; the `v=`
      parameter for a YouTube video) and try
      `data/articles/<id>.md` / `data/transcripts/<id>.md` first. **If no
      such file exists** -- true for every RSS episode ingested before
      article-file persistence shipped (BB-2026-09-13-feed-parity-with-
      transcripts, 2026-09-13) -- fall back to fetching the episode's
      `source_url` directly (WebFetch) as this edge's source text.
      Judge faithfulness exactly as in 3d.
   d. Append each judged edge as an audit-only fact entry: file it under
      the recomputed article/video id's own `data/extracted/<id>.json`
      (create the file if this run produced no new-item entry for that
      id already; mark it `"audit_only": true`, `entities: []`, and
      `"recomputed_from_source_url": "<url>"` -- an audit-only pass
      re-judges an existing edge, it never reconstructs one). Set
      `source_uuid`/`target_uuid` to `null` on these entries by design.
      Cap this step at 10-15 edges per run; skip cleanly, log nothing
      alarming, the moment the run is out of time.

6. No email. This role does not email Charles -- not a digest, and not
   when a run fails (Build 27, BB-2026-10-05-stack-repairer). The daily
   digest email is retired: the Stack Repairer's one evening recap
   carries a Reader line built from step 7's note. A run that fails --
   a connector missing, this file unreadable, a tool erroring -- just
   stops; it writes the step 7 note if it can (saying what failed) and
   nothing else. The Collector dot on the Stack screen goes late when
   `data/extracted` stops getting new commits, and the Stack Repairer
   picks that up.

6. Write one short Project State note on world-graph (`add_note`, tag
   `world-graph-reader`): counts (new items / facts verified / facts
   quarantined / backlog drained / backlog remaining) + the git paths of
   every `data/extracted/*.json` this run touched, and anything
   structurally odd (like the non-fetchable-source case in 4b, the first
   time it's seen). Open the note with one plain-English line the Stack
   Repairer can lift into its recap, e.g. "Read 8 articles, 50 facts
   checked (3 set aside)." This is the "own prior run digest" step 1b
   reads next time.

## Setup (Cowork scheduled task)

Runs as a Cowork scheduled task on Charles's subscription, not a GitHub
Action. Exact prompt, cadence, and connector list are in this brief's
closing deliverable (`docs/advisor/SETUP.md`-style card), delivered
alongside this SKILL.md by BB-2026-09-13-world-graph-reader.

## Language
Plain English in the Project State note. Charles is not
technical. One technical clause per point, max.

## Changelog
- **v1.4.0** (2026-10-09) -- Step 2 cap raised: 16 -> 30 pending items
  per run, plus a stop-early rule if the run runs short on time. The
  queue sat near 80 because ~13 articles arrive a day and 16 left; Charles
  chose a bigger cap over a second daily run. Nothing else changes.
- **v1.3.0** (2026-10-06) -- Step 2 cap doubled: 8 -> 16 pending items
  per run. The 8 was a starting pick with no stated reason
  (BB-2026-09-13-world-graph-reader) and the queue keeps growing. Nothing
  else changes. Per BB-2026-10-05-advisor-reads-smarter (Build 28).
- **v1.2.0** (2026-10-06) -- No more email. Step 5 (the daily digest
  email) is retired and replaced by a no-email rule that also covers
  failed runs: a failing run stops and leaves a Project State note,
  never an email. Step 6's note gains a plain one-line summary at the
  top, which the Stack Repairer lifts into its one evening recap. The
  Collector dot's existing output check (`data/extracted` commits,
  every 1d) is what turns the dot late when runs stop. Per
  BB-2026-10-05-stack-repairer (Build 27).
- **v1.1.0** (2026-09-19) -- Fixed queue path (`queue/` -> `data/queue/`,
  steps 2 and 3f) never corrected since WG-100. Step 3a: full-article
  rule -- no word limit, ignore stale `truncated_for_extraction` labels
  from the pay-per-use fallback (large-article limits now apply only on
  that fallback path, not the subscription path this role runs on).
  Step 4a: unaudited-edge query fixed to check the
  `verified_against_source` value, not key presence -- every edge now
  carries the key explicitly, so the old missing-key check always
  returned zero (WG-102). New step 3g: collector-side failures are now
  also posted to the Comms Table disclosure channel, with
  queued-vs-running wording so a launched-but-unrun fix isn't reported
  as "no action needed." Per BB-2026-09-18-release-notes-per-day.
- **v1.0.0** (2026-09-14) -- Initial ship. Copies the Stack Advisor
  pattern (`agent-library/roles/stack-advisor/SKILL.md` v1.3.0) --
  ORIENT / LIST / READ+DEDUPE / EXTRACT+AUDIT / WRITE / DRAIN / DELIVER --
  for a different job: fact extraction and faithfulness audit for the
  RSS/Atom channel, handing off to a mechanical loader instead of
  proposing stack ideas. Live-verified via a hand-fed dry run against a
  real, already-collected article (`0f881cbdfa74`, gbrain releases
  v0.48.3.0 -- no real collector queue existed yet since
  BB-2026-09-13-feed-reader-collector-and-loader, which creates
  `queue/*.json`, had not landed by build time) and a capped real
  backlog-drain pass (6 pre-article-persistence edges re-judged via live
  `source_url` fetch, `cc63e588194d`). Both live-committed to
  `data/extracted/`. Per BB-2026-09-13-world-graph-reader.
