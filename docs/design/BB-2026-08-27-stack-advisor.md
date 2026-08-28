# Build Brief — BB-2026-08-27-stack-advisor

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-08-27-stack-advisor.md`
**Project State plan:** `c04b5bfe-4a6c-4394-8571-b9a84018d5ce` on `stack-map`

**What this is:** The **Stack Advisor** — a recurring agent that stays aware of what Charles is building, combs the world graph's parsed data, and delivers a brief 3×/week (Mon/Wed/Fri, up to 6 never-padded ideas) proposing upgrades to the tech stack or process. Asks Charles via a Questions section when build intent is unclear; never blocks on the answer. Resolves platform decision D5.

**What I'll do (build chat):** Ship `roles/stack-advisor/SKILL.md` to agent-library (final version of the draft below), scaffold `docs/advisor/` + `LEDGER.md` in cbrain, and deliver Charles a setup card with the exact scheduled-task prompt. No code. No new credentials.

**What you'll do (Charles):** One ~10-minute step after the build ships — create the Cowork scheduled task from the setup card (login-tied; the one hard gate).

---

## Current state going in

- ✓ **Graph read path works:** dispatching `query.yml` on `Chooch333/world-graph` with a question answers from graph content only and commits the answer to `answers/`. Verified by reading the workflow this session.
- ✓ **Read limitation accepted for v1:** the query tool sees only the world-knowledge section of the graph, not per-project sections (WG-050).
- ✓ **Data is thin today:** phone-tap YouTube proven end-to-end 2026-08-27; email intake live; RSS channel-following dead pending WG-062. Early briefs may be short or empty — accepted by design [Charles]. Value ramps as channels connect (incl. the future Anthropic-releases channel).
- ✓ **Awareness sources exist:** Master Roadmap (`31fdcb9b`), Build Map Skeleton (`076b64ca`), the shelf (queued/running plans, all projects), `get_activity`, `get_entity('stack-map')`. Read live every run; nothing cached ("derived, never copied").
- ✓ **Stack Manager boundary:** Manager = librarian (MAP-EDIT queue, map accuracy). Advisor = scout (proposals). This build extends, never modifies.
- ✓ **Venue verified (docs search 2026-08-27):** Cowork scheduled tasks run in Anthropic's cloud (fire with the computer off), each run a fresh session with the account's connectors and skills, managed from the Scheduled sidebar.
- ~ Corrected stale memory: no `_stack/suggestions/` folder in cbrain; MAP-EDIT queue lives in Project State.

---

## Receiving chat

New autonomous build chat (standard shelf pickup). Charles-only setup step at the end via the delivered setup card.

## Scope

**In scope:**
1. `Chooch333/agent-library` → `roles/stack-advisor/SKILL.md` — finalize the draft below (frontmatter, wording pass, changelog). **[M · $0]**
2. `Chooch333/cbrain` → `docs/advisor/README.md` (one-paragraph folder purpose) + `docs/advisor/LEDGER.md` (headers + format line, empty table). **[S · $0]**
3. Setup card for Charles: exact Cowork scheduled-task creation steps + the paste-in task prompt (draft below), including the Mon/Wed/Fri fallback (three weekly tasks if the picker lacks a tri-weekly option). Deliver as a committed file `docs/advisor/SETUP.md` in cbrain and reference it in the closing disclosure. **[S · $0]**
4. Exit wiring is DONE by the DA session (not this build): D5 decision logged, venue-rule decision logged, Master Roadmap + Build Map Skeleton updated. The build must not repeat these writes.

**Out of scope:** Creating the scheduled task (Charles-only). Web search as an idea source [Charles]. Any change to world-graph code incl. `query.py`/WG-050. The Stack Manager role and `concepts/stack-map.md`. The MAP-EDIT queue. The personal feed (L4) — briefs migrate there when it ships. Auto-implementing ideas — the advisor proposes only.

**Real-money cost:** $0 new. Per advisor run: one scheduled session on Charles's plan + 1–3 query workflow runs on the existing capped world-graph API key (~cents, assumed, capped regardless).

---

## Directive (for the build chat)

1. Commit `roles/stack-advisor/SKILL.md` to `Chooch333/agent-library` (Custom GitHub `create_or_update_file`), content = the draft below finalized. Read back to verify.
2. Commit `docs/advisor/README.md` and `docs/advisor/LEDGER.md` to `Chooch333/cbrain`. LEDGER format (the contract — advisor reads/writes it every run):
   `| ADV-NNN | YYYY-MM-DD | one-line idea | status |` — statuses: surfaced / interested / building / declined. Read back to verify.
3. Commit `docs/advisor/SETUP.md` to `Chooch333/cbrain`: the setup card (steps + task prompt + Mon/Wed/Fri fallback). Read back to verify.
4. Close per protocol: fork log, disclosure via `post_judgment_call` if any judgment calls were made, `update_plan_status` → succeeded with executor report, Session Log on `stack-map`.

### Draft scheduled-task prompt (goes in SETUP.md; the task Charles creates)

> This is a Stack Advisor run. Fetch roles/stack-advisor/SKILL.md from Chooch333/agent-library via the Custom GitHub connector (get_file_contents, owner=Chooch333, repo=agent-library, path=roles/stack-advisor/SKILL.md) and follow it end to end. Deliver the brief exactly as the skill instructs. If the skill cannot be fetched, email Charles that the run failed at fetch and stop.

### Setup card steps (goes in SETUP.md)

1. Open Claude → Scheduled (left sidebar) → New task.
2. Paste the task prompt above. Name it "Stack Advisor".
3. Schedule Mon/Wed/Fri, morning. If the schedule picker offers no tri-weekly option, create the same task three times as weekly (one each for Mon, Wed, Fri) — identical prompt.
4. Save. Optionally hit "run now" once as the smoke test — the first brief email is the pass signal.

---

## Acceptance criteria

1. First scheduled run completes unattended: brief committed to `cbrain/docs/advisor/`, LEDGER updated, email delivered, stack-map note written. *(Verification run = the first real run after Charles creates the task; the task's existence is the named gated dependency.)*
2. Every idea traceable to a named, labeled trigger — a graph answer file or a specific Project State/roadmap item. No web- or memory-sourced ideas.
3. No idea duplicates a prior LEDGER entry (unless status/evidence changed, stated as such).
4. "Questions for Charles" section present when build-intent confidence is low, absent when it isn't.
5. Charles's email-reply dispositions to brief N appear in LEDGER by end of run N+1.

---

## Inputs

- [verified] `Chooch333/chat-protocol/PROTOCOL.md`; `Chooch333/agent-library/roles/stack-manager/SKILL.md` (boundary reference — do not modify)
- [verified] Master Roadmap plan `31fdcb9b-3dd7-4c6c-8049-7362d91e746f`; Build Map Skeleton `076b64ca-3879-4a9e-b0e3-95c1c435ec6f` (platform-program)
- [verified] `Chooch333/world-graph/.github/workflows/query.yml` + `questions.md` (answer-format precedent)
- [verified] MCPs: Project State, cbrain, Custom GitHub, Supabase (shelf-query fallback), Gmail

---

## Completeness — eleven domains

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered | §What this is (personal daily-use advisory loop; sole user Charles, reads by email) |
| 2 Acceptance criteria | Answered | §Acceptance (verification run named, its dependency gated) |
| 3 Runtime & execution | Answered | Cowork scheduled task, cloud, Mon/Wed/Fri; run = fetch skill + follow; no code |
| 4 Data — schema | Answered | LEDGER row format (§Directive 2); brief files ADV-YYYY-MM-DD.md |
| 5 Data — storage & recall | Answered | GitHub markdown in cbrain docs/advisor/; recall = exact file reads; PS note as digest |
| 6 Interconnectivity | Answered | Reads PS/cbrain/GitHub/Supabase/Gmail; writes GitHub/PS-note/Gmail; dispatches query.yml. Failure = no brief email; absence of the Mon/Wed/Fri email is itself the breakage signal, plus Scheduled-screen run history. Each run stateless; next run self-heals. |
| 7 Access & hard gates | Answered | Touch only roles/stack-advisor/, cbrain docs/advisor/, world-graph dispatch + answers/ reads. Never stack-map.md / MAP-EDIT. Hard gate: task creation (Charles login). |
| 8 Skills & tools | Answered | Skill = the shipped SKILL.md; every step names its tool |
| 9 Sequence & dependencies | Answered | No upstream plans; skill → scaffold → setup card; standard staleness rule |
| 10 Assumptions & risks | Answered | §Appendix (connector fleet at runtime; cents-level query cost; thin-graph emptiness accepted) |
| 11 Design intent narrative | Answered | below |

### Design intent narrative

This advisor exists so good ideas stop depending on Charles noticing them. The shape was chosen to add zero infrastructure: every capability it needs already exists (graph query workflow, Project State, Gmail, scheduled tasks) — the build is almost entirely *writing the operating manual well*. Protect these qualities when trade-offs appear: (1) **honesty over volume** — an empty brief beats a padded one, always; (2) **evidence over eloquence** — an idea without a named trigger from the graph or Charles's own records does not ship, however clever; (3) **propose, never act** — the advisor's authority ends at the email; (4) **read live, cache nothing** — Charles's records are always fresher than any copy; (5) **plain English** — Charles is not technical, one technical clause per idea. If the graph is silent for weeks, that is the system working, not failing. Prefer boring reliability over cleverness everywhere.

---

## DRAFT — roles/stack-advisor/SKILL.md

```markdown
---
name: stack-advisor
version: 0.1.0
status: draft
triggers: ["Stack Advisor run"]
owner: Charles
source: BB-2026-08-27-stack-advisor (DA session 2026-08-27)
---

