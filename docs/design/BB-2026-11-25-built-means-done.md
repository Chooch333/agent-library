# Build Brief — BB-2026-11-25-built-means-done

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-25-built-means-done.md`
**Project State plan:** `844810f7-c3ad-4126-abb9-9df13ba73640` on `cbrain`

**Build:** 93
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also writes Chooch333/project-state-mcp and Chooch333/cbrain, in the order below) · **after:** none
**Skills:** orchestrate-build

**What this is:** End "prove it later". A build that is built closes as done; nothing it writes outlives it as a test to run later, and nothing asks Charles to view or test.
**Stack Flow:** no change — no running part is added, removed, renamed or re-routed (the checker gains one optional field; its dot, lines and side panel are unchanged).
**Step map:** no change — no workflow steps change.
**What I'll do:** change the done rule in Project State, the build and design rules in agent-library, and the status-light checker in cbrain; close the leftover proof-only briefs.
**What you'll do:** Nothing.

## Current state going in

**Asked for — in Charles's words** (frozen)
- "Testing is something we need to work on. Build after build is hanging open because its completely built, but not 'tested' or 'proven' I know its best practice for doing tech work, but that needs to end. Testing like this can't be left danglin." (2026-11-25)
- "This is a DA chat. to scope removing the proof/checking step from my tech designs/builds" (2026-11-25)
- Checks a build runs on itself before it finishes: "keep". "Draft until proven" on new skills and Operators: "drop". (2026-11-25)

**Verified 2026-11-25**
- Project State trigger `plans_done_receipt_gate`, rule 3: each acceptance item must be `pass` with evidence, or `handed-off` with a `follow_up_plan` uuid that is an open plan; anything else is refused.
- orchestrate-build 7(c) therefore writes a draft follow-up plan for every check it cannot prove on the spot. 52 of 158 receipts handed a check off (25 of 66 in the last 30 days). Of 45 follow-up plans named in receipts, 27 were abandoned, 10 succeeded.
- cbrain `services/lib/stack-status.ts` `recency()`: a check with a late threshold and no last-seen time returns `unknown`, "No sign of it yet.", for good; the Stack Repairer skips unknown rows.
- No cbrain-ui code reads `handed-off` or `done_receipt` (code search; search can miss unindexed files).

## Receiving chat
The night runner (orchestrate-build), one session.

## Scope
**In:** the done-receipt rule; how builds close; how designs write checks; walkthrough and "What to check" asks; "draft until the first live run"; the Operators' six-run proof count; the Stack Repairer's later-only acceptance line; a never-ran-once light; two leftover proof-only plans; three fix-log rows that point at finished plans; three Punch List wording fixes in the same files (PL-027, PL-028, PL-029).
**Out:** status lights for parts that have none today (Punch List PL-039); the night session's expert seats; the site's own tests at deploy; rewriting old receipts; any cbrain-ui screen; flipping the status of existing skills (only the rule for new ones changes).

## Directive
Order matters: a skill that writes `not-checked` before the database accepts it fails every close.

1. **Database (Project State, Supabase `ujditldbqdiqigazkcak`).** `apply_migration`: replace rule 3 of `plans_done_receipt_gate` so an item's `result` may be `pass` (non-empty `evidence`, as now), `not-checked` (non-empty `reason`; else raise 'done-receipt rule 3: an acceptance item marked not-checked has no reason'), or `handed-off` (branch unchanged, so old receipts and running builds still close). The final ELSE message names all three. Commit the same SQL to Chooch333/project-state-mcp as the next numbered file beside `06-done-receipt-gate.sql`.
2. **project-state-mcp.** `lib/tools.ts`: `update_plan_status` `done_receipt.acceptance[].result` enum becomes `pass | not-checked | handed-off`; add optional `reason`; reword the description: a check is passed with evidence or recorded not-checked with a one-line reason; no build writes handed-off any more. `lib/handlers.ts`: pass `reason` through if it filters fields. One commit; wait for the Vercel deploy to read READY.
3. **agent-library, one commit per file, versions bumped, changelog lines citing this brief and CB-784.**
   - `skills/orchestrate-build/SKILL.md` 7(c), replace with: "**(c) Record what you can't show.** Go through the brief's acceptance checks one by one. A check you ran that did not pass is a failure: the plan goes to `failed`. A check you could not run is recorded `result: not-checked` with a `reason` that is one of three: `watched by <dot label>` (that dot's check on the stack map is not `none`); `on demand, seen in use` (Charles starts the part himself); or `this session lacked <tool or key>`. A check waiting on a click only Charles can make is `not-checked` with reason `needs his click: <card name>`, and that one Next steps card is the only thing that outlives the build. A spending-limit or cap check may only pass or fail. Never write a follow-up plan for a check." 7(d): `pass` + `evidence`, or `not-checked` + `reason`. Progress tracking and the changelog note: drop "handed-off follow-up plan". In the no-browser-tests rule, delete the sentence that has the build write a "What to check" list; Session Logs carry no such list.
   - `skills/build/SKILL.md`: the Done receipt gate line and "Succeeded means done" paragraph say pass-with-evidence or not-checked-with-reason; no hand-off. Apply PL-027 as written on the item.
   - `skills/design-assist/SKILL.md`: doctrine rule 10 becomes "**Done-when drafted early.** The brief lists only checks the build itself can show before it finishes (a file read back, a deploy READY, a query returning the row, the part's own test passing). A check that needs a later event (a first scheduled run, a next real email) is never an acceptance check. When the build adds or changes a part that runs on its own, one acceptance check is that the part's status light is set on the stack map in the same build (its `check`, with `since: <build date>`) and reads back." Step 1: delete the walkthrough visibility rule (from "**Walkthrough visibility rule" through "logs his findings as WT rows."). Apply PL-028's SKILL.md part.
   - `skills/design-assist/references/build-brief-template.md` gate 7: "Acceptance checks are things the build itself can show before it finishes; none needs a later event". `references/brief-completeness-framework.md`: same wording where it describes acceptance; apply PL-028's part.
   - `references/skill-design-framework.md` Q11: drop "Status stays `draft` until the first live run ... before `status: active`"; a new skill lands `active`. `skills/team-builder/SKILL.md`, `SKILL_TEMPLATE.md` and `CONVENTIONS.md`: a new skill is committed `active` (same as experts).
   - `skills/operator-run/SKILL.md`: delete the Proof section and its mentions; `skills/operator-setup/SKILL.md` step 7 and `references/operator-mandate.md`: a mandate lands `active`; the build-day test (step 6) stays. `experts/operator-design/BRIEF.md` is not edited here: file one lens-note on expert-bench tagged `lens-note`, `expert-operator-design`, `charles-directed` citing CB-784 and this brief.
   - `skills/stack-repairer/SKILL.md` short brief template: Acceptance 1 becomes "<the fix is in place and read back>"; delete "the dot reads green on the next Stack Inspector check" (the Repairer's own grading does that). A brief written "to dig in" has one acceptance check: the cause is named in the Session Log, or the fix is in place.
   - `references/thread-checkin.md`: in "When and how", drop "a follow-up draft" from the jobs list; the build-chat row closes when "the plan has succeeded". Apply PL-029 (orchestrate-build and AGENT.md wording) as written on the item.
4. **cbrain (main).** `services/lib/stack-status.ts`: `CheckSpec` gains optional `since?: string`. `recency()` takes it as a last optional argument: when there is no last-seen time, a late threshold exists and `now - since` is past that threshold, return `state: 'late'`, reason `Hasn't run once since it was added <duration> ago.`; otherwise as now. Pass `spec.since` from every evaluator that calls `recency()`. Add unit tests beside the existing ones in `services/test/`: no last-seen with `since` past the threshold is late; within it is unknown; no `since` is unchanged. In `concepts/stack-map.md`, add one sentence to the paragraph that documents `ops.check`: a check added by a build carries `since: <date>` so a part that never runs once turns amber. No dot edits.
5. **Cleanup, last.** `update_plan_status` → `abandoned` for the two proof-only plans `7f450f05-43d7-4fa5-9c76-bfcd945590ff` (old milestone date check) and `ffff3736-2e63-4d12-921c-cf024ccb2081` (Advisor critic check), executor_report citing CB-784. Leave the other six open follow-ups (real unbuilt work). In cbrain `stack_repairs`, insert one `graded` row (outcome `green`, finding "its plan finished; nothing left to watch", `detail.grades` = the row id) for each of `153f9d5a-b8f9-4db0-babe-13673e13f7c1`, `662f585f-c672-4b32-abd7-81a55e6a74d2`, `6f82a91c-2ef0-48f4-8d45-9e3548204390`, after re-reading that each one's plan is `succeeded`. `add_punch_note` (author `repairer`) on PL-027, PL-028, PL-029 naming the commits.

