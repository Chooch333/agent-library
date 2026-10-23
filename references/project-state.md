# Project State — shared reference

Shared reference for any skill that reads or writes Project State. Loaded by a skill's `requires:` header; not a trigger.

---

## The seven buckets

Every item that goes into Project State fits one of these. Use the plain-English name on tickets. Never invent new categories; if something doesn't fit, use **Note** and we'll sort it out.

1. **Decision** — a choice that's been made, with the reason why. Example: *"Using Supabase MCP for DDL rather than copy/paste SQL, because it removes a manual step."*
2. **Next step** — a concrete action someone is going to take. Example: *"Wire Google Places API key into Vercel env vars for the Family Trip App."*
3. **Open question** — something unresolved that's blocking or shaping progress. Example: *"Is Joe producing the Ridgeworks operating agreement, or is that on Charles?"*
4. **Learning** — a retrospective observation worth remembering for next time. Example: *"Claude Code prompts need explicit Preserve/Verify sections or it wanders off-scope."*
5. **Assumption** — something being treated as true for now, but might need to be revisited. Example: *"Assume 80% LTV on BRRRR refi until the lender confirms."*
6. **Status** — a narrative snapshot of where a project is right now. Status also absorbs handoff observations — pattern-level notes, unresolved undercurrents, and context that didn't fit a numbered bucket but matters for the next session. Example: *"Family Trip App: vibe planning environment stripped; ready for clean rebuild once Places API key is in place. Worth flagging: Charles kept circling back to whether the vibe buttons should persist — might signal the mental model isn't settled yet."*
7. **Note** — the catch-all. Quick capture when it doesn't cleanly fit yet. Gets promoted into one of the six above later.

### Priority on Next steps

Use the tag `urgent` to elevate a next step. The dashboard shows urgent next steps in their own sub-section. No other priority levels — either it's urgent or it isn't.

---

## Sessions

A **session** is a unit of work within a chat that ends with a Session Log. A chat can contain one or more sessions. Each Session Log is a milestone: future sessions reach back to prior logs as baseline and do not rewrite them. If a later session changes something a prior session decided, it supersedes — it doesn't rewrite the earlier log. "Log this state and keep working" is a session boundary.

---

## Campaigns and the naming rule

Campaigns are a grouping layer that sits above projects and tags — a table (`campaigns`: `slug`, `title`, `purpose`, `status` — `active`/`done`/`parked`) for organizing related plans across a project's lifetime. Plans now carry `plain_title`, `plain_summary`, `campaign_id`, `designed_in`, plus retired review fields (`reviewed_at`, `reviewed_by`, `review_notes` — no longer written; the finished-build review gate was removed 2026-10-23, see "Succeeded means done" in `skills/build/SKILL.md`).

**DA authority over campaigns.** DA/planning chats have full fluidity authority over campaigns — rename one, recategorize a plan into a different campaign, fork a new campaign out of an existing one — freely, logged as a judgment call (same provenance discipline as any other judgment call). Charles is never asked to approve a campaign change.

**The naming rule.** Every chat that creates a plan or files a note writes its best-shot `plain_title` / `plain_summary` at creation — every time. There is no tool gate enforcing this; writes always succeed with or without a plain label. This is mandatory chat behavior, not a validation. If "(needs a name)" is showing on the Board, that's a chat defect — fixed by the next chat that touches the item. Charles is never the one who generates a name.

**What Charles sees (naming legend).** *This paragraph is the text the dashboard displays to Charles.* Builds carry a BB filing code (e.g. `BB-2026-08-27-comms-hub-plumbing`) for chats' cross-referencing only — Charles never needs to know it or use it. The names Charles actually reads are the plain titles: `plain_title` and `plain_summary` on each plan.

---

## Three ticket types — all live as artifacts

**Every time Claude plans to act on the database, it produces a ticket artifact.** The artifact opens beside the chat; the chat itself stays for discussion. Conversational questions ("should we do X or Y?", "what do you think about Z?") stay in chat — they do not go on tickets.

### Session Log

For anything going *into* the database at a session boundary. One Session Log per session, regardless of how many items or what types. If six items across four buckets are going in at once, they all sit on one Session Log.

Every Session Log includes a status snapshot and a next-action line, even if the session feels light. The status snapshot is where handoff observations live — see the Status bucket description above.

**Template:**

```
# Session Log — [YYYY-MM-DD] — [short session topic]

**What this is:** [one-line summary of the session and what's being logged]

**What I'll do:** [plain English — e.g., "Log 4 items to Family Trip App: 2 decisions, 1 next step, 1 learning. Write a status snapshot."]

**What you'll do:** [e.g., "Review entries below, edit wording, approve."]

---

## Current state going in

[brief narrative — where things stand at the moment this session closes, as context for reviewing the entries]

---

## Entries to log

### 1. [Bucket] — [headline in plain English]
**Body:** [what will go in the database, in plain English]
**Project:** [project slug]
**Tags:** [comma-separated tags]

[repeat for each item]

---

## Status snapshot

[narrative covering where the project stands post-session. Include handoff observations: patterns noticed, unresolved undercurrents, anything that didn't fit a bucket but matters for the next session.]

---

## Next action line

[one line — what the next session on this project should start with]

---

## Result (fill in after execution)

**What got logged:** [bullet list of entries with returned IDs]
**Where:** [project name in Project State]
```

