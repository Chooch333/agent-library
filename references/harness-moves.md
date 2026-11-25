# Harness moves — the Harness Pathfinder's bench page (0.1.0)

Moves for the Operator at `operators/harness-pathfinder/MANDATE.md`, run by `skills/operator-run/SKILL.md`. A run fetches this page only when its Bench picks one of these moves, and reads only that section. No skill owns the Total Harness plans, the R&D handoffs and the lab files together, so this page sits beside `references/stack-work-moves.md`, whose Rules for every move (matching a chat to its card, paging the chats, five pieces per report, plain words, Inferred day marks) apply here too.

## Rules for every move
- Writes nothing but the run's own log rows. No card, brief, question, decision or lab file is written here.
- A push is the mandate's (Scope). All the briefs and builds of one speed run are one push: name it once.
- Never run, check or restart a workflow, and never open a follow-up build for a check.

## 1 Needs the stack
**For:** an in-scope brief or build that is blocked.
1. Read the plan's blocker and its executor report.
2. Match what it is blocked on against the dots of cbrain `concepts/stack-map.md` (search for the part by name; never read the whole file).
3. A stack part: give Charles one line that opens a Design Assist chat in the Stack Work Project for that change, naming the push it unblocks, so the change lands in the Chief Engineer's scope. Log a `wait`: `why` = the stack change, `ref` = the blocked plan, `clears_when` = `plan <id>: status not blocked`.
4. Not a stack part: say in one line what it waits on. A click only he can make → name the card it sits on; anything else → run `references/stack-work-moves.md` §3 on it.
**Log:** one `move` row; `detail.evidence` = "blocked on a stack part" or "blocked on something else".

## 2 Handoff waiting
**For:** an open R&D handoff question older than 14 days with no plan.
1. Read the question, its thread and the lab report or card it points to (`lab/reports/`, `lab/cards/`).
2. Say in one line what new reach it offers, and whether an open push or an active speed run (`lab/speed-run.md`) wants it now.
3. Recommend one: scope it (the opening line: "next handoff" only when this is the oldest open handoff, otherwise a Design Assist line that names it), or close it. A close is done in a Total Harness chat under AGENT.md's skills: the chat logs a decision and resolves the question with that decision linked, as the kids' explainer handoff was closed on Total Harness.
**Log:** one `move` row; `detail.evidence` = the question's age in days and the recommendation.

## 3 Call it established
**For:** a push with a decision tagged `established` and that push's own tag (`speed-run-<slug>` or its build tag) that still has an open brief or card.
1. Read the decision (his words) and the push's open briefs and cards.
2. Recommend closing each open card and finishing or dropping each open brief, by title; and taking its line off `lab/speed-run.md` if it is there (the chat does that under AGENT.md's skills).
3. Name what sustains it, one of: an expert to grow (the line "I need an expert in <x>"), another Operator (the line "I need an operator for <x>"), or nothing (its own skill already runs it). An expert or Operator already on the bench that covers it is named instead.
4. Once reported, the push leaves the Pathfinder's work: a later run names it only while a brief or card of it is still open, once per report, as "established, loose ends left".
**Log:** one `move` row; `detail.evidence` = the decision's id and how many open items it has.

## Changelog
- 0.1.0 (2026-11-25): first version, written by Team Builder operator mode from draft note CB-800 (Charles confirmed in the chat, TH-305). Seat: operator-design, reports TH-302 and TH-304.
