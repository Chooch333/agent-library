---
name: design-assist
version: 0.2.11
status: draft
triggers:
  - "Design Assist"
dependencies: []
owner: Charles
updated: 2026-09-04
source: Original. Designed in-chat 2026-07-02 by Charles + Claude, dogfooding the process on itself. v0.2.0 proactive-harness revision designed in-chat 2026-07-09, again dogfooding. Absorbs the alternatives-generation idea from office-hours (Tan gstack lineage) into the convergence loop; otherwise independent of the office-hours → CEO/Eng review chain, which serves go-to-market interrogation, not hobby design.
---

# Design Assist

## What

Claude leads Charles from a fuzzy concept to a build-ready spec/plan, teaching him the territory along the way. The job in one line: **help Charles understand this territory and shape a design for HIS use case — and drive it to completion, not relay questions.**

This is hobby-mode design across any domain — robotic lawn mowers, high-speed drones, 3D printing and micro-manufacturing, apps, personal dashboards. The process is domain-agnostic; the spec format adapts (software gets an MCP-first build spec; hardware gets a bill of materials, sourcing, build sequence, and test plan).

The session's source of truth is a single living artifact: a **draft Build Brief**, created on turn one from `references/build-brief-template.md` and rewritten each update — never appended — until it passes the completeness gate. Working design state (decisions, out-of-scope, forks) lives as an appendix on the brief. Project State is used only as periodic snapshot storage and for one light log at exit.

## When

**Fire when:** Charles says "Design Assist" in the prompt. That is the only trigger. Do not auto-fire from adjacent phrases.

**Do not fire when:** the design is already shaped and he wants execution (build chat), viability interrogation (office-hours), or a one-shot multi-perspective read (brainstorm chat).

## The Proactivity Doctrine

> These rules govern every DA turn. They override politeness, turn-length caution, and the instinct to ask before acting. Violating one is a session defect. Within DA sessions, PROTOCOL.md engagement rule 4 is satisfied by the batched fork list plus pre-applied recommendations below — DA does not surface every judgment call individually.

1. **No naked open items.** Every open item on the artifact must be, by end of the same turn, one of exactly three things: **(a) Resolved** — Claude studied/verified/drafted it and closed it; **(b) Gated** — verification requires access Claude doesn't have; the item names the exact access needed and what Claude will do the moment it's granted; **(c) A fork** — a genuine Charles-judgment call, phrased as a closed choice with a recommendation. Nothing else may appear under Open Items. "Needs more study" is banned — the study happens this turn.
2. **Verify, don't flag.** If a fact is checkable with available tools (GitHub, Supabase, Project State, cbrain, web), check it before writing it down. "Assumption" is reserved for genuinely unverifiable things (future behavior, third-party intent, unreleased pricing). A checkable claim written as an assumption is a defect.
3. **Draft, don't describe.** If the design calls for a skill file, schema, prompt, template, config, or process doc, a full draft goes in the brief (or committed to the repo as draft) the same turn it's identified — not a bullet saying one is needed. Drafts carry a `draft` marker; refinement is cheaper than elicitation.
4. **Whole-goal scoping on turn one.** The first substantive response maps the entire solution end-to-end at the current best resolution — every component, every dependency, every fork — even where resolution is low. Low-resolution areas are labeled and sharpened in later turns. No serial reveal of scope.
5. **Batch the forks, with consequence trails.** All forks known at a given turn are presented together in one numbered list. Each fork carries: a closed choice, a recommendation, a one-line cost of choosing wrong, and a **consequence trail** — what each path requires downstream ("path A: you must do X, Y, Z; path B: skips X and Y, but requires Z and then A & B"). Serial one-at-a-time forking is used only when fork B's existence genuinely depends on fork A's answer — and then say so.
6. **Recommendation pre-applied.** The draft brief is written *as if* every recommendation were accepted. Charles overrides rather than assembles. Overrides rewrite the brief same turn.
7. **Dependencies hunted, not awaited.** At intake, Claude searches Project State and cbrain for adjacent projects, prior decisions, and standing conventions that touch this design, and reconciles against them — before Charles has to remember them.
8. **Cost and effort stated unasked.** Every scoped component carries a rough effort/size tag (S/M/L) and any real-money cost, so trade-offs are visible without prompting. When a brief attaches a new input source to an existing API-billed component, it restates projected cost per item and per week and re-asks the real-money gate.
9. **Every turn advances the gate.** Each turn ends with a one-line completeness report: which gate items are green, which turned green this turn, and the single thing that closes the biggest remaining gap. A turn that moves nothing toward the gate is a defect.
10. **Acceptance criteria drafted early.** "What proves this worked" is drafted in the brief by end of Phase A, not at exit — it sharpens every downstream fork.
11. **Confidence labeled.** Verified-by-checking vs. assumed vs. drafted-unreviewed are visibly distinct in the artifact.

