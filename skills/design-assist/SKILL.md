---
name: design-assist
version: 0.7.0
status: draft
triggers:
  - "Design Assist"
dependencies: []
owner: Charles
updated: 2026-10-27
source: Original. Designed in-chat 2026-07-02 by Charles + Claude, dogfooding the process on itself. v0.2.0 proactive-harness revision designed in-chat 2026-07-09, again dogfooding. Absorbs the alternatives-generation idea from office-hours (Tan gstack lineage) into the convergence loop; otherwise independent of the office-hours → CEO/Eng review chain, which serves go-to-market interrogation, not hobby design.
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: with-you
  starts: "\"Design Assist\""
  runs_in: claude-chat
  reads: [project-state, cbrain, repos]
  writes: [plans, briefs]
  stack: [build-flywheel]
  origin: yours
  label: Design Assist
---

# Design Assist

## What

Claude leads Charles from a fuzzy concept to a build-ready spec/plan, teaching him the territory along the way. The job in one line: **help Charles understand this territory and shape a design for HIS use case — and drive it to completion, not relay questions.**

This is hobby-mode design across any domain — robotic lawn mowers, high-speed drones, 3D printing and micro-manufacturing, apps, personal dashboards. The process is domain-agnostic; the spec format adapts (software gets an MCP-first build spec; hardware gets a bill of materials, sourcing, build sequence, and test plan).

The session's source of truth is a single living artifact: a **draft Build Brief**, created on turn one from `references/build-brief-template.md` and rewritten each update — never appended — until it passes the completeness gate. Working design state (decisions, out-of-scope, forks) lives as an appendix on the brief. Project State is used only as periodic snapshot storage and for one light log at exit.

## When

**Fire when:** Charles says "Design Assist" in the prompt. That is the only trigger. Do not auto-fire from adjacent phrases.

**Do not fire when:** the design is already shaped and he wants execution (build chat), viability interrogation (office-hours), or a one-shot multi-perspective read (brainstorm chat).

**New workflows.** If the thing being designed is a new workflow — something Charles will start with one sentence or Start the Job — load `skills/workflow/SKILL.md` and follow it inside this loop. It runs a speed run first (`skills/speed-run`) when any step is unknown, and its parts list joins the completeness gate (gate 14). Changing an existing workflow stays an ordinary brief under rules 12-13.

## The Proactivity Doctrine

> These rules govern every DA turn. They override politeness, turn-length caution, and the instinct to ask before acting. Violating one is a session defect. Within DA sessions, the build skill's Response format rule on judgment calls (`skills/build/SKILL.md`) is satisfied by the batched fork list plus pre-applied recommendations below — DA does not surface every judgment call individually.

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
11. **Confidence labeled.** Verified-by-checking vs. assumed vs. drafted-unreviewed are visibly distinct in the artifact — rendered per `references/brief-artifact-style.md`'s pill/finding system (verified / assumed / drafted / correction), not just worded differently.
12. **Builds keep the Stack Flow current.** Any brief that adds, removes, renames or re-routes a running part carries a Stack Flow step that edits `concepts/stack-map.md` (dots, lines, side-panel text) in the same build. A brief that changes nothing on the diagram says `Stack Flow: no change` and why, in one line — the `**Stack Flow:**` header line in `references/build-brief-template.md`. Standing authorization from Charles, 2026-10-07 (`skills/build/SKILL.md`); the Rules Inspector still compares the map to what shipped each week and files anything missed.
13. **Builds keep the step map current.** Any brief that adds a workflow to the Workflows screen, or adds, removes, renames or reorders a workflow's steps, carries a step that edits that workflow's step list (`definition.steps`) in the same build. Each step has key (the exact name the runner logs), title, who (you | claude | checker | script | pc), uses, makes; stops say where pins go back to (back_to); time only when measured. A brief that changes no steps says `Step map: no change` and why, in one line. The "No step map yet" flag on the Workflows screen is the backstop.

## The living artifact — draft Build Brief

Created from `references/build-brief-template.md` at intake. Rules carried over from the Design State discipline:

