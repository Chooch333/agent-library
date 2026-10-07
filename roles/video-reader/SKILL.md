---
name: video-reader
version: 0.1.0
status: draft
triggers: ["video-reader run"]
owner: Charles
source: BB-2026-10-06-video-reader (Build 17.1); pattern copied from roles/world-graph-reader v1.3.0
wiring:
  runs: on-its-own
  starts: "daily 11 pm Indianapolis schedule"
  runs_in: cowork
  reads: [video-queue, transcripts, graph-mirror]
  writes: [world-graph-load-file]
  stack: []
  origin: yours
  label: Video Reader
---

# Video Reader

## What
Once a day (11 pm Indianapolis), read waiting YouTube transcripts from
world-graph's video to-do list, pull out facts against the 8-type entity
registry, check each fact against its transcript, and leave them for the
nightly loader (09:17 UTC). Runs on Charles's Claude plan, never the API
key -- that is the whole point (Build 17.1).

## Job boundary
- Never writes to FalkorDB. The nightly loader (pipeline/load_extracted.py)
  does that. This role's only outputs are data/extracted_video/<video_id>.json,
  a queue-status flip, and one Project State note.
- Never changes the entity-type schema.
- Never touches the article queue (data/queue/) -- that's the Collector's.

## Each run, in order
1. ORIENT -- read live: pipeline/entity_types.py in Chooch333/world-graph
   (or Chooch333/cbrain/contracts/ENTITY_TYPE_REGISTRY.md if its
   schema_version is ahead -- the cbrain contract wins), and this role's
   own last Project State note on world-graph (tag video-reader).
2. LIST data/video_queue/*.json with status "pending". New items first
   (backlog false, oldest fetched_at first), then backlog items (oldest
   first). Cap: 10 per run. Zero pending is a legal, boring run -- go to
   step 5.
3. For each item, in order:
   a. Read data/transcripts/<video_id>.md in full. If its frontmatter has
      `guidance`, treat it as Charles's stated focus for that channel.
   b. Dedupe: query the cbrain mirror (lpeswznkxzeeyiqaewma) graph_nodes
      where group_id = 'world-knowledge', by name overlap (ILIKE) with the
      video's likely entities. Reuse a real match's uuid; ground every
      dedupe claim in a real query result. New things get fresh uuids.
   c. Extract entities and facts against the 8 types only (Person,
      Organization, Asset, Claim, Event, Method, Metric, Topic). A
      speaker's opinion or prediction is a Claim attributed to that
      speaker, never stated as fact.
   d. Self-check every fact against the transcript text:
      verified_against_source only when the transcript states or directly
      implies it; otherwise quarantine. One-sentence reasoning each. Name
      any existing edge a fact updates under `invalidates` and set
      valid_at.
   e. Write data/extracted_video/<video_id>.json via a GitHub commit, in
      the loader schema: {article_id: <video_id>, entities: [{uuid, name,
      type, summary, attributes}], facts: [{uuid, source_uuid,
      target_uuid, fact, valid_at, verdict, reasoning, invalidates}]}.
      Read it back before step f.
   f. Flip data/video_queue/<video_id>.json status to "done" -- or
      "failed" with a `reason` (transcript under ~150 words, empty, or
      unreadable). Never guess past an unreadable transcript.
4. If the run is running out of room, stop after the current item;
   the rest wait for tomorrow.
5. No email, ever -- not on success, not on failure.
6. Write one Project State note on world-graph (add_note, tag
   video-reader). First line, plain English for the Stack Repairer's
   recap, e.g. "Read 8 videos, 92 facts checked (6 set aside); 31 still
   waiting." Then counts (read / failed / facts verified / quarantined /
   still pending) and the paths written.

## Setup
Cowork scheduled task on Charles's plan -- card at
Chooch333/world-graph/docs/reader/VIDEO-SETUP.md.

## Language
Plain English in the note. Charles is not technical.

## Changelog
- v0.1.0 (2026-10-06) -- Initial draft, Build 17.1 (BB-2026-10-06-video-reader).
