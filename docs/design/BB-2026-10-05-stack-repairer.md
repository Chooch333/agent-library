# Build Brief — BB-2026-10-05-stack-repairer

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-05-stack-repairer.md`
**Project State plan:** `14e14e13-d61f-4a17-be1e-a6d7f3beea93` on `cbrain`

**Build:** 27
**Skills:** orchestrate-build, checkpoint-deploy (only if cbrain-ui code changes)
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also edits Chooch333/cbrain) · **after:** none

**What this is:** A new Stack Repairer agent fixes things that break while running, so Charles never sees per-problem emails or kicks off fixes. It gets one recap email a day.

**What I'll do (build chat):** Write the Stack Repairer skill, its log table, the renames, quiet the other failure emails, add the protocol line, and leave Charles one setup step.

**What you'll do (Charles):** Create the scheduled routine once (step 7 gives the exact clicks). Nothing else.

---

## Current state going in

### Asked for (frozen — Charles's words)
- Oct 5: "I'm getting emails about various things in my stack failing. I want to create a way for claude to receive these and address them… I'm willing at most to forward emails to that go-between email address, but otherwise I want a solution that takes me more out of the loop. I have the inspector and repairer set up. would it make sense to get them to look at the problems?"
- Oct 5: "I don't want to have to kick off a bunch of responder BB's… I can understand focusing 1 repairer for 1 domain… Maybe no emails about problems, just an email after the Responder is done the provides a synopsis of everything it did."
- Oct 5: "Can we use Stack inspector and Stack repairer. Keeping matching nomenclature is helpful… the big ones, should be queued for overnight as default… give me an succinct email from the stack repairer at a certain time each day hopefully at the end of their work or near the end summing up all that they did today."
- Oct 5: relabel the existing pair "Rules Inspector / Rules Repairer" on screen — yes. Overnight for this build — yes.
- Oct 5: "Confirm the new skills will be UX, also confirm the updated names rules repairer will be updated in the UX"

### Verified at design time (2026-10-05)
- The **Stack Inspector** is the 15-minute checker from Build 11.7.9: `Chooch333/cbrain` `services/api/cron/stack-status.ts`, deployed on Vercel project cbrain-sync. It writes table `stack_status` in cbrain Supabase `lpeswznkxzeeyiqaewma` (columns include id, kind, label, state, own_state, reason, via_allowance, last_seen_at, checked_at, emailed_state, emailed_at, detail).
- **Per-problem alert emails are already off.** The DA chat committed `2e97a2e` on cbrain main (`ALERT_EMAILS_ON = false`); deploy dpl_ECiE6Z2qdkkoEqZX7dAqp6sQjWeQ READY. The 16:00 UTC run sent nothing. Do not turn them back on.
- Red at design time: `world-graph` (ingest_transcript.yml failing since 12:38 UTC). `smoke-tests` (cbrain-ui unit-tests.yml on review) flipped red/green during the day.
- Repeat-email bug: Smoke tests alerted 3× on Oct 5 (10:30, 11:15, 15:15 UTC) — the reason text flipped between two checks and each flip planned a new alert.
- The existing Inspector/Repairer (`roles/inspector`, `roles/repairer`) cover rules, skills and the stack map, weekly. They never look at whether a job ran.
- The night runner (Build 26) is live: `night_runs` has rows, the last at 2026-10-05 06:36 UTC.
- Scheduled routines are created by Charles once (precedent: CB-503 for the night runner).
- The other failure emails come from the Reader (`roles/world-graph-reader`) and the Stack Advisor (`roles/stack-advisor`), sent from claude.go.between@gmail.com. The Reader also sends a daily digest.

## Receiving chat
The night runner (Overnight), or any build chat.

## Scope
**In:**
- New skill `roles/stack-repairer/SKILL.md`.
- New `stack_repairs` table.
- Renames: Stack Inspector, Rules Inspector, Rules Repairer.
- A new Stack Repairer dot on the stack map.
- Quiet the Reader's and the Advisor's failure emails, and fold the Reader digest into the recap.
- Fix the repeat-email bug.
- One PROTOCOL.md section.
- One next move for Charles.

**Out:**
- Turning alert emails back on.
- Changing what the existing Inspector/Repairer do (labels only).
- Showing repair history on the Stack screen (later build).
- Advisor briefs (they stay as they are).

## Design intent (for forks)
Charles is out of the loop for stack breakage. He reads one daily recap and acts only on a key, money, or an irreversible data change.

The roles split cleanly:
- The Stack Inspector (the checker) finds problems and grades the fixes.
- The Stack Repairer only diagnoses and fixes.

When unsure, prefer the smaller, reversible action and record it.

## Directive

**1. Log table** (Supabase MCP `apply_migration`, project `lpeswznkxzeeyiqaewma`).
Create `stack_repairs`:
- `id` uuid pk
- `run_at` timestamptz default now()
- `dot_id` text
- `finding` text
- `action` text check in (`rerun`, `cleared`, `fixed`, `briefed`, `built`, `needs-you`, `watching`)
- `detail` jsonb
- `plan_id` text null
- `commit_sha` text null
- `outcome` text null (filled by a later run: `green`, `still-red`)

RLS on, no policies, same as `stack_status`.

**2. Skill** `roles/stack-repairer/SKILL.md` (Custom GitHub MCP `create_or_update_file` on agent-library main).
- Follow the shape of `roles/repairer/SKILL.md`: frontmatter `wiring` with label "Stack Repairer", runs on-its-own, runs_in claude-code-routine; steps with Precondition / Action / Success evidence / Recovery.
- Trigger: "Stack Repairer: run" plus the routine.

Each run:
- **a. Read.** `stack_status` rows with state `failing` or `late` (dots and allowances), plus today's `stack_repairs` rows. Skip `unknown`.
- **b. Grade earlier work.** For each prior row whose `outcome` is null, set `green` or `still-red` from the current state. A fix that stayed red moves up one size next time.
- **c. Diagnose.** Read the evidence:
  - GitHub workflow runs: `list_workflow_runs`, `get_job_logs`.
  - Vercel: `get_runtime_logs`, `list_deployments`.
  - For a heartbeat: the `detail` URL.
  - Check the Actions-outage modes in PROTOCOL.md's GitHub Actions rule first: a billing lock or a disabled workflow is not a code bug.
- **d. Act at the smallest size that fixes it:**
  - **Re-run / clear.** Use `run_workflow` (explicit `ref`) for a hiccup or an outage that has ended, or re-dispatch a push-triggered job that never fired. At most 2 re-runs per dot per day, then go up a size.
  - **Urgent fix.** Urgent means something has stopped that Charles would feel today, or data is piling up or being lost (email filing, intake, the site). If it's one file with a clear cause, fix it directly. Otherwise, write a short brief and build it in this same run by following `skills/orchestrate-build/SKILL.md`.
  - **Not urgent.** Write a short brief (template below) via `write_plan` on project `cbrain`, set status `queued`, `overnight: true`, `target_repo` set, tags `stack-repairer`, `build-brief`, with plain_title and plain_summary. These briefs carry standing approval (step 5), so never ask.
  - **Hard gate** (a key/credential, spending money, an irreversible data change). Do nothing except log `needs-you` with the exact ask.
  - Standing rules: cbrain-ui changes land on `review` (CB-185); commit as Chooch333 (CB-121); never touch `apply.yml` (CB-103).
- **e. Log.** Write one `stack_repairs` row per action. For each new kind of incident, `add_lesson` on project `cbrain` tagged `stack-incident`, so the Rules Inspector can see repeats.
- **f. Daily recap.** Only the run at or after 17:00 America/Indiana/Indianapolis sends it.
  - Gmail send from claude.go.between@gmail.com to cecourtney10@gmail.com.
  - Subject: `Stack Repairer — <Mon D>`.
  - Plain English, at most ~15 lines, four short sections:
    - Fixed today.
    - Queued for tonight.
    - Last night's builds (from `overnight_line` → last_night).
    - Needs you.
  - Add one Reader line (articles and facts processed today) if it can be read from data. If not, omit it.
  - If all sections are empty, send nothing.
- **Never:**
  - Edit rules, skills or the stack map (that's the Rules Inspector/Repairer's domain).
  - Review its own briefs or dispose disclosures.
  - Email at any other time.

Short brief template for its own briefs: the standard PROTOCOL.md Build Brief fields. Keep it brief. "Asked for" = the failing dot plus the error evidence. `**Build:** unnumbered (Stack Repairer)`.

**3. Renames.**
- `concepts/stack-map.md` on cbrain main (Custom GitHub `replace_in_file`; follow `roles/repairer/references/stack-map-playbook.md`: change the frontmatter entry and its table row together, then `rebuild_index`):
  - The checker's dot becomes "Stack Inspector". If no dot represents the checker, add one with `ops.check` reading `stack_status` `_checker.checked_at` (late after 45 min).
  - The Inspector becomes "Rules Inspector".
  - The Repairer becomes "Rules Repairer".
  - Add a "Stack Repairer" dot with `ops.check` of type output on table `stack_repairs` column `run_at`, late after ~6 hours. Silence on a quiet day is fine, so pick a window that won't flag overnight.
- `wiring.label` in `roles/inspector/SKILL.md` and `roles/repairer/SKILL.md` becomes "Rules Inspector" / "Rules Repairer". Labels only, nothing else in those files.
- **UX check (Charles asked, Oct 5).** The cbrain-ui Skills tab reads each SKILL.md's `wiring` header live (decision CB-355), and Stack Flow dots take their names from the stack map.
  - On the `review` branch, confirm from the Skills tab code that a new `roles/` folder is picked up with no code change, and that `wiring.label` is the name it shows.
  - If either isn't true, make the smallest cbrain-ui change on `review` so that Stack Repairer appears (with the Agent badge) and the Rules labels show.
  - Verified at design time (Supabase copy of the map, which may lag GitHub): dots "Inspector" and "Repairer" exist with `check: none`. No dot exists for the checker. The Reader's dot is "Collector" (output check) and the Advisor's dot is "Stack Advisor" (output check).
- AGENT.md Self-maintenance: add the row `Stack Repairer: run` → `roles/stack-repairer/SKILL.md`, plus a changelog line.

**4. Quiet the other failure emails.**
- `roles/world-graph-reader/SKILL.md` and `roles/stack-advisor/SKILL.md`: remove the "email Charles when the run fails" step, and the Reader's daily digest email. Keep the Advisor brief email.
- First confirm each has a stack-map dot whose `ops.check` can go red (not `none`). If not, add a check in step 3's same map edit (output freshness of what the run writes). Never remove an email before its replacement check exists.

**5. PROTOCOL.md** (chat-protocol main). Add a short "## The Stack Repairer" section after "## The Punch List":
- Two domains: Rules Inspector/Repairer (rules, skills, stack map, weekly) and Stack Inspector/Repairer (things running, daily).
- Stack Repairer briefs are pre-approved: queued and tagged Overnight with no "Overnight: yes or no?" question. Urgent ones may be built in the same run.
- Charles gets one daily recap and no per-problem email.

**6. Fix the repeat-email bug** (cbrain `services/lib/stack-status.ts` `planEmails`). Key an alert on the failing episode (state went to failing) rather than the reason text, so a reason change while still failing plans no email. Add a unit test. Leave `ALERT_EMAILS_ON = false`.

**7. Charles's one step (hard gate — his account).** `add_next_move` on cbrain, tags `charles`, `stack-repairer`, written like CB-503:

"Charles: create the Stack Repairer once — claude.ai/code/routines → New routine → name 'Stack Repairer', repository Chooch333/agent-library, connectors Custom GitHub, Project State, Supabase, Vercel, Gmail, schedule <7:00 · 12:00 · 17:00 Indianapolis>, prompt: `Stack Repairer: run — fetch Chooch333/agent-library roles/stack-repairer/SKILL.md and follow it.` Then press Run now."

If a routine can't hold three times, use the closest supported schedule: three routines, or hourly with the skill skipping off-hours. Write the exact clicks. This is the only thing that waits on Charles. Everything else must be done and verified before it.

## Inputs
- This brief.
- PROTOCOL.md.
- `roles/repairer/SKILL.md` (shape) and `roles/repairer/references/stack-map-playbook.md`.
- `skills/orchestrate-build/SKILL.md` and `skills/night-run/SKILL.md`.
- cbrain `services/api/cron/stack-status.ts` and `services/lib/stack-status.ts`.
- `stack_status` table.
- Build 11.7.9 session log CB-502.
- Decisions CB-355, CB-484 and CB-492.
- PP-029 (venue rule).

## Acceptance (what proves it worked)
1. `roles/stack-repairer/SKILL.md` exists and reads back. The AGENT.md row is present.
2. `stack_repairs` exists, and a dry run of the skill's steps a–e against today's red dots writes rows (or `watching`) without error. Use the `world-graph` transcript failure as the live case.
3. The stack map shows Stack Inspector, Stack Repairer, Rules Inspector and Rules Repairer. `get_entity('stack-map')` agrees.
4. The Reader and Advisor skills no longer email failures, and both of their dots have a check that can go red.
5. The `planEmails` unit test passes, and `ALERT_EMAILS_ON` is still false.
6. The PROTOCOL.md section is present.
7. The Charles next move is open with exact clicks.
8. In the UX (`review` preview): the Skills tab lists Stack Repairer as an Agent, and shows Rules Inspector and Rules Repairer. Stack Flow shows the Stack Inspector, Stack Repairer, Rules Inspector and Rules Repairer dots. Prove it from code plus a fetch of the preview's data or API (no browser test). Charles eyeballs it.

After Charles creates the routine (post-build, not a gate on closing): the first 17:00 run sends one recap, and no other stack email arrives that day.

## Hard gates
- Creating the routine (Charles's account) — handled as a next move, not a halt.
- No money. No irreversible data changes.

## Pasteable prompt
> Build 27 — execute Build Brief BB-2026-10-05-stack-repairer. Pull the plan from Project State (plan_id 14e14e13-d61f-4a17-be1e-a6d7f3beea93, project cbrain, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-10-05-stack-repairer.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none block the build — the routine setup is left as a next move for Charles). Standing rules CB-185, CB-121 and CB-103 apply; leave ALERT_EMAILS_ON false. No browser test: Charles tests by hand.

## Decisions (working appendix)
- Names Stack Inspector / Stack Repairer; existing pair relabelled Rules Inspector / Rules Repairer. **[Charles]**
- New repairer, not the old one widened. **[Charles]**
- No per-problem emails; one daily recap near day's end. **[Charles]**
- Non-urgent fixes queue Overnight by default with standing approval. **[Charles]**
- This build Overnight: yes. **[Charles]**
- Both new and renamed names must show in the UX (Skills tab and Stack Flow). **[Charles]**
- Runs at 7:00, 12:00 and 17:00, with the recap on the 17:00 run (~5:30 pm). **[Claude-per-doctrine]**
- Non-urgent small fixes take the brief path (not the Punch List). The Punch List stays rules-only. **[Claude-per-doctrine]**
- Venue is a Claude Code routine, per PP-029 (it edits repos), and it matches the night runner's setup. **[Claude-per-doctrine]**
- Urgent big fixes are built in the same run via orchestrate-build. **[Claude-per-doctrine]**
