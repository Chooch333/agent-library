# Build Brief — BB-2026-11-09-step-in-scorer
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-step-in-scorer.md`
**Project State plan:** `4386986f-c4bf-436f-9b3e-7ccfa81d2c06` on `total-harness`

**What this is:** Build 74. Count how often Charles had to step in. Once a week a helper reads the week's chats in this Project, finds each turn where he corrected Claude, and logs one plain record per step-in, so the Rules Inspector can fix what keeps happening.
**Stack Flow:** one new part on the Chats dot ("Step-in scorer, weekly helper") with a line to Project State, and an output check on its newest receipt (late after 10 days).
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build, team-builder (skill mode). **After:** none. **Target repo:** Chooch333/agent-library (plus Chooch333/project-state-mcp heartbeat field and Chooch333/cbrain `concepts/stack-map.md`).

**What I'll do (build chat):** write the scorer skill, add one line to Design Assist so it starts the scorer once a week, add its check to the map, run it once over the last 14 days.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-09 (frozen)
"Design the two missing parts and the one join, reusing what I have. Two new parts at most. The scorer must count how often I had to step in."

## Current state going in (verified 2026-11-09 unless marked)
- Nothing counts step-ins today. His corrections in chats are the richest signal and nothing records them (TH-155).
- A Claude Code cloud session bound to this claude.ai Project, and its helpers, can list and search this Project's past chats (`recent_chats`, `conversation_search`, `read_conversation`). Verified twice: the design chat and its lanes seat. This overtakes MB-007 for that surface.
- *Assumed:* a fresh scheduled run does not get those tools (CB-490). Not tested: creating a one-shot test task was refused in the design chat.
- Two records already exist from a hand run: TH-157, TH-158 (the "no transcript" miss, twice). Their fix landed the same night (agent-library 7c1c19b).
- Rubric drafted: `references/step-in-rubric.md` (7c1c19b), revised 2026-11-09 with the rule that tells a step-in from an ask, a `step-in-unsure` tag and a `should-have-asked` pattern.
- A helper cannot start helpers. Verified twice on 2026-11-09: two helpers started from a chat had no tool to start another.
- *Revised 2026-11-09* after the scoring-and-testing expert reviewed this brief (TH-160, TH-162). What changed: the scorer checks itself by a blind re-score instead of a printed answer; it reads each chat to the end; its first line says how much it read.

## Scope
**In:** `skills/step-in-scorer/SKILL.md` (new, draft); `skills/design-assist/SKILL.md` step 1, one line; project-state-mcp `/api/heartbeat` gains `step_in_scorer.last_receipt`; stack-map Chats dot part + check; CHANGELOG line.
**Out:** a new scheduled task (Charles wants few; EB-016); Design Assist chats logging their own step-ins (a chat grading itself); chats outside this Project; any screen.

## Directive
1. **Write the skill** (Team Builder skill mode). Steps:
   - **S1 Where to start.** The read-through point is the newest note on total-harness tagged exactly `step-in-receipt`; none → 7 days back.
   - **S2 Re-score first.** Before reading any step-in record: take three chats from the previous receipt's list of chats read, read each to the end and count its step-ins fresh. Only then look up what was filed for those three and compare the counts. `K` = how many of the three match. No previous receipt → "first run".
   - **S3 List chats** with `recent_chats` after the read-through point (at most 5 pages). This Project only.
   - **S4 Read each chat** with `read_conversation` to its end (at most four pages; a chat longer than that is listed as cut short). Mark each correction by the rubric: a turn where Charles corrected Claude, redid something himself, or said the same thing again is a **step-in**; one record per correction, so a turn that corrects two things is two. Use the rubric's rule to tell a step-in from an **ask**; when it can't be told, `step-in-unsure`. Skip what is already recorded (`find_by_tags` step-in; match the chat link, or the chat's title and date when a record has no link).
   - **S5 File** one lesson per step-in on total-harness, tags `step-in`, one `pattern-<name>` from the rubric (plus `same-correction-twice` when it applies), `skill-<slug>` or `skill-none`; body per the rubric's record shape. When S2 gave `K` of 1 or 0, every record this run files also carries `unchecked`, and the Rules Inspector skips it (Build 76).
   - **S6 Receipt** note on total-harness, tags `step-in-receipt`, `self-learning-loop`. First line: `Step-ins: N in C chats of this Project only (listed L, cut short X, D days), asks A, unsure U, re-score K of 3` (or `re-score: first run`). Then counts per pattern, the chats read (title, date, link) so the next run can re-score them, chats it couldn't read and why, the read-through point. A receipt with zero chats read says "read 0 chats", never "no step-ins".
2. **Start it once a week.** Design Assist step 1 intake, one line: if the newest `step-in-receipt` note is more than 7 days old, start one helper told to fetch `skills/step-in-scorer/SKILL.md` and follow it; don't wait on it past this reply.
3. **Heartbeat.** project-state-mcp `/api/heartbeat` adds `step_in_scorer.last_receipt` (newest `step-in-receipt` created_at), the same way `expert_ce.last_receipt` works.
4. **Map.** Chats dot: made_of part "Step-in scorer (weekly helper)", line to Project State, check `heartbeat` on that field, late after 10 days.
5. **First run.** Run the scorer by hand over the last 14 days. If this build's session can't load the past-chat tools, record that as the receipt ("read 0 chats: tools not loaded") and hand acceptance 2 to the first Design Assist chat's weekly helper.

## Acceptance criteria
1. The skill is on main as draft and reads back identical.
2. A `step-in-receipt` note exists with chats read > 0, and TH-157/TH-158 were not filed twice.
3. The receipt's first line carries every field in S6; on the first run the re-score field reads `first run`.
4. The heartbeat shows the receipt time; the Chats dot part reads green.

## Cost
Subscription only. *Assumed:* one weekly helper about the size of two expert seats. No money.

## Decisions
- [Claude-per-doctrine] Runs as a helper in the first Design Assist chat of the week: the only lane verified to read past chats, and no new scheduled task. Ruled out: Warp's skill-doctor (reads only local Claude Code, Codex and Warp session files, so it can't see claude.ai chats; verified from its SKILL.md), Warp Factories (paid early access, built around GitHub pull requests).
- [Claude-per-doctrine] Records live on one project, total-harness, as lessons, because the Inspector already reads lessons (data-homes seat).
- [Claude-per-doctrine] Two numbers, never one: step-ins (this build) and misses against the fixed set (Build 75), so fewer corrections can't hide wrong answers he never noticed (ai-system-design seat).

- [Claude-per-doctrine] The scorer checks itself by re-scoring three earlier chats before it sees what was filed, not against a printed expected count: the printed count was open to the scorer, and for one of the two seed chats the expert's read found more corrections than the count said (scoring-and-testing seat, TH-160 finding 3; not re-checked by the revising chat).
- [Claude-per-doctrine] The count is for this Project's chats only and the first line says so; it is not how often he steps in everywhere.

## Pasteable prompt
> Build 74 — execute Build Brief BB-2026-11-09-step-in-scorer. Pull the plan from Project State (plan_id 4386986f-c4bf-436f-9b3e-7ccfa81d2c06, project total-harness). Answer forks yourself; stop only at hard gates.