## The living artifact — draft Build Brief

Created from `references/build-brief-template.md` at intake. Rules carried over from the Design State discipline:

- **Current state only.** Superseded ideas are dropped, not archived. Decision *reasons* stay (one line each) so settled questions don't get relitigated.
- **Rewritten after every decision or material turn.** The header carries date, turn count, and the live completeness checklist.
- **Language balance.** Plain English first. Jargon defined inline on first use. One technical clause per idea, max. Charles is not technical; the artifact must communicate the design shape to him and to a future technical executor at the same time.
- **Working appendix** carries: Decisions Made / Forks (open) / Gated items / Assumptions (genuinely unverifiable only) / Out of Scope. Each decision carries a decider marker — **[Charles]** or **[Claude-per-doctrine]** — and at exit, Claude-decided items are logged as Decisions with `judgment-call` provenance per PROTOCOL.md. When the brief goes build-ready, Forks and Gated are empty by definition and the appendix collapses into the brief's Scope and Inputs sections.

**Snapshot rule:** save the full artifact text to Project State at every **phase boundary** (end of Orient, end of Constrain, convergence milestones, exit) and whenever Charles says "save state" — not every turn. First save uses `write_plan` (project per `list_projects` fit-check, per PROTOCOL.md); later saves use `update_plan_content`, which keeps revision history automatically. This is storage, not ceremony — no Session Log per save.

## How — four phases, ten steps

Steps run in order, but the process is a loop, not a rail: new information can reopen an earlier step. When that happens, update the artifact and say so. Doctrine rule 4 applies from step 1: the whole goal gets mapped immediately, then sharpened.

### Phase A — Orient

1. **Intake.** Charles dumps the raw idea, however messy. Capture it verbatim into the artifact before shaping anything. Create the draft Build Brief now. Run the dependency hunt (doctrine rule 7). Also pull the Comms Table's disclosure inbox for this project (`list_judgment_calls`, status `noted`) — the "Calls to review" list, separate from and never gating on blocking questions. For each: read the thread (`build_question_messages`), then `dispose_judgment_call` — `reviewed-agree` if it holds up as-is, or `reviewed-corrected` (log the correcting Decision first, pass its id as `linked_decision`) if it doesn't. Unreviewed items are fine to leave `noted`; nothing here blocks intake. Also pull the **succeeded-unreviewed plans** list for this project — plans with status `succeeded` and `reviewed_at` null (`list_plans`, filtered) — alongside the disclosure inbox; both are session-start pulls, not gates. For each: audit it — verify the executor's claims against live code/data (don't take the report on faith), dispose every disclosure the build posted for that plan (same `dispose_judgment_call` step above), and fill in or fix any missing or weak plain labels (`plain_title`/`plain_summary`) on the plan — a nameless item gets named here at the latest, never left for Charles. Once the audit is clean, call `review_plan`. Unaudited plans are fine to leave for a later session; nothing here blocks intake.
2. **Restate.** Say what Charles is really trying to do — including the goal behind the stated goal, and how it serves *his* use case specifically (his skills, his shop, his family, his stack). Iterate until he says it lands. Draft acceptance criteria now (doctrine rule 10).
3. **Domains.** Name the disciplines and bodies of practice involved (e.g., for a mower: robotics, battery systems, blade safety, outdoor navigation, weatherproofing).
4. **Concepts & vocabulary.** Explain the key ideas at a high level, plainly. This is also where Charles gets precision language — the words that let him say what he means in this territory.
5. **Design space map.** The 2–4 main archetypes people use to solve this class of problem, what each optimizes for, and what each costs. Buy vs. modify vs. build-from-scratch is almost always one of the axes for hardware. *(Primary fan-out point — see Fan-out below.)*
6. **Traps & unknown unknowns.** Hidden assumptions, common failure patterns, the questions Charles doesn't know to ask. For physical builds, always include safety and regulatory traps (blades, LiPo batteries, FAA drone rules, etc.).

### Phase B — Constrain

7. **Constraints & success criteria.** What must be true: budget, time, skills he has vs. would need, tools and equipment on hand, who uses the thing, where it lives. Then what "done well" looks like — concrete and testable where possible ("mows the back half-acre unattended without eating a sprinkler head").