**Forks:** decide them yourself with judgment-call tags. Hard gates: none in this brief. Standing rules CB-121 and CB-103 apply.

## Inputs
Supabase MCP (`apply_migration`, `execute_sql`) on `ujditldbqdiqigazkcak` and `lpeswznkxzeeyiqaewma`; Custom GitHub MCP on the three repos; Vercel MCP for the project-state-mcp and cbrain-sync deploys; Project State MCP.

## Acceptance criteria
Every one is shown by this build before it finishes.
1. On a test plan this build creates on `misc-builds` (tagged `test`): a receipt with one `not-checked` item and a reason is accepted; the same receipt with an empty reason is refused (do this refusal first, on the same plan); a `result` of `maybe` is refused. Evidence: the three replies.
2. project-state-mcp deploy reads READY and `lib/tools.ts` read back shows the three-value enum and `reason`.
3. Each agent-library file in step 3 read back from main shows its change; a search of `skills/orchestrate-build/SKILL.md` finds no instruction to write a follow-up plan.
4. The new unit tests pass in the cbrain deploy's own test run and the deploy reads READY.
5. The two plans read `abandoned`; the three fix-log rows each have a `graded` row.
6. This build's own receipt holds only `pass` and `not-checked` items and it wrote no follow-up plan.

## Decisions made
- [Charles] Testing is never left dangling (CB-784). Keep the checks a build runs on itself; drop "draft until proven" for new skills and Operators.
- [Claude-per-doctrine] "Not checked" is bounded to three reasons plus his-only clicks; spending-limit checks pass or fail only (seats c-stack, oversight; report CB-787).
- [Claude-per-doctrine] `handed-off` stays valid in the database so old receipts and any build already running still close; no build writes it.
- [Claude-per-doctrine] The never-ran-once fix is a `since` date on the check, written by the build that adds the light: the checker is pure and has no other way to know when a part was added.
- [Claude-per-doctrine] Walkthroughs and "What to check" lists are removed: the record already says never ask him to test (thread-checkin, Closing out; charter 3).
- [Claude-per-doctrine] Known limit, accepted: a green light shows a part ran and left its mark, not that it did its job well.
- [Claude-per-doctrine] Existing skills marked draft are not flipped by this build; only the rule for new ones changes.

## Pasteable prompt
> Build 93 — execute Build Brief BB-2026-11-25-built-means-done. Pull the plan from Project State (plan_id 844810f7-c3ad-4126-abb9-9df13ba73640, project cbrain, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-25-built-means-done.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief). Do the steps in the brief's order: the database first. Standing rules CB-121 and CB-103 apply. No browser test.
