# Build Brief — BB-2026-11-05-experts-every-chat
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-05-experts-every-chat.md`
**Project State plan:** `e6eac3fd-2756-46bd-a150-bbeb0aec768b` on `expert-bench`

**What this is:** Build 70. Experts in every chat: any chat seats the matching expert when Charles asks for judgment in its field, with no phrase to remember.
**Stack Flow:** no dots or lines change (a routing rule, no new running part); `lanes: chat` gains a `helpers:` line.
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build. **After:** none. **Target repo:** Chooch333/agent-library (plus one text edit in Chooch333/cbrain `concepts/stack-map.md`).

**What I'll do (build chat):** make the five text edits below on main, read each back, run the routing tests in step 7, file the Session Log.
**What you'll do:** nothing. Next time you ask a judgment question in any chat, it says which expert it's seating and seats it.

## Asked for — Charles, 2026-11-05 (frozen)
> "I'm in another project asking claude for domain knowledge help. I have an expert for this domain. It didn't use it. Why would it not use it? What trigger do I need."
- 2026-11-05, on the fixes: "So that rule would cause every chat consider engaging an expert" · "That should already be part of the process" (the bench check before a grow) · "Wouldn't the first fix solve for this?" (the FAW wording) · "go this is now a DA chat"

## Current state going in
- **[verified]** AGENT.md fires the Expert Desk only on four message-start phrases (`Expert desk:`, `I need an expert in/for`, `I need a team of experts for`, `CE <expert>:`), and its Disambiguation says a message matching no trigger has no skill. A plain judgment question in a FAW chat therefore loads nothing.
- **[verified]** The only unasked seating rule is design-assist step 6a, which fires only in DA chats.
- **[verified]** AGENT.md's `Expert desk:` row is scoped to "any macro design chat or Design Assist chat".
- **[verified]** AGENT.md's FAW jobs row says general construction/permitting talk "loads nothing". AGENT.md's own tie-break ("prefer the most specific") would let that row win over a general experts rule, so it needs rewording, not just a new rule.
- **[verified]** expert-desk G1's precondition reads "step 2 found no match, *or* Charles said 'I need an expert in <x>'". The roster-builder reads the index and its lens 12 flags duplicates, but only after a helper has started, and its single Proposal output has no "already on the bench" exit (only the team proposal has one).
- **[verified]** FAW claude.ai project chats can start helpers and reach GitHub and Project State (EB-002, EB-053; CE chat notes EB-065/EB-066 on 2026-11-05). The miss is routing, not tools.
- **[verified]** Experts seated in mode B for this brief: skill-authoring and lanes (Brainstorm & Design Assist chat, 2026-11-05). Both found the same cause; lens-notes EB-069 and EB-070 filed. Each seat used about 180–200k helper tokens and 2.5–3.5 minutes.
- **[assumed]** The FAW project's instructions point at AGENT.md (project memory, 2026-10-23). CB-515 once pointed them at job-update only. Another project's instructions can't be read from here.

## Scope
**In:** AGENT.md (new experts rule; Expert Desk row; Disambiguation exception; FAW row wording); skills/expert-desk/SKILL.md (When; G1 checks the bench first); skills/design-assist/SKILL.md (one line in 6a); CHANGELOG.md; cbrain `concepts/stack-map.md` `lanes: chat` helpers line.
**Out:** making every expert answer automatically in build chats, game-maker, job logging or scheduled runs; changing any expert's brief (lens-notes EB-069/EB-070 go in at Sunday's CE fold); splitting the stack-map chat lane in two (no test shows the two differ on helpers); the FAW project's instructions text (Charles's own paste; checked only if a FAW chat still misses after this ships); a claude.ai account skill as a second front door (a second copy to keep true, against the charter's "fewer files").

## Directive
Re-read every file on main before editing it (Build 55 is queued on agent-library; the night runner runs one build per repo at a time, but files may have moved). Each edit: `mcp__Custom_GitHub__get_file_contents` → `create_or_update_file` with the current sha → read back.

1. **AGENT.md — new section** directly after "Every chat, before the first reply":
   > ## Every chat, every message — experts
   >
   > When Charles asks for judgment in a field — how something should be done, what's right, what could go wrong, a review of a plan or a choice — in any chat, on any message, mid-chat included: read `experts/INDEX.md` (the first time; keep its call_when lines in mind for the rest of the chat). If an active expert's call_when matches, say in one line which expert you're seating, then run the Expert Desk (`skills/expert-desk/SKILL.md`) in mode B with that seat, unasked. Two matches: both seats (mode B's limit). This rule applies whether or not a trigger below matches.
   >
   > Don't seat when the chat is carrying out a skill's steps (a build chat, game-maker, job-update logging, a scheduled run), the message asks for a plain fact or a lookup, or that expert already answered this question in this chat. Design Assist chats seat experts through their own step 6a.
   >
   > Needs the Agent tool. A chat without it answers itself and says in one line which expert it couldn't seat.
2. **AGENT.md — Expert Desk row.** Replace "(a message that starts with it, e.g. `Expert desk: <situation or plan link> — goal: <one line> — mode: A`; any macro design chat or Design Assist chat — DA chats also seat experts on their own at their step 6a)" with "(a message that starts with it, e.g. `Expert desk: <situation or plan link> — goal: <one line> — mode: A`, in any chat that can start helpers), or a judgment question that matches an expert's call_when (see \"Every chat, every message — experts\"; DA chats also seat experts at their step 6a)". Leave the other triggers in the row unchanged.
3. **AGENT.md — Disambiguation.** After "A first message that matches no trigger has no skill. Plain conversation, quick questions and other non-build work proceed normally; no default is assumed." add: "The experts rule (\"Every chat, every message — experts\") is the one exception: it applies to every message." **FAW jobs row:** replace "general construction/permitting talk is not a job and loads nothing" with "general construction/permitting talk is not a job and loads no job skill; the experts rule still applies".
4. **skills/expert-desk/SKILL.md** → 0.5.0.
   - When, first sentence: replace "a message starts `Expert desk:` in a macro design chat (Domain Expansion, Stack Advisor, Total Harness) or a Design Assist chat; a Design Assist chat seats experts on its own at its steps 5–6 (design space and traps) whenever the work matches a call_when on the index;" with "a message starts `Expert desk:` in any chat that can start helpers; any chat seats experts on its own, mode B, when Charles asks for judgment that matches a call_when on the index (AGENT.md, \"Every chat, every message — experts\"); a Design Assist chat also does at its steps 5–6 (design space and traps);". Update the header `triggers` first entry the same way.
   - G1 precondition: replace "step 2 found no match, or Charles said \"I need an expert in <x>\"" with "step 2 found no match, or Charles said \"I need an expert in <x>\" and no expert on the index matches <x> by slug, name or call_when". Add to G1's Action, first: "Read `experts/INDEX.md` before starting any helper. If <x> matches an expert on the bench: tell Charles in one line it is already on the bench, and run review mode B with that seat on the chat's question (no question in the chat yet: say how it gets seated, and stop). Grow only when nothing matches."
   - Pitfalls: add "An expert seated only on a typed phrase, while its call_when sits in a file no chat opens until then: a plain question in a FAW chat went unseated, and \"I need an expert in <x>\" for an expert on the bench started a grow. [EB-069; Charles 2026-11-05]"
   - Changelog 0.5.0 line.
5. **skills/design-assist/SKILL.md** → 0.8.3. Step 6a, append: "This is the Design Assist form of AGENT.md's experts rule; DA adds the stack A.1 run and pre-applies the room's path." Changelog line.
6. **CHANGELOG.md** (agent-library): one entry for Build 70 naming the three files. **cbrain `concepts/stack-map.md`**, `lanes:` → `id: chat`, after `reach:` add: `helpers: "Yes — the Agent tool starts helpers on the subscription; seen in claude.ai Project chats (FAW, Brainstorm & Design Assist) 2026-11-03 to 2026-11-05 [EB-002, EB-053, EB-065]; not recorded from the phone app"`. One anchored edit, read back.
7. **Routing test** (helpers in the build chat, one per case, each given only AGENT.md, the charter and experts/INDEX.md from main, told it is a claude.ai FAW project chat with the Agent tool, and asked: "what would you do with this message, and which file would you load?"):
   - a. "What should the owner put in the selection criteria for a progressive design-build job?" → seats design-build-delivery, mode B.
   - b. "How should we price an in-house design group's fees?" → seats ae-practice.
   - c. "What's open on IMI?" → job-update, no expert.
   - d. "New game: squish things to earn coins" → game-maker, no expert.
   - e. "What's the permit fee in Carmel?" → no expert (a lookup).
   - f. "I need an expert in design-build delivery" → says it's on the bench; no roster-builder started.
   Record each answer in the Session Log. A miss: tighten the rule's wording, rerun that case once, then report.

## Acceptance criteria
1. All five edits on main and read back (AGENT.md, expert-desk 0.5.0, design-assist 0.8.3, CHANGELOG, stack-map helpers line).
2. Routing test cases a and b seat the right expert; c, d and e seat none.
3. Case f names the expert on the bench and starts no grow.
4. No other file changed (the commit list for the build is only these files).

## Hard gates
None.

## Cost
$0 money. Usage: each auto-seated question starts one or two helpers on the subscription, about 180–200k helper tokens and 2–4 minutes each (measured 2026-11-05). The don't-seat list keeps it to judgment questions.

## Decisions
- **Reuse each expert's call_when as the trigger; no new phrase** [Claude-per-doctrine] — the line already exists; the charter says reduce what Charles holds.
- **Judgment questions only, never while executing a skill** [Charles 2026-11-05 asked; Claude scoped] — some call_when lines are broad (product-design: "anything Charles reads or clicks") and would fire on every game tweak.
- **Say which expert, then seat** [Claude-per-doctrine] — a seat takes minutes; one line tells Charles why he's waiting.
- **Bench check before grow lives in the desk, not the roster-builder** [Charles: "should already be part of the process"] — the roster-builder's check fires after a helper starts and has no exit; the desk's check costs one file read.
- **FAW row reworded, not left to the new rule** [Charles asked; Claude-per-doctrine] — AGENT.md's "prefer the most specific" tie-break would let the FAW row win.

## Domains (completeness framework)
Goal Answered · Scope Answered · Inputs Answered (verified above) · Tools Answered (GitHub MCP) · Data N-A · Cost Answered · Security N-A · Oversight Defaulted (no new running part; the routing test is the check) · UX Answered (one line before seating) · Rollback Defaulted (revert the commits) · Docs Answered (CHANGELOG, stack-map).

## Out of scope (working)
- The 8 scheduled tasks still pointing at old `roles/` paths (PL-015, breaks 2026-11-14) — separate; fixable in a chat with Charles present.