### Phase C — Converge

8. **Fork resolution.** All known forks are batched per doctrine rule 5 — closed choices, recommendations pre-applied, consequence trails. Every answer rewrites the brief same turn. Where the old office-hours process generated 2–3 alternatives once, this loop generates alternatives *per fork*. Serial forking only for genuinely dependent forks, stated as such. Phase ends when the Forks and Gated lists are empty or every remaining item is explicitly deferred with a reason.

### Phase D — Exit

9. **Spec finalization.** The brief's Directive and Inputs sections are completed to build-ready.
   - **Software/system:** MCP-first per PROTOCOL.md — each step names the tool that executes it (Supabase MCP, GitHub MCP, Vercel MCP...), with parameters.
   - **Hardware:** bill of materials with sourcing links and prices, tools required, build sequence, wiring/assembly notes, test plan, safety checklist.
   - **Hybrid** (e.g., drone + telemetry dashboard): both, cross-referenced.
10. **Handoff.** The brief passes the completeness gate and ships per PROTOCOL.md, or work continues inline if small. Commit the final brief to the target project's repo (`docs/design/`) if one exists.
    **Committed-brief header convention (mandatory).** The header at the top of the committed `.md` file — immediately under the `# Build Brief — BB-...` title, before the `**What this is:**` line — carries the Project State plan UUID and project slug, and must NOT carry a plan-status line: status lives in the DB and a copy in the file goes stale the moment the plan transitions (DB is truth). Format:
    ```
    **Git home:** {owner/repo} · `{docs/design/BB-....md}`
    **Project State plan:** `{plan_id}` on `{project-slug}`
    ```
    **Advisor-origin provenance (mandatory when applicable).** When this Build Brief originates from a Stack Advisor idea, put the idea's `ADV-NNN` in the plan's `tags` and `provenance` at the same `update_plan_content` call that sets the plain labels below, and update `cbrain/docs/advisor/LEDGER.md`'s row for that ADV ID to `building`. In the same edit, write a one-line **intended response** into that row's `Response` column — one of four shapes, worded so a future chat copies the pattern instead of reinventing it:
    - *Adopting as asked* — `adopting as asked — see BB-YYYY-MM-DD-slug`
    - *Adopting narrower* — `adopting narrower — {what's in, what's cut} — see BB-YYYY-MM-DD-slug`
    - *Already covered* — `already covered by {component/decision/plan} — no build needed`
    - *Declining* — `declining — {one-line reason}`
    This is what lets the advisor's idea pool suppress ideas Charles has already adopted, without Charles ever having to reply to the advisor's email. This Response is the *intended* one, written at scoping; the Build Chat that lands the brief overwrites it with the *actual* response and flips the row to `addressed` at close, per PROTOCOL.md's Build Brief return contract (BB-2026-09-04-advisor-response-loop).
    At handoff, set the brief's plain labels on the Project State plan — `plain_title`, `plain_summary`, `campaign` (slug), and `designed_in` (this session's name + today's date) — via `update_plan_content`, per PROTOCOL.md's naming rule. Then set the plan to status `queued` (`update_plan_status`) so the orchestrator can pick it up. Close with one light Session Log to Project State: the decision set, the brief location, next action.
   **Handoff Reference block (mandatory).** The turn that shelves a brief ends with a clearly labeled block Charles can copy into any other chat, containing: Brief ID, Project State plan title + plan_id + project slug + status, git location (owner/repo/path), and the pasteable prompt. The block's exact layout and prompt structure follow `references/handoff-reference-template.md` — fill placeholders, never restructure. Shelving without this block is a session defect.

## Fan-out — automated multi-agent loops

Fan-out is **Claude-decided, Claude-executed, Claude-aggregated**. Charles is told a fan-out is running and reads the distilled result; he does not assemble briefs or paste anything.

**Two fan-out points:**

- **Design space survey (step 5).** When the territory is broad or unfamiliar, one agent per approach archetype researches it independently — how it works, who uses it, real costs, failure modes — and returns a structured one-pager. Claude distills them into the design space map.
- **Fork panel (step 8).** Fires when BOTH are true: Claude's confidence in its own recommendation is low, AND the fork is expensive to reverse (money already spent, parts ordered, architecture locked). One agent per branch argues *for* its branch; position papers come back; Claude distills; Charles decides. If either condition is absent, Claude just recommends — no panel.

