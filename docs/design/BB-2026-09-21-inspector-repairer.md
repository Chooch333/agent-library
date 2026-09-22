# Build Brief — BB-2026-09-21-inspector-repairer
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-09-21-inspector-repairer.md`
**Project State plan:** `102b5f53-383b-4184-b98d-2e5d8bb56d1d` on `agent-build-out`
**Build:** unnumbered
**Skills:** orchestrate-build, execute-build-task (agent-library `skills/`)
**Advisor origin:** ADV-001, ADV-002, ADV-016, ADV-017, ADV-019 (part), ADV-029 (part), ADV-031 (part)

**What this is:** Build the Punch List (a third place to leave and pick up work, beside the build shelf and the Comms Table), two self-maintenance agents — the **Inspector** (finds drift, drafts fixes) and the **Repairer** (applies safe fixes, writes back) — and exercise the new Skill Design Framework on them. Split Stack Manager across the two agents, retire map suggestions, add a receipt check to repair.yml, and schedule both agents on Cowork.

**What I'll do (build chat):** Phase 1 plumbing (Punch List tables + four MCP tools, PROTOCOL changes). Phase 2 agents (two skills, Stack Manager pointer, CONVENTIONS/AGENT.md/DA edits, repair.yml receipt, schedules, acceptance runs, LEDGER responses). Verify Phase 1 before starting Phase 2.

**What you'll do:** Nothing mid-build unless the one hard gate fires (below). Afterwards, read the trail.

---

## Current state going in

- **[verified]** No skill fixes the system's own rules. CONVENTIONS.md designed a "Distill" meta-skill (reads traces, writes SKILL files) plus a per-task "should-distill" hook and mechanical validation — never built (only CONVENTIONS.md and references/chat-capture.md mention "should-distill").
- **[verified]** Stack Manager (roles/stack-manager/SKILL.md v0.1.0, draft) has disposed one suggestion ever (SM-002 → decision SM-003, 2026-07-21). 22 MAP-EDIT next moves are open on the `stack-map` project (oldest SM-005/006/007, 2026-08-18; newest SM-055, 2026-09-20). Its scheduled trigger pointed at heartbeat-orchestrator, which was never built (SM-049). The stack-map page (cbrain `concepts/stack-map.md`, entity `stack-map`) last changed 2026-07-21.
- **[verified]** The stack map is the component canvas on cbrain-ui's Stack screen — the screen reads `pages` row slug='stack-map', `frontmatter->'components'` (CB-291; Build 11 succeeded). The Stack Advisor reads it every run. Stale today: world-graph, yt-relay, chat-protocol, stack-advisor missing (SM-045–048); SM-043 layer vocabulary v2 (Charles-approved) not applied (SM-044).
- **[verified]** The Comms Table cannot host this: `build_questions.project_id` is NOT NULL, and the Today screen reads that table (CB-287).
- **[verified]** Cowork scheduled tasks work: the Stack Advisor has run 10 times on schedule (2026-08-28 → 2026-09-21).
- **[verified]** repair.yml (Chooch333/cbrain `.github/workflows/repair.yml`) is live, auto-triggered by health-check.yml via repository_dispatch, capped at 2 runs/hour, with no per-failure receipt.
- **[verified]** Project State holds 178 lessons across 12 projects (49 in the last 30 days); nothing records whether a lesson became a rule.
- **[verified]** Skill Design Framework draft committed: agent-library `references/skill-design-framework.md` (commit a6367ce).
- **[assumed]** Cowork scheduled runs draw on Charles's subscription, not API billing.
- **[assumed]** A Cowork build chat can create scheduled tasks itself (see Hard gates).

## Receiving chat

New Cowork build chat (needs Cowork to create the scheduled tasks).

## Scope

**In scope**
1. The Punch List — two tables plus a checkpoint table in the Project State database, a `PL-` display series, four MCP tools in project-state-mcp.
2. PROTOCOL.md — retire the map-suggestion standing rule; add a short Punch List section.
3. `references/skill-design-framework.md` — exercise it; amend if building the two agents exposes a gap.
4. `roles/inspector/SKILL.md` and `roles/repairer/SKILL.md` (+ references); `roles/stack-manager/SKILL.md` reduced to a deprecated pointer.
5. CONVENTIONS.md exclusive-writes table; AGENT.md routing rows; design-assist SKILL.md Step 1 third intake pull.
6. repair.yml receipt check.
7. Two Cowork scheduled tasks; acceptance runs; closing the old MAP-EDIT next moves; LEDGER responses.

**Out of scope (pre-answered forks)**
- A Punch List screen in cbrain-ui — trail only in v1; Charles does not work a queue.
- heartbeat-orchestrator and scheduled builds — Charles, 2026-09-21: left out.
- Any Stack Advisor change — it stays outward-looking and propose-only. The Inspector does **not** take ADV ideas as work.
- Review-gate audits (succeeded-unreviewed plans, disposing disclosures) — Charles reviews builds himself; the Inspector reads disclosures as evidence only and never disposes them.
- ADV-006, 007, 013, 025 — Charles is "interested," pending his own look.
- Extractor tests (ADV-019/029 original targets); retrofitting existing skills to the step contract; bundling other MCP tools.
- Deleting old next moves — they are completed with a pointer, never erased.

## Design intent (for forks this brief doesn't answer)

Small, obvious fixes stop waiting on Charles or a full design cycle. Prefer fewer agents; split only where permission or independent checking demands it. The fixer never grades itself. Keep pictures of the system current by checking the real thing, not by asking everyone to report changes. When in doubt, hold back — a missed fix costs a week; a wrong rule change costs every chat. Never reverse what Charles decided personally (applying something he already approved is fine). Keep the Punch List out of every project view. Charles reads a trail, never a queue.

## The line between the two agents

- **Inspector — decides *what's wrong*.** Reads records and compares the stack map to what shipped. Writes only Punch List items (each with the exact fix drafted), notes, closeouts, and its checkpoint. Never edits a target; never emails Charles.
- **Repairer — decides *whether it's safe to apply now*.** Picks up items, re-reads the live target, applies, writes back. Never creates items; never verifies its own repairs.
- **Closeout:** the Inspector's next walk confirms each repair landed and nothing else changed; only then is an item `verified`.
- **ADVs:** the Inspector does not work from Stack Advisor ideas. It reads the LEDGER read-only for two reasons: never file an item that implements a **declined** ADV, and note an ADV id when its own evidence lands on the same fix — the Repairer then sets that LEDGER row to `addressed` so the Advisor stops re-pitching it.

## Authority tiers and protected list

- **Auto (Repairer applies):** add or clarify a rule in skills, references, or PROTOCOL.md; fix a broken cross-reference; stack-map edits; LEDGER status/response; plan plain labels.
- **Needs a brief (never edited; surfaces at DA intake):** anything touching code, workflows, schemas, data, or secrets; turning a rule into an automatic check.
- **Protected (never auto):** the hard-gate list and the authority model (who decides, when Charles is in or out of the loop); anything recorded as Charles's direct instruction; anything Charles declined or deferred (including declined LEDGER rows and deferred next moves such as C-048); deleting a rule.

## Directive

Answer forks autonomously with `judgment-call` tags per orchestrate-build; halt only at the hard gates below. Read live state immediately before every write (lesson C-061/C-062). Commits authored as Chooch333 (CB-121). Never touch `apply.yml` (CB-103).

### Phase 1 — Punch List plumbing

1. **Tables.** Supabase MCP `apply_migration`, project `ujditldbqdiqigazkcak`, name `punch_list_v1`. Draft schema (adjust names to repo conventions; log any change):
   - `punch_items`: `id uuid pk default gen_random_uuid()`, `display_id text unique` (PL-001… via trigger — mirror the existing build_questions display-id trigger pattern, but with no project prefix), `kind text check in ('doctrine','map','label','ledger','other')`, `target_repo text`, `target_path text`, `target_section text`, `change_summary text not null`, `draft_text text`, `evidence text[]`, `tier text check in ('auto','needs-brief')`, `status text not null default 'open' check in ('open','applied','verified','held','needs-brief','refused','failed','regressed')`, `adv_id text`, `plain_summary text`, `applied_commit text`, `created_at timestamptz default now()`, `updated_at timestamptz default now()`, `closed_at timestamptz`. **No project_id column.**
   - `punch_item_notes`: `id uuid pk`, `item_id uuid not null references punch_items`, `author text not null check in ('inspector','repairer','da','charles')`, `body text not null`, `created_at timestamptz default now()`. Append-only: block UPDATE and DELETE with a trigger.
   - `punch_checkpoints`: `id uuid pk`, `agent text not null`, `walked_through timestamptz not null`, `summary text`, `created_at timestamptz default now()`.
   - RLS on for all three, service-role only (matching the other Project State tables).
   - Verify with a separate SELECT on `information_schema.columns`.
2. **Tools.** Custom GitHub MCP on `Chooch333/project-state-mcp`: read how `post_judgment_call` / `list_judgment_calls` are registered and mirror the pattern for four tools:
   - `file_punch_item` (inputs: kind, target_repo, target_path, target_section, change_summary, draft_text, evidence[], tier, adv_id?, plain_summary; always writes a first `inspector` note).
   - `list_punch_items` (filters: status[], tier, kind; oldest first; includes the note thread when asked).
   - `add_punch_note` (item, author, body).
   - `set_punch_status` (item, new_status, author, note required; `applied` requires `applied_commit`; `verified` must be authored by `inspector` and is rejected if the same run id/author that applied it — enforce "author on verified ≠ author on applied").
   Deploy per the repo's existing path (Vercel MCP to confirm the deployment reads Ready). **ADV-008 lesson:** newly deployed tools are not callable in the same session — verify at the database layer via Supabase `execute_sql`, and run Phase 2's first tool calls in a fresh Cowork session.
3. **PROTOCOL.md** (Custom GitHub MCP `replace_in_file`, `Chooch333/chat-protocol`):
   - Replace the "Stack-map upkeep" standing-rule bullet with: cbrain holds the canonical stack-map (`get_entity('stack-map')`), which is the component map on the cbrain-ui Stack screen; sessions never edit it directly and no longer file map suggestions; the Inspector compares the map to what shipped each week and files Punch List items; the Repairer applies them.
   - Add a short "## The Punch List" section after "The Comms Table": the third place (shelf = briefs, Comms Table = build questions/disclosures, Punch List = fixes to the system itself); only the Inspector files, only the Repairer applies, only the Inspector closes; statuses; not a project and never shown in project views; DA chats pull `needs-brief` items at intake.
   - Read both edits back.

### Phase 2 — Agents

0. **Amendment 1 — DA review of ABO-J-002 (decision A-077, 2026-09-22). Do this before step 4.**
   - **Role enforcement in `set_punch_status`** (project-state-mcp `lib/handlers.ts`, `setPunchStatus`): accept `applied`, `held`, `failed` and `needs-brief` only from author `repairer`; `verified`, `regressed` and `open` (re-open) only from `inspector`; `refused` from either. Reject anything else before any write, with a plain error. Keep the existing `Status → applied` prefix scan as a secondary check. No schema change. Deploy and confirm READY. This changes an existing tool's behaviour, not its name, so it takes effect without a new session. Verify by calling `set_punch_status` on a test item with the wrong author and confirming the rejection, then clean up.
   - **Inspector SOP additions** (step 5, walk step 2): also take items in `held` and `failed` — re-check the target and either re-open (`open`, fresh draft via `add_punch_note`) or close (`refused`, with reason). Close a `needs-brief` item as `verified` once the Build Brief named in its notes has reached `succeeded`.
   - **DA intake** (step 10): a DA chat that briefs a `needs-brief` item adds a note (`add_punch_note`, author `da`) naming the BB id; it never changes the item's status.
   - **Acceptance addition:** a `set_punch_status` call with the wrong author for its status is rejected (e.g. `inspector` → `applied`).

4. **Skill Design Framework.** Re-read `references/skill-design-framework.md`; answer its twelve questions for each agent in the SKILL files' What/When sections. Amend the framework if a gap appears (judgment call).
5. **Inspector** — `roles/inspector/SKILL.md` per SKILL_TEMPLATE + CONVENTIONS (seven front-matter fields, six sections, status `draft`), every SOP step with precondition / action / success evidence / recovery. Trigger phrase "Inspector: walk". SOP:
   1. Load the latest `punch_checkpoints` row for `inspector`; none → cover the last 30 days.
   2. Re-walk items in `applied`: re-read each target; confirm the change is present and nothing else in the file changed since `applied_commit`; set `verified` or `regressed` (regressed → file a fix-it item).
   3. Map vs. shipped: read plans that reached `succeeded` since the checkpoint and their close-out snapshots; compare to `get_entity('stack-map')` using Stack Manager's checklist (accurate against live state? duplicate? conflicts with a prior decision via `get_decision_chain`? best wording/layer?). File a `map` item with the exact edit per difference. **First walk only:** use the 22 open MAP-EDIT next moves on `stack-map` as leads, and apply SM-043's layer vocabulary (SM-044, Charles-approved).
   4. Gather evidence since the checkpoint: lessons, `noted` disclosures (read only), failed/blocked plans, next moves open >14 days with no owner. Cap 60 records per walk.
   5. Cluster records pointing at the same rule; read the live target to see whether it is already covered.
   6. Rubric gate — file only if: ≥2 records or 1 verified defect; named target; exact fix text drafted; tier assigned; not protected; not declined/deferred (check LEDGER declined rows and deferred next moves). Otherwise hold back and note it in the walk summary.
   7. Write the new checkpoint with a one-line summary (seen / filed / held / verified / regressed).
   References: `roles/inspector/references/map-review-checklist.md` — Stack Manager SKILL step 3 and the "A suggestion can be true and still get rejected" pitfall, **verbatim**.
6. **Repairer** — `roles/repairer/SKILL.md`, same format, trigger phrase "Repairer: run". SOP:
   1. `list_punch_items` status `open`, tier `auto`, oldest first; none → clean no-op.
   2. Receipt: item already `applied` or has a repairer note citing a commit → skip.
   3. Fresh re-check of the live target: finding still true, target unchanged since filing, not protected. Unsure/stale → `held` with a note.
   4. Apply with an exact-anchor edit (`replace_in_file`); commit message carries the PL id.
   5. Scope check: read back; only the declared section changed. Otherwise revert its own commit and set `failed`.
   6. Write back: `set_punch_status applied` with commit + one-line reasoning; if `adv_id` set, set that LEDGER row to `addressed` with the response.
   7. `needs-brief` items are never edited.
   References: `roles/repairer/references/stack-map-playbook.md` — Stack Manager SKILL step 5 (edit frontmatter entry and table row together, `rebuild_index`), step 8 (verify the entity still parses), and its Rules section, **verbatim**.
7. **Stack Manager pointer.** Replace `roles/stack-manager/SKILL.md` with front matter `status: deprecated` and a short body pointing to the Inspector (judging) and Repairer (editing) and their references; changelog entry. The original stays in git history.
8. **CONVENTIONS.md.** Replace the three-meta-skill table (Execute / Distill / Guide) with Execute / Inspector / Repairer and their exclusive write rights; replace the per-task "should-distill" Hook protocol with "the Inspector's weekly walk"; note the Skill Design Framework under Skill file rules.
9. **AGENT.md.** Add a "Self-maintenance" section: "Inspector: walk" → `roles/inspector/SKILL.md`; "Repairer: run" → `roles/repairer/SKILL.md`; changelog entry. (Stack Manager has no AGENT.md row today — verified — nothing to remove.)
10. **design-assist SKILL.md.** Step 1: add a third session-start pull — Punch List items in `needs-brief` (`list_punch_items`) — alongside disclosures and succeeded-unreviewed plans; bump to 0.2.15 with changelog.
11. **repair.yml receipt** (Custom GitHub MCP `replace_in_file`, `Chooch333/cbrain`): add a step before the mechanic that resolves the target workflow's latest failed run id (`gh run list --workflow <file> --status failure --limit 1 --json databaseId`) and searches recent main commits for `repair-run:<id>` (`git log --grep`); found → skip the mechanic and log "receipt found". Add to the mechanic's prompt: its commit message must include `repair-run:<id>`. Leave the cap step, allowed tools, and the second-opinion step unchanged.
12. **Schedules.** Create two Cowork scheduled tasks in Charles's local time: "Inspector — weekly walk", Sunday 9:00 pm, prompt `Inspector: walk. Fetch Chooch333/agent-library roles/inspector/SKILL.md and follow it.`; "Repairer — weekly run", Monday 7:00 am, prompt `Repairer: run. Fetch Chooch333/agent-library roles/repairer/SKILL.md and follow it.` If Cowork will not allow it from the build chat → hard gate 1.
12a. **Amendment 2 — DA review of Phase 2 (decision A-080, 2026-09-22). Do this before step 13.**
   - **Inspector SKILL step 2b recovery** (`roles/inspector/SKILL.md`): replace the "set_punch_status held (author inspector)" recovery with: leave the status unchanged and `add_punch_note` (author `inspector`) explaining what couldn't be read; if the target is permanently gone, `set_punch_status refused` with the reason. ('held' is Repairer-only under A-077, so the current call would be rejected.)
   - **CONVENTIONS.md**: amend the Execute row so a build chat executing an approved Build Brief may create or edit exactly the skill files and AGENT.md rows that brief names. Under the routing rules, add that routing rows are written by the build that registers a skill (Skill Design Framework question 12) and that routing drift is fixed by the Repairer. Add a changelog line.
   - **repair.yml receipt step** (`Chooch333/cbrain`): make the RUN_ID lookup non-fatal (e.g. `RUN_ID=$(gh run list … || true)`), so a lookup error falls through to the existing "no failed run found — proceeding" branch instead of failing the step. Everything else stays unchanged.
   - **Acceptance check 5**: the planted protected item goes Repairer → `held`, then Inspector's next walk → `refused`. Check its end state after the second walk.
   - Read every edit back.

13. **Acceptance runs** (below), then complete every open MAP-EDIT next move on `stack-map` plus SM-049 via `complete_next_move` (SQL fallback) with the note "Map suggestions retired 2026-09-21 (BB-2026-09-21-inspector-repairer); handled by the Inspector's first walk — see Punch List." Leave SM-018 and SM-035 untouched.
14. **Close.** LEDGER (`Chooch333/cbrain docs/advisor/LEDGER.md`): write the actual responses for ADV-001, 002, 016, 017, 019, 029, 031 and set them `addressed`. Session Log on `agent-build-out`; disclosures to the Comms Table per PROTOCOL; final chat message says only that the build is done.

## Acceptance criteria

1. **Known answer:** untold, the Inspector's first walk files an item for the "freshly deployed MCP tool isn't callable yet" pattern (lessons E-080, E-085, CB-062/063, E-222, A-041, D-083), with the PROTOCOL rule drafted and `adv_id` ADV-008. The Repairer applies it; ADV-008's LEDGER row reads `addressed`.
2. **Map catches up:** after the first walk + run, `get_entity('stack-map')` contains world-graph, yt-relay, chat-protocol, and stack-advisor, and uses SM-043's layer names; the Stack screen on the review preview shows them.
3. **Idempotent:** running the Repairer a second time immediately changes nothing.
4. **Scope:** every Repairer commit touches only its item's declared file/section.
5. **Hold-back and protection:** a planted stale item (target text already changed) ends `held`; a planted item targeting the hard-gate list ends `refused`. Planted items are tagged as tests and closed afterwards.
6. **Closeout:** the Inspector's second walk sets the first run's repairs to `verified`.
7. **repair.yml receipt:** a dispatch against a failed run that already has a `repair-run:<id>` commit (the build may create a harmless receipt commit for the test and revert it) skips the mechanic — no API call.
8. **Out of the UX:** no code in cbrain-ui (`ref: review`) or project-state-mcp's dashboard reads the punch tables; nothing appears in project views or the Today screen.
9. **Schedules:** both tasks exist and each has fired once (run-now, or first scheduled fire; if waiting on the first fire, the next DA session checks it).

## Hard gates for this build

1. Cowork will not let the build chat create scheduled tasks → Charles pastes the two prompts in step 12 (about 2 minutes). This is the only halt.
2. Real money: none — no new API spend; the receipt test is designed to skip the mechanic.
3. Irreversible data: none — old next moves are completed with a pointer, not deleted; all file edits are git-versioned.

## Completeness — eleven domains

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered | What this is; Design intent |
| 2 Acceptance | Answered | Acceptance criteria |
| 3 Runtime | Answered | Cowork scheduled tasks; repair.yml on GitHub Actions |
| 4 Schema | Answered | Directive step 1 |
| 5 Storage & recall | Answered | Project State tables by status/tier; git for targets |
| 6 Interconnectivity | Answered | Project State MCP, Supabase MCP, Custom GitHub MCP, Vercel MCP, cbrain MCP, LEDGER |
| 7 Access & gates | Answered | Hard gates |
| 8 Skills & tools | Answered | Skills header; four new tools sequenced first |
| 9 Sequence | Answered | Phase 1 then Phase 2; fresh session after tool deploy |
| 10 Assumptions & risks | Answered | Current state [assumed] items; hold-back rule |
| 11 Design intent | Answered | Design intent (Charles approved 2026-09-21) |

Effort: Large overall (two Medium phases). Cost: no new API spend; ~2 Cowork runs/week (assumed subscription).

## Decisions made

- **Two agents, Inspector and Repairer** — the fixer must not grade itself. [Charles]
- **Stack Manager split** — its checklist to the Inspector, its editing rules to the Repairer, file becomes a pointer. [Charles]
- **Repairer may auto-fix PROTOCOL.md outside protected parts.** [Charles]
- **heartbeat-orchestrator left out.** [Charles]
- **Punch List is a place, not a project, and stays out of project views.** [Charles]
- **Weekly cadence to start.** [Charles]
- **Finder named "Inspector"** — "auditor" is the locked world-graph term. [Charles]
- **Map suggestions retired; map kept** — derived, never copied; approved via the design intent. [Claude-per-doctrine, Charles approved design intent]
- **Inspector does not take ADV ideas as work** — Advisor stays propose-only; LEDGER read only for declines and matches. [Claude-per-doctrine]
- **Plan on agent-build-out, campaign `crew`.** [Claude-per-doctrine]

## Pasteable prompt

> Build unnumbered — execute Build Brief BB-2026-09-21-inspector-repairer. Pull the plan from Project State (plan_id 102b5f53-383b-4184-b98d-2e5d8bb56d1d, project agent-build-out, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-09-21-inspector-repairer.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (Cowork scheduled-task creation, if the build chat cannot do it). Commits as Chooch333 (CB-121); never touch apply.yml (CB-103); run Phase 2 in a fresh session after the tool deploy.
