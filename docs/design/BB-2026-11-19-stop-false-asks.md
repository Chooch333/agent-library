# Build Brief — BB-2026-11-19-stop-false-asks

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-19-stop-false-asks.md`
**Project State plan:** `67f7ea60-d011-4f0d-b094-a4ef408016a4` on `cbrain`
**Build:** 87
**Skills:** orchestrate-build, team-builder (no new skill; edits only)
**Seated:** revision 1, report CB-625, seats c-stack, oversight, lanes, data-homes, services, ai-system-design
**Stack Flow:** edits cbrain `concepts/stack-map.md`: the Stack Repairer dot reads "three times a day, 7 am, noon, 5 pm"; the Expert CE dot and launcher row read "one Sunday session runs every expert in turn, one helper each; it fires no copies"; the lanes: scheduled-helpers line notes Expert CE (auto) has run desk helpers since 11-08.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also two map lines in Chooch333/cbrain) · **after:** none
**Cost:** subscription only, no extra dollars. Saves plan usage: the Stack Repairer drops from about 12 full Opus passes a day to 3 **[assumed: the other passes end in seconds]**. Build ≈ one night builder plus two after-build seats.

**What this is:** First engine-room build. Stops the stack telling Charles things "need you" when they don't, and stops the Stack Repairer re-logging the same items every hour.
**What I'll do (build chat):** the six steps below.
**What you'll do:** nothing. If the build can't change a scheduled task's settings, the skill covers it on its own (step 3).

## Asked for — Charles (frozen)
> 2026-11-19: "brief the engine-room builds from the Stack Engine Room plan doc." Plan build 1: "Stop false 'needs you'… Your rule for what only you can do already exists. Two parts skip it." 2026-11-17: experts learn "the same way that you automatically update the project memory. I don't want to have to suggest it, or approve it, it just happens." 2026-11-19: "Make sure [the charter] gets reviewed before a chat response happens."

## Current state going in (checked 2026-11-19)
- **[verified]** The Email approval gate light is red with "3 forwarded emails waiting". All three are Team Builder tool-fact drafts from the Sunday expert run (cbrain `_briefs/BR-DRAFT-2026-11-08-c39d.md`, `-e447.md`, `BR-DRAFT-2026-11-15-9026.md`), not emails.
- **[verified]** Fix log, last 14 days: gate `needs-you` ×41, RSS feeds `watching` ×31, YouTube `watching` ×30 — the same items every run.
- **[verified]** Stack Repairer task: cron `29 * * * *` (hourly), bypass approval. Skill 0.4.3 says 7:00/12:00/17:00; Charles was shown three a day (A-114, CB-521).
- **[verified]** Expert CE Sunday dispatch fired nothing on 11-08 and 11-15: a tag rewrite turned `ce-dispatch` into `ce-dispatch-failed`, so the 01:00 catch-up ran every expert one after another (worked, ~47 min). Firing a copy from an auto task: worked once (EB-042), refused once with a verbatim error (EB-043). Bypass tasks have fired other tasks (TH-043).
- **[verified]** Seven scheduled-run skills don't read the charter (CB-613). orchestrate-build steps 5 and 7(d) list their own stop reasons; the charter now has "Gates Claude works within" and "Talk with him first".
- **[verified]** Inspector and Repairer skills still `status: draft` after weeks live (PL-014).

## Scope
**In:** team-builder, stack-repairer, expert-desk (CE job + one pitfall), CONVENTIONS, orchestrate-build, the seven charter lines, inspector/repairer status, three stuck drafts, two map lines.
**Out:** Stack Inspector code and lights (Build 88); the cbrain approval gate itself (unchanged); people/company pages (unchanged).

## Directive
1. **Tool facts become expert field notes** (`skills/team-builder` update mode, sort (b)): a tool fact is filed as one `field-note` on `expert-bench` for the expert it came from (tags `field-note`, `expert-ce`, `expert-<slug>`; one finding, Inferred, its source cited), and the lens-note tagged `routed`. No cbrain draft, no gate. Rule 2 unchanged. Update `wiring.writes`, CONVENTIONS' team-builder row, and `references/expert-brief.md`'s tool-fact line to match. Version bump, changelog.
2. **The three stuck drafts:** reject each with the cbrain tool `reject_brief` (kept as `BR-REJECTED-…`, nothing deleted), reason "tool fact moved to the expert's field notes (Build 87)". File three field notes: lanes — "Firing a copy from an auto task has both worked (EB-042) and been refused (EB-043); bypass tasks have fired other tasks (TH-043); nothing relies on firing from auto"; services — the tag fact, worded for after Build 91 ("hyphenated tags are stored as written from Build 91 on"); c-stack — the Vercel `[skip ci]` fact as drafted.
3. **Stack Repairer 0.5.0:**
   - Runs that start outside the 7, 12 and 17 o'clock hours (Indianapolis) end at once and write nothing. Also try `update_trigger` on "Stack Repairer" to `CRON_TZ=America/Indiana/Indianapolis 29 7,12,17 * * *`; if refused, the skip rule covers it; log which.
   - Before any `needs-you`: run the "Hand it on" test in `references/thread-checkin.md` (it covers the charter's "Gates Claude works within" and "Talk with him first", a fact only Charles knows, a click Claude was refused). Fails → Claude handles it: fixed, briefed or watched.
   - A dot or open row already logged `needs-you` or `watching` with the same evidence is not logged again; the run marker counts it.
   - Quiet sources: no row at all (Sources page only, WG-213). Real fetch errors are still fixed.
   - The Email approval gate bullet: needs-you only for drafts that ask Charles something only he knows; otherwise handled.
   - A recheck that can't be run moves up to a short brief whose build runs it.
   - Run marker on the 17:00 run carries `recap: sent | nothing-to-send | error` (Build 88's Gmail light reads it).
   - Rewrite the Expert CE bullet for step 4 (no dispatch tags).
4. **Expert CE** (`skills/expert-desk` CE job): Dispatch fires nothing. The 00:00 session runs every expert itself, one desk helper per expert in turn, then folds. The 01:00 run treats an expert with a `ce-start` note under 90 minutes old as still running and only fills gaps. Remove "nothing but Dispatch ever calls fire_trigger" wording that no longer applies; replace the pitfall "A task can fire a copy of itself…" with the step 2 lanes wording. Drop `ce-dispatch-failed` from CONVENTIONS' expert-desk writes.
5. **Charter first:** one line near the top of How in stack-repairer, night-run, video-reader, world-graph-reader, post-reader, stack-advisor, wake: "Read `references/charter.md` before the first step." orchestrate-build steps 5 and 7(d): stop only at the charter's "Gates Claude works within" and "Talk with him first" sections — name the sections, not item numbers. This covers punch item PL-025 (the Design Assist chat already noted it there); name PL-025 in the Session Log.
6. **Status:** `skills/inspector` and `skills/repairer` (whichever paths hold them) `status: active`, changelog line (PL-014).
Each edited skill: version bump, changelog line citing Build 87. Read every file back after commit.

## Acceptance
1. team-builder sort (b) files field notes; no `BR-DRAFT` is written by an update-mode run.
2. The three drafts are `BR-REJECTED-…` files; three field notes exist with the wording above.
3. stack-repairer 0.5.0 carries the skip rule, the Hand-it-on test, no-repeat rule, recap field; the task's cron result (changed or refused) is in the Session Log.
4. expert-desk CE job fires nothing; the pitfall line is replaced.
5. Seven skills read the charter first; orchestrate-build points at the charter sections.
6. Inspector and Repairer read `status: active`.
7. The two map lines are edited.
8. Next live proof (handed off, no action): Sunday's Expert CE run files receipts for every expert with no fire calls; the gate light goes green once Build 88 lands.

## Decisions
- [Claude-per-doctrine] Tool facts → expert field notes, not cbrain pages. Seats: ai-system-design (narrowest; leaves the approval gate, Charles's rule, alone). data-homes preferred cbrain pages with the approval dropped; c-stack notebook plus cbrain. Ruled out: sealing as Inferred (changes his gate; c39d is disputed).
- [Claude-per-doctrine] Stack Repairer three a day, what Charles was shown. Seat: c-stack. oversight preferred hourly acting only on new evidence.
- [Claude-per-doctrine] Needs-you test = thread-checkin's "Hand it on" list. Seat: oversight.
- [Claude-per-doctrine] Expert CE runs every expert in one session; no firing. Seats: lanes, ai-system-design.

## Pasteable prompt
> Build 87 — execute Build Brief BB-2026-11-19-stop-false-asks. Pull the plan from Project State (plan_id 67f7ea60-d011-4f0d-b094-a4ef408016a4, project cbrain, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-19-stop-false-asks.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
