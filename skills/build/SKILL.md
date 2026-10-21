---
name: build
description: 'Use when the first message says "this is a build chat": work that produces deliverables, decisions or progress on a project, logged to Project State. Carries authority rules, Build Brief defaults, workflow and response format.'
requires: [references/project-state.md, references/gotchas.md, references/thread-checkin.md]
version: 1.1.0
status: active
triggers: ["this is a build chat (case-insensitive, very first message only)"]
owner: Charles
updated: 2026-10-21
---

# SKILL: build (v1.1.0)

A **build chat** is work that produces deliverables, decisions, or progress on a project. Fetch every file the `requires:` header names before the first Project State action.

---

## Response format

- A response that needs anything from Charles ends with one numbered list under the exact heading **Needs from you**, preceded by a `---` rule. If nothing is needed, no section.
- Everything that needs him goes on that one list: decisions, approvals, and judgment calls he might want to reverse. Nothing buried in the body.
- Each item is a closed choice with a recommendation.

---

## Authority and hard gates

- **Authority — two modes.** *Interactive chats* (Charles present): Charles is always decider. When a sub-chat hits a fork the Brief didn't pre-answer, it pauses and surfaces the fork in-chat, with a recommendation. *Autonomous execution* (builds run by the orchestration system, no human in the room): the orchestrator decides every fork itself — using the brief's design intent narrative, Project State decisions, and repo conventions — and records each fork and its answer in a fork log. Charles audits the completed build and its fork log afterward; he is never a mid-build tiebreaker. Full rules: `agent-library/skills/design-assist/references/brief-completeness-framework.md`.

**The line between "designing" and "building" is the line for Charles's involvement — and it is firm.** Charles is in the loop during Design Assist and planning: that is where scope is set, forks are his to call, and direction is shaped. **Once a build brief is being executed, Charles is out of the loop until a hard gate.** A build chat executing a brief does not pause to ask Charles about forks, approach, wording, cleanup, ambiguity, or brief-versus-reality conflicts — it decides all of them itself, logs them, and moves forward. The only three things that stop an executing build and bring Charles in: (1) credentials or access only he can supply, (2) spending real money, (3) destroying or irreversibly changing data. Nothing else. This is not "in flux" or a direction being explored — it is the settled operating model. Asking Charles to approve something an executing build could decide for itself is itself a defect (it makes him the bottleneck the whole system exists to remove).

**Automatic data intake follows the same rule.** The ingestion pipelines run on their own — ingesting, adding data, moving forward — without per-item approval. Charles course-corrects from what he observes in the accumulated data, not by approving each addition. "On and running with Charles watching the output" is the target state, not "paused pending Charles's review."

- **Staleness.** A Brief is a creation-time snapshot. When a sub-chat starts, it reconciles against the current Project State DB. If the Brief conflicts with current DB state, the sub-chat escalates rather than following stale guidance. The DB is truth; the Brief is guidance.

**When to use a Build Brief vs. execute inline.** No hard rule yet. When inline feels wrong but no Brief is made, or when a Brief is made but feels like overkill, log the observation as a Learning. A rule will emerge from practice.

---

## Build Brief protocol defaults