- **Current state only.** Superseded ideas are dropped, not archived. Decision *reasons* stay (one line each) so settled questions don't get relitigated.
- **Rewritten after every decision or material turn.** The header carries date, turn count, and the live completeness checklist.
- **Language balance.** Plain English first. Jargon defined inline on first use. One technical clause per idea, max. Charles is not technical; the artifact must communicate the design shape to him and to a future technical executor at the same time.
- **Presentation.** Every turn that shows the artifact to Charles in chat renders it as a published HTML artifact per `references/brief-artifact-style.md` — pill-badged confidence, the completeness-gate table, `.brief` cards for build-ready content — not a plain chat/markdown dump. Redeploy the same artifact across a session rather than publishing a fresh one each turn; Charles should have one artifact per design thread that updates in place.
- **Working appendix** carries: Decisions Made / Forks (open) / Gated items / Assumptions (genuinely unverifiable only) / Out of Scope. Each decision carries a decider marker — **[Charles]** or **[Claude-per-doctrine]** — and at exit, Claude-decided items are logged as Decisions with `judgment-call` provenance per `skills/build/SKILL.md`. When the brief goes build-ready, Forks and Gated are empty by definition and the appendix collapses into the brief's Scope and Inputs sections.

**Snapshot rule:** save the full artifact text to Project State at every **phase boundary** (end of Orient, end of Constrain, convergence milestones, exit) and whenever Charles says "save state" — not every turn. First save uses `write_plan` (project per `list_projects` fit-check, per `agent-library/references/project-state.md`); later saves use `update_plan_content`, which keeps revision history automatically. This is storage, not ceremony — no Session Log per save.

## Design Board upkeep

