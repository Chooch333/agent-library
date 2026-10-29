# Stack Advisor — brief format and writing for Charles

Read at DELIVER (step 6). Moved here unchanged from SKILL.md v1.8.1 by
BB-2026-10-05-advisor-reads-smarter (Build 28). Build 28.1
(BB-2026-10-05-advisor-thinks-bigger) added the two honest lines, the
one-slot lane's heading and the draft format (bottom). Build 41
(BB-2026-10-19-advisor-new-capability) renamed that lane new-capability:
its heading, its "What you could do afterward" line and the Cost line.
Build 57 (BB-2026-10-28-advisor-done-for-you) made every block one notch
plainer and shorter, dropped "Why it matters here", and added the Lens
line and the Done-for-you block.

## Brief format

```
### ADV-NNN · {plain title, rule 6}{ · NEW CAPABILITY}
Source: {who they are, in a few words} — "{video or article title}" · {url}

**In plain terms:** {1 sentence}

**What they found**
{1–2 sentences}

**What you have today**
{1–2 sentences: the part of Charles's stack this compares to, named by what it does, never a bare code (rules 2 and 4). If nothing comparable exists: "You don't have this today." plus the closest thing.}

**What's wrong today**
{1 sentence: the concrete gap in that part right now — its weak spot from the stack briefing or section file, or what Charles's records show. Never a guess dressed as fact.}
— or, for a new-capability idea, in its place —
**What you could do afterward**
{1 sentence: something Charles can do after this that he can't today. No weak spot needed.}

**What you'd gain**
{1–2 sentences: how Charles's day or stack gets better — plus "Effort: small | medium | large"}

**Why this might be wrong**
{1 sentence: the strongest honest reason this could fail, cost more than it gives, or already be covered. Never empty, never "no risks".}

Lens: {more Claude can do | less work for you | both}
Cost change: {what moves to what, rough cost if the source says}   ← only when the idea moves work off the Claude plan, adds a paid service, or changes what anything costs
{Checked | Assumed} — {one line}
```

Aim for about 120 words per block, headings included. Anything essential
that used to go in "Why it matters here" folds into *What you'd gain*.

**Done-for-you block.** An idea the Advisor put on the build shelf (SKILL
step 4b) gets these four lines right after **In plain terms**, before
**What they found**, and keeps the rest of its block:

```
**What will change**
{1–2 plain sentences. No file, tool or code names.}

**What you'll notice**
{1 sentence: what Charles will see or stop having to do.}

**What I checked**
{1 sentence: what was read live this run and how the idea was trimmed (contract item 9).}

**To stop it**
Click Declined on the Stack screen before 1 am on {day}, or tell any chat "don't build ADV-NNN".
```

`{day}` is the weekday of `builds_on` (SKILL step 4d) — a build at 1 am
Thursday reads "before 1 am on Thursday". While the critic is live, a
Done-for-you candidate gets the single line `Could be done for you: {why
it passes the rule}` instead, and no **To stop it**.

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
   because: {what changed}` line under the Checked/Assumed line.

The committed ADV file ends with a short "How this run worked" section
(rule 7): what was skimmed and deep-read, graph queries sent, reply
checks, items still waiting in the packet, and the Done-for-you plan ids.

## Writing for Charles
Charles is not technical and reads these cold, often days later. Every
sentence must make sense to a smart person who has never seen this
system's files. Since Build 57: one notch plainer than before.

0. **Short sentences.** 20 words or fewer. One idea per sentence.
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
   hook, trace, observability, orchestrator, idempotent, saga, "the X
   pattern", pipeline, endpoint, schema, deploy (→ "put live"), repo
   (→ "project files"), workflow (→ "job"), MCP (→ "connection"), cron
   (→ "timer"), webhook, payload, threshold (→ "pass mark"), lane, slot.
6. **Titles say what we'd do.** Start with a verb and state the move
   directly — the change itself, not a topic or a finding ("Retry the 38
   videos the spending cap blocked," not "Spending-cap failures in video
   intake"). Where it fits, name the concrete thing it touches or the
   number involved. 10 words max, no record codes, no outside company or
   product names. (Charles's own system names — cbrain, Stack screen —
   are fine.) The same title is used in the ADV file, the email and the
   Stack screen (`plain_title`).
7. **Short opening.** At most two sentences: what will build unless he
   says no, how many ideas, and whether anything needs an answer. Run
   mechanics (what was read, queries sent, reply checks, queue counts)
   go in a short "How this run worked" section at the bottom of the
   committed ADV file only — never in the email.
8. **Reread as Charles before sending.** A sentence that needs a
   glossary gets rewritten, not footnoted.
9. **Say what changes for Charles, not how it works inside.** "You'll
   get one email when a build is skipped," not "the runner posts a
   night_runs row and a checkin card."

## Draft format (critic live)

When `cbrain/docs/advisor/critic_live.json` exists the Advisor writes the
brief to `cbrain/docs/advisor/drafts/ADV-YYYY-MM-DD.md` instead, for the
Advisor Critic to judge. Same blocks and opening as above, plus:

```
---
status: draft
run_id: ADV-YYYY-MM-DD
focus: intake | build-machine | app
created_at: <ISO>
new_capability: ADV-NNN[, ADV-NNN] | none — {one-line reason}
---
```

and, as the last lines of each idea block (the critic strips them when it
publishes):

```
Critic notes — Pool: P-NNNN · Lane: fix | new-capability · Score: {parts} = {total} · Connects to: {ids} · Source file: {repo:path, or "records: …"}
```

The critic sets `status: reviewed` and appends a "Critic verdicts" section
(one line per idea: keep / sharpen / cut — reason) once it has ruled.
