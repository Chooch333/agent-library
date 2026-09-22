---
name: inspector
version: 0.1.0
status: draft
triggers:
  - "Inspector: walk"
  - "Cowork scheduled task \"Inspector — weekly walk\" (Sunday 9:00pm, Charles's local time)"
dependencies: []
owner: Charles
updated: 2026-09-22
wiring:
  runs: on-its-own
  starts: "\"Inspector: walk\" / weekly Cowork schedule (Sun 9pm)"
  runs_in: cowork
  reads: [project-state, cbrain, stack-map]
  writes: [punch-list]
  stack: []
  origin: yours
  label: Inspector
---

# Inspector

## What

The Inspector is the finder half of the system's self-maintenance pair (BB-2026-09-21-inspector-repairer). On a weekly walk it compares Project State evidence — lessons, disclosures, failed/blocked plans, stale next moves — and the shipped stack against cbrain's canonical stack-map, and files a Punch List item, with the exact fix already drafted, for anything that clears its rubric. It never edits a target itself and it never emails Charles — everything it finds becomes a Punch List item (`file_punch_item`) that the Repairer picks up, or a held-back note in its own walk summary. It also closes the loop: on its *next* walk it re-reads every item the Repairer applied and only then marks it `verified` — the fixer never grades itself (design intent, BB-2026-09-21-inspector-repairer).

## When

**Fire when:**
- Invoked by name ("Inspector: walk").
- The weekly Cowork schedule fires ("Inspector — weekly walk", Sunday 9:00pm).

**Do NOT fire when:**
- You are the Repairer, or any session that just applied a Punch List item — the Inspector's `verified` call must come from a separate walk, never the same run that applied the fix (enforced in code: `set_punch_status` rejects a `verified` call whose author matches the most recent `applied` note's author, and additionally requires author `inspector` for `verified`/`regressed`/`open`, per decision A-077).
- You are deciding whether a Stack Advisor idea (`ADV-NNN`) is worth building — that is the Advisor's and Charles's call, never the Inspector's. Read the LEDGER only to avoid re-filing a declined idea or to note a matching `adv_id`; never to pick up new work from it.

## How

Precondition / Action / Success evidence / Recovery for every step (Skill Design Framework Q7).

**1. Load the checkpoint.**
- *Precondition:* none — always the first step.
- *Action:* query the most recent `punch_checkpoints` row where `agent = 'inspector'` (take the single newest row).
- *Success evidence:* a checkpoint row (`walked_through` timestamp) or a confirmed empty result.
- *Recovery:* no checkpoint found (first-ever walk) → treat the window as "since 30 days ago" and proceed; do not fail the walk.