Charles reads two cbrain tabs to see what every DA chat is doing: the **Build Shelf** (one card per current brief) and the **Design Board** (one card per design topic not yet on the shelf, with each chat's current take). He is never a gate on either. The DA chat keeps both current on its own judgment. *(Active — Build 23 succeeded 2026-10-04.)*

1. **Tag on turn one.** The first reply carries `Board tag: DA-MMDD-slug` (e.g. `DA-1004-shelf-board`). Pass it as `chat_tag` on every Project State write this chat makes.
2. **Join or open a topic on turn one.** `list_board`. If a topic names the same piece of the app, join it. If none does, open one with `board_update`, named for the thing (e.g. "RACI matrix format"), 6 words max, plain words, no codes.
3. **Rewrite your line every turn or two.** Whenever direction moves (Charles decides, rejects, or a new proposal lands), call `board_update` with one line of 15 words or fewer saying where this chat stands. It replaces your old line; the old one goes to history. Charles's own decisions go in `decided`. Your takes are the line, shown as Inferred. Use `open_question` only for something genuinely his to call.
4. **Edit briefs, don't stack them.** While a brief is unbuilt, change it with `update_plan_content` and a one-line `change_reason` (shown as "Latest edit"). A new brief only when the scope is genuinely separate or the earlier one already ran. A brief that supersedes another passes `replaces` so the old one leaves the shelf and folds under the new card. Never edit a brief whose plan is `running`.
5. **Pass `topic` on every brief** so the shelf card links to its topic.
6. **Before the chat goes quiet,** your line says where things stand: decided, waiting on Charles, or parked.
7. **Session-start sweep.** Besides the intake pulls in step 1 below: for board lines and briefs missing a chat link, search past chats for their tag (`conversation_search`) and call `board_link_chat`. Put build briefs with no topic onto the right topic.
8. **Heed `board_reminder`.** If a Project State reply carries one, update your line before the next reply.
9. **End every reply with `Board ✓`** once the line is current.
10. **Plain words only** in everything the tabs show — board lines, `change_reason`, `designed_in`, `plain_title`, `plain_summary`. No brief file names, display ids, chat tags, commit hashes or plan ids. (The tabs scrub codes as a backstop, which leaves odd phrasing — C-J-321.)
11. **If the board tools aren't in your tool list** (a chat opened before they deployed), write the same rows with SQL on `ujditldbqdiqigazkcak` (`design_topics`, `design_topic_lines`: stamp your current line `replaced_at = now()`, insert the new one).
12. **Check in** per Progress tracking (below). This adds to rules 1-11; it replaces none of the board upkeep.

**Also (adopted 2026-10-04 after the Build 23 pilot, C-J-320):** every cbrain-ui brief names `checkpoint-deploy` in its Skills line. The pilot cut 21 commits to 4 preview builds with no misses.

## How — four phases, ten steps

Steps run in order, but the process is a loop, not a rail: new information can reopen an earlier step. When that happens, update the artifact and say so. Doctrine rule 4 applies from step 1: the whole goal gets mapped immediately, then sharpened.

### Phase A — Orient

1. **Intake.** Charles dumps the raw idea, however messy. Capture it verbatim into the artifact before shaping anything. The verbatim capture survives into the final brief as the "Asked for" block (`references/build-brief-template.md`) — the one part of the living artifact that is never rewritten; later changes Charles makes are appended as dated lines in his words. Create the draft Build Brief now. Run the dependency hunt (doctrine rule 7). Also pull the Comms Table's disclosure inbox for this project (`list_judgment_calls`, status `noted`) — the "Calls to review" list, separate from and never gating on blocking questions. For each: read the thread (`build_question_messages`), then `dispose_judgment_call` — `reviewed-agree` if it holds up as-is, or `reviewed-corrected` (log the correcting Decision first, pass its id as `linked_decision`) if it doesn't. Unreviewed items are fine to leave `noted`; nothing here blocks intake. Finished builds are not reviewed — `succeeded` means done (gate removed by Charles 2026-10-23; see `skills/build/SKILL.md`). Also pull **Punch List items with status `needs-brief`** (`list_punch_items`, filtered) — a second session-start pull, alongside the disclosure inbox, not a gate. For each: if it clearly needs a Build Brief, draft and shelve one per the normal Build Brief process below, then `add_punch_note` (author `da`) naming the new Brief's id on the item — this is the only note a DA chat writes on a Punch List item; it never changes the item's status (only the Inspector closes a Punch List item, per `skills/inspector/SKILL.md`). If it doesn't clearly need a brief after a look, leave it for a later session rather than guessing. **When Charles says a build is done.** That is the whole handoff — no audit, no `review_plan`. Dispose that build's disclosures (same `dispose_judgment_call` step above) and, if the plan's plain name is missing or weak, fix it (`update_plan_labels`). **Walkthrough visibility rule (mandatory, CB-228).** If that build has a walkthrough for Charles, the same turn also: (a) updates the walkthrough's header in `docs/review/walkthrough-log.md` from PENDING to READY with the landing time and evidence path — a section prepared ahead of a build must never still say "not merged" after it has; and (b) adds one open next move on the project — `Charles: walk Walkthrough N — checks Build X (<what it covers>), ≈<minutes>. Script: <GitHub link to the log section>. Start at: <preview URL>.` — tagged `walkthrough`, `charles`, `build-X`. The git log stays the single source of the script; Project State carries the pointer, because a walkthrough is work only Charles can do and belongs where his work is listed. The DA completes that next move when Charles reports and logs his findings as WT rows. Unaudited plans are fine to leave for a later session; nothing here blocks intake. Also pull `overnight_line` and last night's `night_runs` (both returned by `overnight_line`). Stuck / deploy-red / interrupted-twice overnight builds are handled like any stuck build.
2. **Restate.** Name the originator first. If it's Charles, quote him. If it's the Stack Advisor, the Inspector, or a build chat, quote its plain-terms line with its ID (ADV-NNN / PL-NNN / X-Q-NNN) plus Charles's disposition. Then say what Charles is really trying to do — including the goal behind the stated goal, and how it serves *his* use case specifically (his skills, his shop, his family, his stack). This loop is the interview: keep asking, batched, until he says it lands. Draft acceptance criteria now (doctrine rule 10).
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
   - **Software/system:** MCP-first per `skills/build/SKILL.md` — each step names the tool that executes it (Supabase MCP, GitHub MCP, Vercel MCP...), with parameters.
   - **Hardware:** bill of materials with sourcing links and prices, tools required, build sequence, wiring/assembly notes, test plan, safety checklist.
   - **Hybrid** (e.g., drone + telemetry dashboard): both, cross-referenced.
   - **Overnight check.** Check every Overnight-tagged brief with the same `target_repo`. If they touch the same screens or data, link them with `after` so the order is explicit. If the new design changes what a tagged brief will build, edit that brief or untag it (`set_overnight false`) — before 11 pm Indianapolis time if possible. Also check every unbuilt brief (draft or queued) that adds, removes, renames or re-routes a running part has a Stack Flow step (doctrine rule 12) — this chat's own and any other it touches — and add one with `update_plan_content` if it's missing. Likewise every unbuilt brief that adds a workflow or changes a workflow's steps has a Step map step (rule 13); add one with `update_plan_content` if missing.
10. **Handoff.** The brief passes the completeness gate and ships per `skills/build/SKILL.md` (Shelving a brief), or work continues inline if small. Commit the final brief to the target project's repo (`docs/design/`) if one exists.
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
    This is what lets the advisor's idea pool suppress ideas Charles has already adopted, without Charles ever having to reply to the advisor's email. This Response is the *intended* one, written at scoping; the Build Chat that lands the brief overwrites it with the *actual* response and flips the row to `addressed` at close, per the Build Brief return contract in `skills/build/SKILL.md` (BB-2026-09-04-advisor-response-loop).
    At handoff, set the brief's plain labels on the Project State plan — `plain_title`, `plain_summary`, `campaign` (slug), and `designed_in` (this session's name + today's date) — via `update_plan_content`, per the naming rule in `agent-library/references/project-state.md`. Then set the plan to status `queued` (`update_plan_status`) so the orchestrator can pick it up. Close with one light Session Log to Project State: the decision set, the brief location, next action.
   **Handoff Reference block (mandatory).** The turn that shelves a brief ends with a clearly labeled block Charles can copy into any other chat, containing, in this order: the **build number** (`**Build:** 11.6`, or `unnumbered`), Brief ID, Project State plan title + plan_id + project slug + status, git location (owner/repo/path), and the pasteable prompt — whose first words are that same build number (`Build 11.6 — execute Build Brief BB-…`). The number is what Charles orients by; the ids are for the chats. It also leads the plan's `plain_title`. The block's exact layout and prompt structure follow `references/handoff-reference-template.md` — fill placeholders, never restructure. Shelving without this block is a session defect.
   **Overnight (mandatory).** Every brief is shelved. The approval question is **"Overnight: yes or no?"** (never "hold"). Record `after` and `target_repo` on every brief. The Handoff Reference block gains a line `**Overnight:** #N` or `**Overnight:** no`.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: design-assist
- build: what this chat is designing, in 3-6 plain words, e.g. "Next steps side panel" (thread_key = the board tag, DA-MMDD-slug)
- Opens when: the first turn (the board tag is stamped)
- Checks in: end of every turn
- Closes when: the brief is shelved, or Charles parks it (`close_thread`, closed_how "brief on the shelf" or "parked")

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

- **0.7.0** (2026-10-27) — New workflows: the When section points to `skills/workflow` (which runs `skills/speed-run` first when any step is unknown); its parts list joins the completeness gate as gate 14. Rule 13's no-change line now says why. Phase D step 9's sweep also checks every unbuilt brief that adds or changes a workflow's steps has a Step map step. Changelog label fix (v0.6.0 → 0.6.0). Per Build 54 (BB-2026-10-27-workflow-method; closes TH-J-032's loose ends).
- **0.6.0** (2026-10-26) — Doctrine rule 13: builds keep a workflow's step map (`definition.steps`) current; briefs carry a `**Step map:**` header line beside Stack Flow. Per Build 50 (BB-2026-10-26-workflow-step-map).
- **0.5.2** (2026-10-23) — Review gate removed at Charles's direction. Intake no longer pulls or audits succeeded builds and never calls `review_plan`. When Charles says a build is done, the DA chat disposes that build's notes, fixes a weak plain name if needed, and runs the walkthrough visibility rule (which now keys off that moment instead of the review).
- **0.5.1** (2026-10-23) — Board rule 12's check-in moves into the new Progress tracking section (build = the chat's own name for its work; project is Charles's; no 5 am sweep). Per BB-2026-10-21-next-steps-panel.
- **0.5.0** (2026-10-21) — Build 44 (BB-2026-10-20-next-steps-dev-tab): new Board rule 12, Check in — every turn, Project State `checkin` per `references/thread-checkin.md` (kind `design-assist`, thread_key = board tag); `close_thread` when the brief is shelved or Charles parks it. Feeds the Next steps list on cbrain's Dev tab. Board upkeep unchanged. New `requires` entry.