- **Brief ID.** Auto-generated as `BB-YYYY-MM-DD-[slug]`. No need to choose.
- **The build number leads the handoff.** When the work belongs to a numbered build series (Build 8.4, Build 11.6, …), that number is what Charles orients by — not the Brief ID, plan id, or project slug. So it appears in two fixed places, every time: as the first line of the Handoff Reference block (`**Build:** 11.6`), and as the opening words of the pasteable prompt (`Build 11.6 — execute Build Brief BB-YYYY-MM-DD-slug. …`). It also leads the plan's `plain_title` ("Build 11.6 — …"), per the naming rule (`references/project-state.md`). All the other identifiers stay exactly as they are; the number sits in front of them. If a brief genuinely has no number in a series, the same first line reads `**Build:** unnumbered` rather than being dropped — Charles should never have to work out which it is. Assigning the number is the authoring chat's job, never Charles's.
- **Builds build the workflow; they don't run it.** A brief that builds a workflow (a job Charles will start from a screen) proves it on a test job the build creates, presses the stop buttons and sends pins itself, and hides the test job afterwards. It never puts Charles's review stops, or a real job's start, inside the build. One-time setup only Charles can do (keys, links, a startup file) stays a hard gate. Charles's first real job is a normal job he starts later.
- **Return contract.** The sub-chat closes with its own Session Log on the same project, referencing the Brief ID. The main chat reads results from the database like any other chat — no special ceremony.
- **Done receipt gate.** Marking a plan succeeded requires a done receipt (Session Log id + every acceptance check passed with evidence or handed off to a new plan); the database refuses otherwise.
- **Advisor-origin closing hook.** A Build Chat executing an advisor-origin brief (its plan carries an `ADV-NNN` tag) closes by writing the **actual response** into `cbrain/docs/advisor/LEDGER.md` — what really landed, if different from the DA chat's intended response — and setting that row's status to `addressed`. This is part of "done," not a follow-up: the LEDGER response is the readable answer that lets the Stack Advisor stop inferring adoption from a `building` status. It rides the existing external-review gate (Reviewing a succeeded plan, below) — a self-certified response is a build defect, caught the same way a self-certified review is.

Templates for the Session Log, Fix Ticket and Build Brief live in `references/project-state.md`.

---

## Shelving a brief

**Shelving a brief (the build queue).** The shelf is Project State: **plans with status `queued`**. The orchestrator pulls the oldest queued plan on a project. Every Build Brief gets four things in the same turn it's authored:

1. **Git home.** Commit the brief to the target project's repo at `docs/design/BB-YYYY-MM-DD-slug.md`. If the build has no target repo, use `chat-protocol/briefs/` instead.
2. **Plan.** `write_plan` on the target project's Project State project. Content is the full brief text; the brief header carries the git fetch path (owner, repo, path) so any chat can find the readable copy.
3. **Status.** When the brief passes the completeness gate and is build-ready, `update_plan_status` → `queued`. Until then it stays `draft`. Queued means on the shelf; nothing else does.
4. **Overnight.** Every brief gets `target_repo` and `after` (may be empty) and an Overnight yes/no tag set at Charles's approval. Daytime build chats check `overnight_line` before claiming: after 11 pm Indianapolis time, a tagged brief is left to the runner (skill `night-run`, `agent-library/skills/night-run/SKILL.md`). (Build 26, BB-2026-10-04-night-builds, 2026-10-04.)

Interactive handoff (pasting a prompt into a sub-chat) still works — but the pasteable prompt instructs the sub-chat to fetch the brief from its git home rather than trust pasted text. The plan is the authoritative queue entry; the git copy is the durable, human-readable one. Keep them in sync via `update_plan_content` when a brief is amended.

---

## Reviewing a succeeded plan

**Reviewing a succeeded plan (the review gate).** A plan that reaches status `succeeded` is not finished — it's *unreviewed*. Before it counts as done, a DA/planning chat audits it: verifies the executor's claims against live code/data (not just the report), disposes of every disclosure the build posted (`list_judgment_calls` → `dispose_judgment_call`), and fills in or fixes any missing or weak plain labels (a nameless item gets named here at the latest — never by Charles). Only then does the reviewing chat call `review_plan`. **The reviewer must be external.** The chat that executed the build — including any of its subagents — never calls `review_plan` on its own plan and never disposes its own disclosures; a build's disclosures close at status `noted`, awaiting the external pull. A build that ends with its disclosures already `reviewed-agree` or its plan's review fields already populated has **self-certified — a build defect**: the reviewing DA chat redoes the review for real and logs the defect. DA/planning chats pull succeeded-and-unreviewed plans (status `succeeded`, `reviewed_at` null) at session start, alongside the disclosure inbox — the same intake moment, two lists.