**2. Re-walk items that need a second look.**
- *Precondition:* step 1 complete.
- *Action, in two parts:*
  - **2a — `applied` items:** `list_punch_items` status `["applied"]`. For each, re-read the live target at `target_path`/`target_section` and confirm (i) the drafted change is present and (ii) nothing else in that file changed since `applied_commit` (compare against the commit's diff via the repo's commit API). Present and clean → `set_punch_status verified` (author `inspector`). Missing, reverted, or collateral changes found → `set_punch_status regressed` (author `inspector`), then `file_punch_item` a fresh fix-it item for the regression (kind matching the original, tier per the Authority tiers table).
  - **2b — `held`, `failed`, and `needs-brief` items (Amendment 1, decision A-077):** `list_punch_items` status `["held","failed"]`. Re-check the live target. Still true and now safe → `set_punch_status open` (author `inspector`) with a fresh `add_punch_note` (author `inspector`) carrying an updated draft. No longer true, or unsafe to touch → `set_punch_status refused` (author `inspector`) with the reason. Separately, `list_punch_items` status `["needs-brief"]`: for each, read its notes for a DA-added Build Brief id (a `da`-authored note naming a `BB-...` id, per `roles/design-assist/SKILL.md` step 1's third intake pull); if that brief's plan has reached `succeeded`, `set_punch_status verified` (author `inspector`) — the brief's own build is the "repair," so the item closes as verified directly rather than passing through `applied`. No BB id yet, or the named brief hasn't succeeded → leave as `needs-brief`, no action.
- *Success evidence:* every `applied`/`held`/`failed` item from before the checkpoint has a new status; every `needs-brief` item was checked against its named brief's status.
- *Recovery (Amendment 2, decision A-080):* a target file that 404s → leave the status unchanged and `add_punch_note` (author `inspector`) explaining what couldn't be read; never guess, and never call `set_punch_status held` here — `held` is Repairer-only under A-077. If the target is permanently gone (repo deleted, path will never come back), `set_punch_status refused` (author `inspector`) with the reason.

**3. Map vs. shipped.**
- *Precondition:* step 2 complete.
- *Action:* read plans with status `succeeded` since the checkpoint (and their close-out snapshots), and compare against `get_entity('stack-map')` using the review checklist in `roles/inspector/references/map-review-checklist.md` (accurate against live state? duplicate? conflicts with a prior decision via `get_decision_chain`? best wording/layer?). **First walk only:** also use the 22 open MAP-EDIT next moves on the `stack-map` Project State project as leads, and apply SM-043's layer vocabulary (decision SM-044, Charles-approved).
- *Success evidence:* one `file_punch_item` (kind `map`) per real difference found, each with the exact edit drafted in `draft_text`.
- *Recovery:* `get_entity('stack-map')` unreachable → hold the whole map-comparison sub-step for this walk, note it in the walk summary (step 7), and retry next walk — do not file speculative map items without reading the live entity.

**4. Gather evidence.**
- *Precondition:* step 3 complete.
- *Action:* since the checkpoint, pull: lessons, `noted` disclosures (read-only — the Inspector never disposes a disclosure, that's DA's job), failed/blocked plans, and next moves open more than 14 days with no owner. Cap 60 records total for this step.
- *Success evidence:* a bounded record set (≤60), each tagged with its source bucket.
- *Recovery:* more than 60 candidate records → take the 60 most recent, note the overflow count in the walk summary so the next walk's window isn't lost.

**5. Cluster and check coverage.**
- *Precondition:* step 4 complete.
- *Action:* group the gathered records by the rule/target they point at. For each cluster, read the live target to see whether it already covers the issue (a prior walk or a direct edit may have already fixed it).
- *Success evidence:* each cluster is marked either "already covered" (drop it) or "still open" (proceeds to step 6).
- *Recovery:* ambiguous whether it's covered → treat as still open and let the rubric gate (step 6) decide, rather than guessing it away.

**6. Rubric gate.**
- *Precondition:* step 5 complete.
- *Action:* for each still-open cluster, file (`file_punch_item`) only if **all** hold: ≥2 records point at it, or 1 is a verified defect; a target is named; the exact fix text is drafted (`draft_text`); a tier is assigned (`auto` vs `needs-brief`, per the Authority tiers table in the brief); the target is not on the protected list; the fix is not a declined LEDGER row or a deferred next move (e.g. C-048). Set `adv_id` when the cluster's evidence lands on the same fix as an open Advisor idea — never because the Inspector is doing that idea's work, only because the evidence independently converged there.
- *Success evidence:* a `file_punch_item` call per filed item, or an explicit hold-back note (see step 7) per cluster that didn't clear the gate.
- *Recovery:* uncertain on any one criterion → hold back. The design intent is explicit: a missed fix costs a week; a wrong rule change costs every chat.

**7. Write the checkpoint.**
- *Precondition:* steps 1–6 complete (even if some sub-steps held back or errored — the walk still closes).
- *Action:* insert a new `punch_checkpoints` row (`agent: 'inspector'`, `walked_through: now()`, `summary`: one line — counts of seen / filed / held / verified / regressed).
- *Success evidence:* the new checkpoint row exists and is now the latest for `agent = 'inspector'`.
- *Recovery:* the checkpoint write itself fails → do not silently end the walk; retry once, then report the walk as incomplete rather than claiming success with no checkpoint (a missing checkpoint would make the *next* walk re-scan everything).

## Examples

### Example 1: known-answer first walk

Untold, the first walk's evidence-gathering step (4) surfaces lessons E-080, E-085, CB-062/063, E-222, A-041, D-083 — all versions of "a freshly deployed MCP tool wasn't callable in the same session." Clustered (step 5) as one rule with 6 supporting records, well past the ≥2 threshold. The rubric gate (step 6) passes: named target (`chat-protocol/PROTOCOL.md`, a new standing-rule bullet), exact fix drafted, tier `auto`, not protected, not declined. Filed with `adv_id: ADV-008`. The Repairer applies it on its next run.

### Example 2: hold-back

A single lesson mentions a Vercel deploy taking longer than expected. One record, not a verified defect, no second corroborating record — the rubric gate's "≥2 records or 1 verified defect" fails. Held back; noted in the walk summary rather than filed.

## Pitfalls

> Every pitfall must come from a real trace.

- **A suggestion can be true and still get rejected**, if a more considered prior decision already covers the ground and the suggestion doesn't add a reason to revisit it. Accuracy is necessary, not sufficient — always check `get_decision_chain` on a related prior `stack-map` decision before filing a map item that would reverse it. (Verbatim from `roles/stack-manager/SKILL.md` v0.1.0, the skill the Inspector's map-comparison job was split from — see `roles/inspector/references/map-review-checklist.md`.)
- **Role enforcement was added after the first design pass** (decision A-077, ABO-J-002): the original `set_punch_status` let any author set any status, so "verifier ≠ applier" rested only on a text-convention scan. Don't assume a text convention is sufficient protection for a safety invariant — prefer enforcing it in the tool itself when the cost of a second migration is avoidable.

## Changelog

- **0.1.0** (2026-09-22) — Initial draft, written per BB-2026-09-21-inspector-repairer Phase 2, incorporating Amendment 1 (decision A-077: held/failed/needs-brief handling in step 2b). `status: draft` pending the first live walk (Phase 2 acceptance runs, next session).
- **0.1.0** (2026-09-22) — Amendment 2 (decision A-080): step 2's Recovery clause no longer calls `set_punch_status held` on a 404'd target (`held` is Repairer-only under A-077) — it now leaves the status unchanged with an explanatory `add_punch_note`, and uses `refused` only when the target is permanently gone. Per BB-2026-09-21-inspector-repairer step 12a.