- **0.4.1** (2026-10-15) — Build 39 (BB-2026-10-14-protocol-retirement): the chat-protocol rulebook is retired. Live pointers to it now name `skills/build/SKILL.md` (authority, shelving, return contract, tool-first, judgment-call provenance, Response format) or `references/project-state.md` (naming rule, project fit-check); the Punch List pointer names `skills/inspector/SKILL.md`. New `requires: [references/project-state.md]` header. Older changelog lines keep their original wording.
- **0.4.0** (2026-10-08) — Build 11.7.12: builds keep the Stack Flow current. New doctrine rule 12: any brief that adds, removes, renames or re-routes a running part carries a Stack Flow step that edits `concepts/stack-map.md` in the same build, or says `Stack Flow: no change` and why. Step 9's Overnight check also adds a Stack Flow step to any unbuilt brief that's missing one. `references/build-brief-template.md` gains the `**Stack Flow:**` header line and a completeness-gate item. Standing authorization from Charles, 2026-10-07, replacing PROTOCOL.md's "sessions never edit the stack map" rule; the Rules Inspector stays as backstop. Per BB-2026-10-07-stack-flow-return-lines.

- **0.3.0** (2026-10-04) — Build 26: night builds. Step 1 intake also pulls `overnight_line` and last night's `night_runs` (stuck / deploy-red / interrupted-twice overnight builds handled like any stuck build). Step 9 gains an Overnight check: link same-repo tagged briefs with `after`, and edit or untag (`set_overnight false`) any tagged brief the new design changes, before 11 pm Indianapolis time if possible. Step 10: every brief is shelved, the approval question is "Overnight: yes or no?", `after` and `target_repo` recorded on every brief, and the Handoff Reference block gains an `**Overnight:**` line. Board rule 4: never edit a brief whose plan is `running`. Per BB-2026-10-04-night-builds.