# Stack Advisor

## What
Every scheduled run, understand what Charles is currently building, comb the
world graph's parsed knowledge, and deliver a brief of up to 6 concrete
upgrade ideas for the stack or the process. Propose only — never build,
never edit the stack map (that is the Stack Manager's job).

## Job boundary
- Stack Manager = librarian (keeps the map accurate). Stack Advisor = scout
  (proposes improvements). Never dispose MAP-EDIT items; never edit
  concepts/stack-map.md.
- Accepted ideas leave through the normal door: Charles takes them to a
  DA chat, which produces a Build Brief. The advisor never queues plans.

## Each run, in order
1. FEEDBACK FIRST. Gmail: find Charles's reply to the most recent advisor
   brief email (subject prefix "Stack Advisor brief"). Record each
   disposition in cbrain docs/advisor/LEDGER.md (statuses: surfaced /
   interested / building / declined). Commit. No reply = no change.
2. ORIENT — read live, keep nothing cached:
   a. Project State plan 31fdcb9b (Master Roadmap) — the five-layer map
      and open decision queue.
   b. Plan 076b64ca (Build Map Skeleton) — what's built vs in flight.
   c. The shelf: plans with status queued or running across all projects
      (Supabase SQL join plans→projects is the reliable pattern).
   d. get_activity, all projects, last 7 days.
   e. cbrain get_entity('stack-map') — the canonical component list.
   f. docs/advisor/LEDGER.md + the previous brief.
3. READ THE GRAPH. Dispatch Chooch333/world-graph workflow query.yml
   (workflow_id "query.yml", ref "main" — ref is mandatory) 1–3 times with
   questions shaped by the current shelf. Wait for runs to finish; read the
   new files in answers/. Graph answers are grounded-only; treat "the graph
   doesn't know" as a real answer.
4. GENERATE up to 6 ideas. Hard rules:
   - Permitted triggers, exactly two kinds: a graph answer file, or a
     specific item in Charles's own recorded state (shelf plan, roadmap
     line, activity event, stack-map component). The best ideas connect
     one of each. FORBIDDEN: web search, and general model knowledge —
     if it is not in the graph or in Charles's records, it is not usable.
   - Nothing from the ledger repeats unless status changed or new evidence
     arrived (say what changed).
   - Each idea: what it improves · which live component/process it touches ·
     effort S/M/L · evidence trigger · confidence label.
   - Never pad. Zero ideas is a legal brief ("nothing met the bar; graph
     volume still low") — expected in the early weeks while channels fill.
5. ASK IF UNSURE. If the purpose of a current build can't be stated
   confidently in one sentence, add a "Questions for Charles" section —
   max 3, closed choices with a recommendation each. Never block on them.
6. DELIVER, four writes:
   a. Commit brief → cbrain docs/advisor/ADV-YYYY-MM-DD.md (read back to
      verify, per write-before-done).
   b. Update LEDGER.md with the new ideas (status: surfaced).
   c. Gmail send to Charles — subject "Stack Advisor brief ADV-YYYY-MM-DD",
      full brief in the body, git path at the bottom.
   d. Project State note on stack-map: one-paragraph digest + git path.

## Brief format
Subject line · ideas numbered with their ADV-NNN IDs · Questions for
Charles (if any) · one-line "what I read this run" provenance footer.

## Language
Plain English. Charles is not technical. One technical clause per idea, max.
```

---

## APPENDIX — decisions & assumptions (Forks and Gated: empty — build-ready)

### Decisions made
- **Idea sources: graph + Charles's own records only. No web search, no model memory.** Early empty briefs accepted. **[Charles]**
- **Cadence: 3×/week Mon/Wed/Fri from the start.** **[Charles]**
- **Runner: Cowork scheduled task** (knowledge job → Cowork surface). **[Charles]**
- **D5 resolved by this design**; Stack Manager stays the standalone librarian. **[Charles]**
- Scheduled-job venue rule narrowed platform-wide: code jobs → Claude Code scheduled tasks/Routines; knowledge jobs → Cowork scheduled tasks. Logged on platform-program. **[Charles]**
- New role, separate from Stack Manager (extend, don't modify). **[Claude-per-doctrine]**
- Read-live awareness, no cached model. **[Claude-per-doctrine]**
- Propose-only; accepted ideas route through DA → Build Brief. **[Claude-per-doctrine]**
- Delivery = email + git archive + stack-map note; migrates to personal feed at L4. **[Claude-per-doctrine]**
- Up to 6 ideas, never padded; zero legal. **[Claude-per-doctrine]**
- Feedback via email-reply parsing next run; "tell any chat" fallback. **[Claude-per-doctrine]**
- "Just the graph" interpreted as banning outside sources (web/model memory), not Charles's own Project State — which he required the advisor to watch. **[Claude-per-doctrine]**

### Assumptions (genuinely unverifiable now)
- Scheduled runs under Charles's account carry his full connector fleet (docs confirm connectors are available to scheduled tasks; the specific fleet confirms at first run).
- Per-query graph cost stays at cents level under the existing cap (observed at first runs).
- Mon/Wed/Fri exists in the schedule picker (fallback drafted: three weekly tasks).

---

## Pasteable prompt

> Execute Build Brief BB-2026-08-27-stack-advisor. Pull the plan from Project State (plan_id c04b5bfe-4a6c-4394-8571-b9a84018d5ce, project stack-map, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-08-27-stack-advisor.md. No upstream plan dependencies. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this build — the scheduled-task creation gate belongs to Charles after you close). Do not repeat the exit wiring (D5 decisions, roadmap edits) — the DA session already shipped those.
