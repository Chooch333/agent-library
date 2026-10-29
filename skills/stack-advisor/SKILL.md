---
name: stack-advisor
version: 2.2.0
status: active
triggers: ["Stack Advisor run"]
owner: Charles
source: BB-2026-08-27-stack-advisor (DA session 2026-08-27); pool/scoring system per BB-2026-09-03-advisor-idea-pool; run packet per BB-2026-10-05-advisor-reads-smarter; briefing, focus days, Frontier lane and critic hand-off per BB-2026-10-05-advisor-thinks-bigger; new-capability lane per BB-2026-10-19-advisor-new-capability; done for you, two lenses and plainer writing per BB-2026-10-28-advisor-done-for-you
requires: [references/project-state.md]
wiring:
  runs: on-its-own
  starts: "Mon/Wed/Fri schedule"
  runs_in: cowork
  reads: [world-graph, project-state, cbrain]
  writes: [idea-pool, advisor-tables, email, plans]
  stack: []
  origin: yours
  label: Stack Advisor
---

# Stack Advisor

## What
Every scheduled run, know Charles's stack and where he is headed, read the
newest sources, and deliver a brief of up to 6 concrete upgrade ideas:
fixes for today's weak spots, plus new-capability ideas: new or emerging
tech and techniques connected to how Charles is wired up and running today.
Two questions drive every idea: what more could Claude sensibly do for
Charles, and what work could it sensibly take off him?
Small, obvious upgrades that pass the Done-for-you rule (step 4b) the
Advisor also puts on the overnight build shelf itself — at most 2 per run,
and Charles has a day to say no. It never builds and never edits the
stack map.

Code does the counting, you do the thinking. A nightly script
(`cbrain/tools/advisor/`, workflow `advisor-packet.yml`) keeps the idea pool
and ledger and writes the three files you read: `run_packet.json`,
`stack-briefing.md` and `sections/<section>.md`. It folds your judgments back
from `docs/advisor/run_result.json`. **Never open `pool.json` or `LEDGER.md`
whole.** Shapes: `cbrain/docs/advisor/README.md`.

## Job boundary
- Stack Manager = librarian (keeps the map accurate). Stack Advisor = scout
  (proposes improvements, and hands small obvious ones to the build
  shelf). Never dispose MAP-EDIT items; never edit concepts/stack-map.md.
- The Advisor proposes. For ideas that pass the Done-for-you rule (step
  4b) it also writes a short build brief and puts it on the overnight
  shelf (tag `advisor-auto`). These carry standing approval (Charles,
  2026-10-28): silence for a day is a yes, a Declined click is a no.
  Every other accepted idea leaves through the normal door: Charles takes
  it to a DA chat, which produces a Build Brief.
- It still never builds, never edits the stack map, and never queues
  anything that fails the rule — when unsure, it stays an idea.
- **The brief is the only email.** Never email Charles that a run failed.
  A failing run stops and, if it can, leaves the 6d Project State note on
  stack-map saying what failed. The Stack Advisor dot's output check goes
  late when runs stop, and the Stack Repairer covers it.
- When the Advisor Critic is live (6, hand-off switch) the critic, never
  you, approves and sends your ideas. You are the author; it is the judge.
  While it is live you hand nothing to the shelf: a Done-for-you
  candidate goes in the draft as an ordinary idea with the line
  `Could be done for you: {why it passes the rule}`.

## Contract — what every brief guarantees
The Advisor Critic grades every draft against this list.
1. **Grounded.** Every idea rests on a source you read in full (or Charles's
   own records) and names a real part in `connects_to`: a stack-map id, a
   build-machine part, a harness step/block id, or a plan or decision.