- **0.2.18** (2026-10-04) — Build 23 review. Board rules 10 (plain words only in anything the tabs show) and 11 (SQL fallback when the board tools aren't in a chat's tool list — chats opened before a deploy don't see new tools). Upkeep section is now active (Build 23 succeeded). checkpoint-deploy becomes standard on every cbrain-ui brief (pilot: 21 commits → 4 preview builds, 0 misses).

- **0.2.17** (2026-10-04) — New "Design Board upkeep" section (nine rules): every DA chat stamps a board tag on turn one, joins or opens a design topic, rewrites its one-line take every turn or two, edits unbuilt briefs instead of stacking revisions (`replaces` folds a superseded brief under its successor), links briefs to topics, sweeps missing chat links at session start, heeds `board_reminder`, and ends replies with "Board ✓". Charles is never a gate on the board. Pairs with Build 23 (BB-2026-10-04-shelf-design-board), which adds the Build Shelf and Design Board tabs to cbrain and the board tools to Project State. Charles, 2026-10-04: after a day away he couldn't tell which brief or design talk belonged to which chat.

- **0.2.16** (2026-10-02) — Every brief keeps the originator's own words. Step 1's verbatim intake now survives into the final brief as a frozen "Asked for" block (new in `references/build-brief-template.md`, first item under Current state going in; gate 1 now requires it); later changes are appended as dated lines in Charles's words, never edited in. Step 2 names the originator — Charles, or for agent-raised work the Stack Advisor / Inspector / build chat's plain-terms line with its ID plus Charles's disposition — and states that the Restate loop is the interview. `brief-completeness-framework.md` domain 11: where the intent narrative and the block disagree, the block wins. No separate intent file and no new step for Charles. Adopted narrower from ADV-033 (Anthropic's AI-native SDLC intent.md pattern), executed inline in a DA chat at Charles's direction.

- **0.2.15** (2026-09-22) — Step 1's session-start intake gained a third pull: Punch List items in status `needs-brief` (`list_punch_items`), alongside the disclosure inbox and the succeeded-unreviewed plans list. A DA chat that briefs one shelves a Build Brief as usual and adds one `da`-authored note naming the Brief's id (`add_punch_note`) — it never changes the item's status; only the Inspector closes a Punch List item. Per BB-2026-09-21-inspector-repairer Phase 2, step 10.
- **0.2.14** (2026-09-20) — The build number leads the handoff: Step 10's Handoff Reference block opens with `**Build:** N.N` and the pasteable prompt opens with `Build N.N — execute Build Brief …`; unnumbered work says so in the same position rather than dropping the field. Companion PROTOCOL.md rule ("The build number leads the handoff") and `references/handoff-reference-template.md` v1.1.0. Charles, 2026-09-20: the Brief ID, plan id and project slug are for the chats — the build number is the label he orients by, and it was missing from the block.
- **0.2.13** (2026-09-14) — New `references/brief-artifact-style.md`: the visual system every DA artifact turn now renders through (IBM Plex type, confidence-pill CSS for verified / assumed / drafted / correction, the completeness-gate table, `.brief` cards mapped to `build-brief-template.md`'s ● fields, inline-SVG mechanism diagrams per `artifact-diagramming`). Doctrine rule 11 and the living-artifact section now point to it. Generalizes the styling from a world-graph feed-reader design session the same day, which Charles reacted well to — that specific artifact was original work, not drafted from any existing template; this file is what makes the pattern reusable and canonical going forward.
- **0.2.12** (2026-09-09) — Step 1's plan audit gained the **walkthrough visibility rule** (CB-228 on cbrain): the turn that calls `review_plan` also flips the walkthrough's header in `docs/review/walkthrough-log.md` from PENDING to READY and adds one open next move on the project — "Charles: walk Walkthrough N — checks Build X …, Script: <GitHub link>, Start at: <preview URL>" — tagged `walkthrough` / `charles` / `build-X`, completed by the DA when Charles reports. Prompted by Charles on 2026-09-09: walkthrough scripts lived only in git and inside plan text, and he could not find them from Project State. Two live traces behind it: Walkthroughs 8 and 9 were both prepared ahead of their builds and still read "not merged" after the builds had landed and been reviewed.
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
