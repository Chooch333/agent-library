# Map review checklist

*Copied verbatim from `roles/stack-manager/SKILL.md` v0.1.0 (step 3 and its related pitfall), per BB-2026-09-21-inspector-repairer step 5 — the Inspector's map-comparison job is the split-off half of what Stack Manager used to do alone. Stack Manager itself is now a deprecated pointer (`roles/stack-manager/SKILL.md`); this is the surviving copy of its reasoning checklist.*

## The checklist (Stack Manager SKILL.md v0.1.0, step 3, verbatim)

**3. Reason over the suggestion.** For each `MAP-EDIT: <component id> — <proposed change> — <reason> — source: <session/build id>` row, ask:
   - **Accurate against live state?** Where the suggestion claims a fact (a status transition, a new dependency), spot-check it if a cheap live check exists (a `Project_State` plan/project lookup, a repo check). Do not fabricate a check that does not exist — reason from what the suggestion states and what the map already says.
   - **Duplicate?** Does an open or very-recently-disposed suggestion already cover this exact change? If so, treat as a duplicate rather than re-litigating (reject or merge into the reasoning of the disposition, noting the duplicate).
   - **Conflicting with a prior decision?** Pull `get_decision_chain` on any related prior `stack-map` decision if the suggestion appears to reverse or contest one. A suggestion that contradicts a considered, still-valid prior decision needs a stated reason to override it, not a silent accept.
   - **Better phrased or scoped differently?** A suggestion can be directionally right but need tightening (wrong `layer`, `job` wording that drifts from house style, a `depends_on` edge that should point at a different id). That is a **modify**, not a straight accept.

*(The Inspector adapts this to its own evidence — a difference between `get_entity('stack-map')` and what actually shipped — rather than an incoming `MAP-EDIT` suggestion row, since map suggestions are retired. The four questions apply unchanged.)*

## The pitfall (verbatim)

**A suggestion can be true and still get rejected**, if a more considered prior decision already covers the ground and the suggestion doesn't add a reason to revisit it. Accuracy is necessary, not sufficient — see step 3's duplicate/conflict checks before defaulting to accept.
