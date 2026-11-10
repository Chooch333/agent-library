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
- *Revised 2026-11-09* after the scoring-and-testing expert reviewed this brief (TH-160, TH-162). What changed: a fix is verified, waiting or regressed, never judged on a difference of one; clusters form on what was missed; every new test task names the file its fix lives in.

## Scope
**In:** `skills/inspector/SKILL.md` 0.2.0 (steps 2a, 4, 5, 6, 7); stack-map Rules Inspector dot; CHANGELOG line.
**Out:** the Repairer's steps; a shared inbox for all four improvers; any new scheduled task.

## Directive
1. **Step 4, new bucket.** Read lessons on total-harness tagged exactly `step-in`, all time, newest 40, outside the 60-record cap.
2. **Steps 5–6, cluster.** Group by what was missed (the rule or target, as step 5 does today); the pattern and skill tags narrow the search and never form a cluster on their own, so `skill-none` and `other` records are grouped only by what they say. Skip records tagged `unchecked` or `step-in-unsure`. Count across all walks, not since the last one. Two or more from different chats, not already covered by a live fix → file one Punch List item naming the step-in lesson ids, with the edit drafted, plus one new fixed-set task for `tests/fixed-set.md`: the ask, the key, the records behind it, and a `Touches:` line naming the file the edit lands in.
3. **Tiers.** Auto: add or clarify a rule in a skill's body or a reference file. A new fixed-set task is auto only when every key point cites a decision, Charles's dated words, or a lesson the scorer did not write; otherwise the task is needs-brief and the rule edit still goes ahead. Needs-brief: a skill's description or triggers, an AGENT.md row, the charter, an Our way line marked `Charles`, a new skill, deleting a rule (A-074).
4. **Step 2a, effect check, three outcomes.** Step-ins are dated by their chat turn, not by when they were filed.
   - **Verified:** the item's fixed-set task scored 0 on both runs of a replay made after the fix, and no step-in for that cluster appears in at least two receipts since the fix that each read one chat or more and passed their re-score.
   - **Regressed:** a step-in for that cluster dated after the fix, confirmed by opening the record and the chat turn. File it again with what the evidence shows.
   - **Waiting:** anything else (too few receipts, a replay that has not run, a week the scorer read nothing). The item stays `applied`. A count that moved by one is never the reason for verified or regressed.
5. **Step 7.** The checkpoint's first line is a plain count: `Read N step-ins (M new), filed F, verified V, waiting W, regressed R`.
6. **Map.** Rules Inspector dot: line from Chats, side panel says it reads step-in records and checks fixes by effect.
7. **Dry walks.** (a) On TH-157 and TH-158: the cluster is already covered by the AGENT.md transcript row (7c1c19b), so no item is filed; the walk says so. (b) On a planted cluster: two made-up step-in records from different chats about one missed rule, given to the walk as input and never written to Project State. The walk drafts one item and one task with its `Touches:` line and files nothing.

## Acceptance criteria
1. Inspector 0.2.0 on main, reads back identical.
2. Dry walk (a) recognises the transcript cluster as covered and files nothing.
3. Dry walk (b) shows the drafted item and the drafted task with a `Touches:` line; nothing planted is in Project State afterwards.
4. The map's Rules Inspector dot shows the new line.

## Cost
Subscription only; the walk reads up to 40 more short records.

## Decisions
- [Claude-per-doctrine] One improver, not a new one: the Inspector's two-record rule is exactly the "repeated failures only" rule from Warp's loop and from Warp's own update-triage skill (verified in warpdotdev/oz-for-oss).
- [Claude-per-doctrine] Verified means the corrections dropped, not that the text landed (oversight seat).
- [Claude-per-doctrine] Charter edits stay needs-brief: only Charles changes the charter. The first such case is closed: Charles reworded the two-engine line on 2026-11-09 (verified in `references/charter.md`).
- [Claude-per-doctrine] Three outcomes, not two: with only verified or regressed, a fix read as regressed on the first walk after it landed, and a week the scorer did not run read as proof it worked (scoring-and-testing seat, TH-160 finding 1). The effect is measured only in this Project's chats, so a fix to a skill used mostly elsewhere stays waiting.
- [Claude-per-doctrine] A drop from one to none is not evidence (Build 75's own rule), so verified needs a clean replay and two clean receipts.

## Pasteable prompt
> Build 76 — execute Build Brief BB-2026-11-09-inspector-reads-step-ins. Pull the plan from Project State (plan_id f5cb078c-dfcb-47bf-869c-43347c55a2ad, project total-harness). Answer forks yourself; stop only at hard gates.
