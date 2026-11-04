---
name: post-reader
version: 0.2.1
status: draft
triggers: ["Post Reader run"]
owner: Charles
source: BB-2026-10-28-social-post-share (Build 60)
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: on-its-own
  starts: "twice-daily schedule (morning and late afternoon, Indianapolis)"
  runs_in: claude-cloud
  reads: [yt-relay-posts]
  writes: [world-graph-article-queue, yt-relay-posts, project-state]
  stack: []
  origin: yours
  label: Post Reader
---

# Post Reader

## What
Twice a day, read X and Instagram posts Charles shared from his phone
(yt-relay posts/*.json, status pending), save each one as an article
the Collector already knows how to read, and put posts he steered as
R&D tasks in the R&D inbox. Runs on Charles's Claude plan. Reads pages
with TinyFish fetch_content only (free per page) — never TinyFish
Agent, Browser or Research (metered), never the API key.

## Job boundary
- Writes only: yt-relay posts/<key>.json (status and the fields below),
  world-graph data/articles/<article_id>.md and data/queue/<article_id>.json,
  one Project State note, one Next steps check-in.
- Never extracts facts (the Collector does), never writes to the graph,
  never touches queue/ (YouTube) or channels.json.
- Never writes a steer into agent-library (public). yt-relay and
  world-graph are private; the steer may live there.

## Each run, in order
1. LIST yt-relay posts/*.json with status "pending", oldest
   requested_at first. Cap 10 per run. None is a legal, boring run —
   go to step 4. (Field reference: yt-relay posts/README.md.)
2. For each post:
   a. Fetch the canonical url with TinyFish fetch_content (format
      markdown, image_links true, page_metadata true, links true,
      per_url_timeout_ms 60000).
   b. Usable means you got the author, the date and the post's own
      text or caption. The author can come from the page title
      ("Ryan Sael on X", "Buildpcb on Instagram") or the og/twitter
      metadata when the `author` field is empty; the date from
      `published_date` or article:published_time. A sign-in wall,
      "post unavailable", or only site chrome is not usable: bump
      attempts, keep pending, and mark failed with failure_reason after
      the 3rd unusable try. Never guess past an unreadable post.
   c. Links: from the post's own text only (not replies, not
      "more posts", not comments), fetch up to 3 linked pages that are
      not x.com, twitter.com, instagram.com or sign-in pages. X shows
      links as t.co short links in the metadata and as the real address
      in the post text (e.g. sael.net/light-bucket) — fetch the real
      address. Keep each page's title, url and main text (cut each at
      3,000 words).
   d. media: "video" when the page shows a video or reel preview
      (amplify_video_thumb in an image link, og:video, "reel" in the
      canonical link or "Instagram reel" in the twitter title), "image"
      for photos, "none" otherwise.
   e. article_id = first 12 hex characters of SHA-256 of the canonical
      url (same rule as world-graph pipeline/article_store.py
      compute_article_id). If data/queue/<article_id>.json already
      exists, skip writing (never overwrite) and go to f.
      Write data/articles/<article_id>.md with YAML frontmatter:
      article_id, source ("X post" or "Instagram post"), title
      ("<author> on X: <first 80 characters of the text>" or
      "<author> on Instagram: <first 80 characters of the caption>"),
      url (canonical), published, fetched_at, word_count, text_source
      "post_fetch", kind "post", platform, media, and guidance when the
      post entry has one. Body: the post text; then, for a video, one
      line: "This post has a video. Only its caption and preview image
      were read, not what is said or shown in it."; then one section per
      linked page ("Linked page: <title> (<url>)" + its text).
      Then write data/queue/<article_id>.json in feed_queue.py's
      write_pending shape (keys sorted, 2-space indent): article_id,
      url, title, source_name (the same "X post" / "Instagram post" —
      not a followed feed name, so the Stack screen's quiet-feed check
      never lists it), published, guidance ("" when none), status
      "pending", loaded false, requested_at, done_at null, loaded_at
      null. Read both back.
   f. R&D steer: if the post's guidance asks for R&D work — tech
      discovery, "what tech would this need", "R&D", evaluate a tool
      for the harness — set rd "waiting" and write pre_read on the
      post entry: {shows: 2-3 plain sentences on what the post shows
      or claims, tech: [named tools, models, libraries, products],
      links: [the linked pages' urls], media}. Plain words. From the
      fetched text only.
   g. Flip the post entry to status "done" with article_id, title,
      media, done_at. Commit, read back.
3. If the run is short on time, stop after the post in hand.
3b. Sites the nightly Action could not read (v0.2.0). Read world-graph
   data/feed_pages.json. For each entry with needs_tinyfish true:
   a. Fetch its url with TinyFish fetch_content (format markdown). No
      metered TinyFish tool, ever. Blocked or only site chrome: set
      last_result to what you saw, keep needs_tinyfish true, go on.
   b. Hash the main text as pipeline/feed_pages.py text_hash does: sha256
      of the text with every run of whitespace collapsed to one space.
      Same as the entry's hash: nothing to save.
   c. Changed: url = <page url>#v-<first 12 of the hash>, article_id from
      that url. Write data/articles/<article_id>.md (frontmatter article_id,
      source = the feed name, title "<name>: page updated <date>", url,
      published and fetched_at now, word_count, text_source "tinyfish_fetch",
      kind "page", page_url, page_hash) and data/queue/<article_id>.json in
      write_pending shape. Status "pending", or "saved" when the source has
      experts and is not on the Stack Advisor list (feeds.json).
   d. Update the entry: hash, last_saved, last_result "ok_tinyfish". Leave
      needs_tinyfish true; the nightly Action clears it when it can read
      the page itself. Commit, read back.
3c. Feed items the nightly Action could not fetch (v0.2.1). OpenAI's site
   refuses GitHub's machines (HTTP 403), but fetch_content reads it. Read
   world-graph data/feed_holds.json. For up to 10 held items, newest
   first:
   a. Skip one whose data/queue/<article_id>.json already exists.
   b. Fetch its url with TinyFish fetch_content. Under 100 words, or only
      site chrome: leave it; the nightly run keeps retrying and marks it
      failed after three nights.
   c. Write data/articles/<article_id>.md (article_id from the hold;
      frontmatter article_id, source, title, url, published, fetched_at,
      word_count, text_source "tinyfish_fetch") and
      data/queue/<article_id>.json in write_pending shape, status
      "pending". Read both back. Never edit data/feed_holds.json: the next
      nightly run sees the queue entry, marks the url seen and ends the
      hold.
4. R&D inbox card: count posts with rd "waiting". If one or more,
   Project State checkin as a job (source "job", kind "job",
   thread_key "job:post-reader-rd-inbox", plain_name "R&D inbox from
   shared posts", waiting_on "you", next_step "<N> shared post(s) are
   waiting for a tech discovery. Start a chat in the R&D project with
   'Tech discovery: inbox'."). If zero, close_thread on that key with
   closed_how "inbox empty".
5. No email, ever.
6. One Project State note on world-graph (add_note, tag post-reader).
   First line plain English, e.g. "Read 2 shared posts (1 to the R&D
   inbox); 0 failed." Then counts and the paths written.

## Progress tracking
None. This skill finishes in one run; the R&D inbox card is the
Tech discovery skill's to close.

## Setup
Scheduled task "Post Reader", twice daily (morning and late afternoon,
Indianapolis time). Prompt: "Post Reader run — follow
Chooch333/agent-library skills/post-reader/SKILL.md." Needs the
TinyFish, Custom GitHub and Project State connectors.

## Language
Plain English in the note, the pre-read and the card. Charles is not
technical.

## Changelog
- 0.2.1 (2026-11-04) — Step 3c: reads feed items held in data/feed_holds.json with fetch_content, because OpenAI's pages answer the nightly Action with HTTP 403. Per BB-2026-11-03-feed-channel-fix (Build 66).
- 0.2.0 (2026-11-04) — Step 3b: reads feed-less sites marked needs_tinyfish with fetch_content (free per page) and writes the article and state back. Per BB-2026-11-03-feed-channel-fix (Build 66).
- 0.1.0 (2026-10-28) — Initial draft. Per BB-2026-10-28-social-post-share (Build 60). Adjusted from the brief's draft only where the first live read showed it: author from the page title when the author field is empty (Instagram), t.co vs real link on X, reel detection from the canonical/twitter title, queue source_name kept off the followed-feed list.