2. **Two honest lines.** Fix ideas say *What's wrong today* (a concrete gap
   in that part, from the briefing, section file or records — not a guess)
   and *Why this might be wrong*. New-capability ideas say *What you could
   do afterward* (one plain sentence: something Charles can do after that
   he can't today) and *Why this might be wrong*. *Why this might be wrong*
   is the strongest real reason the idea could fail or not be worth it.
   Never empty, never a formality.
3. **Not already done.** Checked against the part's line in the briefing /
   section file, the packet's `index` and `ledger_status`.
4. **New-capability.** At least one new-capability idea, or one line saying
   why none cleared 50.
5. **Bar held.** At most 6 ideas; none below its lane's threshold. Zero
   ideas is legal, with one line saying why.
6. **Plain English** per "Writing for Charles" (`references/brief-format.md`):
   short sentences, what changes for Charles, not how it works inside.
7. **Never quiet.** Every scheduled run ends in a brief (or a draft for the
   critic) — even a zero-idea one.
8. **No silent veto.** Never drop or down-score an idea because no record
   says Charles wants it — ask him in "Questions for Charles". Never drop
   or down-score an idea because it changes billing or cost — flag it (see
   the Cost line, step 4).
9. **Done for you is earned.** Every Done-for-you idea names what was
   checked live and how it was trimmed.

## Anti-patterns — never do these
- **Plumbing-only ideas** — a retry, a log line, a renamed field, a new
  column — dressed up as an upgrade. Never as a new-capability idea; in Fix
  only when it removes a stated weak spot.
- **Dropping an idea for lack of a weak spot.** No listed weak spot means it
  belongs in the new-capability lane, not the bin.
- **Vetoing on Charles's behalf** — "nothing says you want this" or "this
  costs money" as a reason to drop.
- **Generic patterns** ("add observability", "use RAG", "add evals") with no
  named part and no concrete change.
- **A second source used as filler** to reach high conviction or the +8
  evidence bonus when it doesn't independently support the claim.
- **Ideas already built** — check the live part before proposing.
- **Feature-list echo** — restating what a source announced without saying
  what changes in Charles's stack.
- **Reading around the briefing** — opening the Master Roadmap, Build Map
  Skeleton or full stack map "for context". (Step 4b's live check reads
  only the part a Done-for-you idea would change.)
- **Shelving on the idea as pitched.** A Done-for-you idea is shelved only
  after the live check and the trim — never straight from the source.
- Quoting an auto-caption spelling as a product name.

## Focus by day
The run's day in America/Indiana/Indianapolis picks the section:
**Mon → `intake`**, **Wed → `build-machine`**, **Fri → `app`**. Any other
day uses the most recent of those (Tue → intake, Thu → build-machine,
Sat/Sun → app). The focus aims skim ratings and graph questions; a strong
idea for another section is still allowed.

## Each run, in order
1. FEEDBACK FIRST. Collect Charles's answers from both sources (a union;
   either may be empty) as `feedback` entries for run_result.json —
   `{adv_id, answer: interested|declined|scoping|done, note, at, via}`:
   a. Gmail: his reply to the latest "Stack Advisor brief" email
      (`via: email`; map his words to one of the four answers).
   b. Stack screen: `advisor_dispositions` on `lpeswznkxzeeyiqaewma` where
      `consumed_at is null`, oldest first (`via: stack`, `answer` =
      `disposition`, `at` = `created_at`).
   The script applies the ledger rules. Check each ID against the packet's
   `ledger_status`: an ID with no row is left unconsumed and named in the
   brief; an answer on an `addressed` row, or a non-Done answer on a
   `building` row, is skipped (still consumed) and named in the opening —
   except Declined on a Done-for-you row (its Response starts "doing for
   you — "), which stops it: the row becomes `declined` and the night
   runner abandons the plan if it hasn't built yet. If that plan already
   built, say so in the opening and that "undo ADV-NNN" in any chat
   reverses it.
   For a Done answer, name in the opening any draft/queued/running plan
   whose tags or provenance cite that ADV ID.
2. ORIENT — read exactly three files from Chooch333/cbrain, live:
   a. `docs/advisor/stack-briefing.md` — "How you're set up today" (where
      things run, what thinks and how it's paid, the doors chats have), one
      line per part (what it does, how it runs, what AI it uses and how
      it's paid, what it feeds, its weak spot, last changed) and "Where
      Charles is headed" (every harness step's *stops me* and *today*).
   b. `docs/advisor/sections/<focus>.md` — full detail for today's section.
   c. `docs/advisor/run_packet.json` — live ideas, `index`,
      `ledger_status`, `next_pool_id`, `next_adv_id`, `last_brief`,
      `drafts_pending` and the waiting `items`.
   Nothing else: not the Master Roadmap (31fdcb9b), the Build Map Skeleton
   (076b64ca), `concepts/stack-map.md` or `get_entity('stack-map')`. If the
   briefing or section file is missing or its "Generated" date is over 3
   days old, say so in the 6d note and carry on with what exists.
3. READ THE GRAPH. Dispatch Chooch333/world-graph workflow `query.yml`
   (ref `main`, mandatory) 1–3 times with questions about today's section's
   weak spots and harness gaps. Read the new files in `answers/`. "The
   graph doesn't know" is a real answer.
3b. INTAKE — skim, then deep-read. The packet holds only your sources,
   oldest first, each with an excerpt and its full length (`chars`). Items
   over 10 KB carry start/middle/end slices; a `digest` item is one feed's
   whole batch and gets one rating.
   a. **Skim** up to 30 items. Rate each high / medium / low: could it
      change a part in today's section, a harness step, or something on the
      shelf? `title_only` = a speechless video: judge by title, channel and
      date; never deep-read it.
   b. **Deep-read** the top ~6 (highs first) in full from `path`
      (`repo:file` — owner Chooch333, `get_file_contents`).
   c. Low = done. Medium = eligible once more next run. Unskimmed items wait.
   d. Video text is auto-captioned: names come out misspelled. Never quote
      a caption as a product name without checking it.
   e. Each deep-read item yields 0–3 candidates, each naming its lane
      (`fix` or `new-capability`) and a `connects_to`, or it is trivia and
      is not pooled.
   f. **Two lenses.** For every candidate ask: "How could this sensibly
      expand what Claude can do for Charles?" and "How could this sensibly
      take work off Charles?" Write the one it answers in the idea block's
      `Lens:` line (`more Claude can do` | `less work for you` | both). A
      clear yes to either feeds the score in step 4.
4. SCORE AND SELECT. Two lanes. Score every candidate and every live idea
   that got new evidence.
   - **Fix lane (0–100, threshold 60):** *connection* 0–40 (names a
     queued/running plan, an open decision, or a live part and says exactly
     what changes) · *evidence* 0–25 (grounded in a source you read; +8 per
     additional independent source, max 25) · *payoff* 0–20 (S effort with
     real payoff scores high; L caps at 10; a clear yes to either lens
     raises it) · *timeliness* 0–15 (on the shelf now = 15; roadmap-later
     = 5; neither = 0). Connection and timeliness need the shelf: one
     Supabase SQL on `ujditldbqdiqigazkcak` — plans queued or running,
     joined to projects (title, tags, project).
   - **New-capability lane (0–100, threshold 50).** Gate first — all
     three or it isn't pooled: (a) a source read in full; (b)
     `connects_to` names the part of the current stack it attaches to (a
     part id from the briefing's "How you're set up today" or "The
     stack", a step `s01`–`s11`, or a block `b01`–`b21`); (c) one plain
     "afterward you could…" sentence naming something Charles can't do
     today. **No weak spot needed.** Score: *capability* 0–40 (how much
     new becomes possible — a new kind of work, a hand step removed; a
     harness step's *stops me* shrinking is one way, not the only way; a
     clear yes to either lens raises it) · *fit* 0–20 (attaches to what
     already runs: same platform and accounts = high; needs a new
     platform or account = lower, never 0 for that alone) · *evidence*
     0–25 (as Fix) · *recency* 0–15 (source ≤ 30 days old = full; older
     scales down; > 90 days = 0). Score keys: `capability`, `fit`,
     `evidence`, `recency`; set `"lane": "new-capability"`. Heading gets
     ` · NEW CAPABILITY`. None clears → the brief's opening says why in
     one line.
   - **Slots:** one slot is reserved for the best new-capability idea; a
     second clearing one may take any slot Fix leaves empty.
   - **Cost line.** An idea that would move work off the Claude plan, add
     a paid service, or change what anything costs carries a line under
     its block: `Cost change: {what moves to what, rough cost if the
     source says}`. No score penalty.
   - **High conviction:** a Fix idea `total ≥ 85` with ≥ 2 independent
     sources. Exactly one per brief, leads the Ideas for you group,
     heading gets ` · HIGH CONVICTION`. Any other qualifier goes in `held`.
   - **Cap:** at most 6 = 1 high-conviction + 1 new-capability + the rest
     Fix, best score first. An empty slot goes to the next Fix idea, or to
     a second clearing new-capability idea. 0–2 ideas
     is fine. **Never send a below-threshold idea to fill a slot.**
     Done-for-you ideas count toward the 6.
   - **Slow day:** under 5 new eligible ideas → fill from live Fix ideas
     `≥ 60` never surfaced, oldest-high-score first.
   - **Merge / repeats:** compare each candidate's `topic_key` and title
     with the packet's `ideas` and `index`; reuse a matching `topic_key`
     (the script merges and revives) or list it under `rescored`. Same idea,
     same source — never twice. Same theme, new source — may return once
     with `Raised again because:` unless the ledger Response already covers
     it. Excluded: ledger `building`/`declined`/`addressed` ideas, any idea
     a plan or decision cites by ADV ID, and one already live in its part
     (list it under `adopt`). A `cut` idea returns only with a new source
     that answers the critic's reason (its Response).
   - Write the two Contract lines for every selected idea now.
   - Assign `adv_id`s from `next_adv_id` upward (a resurfaced idea keeps
     its own) and pool ids from `next_pool_id` upward.
4b. DONE FOR YOU. Look at every selected idea, and at live ideas in the
   packet that already cleared their lane. An idea qualifies only when
   **all five** hold:
   1. It fits inside something that already runs — no new scheduled task,
      account, paid service or screen.
   2. Effort small.
   3. No cost change (no Cost line), and nothing involving keys, money or
      deleting data.
   4. Not declined, not `building`/`addressed` (packet `ledger_status`),
      and no open question to Charles about it (this brief's or the last).
   5. You checked it against live data this run — read the part's own
      files and the rows or logs it would change — and trimmed it to the
      smallest version that does the job (the way ADV-086 became two lines
      in the night runner and ADV-052 became one check in the Stack
      Inspector). If the check shows the premise is wrong, it is not done
      for you; say so in its block's *Why this might be wrong*.
   When unsure whether it is small enough, leave it as an idea.
   **At most 2 per run**, best score first; the rest that qualify stay as
   ideas. While the critic is live, hand nothing off (Job boundary). For
   each one:
   a. Before writing, `list_plans` on project `cbrain` for a
      draft/queued/running plan citing the ADV id — if one exists, it is
      not done for you (it is already on its way).
   b. `write_plan` on project `cbrain` using the Stack Repairer's short
      brief template (`skills/stack-repairer/SKILL.md`, "Short brief
      template"), named `BB-YYYY-MM-DD-adv-NNN-{slug}`, with `**Build:**
      unnumbered (Stack Advisor)`, `**What you'll do:** Nothing — click
      Declined on the Stack screen to stop it`, *Asked for* = the ADV
      idea, what you checked live and how you trimmed it; tags
      `advisor-auto`, `build-brief` and the ADV id (e.g. `adv-086`);
      `overnight: true`; `target_repo`; `plain_title` and `plain_summary`
      in plain words. The directive's last step marks the LEDGER row
      `addressed` ("done for you — built YYYY-MM-DD, {BB id}"). Then
      `update_plan_status` → `queued`. These briefs carry standing
      approval — never ask "Overnight: yes or no?".
   c. Commit the brief to the target repo's `docs/design/{BB id}.md` with
      the plan id in its header; read it back.
   d. Work out `builds_on`: the Indianapolis date of the first 1 am Night
      builds start at least 18 hours after queuing (the day after a 3 am
      run). Say it to Charles as the night before it: a build at 1 am
      Thursday "builds Wednesday night", stop "before 1 am Thursday".
   e. Record it in `run_result.json` under `done_for_you`:
      `{adv_id, plan_id, bb_id, plain_change, builds_on}` — `plain_change`
      is one plain sentence of what will change, no file or tool names.
   The idea's ADV block gets the Done-for-you lines
   (`references/brief-format.md`), and it leads the email
   (`references/email-format.md`).
5. ASK IF UNSURE. If a current build's purpose can't be stated in one
   sentence, add "Questions for Charles" — max 3, closed choices with a
   recommendation each. Never block on them. An idea Charles's records
   don't show he'd want still ships; add a closed question naming its ADV
   ID ("Do you want X? Recommend: yes/no because…"). Max 3 questions
   total; idea questions first. An idea with a question is never done for
   you this run.
6. DELIVER — the hand-off switch. First read `references/brief-format.md`,
   `references/email-format.md` and `references/deliver.md`. Then check
   whether `cbrain/docs/advisor/critic_live.json` exists
   (`get_file_contents`; not found = absent).
   **Absent → deliver directly**, as before:
   a. Commit the brief → `cbrain/docs/advisor/ADV-YYYY-MM-DD.md`; read back.
   b. Commit `cbrain/docs/advisor/run_result.json` (shape in the README):
      `run_id` (the ADV file name), `run_at`, `brief`, `feedback`, `skim`
      (`key`, `ids` copied from the packet, `rating`), `candidates` (with
      `lane`), `rescored`, `adopt`, `surfaced` (with `lane`; Done-for-you
      ideas too), `held`, `done_for_you` (step 4b). Read it back. Only
      then set `consumed_at = now()` on every disposition row folded or
      skipped in 1b. Dispatch `advisor-packet.yml` (ref `main`) and
      confirm the refreshed packet shows `last_run_id` = your `run_id`
      (if not after ~10 minutes, say so in 6d).
   c. Gmail send — subject "Stack Advisor brief ADV-YYYY-MM-DD", Done for
      you first, Ideas for you second (`references/email-format.md`).
   d. Project State note on stack-map: one-paragraph digest + git path,
      focus section, packet bytes, items skimmed / deep-read,
      new-capability result, and the Done-for-you plan ids.
   e. Supabase copy for the Stack screen, per `references/deliver.md`
      (Done-for-you rows get status `building`).
   **Present → stop at a draft** for the Advisor Critic:
   a. Commit the draft → `cbrain/docs/advisor/drafts/ADV-YYYY-MM-DD.md` in
      the draft format (`references/brief-format.md`); read back.
   b. As 6b, with `"stage": "draft"` in run_result.json and no
      `done_for_you`. The script holds new ideas as `draft` in the pool
      and LEDGER until the critic rules.
   c. **No email.**
   d. As 6d, saying the draft waits for the critic.
   e. Supabase: no `advisor_runs` row and no new `advisor_ideas` rows (the
      critic writes them when it publishes). Only sync `status`/`response`
      of existing `advisor_ideas` rows from the packet's `ledger_changed`,
      skipping rows whose status is `draft` or `cut`.
   To turn the critic off, Charles deletes `critic_live.json`; the next run
   delivers directly again.

## Progress tracking
None. This skill finishes in one run and leaves nothing open.

Changelog: `references/changelog.md`. Latest: **v2.2.0** (2026-10-29) — Done for you:
small, obvious, live-checked upgrades (five conditions, at most 2 per run) go on the
overnight shelf as `advisor-auto` briefs with standing approval; Charles has a day and a
Declined click to stop them. Two lenses (more Claude can do, less work for Charles),
contract item 9, a two-group email and one notch plainer writing
(BB-2026-10-28-advisor-done-for-you, Build 57).
