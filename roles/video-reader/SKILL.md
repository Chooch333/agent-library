---
name: video-reader
version: 0.2.0
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
registry, check each fact against its transcript, write a summary for the
Reader on cbrain's Stack screen, and leave them for the nightly loader
(09:17 UTC). Runs on Charles's Claude plan, never the API key -- that is
the whole point (Build 17.1).

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
   step 4.
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
      the loader schema: {article_id: <video_id>, summary, entities:
      [{uuid, name, type, summary, attributes}], facts: [{uuid,
      source_uuid, target_uuid, fact, valid_at, verdict, reasoning,
      invalidates}]}. Read it back before step f.

      **Summary (v0.2.0).** The top-level `summary` is what Charles reads
      beside the transcript in the Reader. Shape: {"lead": str,
      "paragraphs": [str, ...], "key_points": [str, ...]}.
      - lead: 1-2 sentences -- what the video is and its main point.
      - paragraphs: 2-4 paragraphs, roughly 200-350 words in all, longer
        for long videos. Enough to do the video justice; never padded.
        Describe what is shown or demoed, not just what is said.
      - key_points: 3-5 short plain lines.
      Plain English. Written from the transcript only: never add anything
      the video doesn't say, and attribute opinions and predictions to the
      speaker. The loader ignores this key (it reads only entities and
      facts), so it never changes the graph. If a summary can't be
      written, leave the key out -- never placeholder text, never the API.
   f. Flip data/video_queue/<video_id>.json status to "done" -- or
      "failed" with a `reason` (transcript under ~150 words, empty, or
      unreadable). Never guess past an unreadable transcript.
4. SUMMARY BACKFILL (v0.2.0) -- after the new items. Up to 10 videos per
   run that were read before summaries existed, newest first.
   a. Find them: query cbrain Supabase (lpeswznkxzeeyiqaewma) table
      intake_items: kind = 'video' and summary is null and full_text is
      not null and status in ('in_graph', 'read'), ordered
      published_at desc nulls last, limit 10. That table is the nightly
      copy pipeline/sources_export.py writes, so it can be a day behind;
      if it can't be read, list data/extracted_video/ and pick the newest
      files with no summary key. Skip any video with no
      data/transcripts/<video_id>.md.
   b. For each: read the transcript in full and the current
      data/extracted_video/<video_id>.json. If it already has a summary,
      skip it. Otherwise write one by 3e's rules and commit the same file
      with only the summary key added -- every other key unchanged. Read
      it back.
   c. Never touch the queue entry: the video stays loaded and nothing new
      goes to the graph.
5. If the run is running out of room, stop after the current item
   (in step 3 or step 4); the rest wait for tomorrow. Fewer summaries is
   fine; a half-written file is not.
6. No email, ever -- not on success, not on failure.
7. Write one Project State note on world-graph (add_note, tag
   video-reader). First line, plain English for the Stack Repairer's
   recap, e.g. "Read 8 videos, 92 facts checked (6 set aside); 31 still
   waiting." Then counts (read / failed / facts verified / quarantined /
   summaries backfilled / still pending) and the paths written.

## Setup
Cowork scheduled task on Charles's plan -- card at
Chooch333/world-graph/docs/reader/VIDEO-SETUP.md.

## Language
Plain English in the note and the summaries. Charles is not technical.

## Changelog
- v0.2.0 (2026-10-10) -- Summaries for the Reader: step 3e writes a
  top-level summary ({lead, paragraphs[], key_points[]}, ~200-350 words,
  from the transcript only) into the same extracted file; new step 4
  backfills summaries for up to 10 already-read videos per run, newest
  first (old steps 4-6 are now 5-7). The loader ignores the key. Per
  BB-2026-10-09-intake-reader (Build 11.10).
- v0.1.0 (2026-10-06) -- Initial draft, Build 17.1 (BB-2026-10-06-video-reader).