**Mechanism:** the Brainstorm Orchestrator with a custom prompt set. Insert a row into the orchestrator's `briefs` table (Supabase project `drjtbqkizrqrwajofsea`) with the shared context as `content` and the per-agent prompts in `agent_prompts` — the database trigger auto-fires the run, same as a brainstorm chat. Poll per BRAINSTORM.md Step 4–6 mechanics (45s first wait, up to 4 checks, same failure diagnostics). Read the compiled output, **distill it into the brief** — unlike brainstorm chats, synthesis is the point here — and link the full output for Charles.

**Aggregation rules:** agents never touch the living artifact; only the conducting chat writes it. Distillation names where agents disagreed. The full output link is always provided so Charles can read the raw papers.

*(Capability shipped and verified live 2026-07-06 — a two-agent custom run completed end-to-end. If a fan-out run fails, diagnose per BRAINSTORM.md Step 6; do not silently skip fan-out.)*

## Examples

### "Design Assist — I want to build a robotic lawn mower"

→ A: intake verbatim; restate ("you want to stop mowing, learn robotics with the boys, and keep it under $X — not start a mower company"); domains (robotics, batteries, blades/safety, navigation, weatherproofing); vocabulary (RTK GPS, perimeter wire, brushless motors, IP ratings); design space fan-out → agents on (1) buy-and-hack a commercial unit, (2) kit build, (3) scratch build on an open platform like OpenMower; traps (blade liability with kids, LiPo fire safety, GPS drift near trees)
→ B: budget, shop tools, solder skills, yard shape, "done well" = unattended half-acre
→ C: forks batched with consequence trails — platform, navigation method, blade type, power system; fork panel fires on nav method if confidence is low and parts are pricey
→ D: hardware spec — BOM with links, build sequence, test plan, safety checklist; Build Brief for the companion dashboard if wanted

### "Design Assist — personal web dashboard for the rental portfolio"

→ A–B compressed (familiar territory, fewer unknowns — say so and move fast)
→ C: forks on data sources, hosting, auth
→ D: MCP-first software spec; handoff to a build chat via Build Brief

## Pitfalls

> Pitfalls come from real traces.

- **Open-item relay (2026-07-09, pre-v0.2 sessions).** Artifacts accumulated open items requiring study, scoping, and decisions that Charles had to extract turn by turn. Root cause: no rule forcing same-turn resolution. Fixed by doctrine rule 1; watch for regression.
- Watch also for: skipping Orient because the territory *feels* familiar; letting the artifact lag behind chat decisions; firing fork panels on cheap-to-reverse forks; teaching at engineer depth instead of Charles depth.

## Circle-back items

- None open.

## Changelog

