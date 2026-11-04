# Build Brief — BB-2026-11-03-stack-fix-log
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-03-stack-fix-log.md`
**Project State plan:** `a0639c2e-a9ed-4f26-b7d5-a293c200f281` on `total-harness`

**What this is:** Build 67. There is no stack fix log the Stack Repairer reads for problems that aren't a red or late dot. Its own repair log (`stack_repairs`, cbrain Supabase `lpeswznkxzeeyiqaewma`) becomes that log. No new table or file. Also fixes Project State's tag shortening.
**Stack Flow:** Repair log side panel ("also problems reported from chats and runs"); one line chats → stack-repairer (report).
**Step map:** no change.
**Skills:** orchestrate-build. **After:** Build 66 (both edit cbrain `concepts/stack-map.md`). **Overnight:** yes.

## Asked for — Charles, 2026-11-03 (frozen)
> "Is there a stack fix log that the stack repairer references? If so put this repair list there. If not create one and suggest a scope to integrate it into the stack repair process. It can be a source of learning for the stack experts. Include the [backlog] of the source intake"

## What exists (oversight expert, verified 2026-11-03)
- Stack Repairer reads only failing or late `stack_status` rows, the checker row and its own `stack_repairs` rows. Punch List is the Rules side (weekly); the Stack Repairer never reads it. 91 needs-design-check posts sit at "noted" on the Comms Table (59 cbrain, 17 world-graph), including the summary backlog's causes since Oct 16.
- Done by the design chat 2026-11-03 with existing actions: five `stack_repairs` rows — project-state (tag bug, watching), rss-feeds (feed channel, watching, plan 82569503), collector (summary backlog, watching, plan 82569503), post-reader (needs-you: add TinyFish to the World Graph Reader task), _unmapped (needs-you: turn off the Tier-2 task). Each carries reported_by, evidence, recheck.

## Directive
1. Migration (Supabase MCP, apply_migration on lpeswznkxzeeyiqaewma): add `reported` to stack_repairs_action_check. A reported row: dot_id (nearest map dot or `_unmapped`), finding (one plain line), detail {evidence, found_by, recheck, plan_id?}. Insert-only. No recheck, no row.
2. skills/stack-repairer/SKILL.md 0.4.0: a "Reported problems" section with the row shape; step 1 also reads reported rows (and needs-you / watching rows with detail.reported_by) with no graded row; steps 3–4 treat them like a red dot (re-check live state first; smallest fix; needs-you for a click or hard gate; `watching` with plan_id when a plan already covers it); step 2 grades green when detail.recheck passes; an ongoing condition gets a real check on the map so it becomes a dot. Keep-or-drop questions to Charles are gone (WG-213): a quiet or failing source is an alert on the Sources page only.
3. AGENT.md, one line: "A broken running part you notice outside your job → one `reported` row (shape in stack-repairer, Reported problems)." Running-part problems go here instead of the Comms Table; design questions stay on the Comms Table. Sweep the 91 noted needs-design-check posts once: running-part ones become reported rows, the rest stay.
4. Tag fix (Chooch333/project-state-mcp lib/tags.ts): never singularize hyphenated tags; return every substitution the normalizer still makes in tag_substitutions; search notes, decisions, plans and lessons for already-shortened tags and repair them (Build 62 pattern). Repaired by hand already: EB-009, EB-011, EB-019, EB-020, plan 82569503.
5. Close PL-019 (Tier-2 task) with a pointer to its log row; have the Rules Inspector verify and close PL-015 (task prompts already use skills/).
6. CE learning source: the stack experts' weekly CE reads `stack_repairs` since their last read-through point (excluding `_run` marker rows) and lessons tagged `stack-incident` (wired in Build 68).
7. Stack Flow text and line (cbrain concepts/stack-map.md; anchored replace_in_file, serial, `[skip ci]` on all but the last commit).

## What Charles sees
Nothing new: the evening recap is built from stack_repairs, so reported rows show under Fixed today, Queued for tonight and Needs you; a needs-you opens a Next steps card and closes itself when its recheck passes.

## Acceptance criteria
1. A chat files a reported row; the next Stack Repairer run picks it up, re-checks, acts and grades it.
2. The two needs-you rows from 2026-11-03 appear in the evening recap and close when their rechecks pass.
3. A note tagged `expert-lanes` is stored as `expert-lanes`; any substitution is reported.
4. PL-019 closed with a pointer; no ask lives in two queues.

## Hard gates
None. The migration only widens an allowed-values list.
