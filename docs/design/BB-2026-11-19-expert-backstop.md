# Build Brief — BB-2026-11-19-expert-backstop

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-19-expert-backstop.md`
**Project State plan:** `fb7c1817-816e-4f39-8ace-a99daf809450` on `cbrain`
**Build:** 89
**Skills:** orchestrate-build
**Seated:** revision 1, report CB-625, seats c-stack, oversight, lanes, data-homes, services, ai-system-design
**Stack Flow:** edits the Step-in scorer side panel in cbrain `concepts/stack-map.md` (it now also files Charles's missed decisions); no new dot.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** Build 87
**Cost:** subscription only. The weekly scorer helper reads a little more per run (it already reads these chats); seats read fewer old notes.

**What this is:** Finishes "experts learn from every chat". A weekly backstop catches anything Charles decided that a chat forgot to file, and each expert reads a sensible amount of its own notes.
**What I'll do (build chat):** the two steps below.
**What you'll do:** nothing.

## Asked for — Charles (frozen)
> 2026-11-19: "how do we save expert level decisions … back to those experts? And I want it done in the same way that you do memories … I don't want to be asked." Plan doc status: "Still to do: the backstop that skims past chats, and a cap on how much each expert loads."

## Current state going in (checked 2026-11-19)
- **[verified]** AGENT.md's corrections rule now covers any decision he states (CB-619); the night run folds notebook entries into briefs.
- **[verified]** The step-in scorer runs weekly as a helper of the first Design Assist chat and already reads this Project's chats. Its rule 8 forbids quoting him beyond a few words; rule 3 reads at most four pages per chat (CB-608: 56 of 79 turns unread in one chat).
- **[verified]** Seats read all waiting notebook entries and their latest field notes with no count limit. Field notes never fold into a brief.

## Scope
**In:** `skills/step-in-scorer/SKILL.md`, `skills/expert-desk/references/seat-template.md` (review seat and CE seat).
**Out:** AGENT.md's rule (already done); the night fold (already exists).

## Directive
1. **Backstop in the step-in scorer:** for each chat it reads, list every statement where Charles said how something should be done or decided something that would still hold in a month. For each, look for a decision whose source carries that chat's link and turn; none → file it the AGENT.md way: one decision tagged `charles-directed`, quoting his words, with the chat link and turn in its source, plus one notebook entry (`lens-note`) for the expert whose call_when matches. Only his own quoted words count; where he reversed himself in the chat, file his last word. Add a rule 8 exception for these records; add decisions and lens-notes to `wiring.writes`. A chat cut short by the four-page cap records where it stopped, and the next run starts there. Version bump, changelog.
2. **Seat read cap:** in both the review seat and the CE seat: waiting notebook entries (no `folded`/`routed` tag) — all, unchanged; field notes — the newest 10; record searches — unchanged (already capped at 10). Version bump, changelog.

## Acceptance
1. step-in-scorer carries the backstop, the exception, the resume point, last-word rule and exact-source check; version bumped.
2. seat-template caps field notes at the newest 10 in both seats.
3. Live proof handed off (no action): the next weekly scorer run files its backstop list (none, or decisions with chat links); build sessions can't read past chats, so this proves in the first Design Assist chat of the week.

## Decisions
- [Claude-per-doctrine] Backstop rides the existing weekly scorer, not a new run. Seat: ai-system-design. Ruled out: a helper at every chat start (load on every chat).
- [Claude-per-doctrine] Cap field notes by count, not by date. Seats: ai-system-design, data-homes (a date cap hides field notes that never fold).

## Pasteable prompt
> Build 89 — execute Build Brief BB-2026-11-19-expert-backstop. Pull the plan from Project State (plan_id fb7c1817-816e-4f39-8ace-a99daf809450, project cbrain, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-19-expert-backstop.md. Build 87 must have landed (same repo). Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