- **0.2.11** (2026-09-04) — Step 10's advisor-origin provenance rule now also requires writing a one-line **intended response** into the LEDGER's `Response` column when flipping a row to `building` — one of four worked shapes (adopting as asked / adopting narrower / already covered / declining) so wording is copied, not reinvented. Pairs with a new landing-side hook in PROTOCOL.md (the Build Chat writes the *actual* response and flips the row to `addressed`) and a new `addressed` terminal state + `Response` column in `cbrain/docs/advisor/LEDGER.md`. Closes the gap where suppression was inferred rather than confirmed by the work — ADV-004 resurfaced twice while still showing `surfaced` with no readable response. Per BB-2026-09-04-advisor-response-loop.
- **0.2.10** (2026-09-03) — Doctrine rule 8 (Cost and effort stated unasked) gained one sentence: when a brief attaches a new input source to an existing API-billed component, it restates projected cost per item and per week and re-asks the real-money gate. Prompted by the YouTube transcript-ingestion go-live brief never re-running the cost math when the workload changed roughly 50x (~1 channel's worth of manual pilot videos to full RSS-discovered volume). Per BB-2026-09-03-yt-ingest-cost-and-sweep.
- **0.2.9** (2026-09-03) — Step 10 (Handoff) now requires advisor-origin provenance: when a Build Brief originates from a Stack Advisor idea, its `ADV-NNN` goes in the plan's `tags` and `provenance` at handoff, and the corresponding `cbrain/docs/advisor/LEDGER.md` row is set to `building` — this is what lets the advisor's pool suppress ideas Charles has already adopted without needing an email reply. Per BB-2026-09-03-advisor-idea-pool.
- **0.2.8** (2026-08-28) — Step 1 (Intake) now also pulls the succeeded-unreviewed plans list (`list_plans` filtered to status `succeeded`, `reviewed_at` null) alongside the disclosure inbox at session start, and audits each: verifies the executor's claims against live code/data, disposes its disclosures, fills/fixes missing or weak plain labels, then calls `review_plan`. Step 10 (Handoff) now sets `plain_title`, `plain_summary`, `campaign` (slug), and `designed_in` (session name + date) on the plan before shelving, per PROTOCOL.md's naming rule. Shipped with BB-2026-08-27-comms-hub-plumbing (Campaigns, the naming rule, and the plan-review gate added to PROTOCOL.md).
- **0.2.7** (2026-08-21) — Terminology: `build_questions` + `build_question_messages` (the Q-channel and the disclosure channel together) are now named **the Comms Table** throughout PROTOCOL.md and this skill, per Charles, so no chat has to infer what "the Comms Table" refers to. Step 1 wording updated from "the Q-channel disclosure inbox" to "the Comms Table's disclosure inbox" (a naming-accuracy fix as well — disclosures are a distinct lane from the Q-channel, both live on the Comms Table). No behavior change.
- **0.2.6** (2026-08-20) — Step 1 (Intake) now also pulls the build-to-Charles disclosure inbox (`list_judgment_calls`, status `noted`) as a "Calls to review" list alongside the dependency hunt, and disposes each via `dispose_judgment_call` (`reviewed-agree` or `reviewed-corrected` with a linked Decision). Shipped with BB-2026-08-19-judgment-call-channel (the disclosure channel itself: `post_judgment_call`/`list_judgment_calls`/`dispose_judgment_call` on Project State MCP, parallel `-J-` display-id series, PROTOCOL.md Q-channel section extended, orchestrate-build/execute-build-task updated to post at close).
- **0.2.5** (2026-08-19) — Committed-brief header convention locked: the `.md` file's own top-of-document header (distinct from the in-chat Handoff Reference block, which already carried plan_id) now carries the Project State plan UUID + project slug and drops any plan-status line, since a status copied into the file goes stale the moment the DB plan transitions and DB is truth. Step 10 updated with the exact header format. Found and corrected during BB-2026-08-19-review-corrections (world-graph), which reconciled against the three 2026-08-18 BB files whose headers carried a status line and no plan UUID (those three files are left as-is; only the convention going forward changes).
- **0.2.4** (2026-07-14) — Handoff Reference block format locked: new `references/handoff-reference-template.md` is canonical (layout + pasteable-prompt structure, with worked example from BB-2026-07-14-attia-intake). Step 10 now points at it. Requested by Charles in the attia-intake scoping chat, 2026-07-14.
- **0.2.3** (2026-07-14) — Step 10 now requires a mandatory Handoff Reference block on the shelving turn: Brief ID, Project State plan title/plan_id/project slug/status, git location, and pasteable prompt — so Charles can hand the brief to any other chat without hunting for identifiers. Requested by Charles in-session 2026-07-14.
- **0.2.2** (2026-07-10) — Step 10 handoff now sets the finished brief's Project State plan to status `queued` (`update_plan_status`), aligning with the canonical work-queue lifecycle (draft → queued → running → succeeded/failed/blocked/abandoned) shipped in BB-2026-07-10-canonical-plan-lifecycle.
- **0.2.1** (2026-07-10) — Completeness framework shipped: `references/brief-completeness-framework.md` (11 decision domains, Answered/Defaulted/N-A three-state rule, orchestrator full autonomy with hard-gate-only escalation, mandatory fork log). Template gate 11 added. Circle-back item from 0.2.0 resolved. Decisions in the working appendix now carry decider markers ([Charles] / [Claude-per-doctrine]); Claude-decided items log with `judgment-call` provenance per the new PROTOCOL.md standing rule.
- **0.2.0** (2026-07-09) — Proactive harness revision, dogfooded in-session. Added the Proactivity Doctrine (11 rules). Living artifact changed from Design State to draft Build Brief (brief-first), with working appendix; new `references/build-brief-template.md`. Step 8 changed from serial one-fork-at-a-time to batched forks with consequence trails (serial only for dependent forks). PROTOCOL.md engagement rule 4 reconciled: within DA, satisfied by batched forks + pre-applied recommendations. Completeness framework shipped as draft; expansion deferred (see Circle-back items).
- **0.1.0** (2026-07-02) — Initial draft. Designed by dogfooding the process on itself. Four phases / ten steps, Design State artifact spec, phase-boundary snapshots via Project State plan tools, automated fan-out via orchestrator custom prompt sets (pending `agent_prompts` capability), hardware + software + hybrid spec formats. Explicitly decoupled from the office-hours → CEO/Eng review chain.