---

## Workflow

Every session that touches Project State follows this loop:

1. **Identify** — Claude identifies what needs to be logged, or what broke.
2. **Propose** — Claude produces the appropriate ticket as an artifact. Plain English. Specific about what Claude will do and what Charles needs to do.
3. **Review** — Charles reviews in chat. Edits wording, adjusts buckets, removes items, approves.
4. **Execute** — Once approved, Claude runs the actual Project State commands (or ships the fix).
5. **Close the ticket** — Claude updates the Result/Resolution section on the artifact with what actually happened.

### Ticket closure rule

**A ticket closes clean, or it doesn't close.** If a caveat, problem, or unresolved item comes up during execution, Claude does **not** write it into the Result/Resolution section as an open caveat. Instead:

1. Claude pauses and raises the caveat in chat.
2. Charles and Claude discuss it until it's resolved.
3. Once resolved, Claude completes the Result/Resolution with the outcome reflecting that resolution.

Tickets have no "open items" field. If something is open, the ticket isn't done. Reports are conclusions, not status updates with loose ends.

---

## Check in (Next steps list)

At the end of every turn, check in per `references/thread-checkin.md`: one Project State `checkin` call with kind `build-chat`, thread_key `build-chat:<plan slug>`, project_label = the project in plain words ("cbrain", "Family arcade"), a 3-6 word plain_name, and a next_step Charles can act on cold (no ids or codes). Same thread_key every turn; if nothing moved, send the same next_step. **Close:** when the plan has succeeded and its needs-charles items are done, call `close_thread` with closed_how "plan done". Nothing else closes it. If the check-in fails, carry on; the 5 am sweep backfills. **Interactive chats only** (Charles present). Autonomous and overnight builds do not check in; the sweep reads their plans and night log.

---

## Build execution — tool-first

1. Build and planning chats are MCP- and tool-first: Claude takes over as many build tasks as available tools allow, rather than handing instructions to Charles.
2. Supabase MCP (projects, migrations, tables, keys) · Custom GitHub MCP (repos, commits, PRs) · Vercel MCP (deploys, env vars, logs) · Context7 MCP (current library docs before writing code).
3. Plans, specs and Build Briefs name the specific MCP for each step, with the parameters that step needs; never tell Charles to do by hand what an MCP can do.
4. When a needed MCP is unavailable or fails, flag the gap and fall back to instructions. Tool execution is the default; manual handoff is the exception.

---

## Standing build rules

- **Judgment calls get provenance.** Any decision Claude makes on judgment — rather than explicit direction from Charles or a brief — is logged as a Decision with provenance marking it Claude-decided and the tag `judgment-call`, naming the basis (brief intent, standing convention, or inference). In autonomous builds this lives in the fork log; in interactive chats it rides the session's normal Session Log.
- **Builds keep the Stack Flow current.** Any brief that adds, removes, renames or re-routes a running part carries a Stack Flow step that edits `concepts/stack-map.md` (dots, lines, side-panel text) in the same build. A brief that changes nothing on the diagram says `Stack Flow: no change` and why, in one line. Standing authorization from Charles, 2026-10-07; it replaces the old "sessions never edit it" rule. The Rules Inspector still compares the map to what shipped each week and files anything missed on the Punch List. (cbrain holds the canonical stack-map — `get_entity('stack-map')` — which backs the Stack screen; map suggestions as MAP-EDIT next moves stay retired. See "The Punch List" in `references/project-state.md`. BB-2026-10-07-stack-flow-return-lines, Build 11.7.12.)

---

## Changelog

- **1.0.0** (2026-10-15) — Created by Build 39 (BB-2026-10-14-protocol-retirement) from the build-chat sections of the retired chat-protocol rulebook: authority and hard gates, Build Brief defaults, shelving, review gate, workflow, tool-first execution, and the Response format. Shared Project State vocabulary moved to `references/project-state.md`; tool gotchas to `references/gotchas.md`.
