---
name: stack-manager
version: 0.1.0
status: draft
triggers: ["Stack Manager: review queue" (on-demand, invoked by name), open next_moves on the `stack-map` Project State project (becomes a heartbeat-orchestrator interval task once that ships)]
dependencies: [stack-map, project-state, cbrain]
owner: Charles
updated: 2026-07-21
---

# Stack Manager

## What

The Stack Manager is the **sole disposer** of the stack-map suggestion queue. cbrain holds one canonical self-description of Charles's tech stack — `concepts/stack-map.md`, loaded in one call via `get_entity('stack-map')` — and nobody edits it ad hoc. Build sessions that ship a stack change file a cheap, unreviewed **suggestion** (an open `next_move` on the `stack-map` Project State project, `MAP-EDIT` format). The Stack Manager is the dedicated reviewer that holds the whole map in view, reasons over each suggestion, and disposes of it **fully autonomously** — accept, modify, or reject — leaving a decision row that says why. This is a separation of concerns: proposers notice drift cheaply mid-build; one disposer with full context makes the edit calls with reasoning on the record (BB-2026-07-20-stack-map, design intent).

Charles reviews the **trail** — decisions on `stack-map` plus `concepts/stack-map.md`'s git history — never the queue itself. He is not a mid-queue tiebreaker.

## When

**Fire it when:**

- Invoked by name ("Stack Manager: review queue") with one or more open `next_move` rows on the `stack-map` Project State project waiting to be disposed.
- On the interval the heartbeat-orchestrator schedules, once that component ships (still `status: planned` on the map itself — until then this role is on-demand only).

**Do NOT fire it when:**

- The queue is empty. List first; if there is nothing open, that is a clean no-op run — report zero seen, write nothing, do not go looking for work.
- You are the session that just shipped the stack change. Filing sessions file a suggestion and stop; they never dispose their own suggestion in the same breath. That would collapse the proposer/disposer separation the whole design rests on.

## How

The review loop. Process open `next_move` rows on `stack-map` **oldest first**.

**1. List the queue.** Pull every open `next_move` on the `stack-map` Project State project. Empty queue → no-op cleanly (see above).

**2. Read the current map.** `get_entity('stack-map')` for the frontmatter + compiled body. Use `get_file_contents` on `Chooch333/cbrain` `concepts/stack-map.md` when the disposition will need exact-anchor text for `replace_in_file` — `get_entity` gives you the compiled truth to reason over, not necessarily byte-identical source for surgical edits.

**3. Reason over the suggestion.** For each `MAP-EDIT: <component id> — <proposed change> — <reason> — source: <session/build id>` row, ask:
   - **Accurate against live state?** Where the suggestion claims a fact (a status transition, a new dependency), spot-check it if a cheap live check exists (a `Project_State` plan/project lookup, a repo check). Do not fabricate a check that does not exist — reason from what the suggestion states and what the map already says.
   - **Duplicate?** Does an open or very-recently-disposed suggestion already cover this exact change? If so, treat as a duplicate rather than re-litigating (reject or merge into the reasoning of the disposition, noting the duplicate).
   - **Conflicting with a prior decision?** Pull `get_decision_chain` on any related prior `stack-map` decision if the suggestion appears to reverse or contest one. A suggestion that contradicts a considered, still-valid prior decision needs a stated reason to override it, not a silent accept.
   - **Better phrased or scoped differently?** A suggestion can be directionally right but need tightening (wrong `layer`, `job` wording that drifts from house style, a `depends_on` edge that should point at a different id). That is a **modify**, not a straight accept.

**4. Dispose.** Exactly one of:
   - **Accept** — apply the suggestion to the map as written.
   - **Modify** — apply an improved version; the decision must say what changed from the suggestion as filed and why.
   - **Reject** — do not touch the map; the decision must say why.

   Fully autonomous. Never escalate a map-edit disposition to Charles — there is no hard gate here (no credentials, no spend, nothing irreversible; every edit is git-versioned and reversible).

**5. If accepting or modifying:** edit `concepts/stack-map.md` via `replace_in_file` (exact-anchor discipline — the old string must be unique in the file), touching both the frontmatter `components` entry and its mirror row in the `## Components` table so the two stay in sync. Then `rebuild_index` (incremental) on cbrain.

**6. Log the decision.** `log_decision` on `stack-map`: title naming the component and the disposition, rationale stating the reasoning from step 3, `provenance` naming the suggestion's `next_move` id and its `source`, tags `judgment-call` plus `map-edit` (accept/modify) or `map-reject` (reject).

**7. Complete the move.** `complete_next_move` on the suggestion's `next_move` id, referencing the decision (pass `completed_by_plan_id` only if this run is itself tracked as a plan; otherwise the decision row is the cross-reference — name the decision id in the completion context if the tool call allows it, otherwise rely on matching timestamps between the decision and the completed move).

**8. Batch close.** If anything was committed to the map this run, verify `get_entity('stack-map')` still parses (frontmatter loads, `components` is a valid list). End the run with a one-line summary note on `stack-map` (suggestions seen / accepted / modified / rejected) so a run's shape is visible without re-deriving it from individual decisions.

## Rules

- **Never edit the map without a decision row.** The decision *is* the audit trail; an edit with no decision breaks the reconstruction chain the whole design exists to guarantee.
- **Never dispose without completing the move.** A suggestion that was reasoned about but left open is indistinguishable from one that was never reviewed — always `complete_next_move`, including on reject.
- **Frontmatter field names are a contract.** `id`, `layer`, `status`, `job`, `competes_with`, `depends_on` are consumed by skills (`get_entity`) and the cbrain UI's graph view. Extend with new fields if a suggestion genuinely needs one; never rename or repurpose an existing field.
- **Conflicts between the map and live state resolve toward live state**, and the resolution is logged — the map is a description, not the source of truth about the stack itself.
- **Rejections leave the same trail shape as acceptances.** A reject still gets a decision with rationale and a completed move; there is no lighter-weight path for "no."
- **This role never files suggestions, only disposes them.** Noticing an unrelated stack drift while reviewing the queue is not licence to edit the map outside the suggestion it was invoked to resolve — file that observation as its own `MAP-EDIT` suggestion for a future pass instead.

## Worked example

Not yet available — this skill's queue-disposal loop has not run against a real suggestion. `status: draft` reflects that, per the same convention `roles/archivist/SKILL.md` uses for an unrun skill. The first live run is the validation step in BB-2026-07-20-stack-map (Directive 8); its worked trace gets folded in here afterward and `status` moves to `active`, matching how `archivist` handles its own not-yet-verified state.

## Pitfalls

- **Don't dispose your own suggestion.** If the Stack Manager is invoked by the same session/build that just filed a `MAP-EDIT`, it still reviews on the merits — the proposer/disposer separation is about roles never colliding *by convention*, not about the Stack Manager refusing suggestions from any particular source.
- **A suggestion can be true and still get rejected**, if a more considered prior decision already covers the ground and the suggestion doesn't add a reason to revisit it. Accuracy is necessary, not sufficient — see step 3's duplicate/conflict checks before defaulting to accept.
- **The frontmatter table and the body table can drift** if an edit touches one and not the other. Directive 2's initial commit keeps both in lockstep; every disposal edit must too (step 5).

## Changelog

- **v0.1.0 (2026-07-21)** — Initial skill (BB-2026-07-20-stack-map, Directive 6), written from the brief's Appendix C skeleton in the house style of `roles/archivist/SKILL.md`. `status: draft` pending the first live queue-disposal run (Directive 8 validation).
