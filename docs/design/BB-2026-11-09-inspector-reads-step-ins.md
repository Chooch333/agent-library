# Build Brief — BB-2026-11-09-inspector-reads-step-ins
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-inspector-reads-step-ins.md`
**Project State plan:** `f5cb078c-dfcb-47bf-869c-43347c55a2ad` on `total-harness`

**What this is:** Build 76. The join. The Rules Inspector, which already turns repeated problems into drafted fixes every Sunday, also reads the step-in records. When the same kind of correction shows up twice it drafts the fix, the Rules Repairer applies it, and the Inspector only calls it fixed once the corrections actually drop.
**Stack Flow:** the Rules Inspector dot gains a line from Chats (step-in records) and new side-panel text; its skill version updates.
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build. **After:** Build 75. **Target repo:** Chooch333/agent-library (plus Chooch333/cbrain `concepts/stack-map.md`).

**What I'll do (build chat):** edit the Inspector skill, update its dot, dry-walk it on the two records that exist.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-09 (frozen)
"Design the two missing parts and the one join, reusing what I have."

## Current state going in (verified 2026-11-09)
- The Inspector has walked nine Sundays. Step 4 gathers lessons, disclosures, failed plans and stale next moves since the last walk, capped at 60; step 6 files a Punch List item only when two or more records point at one target, with the fix drafted. The Rules Repairer applies auto items Monday; only the Inspector marks them verified.
- So the improver already exists. What it lacks is the step-in records as evidence, and a check that a fix worked rather than just landed.
- The other three improvers stay as they are, because their inputs differ: Stack Repairer (broken running parts), Team Builder update mode (expert briefs), Stack Advisor (outside ideas).

## Scope
**In:** `skills/inspector/SKILL.md` 0.2.0 (steps 2a, 4, 5, 6, 7); stack-map Rules Inspector dot; CHANGELOG line.
**Out:** the Repairer's steps; a shared inbox for all four improvers; any new scheduled task.

## Directive
1. **Step 4, new bucket.** Read lessons on total-harness tagged exactly `step-in`, all time, newest 40, outside the 60-record cap.
2. **Steps 5–6, cluster.** Group by pattern and skill (`skill-none` points at AGENT.md routing or a reference file). Count across all walks, not since the last one. Two or more from different chats, not already covered by a live fix → file one Punch List item naming the step-in lesson ids, with the edit drafted, plus one new fixed-set task (ask, key, the records behind it) for `tests/fixed-set.md`.
3. **Tiers.** Auto: add or clarify a rule in a skill's body or a reference file; add a fixed-set task. Needs-brief: a skill's description or triggers, an AGENT.md row, the charter, an Our way line marked `Charles`, a new skill, deleting a rule (A-074).
4. **Step 2a, effect check.** An applied step-in item is verified only when (a) its fixed-set task scores 0 in the newest `fixed-set-run`, and (b) step-ins for that pattern and skill in the two walks since it was applied are fewer than in the two before. Otherwise `regressed`, and file it again with what the evidence shows.
5. **Step 7.** The checkpoint's first line is a plain count: `Read N step-ins (M new), filed F, verified V, regressed R`.
6. **Map.** Rules Inspector dot: line from Chats, side panel says it reads step-in records and checks fixes by effect.
7. **Dry walk** on TH-157 and TH-158: the cluster is already covered by the AGENT.md transcript row (7c1c19b), so no item is filed; the walk says so.

## Acceptance criteria
1. Inspector 0.2.0 on main, reads back identical.
2. The dry walk recognises the transcript cluster as covered and files nothing.
3. The map's Rules Inspector dot shows the new line.

## Cost
Subscription only; the walk reads up to 40 more short records.

## Decisions
- [Claude-per-doctrine] One improver, not a new one: the Inspector's two-record rule is exactly the "repeated failures only" rule from Warp's loop and from Warp's own update-triage skill (verified in warpdotdev/oz-for-oss).
- [Claude-per-doctrine] Verified means the corrections dropped, not that the text landed (oversight seat).
- [Claude-per-doctrine] Charter edits stay needs-brief: only Charles changes the charter. The first such case is already open (the two-engine line, below).

## For Charles (the one call this design leaves him)
Plain chats twice put a nightly timer on GitHub Actions because the charter says deterministic work goes on Actions; Actions timers are off since 2026-10-12 and timers live in Vercel. Recommended charter wording: "Two-engine rule: deterministic work on GitHub Actions or a Vercel cron (timers go on Vercel while Actions timers are off); Claude-as-worker on scheduled tasks; Claude inside application code on a capped API key."

## Pasteable prompt
> Build 76 — execute Build Brief BB-2026-11-09-inspector-reads-step-ins. Pull the plan from Project State (plan_id f5cb078c-dfcb-47bf-869c-43347c55a2ad, project total-harness). Answer forks yourself; stop only at hard gates.
