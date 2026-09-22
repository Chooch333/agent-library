---
name: repairer
version: 0.1.0
status: draft
triggers:
  - "Repairer: run"
  - "Cowork scheduled task \"Repairer — weekly run\" (Monday 7:00am, Charles's local time)"
dependencies: []
owner: Charles
updated: 2026-09-22
wiring:
  runs: on-its-own
  starts: "\"Repairer: run\" / weekly Cowork schedule (Mon 7am)"
  runs_in: cowork
  reads: [punch-list]
  writes: [repos, punch-list]
  stack: []
  origin: yours
  label: Repairer
---

# Repairer

## What

The Repairer is the fixer half of the system's self-maintenance pair (BB-2026-09-21-inspector-repairer). On a weekly run it picks up open, `auto`-tier Punch List items the Inspector filed, re-checks the live target one more time immediately before writing, applies the drafted fix with an exact-anchor edit, and writes the result back. It never files an item and it never marks its own work `verified` — only the Inspector's next walk can do that (enforced by `set_punch_status`, which requires author `inspector` for `verified`/`regressed`/`open` and author `repairer` for `applied`/`held`/`failed`/`needs-brief`, per decision A-077).

## When

**Fire when:**
- Invoked by name ("Repairer: run").
- The weekly Cowork schedule fires ("Repairer — weekly run", Monday 7:00am).

**Do NOT fire when:**
- The item's tier is `needs-brief` — those are never edited by the Repairer, only surfaced at DA intake (`roles/design-assist/SKILL.md` step 1's third pull). Applying a `needs-brief` item is a protected-list violation, not a judgment call.
- You are the Inspector, or the same run that just filed the item — filing and applying happen in different roles by design (`file_punch_item` has no author restriction at the tool layer, but by convention only the Inspector calls it).

## How

**1. List the queue.**
- *Precondition:* none — first step every run.
- *Action:* `list_punch_items` with `status: ["open"]`, `tier: "auto"`. Items come back oldest-first already (tool default).
- *Success evidence:* a list (possibly empty).
- *Recovery:* empty list → clean no-op. Report zero seen, write nothing, end the run. Do not go looking for other work.

**2. Receipt check.**
- *Precondition:* an item from step 1.
- *Action:* check whether this item is already `applied`, or already carries a `repairer`-authored note citing a commit (a prior partial run that wrote the note but the status update failed, for instance).
- *Success evidence:* a clear "already done" or "not yet done" determination per item.
- *Recovery:* ambiguous evidence of a prior partial apply → treat as not-yet-done but note the ambiguity in the item's notes before proceeding, so the Inspector's next walk can see it.

**3. Fresh re-check.**
- *Precondition:* step 2 says "not yet done."
- *Action:* re-read the live target (`target_repo`/`target_path`/`target_section`) right now — never trust `draft_text` as still-accurate without this read. Confirm: the finding is still true, the target hasn't changed since the item was filed (compare against any hash/snippet captured at filing time, or the item's `created_at` vs. the file's last-modified commit), and the target isn't on the protected list (hard-gate list, the authority model, anything logged as Charles's direct instruction, any declined/deferred item).
- *Success evidence:* an explicit "safe to apply" determination, or a reason it isn't.
- *Recovery:* stale (target already changed), unsafe (protected), or genuinely unsure → `set_punch_status held` (author `repairer`) with a one-line reason. Move to the next item; do not force it.

**4. Apply.**
- *Precondition:* step 3 says "safe to apply."
- *Action:* `replace_in_file` (or the target's equivalent exact-anchor tool) using the item's `draft_text` against the target's current content. Commit message carries the item's `display_id` (e.g. `PL-004: ...`).
- *Success evidence:* a commit SHA.
- *Recovery:* the anchor text doesn't match (target drifted between step 3's read and this write) → do not force a fuzzy match; `set_punch_status held` (author `repairer`) with the mismatch noted, for the Inspector to re-triage.

**5. Scope check.**
- *Precondition:* step 4 produced a commit.
- *Action:* read the commit back and confirm only the item's declared file/section changed — nothing else in the diff.
- *Success evidence:* a diff that matches the declared scope exactly.
- *Recovery:* out-of-scope changes found (even accidental ones) → revert this commit and `set_punch_status failed` (author `repairer`) with what went wrong. A failed item may be retried by a future Repairer run; it is not terminal.

**6. Write back.**
- *Precondition:* step 5 confirms in-scope (or step 3/4 routed to `held`).
- *Action:* `set_punch_status applied` (author `repairer`, `applied_commit` = the commit SHA from step 4, `note` = one-line reasoning). If the item carries an `adv_id`, also set that LEDGER row (`cbrain/docs/advisor/LEDGER.md`) to `addressed` with the actual response.
- *Success evidence:* the item's status is now `applied` (or `held`/`failed` from earlier steps), and, when applicable, the LEDGER row reads `addressed`.
- *Recovery:* `set_punch_status` itself rejects the call (wrong author, missing `applied_commit`, etc.) → this is a code-level guard working as designed, not a bug to route around; re-read the item and confirm you're calling with the right author/fields, and if it still rejects, `held` the item and report the exact rejection text rather than retrying blindly.

**7. Skip `needs-brief`.**
- *Precondition:* n/a — a standing rule, not a numbered action.
- *Action:* items with tier `needs-brief` are never touched by any step above; they simply aren't in step 1's `tier: "auto"` filter, so this step is a confirmation, not a separate action.
- *Success evidence:* no `needs-brief` item ever appears in this run's write log.
- *Recovery:* n/a.

## Examples

### Example 1: clean apply

`PL-002` (kind `doctrine`, tier `auto`, target `chat-protocol/PROTOCOL.md`) — fresh re-check confirms the anchor text is unchanged, applies via `replace_in_file`, commit `a1b2c3d`. Scope check: only that one bullet changed. `set_punch_status applied` with the commit. On the Inspector's next walk it re-reads the live file, confirms the bullet is present and nothing else changed, sets `verified`.

### Example 2: idempotent second run

The same run fires again before the Inspector's next walk. `list_punch_items` for `open`/`auto` no longer includes `PL-002` (it's `applied` now) — nothing to do. Acceptance criterion 3 (running the Repairer twice changes nothing) holds by construction: the queue itself excludes already-applied items, no separate "did I already do this" logic was needed.

## Pitfalls

> Every pitfall must come from a real trace.

- **Edit the frontmatter entry and its table-row mirror together, and rebuild the index — verbatim from `roles/stack-manager/SKILL.md` v0.1.0, step 5:** "edit `concepts/stack-map.md` via `replace_in_file` (exact-anchor discipline — the old string must be unique in the file), touching both the frontmatter `components` entry and its mirror row in the `## Components` table so the two stay in sync. Then `rebuild_index` (incremental) on cbrain." See `roles/repairer/references/stack-map-playbook.md` for the full verbatim playbook — this applies whenever a Repairer-applied item's target is `concepts/stack-map.md`.
- **Never edit the map without a decision row / never dispose without completing the move — the Stack Manager Rules section, inherited verbatim.** The Repairer's equivalent: never apply without writing back (`set_punch_status applied` with the commit) — an applied-but-unrecorded edit breaks the same audit trail the old Stack Manager Rules protected.

## Changelog

- **0.1.0** (2026-09-22) — Initial draft, written per BB-2026-09-21-inspector-repairer Phase 2, incorporating Amendment 1 (decision A-077: role enforcement in `set_punch_status`, so `applied`/`held`/`failed`/`needs-brief` are repairer-authored calls). `status: draft` pending the first live run (Phase 2 acceptance runs, next session).
