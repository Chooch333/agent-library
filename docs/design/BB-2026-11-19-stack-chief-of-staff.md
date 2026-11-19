# Build Brief — BB-2026-11-19-stack-chief-of-staff

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-19-stack-chief-of-staff.md`
**Project State plan:** `296c7ec6-c195-4f68-b553-f278fee258ee` on `cbrain`
**Build:** 90
**Skills:** orchestrate-build, team-builder (skill mode: new skill `stack-chief-of-staff`)
**Seated:** revision 1, report CB-625, seats c-stack, oversight, lanes, data-homes, services, ai-system-design
**Stack Flow:** adds one dot "Stack Chief of Staff" (runs with you, on demand; reads the lights, fix log, night builds, shelf, Advisor, Punch List, expert updates, readers, Next steps; writes one receipt note) to cbrain `concepts/stack-map.md`.
**Step map:** no change — not a Workflows-screen workflow.
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** Builds 87, 88, 89
**Cost:** subscription only. One ask ≈ one chat turn reading summaries first (recap, lights) and details only when needed.

**What this is:** New: a read-only skill that tells Charles, in about a minute and in plain words, where his stack stands. Never scheduled. Usable from any chat; built so Duet can run it.
**What I'll do (build chat):** the four steps below.
**What you'll do:** nothing for the build. Afterwards, asking Duet "what's going on with my stack?" is just using it.

## Asked for — Charles (frozen)
> 2026-11-17: "It will run on demand. I'm planning on having Duet trigger the Chief of Staff and then read back to me what's new or going on. I don't intend to read any output and I don't want it to be scheduled." "This isn't an expert, it's a skill that gets run when Duet triggers it. Scope the skill to be able to survey the automated items and provide a brief clear (non lingo/non tech) description of where things stand."

## Current state going in (checked 2026-11-19)
- **[verified]** Duet made the "Morning brief" and "Heartbeat" scheduled tasks; both carry no connectors, yet the Morning brief reads his mail and invites.
- **[assumed]** Whether a live Duet conversation can reach GitHub, Supabase and Project State, and where Duet keeps standing instructions. Only a live Duet ask shows it.
- **[verified]** Needs-you already has one home: the Next steps list (the Stack Repairer recap reads it word for word).
- **[assumed]** The Stack Inspector's plain status summary is readable without a connector (CB-583, per the c-stack seat) — the build checks.

## Directive
1. **Write the skill** (Team Builder skill mode, `skills/stack-chief-of-staff/SKILL.md`, draft):
   - **Step 0, tool check:** list which sources this session can reach. Read first what needs no connector (the Stack Inspector's plain summary, if reachable), then connectors. Any source it can't reach is named plainly in one sentence in the read-out ("I couldn't see the night builds today"); reading nothing is never "all fine".
   - **Read** (summaries first): lights (`stack_status`), today's fix log and newest recap marker, last night's builds (`overnight_line`), the shelf, the newest Stack Advisor run, the Punch List, the week's expert receipts and folds, the readers' newest notes, the Next steps list.
   - **Say**, in this order, about a minute: one-line headline; Needs you = the Next steps cards waiting on Charles, in their own words, never re-judged; what happened since he last heard (from the receipt); what's off and who's on it ("nobody" when a watching row points at a draft plan or an unrunnable recheck); long-running known issues once, then just counted. Plain words, no ids, codes, tool names or file names (charter, "Communicate cleanly").
   - **Write** only: one receipt note on Project State project `cbrain`, tag `stack-cos-receipt` (newest note = the "since he last heard" marker), plus a `reported` row in the stack fix log for anything broken with nobody on it.
   - Never fixes, re-runs, emails or changes anything. Never scheduled.
2. **Trigger:** AGENT.md row under Self-maintenance: "what's going on with my stack", "stack status", "Chief of Staff" → `skills/stack-chief-of-staff/SKILL.md`. Add it to the Skills tab wiring.
3. **Test in the build session** (it has every connector): run the skill on live data and save the read-out in the Session Log; run it again with Project State treated as unreachable and check the read-out names the gap. Both read-outs: no ids, under ~200 words.
4. **Duet handoff:** add one open next move on cbrain tagged `da-followup`: "Next Design Assist chat: offer the Stack Chief of Staff as an account skill (one save) so Duet can load it; note what Duet reaches on its first ask in the lanes notebook." This stays with Claude; it is not a card for Charles.

## Acceptance
1. Skill file exists, draft, seven sections, wiring block; AGENT.md row present.
2. Two test read-outs in the Session Log: one full, one naming the missing source.
3. Map dot added.
4. The follow-up next move exists for the next Design Assist chat.

## Decisions
- [Claude-per-doctrine] Needs you is read, never re-judged. Seats: oversight, ai-system-design (two lists would disagree).
- [Claude-per-doctrine] Tool check first; gaps said plainly. Seats: c-stack, lanes, ai-system-design.
- [Claude-per-doctrine] No public endpoint or key in a URL for Duet. Seat: services. Ruled out until a live Duet ask shows it's needed.

## Pasteable prompt
> Build 90 — execute Build Brief BB-2026-11-19-stack-chief-of-staff. Pull the plan from Project State (plan_id 296c7ec6-c195-4f68-b553-f278fee258ee, project cbrain, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-19-stack-chief-of-staff.md. Builds 87, 88 and 89 must have landed. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
