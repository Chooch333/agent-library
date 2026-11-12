# Build Brief — BB-2026-11-12-funnel-advisor-seats

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-12-funnel-advisor-seats.md`
**Project State plan:** `7595449f-e2f8-41f3-9993-13f1ca1d9fc9` on `total-harness`
**Build:** 85
**Skills:** orchestrate-build
**Seated:** revision 2, report TH-200, seats c-stack, lanes, oversight, data-homes, github-integrations, ai-system-design
**Stack Flow:** edits the Stack Advisor dot's side panel (experts judge its ideas; the critic step removed) and adds the line Expert bench → Stack Advisor (field notes feed its ideas) if missing.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also writes Chooch333/cbrain `docs/advisor/` files) · **after:** Build 83
**Cost:** subscription only. At most 3 seats per Advisor run (≈ 570k tokens), three runs a week ≈ 1.7M tokens a week **[assumed: plan headroom is unreadable]**.

**What this is:** Fourth of four alignment-funnel builds. The Stack Advisor's ideas pass the matching expert before they reach Charles, the experts' own reading feeds the Advisor, and the critic that never ran is removed.
**What I'll do (build chat):** the five steps below.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-12 (frozen; TH-199 item 6)
> Accepted: "joining the Stack Advisor with the experts" — ideas pass the matching expert before reaching Charles; expert field notes feed the idea pool.

## Current state going in (checked 2026-11-12)
- **[verified]** stack-advisor 2.2.0: step 4b shelves at most 2 Done-for-you briefs a run on cbrain (tag `advisor-auto`, overnight, queued); step 6 checks `cbrain/docs/advisor/critic_live.json` and, when present, stops at a draft for the Advisor Critic. The file is absent; the critic has never run. The skill names neither the charter nor the experts. Its wiring says `runs_in: cowork`; the stack map says it is a Claude Code scheduled task (Mon/Wed/Fri 3 am).
- **[verified]** The ledger already has a `cut` status the critic used for rejected ideas, and contract item 8 bars a veto on "nothing says he wants it".
- **[assumed]** Whether the Stack Advisor's scheduled session has the helper tool: unproven (the Night builds session has it, EB-072; each task's tool set differs, CB-600).
- **[verified]** After Build 83, an `advisor-auto` brief without the seated marker is seated by the night session before it builds, so Done-for-you work is covered even if the Advisor cannot seat.
- **[verified]** Expert CE files `field-note`s on `expert-bench` weekly (37 by 2026-11-12, TH-197); nothing turns them into a suggestion.

## Scope
**In:** the Advisor's judge; field notes as a source; removing the critic switch; the wiring line.
**Out:** the Advisor's scoring, lanes and email format otherwise; seating ideas inside Expert CE.

## Directive
1. **Probe first** (stack-advisor, new first line of step 4): check that the session has the Agent tool. None → write `seats: unavailable` in `run_result.json` and go on exactly as today (the night session seats Done-for-you briefs before they build); no error, nothing to Charles.
2. **Experts judge the ideas** (stack-advisor step 4, replacing the critic hand-off): group the run's surviving ideas by the expert whose call_when best matches (`experts/INDEX.md`); one Expert Desk seat per group, mode B, at most 3 seats a run (the largest groups first; the rest go out unjudged and say so in their block). Seat prompt: the ideas, their ADV blocks, contract item 8 ("no veto because nothing says he wants it") as Already decided. A rejected idea is written through `run_result.json` as `cut` with the seat's reason as its Response; a sharpened idea is rewritten; a Done-for-you brief the seat passed gets tag `experts-seated` and the provenance line `Seated: revision 1, report <note id>, seats <slug>`. The desk files its report note on cbrain (tag `expert-desk-report`).
3. **Field notes feed the pool** (stack-advisor step 1, its reading): read `field-note` notes on `expert-bench` (exact tags) created after `run_result.json`'s `field_notes_read_through`, at most 10, oldest first; treat each as a source item; store the newest `created_at` read as the new `field_notes_read_through`.
4. **Remove the critic switch**: delete the Job boundary bullet about the critic, the "The Advisor Critic grades" opener, 4b's "while the critic is live", and step 6's Present branch; step 6 delivers directly. Set `skills/advisor-critic/SKILL.md` `status: retired` with a changelog line naming this build. Fix the wiring line to `runs_in: claude-code-cloud` (scheduled task). Version bump stack-advisor, changelog line in `references/changelog.md`.
5. **Stack Flow**: the Stack Advisor dot's side panel says ideas are judged by the matching expert before the email and that field notes are read; remove critic mentions.

## Acceptance
1. stack-advisor reads as steps 1–4; no "critic_live" left outside changelogs (`grep`).
2. advisor-critic is `status: retired`.
3. `run_result.json`'s documented shape (cbrain `docs/advisor/README.md`) gains `seats` and `field_notes_read_through`.
4. The Stack Advisor dot's side panel reads as step 5.
5. Handed off if not provable tonight: the next Advisor run's `run_result.json` shows `seats` (a number or `unavailable`) — a draft follow-up plan "Build 85.1: first judged Advisor run".

## Decisions
- [Charles] Advisor ideas pass the matching expert before reaching him; field notes feed the pool (TH-199 item 6).
- [Claude-per-doctrine] One seat per expert corner across the run, at most 3, not one per idea. Seats split: c-stack and ai-system-design suggested Done-for-you only; that leaves emailed ideas unjudged, against item 6. ≈ 1.7M tokens a week instead of ≈ 3.4M.
- [Claude-per-doctrine] Rejections use the existing `cut` path; the critic is retired, not kept dormant ("each addition replaces something"). Seat: ai-system-design.
- [Claude-per-doctrine] No separate end-of-work review job: Build 83's after-build seat reviews every build, and AGENT.md's clause seats every harness change in any chat. Known gap: chats in Projects whose instructions don't fetch AGENT.md.

## Pasteable prompt
> Build 85 — execute Build Brief BB-2026-11-12-funnel-advisor-seats. Pull the plan from Project State (plan_id 7595449f-e2f8-41f3-9993-13f1ca1d9fc9, project total-harness, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-12-funnel-advisor-seats.md. Build 83 (night seats) must have landed. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
