---
name: inspector
version: 0.2.1
status: draft
triggers:
  - "Inspector: walk"
  - "Cowork scheduled task \"Inspector — weekly walk\" (Sunday 9:00pm, Charles's local time)"
dependencies: []
owner: Charles
updated: 2026-11-10
requires: [references/project-state.md, references/thread-checkin.md]
wiring:
  runs: on-its-own
  starts: "\"Inspector: walk\" / weekly Cowork schedule (Sun 9pm)"
  runs_in: cowork
  reads: [project-state, step-in records, step-in receipts, fixed-set-run notes, tests/fixed-set.md, cbrain, stack-map]
  writes: [punch-list]
  stack: []
  origin: yours
  label: Rules Inspector
---

# Inspector

## What

The Inspector is the finder half of the system's self-maintenance pair (BB-2026-09-21-inspector-repairer). On a weekly walk it compares Project State evidence — lessons, disclosures, failed/blocked plans, stale next moves, and the step-in records the step-in scorer files (Build 76) — and the shipped stack against cbrain's canonical stack-map, and files a Punch List item, with the exact fix already drafted, for anything that clears its rubric. It never edits a target itself and it never emails Charles — everything it finds becomes a Punch List item (`file_punch_item`) that the Repairer picks up, or a held-back note in its own walk summary. It also closes the loop: on its *next* walk it re-reads every item the Repairer applied and only then marks it `verified` — the fixer never grades itself (design intent, BB-2026-09-21-inspector-repairer). A fix that came from step-ins is verified by its effect, not by its text: only when the corrections actually stopped (step 2a).

## When

**Fire when:**
- Invoked by name ("Inspector: walk").
- The weekly Cowork schedule fires ("Inspector — weekly walk", Sunday 9:00pm).