### Fix Ticket

For anything that breaks — and the fix. Break and solution live on the same ticket; the resolution section gets filled in after the fix lands.

**Template:**

```
# Fix Ticket — [YYYY-MM-DD] — [short description of what broke]

**What broke (plain English):** [the symptom — what Charles is seeing, or what stopped working]

**What I think is happening:** [hypothesis in plain English, not jargon]

**What I want to try:** [the proposed fix, described as actions not code]

**What could go wrong:** [risks, side effects, anything else that might be affected]

**What you'll do:** [review and approve, provide info, run a command, etc.]

---

## Resolution (fill in after)

**What we actually did:** [...]
**Did it work:** [yes / no / partially — with note]
**Learning to capture:** [if applicable — this often becomes a Learning entry in a future Session Log]
```

### Build Brief

For handing off a scoped task to a sub-chat. Use when the current chat needs to spawn focused work elsewhere — a different codebase, a narrow investigation, a deliverable that belongs in its own context — rather than execute inline.

A Build Brief is both a handoff payload and a queue entry. At authoring it is committed to git and written to Project State as a plan (see Shelving a brief, `skills/build/SKILL.md`) — it does not otherwise write Decisions, Next steps, or other buckets on creation.

**Template:**

```
# Build Brief — BB-[YYYY-MM-DD-slug]

**What this is:** [one-line summary of the task being handed off]

**What I'll do:** [what the sub-chat is expected to produce]

**What you'll do:** [approve the Brief, paste it into the sub-chat, any other context-setting]

---

## Current state going in

[brief narrative — what the main chat knows that matters for this work]

---

## Receiving chat

[named sub-chat, or "new chat to be opened"]

---

## Scope

**In scope:** [what the sub-chat will work on]

**Out of scope:** [what it won't touch; common forks pre-answered]

---

## Directive

[do X, return Y in format Z — prescriptive]

---

## Inputs

[files, links, DB entries, prior decisions the sub-chat needs]

---

## Pasteable prompt

[exact first-message text for the sub-chat]
```

---

## Standing rules (database behavior)

- **No logging without a ticket.** Even a single-item log goes on a Session Log artifact.
- **One Session Log per session.** Batch all log entries onto one Session Log. Don't spawn multiple artifacts for the same session.
- **Every Session Log writes a status snapshot.** The snapshot is a mandatory field on every Session Log, not optional. Light sessions still get one.
- **Plain English on tickets.** Technical syntax (SQL, function calls, MCP commands) belongs in the execution step, not on the ticket Charles is reviewing.
- **Chat questions stay in chat.** Clarifying questions, trade-off discussions, and open-ended thinking happen in the chat thread — not on artifacts.
- **Coordinate with existing projects before creating new ones.** Build chats do not automatically create a new project on start. At the first log moment, Claude calls `list_projects` and identifies which existing project the content belongs to. If the fit is clear, log there. If the content doesn't clearly fall under an existing project, Claude pauses and asks for direction before creating one.

---

## The Comms Table

**The Comms Table** is the standing name for this location — the `build_questions` + `build_question_messages` table pair. Use "the Comms Table" in chat, tickets, and doctrine whenever referring to this location; it is the canonical term and no chat should have to infer what it means. The Comms Table carries two lanes, described below: the **Q-channel** (blocking questions) and the **disclosure channel** (non-blocking judgment calls).

### The Q-channel (blocking questions)

The Q-channel is a **build-chat instrument**. Its whole job: when a build chat executing a brief hits something genuinely above its authority, it files a question instead of stalling or guessing, and Charles carries the ID to a DA/planning chat that answers it — without Charles having to relay the content by hand. It is not a general question box.

**Who does what:**
- **Build chats MUST use it.** A build chat executing a brief that hits a decision point beyond its authority (see the hard-gate list in `skills/build/SKILL.md` — but also genuinely design-level forks the brief left silent) files a question here rather than asking Charles ad hoc. Every build-chat question is **bound to its build brief** (`plan_id`), so two builds' questions never blur even on the same project.
- **DA/planning chats ANSWER; they do not originate.** A DA/planning chat, at session start, checks for open questions on its project and answers them. It does **not** push new questions to Charles through this channel on its own initiative — DA chats surface their forks to Charles in-chat as normal. The one exception: if Charles explicitly says "log this as a question," the DA chat files it (origin `charles-directed`) and Charles's reference resolves to it.
- **Charles carries the pointer, not the payload.** Build chat surfaces the ID → Charles brings it to a DA/planning chat → that chat reads the thread and answers. The thread holds the content; Charles moves only the ID.

