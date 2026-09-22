# Stack-map edit playbook

*Copied verbatim from `roles/stack-manager/SKILL.md` v0.1.0 (steps 5 and 8, and the full Rules section), per BB-2026-09-21-inspector-repairer step 6 — the Repairer's target-editing job (when the target is the stack-map) is the split-off half of what Stack Manager used to do alone. Stack Manager itself is now a deprecated pointer (`roles/stack-manager/SKILL.md`); this is the surviving copy of its editing procedure and rules.*

## Editing the map (step 5, verbatim)

**5. If accepting or modifying:** edit `concepts/stack-map.md` via `replace_in_file` (exact-anchor discipline — the old string must be unique in the file), touching both the frontmatter `components` entry and its mirror row in the `## Components` table so the two stay in sync. Then `rebuild_index` (incremental) on cbrain.

## Verifying the edit (step 8, verbatim)

**8. Batch close.** If anything was committed to the map this run, verify `get_entity('stack-map')` still parses (frontmatter loads, `components` is a valid list). End the run with a one-line summary note on `stack-map` (suggestions seen / accepted / modified / rejected) so a run's shape is visible without re-deriving it from individual decisions.

## Rules (verbatim)

- **Never edit the map without a decision row.** The decision *is* the audit trail; an edit with no decision breaks the reconstruction chain the whole design exists to guarantee.
- **Never dispose without completing the move.** A suggestion that was reasoned about but left open is indistinguishable from one that was never reviewed — always `complete_next_move`, including on reject.
- **Frontmatter field names are a contract.** `id`, `layer`, `status`, `job`, `competes_with`, `depends_on` are consumed by skills (`get_entity`) and the cbrain UI's graph view. Extend with new fields if a suggestion genuinely needs one; never rename or repurpose an existing field.
- **Conflicts between the map and live state resolve toward live state**, and the resolution is logged — the map is a description, not the source of truth about the stack itself.
- **Rejections leave the same trail shape as acceptances.** A reject still gets a decision with rationale and a completed move; there is no lighter-weight path for "no."
- **This role never files suggestions, only disposes them.** Noticing an unrelated stack drift while reviewing the queue is not licence to edit the map outside the suggestion it was invoked to resolve — file that observation as its own `MAP-EDIT` suggestion for a future pass instead.

*(The Repairer adapts "never edit the map without a decision row" to its own equivalent: never apply a Punch List item without writing back via `set_punch_status applied` — the Punch List item + note is the Repairer's audit trail, playing the role the decision row played for Stack Manager. "Never dispose without completing the move" maps to "never leave an item picked up without a terminal write" — `applied`, `held`, or `failed`, never silently abandoned mid-run.)*