**Do NOT fire when:**
- You are the Repairer, or any session that just applied a Punch List item — the Inspector's `verified` call must come from a separate walk, never the same run that applied the fix (enforced in code: `set_punch_status` rejects a `verified` call whose author matches the most recent `applied` note's author, and additionally requires author `inspector` for `verified`/`regressed`/`open`, per decision A-077).
- You are deciding whether a Stack Advisor idea (`ADV-NNN`) is worth building — that is the Advisor's and Charles's call, never the Inspector's. Read the LEDGER only to avoid re-filing a declined idea or to note a matching `adv_id`; never to pick up new work from it.
- The job is scoring chats for step-ins (the step-in scorer's job) or replaying the fixed set (a Design Assist chat runs the Replay section of `skills/step-in-scorer`). The Inspector only reads what those leave.

## How

Precondition / Action / Success evidence / Recovery for every step (Skill Design Framework Q7).

**Step-in terms used below** (Build 76, BB-2026-11-09-inspector-reads-step-ins):
- A **step-in record** is a lesson on total-harness whose own tags hold exactly `step-in` (`find_by_tags` expands fuzzily, so drop rows that only carry `step-in-receipt`, `step-in-unsure` or `step-in-attempt`). Its **chat** is the link, or the title and date, in its situation; its **date** is that chat turn's date, never `created_at` (a record can be filed days after the turn).
- A **step-in item** is a Punch List item whose `evidence` names one or more step-in lesson display ids. Its **fixed-set task** is the task in `tests/fixed-set.md` whose `From:` line names that item's display id.
- A **clean receipt** is a `step-in-receipt` note (not tagged `step-in-attempt`) whose first line reads one chat or more and whose re-score passed: `re-score K of 3` with K at least 2, or `K of M` with K equal to M. `re-score: first run` and `K of 3` with K below 2 are not clean.

**1. Load the checkpoint.**
- *Precondition:* none — always the first step.
- *Action:* query the most recent `punch_checkpoints` row where `agent = 'inspector'` (take the single newest row).
- *Success evidence:* a checkpoint row (`walked_through` timestamp) or a confirmed empty result.
- *Recovery:* no checkpoint found (first-ever walk) → treat the window as "since 30 days ago" and proceed; do not fail the walk.

**2. Re-walk items that need a second look.**
- *Precondition:* step 1 complete.
- *Action, in two parts:*
  - **2a — `applied` items:** `list_punch_items` status `["applied"]`. For each, re-read the live target at `target_path`/`target_section` and confirm (i) the drafted change is present and (ii) nothing else in that file changed since `applied_commit` (compare against the commit's diff via the repo's commit API). Missing, reverted, or collateral changes found → `set_punch_status regressed` (author `inspector`), then `file_punch_item` a fresh fix-it item for the regression (kind matching the original, tier per the Authority tiers table). Present and clean, and **not** a step-in item → `set_punch_status verified` (author `inspector`).
    **Present and clean, and a step-in item → effect check, three outcomes.** The fix's time is its `applied_commit`'s commit time.
    - **Verified:** a `fixed-set-run` note dated after the fix ran the item's fixed-set task and it scored 0 step-ins on both runs of every setup that note ran, **and** at least two clean receipts whose window began after the fix (the receipt before each one has a `Read through` later than the fix) show no step-in record for this cluster. → `set_punch_status verified` (author `inspector`), `add_punch_note` naming the run note and the two receipts.
    - **Regressed:** a step-in record for this cluster dated after the fix, confirmed by opening the record and reading that chat turn (`read_conversation` when the walk has it; else the record's own situation, and say so in the note). → `set_punch_status regressed` (author `inspector`), then file the cluster again (step 6) with what the new record shows the fix missed.
    - **Waiting:** anything else — fewer than two clean receipts since the fix, no replay of its task yet, a week the scorer read nothing, a skill used mostly outside this Project's chats. → leave the item `applied`, `add_punch_note` (author `inspector`) saying which part is still missing; never change its status. A count that moved by one is never the reason for verified or regressed.
  - **2b — `held`, `failed`, and `needs-brief` items (Amendment 1, decision A-077):** `list_punch_items` status `["held","failed"]`. Re-check the live target. Still true and now safe → `set_punch_status open` (author `inspector`) with a fresh `add_punch_note` (author `inspector`) carrying an updated draft. No longer true, or unsafe to touch → `set_punch_status refused` (author `inspector`) with the reason. Separately, `list_punch_items` status `["needs-brief"]`: for each, read its notes for a DA-added Build Brief id (a `da`-authored note naming a `BB-...` id, per `skills/design-assist/SKILL.md` step 1's third intake pull); if that brief's plan has reached `succeeded`, `set_punch_status verified` (author `inspector`) — the brief's own build is the "repair," so the item closes as verified directly rather than passing through `applied`. No BB id yet, or the named brief hasn't succeeded → leave as `needs-brief`, no action.
- *Success evidence:* every `applied`/`held`/`failed` item from before the checkpoint has a new status or, for a step-in item, a waiting note; every `needs-brief` item was checked against its named brief's status.
- *Recovery (Amendment 2, decision A-080):* a target file that 404s → leave the status unchanged and `add_punch_note` (author `inspector`) explaining what couldn't be read; never guess, and never call `set_punch_status held` here — `held` is Repairer-only under A-077. If the target is permanently gone (repo deleted, path will never come back), `set_punch_status refused` (author `inspector`) with the reason. The receipts, run notes or `tests/fixed-set.md` can't be read → the step-in item is waiting, never verified.

**3. Map vs. shipped.**
- *Precondition:* step 2 complete.
- *Action:* read plans with status `succeeded` since the checkpoint (and their close-out snapshots), and compare against `get_entity('stack-map')` using the review checklist in `skills/inspector/references/map-review-checklist.md` (accurate against live state? duplicate? conflicts with a prior decision via `get_decision_chain`? best wording/layer?). **First walk only:** also use the 22 open MAP-EDIT next moves on the `stack-map` Project State project as leads, and apply SM-043's layer vocabulary (decision SM-044, Charles-approved).
- *Success evidence:* one `file_punch_item` (kind `map`) per real difference found, each with the exact edit drafted in `draft_text`.
- *Recovery:* `get_entity('stack-map')` unreachable → hold the whole map-comparison sub-step for this walk, note it in the walk summary (step 7), and retry next walk — do not file speculative map items without reading the live entity.

**3b. Timed jobs vs. map schedules** (Build 11.7.13, BB-2026-10-12-stack-day-calendar).
- *Precondition:* step 3 read the live `stack-map` entity.
- *Action:* collect every clock-timed job that is switched on: (i) `crons` in each `vercel.json` (cbrain `services/vercel.json`, email-watcher, subscription-content-mcp, cbrain-ui on its production branch only — Vercel crons don't run on previews), (ii) uncommented `on: schedule: - cron:` lines in `.github/workflows/*.yml` of cbrain, cbrain-ui, world-graph and yt-relay, (iii) `list_triggers` (recurring, enabled Claude scheduled tasks). For each, look for a matching entry in some dot's `flow_nodes[].ops.schedule` list — same cron (ignore a `CRON_TZ=` prefix; compare its zone with the entry's `tz`). Also flag the reverse: a schedule entry without `paused: true` whose cron no longer exists or is switched off, and a `paused: true` entry whose cron has been switched back on.
- *Success evidence:* one `file_punch_item` (kind `map`, tier `auto`) per mismatch, `target_path` `concepts/stack-map.md`, with the exact `schedule` entry to add, remove or flip drafted in `draft_text` (`label`, `cron`, `tz`, `where`, plus `paused`/`assumed`/`acts_at` when they apply). These are verified defects, so one record is enough for the step 6 gate.
- *Recovery:* a repo or `list_triggers` can't be read → skip that source for this walk and say so in the walk summary; never file a "missing" item from a source you couldn't read. A job that only a person can see (the PC's Task Scheduler) is never flagged — its entry carries `assumed: true`.

**4. Gather evidence.**
- *Precondition:* step 3 complete.
- *Action, two buckets:*
  - **Since the checkpoint:** lessons (not step-in records), `noted` disclosures (read-only — the Inspector never disposes a disclosure, that's DA's job), failed/blocked plans, and next moves open more than 14 days with no owner. Cap 60 records total for this bucket.
  - **Step-ins, all time:** `find_by_tags` `["step-in"]`, entity_types `["lesson"]`, project total-harness; keep only step-in records (exact tag, see Step-in terms) and take the newest 40 by chat date. This bucket is outside the 60 cap and is read in full every walk, so a cluster counts records from every walk, not only since the last one. Set aside records tagged `unchecked` or `step-in-unsure`: counted in the summary, never clustered. `N` = records kept; `M` = those created since the checkpoint.
- *Success evidence:* a bounded record set (≤60, plus ≤40 step-in records), each tagged with its source bucket.
- *Recovery:* more than 60 candidate records → take the 60 most recent, note the overflow count in the walk summary so the next walk's window isn't lost. More than 40 step-in records → note the overflow; the older ones are read again next walk only if they fall back inside the newest 40, so a cluster that big has already cleared the gate. Step-in records can't be read → say so in the summary and the checkpoint's first line reads `Read 0 step-ins: <reason>`.

**5. Cluster and check coverage.**
- *Precondition:* step 4 complete.
- *Action:* group the gathered records by the rule/target they point at. Step-in records are grouped by **what was missed** — the rule Claude didn't follow or the place the fix would live, read from the situation and lesson text. The `pattern-*` and `skill-*` tags only narrow where to look; two records sharing a tag are never a cluster on that alone, and `skill-none` or `pattern-other` records are grouped only by what they say. A step-in record may join a cluster of other evidence (a lesson or disclosure pointing at the same rule). For each cluster, read the live target to see whether it already covers the issue (a prior walk or a direct edit may have already fixed it), and check for a **live fix**: an `open`, `applied`, `verified` or `needs-brief` Punch List item for the same target and miss, or a direct edit to the target that covers it (find its commit with `list_commits` on that path).
- *Success evidence:* each cluster is marked either "already covered" (drop it, naming the fix and its commit or item id in the walk summary) or "still open" (proceeds to step 6). A step-in cluster covered by a direct edit is still open when any of its records is dated after that edit's commit: that is a regression of the direct fix, filed in step 6 with the new record as evidence.
- *Recovery:* ambiguous whether it's covered → treat as still open and let the rubric gate (step 6) decide, rather than guessing it away.

**6. Rubric gate.**
- *Precondition:* step 5 complete.
- *Action:* for each still-open cluster, file (`file_punch_item`) only if **all** hold: ≥2 records point at it, or 1 is a verified defect; a target is named; the exact fix text is drafted (`draft_text`); a tier is assigned (`auto` vs `needs-brief`, per the Authority tiers table in the brief); the target is not on the protected list; the fix is not a declined LEDGER row or a deferred next move (e.g. C-048). Set `adv_id` when the cluster's evidence lands on the same fix as an open Advisor idea — never because the Inspector is doing that idea's work, only because the evidence independently converged there.
  **Step-in clusters** need two or more step-in records **from different chats** (a step-in record is never a verified defect on its own), and file two items:
  1. **The rule edit.** `evidence` names every step-in lesson display id behind it, with each chat and date. Tier: `auto` when it adds or clarifies a rule in a skill's body or a reference file; `needs-brief` when it touches a skill's description or triggers, an `AGENT.md` row, `references/charter.md`, an Our way line marked `Charles`, a new skill, or deletes a rule (A-074).
  2. **Its fixed-set task**, filed right after, kind `other`, `target_path` `tests/fixed-set.md`, `target_section` `Tasks`, `draft_text` the whole task in the file's shape, numbered one past the highest task there:
     - `### T<n>. <short name> (from step-ins <ids>)`
     - `**From:** <the rule edit's display id>; step-ins <ids>`
     - `**Ask:**` what Charles would say, in his words, that led to the step-ins
     - `**Touches:**` the file the rule edit lands in (the routing files every task touches are implied)
     - `**Key:**` numbered points, each citing its source in brackets; a point true only for now carries `until:`
     Tier: `auto` only when every key point cites a decision, Charles's dated words, or a lesson the scorer did not write (its source does not start `Step-in scorer`); otherwise `needs-brief`. A needs-brief task never holds back the rule edit; the rule edit is filed and applied on its own tier.
- *Success evidence:* a `file_punch_item` call per filed item, or an explicit hold-back note (see step 7) per cluster that didn't clear the gate. Every filed step-in rule edit has its task item, and the task's `From:` line names the rule edit.
- *Recovery:* uncertain on any one criterion → hold back. The design intent is explicit: a missed fix costs a week; a wrong rule change costs every chat. Records from one chat only → hold back and note it; the next walk counts them again.

**7. Write the checkpoint.**
- *Precondition:* steps 1–6 complete (even if some sub-steps held back or errored — the walk still closes).
- *Action:* insert a new `punch_checkpoints` row (`agent: 'inspector'`, `walked_through: now()`). `summary` first line, exactly: `Read N step-ins (M new), filed F, verified V, waiting W, regressed R` — F counts every item filed this walk, V/W/R the step-in items from step 2a. Then one line: counts of other records seen / filed / held / verified / regressed, plus the step-in records set aside as `unchecked` or `step-in-unsure`, each covered cluster with its fix, and any overflow.
- *Success evidence:* the new checkpoint row exists and is now the latest for `agent = 'inspector'`.
- *Recovery:* the checkpoint write itself fails → do not silently end the walk; retry once, then report the walk as incomplete rather than claiming success with no checkpoint (a missing checkpoint would make the *next* walk re-scan everything).

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: "Weekly rules walk" (thread_key "job:inspector-weekly-walk")
- Opens when: a walk ends incomplete (no checkpoint written) or skips a source it couldn't read. Findings themselves go on the Punch List, not the Next steps list
- Checks in: when a run leaves something open
- Closes when: a later walk completes with every source read and its checkpoint written (`close_thread`, closed_how "walk completed"), or Charles clicks Done

## Examples

### Example 1: known-answer first walk

Untold, the first walk's evidence-gathering step (4) surfaces lessons E-080, E-085, CB-062/063, E-222, A-041, D-083 — all versions of "a freshly deployed MCP tool wasn't callable in the same session." Clustered (step 5) as one rule with 6 supporting records, well past the ≥2 threshold. The rubric gate (step 6) passes: named target (`agent-library/references/gotchas.md`, a new bullet), exact fix drafted, tier `auto`, not protected, not declined. Filed with `adv_id: ADV-008`. The Repairer applies it on its next run.

### Example 2: hold-back

A single lesson mentions a Vercel deploy taking longer than expected. One record, not a verified defect, no second corroborating record — the rubric gate's "≥2 records or 1 verified defect" fails. Held back; noted in the walk summary rather than filed.

### Example 3: a step-in cluster already covered (Build 76 dry walk, 2026-11-10)

Step 4's step-in bucket holds TH-157 (graph engineering chat, 2026-11-04) and TH-158 (loop scope chat, 2026-11-09), both `step-in`, neither `unchecked`. Both say a chat handed a YouTube link said it could not get the transcript instead of checking the store and queueing the video: one cluster, two different chats. Step 5 finds the live fix: the `AGENT.md` Outside content row and `references/youtube-transcript.md`, both from commit 7c1c19b (2026-11-09 evening, Indianapolis), and task T4 already checks it. Both chat turns come before that commit (the fix was written in answer to the second), so the cluster is covered and nothing is filed. Checkpoint first line: `Read 2 step-ins (2 new), filed 0, verified 0, waiting 0, regressed 0`. A step-in on this miss dated after 7c1c19b would make it still open and be filed as a regression.

### Example 4: a step-in cluster filed (Build 76 dry walk, planted records)

Two step-in records from different chats, both `pattern-cant-reach`, `skill-none`: asked what a Stack Flow dot says, Claude said the stack map was too big to open and asked Charles to paste the dot. One cluster on what was missed; no gotcha covers it. Step 6 drafts (1) a rule edit, tier `auto`: a new bullet in `references/gotchas.md` saying the over-limit reply saves the file locally and the dot is read from there or from `get_entity('stack-map')`; and (2) its task, `**From:**` that item, `**Touches:** references/gotchas.md`, tier `needs-brief` because its only key sources are the two scorer-written lessons. The rule edit goes ahead regardless.

## Pitfalls

> Every pitfall must come from a real trace.

- **A suggestion can be true and still get rejected**, if a more considered prior decision already covers the ground and the suggestion doesn't add a reason to revisit it. Accuracy is necessary, not sufficient — always check `get_decision_chain` on a related prior `stack-map` decision before filing a map item that would reverse it. (Verbatim from `skills/stack-manager/SKILL.md` v0.1.0, the skill the Inspector's map-comparison job was split from — see `skills/inspector/references/map-review-checklist.md`.)
- **Role enforcement was added after the first design pass** (decision A-077, ABO-J-002): the original `set_punch_status` let any author set any status, so "verifier ≠ applier" rested only on a text-convention scan. Don't assume a text convention is sufficient protection for a safety invariant — prefer enforcing it in the tool itself when the cost of a second migration is avoidable.
- **Two outcomes misread a fix.** With only verified or regressed, a step-in fix would read as regressed on the first walk after it landed (a record filed late, dated before the fix), and a week the scorer read no chats would read as proof it worked. Hence the three outcomes, dating by chat turn, and clean receipts only. (Scoring-and-testing seat, TH-160 finding 1.)
- **`find_by_tags` expands tags fuzzily**: `step-in` also returns `step-in-receipt` and `step-in-unsure` rows. Keep only rows whose own tags hold exactly `step-in`. (skills/step-in-scorer, Pitfalls.)

## Changelog

- **0.2.0** (2026-11-10) — Reads step-in records and checks fixes by effect. Step 4 gains an all-time step-in bucket (newest 40, outside the 60 cap; `unchecked` and `step-in-unsure` set aside). Step 5 clusters step-ins by what was missed, never by tag alone, and treats a step-in dated after a direct fix as still open. Step 6 files a step-in cluster (two or more chats) as a rule edit plus its fixed-set task with `From:` and `Touches:` lines, each on its own tier. Step 2a: a step-in item is verified only after a clean replay and two clean receipts, regressed only on a confirmed later step-in, and otherwise waiting. Step 7's first line is the step-in count. Examples 3 and 4 are this build's dry walks. Per Build 76 (BB-2026-11-09-inspector-reads-step-ins).
- **0.1.2** (2026-10-23) — Progress tracking section after How. Per BB-2026-10-21-next-steps-panel.
- **0.1.1** (2026-10-13) — Step 3b added: every switched-on cron (vercel.json, workflow schedules, Claude scheduled tasks) must have a matching `ops.schedule` entry on the stack map, which feeds the Stack Flow Day view; a mismatch is a Punch List item (kind `map`). Per Build 11.7.13 (BB-2026-10-12-stack-day-calendar).
- **0.1.0** (2026-09-22) — Initial draft, written per BB-2026-09-21-inspector-repairer Phase 2, incorporating Amendment 1 (decision A-077: held/failed/needs-brief handling in step 2b). `status: draft` pending the first live walk (Phase 2 acceptance runs, next session).
- **0.1.0** (2026-09-22) — Amendment 2 (decision A-080): step 2's Recovery clause no longer calls `set_punch_status held` on a 404'd target (`held` is Repairer-only under A-077) — it now leaves the status unchanged with an explanatory `add_punch_note`, and uses `refused` only when the target is permanently gone. Per BB-2026-09-21-inspector-repairer step 12a.