**The tables:** `build_questions` (one row per question) and `build_question_messages` (append-only dialogue — every turn a new row, nothing overwritten) — together, the Comms Table. Key fields on a question: `display_id` (globally unique, see below), `plan_id` (the build brief it belongs to — required for build-origin questions), `origin` (`build` or `charles-directed`), `status`, `linked_decision` and `resolved_decision_project` (the answer, and which project it lives on — they can differ).

**IDs are globally unique — always cite them in full.** Display IDs are project-prefixed: `ABO-Q-001` (agent-build-out), `CBR-Q-001` (cbrain), etc. There is no bare `Q-001` — the prefix is part of the ID. Never drop it; a bare number is ambiguous and the prefixed form is the whole point.

**Status lifecycle:** `open` (needs an answer) → `answered` (build chat can proceed) → `discussing` (clarification bouncing) → `resolved` (settled). The database **enforces** that a question cannot be marked `resolved` without naming its resolving decision (`linked_decision`), and the decision may live on a different project than the question — record that project in `resolved_decision_project`. This is the fix for the drift class where an answer got logged as a decision elsewhere and the question was left orphaned-open.

**Answering rules (DA/planning chats):**
1. At session start, query `build_questions` for `open`/`discussing` on the current project.
2. To answer: append a `build_question_messages` row (author `da`/`planning`) and set status `answered`; or ask back and set `discussing`.
3. If the answer is a durable decision, log the Decision, set `linked_decision` + `resolved_decision_project`, then set status `resolved`. Do this **even when the decision lands on another project** — the link is mandatory, not optional.
4. **Before telling Charles an open question still needs him, search for an existing decision that already answers it.** An open flag is not proof the decision is unmade — decisions can land on other projects (lesson: `cbrain/CB-101`).

### Disclosures — the build-to-Charles channel (`origin='build-judgment'`)

Alongside blocking questions, the Comms Table carries a second, non-blocking lane: anything a build chat would otherwise tell Charles beyond "done and logged" — a judgment call made on its own authority, a loose end, an FYI — posted as a disclosure rather than relayed in a chat closeout.

**The routing rule.** If a build chat is going to tell Charles anything other than "it's done and ready to log," that thing goes on the Comms Table, not into a chat message. The build decides what counts; the Comms Table is just the destination.

**The closing rule.** A build chat's final chat message may only say the build is done and that everything else is on the Board. Every judgment call, loose end, follow-up, or FYI goes to the Comms Table — with a `plain_summary` and `action_needed` flag set — never into chat text.

**Born non-blocking.** A disclosure starts in status `noted`, origin `build-judgment`, tagged `judgment-call` — never `open`. Every "what's blocking this build" query filters `status IN ('open','discussing')`, so disclosures are invisible to it automatically; that's the entire isolation mechanism, no special-casing needed elsewhere.

**Status lifecycle:** `noted` (posted, awaiting optional review) → `reviewed-agree` (a DA chat looked, concurs, done — no decision required) or `reviewed-corrected` (a DA chat disagreed and logged a correcting Decision — `linked_decision` is required, the same rule as blocking-question `resolved`).

**Prefix:** a parallel per-project `-J-` series (`CBR-J-001`), independent of and never continuing the `-Q-` series.

**Pull only, no push.** DA/planning chats pull the "Calls to review" inbox (`list_judgment_calls`, status `noted`) at session start, listed separately from blocking questions — nothing pushes, nothing gates. If a build hits something it genuinely can't decide, that's a blocking question (`open`), not a disclosure.

**Tools:** `post_judgment_call` (build side, at brief close), `list_judgment_calls` and `dispose_judgment_call` (DA side, at session start). Scoped strictly to `origin='build-judgment'` — the blocking-question tooling and behavior above are untouched.

---

## The Punch List

Design Assist chats pull needs-brief punch items at intake.

---

## Appendix — Bucket to MCP tool mapping (for Claude)

This is for Claude's reference when executing after ticket approval. Charles does not need to read this.

| Bucket         | Project State tool            |
|----------------|-------------------------------|
| Decision       | `log_decision`                |
| Next step      | `add_next_move`               |
| Open question  | `add_blocker`                 |
| Learning       | `add_lesson`                  |
| Assumption     | `add_assumption`              |
| Status         | `write_status_snapshot`       |
| Note           | `add_note`                    |

For supersessions, use `supersede_decision` (decisions) or `update_plan_content` (plans). Tags go in via `add_tags` or at creation time. Always verify the project is registered with `list_projects` before logging; if not, `create_project` first.

**Plans and disclosures.** `write_plan` creates a plan (Build Brief or otherwise); `update_plan_content` amends one and keeps revision history; `post_judgment_call` files a disclosure on the Comms Table at build close. All three take `plain_title`/`plain_summary` (disclosures also take `action_needed`) — set them every time per the naming rule above.

**Soft enforcement only.** Labels are never mandatory at write time — writes always succeed with or without them. A plan tagged `build-brief` that lands without `plain_title`/`campaign` gets a warning line back to the writing chat — not a rejection, and not a note routed to Charles.
