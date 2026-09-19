---
name: world-graph-reader
version: 1.1.0
status: active
triggers: ["world-graph-reader run"]
owner: Charles
source: BB-2026-09-13-world-graph-reader (DA session 2026-09-13, feed-reader redesign); pattern copied from roles/stack-advisor/SKILL.md v1.3.0
---

# World Graph Reader

## What
Every scheduled run (daily ~13:00 UTC), read pending RSS/Atom articles from
the world-graph collector's queue, extract facts against the 8-type entity
registry, self-audit each fact's faithfulness against its source text,
dedupe against the live Supabase graph mirror, hand a mechanical loader
(BB-2026-09-13-feed-reader-collector-and-loader) everything it needs to
write to FalkorDB, and tell Charles what it found. Runs on Charles's Claude
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
      case in step 4b).

2. LIST pending items: `data/queue/*.json` (GitHub MCP `get_file_contents` on
   the directory) with `status: "pending"`, oldest `published` first,
   capped at 8/run. Zero pending items is a legal, boring run -- skip
   straight to step 4.

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
      `{article_id, entities: [{uuid, name, type, summary, attributes}],
      facts: [{uuid, source_uuid, target_uuid, fact, valid_at, verdict,
      reasoning, invalidates}]}`. Read the commit back to verify it
      landed (write-before-done) before flipping the queue entry.
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

4. If run budget/turns remain after the queue is drained (an empty queue
   in step 2 counts as budget remaining): drain backlog. Capped, strictly
   lower priority than new items, skip cleanly if there's no time left
   this run.
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

5. Email Charles a plain-English digest of the run (Gmail MCP, subject
   `world-graph-reader digest YYYY-MM-DD`): new items processed (counts:
   extracted / facts verified / facts quarantined / failed), entities
   reused vs. newly minted, backlog drained this run + backlog remaining,
   and anything structurally odd (like the non-fetchable-source case in
   4b, the first time it's seen). Plain English, one technical clause per
   point max -- Charles is not technical.

6. Write one short Project State note on world-graph (`add_note`, tag
   `world-graph-reader`): counts (new items / facts verified / facts
   quarantined / backlog drained / backlog remaining) + the git paths of
   every `data/extracted/*.json` this run touched. This is the "own prior
   run digest" step 1b reads next time.

## Setup (Cowork scheduled task)

Runs as a Cowork scheduled task on Charles's subscription, not a GitHub
Action. Exact prompt, cadence, and connector list are in this brief's
closing deliverable (`docs/advisor/SETUP.md`-style card), delivered
alongside this SKILL.md by BB-2026-09-13-world-graph-reader.

## Language
Plain English in the digest email and Project State note. Charles is not
technical. One technical clause per point, max.

## Changelog
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
