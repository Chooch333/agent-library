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

## Stack Flow (added 2026-09-23, BB-2026-09-23-stack-flow)

- **Stack Flow (flow_nodes / flow_edges on the stack-map page).** Every skill whose wiring says `runs: on-its-own` has a flow dot (its `skill` field). Every flow edge still matches what the skill's wiring says it reads and writes, or what the component's job says it does. A new stack component that moves information has a dot and its edges. A dot's small text still says where it really runs. Color is decided by `role`, never by host. File any difference as a `map` Punch List item with the exact YAML edit drafted.

### Part facts and stories (added 2026-10-05, Build 11.7.11 (BB-2026-10-04-stack-flow-part-stories))

- **Four facts on every `made_of` part.** Each part carries `runs_on` (the exact thing that runs it, named the way the product names it — e.g. "Vercel Cron Job → function in Vercel project email-watcher, every 15 min", "Claude Code scheduled task (cloud)", "Nothing — it's a folder"), `thinks_with` (AI model + how it's paid, or exactly "No AI"; never a guessed model name), `instructions` ("Its own code in the <repo> repo" and/or "Skill: <path> in agent-library"), and `saves_to` (repo + folder, Supabase project + table, Gmail label, or "Nothing"). A fact that can't be confirmed says "not confirmed — <why>". Check each fact against the code/config the part's `ref` points to.
- **Story and overview.** Each part carries `story` (2–4 plain sentences written only from the four facts plus `does`/`lives`; no file paths or code names). Each dot carries `overview` (2–4 sentences, end to end, saying where results land). The Stack Flow side panel shows `overview` and `story`, never `ref` or the four facts.
- **Rewrite rule.** Whenever any of the four facts (or `does`/`lives`) changes, `story` — and the dot's `overview` if affected — must be rewritten from the updated facts in the same change. File as a `map` Punch List item: a `story` or `overview` that contradicts its facts; a fact that doesn't match what its `ref` shows; a part missing any of the five fields (`runs_on`, `thinks_with`, `instructions`, `saves_to`, `story`); a dot missing `overview`.
