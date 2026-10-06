# Stack Advisor — brief format and writing for Charles

Read at DELIVER (step 6). Moved here unchanged from SKILL.md v1.8.1 by
BB-2026-10-05-advisor-reads-smarter (Build 28). Build 28.1
(BB-2026-10-05-advisor-thinks-bigger) added the two honest lines, the
Frontier heading and the draft format (bottom).

## Brief format

```
### ADV-NNN · {plain title, rule 6}{ · FRONTIER}
Source: {who they are, in a few words} — "{video or article title}" · {url}

**In plain terms:** {one sentence}

**What they found**
{2–4 sentences}

**What you have today**
{2–3 sentences: the component, process, or convention in Charles's stack this compares to, named by what it does, never a bare code (rules 2 and 4). If nothing comparable exists: "You don't have this today." plus one sentence on the closest thing.}

**What's wrong today**
{1–2 sentences: the concrete gap in that part right now — its weak spot from the stack briefing or section file, or what Charles's records show. Never a guess dressed as fact.}

**Why it matters here**
{2–3 sentences: why the advisor is pulling this out and tying it to that component — the link must be concrete, not thematic}

**What you'd gain**
{2–3 sentences: how Charles's day or stack improves if this is added or changed — plus "Effort: small | medium | large"}

{Checked | Assumed} — {one line}
```

Every idea in the committed ADV file (and the `advisor_ideas.body` copy
the Stack screen reads) renders exactly like this, in this order, nothing
else between blocks. The email uses its own short format — see
`email-format.md`.

Rules:
a. The heading line carries the ADV ID first, always.
b. When the evidence is Charles's own records rather than a video or
   article, the heading is still `### ADV-NNN · {plain title, rule 6}`;
   the next line reads `Source: your own records — {what the records
   are, in plain words, with codes in parentheses}` with no URL; and
   the first header reads **What your records show** (instead of "What
   they found").
c. To write *What they found* the advisor fetches the source file itself
   — `world-graph/data/transcripts/{video_id}.md` (video id from the
   URL's `v=` parameter) for a video, or
   `world-graph/data/articles/{article_id}.md` (article id: the first 12
   hex characters of SHA-256 of the canonical URL, matching
   `pipeline/article_store.py`'s `compute_article_id()`) for an article
   — via Custom GitHub MCP `get_file_contents`, and grounds the blurb in
   it; if the source file can't be read, the idea is dropped, not
   guessed. Video text is auto-captioned: check any product or person
   name against another source before quoting it.
d. One block per idea — the same video or article may appear twice with
   two different ADV IDs.
e. Resurfaced ideas keep their original ID and add a `Raised again
   because: {what changed}` line under Confidence.

The committed ADV file ends with a short "How this run worked" section
(rule 7): what was skimmed and deep-read, graph queries sent, reply
checks, items still waiting in the packet.

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
6. **Titles say what we'd do.** Start with a verb and state the move
   directly — the change itself, not a topic or a finding ("Retry the 38
   videos the spending cap blocked," not "Spending-cap failures in video
   intake"). Where it fits, name the concrete thing it touches or the
   number involved. 10 words max, no record codes, no outside company or
   product names. (Charles's own system names — cbrain, Stack screen —
   are fine.) The same title is used in the ADV file, the email and the
   Stack screen (`plain_title`).
7. **Short opening.** At most three sentences: how many ideas, and
   whether anything needs an answer. Run mechanics (what was read,
   queries sent, reply checks, queue counts) go in a short "How this run
   worked" section at the bottom of the committed ADV file only — never
   in the email.
8. **Reread as Charles before sending.** A sentence that needs a
   glossary gets rewritten, not footnoted.
